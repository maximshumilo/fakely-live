import pickle

import numpy as np
import pika
from typing import Optional

from pika.exceptions import UnroutableError, AMQPError

from config import CONFIG
from utils import get_logger


class FrameBuffer:
    _SOURCE_FRAMES_QUEUE = 'source_frames'
    _HANDLED_FRAMES_QUEUE = 'handled_frames'

    def __init__(self, max_size: int = 10):
        self._logger = get_logger(self.__class__.__name__)
        self._max_queue_size = max_size
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self._connect()

    def _connect(self):
        credentials = pika.PlainCredentials(CONFIG.RABBITMQ_USER, CONFIG.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=CONFIG.RABBITMQ_HOST,
            port=CONFIG.RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=0,
            socket_timeout=1,
            blocked_connection_timeout=1
        )
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

        args = {
            "x-max-length": self._max_queue_size,
            "x-overflow": "reject-publish"
        }

        self._channel.queue_declare(
            queue=self._SOURCE_FRAMES_QUEUE,
            arguments=args
        )
        self._channel.queue_declare(
            queue=self._HANDLED_FRAMES_QUEUE,
            arguments=args
        )

    def close(self):
        if self._channel and self._channel.is_open:
            self._channel.close()
        if self._connection and self._connection.is_open:
            self._connection.close()

    def fetch_source_frame(self) -> tuple[np.ndarray, str, str]  | None:
        return self._consume_frame(queue=self._SOURCE_FRAMES_QUEUE)

    def add_handled_frame(self, frame_data: tuple[np.ndarray, str, str]):
        self._publish_frame(frame_data, queue=self._HANDLED_FRAMES_QUEUE)

    def _consume_frame(self, queue: str) -> tuple[np.ndarray, str, str] | None:
        method_frame, header_frame, body = self._channel.basic_get(queue, auto_ack=False)
        if method_frame:
            frame_nd, pts, time_base = pickle.loads(body)
            self._channel.basic_ack(method_frame.delivery_tag)
            return frame_nd, pts, time_base
        return None

    def _publish_frame(self, frame_data: tuple[np.ndarray, str, str], queue: str):
        try:

            body = pickle.dumps(frame_data)
            self._channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(delivery_mode=1)  # non-persistent
            )
        except UnroutableError:
            self._logger.warning(f"Frame dropped — queue '{queue}' is full (unroutable)")
        except AMQPError as e:
            self._logger.error(f"Failed to publish frame to '{queue}': {e}", exc_info=True)


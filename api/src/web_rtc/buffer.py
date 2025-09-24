import pickle
from contextlib import suppress

from aio_pika import (
    Message,
    connect_robust,
)
from aio_pika.abc import (
    AbstractExchange,
    AbstractQueue,
    AbstractRobustChannel,
    AbstractRobustConnection,
)
from aiormq import DeliveryError
from av import VideoFrame

from config import CONFIG
from utils import get_logger


class FrameBuffer:
    """Buffer for video frames using RabbitMQ queues.

    This class handles the buffering of video frames between the source
    (WebRTC) and the processing backend using RabbitMQ queues.
    """

    _SOURCE_FRAMES_QUEUE = "source_frames"
    _HANDLED_FRAMES_QUEUE = "handled_frames"
    _FRAME_CONVERT_FORMAT = "bgr24"

    def __init__(self, max_size: int = 10):
        """Initialize the frame buffer.

        Args:
            max_size: Maximum number of frames to keep in each queue.
        """
        self._logger = get_logger(self.__class__.__name__)
        self._max_queue_size = max_size
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractRobustChannel | None = None
        self._source_queue: AbstractQueue | None = None
        self._handled_queue: AbstractQueue | None = None
        self._exchange: AbstractExchange | None = None

    async def init(self):
        """Initialize the RabbitMQ connection and declare queues.

        This method must be called before using any other methods of this class.
        """
        amqp_url = f"amqp://{CONFIG.RABBITMQ_USER}:{CONFIG.RABBITMQ_PASSWORD}@{CONFIG.RABBITMQ_HOST}:{CONFIG.RABBITMQ_PORT}/"
        self._connection = await connect_robust(
            url=amqp_url,
            timeout=300,
            client_properties={"heartbeat": 60}
        )
        self._channel = await self._connection.channel()

        arguments = {
            "x-max-length": self._max_queue_size,
            "x-overflow": "reject-publish",
        }

        self._source_queue = await self._channel.declare_queue(
            self._SOURCE_FRAMES_QUEUE, arguments=arguments
        )
        self._handled_queue = await self._channel.declare_queue(
            self._HANDLED_FRAMES_QUEUE, arguments=arguments
        )

    async def close(self):
        """Close the RabbitMQ connection and channel."""
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()

    async def add_source_frame(self, frame: VideoFrame):
        """Add a source frame to the source frames queue.

        Args:
            frame: The video frame to add to the source queue.
        """
        await self.add_frame(frame=frame, queue=self._SOURCE_FRAMES_QUEUE)

    async def fetch_handled_frame(self) -> VideoFrame | None:
        """Fetch a handled frame from the handled frames queue.

        Returns
        -------
            The handled video frame, or None if no frame is available.
        """
        return await self._fetch_frame(queue=self._handled_queue)

    async def _fetch_frame(self, queue: AbstractQueue) -> VideoFrame | None:
        """Fetch a frame from the specified queue.

        Args:
            queue: The queue to fetch the frame from.

        Returns
        -------
            The video frame, or None if no frame is available.
        """
        frame = None
        if msg := await queue.get(no_ack=False, fail=False):
            frame = self._convert_to_frame(msg.body)
            await msg.ack()
        return frame

    async def add_frame(self, frame: VideoFrame, queue: str):
        """Add a frame to the specified queue.

        Args:
            frame: The video frame to add.
            queue: The name of the queue to add the frame to.
        """
        if self._channel is None or self._channel.is_closed:
            await self._reconnect()

        data = self._convert_to_frame_data_bytes(frame)
        msg = Message(body=data)

        with suppress(DeliveryError):
            await self._channel.default_exchange.publish(message=msg, routing_key=queue)

    @staticmethod
    def _convert_to_frame_data_bytes(frame: VideoFrame) -> bytes:
        """Convert a video frame to bytes for storage.

        Args:
            frame: The video frame to convert.

        Returns
        -------
            The serialized frame data as bytes.
        """
        frame_data = (frame.to_ndarray(format="bgr24"), frame.pts, frame.time_base)
        return pickle.dumps(frame_data)

    @staticmethod
    def _convert_to_frame(frame_data: bytes) -> VideoFrame:
        """Convert serialized frame data back to a video frame.

        Args:
            frame_data: The serialized frame data.

        Returns
        -------
            The reconstructed video frame.
        """
        frame_nd, pts, time_base = pickle.loads(frame_data)
        frame = VideoFrame.from_ndarray(frame_nd, format="bgr24")
        frame.pts = pts
        frame.time_base = time_base
        return frame

    async def _reconnect(self):
        """Reconnect to RabbitMQ if the connection is lost.

        Raises
        ------
            Exception: If reconnection fails.
        """
        try:
            if self._connection and not self._connection.is_closed:
                await self._connection.close()

            await self.init()
            self._logger.info("Reconnected to RabbitMQ")
        except Exception as e:
            self._logger.error(f"Failed to reconnect to RabbitMQ: {e}")
            raise


buffer = FrameBuffer(max_size=1)

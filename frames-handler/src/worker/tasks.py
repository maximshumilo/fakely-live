import numpy as np
from face_swapper.main import FaceSwapper
from buffer import FrameBuffer


class FrameHandlerTask:
    _FRAME_CONVERT_FORMAT = "bgr24"

    _SOURCE_FRAMES_QUEUE = 'source_frames'
    _HANDLED_FRAMES_QUEUE = 'handled_frames'

    buffer: FrameBuffer = None
    swapper: FaceSwapper = None

    @classmethod
    def run(cls):
        cls.swapper = FaceSwapper()
        cls.buffer = FrameBuffer(max_size=1)
        cls._handle_frames()

    @classmethod
    def _handle_frames(cls):
        while True:
            if not (frame_data := cls.buffer.fetch_source_frame()):
                continue
            handled_frame = cls._handle_frame(frame_nd=frame_data[0])
            cls.buffer.add_handled_frame(frame_data=(handled_frame, frame_data[1], frame_data[2]))


    @classmethod
    def _handle_frame(cls, frame_nd: np.ndarray) -> np.ndarray:
        handled_frame_nd = cls.swapper.swap_face(source_img=frame_nd)
        return handled_frame_nd

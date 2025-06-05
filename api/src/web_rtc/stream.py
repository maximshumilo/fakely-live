import asyncio

from aiortc import VideoStreamTrack
from av import VideoFrame
from av.frame import Frame

from utils import get_logger
from web_rtc.buffer import buffer


logger = get_logger("StreamHandler")


class VideoStream(VideoStreamTrack):
    """Basic video stream track that passes through frames from the source track.

    This class extends aiortc's VideoStreamTrack to provide a simple
    pass-through of video frames from the source track.
    """

    def __init__(self, track):
        """Initialize the video stream with a source track.

        Args:
            track: The source video track to receive frames from.
        """
        super().__init__()
        self.track = track

    async def recv(self) -> Frame:
        """Receive the next frame from the source track.

        Returns
        -------
            The next video frame from the source track.
        """
        return await self.track.recv()


class FaceSwapStream(VideoStream):
    """Specialized video stream track for face swapping.

    This class extends VideoStream to add face swapping functionality.
    It saves source frames to a buffer for processing and retrieves
    processed frames when available.
    """

    def __init__(self, track):
        """Initialize the face swap stream with a source track.

        Args:
            track: The source video track to receive frames from.
        """
        super().__init__(track)
        self.buffer = buffer
        asyncio.create_task(self._save_source_frames())

    async def _save_source_frames(self):
        """Continuously save source frames to the buffer for processing.

        This method runs as a background task to continuously receive
        frames from the source track and add them to the buffer.
        """
        while True:
            frame = await self.track.recv()
            await self.buffer.add_source_frame(frame)

    async def recv(self) -> VideoFrame:
        """Receive the next processed frame or fall back to the source frame.

        Returns
        -------
            The next processed video frame if available, otherwise a source frame.
        """
        if not (frame := await self.buffer.fetch_handled_frame()):
            frame = await self.recv()
        return frame

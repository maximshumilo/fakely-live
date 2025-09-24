from aiortc import (
    RTCConfiguration,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.contrib.media import MediaRelay

from config import CONFIG
from ._host_replace import rewrite_sdp_candidates_for_vpn

from .stream import (
    FaceSwapStream,
    VideoStream,
)


class WebRtc:
    """WebRTC connection manager.

    This class handles WebRTC peer connections, ICE negotiation,
    and video track setup.
    """

    connections: set[RTCPeerConnection] = set()

    def __init__(self):
        """Initialize the WebRTC connection manager with default configuration."""
        self.configuration = RTCConfiguration()

    async def init_connection(self, sdp: str, request_type: str):
        """Initialize a new WebRTC connection.

        Args:
            sdp: Session Description Protocol string.
            request_type: Type of the request (offer, answer, etc.).

        Returns
        -------
            Dictionary containing the SDP and type of the local description.
        """
        session = RTCSessionDescription(sdp=sdp, type=request_type)
        pc = RTCPeerConnection(self.configuration)
        self.connections.add(pc)

        await self._setup_peer_connection(pc=pc, session=session)
        sdp = pc.localDescription.sdp
        pc_type = pc.localDescription.type

        if CONFIG.ICE_CANDIDATE_HOST:
            sdp = rewrite_sdp_candidates_for_vpn(sdp=sdp, new_ip=CONFIG.ICE_CANDIDATE_HOST)

        return {
            "sdp": sdp,
            "type": pc_type
        }

    async def _setup_peer_connection(self, pc: RTCPeerConnection, session: RTCSessionDescription):
        """Set up a peer connection with ICE and track handlers.

        Args:
            pc: The RTCPeerConnection to set up.
            session: The remote session description.
        """
        self._setup_ice(pc=pc)
        self._setup_track_handler(pc=pc)

        await pc.setRemoteDescription(session)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

    def _setup_ice(self, pc: RTCPeerConnection):
        """Set up ICE connection state change handler.

        Args:
            pc: The RTCPeerConnection to set up ICE for.
        """
        def on_ice_change():
            print("ICE state:", pc.iceConnectionState)
            if pc.iceConnectionState in "failed":
                self.connections.discard(pc)

        pc.on("iceconnectionstatechange", on_ice_change)

    def _setup_track_handler(self, pc: RTCPeerConnection) -> None:
        """Set up track handler for incoming media tracks.

        Args:
            pc: The RTCPeerConnection to set up track handling for.
        """
        def on_track(track):
            if track.kind == "video":
                self._update_video_track(pc, track)

        pc.on("track", on_track)

    @staticmethod
    def _update_video_track(pc: RTCPeerConnection, track: VideoStreamTrack):
        """Update video track with appropriate stream handler.

        Args:
            pc: The RTCPeerConnection to add the track to.
            track: The original video track.
        """
        relay = MediaRelay()
        track = relay.subscribe(track)

        stram_cls = FaceSwapStream if CONFIG.ENABLE_HANDLE_STREAM else VideoStream
        new_track = stram_cls(track=track)
        pc.addTrack(track=new_track)

web_rtc = WebRtc()

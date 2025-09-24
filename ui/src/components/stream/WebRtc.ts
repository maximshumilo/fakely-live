import {apiClient} from "../../ApiClient.ts";
import {RefObject} from "react";

interface WebRtcI {
    ref: RefObject<HTMLVideoElement | null>
    stream: MediaStream
}

export const initWebRtcConnection = async (args: WebRtcI) => {
    const config = {
      // iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
    };
    const pc = new RTCPeerConnection(config);

    for (const track of args.stream.getTracks()) {
      pc.addTrack(track, args.stream);
    }

    pc.ontrack = (event) => {
      if (args.ref.current) {
        args.ref.current.srcObject = event.streams[0];
      }
    };

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    const offerData = await apiClient.sendOffer({sdp: offer. sdp,type: offer.type})

    await pc.setRemoteDescription(new RTCSessionDescription(offerData));
    const senders = pc.getSenders();
    senders.forEach((sender) => {
      if (sender.track !== null && sender.track.kind === "video") {
        const parameters = sender.getParameters();
        if (!parameters.encodings) {
          parameters.encodings = [{}];
        }
        parameters.encodings[0].maxBitrate = 999_999_999;
        sender.setParameters(parameters).catch(console.error);
      }
    });
  }
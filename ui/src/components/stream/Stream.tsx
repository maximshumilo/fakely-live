import React, {RefObject, useEffect, useState} from "react";
import "./Stream.css";
import {calculateFps, setStreamToRef} from "../../utils/utils.ts";
import {initWebRtcConnection} from "./WebRtc.ts";

interface StreamProps {
    localStreamState: MediaStream | null;
    videoRef: RefObject<HTMLVideoElement | null>;
    isRecording: boolean;
    isPrepRecord: boolean;
    timeLeft: number;
    beforeRecCounter: number;
}

const Stream: React.FC<StreamProps> = (props) => {
    const [fps, setFps] = useState(0);

    useEffect(() => {
        if (!navigator.mediaDevices || !window.MediaRecorder) {
            new Error('Ваш браузер не поддерживает запись видео');
        }
    }, []);

    useEffect(() => {
        const startWebRTC = async () => {
            if (props.localStreamState !== undefined && props.localStreamState !== null) {
                await initWebRtcConnection({ref: props.videoRef, stream: props.localStreamState});
            }
        }

        setStreamToRef(props.localStreamState, props.videoRef)
        startWebRTC().catch(console.error);
        calculateFps(setFps, props.videoRef)
        console.log('ddd')
    }, [props.localStreamState]);


    return (
        <div className="fake-stream-container">
            <div className={'fake-stream'}>
                <video
                    ref={props.videoRef}
                    autoPlay
                    playsInline
                    className="stream fake"
                />
                <div className={"before-rec-counter"} style={props.isPrepRecord ? {display: 'block'} : {display: 'none'}}>{props.beforeRecCounter}</div>
                <div className="fps-counter">FPS: {fps}</div>
                <div className={'record-wrapper-frame'} style={props.isRecording ? {display: 'block'} : {display: 'none'}}>
                    <div className={'rec-indicator'}>
                        <span className={'dot'}></span>
                        REC
                    </div>
                    <div className="countdown" id="countdown">{props.timeLeft} сек</div>
                </div>
                <div className={'record-wrapper-frame-2'} style={props.isRecording ? {display: 'block'} : {display: 'none'}}>
                </div>
            </div>
        </div>
    );
};

export default Stream;

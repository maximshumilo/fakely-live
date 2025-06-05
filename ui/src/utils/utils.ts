import React, {RefObject, SetStateAction} from "react";
import {HTMLMediaElementWithCaptureStream} from "../customTypes.ts";

export const setStreamToRef = (stream: MediaStream | null, ref: RefObject<HTMLVideoElement | null>) => {
    if (ref.current && stream !== null) {
        ref.current.srcObject = stream;
    }
}

export const calculateFps = (setFpsCallback: React.Dispatch<any>, ref: RefObject<HTMLVideoElement | null>) => {
    let lastTime = performance.now();
    let frames = 0;

    const update = (now: number) => {
        frames += 1;
        const elapsed = now - lastTime;
        if (elapsed >= 1000) {
            setFpsCallback(frames);
            frames = 0;
            lastTime = now;
        }
        if (ref.current?.requestVideoFrameCallback) {
            ref.current.requestVideoFrameCallback(update);
        }
    };

    if (ref.current?.requestVideoFrameCallback) {
        ref.current.requestVideoFrameCallback(update);
    }
}

export const takeScreenshot = (remoteVideoRef: RefObject<HTMLVideoElement | null>) => {
    if (!remoteVideoRef.current) return;

    const video = remoteVideoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);

    const link = document.createElement('a');
    link.download = `deepfake-${new Date().toISOString()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
};


const getStreams = (videoRef: RefObject<HTMLMediaElementWithCaptureStream | null>) => {

    const videoElement = videoRef.current;
    if (!videoElement) {
        alert("Видеоэлемент не найден!");
        throw new Error("Видеоэлемент не найден!");
    }

    const hasSource = videoElement.src || videoElement.srcObject;
    if (!hasSource) {
        alert("Видео не воспроизводится — запись невозможна!");
        throw new Error("Видео не воспроизводится — запись невозможна!");
    }

    let originalStream;

    if (typeof videoElement.captureStream === 'function') {
        originalStream = videoElement.captureStream();
    } else if (videoElement.srcObject instanceof MediaStream) {
        originalStream = videoElement.srcObject;
    } else {
        alert("Ваш браузер не поддерживает запись видео из этого элемента!");
        throw new Error("Ваш браузер не поддерживает запись видео из этого элемента!");
    }

    const stream = new MediaStream();
    originalStream.getTracks().forEach((track: { clone: () => MediaStreamTrack; }) => {
        stream.addTrack(track.clone());
    });

    return [stream, originalStream];

}


interface getMediaRecorderParams {
    originalStream: any
    stream: MediaStream
    chunks: BlobPart[]
    videoRef: RefObject<HTMLMediaElementWithCaptureStream|null>
}


const getMediaRecorder = (params: getMediaRecorderParams): MediaRecorder => {
    const mediaRecorder = new MediaRecorder(params.stream, {mimeType: 'video/webm'});
    mediaRecorder.ondataavailable = (event) => pushToChunks(event, params.chunks)
    mediaRecorder.onstop = () => downloadVideo({
        chunks: params.chunks,
        originalStream: params.originalStream,
        videoRef: params.videoRef
    });
    return mediaRecorder;
}

const pushToChunks = (event: BlobEvent, chunks: BlobPart[]) => {
    if (event.data.size > 0) {
        chunks.push(event.data);
    }
}

interface downloadVideoParams {
    chunks: BlobPart[]
    originalStream: any
    videoRef: RefObject<HTMLMediaElementWithCaptureStream|null>
}


const downloadVideo = (params: downloadVideoParams) => {
    const blob = new Blob(params.chunks, {type: 'video/webm'});
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `recorded-video-${new Date().toISOString()}.webm`;
    a.click();

    URL.revokeObjectURL(url);

    if (params.videoRef.current) {
        params.videoRef.current.srcObject = params.originalStream;
        params.videoRef.current.play().catch(e => console.error("Ошибка воспроизведения:", e));
    }
    }

interface recordVideoParams {
    videoRef: RefObject<HTMLMediaElementWithCaptureStream | null>
    setIsRecording: React.Dispatch<SetStateAction<boolean>>
    setTimeLeft: React.Dispatch<SetStateAction<number>>
}


export const recordVideo = async (params: recordVideoParams) => {
    params.setIsRecording(true);
    const chunks: BlobPart[] = [];

    try {
        const [stream, originalStream] = getStreams(params.videoRef)
        const mediaRecorder = getMediaRecorder({
            chunks: chunks,
            originalStream: originalStream,
            videoRef: params.videoRef,
            stream: stream
        })

        mediaRecorder.start();

        let count = 10;
        params.setTimeLeft(count);

        const countdownInterval = setInterval(() => {
          count -= 1;
          params.setTimeLeft(count);
          if (count <= 0) clearInterval(countdownInterval);
        }, 1000);

        setTimeout(() => {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                params.setIsRecording(false);
            }
        }, 10000);

        console.log('Recording started for 10 seconds...');
    } catch (error) {
        console.error('Error recording video:', error);
        params.setIsRecording(false);
    }
};
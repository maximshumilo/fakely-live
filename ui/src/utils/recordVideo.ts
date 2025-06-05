import {RefObject} from "react";
import {apiClient} from "../ApiClient.ts";

interface recordVideoParams {
    canvasRef: RefObject<HTMLCanvasElement | null>;
    setIsRecording: React.Dispatch<React.SetStateAction<boolean>>;
    setTimeLeft: React.Dispatch<React.SetStateAction<number>>;
}

export const recordVideo = async (params: recordVideoParams) => {
    const {canvasRef, setIsRecording, setTimeLeft} = params;
    const canvas = canvasRef.current;
    if (!canvas) {
        console.error("Canvas not found.");
        return;
    }

    const stream = canvas.captureStream(30);
    const chunks: BlobPart[] = [];
    setIsRecording(true);

    const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'video/webm;codecs=vp8',
    });

    mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
            chunks.push(e.data);
        }
    };

    mediaRecorder.start();

    let count = 10;
    setTimeLeft(count);
    const countdownInterval = setInterval(() => {
        count -= 1;
        setTimeLeft(count);
        if (count <= 0) clearInterval(countdownInterval);
    }, 1000);

    setTimeout(async () => {
        mediaRecorder.stop();

        mediaRecorder.onstop = async () => {
            let blob = new Blob(chunks, {type: 'video/webm'});
            blob = await apiClient.convertToMp4(blob);
            console.log('Converted to ', blob.type);

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `recorded-${new Date().toISOString()}.mp4`;
            a.click();
            URL.revokeObjectURL(url);

            setIsRecording(false);
        };
    }, 10000);
};

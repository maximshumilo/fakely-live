import {useEffect, useRef, useState} from "react";
import Stream from "./components/stream/Stream.tsx";
import Masks from "./components/masks/Masks.tsx";
import "./App.css";
import Logo from "./components/logo/logo.tsx";
import ButtonBlock from "./components/button-block/ButtonBlock.tsx";
import {HTMLMediaElementWithCaptureStream} from "./customTypes.ts";
import DisappearingPanel from "./components/panel/Panel.tsx";

interface Mask {
    name: string;
    file_urn: string;
}

function App() {
    const [selectedMask, setSelectedMask] = useState<Mask | null>(null);
    const [localStream, setLocalStream] = useState<MediaStream | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [isAgreed, setIsAgreed] = useState(false);
    const [isPrepRecord, setIsPrepRecord] = useState(false);
    const [beforeRecCounter, setBeforeRecCounter] = useState(0);
    const [timeLeft, setTimeLeft] = useState(10);

    const remoteVideoRef = useRef<HTMLMediaElementWithCaptureStream>(null);

    const handleFaceSelection = (mask: Mask | null) => {
        setSelectedMask(mask);
        console.debug('Set selected mask', mask);
    };

    useEffect(() => {
        const getLocalStream = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    frameRate: 25,
                    width: 1280,
                    height: 720,
                },
                audio: false,
            });
            setLocalStream(stream);
        }
        getLocalStream().catch(console.error);
    }, []);

    const mainClass = isAgreed ? "main-content" : "main-content background-blur";

    return (
        <div className="body">
            <DisappearingPanel isAgreed={isAgreed} setIsAgreed={setIsAgreed}/>
            <div className={mainClass}>
                <div className={'logo'}>
                    <Logo/>
                </div>
                <Stream
                    localStreamState={localStream}
                    videoRef={remoteVideoRef}
                    isRecording={isRecording}
                    timeLeft={timeLeft}
                    beforeRecCounter={beforeRecCounter}
                    isPrepRecord={isPrepRecord}
                />
                <div className={'button-block'}>
                    <ButtonBlock
                        isRecording={isRecording}
                        setIsRecording={setIsRecording}
                        videoRef={remoteVideoRef}
                        setTimeLeft={setTimeLeft}
                        setBeforeRecCounter={setBeforeRecCounter}
                        isPrepRecord={isPrepRecord}
                        setIsPrepRecord={setIsPrepRecord}
                    />
                </div>
                <div className={'mask-items'}>
                    <Masks
                        selectedMaskState={selectedMask}
                        onSelectMask={handleFaceSelection}
                        localStreamState={localStream}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;


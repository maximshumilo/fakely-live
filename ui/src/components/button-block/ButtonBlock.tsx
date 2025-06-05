import {recordVideo, takeScreenshot} from "../../utils/utils.ts";
import React, {RefObject, SetStateAction} from "react";
import "./ButtonBlock.css"
import {HTMLMediaElementWithCaptureStream} from "../../customTypes.ts";

interface ButtonBlockProps {
    videoRef: RefObject<HTMLMediaElementWithCaptureStream | null>;
    isRecording: boolean;
    setIsRecording: React.Dispatch<SetStateAction<boolean>>
    setTimeLeft: React.Dispatch<SetStateAction<number>>
    setBeforeRecCounter: React.Dispatch<SetStateAction<number>>
    isPrepRecord: boolean
    setIsPrepRecord: React.Dispatch<SetStateAction<boolean>>
}


const ButtonBlock: React.FC<ButtonBlockProps> = (props) => {

    const onClickRecording = async () => {
        props.setBeforeRecCounter(3);
        props.setIsPrepRecord(true);

        const prepInterval = setInterval(() => {
            props.setBeforeRecCounter(prev => {
                if (prev === 1) {
                    clearInterval(prepInterval);
                    props.setIsPrepRecord(false);
                    recordVideo(props)
                    console.debug('Record clicked');
                }
                return prev - 1;
            });
        }, 1000);

    }

    const getRecordButtonText = () => {
      if (props.isPrepRecord) {
        return "Подготовка к записи ...";
      } else if (props.isRecording) {
        return "Идет запись ...";
      } else {
        return "Записать видео";
      }
    };


    return (
        <div className={'button-block-main'}>
            <button className={''} onClick={() => takeScreenshot(props.videoRef)}>
                Сделать скриншот
            </button>
            <button onClick={onClickRecording} disabled={props.isRecording}>
                {getRecordButtonText()}
            </button>
        </div>
    )
}

export default ButtonBlock;
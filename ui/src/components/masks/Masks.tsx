import React, {useEffect, useRef, useState} from "react";
import "./Masks.css"
import {apiClient, MaskInfo} from "../../ApiClient.ts";
import {config} from "../../config.ts";
import {setStreamToRef} from "../../utils/utils.ts";

interface MaskProps {
    maskData: MaskInfo | null;
    selectedMaskState: MaskInfo | null;
    onSelectMask: (mask: MaskInfo | null) => void;
}

const Mask: React.FC<MaskProps> = ({maskData, selectedMaskState, onSelectMask}) => {
    const onClick = async () => {
        try {
          await apiClient.setMask(maskData ? maskData.name : null);
          onSelectMask(maskData);

        } catch (error) {
          console.error("Ошибка при выборе маски:", error);
        }
    }

    const imgUrl = maskData ? `${config.baseUrl}${maskData.file_urn}` : "/no_mask.jpg";
    const isSelected = () => {
        if (selectedMaskState === null && maskData == null) {
            return true
        } else {
            return selectedMaskState?.name === maskData?.name;
        }
    }

    return (
        <div
            className={`face-option ${isSelected() ? "selected" : ""}`}
            onClick={onClick}
        >
            <img
                src={imgUrl}
                alt={`mask ${maskData ? maskData.name : 'no_mask'}`}
                className="face-thumb"
            />
        </div>
    )
}

interface SidebarProps {
    selectedMaskState: MaskInfo | null;
    onSelectMask: (mask: MaskInfo | null) => void;
    localStreamState: MediaStream | null;
}

const Masks: React.FC<SidebarProps> = ({selectedMaskState, onSelectMask, localStreamState}) => {
    const [masks, setMasks] = useState<MaskInfo[]>([]);
    const localVideoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        const getMasksUrn = async () => {
            try {
                const masksData = await apiClient.getMasks();
                setMasks(masksData.items);
            } catch (error) {
                console.error("Failed to fetch masks:", error);
            }
        };

        const setNoMask = async () => {
            try {
                await apiClient.setMask(null);
                onSelectMask(null);
            } catch (error) {
                console.error("Failed to fetch masks:", error);
            }
        };

        setStreamToRef(localStreamState, localVideoRef)
        setNoMask().catch(console.error);
        getMasksUrn().catch(console.error);
    }, [localStreamState]);

    return (
        <div className="items">
                <Mask
                key={'no_mask'}
                maskData={null}
                selectedMaskState={selectedMaskState}
                onSelectMask={onSelectMask}
                />
                {masks.length > 0 ? (
                    masks.map((mask) => (
                        <Mask
                            key={mask.name}
                            maskData={mask}
                            selectedMaskState={selectedMaskState}
                            onSelectMask={onSelectMask}
                        />
                    ))
                ) : (
                    <p>Загрузка масок...</p>
                )}
        </div>
    );
};

export default Masks;
import React, {SetStateAction} from 'react';
import "./Panel.css"
import Offer from "../offer/Offer.tsx";

interface PanelProps {
    isAgreed: boolean;
    setIsAgreed: React.Dispatch<SetStateAction<boolean>>;
}

function DisappearingPanel(props: PanelProps) {
    const extraStyles = props.isAgreed ? {display: 'none'} : undefined;

    return (
        <div className='panel' style={extraStyles}>
            <Offer/>

            <div className={'control'}>
                <button onClick={() => props.setIsAgreed(true)}>Принять</button>
            </div>
        </div>
    );
}

export default DisappearingPanel;
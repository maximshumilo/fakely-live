// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogoHeader from './svg/headerLogo.svg?react';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogoVisionLabs from './svg/VisionLabs.svg?react';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogoUBS from './svg/EBS.svg?react';
import "./logo.css"

const Logo = () => {
    return (
        <>
            <LogoHeader />
            <div className={'partners'}>
                <LogoUBS />
                <LogoVisionLabs />
            </div>
        </>
    )
}

export default Logo;
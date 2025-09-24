// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogoVisionLabs from './svg/VisionLabs.svg?react';
import "./logo.css"

const Logo = () => {
    return (
        <>
            <LogoVisionLabs />
        </>
    )
}

export default Logo;
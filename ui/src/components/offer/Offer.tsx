import html from './offer.html?raw';
import "./Offer.css"


const Offer = () => {
    return (
        <div className={"offer-container"}>
            <div dangerouslySetInnerHTML={{ __html: html }} />
        </div>
    )
}

export default Offer;
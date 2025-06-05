import {config} from "./config.ts";

export interface OfferRequest {
    sdp?: string;
    type: RTCSdpType;
}

export interface OfferResponse {
    sdp: string;
    type: RTCSdpType;
}

export interface MaskInfo {
    name: string;
    file_urn: string;
}

export interface GetMasksResponse {
    items: MaskInfo[];
}

export interface SetMaskResponse {
    status: string;
    name: string;
}

export class ApiClient {
    private readonly baseUrl: string;

    constructor() {
        this.baseUrl = config.baseUrl;
    }

    public async sendOffer(offer: OfferRequest): Promise<OfferResponse> {
        const response = await fetch(`${this.baseUrl}/api/offer`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(offer),
        });

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        return response.json();
    }

    public async getMasks(): Promise<GetMasksResponse> {
        const response = await fetch(`${this.baseUrl}/api/masks`, {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        });

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        return response.json();
    }

    public async setMask(name: string | null): Promise<SetMaskResponse> {
        const response = await fetch(`${this.baseUrl}/api/masks`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: name}),
        });

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        return response.json();
    }

    public async convertToMp4(webmBlob: Blob): Promise<Blob> {
        const formData = new FormData();
        formData.append('file', webmBlob, 'video.webm');

        const response = await fetch(`${this.baseUrl}/api/converter`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        return await response.blob();
    }
}

export const apiClient: ApiClient = new ApiClient();
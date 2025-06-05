from contextlib import asynccontextmanager
from enum import StrEnum

from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from config import CONFIG
from mask import face_mask
from web_rtc import web_rtc
from web_rtc.buffer import buffer


STATIC_URN = "/static"
STATIC_FACES_URN = f"{STATIC_URN}/faces"

@asynccontextmanager
async def lifespan(*_, **__):
    """Initialize required components during application startup.

    This context manager initializes the frame buffer and face mask
    when the application starts.
    """
    await buffer.init()
    await face_mask.init()
    yield

app = FastAPI(lifespan=lifespan)
app.mount(STATIC_FACES_URN, StaticFiles(directory="faces"), name="faces")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WebRtcConnectionType(StrEnum):
    """Enum for WebRTC connection types."""

    ANSWER = "answer"
    OFFER = "offer"
    PRANSWER = "pranswer"
    ROLLBACK = "rollback"


class PayloadOffer(BaseModel):
    """Model for WebRTC connection offer payload."""

    sdp: str
    type: WebRtcConnectionType


class PayloadSetMask(BaseModel):
    """Model for setting a face mask payload."""

    name: str | None = None

@app.post("/api/offer")
async def activate_connection(payload: PayloadOffer):
    """Activate a WebRTC connection.

    Args:
        payload: The WebRTC connection offer payload.

    Returns
    -------
        JSON response with WebRTC connection information.
    """
    rtc_info = await web_rtc.init_connection(
        sdp=payload.sdp,
        request_type=payload.type
    )
    return JSONResponse(content=rtc_info)

@app.get("/api/masks")
async def get_all_mask_names():
    """Get all available face mask names.

    Returns
    -------
        JSON response with a list of available face masks.
    """
    names = [
        {
            "name": file.name.removesuffix(file.suffix),
            "file_urn": f"{STATIC_FACES_URN}/{file.name}",
        }
        for file in CONFIG.FACES_PATH.iterdir() if file.is_file()
    ]
    return JSONResponse(content={"items": names})

@app.post("/api/masks")
async def set_mask(payload: PayloadSetMask):
    """Set the active face mask.

    Args:
        payload: The payload containing the mask name to set.

    Returns
    -------
        JSON response indicating success and the set mask name.

    Raises
    ------
        HTTPException: If the specified mask name is not found.
    """
    if payload.name is None:
        face_path = None
    else:
        try:
            face_path = next(
                filter(
                    lambda f: f.name.removesuffix(f.suffix) == payload.name,
                    CONFIG.FACES_PATH.iterdir()
                )
            )
        except StopIteration:
            raise HTTPException(status_code=404, detail=f"Could not found mask by name: {payload.name}") from None

    await face_mask.update(image_path=face_path)
    return JSONResponse(content={"status": "success", "mask": payload.name})


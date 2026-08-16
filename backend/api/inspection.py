from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from backend.services.detector import detect_image
from backend.services.video_processor import process_video


router = APIRouter(
    prefix="/inspect",
    tags=["Inspection"]
)


@router.post("/image")
async def inspect_image(
    file: UploadFile = File(...)
):
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File type not detected."
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    return detect_image(
        image_bytes=image_bytes
    )


@router.post("/video")
async def inspect_video(
    file: UploadFile = File(...)
):
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File type not detected."
        )

    if not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a video."
        )

    video_bytes = await file.read()

    if not video_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded video is empty."
        )

    return process_video(
        video_bytes=video_bytes,
        filename=file.filename or "inspection.mp4"
    )
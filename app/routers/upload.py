from beanie import PydanticObjectId
from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
import cloudinary
import cloudinary.uploader
import cloudinary.api

import os



from ..settings import settings
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ..utils.response import CustomResponse


router = APIRouter(tags=["upload"])

cloudinary.config(
    cloud_name=settings.CLOUDINARY.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY.CLOUDINARY_API_SECRET,
    secure=True,
)


class CloudinaryUploadResponse(BaseModel):
    asset_id: str
    public_id: str
    version: int
    version_id: Optional[str]
    signature: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    resource_type: str
    created_at: datetime
    tags: List[str]
    bytes: int
    type: str
    etag: str
    placeholder: bool
    url: str
    secure_url: str
    folder: Optional[str]
    original_filename: str
    api_key: str


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_name = str(uuid4())

    folder_name = "farm_riders"

    public_id = f"{folder_name}/{file_name}"

    # store reference to file in database, for deletion later

    response = cloudinary.uploader.upload(file.file, folder=folder_name, resource_type="auto", public_id=public_id)

    metadata = CloudinaryUploadResponse(**response)

    result = {"url": metadata.secure_url, "public_id": metadata.public_id}

    return CustomResponse(message="File uploaded successfully", data=result)

    # return await UploadService.upload_file(file, file_name)




from fastapi import APIRouter,  UploadFile, File


from ..services.upload import UploadService


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), file_name: str = ""):
    return await UploadService.upload_file(file, file_name)   
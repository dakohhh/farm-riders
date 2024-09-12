from fastapi import UploadFile
from ..libraries.upload import FarmRidersUpload


class UploadService:

    @staticmethod
    async def upload_file(file: UploadFile, file_name: str) -> dict:

        print(file_name)
        uploader = FarmRidersUpload(file_name)

        return uploader.handle_upload(file)

from beanie import PydanticObjectId
from fastapi import APIRouter, UploadFile, File, Request
from ..utils.response import CustomResponse
from ..services.vehicle import VehicleService
from typing import Dict, Any, Union
from pydantic import BaseModel



class SuccessResponse(BaseModel):
    message: str
    data: Union[Dict[str, Any], Any]  


class ErrorResponse(BaseModel):
    message: str


router = APIRouter(tags=["Vehicles"], prefix="/vehicles")

@router.get("/",  responses={
    200: {"model": SuccessResponse, "description": "Successful response"},
    400: {"model": ErrorResponse, "description": "Error occurred"},
})
async def get_all_vehicles(request: Request):

    result = await VehicleService.get_all_vehicles()

    # context = {"vehicles": result.vehicles}

    return SuccessResponse(message="Vehicles fetched successfully", data=result)




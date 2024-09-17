from beanie import PydanticObjectId
from fastapi import APIRouter, UploadFile, File, Request
from ..utils.response import CustomResponse
from ..services.vehicle import VehicleService
from ..services.rentals import RentalService
from typing import Dict, Any, Union
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    message: str
    data: Union[Dict[str, Any], Any]


class ErrorResponse(BaseModel):
    message: str


router = APIRouter(tags=["Rentals"], prefix="/rentals")


@router.get(
    "/",
    responses={
        200: {"model": SuccessResponse, "description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Error occurred"},
    },
)
async def get_all_farm_rider_rentals(request: Request):

    result = await RentalService.get_all_rentals()

    # context = {"vehicles": result.vehicles}

    return SuccessResponse(message="Farm Riders Rentals fetched successfully", data=result)

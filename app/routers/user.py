from fastapi import APIRouter, Depends, Request

from app.utils.helper_functions import find_nearest_drivers
from ..services.user import UserService

from ..utils.response import CustomResponse
from ..enums.user import UserRoles
from ..middleware.auth import Auth
from ..models.user import User
from ..models.ride import RideRequest
from ..schema.user import UserProfile, DriverProfile
from ..schema.ride import RideRequestIn
from ..libraries.socket import socket_database

router = APIRouter(prefix="/user", tags=["Vendor"])


@router.patch("/profile")
async def update_farmer_and_aggregator_profile(
    update_profile: UserProfile, user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator]))
):
    await UserService.update_farmer_and_aggregator_profile(update_profile, user)

    return CustomResponse("Profile updated successfully")


@router.patch("/driver/profile")
async def update_driver_profile(update_profile: DriverProfile, user: User = Depends(Auth(UserRoles.driver))):

    await UserService.update_driver_profile(update_profile, user)

    return CustomResponse("Profile updated successfully")


from enum import Enum
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import Optional


class Location(BaseModel):
    latitude: float
    longitude: float


class DriverRequestStatus(Enum):
    pending = "pending"
    assigned = "assigned"
    completed = "completed"
    cancelled = "cancelled"


class DriverRequest(BaseModel):
    pickup_location: Location
    dropoff_location: Location
    driver_id: PydanticObjectId  # Assigned driver
    status: DriverRequestStatus  # pending, assigned, completed, cancelled
    cost: Optional[float] = None  # Trip cost estimate


@router.post("/request/driver")
async def request_driver(
    request: Request,
    ride_request_in: RideRequestIn,
    user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator])),
):
    from pprint import pprint

    ride_request_dict = ride_request_in.model_dump()

    ride_request_dict.update({'user': user})

    ride_request = RideRequest(**ride_request_dict)

    # ride_request.save()

    pickup_location = Location(
        latitude=ride_request.pickup_location.latitude, longitude=ride_request.pickup_location.longitude
    )

    drivers = find_nearest_drivers(pickup_location, socket_database)

    print(drivers)

    # Get available drivers within the location

    # Find available drivers  withing the location

    return CustomResponse("Request Driver")

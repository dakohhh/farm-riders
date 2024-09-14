from fastapi import APIRouter, Depends, Request

from app.utils.helper_functions import find_nearest_drivers, normalize_phone_number
from ..services.user import UserService

from ..utils.response import CustomResponse
from ..enums.user import UserRoles
from ..middleware.auth import Auth
from ..models.user import User
from ..models.ride import RideRequest
from ..schema.user import UserProfile, DriverProfile
from ..schema.ride import OrderTruck
from ..libraries.socket import socket_database

router = APIRouter(prefix="/user", tags=["Vendor"])



@router.get("/")
async def get_user(
    request:Request, user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator]))
):
    
    result = await UserService.get_user(user)

    return CustomResponse("Get user successful", data=result)


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




@router.post("/order_truck")
async def order_truck(
    request: Request,
    order_truck: OrderTruck,
    user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator])),
):

    order_truck_dict = order_truck.model_dump(exclude={"max_distance_km"})

    order_truck_dict.update({'user': user})

    order_truck = RideRequest(**order_truck_dict)

    order_truck.save()

    pickup_location = Location(
        latitude=order_truck.pickup_location.latitude, longitude=order_truck.pickup_location.longitude
    )

    nearest_drivers = find_nearest_drivers(pickup_location, socket_database, max_distance_km=order_truck.max_distance_km)

    if not nearest_drivers:
        return CustomResponse("No available drivers, try again with a larger max distance radius", status=404)
    
    
    # order_truck.delete()

    drivers = []
    
    for driver in nearest_drivers:
        _driver_dict = driver[0].model_dump()

        _driver_dict['user'] =  _driver_dict['user'].to_mongo()

        _driver_dict['user']['_id'] = str(_driver_dict['user']['_id'])

        _driver_dict['user']['phone_number'] = normalize_phone_number(_driver_dict['user']['phone_number'])

        _driver_dict['user'].pop('password', None)
        _driver_dict['user'].pop('balance', None)
        
        drivers.append(_driver_dict)

    # Get available drivers within the location

    # Find available drivers  withing the location

    result = {"order_truck_id": str(order_truck.id), "drivers": drivers}

    return CustomResponse("Request Driver", data=result)

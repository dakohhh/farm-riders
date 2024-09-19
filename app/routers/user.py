from fastapi import APIRouter, Depends, Request
from enum import Enum

from ..clients import PaystackClient, CheckoutParams
from app.utils.helper_functions import find_nearest_drivers, normalize_phone_number
from ..services.user import UserService

from ..utils.response import CustomResponse
from ..utils.exceptions import NotFoundException, BadRequestException
from ..enums.user import UserRoles
from ..middleware.auth import Auth
from ..models.user import User
from ..models.profile import Profile, DriverProfile
from ..models.order_truck import OrderTruckRequest
from ..models.vehicle import Vehicle
from ..models.rental import Rentals, RentalRequest
from ..schema.user import UserProfileIn, DriverProfileIn, DriverProfileOut
from ..schema.vehicle import VehicleOut
from ..schema.order_truck import OrderTruckIn, Location, OrderTruckOut
from ..schema.rentals import RentalsOut, ListRentalsOut, RequestRentalsIn, RequestRentalsOut

from ..libraries.socket import socket_database

router = APIRouter(prefix="/user", tags=["Vendor"])


@router.get("/")
async def get_user(request: Request, user: User = Depends(Auth())):

    result = await UserService.get_user(user)

    return CustomResponse("Get user successful", data=result)


@router.patch("/profile")
async def update_farmer_and_aggregator_profile(
    update_profile: UserProfileIn, user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator]))
):
    await UserService.update_farmer_and_aggregator_profile(update_profile, user)

    return CustomResponse("Profile updated successfully")


@router.patch("/driver/profile")
async def update_driver_profile(update_profile: DriverProfileIn, user: User = Depends(Auth(UserRoles.driver))):

    await UserService.update_driver_profile(update_profile, user)

    return CustomResponse("Profile updated successfully")


class DriverRequestStatus(Enum):
    pending = "pending"
    assigned = "assigned"
    completed = "completed"
    cancelled = "cancelled"


@router.post("/nearest_drivers")
async def get_nearest_driver(
    request: Request,
    pickup_location: Location,
    max_distance_km: float = 10.0,
    user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator])),
):

    nearest_drivers = find_nearest_drivers(pickup_location, socket_database, max_distance_km=max_distance_km)

    if not nearest_drivers:
        raise NotFoundException("No available drivers, try again with a larger max distance radius")

    drivers = []

    for driver in nearest_drivers:
        driver_dict = driver[0].model_dump()

        driver_dict['user'] = driver_dict['user'].to_mongo()

        driver_profile = (
            DriverProfile.objects.filter(user=driver_dict['user']['_id'])
            .only('firstname', 'lastname', 'vehicle_info')
            .as_pymongo()
            .first()
        )

        if not driver_profile:
            continue

        driver_profile = DriverProfileOut(**driver_profile)

        vehicle = Vehicle.objects.filter(id=driver_profile.vehicle_info.vehicle).as_pymongo().first()

        if not vehicle:
            continue

        vehicle = VehicleOut(**vehicle)

        driver_profile = driver_profile.model_dump(exclude_unset=True)

        driver_profile['vehicle_info']['vehicle'] = vehicle.model_dump(exclude_unset=True)

        driver_dict['user']['id'] = str(driver_dict['user']['_id'])

        driver_dict['user']['phone_number'] = normalize_phone_number(driver_dict['user']['phone_number'])

        driver_dict['user']['profile'] = driver_profile

        driver_dict['user'].pop('_id', None)
        driver_dict['user'].pop('password', None)
        driver_dict['user'].pop('balance', None)

        drivers.append(driver_dict)

    result = {"drivers": drivers}

    return CustomResponse("Nearest Drivers", data=result)


@router.post("/order_truck")
async def order_truck(
    request: Request, order_truck: OrderTruckIn, user: User = Depends(Auth([UserRoles.farmers, UserRoles.aggregator]))
):

    order_truck.driver

    # Check if the driver exists

    driver = User.objects.filter(id=order_truck.driver).first()

    if not driver:
        raise BadRequestException("Driver does not exists")

    order_truck_dict = order_truck.model_dump(exclude={'driver'})

    order_truck_dict.update({'user': user})

    order_truck_request = OrderTruckRequest(**order_truck_dict)

    order_truck_request.save()

    order_truck_out = OrderTruckOut(**order_truck_request.to_mongo().to_dict())

    result = order_truck_out.model_dump(exclude_unset=True)

    return CustomResponse("Request Driver", data=result)


@router.post("/rental/request")
async def rental_service(request: Request, rental: RequestRentalsIn, user: User = Depends(Auth())):

    rental: Rentals | None = Rentals.objects.filter(id=rental.rental).first()

    if not rental:
        raise NotFoundException("rental service not found")

    additional_fees = 0.00

    total_price = float(rental.price) + additional_fees

    rental_request: RentalRequest = RentalRequest.objects.create(rental=rental, total_price=total_price)

    result = RequestRentalsOut(**rental_request.to_mongo())

    metadata = {'type': 'rental_request', 'rental_request_id': str(result.id), 'user_id': str(user.id)}


    params = CheckoutParams(email=user.email, amount=int(rental_request.total_price), metadata=metadata)

    response = await PaystackClient().APIPaystackCheckoutURL(params)

    result = {'rental_request': result.model_dump(), 'checkout_url': response.data["authorization_url"]}

    return CustomResponse("rental services", data=result)

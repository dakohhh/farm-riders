from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, EmailStr, Field, constr, model_validator
from typing import List, Optional

from ..enums.user import UserGender


class User(BaseModel):
    password: str
    email: EmailStr
    phone_number: str
    role: str


class UserProfileDocument(BaseModel):
    selfie_photo: HttpUrl = Field(None, example="https://example.com/selfie.jpg")
    nin_photo: Optional[HttpUrl] = Field(None, example="https://example.com/nin.jpg")
    drivers_license_phone: Optional[HttpUrl] = Field(None, example="https://example.com/drivers_license.jpg")

    @model_validator(mode='after')
    def check_nin_or_drivers_license(self):
        nin_photo, drivers_license_phone = self.nin_photo, self.drivers_license_phone
        if not nin_photo and not drivers_license_phone:
            raise ValueError('Either nin photo or drivers license phone must be provided')
        return self


class VehicleInfo(BaseModel):
    plate_number: str
    vehicle_year: int
    manufacturer_model: str
    vehicle_color: str
    proof_of_ownership: HttpUrl  # Proof of vehicle ownership


class UserProfile(BaseModel):
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    gender : UserGender = Field(..., example=UserGender.male.value)
    nin: Optional[str] = Field(None, example="12345678901")
    drivers_license_number: Optional[constr(min_length=20, max_length=20)] = Field(None, example="12345678901234567890")  # type: ignore
    documents: UserProfileDocument


class DriverProfile(UserProfile):
    vehicle_info: VehicleInfo
    has_vehicle: bool
    not_driving_self: bool

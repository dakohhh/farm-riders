from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, EmailStr, Field, constr, model_validator
from typing import List, Optional

from ..enums.user import UserGender


class User(BaseModel):
    password: str
    email: EmailStr
    phone_number: str
    role: str

class UserOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    

    


class UserProfileDocument(BaseModel):
    selfie_photo: Optional[HttpUrl] = Field(None, example="https://example.com/selfie.jpg")
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
    vehicle: Optional[PydanticObjectId] = None
    vehicle_color: str
    proof_of_ownership: Optional[HttpUrl] = Field(
        None, example="https://example.com/proof_of_ownwership.jpg"
    )  # Proof of vehicle ownership


class UserProfileIn(BaseModel):
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    gender: UserGender = Field(..., example=UserGender.male.value)
    nin: Optional[str] = Field(None, example="12345678901")
    drivers_license_number: Optional[str] = Field(None, example="12345678901234567890")  # type: ignore
    documents: UserProfileDocument



class DriverProfileIn(UserProfileIn):
    vehicle_info: VehicleInfo
    has_vehicle: bool
    not_driving_self: bool


class UserProfileOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    firstname: Optional[str] = None
    lastname: Optional[str] = Field(None)
    gender: Optional[UserGender] = None


class VehicleInfoOut(BaseModel):
    plate_number: Optional[str]
    vehicle_year: Optional[int]
    vehicle: Optional[PydanticObjectId] = None
    vehicle_color: Optional[str]

class DriverProfileOut(UserProfileOut):
    vehicle_info: Optional[VehicleInfoOut]


from pydantic import BaseModel, Field, HttpUrl, field_serializer
from typing import Optional, List
from beanie import PydanticObjectId
from datetime import datetime


class RequestRentalsIn(BaseModel):
    rental: PydanticObjectId


class RequestRentalsOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    rental: Optional[PydanticObjectId] = None
    total_price: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer('created_at')
    def serialize_created_at(self, value, _info):
        return str(value) if value else None

    @field_serializer('updated_at')
    def serialize_updated_at(self, value, _info):
        return str(value) if value else None


class RentalsIn(BaseModel):
    name: str

    price: float

    image_url: HttpUrl


class RentalsOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: Optional[str] = None

    price: Optional[float] = None

    image_url: Optional[HttpUrl] = None

    @field_serializer("image_url")
    def serialize_image_url(self, value, _info):
        return str(value) if value else None


class ListRentalsOut(BaseModel):
    rentals: List[RentalsOut]

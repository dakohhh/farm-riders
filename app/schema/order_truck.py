from pydantic import BaseModel, Field, ConfigDict, field_serializer
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional


# 6.4760654
# 3.6169789


class Location(BaseModel):
    address: str
    latitude: float = Field(..., example=6.4760654)
    longitude: float = Field(..., example=3.6169789)


class OrderTruckIn(BaseModel):
    pickup_location: Location
    dropoff_location: Location

    pickup_time: datetime

    type_of_goods: str
    weight_of_goods: float
    quantity_of_goods: int
    issued_insurance: bool

    insurance_cost: float

    total_cost: float

    driver: Optional[PydanticObjectId] = None

    # rental_duration_days: int
    # special_instructions: Optional[str] = None


class OrderTruckOut(BaseModel):
    order_truck_id: PydanticObjectId = Field(alias="_id")
    pickup_location: Optional[Location] = None
    dropoff_location: Optional[Location] = None

    pickup_time: Optional[datetime] = None

    type_of_goods: Optional[str] = None
    weight_of_goods: Optional[float] = None
    quantity_of_goods: Optional[int] = None
    issued_insurance: Optional[bool] = None

    insurance_cost: Optional[float] = None

    total_cost: Optional[float] = None

    driver: Optional[PydanticObjectId] = None

    @field_serializer("pickup_time")
    def serialize_pickup_time(self, value, _info):
        return str(value) if value else None

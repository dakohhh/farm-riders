from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from datetime import datetime
from typing import Optional


# 6.4760654
# 3.6169789


class Location(BaseModel):
    address: str
    latitude: float = Field(..., example=6.4760654)
    longitude: float = Field(..., example=3.6169789)


class OrderTruck(BaseModel):
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

    rental_duration_days: int

    max_distance_km: float = Field(..., example=10.0)
    special_instructions: Optional[str] = None

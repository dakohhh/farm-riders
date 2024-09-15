from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List


class VehicleIn(BaseModel):
    name: str
    image_url: str


class VehicleOut(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    name: str
    price: int
    image_url: str

    class Config:
        allow_population_by_field_name = True


class ListVehicleOut(BaseModel):
    vehicles: List[VehicleOut]

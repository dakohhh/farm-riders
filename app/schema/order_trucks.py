from pydantic import BaseModel, Field
from datetime import datetime

class Location(BaseModel):
    address: str
    latitude: float = Field(..., example=6.4760654)
    longitude: float = Field(..., example=3.6169789)



class OrderTruck(BaseModel):
    is_insured: bool
    pickup_location: str
    dropoff_location: str
    types_of_goods: str
    weight_of_goods:str
    quantity_of_goods:int
    preferred_time: datetime
    vehicle_type: str
    rental_duration: str
    location:str
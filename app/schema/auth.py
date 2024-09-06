from pydantic import BaseModel
from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import List, Optional
from ..enums.user import UserRoles


class CreateUser(BaseModel):
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    password: str = Field(..., example="Password123")
    email: EmailStr = Field(..., example="john@example.com")
    phone_number: str = Field(..., example="+1234567890")
    role: str = Field(..., example=UserRoles.farmers.value)


class Login(BaseModel):
    email: str = Field(..., example="john@example.com")
    password: str = Field(..., example="Password123")

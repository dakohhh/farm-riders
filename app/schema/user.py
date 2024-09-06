from beanie import PydanticObjectId
from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import List, Optional


class User(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: EmailStr
    phone_number: str
    role: str


class UserProfile(BaseModel):
    nin: Optional[str] = Field(None, example="12345678901")
    verification_document: Optional[HttpUrl] = Field(None, example="https://example.com/verification_document.jpg")


    
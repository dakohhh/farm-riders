from pydantic import BaseModel, EmailStr, Field, model_validator, constr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from ..enums.user import UserRoles


class CreateUser(BaseModel):
    password: constr(min_length=6, max_length=100) = Field(..., example="Password123")  # type: ignore
    email: EmailStr = Field(..., example="john@example.com")
    phone_number: Optional[PhoneNumber] = Field(None, example="+2347052316803")
    role: str = Field(..., example=UserRoles.farmers.value)


class Login(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john@example.com")
    phone_number: Optional[PhoneNumber] = Field(None, example="+2347052316803")
    password: constr(min_length=6, max_length=100) = Field(..., example="Password123")  # type: ignore

    @model_validator(mode='after')
    def check_email_or_phone(self):
        email, phone_number = self.email, self.phone_number
        if not email and not phone_number:
            raise ValueError('Either email or phone_number must be provided')
        return self

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class SignupResponse(BaseModel):
    status: Literal["success", "error"]
    email: EmailStr
    email_verified: bool
    message: str


class UserInfoResponse(BaseModel):
    id: str
    email: EmailStr
    email_verified: bool
    created_at: datetime

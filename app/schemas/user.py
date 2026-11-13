"""This module defines how data enters and leaves application over HTTP"""
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    is_active: bool

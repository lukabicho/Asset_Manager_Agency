"""This module defines how data enters and leaves application over HTTP"""
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    """Schema for validation user login credentials"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for serializing user profile in API response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    is_active: bool

class TokenResponse(BaseModel):
    """Schema returned upon successful Oauth2 login or token refresh"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    """Schema for requesting a new access token or logging out"""
    refresh_token: str

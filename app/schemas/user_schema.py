from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# -------------------------------
# BASE
# -------------------------------
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: str = Field(default="worker", pattern="^(owner|manager|worker)$")


# -------------------------------
# CREATE
# -------------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


# -------------------------------
# UPDATE
# -------------------------------
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = Field(None, pattern="^(owner|manager|worker)$")


# -------------------------------
# RESPONSE
# -------------------------------
class UserResponse(UserBase):
    id: str
    business_id: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
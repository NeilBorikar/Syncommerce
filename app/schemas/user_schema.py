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
    phone: Optional[str] = Field(default=None)
    branch_id: Optional[str] = Field(default=None)


# -------------------------------
# CREATE
# -------------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    salary: Optional[float] = Field(default=0.0, ge=0)
    date_joined: Optional[str] = Field(default="")


# -------------------------------
# UPDATE
# -------------------------------
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = Field(None, pattern="^(owner|manager|worker)$")
    phone: Optional[str] = None
    salary: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|suspended|inactive)$")
    branch_id: Optional[str] = None
    managed_by: Optional[str] = None


# -------------------------------
# RESPONSE
# -------------------------------
class UserResponse(UserBase):
    id: str
    business_id: Optional[str] = None
    is_active: bool
    salary: Optional[float] = 0.0
    date_joined: Optional[str] = ""
    status: Optional[str] = "active"
    created_at: datetime

    model_config = {"from_attributes": True}
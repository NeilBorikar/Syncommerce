from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# -------------------------------
# CREATE
# -------------------------------
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="worker", pattern="^(manager|worker)$")
    phone: Optional[str] = Field(default="")
    salary: Optional[float] = Field(default=0.0, ge=0)
    date_joined: Optional[str] = Field(default="")
    branch_id: Optional[str] = None
    business_id: str


# -------------------------------
# UPDATE
# -------------------------------
class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = Field(None, pattern="^(manager|worker)$")
    phone: Optional[str] = None
    salary: Optional[float] = Field(None, ge=0)
    date_joined: Optional[str] = None
    branch_id: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|suspended|inactive)$")


# -------------------------------
# RESPONSE
# -------------------------------
class EmployeeResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    phone: Optional[str] = ""
    salary: Optional[float] = 0.0
    date_joined: Optional[str] = ""
    branch_id: Optional[str] = None
    business_id: Optional[str] = None
    status: Optional[str] = "active"
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

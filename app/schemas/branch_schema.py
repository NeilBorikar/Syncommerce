from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------------------------------
# CREATE
# -------------------------------
class BranchCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: Optional[str] = Field(default="")
    phone: Optional[str] = Field(default="")
    business_id: str


# -------------------------------
# UPDATE
# -------------------------------
class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


# -------------------------------
# RESPONSE
# -------------------------------
class BranchResponse(BranchCreate):
    id: str
    is_active: bool = True
    created_at: datetime

    model_config = {"from_attributes": True}

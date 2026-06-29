from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


# -------------------------------
# BASE
# -------------------------------
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    phone: str = Field(..., min_length=1, max_length=20)
    billing_address: Optional[str] = Field(default="")
    shipping_address: Optional[str] = Field(default="")
    email: Optional[str] = Field(default="")


# -------------------------------
# CREATE
# -------------------------------
class CustomerCreate(CustomerBase):
    business_id: str
    branch_id: Optional[str] = None


# -------------------------------
# UPDATE
# -------------------------------
class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    email: Optional[str] = None


# -------------------------------
# RESPONSE
# -------------------------------
class CustomerResponse(CustomerBase):
    id: str
    business_id: str
    branch_id: Optional[str] = None
    total_spend: float = 0.0
    bill_count: int = 0
    favorite_items: List[Any] = []
    created_at: datetime

    model_config = {"from_attributes": True}

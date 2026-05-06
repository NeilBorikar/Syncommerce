from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -------------------------------
# ITEM SCHEMA
# -------------------------------
class BillItem(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


# -------------------------------
# BASE
# -------------------------------
class BillBase(BaseModel):
    items: List[BillItem]
    discount: Optional[float] = Field(default=0, ge=0)
    tax: Optional[float] = Field(default=0, ge=0)


# -------------------------------
# CREATE
# -------------------------------
class BillCreate(BillBase):
    business_id: str
    created_by: str


# -------------------------------
# UPDATE
# -------------------------------
class BillUpdate(BaseModel):
    items: Optional[List[BillItem]]
    discount: Optional[float] = Field(None, ge=0)
    tax: Optional[float] = Field(None, ge=0)


# -------------------------------
# RESPONSE
# -------------------------------
class BillResponse(BillBase):
    id: str
    business_id: str
    created_by: str
    total: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
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
    gst_percent: float = Field(default=0, ge=0, le=100)


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
    customer_id: Optional[str] = None
    customer_name: Optional[str] = ""
    customer_phone: Optional[str] = ""
    billing_address: Optional[str] = ""
    shipping_address: Optional[str] = ""
    notes: Optional[str] = ""
    branch_id: Optional[str] = None


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
    gst_total: Optional[float] = 0
    status: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = ""
    customer_phone: Optional[str] = ""
    billing_address: Optional[str] = ""
    shipping_address: Optional[str] = ""
    notes: Optional[str] = ""
    branch_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------------------------------
# BASE
# -------------------------------
class InventoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)
    low_stock_threshold: Optional[int] = Field(default=5, ge=0)


# -------------------------------
# CREATE
# -------------------------------
class InventoryCreate(InventoryBase):
    business_id: str


# -------------------------------
# UPDATE
# -------------------------------
class InventoryUpdate(BaseModel):
    name: Optional[str]
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)


# -------------------------------
# RESPONSE
# -------------------------------
class InventoryResponse(InventoryBase):
    id: str
    business_id: str
    updated_at: datetime

    class Config:
        from_attributes = True
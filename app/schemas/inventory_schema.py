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
    sku: Optional[str] = Field(default="")
    category: Optional[str] = Field(default="")
    cost_price: Optional[float] = Field(default=0.0, ge=0)
    selling_price: Optional[float] = Field(default=0.0, ge=0)
    unit: Optional[str] = Field(default="pcs")
    description: Optional[str] = Field(default="")


# -------------------------------
# CREATE
# -------------------------------
class InventoryCreate(InventoryBase):
    business_id: str
    branch_id: Optional[str] = None


# -------------------------------
# UPDATE
# -------------------------------
class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = None
    category: Optional[str] = None
    cost_price: Optional[float] = Field(None, ge=0)
    selling_price: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = None
    description: Optional[str] = None
    branch_id: Optional[str] = None


# -------------------------------
# RESPONSE
# -------------------------------
class InventoryResponse(InventoryBase):
    id: str
    business_id: str
    branch_id: Optional[str] = None
    updated_at: datetime

    model_config = {"from_attributes": True}


# -------------------------------
# SEARCH
# -------------------------------
class InventorySearch(BaseModel):
    query: str = Field(..., min_length=1)
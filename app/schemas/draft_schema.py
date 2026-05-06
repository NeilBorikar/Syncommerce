from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DraftItem(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    price: Optional[float]


# -------------------------------
# BASE
# -------------------------------
class DraftBase(BaseModel):
    items: List[DraftItem] = []
    notes: Optional[str] = Field(None, max_length=500)


# -------------------------------
# CREATE
# -------------------------------
class DraftCreate(DraftBase):
    business_id: str
    created_by: str


# -------------------------------
# UPDATE
# -------------------------------
class DraftUpdate(BaseModel):
    items: Optional[List[DraftItem]]
    notes: Optional[str]


# -------------------------------
# RESPONSE
# -------------------------------
class DraftResponse(DraftBase):
    id: str
    business_id: str
    created_by: str
    last_updated_by: Optional[str]
    updated_at: datetime

    class Config:
        from_attributes = True
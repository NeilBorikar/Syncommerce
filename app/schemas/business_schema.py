from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class BusinessBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    address: Optional[str] = None

class BusinessCreate(BusinessBase):
    password: str = Field(..., min_length=6)

class BusinessResponse(BusinessBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class BusinessRegistrationPayload(BaseModel):
    business: BusinessCreate
    owner_name: str = Field(..., min_length=2, max_length=100)
    owner_email: EmailStr
    owner_password: str = Field(..., min_length=6)

class BusinessLoginPayload(BaseModel):
    email: EmailStr
    password: str

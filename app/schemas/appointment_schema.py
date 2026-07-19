from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_id: str
    slot_time: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    business_id: str
    patient_id: str
    token_number: int
    status: str
    slot_time: Optional[str] = None
    date: str
    created_at: datetime

    model_config = {"from_attributes": True}

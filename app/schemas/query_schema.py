from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QueryCreate(BaseModel):
    question_text: str = Field(..., min_length=1)

class QueryAnswer(BaseModel):
    answer_text: str = Field(..., min_length=1)

class QueryForward(BaseModel):
    forwarded_to: str = Field(...)

class QueryResponse(BaseModel):
    id: str
    business_id: str
    patient_id: str
    question_text: str
    status: str
    answer_text: Optional[str] = None
    answered_by: Optional[str] = None
    forwarded_to: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

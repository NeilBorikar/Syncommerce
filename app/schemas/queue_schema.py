from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QueueResponse(BaseModel):
    id: str
    business_id: str
    current_token: int
    avg_wait_minutes: int
    date: str
    created_at: datetime

    model_config = {"from_attributes": True}

from app.models.base_model import BaseModelMixin
from datetime import datetime, timezone

class Appointment(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        patient_id: str,
        token_number: int,
        status: str = "waiting", # waiting, in_progress, completed, cancelled
        slot_time: str = None, # e.g., "10:30 AM" if applicable
        date: str = None
    ):
        super().__init__()
        self.business_id = business_id
        self.patient_id = patient_id
        self.token_number = token_number
        self.status = status
        self.slot_time = slot_time
        self.date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

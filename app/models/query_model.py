from app.models.base_model import BaseModelMixin
from datetime import datetime, timezone

class PatientQuery(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        patient_id: str,
        question_text: str,
        status: str = "open", # open, forwarded, answered
        answer_text: str = None,
        answered_by: str = None, # User ID of staff
        forwarded_to: str = None # User ID of doctor if forwarded
    ):
        super().__init__()
        self.business_id = business_id
        self.patient_id = patient_id
        self.question_text = question_text
        self.status = status
        self.answer_text = answer_text
        self.answered_by = answered_by
        self.forwarded_to = forwarded_to

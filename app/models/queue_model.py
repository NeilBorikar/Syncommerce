from datetime import datetime, timezone
from app.models.base_model import BaseModelMixin

class Queue(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        current_token: int = 0,
        avg_wait_minutes: int = 15,
        date: str = None
    ):
        super().__init__()
        self.business_id = business_id
        self.current_token = current_token
        self.avg_wait_minutes = avg_wait_minutes
        self.date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

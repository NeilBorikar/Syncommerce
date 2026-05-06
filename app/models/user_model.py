from datetime import datetime, timezone
from app.models.base_model import BaseModelMixin


class User(BaseModelMixin):
    def __init__(
        self,
        name: str,
        email: str,
        hashed_password: str,
        role: str = "worker",
        business_id: str = None,
        is_active: bool = True,
    ):
        super().__init__()

        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.business_id = business_id
        self.is_active = is_active
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
        phone: str = "",
        salary: float = 0.0,
        date_joined: str = "",
        status: str = "active",
        managed_by: str = None,
        branch_id: str = None,
    ):
        super().__init__()

        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.business_id = business_id
        self.is_active = is_active
        self.phone = phone
        self.salary = salary
        self.date_joined = date_joined
        self.status = status
        self.managed_by = managed_by
        self.branch_id = branch_id
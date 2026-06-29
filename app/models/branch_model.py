from app.models.base_model import BaseModelMixin


class Branch(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        name: str,
        address: str = "",
        phone: str = "",
        is_active: bool = True,
    ):
        super().__init__()
        self.business_id = business_id
        self.name = name
        self.address = address
        self.phone = phone
        self.is_active = is_active

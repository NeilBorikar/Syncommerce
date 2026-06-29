from app.models.base_model import BaseModelMixin


class Business(BaseModelMixin):
    def __init__(
        self,
        name: str,
        email: str,
        hashed_password: str,
        owner_id: str,
        address: str = None,
    ):
        super().__init__()

        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.owner_id = owner_id
        self.address = address
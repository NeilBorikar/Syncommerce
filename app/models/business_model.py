from app.models.base_model import BaseModelMixin


class Business(BaseModelMixin):
    def __init__(
        self,
        name: str,
        owner_id: str,
        address: str = None,
    ):
        super().__init__()

        self.name = name
        self.owner_id = owner_id
        self.address = address
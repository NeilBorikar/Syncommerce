from app.models.base_model import BaseModelMixin


class Bill(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        created_by: str,
        items: list,
        total: float,
        discount: float = 0,
        tax: float = 0,
        status: str = "final",
    ):
        super().__init__()

        self.business_id = business_id
        self.created_by = created_by
        self.items = items
        self.total = total
        self.discount = discount
        self.tax = tax
        self.status = status
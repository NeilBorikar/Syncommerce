from app.models.base_model import BaseModelMixin


class Inventory(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        name: str,
        quantity: int,
        price: float,
        low_stock_threshold: int = 5,
    ):
        super().__init__()

        self.business_id = business_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.low_stock_threshold = low_stock_threshold
from app.models.base_model import BaseModelMixin


class Inventory(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        name: str,
        quantity: int,
        price: float,
        low_stock_threshold: int = 5,
        sku: str = "",
        category: str = "",
        cost_price: float = 0.0,
        selling_price: float = 0.0,
        unit: str = "pcs",
        description: str = "",
        branch_id: str = None,
    ):
        super().__init__()

        self.business_id = business_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.low_stock_threshold = low_stock_threshold
        self.sku = sku
        self.category = category
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.unit = unit
        self.description = description
        self.branch_id = branch_id
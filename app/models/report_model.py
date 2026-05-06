from app.models.base_model import BaseModelMixin


class Report(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        total_sales: float,
        total_orders: int,
        date: str,
    ):
        super().__init__()

        self.business_id = business_id
        self.total_sales = total_sales
        self.total_orders = total_orders
        self.date = date
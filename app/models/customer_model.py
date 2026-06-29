from app.models.base_model import BaseModelMixin


class Customer(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        branch_id: str,
        name: str,
        phone: str,
        billing_address: str = "",
        shipping_address: str = "",
        email: str = "",
    ):
        super().__init__()
        self.business_id = business_id
        self.branch_id = branch_id
        self.name = name
        self.phone = phone  # used as unique lookup key per business
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.email = email
        self.total_spend = 0.0
        self.bill_count = 0
        self.favorite_items = []  # list of {name, count}

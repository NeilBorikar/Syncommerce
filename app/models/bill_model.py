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
        customer_id: str = None,
        customer_name: str = "",
        customer_phone: str = "",
        billing_address: str = "",
        shipping_address: str = "",
        gst_total: float = 0,
        notes: str = "",
        branch_id: str = None,
    ):
        super().__init__()

        self.business_id = business_id
        self.created_by = created_by
        self.items = items
        self.total = total
        self.discount = discount
        self.tax = tax
        self.status = status
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.gst_total = gst_total
        self.notes = notes
        self.branch_id = branch_id
from app.models.base_model import BaseModelMixin


class Draft(BaseModelMixin):
    def __init__(
        self,
        business_id: str,
        created_by: str,
        items: list = None,
        notes: str = None,
        last_updated_by: str = None,
    ):
        super().__init__()

        self.business_id = business_id
        self.created_by = created_by
        self.items = items or []
        self.notes = notes
        self.last_updated_by = last_updated_by
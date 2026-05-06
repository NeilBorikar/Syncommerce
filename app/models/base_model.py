from datetime import datetime, timezone
from bson import ObjectId


class BaseModelMixin:
    def __init__(self):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        data = self.__dict__.copy()

        # Convert ObjectId to string
        if "_id" in data and isinstance(data["_id"], ObjectId):
            data["_id"] = str(data["_id"])

        return data
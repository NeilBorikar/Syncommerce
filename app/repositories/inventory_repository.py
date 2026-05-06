from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["inventory"])

    def get_low_stock(self, business_id: str):
        items = self.collection.find({
            "business_id": business_id,
            "$expr": {"$lte": ["$quantity", "$low_stock_threshold"]}
        })
        return self._convert_many(list(items))

    def update_stock(self, item_id: str, quantity: int):
        return self.update(item_id, {"quantity": quantity})
from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class BillRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["bills"])

    def get_by_business(self, business_id: str):
        bills = self.collection.find({"business_id": business_id})
        return self._convert_many(list(bills))

    def get_by_user(self, user_id: str):
        bills = self.collection.find({"created_by": user_id})
        return self._convert_many(list(bills))

    def get_daily_sales(self, business_id: str, start, end):
        bills = self.collection.find({
            "business_id": business_id,
            "created_at": {"$gte": start, "$lte": end}
        })
        return self._convert_many(list(bills))
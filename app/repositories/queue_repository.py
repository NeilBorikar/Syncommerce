from pymongo.database import Database
from app.repositories.base_repository import BaseRepository

class QueueRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["queues"])

    def get_by_business_and_date(self, business_id: str, date: str):
        queue = self.collection.find_one({"business_id": business_id, "date": date})
        if queue:
            return self._convert_one(queue)
        return None

from pymongo.database import Database
from app.repositories.base_repository import BaseRepository

class QueryRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["queries"])

    def get_by_business(self, business_id: str):
        queries = self.collection.find({"business_id": business_id}).sort("created_at", -1)
        return self._convert_many(list(queries))

    def get_by_patient(self, patient_id: str):
        queries = self.collection.find({"patient_id": patient_id}).sort("created_at", -1)
        return self._convert_many(list(queries))

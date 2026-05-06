from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["reports"])

    def get_by_date(self, business_id: str, date: str):
        report = self.collection.find_one({
            "business_id": business_id,
            "date": date
        })
        return self._convert_id(report)
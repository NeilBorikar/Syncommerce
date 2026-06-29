from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class BusinessRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["businesses"])

    def get_by_owner(self, owner_id: str):
        businesses = self.collection.find({"owner_id": owner_id})
        return self._convert_many(list(businesses))

    def get_by_email(self, email: str):
        business = self.collection.find_one({"email": email})
        return self._convert_id(business)
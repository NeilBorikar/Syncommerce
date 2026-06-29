from typing import List, Optional, Dict
from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["users"])

    def get_by_email(self, email: str) -> Optional[Dict]:
        user = self.collection.find_one({"email": email})
        return self._convert_id(user)

    def get_by_business(self, business_id: str) -> List[Dict]:
        users = self.collection.find({"business_id": business_id})
        return self._convert_many(list(users))

    def get_by_business_and_role(self, business_id: str, role: str) -> List[Dict]:
        """Filter users by business and role."""
        users = self.collection.find({"business_id": business_id, "role": role})
        return self._convert_many(list(users))

    def deactivate_user(self, user_id: str) -> Optional[Dict]:
        return self.update(user_id, {"is_active": False})
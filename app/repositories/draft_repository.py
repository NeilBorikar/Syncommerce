from pymongo.database import Database
from app.repositories.base_repository import BaseRepository


class DraftRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["drafts"])

    def get_by_business(self, business_id: str):
        drafts = self.collection.find({"business_id": business_id})
        return self._convert_many(list(drafts))

    def update_draft_user(self, draft_id: str, user_id: str):
        return self.update(draft_id, {"last_updated_by": user_id})
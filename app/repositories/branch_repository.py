from app.repositories.base_repository import BaseRepository

class BranchRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "branches")

    def get_by_business(self, business_id: str):
        return list(self.collection.find({"business_id": business_id}))

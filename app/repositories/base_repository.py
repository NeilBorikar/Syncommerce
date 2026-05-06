from typing import Any, Dict, List, Optional
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime, timezone


class BaseRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    # -------------------------------
    # HELPERS
    # -------------------------------
    def _convert_id(self, data: Dict) -> Dict:
        if data and "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]
        return data

    def _convert_many(self, data: List[Dict]) -> List[Dict]:
        return [self._convert_id(doc) for doc in data]

    def _get_timestamp(self):
        return datetime.now(timezone.utc)

    # -------------------------------
    # CREATE
    # -------------------------------
    def create(self, data: Dict) -> Dict:
        data["created_at"] = self._get_timestamp()
        data["updated_at"] = self._get_timestamp()

        result = self.collection.insert_one(data)
        created = self.collection.find_one({"_id": result.inserted_id})

        return self._convert_id(created)

    # -------------------------------
    # GET ONE
    # -------------------------------
    def get_by_id(self, id: str) -> Optional[Dict]:
        try:
            obj_id = ObjectId(id)
        except:
            return None

        data = self.collection.find_one({"_id": obj_id})
        return self._convert_id(data)

    # -------------------------------
    # GET MANY
    # -------------------------------
    def get_many(
        self,
        filters: Dict = {},
        skip: int = 0,
        limit: int = 10,
        sort: Optional[List] = None,
    ) -> List[Dict]:

        cursor = self.collection.find(filters)

        if sort:
            cursor = cursor.sort(sort)

        cursor = cursor.skip(skip).limit(limit)

        return self._convert_many(list(cursor))

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, id: str, data: Dict) -> Optional[Dict]:
        try:
            obj_id = ObjectId(id)
        except:
            return None

        data["updated_at"] = self._get_timestamp()

        self.collection.update_one(
            {"_id": obj_id},
            {"$set": data}
        )

        updated = self.collection.find_one({"_id": obj_id})
        return self._convert_id(updated)

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, id: str) -> bool:
        try:
            obj_id = ObjectId(id)
        except:
            return False

        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0

    # -------------------------------
    # COUNT
    # -------------------------------
    def count(self, filters: Dict = {}) -> int:
        return self.collection.count_documents(filters)
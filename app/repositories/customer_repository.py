from typing import List, Optional, Dict
from pymongo.database import Database
from bson import ObjectId
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db["customers"])

    def get_by_phone(self, business_id: str, phone: str) -> Optional[Dict]:
        """Find a customer by phone within a business."""
        customer = self.collection.find_one({
            "business_id": business_id,
            "phone": phone,
        })
        return self._convert_id(customer)

    def get_by_business(self, business_id: str) -> List[Dict]:
        """Get all customers for a business."""
        customers = self.collection.find({"business_id": business_id}).sort("name", 1)
        return self._convert_many(list(customers))

    def update_spend_and_favorites(
        self,
        customer_id: str,
        amount: float,
        items: list,
    ) -> Optional[Dict]:
        """
        Increment total_spend and bill_count, then recompute favorite_items
        by counting occurrences of each item name across the stored item history.

        `items` is the list of bill items dicts: [{name, quantity, price, ...}]
        """
        try:
            obj_id = ObjectId(customer_id)
        except Exception:
            return None

        # Fetch existing customer to read current favorite_items accumulator
        customer = self.collection.find_one({"_id": obj_id})
        if not customer:
            return None

        # Build updated item count from existing favorites + new items
        item_counts: Dict[str, int] = {}
        for fav in customer.get("favorite_items", []):
            item_counts[fav["name"]] = fav.get("count", 0)

        for item in items:
            name = item.get("name", "")
            if name:
                item_counts[name] = item_counts.get(name, 0) + item.get("quantity", 1)

        # Sort by count descending, keep top 5
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        favorite_items = [{"name": n, "count": c} for n, c in sorted_items[:5]]

        from datetime import datetime, timezone
        self.collection.update_one(
            {"_id": obj_id},
            {
                "$inc": {"total_spend": amount, "bill_count": 1},
                "$set": {
                    "favorite_items": favorite_items,
                    "updated_at": datetime.now(timezone.utc),
                },
            },
        )

        updated = self.collection.find_one({"_id": obj_id})
        return self._convert_id(updated)

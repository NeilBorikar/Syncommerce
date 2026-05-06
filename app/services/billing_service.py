from app.repositories.bill_repository import BillRepository
from app.utils.logger import logger


class BillingService:
    def __init__(self, db, sync_engine=None):
        self.repo = BillRepository(db)
        self.sync_engine = sync_engine

    def _calculate_total(self, items, discount=0, tax=0):
        total = sum(item["quantity"] * item["price"] for item in items)
        total -= discount
        total += tax
        return max(total, 0)

    async def create_bill(self, data: dict):
        try:
            total = self._calculate_total(
                data["items"],
                data.get("discount", 0),
                data.get("tax", 0),
            )

            bill_data = {
                **data,
                "total": total,
                "status": "final",
            }

            bill = self.repo.create(bill_data)

            logger.info(f"Bill created: {bill['id']}")

            # 🔥 REALTIME TRIGGER
            if self.sync_engine:
                await self.sync_engine.handle_bill_created(
                    data["business_id"],
                    bill
                )

            return bill

        except Exception as e:
            logger.error("Bill creation failed", exc_info=True)
            raise e

    def get_business_bills(self, business_id: str):
        return self.repo.get_by_business(business_id)
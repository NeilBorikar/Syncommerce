from app.repositories.inventory_repository import InventoryRepository
from app.utils.logger import logger


class InventoryService:
    def __init__(self, db, sync_engine=None):
        self.repo = InventoryRepository(db)
        self.sync_engine = sync_engine

    async def create_item(self, data: dict):
        item = self.repo.create(data)

        logger.info(f"Inventory item created: {item['id']}")

        if self.sync_engine:
            await self.sync_engine.handle_inventory_updated(
                data["business_id"],
                item
            )

        return item

    async def update_stock(self, item_id: str, quantity: int, business_id: str):
        item = self.repo.update_stock(item_id, quantity)

        if self.sync_engine:
            await self.sync_engine.handle_inventory_updated(
                business_id,
                item
            )

        return item

    def get_low_stock(self, business_id: str):
        return self.repo.get_low_stock(business_id)
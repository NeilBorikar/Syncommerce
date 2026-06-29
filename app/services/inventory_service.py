from app.repositories.inventory_repository import InventoryRepository
from app.utils.logger import logger
import io
from openpyxl import Workbook


class InventoryService:
    def __init__(self, db, sync_engine=None):
        self.repo = InventoryRepository(db)
        self.sync_engine = sync_engine

    def get_all_items(self, business_id: str, branch_id: str = None):
        if branch_id:
            # Need to implement in repo or filter here
            items = self.repo.get_by_business(business_id)
            return [i for i in items if i.get("branch_id") == branch_id]
        return self.repo.get_by_business(business_id)

    def search_items(self, business_id: str, query: str, branch_id: str = None):
        items = self.repo.search_items(business_id, query)
        if branch_id:
            return [i for i in items if i.get("branch_id") == branch_id]
        return items

    async def create_item(self, data: dict):
        item = self.repo.create(data)
        logger.info(f"Inventory item created: {item['id']}")

        if self.sync_engine:
            await self.sync_engine.handle_inventory_updated(
                data["business_id"],
                item
            )

        return item

    async def update_item(self, item_id: str, data: dict, business_id: str):
        item = self.repo.update(item_id, data)
        if self.sync_engine and item:
            await self.sync_engine.handle_inventory_updated(
                business_id,
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
        
    async def delete_item(self, item_id: str, business_id: str):
        result = self.repo.delete(item_id)
        if self.sync_engine and result:
            await self.sync_engine.handle_inventory_updated(business_id, {"deleted_id": item_id})
        return result

    def get_low_stock(self, business_id: str):
        return self.repo.get_low_stock(business_id)

    def export_excel(self, business_id: str) -> bytes:
        try:
            items = self.repo.get_by_business(business_id)
            wb = Workbook()
            ws = wb.active
            ws.title = "Inventory"
            headers = ["ID", "SKU", "Name", "Category", "Quantity", "Cost Price", "Selling Price", "Unit", "Low Stock Threshold", "Branch ID"]
            ws.append(headers)
            for i in items:
                ws.append([
                    i.get("id", ""), i.get("sku", ""), i.get("name", ""), i.get("category", ""),
                    i.get("quantity", 0), i.get("cost_price", 0.0), i.get("selling_price", 0.0),
                    i.get("unit", "pcs"), i.get("low_stock_threshold", 5), i.get("branch_id", "")
                ])
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            logger.error("Inventory Excel export failed", exc_info=True)
            raise e
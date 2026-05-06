from app.realtime.manager import ConnectionManager
from app.realtime.events import build_event, EventType
from app.utils.logger import logger


class SyncEngine:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    # -------------------------------
    # BILL CREATED
    # -------------------------------
    async def handle_bill_created(self, business_id: str, bill_data: dict):
        event = build_event(EventType.BILL_CREATED, bill_data)

        logger.info(f"Broadcasting BILL_CREATED for {business_id}")

        await self.manager.broadcast(business_id, event)

    # -------------------------------
    # DRAFT UPDATED
    # -------------------------------
    async def handle_draft_updated(self, business_id: str, draft_data: dict):
        event = build_event(EventType.DRAFT_UPDATED, draft_data)

        logger.info(f"Broadcasting DRAFT_UPDATED for {business_id}")

        await self.manager.broadcast(business_id, event)

    # -------------------------------
    # INVENTORY UPDATED
    # -------------------------------
    async def handle_inventory_updated(self, business_id: str, data: dict):
        event = build_event(EventType.INVENTORY_UPDATED, data)

        logger.info(f"Broadcasting INVENTORY_UPDATED for {business_id}")

        await self.manager.broadcast(business_id, event)
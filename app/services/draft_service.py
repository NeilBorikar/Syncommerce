from app.repositories.draft_repository import DraftRepository
from app.utils.logger import logger


class DraftService:
    def __init__(self, db, sync_engine=None):
        self.repo = DraftRepository(db)
        self.sync_engine = sync_engine

    async def create_draft(self, data: dict):
        draft = self.repo.create(data)

        logger.info(f"Draft created: {draft['id']}")

        if self.sync_engine:
            await self.sync_engine.handle_draft_updated(
                data["business_id"],
                draft
            )

        return draft

    async def update_draft(self, draft_id: str, data: dict, user_id: str):
        data["last_updated_by"] = user_id
        draft = self.repo.update(draft_id, data)

        logger.info(f"Draft updated: {draft_id}")

        if self.sync_engine:
            await self.sync_engine.handle_draft_updated(
                draft["business_id"],
                draft
            )

        return draft

    def get_drafts(self, business_id: str):
        return self.repo.get_by_business(business_id)
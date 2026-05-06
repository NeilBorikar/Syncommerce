from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.services.draft_service import DraftService

router = APIRouter()


@router.post("/")
def create_draft(data: dict, db=Depends(get_db)):
    service = DraftService(db)
    return service.create_draft(data)


@router.put("/{draft_id}")
def update_draft(draft_id: str, data: dict, db=Depends(get_db)):
    service = DraftService(db)
    return service.update_draft(draft_id, data, data.get("user_id"))


@router.get("/{business_id}")
def get_drafts(business_id: str, db=Depends(get_db)):
    service = DraftService(db)
    return service.get_drafts(business_id)
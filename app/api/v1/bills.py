from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.services.billing_service import BillingService
from app.realtime.manager import ConnectionManager
from app.realtime.sync_engine import SyncEngine

router = APIRouter()

# Module-level sync_engine reference — set by main.py after app creation
_sync_engine: SyncEngine | None = None

def set_sync_engine(engine: SyncEngine):
    global _sync_engine
    _sync_engine = engine


@router.post("/")
async def create_bill(data: dict, db=Depends(get_db)):
    service = BillingService(db, _sync_engine)
    return await service.create_bill(data)


@router.get("/{business_id}")
def get_bills(business_id: str, db=Depends(get_db)):
    service = BillingService(db)
    return service.get_business_bills(business_id)
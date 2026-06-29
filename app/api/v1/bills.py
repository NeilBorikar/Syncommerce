from fastapi import APIRouter, Depends
from app.api.deps import get_db, require_role
from app.services.billing_service import BillingService
from app.realtime.sync_engine import SyncEngine

router = APIRouter()
owner_only = Depends(require_role(["owner"]))

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

@router.get("/{business_id}/customer/{customer_id}")
def get_customer_bills(business_id: str, customer_id: str, db=Depends(get_db)):
    service = BillingService(db)
    bills = service.get_business_bills(business_id)
    return [b for b in bills if b.get("customer_id") == customer_id]

@router.delete("/{id}", dependencies=[owner_only])
def delete_bill(id: str, db=Depends(get_db)):
    # Assuming delete is implemented in the repository
    service = BillingService(db, _sync_engine)
    result = service.repo.delete(id)
    return {"deleted": result}
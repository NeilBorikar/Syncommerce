from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.services.billing_service import BillingService

router = APIRouter()


@router.post("/")
async def create_bill(data: dict, db=Depends(get_db)):
    service = BillingService(db)
    return await service.create_bill(data)


@router.get("/{business_id}")
def get_bills(business_id: str, db=Depends(get_db)):
    service = BillingService(db)
    return service.get_business_bills(business_id)
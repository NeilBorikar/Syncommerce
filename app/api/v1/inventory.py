from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.services.inventory_service import InventoryService

router = APIRouter()


@router.post("/")
def create_item(data: dict, db=Depends(get_db)):
    service = InventoryService(db)
    return service.create_item(data)


@router.get("/low-stock/{business_id}")
def low_stock(business_id: str, db=Depends(get_db)):
    service = InventoryService(db)
    return service.get_low_stock(business_id)
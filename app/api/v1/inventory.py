from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io
from app.api.deps import get_db, require_role
from app.services.inventory_service import InventoryService
from typing import Optional

router = APIRouter()
manager_or_owner = Depends(require_role(["manager", "owner"]))
owner_only = Depends(require_role(["owner"]))

@router.get("/")
def get_inventory(business_id: str, branch_id: Optional[str] = None, db=Depends(get_db)):
    service = InventoryService(db)
    return service.get_all_items(business_id, branch_id)

@router.get("/search")
def search_inventory(business_id: str, q: str, branch_id: Optional[str] = None, db=Depends(get_db)):
    service = InventoryService(db)
    return service.search_items(business_id, q, branch_id)

@router.post("/", dependencies=[manager_or_owner])
async def create_item(data: dict, db=Depends(get_db)):
    service = InventoryService(db)
    return await service.create_item(data)

@router.put("/{id}", dependencies=[manager_or_owner])
async def update_item(id: str, data: dict, business_id: str, db=Depends(get_db)):
    service = InventoryService(db)
    return await service.update_item(id, data, business_id)

@router.delete("/{id}", dependencies=[owner_only])
async def delete_item(id: str, business_id: str, db=Depends(get_db)):
    service = InventoryService(db)
    return await service.delete_item(id, business_id)

@router.get("/low-stock/{business_id}")
def low_stock(business_id: str, db=Depends(get_db)):
    service = InventoryService(db)
    return service.get_low_stock(business_id)

@router.get("/export/{business_id}", dependencies=[manager_or_owner])
def export_inventory_excel(business_id: str, db=Depends(get_db)):
    service = InventoryService(db)
    content = service.export_excel(business_id)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=inventory_{business_id}.xlsx"}
    )
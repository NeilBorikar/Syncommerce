from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io
from app.api.deps import get_db, get_current_user, require_role
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter()
manager_or_owner = Depends(require_role(["manager", "owner"]))

@router.post("/")
def register_customer(data: CustomerCreate, db=Depends(get_db), user=Depends(get_current_user)):
    service = CustomerService(db)
    return service.register_customer(data.model_dump())

@router.get("/lookup")
def lookup_customer(phone: str, business_id: str, db=Depends(get_db), user=Depends(get_current_user)):
    service = CustomerService(db)
    return service.lookup_customer(business_id, phone)

@router.get("/{business_id}")
def list_customers(business_id: str, db=Depends(get_db), user=Depends(get_current_user)):
    service = CustomerService(db)
    return service.get_all(business_id)

@router.put("/{id}")
def update_customer(id: str, data: CustomerUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    service = CustomerService(db)
    return service.update_customer(id, data.model_dump(exclude_unset=True))

@router.get("/export/{business_id}", dependencies=[manager_or_owner])
def export_customers_excel(business_id: str, db=Depends(get_db)):
    service = CustomerService(db)
    content = service.export_excel(business_id)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=customers_{business_id}.xlsx"}
    )

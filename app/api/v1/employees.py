from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io
from app.api.deps import get_db, get_current_user, require_role
from app.schemas.employee_schema import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import EmployeeService

router = APIRouter()
manager_or_owner = Depends(require_role(["manager", "owner"]))
owner_only = Depends(require_role(["owner"]))

@router.post("/", dependencies=[manager_or_owner])
def add_employee(data: EmployeeCreate, db=Depends(get_db), user=Depends(get_current_user)):
    service = EmployeeService(db)
    return service.add_employee(data.model_dump(), user)

@router.get("/{business_id}", dependencies=[manager_or_owner])
def list_employees(business_id: str, db=Depends(get_db), user=Depends(get_current_user)):
    service = EmployeeService(db)
    return service.list_employees(business_id)

@router.put("/{id}", dependencies=[manager_or_owner])
def update_employee(id: str, data: EmployeeUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    service = EmployeeService(db)
    return service.update_employee(id, data.model_dump(exclude_unset=True), user)

@router.delete("/{id}", dependencies=[owner_only])
def delete_employee(id: str, db=Depends(get_db), user=Depends(get_current_user)):
    service = EmployeeService(db)
    return service.delete_employee(id, user)

@router.put("/{id}/suspend", dependencies=[manager_or_owner])
def suspend_employee(id: str, status: str, db=Depends(get_db), user=Depends(get_current_user)):
    service = EmployeeService(db)
    return service.suspend_employee(id, status, user)

@router.get("/export/{business_id}", dependencies=[owner_only])
def export_employees_excel(business_id: str, db=Depends(get_db)):
    service = EmployeeService(db)
    content = service.export_excel(business_id)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=employees_{business_id}.xlsx"}
    )

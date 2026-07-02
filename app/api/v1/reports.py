from fastapi import APIRouter, Depends
from app.api.deps import get_db, require_role
from app.services.report_service import ReportService

router = APIRouter()
manager_or_owner = Depends(require_role(["manager", "owner"]))
owner_only = Depends(require_role(["owner"]))

@router.post("/{business_id}")
async def generate_report(business_id: str, db=Depends(get_db)):
    service = ReportService(db)
    return await service.generate_daily_report(business_id)

@router.get("/sales", dependencies=[manager_or_owner])
def get_sales_report(business_id: str, from_date: str, to_date: str, branch_id: str = None, db=Depends(get_db)):
    service = ReportService(db)
    return service.get_sales_report(business_id, from_date, to_date, branch_id)

@router.get("/inventory", dependencies=[manager_or_owner])
def get_inventory_report(business_id: str, branch_id: str = None, db=Depends(get_db)):
    service = ReportService(db)
    return service.get_inventory_report(business_id, branch_id)

@router.get("/employees", dependencies=[manager_or_owner])
def get_employee_performance(business_id: str, from_date: str, to_date: str, db=Depends(get_db)):
    service = ReportService(db)
    return service.get_employee_performance(business_id, from_date, to_date)

@router.get("/gst", dependencies=[owner_only])
def get_gst_report(business_id: str, month: int, year: int, db=Depends(get_db)):
    service = ReportService(db)
    return service.get_gst_report(business_id, month, year)
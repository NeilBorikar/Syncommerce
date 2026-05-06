from fastapi import APIRouter, Depends
from app.api.deps import get_db
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/{business_id}")
def generate_report(business_id: str, db=Depends(get_db)):
    service = ReportService(db)
    return service.generate_daily_report(business_id)
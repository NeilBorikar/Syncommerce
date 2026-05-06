from datetime import datetime, timedelta
from app.repositories.bill_repository import BillRepository
from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, db, sync_engine=None):
        self.bill_repo = BillRepository(db)
        self.report_repo = ReportRepository(db)
        self.sync_engine = sync_engine

    async def generate_daily_report(self, business_id: str):
        today = datetime.utcnow()
        start = datetime(today.year, today.month, today.day)
        end = start + timedelta(days=1)

        bills = self.bill_repo.get_daily_sales(business_id, start, end)

        total_sales = sum(b["total"] for b in bills)
        total_orders = len(bills)

        report_data = {
            "business_id": business_id,
            "total_sales": total_sales,
            "total_orders": total_orders,
            "date": start.isoformat(),
        }

        report = self.report_repo.create(report_data)

        # Optional realtime
        if self.sync_engine:
            await self.sync_engine.handle_inventory_updated(
                business_id,
                {"report": report}
            )

        return report
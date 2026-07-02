from datetime import datetime, timedelta
from app.repositories.bill_repository import BillRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.inventory_repository import InventoryRepository

class ReportService:
    def __init__(self, db, sync_engine=None):
        self.bill_repo = BillRepository(db)
        self.report_repo = ReportRepository(db)
        self.inventory_repo = InventoryRepository(db)
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
        if self.sync_engine:
            await self.sync_engine.handle_inventory_updated(
                business_id,
                {"report": report}
            )
        return report

    def get_sales_report(self, business_id: str, from_date: str, to_date: str, branch_id: str = None):
        # We parse ISO dates if possible
        try:
            start = datetime.fromisoformat(from_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(to_date.replace('Z', '+00:00'))
        except ValueError:
            # Fallback if just YYYY-MM-DD
            start = datetime.strptime(from_date, "%Y-%m-%d")
            end = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)

        bills = self.bill_repo.get_daily_sales(business_id, start, end)
        if branch_id:
            bills = [b for b in bills if b.get("branch_id") == branch_id]

        total_sales = sum(b.get("total", 0) for b in bills if b.get("status") == "final")
        total_orders = sum(1 for b in bills if b.get("status") == "final")
        gst_total = sum(b.get("gst_total", 0) for b in bills if b.get("status") == "final")
        
        # Calculate product aggregations
        product_map = {}
        employee_map = {}

        for b in bills:
            if b.get("status") != "final":
                continue
                
            creator = b.get("created_by", "Unknown")
            if creator not in employee_map:
                employee_map[creator] = {"name": creator, "bills_created": 0, "sales_generated": 0}
            employee_map[creator]["bills_created"] += 1
            employee_map[creator]["sales_generated"] += b.get("total", 0)

            for item in b.get("items", []):
                name = item.get("name")
                if name not in product_map:
                    product_map[name] = {"name": name, "quantity": 0, "revenue": 0}
                product_map[name]["quantity"] += item.get("quantity", 0)
                product_map[name]["revenue"] += item.get("quantity", 0) * item.get("price", 0)

        # Sort top products
        top_products = sorted(product_map.values(), key=lambda x: x["revenue"], reverse=True)[:10]

        # Process employee performance
        employee_performance = []
        for emp in employee_map.values():
            bills_created = emp["bills_created"]
            sales_gen = emp["sales_generated"]
            emp["avg_bill"] = sales_gen / bills_created if bills_created > 0 else 0
            employee_performance.append(emp)

        employee_performance.sort(key=lambda x: x["sales_generated"], reverse=True)

        return {
            "total_sales": total_sales,
            "total_orders": total_orders,
            "total_profit": 0, # Assuming 0 for now as requested
            "gst_total": gst_total,
            "top_products": top_products,
            "employee_performance": employee_performance,
            "date_range": {"from": from_date, "to": to_date}
        }

    def get_inventory_report(self, business_id: str, branch_id: str = None):
        inventory = self.inventory_repo.get_by_business(business_id)
        if branch_id:
            inventory = [i for i in inventory if i.get("branch_id") == branch_id]
            
        low_stock = [i for i in inventory if i.get("quantity", 0) <= i.get("low_stock_threshold", 5) and i.get("quantity", 0) > 0]
        out_of_stock = [i for i in inventory if i.get("quantity", 0) <= 0]
        
        # Simplified moving items without extensive history
        # You'd normally join with bills to see real sold_quantity over time
        fast_moving = []
        slow_moving = []

        return {
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
            "fast_moving": fast_moving,
            "slow_moving": slow_moving
        }

    def get_employee_performance(self, business_id: str, from_date: str, to_date: str):
        # We can reuse the sales report since it aggregates employees already
        res = self.get_sales_report(business_id, from_date, to_date)
        return res["employee_performance"]

    def get_gst_report(self, business_id: str, month: int, year: int):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
            
        bills = self.bill_repo.get_daily_sales(business_id, start, end)
        gst_total = sum(b.get("gst_total", 0) for b in bills if b.get("status") == "final")
        total_sales = sum(b.get("total", 0) for b in bills if b.get("status") == "final")
        
        return {
            "business_id": business_id,
            "month": month,
            "year": year,
            "gst_total": gst_total,
            "total_sales": total_sales,
            "total_bills": len([b for b in bills if b.get("status") == "final"])
        }
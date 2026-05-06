from app.repositories.bill_repository import BillRepository


class AIService:
    def __init__(self, db):
        self.bill_repo = BillRepository(db)

    def get_sales_summary(self, business_id: str):
        bills = self.bill_repo.get_by_business(business_id)

        if not bills:
            return {"message": "No data available"}

        total_sales = sum(b["total"] for b in bills)
        avg_sale = total_sales / len(bills)

        # 🔥 EXTENSIBLE STRUCTURE
        return {
            "total_sales": total_sales,
            "average_sale": avg_sale,
            "total_orders": len(bills),
            "insights": self._generate_basic_insights(bills),
        }

   
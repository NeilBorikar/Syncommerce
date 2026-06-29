import io
from typing import Optional, Dict
from openpyxl import Workbook
from app.repositories.customer_repository import CustomerRepository
from app.repositories.bill_repository import BillRepository
from app.utils.logger import logger


class CustomerService:
    def __init__(self, db):
        self.repo = CustomerRepository(db)
        self.bill_repo = BillRepository(db)

    # -------------------------------
    # REGISTER / UPSERT
    # -------------------------------
    def register_customer(self, data: dict) -> Dict:
        """
        Register a new customer. If a customer with the same phone already
        exists under this business, return the existing record instead of
        creating a duplicate.
        """
        try:
            business_id = data["business_id"]
            phone = data["phone"]

            existing = self.repo.get_by_phone(business_id, phone)
            if existing:
                logger.info(f"Customer lookup returned existing record: {existing['id']}")
                return {"customer": existing, "created": False}

            customer = self.repo.create(data)
            logger.info(f"New customer created: {customer['id']}")
            return {"customer": customer, "created": True}

        except Exception as e:
            logger.error("Customer registration failed", exc_info=True)
            raise e

    # -------------------------------
    # LOOKUP BY PHONE
    # -------------------------------
    def lookup_customer(self, business_id: str, phone: str) -> Optional[Dict]:
        """
        Find a customer by phone and enrich with their bill history.
        Returns None if not found.
        """
        try:
            customer = self.repo.get_by_phone(business_id, phone)
            if not customer:
                return None

            bills = self.bill_repo.get_by_business(business_id)
            customer_bills = [
                b for b in bills
                if b.get("customer_id") == customer["id"]
                or b.get("customer_phone") == phone
            ]

            return {
                "customer": customer,
                "bills": customer_bills,
                "bill_count": len(customer_bills),
                "total_spend": customer.get("total_spend", 0.0),
                "favorite_items": customer.get("favorite_items", []),
            }

        except Exception as e:
            logger.error("Customer lookup failed", exc_info=True)
            raise e

    # -------------------------------
    # UPDATE SPEND & FAVORITES
    # -------------------------------
    def update_spend_and_favorites(
        self, customer_id: str, amount: float, items: list
    ) -> Optional[Dict]:
        """Called after a bill is created to keep customer stats current."""
        try:
            return self.repo.update_spend_and_favorites(customer_id, amount, items)
        except Exception as e:
            logger.error("Failed to update customer spend/favorites", exc_info=True)
            raise e

    # -------------------------------
    # GET ALL FOR BUSINESS
    # -------------------------------
    def get_all(self, business_id: str):
        return self.repo.get_by_business(business_id)

    # -------------------------------
    # UPDATE CUSTOMER
    # -------------------------------
    def update_customer(self, customer_id: str, data: dict) -> Optional[Dict]:
        try:
            # Remove None values so we don't overwrite with nulls
            clean_data = {k: v for k, v in data.items() if v is not None}
            updated = self.repo.update(customer_id, clean_data)
            if not updated:
                return None
            logger.info(f"Customer updated: {customer_id}")
            return updated
        except Exception as e:
            logger.error("Customer update failed", exc_info=True)
            raise e

    # -------------------------------
    # EXPORT TO EXCEL
    # -------------------------------
    def export_excel(self, business_id: str) -> bytes:
        """
        Generate an Excel workbook with all customer data for a business.
        Returns raw bytes suitable for StreamingResponse.
        """
        try:
            customers = self.repo.get_by_business(business_id)

            wb = Workbook()
            ws = wb.active
            ws.title = "Customers"

            headers = [
                "ID", "Name", "Phone", "Email",
                "Billing Address", "Shipping Address",
                "Total Spend", "Bill Count",
                "Favorite Items", "Created At",
            ]
            ws.append(headers)

            for c in customers:
                fav_str = ", ".join(
                    f"{f['name']}({f['count']})"
                    for f in c.get("favorite_items", [])
                )
                ws.append([
                    c.get("id", ""),
                    c.get("name", ""),
                    c.get("phone", ""),
                    c.get("email", ""),
                    c.get("billing_address", ""),
                    c.get("shipping_address", ""),
                    c.get("total_spend", 0),
                    c.get("bill_count", 0),
                    fav_str,
                    str(c.get("created_at", "")),
                ])

            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            return buffer.read()

        except Exception as e:
            logger.error("Customer Excel export failed", exc_info=True)
            raise e

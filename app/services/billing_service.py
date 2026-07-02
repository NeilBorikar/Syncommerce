from app.repositories.bill_repository import BillRepository
from app.repositories.inventory_repository import InventoryRepository
from app.services.customer_service import CustomerService
from app.utils.logger import logger


class BillingService:
    def __init__(self, db, sync_engine=None):
        self.repo = BillRepository(db)
        self.inventory_repo = InventoryRepository(db)
        self.customer_service = CustomerService(db)
        self.sync_engine = sync_engine

    def _calculate_total(self, items, discount=0, tax=0):
        total = sum(item["quantity"] * item["price"] for item in items)
        total -= discount
        total += tax
        return max(total, 0)
        
    def _calculate_gst(self, items):
        gst_total = 0.0
        for item in items:
            try:
                gst_percent = float(item.get("gst_percent", 0.0))
            except (ValueError, TypeError):
                gst_percent = 0.0
            item_gst = item["price"] * item["quantity"] * (gst_percent / 100)
            gst_total += item_gst
        return gst_total

    async def create_bill(self, data: dict):
        try:
            # Look up customer if phone provided
            customer_phone = data.get("customer_phone")
            business_id = data.get("business_id")
            customer_id = data.get("customer_id")
            
            if customer_phone and not customer_id:
                cust_res = self.customer_service.lookup_customer(business_id, customer_phone)
                if cust_res and cust_res.get("customer"):
                    cust = cust_res["customer"]
                    customer_id = cust["id"]
                    data["customer_id"] = customer_id
                    data["customer_name"] = cust.get("name", data.get("customer_name"))
                    if not data.get("billing_address"):
                        data["billing_address"] = cust.get("billing_address", "")
                    if not data.get("shipping_address"):
                        data["shipping_address"] = cust.get("shipping_address", "")
                else:
                    # Auto-register new customer
                    new_cust_data = {
                        "business_id": business_id,
                        "phone": customer_phone,
                        "name": data.get("customer_name") or "Walk-in",
                        "total_spend": 0,
                        "bill_count": 0,
                        "favorite_items": []
                    }
                    new_cust = self.customer_service.register_customer(new_cust_data)
                    if new_cust and new_cust.get("customer"):
                        customer_id = new_cust["customer"]["id"]
                        data["customer_id"] = customer_id

            # Calculate GST
            gst_total = self._calculate_gst(data["items"])
            data["gst_total"] = gst_total
            
            total = self._calculate_total(
                data["items"],
                data.get("discount", 0),
                data.get("tax", 0),
            )
            # Add gst to total if tax isn't already used for it
            total += gst_total

            bill_data = {
                **data,
                "total": total,
                "status": "final",
            }

            bill = self.repo.create(bill_data)
            logger.info(f"Bill created: {bill['id']}")

            # Decrement inventory
            for item in data["items"]:
                # We need to find by name and decrement
                inv_items = self.inventory_repo.search_items(business_id, item["name"])
                for inv in inv_items:
                    if inv["name"] == item["name"]:
                        new_qty = max(0, inv["quantity"] - item["quantity"])
                        self.inventory_repo.update_stock(inv["id"], new_qty)
                        break

            # Update customer spend & favorites
            if customer_id:
                self.customer_service.update_spend_and_favorites(customer_id, total, data["items"])

            # 🔥 REALTIME TRIGGER
            if self.sync_engine:
                await self.sync_engine.handle_bill_created(
                    data["business_id"],
                    bill
                )

            return bill

        except Exception as e:
            logger.error("Bill creation failed", exc_info=True)
            raise e

    def get_business_bills(self, business_id: str):
        return self.repo.get_by_business(business_id)
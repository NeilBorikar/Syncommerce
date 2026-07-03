import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone

async def run():
    client = AsyncIOMotorClient("mongodb+srv://neilborikar25_db_user:Neil1708@cluster0.vrvaenz.mongodb.net/syncommerce_db?retryWrites=true&w=majority")
    db = client["syncommerce_db"]
    
    # Check bills
    bills = await db.bills.find({}).to_list(None)
    print(f"Total bills in DB: {len(bills)}")
    if bills:
        print(f"Sample bill created_at: {bills[0].get('created_at')}")
    print(f"Total bills in DB: {len(bills)}")
    if bills:
        import pprint
        pprint.pprint(bills[0])
        print("Status is:", bills[0].get("status"))

asyncio.run(run())

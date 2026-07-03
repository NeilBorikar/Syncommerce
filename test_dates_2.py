import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

async def run():
    client = AsyncIOMotorClient("mongodb+srv://neilborikar25_db_user:Neil1708@cluster0.vrvaenz.mongodb.net/syncommerce_db?retryWrites=true&w=majority")
    db = client["syncommerce_db"]
    
    from_date = "2026-06-03"
    to_date = "2026-07-03"
    
    try:
        start = datetime.fromisoformat(from_date.replace("Z", "+00:00"))
        end = datetime.fromisoformat(to_date.replace("Z", "+00:00"))
    except ValueError:
        start = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end = (datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)).replace(tzinfo=timezone.utc)
        
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
        
    business_id = "6a42a74288aeff9918a4dc9e" # Hardi business id
    print(f"Querying business {business_id} from {start} to {end}")
    
    bills = await db.bills.find({
        "business_id": business_id,
        "created_at": {"$gte": start, "$lte": end}
    }).to_list(None)
    
    print(f"Bills found: {len(bills)}")

asyncio.run(run())

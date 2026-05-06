from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import mongo, async_mongo
from app.utils.logger import logger

# -------------------------------
# API ROUTES
# -------------------------------
from app.api.v1 import auth, users, bills, drafts, inventory, reports

# -------------------------------
# REALTIME
# -------------------------------
from app.realtime.manager import ConnectionManager
from app.realtime.sync_engine import SyncEngine


# Initialize realtime components
manager = ConnectionManager()
sync_engine = SyncEngine(manager)


# -------------------------------
# LIFESPAN EVENTS
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting SynCommerce AI Backend...")

    try:
        mongo.connect()
        await async_mongo.connect()

        logger.info("All services started successfully")

    except Exception as e:
        logger.error("Startup failed", exc_info=True)
        raise e

    yield

    logger.info("Shutting down services...")

    mongo.close()
    await async_mongo.close()

    logger.info("Shutdown complete")


# -------------------------------
# CREATE APP
# -------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)


# -------------------------------
# ROOT ROUTE
# -------------------------------
@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running 🚀",
        "env": settings.ENV
    }


# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENV,
    }


# -------------------------------
# API ROUTE REGISTRATION (v1)
# -------------------------------
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(bills.router, prefix="/api/v1/bills", tags=["Bills"])
app.include_router(drafts.router, prefix="/api/v1/drafts", tags=["Drafts"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])


# -------------------------------
# WEBSOCKET ENDPOINT
# -------------------------------
@app.websocket("/ws/{business_id}")
async def websocket_endpoint(websocket: WebSocket, business_id: str):
    await manager.connect(websocket, business_id)

    try:
        while True:
            data = await websocket.receive_json()

            # Basic ping-pong
            if data.get("type") == "PING":
                await websocket.send_json({"type": "PONG"})
                continue

            # Optional: route events
            logger.info(f"Received WS event: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, business_id)
        logger.info(f"WebSocket disconnected: {business_id}")

    except Exception as e:
        logger.error("WebSocket error", exc_info=True)
        manager.disconnect(websocket, business_id)
import os

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )
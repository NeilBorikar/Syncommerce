from fastapi import WebSocket
from typing import Dict, List
from app.utils.logger import logger


class ConnectionManager:
    def __init__(self):
        # business_id -> list of connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, business_id: str):
        await websocket.accept()

        if business_id not in self.active_connections:
            self.active_connections[business_id] = []

        self.active_connections[business_id].append(websocket)

        logger.info(f"Client connected to business {business_id}")

    def disconnect(self, websocket: WebSocket, business_id: str):
        self.active_connections[business_id].remove(websocket)

        logger.info(f"Client disconnected from business {business_id}")

    async def broadcast(self, business_id: str, message: dict):
        if business_id not in self.active_connections:
            return

        for connection in self.active_connections[business_id]:
            try:
                await connection.send_json(message)
            except Exception:
                logger.error("WebSocket send failed", exc_info=True)


# Global manager
ws_manager = ConnectionManager()
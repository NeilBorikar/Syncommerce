from fastapi import WebSocket
from typing import Dict, List
from app.utils.logger import logger


class ConnectionManager:
    def __init__(self):
        # business_id -> list of websockets
        self.connections: Dict[str, List[WebSocket]] = {}

    # -------------------------------
    # CONNECT
    # -------------------------------
    async def connect(self, websocket: WebSocket, business_id: str):
        await websocket.accept()

        if business_id not in self.connections:
            self.connections[business_id] = []

        self.connections[business_id].append(websocket)

        logger.info(f"User connected to business {business_id}")

    # -------------------------------
    # DISCONNECT
    # -------------------------------
    def disconnect(self, websocket: WebSocket, business_id: str):
        if business_id in self.connections:
            if websocket in self.connections[business_id]:
                self.connections[business_id].remove(websocket)

        logger.info(f"User disconnected from business {business_id}")

    # -------------------------------
    # BROADCAST
    # -------------------------------
    async def broadcast(self, business_id: str, message: dict):
        if business_id not in self.connections:
            return

        dead_connections = []

        for connection in self.connections[business_id]:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        # Cleanup dead sockets
        for conn in dead_connections:
            self.connections[business_id].remove(conn)
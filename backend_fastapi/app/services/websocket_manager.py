import json
import asyncio
from typing import List, Dict, Any
from fastapi import WebSocket

class HotlineWebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event_type: str, data: Dict[str, Any]):
        message = {
            "type": event_type,
            "data": data
        }
        text = json.dumps(message, default=str)
        dead = []
        for ws in self.active_connections:
            try:
                await ws.send_text(text)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

ws_manager = HotlineWebSocketManager()

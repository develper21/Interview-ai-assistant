"""
WebSocket router for real-time features
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

router = APIRouter()

# Store active connections
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/interview")
async def interview_websocket(websocket: WebSocket):
    """WebSocket for interview real-time features"""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            message_type = message_data.get("type")

            if message_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

            elif message_type == "subscribe":
                session_id = message_data.get("session_id")
                if session_id:
                    active_connections[session_id] = websocket

            elif message_type == "unsubscribe":
                session_id = message_data.get("session_id")
                if session_id and session_id in active_connections:
                    del active_connections[session_id]

    except WebSocketDisconnect:
        # Clean up connections
        for session_id, conn in list(active_connections.items()):
            if conn == websocket:
                del active_connections[session_id]


async def broadcast_to_session(session_id: str, message: dict):
    """Broadcast message to all connections for a session"""
    if session_id in active_connections:
        websocket = active_connections[session_id]
        try:
            await websocket.send_text(json.dumps(message))
        except:
            # Connection is dead, remove it
            del active_connections[session_id]

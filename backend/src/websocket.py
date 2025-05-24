import asyncio
import websockets
import json
from database import fetch_cached_weapon

clients = set()  # Store connected clients

async def notify_clients(message):
    """Broadcasts patch updates or loadout changes to all connected users."""
    if clients:  # Only send if users are connected
        await asyncio.wait([ws.send(message) for ws in clients])

async def websocket_handler(websocket, path):
    """Handles incoming WebSocket connections & listens for updates."""
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("action") == "fetch_weapon":
                weapon_data = fetch_cached_weapon(data.get("weapon_name"))
                await websocket.send(json.dumps({"type": "weapon_update", "data": weapon_data}))
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def start_websocket_server():
    """Launches the WebSocket server."""
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Keeps the server running

if __name__ == "__main__":
    print("Starting WebSocket server for real-time updates...")
    asyncio.run(start_websocket_server())
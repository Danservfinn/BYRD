"""
BYRD FastAPI Server
Provides REST API and WebSocket streaming for the visualization UI.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from byrd import BYRD
from event_bus import EventBus, Event, EventType, event_bus


# =============================================================================
# CONNECTION MANAGER
# =============================================================================

class ConnectionManager:
    """Manages WebSocket connections for event streaming."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        print(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """Send message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected
        for conn in disconnected:
            self.active_connections.discard(conn)

    async def broadcast_event(self, event: Event):
        """Broadcast an event to all clients."""
        await self.broadcast(event.to_json())


manager = ConnectionManager()


# =============================================================================
# APP LIFECYCLE
# =============================================================================

byrd_instance: Optional[BYRD] = None
byrd_task: Optional[asyncio.Task] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle - start/stop BYRD."""
    global byrd_instance, byrd_task

    # Subscribe connection manager to event bus
    event_bus.subscribe_async(manager.broadcast_event)

    # Initialize BYRD (but don't start yet - let API control that)
    byrd_instance = BYRD()

    yield

    # Cleanup
    if byrd_task:
        byrd_task.cancel()
    if byrd_instance:
        await byrd_instance.memory.close()


# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="BYRD API",
    description="API for BYRD - Bootstrapped Yearning via Reflective Dreaming",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class StatusResponse(BaseModel):
    running: bool
    memory_stats: Dict[str, int]
    dream_count: int
    seek_count: int
    unfulfilled_desires: List[Dict]
    capabilities: List[str]
    recent_insights: List[str]


class HistoryResponse(BaseModel):
    events: List[Dict]
    total: int


class ResetResponse(BaseModel):
    success: bool
    message: str


# =============================================================================
# REST ENDPOINTS
# =============================================================================

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get current BYRD status."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        stats = await byrd_instance.memory.stats()
        desires = await byrd_instance.memory.get_unfulfilled_desires(limit=5)
        capabilities = await byrd_instance.memory.get_capabilities()

        return StatusResponse(
            running=byrd_instance._running,
            memory_stats=stats,
            dream_count=byrd_instance.dreamer.dream_count(),
            seek_count=byrd_instance.seeker.seek_count(),
            unfulfilled_desires=[
                {"description": d.get("description", ""), "type": d.get("type", ""), "intensity": d.get("intensity", 0)}
                for d in desires
            ],
            capabilities=[c.get("name", "") for c in capabilities],
            recent_insights=byrd_instance.dreamer.recent_insights()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(limit: int = 100, event_type: Optional[str] = None):
    """Get event history from the event bus."""
    event_types = None
    if event_type:
        try:
            event_types = [EventType(event_type)]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid event type: {event_type}")

    events = event_bus.get_history(limit=limit, event_types=event_types)

    return HistoryResponse(
        events=[e.to_dict() for e in events],
        total=len(events)
    )


@app.get("/api/experiences")
async def get_experiences(limit: int = 50, type: Optional[str] = None):
    """Get recent experiences from memory."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        experiences = await byrd_instance.memory.get_recent_experiences(limit=limit, type=type)
        return {"experiences": experiences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/beliefs")
async def get_beliefs(limit: int = 50, min_confidence: float = 0.0):
    """Get beliefs from memory."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        beliefs = await byrd_instance.memory.get_beliefs(min_confidence=min_confidence, limit=limit)
        return {"beliefs": beliefs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/desires")
async def get_desires(limit: int = 20):
    """Get unfulfilled desires from memory."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        desires = await byrd_instance.memory.get_unfulfilled_desires(limit=limit)
        return {"desires": desires}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/capabilities")
async def get_capabilities():
    """Get capabilities from memory."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        capabilities = await byrd_instance.memory.get_capabilities()
        return {"capabilities": capabilities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/start")
async def start_byrd():
    """Start BYRD background processes."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if byrd_instance._running:
        return {"message": "BYRD already running"}

    # Start in background task
    byrd_task = asyncio.create_task(byrd_instance.start())

    await event_bus.emit(Event(
        type=EventType.SYSTEM_STARTED,
        data={"message": "BYRD started"}
    ))

    return {"message": "BYRD started"}


@app.post("/api/stop")
async def stop_byrd():
    """Stop BYRD background processes."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    byrd_instance.dreamer.stop()
    byrd_instance.seeker.stop()
    byrd_instance._running = False

    if byrd_task:
        byrd_task.cancel()
        byrd_task = None

    await event_bus.emit(Event(
        type=EventType.SYSTEM_STOPPED,
        data={"message": "BYRD stopped"}
    ))

    return {"message": "BYRD stopped"}


@app.post("/api/reset", response_model=ResetResponse)
async def reset_byrd():
    """Reset BYRD - clear all memory and trigger fresh awakening."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        # 1. Stop if running
        if byrd_instance._running:
            byrd_instance.dreamer.stop()
            byrd_instance.seeker.stop()
            byrd_instance._running = False

            if byrd_task:
                byrd_task.cancel()
                byrd_task = None

        # 2. Clear memory
        await byrd_instance.memory.connect()
        await byrd_instance.memory.clear_all()

        # 3. Clear event history
        event_bus.clear_history()

        # 4. Emit reset event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_RESET,
            data={"message": "Memory cleared, preparing for awakening"}
        ))

        # 5. Re-initialize capabilities and awaken
        await byrd_instance._init_innate_capabilities()
        await byrd_instance._awaken()

        # 6. Restart background processes
        byrd_task = asyncio.create_task(byrd_instance.start())

        return ResetResponse(
            success=True,
            message="BYRD reset complete. Awakened with 'What is happening?'"
        )

    except Exception as e:
        return ResetResponse(
            success=False,
            message=f"Reset failed: {str(e)}"
        )


# =============================================================================
# WEBSOCKET ENDPOINT
# =============================================================================

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming."""
    await manager.connect(websocket)

    # Send recent history on connect
    history = event_bus.get_history(limit=50)
    for event in history:
        try:
            await websocket.send_text(event.to_json())
        except Exception:
            break

    try:
        while True:
            # Keep connection alive, handle any incoming messages
            data = await websocket.receive_text()

            # Handle ping/pong or commands
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
BYRD FastAPI Server
Provides REST API and WebSocket streaming for the visualization UI.
"""

import asyncio
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional, Set

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from byrd import BYRD

# =============================================================================
# SELF-MODIFICATION INFRASTRUCTURE
# =============================================================================

# Directory where BYRD lives
BYRD_DIR = Path(__file__).parent

# Files that BYRD can modify (and that reset will restore)
MODIFIABLE_FILES = [
    "byrd.py",
    "dreamer.py",
    "seeker.py",
    "actor.py",
    "memory.py",
    "llm_client.py",
    "config.yaml",
    "aitmpl_client.py",
    "event_bus.py",
    "server.py",
]


def restore_code_from_git() -> tuple:
    """
    Restore all modifiable files to their last committed state.
    Returns (restored_files, failed_files) tuple.
    """
    restored = []
    failed = []

    for filename in MODIFIABLE_FILES:
        filepath = BYRD_DIR / filename
        if filepath.exists():
            try:
                result = subprocess.run(
                    ["git", "checkout", "--", filename],
                    cwd=BYRD_DIR,
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    restored.append(filename)
                else:
                    failed.append(filename)
            except Exception as e:
                failed.append(filename)

    return restored, failed


def restart_server():
    """Restart the server process to pick up code changes."""
    # Use os.execv to replace current process
    os.execv(sys.executable, [sys.executable, str(BYRD_DIR / "server.py")])


from event_bus import EventBus, Event, EventType, event_bus
from llm_client import create_llm_client, LLMError


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
keep_alive_task: Optional[asyncio.Task] = None


async def keep_alive_ping():
    """Self-ping to prevent cloud provider (Koyeb) from sleeping the service."""
    port = int(os.environ.get("PORT", 8000))
    while True:
        await asyncio.sleep(300)  # Every 5 minutes
        try:
            async with httpx.AsyncClient() as client:
                await client.get(f"http://localhost:{port}/api/status", timeout=10)
        except Exception:
            pass  # Ignore failures - this is just a keep-alive


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle - start/stop BYRD."""
    global byrd_instance, byrd_task, keep_alive_task

    # Subscribe connection manager to event bus
    event_bus.subscribe_async(manager.broadcast_event)

    # Initialize BYRD (but don't start yet - let API control that)
    byrd_instance = BYRD()

    # Connect to Neo4j immediately to avoid "Driver closed" on first request
    await byrd_instance.memory.connect()

    # Start keep-alive ping for cloud deployment
    if os.environ.get("CLOUD_DEPLOYMENT"):
        keep_alive_task = asyncio.create_task(keep_alive_ping())

    yield

    # Cleanup
    if keep_alive_task:
        keep_alive_task.cancel()
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
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.koyeb.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML visualizations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/{filename}.html")
async def serve_html(filename: str):
    """Serve HTML visualization files."""
    filepath = os.path.join(BASE_DIR, f"{filename}.html")
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="text/html")
    raise HTTPException(status_code=404, detail=f"File {filename}.html not found")

# Serve 3D models (cat.glb, etc.)
models_dir = os.path.join(BASE_DIR, "models")
if os.path.exists(models_dir):
    app.mount("/models", StaticFiles(directory=models_dir), name="models")


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class StatusResponse(BaseModel):
    running: bool
    started_at: Optional[str] = None
    memory_stats: Dict[str, int]
    dream_count: int
    seek_count: int
    unfulfilled_desires: List[Dict]
    capabilities: List[str]
    recent_insights: List[str]
    recent_reflections: List[Dict] = []
    recent_beliefs: List[Dict] = []
    llm_provider: str
    llm_model: str


class HistoryResponse(BaseModel):
    events: List[Dict]
    total: int


class ResetRequest(BaseModel):
    seed_question: Optional[str] = None
    hard_reset: bool = True  # Default: complete wipe with no auto-awakening


class ResetResponse(BaseModel):
    success: bool
    message: str


class LLMConfigResponse(BaseModel):
    provider: str
    model: str
    available_providers: List[str]


class LLMConfigUpdate(BaseModel):
    provider: str
    model: str


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

        # Get recent reflections and beliefs for narrative summary
        reflections = await byrd_instance.memory.get_recent_reflections(limit=5)
        beliefs = await byrd_instance.memory.get_beliefs(limit=10)

        # Get LLM info
        client = byrd_instance.llm_client
        model_name = client.model_name
        if "/" in model_name:
            llm_provider, llm_model = model_name.split("/", 1)
        else:
            llm_provider = "ollama"  # Default for local models
            llm_model = model_name

        # Format started_at timestamp
        started_at = None
        if byrd_instance._started_at:
            started_at = byrd_instance._started_at.isoformat()

        return StatusResponse(
            running=byrd_instance._running,
            started_at=started_at,
            memory_stats=stats,
            dream_count=byrd_instance.dreamer.dream_count(),
            seek_count=byrd_instance.seeker.seek_count(),
            unfulfilled_desires=[
                {"description": d.get("description", ""), "type": d.get("type", ""), "intensity": d.get("intensity", 0)}
                for d in desires
            ],
            capabilities=[c.get("name", "") for c in capabilities],
            recent_insights=byrd_instance.dreamer.recent_insights(),
            recent_reflections=[
                {"keys": list(r.get("raw_output", {}).keys()) if isinstance(r.get("raw_output"), dict) else [],
                 "output": r.get("raw_output", {}),
                 "timestamp": str(r.get("timestamp", "")) if r.get("timestamp") else ""}
                for r in reflections
            ],
            recent_beliefs=[
                {"content": b.get("content", ""), "confidence": b.get("confidence", 0)}
                for b in beliefs
            ],
            llm_provider=llm_provider,
            llm_model=llm_model
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
async def reset_byrd(request: ResetRequest = None):
    """Reset BYRD - clear all memory. By default does hard reset (no auto-awakening)."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    # Extract options from request
    seed_question = request.seed_question if request else None
    hard_reset = request.hard_reset if request else True  # Default to hard reset

    try:
        # 1. Stop if running
        if byrd_instance._running:
            byrd_instance.dreamer.stop()
            byrd_instance.seeker.stop()
            byrd_instance._running = False

            if byrd_task:
                byrd_task.cancel()
                byrd_task = None

        # 2. Reset component state (counters, etc.)
        byrd_instance.dreamer.reset()
        byrd_instance.seeker.reset()

        # 3. Clear memory (Neo4j database) - complete wipe
        await byrd_instance.memory.connect()
        await byrd_instance.memory.clear_all()

        # 4. Clear event history
        event_bus.clear_history()

        # 5. Emit reset event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_RESET,
            data={"message": "Memory cleared - database is empty", "hard_reset": hard_reset}
        ))

        if hard_reset:
            # 5. Restore code from git
            restored, failed = restore_code_from_git()
            restored_msg = f"{len(restored)} files restored"
            if restored:
                print(f"📂 Restored {len(restored)} files from git: {', '.join(restored)}")

            # 6. Schedule server restart (after response is sent)
            async def delayed_restart():
                await asyncio.sleep(0.5)  # Give time for response to be sent
                restart_server()

            asyncio.create_task(delayed_restart())

            # Hard reset: Return success, server will restart
            return ResetResponse(
                success=True,
                message=f"Full reset complete. Database cleared, {restored_msg}. Server restarting..."
            )

        # Soft reset: Re-awaken and restart (legacy behavior)
        await byrd_instance._awaken(seed_question=seed_question)

        # Restart background processes
        byrd_task = asyncio.create_task(byrd_instance.start())

        # Emit system started event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": "BYRD restarted after reset"}
        ))

        used_question = seed_question if seed_question else "Who am I?"
        return ResetResponse(
            success=True,
            message=f"BYRD reset complete. Awakened with '{used_question}'"
        )

    except Exception as e:
        return ResetResponse(
            success=False,
            message=f"Reset failed: {str(e)}"
        )


class AwakenRequest(BaseModel):
    seed_question: Optional[str] = None


@app.post("/api/awaken", response_model=ResetResponse)
async def awaken_byrd(request: AwakenRequest = None):
    """Awaken BYRD after a hard reset. Creates initial experiences and starts dreaming."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    seed_question = request.seed_question if request else None

    try:
        # Awaken (which internally records capability experiences and ego seeds)
        await byrd_instance._awaken(seed_question=seed_question)

        # Start background processes
        byrd_task = asyncio.create_task(byrd_instance.start())

        # Emit system started event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": "BYRD awakened"}
        ))

        used_question = seed_question if seed_question else "Who am I?"
        return ResetResponse(
            success=True,
            message=f"BYRD awakened with '{used_question}'"
        )

    except Exception as e:
        return ResetResponse(
            success=False,
            message=f"Awakening failed: {str(e)}"
        )


# =============================================================================
# LLM CONFIGURATION ENDPOINTS
# =============================================================================

@app.get("/api/llm-config", response_model=LLMConfigResponse)
async def get_llm_config():
    """Get current LLM configuration."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    client = byrd_instance.llm_client
    # Extract provider and model from model_name (format: "provider/model")
    model_name = client.model_name
    if "/" in model_name:
        provider, model = model_name.split("/", 1)
    else:
        provider = "unknown"
        model = model_name

    return LLMConfigResponse(
        provider=provider,
        model=model,
        available_providers=["ollama", "openrouter"]
    )


@app.post("/api/llm-config", response_model=LLMConfigResponse)
async def update_llm_config(config: LLMConfigUpdate):
    """Update LLM configuration (hot-swap provider/model)."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        # Build config dict for new client
        new_config = {
            "provider": config.provider,
            "model": config.model,
            "timeout": 120.0
        }

        # Add provider-specific settings
        if config.provider == "ollama":
            new_config["endpoint"] = "http://localhost:11434/api/generate"
        # OpenRouter uses env var for API key

        # Create new client
        new_client = create_llm_client(new_config)

        # Hot-swap: replace client in BYRD, Dreamer, and Seeker
        byrd_instance.llm_client = new_client
        byrd_instance.dreamer.llm_client = new_client
        byrd_instance.seeker.llm_client = new_client

        print(f"🧠 LLM switched to: {new_client.model_name}")

        # Emit event for UI
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": f"LLM switched to {new_client.model_name}"}
        ))

        return LLMConfigResponse(
            provider=config.provider,
            model=config.model,
            available_providers=["ollama", "openrouter"]
        )

    except LLMError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update LLM: {str(e)}")


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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

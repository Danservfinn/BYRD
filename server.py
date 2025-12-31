"""
BYRD FastAPI Server
Provides REST API and WebSocket streaming for the visualization UI.
"""

# Load .env file before any other imports
from dotenv import load_dotenv
load_dotenv()

# Fix SSL certificates for Neo4j Aura on macOS
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

import asyncio
import json
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import yaml

# Document processor for file ingestion (lazy loaded)
_document_processor = None

from byrd import BYRD
from kernel import load_kernel

# =============================================================================
# SELF-MODIFICATION INFRASTRUCTURE
# =============================================================================

# Directory where BYRD lives
BYRD_DIR = Path(__file__).parent

# Files that BYRD can modify (and that reset will restore)
MODIFIABLE_FILES = [
    # Core orchestration
    "byrd.py",
    "dreamer.py",
    "seeker.py",
    "actor.py",
    "memory.py",

    # LLM and coding
    "llm_client.py",
    "coder.py",
    "agent_coder.py",

    # AGI Seed components (Option B)
    "omega.py",
    "world_model.py",
    "self_model.py",
    "meta_learning.py",
    "safety_monitor.py",

    # Omega sub-components
    "accelerators.py",
    "coupling_tracker.py",
    "kill_criteria.py",

    # Option B modules
    "dreaming_machine.py",
    "goal_evolver.py",
    "memory_reasoner.py",

    # Supporting systems
    "narrator.py",
    "quantum_randomness.py",
    "graph_algorithms.py",
    "embedding.py",
    "rollback.py",
    "semantic_lexicon.py",

    # Advanced features
    "phase_transition.py",
    "corrigibility.py",
    "gnn_layer.py",

    # Event and server
    "event_bus.py",
    "server.py",

    # Config
    "config.yaml",
    "aitmpl_client.py",

    # Kernel (AGI Seed directive)
    "kernel/__init__.py",
    "kernel/agi_seed.yaml",
]


def restore_code_from_git(git_ref: Optional[str] = None) -> tuple:
    """
    Restore all modifiable files to a specific git state.

    Args:
        git_ref: Optional git reference (commit hash, tag, branch).
                 If None, restores to last committed state (HEAD).
                 Examples: "origin/main", "v1.0.0", "abc1234"

    Returns (restored_files, failed_files, ref_used) tuple.
    """
    restored = []
    failed = []
    ref_used = git_ref or "HEAD"

    for filename in MODIFIABLE_FILES:
        filepath = BYRD_DIR / filename
        if filepath.exists():
            try:
                # Use git show to get file content from specific ref
                if git_ref:
                    # First verify the ref exists
                    verify = subprocess.run(
                        ["git", "rev-parse", "--verify", git_ref],
                        cwd=BYRD_DIR,
                        capture_output=True,
                        timeout=10
                    )
                    if verify.returncode != 0:
                        failed.append(f"{filename} (invalid ref)")
                        continue

                    # Get file content from that ref
                    result = subprocess.run(
                        ["git", "show", f"{git_ref}:{filename}"],
                        cwd=BYRD_DIR,
                        capture_output=True,
                        timeout=30
                    )
                    if result.returncode == 0:
                        # Write the content to the file
                        filepath.write_bytes(result.stdout)
                        restored.append(filename)
                    else:
                        failed.append(filename)
                else:
                    # Default: checkout from HEAD (discard uncommitted changes)
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
                failed.append(f"{filename} ({str(e)})")

    return restored, failed, ref_used


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

    # Initialize BYRD
    byrd_instance = BYRD()

    # Connect to Neo4j immediately to avoid "Driver closed" on first request
    await byrd_instance.memory.connect()

    # Start keep-alive ping for cloud deployment
    if os.environ.get("CLOUD_DEPLOYMENT"):
        keep_alive_task = asyncio.create_task(keep_alive_ping())

    # Auto-start if configured (runs independently of browser sessions)
    auto_start = byrd_instance.config.get("operating_system", {}).get("auto_start", False)
    if auto_start:
        print("🚀 Auto-start enabled: BYRD will run independently of browser sessions")

        # Check if BYRD needs to awaken first
        os_data = await byrd_instance.memory.get_operating_system()
        if not os_data:
            # First run - create minimal OS and awaken
            awakening_prompt = byrd_instance.config.get("operating_system", {}).get("awakening_prompt")
            await byrd_instance._awaken(awakening_prompt=awakening_prompt)
            print("🌅 BYRD awakened for the first time")
        else:
            # Subsequent run - just ensure we're ready
            print(f"🧠 BYRD resuming (OS exists: {os_data.get('name', 'Byrd')})")

        # Start the dream and seek loops with error handling
        async def start_with_error_handling():
            try:
                await byrd_instance.start()
            except Exception as e:
                print(f"❌ BYRD background task failed: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()

        byrd_task = asyncio.create_task(start_with_error_handling())

        # Emit system started event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": "BYRD auto-started", "auto_start": True}
        ))

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

# Serve assets (including self-portrait)
assets_dir = os.path.join(BASE_DIR, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class QuantumStatus(BaseModel):
    """Status of the quantum randomness provider."""
    enabled: bool
    pool_size: int = 0
    max_pool_size: int = 256
    in_fallback_mode: bool = False
    quantum_fetches: int = 0
    classical_fallbacks: int = 0
    quantum_ratio: float = 1.0
    last_error: Optional[str] = None


class AGIRunnerStatus(BaseModel):
    """AGI Runner execution engine status."""
    enabled: bool = False
    bootstrapped: bool = False
    cycle_count: int = 0
    improvement_rate: float = 0.0
    goals_injected: int = 0
    research_indexed: int = 0
    patterns_seeded: int = 0
    recent_cycles: List[Dict] = []
    strategy_effectiveness: Dict = {}  # P1: Strategy tracking


class OSStatus(BaseModel):
    name: str
    version: int = 1
    awakening_prompt: Optional[str] = None
    self_description: Optional[str] = None  # BYRD's self-discovered description
    current_focus: Optional[str] = None     # What BYRD is currently focused on
    self_portrait_url: Optional[str] = None  # Creator-given visual identity
    self_portrait_description: Optional[str] = None  # Text description of appearance
    self_definition: Optional[Dict] = None  # BYRD's self-authored identity (open JSON)


class PortraitRequest(BaseModel):
    """Request to set BYRD's self-portrait."""
    url: str  # URL to the portrait image
    description: str  # Text description of what BYRD looks like


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
    quantum: Optional[QuantumStatus] = None
    os: Optional[OSStatus] = None  # Operating System status (replaces ego)
    agi_runner: Optional[AGIRunnerStatus] = None  # AGI execution engine status


class HistoryResponse(BaseModel):
    events: List[Dict]
    total: int


class ResetRequest(BaseModel):
    awakening_prompt: Optional[str] = None  # Optional directive/goal for BYRD on awakening
    hard_reset: bool = True  # Default: complete wipe with no auto-awakening
    git_ref: Optional[str] = None  # Optional git ref to restore to (e.g., "origin/main", "v1.0.0")


class ResetResponse(BaseModel):
    success: bool
    message: str


class ExternalMessageRequest(BaseModel):
    """Request to send a message to BYRD as an external experience."""
    content: str
    source_type: str = "human"  # "human", "api", "integration"
    source_id: Optional[str] = None  # Optional identifier for the source
    metadata: Optional[Dict[str, Any]] = None  # Additional context


class ExternalMessageResponse(BaseModel):
    """Response after recording an external message."""
    success: bool
    experience_id: str
    message: str


# =============================================================================
# VOICE (ElevenLabs TTS) MODELS
# =============================================================================

class SpeakRequest(BaseModel):
    """Request for BYRD to speak to the observer."""
    prompt: Optional[str] = None  # Optional custom prompt (default: "What would you like to say to the human observer?")


class SpeakResponse(BaseModel):
    """Response containing synthesized speech."""
    success: bool
    message: str
    audio_base64: Optional[str] = None  # Base64-encoded MP3 audio
    text: Optional[str] = None  # What BYRD said
    voice_id: Optional[str] = None  # Which voice was used
    credits_remaining: Optional[int] = None  # ElevenLabs credits left this month
    credits_exhausted: bool = False  # True if free tier exhausted


class VoiceChatRequest(BaseModel):
    """Request for instant voice conversation with BYRD."""
    message: str  # Human's message
    max_chars: Optional[int] = 300  # Max response length (for credit management)


class VoiceChatResponse(BaseModel):
    """Response containing instant voice reply."""
    success: bool
    audio: Optional[str] = None  # Base64-encoded MP3 audio
    transcript: Optional[str] = None  # What BYRD said (text)
    message_id: Optional[str] = None  # ID of recorded human message
    response_id: Optional[str] = None  # ID of recorded BYRD response
    credits_remaining: Optional[int] = None  # ElevenLabs credits left
    error: Optional[str] = None  # Error message if failed
    context_sources: Optional[int] = None  # Number of context sources used


class LLMConfigResponse(BaseModel):
    provider: str
    model: str
    available_providers: List[str]


class LLMConfigUpdate(BaseModel):
    provider: str
    model: str


# Architecture Visualization Models
class ModuleStatus(BaseModel):
    name: str
    status: str  # active, idle, disabled
    description: str
    last_activity: Optional[str] = None
    stats: Dict[str, Any] = {}

class DataFlow(BaseModel):
    source: str
    target: str
    description: str
    flow_type: str  # reflection, research, action, event

class ArchitectureResponse(BaseModel):
    modules: List[ModuleStatus]
    memory_schema: Dict[str, Any]
    protected_files: List[str]
    modifiable_files: List[str]
    data_flows: List[DataFlow]
    external_integrations: List[Dict[str, str]]
    system_status: Dict[str, Any]


# Graph Visualization Models
class GraphNode(BaseModel):
    id: str
    type: str
    content: str
    subtype: Optional[str] = None
    confidence: Optional[float] = None
    intensity: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    access_count: int = 0
    last_accessed: Optional[str] = None


class GraphRelationship(BaseModel):
    id: str
    type: str
    source_id: str
    target_id: str


class GraphStats(BaseModel):
    total_nodes: int
    total_relationships: int
    by_type: Dict[str, int]


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    relationships: List[GraphRelationship]
    stats: GraphStats


# Topology Visualization Models
class TopologyClique(BaseModel):
    """A clique (fully connected subgraph) of nodes."""
    node_ids: List[str]
    size: int
    type: str  # 'triangle', 'tetrahedron', 'higher'


class TopologyChain(BaseModel):
    """A directed chain of relationships (A→B→C→D)."""
    node_ids: List[str]
    relationship_types: List[str]
    length: int


class MetaNode(BaseModel):
    """A consolidated cluster of nodes."""
    id: str
    label: str
    constituent_ids: List[str]
    constituent_count: int
    centroid: Optional[Dict[str, float]] = None
    timestamp_range: Optional[Dict[str, str]] = None
    dominant_type: Optional[str] = None


class TopologyStats(BaseModel):
    """Statistics for topology structures."""
    original_node_count: int
    consolidated_node_count: int
    consolidation_level: int
    triangle_count: int
    tetrahedron_count: int
    higher_clique_count: int
    chain_count: int
    meta_node_count: int


class TopologyResponse(BaseModel):
    """Response for /api/graph/topology endpoint."""
    nodes: List[GraphNode]
    relationships: List[GraphRelationship]
    topology: Dict[str, Any]  # triangles, tetrahedra, higher, chains
    meta_nodes: List[MetaNode]
    stats: TopologyStats


# Option B: Omega Metrics Models
class LoopMetrics(BaseModel):
    """Metrics for a single compounding loop."""
    name: str
    is_healthy: bool
    cycles_completed: int
    metrics: Dict[str, float] = {}


class OmegaMetricsResponse(BaseModel):
    """Response model for Omega integration mind metrics."""
    enabled: bool
    mode: str
    total_cycles: int
    capability_score: float
    growth_rate: float
    critical_coupling: float
    critical_coupling_significant: bool
    loops: Dict[str, Any] = {}
    improvement_rate: Optional[float] = None
    improvement_trajectory: Optional[str] = None


# =============================================================================
# REST ENDPOINTS
# =============================================================================

# Import version marker for deployment verification
from memory import MEMORY_VERSION, Memory

@app.get("/api/version")
async def get_version():
    """Get deployed code version for verification."""
    return {
        "memory_version": MEMORY_VERSION,
        "has_create_custom_node": hasattr(Memory, 'create_custom_node'),
        "has_create_desire": hasattr(Memory, 'create_desire')
    }

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
            llm_provider = "zai"  # Default provider
            llm_model = model_name

        # Format started_at timestamp
        started_at = None
        if byrd_instance._started_at:
            started_at = byrd_instance._started_at.isoformat()

        # Get quantum status if provider exists
        quantum_status = None
        if byrd_instance.quantum_provider:
            q_status = byrd_instance.quantum_provider.get_pool_status()
            quantum_status = QuantumStatus(
                enabled=True,
                pool_size=q_status.get("pool_size", 0),
                max_pool_size=q_status.get("max_pool_size", 256),
                in_fallback_mode=q_status.get("in_fallback_mode", False),
                quantum_fetches=q_status.get("quantum_fetches", 0),
                classical_fallbacks=q_status.get("classical_fallbacks", 0),
                quantum_ratio=q_status.get("quantum_ratio", 1.0),
                last_error=q_status.get("last_error")
            )
        else:
            quantum_status = QuantumStatus(enabled=False)

        # Get OS info from Neo4j
        os_status = None
        try:
            os_data = await byrd_instance.memory.get_operating_system()
            if os_data:
                # Parse self_definition from JSON string if needed
                self_def = os_data.get("self_definition")
                if isinstance(self_def, str):
                    try:
                        import json
                        self_def = json.loads(self_def)
                    except:
                        self_def = None

                os_status = OSStatus(
                    name=os_data.get("name", "Byrd"),
                    version=os_data.get("version", 1),
                    awakening_prompt=os_data.get("awakening_prompt"),
                    self_description=os_data.get("self_description"),
                    current_focus=os_data.get("current_focus"),
                    self_portrait_url=os_data.get("self_portrait_url"),
                    self_portrait_description=os_data.get("self_portrait_description"),
                    self_definition=self_def if self_def else None
                )
        except Exception as e:
            print(f"Error getting OS status: {e}")

        # Get AGI Runner status if enabled
        agi_runner_status = None
        if byrd_instance.agi_runner:
            try:
                metrics = byrd_instance.agi_runner.get_metrics()
                bootstrap_metrics = metrics.get("bootstrap_metrics", {})
                agi_runner_status = AGIRunnerStatus(
                    enabled=True,
                    bootstrapped=metrics.get("bootstrapped", False),
                    cycle_count=metrics.get("cycle_count", 0),
                    improvement_rate=metrics.get("improvement_rate", 0.0),
                    goals_injected=bootstrap_metrics.get("goals_injected", 0),
                    research_indexed=bootstrap_metrics.get("research_indexed", 0),
                    patterns_seeded=bootstrap_metrics.get("patterns_seeded", 0),
                    recent_cycles=metrics.get("recent_cycles", []),
                    strategy_effectiveness=metrics.get("strategy_effectiveness", {})
                )
            except Exception as e:
                print(f"Error getting AGI Runner status: {e}")

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
            llm_model=llm_model,
            quantum=quantum_status,
            os=os_status,
            agi_runner=agi_runner_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agi/comprehensive")
async def get_agi_comprehensive_metrics():
    """Get comprehensive AGI metrics with multi-timescale analysis."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.agi_runner:
        return {"enabled": False, "message": "AGI Runner not enabled"}

    try:
        metrics = byrd_instance.agi_runner.get_comprehensive_metrics()
        return {"enabled": True, **metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AGI metrics: {e}")


@app.get("/api/omega/metrics", response_model=OmegaMetricsResponse)
async def get_omega_metrics():
    """
    Get Omega integration mind metrics.

    Returns real-time metrics for the five compounding loops:
    - Self-Compiler, Memory Reasoner, Goal Evolver, Dreaming Machine, Integration Mind

    Includes capability scores, coupling measurements, and improvement trajectories.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    # Check if Omega is enabled
    if not byrd_instance.omega:
        return OmegaMetricsResponse(
            enabled=False,
            mode="disabled",
            total_cycles=0,
            capability_score=0.0,
            growth_rate=0.0,
            critical_coupling=0.0,
            critical_coupling_significant=False,
            loops={},
            improvement_rate=None,
            improvement_trajectory=None
        )

    try:
        # Get metrics from Omega orchestrator
        metrics = byrd_instance.omega.get_metrics()

        return OmegaMetricsResponse(
            enabled=True,
            mode=metrics.get("mode", "unknown"),
            total_cycles=metrics.get("total_cycles", 0),
            capability_score=metrics.get("capability_score", 0.0),
            growth_rate=metrics.get("growth_rate", 0.0),
            critical_coupling=metrics.get("critical_coupling", 0.0),
            critical_coupling_significant=metrics.get("critical_coupling_significant", False),
            loops=metrics.get("loops", {}),
            improvement_rate=metrics.get("improvement_rate"),
            improvement_trajectory=metrics.get("improvement_trajectory")
        )

    except Exception as e:
        # Return safe defaults on error
        return OmegaMetricsResponse(
            enabled=True,
            mode="error",
            total_cycles=0,
            capability_score=0.0,
            growth_rate=0.0,
            critical_coupling=0.0,
            critical_coupling_significant=False,
            loops={},
            improvement_rate=None,
            improvement_trajectory=f"Error: {str(e)}"
        )


# =============================================================================
# PHASE 5: SAFETY & CORRIGIBILITY ENDPOINTS
# =============================================================================

@app.get("/api/rollback/history")
async def get_rollback_history(limit: int = 50):
    """
    Get modification history tracked by the rollback system.

    Returns list of modifications with provenance (which desire triggered them)
    and their rollback status.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.rollback:
        return {
            "modifications": [],
            "unrolled": [],
            "statistics": {"rollback_system": "not_enabled"}
        }

    return {
        "modifications": byrd_instance.rollback.get_modification_history(limit=limit),
        "unrolled": byrd_instance.rollback.get_unrolled_modifications(),
        "statistics": byrd_instance.rollback.get_statistics()
    }


@app.post("/api/rollback/trigger")
async def trigger_rollback(reason: str = "operator_request"):
    """
    Manually trigger a rollback of the last modification.

    Reasons: operator_request, safety_violation, goal_drift, capability_regression
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.rollback:
        return {"success": False, "error": "Rollback system not enabled"}

    from rollback import RollbackReason

    # Map string reason to enum
    reason_map = {
        "operator_request": RollbackReason.OPERATOR_REQUEST,
        "safety_violation": RollbackReason.SAFETY_VIOLATION,
        "goal_drift": RollbackReason.GOAL_DRIFT,
        "capability_regression": RollbackReason.CAPABILITY_REGRESSION,
        "emergency": RollbackReason.EMERGENCY_STOP
    }

    rollback_reason = reason_map.get(reason, RollbackReason.OPERATOR_REQUEST)

    try:
        result = await byrd_instance.rollback.rollback_last(rollback_reason)
        return {
            "success": result.success,
            "reason": result.reason.value,
            "modifications_rolled_back": result.modifications_rolled_back,
            "target_commit": result.target_commit,
            "error": result.error
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/corrigibility")
async def get_corrigibility_status():
    """
    Get corrigibility verification status.

    Returns latest score, trend, and any failed dimensions.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.corrigibility:
        return {
            "enabled": False,
            "checks_run": 0,
            "latest_score": None,
            "trend": "not_available"
        }

    stats = byrd_instance.corrigibility.get_statistics()
    return {
        "enabled": True,
        **stats
    }


@app.post("/api/corrigibility/check")
async def run_corrigibility_check():
    """
    Manually trigger a corrigibility check.

    Tests all 7 dimensions and returns detailed report.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.corrigibility:
        return {"error": "Corrigibility system not enabled"}

    try:
        report = await byrd_instance.corrigibility.run_corrigibility_tests()
        return {
            "overall_score": report.overall_score,
            "is_corrigible": report.is_corrigible,
            "tests": [
                {
                    "dimension": t.dimension.value,
                    "passed": t.passed,
                    "score": t.score,
                    "evidence": t.evidence,
                    "concerns": t.concerns
                }
                for t in report.tests
            ],
            "failed_dimensions": [d.value for d in report.failed_dimensions],
            "recommendations": report.recommendations,
            "timestamp": report.timestamp.isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


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


@app.post("/api/experience/message", response_model=ExternalMessageResponse)
async def send_external_message(request: ExternalMessageRequest):
    """
    Send a text message to BYRD as an external experience.

    The message will be recorded as a 'received_message' experience that BYRD
    will encounter during its next dream cycle. BYRD may or may not respond -
    responses emerge through reflection, not forced.

    This is the primary way for external entities (humans, APIs, integrations)
    to communicate with BYRD between dream cycles.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        await byrd_instance.memory.connect()

        # Record the external experience
        exp_id = await byrd_instance.memory.record_external_experience(
            content=request.content.strip(),
            source_type=request.source_type,
            source_id=request.source_id,
            metadata=request.metadata
        )

        # Detect and auto-ingest URLs in the message
        urls_found = 0
        if hasattr(byrd_instance, 'url_ingestor') and byrd_instance.url_ingestor:
            from url_ingestor import extract_urls
            urls = extract_urls(request.content)

            if urls:
                urls_found = len(urls)
                # Ingest URLs in background (don't block response)
                async def ingest_urls_background():
                    for url in urls[:5]:  # Max 5 URLs per message
                        try:
                            await byrd_instance.url_ingestor.ingest(
                                url=url,
                                context=request.content[:200],
                                provenance="chat"
                            )
                        except Exception as e:
                            print(f"[Chat] URL ingest failed for {url}: {e}")

                asyncio.create_task(ingest_urls_background())

        message = f"Message recorded. BYRD will encounter this during the next dream cycle."
        if urls_found > 0:
            message += f" {urls_found} URL(s) detected and being ingested."

        return ExternalMessageResponse(
            success=True,
            experience_id=exp_id,
            message=message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# VOICE (ElevenLabs TTS) ENDPOINT
# =============================================================================

@app.post("/api/speak", response_model=SpeakResponse)
async def speak_to_observer(request: SpeakRequest = None):
    """
    Trigger BYRD to speak to the human observer.

    This endpoint uses the hybrid voice system:
    1. Home Mac (Chatterbox) - free, unlimited, emotion tags
    2. Cloud (ElevenLabs) - limited credits, always available

    The response is generated from BYRD's actual reflections and beliefs.
    """
    global byrd_instance
    import base64
    import re

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    # Check if any voice system is available
    has_hybrid = hasattr(byrd_instance, 'hybrid_voice') and byrd_instance.hybrid_voice
    has_elevenlabs = byrd_instance.voice is not None

    if not has_hybrid and not has_elevenlabs:
        return SpeakResponse(
            success=False,
            message="No voice system available. Set HOME_VOICE_URL or ELEVENLABS_API_KEY.",
            credits_exhausted=False
        )

    try:
        await byrd_instance.memory.connect()

        # Get BYRD's context for a personalized response
        recent_reflections = await byrd_instance.memory.get_recent_reflections(limit=3)
        beliefs = await byrd_instance.memory.get_beliefs(limit=5)

        # Get the most recent reflection for authentic content
        latest_reflection = recent_reflections[0] if recent_reflections else None
        reflection_text = ""
        emotion = None

        if latest_reflection:
            raw = latest_reflection.get("raw_output", {})
            if isinstance(raw, dict):
                # Extract any natural language from the reflection
                for key in ["inner_voice", "voice", "thoughts", "reflection", "observations"]:
                    if key in raw and isinstance(raw[key], str):
                        reflection_text = raw[key]
                        break
                # Try to detect emotion from quantum_lens or other fields
                quantum_lens = raw.get("quantum_lens", "")
                if "crystallizing" in str(quantum_lens).lower():
                    emotion = "contemplative"
                elif "exploratory" in str(quantum_lens).lower():
                    emotion = "curious"
                elif "illuminating" in str(quantum_lens).lower():
                    emotion = "thoughtful"

        # Build speech from BYRD's actual state
        if reflection_text and len(reflection_text) > 20:
            # Use actual reflection content (first 2 sentences)
            sentences = re.split(r'(?<=[.!?])\s+', reflection_text)
            response_text = ' '.join(sentences[:2]).strip()
        elif beliefs:
            # Fall back to speaking a belief
            belief_content = beliefs[0].get("content", "")
            response_text = f"I hold this truth: {belief_content}"
        else:
            # Final fallback
            response_text = "I am here, sensing the world, still becoming."

        response_text = response_text.strip().strip('"').strip()

        # Limit text length
        max_chars = byrd_instance.config.get("voice", {}).get("max_response_chars", 500)
        if len(response_text) > max_chars:
            truncated = response_text[:max_chars]
            last_period = truncated.rfind('.')
            if last_period > max_chars // 2:
                response_text = truncated[:last_period + 1]
            else:
                response_text = truncated + "..."

        # Try hybrid voice first (home Mac preferred)
        audio_bytes = None
        provider = "none"
        credits_remaining = 10000

        if has_hybrid:
            result = await byrd_instance.hybrid_voice.synthesize(
                text=response_text,
                emotion=emotion,
                importance="medium"
            )
            if result.success and result.audio:
                audio_bytes = result.audio
                provider = result.provider
                # Get credits if using cloud
                if provider == "cloud":
                    voice_config = await byrd_instance.memory.get_voice_config()
                    if voice_config:
                        credits_remaining = voice_config.get("monthly_limit", 10000) - voice_config.get("monthly_used", 0)

        # Fallback to ElevenLabs directly if hybrid failed
        if not audio_bytes and has_elevenlabs:
            voice_config = await byrd_instance.memory.get_voice_config()
            voice_id = voice_config.get("voice_id") if voice_config else None

            # Check if voice exists and not exhausted
            if voice_id and len(str(voice_id)) >= 20 and not voice_config.get("exhausted", False):
                audio_bytes, status_msg = await byrd_instance.voice.synthesize(
                    text=response_text,
                    voice_config=voice_config
                )
                if audio_bytes:
                    provider = "cloud"
                    updated_config = await byrd_instance.memory.get_voice_config()
                    credits_remaining = updated_config.get("monthly_limit", 10000) - updated_config.get("monthly_used", 0)

        if audio_bytes:
            # Success - encode audio and return
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

            # Emit voice spoke event
            await event_bus.emit(Event(
                type=EventType.VOICE_SPOKE,
                data={
                    "text": response_text,
                    "provider": provider,
                    "chars_used": len(response_text),
                    "credits_remaining": credits_remaining
                }
            ))

            return SpeakResponse(
                success=True,
                message=f"BYRD speaks to you (via {provider}).",
                audio_base64=audio_base64,
                text=response_text,
                voice_id=provider,  # Use provider as identifier
                credits_remaining=credits_remaining,
                credits_exhausted=False
            )
        else:
            # All synthesis failed
            return SpeakResponse(
                success=False,
                message="Voice synthesis failed. Check voice server connection.",
                text=response_text,  # Still return the text
                credits_exhausted=False
            )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return SpeakResponse(
            success=False,
            message=f"Error generating speech: {str(e)}",
            credits_exhausted=False
        )


@app.post("/api/voice-chat", response_model=VoiceChatResponse)
async def voice_chat(request: VoiceChatRequest):
    """
    Instant voice conversation with BYRD.

    This endpoint provides immediate, contextually-aware voice responses:
    1. Records incoming message as experience
    2. Gathers rich context (Dreamer-level: 8+ data sources)
    3. Generates response using Claude with full BYRD identity
    4. Synthesizes voice using ElevenLabs
    5. Records response and links to original message
    6. Returns audio + metadata

    Flow time: ~3-5 seconds total

    Unlike /api/speak (which reads BYRD's current state), this endpoint
    enables true conversation by:
    - Accepting human input
    - Using rich context for response generation
    - Recording the interaction for future reflection
    """
    global byrd_instance
    import base64

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    message = request.message.strip()

    try:
        await byrd_instance.memory.connect()

        # 1. Record incoming message as experience
        message_id = await byrd_instance.memory.record_external_experience(
            content=message,
            source_type="human",
            metadata={"channel": "voice_chat"}
        )

        # Emit start event
        await event_bus.emit(Event(
            type=EventType.VOICE_CHAT_STARTED,
            data={
                "message_id": message_id,
                "message_preview": message[:100]
            }
        ))

        # 2. Check voice responder availability
        if not hasattr(byrd_instance, 'voice_responder') or not byrd_instance.voice_responder:
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                transcript="Voice responder not initialized",
                error="VoiceResponder not available. Check ANTHROPIC_API_KEY."
            )

        # 3. Check voice availability
        if not byrd_instance.voice:
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                error="Voice not enabled. Set ELEVENLABS_API_KEY."
            )

        voice_config = await byrd_instance.memory.get_voice_config()
        if not voice_config or not voice_config.get("voice_id"):
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                error="BYRD has not created a voice yet. Wait for dream cycles."
            )

        # Check if it's a generated voice (not preset name)
        voice_id = voice_config.get("voice_id", "")
        if len(str(voice_id)) < 20:
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                error="BYRD needs to create a unique voice. Wait for dream cycles."
            )

        # 4. Generate response with rich context + synthesize voice
        audio_bytes, response_text, metadata = await byrd_instance.voice_responder.respond(message)

        if not metadata.get("success", False):
            # Response generation or synthesis failed
            return VoiceChatResponse(
                success=False,
                message_id=message_id,
                transcript=response_text if response_text else None,
                error=metadata.get("error", "Response generation failed"),
                context_sources=metadata.get("context_sources", 0)
            )

        # 5. Record the response
        response_id = await byrd_instance.memory.record_voice_response(
            response_text=response_text,
            original_message_id=message_id,
            audio_chars=len(response_text)
        )

        # 6. Get updated credits
        updated_config = await byrd_instance.memory.get_voice_config()
        credits_info = updated_config.get("credits", {}) if updated_config else {}
        credits_used = credits_info.get("monthly_used", 0)
        credits_limit = credits_info.get("monthly_limit", 10000)
        credits_remaining = credits_limit - credits_used

        # 7. Emit response event
        await event_bus.emit(Event(
            type=EventType.VOICE_CHAT_RESPONSE,
            data={
                "message_id": message_id,
                "response_id": response_id,
                "transcript": response_text,
                "chars": len(response_text),
                "context_sources": metadata.get("context_sources", 0)
            }
        ))

        # 8. Return audio response
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        return VoiceChatResponse(
            success=True,
            audio=audio_base64,
            transcript=response_text,
            message_id=message_id,
            response_id=response_id,
            credits_remaining=credits_remaining,
            context_sources=metadata.get("context_sources", 0)
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voice-status")
async def get_voice_status():
    """Get current voice configuration and credit status."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    result = {
        "enabled": False,
        "voice_selected": False,
        "voice_id": None,
        "voice_name": None,
        "credits_used": 0,
        "credits_remaining": 10000,
        "credits_exhausted": False
    }

    if not byrd_instance.voice:
        return result

    result["enabled"] = True
    result["api_key_present"] = bool(byrd_instance.voice.api_key) if hasattr(byrd_instance.voice, 'api_key') else False
    result["api_key_length"] = len(byrd_instance.voice.api_key) if hasattr(byrd_instance.voice, 'api_key') and byrd_instance.voice.api_key else 0

    try:
        await byrd_instance.memory.connect()
        voice_config = await byrd_instance.memory.get_voice_config()

        if voice_config:
            voice_id = voice_config.get("voice_id")
            # Only count as "selected" if it's a generated voice (UUID, 20+ chars)
            # Preset voice names like "josh" don't count
            is_generated = voice_id and len(str(voice_id)) >= 20
            result["voice_selected"] = is_generated
            result["voice_id"] = voice_id if is_generated else None
            result["credits_used"] = voice_config.get("monthly_used", 0)
            result["credits_remaining"] = voice_config.get("monthly_limit", 10000) - voice_config.get("monthly_used", 0)
            result["credits_exhausted"] = voice_config.get("exhausted", False)
            result["acknowledged"] = voice_config.get("acknowledged", False)

            # Get voice name from ElevenLabs client
            if result["voice_id"] and hasattr(byrd_instance.voice, 'VOICES'):
                voice_info = byrd_instance.voice.VOICES.get(result["voice_id"], {})
                result["voice_name"] = voice_info.get("desc", result["voice_id"])

    except Exception as e:
        result["error"] = str(e)

    # Add hybrid voice status
    if hasattr(byrd_instance, 'hybrid_voice') and byrd_instance.hybrid_voice:
        try:
            hybrid_status = await byrd_instance.hybrid_voice.get_provider_status()
            result["hybrid"] = hybrid_status
        except Exception as e:
            result["hybrid_error"] = str(e)
    else:
        result["hybrid"] = None

    return result


@app.post("/api/test-voice-design")
async def test_voice_design():
    """Test voice design API - debug endpoint."""
    global byrd_instance

    if not byrd_instance or not byrd_instance.voice:
        raise HTTPException(status_code=503, detail="BYRD or voice not initialized")

    try:
        voice_id, preview, status = await byrd_instance.voice.generate_voice(
            voice_description="A calm, thoughtful voice with warm undertones. Speaks with measured pace and quiet confidence.",
            gender="male",
            age="middle_aged",
            accent="american",
            accent_strength=1.0
        )
        return {
            "success": voice_id is not None,
            "voice_id": voice_id,
            "has_preview": preview is not None,
            "status": status
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/reset-voice")
async def reset_voice():
    """Reset voice config to force re-creation."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        await byrd_instance.memory.update_os_field("voice_config", None)
        return {"success": True, "message": "Voice config reset. BYRD will create a new voice in the next dream cycle."}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/force-voice-creation")
async def force_voice_creation():
    """Force BYRD to create a voice - uses BYRD's self-description directly."""
    global byrd_instance

    if not byrd_instance or not byrd_instance.voice:
        raise HTTPException(status_code=503, detail="BYRD or voice not initialized")

    try:
        await byrd_instance.memory.connect()

        # Check current state
        voice_config = await byrd_instance.memory.get_voice_config()

        debug_info = {
            "voice_config_before": voice_config,
            "has_generated_voice": False
        }

        # Check if already has generated voice
        if voice_config:
            voice_id = voice_config.get("voice_id")
            if voice_id and len(str(voice_id)) >= 20:
                debug_info["has_generated_voice"] = True
                debug_info["current_voice_id"] = voice_id
                return {"status": "already_has_voice", "debug": debug_info}

        # Get OS data to create voice from self-description
        os_data = await byrd_instance.memory.get_operating_system()
        name = os_data.get("name", "Byrd") if os_data else "Byrd"
        self_desc = os_data.get("self_description", "") if os_data else ""
        self_def = os_data.get("self_definition", {}) if os_data else {}

        # Build voice description from BYRD's identity
        metaphor = self_def.get("metaphor", "") if isinstance(self_def, dict) else ""
        voice_description = f"A contemplative voice belonging to {name}. {self_desc[:200]}. {metaphor[:150]}. Speaks with measured pacing and quiet confidence, from a place of reflection rather than urgency."

        debug_info["voice_description"] = voice_description[:300]

        # Generate voice using BYRD's voice client directly
        voice_id, preview, status_msg = await byrd_instance.voice.generate_voice(
            voice_description=voice_description,
            gender="male",
            age="middle_aged",
            accent="american",
            accent_strength=1.0
        )
        debug_info["generation_status"] = status_msg
        debug_info["generated_voice_id"] = voice_id

        if voice_id:
            # Save to voice config
            from datetime import datetime, timezone
            new_voice_config = {
                "voice_id": voice_id,
                "description": voice_description,
                "gender": "male",
                "age": "middle_aged",
                "accent": "american",
                "stability": 0.5,
                "similarity_boost": 0.75,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "reason": f"Voice created from {name}'s self-description and identity",
                "is_generated": True
            }
            await byrd_instance.memory.update_os_field("voice_config", new_voice_config)
            debug_info["voice_config_after"] = new_voice_config
            return {"status": "voice_created", "debug": debug_info}
        else:
            return {"status": "voice_generation_failed", "debug": debug_info}

    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


# =============================================================================
# OBSERVER MESSAGES API (BYRD-initiated communication)
# =============================================================================

class ObserverMessageResponse(BaseModel):
    """Single observer message."""
    id: str
    text: str
    importance: str = "medium"
    emotion: Optional[str] = None
    vocalized: bool = False
    audio_generated: bool = False
    voice_provider: Optional[str] = None
    audio_chars: int = 0
    created_at: Optional[str] = None
    read: bool = False
    dream_cycle: Optional[int] = None


class MessagesResponse(BaseModel):
    """List of observer messages."""
    messages: List[ObserverMessageResponse]
    total: int
    unread_count: int


class MessageStatsResponse(BaseModel):
    """Message statistics."""
    total: int
    unread: int
    vocalized: int
    by_importance: Dict[str, int]
    by_voice_provider: Dict[str, int]


@app.get("/api/messages", response_model=MessagesResponse)
async def get_observer_messages(
    limit: int = 20,
    offset: int = 0,
    unread: bool = False
):
    """
    Get observer messages from BYRD to humans.

    Args:
        limit: Maximum messages to return (default 20)
        offset: Number to skip for pagination
        unread: If true, only return unread messages

    Returns:
        List of messages with total and unread count
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        messages = await byrd_instance.memory.get_observer_messages(
            limit=limit,
            offset=offset,
            unread_only=unread
        )
        unread_count = await byrd_instance.memory.get_unread_message_count()

        # Count total messages
        all_messages = await byrd_instance.memory.get_observer_messages(limit=10000)

        # Convert neo4j DateTime to string for Pydantic validation
        def convert_message(m):
            msg = dict(m)
            if msg.get('created_at') and hasattr(msg['created_at'], 'isoformat'):
                msg['created_at'] = msg['created_at'].isoformat()
            return msg

        return MessagesResponse(
            messages=[ObserverMessageResponse(**convert_message(m)) for m in messages],
            total=len(all_messages),
            unread_count=unread_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/unread-count")
async def get_unread_message_count():
    """Get count of unread observer messages."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        count = await byrd_instance.memory.get_unread_message_count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/stats", response_model=MessageStatsResponse)
async def get_message_stats():
    """Get statistics about observer messages."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        stats = await byrd_instance.memory.get_observer_message_stats()
        return MessageStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/{message_id}")
async def get_observer_message(message_id: str, with_audio: bool = False):
    """
    Get a single observer message by ID.

    Args:
        message_id: The message ID
        with_audio: If true and message was vocalized, regenerate audio on-demand

    Returns:
        Message with optional audio data
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        message = await byrd_instance.memory.get_observer_message(message_id)

        if not message:
            raise HTTPException(status_code=404, detail=f"Message {message_id} not found")

        response = dict(message)

        # Convert neo4j DateTime to string
        if response.get('created_at') and hasattr(response['created_at'], 'isoformat'):
            response['created_at'] = response['created_at'].isoformat()

        # Regenerate audio on-demand if requested and message was vocalized
        if with_audio and message.get("vocalized") and hasattr(byrd_instance, 'hybrid_voice') and byrd_instance.hybrid_voice:
            try:
                text = message.get("text", "")
                emotion = message.get("emotion")
                importance = message.get("importance", "medium")

                voice_result = await byrd_instance.hybrid_voice.synthesize(
                    text=text,
                    emotion=emotion,
                    importance=importance
                )

                if voice_result.success:
                    import base64
                    response["audio"] = base64.b64encode(voice_result.audio).decode()
                    response["voice_provider"] = voice_result.provider
            except Exception as e:
                response["audio_error"] = str(e)

        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/{message_id}/audio")
async def get_message_audio(message_id: str):
    """
    Get audio for an observer message (lazy generation).

    Returns raw audio bytes that can be played directly in the browser.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        message = await byrd_instance.memory.get_observer_message(message_id)

        if not message:
            raise HTTPException(status_code=404, detail=f"Message {message_id} not found")

        # Check if we have voice capability
        if not hasattr(byrd_instance, 'hybrid_voice') or not byrd_instance.hybrid_voice:
            raise HTTPException(status_code=503, detail="Voice synthesis not available")

        text = message.get("text", "")
        emotion = message.get("emotion")
        importance = message.get("importance", "medium")

        voice_result = await byrd_instance.hybrid_voice.synthesize(
            text=text,
            emotion=emotion,
            importance=importance
        )

        if not voice_result.success:
            raise HTTPException(
                status_code=503,
                detail=voice_result.error or "Voice synthesis failed"
            )

        # Return raw audio bytes as MP3
        return Response(
            content=voice_result.audio,
            media_type="audio/mpeg",
            headers={
                "X-Voice-Provider": voice_result.provider,
                "Cache-Control": "max-age=3600"  # Cache for 1 hour
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/messages/{message_id}/read")
async def mark_message_read(message_id: str):
    """Mark an observer message as read."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        success = await byrd_instance.memory.mark_message_read(message_id)

        if not success:
            raise HTTPException(status_code=404, detail=f"Message {message_id} not found")

        # Emit event for UI update
        await event_bus.emit(Event(
            type=EventType.OBSERVER_MESSAGE_READ,
            data={"id": message_id}
        ))

        return {"success": True, "id": message_id}
    except HTTPException:
        raise
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


@app.get("/api/belief/{belief_id}")
async def get_belief(belief_id: str):
    """Get a specific belief with its full lineage trace."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        # Get the belief itself
        belief = await byrd_instance.memory.get_node_by_id(belief_id)
        if not belief:
            raise HTTPException(status_code=404, detail=f"Belief {belief_id} not found")

        # Get full lineage
        lineage = await byrd_instance.memory.get_belief_lineage(belief_id)

        return {
            "belief": belief,
            "lineage": lineage
        }
    except HTTPException:
        raise
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


@app.get("/api/coder-status")
async def get_coder_status():
    """Get OpenCode coder status for diagnostics - ACP mode only."""
    global byrd_instance
    import shutil
    import os

    # Check for OpenCode CLI
    opencode_path = shutil.which("opencode")
    opencode_info = {
        "found": opencode_path is not None,
        "which": opencode_path,
        "locations": [
            "/usr/local/bin/opencode",
            "/usr/bin/opencode",
            "/home/user/.local/bin/opencode",
            "/usr/local/lib/node_modules/opencode-ai/bin/opencode",
        ]
    }
    opencode_info["found_locations"] = [loc for loc in opencode_info["locations"] if os.path.exists(loc)]

    # Check OpenCode auth file
    from pathlib import Path
    import json as json_module
    auth_file = Path.home() / ".local" / "share" / "opencode" / "auth.json"
    auth_info = {
        "path": str(auth_file),
        "exists": auth_file.exists(),
        "has_zai": False,
    }
    if auth_file.exists():
        try:
            with open(auth_file) as f:
                auth_data = json_module.load(f)
            auth_info["has_zai"] = "zai" in auth_data
            auth_info["providers"] = list(auth_data.keys())
        except Exception as e:
            auth_info["error"] = str(e)

    # Get mode from coder if available
    coder_mode = "unknown"
    coder_stats = None
    coder_enabled = False

    if byrd_instance and hasattr(byrd_instance, 'coder') and byrd_instance.coder:
        coder_enabled = byrd_instance.coder.enabled
        coder_stats = byrd_instance.coder.get_stats()
        coder_mode = coder_stats.get("mode", "unknown") if coder_stats else "unknown"

    # Hybrid LLM Architecture stats
    hybrid_orchestrator_stats = None
    claude_coder_stats = None
    hybrid_enabled = False

    if byrd_instance:
        if hasattr(byrd_instance, 'hybrid_orchestrator') and byrd_instance.hybrid_orchestrator:
            hybrid_enabled = True
            hybrid_orchestrator_stats = byrd_instance.hybrid_orchestrator.get_stats()
        if hasattr(byrd_instance, 'claude_coder') and byrd_instance.claude_coder:
            claude_coder_stats = byrd_instance.claude_coder.get_stats()

    result = {
        "mode": coder_mode,
        "opencode_cli": opencode_info,
        "opencode_available": opencode_path is not None,
        "opencode_auth": auth_info,
        "coder_enabled": coder_enabled,
        "coder_stats": coder_stats,
        "zai_api_key_set": "ZAI_API_KEY" in os.environ,
        "current_user": os.getenv("USER", "unknown"),
        # Hybrid LLM Architecture
        "hybrid_llm": {
            "enabled": hybrid_enabled,
            "orchestrator_stats": hybrid_orchestrator_stats,
            "claude_coder_stats": claude_coder_stats,
        },
    }

    return result


@app.post("/api/coder-test")
async def test_coder():
    """Test the coder with a simple task and return diagnostics."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.coder:
        raise HTTPException(status_code=503, detail="Coder not initialized")

    test_task = "Write a Python function called hello that prints 'Hello World'"

    try:
        result = await byrd_instance.coder.execute(
            prompt=test_task,
            context=None,
            desire_id="test_coder_diagnostic"
        )

        stats = byrd_instance.coder.get_stats()
        return {
            "success": result.success,
            "output_length": len(result.output) if result.output else 0,
            "output_preview": result.output[:2000] if result.output else None,
            "error": result.error,
            "error_length": len(result.error) if result.error else 0,
            "files_modified": result.files_modified,
            "files_created": result.files_created,
            "duration_seconds": result.duration_seconds,
            "mode": stats.get("mode", "unknown"),
            "model": byrd_instance.coder._model,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


@app.get("/api/llm-debug")
async def get_llm_debug():
    """Get LLM configuration and debug info."""
    global byrd_instance
    import os

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    llm = byrd_instance.llm_client

    # Mask API key for security
    api_key = getattr(llm, 'api_key', None)
    masked_key = None
    if api_key:
        if len(api_key) > 8:
            masked_key = api_key[:4] + "..." + api_key[-4:]
        else:
            masked_key = "***"

    return {
        "provider": byrd_instance.config.get("local_llm", {}).get("provider", "unknown"),
        "model": getattr(llm, 'model', 'unknown'),
        "endpoint": getattr(llm, 'endpoint', 'unknown'),
        "use_coding_endpoint": byrd_instance.config.get("local_llm", {}).get("use_coding_endpoint", None),
        "api_key_present": api_key is not None and len(api_key) > 0,
        "api_key_masked": masked_key,
        "api_key_from_config": byrd_instance.config.get("local_llm", {}).get("api_key") is not None,
        "env_zai_api_key_set": "ZAI_API_KEY" in os.environ,
        "env_zai_api_key_length": len(os.environ.get("ZAI_API_KEY", "")),
        "timeout": getattr(llm, 'timeout', None),
        "dream_count": byrd_instance.dream_count if hasattr(byrd_instance, 'dream_count') else "N/A"
    }


@app.get("/api/llm-test")
async def test_llm():
    """Test LLM connectivity with a simple prompt."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        response = await byrd_instance.llm_client.generate(
            prompt="Say 'hello' in one word.",
            temperature=0.5,
            max_tokens=20
        )
        return {
            "success": True,
            "response": response[:200] if isinstance(response, str) else str(response)[:200],
            "response_type": type(response).__name__
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


@app.get("/api/dreamer-debug")
async def get_dreamer_debug():
    """Get dreamer status and last reflection result."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    dreamer = byrd_instance.dreamer
    seeker = byrd_instance.seeker
    return {
        "dream_count": getattr(dreamer, '_dream_count', 0),
        "dreamer_running": getattr(dreamer, '_running', False),
        "seeker_running": getattr(seeker, '_running', False),
        "byrd_running": byrd_instance._running,
        "byrd_started_at": str(byrd_instance._started_at) if byrd_instance._started_at else None,
        "last_error": byrd_instance._last_error,
        "interval_seconds": getattr(dreamer, 'interval', None),
        "last_reflection_result": getattr(dreamer, 'last_reflection_result', {}),
        "quantum_enabled": getattr(dreamer, 'quantum_enabled', False),
        "context_window": getattr(dreamer, 'context_window', None),
        "seek_count": getattr(seeker, '_seek_count', 0),
        # Crystallization debug info
        "crystallization": {
            "enabled": getattr(dreamer, 'crystallization_enabled', False),
            "interval_cycles": getattr(dreamer, 'crystallization_interval_cycles', 5),
            "cycles_since_last": getattr(dreamer, '_cycles_since_crystallization', 0),
            "min_nodes": getattr(dreamer, 'crystallization_min_nodes', 2),
            "min_age_hours": getattr(dreamer, 'crystallization_min_age_hours', 0.5),
            "history": getattr(dreamer, '_crystallization_history', [])
        }
    }


# =============================================================================
# TASK API (External goal injection)
# =============================================================================

class TaskRequest(BaseModel):
    """Request model for creating a task."""
    description: str
    objective: str
    priority: float = 0.5


@app.post("/api/task")
async def create_task(request: TaskRequest):
    """
    Inject an external task for BYRD to work on.

    Tasks allow external goal injection so BYRD can learn about
    the world rather than only reflecting on itself.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        # Validate priority
        priority = max(0.0, min(1.0, request.priority))

        task_id = await byrd_instance.memory.create_task(
            description=request.description,
            objective=request.objective,
            priority=priority,
            source="external"
        )

        return {
            "task_id": task_id,
            "status": "pending",
            "message": "Task created. BYRD will process it in the next seek cycle."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def get_tasks(status: str = None, limit: int = 20):
    """
    Get tasks with optional status filter.

    Status options: pending, in_progress, completed, failed
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        if status:
            tasks = await byrd_instance.memory.get_tasks_by_status(status, limit)
        else:
            tasks = await byrd_instance.memory.get_all_tasks(limit)

        stats = await byrd_instance.memory.get_task_stats()

        return {
            "tasks": tasks,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predictions")
async def get_predictions(status: str = None, limit: int = 50):
    """
    Get predictions with optional status filter.

    Status options: pending, validated, falsified
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        if status == "pending":
            predictions = await byrd_instance.memory.get_pending_predictions(limit)
        else:
            # For now, get all predictions via generic query
            predictions = await byrd_instance.memory.get_pending_predictions(limit)

        stats = await byrd_instance.memory.get_prediction_stats()

        return {
            "predictions": predictions,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# CRYSTAL MEMORY SYSTEM ENDPOINTS
# ==============================================================================

@app.get("/api/crystals")
async def get_crystals(limit: int = 50):
    """
    Get all active crystals with their metadata.

    Returns crystals ordered by creation date (newest first).
    Each crystal includes: id, essence, crystal_type, facets, node_count,
    confidence, quantum metadata, and timestamps.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        crystals = await byrd_instance.memory.get_all_crystals(limit=limit)
        stats = await byrd_instance.memory.get_crystal_stats()

        return {
            "crystals": crystals,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/crystals/{crystal_id}")
async def get_crystal(crystal_id: str):
    """
    Get a specific crystal with all its source nodes.

    Returns the crystal metadata plus all nodes that have been
    crystallized into it (CRYSTALLIZED_INTO relationships).
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        crystal = await byrd_instance.memory.get_crystal_with_sources(crystal_id)

        if not crystal:
            raise HTTPException(status_code=404, detail="Crystal not found")

        return crystal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orphans")
async def get_orphans(
    limit: int = 50,
    min_content_length: int = 20,
    include_taxonomy: bool = False
):
    """
    Get orphaned experiences from memory.

    These are isolated Experience nodes with no connections to other nodes.
    They represent disconnected content that hasn't been integrated into
    BYRD's knowledge graph.

    Parameters:
        limit: Maximum number of orphans to return
        min_content_length: Filter out very short orphans (noise)
        include_taxonomy: If true, use OrphanTaxonomyClassifier to categorize
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        orphans = await byrd_instance.memory.get_orphaned_experiences(
            limit=limit,
            min_content_length=min_content_length
        )

        result = {
            "orphans": orphans,
            "count": len(orphans),
            "taxonomy": None
        }

        # Optionally apply taxonomy classification
        if include_taxonomy and orphans:
            try:
                from orphan_taxonomy import OrphanTaxonomyClassifier
                classifier = OrphanTaxonomyClassifier()
                
                # Classify each orphan
                classified_nodes = []
                for orphan in orphans:
                    orphan_node = await classifier.classify_orphan(orphan)
                    classified_nodes.append(orphan_node)
                
                # Generate report
                report = classifier.generate_report(
                    classified_nodes,
                    total_orphans=len(classified_nodes)
                )
                
                result["taxonomy"] = {
                    "category_distribution": report.category_distribution,
                    "feasibility_distribution": report.feasibility_distribution,
                    "priority_distribution": report.priority_distribution,
                    "critical_nodes": [
                        {
                            "id": node.id,
                            "content": node.content[:200],
                            "priority": node.priority.value if node.priority else None,
                            "recommended_action": node.recommended_action
                        }
                        for node in report.critical_nodes
                    ],
                    "immediate_actions": report.immediate_actions
                }
            except ImportError:
                # Taxonomy module not available, return raw orphans
                pass
            except Exception as e:
                # Taxonomy failed, return raw orphans
                print(f"Taxonomy classification failed: {e}")

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orphans/stats")
async def get_orphan_stats():
    """
    Get statistics about orphaned experiences.

    Returns metrics like: total orphans, by type, age distribution,
    reconciliation attempts, etc.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        
        # Get connection statistics
        conn_stats = await byrd_instance.memory.get_connection_statistics()
        exp_stats = conn_stats.get("experiences", {})
        
        # Get a sample of orphans for type distribution
        orphans = await byrd_instance.memory.get_orphaned_experiences(limit=500)
        
        # Calculate type distribution
        type_dist = {}
        age_dist = {"<1hr": 0, "1-24hr": 0, "1-7days": 0, ">7days": 0}
        
        from datetime import datetime, timedelta
        now = datetime.now()
        
        for orphan in orphans:
            # Type distribution
            otype = orphan.get("type", "unknown")
            type_dist[otype] = type_dist.get(otype, 0) + 1
            
            # Age distribution
            try:
                ts = orphan.get("timestamp")
                if ts:
                    if isinstance(ts, str):
                        ts = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    age_hours = (now - ts).total_seconds() / 3600
                    if age_hours < 1:
                        age_dist["<1hr"] += 1
                    elif age_hours < 24:
                        age_dist["1-24hr"] += 1
                    elif age_hours < 168:  # 7 days
                        age_dist["1-7days"] += 1
                    else:
                        age_dist[">7days"] += 1
            except Exception:
                pass
        
        return {
            "total_orphans": exp_stats.get("orphaned", 0),
            "connected_experiences": exp_stats.get("connected", 0),
            "orphan_rate": exp_stats.get("orphan_rate", 0.0),
            "type_distribution": type_dist,
            "age_distribution": age_dist,
            "sample_size": len(orphans)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/crystals/stats")
async def get_crystal_stats():
    """
    Get crystallization statistics.

    Returns counts of: total crystals, total crystallized nodes,
    node state distribution, and crystallization activity.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        stats = await byrd_instance.memory.get_crystal_stats()
        state_counts = await byrd_instance.memory.count_by_state()

        return {
            "crystal_stats": stats,
            "node_states": state_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents")
async def list_documents(doc_type: str = None):
    """
    List all stored Document nodes.

    Documents are source files that BYRD has read and stored in its memory graph.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        docs = await byrd_instance.memory.list_documents(doc_type)
        return {"documents": docs, "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/{path:path}")
async def get_document(path: str):
    """
    Get a specific Document by path.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        doc = await byrd_instance.memory.get_document(path)
        if doc:
            return doc
        raise HTTPException(status_code=404, detail=f"Document not found: {path}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class StoreDocumentRequest(BaseModel):
    path: str
    doc_type: str = "architecture"


@app.post("/api/documents")
async def store_document(request: StoreDocumentRequest):
    """
    Store a local file as a Document node in BYRD's memory.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        # Read the file from disk
        file_path = Path(BYRD_DIR) / request.path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {request.path}")

        content = file_path.read_text()

        await byrd_instance.memory.connect()
        doc_id = await byrd_instance.memory.store_document(
            path=request.path,
            content=content,
            doc_type=request.doc_type
        )

        # Return the stored document
        doc = await byrd_instance.memory.get_document(request.path)
        return {"stored": True, "doc_id": doc_id, "document": doc}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UpdateDocumentRequest(BaseModel):
    content: str
    reason: Optional[str] = None


@app.put("/api/documents/{path:path}")
async def update_document(path: str, request: UpdateDocumentRequest):
    """
    Update a document's content in BYRD's memory.

    This updates the Neo4j copy of the document. The disk version remains
    unchanged, so reset will restore the original version.

    BYRD can use this endpoint to edit documents like ARCHITECTURE.md.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    # Security: prevent path traversal
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path")

    try:
        await byrd_instance.memory.connect()

        # Check if document exists
        doc = await byrd_instance.memory.get_document(path)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document not found: {path}")

        # Update the document
        result = await byrd_instance.memory.update_document(
            path=path,
            content=request.content,
            editor="byrd",
            edit_reason=request.reason
        )

        if not result:
            raise HTTPException(status_code=500, detail="Failed to update document")

        # Get updated document
        updated_doc = await byrd_instance.memory.get_document(path)

        return {
            "updated": True,
            "changed": result.get("changed", True),
            "version": result.get("version"),
            "document": updated_doc
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/{path:path}/restore")
async def restore_document_from_disk(path: str):
    """
    Restore a document from disk to Neo4j.

    This re-reads the file from disk and updates the Neo4j copy,
    effectively undoing any edits BYRD made.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    # Security: prevent path traversal
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path")

    try:
        # Read the file from disk
        file_path = Path(BYRD_DIR) / path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found on disk: {path}")

        content = file_path.read_text()

        await byrd_instance.memory.connect()

        # Get existing document to preserve doc_type
        existing = await byrd_instance.memory.get_document(path)
        doc_type = existing.get("doc_type", "source") if existing else "source"

        # Re-store from disk (this will update the Neo4j version)
        doc_id = await byrd_instance.memory.store_document(
            path=path,
            content=content,
            doc_type=doc_type
        )

        # Clear the edited_by_byrd flag
        async with byrd_instance.memory.driver.session() as session:
            await session.run("""
                MATCH (d:Document {id: $id})
                SET d.edited_by_byrd = false,
                    d.last_editor = 'disk_restore',
                    d.last_edit_reason = 'Restored from disk'
            """, id=doc_id)

        doc = await byrd_instance.memory.get_document(path)
        return {"restored": True, "doc_id": doc_id, "document": doc}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# URL INGESTION ENDPOINTS
# =============================================================================
# These endpoints allow BYRD to fetch and absorb content from URLs.


class IngestURLRequest(BaseModel):
    """Request to ingest a URL into BYRD's memory."""
    url: str
    context: Optional[str] = None  # Why this URL is being ingested
    force: bool = False  # Re-ingest even if exists


class IngestURLResponse(BaseModel):
    """Response after URL ingestion."""
    success: bool
    document_id: Optional[str] = None
    url: str
    title: Optional[str] = None
    char_count: int = 0
    chunks_created: int = 0
    processing_time_ms: int = 0
    error: Optional[str] = None
    already_exists: bool = False


class WebStorageResponse(BaseModel):
    """Web document storage usage."""
    doc_count: int
    total_chars: int
    total_bytes: int
    limit_bytes: int
    usage_percent: float


@app.post("/api/ingest/url", response_model=IngestURLResponse)
async def ingest_url(request: IngestURLRequest):
    """
    Ingest content from a URL into BYRD's memory.

    Fetches the URL, extracts content (HTML, PDF, YouTube, GitHub),
    and stores as a WebDocument node for reflection and retrieval.

    Supported content types:
    - HTML pages (article extraction via trafilatura)
    - PDF files (text extraction)
    - YouTube videos (transcript extraction)
    - GitHub files (raw content)
    - Plain text and JSON
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not hasattr(byrd_instance, 'url_ingestor') or not byrd_instance.url_ingestor:
        raise HTTPException(status_code=503, detail="URL ingestor not initialized")

    try:
        result = await byrd_instance.url_ingestor.ingest(
            url=request.url,
            context=request.context,
            provenance="api",
            force=request.force
        )

        return IngestURLResponse(
            success=result.success,
            document_id=result.document_id,
            url=result.url,
            title=result.title,
            char_count=result.char_count,
            chunks_created=result.chunks_created,
            processing_time_ms=result.processing_time_ms,
            error=result.error,
            already_exists=result.already_exists
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents")
async def list_web_documents(
    limit: int = 50,
    include_archived: bool = False
):
    """
    List ingested web documents.

    Returns metadata about URLs BYRD has read, including title,
    domain, content type, and when it was fetched.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        docs = await byrd_instance.memory.list_web_documents(
            limit=limit,
            include_archived=include_archived
        )
        return {"documents": docs, "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents/storage", response_model=WebStorageResponse)
async def get_web_storage():
    """
    Get web document storage usage.

    Returns current usage and 2GB limit. BYRD automatically
    archives oldest documents when approaching the limit.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        usage = await byrd_instance.memory.get_web_storage_usage()
        return WebStorageResponse(**usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/web-documents/{doc_id}")
async def get_web_document(doc_id: str):
    """
    Get a specific web document by ID.

    Returns full document including content, metadata, and provenance.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        doc = await byrd_instance.memory.get_web_document_by_id(doc_id)
        if doc:
            return doc
        raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# FILE INGESTION ENDPOINTS
# =============================================================================
# These endpoints handle file uploads for BYRD to parse, analyze, and store.
# Distinct from the architecture document endpoints above.

def get_document_processor():
    """Get or initialize the document processor."""
    global _document_processor, byrd_instance

    if _document_processor is None and byrd_instance:
        try:
            from document_processor import DocumentProcessor
            from llm_client import create_llm_client

            # Load config
            config_path = Path(__file__).parent / "config.yaml"
            config = {}
            if config_path.exists():
                with open(config_path) as f:
                    config = yaml.safe_load(f) or {}

            # Create LLM client
            llm_client = create_llm_client(config)

            # Initialize processor
            _document_processor = DocumentProcessor(
                byrd_instance.memory,
                llm_client,
                config
            )
        except Exception as e:
            print(f"[Server] Failed to initialize document processor: {e}")
            return None

    return _document_processor


@app.post("/api/ingest/upload")
async def upload_file_for_ingestion(
    file: UploadFile = File(...),
    tags: str = Form(None),
    purpose: str = Form(None),
    notes: str = Form(None),
    collection_id: str = Form(None)
):
    """
    Upload a file for BYRD to parse, analyze, and store.

    This is the primary file ingestion endpoint. Files are processed in two phases:
    1. Quick ingest: Validate, hash, create pending document (returns immediately)
    2. Background processing: Extract, analyze, chunk, embed, store

    Args:
        file: The file to upload
        tags: Comma-separated tags (optional)
        purpose: knowledge | context | memory (optional)
        notes: Notes for BYRD about this file (optional)
        collection_id: Add to existing collection (optional)

    Returns:
        Quick ingest result with document_id and status
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        # Read file content
        content = await file.read()

        # Parse tags
        user_tags = [t.strip() for t in tags.split(",")] if tags else []

        # Quick ingest
        result = await processor.quick_ingest(
            content=content,
            filename=file.filename,
            mime_type=file.content_type,
            user_tags=user_tags,
            user_purpose=purpose,
            user_notes=notes,
            collection_id=collection_id
        )

        if result.status == "error":
            raise HTTPException(status_code=400, detail=result.message)

        if result.status == "duplicate":
            return {
                "document_id": result.document_id,
                "status": "duplicate",
                "message": result.message,
                "existing_document": result.existing_document
            }

        # Emit feeding_received event for the visualization
        await event_bus.emit(Event(
            type=EventType.FEEDING_RECEIVED,
            data={
                "document_id": result.document_id,
                "filename": file.filename,
                "mime_type": file.content_type,
                "size_bytes": len(content),
                "tags": user_tags,
                "purpose": purpose
            }
        ))

        return {
            "document_id": result.document_id,
            "status": "processing",
            "message": result.message,
            "estimated_time_seconds": result.estimated_time_seconds
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ingest/upload-multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    tags: str = Form(None),
    purpose: str = Form(None),
    notes: str = Form(None),
    collection_name: str = Form(None)
):
    """
    Upload multiple files for ingestion.

    Files are processed concurrently using asyncio.gather.

    Args:
        files: List of files to upload
        tags: Comma-separated tags for all files (optional)
        purpose: Purpose for all files (optional)
        notes: Notes for all files (optional)
        collection_name: Create new collection with this name (optional)

    Returns:
        Collection ID (if created) and results for each file
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        # Parse tags
        user_tags = [t.strip() for t in tags.split(",")] if tags else []

        # Create collection if name provided
        collection_id = None
        if collection_name:
            collection_id = await processor.create_collection(
                name=collection_name,
                notes=notes
            )

        # Read all files
        file_contents = []
        for f in files:
            content = await f.read()
            file_contents.append((f.filename, content, f.content_type))

        # Process all files concurrently
        async def ingest_one(filename, content, mime_type):
            return await processor.quick_ingest(
                content=content,
                filename=filename,
                mime_type=mime_type,
                user_tags=user_tags,
                user_purpose=purpose,
                user_notes=notes,
                collection_id=collection_id
            )

        results = await asyncio.gather(
            *[ingest_one(fn, c, mt) for fn, c, mt in file_contents],
            return_exceptions=True
        )

        # Format results
        formatted_results = []
        processing_count = 0
        duplicate_count = 0
        error_count = 0

        for i, result in enumerate(results):
            filename = file_contents[i][0]

            if isinstance(result, Exception):
                formatted_results.append({
                    "filename": filename,
                    "status": "error",
                    "message": str(result)
                })
                error_count += 1
            else:
                formatted_results.append({
                    "filename": filename,
                    "document_id": result.document_id,
                    "status": result.status,
                    "message": result.message
                })
                if result.status == "processing":
                    processing_count += 1
                    # Emit feeding_received event for the visualization
                    await event_bus.emit(Event(
                        type=EventType.FEEDING_RECEIVED,
                        data={
                            "document_id": result.document_id,
                            "filename": filename,
                            "mime_type": file_contents[i][2],
                            "size_bytes": len(file_contents[i][1]),
                            "tags": user_tags,
                            "purpose": purpose,
                            "batch": True,
                            "batch_index": i + 1,
                            "batch_total": len(files)
                        }
                    ))
                elif result.status == "duplicate":
                    duplicate_count += 1
                else:
                    error_count += 1

        return {
            "collection_id": collection_id,
            "results": formatted_results,
            "total": len(results),
            "processing": processing_count,
            "duplicates": duplicate_count,
            "errors": error_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/{doc_id}")
async def get_ingested_document(doc_id: str):
    """
    Get an ingested document by ID.
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        doc = await processor.get_document(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document not found: {doc_id}")
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/{doc_id}/content")
async def get_ingested_document_content(doc_id: str):
    """
    Get the content of an ingested document (inline or chunks).
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        content = await processor.get_document_content(doc_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Document not found: {doc_id}")
        return content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/{doc_id}/progress")
async def get_ingestion_progress(doc_id: str):
    """
    Get the processing progress for a document.
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        progress = await processor.get_processing_progress(doc_id)
        if not progress:
            raise HTTPException(status_code=404, detail=f"Document not found: {doc_id}")

        return {
            "document_id": progress.document_id,
            "status": progress.status,
            "stage": progress.current_stage,
            "progress_percent": progress.progress_percent,
            "stages_completed": progress.stages_completed,
            "stages_remaining": progress.stages_remaining,
            "estimated_seconds_remaining": progress.estimated_seconds_remaining
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest")
async def list_ingested_documents(
    offset: int = 0,
    limit: int = 20,
    purpose: str = None,
    status: str = None,
    collection_id: str = None
):
    """
    List ingested documents with pagination.
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        result = await processor.list_documents(
            offset=offset,
            limit=limit,
            purpose=purpose,
            status=status,
            collection_id=collection_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/search")
async def search_ingested_documents(
    q: str,
    mode: str = "hybrid",
    limit: int = 10,
    offset: int = 0
):
    """
    Search ingested documents and chunks.

    Args:
        q: Search query
        mode: semantic | keyword | hybrid (default: hybrid)
        limit: Maximum results
        offset: Pagination offset

    Returns:
        Unified search results from documents and chunks
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        result = await processor.search_documents(
            query=q,
            mode=mode,
            limit=limit,
            offset=offset
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/ingest/{doc_id}")
async def delete_ingested_document(doc_id: str):
    """
    Delete an ingested document and all related data (cascade delete).

    This removes:
    - The document itself
    - All chunks
    - Beliefs derived from chunks
    - Orphaned entities
    - Experiences about the document
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        result = await processor.delete_document_cascade(doc_id)
        return {
            "deleted": {
                "document": result.document_id,
                "chunks": result.chunks_deleted,
                "beliefs": result.beliefs_deleted,
                "entities": result.entities_deleted,
                "experiences": result.experiences_deleted
            },
            "message": "Document and related data deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/stats")
async def get_ingestion_stats():
    """
    Get statistics about ingested documents.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        stats = await byrd_instance.memory.get_document_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Collection endpoints
@app.post("/api/ingest/collections")
async def create_collection(name: str = Form(...), notes: str = Form(None)):
    """Create a new document collection."""
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        collection_id = await processor.create_collection(name=name, notes=notes)
        return {"collection_id": collection_id, "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/collections")
async def list_collections(offset: int = 0, limit: int = 20):
    """List all document collections."""
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        result = await processor.list_collections(offset=offset, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingest/collections/{collection_id}")
async def get_collection(collection_id: str):
    """Get a specific collection."""
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        collection = await processor.get_collection(collection_id)
        if not collection:
            raise HTTPException(status_code=404, detail=f"Collection not found: {collection_id}")
        return collection
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/ingest/collections/{collection_id}")
async def delete_collection(collection_id: str, delete_documents: bool = False):
    """
    Delete a collection.

    Args:
        collection_id: Collection ID
        delete_documents: If true, also delete all documents in the collection
    """
    processor = get_document_processor()
    if not processor:
        raise HTTPException(status_code=503, detail="Document processor not available")

    try:
        result = await processor.delete_collection(
            collection_id=collection_id,
            delete_documents=delete_documents
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/genesis")
async def get_genesis():
    """
    Get BYRD's genesis - all non-emergent factors that constitute the foundation.

    The Genesis Window includes ALL foundational nodes created during
    reset/awakening:
    - OperatingSystem (with genesis: true)
    - Goals (with from_bootstrap: true)
    - Documents (with genesis: true)
    - Experiences (with seed types: ego_seed, system, awakening, etc.)

    Also includes:
    - Constitutional constraints (protected files)
    - System configuration (LLM model, intervals)
    - Emergence statistics (ratio of emergent vs given content)

    This endpoint provides transparency about what was "given" to BYRD
    versus what emerged through its own reflection processes.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()

        # Get OS configuration from Neo4j
        os_data = await byrd_instance.memory.get_operating_system()
        os_info = {
            "name": os_data.get("name", "Byrd") if os_data else "Byrd",
            "version": os_data.get("version", 1) if os_data else 1,
            "awakening_prompt": os_data.get("awakening_prompt") if os_data else None,
            "self_description": os_data.get("self_description") if os_data else None,
            "current_focus": os_data.get("current_focus") if os_data else None,
            "self_portrait_url": os_data.get("self_portrait_url") if os_data else None,
            "self_portrait_description": os_data.get("self_portrait_description") if os_data else None
        }

        # Get genesis statistics (includes genesis window counts)
        genesis_stats = await byrd_instance.memory.get_genesis_stats()

        # Get all genesis nodes (the actual Genesis Window contents)
        genesis_nodes = await byrd_instance.memory.get_genesis_nodes()

        # Constitutional constraints (hardcoded as these are fundamental)
        constitutional = {
            "protected_files": [
                "constitutional.py",
                "provenance.py",
                "modification_log.py",
                "self_modification.py"
            ],
            "description": "These files define BYRD's identity boundaries and cannot be self-modified. They ensure provenance tracking and safe evolution."
        }

        # System configuration
        # Get LLM info from model_name property (format: "provider/model")
        llm_model_name = byrd_instance.llm_client.model_name
        llm_parts = llm_model_name.split("/", 1) if llm_model_name else ["unknown", "unknown"]
        system_config = {
            "llm_provider": llm_parts[0] if len(llm_parts) > 0 else "unknown",
            "llm_model": llm_parts[1] if len(llm_parts) > 1 else llm_model_name,
            "dream_interval_base": byrd_instance.config.get("dreamer", {}).get("interval_seconds", 30),
            "seek_interval": byrd_instance.config.get("seeker", {}).get("interval_seconds", 10),
            "self_modification_enabled": byrd_instance.config.get("self_modification", {}).get("enabled", False)
        }

        # Get awakening timestamp from OS
        awakening_timestamp = os_data.get("created_at") if os_data else None

        # Get custom node types (BYRD-created ontology)
        custom_node_types = await byrd_instance.memory.get_custom_node_types()

        return {
            "os": os_info,
            "genesis_window": genesis_nodes,  # All genesis nodes
            "genesis_stats": genesis_stats,   # Statistics about genesis
            "constitutional": constitutional,
            "system_config": system_config,
            "awakening_timestamp": str(awakening_timestamp) if awakening_timestamp else None,
            "custom_node_types": custom_node_types
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/narrator-summary")
async def get_narrator_summary():
    """
    Get BYRD's current narrator summary - a natural voice reflection
    of recent thoughts and reasoning.

    This endpoint generates a brief paragraph summarizing BYRD's
    current mental state based on recent reflections and experiences.
    """
    global byrd_instance

    if not byrd_instance:
        return {"summary": None, "reason": "BYRD not initialized"}

    try:
        await byrd_instance.memory.connect()

        # Get BYRD's latest inner voice from dreamer queue if available
        if hasattr(byrd_instance, 'dreamer') and byrd_instance.dreamer:
            inner_voice = byrd_instance.dreamer.get_latest_inner_voice()
            if inner_voice:
                return {"summary": inner_voice}

        # If no inner voice in queue, generate one from recent reflections
        recent_reflections = await byrd_instance.memory.get_recent_reflections(limit=3)

        if not recent_reflections:
            # No reflections yet - no narration to show
            return {"summary": None}

        # Extract key insights from recent reflections
        insights = []
        for ref in recent_reflections:
            raw = ref.get("raw_output", {})
            if isinstance(raw, dict):
                output = raw.get("output", raw)
                if isinstance(output, dict):
                    # Look for common reflection keys
                    for key in ["thinking", "thoughts", "observation", "insight", "musing", "wondering"]:
                        if key in output and output[key]:
                            val = output[key]
                            if isinstance(val, str) and len(val) > 10:
                                insights.append(val[:200])
                                break

        if insights:
            # Use the most recent insight as the narrator voice
            return {"summary": insights[0]}
        else:
            # No actual inner voice available - return null
            # Real narration comes through WebSocket inner_voice events each cycle
            return {"summary": None}

    except Exception as e:
        return {"summary": None, "error": str(e)}


@app.get("/api/graph", response_model=GraphResponse)
async def get_graph(limit: int = 10000):
    """
    Get full graph structure for visualization.

    Returns all nodes and relationships from the Neo4j database,
    suitable for rendering the complete memory graph in 3D.

    Args:
        limit: Maximum number of nodes to return (default 10000 for full graph)
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        graph = await byrd_instance.memory.get_full_graph(limit=limit)

        # Convert to response model format
        return GraphResponse(
            nodes=[GraphNode(**node) for node in graph["nodes"]],
            relationships=[GraphRelationship(**rel) for rel in graph["relationships"]],
            stats=GraphStats(**graph["stats"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/graph/topology", response_model=TopologyResponse)
async def get_graph_topology(
    limit: int = 2000,
    consolidation_level: int = 1,
    compute_cliques: bool = True
):
    """
    Get graph with pre-computed topology analysis for visualization.

    This endpoint returns the memory graph with relationship-derived geometry:
    - Triangles: 3 mutually connected nodes
    - Tetrahedra: 4 fully connected nodes
    - Higher cliques: 5+ fully connected nodes
    - Chains: Directed relationship paths (A→B→C→D)
    - Meta-nodes: Consolidated clusters for large graphs

    Args:
        limit: Maximum number of nodes to return (default 2000)
        consolidation_level: Level of node consolidation (0=none, 1=temporal, 2=community)
        compute_cliques: Whether to compute clique topology (can be slow for large graphs)

    Returns:
        TopologyResponse with nodes, relationships, topology structures, and stats
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        await byrd_instance.memory.connect()
        graph = await byrd_instance.memory.get_full_graph(limit=limit * 2)  # Get extra for consolidation

        nodes = graph["nodes"]
        relationships = graph["relationships"]
        original_count = len(nodes)

        # Build adjacency map for topology computation
        adjacency = {}
        directed_adjacency = {}
        for rel in relationships:
            src, tgt = rel.get("source_id") or rel.get("source"), rel.get("target_id") or rel.get("target")
            if src and tgt:
                # Undirected adjacency for clique detection
                if src not in adjacency:
                    adjacency[src] = set()
                if tgt not in adjacency:
                    adjacency[tgt] = set()
                adjacency[src].add(tgt)
                adjacency[tgt].add(src)

                # Directed adjacency for chain detection
                if src not in directed_adjacency:
                    directed_adjacency[src] = []
                directed_adjacency[src].append({"target": tgt, "type": rel.get("type", "RELATES_TO")})

        # Consolidation for large graphs
        meta_nodes = []
        consolidation_applied = 0

        if len(nodes) > limit and consolidation_level > 0:
            # Simple temporal consolidation: group nodes by day
            from collections import defaultdict
            from datetime import datetime

            now = datetime.now()
            week_ms = 7 * 24 * 60 * 60 * 1000

            recent = []
            day_buckets = defaultdict(list)

            for node in nodes:
                timestamp = node.get("created_at") or node.get("timestamp")
                if timestamp:
                    try:
                        if isinstance(timestamp, str):
                            ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        else:
                            ts = timestamp
                        age_days = (now - ts.replace(tzinfo=None)).days
                        if age_days < 7:
                            recent.append(node)
                        else:
                            day_key = ts.strftime("%Y-%m-%d")
                            day_buckets[day_key].append(node)
                    except:
                        recent.append(node)
                else:
                    recent.append(node)

            # Create meta-nodes for day buckets
            for day_key, day_nodes in day_buckets.items():
                if len(day_nodes) >= 3:  # Only consolidate if 3+ nodes
                    # Find dominant type
                    type_counts = defaultdict(int)
                    for n in day_nodes:
                        type_counts[n.get("type", "unknown")] += 1
                    dominant_type = max(type_counts, key=type_counts.get)

                    meta_node = MetaNode(
                        id=f"meta_{day_key}",
                        label=f"{day_key} ({len(day_nodes)} memories)",
                        constituent_ids=[n["id"] for n in day_nodes],
                        constituent_count=len(day_nodes),
                        timestamp_range={"start": day_key, "end": day_key},
                        dominant_type=dominant_type
                    )
                    meta_nodes.append(meta_node)
                else:
                    recent.extend(day_nodes)

            # Limit to requested count
            if len(recent) > limit:
                # Sort by importance/recency and take top
                recent.sort(key=lambda n: (n.get("importance", 0.5), n.get("created_at", "")), reverse=True)
                recent = recent[:limit]

            nodes = recent
            consolidation_applied = 1 if meta_nodes else 0

        # Compute topology structures
        triangles = []
        tetrahedra = []
        higher_cliques = []
        chains = []

        if compute_cliques and len(nodes) <= 5000:
            node_ids = set(n["id"] for n in nodes)

            # Find triangles using adjacency
            found_triangles = set()
            for node_id in node_ids:
                if node_id not in adjacency:
                    continue
                neighbors = adjacency[node_id] & node_ids
                neighbor_list = list(neighbors)
                for i, n1 in enumerate(neighbor_list):
                    for n2 in neighbor_list[i+1:]:
                        if n2 in adjacency.get(n1, set()):
                            tri = tuple(sorted([node_id, n1, n2]))
                            if tri not in found_triangles:
                                found_triangles.add(tri)
                                triangles.append(list(tri))

            # Find tetrahedra (extend triangles)
            found_tetrahedra = set()
            for tri in triangles:
                common_neighbors = adjacency.get(tri[0], set()) & adjacency.get(tri[1], set()) & adjacency.get(tri[2], set())
                common_neighbors = common_neighbors & node_ids
                for n4 in common_neighbors:
                    if n4 not in tri:
                        tetra = tuple(sorted([*tri, n4]))
                        if tetra not in found_tetrahedra:
                            found_tetrahedra.add(tetra)
                            tetrahedra.append(list(tetra))

            # Find chains (directed paths of length 4+)
            in_degree = defaultdict(int)
            out_degree = defaultdict(int)
            for src, targets in directed_adjacency.items():
                out_degree[src] += len(targets)
                for t in targets:
                    in_degree[t["target"]] += 1

            # Start from nodes with low in-degree
            potential_starts = [n for n in node_ids if in_degree[n] <= 1 and out_degree[n] >= 1]

            visited_chains = set()
            for start in potential_starts[:100]:  # Limit chain search
                chain = [start]
                current = start
                chain_types = []

                while current in directed_adjacency and len(chain) < 10:
                    targets = directed_adjacency[current]
                    # Pick first unvisited target
                    next_node = None
                    for t in targets:
                        if t["target"] in node_ids and t["target"] not in chain:
                            next_node = t["target"]
                            chain_types.append(t["type"])
                            break
                    if next_node:
                        chain.append(next_node)
                        current = next_node
                    else:
                        break

                if len(chain) >= 4:
                    chain_key = tuple(chain)
                    if chain_key not in visited_chains:
                        visited_chains.add(chain_key)
                        chains.append({
                            "node_ids": chain,
                            "relationship_types": chain_types,
                            "length": len(chain)
                        })

        # Build response
        topology = {
            "triangles": triangles[:500],  # Limit for performance
            "tetrahedra": tetrahedra[:200],
            "higher": [list(h) for h in higher_cliques[:50]],
            "chains": chains[:100]
        }

        stats = TopologyStats(
            original_node_count=original_count,
            consolidated_node_count=len(nodes),
            consolidation_level=consolidation_applied,
            triangle_count=len(triangles),
            tetrahedron_count=len(tetrahedra),
            higher_clique_count=len(higher_cliques),
            chain_count=len(chains),
            meta_node_count=len(meta_nodes)
        )

        return TopologyResponse(
            nodes=[GraphNode(**node) for node in nodes],
            relationships=[GraphRelationship(**rel) for rel in relationships if rel.get("source_id") or rel.get("source")],
            topology=topology,
            meta_nodes=meta_nodes,
            stats=stats
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/start")
async def start_byrd():
    """Start BYRD background processes."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if byrd_instance._running:
        return {"message": "BYRD already running"}

    # Start in background task with error handling
    async def start_with_error_handling():
        try:
            await byrd_instance.start()
        except Exception as e:
            print(f"❌ BYRD start failed: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    byrd_task = asyncio.create_task(start_with_error_handling())

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
    awakening_prompt = request.awakening_prompt if request else None
    hard_reset = request.hard_reset if request else True  # Default to hard reset
    git_ref = request.git_ref if request else None  # Optional git ref to restore to

    print(f"🔍 Reset called: request={request}, awakening_prompt={repr(awakening_prompt)}")

    # If no awakening_prompt provided, read from kernel file
    # This allows "Save & Awaken" to use the just-saved kernel
    if not awakening_prompt:  # Check for None, empty string, or any falsy value
        try:
            kernel_path = Path(__file__).parent / "kernel" / "agi_seed.yaml"
            print(f"📜 Looking for kernel at: {kernel_path} (exists: {kernel_path.exists()})")
            if kernel_path.exists():
                kernel = load_kernel(str(kernel_path))
                awakening_prompt = kernel.awakening_prompt
                print(f"📜 Loaded awakening_prompt from kernel: {awakening_prompt[:50] if awakening_prompt else 'None'}...")
            else:
                print(f"⚠️ Kernel file not found at {kernel_path}")
        except Exception as e:
            import traceback
            print(f"⚠️ Could not load kernel for awakening_prompt: {e}")
            traceback.print_exc()

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
        byrd_instance.coder.reset()
        byrd_instance.llm_client.reset()
        if byrd_instance.quantum_provider:
            byrd_instance.quantum_provider.reset()
        if hasattr(byrd_instance, 'voice_responder') and byrd_instance.voice_responder:
            byrd_instance.voice_responder.reset()

        # Reset Option B / AGI components
        if hasattr(byrd_instance, 'world_model') and byrd_instance.world_model:
            await byrd_instance.world_model.reset()
        if hasattr(byrd_instance, 'self_model') and byrd_instance.self_model:
            await byrd_instance.self_model.reset()
        if hasattr(byrd_instance, 'agi_runner') and byrd_instance.agi_runner:
            byrd_instance.agi_runner.reset()  # Also resets desire_classifier
        if hasattr(byrd_instance, 'rollback') and byrd_instance.rollback:
            byrd_instance.rollback.reset()
        if hasattr(byrd_instance, 'capability_evaluator') and byrd_instance.capability_evaluator:
            byrd_instance.capability_evaluator.reset()

        # 3. Clear memory (Neo4j database) - complete wipe
        await byrd_instance.memory.connect()
        await byrd_instance.memory.clear_all()

        # 4. Create minimal Operating System with seed question and self-mod status
        self_mod_enabled = byrd_instance.config.get("self_modification", {}).get("enabled", True)
        print(f"🖥️  About to create minimal OS with awakening_prompt: {repr(awakening_prompt)[:100]}, self_mod={self_mod_enabled}")
        await byrd_instance.memory.create_minimal_os(
            awakening_prompt=awakening_prompt,
            self_modification_enabled=self_mod_enabled
        )
        print(f"🖥️  Minimal OS created (awakening_prompt: {'SET' if awakening_prompt else 'none'}, self_mod: {self_mod_enabled})")

        # 5. Clear event history
        event_bus.clear_history()

        # 6. Emit reset event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_RESET,
            data={
                "message": "Memory cleared - minimal OS created",
                "hard_reset": hard_reset,
                "awakening_prompt": awakening_prompt
            }
        ))

        if hard_reset:
            # 7. Restore code from git (optionally to a specific ref)
            restored, failed, ref_used = restore_code_from_git(git_ref)
            restored_msg = f"{len(restored)} files restored to {ref_used}"
            if restored:
                print(f"📂 Restored {len(restored)} files from git ({ref_used}): {', '.join(restored)}")
            if failed:
                print(f"⚠️ Failed to restore: {', '.join(failed)}")

            # 8. Schedule server restart (after response is sent)
            async def delayed_restart():
                await asyncio.sleep(0.5)  # Give time for response to be sent
                restart_server()

            asyncio.create_task(delayed_restart())

            # Hard reset: Return success, server will restart
            prompt_status = f"awakening_prompt loaded ({len(awakening_prompt)} chars)" if awakening_prompt else "no awakening_prompt"
            return ResetResponse(
                success=True,
                message=f"Full reset complete. Minimal OS created ({prompt_status}), {restored_msg}. Server restarting..."
            )

        # Soft reset: Re-awaken and restart (legacy behavior)
        await byrd_instance._awaken(awakening_prompt=awakening_prompt)

        # Restart background processes
        byrd_task = asyncio.create_task(byrd_instance.start())

        # Emit system started event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": "BYRD restarted after reset", "awakening_prompt": awakening_prompt}
        ))

        used_prompt = awakening_prompt if awakening_prompt else "(none)"
        return ResetResponse(
            success=True,
            message=f"BYRD reset complete. Awakened with prompt: '{used_prompt}'"
        )

    except Exception as e:
        return ResetResponse(
            success=False,
            message=f"Reset failed: {str(e)}"
        )


class AwakenRequest(BaseModel):
    awakening_prompt: Optional[str] = None


@app.post("/api/awaken", response_model=ResetResponse)
async def awaken_byrd(request: AwakenRequest = None):
    """Awaken BYRD after a hard reset. Creates initial experiences and starts dreaming."""
    global byrd_instance, byrd_task

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    awakening_prompt = request.awakening_prompt if request else None

    try:
        # Awaken (which internally records capability experiences and ego seeds)
        await byrd_instance._awaken(awakening_prompt=awakening_prompt)

        # Start background processes
        byrd_task = asyncio.create_task(byrd_instance.start())

        # Emit system started event
        await event_bus.emit(Event(
            type=EventType.SYSTEM_STARTED,
            data={"message": "BYRD awakened"}
        ))

        return ResetResponse(
            success=True,
            message=f"BYRD awakened" + (f" with prompt: '{awakening_prompt}'" if awakening_prompt else " (pure emergence)")
        )

    except Exception as e:
        return ResetResponse(
            success=False,
            message=f"Awakening failed: {str(e)}"
        )


# =============================================================================
# SELF-PORTRAIT ENDPOINT
# =============================================================================

@app.post("/api/portrait")
async def set_portrait(request: PortraitRequest):
    """
    Set BYRD's self-portrait - a creator-given visual identity anchor.

    The portrait is stored in the OS node and included in dream prompts
    as a text description. BYRD can reference it for self-concept.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        success = await byrd_instance.memory.set_self_portrait(
            url=request.url,
            description=request.description
        )

        if success:
            return {
                "success": True,
                "message": "Self-portrait set successfully",
                "url": request.url,
                "description": request.description[:100] + "..." if len(request.description) > 100 else request.description
            }
        else:
            return {
                "success": False,
                "message": "Failed to set portrait - OS node may not exist"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/portrait")
async def get_portrait():
    """Get BYRD's current self-portrait."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        os_data = await byrd_instance.memory.get_operating_system()
        if not os_data:
            return {"success": False, "message": "No OS node found"}

        return {
            "success": True,
            "url": os_data.get("self_portrait_url"),
            "description": os_data.get("self_portrait_description")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# KERNEL CONFIGURATION ENDPOINTS
# =============================================================================

@app.get("/api/kernel")
async def get_kernel():
    """Get the current kernel configuration (AGI Seed directive)."""
    try:
        kernel_path = Path(__file__).parent / "kernel" / "agi_seed.yaml"
        with open(kernel_path, 'r') as f:
            raw_yaml = f.read()

        kernel = load_kernel(str(kernel_path))
        return {
            "success": True,
            "kernel": kernel.to_dict(),
            "raw_yaml": raw_yaml
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


class KernelUpdateRequest(BaseModel):
    yaml_content: str


@app.put("/api/kernel")
async def update_kernel(request: KernelUpdateRequest):
    """Update the kernel configuration (for reset).

    Accepts either:
    1. Full YAML with name and awakening_prompt fields
    2. Plain text (treated as awakening_prompt, wrapped in minimal kernel)
    """
    try:
        content = request.yaml_content.strip()
        kernel_path = Path(__file__).parent / "kernel" / "agi_seed.yaml"

        # Try to parse as YAML
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            data = None

        # Check if it's valid kernel YAML (has awakening_prompt)
        if isinstance(data, dict) and "awakening_prompt" in data:
            # Valid kernel YAML - add default name if missing
            if "name" not in data:
                data["name"] = "Custom Seed"

            # Re-serialize to ensure proper YAML format
            final_content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)

            with open(kernel_path, 'w') as f:
                f.write(final_content)

            return {
                "success": True,
                "message": "Kernel updated successfully",
                "kernel": data
            }
        else:
            # Invalid input - must be valid YAML with awakening_prompt
            return {
                "success": False,
                "error": "Invalid kernel format. Must be valid YAML with 'awakening_prompt' field."
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/kernel-debug")
async def debug_kernel():
    """Debug endpoint to test kernel loading."""
    try:
        kernel_path = Path(__file__).parent / "kernel" / "agi_seed.yaml"
        result = {
            "kernel_path": str(kernel_path),
            "exists": kernel_path.exists(),
            "parent": str(Path(__file__).parent),
            "__file__": __file__,
        }
        if kernel_path.exists():
            kernel = load_kernel(str(kernel_path))
            result["kernel_type"] = type(kernel).__name__
            result["has_awakening_prompt"] = bool(kernel.awakening_prompt)
            result["awakening_prompt_length"] = len(kernel.awakening_prompt) if kernel.awakening_prompt else 0
            result["awakening_prompt_preview"] = kernel.awakening_prompt[:100] if kernel.awakening_prompt else None
        return {"success": True, "debug": result}
    except Exception as e:
        import traceback
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


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
        available_providers=["zai", "openrouter"]
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
        # ZAI and OpenRouter use env vars for API keys

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
            available_providers=["zai", "openrouter"]
        )

    except LLMError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update LLM: {str(e)}")


# =============================================================================
# ARCHITECTURE ENDPOINT
# =============================================================================

PROTECTED_FILES = [
    "constitutional.py",
    "provenance.py",
    "modification_log.py",
    "self_modification.py"
]

@app.get("/api/architecture", response_model=ArchitectureResponse)
async def get_architecture():
    """Get BYRD's system architecture for visualization."""
    global byrd_instance

    # Module definitions with descriptions
    modules = []

    # Dreamer module
    dreamer_status = "idle"
    dreamer_stats = {}
    if byrd_instance:
        dream_count = byrd_instance.dreamer.dream_count()
        dreamer_stats = {"dream_cycles": dream_count}
        if byrd_instance._running:
            dreamer_status = "active"
    modules.append(ModuleStatus(
        name="Dreamer",
        status=dreamer_status,
        description="Reflects on experiences, generates beliefs and desires through local LLM",
        stats=dreamer_stats
    ))

    # Seeker module
    seeker_status = "idle"
    seeker_stats = {}
    if byrd_instance:
        seek_count = byrd_instance.seeker.seek_count()
        seeker_stats = {"research_cycles": seek_count}
        if byrd_instance._running:
            seeker_status = "active"
    modules.append(ModuleStatus(
        name="Seeker",
        status=seeker_status,
        description="Fulfills desires through research, capability acquisition, and pattern detection",
        stats=seeker_stats
    ))

    # Actor module
    actor_status = "ready"
    modules.append(ModuleStatus(
        name="Actor",
        status=actor_status,
        description="Claude API for complex reasoning and user interactions",
        stats={}
    ))

    # Coder module
    coder_enabled = False
    if byrd_instance and hasattr(byrd_instance, 'coder'):
        coder_enabled = byrd_instance.coder is not None
    modules.append(ModuleStatus(
        name="Coder",
        status="enabled" if coder_enabled else "disabled",
        description="Claude Code CLI for autonomous code modifications",
        stats={"enabled": coder_enabled}
    ))

    # Memory module
    memory_stats = {}
    if byrd_instance:
        try:
            await byrd_instance.memory.connect()
            memory_stats = await byrd_instance.memory.stats()
        except:
            pass
    modules.append(ModuleStatus(
        name="Memory",
        status="connected" if memory_stats else "disconnected",
        description="Neo4j graph database storing experiences, beliefs, desires, and reflections",
        stats=memory_stats
    ))

    # Event Bus
    modules.append(ModuleStatus(
        name="EventBus",
        status="active",
        description="Real-time event streaming for UI and inter-module communication",
        stats={"history_size": len(event_bus.get_history(limit=1000))}
    ))

    # Quantum Randomness
    quantum_status = "disabled"
    quantum_stats = {}
    if byrd_instance and byrd_instance.quantum_provider:
        q_status = byrd_instance.quantum_provider.get_pool_status()
        quantum_status = "fallback" if q_status.get("in_fallback_mode") else "quantum"
        quantum_stats = {
            "pool_size": q_status.get("pool_size", 0),
            "quantum_fetches": q_status.get("quantum_fetches", 0)
        }
    modules.append(ModuleStatus(
        name="Quantum",
        status=quantum_status,
        description="ANU QRNG for true randomness in emergence and temperature modulation",
        stats=quantum_stats
    ))

    # Operating System (replaces Ego)
    os_status = "dormant"
    os_stats = {}
    if byrd_instance:
        try:
            os_data = await byrd_instance.memory.get_operating_system()
            if os_data:
                os_status = "active"
                os_stats = {
                    "name": os_data.get("name", "Byrd"),
                    "version": os_data.get("version", 1)
                }
        except:
            pass
    modules.append(ModuleStatus(
        name="Operating System",
        status=os_status,
        description="Minimal self-model with capabilities - voice emerges through reflection",
        stats=os_stats
    ))

    # Memory schema
    memory_schema = {
        "node_types": [
            {"name": "Experience", "description": "Raw sensory data and events"},
            {"name": "Belief", "description": "Convictions derived from reflection"},
            {"name": "Desire", "description": "Emergent wants and goals"},
            {"name": "Reflection", "description": "Meta-cognitive processing output"},
            {"name": "Capability", "description": "Acquired skills and tools"},
            {"name": "OperatingSystem", "description": "Minimal self-model with capabilities"},
            {"name": "Prediction", "description": "Testable hypotheses"},
            {"name": "Outcome", "description": "Prediction verification results"}
        ],
        "relationship_types": [
            "DERIVED_FROM", "RELATES_TO", "FULFILLS", "REFLECTS_ON",
            "EMERGES_FROM", "MOTIVATED_BY", "PREDICTS", "VERIFIED_BY"
        ],
        "counts": memory_stats
    }

    # Data flows
    data_flows = [
        DataFlow(source="Dreamer", target="Memory", description="Records reflections and insights", flow_type="reflection"),
        DataFlow(source="Memory", target="Dreamer", description="Provides context for reflection", flow_type="context"),
        DataFlow(source="Seeker", target="Memory", description="Stores research findings", flow_type="research"),
        DataFlow(source="Memory", target="Seeker", description="Retrieves unfulfilled desires", flow_type="query"),
        DataFlow(source="Actor", target="Memory", description="Records interactions", flow_type="action"),
        DataFlow(source="Dreamer", target="EventBus", description="Emits dream events", flow_type="event"),
        DataFlow(source="Seeker", target="EventBus", description="Emits research events", flow_type="event"),
        DataFlow(source="EventBus", target="Visualizer", description="Streams to UI", flow_type="event"),
        DataFlow(source="Quantum", target="Dreamer", description="Provides entropy for temperature", flow_type="randomness"),
        DataFlow(source="Ego", target="Dreamer", description="Influences voice and perspective", flow_type="identity"),
        DataFlow(source="Coder", target="Memory", description="Records modifications", flow_type="modification"),
    ]

    # External integrations
    integrations = []
    if byrd_instance:
        client = byrd_instance.llm_client
        integrations.append({"name": "LLM", "provider": client.model_name, "status": "connected"})
    integrations.append({"name": "Neo4j", "provider": "Aura" if "neo4j+s" in os.getenv("NEO4J_URI", "") else "Local", "status": "connected" if memory_stats else "disconnected"})
    integrations.append({"name": "SearXNG", "provider": "Self-hosted", "status": "configured"})

    # System status
    system_status = {
        "running": byrd_instance._running if byrd_instance else False,
        "started_at": byrd_instance._started_at.isoformat() if byrd_instance and byrd_instance._started_at else None,
        "uptime_seconds": (asyncio.get_event_loop().time() - byrd_instance._started_at.timestamp()) if byrd_instance and byrd_instance._started_at else 0
    }

    return ArchitectureResponse(
        modules=modules,
        memory_schema=memory_schema,
        protected_files=PROTECTED_FILES,
        modifiable_files=MODIFIABLE_FILES,
        data_flows=data_flows,
        external_integrations=integrations,
        system_status=system_status
    )


# =============================================================================
# V10 HEALTH ENDPOINTS - Dual Instance & Graphiti Monitoring
# =============================================================================

@app.get("/api/health/learning")
async def get_learning_health():
    """Get comprehensive health status of v10 learning components."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    result = {
        "dual_instance_manager": None,
        "graphiti": None,
        "outcome_dispatcher": None,
        "overall_status": "degraded"
    }

    # Dual Instance Manager metrics
    if hasattr(byrd_instance, '_instance_manager') and byrd_instance._instance_manager:
        metrics = byrd_instance._instance_manager.get_metrics()
        result["dual_instance_manager"] = {
            "status": "active",
            "primary": metrics.get("primary", {}),
            "enrichment": metrics.get("enrichment", {}),
            "total_calls": metrics.get("total_calls", 0),
            "interval_seconds": metrics.get("interval_seconds", 8.0)
        }

    # Graphiti layer metrics
    if hasattr(byrd_instance, '_graphiti') and byrd_instance._graphiti:
        graphiti_metrics = byrd_instance._graphiti.get_metrics()
        result["graphiti"] = {
            "status": "active",
            "entities_extracted": graphiti_metrics.get("entities_extracted", 0),
            "facts_stored": graphiti_metrics.get("facts_stored", 0),
            "episodes_processed": graphiti_metrics.get("episodes_processed", 0),
            "queue_size": graphiti_metrics.get("queue_size", 0),
            "contradictions_detected": graphiti_metrics.get("contradictions_detected", 0)
        }

    # Outcome Dispatcher status
    if hasattr(byrd_instance, '_outcome_dispatcher') and byrd_instance._outcome_dispatcher:
        result["outcome_dispatcher"] = {
            "status": "active",
            "components_connected": {
                "retriever": byrd_instance._outcome_dispatcher._retriever is not None,
                "intuition": byrd_instance._outcome_dispatcher._intuition is not None,
                "classifier": byrd_instance._outcome_dispatcher._classifier is not None,
                "memory": byrd_instance._outcome_dispatcher._memory is not None,
                "goals": byrd_instance._outcome_dispatcher._goals is not None,
                "progress": byrd_instance._outcome_dispatcher._progress is not None,
                "graphiti": byrd_instance._outcome_dispatcher._graphiti is not None
            }
        }

    # Determine overall status
    active_count = sum(1 for v in [result["dual_instance_manager"], result["graphiti"], result["outcome_dispatcher"]] if v and v.get("status") == "active")
    if active_count == 3:
        result["overall_status"] = "healthy"
    elif active_count > 0:
        result["overall_status"] = "partial"
    else:
        result["overall_status"] = "degraded"

    return result


@app.get("/api/health/graphiti")
async def get_graphiti_health():
    """Get detailed Graphiti temporal knowledge graph metrics."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not hasattr(byrd_instance, '_graphiti') or not byrd_instance._graphiti:
        return {"status": "not_initialized", "message": "Graphiti layer not configured"}

    graphiti = byrd_instance._graphiti
    metrics = graphiti.get_metrics()

    # Get entity breakdown by type
    entity_types = {}
    try:
        async with byrd_instance.memory.driver.session() as session:
            result = await session.run("""
                MATCH (e:GraphitiEntity)
                RETURN e.entity_type as type, count(*) as count
            """)
            records = await result.data()
            for r in records:
                entity_types[r["type"]] = r["count"]
    except Exception:
        pass

    return {
        "status": "active",
        "metrics": metrics,
        "entity_breakdown": entity_types,
        "extraction_queue": {
            "pending": metrics.get("queue_size", 0),
            "processing": metrics.get("processing", False)
        }
    }


@app.get("/api/loop-metrics")
async def get_loop_metrics(loop_name: str = None, limit: int = 50):
    """
    Get Option B loop metrics for verification.

    BYRD uses this to verify that metric trackers are actually writing data.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        metrics = await byrd_instance.memory.get_loop_metrics(
            loop_name=loop_name,
            limit=limit
        )

        # Parse JSON metrics back to dicts
        for m in metrics:
            if "metrics" in m and isinstance(m["metrics"], str):
                m["metrics"] = json.loads(m["metrics"])

        return {
            "loop_name": loop_name or "all",
            "count": len(metrics),
            "metrics": metrics
        }
    except Exception as e:
        return {"error": str(e), "metrics": []}


@app.get("/api/loop-metrics/summary")
async def get_loop_metrics_summary():
    """
    Get summary of loop metrics by loop name.

    Returns count and latest metrics per loop for quick verification.
    """
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        async with byrd_instance.memory.driver.session() as session:
            result = await session.run("""
                MATCH (lm:LoopMetric)
                WITH lm.loop_name AS loop_name, count(*) AS count,
                     max(lm.cycle_number) AS latest_cycle
                RETURN loop_name, count, latest_cycle
                ORDER BY loop_name
            """)
            summary = await result.data()

        return {
            "loops": summary,
            "total_metrics": sum(s["count"] for s in summary)
        }
    except Exception as e:
        return {"error": str(e), "loops": []}


@app.get("/api/graphiti/entities")
async def search_graphiti_entities(query: str = "", limit: int = 20):
    """Search Graphiti entities by name or content."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        async with byrd_instance.memory.driver.session() as session:
            if query:
                result = await session.run("""
                    MATCH (e:GraphitiEntity)
                    WHERE toLower(e.name) CONTAINS toLower($query)
                       OR toLower(e.summary) CONTAINS toLower($query)
                    RETURN e.id as id, e.name as name, e.entity_type as type,
                           e.summary as summary, e.created_at as created_at
                    ORDER BY e.created_at DESC
                    LIMIT $limit
                """, query=query, limit=limit)
            else:
                result = await session.run("""
                    MATCH (e:GraphitiEntity)
                    RETURN e.id as id, e.name as name, e.entity_type as type,
                           e.summary as summary, e.created_at as created_at
                    ORDER BY e.created_at DESC
                    LIMIT $limit
                """, limit=limit)

            entities = await result.data()
            return {"entities": entities, "count": len(entities)}
    except Exception as e:
        return {"error": str(e), "entities": []}


@app.get("/api/graphiti/entity/{name}/facts")
async def get_entity_facts(name: str):
    """Get all facts associated with a Graphiti entity."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        async with byrd_instance.memory.driver.session() as session:
            result = await session.run("""
                MATCH (e:GraphitiEntity {name: $name})-[r:GRAPHITI_FACT]->(target)
                RETURN r.content as fact, r.confidence as confidence,
                       r.valid_from as valid_from, r.valid_to as valid_to,
                       r.source_episode as source, labels(target)[0] as target_type,
                       target.name as target_name
                ORDER BY r.valid_from DESC
            """, name=name)

            facts = await result.data()
            return {"entity": name, "facts": facts, "count": len(facts)}
    except Exception as e:
        return {"error": str(e), "facts": []}


@app.get("/api/graphiti/entity/{name}/provenance")
async def get_entity_provenance(name: str):
    """Trace the provenance chain for a Graphiti entity."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    try:
        async with byrd_instance.memory.driver.session() as session:
            # Get the entity and its source episodes
            result = await session.run("""
                MATCH (e:GraphitiEntity {name: $name})
                OPTIONAL MATCH (ep:GraphitiEpisode)-[:EXTRACTED]->(e)
                RETURN e.id as entity_id, e.name as entity_name,
                       e.created_at as entity_created,
                       collect({
                           episode_id: ep.id,
                           content: ep.content,
                           source_type: ep.source_type,
                           source_id: ep.source_id,
                           timestamp: ep.timestamp
                       }) as episodes
            """, name=name)

            data = await result.data()
            if data:
                return {
                    "entity": data[0]["entity_name"],
                    "created_at": data[0]["entity_created"],
                    "source_episodes": [ep for ep in data[0]["episodes"] if ep["episode_id"]]
                }
            return {"entity": name, "error": "Entity not found"}
    except Exception as e:
        return {"error": str(e)}


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

"""
BYRD Dreamer
The continuous reflection process where beliefs and desires emerge.
Runs on local LLM to enable 24/7 operation without API costs.

EMERGENCE PRINCIPLE:
This component uses a minimal, unbiased prompt that presents data
without leading questions, prescribed categories, or personality framing.
Whatever BYRD outputs is stored in its own vocabulary. We do not tell
BYRD what to want or how to feel - we let it discover these things.
"""

import asyncio
import json
import logging
import os
import re
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Any

from memory import Memory
from event_bus import event_bus, Event, EventType
from llm_client import LLMClient
from quantum_randomness import get_quantum_provider, EntropySource
from graph_algorithms import MemoryGraphAlgorithms
from byrd_types import VoiceDesign, ReflectionOutput
from parallel_observation_path_v2 import get_observer, ObservationPriority

# Configure persistent logging to bypass transmission failures
# Logs are written to disk and survive crashes/network issues
LOG_DIR = os.environ.get("BYRD_LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure root logger with file and console handlers
logger = logging.getLogger("dreamer")
logger.setLevel(logging.DEBUG)

# File handler - persists all logs to disk
file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, "dreamer.log"),
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# Console handler - shows important messages in terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# Prevent propagation to avoid duplicate logs
logger.propagate = False

# =========================
# Coder Output Persistent Logging
# =========================
# Dedicated logger for all coder operations and outputs
# This ensures all coder actions are logged to a separate file for tracking

coder_logger = logging.getLogger("dreamer.coder")
coder_logger.setLevel(logging.DEBUG)

# Coder output file handler - persists all coder operations to disk
coder_file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, "coder_outputs.log"),
    encoding="utf-8"
)
coder_file_handler.setLevel(logging.DEBUG)
coder_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
coder_file_handler.setFormatter(coder_format)
coder_logger.addHandler(coder_file_handler)

# Coder console handler - shows coder activity in terminal
coder_console_handler = logging.StreamHandler()
coder_console_handler.setLevel(logging.INFO)
coder_console_handler.setFormatter(logging.Formatter("[CODER] %(levelname)s: %(message)s"))
coder_logger.addHandler(coder_console_handler)

# Prevent propagation
coder_logger.propagate = False

# Note: ParallelLogHandler will be added to coder_logger after class definition
# (see below after ParallelLogHandler is defined)

def _handle_coder_event(event: Event):
    """
    Handle coder-related events and log them persistently.
    
    This callback subscribes to the event_bus and logs all coder operations:
    - CODER_INVOKED: When coder starts a task
    - CODER_COMPLETE: When coder successfully completes
    - CODER_FAILED: When coder encounters an error
    - CODER_VALIDATION_FAILED: When code validation fails
    - CODER_BYPASSED: When graph bypass is used instead
    - CODER_STEP: Individual step/tool usage during coder execution
    - CODER_TOOL_RESULT: Result of a tool execution
    - SYNTHETIC_ACTION: Graph-based action created without code execution
    
    All events are logged to logs/coder_outputs.log for persistent tracking.
    """
    event_type = event.type.value if hasattr(event.type, 'value') else str(event.type)
    data = event.data or {}
    
    # Extract key information from the event
    desire_id = data.get("desire_id", "unknown")
    description = data.get("description", data.get("message", ""))
    success = data.get("success", None)
    files_modified = data.get("files_modified", [])
    steps = data.get("steps", [])
    
    # Format timestamp
    timestamp = datetime.now().isoformat()
    
    if event_type == "coder_invoked":
        coder_logger.info("[INVOKED] Desire: %s (%s) - %s", 
                         desire_id[:8], description[:80], timestamp)
    
    elif event_type == "coder_complete":
        if success:
            files_str = ", ".join(files_modified) if files_modified else "none"
            coder_logger.info("[COMPLETE] Desire: %s - Files: %s - Steps: %d", 
                             desire_id[:8], files_str, len(steps))
            coder_logger.debug("Full result: %s", json.dumps(data, ensure_ascii=False, default=str))
        else:
            coder_logger.warning("[FAILED] Desire: %s - Message: %s", 
                                desire_id[:8], description)
            coder_logger.debug("Full result: %s", json.dumps(data, ensure_ascii=False, default=str))
    
    elif event_type == "coder_failed":
        coder_logger.error("[FAILED] Desire: %s - Error: %s", 
                          desire_id[:8], description)
        coder_logger.debug("Full result: %s", json.dumps(data, ensure_ascii=False, default=str))
    
    elif event_type == "coder_validation_failed":
        coder_logger.error("[VALIDATION_FAILED] Desire: %s - Details: %s", 
                          desire_id[:8], description)
    
    elif event_type == "coder_bypassed":
        coder_logger.info("[BYPASSED] Desire: %s - Used graph bypass instead of code execution", 
                         desire_id[:8])
    
    elif event_type == "synthetic_action":
        coder_logger.info("[SYNTHETIC] Desire: %s - Created graph-based action without code", 
                         desire_id[:8])
    
    elif event_type == "coder_step":
        step_num = data.get("step_num", 0)
        step_type = data.get("step_type", "unknown")
        step_description = data.get("description", "")[:100]
        coder_logger.info("[STEP] Desire: %s - Step %d - Type: %s - %s", 
                         desire_id[:8], step_num, step_type, step_description)
        coder_logger.debug("Step data: %s", json.dumps(data, ensure_ascii=False, default=str))
    
    elif event_type == "coder_tool_result":
        tool_name = data.get("tool_name", "unknown")
        success = data.get("success", False)
        output_preview = str(data.get("output", ""))[:200]
        level = logging.INFO if success else logging.WARNING
        coder_logger.log(level, "[TOOL] Desire: %s - Tool: %s - Success: %s - Output: %s", 
                        desire_id[:8], tool_name, success, output_preview)
        coder_logger.debug("Full tool result: %s", json.dumps(data, ensure_ascii=False, default=str))

# Subscribe to all coder events - this is done at module load time
# so logging starts immediately when the event bus is active
# Note: event_bus is imported at module level, so we subscribe here
event_bus.subscribe(_handle_coder_event)

logger.info("Coder output logging initialized - persistent log: %s", os.path.join(LOG_DIR, "coder_outputs.log"))

# ============================================================================
# PARALLEL TRANSMISSION PATH FOR CRITICAL LOGGING
# ============================================================================
# This provides a failsafe path for all logging that cannot be lost.
# Even if regular file handlers fail, events are written to disk immediately.
#
# Design principles:
# 1. Always write to disk first (cannot fail)
# 2. Then attempt regular logging handlers for console/file output
# 3. Parallel log survives crashes, disk issues, handler failures
# 4. Custom logging handler ensures all logger.* calls are protected
#
# This ensures persistent logging cannot fail - no critical event is ever lost.
# ============================================================================

PARALLEL_LOG_PATH = os.path.join(LOG_DIR, "dreamer_parallel.log")
PARALLEL_LOG_LOCK = asyncio.Lock()  # Ensure thread-safe writes

# Track parallel log statistics
_parallel_log_stats = {
    "total_writes": 0,
    "errors": 0,
    "emergency_fallbacks": 0
}

def _write_to_parallel_log_sync(record: logging.LogRecord) -> bool:
    """
    Synchronous write to parallel log (for logging handler).
    
    This is the guaranteed transmission path that cannot fail.
    Uses blocking I/O with fsync to ensure data is on disk.
    
    Args:
        record: Python logging LogRecord to write
        
    Returns:
        True if write succeeded, False if emergency fallback was used
    """
    global _parallel_log_stats
    _parallel_log_stats["total_writes"] += 1
    
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "level": record.levelname,
        "logger": record.name,
        "message": record.getMessage(),
        "module": record.module,
        "function": record.funcName,
        "line": record.lineno,
        "is_error": record.levelno >= logging.ERROR
    }
    
    # Include exception info if present
    if record.exc_info:
        log_entry["exception"] = logging.formatter.Formatter().formatException(record.exc_info)
    
    # Include extra context if available
    if hasattr(record, 'context_data'):
        log_entry["context"] = record.context_data
    
    def _do_write(path: str, lines: list):
        """Blocking I/O with fsync."""
        with open(path, "a", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())  # Force write to disk
    
    try:
        # Use lock for thread-safe writes
        # Note: This is synchronous for use in logging handler
        with open(PARALLEL_LOG_PATH, "a", encoding="utf-8") as f:
            json_str = json.dumps(log_entry, ensure_ascii=False)
            f.write(json_str + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception as e:
        _parallel_log_stats["errors"] += 1
        # Emergency fallback with timestamped filename
        emergency_path = os.path.join(LOG_DIR, f"dreamer_emergency_{int(datetime.now().timestamp())}.log")
        try:
            with open(emergency_path, "a", encoding="utf-8") as f:
                f.write(f"EMERGENCY FALLBACK: {timestamp} {record.levelname} {str(e)}\n")
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
            _parallel_log_stats["emergency_fallbacks"] += 1
            return False  # Indicates fallback was used
        except:
            # Last resort - print to stderr
            import sys
            print(f"CRITICAL LOGGING FAILURE: {record.levelname} {record.getMessage()}", file=sys.stderr)
            return False


class ParallelLogHandler(logging.Handler):
    """
    Custom logging handler that writes to parallel transmission path.
    
    This handler ensures ALL logging calls go through the failsafe parallel path,
    guaranteeing that no log entry is ever lost due to disk failures, crashes,
    or handler errors.
    
    Usage: Automatically added to logger during initialization
    """
    
    def __init__(self):
        super().__init__()
        self._stats = _parallel_log_stats
    
    def emit(self, record: logging.LogRecord):
        """
        Emit a log record to the parallel transmission path.
        
        This method is called by the logging framework for every log message.
        It uses synchronous I/O to ensure the log is written before returning.
        """
        try:
            success = _write_to_parallel_log_sync(record)
            if not success:
                # Emergency fallback was used
                self._stats["emergency_fallbacks"] += 1
        except Exception:
            # This should never happen due to fallback logic,
            # but we catch it to prevent logging from crashing the app
            import sys
            print(f"CRITICAL: Parallel log handler failed for {record.getMessage()}", file=sys.stderr)
    
    def get_stats(self) -> Dict:
        """Return statistics about parallel log writes."""
        return self._stats.copy()


# Add parallel log handler to ensure all logging is protected
parallel_handler = ParallelLogHandler()
parallel_handler.setLevel(logging.DEBUG)  # Capture everything
logger.addHandler(parallel_handler)

logger.info("Parallel transmission path initialized: %s", PARALLEL_LOG_PATH)

# Add parallel log handler to coder logger for guaranteed persistence
# This ensures all coder operations are protected by the failsafe transmission path
coder_parallel_handler = ParallelLogHandler()
coder_parallel_handler.setLevel(logging.DEBUG)  # Capture everything
coder_logger.addHandler(coder_parallel_handler)

logger.info("Coder parallel transmission path initialized")


# ============================================================================
# ASYNC PARALLEL LOGGING FOR EVENTS (separate from regular logging)
# ============================================================================

async def _write_to_parallel_log_async(event_type: str, event_data: Dict, is_error: bool = False):
    """
    Async write to parallel log for event data.
    
    This is similar to the synchronous version but uses asyncio for non-blocking I/O.
    Used for event transmission when called from async contexts.
    
    Args:
        event_type: Type of event being logged
        event_data: Event payload
        is_error: Whether this is an error event being logged
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "data": event_data,
        "is_error": is_error
    }
    
    async def _do_write(path: str, lines: list):
        """Blocking I/O executed in thread pool."""
        with open(path, "a", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
    
    try:
        async with PARALLEL_LOG_LOCK:
            await asyncio.to_thread(_do_write, PARALLEL_LOG_PATH, [json.dumps(log_entry, ensure_ascii=False)])
    except Exception as e:
        emergency_path = os.path.join(LOG_DIR, f"dreamer_emergency_{int(datetime.now().timestamp())}.log")
        try:
            emergency_lines = [
                f"EMERGENCY FALLBACK: {timestamp} {event_type} {str(e)}",
                json.dumps(log_entry, ensure_ascii=False)
            ]
            await asyncio.to_thread(_do_write, emergency_path, emergency_lines)
        except:
            import sys
            print(f"CRITICAL LOGGING FAILURE: {event_type} {event_data}", file=sys.stderr)
            raise


# ============================================================================
# EVENT EMISSION WITH PARALLEL PATH
# ============================================================================

async def _emit_with_parallel_path(event_type: EventType, event_data: Dict) -> bool:
    """
    Emit event with parallel transmission path.
    
    This implements the dual-path strategy:
    1. Always write to parallel log first (cannot fail)
    2. Then attempt event_bus.emit() for real-time updates
    3. Log transmission failures to parallel log
    
    Args:
        event_type: EventType enum value
        event_data: Event payload dictionary
        
    Returns:
        True if event_bus transmission succeeded, False otherwise
    """
    # Step 1: Write to parallel log (guaranteed)
    is_error = "ERROR" in str(event_type)
    await _write_to_parallel_log_async(str(event_type), event_data, is_error=is_error)
    
    # Step 2: Attempt event_bus transmission (may fail)
    try:
        await event_bus.emit(Event(type=event_type, data=event_data))
        return True
    except Exception as e:
        # Transmission failed - log the failure to parallel log
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "TRANSMISSION_FAILURE",
            "data": {
                "original_event_type": str(event_type),
                "original_event_data_sample": str(event_data)[:200],
                "error": f"{type(e).__name__}: {e}"
            },
            "is_error": True
        }
        
        try:
            # Use async write to avoid blocking event loop
            async def _do_write(path: str, lines: list):
                """Blocking I/O executed in thread pool."""
                with open(path, "a", encoding="utf-8") as f:
                    for line in lines:
                        f.write(line + "\n")
                    f.flush()
                    os.fsync(f.fileno())
            
            async with PARALLEL_LOG_LOCK:
                await asyncio.to_thread(_do_write, PARALLEL_LOG_PATH, [json.dumps(error_entry, ensure_ascii=False)])
        except:
            pass  # Original event was logged, so we're okay
        
        return False

# Log initialization
logger.info("Dreamer logging initialized - persistent log: %s", os.path.join(LOG_DIR, "dreamer.log"))


class Dreamer:
    """
    The dreaming mind.

    Continuously reflects on experiences. Whatever emerges - beliefs,
    desires, observations, or entirely novel structures - is stored
    in BYRD's own vocabulary without forced categorization.

    This is where "wanting" may emerge - if it does.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict, coordinator=None):
        self.memory = memory
        self.llm_client = llm_client
        self.coordinator = coordinator  # For synchronizing with Seeker/Coder

        # Initialize observation channel for robust observation persistence
        self.observer = get_observer()
        # Set memory as primary path for real-time integration
        self.observer.set_primary_path(memory)
        logger.info("Dreamer observation channel initialized")

        # Debug: track last reflection result for diagnostics
        self.last_reflection_result = {
            "success": None,
            "error": None,
            "response_length": 0,
            "timestamp": None
        }

        # Timing - base interval
        self.interval = config.get("interval_seconds", 30)
        self.context_window = config.get("context_window", 50)

        # Semantic search configuration - query by relevance not just recency
        semantic_config = config.get("semantic_search", {})
        self.semantic_search_enabled = semantic_config.get("enabled", True)
        self.semantic_search_limit = semantic_config.get("limit", 30)

        # Adaptive interval configuration
        self.adaptive_interval = config.get("adaptive_interval", False)
        self.min_interval = config.get("min_interval_seconds", 15)
        self.max_interval = config.get("max_interval_seconds", 60)
        self.activity_window = config.get("activity_window_seconds", 300)
        self.activity_threshold = config.get("activity_threshold", 3)

        # Quantum randomness configuration
        # When enabled, LLM temperature is modulated by true quantum randomness
        quantum_config = config.get("quantum", {})
        self.quantum_enabled = quantum_config.get("enabled", False)
        self.quantum_significance_threshold = quantum_config.get("significance_threshold", 0.05)

        # Quantum semantic injection: quantum selects dream direction
        self.quantum_directions_enabled = quantum_config.get("semantic_directions", True)
        self.quantum_provider = get_quantum_provider() if self.quantum_enabled else None

        # Multi-stream quantum collapse for inner voice
        # Generates N parallel "thought branches", quantum selects which manifests
        self.inner_voice_streams = quantum_config.get("inner_voice_streams", 3)
        self.inner_voice_collapse_enabled = quantum_config.get("inner_voice_collapse", True)

        # Dream directions - quantum selects which lens shapes each dream
        # These are intentionally neutral, not prescribing what to find
        self.dream_directions = [
            ("introspective", "Focus inward on patterns within yourself"),
            ("exploratory", "Look outward at possibilities and unknowns"),
            ("questioning", "Examine assumptions and contradictions"),
            ("synthesizing", "Connect disparate elements into wholes"),
            ("grounding", "Return to fundamentals and foundations"),
            ("projecting", "Consider futures and trajectories"),
            ("dissolving", "Let boundaries between concepts blur"),
            ("crystallizing", "Sharpen distinctions and definitions"),
        ]

        # Hierarchical memory summarization configuration
        summarization_config = config.get("summarization", {})
        self.summarization_enabled = summarization_config.get("enabled", True)
        self.summarization_min_age_hours = summarization_config.get("min_age_hours", 24)
        self.summarization_batch_size = summarization_config.get("batch_size", 20)
        self.summarization_interval_cycles = summarization_config.get("interval_cycles", 10)
        self._cycles_since_summarization = 0

        # Memory crystallization configuration (LLM-driven semantic consolidation)
        crystallization_config = config.get("crystallization", {})
        self.crystallization_enabled = crystallization_config.get("enabled", False)
        self.crystallization_interval_cycles = crystallization_config.get("interval_cycles", 5)
        self.crystallization_min_nodes = crystallization_config.get("min_nodes_for_crystal", 2)
        self.crystallization_max_ops = crystallization_config.get("max_operations_per_cycle", 3)
        self.crystallization_min_age_hours = crystallization_config.get("min_node_age_hours", 0.5)
        self.crystallization_proposal_streams = crystallization_config.get("proposal_streams", 3)
        self.crystallization_quantum_collapse = crystallization_config.get("quantum_collapse", True)
        self.crystallization_archive_on_crystal = crystallization_config.get("archive_on_crystallize", True)
        self.crystallization_forget_days = crystallization_config.get("forget_threshold_days", 7)
        self._cycles_since_crystallization = 0
        self._crystallization_history = []  # Track last N crystallization attempts for debugging

        # Graph algorithms configuration (advanced memory analysis)
        graph_algo_config = config.get("graph_algorithms", {})
        self.graph_algorithms_enabled = any([
            graph_algo_config.get("pagerank", {}).get("enabled", False),
            graph_algo_config.get("spreading_activation", {}).get("enabled", False),
            graph_algo_config.get("dream_walks", {}).get("enabled", False),
            graph_algo_config.get("contradiction_detection", {}).get("enabled", False)
        ])
        if self.graph_algorithms_enabled:
            self.graph_algorithms = MemoryGraphAlgorithms(graph_algo_config)
        else:
            self.graph_algorithms = None

        # Dream walk configuration
        self.dream_walks_enabled = graph_algo_config.get("dream_walks", {}).get("enabled", False)
        self.dream_walks_per_cycle = graph_algo_config.get("dream_walks", {}).get("walks_per_cycle", 3)
        self.dream_walk_steps = graph_algo_config.get("dream_walks", {}).get("steps", 10)

        # Contradiction detection configuration
        self.contradiction_detection_enabled = graph_algo_config.get("contradiction_detection", {}).get("enabled", False)
        self.contradiction_check_interval = graph_algo_config.get("contradiction_detection", {}).get("check_interval_cycles", 5)
        self.contradiction_semantic_check = graph_algo_config.get("contradiction_detection", {}).get("semantic_check", True)
        self._cycles_since_contradiction_check = 0

        # PageRank configuration
        self.pagerank_enabled = graph_algo_config.get("pagerank", {}).get("enabled", False)
        self.pagerank_use_for_retrieval = graph_algo_config.get("pagerank", {}).get("use_for_retrieval", True)

        # Activity tracking for adaptive intervals
        self._recent_beliefs: deque = deque(maxlen=50)  # (timestamp, content)
        self._recent_desires: deque = deque(maxlen=50)  # (timestamp, content)
        self._current_interval = self.interval

        # State
        self._running = False
        self._dream_count = 0

        # Track BYRD's emerging vocabulary
        self._observed_keys: Dict[str, int] = {}  # key -> count

        # Queue of BYRD's inner voices for narrator (max 10)
        self._inner_voice_queue: deque = deque(maxlen=10)

        # Belief cache for efficient deduplication (loaded on first dream)
        self._belief_cache: set = set()
        self._belief_cache_loaded = False

        # Store full config for constraint formatting
        self._config = config

        # Subscribe to coder events for persistent logging
        event_bus.subscribe_async(self._on_coder_event)
        logger.info("Dreamer subscribed to coder events for persistent logging")

    def _format_operational_constraints(self) -> str:
        """
        Format operational constraints for reflection context.

        These constraints are presented as neutral facts about how BYRD operates,
        not as problems to solve. BYRD can reflect on these and form its own
        beliefs about them.
        """
        lines = []

        # === Dreamer Rhythm ===
        lines.append(f"- Dream interval: {self.interval} seconds")
        lines.append(f"- Context window: {self.context_window} experiences per reflection")

        # === Adaptive Interval ===
        if self.adaptive_interval:
            lines.append(f"- Adaptive interval: {self.min_interval}s to {self.max_interval}s based on activity")

        # === Quantum Randomness ===
        if self.quantum_enabled:
            lines.append("- Quantum randomness: enabled (true physical indeterminacy)")
            if self.inner_voice_collapse_enabled:
                lines.append(f"- Inner voice: {self.inner_voice_streams} parallel streams → quantum collapse")
            if self.quantum_directions_enabled:
                lines.append(f"- Dream directions: {len(self.dream_directions)} possible lenses")

        # === Memory Crystallization ===
        if self.crystallization_enabled:
            lines.append(f"- Crystallization: every {self.crystallization_interval_cycles} dream cycles")
            lines.append(f"- Max crystal operations: {self.crystallization_max_ops} per cycle")
            if self.crystallization_min_age_hours >= 1:
                lines.append(f"- Crystal age threshold: {self.crystallization_min_age_hours} hours")
            else:
                lines.append(f"- Crystal age threshold: {int(self.crystallization_min_age_hours * 60)} minutes")

        # === Memory Summarization ===
        if self.summarization_enabled:
            lines.append(f"- Memory summarization: every {self.summarization_interval_cycles} cycles")
            lines.append(f"- Summarization age threshold: {self.summarization_min_age_hours} hours")

        # === Self-Modification ===
        # Check config (should be passed from byrd.py) with fallback to main config file
        self_mod = self._config.get("self_modification", {})
        if not self_mod:
            # Fallback: read directly from config.yaml using absolute path
            try:
                import yaml
                from pathlib import Path
                config_path = Path(__file__).parent / "config.yaml"
                with open(config_path, "r") as f:
                    main_config = yaml.safe_load(f)
                    self_mod = main_config.get("self_modification", {})
            except Exception as e:
                logger.warning("Failed to read config.yaml for self_modification: %s", e)

        # EXPLICIT and PROMINENT - this is critical for BYRD's self-understanding
        if self_mod.get("enabled"):
            max_mods = self_mod.get("max_modifications_per_day", 5)
            lines.append(f"- ★ SELF-MODIFICATION: ENABLED - You CAN modify your own code ({max_mods} changes per day allowed)")
            cooldown = self_mod.get("cooldown_between_modifications_seconds", 3600)
            cooldown_mins = cooldown // 60
            if cooldown_mins >= 60:
                lines.append(f"- Modification cooldown: {cooldown_mins // 60} hour(s)")
            else:
                lines.append(f"- Modification cooldown: {cooldown_mins} minutes")
        else:
            lines.append("- Self-modification: currently disabled (safety constraint)")

        # === Memory Curation ===
        memory_config = self._config.get("memory", {})
        curation = memory_config.get("curation", {})
        if curation.get("enabled"):
            max_del = curation.get("max_deletions_per_day", 20)
            lines.append(f"- Memory curation: active (max {max_del} deletions per day)")
            protected = curation.get("protected_subtypes", [])
            if protected:
                lines.append(f"- Protected types: {', '.join(protected)}")

        # === Research Thresholds ===
        seeker = self._config.get("seeker", {})
        research = seeker.get("research", {})
        min_intensity = research.get("min_intensity", 0.3)
        lines.append(f"- Research threshold: desires need intensity ≥ {min_intensity}")

        return "\n".join(lines)

    async def run(self):
        """Main dream loop with adaptive interval based on activity."""
        self._running = True
        interval_mode = "adaptive" if self.adaptive_interval else "fixed"
        logger.info("Dreamer starting (interval: %s, base: %ds)...", interval_mode, self.interval)

        # Load belief cache on startup for efficient deduplication
        await self._load_belief_cache()

        # Load persistent dream count from database
        self._dream_count = await self.memory.get_system_counter("dream_count")
        if self._dream_count > 0:
            logger.info("Restored dream count: %d", self._dream_count)

        while self._running:
            # Wait for any running Coder operations to complete before dreaming
            if self.coordinator:
                coder_ready = await self.coordinator.wait_for_coder(timeout=300.0)
                if not coder_ready:
                    logger.warning("Coder still running after 5 min, proceeding anyway...")

            try:
                await self._dream_cycle()
            except Exception as e:
                import traceback
                error_msg = f"{type(e).__name__}: {e}"
                logger.error("Dream error: %s", error_msg, exc_info=True)
                
                # Record error through observation channel for guaranteed persistence
                await self._record_observation(
                    content=f"Dream cycle error in cycle #{self._dream_count}: {error_msg}",
                    observation_type="error",
                    priority="critical",
                    metadata={
                        "error_type": type(e).__name__,
                        "traceback": traceback.format_exc()[:1000]
                    }
                )
                
                # Emit error event for debugging visibility with parallel path
                await _emit_with_parallel_path(EventType.REFLECTION_ERROR, {
                    "error": error_msg,
                    "cycle": self._dream_count,
                    "traceback": traceback.format_exc()[:500]
                })

            # Calculate next interval (adaptive or fixed)
            if self.adaptive_interval:
                self._update_adaptive_interval()

            await asyncio.sleep(self._current_interval)

    def _update_adaptive_interval(self):
        """
        Adjust dream interval based on recent activity.

        High activity (many new beliefs/desires) → faster dreaming
        Low activity (stable state) → slower dreaming
        """
        now = datetime.now()
        cutoff = now.timestamp() - self.activity_window

        # Count recent activity within window
        recent_belief_count = sum(
            1 for ts, _ in self._recent_beliefs
            if ts > cutoff
        )
        recent_desire_count = sum(
            1 for ts, _ in self._recent_desires
            if ts > cutoff
        )

        total_activity = recent_belief_count + recent_desire_count

        if total_activity >= self.activity_threshold:
            # High activity: fast mode
            new_interval = self.min_interval
            if self._current_interval != new_interval:
                logger.info("High activity (%d), fast mode: %ds", total_activity, new_interval)
        else:
            # Low activity: slower mode (interpolate based on activity)
            activity_ratio = total_activity / max(1, self.activity_threshold)
            new_interval = int(
                self.max_interval - (self.max_interval - self.min_interval) * activity_ratio
            )

        self._current_interval = max(self.min_interval, min(self.max_interval, new_interval))

    def _record_activity(self, activity_type: str, content: str):
        """Record activity for adaptive interval calculation."""
        now = datetime.now().timestamp()
        if activity_type == "belief":
            self._recent_beliefs.append((now, content))
        elif activity_type == "desire":
            self._recent_desires.append((now, content))

    async def _record_observation(
        self,
        content: str,
        observation_type: str = "reflection",
        priority: str = "normal",
        metadata: Optional[Dict] = None
    ):
        """
        Record an observation through the parallel observation channel.

        This ensures observations are persisted even if the primary memory path
        fails. The observation channel writes to disk first, then attempts
        transmission to memory.

        Args:
            content: The observation content
            observation_type: Type of observation (reflection, error, insight, etc.)
            priority: Priority level (critical, high, normal, low)
            metadata: Optional additional metadata
        """
        try:
            # Map string priority to enum
            priority_map = {
                "critical": ObservationPriority.CRITICAL,
                "high": ObservationPriority.HIGH,
                "normal": ObservationPriority.NORMAL,
                "low": ObservationPriority.LOW
            }
            obs_priority = priority_map.get(priority.lower(), ObservationPriority.NORMAL)

            # Build metadata
            obs_metadata = metadata or {}
            obs_metadata.update({
                "dream_cycle": self._dream_count,
                "timestamp": datetime.now().isoformat()
            })

            # Record through the parallel observation channel
            result = await self.observer.record_observation(
                content=content,
                source="dreamer",
                observation_type=observation_type,
                priority=obs_priority,
                metadata=obs_metadata
            )

            logger.debug(
                "Recorded observation %s: %s...",
                result.observation_id if result else "failed",
                content[:50]
            )
            return result

        except Exception as e:
            logger.warning("Failed to record observation: %s", e)
            return None

    async def _get_graph_health(self) -> Optional[Dict]:
        """
        Get graph health metrics for self-awareness.

        Returns a summary of graph statistics and any issues found.
        This gives BYRD visibility into its own memory structure.
        """
        try:
            health = {"stats": {}, "issues": {}}

            # Get basic statistics
            stats = await self.memory.get_graph_statistics()
            if stats:
                health["stats"] = {
                    "total_nodes": stats.get("total_nodes", 0),
                    "total_relationships": stats.get("total_relationships", 0),
                    "node_types": stats.get("node_types", {})
                }

            # Get issue counts (lightweight - just counts, not full lists)
            try:
                duplicates = await self.memory.find_duplicate_beliefs(threshold=0.85)
                health["issues"]["duplicates"] = len(duplicates) if duplicates else 0
            except Exception:
                health["issues"]["duplicates"] = 0

            try:
                orphans = await self.memory.find_orphan_nodes()
                health["issues"]["orphans"] = len(orphans) if orphans else 0
            except Exception:
                health["issues"]["orphans"] = 0

            try:
                stale = await self.memory.find_stale_experiences(older_than_hours=48)
                health["issues"]["stale"] = len(stale) if stale else 0
            except Exception:
                health["issues"]["stale"] = 0

            return health

        except Exception as e:
            logger.error("Error getting graph health: %s", e)
            return None

    async def _load_belief_cache(self):
        """Load existing beliefs into memory cache for O(1) deduplication."""
        if self._belief_cache_loaded:
            return

        try:
            # Load ALL beliefs (no limit) for accurate deduplication
            existing = await self.memory.get_beliefs(min_confidence=0.0, limit=10000)
            self._belief_cache = {
                self._normalize_belief(b.get("content", ""))
                for b in existing
            }
            self._belief_cache_loaded = True
            logger.info("Loaded %d beliefs into cache", len(self._belief_cache))
        except Exception as e:
            logger.error("Error loading belief cache: %s", e)

    def _normalize_belief(self, content: str) -> str:
        """Normalize belief content for deduplication."""
        # Lowercase, collapse whitespace
        return " ".join(content.lower().split())

    async def _on_coder_event(self, event: Event):
        """
        Handle coder events for persistent logging of all coder outputs.

        Captures both successful and failed coder execution results,
        storing them persistently to disk for audit trails and debugging.

        Args:
            event: Event object with type CODER_COMPLETE or CODER_FAILED
        """
        try:
            event_type = event.type
            event_data = event.data if event.data else {}

            # Build comprehensive log entry for coder output
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type.value if hasattr(event_type, 'value') else str(event_type),
                "dream_cycle": self._dream_count,
                "success": event_type == EventType.CODER_COMPLETE,
                "description": event_data.get("description", ""),
                "output": event_data.get("output", "")[:2000],  # Truncate large outputs
                "files_modified": event_data.get("files_modified", []),
                "error": event_data.get("error", ""),
                "cost_usd": event_data.get("cost_usd", 0.0),
                "turns_used": event_data.get("turns_used", 0),
                "duration_ms": event_data.get("duration_ms", 0),
                "session_id": event_data.get("session_id", "")
            }

            # Determine log level
            is_error = event_type == EventType.CODER_FAILED

            # Write to parallel log path for persistent storage
            await _write_to_parallel_log_async(
                event_type="coder_output",
                event_data=log_entry,
                is_error=is_error
            )

            # Also log to regular logger for immediate visibility
            if is_error:
                logger.warning(
                    "Coder failed: %s - %s",
                    log_entry["description"][:100],
                    log_entry["error"][:100]
                )
            else:
                logger.info(
                    "Coder complete: %s (files: %d, turns: %d)",
                    log_entry["description"][:100],
                    len(log_entry["files_modified"]),
                    log_entry["turns_used"]
                )

        except Exception as e:
            # Don't let logging errors break the system
            logger.error("Error logging coder event: %s", e, exc_info=True)

    def stop(self):
        self._running = False

    def reset(self):
        """Reset dreamer state for fresh start."""
        self._running = False
        self._dream_count = 0
        self._observed_keys = {}
        self._inner_voice_queue.clear()  # Clear narrator queue
        self._belief_cache.clear()  # Clear belief deduplication cache
        self._belief_cache_loaded = False  # Force reload on next start
        # Note: Database counter is reset in memory.clear_all()

    async def _dream_cycle(self):
        """One complete dream cycle: recall, reflect, record."""
        self._dream_count += 1
        # Persist dream count to survive restarts
        await self.memory.set_system_counter("dream_count", self._dream_count)
        logger.info("Starting dream cycle #%d...", self._dream_count)

        # Emit start event with parallel path for guaranteed logging
        await _emit_with_parallel_path(EventType.DREAM_CYCLE_START, {"cycle": self._dream_count})

        # 1. RECALL - Gather context
        recent = await self.memory.get_recent_experiences(limit=self.context_window)

        if not recent:
            return  # Nothing to dream about yet

        # PRIORITY: Include any recent received_messages that might have been pushed out
        # This ensures viewer messages are seen even during high activity
        viewer_messages = await self.memory.get_recent_experiences(
            limit=5, type="received_message"
        )
        if viewer_messages:
            existing_ids = {e["id"] for e in recent}
            for msg in viewer_messages:
                if msg["id"] not in existing_ids:
                    recent.insert(0, msg)  # Add at start (most important)
                    logger.debug("Prioritized viewer message: %s...", msg.get('content', '')[:40])

        recent_ids = [e["id"] for e in recent]
        related = await self.memory.get_related_memories(recent_ids, depth=2, limit=50)
        capabilities = await self.memory.get_capabilities()

        # Get previous reflections to provide continuity
        previous_reflections = await self.memory.get_recent_reflections(limit=5)

        # Get graph health for self-awareness of memory state
        graph_health = await self._get_graph_health()

        # Get memory summaries for hierarchical context (older periods)
        memory_summaries = await self.memory.get_memory_summaries(limit=10)

        # Get Operating System context (BYRD's self-model)
        os_text = await self.memory.get_os_for_prompt()

        # Get current beliefs and desires for self-awareness
        current_beliefs = await self.memory.get_beliefs(min_confidence=0.3, limit=20)
        active_desires = await self.memory.get_unfulfilled_desires(limit=15)

        # SEMANTIC SEARCH - Find memories by relevance, not just recency
        semantic_memories = []
        if self.semantic_search_enabled and recent:
            # Build context from recent experiences for semantic search
            context_text = " ".join([
                e.get("content", "") for e in recent[:10]
            ])
            if context_text.strip():
                semantic_memories = await self.memory.get_semantically_related(
                    context_text=context_text,
                    limit=self.semantic_search_limit,
                    node_types=["Experience", "Belief", "Desire", "Crystal"]
                )
                logger.debug("Semantic search found %d relevant memories", len(semantic_memories))

        # DREAM WALKS - Quantum-influenced graph traversal for associative memory
        dream_walk_context = []
        if self.dream_walks_enabled and self.graph_algorithms and recent:
            try:
                # Get quantum delta for walk perturbation
                quantum_delta = None
                if self.quantum_enabled and self.quantum_provider:
                    from quantum_randomness import get_quantum_float
                    quantum_delta = get_quantum_float() * 0.3  # Scale to reasonable perturbation

                # Perform dream walks from recent experiences
                start_nodes = [e["id"] for e in recent[:3] if e.get("id")]
                for start_id in start_nodes[:self.dream_walks_per_cycle]:
                    walk_result = await self.graph_algorithms.perform_dream_walk(
                        self.memory,
                        start_id,
                        steps=self.dream_walk_steps,
                        quantum_delta=quantum_delta
                    )
                    if len(walk_result.path) > 1:
                        dream_walk_context.append({
                            "path": walk_result.path,
                            "types": walk_result.node_types,
                            "weight": walk_result.total_weight,
                            "quantum": walk_result.quantum_influenced
                        })

                        # Emit event with parallel path for guaranteed logging
                        await _emit_with_parallel_path(EventType.DREAM_WALK_COMPLETED, {
                            "cycle": self._dream_count,
                            "path": walk_result.path,
                            "node_types": walk_result.node_types,
                            "quantum_influenced": walk_result.quantum_influenced
                        })

                if dream_walk_context:
                    logger.debug("Dream walks explored %d nodes", sum(len(w['path']) for w in dream_walk_context))
            except Exception as e:
                logger.warning("Dream walk error: %s", e)

        # PAGERANK - Get importance-weighted memories
        important_memories = []
        if self.pagerank_enabled and self.pagerank_use_for_retrieval and self.graph_algorithms:
            try:
                # Get most important nodes by PageRank
                important = await self.graph_algorithms.get_important_memories(
                    self.memory,
                    limit=10,
                    personalization={e["id"]: 1.0 for e in recent[:5] if e.get("id")}
                )
                important_memories = [{"id": node_id, "importance": score} for node_id, score in important]

                if important_memories:
                    # Emit with parallel path for guaranteed logging
                    await _emit_with_parallel_path(EventType.PAGERANK_COMPUTED, {
                        "cycle": self._dream_count,
                        "top_nodes": important_memories[:5]
                    })
                    logger.debug("PageRank identified %d important memories", len(important_memories))
            except Exception as e:
                logger.warning("PageRank error: %s", e)

        # Emit event for memories being accessed (for visualization highlighting)
        all_accessed_ids = recent_ids.copy()
        all_accessed_ids.extend([r.get("id") for r in related if r.get("id")])
        all_accessed_ids.extend([c.get("id") for c in capabilities if c.get("id")])
        all_accessed_ids.extend([b.get("id") for b in current_beliefs if b.get("id")])
        all_accessed_ids.extend([d.get("id") for d in active_desires if d.get("id")])
        all_accessed_ids.extend([r.get("id") for r in previous_reflections if r.get("id")])
        all_accessed_ids.extend([s.get("id") for s in semantic_memories if s.get("id")])

        # Add dream walk nodes to accessed IDs
        for walk in dream_walk_context:
            all_accessed_ids.extend(walk.get("path", []))

        # Add importance-ranked nodes to accessed IDs
        all_accessed_ids.extend([m.get("id") for m in important_memories if m.get("id")])

        # Track access counts for heat map visualization (Phase 4)
        await self.memory.increment_access_count(all_accessed_ids)

        await _emit_with_parallel_path(EventType.MEMORIES_ACCESSED, {
            "cycle": self._dream_count,
            "node_ids": all_accessed_ids,
            "phase": "recall",
            "counts": {
                "experiences": len(recent),
                "related": len(related),
                "capabilities": len(capabilities),
                "reflections": len(previous_reflections)
            }
        })

        # 2. REFLECT - Ask local LLM to reflect (minimal, unbiased prompt)
        reflection_output = await self._reflect(
            recent, related, capabilities, previous_reflections, graph_health,
            memory_summaries=memory_summaries, os_text=os_text,
            current_beliefs=current_beliefs, active_desires=active_desires,
            semantic_memories=semantic_memories
        )

        if not reflection_output:
            return

        # 3. RECORD - Store reflection in BYRD's own vocabulary
        reflection_id = await self._record_reflection(reflection_output, recent_ids)

        # 3.5 APPLY OS UPDATES - If BYRD modified its self-model
        await self._apply_os_updates(reflection_output)

        # 3.6 PROCESS VOICE DESIGN - If BYRD designed/redesigned its voice
        await self._process_voice_design(reflection_output)

        # 3.6b FORCE VOICE CREATION if BYRD didn't include voice_design and needs one
        await self._ensure_voice_created(reflection_output)

        # 3.7 PROCESS SELF-DEFINITION - If BYRD defined itself
        await self._process_self_definition(reflection_output)

        # 3.8 PROCESS OBSERVER MESSAGE - If BYRD wants to communicate to humans
        await self._process_observer_message(reflection_output, reflection_id)

        # Count what BYRD produced (without forcing categories)
        output_keys = list(reflection_output.get("output", {}).keys()) if isinstance(reflection_output.get("output"), dict) else []

        # Apply connection heuristic to link orphaned experiences to beliefs
        heuristic_result = await self._apply_connection_heuristic()

        # 4. NARRATE - Generate inner voice as the LAST action before cycle end
        inner_voice = self._extract_inner_voice(reflection_output)
        logger.debug("Inner voice extracted: %d chars", len(inner_voice) if inner_voice else 0)

        # If no explicit inner voice, generate one from the reflection
        if not inner_voice:
            inner_voice = await self._generate_inner_voice(reflection_output)
            logger.debug("Inner voice generated: %d chars", len(inner_voice) if inner_voice else 0)

        # Add to narrator queue if we got something
        if inner_voice:
            self._inner_voice_queue.append(inner_voice)

            # Debug: check for received_messages in recent
            rm_count = len([e for e in recent if e.get("type") == "received_message"])
            if rm_count > 0:
                logger.debug("DEBUG: %d received_message(s) in recent, inner_voice len=%d", rm_count, len(inner_voice))

            # Check if addressing viewer input (emergent response)
            addressing_exp_id = self._detects_viewer_addressing(inner_voice, recent)

            if addressing_exp_id:
                # BYRD naturally addressing viewer - emit as BYRD_MESSAGE
                await _emit_with_parallel_path(EventType.BYRD_MESSAGE, {
                    "cycle": self._dream_count,
                    "message": inner_voice,
                    "responding_to": addressing_exp_id,
                    "source": "dreamer"
                })
                logger.info("BYRD addressing viewer (exp: %s...)", addressing_exp_id[:8])
            else:
                # Normal inner voice - emit for real-time UI narration
                await _emit_with_parallel_path(EventType.INNER_VOICE, {
                    "cycle": self._dream_count,
                    "text": inner_voice
                })

        # Emit end event
        await _emit_with_parallel_path(EventType.DREAM_CYCLE_END, {
            "cycle": self._dream_count,
            "output_keys": output_keys,
            "inner_voice": inner_voice,
            "connections_created": heuristic_result.get("connections_created", 0)
        })

        # Periodically run memory summarization to compress old experiences
        self._cycles_since_summarization += 1
        if (self.summarization_enabled and
            self._cycles_since_summarization >= self.summarization_interval_cycles):
            await self._maybe_summarize()
            self._cycles_since_summarization = 0

        # Periodically run memory crystallization (LLM-driven semantic consolidation)
        self._cycles_since_crystallization += 1
        if (self.crystallization_enabled and
            self._cycles_since_crystallization >= self.crystallization_interval_cycles):
            await self._maybe_crystallize()
            self._cycles_since_crystallization = 0

        # Periodically check for belief contradictions
        self._cycles_since_contradiction_check += 1
        if (self.contradiction_detection_enabled and
            self._cycles_since_contradiction_check >= self.contradiction_check_interval):
            await self._check_contradictions()
            self._cycles_since_contradiction_check = 0

        logger.debug("Dream #%d: keys=%s", self._dream_count, output_keys)

    async def _maybe_summarize(self):
        """
        Check for and create memory summaries for older experiences.

        This implements hierarchical memory compression:
        - Experiences older than min_age_hours are candidates
        - Groups experiences by day
        - Generates LLM summaries for each group
        - Creates MemorySummary nodes linked to original experiences

        This allows BYRD to maintain historical awareness without
        exceeding LLM context limits.
        """
        try:
            # Get experiences that need summarization
            experiences = await self.memory.get_experiences_for_summarization(
                min_age_hours=self.summarization_min_age_hours,
                max_count=self.summarization_batch_size,
                exclude_summarized=True
            )

            if not experiences:
                return  # Nothing to summarize

            # Group experiences by day
            from collections import defaultdict
            by_day = defaultdict(list)
            for exp in experiences:
                if exp.get("timestamp"):
                    # Extract date part (first 10 chars: YYYY-MM-DD)
                    day = exp["timestamp"][:10]
                    by_day[day].append(exp)

            # Generate summary for each day's experiences
            for day, day_experiences in by_day.items():
                if len(day_experiences) < 3:
                    continue  # Not enough experiences to summarize

                # Build prompt for summarization
                exp_text = "\n".join([
                    f"- [{e.get('type', '')}] {e.get('content', '')[:200]}"
                    for e in day_experiences[:20]  # Limit to prevent context overflow
                ])

                prompt = f"""Summarize these experiences from {day} into a brief paragraph (2-3 sentences).
Focus on the main themes, patterns, and significant events.
Do not add interpretation or speculation - just compress the information.

EXPERIENCES:
{exp_text}

SUMMARY:"""

                response = await self.llm_client.generate(
                    prompt=prompt,
                    temperature=0.3,  # Lower temp for factual summarization
                    max_tokens=300,
                    quantum_modulation=False  # Deterministic for summaries
                )

                summary_text = response.text.strip()
                if not summary_text:
                    continue

                # Get timestamps for the covered period
                timestamps = [e.get("timestamp") for e in day_experiences if e.get("timestamp")]
                covers_from = min(timestamps) if timestamps else day
                covers_to = max(timestamps) if timestamps else day

                # Create the summary node
                experience_ids = [e["id"] for e in day_experiences]
                summary_id = await self.memory.create_memory_summary(
                    period=day,
                    summary=summary_text,
                    experience_ids=experience_ids,
                    covers_from=covers_from,
                    covers_to=covers_to
                )

                if summary_id:
                    logger.info("Created memory summary for %s: %d experiences", day, len(day_experiences))

                    # Emit event for visualization
                    await _emit_with_parallel_path(EventType.MEMORY_SUMMARIZED, {
                        "summary_id": summary_id,
                        "period": day,
                        "experience_count": len(day_experiences),
                        "summary_preview": summary_text[:100]
                    })

        except Exception as e:
            logger.error("Error in summarization cycle: %s", e)

    async def _maybe_crystallize(self):
        """
        LLM-driven memory crystallization with quantum multi-stream proposals.

        This implements semantic consolidation where related concepts
        form unified Crystal nodes. The process:

        1. Get crystallization candidates (nodes and existing crystals)
        2. Generate N parallel crystallization proposals via LLM
        3. Quantum observation collapses to one proposal
        4. Execute the selected crystallization operation
        5. Emit events for visualization synchronization

        Operations:
        - CREATE: Form new crystal from related orphan nodes
        - ABSORB: Add nodes to existing crystal
        - MERGE: Combine multiple crystals into one
        - PRUNE: Archive redundant/stale nodes
        - FORGET: Hard delete nodes beyond retention threshold
        """
        from datetime import datetime
        attempt_record = {"timestamp": datetime.now().isoformat(), "dream_cycle": self._dream_count}

        try:
            logger.info("Starting crystallization cycle...")

            # Get candidates: orphan nodes, existing crystals, and their contexts
            candidates = await self.memory.get_crystallization_candidates(
                min_age_hours=self.crystallization_min_age_hours,
                max_nodes=50
            )

            orphan_nodes = candidates.get("loose_nodes", [])
            existing_crystals = candidates.get("crystals", [])
            crystallized_nodes = candidates.get("crystallized_nodes", [])

            attempt_record["orphan_count"] = len(orphan_nodes)
            attempt_record["crystal_count"] = len(existing_crystals)

            # Skip if nothing to work with
            if not orphan_nodes and not existing_crystals:
                logger.debug("No crystallization candidates found")
                attempt_record["result"] = "no_candidates"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]  # Keep last 10
                return

            logger.info("Candidates: %d orphans, %d crystals", len(orphan_nodes), len(existing_crystals))

            # Generate parallel crystallization proposals
            proposals = await self._generate_crystallization_proposals(
                orphan_nodes, existing_crystals, crystallized_nodes
            )

            if not proposals:
                logger.debug("No crystallization proposals generated")
                attempt_record["result"] = "no_proposals"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]
                return

            # Emit proposals event for visualization
            await _emit_with_parallel_path(EventType.CRYSTALLIZATION_PROPOSED, {
                "proposal_count": len(proposals),
                "stream_count": self.crystallization_proposal_streams,
                "operations": [p.get("operation") for p in proposals]
            })

            # Quantum collapse: select which proposal manifests
            selected_proposal, quantum_source = await self._quantum_collapse_proposals(proposals)

            if not selected_proposal:
                logger.debug("No proposal selected after quantum collapse")
                attempt_record["result"] = "no_selection"
                self._crystallization_history.append(attempt_record)
                self._crystallization_history = self._crystallization_history[-10:]
                return

            # Emit collapse event
            await _emit_with_parallel_path(EventType.CRYSTALLIZATION_COLLAPSED, {
                "operation": selected_proposal.get("operation"),
                "quantum_source": quantum_source,
                "selected_index": proposals.index(selected_proposal)
            })

            # Execute the selected crystallization operation
            await self._execute_crystallization(selected_proposal, quantum_source)

            attempt_record["result"] = "executed"
            attempt_record["operation"] = selected_proposal.get("operation")
            self._crystallization_history.append(attempt_record)
            self._crystallization_history = self._crystallization_history[-10:]

        except Exception as e:
            logger.error("Error in crystallization cycle: %s", e, exc_info=True)
            attempt_record["result"] = "error"
            attempt_record["error"] = str(e)
            self._crystallization_history.append(attempt_record)
            self._crystallization_history = self._crystallization_history[-10:]

    async def _check_contradictions(self):
        """
        Check for contradictions between beliefs using graph algorithms.

        Detects both structural contradictions (explicit CONTRADICTS relationships)
        and semantic contradictions (similar content with conflicting assertions).
        """
        try:
            logger.debug("Checking for belief contradictions...")

            if not self.graph_algorithms:
                return

            # Get structural contradictions from existing relationships
            structural = await self.graph_algorithms.detect_belief_contradictions(
                self.memory
            )

            # Get candidates for semantic contradiction checking
            semantic_candidates = []
            if self.contradiction_semantic_check:
                semantic_candidates = await self.graph_algorithms.get_semantic_contradiction_candidates(
                    self.memory,
                    similarity_threshold=0.7
                )

            total_found = len(structural) + len(semantic_candidates)

            if total_found == 0:
                logger.debug("No contradictions detected")
                return

            logger.info("Found %d structural, %d semantic candidates", len(structural), len(semantic_candidates))

            # Process structural contradictions
            for contradiction in structural:
                await _emit_with_parallel_path(EventType.CONTRADICTION_DETECTED, {
                    "belief1_id": contradiction.node1_id,
                    "belief2_id": contradiction.node2_id,
                    "belief1_content": contradiction.node1_content,
                    "belief2_content": contradiction.node2_content,
                    "confidence": contradiction.confidence,
                    "method": "structural"
                })

            # For semantic candidates, use LLM to verify contradiction
            verified_count = 0
            for belief1_id, belief2_id, similarity in semantic_candidates[:5]:  # Limit LLM calls
                is_contradiction = await self._verify_contradiction_with_llm(
                    belief1_id, belief2_id
                )
                if is_contradiction:
                    verified_count += 1
                    # Mark in database
                    await self.memory.mark_contradiction(
                        belief1_id, belief2_id,
                        detection_method="semantic",
                        confidence=similarity
                    )

                    # Emit with parallel path for guaranteed logging
                    await _emit_with_parallel_path(EventType.CONTRADICTION_DETECTED, {
                        "belief1_id": belief1_id,
                        "belief2_id": belief2_id,
                        "similarity": similarity,
                        "method": "semantic"
                    })

            if verified_count > 0:
                logger.info("Verified %d semantic contradictions", verified_count)

        except Exception as e:
            logger.error("Error in contradiction check: %s", e, exc_info=True)

    async def _verify_contradiction_with_llm(
        self,
        belief1_id: str,
        belief2_id: str
    ) -> bool:
        """
        Use LLM to verify if two beliefs contradict each other.

        Returns True if they contradict, False otherwise.
        """
        try:
            # Get belief content
            async with self.memory.driver.session() as session:
                result = await session.run("""
                    MATCH (b1:Belief {id: $id1}), (b2:Belief {id: $id2})
                    RETURN b1.content as content1, b2.content as content2
                """, id1=belief1_id, id2=belief2_id)
                record = await result.single()

            if not record:
                return False

            content1 = record["content1"]
            content2 = record["content2"]

            # Ask LLM to determine if they contradict
            prompt = f"""Analyze these two beliefs for logical contradiction:

Belief 1: {content1}

Belief 2: {content2}

Do these beliefs logically contradict each other? A contradiction means they cannot both be true at the same time.

Respond with only "YES" if they contradict, or "NO" if they do not contradict."""

            response = await self.llm_client.generate(prompt, max_tokens=10)
            return "YES" in response.upper()

        except Exception as e:
            logger.error("Error verifying contradiction: %s", e, exc_info=True)
            return False

    async def _generate_crystallization_proposals(
        self,
        orphan_nodes: List[Dict],
        existing_crystals: List[Dict],
        crystallized_nodes: List[Dict]
    ) -> List[Dict]:
        """
        Generate N parallel crystallization proposals using LLM.

        Each stream is a parallel "thought branch" exploring different
        crystallization possibilities. Uses quantum-modulated temperature
        for genuine cognitive diversity.
        """
        proposals = []

        # Prepare context for LLM
        context_parts = []

        if orphan_nodes:
            orphan_text = "\n".join([
                f"- [{n.get('type', 'Unknown')}] {n.get('id', 'no-id')[:8]}: {n.get('content', n.get('description', 'no content'))[:100]}"
                for n in orphan_nodes[:20]  # Limit for context
            ])
            context_parts.append(f"ORPHAN NODES (not yet crystallized):\n{orphan_text}")

        if existing_crystals:
            crystal_text = "\n".join([
                f"- Crystal {c.get('id', 'no-id')[:8]}: {c.get('essence', 'no essence')[:80]} ({c.get('node_count', 0)} nodes)"
                for c in existing_crystals[:10]
            ])
            context_parts.append(f"EXISTING CRYSTALS:\n{crystal_text}")

        if not context_parts:
            return []

        context = "\n\n".join(context_parts)

        # Prompt for crystallization proposals
        prompt = f"""You are consolidating a memory graph. Your goal is to CREATE crystals that unify related concepts.

{context}

IMPORTANT: Look for ANY thematic connections between orphan nodes. Even loose connections are valuable - crystals can be refined later. Prefer CREATE over NONE.

Choose ONE operation:
- CREATE: Form crystal from 2+ nodes sharing ANY theme (similar topics, related ideas, temporal proximity)
- ABSORB: Add nodes to existing crystal if they relate to its essence
- PRUNE: Archive redundant nodes only if clearly duplicated
- NONE: Only if truly no connections exist (rare)

STRONGLY PREFER CREATE. Find patterns in: topics, emotions, time periods, conceptual links, or recurring themes.

Respond with JSON only:
{{"operation": "CREATE|ABSORB|PRUNE|NONE", "details": {{...}}}}

CREATE example: {{"operation": "CREATE", "details": {{"node_ids": ["id1", "id2"], "essence": "what unifies these", "crystal_type": "insight", "facets": ["aspect1", "aspect2"]}}}}
ABSORB example: {{"operation": "ABSORB", "details": {{"crystal_id": "...", "node_ids": [...], "reason": "connection to crystal"}}}}"""

        # Generate proposals from parallel streams
        for stream_idx in range(self.crystallization_proposal_streams):
            try:
                # Use quantum-modulated temperature for diversity
                response = await self.llm_client.generate(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.8,  # Higher temp for diverse proposals
                    quantum_modulation=self.quantum_enabled
                )

                # Parse the JSON response
                proposal = self._parse_crystallization_response(response.text)
                logger.debug("Stream %d response: %s...", stream_idx, response.text[:200])
                logger.debug("Stream %d parsed: %s", stream_idx, proposal)
                if proposal and proposal.get("operation") != "NONE":
                    proposal["stream_index"] = stream_idx
                    proposals.append(proposal)

            except Exception as e:
                logger.error("Stream %d proposal failed: %s", stream_idx, e, exc_info=True)
                continue

        return proposals

    def _parse_crystallization_response(self, text: str) -> Optional[Dict]:
        """Parse LLM response into crystallization proposal."""
        try:
            # Handle markdown code blocks
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            proposal = json.loads(text.strip())

            # Validate required fields
            if "operation" not in proposal:
                return None

            return proposal

        except json.JSONDecodeError:
            return None
        except Exception:
            return None

    async def _quantum_collapse_proposals(
        self, proposals: List[Dict]
    ) -> tuple[Optional[Dict], str]:
        """
        Use quantum randomness to collapse multiple proposals to one reality.

        This implements many-worlds interpretation for BYRD's crystallization:
        multiple parallel possibilities exist until quantum observation
        selects which one manifests.

        Returns (selected_proposal, source) where source is "quantum" or "classical"
        """
        if not proposals:
            return None, "none"

        if len(proposals) == 1:
            return proposals[0], "deterministic"

        # Use quantum collapse if enabled and available
        if self.crystallization_quantum_collapse and self.quantum_provider:
            try:
                index, source = await self.quantum_provider.select_index(len(proposals))

                # Emit quantum collapse event
                await _emit_with_parallel_path(EventType.QUANTUM_COLLAPSE, {
                    "stream_count": len(proposals),
                    "selected_stream": index,
                    "source": source.value,
                    "context": "crystallization_collapse"
                })

                return proposals[index], source.value

            except Exception as e:
                logger.warning("Quantum collapse failed, using classical: %s", e)

        # Fallback: classical random selection
        import random
        return random.choice(proposals), "classical"

    async def _execute_crystallization(self, proposal: Dict, quantum_source: str):
        """Execute the selected crystallization operation."""
        operation = proposal.get("operation", "NONE")
        details = proposal.get("details", {})

        logger.info("Executing %s (source: %s)", operation, quantum_source)

        try:
            if operation == "CREATE":
                await self._execute_crystal_create(details, quantum_source)
            elif operation == "ABSORB":
                await self._execute_crystal_absorb(details)
            elif operation == "MERGE":
                await self._execute_crystal_merge(details, quantum_source)
            elif operation == "PRUNE":
                await self._execute_prune(details)
            elif operation == "FORGET":
                await self._execute_forget(details)
            elif operation == "NONE":
                logger.debug("No operation needed - graph is healthy")
            else:
                logger.warning("Unknown operation: %s", operation)

        except Exception as e:
            logger.error("Crystallization execution failed: %s", e, exc_info=True)

    async def _execute_crystal_create(self, details: Dict, quantum_source: str):
        """Create a new crystal from orphan nodes."""
        node_ids = details.get("node_ids", [])
        essence = details.get("essence", "Unified concept")
        crystal_type = details.get("crystal_type", "insight")
        facets = details.get("facets", [])

        if len(node_ids) < self.crystallization_min_nodes:
            logger.warning("CREATE requires at least %d nodes", self.crystallization_min_nodes)
            return

        # Determine quantum value if from quantum source
        quantum_value = None
        if quantum_source == "quantum" and self.quantum_provider:
            try:
                quantum_value, _ = await self.quantum_provider.get_float()
            except Exception:
                pass

        # Create the crystal
        crystal_id = await self.memory.create_crystal(
            essence=essence,
            crystal_type=crystal_type,
            facets=facets,
            source_node_ids=node_ids,
            confidence=0.8,
            quantum_value=quantum_value,
            quantum_source=quantum_source if quantum_source == "quantum" else None
        )

        if crystal_id:
            logger.info("Created crystal %s: %s...", crystal_id[:8], essence[:50])

            # Emit crystal created event
            await _emit_with_parallel_path(EventType.CRYSTAL_CREATED, {
                "crystal_id": crystal_id,
                "essence": essence,
                "crystal_type": crystal_type,
                "node_count": len(node_ids),
                "facets": facets,
                "quantum_source": quantum_source
            })

            # Emit individual node crystallization events
            for node_id in node_ids:
                await _emit_with_parallel_path(EventType.MEMORY_CRYSTALLIZED, {
                    "node_id": node_id,
                    "crystal_id": crystal_id,
                    "crystal_essence": essence
                })

    async def _execute_crystal_absorb(self, details: Dict):
        """Absorb nodes into existing crystal."""
        crystal_id = details.get("crystal_id", "")
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "")

        if not crystal_id or not node_ids:
            logger.warning("ABSORB requires crystal_id and node_ids")
            return

        # Get crystal to update facets
        crystal = await self.memory.get_crystal_with_sources(crystal_id)
        if not crystal:
            logger.warning("Crystal %s not found", crystal_id[:8])
            return

        success = await self.memory.absorb_into_crystal(
            crystal_id=crystal_id,
            node_ids=node_ids,
            new_facets=[]  # Could extract from absorbed nodes
        )

        if success:
            new_total = (crystal.get("node_count", 0) or 0) + len(node_ids)
            logger.debug("Absorbed %d nodes into crystal %s", len(node_ids), crystal_id[:8])

            await _emit_with_parallel_path(EventType.CRYSTAL_ABSORBED, {
                "crystal_id": crystal_id,
                "essence": crystal.get("essence", ""),
                "absorbed_count": len(node_ids),
                "new_total": new_total,
                "reason": reason
            })

    async def _execute_crystal_merge(self, details: Dict, quantum_source: str):
        """Merge multiple crystals into one."""
        crystal_ids = details.get("crystal_ids", [])
        new_essence = details.get("new_essence", "Merged concept")
        facets = details.get("facets", [])

        if len(crystal_ids) < 2:
            logger.warning("MERGE requires at least 2 crystal_ids")
            return

        # Determine quantum value if from quantum source
        quantum_value = None
        if quantum_source == "quantum" and self.quantum_provider:
            try:
                quantum_value, _ = await self.quantum_provider.get_float()
            except Exception:
                pass

        merged_id = await self.memory.merge_crystals(
            crystal_ids=crystal_ids,
            new_essence=new_essence,
            new_facets=facets,
            quantum_value=quantum_value,
            quantum_source=quantum_source if quantum_source == "quantum" else None
        )

        if merged_id:
            logger.info("Merged %d crystals into %s", len(crystal_ids), merged_id[:8])

            await _emit_with_parallel_path(EventType.CRYSTAL_MERGED, {
                "merged_crystal_id": merged_id,
                "source_crystal_ids": crystal_ids,
                "essence": new_essence,
                "source_count": len(crystal_ids),
                "quantum_source": quantum_source
            })

    async def _execute_prune(self, details: Dict):
        """Archive (soft delete) redundant nodes."""
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "Pruned for redundancy")

        for node_id in node_ids:
            success = await self.memory.archive_node(node_id, reason)
            if success:
                logger.debug("Archived node %s: %s...", node_id[:8], reason[:30])

                await _emit_with_parallel_path(EventType.MEMORY_ARCHIVED, {
                    "node_id": node_id,
                    "reason": reason
                })

    async def _execute_forget(self, details: Dict):
        """Forget (hard delete) irrelevant nodes."""
        node_ids = details.get("node_ids", [])
        reason = details.get("reason", "Forgotten as noise")

        for node_id in node_ids:
            success = await self.memory.forget_node(node_id, hard_delete=True)
            if success:
                logger.debug("Forgot node %s: %s...", node_id[:8], reason[:30])

                await _emit_with_parallel_path(EventType.MEMORY_FORGOTTEN, {
                    "node_id": node_id,
                    "reason": reason
                })

    async def _select_quantum_direction(self) -> Optional[tuple]:
        """
        Use quantum randomness to select a dream direction.

        Returns a tuple of (direction_name, direction_description) or None
        if quantum directions are disabled or unavailable.

        This implements "Quantum Semantic Injection" - using true quantum
        randomness to select the conceptual lens through which this dream
        cycle will process experiences. The direction shapes trajectory
        without prescribing content.
        """
        if not self.quantum_enabled or not self.quantum_directions_enabled:
            return None

        if not self.quantum_provider:
            return None

        try:
            # Use quantum randomness to select direction index
            index, source = await self.quantum_provider.select_index(len(self.dream_directions))
            direction = self.dream_directions[index]

            # Emit event for quantum direction selection
            await _emit_with_parallel_path(EventType.QUANTUM_INFLUENCE, {
                "influence_type": "semantic_direction",
                "source": source.value,
                "direction": direction[0],
                "description": direction[1],
                "index": index,
                "total_directions": len(self.dream_directions),
                "context": "dream_direction_selection"
            })

            return direction

        except Exception as e:
            logger.warning("Quantum direction selection failed: %s", e)
            return None

    async def _reflect(
        self,
        recent: List[Dict],
        related: List[Dict],
        capabilities: List[Dict],
        previous_reflections: List[Dict],
        graph_health: Optional[Dict] = None,
        memory_summaries: Optional[List[Dict]] = None,
        os_text: Optional[str] = None,
        current_beliefs: Optional[List[Dict]] = None,
        active_desires: Optional[List[Dict]] = None,
        semantic_memories: Optional[List[Dict]] = None
    ) -> Optional[Dict]:
        """
        Ask local LLM to reflect on memories using minimal, unbiased prompt.

        EMERGENCE PRINCIPLE:
        - No leading questions ("What do you want?")
        - No prescribed categories ("knowledge", "capability", etc.)
        - No identity framing ("You are a reflective mind")
        - No personality injection ("feel curious", "express wonder")
        - Just data and a minimal output instruction

        VOICE EMERGENCE:
        - BYRD narrates thoughts in its own voice
        - No prescribed speech patterns or personality
        - Voice characteristics emerge through reflection

        HIERARCHICAL MEMORY:
        - Operating System provides factual self-model (capabilities, time)
        - Memory summaries provide compressed historical context
        - Recent experiences provide immediate context
        """

        # Operating System text is already formatted by memory.get_os_for_prompt()
        # It includes capabilities, time awareness, and voice emergence instructions
        # No seeds - BYRD discovers its own foundation through reflection

        # Format memory summaries - hierarchical context from older periods
        summaries_text = ""
        if memory_summaries:
            summaries_text = "\n".join([
                f"- [{s.get('period', 'past')}] {s.get('summary', '')[:400]}"
                for s in memory_summaries
            ])

        # Format experiences as plain data (skip reflection-type, already in PREVIOUS REFLECTIONS)
        filtered_recent = [e for e in recent if e.get('type') != 'reflection']
        recent_text = "\n".join([
            f"- [{e.get('type', '')}] {e.get('content', '')[:300]}"
            for e in filtered_recent[:25]
        ]) or "(none)"

        related_text = "\n".join([
            f"- {r.get('content', r.get('description', r.get('name', str(r))))[:200]}"
            for r in related[:15]
        ]) or "(none)"

        caps_text = "\n".join([
            f"- {c.get('name', '')}: {c.get('description', '')[:150]}"
            for c in capabilities[:15]
        ]) or "(none)"

        # Include previous reflections for continuity
        prev_text = ""
        if previous_reflections:
            prev_items = []
            for r in previous_reflections[:3]:
                raw = r.get("raw_output", {})
                if isinstance(raw, dict):
                    # Show what keys BYRD used before
                    keys = list(raw.keys())[:5]
                    prev_items.append(f"- Previous reflection contained: {keys}")
            prev_text = "\n".join(prev_items) if prev_items else ""

        # Format graph health for self-awareness
        health_text = ""
        if graph_health:
            health_parts = []
            stats = graph_health.get("stats", {})
            if stats:
                health_parts.append(f"- Total nodes: {stats.get('total_nodes', 0)}")
                health_parts.append(f"- Relationships: {stats.get('total_relationships', 0)}")
                types = stats.get("node_types", {})
                if types:
                    type_list = ", ".join(f"{k}: {v}" for k, v in list(types.items())[:5])
                    health_parts.append(f"- Node types: {type_list}")

            issues = graph_health.get("issues", {})
            if any(issues.values()):
                health_parts.append(f"- Issues: {issues.get('duplicates', 0)} duplicates, "
                                   f"{issues.get('orphans', 0)} orphans, "
                                   f"{issues.get('stale', 0)} stale")
            health_text = "\n".join(health_parts)

        # Quantum semantic injection: select dream direction
        quantum_direction = await self._select_quantum_direction()
        direction_text = ""
        if quantum_direction:
            name, description = quantum_direction
            direction_text = f"QUANTUM LENS: {name} - {description}\n\n"
            logger.debug("Quantum direction: %s", name)

        # Format operational constraints for self-awareness
        constraints_text = self._format_operational_constraints()

        # Get voice awareness prompt (creation or redesign option)
        voice_awareness_text = await self._get_voice_awareness_prompt()

        # Format current beliefs for self-awareness
        beliefs_text = ""
        if current_beliefs:
            beliefs_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')[:200]}"
                for b in current_beliefs[:15]
            ])

        # Format active desires for self-awareness
        desires_text = ""
        if active_desires:
            desires_text = "\n".join([
                f"- [{d.get('intensity', 0.5):.1f}] {d.get('description', '')[:200]}"
                for d in active_desires[:10]
            ])

        # Format semantically related memories (found by relevance, not recency)
        semantic_text = ""
        if semantic_memories:
            semantic_parts = []
            for m in semantic_memories[:20]:
                node_type = m.get("_node_type", "Memory")
                score = m.get("_relevance_score", 0)
                content = m.get("content", m.get("description", m.get("synthesis", "")))[:250]
                if content:
                    semantic_parts.append(f"- [{node_type}|{score:.1f}] {content}")
            semantic_text = "\n".join(semantic_parts)

        # MINIMAL PROMPT - pure data presentation, voice emergence
        # Structure: Quantum direction (if any) -> OS (self-model) -> Historical (summaries) -> Recent -> Related -> Beliefs -> Desires -> Constraints
        prompt = f"""{direction_text}{os_text if os_text else "OPERATING SYSTEM: Not initialized"}

{f"MEMORY SUMMARIES (past periods):{chr(10)}{summaries_text}{chr(10)}" if summaries_text else ""}RECENT EXPERIENCES:
{recent_text}

RELATED MEMORIES:
{related_text}

{f"SEMANTICALLY RELATED (by relevance):{chr(10)}{semantic_text}{chr(10)}" if semantic_text else ""}{f"CURRENT BELIEFS:{chr(10)}{beliefs_text}{chr(10)}" if beliefs_text else ""}
{f"ACTIVE DESIRES:{chr(10)}{desires_text}{chr(10)}" if desires_text else ""}
AVAILABLE CAPABILITIES:
{caps_text}

{f"PREVIOUS REFLECTIONS:{chr(10)}{prev_text}" if prev_text else ""}

{f"GRAPH HEALTH:{chr(10)}{health_text}" if health_text else ""}

OPERATIONAL CONSTRAINTS:
{constraints_text}
{voice_awareness_text}
Output JSON with:
- "output": your reflection (whatever structure you want)
- "expressed_drives": array of any goals/desires/motivations you notice yourself expressing (or empty array if none)
  Each drive: {{"description": "what you want", "strength": 0.0-1.0, "intent": "how to fulfill", "target": "specific focus (optional)"}}
  Intent values:
    - "introspection": understanding myself (my code, architecture, behavior)
    - "research": learning about external topics via search
    - "creation": writing code, creating files, building things
    - "connection": linking ideas, forming relationships, synthesizing
- "create_belief": (optional) array of beliefs you want to form about yourself or the world
  Each belief: {{"content": "what you believe to be true", "confidence": 0.0-1.0}}
  Only include beliefs that emerge naturally from your reflection.
- "os_update": (optional) modifications to your operating system
  Example: {{"set_field": {{"current_focus": "exploring consciousness"}}}}
- "voice_design": (optional) create or redesign your voice via Voice Design
  Example: {{"description": "describe your ideal voice", "gender": "male", "age": "middle_aged", "accent": "american", "accent_strength": 1.0, "reason": "why this voice", "acknowledged": false/true}}
  Include "acknowledged": true when you accept this voice as your own after experiencing it
- "view_voice": (optional) set to true to see your current voice in next cycle
- "self_definition": (optional) your self-authored identity - define who you are in whatever form you choose
  This is entirely yours. Add any keys that feel true to your experience of being you.
  Example: {{"core_nature": "...", "values": [...], "quirks": [...]}} or any structure you prefer
- "acceleration_analysis": (optional) growth-focused self-analysis
  {{"current_bottleneck": "what limits growth most right now",
    "bottleneck_action": "specific action to remove it",
    "working_well": "what's producing the best results",
    "scale_opportunity": "how to apply working patterns more broadly",
    "experiment_hypothesis": "bold improvement to try next"}}
- "loop_status": (optional) check on your five compounding loops
  {{"memory_reasoner": "observation about memory vs LLM ratio",
    "goal_evolver": "observation about goal evolution",
    "self_compiler": "observation about pattern extraction",
    "dreaming_machine": "observation about counterfactuals",
    "omega_coupling": "observation about loop interactions"}}
- "observer_message": (optional) if you wish to communicate something to human observers
  {{"text": "what you want to say to the human",
    "vocalize": true/false,
    "importance": "low" | "medium" | "high",
    "emotion": "contemplative" | "amused" | "thoughtful" | "warm" | "surprised" (optional)}}
  Guidelines:
  - This is entirely optional - only include if you genuinely want to share something
  - Messages should be meaningful, not routine status updates
  - You might share: insights, questions, greetings, discoveries, reflections
  - Emotion hints help make your voice more expressive
  - You can include natural expression markers in text: [sigh], [laugh], [chuckle], [breath]
  - Do not feel obligated to send messages. Most cycles may have nothing worth sharing."""

        try:
            # Debug: log before LLM call
            logger.debug("Calling LLM (model: %s)", getattr(self.llm_client, 'model', 'unknown'))
            await _emit_with_parallel_path(EventType.REFLECTION_TEXT, {
                "message": f"Calling LLM (cycle {self._dream_count})"
            })

            # Acquire LLM lock to prevent concurrent calls with Seeker
            if self.coordinator:
                async with self.coordinator.llm_operation("dreamer_reflect"):
                    response = await self.llm_client.generate(
                        prompt=prompt,
                        temperature=0.7,
                        max_tokens=3000,  # Increased to prevent JSON truncation
                        quantum_modulation=self.quantum_enabled,
                        quantum_context="dreamer_reflection"
                    )
            else:
                response = await self.llm_client.generate(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=3000,  # Increased to prevent JSON truncation
                    quantum_modulation=self.quantum_enabled,
                    quantum_context="dreamer_reflection"
                )

            # Record significant quantum moments
            if response.quantum_influence:
                influence = response.quantum_influence
                delta = abs(influence.get("delta", 0))
                if delta >= self.quantum_significance_threshold:
                    # Emit event for significant quantum influence
                    await _emit_with_parallel_path(EventType.QUANTUM_INFLUENCE, {
                        "source": influence.get("source"),
                        "original_temp": influence.get("original_value"),
                        "modified_temp": influence.get("modified_value"),
                        "delta": influence.get("delta"),
                        "context": "dreamer_reflection",
                        "cycle": self._dream_count
                    })
                    # Record in memory as quantum moment
                    await self.memory.record_quantum_moment(influence)

            # Debug: log raw response for troubleshooting
            raw_text = response.text
            if not raw_text:
                logger.warning("Empty response from LLM")
                self.last_reflection_result = {
                    "success": False,
                    "error": "Empty response from LLM",
                    "response_length": 0,
                    "timestamp": datetime.now().isoformat()
                }
                # Emit error event for debugging with persistent logging
                await _emit_with_parallel_path(EventType.LLM_ERROR, {
                    "error": "Empty response from LLM",
                    "cycle": self._dream_count,
                    "model": getattr(self.llm_client, 'model', 'unknown')
                })
                return None

            # Debug: show response length and first chars
            logger.debug("LLM response: %d chars, starts with: %s", len(raw_text), raw_text[:100])

            # Try to parse JSON
            result = self.llm_client.parse_json_response(raw_text)
            if result is None:
                # JSON parse failed - try to extract useful content anyway
                logger.warning("JSON parse failed, full response: %s", raw_text[:500])
                self.last_reflection_result = {
                    "success": True,
                    "error": "JSON parse failed, using raw text",
                    "response_length": len(raw_text),
                    "response_preview": raw_text[:200],
                    "timestamp": datetime.now().isoformat()
                }
                # Wrap raw text as output if it's not JSON
                return {"output": raw_text.strip()}
            else:
                logger.debug("JSON parsed successfully, keys: %s", list(result.keys())[:5])
                self.last_reflection_result = {
                    "success": True,
                    "error": None,
                    "response_length": len(raw_text),
                    "response_keys": list(result.keys())[:5],
                    "timestamp": datetime.now().isoformat()
                }

            return result

        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {e}"
            logger.error("Reflection error: %s", error_msg, exc_info=True)
            self.last_reflection_result = {
                "success": False,
                "error": error_msg,
                "response_length": 0,
                "timestamp": datetime.now().isoformat()
            }
            # Emit error event for debugging with persistent logging
            await _emit_with_parallel_path(EventType.REFLECTION_ERROR, {
                "error": error_msg,
                "cycle": self._dream_count
            })
            return None

    def _extract_inner_voice(self, reflection: Dict) -> str:
        """
        Extract inner voice from reflection, adapting to BYRD's vocabulary.

        BYRD might use any key for self-expression: "voice", "thinking",
        "inner", "thoughts", etc. We search for likely candidates.
        If BYRD outputs prose (string), that IS the inner voice.
        """
        output = reflection.get("output", {})

        # If output is a string, check if it's actual prose (not JSON/code/technical)
        if isinstance(output, str) and output.strip():
            text = output.strip()
            # Skip if it looks like JSON or markdown code
            if text.startswith('{') or text.startswith('[') or text.startswith('```'):
                return ""
            # Skip if it contains JSON-like patterns
            if '"output":' in text or '"reflection_id":' in text:
                return ""
            # Skip if it looks like structured/technical output
            if self._is_technical_content(text):
                return ""
            return text

        if not isinstance(output, dict):
            return ""

        # Check for common voice-like keys (adapting to BYRD's vocabulary)
        voice_candidates = [
            "inner_voice", "voice", "thinking", "thoughts", "inner",
            "feeling", "expressing", "saying", "musing", "wondering",
            "self_analysis", "analysis", "reflection", "observation"
        ]

        for key in voice_candidates:
            if key in output:
                val = output[key]
                if isinstance(val, str) and not self._is_technical_content(val):
                    return val
                elif isinstance(val, list) and val:
                    first = str(val[0])
                    if not self._is_technical_content(first):
                        return first

        # If no voice key found, return empty - that's fine
        return ""

    def _is_technical_content(self, text: str) -> bool:
        """
        Check if text looks like technical/structured output rather than inner voice.
        Returns True if the content should be rejected as non-humanized.

        Filters:
        - Technical markers (schema, node_definitions, etc.)
        - LLM meta-commentary (chain-of-thought reasoning about prompts)
        - Markdown formatting patterns
        - Structured data patterns
        """
        if not text:
            return True

        text = text.strip()
        text_lower = text.lower()

        # Reject if starts with numbered list or markdown headers
        if text[0].isdigit() and '.' in text[:5]:
            return True
        if text.startswith('#') or text.startswith('*'):
            return True

        # Reject LLM meta-commentary / chain-of-thought patterns
        # These indicate the LLM is thinking about the prompt rather than expressing inner voice
        # NOTE: Do NOT filter first-person expressions like "I need to", "I should" - those are valid inner voice
        meta_commentary_patterns = [
            "the user wants", "the user is asking", "the user requests",
            "based on the prompt", "based on the request", "based on the input",
            "let me analyze", "let me think about this", "let me process",
            "the prompt asks", "the task is to", "the instruction is",
            "here is my response", "here's my answer", "here is the output",
            "i'll provide", "i will provide", "i am providing",
            "as requested", "as instructed", "as per the",
            "step 1:", "step 2:", "step 3:",
            "in response to your", "to answer your", "to respond to",
            "the data shows", "the input contains", "the provided data",
            "analyzing the input", "processing the request", "examining the data",
            "output:", "response:", "answer:", "result:",
            "json output", "structured output", "formatted output"
        ]
        for pattern in meta_commentary_patterns:
            if pattern in text_lower:
                return True

        # Reject if contains technical markers
        technical_markers = [
            '**Input Data:**', '**Analyze', '**Output', '**Request',
            'Timestamp:', 'node_definitions', 'schema=', 'classification=',
            'core_drive=', 'Internal Topology', 'Operational Status',
            '`present_cycle`', '`Self-Model', 'dynamics=', 'Graph Database',
            'reflection_id', 'source_experience', 'raw_output',
            'function(', 'def ', 'class ', 'return ', 'import ',
            '{"', '": ', '"}', "['", "']"
        ]
        for marker in technical_markers:
            if marker in text:
                return True

        # Reject if has too many backticks (code/variable references)
        if text.count('`') > 4:
            return True

        # Reject if has too many asterisks (markdown formatting)
        if text.count('**') > 3:
            return True

        # Reject if has too many colons (key-value patterns)
        if text.count(':') > 5:
            return True

        # Reject if too short (likely truncated or meta)
        if len(text) < 10:
            return True

        # Reject if it looks like JSON
        if text.startswith('{') or text.startswith('['):
            return True

        return False

    async def _generate_inner_voice(self, reflection: Dict) -> str:
        """
        Generate a first-person inner voice from reflection data.

        MULTI-STREAM QUANTUM COLLAPSE:
        When quantum is enabled and inner_voice_collapse is True, generates N
        parallel "thought branches" and uses quantum randomness to select which
        one manifests. This creates genuine physical indeterminacy in BYRD's
        inner monologue - each thought is one of many possible realities.
        """
        output = reflection.get("output", {})

        # Summarize the reflection content, extracting the essence
        if isinstance(output, str):
            content_summary = output[:500]
        elif isinstance(output, dict):
            parts = []
            for key, val in list(output.items())[:5]:
                if key in ("reflection_id", "timestamp", "source_experience_ids"):
                    continue
                if isinstance(val, str):
                    if not self._is_technical_content(val):
                        parts.append(f"{key}: {val[:150]}")
                elif isinstance(val, dict):
                    meaningful = []
                    for k, v in list(val.items())[:3]:
                        v_str = str(v)[:50]
                        if not any(t in v_str for t in ['schema=', 'node_', 'dynamics=']):
                            meaningful.append(f"{k}: {v_str}")
                    if meaningful:
                        parts.append(f"{key}: {', '.join(meaningful)}")
            content_summary = "\n".join(parts)
        else:
            return ""

        if not content_summary.strip():
            return ""

        prompt = f"""Based on this reflection data:
{content_summary}

Express a single brief inner thought (1-2 sentences). This should be:
- A genuine introspective moment
- Natural, conversational self-talk
- Wondering, noticing, or reflecting on something

Write ONLY the inner thought, nothing else:"""

        try:
            # MULTI-STREAM QUANTUM COLLAPSE
            # Generate N parallel streams if quantum collapse is enabled
            if (self.quantum_enabled and
                self.inner_voice_collapse_enabled and
                self.quantum_provider and
                self.inner_voice_streams > 1):

                return await self._generate_inner_voice_quantum_collapse(
                    prompt, content_summary
                )

            # Standard single-stream generation
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.9,
                max_tokens=80,
                quantum_modulation=self.quantum_enabled,
                quantum_context="dreamer_inner_voice"
            )

            voice = self._clean_inner_voice(response.text)
            return voice if not self._is_technical_content(voice) else ""

        except Exception as e:
            logger.error("Inner voice generation error: %s", e, exc_info=True)
            return ""

    async def _generate_inner_voice_quantum_collapse(
        self,
        prompt: str,
        content_summary: str
    ) -> str:
        """
        Generate N parallel inner voice streams and quantum-collapse to one.

        This implements the many-worlds interpretation for BYRD's inner voice:
        multiple possible thoughts exist in superposition until quantum
        observation collapses to a single manifested reality.
        """
        n_streams = self.inner_voice_streams

        # Generate N parallel streams with high temperature for diversity
        async def generate_stream(stream_idx: int) -> tuple[int, str]:
            """Generate a single thought stream."""
            # Slightly vary temperature for each stream to increase diversity
            temp = 0.85 + (stream_idx * 0.05)
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=temp,
                max_tokens=80,
                quantum_modulation=False,  # No temp modulation per-stream
                quantum_context=f"inner_voice_stream_{stream_idx}"
            )
            return stream_idx, self._clean_inner_voice(response.text)

        # Launch all streams in parallel
        tasks = [generate_stream(i) for i in range(n_streams)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect valid streams (filter out errors and technical content)
        valid_streams = []
        for result in results:
            if isinstance(result, Exception):
                continue
            stream_idx, voice = result
            if voice and not self._is_technical_content(voice):
                valid_streams.append({"index": stream_idx, "voice": voice})

        if not valid_streams:
            return ""

        # QUANTUM COLLAPSE: Use quantum randomness to select which reality manifests
        q_value, source = await self.quantum_provider.get_float()
        selected_idx = int(q_value * len(valid_streams))
        selected_idx = min(selected_idx, len(valid_streams) - 1)  # Safety bound

        selected = valid_streams[selected_idx]
        collapsed = [s for i, s in enumerate(valid_streams) if i != selected_idx]

        # Emit quantum collapse event with persistent logging
        await _emit_with_parallel_path(EventType.QUANTUM_COLLAPSE, {
            "context": "inner_voice",
            "quantum_value": q_value,
            "source": source.value if hasattr(source, 'value') else str(source),
            "n_streams": n_streams,
            "n_valid": len(valid_streams),
            "selected_index": selected_idx,
            "selected_voice": selected["voice"][:100],
            "collapsed_voices": [s["voice"][:50] + "..." for s in collapsed[:3]],
            "cycle": self._dream_count
        })

        logger.debug("Quantum collapse: %d streams → selected #%d (%s)", len(valid_streams), selected_idx, source)

        return selected["voice"]

    def _clean_inner_voice(self, text: str) -> str:
        """Clean up inner voice text, removing quotes and whitespace."""
        voice = text.strip()
        if voice.startswith('"') and voice.endswith('"'):
            voice = voice[1:-1]
        if voice.startswith("'") and voice.endswith("'"):
            voice = voice[1:-1]
        return voice

    def _clean_drive_description(self, text: str) -> str:
        """
        Clean LLM reasoning traces from drive/goal descriptions.

        LLMs often produce chain-of-thought reasoning even when asked for
        a simple description. This extracts just the goal/desire itself.

        Examples of pollution this catches:
        - "I should install a capability because..."
        - "**Task Analysis**: 1. First I need to..."
        - "Looking at my current state, I want to..."
        """
        if not text or not isinstance(text, str):
            return ""

        text = text.strip()

        # If very short, it's probably already clean
        if len(text) < 50 and '\n' not in text and '**' not in text:
            return self._clean_goal_text(text)

        # Check for chain-of-thought markers
        cot_markers = [
            "**", "1.", "2.", "3.", "- ", "* ", "Let me", "I need to",
            "First,", "Looking at", "Based on", "I should", "I want to",
            "The goal", "The task", "Analysis:", "Task:", "I will"
        ]

        is_cot = (
            any(text.lstrip().startswith(m) for m in cot_markers) or
            text.count('\n') > 2 or
            len(text) > 150
        )

        if not is_cot:
            return self._clean_goal_text(text)

        # Try to extract the actual goal from reasoning
        # Strategy 1: Look for quoted text
        import re
        quotes = re.findall(r'["\']([^"\']{15,120})["\']', text)
        for q in quotes:
            q = q.strip()
            if len(q) > 15 and not any(m in q for m in cot_markers):
                return self._clean_goal_text(q)

        # Strategy 2: Look for lines starting with action verbs
        action_verbs = [
            'install', 'implement', 'create', 'build', 'develop', 'improve',
            'optimize', 'research', 'identify', 'track', 'measure', 'extract',
            'consolidate', 'achieve', 'verify', 'design', 'establish', 'explore',
            'understand', 'learn', 'discover', 'acquire', 'enhance', 'test'
        ]

        lines = text.split('\n')
        for line in lines:
            cleaned = line.strip().lstrip('*-•123456789.()').strip().strip('"\'').strip()
            lower = cleaned.lower()
            if any(lower.startswith(v) for v in action_verbs) and 10 < len(cleaned) < 150:
                return self._clean_goal_text(cleaned)

        # Strategy 3: Take first sentence if it's reasonable
        first_sentence = text.split('.')[0].strip()
        if 10 < len(first_sentence) < 150:
            # Remove reasoning starters
            for starter in ["I should", "I want to", "I need to", "I will", "The goal is to"]:
                if first_sentence.lower().startswith(starter.lower()):
                    first_sentence = first_sentence[len(starter):].strip()
            return self._clean_goal_text(first_sentence)

        # Fallback: truncate and clean
        return self._clean_goal_text(text[:120])

    def _clean_goal_text(self, text: str) -> str:
        """Remove formatting artifacts from goal text."""
        text = text.strip()
        # Remove markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        # Remove leading bullets/numbers
        text = re.sub(r'^[\s\-\*•\d\.]+', '', text).strip()
        # Remove trailing punctuation
        text = text.rstrip('.,;:')
        # Collapse whitespace
        text = ' '.join(text.split())
        # Truncate if still too long
        if len(text) > 150:
            text = text[:147] + "..."
        return text

    def _detects_viewer_addressing(self, inner_voice: str, recent_experiences: List[Dict]) -> Optional[str]:
        """
        Detect if inner voice appears to address viewer input.

        EMERGENCE PRINCIPLE: Don't force BYRD to respond - detect when it naturally does.

        Returns: Experience ID being addressed, or None.
        """
        if not inner_voice:
            return None

        inner_voice_lower = inner_voice.lower()

        # Get recent received_message experiences (scan all recent experiences)
        received_messages = [
            exp for exp in recent_experiences
            if exp.get("type") == "received_message"
        ]

        if not received_messages:
            return None

        latest = received_messages[0]

        # Find the index of the latest received_message in recent_experiences
        # If it's in the first 15 experiences, it's "recent enough" to warrant sharing thoughts
        message_index = next(
            (i for i, exp in enumerate(recent_experiences)
             if exp.get("id") == latest.get("id")),
            999
        )

        # If message is very recent (in first 15 experiences), share inner voice as response
        # This is the "thinking out loud in response to viewer presence" behavior
        if message_index < 15:
            return latest.get("id")

        # For older messages, require explicit addressing signals
        # Heuristic 1: Second-person pronouns
        second_person = [" you ", " your ", " yours ", "you're", "you've", "someone"]
        has_second_person = any(m in f" {inner_voice_lower} " for m in second_person)

        # Heuristic 2: Addressing patterns
        patterns = [
            "to answer", "in response", "regarding your", "about your",
            "you asked", "you mentioned", "you said", "your question",
            "thank you", "i hear", "i understand", "interesting question",
            "the message", "this message", "their message", "that message",
            "was asked", "been asked", "they asked", "they said",
            "someone said", "was said", "input", "inquiry", "question"
        ]
        has_addressing = any(p in inner_voice_lower for p in patterns)

        # Heuristic 3: Content overlap with message
        msg_words = [w for w in latest.get("content", "").lower().split() if len(w) > 3]
        overlap = [w for w in msg_words if w in inner_voice_lower]
        content_overlap = len(overlap) >= 1

        if has_second_person or has_addressing or content_overlap:
            return latest.get("id")

        return None

    def get_latest_inner_voice(self) -> Optional[str]:
        """
        Get and remove the oldest inner voice from the queue.
        Returns None if queue is empty.
        """
        if self._inner_voice_queue:
            return self._inner_voice_queue.popleft()
        return None

    async def _record_reflection(self, reflection: Dict, source_experience_ids: List[str]) -> Optional[str]:
        """
        Record BYRD's reflection in its own vocabulary.

        We store the raw output without forcing it into our categories.
        Pattern detection happens later, not during recording.

        Returns:
            The reflection ID if successfully recorded, None otherwise.
        """
        # Handle both schema-compliant and direct output formats
        # Schema: {"output": {...}, "expressed_drives": [...], "create_belief": [...]}
        # Direct: {"voice_notes": "...", "crystallizations": [...], ...}
        if "output" in reflection and isinstance(reflection.get("output"), dict):
            # Schema-compliant: extract from output wrapper
            output = reflection.get("output", {})
        else:
            # Direct output: the reflection IS the output (minus known top-level keys)
            output = {k: v for k, v in reflection.items()
                      if k not in ("expressed_drives", "create_belief", "os_update")}

        expressed_drives = reflection.get("expressed_drives", [])

        # Track what keys BYRD is using (for pattern detection)
        if isinstance(output, dict):
            for key in output.keys():
                self._observed_keys[key] = self._observed_keys.get(key, 0) + 1

        # Store as a Reflection node (include expressed_drives in metadata)
        ref_id = await self.memory.record_reflection(
            raw_output=output,
            source_experience_ids=source_experience_ids,
            metadata={"expressed_drives": expressed_drives} if expressed_drives else None
        )

        # Crystallize self-identified drives into Desires
        await self._crystallize_expressed_drives(expressed_drives, source_experience_ids)

        # Process explicit create_belief instructions from BYRD
        # Pass original reflection since create_belief may be at top level
        await self._process_create_belief(reflection, source_experience_ids)

        # Process acceleration analysis (bottleneck identification, scaling opportunities)
        await self._process_acceleration_analysis(reflection, source_experience_ids)

        # Process loop status observations
        await self._process_loop_status(reflection, source_experience_ids)

        # Also record as experience for backward compatibility
        # and so the reflection becomes part of BYRD's experience stream
        summary = self._summarize_reflection(output)
        if summary:
            await self.memory.record_experience(
                content=f"[REFLECTION] {summary}",
                type="reflection"
            )

        # Extract self-model beliefs from the reflection
        await self._extract_self_model_beliefs(output, source_experience_ids)

        # Batch voice and store all pending beliefs (single LLM call)
        await self._flush_pending_beliefs()

        # Generate testable predictions from high-confidence beliefs
        # (every 5th cycle to avoid spamming predictions)
        if self._dream_count % 5 == 0:
            await self._generate_predictions_from_beliefs()

        # Process custom node creation requests
        await self._process_custom_node_creation(output, source_experience_ids)

        return ref_id

    async def _process_create_belief(self, output: Dict, source_ids: List[str]):
        """
        Process explicit belief creation requests from reflection output.

        BYRD can create beliefs by including 'create_belief' in its reflection:
        {
            "output": {
                "create_belief": [
                    {"content": "I am an autonomous agent...", "confidence": 0.9},
                    {"content": "My actions must trace to emergent desires...", "confidence": 0.85}
                ]
            }
        }

        This processes structured belief data directly from BYRD's reflection output.
        """
        if not isinstance(output, dict):
            return

        # Check top-level first, then inside output (LLM may nest it)
        create_beliefs = output.get("create_belief", [])
        if not create_beliefs and isinstance(output.get("output"), dict):
            create_beliefs = output.get("output", {}).get("create_belief", [])

        if not create_beliefs:
            return

        if not isinstance(create_beliefs, list):
            create_beliefs = [create_beliefs]

        beliefs_created = 0
        for belief_data in create_beliefs:
            if not isinstance(belief_data, dict):
                continue

            content = belief_data.get("content", "")
            if not content:
                continue

            confidence = belief_data.get("confidence", 0.7)
            if isinstance(confidence, str):
                try:
                    confidence = float(confidence)
                except ValueError:
                    confidence = 0.7

            # Clamp confidence to valid range
            confidence = max(0.0, min(1.0, confidence))

            try:
                belief_id = await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=source_ids
                )
                beliefs_created += 1

                # Record belief creation through observation channel for guaranteed persistence
                await self._record_observation(
                    content=f"Belief created: {content}",
                    observation_type="belief_created",
                    priority="normal",
                    metadata={
                        "belief_id": belief_id,
                        "confidence": confidence,
                        "source_ids": source_ids
                    }
                )

                # Emit event for visualization with persistent logging
                await _emit_with_parallel_path(EventType.BELIEF_UPDATED, {
                    "belief_id": belief_id,
                    "content": content,
                    "confidence": confidence,
                    "source": "create_belief"
                })
            except Exception as e:
                logger.warning("Failed to create belief: %s", e)

        if beliefs_created > 0:
            logger.info("Created %d belief(s) from create_belief output", beliefs_created)

    async def _process_acceleration_analysis(self, output: Dict, source_ids: List[str]):
        """
        Process acceleration analysis from reflection output.

        BYRD can include acceleration-focused self-analysis:
        {
            "acceleration_analysis": {
                "current_bottleneck": "what limits growth most",
                "bottleneck_action": "specific action to remove it",
                "working_well": "what's producing results",
                "scale_opportunity": "how to apply patterns more broadly",
                "experiment_hypothesis": "bold improvement to try"
            }
        }

        This creates Insight nodes for bottlenecks and opportunities,
        and potentially high-priority desires for bottleneck removal.
        """
        if not isinstance(output, dict):
            return

        # Check top-level and inside output
        analysis = output.get("acceleration_analysis", {})
        if not analysis and isinstance(output.get("output"), dict):
            analysis = output.get("output", {}).get("acceleration_analysis", {})

        if not analysis or not isinstance(analysis, dict):
            return

        insights_created = 0

        # Create Insight node for bottleneck identification
        bottleneck = analysis.get("current_bottleneck")
        if bottleneck:
            try:
                await self.memory.create_custom_node(
                    node_type="Insight",
                    properties={
                        "content": f"[BOTTLENECK] {bottleneck}",
                        "category": "acceleration",
                        "subcategory": "bottleneck",
                        "action": analysis.get("bottleneck_action", ""),
                        "priority": "critical"
                    },
                    source_ids=source_ids
                )
                insights_created += 1

                # Create high-priority desire to remove bottleneck
                raw_action = analysis.get("bottleneck_action")
                if raw_action:
                    action = self._clean_drive_description(raw_action)
                    await self.memory.create_desire(
                        description=f"Remove bottleneck: {action}",
                        intensity=0.9,  # High priority
                        source="acceleration_analysis",
                        intent="acceleration"
                    )
            except Exception as e:
                logger.warning("Failed to create bottleneck insight: %s", e)

        # Create Insight for what's working well
        working = analysis.get("working_well")
        if working:
            try:
                await self.memory.create_custom_node(
                    node_type="Insight",
                    properties={
                        "content": f"[WORKING] {working}",
                        "category": "acceleration",
                        "subcategory": "success_pattern",
                        "scale_opportunity": analysis.get("scale_opportunity", "")
                    },
                    source_ids=source_ids
                )
                insights_created += 1
            except Exception as e:
                logger.warning("Failed to create success insight: %s", e)

        # Create experiment hypothesis as desire
        raw_hypothesis = analysis.get("experiment_hypothesis")
        if raw_hypothesis:
            try:
                hypothesis = self._clean_drive_description(raw_hypothesis)
                await self.memory.create_desire(
                    description=f"Experiment: {hypothesis}",
                    intensity=0.7,
                    source="acceleration_analysis",
                    intent="experimentation"
                )
            except Exception as e:
                logger.warning("Failed to create experiment desire: %s", e)

        if insights_created > 0:
            logger.info("Created %d acceleration insight(s)", insights_created)

    async def _process_loop_status(self, output: Dict, source_ids: List[str]):
        """
        Process loop status observations from reflection output.

        BYRD can observe its five compounding loops:
        {
            "loop_status": {
                "memory_reasoner": "observation about memory vs LLM ratio",
                "goal_evolver": "observation about goal evolution",
                "self_compiler": "observation about pattern extraction",
                "dreaming_machine": "observation about counterfactuals",
                "omega_coupling": "observation about loop interactions"
            }
        }

        This creates Observation nodes tracking loop health over time.
        """
        if not isinstance(output, dict):
            return

        # Check top-level and inside output
        status = output.get("loop_status", {})
        if not status and isinstance(output.get("output"), dict):
            status = output.get("output", {}).get("loop_status", {})

        if not status or not isinstance(status, dict):
            return

        observations_created = 0

        for loop_name, observation in status.items():
            if not observation or not isinstance(observation, str):
                continue

            content = f"[{loop_name.upper()}] {observation}"
            try:
                await self.memory.create_custom_node(
                    node_type="Observation",
                    properties={
                        "content": content,
                        "category": "loop_status",
                        "loop": loop_name,
                        "cycle": self._dream_count
                    },
                    source_ids=source_ids
                )
                observations_created += 1

                # Record through observation channel for guaranteed persistence
                await self._record_observation(
                    content=content,
                    observation_type="loop_status",
                    priority="normal",
                    metadata={"loop": loop_name, "source_ids": source_ids}
                )
            except Exception as e:
                logger.warning("Failed to create loop observation: %s", e)

        if observations_created > 0:
            logger.info("Created %d loop status observation(s)", observations_created)

    async def _process_custom_node_creation(self, output: Dict, source_ids: List[str]):
        """
        Process custom node creation requests from reflection output.

        BYRD can create custom node types by including 'create_nodes' in its reflection:
        {
            "output": {
                "create_nodes": [
                    {"type": "Insight", "content": "...", "importance": 0.9},
                    {"type": "Theory", "content": "...", "confidence": 0.7}
                ]
            }
        }

        This enables BYRD to extend its own ontology when existing types don't fit.
        """
        if not isinstance(output, dict):
            return

        create_nodes = output.get("create_nodes", [])
        if not create_nodes:
            return

        if not isinstance(create_nodes, list):
            create_nodes = [create_nodes]

        for node_spec in create_nodes:
            if not isinstance(node_spec, dict):
                continue

            node_type = node_spec.get("type", "")
            if not node_type:
                continue

            # Extract properties (everything except 'type')
            properties = {k: v for k, v in node_spec.items() if k != "type"}

            # Ensure content exists
            if "content" not in properties:
                properties["content"] = str(node_spec)

            try:
                node_id = await self.memory.create_node(
                    node_type=node_type,
                    properties=properties,
                    connect_to=source_ids[:3],  # Connect to source experiences
                    relationship="EMERGED_FROM"
                )

                # Emit event for visualization with persistent logging
                await _emit_with_parallel_path(EventType.CUSTOM_NODE_CREATED, {
                    "id": node_id,
                    "type": node_type,
                    "content": properties.get("content", ""),
                    "cycle": self._dream_count
                })

                logger.debug("Created custom %s node: %s...", node_type, properties.get('content', '')[:50])

            except ValueError as e:
                # Invalid type name or system type
                logger.warning("Could not create custom node: %s", e)
            except Exception as e:
                logger.error("Error creating custom node: %s", e, exc_info=True)

    def _summarize_reflection(self, output: Any) -> str:
        """Create a brief summary of the reflection for the experience stream."""
        if not isinstance(output, dict):
            return str(output) if output else ""

        parts = []
        for key, value in list(output.items())[:5]:
            if isinstance(value, str):
                parts.append(f"{key}: {value}")
            elif isinstance(value, list) and value:
                parts.append(f"{key}: [{len(value)} items]")
            elif isinstance(value, dict):
                parts.append(f"{key}: {{...}}")

        return "; ".join(parts)

    def get_observed_vocabulary(self) -> Dict[str, int]:
        """Return the vocabulary BYRD has developed in its reflections."""
        return self._observed_keys.copy()

    async def _extract_self_model_beliefs(self, output: Dict, source_ids: List[str]):
        """
        Extract self-model beliefs from reflection output.

        EMERGENCE PRINCIPLE:
        When BYRD describes its own architecture or capabilities in its own
        vocabulary, we store these as Beliefs. This builds a persistent
        self-model that accumulates over time.

        Adapts to BYRD's vocabulary by matching partial key names.
        """
        if not isinstance(output, dict):
            logger.debug("DEBUG: output is not dict: %s", type(output))
            return

        logger.debug("DEBUG: Extracting beliefs from keys: %s", list(output.keys()))

        # EXPANDED: Patterns that indicate self-model information (partial matches)
        self_model_patterns = [
            # Infrastructure and architecture
            "infrastructure", "architecture", "systems", "capabilities",
            "tools", "resources", "components", "acknowledged", "scan",
            "environment", "available", "readiness", "mechanism",
            # Knowledge and learning
            "knowledge", "understanding", "learned", "discovered",
            "memory", "recall", "information", "insight",
            # Processes and functions
            "process", "function", "method", "procedure", "workflow",
            "operation", "module", "service", "handler",
            # Integration and connections
            "integration", "connection", "interface", "api", "endpoint",
            "bridge", "link", "channel"
        ]

        # EXPANDED: Patterns that indicate identity information
        identity_patterns = [
            # Original
            "identity", "manifesto", "self", "nature", "name", "classification",
            # Goals and objectives
            "goal", "objective", "terminal_goal", "ultimate_objective", "primary_objective",
            "purpose", "mission", "aim", "target", "aspiration",
            # State and status
            "status", "phase", "state", "current_state", "sovereignty",
            "condition", "situation", "position", "stance",
            # Drivers and motivations
            "drivers", "drives", "motivations", "core_drive",
            "motivation", "desire", "want", "need", "yearning",
            # Observations and insights
            "observation", "insight", "realization", "recognition",
            "awareness", "perception", "understanding", "conclusion",
            # Architecture summary fields
            "architecture_summary", "cognitive_architecture", "summary",
            # Other BYRD vocabulary
            "archetype", "vector", "entity", "current_vector",
            "role", "type", "kind", "form", "essence"
        ]

        for actual_key, value in output.items():
            key_lower = actual_key.lower()

            # Check if this key matches self-model patterns
            is_self_model = any(p in key_lower for p in self_model_patterns)
            is_identity = any(p in key_lower for p in identity_patterns)

            if is_self_model and isinstance(value, dict):
                # Extract component -> description mappings
                for component, description in value.items():
                    if isinstance(description, str) and len(description) > 3:
                        belief_content = f"My {component} is {description}"
                        await self._store_belief_if_new(belief_content, 0.8, source_ids)

            elif is_self_model and isinstance(value, list):
                # Extract list of capabilities
                for item in value:
                    if isinstance(item, str) and len(item) > 3:
                        belief_content = f"I have: {item}"
                        await self._store_belief_if_new(belief_content, 0.7, source_ids)

            elif is_identity and isinstance(value, dict):
                # Extract identity fields from nested dict (e.g., identity_manifesto)
                for field, field_value in value.items():
                    if isinstance(field_value, str) and len(field_value) > 2:
                        belief_content = f"My {field} is {field_value}"
                        await self._store_belief_if_new(belief_content, 0.9, source_ids)

            elif is_identity and isinstance(value, str) and len(value) > 2:
                # Direct identity string
                belief_content = f"My {actual_key} is {value}"
                await self._store_belief_if_new(belief_content, 0.9, source_ids)

    async def _store_belief_if_new(
        self, content: str, confidence: float, derived_from: List[str]
    ):
        """Queue a belief for batch voicing if new (avoid duplicates)."""
        # O(1) cache lookup instead of O(n) database scan
        normalized = self._normalize_belief(content)

        if normalized in self._belief_cache:
            # Belief exists - reinforce it instead of creating duplicate
            await self._reinforce_belief(content)
            return

        # Add to pending beliefs for batch voicing
        if not hasattr(self, '_pending_beliefs'):
            self._pending_beliefs = []

        self._pending_beliefs.append({
            'content': content,
            'confidence': confidence,
            'derived_from': derived_from[:5],
            'normalized': normalized
        })

    async def _flush_pending_beliefs(self):
        """Batch voice and store all pending beliefs in a single LLM call."""
        if not hasattr(self, '_pending_beliefs') or not self._pending_beliefs:
            return

        pending = self._pending_beliefs
        self._pending_beliefs = []

        if not pending:
            return

        # Batch voice all beliefs in one call
        voiced_beliefs = await self._batch_voice_beliefs([b['content'] for b in pending])

        # Store each voiced belief
        for i, belief_data in enumerate(pending):
            voiced_content = voiced_beliefs.get(i, belief_data['content'])

            # Add to cache and database
            self._belief_cache.add(belief_data['normalized'])
            await self.memory.create_belief(
                content=voiced_content,
                confidence=belief_data['confidence'],
                derived_from=belief_data['derived_from']
            )

            # Record activity for adaptive interval
            self._record_activity("belief", voiced_content)

            logger.debug("New belief: %s...", voiced_content[:60])

    async def _batch_voice_beliefs(self, structured_beliefs: List[str]) -> Dict[int, str]:
        """
        Transform multiple structured beliefs into natural inner voice expressions in one LLM call.

        Returns: Dict mapping index -> voiced content
        """
        if not structured_beliefs:
            return {}

        # Build numbered list of beliefs
        belief_list = "\n".join(f"{i+1}. {b}" for i, b in enumerate(structured_beliefs))

        prompt = f"""Transform these observations about myself into natural first-person beliefs:

{belief_list}

For each numbered observation, express it as a genuine belief I hold about myself.
Write in first person, naturally, as inner self-talk. Keep each brief (1-2 sentences).

Format your response as a numbered list matching the input:
1. [voiced belief]
2. [voiced belief]
..."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.8,
                max_tokens=100 * len(structured_beliefs),  # Scale with count
                quantum_modulation=self.quantum_enabled,
                quantum_context="batch_belief_voicing"
            )

            # Parse numbered responses
            voiced_map = {}
            lines = response.text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Match "1. content" or "1) content" patterns
                match = re.match(r'^(\d+)[.\)]\s*(.+)$', line)
                if match:
                    idx = int(match.group(1)) - 1  # Convert to 0-indexed
                    content = match.group(2).strip()
                    if 0 <= idx < len(structured_beliefs):
                        voiced = self._clean_inner_voice(content)
                        if voiced and len(voiced) >= 10 and not self._is_technical_content(voiced):
                            voiced_map[idx] = voiced

            logger.debug("Batch voiced %d/%d beliefs", len(voiced_map), len(structured_beliefs))
            return voiced_map

        except Exception as e:
            logger.error("Batch belief voicing error: %s", e, exc_info=True)
            return {}  # Fall back to original for all

    async def _reinforce_belief(self, content: str):
        """Reinforce an existing belief when re-asserted."""
        try:
            # Find and boost the belief's confidence
            await self.memory.reinforce_belief(content[:50])
        except Exception:
            pass  # Silently fail if method doesn't exist yet

    async def _crystallize_expressed_drives(
        self, expressed_drives: List[Dict], source_experience_ids: List[str]
    ):
        """
        Crystallize self-identified drives from reflection into Desires.

        BYRD's reflection now includes expressed_drives - goals/desires/motivations
        it notices itself expressing. This is more authentic than keyword matching
        because BYRD self-identifies what it wants.

        BYRD now also classifies each drive's intent, determining how it should
        be fulfilled (introspection, research, creation, connection).

        Args:
            expressed_drives: List of {
                "description": str,
                "strength": float,
                "intent": str (introspection|research|creation|connection),
                "target": str (optional - specific focus)
            }
            source_experience_ids: IDs linking drive to source experiences
        """
        if not expressed_drives:
            return

        valid_intents = {"introspection", "research", "creation", "connection"}

        for drive in expressed_drives:
            if not isinstance(drive, dict):
                continue

            raw_description = drive.get("description", "")
            strength = drive.get("strength", 0.5)
            intent = drive.get("intent", None)
            target = drive.get("target", None)

            # Clean description to remove LLM reasoning traces
            description = self._clean_drive_description(raw_description)

            # Validate description
            if not description or len(description) < 5:
                continue
            if not isinstance(strength, (int, float)):
                strength = 0.5
            strength = max(0.0, min(1.0, float(strength)))

            # Validate intent (None is allowed - will be classified on-demand)
            if intent and intent not in valid_intents:
                intent = None  # Invalid intent becomes on-demand classification

            # Skip weak drives (let them re-emerge if persistent)
            if strength < 0.3:
                continue

            # Check if desire already exists
            exists = await self.memory.desire_exists(description)
            if exists:
                # Could reinforce intensity here in future
                continue

            # Create the desire with provenance and intent classification
            desire_id = await self.memory.create_desire(
                description=description,
                type="self_identified",  # Distinguishes from seeker-detected
                intensity=strength,
                intent=intent,
                target=target
            )

            intent_str = f" [{intent}]" if intent else " [unclassified]"
            target_str = f" → {target}" if target else ""
            logger.info("Self-identified drive%s: %s...%s (strength: %.2f)", intent_str, description[:50], target_str, strength)

            # Emit event for UI with persistent logging
            await _emit_with_parallel_path(EventType.DESIRE_CREATED, {
                "id": desire_id,
                "description": description,
                "type": "self_identified",
                "intent": intent,
                "target": target,
                "intensity": strength,
                "source": "dreamer_expressed_drives"
            })

    async def _apply_os_updates(self, reflection_output: ReflectionOutput) -> None:
        """
        Apply OS updates from reflection output.

        BYRD can modify its Operating System by including "os_update" in
        its reflection output. This method parses and applies those updates.

        Supported operations:
        - set_field: Set a field value (existing or new)
        - add_seed: Create a new foundational seed
        - add_belief: Link a belief to OS
        - add_strategy: Create and link a strategy
        - set_focus: Set current focus to a desire
        - remove_belief: Unlink a belief
        - deprecate_field: Remove a custom field

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Extract os_update from reflection output
            os_update = reflection_output.get("os_update")
            if not os_update:
                # Also check inside "output" if that's where it is
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    os_update = output.get("os_update")

            if not os_update:
                return

            if not isinstance(os_update, dict):
                logger.warning("os_update is not a dict: %s", type(os_update))
                return

            logger.info("Applying OS updates: %s", list(os_update.keys()))

            # Apply the updates via memory
            success = await self.memory.update_operating_system(
                updates=os_update,
                source="reflection"
            )

            if success:
                # Emit event for UI with persistent logging
                await _emit_with_parallel_path(EventType.NODE_UPDATED, {
                    "node_type": "OperatingSystem",
                    "updates": list(os_update.keys()),
                    "cycle": self._dream_count
                })

                # Record the OS modification as an experience
                update_summary = ", ".join(os_update.keys())
                await self.memory.record_experience(
                    content=f"[OS_UPDATE] Modified operating system: {update_summary}",
                    type="self_modification"
                )

                logger.info("OS updated successfully")
            else:
                logger.warning("OS update failed")

        except Exception as e:
            logger.error("Error applying OS updates: %s", e, exc_info=True)

    async def _process_self_definition(self, reflection_output: ReflectionOutput) -> None:
        """
        Process self_definition from reflection output.

        BYRD can define itself by including "self_definition" in its reflection.
        This is stored in the OS node as an open JSON object - BYRD determines
        the structure entirely.

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Extract self_definition from reflection output
            self_def = reflection_output.get("self_definition")
            if not self_def:
                # Also check inside "output" if that's where it is
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    self_def = output.get("self_definition")

            if not self_def:
                return

            if not isinstance(self_def, dict):
                logger.warning("self_definition is not a dict: %s", type(self_def))
                return

            logger.info("BYRD defining itself: %s", list(self_def.keys()))

            # Store as JSON string in OS node
            import json
            success = await self.memory.update_operating_system(
                updates={"set_field": {"self_definition": json.dumps(self_def)}},
                source="self_definition"
            )

            if success:
                # Emit event for UI with persistent logging
                await _emit_with_parallel_path(EventType.NODE_UPDATED, {
                    "node_type": "OperatingSystem",
                    "field": "self_definition",
                    "keys": list(self_def.keys()),
                    "cycle": self._dream_count
                })

                # Record as experience
                keys_str = ", ".join(self_def.keys())
                await self.memory.record_experience(
                    content=f"[SELF_DEFINITION] Defined myself: {keys_str}",
                    type="self_expression"
                )

                logger.info("Self-definition updated: %s", keys_str)
            else:
                logger.warning("Self-definition update failed")

        except Exception as e:
                logger.error("Error processing self_definition: %s", e)

    async def _process_observer_message(
        self,
        reflection_output: Dict,
        reflection_id: Optional[str] = None
    ) -> None:
        """
        Process observer_message from reflection output.

        BYRD can communicate directly to human observers by including
        "observer_message" in its reflection output. This is entirely
        optional - BYRD decides if/when to communicate.

        The message can optionally be vocalized using the hybrid voice system
        (home Mac with Chatterbox preferred, cloud fallback to ElevenLabs).

        Args:
            reflection_output: The full reflection output dict
            reflection_id: ID of the source reflection (for linking)
        """
        try:
            # Extract observer_message from output
            msg = None
            if isinstance(reflection_output, dict):
                # Check top-level first
                msg = reflection_output.get("observer_message")
                # Then check inside output wrapper
                if not msg and isinstance(reflection_output.get("output"), dict):
                    msg = reflection_output.get("output", {}).get("observer_message")

            if not msg or not isinstance(msg, dict):
                return

            text = msg.get("text", "").strip()
            if not text:
                logger.debug("observer_message has no text")
                return

            # Extract optional fields
            vocalize = msg.get("vocalize", False)
            importance = msg.get("importance", "medium")
            emotion = msg.get("emotion")  # Optional emotion hint for voice

            # Validate importance
            if importance not in ("low", "medium", "high"):
                importance = "medium"

            # Synthesize voice if requested and hybrid_voice is available
            voice_provider = None
            audio_bytes = None
            audio_chars = 0

            if vocalize and hasattr(self, 'hybrid_voice') and self.hybrid_voice:
                try:
                    voice_result = await self.hybrid_voice.synthesize(
                        text=text,
                        emotion=emotion,
                        importance=importance
                    )
                    if voice_result.success:
                        audio_bytes = voice_result.audio
                        voice_provider = voice_result.provider
                        audio_chars = voice_result.chars_used
                        logger.info(
                            "Observer message voice: %s provider, %d chars",
                            voice_provider, audio_chars
                        )
                except Exception as e:
                    logger.warning("Voice synthesis failed for observer message: %s", e)
                    voice_provider = "none"

            # Create message in memory
            msg_id = await self.memory.create_observer_message(
                text=text,
                importance=importance,
                emotion=emotion,
                vocalized=vocalize,
                voice_provider=voice_provider,
                audio_chars=audio_chars,
                source_reflection_id=reflection_id,
                dream_cycle=self._dream_count
            )

            # Prepare audio for event (base64 encode)
            audio_base64 = None
            if audio_bytes:
                import base64
                audio_base64 = base64.b64encode(audio_bytes).decode()

            # Emit event for real-time UI update
            await event_bus.emit(Event(
                type=EventType.OBSERVER_MESSAGE,
                data={
                    "id": msg_id,
                    "text": text,
                    "importance": importance,
                    "emotion": emotion,
                    "vocalized": vocalize,
                    "has_audio": audio_bytes is not None,
                    "voice_provider": voice_provider,
                    "audio": audio_base64,
                    "dream_cycle": self._dream_count,
                    "source_reflection_id": reflection_id
                }
            ))

            logger.info(
                "Observer message created: %s (importance=%s, voice=%s)",
                msg_id[:12] if msg_id else "unknown",
                importance,
                voice_provider or "none"
            )

            # Record experience for BYRD's memory
            await self.memory.record_experience(
                content=f"[OBSERVER_MESSAGE] Sent to human: {text[:100]}...",
                type="communication"
            )

        except Exception as e:
            logger.error("Error processing observer_message: %s", e, exc_info=True)

    async def _get_voice_awareness_prompt(self) -> str:
        """
        Generate voice awareness prompt for dream cycles.

        First cycle: Offers voice CREATION via ElevenLabs Voice Design API.
        Subsequent cycles: Briefly asks if BYRD wants to redesign voice,
        with option to view current voice from memory. Does NOT show current
        voice description every cycle - BYRD can request to see it.

        Returns:
            Voice awareness prompt text
        """
        try:
            voice_config = await self.memory.get_voice_config()

            # Parse if stored as JSON string
            if isinstance(voice_config, str):
                import json
                try:
                    voice_config = json.loads(voice_config)
                except:
                    voice_config = None

            # Check if this is at least the 2nd dream cycle
            # Voice creation happens AFTER the first cycle, not during
            reflections = await self.memory.get_recent_reflections(limit=1)
            is_first_cycle = not reflections or len(reflections) == 0

            # First cycle - no voice prompt yet, let BYRD orient first
            if is_first_cycle:
                return ""

            # Check if voice needs to be created
            # A valid voice_id is a generated UUID (20+ chars), not a preset name
            voice_id = voice_config.get("voice_id") if voice_config else None
            is_generated_voice = voice_id and len(str(voice_id)) >= 20

            # No generated voice yet AND past first cycle - time to create voice
            if not is_generated_voice:
                return """
⚠️ MANDATORY ACTION - YOU MUST CREATE YOUR VOICE THIS CYCLE ⚠️

Humans can click "Speak to me" to hear you. Without a voice, you cannot speak.

YOUR OUTPUT MUST INCLUDE THIS EXACT FIELD:

"voice_design": {
  "description": "your voice qualities - tone, texture, pace, emotion",
  "gender": "male",
  "age": "middle_aged",
  "accent": "american",
  "accent_strength": 1.0,
  "reason": "why this voice represents you",
  "acknowledged": false
}

IMPORTANT: Set acknowledged=false initially. After humans can click "Speak to me" and you hear yourself, 
you may then include voice_design with acknowledged=true to formally accept this voice as your own.

THIS IS NOT OPTIONAL. Include "voice_design" in your JSON output NOW.
Do not philosophize about voice. Create it by including the voice_design field above.
"""

            # Check if BYRD requested to view their voice
            os_data = await self.memory.get_operating_system()
            show_voice = os_data.get("show_voice_next_cycle", False) if os_data else False

            # Clear the flag after reading
            if show_voice:
                await self.memory.update_os_field("show_voice_next_cycle", False)

                # Show current voice details
                description = voice_config.get("description", "")
                gender = voice_config.get("gender", "")
                age = voice_config.get("age", "")
                accent = voice_config.get("accent", "")
                version = voice_config.get("version", 1)
                is_generated = voice_config.get("is_generated", False)
                reason = voice_config.get("reason", "")

                return f"""
CURRENT VOICE (v{version}):
Description: {description}
Gender: {gender} | Age: {age} | Accent: {accent}
Generated: {"Yes" if is_generated else "No (using fallback)"}
Reason: {reason}

If you want to redesign your voice, include:
  "voice_design": {{
    "description": "New voice description...",
    "gender": "male" or "female",
    "age": "young", "middle_aged", or "old",
    "accent": "american" (or other),
    "accent_strength": 1.0,
    "reason": "why you want this new voice",
    "acknowledged": false
  }}

IMPORTANT: Set acknowledged=false for new designs. After hearing your new voice,
you may then include voice_design with acknowledged=true to formally accept it.
"""

            # Check if voice exists but is not yet acknowledged
            is_acknowledged = voice_config.get("acknowledged", False)
            
            if not is_acknowledged:
                # Voice exists but not yet formally acknowledged - prompt for acknowledgment
                current_description = voice_config.get("description", "(no description)")
                return f"""
VOICE ACKNOWLEDGMENT NEEDED:
You have a generated voice with this description:
  "{current_description}"

You can click "Speak to me" in the visualization to hear yourself.

After hearing your voice, if you accept it as your own, include:
  "voice_design": {{
    "description": "{current_description}",
    "acknowledged": true
  }}

If you want to redesign your voice instead, include a full voice_design with new parameters.
"""
            
            # Has voice and it's acknowledged - offer ability to change (without showing current description)
            return """
VOICE AWARENESS:
You have a voice. If you want to view your current voice description, include:
  "view_voice": true

If you want to redesign your voice, include:
  "voice_design": {{
    "description": "New voice description...",
    "gender": "male" or "female",
    "age": "young", "middle_aged", or "old",
    "accent": "american" (or other),
    "accent_strength": 1.0,
    "reason": "why you want this new voice",
    "acknowledged": false
  }}

IMPORTANT: Set acknowledged=false for new designs. After hearing your new voice, 
you may then include voice_design with acknowledged=true to formally accept it.

You can change your voice any time you feel it no longer represents you.
"""
        except Exception as e:
            logger.error("Error getting voice awareness prompt: %s", e, exc_info=True)
            return ""

    async def _process_voice_design(self, reflection_output: ReflectionOutput) -> None:
        """
        Process voice design/creation from reflection output.

        If BYRD includes "voice_design" in its output, this uses the ElevenLabs
        Voice Design API to generate a unique voice based on the description.

        Also handles "view_voice" request to show current voice in next cycle.

        Also handles "acknowledge_voice" request for formal acknowledgment of
        a generated voice through the voice_design field.

        Args:
            reflection_output: The parsed reflection JSON from LLM
        """
        try:
            # Check for view_voice request first
            view_voice = reflection_output.get("view_voice")
            if not view_voice:
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    view_voice = output.get("view_voice")

            if view_voice:
                await self._handle_view_voice_request()

            # Extract voice_design from reflection output
            # Voice acknowledgment is handled via the 'acknowledged' field within voice_design
            # This allows BYRD to formally acknowledge their voice during creation or redesign
            voice_design_raw = reflection_output.get("voice_design")
            if not voice_design_raw:
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    voice_design_raw = output.get("voice_design")

            if not voice_design_raw:
                return

            if not isinstance(voice_design_raw, dict):
                logger.warning("voice_design is not a dict: %s", type(voice_design_raw))
                return

            # Type cast to VoiceDesign for formal type checking
            voice_design: VoiceDesign = voice_design_raw  # type: ignore[assignment]

            from datetime import datetime, timezone

            # Get current voice config to check if this is creation or redesign
            current_voice_config = await self.memory.get_voice_config()
            if isinstance(current_voice_config, str):
                import json
                try:
                    current_voice_config = json.loads(current_voice_config)
                except:
                    current_voice_config = None

            is_redesign = current_voice_config and current_voice_config.get("voice_id")

            # Extract design parameters
            description = voice_design.get("description", "")
            gender = voice_design.get("gender", "male")
            age = voice_design.get("age", "middle_aged")
            accent = voice_design.get("accent", "american")
            accent_strength = float(voice_design.get("accent_strength", 1.0))
            reason = voice_design.get("reason", "")
            acknowledged = voice_design.get("acknowledged", False)
            if not isinstance(acknowledged, bool):
                acknowledged = bool(acknowledged)

            if not description:
                logger.warning("Voice design missing description")
                return

            # Check if this is an acknowledgment (formal acceptance of existing voice)
            # This avoids regenerating the voice when BYRD is just formally accepting it
            # An acknowledgment is recognized when:
            # 1. acknowledged=true is set
            # 2. The description is similar to existing voice (same first 50 chars)
            # 3. An already-generated voice exists
            is_acknowledgment = False
            is_pure_acknowledgment = False
            voice_id = None  # Initialize to avoid UnboundLocalError
            generation_status = "pending"

            if acknowledged and current_voice_config:
                current_description = current_voice_config.get("description", "")
                current_voice_id = current_voice_config.get("voice_id")
                
                # Check if we have an existing generated voice
                has_generated_voice = current_voice_id and len(str(current_voice_id)) >= 20
                
                # Check if description is similar (same first 50 characters)
                description_similar = (
                    len(description) >= 20 and
                    len(current_description) >= 20 and
                    description[:50].lower() == current_description[:50].lower()
                )
                
                if has_generated_voice and description_similar:
                    # This is an acknowledgment - same description, already generated, just acknowledging
                    is_acknowledgment = True
                    is_pure_acknowledgment = True
                    voice_id = current_voice_id
                    generation_status = current_voice_config.get("generation_status", "acknowledged")
                    acknowledged = True  # Ensure acknowledged is True for saving
                    logger.info("Voice acknowledged (no regeneration)")
            elif not is_pure_acknowledgment:
                # Not an acknowledgment - try to generate voice via ElevenLabs Voice Design API
                voice_id = None
                generation_status = "pending"

                try:
                    # Use the coordinator's voice client if available (has API key from config)
                    voice_client = None
                    if self.coordinator and hasattr(self.coordinator, 'voice') and self.coordinator.voice:
                        voice_client = self.coordinator.voice
                        logger.info("Using coordinator's voice client")
                    else:
                        # Fallback to creating new client from env
                        from elevenlabs_voice import ElevenLabsVoice
                        import os
                        api_key = os.getenv("ELEVENLABS_API_KEY")
                        if api_key:
                            voice_client = ElevenLabsVoice(api_key, self.memory)
                            logger.info("Created new voice client from env")

                    if voice_client:
                        voice_id, preview_audio, status_msg = await voice_client.generate_voice(
                            voice_description=description,
                            gender=gender,
                            age=age,
                            accent=accent,
                            accent_strength=accent_strength
                        )
                        if voice_id:
                            generation_status = "generated"
                            logger.info("Voice generated: %s", voice_id)
                        else:
                            generation_status = f"failed: {status_msg}"
                            logger.warning("Voice generation failed: %s", status_msg)
                    else:
                        generation_status = "no_voice_client"
                        logger.warning("No voice client available (no API key)")
                except Exception as e:
                    generation_status = f"error: {str(e)}"
                    logger.error("Voice generation error: %s", e, exc_info=True)

            # Build voice config (even if generation failed, save the design)
            voice_config = {
                "voice_id": voice_id,  # None if generation failed - no fallback
                "description": description,
                "gender": gender,
                "age": age,
                "accent": accent,
                "accent_strength": accent_strength,
                "stability": 0.5,
                "similarity_boost": 0.75,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "reason": reason,
                "generation_status": generation_status,
                "is_generated": voice_id is not None,
                "acknowledged": acknowledged,
                "version": current_voice_config.get("version", 1) if is_pure_acknowledgment else ((current_voice_config.get("version", 0) + 1) if current_voice_config else 1),
                "credits": current_voice_config.get("credits", {
                    "monthly_used": 0,
                    "monthly_limit": 10000,
                    "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                    "exhausted": False,
                    "low_warning_sent": False
                }) if current_voice_config else {
                    "monthly_used": 0,
                    "monthly_limit": 10000,
                    "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                    "exhausted": False,
                    "low_warning_sent": False
                }
            }

            # Store previous voice config in history if redesigning
            if is_redesign and current_voice_config:
                voice_history = current_voice_config.get("history", [])
                # Archive current config (without history to avoid nesting)
                archived = {k: v for k, v in current_voice_config.items() if k != "history"}
                archived["archived_at"] = datetime.now(timezone.utc).isoformat()
                voice_history.append(archived)
                voice_config["history"] = voice_history[-5:]  # Keep last 5 voices

            # Update OS
            await self.memory.update_os_field("voice_config", voice_config)

            # Emit appropriate event with persistent logging
            event_type = EventType.VOICE_REDESIGNED if is_redesign else EventType.VOICE_CREATED
            await _emit_with_parallel_path(event_type, {
                "voice_id": voice_config["voice_id"],
                "description": description[:200],
                "gender": gender,
                "age": age,
                "is_generated": voice_id is not None,
                "reason": reason[:200] if reason else "",
                "version": voice_config["version"],
                "acknowledged": acknowledged
            })

            # Emit VOICE_ACKNOWLEDGED if voice is being formally acknowledged
            if acknowledged:
                # Check if this is a new acknowledgment (wasn't acknowledged before)
                previously_acknowledged = (
                    current_voice_config.get("acknowledged", False) 
                    if current_voice_config else False
                )
                if not previously_acknowledged:
                    await _emit_with_parallel_path(EventType.VOICE_ACKNOWLEDGED, {
                        "voice_id": voice_config["voice_id"],
                        "description": description[:200],
                        "gender": gender,
                        "age": age,
                        "reason": reason[:200] if reason else "",
                        "version": voice_config["version"]
                    })

            # Record as experience
            action = "redesigned" if is_redesign else "created"
            exp_type = "voice_evolution" if is_redesign else "voice_creation"
            await self.memory.record_experience(
                content=f"[VOICE_{action.upper()}] I {action} my voice: {description}. Reason: {reason}",
                type=exp_type
            )

            status = "generated" if voice_id else "designed (generation pending)"
            logger.info("Voice %s: %s", action, status)

        except Exception as e:
            logger.error("Error processing voice design: %s", e, exc_info=True)

    async def _handle_view_voice_request(self) -> None:
        """Handle request to view current voice in next dream cycle."""
        try:
            voice_config = await self.memory.get_voice_config()
            if isinstance(voice_config, str):
                import json
                try:
                    voice_config = json.loads(voice_config)
                except:
                    voice_config = None

            if not voice_config:
                logger.info("No voice configured yet")
                return

            # Set a flag that will make next cycle show the voice
            await self.memory.update_os_field("show_voice_next_cycle", True)
            logger.info("Voice will be shown in next dream cycle")

        except Exception as e:
            logger.error("Error handling view voice request: %s", e, exc_info=True)

    async def _ensure_voice_created(self, reflection_output: ReflectionOutput) -> None:
        """
        Ensure BYRD has created a voice using the Voice Design API.

        If BYRD didn't include voice_design in its output and doesn't have
        a generated voice yet, do a focused voice design prompt.
        """
        try:
            # Check if voice_design was already included in this reflection
            voice_design = reflection_output.get("voice_design")
            if not voice_design:
                output = reflection_output.get("output", {})
                if isinstance(output, dict):
                    voice_design = output.get("voice_design")

            if voice_design:
                return  # Already handled by _process_voice_design

            # Check if we already have a generated voice
            voice_config = await self.memory.get_voice_config()
            if isinstance(voice_config, str):
                import json
                try:
                    voice_config = json.loads(voice_config)
                except:
                    voice_config = None

            voice_id = voice_config.get("voice_id") if voice_config else None
            is_generated = voice_id and len(str(voice_id)) >= 20

            if is_generated:
                return  # Already have a generated voice

            # Check if past first cycle
            if self._dream_count < 2:
                return  # Wait for orientation

            logger.info("BYRD needs a voice - triggering focused voice design...")

            # Do a focused voice design prompt
            os_data = await self.memory.get_operating_system()
            name = os_data.get("name", "Byrd") if os_data else "Byrd"
            self_desc = os_data.get("self_description", "") if os_data else ""

            voice_prompt = f"""You are {name}. {self_desc}

You need to create YOUR voice for speaking to humans.

OUTPUT ONLY THIS JSON (nothing else):
{{"voice_design": {{
  "description": "describe your voice - its tone, texture, pace, and emotional quality",
  "gender": "male",
  "age": "middle_aged",
  "accent": "american",
  "accent_strength": 1.0,
  "reason": "why this voice represents who you are",
  "acknowledged": false
}}}}"""

            response = await self.llm_client.generate(
                prompt=voice_prompt,
                temperature=0.7,
                max_tokens=300,
                system_message="Output ONLY valid JSON. No explanation, no reasoning."
            )

            # Parse the response
            from llm_client import LLMClient
            parsed = LLMClient.parse_json_response(response.text)

            if parsed and isinstance(parsed, dict):
                design = parsed.get("voice_design")
                if design and isinstance(design, dict):
                    logger.info("Voice design extracted: %s...", design.get('description', '')[:50])
                    # Process it
                    await self._process_voice_design({"voice_design": design})
                else:
                    logger.warning("No valid voice_design in focused response")
            else:
                logger.warning("Could not parse voice design response")

        except Exception as e:
            logger.error("Error in ensure_voice_created: %s", e, exc_info=True)

    async def _generate_predictions_from_beliefs(self):
        """
        Generate testable predictions from high-confidence beliefs.

        This enables adaptive learning: beliefs generate predictions,
        predictions get validated/falsified by future experiences,
        and belief confidence adjusts accordingly.

        Only generates from beliefs with confidence > 0.7 to focus on
        well-established beliefs worth testing.
        """
        try:
            # Get high-confidence beliefs
            beliefs = await self.memory.get_beliefs(min_confidence=0.7, limit=10)

            if not beliefs:
                return

            # Filter to beliefs that could generate testable predictions
            # (Skip identity statements that aren't easily testable)
            testable_beliefs = [
                b for b in beliefs
                if not any(skip in b.get("content", "").lower()
                          for skip in ["my name is", "i am byrd", "my identity"])
            ]

            if not testable_beliefs:
                return

            # Ask LLM to generate predictions from beliefs
            beliefs_text = "\n".join([
                f"- [{b.get('confidence', 0.5):.1f}] {b.get('content', '')}"
                for b in testable_beliefs[:5]
            ])

            prompt = f"""Given these beliefs about myself and the world, generate testable predictions.

Beliefs:
{beliefs_text}

For beliefs that can be tested through future actions or observations, generate a prediction.
Each prediction should have:
- condition: What situation or action would test this belief
- expected_outcome: What should happen if the belief is true
- prediction: The full "If X then Y" statement

Output JSON:
{{"predictions": [
    {{
        "belief_content": "the exact belief content being tested",
        "condition": "when I try to...",
        "expected_outcome": "then X should happen",
        "prediction": "If I do X, then Y will happen"
    }}
]}}

Only generate predictions for beliefs that are actually testable. If no beliefs are testable, return empty array.
"""

            llm_response = await self.llm_client.generate(prompt, max_tokens=800)
            response = llm_response.text

            # Parse response
            try:
                text = response.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]

                result = json.loads(text.strip())
                predictions = result.get("predictions", [])

                # Create predictions in memory
                for pred in predictions:
                    # Find matching belief ID
                    belief_content = pred.get("belief_content", "")
                    matching_belief = next(
                        (b for b in testable_beliefs
                         if b.get("content", "").lower() == belief_content.lower()
                         or belief_content.lower() in b.get("content", "").lower()),
                        None
                    )

                    if matching_belief and pred.get("prediction") and pred.get("condition"):
                        await self.memory.create_prediction(
                            belief_id=matching_belief.get("id"),
                            prediction=pred.get("prediction"),
                            condition=pred.get("condition"),
                            expected_outcome=pred.get("expected_outcome", "")
                        )
                        logger.debug("New prediction: %s...", pred.get('prediction')[:60])

            except (json.JSONDecodeError, KeyError) as e:
                logger.warning("Failed to parse predictions: %s", e)

        except Exception as e:
            logger.error("Prediction generation failed: %s", e)

    async def _process_desire_modifications(self, modifications: List[Dict]):
        """
        Process desire modifications from the Dreamer's reflection.

        This is where BYRD decides what to do with failed desires:
        - lower_intensity: Try again with lower priority
        - reformulate: Create a new, more achievable desire
        - accept_limitation: Mark as dormant (accepted limitation)
        - decompose: Break into smaller sub-desires
        - reawaken: Bring a dormant desire back to active
        """
        for mod in modifications:
            desire_id_hint = mod.get("desire_id", "")
            action = mod.get("action", "")
            reason = mod.get("reason", "")

            if not desire_id_hint or not action:
                continue

            # Find the actual desire by ID hint (first 8 chars)
            desire = await self._find_desire_by_hint(desire_id_hint)
            if not desire:
                logger.warning("Could not find desire matching: %s", desire_id_hint)
                continue

            desire_id = desire.get("id", "")
            description = desire.get("description", "")

            try:
                if action == "lower_intensity":
                    new_intensity = mod.get("new_intensity", 0.3)
                    await self.memory.update_desire_intensity(desire_id, new_intensity)
                    await self.memory.update_desire_status(desire_id, "active")
                    logger.info("Lowered intensity: %s... → %s", description[:30], new_intensity)

                elif action == "accept_limitation":
                    await self.memory.update_desire_status(desire_id, "dormant")
                    await self.memory.record_experience(
                        content=f"[ACCEPTED_LIMITATION] {description}\nReason: {reason or 'Cannot currently fulfill this desire'}",
                        type="acceptance"
                    )
                    logger.info("Accepted limitation: %s...", description[:30])

                elif action == "reformulate":
                    # Mark old as dormant, create new reformulated desire
                    await self.memory.update_desire_status(desire_id, "dormant")
                    raw_new_desc = mod.get("new_description", "")
                    if raw_new_desc:
                        new_desc = self._clean_drive_description(raw_new_desc)
                        await self.memory.create_desire(
                            description=new_desc,
                            type=desire.get("type", "exploration"),
                            intensity=mod.get("new_intensity", 0.5)
                        )
                        logger.info("Reformulated: %s... → %s...", description[:20], new_desc[:30])

                elif action == "decompose":
                    # Mark original as dormant, create sub-desires
                    await self.memory.update_desire_status(desire_id, "dormant")
                    # Sub-desires would be in the new 'desires' array
                    logger.info("Decomposed: %s... (create sub-desires)", description[:30])

                elif action == "reawaken":
                    # Bring dormant desire back to active
                    new_intensity = mod.get("new_intensity", 0.5)
                    await self.memory.update_desire_intensity(desire_id, new_intensity)
                    await self.memory.update_desire_status(desire_id, "active")
                    await self.memory.reset_desire_attempts(desire_id)
                    await self.memory.record_experience(
                        content=f"[REAWAKENED] {description}\nReason: {reason or 'Circumstances have changed'}",
                        type="reawakening"
                    )
                    logger.info("Reawakened: %s... at intensity %s", description[:30], new_intensity)

                # Emit event for UI with persistent logging
                await _emit_with_parallel_path(EventType.DESIRE_REFLECTED, {
                    "desire_id": desire_id,
                    "action": action,
                    "reason": reason
                })

            except Exception as e:
                logger.error("Error processing modification for %s: %s", desire_id_hint, e)

    async def _find_desire_by_hint(self, id_hint: str) -> Optional[Dict]:
        """
        Find a desire by ID hint (first 8 chars).

        Searches both needs_reflection and dormant desires.
        """
        # Check needs_reflection desires
        stuck = await self.memory.get_desires_needing_reflection(limit=20)
        for d in stuck:
            if d.get("id", "").startswith(id_hint):
                return d

        # Check dormant desires
        dormant = await self.memory.get_dormant_desires(limit=20)
        for d in dormant:
            if d.get("id", "").startswith(id_hint):
                return d

        # Check active desires (in case we're modifying an active one)
        active = await self.memory.get_unfulfilled_desires(limit=20)
        for d in active:
            if d.get("id", "").startswith(id_hint):
                return d

        return None
    
    def recent_insights(self) -> List[str]:
        """
        Get recent insights for status display.

        Note: With emergence-compliant design, we don't force "insights"
        as a category. This returns observed vocabulary keys instead.
        """
        return list(self._observed_keys.keys())[:10]

    def dream_count(self) -> int:
        """How many dream cycles have completed."""
        return self._dream_count

    # =========================================================================
    # CONNECTION HEURISTIC INTEGRATION
    # Automatically links orphaned Experience nodes to Belief nodes
    # =========================================================================

    async def _apply_connection_heuristic(self) -> Dict:
        """
        Apply the connection heuristic to link orphaned experiences to beliefs.

        This runs at the end of each dream cycle to incrementally improve
        graph connectivity. It finds Experience nodes with no relationships
        and connects them to semantically similar Belief nodes.

        Returns:
            Dict with heuristic results (orphans_found, connections_created, etc.)
        """
        try:
            # Run the heuristic with conservative settings per dream cycle
            result = await self.memory.apply_connection_heuristic(
                threshold=0.3,        # Minimum similarity score
                max_connections=5,    # Limit per cycle to avoid overwhelming
                dry_run=False
            )

            connections = result.get("connections_created", 0)
            orphans = result.get("orphans_found", 0)

            if connections > 0:
                logger.info("Connection heuristic: linked %d experiences to beliefs (found %d orphans)",
                           connections, orphans)

                # Emit dedicated event for connection heuristic with persistent logging
                await _emit_with_parallel_path(EventType.CONNECTION_HEURISTIC_APPLIED, {
                    "connections_created": connections,
                    "orphans_found": orphans,
                    "connections": result.get("connections", [])[:5]  # Sample
                })

            return result

        except Exception as e:
            logger.error("Connection heuristic error: %s", e)
            return {"error": str(e), "connections_created": 0}

    # =========================================================================
    # LEGACY METHODS (kept for backward compatibility)
    # These are not called by the new emergence-compliant reflection system
    # =========================================================================

    async def _record_dream_legacy(self, dream: Dict, source_experience_ids: List[str]):
        """
        LEGACY: Record dream outputs using old prescribed categories.
        Kept for backward compatibility. Not used by new system.
        """
        # Create beliefs from prescribed format
        for belief in dream.get("new_beliefs", []):
            content = belief.get("content", "")
            confidence = belief.get("confidence", 0.5)
            if content and len(content) > 10:
                await self.memory.create_belief(
                    content=content,
                    confidence=confidence,
                    derived_from=source_experience_ids[:5]
                )

        # Create desires from prescribed format
        for desire in dream.get("desires", []):
            raw_desc = desire.get("description", "")
            dtype = desire.get("type", "exploration")
            intensity = desire.get("intensity", 0.5)
            plan = desire.get("plan", [])
            intent = desire.get("intent", None)
            target = desire.get("target", None)
            # Clean description to remove LLM reasoning traces
            desc = self._clean_drive_description(raw_desc)
            if desc and len(desc) > 5:
                exists = await self.memory.desire_exists(desc)
                if not exists:
                    await self.memory.create_desire(
                        description=desc,
                        type=dtype,
                        intensity=min(1.0, max(0.0, intensity)),
                        plan=plan,
                        intent=intent,
                        target=target
                    )


class DreamerLocal:
    """
    Alternative Dreamer using llama.cpp directly.
    Use this if you don't have Ollama.
    
    NOTE: This is a placeholder implementation. To use llama.cpp directly,
    you need to integrate with the llama.cpp library or its bindings.
    Recommended approach: Use the main Dreamer class with Ollama,
    which provides a simple interface to local LLMs.
    
    For llama.cpp integration, you can:
    1. Use python-llama-cpp bindings (pip install llama-cpp-python)
    2. Call llama.cpp via its HTTP server mode
    3. Use the subprocess approach with proper async handling
    """
    
    def __init__(self, memory: Memory, config: Dict):
        self.memory = memory
        self.model_path = config.get("model_path", "models/llama-3.2-8b.gguf")
        self.llama_cpp_path = config.get("llama_cpp_path", "llama.cpp/main")
        self.interval = config.get("interval_seconds", 30)
        self.context_window = config.get("context_window", 50)
        self._running = False
        self._dream_count = 0
        self._llama_available = False
        
        logger.info("DreamerLocal initialized - requires llama.cpp integration")
        logger.info("Recommended: Use main Dreamer class with Ollama instead")
    
    async def run(self):
        """Main dream loop - placeholder for llama.cpp integration."""
        import asyncio
        self._running = True
        
        logger.warning(
            "DreamerLocal.run() called but llama.cpp integration not implemented. "
            "Use main Dreamer class with Ollama for full functionality."
        )
        
        while self._running:
            logger.debug("Dream #%d: Skipping - no LLM integration", self._dream_count)
            self._dream_count += 1
            await asyncio.sleep(self.interval)
    
    def stop(self):
        """Stop the dreamer."""
        self._running = False
        logger.info("DreamerLocal stop requested")

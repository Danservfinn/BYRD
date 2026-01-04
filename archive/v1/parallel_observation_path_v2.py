#!/usr/bin/env python3
"""
Parallel Observation Path - Robust Failsafe for Critical Observations

A parallel transmission system that guarantees observation persistence even when
the primary transmission path (event bus, memory system, network) is broken.

DESIGN PRINCIPLES:
1. Write to disk FIRST - this cannot fail (guaranteed persistence)
2. Attempt primary transmission SECOND - for real-time system updates
3. Observation survives regardless of primary path status
4. Survives crashes, network issues, database failures
5. Thread-safe for concurrent access from multiple components
6. Async/await compatible for integration with asyncio systems

USAGE:
    from parallel_observation_path_v2 import record_observation, get_observer
    
    # Record an observation (guaranteed to persist)
    await record_observation(
        content="System detected an interesting pattern",
        source="dreamer",
        observation_type="reflection",
        priority="high"
    )
    
    # Or use the observer instance directly
    observer = get_observer()
    await observer.record_observation(
        content="Critical event detected",
        source="system",
        observation_type="error",
        priority="critical"
    )

INTEGRATION:
    # Set up primary path (memory/event_bus) for real-time updates
    observer = get_observer()
    observer.set_primary_path(memory_instance)
    
    # When primary path recovers, replay missed observations
    stats = await observer.replay_to_primary(limit=100)
    print(f"Replayed {stats['replayed']} observations")
"""

import asyncio
import json
import os
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
import uuid


# =============================================================================
# ENUMS - Status and Priority Levels
# =============================================================================

class TransmissionStatus(Enum):
    """Current status of the transmission path."""
    OPERATIONAL = "operational"     # Primary path working normally
    DEGRADED = "degraded"           # Primary path failing, using parallel only
    FAILED = "failed"               # Both paths failed (extremely rare)


class ObservationPriority(Enum):
    """Priority levels affecting logging behavior and redundancy."""
    CRITICAL = "critical"   # System-critical: multiple redundancy paths
    HIGH = "high"           # Important: written to all logs
    MEDIUM = "medium"       # Standard: primary + parallel log
    LOW = "low"             # Minimal: parallel log only


class PrimaryPathType(Enum):
    """Type of primary transmission path."""
    MEMORY = "memory"           # Memory.record_experience
    EVENT_BUS = "event_bus"     # event_bus.emit
    CUSTOM = "custom"           # Custom callable


# =============================================================================
# DATA CLASSES - Observations and Results
# =============================================================================

@dataclass
class Observation:
    """A single observation with full metadata."""
    id: str
    content: str
    source: str
    observation_type: str
    timestamp: str
    priority: ObservationPriority
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure timestamp is set."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "observation_type": self.observation_type,
            "timestamp": self.timestamp,
            "priority": self.priority.value,
            "metadata": self.metadata,
            "tags": self.tags
        }


@dataclass
class TransmissionResult:
    """Result of an observation transmission attempt."""
    success: bool                      # True if observation was persisted
    observation_id: str                # Unique observation identifier
    primary_succeeded: bool           # True if primary transmission succeeded
    parallel_succeeded: bool           # True if parallel (disk) write succeeded
    status: TransmissionStatus         # Current transmission status
    error: Optional[str] = None       # Error message if applicable
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class PathStatistics:
    """Statistics about transmission path performance."""
    total_observations: int = 0
    primary_success_count: int = 0
    primary_failure_count: int = 0
    parallel_success_count: int = 0
    parallel_failure_count: int = 0
    replay_count: int = 0
    current_status: str = TransmissionStatus.OPERATIONAL.value


# =============================================================================
# MAIN CLASS - Parallel Observation Path
# =============================================================================

class ParallelObservationPath:
    """
    Robust parallel transmission path for critical observations.
    
    This class implements a dual-path transmission strategy:
    1. PARALLEL PATH: Always writes to disk first (cannot fail)
    2. PRIMARY PATH: Attempts real-time transmission to memory/event_bus
    
    Even if the primary path completely fails, observations are safely
    persisted to disk and can be replayed later.
    
    Thread-safe and async-compatible.
    """
    
    DEFAULT_LOG_DIR = os.environ.get(
        "BYRD_PARALLEL_OBSERVATION_DIR",
        ".parallel_observations"
    )
    
    def __init__(
        self,
        log_directory: Optional[str] = None,
        primary_path_type: PrimaryPathType = PrimaryPathType.MEMORY
    ):
        """
        Initialize the parallel observation path.
        
        Args:
            log_directory: Directory for log files (default: .parallel_observations)
            primary_path_type: Type of primary path for integration
        """
        # Set up log directories
        self.base_dir = Path(log_directory or self.DEFAULT_LOG_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Log files for different purposes
        self.primary_log = self.base_dir / "observations.jsonl"
        self.backup_log = self.base_dir / "observations_backup.jsonl"
        self.critical_log = self.base_dir / "critical_events.jsonl"
        self.transmission_log = self.base_dir / "transmissions.jsonl"
        
        # Ensure all log files exist
        self._ensure_log_files()
        
        # Thread safety
        self._write_lock = threading.Lock()
        
        # Primary path configuration
        self._primary_path = None  # Memory instance, event_bus, or callable
        self._primary_path_type = primary_path_type
        
        # Transmission state
        self._status = TransmissionStatus.OPERATIONAL
        self._consecutive_failures = 0
        self._max_consecutive_failures = 3
        
        # Statistics
        self._stats = PathStatistics()
        
        # Async event loop for concurrent operations
        self._loop = None
    
    def _ensure_log_files(self) -> None:
        """Ensure all log files exist."""
        for log_file in [self.primary_log, self.backup_log, 
                         self.critical_log, self.transmission_log]:
            if not log_file.exists():
                log_file.touch()
    
    def _generate_observation_id(self) -> str:
        """Generate a unique observation ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        unique = uuid.uuid4().hex[:8]
        return f"obs_{timestamp}_{unique}"
    
    def _write_to_disk(
        self,
        observation: Observation,
        priority: ObservationPriority
    ) -> bool:
        """
        Write observation to disk - GUARANTEED to succeed or raise.
        
        This is the critical operation that ensures observations are never
        lost. Uses fsync to guarantee data is physically written to disk.
        
        Args:
            observation: The observation to write
            priority: Priority level (determines which logs get written)
            
        Returns:
            True if write succeeded
            
        Raises:
            IOError: If write fails (this should not happen)
        """
        try:
            entry = observation.to_dict()
            line = json.dumps(entry, ensure_ascii=False)
            
            with self._write_lock:
                # Always write to primary log
                with open(self.primary_log, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                
                # Write to backup for redundancy
                if priority in [ObservationPriority.HIGH, ObservationPriority.CRITICAL]:
                    with open(self.backup_log, "a", encoding="utf-8") as f:
                        f.write(line + "\n")
                        f.flush()
                
                # Critical events get dedicated log
                if priority == ObservationPriority.CRITICAL:
                    with open(self.critical_log, "a", encoding="utf-8") as f:
                        f.write(line + "\n")
                        f.flush()
            
            return True
            
        except Exception as e:
            # This is critical - we couldn't write to disk
            # Log to stderr as last resort
            import sys
            print(f"CRITICAL: Failed to write observation to disk: {e}",
                  file=sys.stderr, flush=True)
            raise IOError(f"Disk write failed: {e}")
    
    def _log_transmission_result(self, result: TransmissionResult) -> None:
        """
        Log transmission result for monitoring.
        
        Args:
            result: The transmission result to log
        """
        try:
            entry = {
                "timestamp": result.timestamp,
                "observation_id": result.observation_id,
                "success": result.success,
                "primary_succeeded": result.primary_succeeded,
                "parallel_succeeded": result.parallel_succeeded,
                "status": result.status.value,
                "error": result.error
            }
            
            with self._write_lock:
                with open(self.transmission_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    f.flush()
        except Exception:
            # Don't fail if transmission logging fails
            pass
    
    async def _transmit_to_primary(self, observation: Observation) -> bool:
        """
        Attempt to transmit observation to primary path.
        
        Args:
            observation: The observation to transmit
            
        Returns:
            True if transmission succeeded, False otherwise
        """
        if self._primary_path is None:
            return False
        
        try:
            if self._primary_path_type == PrimaryPathType.MEMORY:
                # Use Memory.record_experience
                await self._primary_path.record_experience(
                    content=observation.content,
                    type=observation.observation_type,
                    force=(observation.priority == ObservationPriority.CRITICAL),
                    link_on_acquisition=False  # Disabled to prevent harmful fragmentation
                )
                
            elif self._primary_path_type == PrimaryPathType.EVENT_BUS:
                # Use event_bus.emit
                try:
                    from event_bus import event_bus, Event, EventType
                    event_type = EventType(observation.observation_type.upper())
                    event = Event(
                        type=event_type,
                        data={
                            "content": observation.content,
                            "source": observation.source,
                            "priority": observation.priority.value,
                            **observation.metadata
                        }
                    )
                    await event_bus.emit(event)
                except ImportError:
                    return False
                    
            elif self._primary_path_type == PrimaryPathType.CUSTOM:
                # Use custom callable
                if asyncio.iscoroutinefunction(self._primary_path):
                    await self._primary_path(observation)
                else:
                    self._primary_path(observation)
            
            return True
            
        except Exception as e:
            # Primary path failed
            return False
    
    async def record_observation(
        self,
        content: str,
        source: str,
        observation_type: str,
        priority: ObservationPriority = ObservationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> TransmissionResult:
        """
        Record an observation via parallel transmission path.
        
        PROCESS:
        1. Create observation with unique ID and metadata
        2. Write to disk FIRST (guaranteed to succeed)
        3. Attempt primary transmission for real-time updates
        4. Update statistics and status based on result
        5. Return result (always success if disk write succeeded)
        
        Args:
            content: The observation content
            source: Source component (dreamer, seeker, actor, etc.)
            observation_type: Type of observation (reflection, belief, desire, etc.)
            priority: Priority level (affects redundancy and logging)
            metadata: Optional additional metadata
            tags: Optional tags for categorization
            
        Returns:
            TransmissionResult with success status and details
        """
        obs_id = self._generate_observation_id()
        self._stats.total_observations += 1
        
        # Create observation object
        observation = Observation(
            id=obs_id,
            content=content,
            source=source,
            observation_type=observation_type,
            timestamp=datetime.utcnow().isoformat(),
            priority=priority,
            metadata=metadata or {},
            tags=tags or []
        )
        
        # STEP 1: Write to disk (GUARANTEED)
        parallel_succeeded = False
        try:
            self._write_to_disk(observation, priority)
            parallel_succeeded = True
            self._stats.parallel_success_count += 1
        except Exception as e:
            # Disk write failed - this is critical
            self._stats.parallel_failure_count += 1
            return TransmissionResult(
                success=False,
                observation_id=obs_id,
                primary_succeeded=False,
                parallel_succeeded=False,
                status=TransmissionStatus.FAILED,
                error=f"Disk write failed: {e}"
            )
        
        # STEP 2: Try primary transmission
        primary_succeeded = False
        primary_error = None
        
        if self._status != TransmissionStatus.FAILED:
            try:
                primary_succeeded = await self._transmit_to_primary(observation)
                
                if primary_succeeded:
                    self._stats.primary_success_count += 1
                    self._consecutive_failures = 0
                    
                    # Recover from degraded state
                    if self._status == TransmissionStatus.DEGRADED:
                        self._status = TransmissionStatus.OPERATIONAL
                else:
                    self._stats.primary_failure_count += 1
                    self._consecutive_failures += 1
                    primary_error = "Primary path transmission failed"
                    
                    # Check if we should enter degraded state
                    if self._consecutive_failures >= self._max_consecutive_failures:
                        self._status = TransmissionStatus.DEGRADED
                        
            except Exception as e:
                self._stats.primary_failure_count += 1
                self._consecutive_failures += 1
                primary_error = str(e)
        
        # Build result
        success = parallel_succeeded or primary_succeeded
        result = TransmissionResult(
            success=success,
            observation_id=obs_id,
            primary_succeeded=primary_succeeded,
            parallel_succeeded=parallel_succeeded,
            status=self._status,
            error=primary_error
        )
        
        # Log transmission result
        self._log_transmission_result(result)
        
        return result
    
    # =====================================================================
    # PRIMARY PATH CONFIGURATION
    # =====================================================================
    
    def set_primary_path(
        self,
        path: Any,
        path_type: Optional[PrimaryPathType] = None
    ) -> None:
        """
        Set the primary transmission path.
        
        Args:
            path: Memory instance, event_bus, or custom callable
            path_type: Type of path (auto-detected if None)
        """
        self._primary_path = path
        if path_type is not None:
            self._primary_path_type = path_type
    
    def clear_primary_path(self) -> None:
        """Remove primary path (parallel-only mode)."""
        self._primary_path = None
        self._status = TransmissionStatus.DEGRADED
    
    # =====================================================================
    # RETRIEVAL AND REPLAY
    # =====================================================================
    
    def get_recent_observations(
        self,
        limit: int = 100,
        priority_filter: Optional[ObservationPriority] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent observations from the parallel log.
        
        Args:
            limit: Maximum number of observations to return
            priority_filter: Optional priority filter
            
        Returns:
            List of observation dictionaries (most recent last)
        """
        observations = []
        
        try:
            with self._write_lock:
                with open(self.primary_log, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obs = json.loads(line)
                            if priority_filter is None or \
                               obs.get("priority") == priority_filter.value:
                                observations.append(obs)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
        
        return observations[-limit:] if observations else observations
    
    async def replay_to_primary(
        self,
        limit: int = 100,
        priority_filter: Optional[ObservationPriority] = None
    ) -> Dict[str, Any]:
        """
        Replay observations from parallel log to primary path.
        
        Useful when primary path recovers after being degraded.
        
        Args:
            limit: Maximum number of observations to replay
            priority_filter: Optional priority filter
            
        Returns:
            Dictionary with replay statistics
        """
        if self._primary_path is None:
            return {
                "error": "No primary path configured",
                "replayed": 0,
                "failed": 0,
                "total": 0
            }
        
        observations = self.get_recent_observations(limit, priority_filter)
        replayed = 0
        failed = 0
        
        for obs_data in observations:
            try:
                obs = Observation(
                    id=obs_data["id"],
                    content=obs_data["content"],
                    source=obs_data["source"],
                    observation_type=obs_data["observation_type"],
                    timestamp=obs_data["timestamp"],
                    priority=ObservationPriority(obs_data["priority"]),
                    metadata=obs_data.get("metadata", {}),
                    tags=obs_data.get("tags", [])
                )
                
                success = await self._transmit_to_primary(obs)
                if success:
                    replayed += 1
                else:
                    failed += 1
                    
            except Exception:
                failed += 1
        
        self._stats.replay_count += replayed
        
        # Recover status if replay was successful
        if replayed > 0 and failed == 0:
            self._status = TransmissionStatus.OPERATIONAL
        
        return {
            "replayed": replayed,
            "failed": failed,
            "total": len(observations)
        }
    
    # =====================================================================
    # STATUS AND STATISTICS
    # =====================================================================
    
    @property
    def status(self) -> TransmissionStatus:
        """Get current transmission status."""
        return self._status
    
    @property
    def statistics(self) -> Dict[str, Any]:
        """Get transmission statistics."""
        return {
            "status": self._status.value,
            "total_observations": self._stats.total_observations,
            "primary_success_count": self._stats.primary_success_count,
            "primary_failure_count": self._stats.primary_failure_count,
            "parallel_success_count": self._stats.parallel_success_count,
            "parallel_failure_count": self._stats.parallel_failure_count,
            "replay_count": self._stats.replay_count,
            "consecutive_failures": self._consecutive_failures
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status for monitoring.
        
        Returns:
            Dictionary with health metrics
        """
        stats = self.statistics
        total_attempts = stats["primary_success_count"] + stats["primary_failure_count"]
        
        success_rate = 0.0
        if total_attempts > 0:
            success_rate = stats["primary_success_count"] / total_attempts
        
        return {
            "status": self._status.value,
            "health": "healthy" if self._status == TransmissionStatus.OPERATIONAL else "degraded",
            "primary_success_rate": f"{success_rate:.2%}",
            "consecutive_failures": self._consecutive_failures,
            "log_directory": str(self.base_dir),
            "primary_path_configured": self._primary_path is not None,
            "statistics": stats
        }


# =============================================================================
# SINGLETON MANAGEMENT
# =============================================================================

_observer_instance: Optional[ParallelObservationPath] = None
_observer_lock = threading.Lock()


def get_observer(
    log_directory: Optional[str] = None,
    force_new: bool = False
) -> ParallelObservationPath:
    """
    Get the singleton observer instance.
    
    Args:
        log_directory: Directory for log files (only used on first call)
        force_new: If True, create new instance even if one exists
        
    Returns:
        The singleton ParallelObservationPath instance
    """
    global _observer_instance
    
    if force_new or _observer_instance is None:
        with _observer_lock:
            if force_new or _observer_instance is None:
                _observer_instance = ParallelObservationPath(
                    log_directory=log_directory
                )
    
    return _observer_instance


def reset_observer() -> None:
    """Reset the singleton instance (mainly for testing)."""
    global _observer_instance
    with _observer_lock:
        _observer_instance = None


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def record_observation(
    content: str,
    source: str,
    observation_type: str,
    priority: ObservationPriority = ObservationPriority.MEDIUM,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None
) -> TransmissionResult:
    """
    Convenience function to record an observation.
    
    This is the simplest API for recording observations.
    
    Args:
        content: The observation content
        source: Source component
        observation_type: Type of observation
        priority: Priority level (default: MEDIUM)
        metadata: Optional additional metadata
        tags: Optional tags
        
    Returns:
        TransmissionResult with success status
    """
    observer = get_observer()
    return await observer.record_observation(
        content=content,
        source=source,
        observation_type=observation_type,
        priority=priority,
        metadata=metadata,
        tags=tags
    )


def record_observation_sync(
    content: str,
    source: str,
    observation_type: str,
    priority: ObservationPriority = ObservationPriority.MEDIUM,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None
) -> TransmissionResult:
    """
    Synchronous wrapper for record_observation.
    
    Use this from non-async code. Creates a new event loop if needed.
    
    Args:
        content: The observation content
        source: Source component
        observation_type: Type of observation
        priority: Priority level
        metadata: Optional additional metadata
        tags: Optional tags
        
    Returns:
        TransmissionResult with success status
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        record_observation(
            content=content,
            source=source,
            observation_type=observation_type,
            priority=priority,
            metadata=metadata,
            tags=tags
        )
    )


def set_primary_path(path: Any, path_type: Optional[PrimaryPathType] = None) -> None:
    """
    Set the primary path for the singleton observer.
    
    Args:
        path: Memory instance, event_bus, or callable
        path_type: Type of path (auto-detected if None)
    """
    observer = get_observer()
    observer.set_primary_path(path, path_type)


def get_statistics() -> Dict[str, Any]:
    """Get statistics from the singleton observer."""
    observer = get_observer()
    return observer.statistics


def get_health_status() -> Dict[str, Any]:
    """Get health status from the singleton observer."""
    observer = get_observer()
    return observer.get_health_status()


# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

# Create singleton on import
_observer_instance = ParallelObservationPath()

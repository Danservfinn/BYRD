#!/usr/bin/env python3
"""
Parallel Transmission Path - Bypasses Broken Transmission

A simple, robust failsafe mechanism for recording observations when the
primary transmission path fails. This ensures critical events are never lost.

Design Principles:
1. Always write to disk first - this cannot fail
2. Try primary path (Memory/event_bus) second - for real-time updates
3. If primary fails, observation is already safely persisted
4. Observations survive crashes, network issues, and system failures

Usage:
    from parallel_transmission_path import get_transmission_path
    
    # Record an observation (guaranteed to persist)
    await get_transmission_path().record_observation(
        content="The system noticed something important",
        source="dreamer",
        observation_type="reflection"
    )
"""

import asyncio
import json
import os
import threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict, field
import uuid


class TransmissionStatus(Enum):
    """Status of the transmission path."""
    OPERATIONAL = "operational"  # Primary path working
    DEGRADED = "degraded"  # Using parallel path only
    FAILED = "failed"  # Both paths failed (rare)


class ObservationPriority(Enum):
    """Priority levels for observations."""
    CRITICAL = "critical"  # System-critical events
    HIGH = "high"  # Important reflections
    MEDIUM = "medium"  # Routine observations
    LOW = "low"  # Noise/logging


@dataclass
class Observation:
    """A single observation with metadata."""
    id: str
    content: str
    source: str
    observation_type: str
    timestamp: str
    priority: ObservationPriority
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert observation to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "observation_type": self.observation_type,
            "timestamp": self.timestamp,
            "priority": self.priority.value,
            "metadata": self.metadata
        }


@dataclass
class TransmissionResult:
    """Result of a transmission attempt."""
    success: bool
    observation_id: str
    primary_succeeded: bool
    parallel_succeeded: bool
    status: TransmissionStatus
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ParallelTransmissionPath:
    """
    Parallel transmission path that guarantees observation persistence.
    
    This class implements a dual-path strategy:
    1. Parallel path: Write to disk immediately (cannot fail or crashes system)
    2. Primary path: Try to send to Memory/event_bus for real-time updates
    
    Even if the primary path fails completely, observations are preserved.
    """
    
    def __init__(self, log_directory: Optional[str] = None):
        # Set up log directories
        self.base_dir = Path(log_directory or ".parallel_transmission")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Observation log file
        self.observation_log = self.base_dir / "observations.jsonl"
        
        # Critical events get separate log
        self.critical_log = self.base_dir / "critical_events.jsonl"
        
        # Transmission log for monitoring
        self.transmission_log = self.base_dir / "transmissions.jsonl"
        
        # Ensure log files exist
        self._ensure_log_files()
        
        # Thread lock for disk writes
        self._write_lock = threading.Lock()
        
        # Primary path (Memory instance)
        self._memory = None
        
        # Statistics
        self._total_observations = 0
        self._primary_success_count = 0
        self._parallel_success_count = 0
        self._primary_failure_count = 0
        
        # Current status
        self._status = TransmissionStatus.OPERATIONAL
    
    def _ensure_log_files(self) -> None:
        """Ensure all log files exist."""
        for log_file in [self.observation_log, self.critical_log, self.transmission_log]:
            if not log_file.exists():
                log_file.touch()
    
    def set_memory(self, memory) -> None:
        """Set the primary memory instance for transmission."""
        self._memory = memory
    
    @property
    def status(self) -> TransmissionStatus:
        """Get current transmission status."""
        return self._status
    
    @property
    def statistics(self) -> Dict[str, Any]:
        """Get transmission statistics."""
        return {
            "status": self._status.value,
            "total_observations": self._total_observations,
            "primary_success_count": self._primary_success_count,
            "parallel_success_count": self._parallel_success_count,
            "primary_failure_count": self._primary_failure_count,
            "success_rate": (
                self._primary_success_count / self._total_observations
                if self._total_observations > 0 else 1.0
            )
        }
    
    def _generate_observation_id(self) -> str:
        """Generate a unique observation ID."""
        return f"obs_{uuid.uuid4().hex[:16]}"
    
    def _write_to_disk(self, observation: Observation) -> bool:
        """
        Write observation to disk immediately.
        
        This is the guaranteed path that cannot fail (or crashes the system).
        Critical observations go to a separate log file.
        """
        try:
            log_path = (
                self.critical_log
                if observation.priority == ObservationPriority.CRITICAL
                else self.observation_log
            )
            
            with self._write_lock:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(observation.to_dict()) + "\n")
            
            return True
        except Exception as e:
            # If we can't write to disk, we have a serious problem
            # Try stderr as last resort
            import sys
            print(f"CRITICAL: Failed to write observation to disk: {e}", file=sys.stderr)
            return False
    
    def _log_transmission_result(self, result: TransmissionResult) -> None:
        """Log transmission result to transmission log."""
        try:
            with self._write_lock:
                with open(self.transmission_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "timestamp": result.timestamp,
                        "observation_id": result.observation_id,
                        "success": result.success,
                        "primary_succeeded": result.primary_succeeded,
                        "parallel_succeeded": result.parallel_succeeded,
                        "status": result.status.value,
                        "error": result.error
                    }) + "\n")
        except Exception:
            pass  # Don't fail if logging fails
    
    async def record_observation(
        self,
        content: str,
        source: str,
        observation_type: str,
        priority: ObservationPriority = ObservationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TransmissionResult:
        """
        Record an observation via parallel transmission path.
        
        Process:
        1. Write to disk immediately (guaranteed to succeed)
        2. Try primary path (Memory.record_experience)
        3. Return result regardless of primary path success
        
        Args:
            content: Observation content
            source: Source component (dreamer, seeker, etc.)
            observation_type: Type of observation
            priority: Priority level (affects logging behavior)
            metadata: Optional additional metadata
            
        Returns:
            TransmissionResult with success status and details
        """
        obs_id = self._generate_observation_id()
        self._total_observations += 1
        
        # Create observation
        observation = Observation(
            id=obs_id,
            content=content,
            source=source,
            observation_type=observation_type,
            timestamp=datetime.utcnow().isoformat(),
            priority=priority,
            metadata=metadata or {}
        )
        
        # Step 1: Write to disk (guaranteed)
        parallel_succeeded = self._write_to_disk(observation)
        
        if not parallel_succeeded:
            # This is critical - we couldn't write to disk
            return TransmissionResult(
                success=False,
                observation_id=obs_id,
                primary_succeeded=False,
                parallel_succeeded=False,
                status=TransmissionStatus.FAILED,
                error="Failed to write to disk"
            )
        
        self._parallel_success_count += 1
        
        # Step 2: Try primary path
        primary_succeeded = False
        primary_error = None
        
        if self._memory is not None and self._status != TransmissionStatus.FAILED:
            try:
                # Try to record to primary memory
                await self._memory.record_experience(
                    content=content,
                    type=observation_type,
                    force=priority == ObservationPriority.CRITICAL,
                    link_on_acquisition=True
                )
                primary_succeeded = True
                self._primary_success_count += 1
                self._primary_failure_count = 0  # Reset failure counter
                
                # If we were degraded, we're now operational
                if self._status == TransmissionStatus.DEGRADED:
                    self._status = TransmissionStatus.OPERATIONAL
                    
            except Exception as e:
                primary_error = str(e)
                self._primary_failure_count += 1
                
                # If we fail 3 times in a row, mark as degraded
                if self._primary_failure_count >= 3:
                    self._status = TransmissionStatus.DEGRADED
        
        # Build result
        success = primary_succeeded or parallel_succeeded
        status = self._status
        
        result = TransmissionResult(
            success=success,
            observation_id=obs_id,
            primary_succeeded=primary_succeeded,
            parallel_succeeded=parallel_succeeded,
            status=status,
            error=primary_error
        )
        
        # Log transmission result
        self._log_transmission_result(result)
        
        return result
    
    def get_recent_transmissions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent transmission log entries."""
        transmissions = []
        
        if not self.transmission_log.exists():
            return transmissions
        
        try:
            with open(self.transmission_log, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        transmissions.append(json.loads(line))
        except Exception:
            pass
        
        return transmissions[-limit:] if transmissions else transmissions
    
    def get_recent_observations(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent observations from the log."""
        observations = []
        
        for log_file in [self.observation_log, self.critical_log]:
            if not log_file.exists():
                continue
            
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            observations.append(json.loads(line))
            except Exception:
                pass
        
        # Sort by timestamp and return most recent
        observations.sort(key=lambda x: x.get("timestamp", ""))
        return observations[-limit:] if observations else observations
    
    async def replay_to_primary(self, limit: int = 100) -> Dict[str, Any]:
        """
        Replay observations from parallel log to primary memory.
        
        Useful when primary path recovers after being degraded.
        
        Args:
            limit: Maximum number of observations to replay
            
        Returns:
            Dictionary with replay statistics
        """
        if self._memory is None:
            return {"error": "No primary memory set", "replayed": 0}
        
        observations = self.get_recent_observations(limit)
        replayed = 0
        failed = 0
        
        for obs in observations:
            try:
                await self._memory.record_experience(
                    content=obs["content"],
                    type=obs["observation_type"],
                    link_on_acquisition=True
                )
                replayed += 1
            except Exception:
                failed += 1
        
        return {"replayed": replayed, "failed": failed, "total": len(observations)}


# Singleton instance
_transmission_path: Optional[ParallelTransmissionPath] = None
_transmission_lock = threading.Lock()


def get_transmission_path(log_directory: Optional[str] = None) -> ParallelTransmissionPath:
    """Get the singleton transmission path instance."""
    global _transmission_path
    
    if _transmission_path is None:
        with _transmission_lock:
            if _transmission_path is None:
                _transmission_path = ParallelTransmissionPath(log_directory)
    
    return _transmission_path


def reset_transmission_path() -> None:
    """Reset the singleton instance (mainly for testing)."""
    global _transmission_path
    with _transmission_lock:
        _transmission_path = None


# Convenience functions for synchronous recording
def record_observation_sync(
    content: str,
    source: str,
    observation_type: str,
    priority: ObservationPriority = ObservationPriority.MEDIUM,
    metadata: Optional[Dict[str, Any]] = None
) -> TransmissionResult:
    """Synchronous wrapper for recording observations."""
    async def _record():
        return await get_transmission_path().record_observation(
            content=content,
            source=source,
            observation_type=observation_type,
            priority=priority,
            metadata=metadata
        )
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is running, we can't do sync properly
            # Create a new observation directly to disk
            obs_id = f"obs_{uuid.uuid4().hex[:16]}"
            observation = Observation(
                id=obs_id,
                content=content,
                source=source,
                observation_type=observation_type,
                timestamp=datetime.utcnow().isoformat(),
                priority=priority,
                metadata=metadata or {}
            )
            path = get_transmission_path()
            parallel_succeeded = path._write_to_disk(observation)
            return TransmissionResult(
                success=parallel_succeeded,
                observation_id=obs_id,
                primary_succeeded=False,
                parallel_succeeded=parallel_succeeded,
                status=path.status,
                error="Synchronous call - primary path skipped"
            )
        else:
            return loop.run_until_complete(_record())
    except RuntimeError:
        # No event loop - write directly
        obs_id = f"obs_{uuid.uuid4().hex[:16]}"
        observation = Observation(
            id=obs_id,
            content=content,
            source=source,
            observation_type=observation_type,
            timestamp=datetime.utcnow().isoformat(),
            priority=priority,
            metadata=metadata or {}
        )
        path = get_transmission_path()
        parallel_succeeded = path._write_to_disk(observation)
        return TransmissionResult(
            success=parallel_succeeded,
            observation_id=obs_id,
            primary_succeeded=False,
            parallel_succeeded=parallel_succeeded,
            status=path.status,
            error="No event loop - primary path skipped"
        )


if __name__ == "__main__":
    # Simple test
    import sys
    
    async def test():
        path = get_transmission_path()
        
        print("Testing parallel transmission path...")
        
        # Test recording
        result = await path.record_observation(
            content="Test observation from parallel path",
            source="test",
            observation_type="test",
            priority=ObservationPriority.HIGH
        )
        
        print(f"Result: {result}")
        print(f"Statistics: {path.statistics}")
        
        # Test synchronous recording
        result_sync = record_observation_sync(
            content="Sync test observation",
            source="test",
            observation_type="test"
        )
        print(f"Sync result: {result_sync}")
        
        print("\nTest completed!")
    
    asyncio.run(test())

#!/usr/bin/env python3
"""
Parallel Observation Path

A redundant transmission system for observations that bypasses broken
transmission paths in the main event bus system.

This module provides a failsafe mechanism for recording observations
even when the primary transmission channel (event_bus) is experiencing
issues, network failures, or other interruptions.

Design Principles:
1. Observations are written to disk immediately - this cannot fail
2. Multiple parallel paths ensure redundancy
3. Transmission failures are logged for later recovery
4. Observations survive crashes, network issues, and system failures
5. Critical observations are prioritized and receive additional redundancy

Usage:
    from parallel_observation_path import record_observation
    
    # Record an observation (guaranteed to persist)
    await record_observation(
        content="The system noticed an interesting pattern",
        source="dreamer",
        priority="medium"
    )
"""

import asyncio
import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import threading
from pathlib import Path


class ObservationPriority(Enum):
    """Priority levels for observations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NOISE = "noise"


class TransmissionStatus(Enum):
    """Status of transmission attempts."""
    SUCCESS = "success"
    FAILED_PRIMARY = "failed_primary"
    FAILED_ALL = "failed_all"
    PARALLEL_ONLY = "parallel_only"


@dataclass
class Observation:
    """A single observation with metadata."""
    id: str
    content: str
    source: str
    timestamp: datetime
    priority: ObservationPriority
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransmissionResult:
    """Result of an observation transmission attempt."""
    observation_id: str
    primary_success: bool
    parallel_success: bool
    transmission_time_ms: float
    status: TransmissionStatus
    error_message: Optional[str] = None


@dataclass
class PathStatistics:
    """Statistics about the observation path."""
    total_observations: int = 0
    primary_successes: int = 0
    primary_failures: int = 0
    parallel_writes: int = 0
    critical_observations: int = 0
    recovery_candidates: int = 0
    last_transmission_time: Optional[datetime] = None


class ParallelObservationPath:
    """
    Redundant transmission path for observations.
    
    Ensures observations are never lost by:
    1. Writing to primary parallel log immediately
    2. Maintaining a backup log for redundancy
    3. Attempting event_bus transmission for real-time updates
    4. Logging all transmission outcomes
    """
    
    DEFAULT_LOG_DIR = os.environ.get(
        "BYRD_OBSERVATION_LOG_DIR", 
        os.path.join("logs", "observations")
    )
    
    def __init__(self, log_dir: Optional[str] = None):
        """Initialize the parallel observation path."""
        self.log_dir = log_dir or self.DEFAULT_LOG_DIR
        
        self.primary_log_path = os.path.join(self.log_dir, "observations.log")
        self.backup_log_path = os.path.join(self.log_dir, "observations_backup.log")
        self.critical_log_path = os.path.join(self.log_dir, "critical_observations.log")
        self.transmission_log_path = os.path.join(self.log_dir, "transmission_status.log")
        
        os.makedirs(self.log_dir, exist_ok=True)
        
        self._write_lock = threading.Lock()
        self._stats = PathStatistics()
        self._event_bus = None
        
    def set_event_bus(self, event_bus):
        """Set the event bus for primary transmission attempts."""
        self._event_bus = event_bus
    
    def _generate_observation_id(self) -> str:
        """Generate a unique observation ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"obs_{timestamp}"
    
    def _write_to_log(
        self, 
        log_path: str, 
        entry: Dict[str, Any]
    ) -> bool:
        """Write an entry to a log file."""
        try:
            with self._write_lock:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    f.flush()
            return True
        except Exception:
            return False
    
    def _log_transmission(
        self, 
        result: TransmissionResult, 
        observation: Observation
    ):
        """Log the result of a transmission attempt."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "observation_id": observation.id,
            "observation_source": observation.source,
            "observation_priority": observation.priority.value,
            "content_sample": observation.content[:100] + "..." if len(observation.content) > 100 else observation.content,
            "primary_success": result.primary_success,
            "parallel_success": result.parallel_success,
            "transmission_time_ms": result.transmission_time_ms,
            "status": result.status.value,
            "error_message": result.error_message
        }
        self._write_to_log(self.transmission_log_path, entry)
    
    def _write_observation_to_parallel_paths(
        self, 
        observation: Observation
    ) -> List[bool]:
        """Write observation to all parallel paths."""
        entry = {
            "id": observation.id,
            "timestamp": observation.timestamp.isoformat(),
            "content": observation.content,
            "source": observation.source,
            "priority": observation.priority.value,
            "tags": observation.tags,
            "metadata": observation.metadata
        }
        
        results = []
        results.append(self._write_to_log(self.primary_log_path, entry))
        results.append(self._write_to_log(self.backup_log_path, entry))
        
        if observation.priority == ObservationPriority.CRITICAL:
            results.append(self._write_to_log(self.critical_log_path, entry))
            self._stats.critical_observations += 1
        
        self._stats.parallel_writes += 1
        return results
    
    async def _attempt_primary_transmission(
        self, 
        observation: Observation
    ) -> bool:
        """Attempt transmission via the primary event bus."""
        if self._event_bus is None:
            return False
        
        try:
            from event_bus import Event, EventType
            event = Event(
                type=EventType.REFLECTION_TEXT if observation.source == "dreamer" else EventType.EXPERIENCE_CREATED,
                data={
                    "observation_id": observation.id,
                    "content": observation.content,
                    "source": observation.source,
                    "priority": observation.priority.value,
                    "tags": observation.tags
                }
            )
            await self._event_bus.emit(event)
            return True
        except Exception:
            return False
    
    async def record_observation(
        self,
        content: str,
        source: str,
        priority: str = "medium",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TransmissionResult:
        """
        Record an observation via the parallel transmission path.
        
        This guarantees that the observation will be persisted even if
        the primary transmission system is broken.
        
        Args:
            content: The observation content
            source: Source of the observation
            priority: Priority level ("critical", "high", "medium", "low")
            tags: Optional list of tags for categorization
            metadata: Optional additional metadata
            
        Returns:
            TransmissionResult with details of the transmission attempt
        """
        start_time = datetime.now()
        
        observation = Observation(
            id=self._generate_observation_id(),
            content=content,
            source=source,
            timestamp=start_time,
            priority=ObservationPriority(priority.lower()),
            tags=tags or [],
            metadata=metadata or {}
        )
        
        parallel_successes = self._write_observation_to_parallel_paths(observation)
        parallel_success = all(parallel_successes)
        
        primary_success = await self._attempt_primary_transmission(observation)
        
        transmission_time = (datetime.now() - start_time).total_seconds() * 1000
        
        if primary_success and parallel_success:
            status = TransmissionStatus.SUCCESS
            self._stats.primary_successes += 1
        elif not primary_success and parallel_success:
            status = TransmissionStatus.FAILED_PRIMARY
            self._stats.primary_failures += 1
        elif not primary_success and not parallel_success:
            status = TransmissionStatus.FAILED_ALL
        else:
            status = TransmissionStatus.PARALLEL_ONLY
        
        result = TransmissionResult(
            observation_id=observation.id,
            primary_success=primary_success,
            parallel_success=parallel_success,
            transmission_time_ms=transmission_time,
            status=status
        )
        
        self._log_transmission(result, observation)
        self._stats.total_observations += 1
        self._stats.last_transmission_time = datetime.now()
        
        return result
    
    async def record_critical_observation(
        self,
        content: str,
        source: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TransmissionResult:
        """Record a critical observation with maximum redundancy."""
        return await self.record_observation(
            content=content,
            source=source,
            priority="critical",
            tags=tags or ["CRITICAL"],
            metadata=metadata or {}
        )
    
    def get_statistics(self) -> PathStatistics:
        """Get current statistics about the observation path."""
        return self._stats
    
    async def recover_observations(
        self,
        since: Optional[datetime] = None
    ) -> List[Observation]:
        """
        Recover observations from the parallel logs.
        
        Args:
            since: Optional timestamp to filter observations
            
        Returns:
            List of recovered observations
        """
        observations = []
        
        try:
            with open(self.primary_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                        obs_timestamp = datetime.fromisoformat(entry["timestamp"])
                        
                        if since and obs_timestamp < since:
                            continue
                        
                        observation = Observation(
                            id=entry["id"],
                            content=entry["content"],
                            source=entry["source"],
                            timestamp=obs_timestamp,
                            priority=ObservationPriority(entry["priority"]),
                            tags=entry.get("tags", []),
                            metadata=entry.get("metadata", {})
                        )
                        observations.append(observation)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except FileNotFoundError:
            pass
        
        self._stats.recovery_candidates = len(observations)
        return observations
    
    async def replay_to_event_bus(
        self,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Replay recovered observations to the event bus.
        
        Args:
            since: Optional timestamp to filter observations
            limit: Maximum number of observations to replay
            
        Returns:
            Dictionary with replay statistics
        """
        if self._event_bus is None:
            return {"error": "No event bus configured"}
        
        observations = await self.recover_observations(since=since)
        observations = observations[:limit]
        
        success_count = 0
        failure_count = 0
        
        for observation in observations:
            try:
                success = await self._attempt_primary_transmission(observation)
                if success:
                    success_count += 1
                else:
                    failure_count += 1
            except Exception:
                failure_count += 1
        
        return {
            "total_recovered": len(observations),
            "success_count": success_count,
            "failure_count": failure_count,
            "replay_time": datetime.now().isoformat()
        }
    
    def _count_lines(self, filepath: str) -> int:
        """Count lines in a file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except FileNotFoundError:
            return 0


# Global instance for easy access
_global_path: Optional[ParallelObservationPath] = None


def get_parallel_observation_path() -> ParallelObservationPath:
    """Get the global parallel observation path instance."""
    global _global_path
    if _global_path is None:
        _global_path = ParallelObservationPath()
    return _global_path


def configure_parallel_observation_path(
    log_dir: Optional[str] = None,
    event_bus: Optional[Any] = None
) -> ParallelObservationPath:
    """Configure the global parallel observation path."""
    global _global_path
    _global_path = ParallelObservationPath(log_dir=log_dir)
    if event_bus:
        _global_path.set_event_bus(event_bus)
    return _global_path


# Convenience functions for quick usage

async def record_observation(
    content: str,
    source: str,
    priority: str = "medium",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> TransmissionResult:
    """Record an observation using the global parallel path."""
    path = get_parallel_observation_path()
    return await path.record_observation(
        content=content,
        source=source,
        priority=priority,
        tags=tags,
        metadata=metadata
    )


async def record_critical_observation(
    content: str,
    source: str,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> TransmissionResult:
    """Record a critical observation using the global parallel path."""
    path = get_parallel_observation_path()
    return await path.record_critical_observation(
        content=content,
        source=source,
        tags=tags,
        metadata=metadata
    )

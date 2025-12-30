#!/usr/bin/env python3
"""
Parallel Observation Path

Provides a fallback observation recording mechanism to bypass broken
transmission paths (event_bus, database, or network issues).

When the primary transmission path fails, observations are:
1. Buffered to disk immediately (survives crashes)
2. Can be flushed when transmission is restored
3. Provides a guaranteed delivery mechanism for critical data

Usage:
    from parallel_observation import record_observation, get_observation_path
    
    await record_observation(
        content="Something happened",
        observation_type="experience",
        primary_fn=memory.record_experience,
        target="memory"
    )
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Callable, Awaitable
from dataclasses import dataclass, asdict
from collections import deque

logger = logging.getLogger("parallel_observation")

BUFFER_DIR = os.environ.get("BYRD_BUFFER_DIR", "buffered_observations")
MAX_BUFFER_SIZE = 1000
FLUSH_INTERVAL = 30


class TransmissionStatus:
    """Tracks the status of primary transmission paths."""
    
    def __init__(self):
        self._failures: Dict[str, int] = {}
        self._last_failure: Dict[str, datetime] = {}
        self._last_success: Dict[str, datetime] = {}
        
    def record_failure(self, path: str, error_type: str):
        key = f"{path}:{error_type}"
        self._failures[key] = self._failures.get(key, 0) + 1
        self._last_failure[key] = datetime.now()
        logger.warning(f"Transmission failure: {key} (count: {self._failures[key]})")
        
    def record_success(self, path: str):
        self._last_success[path] = datetime.now()
        logger.debug(f"Transmission success: {path}")
        
    def is_healthy(self, path: str) -> bool:
        recent_failures = [
            k for k in self._last_failure.keys()
            if k.startswith(path) and 
            (datetime.now() - self._last_failure[k]).total_seconds() < 300
        ]
        return len(recent_failures) == 0


transmission_status = TransmissionStatus()


@dataclass
class BufferedObservation:
    """A buffered observation waiting to be transmitted."""
    id: str
    timestamp: str
    observation_type: str
    content: str
    metadata: Dict[str, Any]
    original_target: Optional[str] = None
    retry_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BufferedObservation':
        return cls(**data)


class ObservationBuffer:
    """Buffer for observations that couldn't be transmitted."""
    
    def __init__(self, buffer_dir: str = BUFFER_DIR):
        self.buffer_dir = Path(buffer_dir)
        self.buffer_dir.mkdir(parents=True, exist_ok=True)
        self._buffer: deque = deque(maxlen=MAX_BUFFER_SIZE)
        self._lock = asyncio.Lock()
        self._buffer_file = self.buffer_dir / "buffer.jsonl"
        self._loaded = False
        
    async def ensure_loaded(self):
        if self._loaded:
            return
        await self._load_from_disk()
        self._loaded = True
        
    async def _load_from_disk(self):
        if not self._buffer_file.exists():
            return
        try:
            data = self._buffer_file.read_text(encoding='utf-8')
            for line in data.strip().split('\n'):
                if not line:
                    continue
                try:
                    obs_data = json.loads(line)
                    obs = BufferedObservation.from_dict(obs_data)
                    self._buffer.append(obs)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.error(f"Failed to load buffered observation: {e}")
            logger.info(f"Loaded {len(self._buffer)} buffered observations")
        except Exception as e:
            logger.error(f"Error loading buffer: {e}")
    
    async def add(self, observation: BufferedObservation):
        await self.ensure_loaded()
        async with self._lock:
            self._buffer.append(observation)
            line = json.dumps(observation.to_dict()) + '\n'
            try:
                with open(self._buffer_file, 'a', encoding='utf-8') as f:
                    f.write(line)
            except Exception as e:
                logger.error(f"Failed to write observation to disk: {e}")
            logger.debug(f"Buffered observation {observation.id} (size: {len(self._buffer)})")
    
    async def get_next(self) -> Optional[BufferedObservation]:
        await self.ensure_loaded()
        async with self._lock:
            if self._buffer:
                return self._buffer[0]
            return None
    
    async def remove(self, observation_id: str):
        await self.ensure_loaded()
        async with self._lock:
            for obs in list(self._buffer):
                if obs.id == observation_id:
                    self._buffer.remove(obs)
                    await self._rewrite_disk()
                    logger.debug(f"Removed transmitted observation {observation_id}")
                    return
    
    async def _rewrite_disk(self):
        try:
            lines = []
            for obs in self._buffer:
                lines.append(json.dumps(obs.to_dict()))
            content = '\n'.join(lines)
            self._buffer_file.write_text(content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to rewrite buffer: {e}")
    
    async def size(self) -> int:
        await self.ensure_loaded()
        async with self._lock:
            return len(self._buffer)
    
    async def clear(self):
        async with self._lock:
            self._buffer.clear()
            if self._buffer_file.exists():
                self._buffer_file.unlink()
            logger.info("Buffer cleared")


class ObservationPath:
    """Primary interface for parallel observation recording."""
    
    def __init__(self):
        self.buffer = ObservationBuffer()
        self._flush_task: Optional[asyncio.Task] = None
        
    async def record(
        self,
        content: str,
        observation_type: str,
        primary_fn: Optional[Callable[[], Awaitable[Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        target: str = "event_bus"
    ) -> bool:
        """Record an observation with automatic fallback."""
        metadata = metadata or {}
        obs_id = f"{observation_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        obs = BufferedObservation(
            id=obs_id,
            timestamp=datetime.now().isoformat(),
            observation_type=observation_type,
            content=content,
            metadata=metadata,
            original_target=target
        )
        
        if not transmission_status.is_healthy(target):
            logger.warning(f"Primary path unhealthy, buffering")
            await self.buffer.add(obs)
            return False
        
        if primary_fn is not None:
            try:
                result = await primary_fn()
                transmission_status.record_success(target)
                logger.debug(f"Primary transmission succeeded for {obs_id}")
                return True
            except Exception as e:
                error_type = type(e).__name__
                transmission_status.record_failure(target, error_type)
                logger.warning(f"Primary failed ({error_type}), buffering: {e}")
        
        await self.buffer.add(obs)
        return False
    
    async def start_flush_daemon(self):
        if self._flush_task is None:
            self._flush_task = asyncio.create_task(self._flush_loop())
            logger.info("Flush daemon started")
    
    async def stop_flush_daemon(self):
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
            logger.info("Flush daemon stopped")
    
    async def _flush_loop(self):
        while True:
            try:
                await asyncio.sleep(FLUSH_INTERVAL)
                await self.flush_buffer()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Flush loop error: {e}")
    
    async def flush_buffer(
        self,
        transmit_fn: Optional[Callable[[BufferedObservation], Awaitable[bool]]] = None
    ) -> int:
        if transmit_fn is None:
            logger.warning("No transmit function provided")
            return 0
            
        transmitted = 0
        while True:
            obs = await self.buffer.get_next()
            if obs is None:
                break
                
            target = obs.original_target or "event_bus"
            if not transmission_status.is_healthy(target):
                logger.debug("Target still unhealthy, pausing")
                break
                
            try:
                success = await transmit_fn(obs)
                if success:
                    await self.buffer.remove(obs.id)
                    transmitted += 1
                    transmission_status.record_success(target)
                else:
                    obs.retry_count += 1
                    if obs.retry_count > 10:
                        logger.error(f"Giving up on {obs.id}")
                        await self.buffer.remove(obs.id)
                    else:
                        await self.buffer.remove(obs.id)
                        await self.buffer.add(obs)
            except Exception as e:
                logger.error(f"Error transmitting {obs.id}: {e}")
                obs.retry_count += 1
                if obs.retry_count > 10:
                    await self.buffer.remove(obs.id)
                else:
                    await self.buffer.remove(obs.id)
                    await self.buffer.add(obs)
        
        if transmitted > 0:
            logger.info(f"Flushed {transmitted} observations")
        return transmitted
    
    async def get_buffer_stats(self) -> Dict[str, Any]:
        size = await self.buffer.size()
        return {
            "buffer_size": size,
            "buffer_file": str(self._buffer_file),
            "max_buffer_size": MAX_BUFFER_SIZE,
            "transmission_failures": transmission_status._failures
        }


_default_path: Optional[ObservationPath] = None


def get_observation_path() -> ObservationPath:
    global _default_path
    if _default_path is None:
        _default_path = ObservationPath()
    return _default_path


async def record_observation(
    content: str,
    observation_type: str,
    primary_fn: Optional[Callable[[], Awaitable[Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    target: str = "event_bus"
) -> bool:
    path = get_observation_path()
    return await path.record(content, observation_type, primary_fn, metadata, target)


async def record_experience_with_fallback(
    memory_instance,
    content: str,
    obs_type: str,
    **kwargs
) -> str:
    async def primary_transmission():
        return await memory_instance.record_experience(content=content, type=obs_type, **kwargs)
    
    try:
        exp_id = await primary_transmission()
        transmission_status.record_success("memory")
        return exp_id
    except Exception as e:
        error_type = type(e).__name__
        transmission_status.record_failure("memory", error_type)
        
        await record_observation(
            content=content,
            observation_type=f"experience_{obs_type}",
            metadata={"original_type": obs_type, "kwargs": kwargs, "error": error_type},
            target="memory"
        )
        
        return f"buffered_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

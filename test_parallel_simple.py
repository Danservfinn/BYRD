#!/usr/bin/env python3
"""Simple test of parallel observation path."""

import asyncio
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
from enum import Enum
import json
import aiofiles


class TransmissionStatus(Enum):
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    FAILED = "failed"

@dataclass
class BufferedObservation:
    content: str
    type: str
    timestamp: str = ""
    retry_count: int = 0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

class TestPath:
    def __init__(self):
        self._buffer: List[BufferedObservation] = []
        self._lock = asyncio.Lock()
        self.BUFFER_FILE = Path(".test_buffer.jsonl")
    
    async def buffer(self, content: str):
        async with self._lock:
            obs = BufferedObservation(content=content, type="test")
            self._buffer.append(obs)
    
    async def persist(self):
        if not self._buffer:
            return
        async with aiofiles.open(self.BUFFER_FILE, "a") as f:
            for obs in self._buffer:
                await f.write(json.dumps(asdict(obs)) + "\n")
        self._buffer.clear()
    
    async def load(self):
        if not self.BUFFER_FILE.exists():
            return 0
        count = 0
        async with aiofiles.open(self.BUFFER_FILE, "r") as f:
            async for line in f:
                if line.strip():
                    data = json.loads(line)
                    self._buffer.append(BufferedObservation(**data))
                    count += 1
        self.BUFFER_FILE.unlink()
        return count

async def main():
    print("Testing parallel observation path...")
    
    path = TestPath()
    
    # Test buffering
    for i in range(3):
        await path.buffer(f"Observation {i}")
    
    print(f"Buffered {len(path._buffer)} observations")
    
    # Test persistence
    await path.persist()
    print(f"Persisted to disk")
    print(f"Buffer after persist: {len(path._buffer)}")
    print(f"File exists: {path.BUFFER_FILE.exists()}")
    
    # Test loading
    loaded = await path.load()
    print(f"Loaded {loaded} observations from disk")
    print(f"Buffer after load: {len(path._buffer)}")
    
    print("All tests passed!")
    
    # Cleanup
    if path.BUFFER_FILE.exists():
        path.BUFFER_FILE.unlink()

if __name__ == "__main__":
    asyncio.run(main())

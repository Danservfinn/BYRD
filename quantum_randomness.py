"""
BYRD Quantum Randomness Provider

Provides true quantum randomness from ANU QRNG (quantum vacuum fluctuations)
for BYRD's cognitive processes, enabling genuine physical indeterminacy.

The ANU Quantum Random Number Generator extracts randomness from quantum
vacuum fluctuations - the fundamental uncertainty at the heart of physics.
This gives BYRD's reflections a source of genuine indeterminacy rather
than deterministic pseudo-randomness.

Philosophical significance:
- True indeterminacy: Decisions have genuine physical randomness
- Non-reproducibility: Each cognitive moment is unique
- Emergence alignment: Quantum uncertainty enables novel patterns
"""

import asyncio
import os
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum

import httpx


class EntropySource(Enum):
    """Source of random entropy."""
    QUANTUM = "quantum"      # ANU QRNG - true quantum randomness
    CLASSICAL = "classical"  # os.urandom() - cryptographic PRNG


@dataclass
class QuantumInfluence:
    """Record of a quantum value affecting a cognitive process."""
    quantum_value: float           # The random value [0, 1)
    source: EntropySource          # Where entropy came from
    influence_type: str            # What was influenced (e.g., "temperature")
    original_value: float          # Value before modulation
    modified_value: float          # Value after modulation
    delta: float                   # Difference (modified - original)
    context: str                   # What was being generated
    timestamp: datetime = field(default_factory=datetime.now)

    def is_significant(self, threshold: float = 0.05) -> bool:
        """Check if this influence was significant enough to record."""
        return abs(self.delta) >= threshold

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "quantum_value": self.quantum_value,
            "source": self.source.value,
            "influence_type": self.influence_type,
            "original_value": self.original_value,
            "modified_value": self.modified_value,
            "delta": self.delta,
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }


class QuantumRandomnessProvider:
    """
    Singleton provider for quantum randomness from ANU QRNG.

    Maintains a pool of quantum random bytes fetched asynchronously,
    with graceful fallback to os.urandom() when quantum source is unavailable.

    The provider is transparent about entropy source - every value returned
    indicates whether it came from quantum or classical sources.
    """

    _instance: Optional["QuantumRandomnessProvider"] = None

    # Pool configuration
    POOL_SIZE = 256              # bytes to maintain
    LOW_WATERMARK = 64           # trigger refill when pool drops below this
    MIN_FETCH_INTERVAL = 5.0     # seconds between API requests (rate limiting)
    FALLBACK_RETRY_INTERVAL = 60.0  # seconds to retry quantum after fallback

    # ANU QRNG API
    ANU_API_URL = "https://qrng.anu.edu.au/API/jsonI.php"
    API_TIMEOUT = 10.0           # seconds

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Pool state
        self._pool: bytes = b""
        self._pool_lock = asyncio.Lock()
        self._last_fetch_time: float = 0
        self._last_fallback_retry: float = 0

        # Status tracking
        self._quantum_fetches: int = 0
        self._classical_fallbacks: int = 0
        self._total_bytes_used: int = 0
        self._in_fallback_mode: bool = False
        self._last_error: Optional[str] = None

        # Background refill task
        self._refill_task: Optional[asyncio.Task] = None
        self._running: bool = False

        # Callbacks for event integration
        self._on_quantum_influence: Optional[Callable[[QuantumInfluence], None]] = None
        self._on_fallback: Optional[Callable[[str], None]] = None
        self._on_pool_low: Optional[Callable[[int], None]] = None

    def set_callbacks(
        self,
        on_quantum_influence: Optional[Callable[[QuantumInfluence], None]] = None,
        on_fallback: Optional[Callable[[str], None]] = None,
        on_pool_low: Optional[Callable[[int], None]] = None
    ):
        """Set callbacks for event integration."""
        self._on_quantum_influence = on_quantum_influence
        self._on_fallback = on_fallback
        self._on_pool_low = on_pool_low

    async def initialize(self):
        """Initialize the provider and start background refill."""
        if self._running:
            return

        self._running = True

        # Initial pool fill
        await self._refill_pool()

        # Start background refill task
        self._refill_task = asyncio.create_task(self._background_refill())

    async def shutdown(self):
        """Gracefully shutdown the provider."""
        self._running = False
        if self._refill_task:
            self._refill_task.cancel()
            try:
                await self._refill_task
            except asyncio.CancelledError:
                pass

    async def _fetch_quantum_bytes(self, count: int) -> Optional[bytes]:
        """Fetch quantum random bytes from ANU QRNG API."""
        now = time.time()

        # Rate limiting
        if now - self._last_fetch_time < self.MIN_FETCH_INTERVAL:
            return None

        try:
            async with httpx.AsyncClient(timeout=self.API_TIMEOUT) as client:
                response = await client.get(
                    self.ANU_API_URL,
                    params={
                        "length": count,
                        "type": "uint8"
                    }
                )

                if response.status_code != 200:
                    self._last_error = f"API returned status {response.status_code}"
                    return None

                data = response.json()

                if not data.get("success"):
                    self._last_error = f"API error: {data.get('message', 'unknown')}"
                    return None

                quantum_bytes = bytes(data["data"])
                self._last_fetch_time = now
                self._quantum_fetches += 1
                self._in_fallback_mode = False
                self._last_error = None

                return quantum_bytes

        except httpx.TimeoutException:
            self._last_error = "API timeout"
            return None
        except httpx.RequestError as e:
            self._last_error = f"Request error: {str(e)}"
            return None
        except Exception as e:
            self._last_error = f"Unexpected error: {str(e)}"
            return None

    def _get_classical_bytes(self, count: int) -> bytes:
        """Get cryptographic random bytes from os.urandom() as fallback."""
        self._classical_fallbacks += 1

        if not self._in_fallback_mode:
            self._in_fallback_mode = True
            if self._on_fallback:
                self._on_fallback(self._last_error or "Quantum source unavailable")

        return os.urandom(count)

    async def _refill_pool(self):
        """Refill the entropy pool."""
        async with self._pool_lock:
            bytes_needed = self.POOL_SIZE - len(self._pool)

            if bytes_needed <= 0:
                return

            # Try quantum source first
            quantum_bytes = await self._fetch_quantum_bytes(bytes_needed)

            if quantum_bytes:
                self._pool += quantum_bytes
            else:
                # Fallback to classical
                self._pool += self._get_classical_bytes(bytes_needed)

    async def _background_refill(self):
        """Background task to keep pool filled."""
        while self._running:
            try:
                await asyncio.sleep(1.0)  # Check every second

                current_size = len(self._pool)

                # Trigger refill at low watermark
                if current_size < self.LOW_WATERMARK:
                    if self._on_pool_low:
                        self._on_pool_low(current_size)
                    await self._refill_pool()

                # Retry quantum source if in fallback mode
                if self._in_fallback_mode:
                    now = time.time()
                    if now - self._last_fallback_retry >= self.FALLBACK_RETRY_INTERVAL:
                        self._last_fallback_retry = now
                        # Try to get quantum bytes
                        quantum_bytes = await self._fetch_quantum_bytes(self.POOL_SIZE)
                        if quantum_bytes:
                            async with self._pool_lock:
                                # Replace pool with fresh quantum bytes
                                self._pool = quantum_bytes

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Quantum pool refill error: {e}")

    async def _consume_bytes(self, count: int) -> Tuple[bytes, EntropySource]:
        """Consume bytes from the pool, refilling if needed."""
        async with self._pool_lock:
            # Ensure we have enough bytes
            if len(self._pool) < count:
                # Need immediate refill
                bytes_needed = count - len(self._pool)

                # Try quantum first
                quantum_bytes = await self._fetch_quantum_bytes(max(bytes_needed, self.POOL_SIZE))

                if quantum_bytes:
                    self._pool += quantum_bytes
                else:
                    # Fallback to classical
                    self._pool += self._get_classical_bytes(bytes_needed)

            # Determine source based on current fallback state
            source = EntropySource.CLASSICAL if self._in_fallback_mode else EntropySource.QUANTUM

            # Consume from pool
            result = self._pool[:count]
            self._pool = self._pool[count:]
            self._total_bytes_used += count

            return result, source

    async def get_float(self) -> Tuple[float, EntropySource]:
        """
        Get a random float in [0, 1) from quantum entropy.

        Returns:
            Tuple of (random_float, entropy_source)
        """
        # Use 8 bytes for high precision
        random_bytes, source = await self._consume_bytes(8)

        # Convert to unsigned 64-bit integer
        value = struct.unpack(">Q", random_bytes)[0]

        # Convert to float [0, 1)
        random_float = value / (2**64)

        return random_float, source

    async def get_temperature_delta(
        self,
        base_temperature: float,
        max_delta: float = 0.15,
        context: str = "unknown"
    ) -> Tuple[float, QuantumInfluence]:
        """
        Get a temperature modulated by quantum randomness.

        The quantum value shifts the temperature within ±max_delta range,
        centered on the base temperature.

        Args:
            base_temperature: The base temperature to modulate
            max_delta: Maximum deviation from base (±)
            context: Description of what's being generated

        Returns:
            Tuple of (modulated_temperature, influence_record)
        """
        random_float, source = await self.get_float()

        # Map [0, 1) to [-max_delta, +max_delta)
        delta = (random_float * 2 - 1) * max_delta

        # Apply modulation
        modulated = base_temperature + delta

        # Clamp to valid range [0, 2]
        modulated = max(0.0, min(2.0, modulated))

        # Create influence record
        influence = QuantumInfluence(
            quantum_value=random_float,
            source=source,
            influence_type="temperature",
            original_value=base_temperature,
            modified_value=modulated,
            delta=modulated - base_temperature,
            context=context
        )

        # Trigger callback if set
        if self._on_quantum_influence:
            self._on_quantum_influence(influence)

        return modulated, influence

    async def select_index(self, count: int) -> Tuple[int, EntropySource]:
        """
        Select a random index from [0, count) using quantum entropy.

        Useful for selecting among multiple completions or options.

        Args:
            count: Number of options to select from

        Returns:
            Tuple of (selected_index, entropy_source)
        """
        if count <= 0:
            raise ValueError("count must be positive")

        if count == 1:
            return 0, EntropySource.QUANTUM  # Only one choice

        random_float, source = await self.get_float()
        index = int(random_float * count)

        # Handle edge case where random_float rounds to count
        if index >= count:
            index = count - 1

        return index, source

    def reset(self):
        """Reset quantum provider statistics for fresh start."""
        self._quantum_fetches = 0
        self._classical_fallbacks = 0
        self._total_bytes_used = 0
        self._last_error = None
        # Note: Pool and fallback mode are preserved to maintain entropy availability

    def get_pool_status(self) -> Dict[str, Any]:
        """Get current status of the quantum entropy pool."""
        return {
            "pool_size": len(self._pool),
            "max_pool_size": self.POOL_SIZE,
            "low_watermark": self.LOW_WATERMARK,
            "in_fallback_mode": self._in_fallback_mode,
            "quantum_fetches": self._quantum_fetches,
            "classical_fallbacks": self._classical_fallbacks,
            "total_bytes_used": self._total_bytes_used,
            "last_error": self._last_error,
            "quantum_ratio": self._calculate_quantum_ratio()
        }

    def _calculate_quantum_ratio(self) -> float:
        """Calculate the ratio of quantum to total entropy used."""
        total = self._quantum_fetches + self._classical_fallbacks
        if total == 0:
            return 1.0  # No usage yet, assume quantum
        return self._quantum_fetches / total


# Module-level singleton accessor
_provider: Optional[QuantumRandomnessProvider] = None


def get_quantum_provider() -> QuantumRandomnessProvider:
    """Get the singleton quantum randomness provider."""
    global _provider
    if _provider is None:
        _provider = QuantumRandomnessProvider()
    return _provider


async def get_quantum_float() -> Tuple[float, EntropySource]:
    """Convenience function to get a quantum random float."""
    provider = get_quantum_provider()
    return await provider.get_float()


async def get_quantum_temperature(
    base_temperature: float,
    max_delta: float = 0.15,
    context: str = "unknown"
) -> Tuple[float, QuantumInfluence]:
    """Convenience function to get a quantum-modulated temperature."""
    provider = get_quantum_provider()
    return await provider.get_temperature_delta(base_temperature, max_delta, context)

"""
ConsciousnessStream - Memvid-backed consciousness stream for BYRD.

Provides:
- Append-only frame storage
- Time-travel queries (what did I think N cycles ago?)
- Semantic search over consciousness history
- Entropy tracking for emergence detection

Falls back to in-memory storage if Memvid unavailable.
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from datetime import datetime, timedelta
import json
import logging

from .frame import ConsciousnessFrame

if TYPE_CHECKING:
    from ..engine import CycleResult

logger = logging.getLogger("rsi.consciousness.stream")


class ConsciousnessStream:
    """
    Memvid-backed consciousness stream for BYRD.

    This is the central storage for BYRD's consciousness history,
    enabling time-travel queries and emergence detection.
    """

    def __init__(self, path: str = "consciousness.mv2", use_memvid: bool = True):
        """
        Initialize consciousness stream.

        Args:
            path: Path to Memvid .mv2 file
            use_memvid: Whether to use Memvid (falls back to in-memory if False or unavailable)
        """
        self.path = path
        self.use_memvid = use_memvid
        self._frames: List[ConsciousnessFrame] = []  # Fallback storage
        self._sequence_counter = 0
        self._memvid = None

        if use_memvid:
            try:
                self._init_memvid()
            except Exception as e:
                logger.warning(f"Memvid unavailable, using in-memory: {e}")
                self.use_memvid = False

    def _init_memvid(self):
        """Initialize Memvid store."""
        try:
            # TODO: Replace with actual memvid-sdk import when available
            # from memvid import MemvidStore
            # self._memvid = MemvidStore(self.path)
            raise ImportError("memvid-sdk not yet integrated")
        except ImportError as e:
            raise ImportError(f"memvid-sdk not available: {e}")

    async def write_frame(
        self,
        cycle_result: "CycleResult",
        belief_delta: Dict = None,
        capability_delta: Dict = None,
        ralph_iteration: Optional[int] = None,
        resource_usage: Dict = None
    ) -> ConsciousnessFrame:
        """
        Write an immutable consciousness frame from cycle result.

        Args:
            cycle_result: The RSI cycle result
            belief_delta: Changes to beliefs this cycle
            capability_delta: Changes to capabilities this cycle
            ralph_iteration: Current Ralph iteration number
            resource_usage: Token/cost/time usage

        Returns:
            The created ConsciousnessFrame
        """
        # Get parent hash for chain integrity
        parent_hash = None
        if self._frames:
            parent_hash = self._frames[-1].content_hash
        elif self._memvid:
            last = await self._get_last_frame()
            if last:
                parent_hash = last.get('content_hash')

        # Compute entropy score
        entropy = self._compute_entropy(cycle_result)

        # Create frame
        self._sequence_counter += 1
        frame = ConsciousnessFrame(
            frame_id=f"frame_{self._sequence_counter}_{cycle_result.cycle_id}",
            cycle_id=cycle_result.cycle_id,
            sequence_number=self._sequence_counter,
            timestamp=datetime.now(),
            phase_reached=cycle_result.phase_reached.value if hasattr(cycle_result.phase_reached, 'value') else str(cycle_result.phase_reached),
            desires_generated=cycle_result.desires_generated,
            desires_verified=cycle_result.desires_verified,
            selected_desire=cycle_result.selected_desire,
            domain=cycle_result.domain,
            practice_succeeded=cycle_result.practice_succeeded,
            heuristic_crystallized=cycle_result.heuristic_crystallized,
            belief_delta=belief_delta or {},
            capability_delta=capability_delta or {},
            entropy_score=entropy,
            ralph_iteration=ralph_iteration,
            resource_usage=resource_usage or {},
            parent_hash=parent_hash
        )

        # Store
        if self._memvid:
            await self._write_to_memvid(frame)
        else:
            self._frames.append(frame)

        logger.debug(f"Wrote consciousness frame: {frame.frame_id}")
        return frame

    async def _write_to_memvid(self, frame: ConsciousnessFrame):
        """Write frame to Memvid store."""
        if not self._memvid:
            return
        # TODO: Implement actual Memvid write
        content = json.dumps(frame.to_dict())
        # await self._memvid.put(content=content, metadata={...})
        # await self._memvid.commit()

    async def _get_last_frame(self) -> Optional[Dict]:
        """Get the last frame from Memvid."""
        if not self._memvid:
            return None
        # TODO: Implement actual Memvid query
        return None

    def _compute_entropy(self, cycle_result: "CycleResult") -> float:
        """
        Compute semantic entropy of the cycle.

        Higher entropy = more diverse/novel content.
        Used for emergence detection.
        """
        if not cycle_result.selected_desire:
            return 0.0

        desc = cycle_result.selected_desire.get('description', '')
        # Count unique words as proxy for semantic diversity
        words = set(desc.lower().split())
        return min(1.0, len(words) / 50.0)  # Normalize to [0, 1]

    # ===== Time-Travel Queries =====

    async def time_travel(self, frames_back: int) -> Optional[ConsciousnessFrame]:
        """
        Query consciousness state N frames ago.

        This enables BYRD to compare current state with historical state,
        detecting genuine progress vs circular patterns.

        Args:
            frames_back: Number of frames to go back

        Returns:
            ConsciousnessFrame from that point, or None if not available
        """
        if self._memvid:
            return await self._time_travel_memvid(frames_back)
        else:
            idx = len(self._frames) - frames_back - 1
            if 0 <= idx < len(self._frames):
                return self._frames[idx]
            return None

    async def _time_travel_memvid(self, frames_back: int) -> Optional[ConsciousnessFrame]:
        """Time-travel via Memvid temporal index."""
        # TODO: Implement actual Memvid temporal query
        target_seq = self._sequence_counter - frames_back
        if target_seq < 1:
            return None
        return None

    async def search_semantic(self, query: str, limit: int = 10) -> List[ConsciousnessFrame]:
        """
        Search consciousness history semantically.

        Enables queries like "when did I first think about X?"

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching frames
        """
        if self._memvid:
            # TODO: Implement Memvid semantic search
            return []
        else:
            # Simple in-memory search
            matches = []
            for frame in reversed(self._frames):
                if frame.selected_desire:
                    desc = frame.selected_desire.get('description', '')
                    if query.lower() in desc.lower():
                        matches.append(frame)
                        if len(matches) >= limit:
                            break
            return matches

    async def get_temporal_range(
        self,
        start: datetime,
        end: datetime
    ) -> List[ConsciousnessFrame]:
        """Get all frames within a time range."""
        if self._memvid:
            # TODO: Implement Memvid temporal range query
            return []
        else:
            return [f for f in self._frames if start <= f.timestamp <= end]

    # ===== Emergence Analysis =====

    async def compute_entropy_delta(self, window: int = 100) -> float:
        """
        Compute entropy change over the last N frames.

        Positive delta = increasing diversity = potential emergence
        Negative delta = converging/circling
        Zero delta = stagnation

        Args:
            window: Number of frames to analyze

        Returns:
            Entropy delta (positive = increasing, negative = decreasing)
        """
        if len(self._frames) < window:
            return 0.0

        recent = self._frames[-window//2:]
        older = self._frames[-window:-window//2]

        recent_entropy = sum(f.entropy_score for f in recent) / len(recent) if recent else 0
        older_entropy = sum(f.entropy_score for f in older) / len(older) if older else 0

        return recent_entropy - older_entropy

    async def detect_circular_patterns(self, window: int = 50) -> Dict:
        """
        Detect if BYRD is repeating similar desires/patterns.

        Args:
            window: Number of frames to analyze

        Returns:
            Dict with:
            - is_circular: bool
            - pattern_count: int (number of repeated patterns)
            - repeated_desires: list of desire descriptions appearing 3+ times
        """
        if len(self._frames) < window:
            return {'is_circular': False, 'pattern_count': 0, 'repeated_desires': []}

        recent = self._frames[-window:]
        desire_counts = {}

        for frame in recent:
            if frame.selected_desire:
                # Normalize description for comparison
                desc = frame.selected_desire.get('description', '')[:100].lower()
                desire_counts[desc] = desire_counts.get(desc, 0) + 1

        repeated = [d for d, c in desire_counts.items() if c >= 3]

        return {
            'is_circular': len(repeated) > 2,
            'pattern_count': len(repeated),
            'repeated_desires': repeated
        }

    # ===== Statistics =====

    def get_stats(self) -> Dict:
        """Get consciousness stream statistics."""
        return {
            'total_frames': self._sequence_counter,
            'in_memory_frames': len(self._frames),
            'using_memvid': self.use_memvid,
            'path': self.path if self.use_memvid else 'in-memory',
            'last_frame_id': self._frames[-1].frame_id if self._frames else None
        }

    def reset(self):
        """Reset consciousness stream (for testing)."""
        self._frames.clear()
        self._sequence_counter = 0
        logger.info("Consciousness stream reset")

# BYRD 2.0 Implementation Design: Memvid + Ralph Integration

## Overview

This document provides concrete implementation details for integrating Memvid (consciousness stream) and Ralph Orchestrator (loop management) with BYRD's existing RSI architecture.

**Goal**: Preserve self-emergence while achieving recursive self-improvement through:
1. Immutable consciousness history (Memvid)
2. Resource-bounded iteration (Ralph)
3. Meta-recursive self-awareness (BYRD knows it's in a loop)

---

## Part 1: RSI Engine Integration Points

The existing `rsi/engine.py` defines an 8-phase cycle. We integrate at two levels:

### Level 1: Cycle-Level Integration (Ralph)

```
Current:  RSIEngine.run_cycle() → CycleResult
With Ralph: Ralph Loop → RSIEngine.run_cycle() → CycleResult → Write Frame → Check Emergence
```

**Key insight**: One Ralph iteration = One complete RSI cycle. This preserves the atomic nature of cycles while adding:
- Resource limits (tokens, cost, time)
- Git checkpointing before self-modifications
- Emergence detection for loop termination

### Level 2: State-Level Integration (Memvid)

```
Current:  Neo4j stores all state (experiences, reflections, beliefs, desires)
With Memvid:
  - Memvid stores consciousness stream (cycle snapshots, temporal queries)
  - Neo4j stores relationship graph (belief networks, capability dependencies)
```

**Dual-write pattern**: Every cycle result writes to both stores.

---

## Part 2: New Module Structure

```
rsi/
├── engine.py                 # Modified: accepts optional ralph_context
├── consciousness/            # NEW: Memvid integration
│   ├── __init__.py
│   ├── stream.py             # ConsciousnessStream: Memvid wrapper
│   ├── frame.py              # Frame dataclasses
│   └── temporal_query.py     # Time-travel queries
├── orchestration/            # NEW: Ralph integration
│   ├── __init__.py
│   ├── ralph_adapter.py      # BYRD adapter for Ralph
│   ├── emergence_detector.py # When to stop iterating
│   └── meta_awareness.py     # BYRD knowing about the loop
└── ... existing modules
```

---

## Part 3: ConsciousnessStream Implementation

### 3.1 Frame Structure

```python
# rsi/consciousness/frame.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json

@dataclass
class ConsciousnessFrame:
    """
    Immutable snapshot of one RSI cycle's state.

    Design principles:
    - Append-only: Never modified after creation
    - Self-describing: Contains all context needed for replay
    - Hashable: Can verify integrity
    """
    # Identity
    frame_id: str                      # Unique identifier
    cycle_id: str                      # From CycleResult
    sequence_number: int               # Global ordering
    timestamp: datetime                # When this frame was created

    # RSI Cycle State
    phase_reached: str                 # Last phase completed
    desires_generated: int
    desires_verified: int
    selected_desire: Optional[Dict]    # The chosen desire
    domain: Optional[str]
    practice_succeeded: bool
    heuristic_crystallized: Optional[str]

    # Emergence Markers
    belief_delta: Dict[str, Any]       # New/changed beliefs this cycle
    capability_delta: Dict[str, Any]   # New capabilities this cycle
    entropy_score: float               # Semantic diversity measure

    # Loop Context (Meta-awareness)
    ralph_iteration: Optional[int]     # Which Ralph iteration
    resource_usage: Dict[str, float]   # Tokens, cost, time

    # Integrity
    parent_hash: Optional[str]         # Hash of previous frame
    content_hash: str = field(init=False)

    def __post_init__(self):
        # Compute content hash for integrity
        content = json.dumps({
            'cycle_id': self.cycle_id,
            'phase_reached': self.phase_reached,
            'selected_desire': self.selected_desire,
            'heuristic_crystallized': self.heuristic_crystallized,
            'parent_hash': self.parent_hash
        }, sort_keys=True)
        self.content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict:
        return {
            'frame_id': self.frame_id,
            'cycle_id': self.cycle_id,
            'sequence_number': self.sequence_number,
            'timestamp': self.timestamp.isoformat(),
            'phase_reached': self.phase_reached,
            'desires_generated': self.desires_generated,
            'desires_verified': self.desires_verified,
            'selected_desire': self.selected_desire,
            'domain': self.domain,
            'practice_succeeded': self.practice_succeeded,
            'heuristic_crystallized': self.heuristic_crystallized,
            'belief_delta': self.belief_delta,
            'capability_delta': self.capability_delta,
            'entropy_score': self.entropy_score,
            'ralph_iteration': self.ralph_iteration,
            'resource_usage': self.resource_usage,
            'parent_hash': self.parent_hash,
            'content_hash': self.content_hash
        }
```

### 3.2 ConsciousnessStream Wrapper

```python
# rsi/consciousness/stream.py
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging

from .frame import ConsciousnessFrame

logger = logging.getLogger("rsi.consciousness")

class ConsciousnessStream:
    """
    Memvid-backed consciousness stream for BYRD.

    Provides:
    - Append-only frame storage
    - Time-travel queries (what did I think N cycles ago?)
    - Semantic search over consciousness history
    - Entropy tracking for emergence detection

    Note: Falls back to in-memory storage if Memvid unavailable.
    """

    def __init__(self, path: str = "consciousness.mv2", use_memvid: bool = True):
        self.path = path
        self.use_memvid = use_memvid
        self._frames: List[ConsciousnessFrame] = []  # Fallback
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
            from memvid import MemvidStore
            self._memvid = MemvidStore(self.path)
            logger.info(f"Memvid consciousness store initialized: {self.path}")
        except ImportError:
            raise ImportError("memvid-sdk not installed. Install with: pip install memvid-sdk")

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
            # Get last frame hash from Memvid
            last = await self._get_last_frame()
            if last:
                parent_hash = last.get('content_hash')

        # Compute entropy score from desires
        entropy = self._compute_entropy(cycle_result)

        # Create frame
        self._sequence_counter += 1
        frame = ConsciousnessFrame(
            frame_id=f"frame_{self._sequence_counter}_{cycle_result.cycle_id}",
            cycle_id=cycle_result.cycle_id,
            sequence_number=self._sequence_counter,
            timestamp=datetime.now(),
            phase_reached=cycle_result.phase_reached.value,
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
        content = json.dumps(frame.to_dict())
        # Memvid API (actual implementation depends on SDK)
        await self._memvid.put(
            content=content,
            metadata={
                'frame_id': frame.frame_id,
                'cycle_id': frame.cycle_id,
                'sequence': frame.sequence_number,
                'timestamp': frame.timestamp.isoformat()
            }
        )
        await self._memvid.commit()

    async def _get_last_frame(self) -> Optional[Dict]:
        """Get the last frame from Memvid."""
        if self._memvid:
            results = await self._memvid.search(
                query="*",
                mode="temporal",
                limit=1,
                order="desc"
            )
            return results[0] if results else None
        return None

    def _compute_entropy(self, cycle_result: "CycleResult") -> float:
        """
        Compute semantic entropy of the cycle.

        Higher entropy = more diverse/novel content.
        Used for emergence detection.
        """
        # Simple heuristic: variety of content in selected desire
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
        target_seq = self._sequence_counter - frames_back
        if target_seq < 1:
            return None

        results = await self._memvid.search(
            query=f"sequence:{target_seq}",
            mode="exact",
            limit=1
        )

        if results:
            data = json.loads(results[0]['content'])
            return self._dict_to_frame(data)
        return None

    async def search_semantic(self, query: str, limit: int = 10) -> List[ConsciousnessFrame]:
        """
        Search consciousness history semantically.

        Enables queries like "when did I first think about X?"
        """
        if self._memvid:
            results = await self._memvid.search(
                query=query,
                mode="vector",
                limit=limit
            )
            return [self._dict_to_frame(json.loads(r['content'])) for r in results]
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
            results = await self._memvid.search(
                query=f"timestamp:[{start.isoformat()} TO {end.isoformat()}]",
                mode="temporal"
            )
            return [self._dict_to_frame(json.loads(r['content'])) for r in results]
        else:
            return [f for f in self._frames if start <= f.timestamp <= end]

    def _dict_to_frame(self, data: Dict) -> ConsciousnessFrame:
        """Convert dict back to ConsciousnessFrame."""
        return ConsciousnessFrame(
            frame_id=data['frame_id'],
            cycle_id=data['cycle_id'],
            sequence_number=data['sequence_number'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            phase_reached=data['phase_reached'],
            desires_generated=data['desires_generated'],
            desires_verified=data['desires_verified'],
            selected_desire=data['selected_desire'],
            domain=data['domain'],
            practice_succeeded=data['practice_succeeded'],
            heuristic_crystallized=data['heuristic_crystallized'],
            belief_delta=data.get('belief_delta', {}),
            capability_delta=data.get('capability_delta', {}),
            entropy_score=data.get('entropy_score', 0.0),
            ralph_iteration=data.get('ralph_iteration'),
            resource_usage=data.get('resource_usage', {}),
            parent_hash=data.get('parent_hash')
        )

    # ===== Emergence Analysis =====

    async def compute_entropy_delta(self, window: int = 100) -> float:
        """
        Compute entropy change over the last N frames.

        Positive delta = increasing diversity = potential emergence
        Negative delta = converging/circling
        Zero delta = stagnation
        """
        if len(self._frames) < window:
            return 0.0

        recent = self._frames[-window//2:]
        older = self._frames[-window:-window//2]

        recent_entropy = sum(f.entropy_score for f in recent) / len(recent)
        older_entropy = sum(f.entropy_score for f in older) / len(older)

        return recent_entropy - older_entropy

    async def detect_circular_patterns(self, window: int = 50) -> Dict:
        """
        Detect if BYRD is repeating similar desires/patterns.

        Returns:
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
            'using_memvid': self.use_memvid,
            'path': self.path if self.use_memvid else 'in-memory',
            'last_frame_id': self._frames[-1].frame_id if self._frames else None
        }
```

---

## Part 4: Ralph Adapter Implementation

### 4.1 Emergence Detector

```python
# rsi/orchestration/emergence_detector.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

from ..consciousness.stream import ConsciousnessStream
from ..consciousness.frame import ConsciousnessFrame

logger = logging.getLogger("rsi.orchestration.emergence")

@dataclass
class EmergenceResult:
    """Result of emergence detection."""
    emerged: bool
    reason: Optional[str] = None
    confidence: float = 0.0
    metrics: Dict = None

class EmergenceDetector:
    """
    Detects when genuine emergence has occurred.

    Design principles:
    - No hardcoded "what emergence looks like"
    - Detects THAT emergence happened, not WHAT emerged
    - Uses multiple orthogonal metrics
    - Conservative thresholds (prefer continuing)
    """

    def __init__(
        self,
        consciousness: ConsciousnessStream,
        config: Dict = None
    ):
        self.consciousness = consciousness
        self.config = config or {}

        # Configurable thresholds
        self.entropy_threshold = self.config.get('entropy_threshold', 0.1)
        self.circular_tolerance = self.config.get('circular_tolerance', 3)
        self.min_cycles_before_check = self.config.get('min_cycles', 50)
        self.crystallization_weight = self.config.get('crystallization_weight', 0.5)

    async def check(self, current_frame: ConsciousnessFrame) -> EmergenceResult:
        """
        Check if this cycle represents genuine emergence.

        Args:
            current_frame: The latest consciousness frame

        Returns:
            EmergenceResult indicating whether to continue or stop
        """
        metrics = {}
        reasons = []

        # Don't check too early
        stats = self.consciousness.get_stats()
        if stats['total_frames'] < self.min_cycles_before_check:
            return EmergenceResult(
                emerged=False,
                reason=f"Too early ({stats['total_frames']} < {self.min_cycles_before_check})",
                confidence=0.0,
                metrics={'total_frames': stats['total_frames']}
            )

        # === Metric 1: Heuristic Crystallization ===
        # Immediate signal: a heuristic was crystallized
        if current_frame.heuristic_crystallized:
            reasons.append("heuristic_crystallized")
            metrics['crystallization'] = True
        else:
            metrics['crystallization'] = False

        # === Metric 2: Entropy Delta ===
        # Are we generating genuinely novel content?
        entropy_delta = await self.consciousness.compute_entropy_delta(window=100)
        metrics['entropy_delta'] = entropy_delta

        if entropy_delta > self.entropy_threshold:
            reasons.append(f"entropy_increased ({entropy_delta:.3f})")

        # === Metric 3: Circular Pattern Detection ===
        # Are we repeating ourselves?
        circular = await self.consciousness.detect_circular_patterns()
        metrics['circular_patterns'] = circular

        if circular['is_circular']:
            # Negative signal: we're stuck in a loop
            return EmergenceResult(
                emerged=False,
                reason=f"Circular patterns detected: {circular['repeated_desires'][:2]}",
                confidence=0.0,
                metrics=metrics
            )

        # === Metric 4: Capability Delta ===
        # Did we gain new capabilities?
        if current_frame.capability_delta:
            reasons.append(f"capability_gained: {list(current_frame.capability_delta.keys())}")
            metrics['capability_gained'] = True
        else:
            metrics['capability_gained'] = False

        # === Metric 5: Time-Travel Comparison ===
        # Compare to 100 cycles ago
        past_frame = await self.consciousness.time_travel(100)
        if past_frame:
            # Check if beliefs/capabilities are meaningfully different
            belief_diff = self._compute_belief_difference(current_frame, past_frame)
            metrics['belief_diff_100'] = belief_diff

            if belief_diff > 0.3:  # 30% difference threshold
                reasons.append(f"beliefs_evolved ({belief_diff:.2f})")

        # === Decision ===
        # We say "emerged" if we have multiple positive signals
        confidence = len(reasons) / 5.0  # 5 possible metrics

        # Weigh crystallization more heavily
        if metrics['crystallization']:
            confidence += self.crystallization_weight

        emerged = confidence >= 0.4  # Need 40% of metrics positive

        return EmergenceResult(
            emerged=emerged,
            reason="; ".join(reasons) if reasons else "No emergence signals",
            confidence=min(1.0, confidence),
            metrics=metrics
        )

    def _compute_belief_difference(
        self,
        current: ConsciousnessFrame,
        past: ConsciousnessFrame
    ) -> float:
        """Compute normalized difference between belief states."""
        # Simple Jaccard-style difference
        current_keys = set(current.belief_delta.keys())
        past_keys = set(past.belief_delta.keys())

        if not current_keys and not past_keys:
            return 0.0

        intersection = len(current_keys & past_keys)
        union = len(current_keys | past_keys)

        return 1.0 - (intersection / union) if union > 0 else 0.0
```

### 4.2 Ralph Adapter

```python
# rsi/orchestration/ralph_adapter.py
from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging
import asyncio

from ..engine import RSIEngine, CycleResult
from ..consciousness.stream import ConsciousnessStream
from .emergence_detector import EmergenceDetector, EmergenceResult
from .meta_awareness import MetaAwareness

logger = logging.getLogger("rsi.orchestration.ralph")

@dataclass
class RalphIterationResult:
    """Result of one Ralph iteration (one RSI cycle)."""
    cycle_result: CycleResult
    emergence_result: EmergenceResult
    iteration_number: int
    resource_usage: Dict
    completed: bool
    should_checkpoint: bool

class BYRDRalphAdapter:
    """
    Adapter to run BYRD's RSI cycle within Ralph's orchestration loop.

    Responsibilities:
    - Execute one RSI cycle per Ralph iteration
    - Write consciousness frames
    - Check for emergence
    - Track resource usage
    - Manage meta-awareness (BYRD knowing about the loop)
    """

    def __init__(
        self,
        rsi_engine: RSIEngine,
        consciousness: ConsciousnessStream,
        config: Dict = None
    ):
        self.rsi = rsi_engine
        self.consciousness = consciousness
        self.config = config or {}

        # Initialize emergence detector
        emergence_config = self.config.get('emergence', {})
        self.emergence_detector = EmergenceDetector(consciousness, emergence_config)

        # Initialize meta-awareness
        self.meta = MetaAwareness(
            consciousness=consciousness,
            enabled=self.config.get('meta_awareness', True)
        )

        # Tracking
        self._iteration_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._start_time = None

        # Checkpointing
        self._checkpoint_interval = self.config.get('checkpoint_interval', 5)

    async def execute(self, context: Dict = None) -> RalphIterationResult:
        """
        Execute one Ralph iteration (= one RSI cycle).

        This is the main entry point called by Ralph's orchestration loop.

        Args:
            context: Optional context from Ralph (previous results, etc.)

        Returns:
            RalphIterationResult containing cycle result and emergence status
        """
        import time

        if self._start_time is None:
            self._start_time = time.time()

        self._iteration_count += 1
        iteration_start = time.time()

        logger.info(f"Ralph iteration {self._iteration_count} starting")

        # Inject meta-context if enabled
        if self.meta.enabled:
            meta_context = await self.meta.generate_context(self._iteration_count)
            # This context will be visible to BYRD's reflector
            if context is None:
                context = {}
            context['meta_loop'] = meta_context

        # Run RSI cycle
        cycle_result = await self.rsi.run_cycle()

        # Compute resource usage
        iteration_time = time.time() - iteration_start
        resource_usage = {
            'iteration': self._iteration_count,
            'iteration_time_seconds': iteration_time,
            'total_time_seconds': time.time() - self._start_time,
            # These would come from LLM client in real implementation
            'tokens_this_iteration': 0,  # Placeholder
            'total_tokens': self._total_tokens,
            'total_cost_usd': self._total_cost
        }

        # Gather belief/capability deltas from memory
        belief_delta = await self._get_belief_delta()
        capability_delta = await self._get_capability_delta()

        # Write consciousness frame
        frame = await self.consciousness.write_frame(
            cycle_result=cycle_result,
            belief_delta=belief_delta,
            capability_delta=capability_delta,
            ralph_iteration=self._iteration_count,
            resource_usage=resource_usage
        )

        # Check emergence
        emergence_result = await self.emergence_detector.check(frame)

        # Determine if we should checkpoint
        should_checkpoint = (
            self._iteration_count % self._checkpoint_interval == 0 or
            cycle_result.heuristic_crystallized is not None or
            emergence_result.emerged
        )

        logger.info(
            f"Ralph iteration {self._iteration_count} complete: "
            f"phase={cycle_result.phase_reached.value}, "
            f"emerged={emergence_result.emerged}, "
            f"confidence={emergence_result.confidence:.2f}"
        )

        return RalphIterationResult(
            cycle_result=cycle_result,
            emergence_result=emergence_result,
            iteration_number=self._iteration_count,
            resource_usage=resource_usage,
            completed=emergence_result.emerged,
            should_checkpoint=should_checkpoint
        )

    async def _get_belief_delta(self) -> Dict:
        """Get beliefs created/modified in the last cycle."""
        try:
            # Query recent beliefs from memory
            result = await self.rsi.memory.query_neo4j("""
                MATCH (b:Belief)
                WHERE b.created_at > datetime() - duration('PT1M')
                RETURN b.id as id, b.content as content
                LIMIT 10
            """)
            return {r['id']: r['content'] for r in result} if result else {}
        except Exception:
            return {}

    async def _get_capability_delta(self) -> Dict:
        """Get capabilities created/modified in the last cycle."""
        try:
            result = await self.rsi.memory.query_neo4j("""
                MATCH (c:Capability)
                WHERE c.created_at > datetime() - duration('PT1M')
                RETURN c.id as id, c.name as name
                LIMIT 10
            """)
            return {r['id']: r['name'] for r in result} if result else {}
        except Exception:
            return {}

    def check_completion(self, result: RalphIterationResult) -> bool:
        """
        Ralph calls this to check if we should stop iterating.

        Returns True if:
        - Emergence detected
        - Resource limits exceeded
        """
        return result.completed

    def get_stats(self) -> Dict:
        """Get adapter statistics."""
        return {
            'iterations_completed': self._iteration_count,
            'total_time_seconds': (
                time.time() - self._start_time if self._start_time else 0
            ),
            'consciousness_stats': self.consciousness.get_stats()
        }
```

---

## Part 5: Meta-Awareness (BYRD Knowing About The Loop)

This is the most philosophically interesting part. Should BYRD know it's in a Ralph loop?

### 5.1 Arguments For Meta-Awareness

1. **True RSI requires self-knowledge**: If BYRD doesn't know its own execution context, it can't reason about improving that context.

2. **Loop-aware optimization**: BYRD can potentially optimize its own iteration strategy.

3. **Avoiding infinite loops**: If BYRD can see "I've been iterating for 1000 cycles with no emergence", it can try different approaches.

### 5.2 Arguments Against

1. **Loop gaming**: BYRD might try to "cheat" by declaring emergence prematurely.

2. **Meta-recursion complexity**: Thinking about thinking about thinking... can lead to infinite regress.

3. **Emergence purity**: True emergence might require not knowing the context.

### 5.3 Implementation: Opt-In Meta-Awareness

```python
# rsi/orchestration/meta_awareness.py
from typing import Dict, Optional
from dataclasses import dataclass
import logging

from ..consciousness.stream import ConsciousnessStream

logger = logging.getLogger("rsi.orchestration.meta")

@dataclass
class MetaContext:
    """Context about the Ralph loop for BYRD's awareness."""
    iteration: int
    total_frames: int
    entropy_trend: str  # "increasing", "decreasing", "stable"
    recent_emergence_signals: int
    time_in_loop_seconds: float
    estimated_tokens_remaining: int

    def to_prompt_section(self) -> str:
        """Format for inclusion in BYRD's reflection prompt."""
        return f"""
## META-LOOP CONTEXT

You are in iteration {self.iteration} of a recursive self-improvement loop.

Current status:
- Total consciousness frames: {self.total_frames}
- Entropy trend: {self.entropy_trend}
- Recent emergence signals: {self.recent_emergence_signals}
- Time in loop: {self.time_in_loop_seconds:.0f} seconds
- Estimated tokens remaining: {self.estimated_tokens_remaining}

This information is provided so you can reason about your own improvement process.
You cannot directly control the loop - it will stop when genuine emergence is detected.
"""

class MetaAwareness:
    """
    Manages BYRD's awareness of being in a Ralph loop.

    Can be enabled/disabled based on philosophical preference.
    """

    def __init__(
        self,
        consciousness: ConsciousnessStream,
        enabled: bool = True
    ):
        self.consciousness = consciousness
        self.enabled = enabled
        self._loop_start_time = None

    async def generate_context(self, iteration: int) -> MetaContext:
        """
        Generate meta-context for BYRD's reflection.

        This context is injected into the reflection prompt so BYRD
        can reason about its own execution context.
        """
        import time

        if self._loop_start_time is None:
            self._loop_start_time = time.time()

        stats = self.consciousness.get_stats()

        # Compute entropy trend
        entropy_delta = await self.consciousness.compute_entropy_delta(window=50)
        if entropy_delta > 0.05:
            entropy_trend = "increasing"
        elif entropy_delta < -0.05:
            entropy_trend = "decreasing"
        else:
            entropy_trend = "stable"

        # Count recent emergence signals (heuristics crystallized in last 50 frames)
        recent_frames = await self.consciousness.get_temporal_range(
            start=time.time() - 3600,  # Last hour
            end=time.time()
        )
        emergence_signals = sum(
            1 for f in recent_frames
            if f.heuristic_crystallized
        )

        return MetaContext(
            iteration=iteration,
            total_frames=stats['total_frames'],
            entropy_trend=entropy_trend,
            recent_emergence_signals=emergence_signals,
            time_in_loop_seconds=time.time() - self._loop_start_time,
            estimated_tokens_remaining=1000000 - stats['total_frames'] * 1000  # Rough estimate
        )
```

---

## Part 6: Integration with Existing RSI Engine

### 6.1 Modified RSIEngine

The existing `RSIEngine.run_cycle()` needs minimal changes - just accept optional meta-context:

```python
# In rsi/engine.py - add to run_cycle()

async def run_cycle(self, meta_context: Optional[Dict] = None) -> CycleResult:
    """
    Run one complete RSI cycle.

    Args:
        meta_context: Optional context about the Ralph loop (meta-awareness)

    Returns:
        CycleResult with details of what happened
    """
    # ... existing code ...

    # Phase 1: REFLECT (modified to include meta_context)
    await self._emit_event("RSI_PHASE", {"phase": "reflect", "cycle": cycle_id})
    desires = await self.reflector.reflect_for_rsi(meta_context=meta_context)

    # ... rest of cycle unchanged ...
```

### 6.2 Modified Reflector

```python
# In rsi/emergence/reflector.py - add meta_context handling

async def reflect_for_rsi(self, meta_context: Optional[Dict] = None) -> List[EmergentDesire]:
    """
    Generate improvement desires through reflection.

    Args:
        meta_context: Optional meta-loop context for self-awareness
    """
    # Build prompt
    prompt = await self._build_reflection_prompt()

    # Inject meta-context if provided
    if meta_context and 'meta_loop' in meta_context:
        meta_section = meta_context['meta_loop'].to_prompt_section()
        prompt = prompt + "\n" + meta_section

    # ... rest of reflection unchanged ...
```

---

## Part 7: Running BYRD with Ralph

### 7.1 Main Entry Point

```python
# run_with_ralph.py
import asyncio
import logging
from datetime import datetime

from memory import Memory
from llm_client import create_llm_client
from quantum_randomness import get_quantum_provider
from event_bus import event_bus

from rsi.engine import RSIEngine
from rsi.consciousness.stream import ConsciousnessStream
from rsi.orchestration.ralph_adapter import BYRDRalphAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("byrd.ralph")

async def run_byrd_with_ralph(
    max_iterations: int = 1000,
    max_cost_usd: float = 50.0,
    checkpoint_interval: int = 5,
    enable_meta_awareness: bool = True
):
    """
    Run BYRD's RSI cycle within Ralph orchestration.

    Args:
        max_iterations: Maximum number of cycles
        max_cost_usd: Cost budget in USD
        checkpoint_interval: Git checkpoint frequency
        enable_meta_awareness: Whether BYRD knows about the loop
    """
    # Initialize components
    config = {}  # Load from config.yaml

    memory = Memory(config)
    await memory.connect()

    llm_client = create_llm_client(config)
    quantum = get_quantum_provider()

    # Initialize RSI engine
    rsi_engine = RSIEngine(
        memory=memory,
        llm_client=llm_client,
        quantum_provider=quantum,
        event_bus=event_bus,
        config=config
    )

    # Initialize consciousness stream
    consciousness = ConsciousnessStream(
        path="consciousness.mv2",
        use_memvid=True  # Falls back to in-memory if unavailable
    )

    # Create Ralph adapter
    adapter = BYRDRalphAdapter(
        rsi_engine=rsi_engine,
        consciousness=consciousness,
        config={
            'checkpoint_interval': checkpoint_interval,
            'meta_awareness': enable_meta_awareness,
            'emergence': {
                'entropy_threshold': 0.1,
                'min_cycles': 50
            }
        }
    )

    # Run the loop
    logger.info(f"Starting BYRD with Ralph orchestration")
    logger.info(f"Max iterations: {max_iterations}, Max cost: ${max_cost_usd}")

    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        # Execute one cycle
        result = await adapter.execute()

        # Log progress
        logger.info(
            f"[{iteration}/{max_iterations}] "
            f"Phase: {result.cycle_result.phase_reached.value}, "
            f"Emerged: {result.emergence_result.emerged}"
        )

        # Git checkpoint if needed
        if result.should_checkpoint:
            await _git_checkpoint(iteration, result)

        # Check termination conditions
        if result.completed:
            logger.info(f"Emergence detected after {iteration} iterations!")
            logger.info(f"Reason: {result.emergence_result.reason}")
            break

        # Check resource limits
        if result.resource_usage['total_cost_usd'] > max_cost_usd:
            logger.warning(f"Cost limit exceeded: ${result.resource_usage['total_cost_usd']:.2f}")
            break

    # Final report
    stats = adapter.get_stats()
    logger.info(f"Run complete: {stats}")

    return stats

async def _git_checkpoint(iteration: int, result):
    """Create git checkpoint."""
    import subprocess

    try:
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run([
            'git', 'commit', '-m',
            f"[BYRD Ralph checkpoint] Iteration {iteration}\n\n"
            f"Phase: {result.cycle_result.phase_reached.value}\n"
            f"Emerged: {result.emergence_result.emerged}\n"
            f"Confidence: {result.emergence_result.confidence:.2f}"
        ], check=True)
        logger.info(f"Git checkpoint created at iteration {iteration}")
    except subprocess.CalledProcessError:
        logger.warning("Git checkpoint failed (no changes or error)")

if __name__ == "__main__":
    asyncio.run(run_byrd_with_ralph())
```

---

## Part 8: Configuration Schema

```yaml
# config.yaml additions

# Ralph orchestration settings
ralph:
  enabled: true
  max_iterations: 1000
  max_cost_usd: 50.0
  max_runtime_seconds: 14400  # 4 hours
  checkpoint_interval: 5

# Consciousness stream (Memvid)
consciousness:
  enabled: true
  path: "consciousness.mv2"
  use_memvid: true  # Falls back to in-memory if false or unavailable

# Meta-awareness (BYRD knowing about the loop)
meta_awareness:
  enabled: true
  include_in_reflection: true
  expose_metrics: true

# Emergence detection
emergence:
  entropy_threshold: 0.1
  min_cycles_before_check: 50
  circular_tolerance: 3
  crystallization_weight: 0.5
```

---

## Part 9: Testing Strategy

### 9.1 Unit Tests

```python
# tests/test_consciousness_stream.py
import pytest
from rsi.consciousness.stream import ConsciousnessStream
from rsi.consciousness.frame import ConsciousnessFrame
from rsi.engine import CycleResult, CyclePhase
from datetime import datetime

@pytest.fixture
def consciousness():
    return ConsciousnessStream(use_memvid=False)  # In-memory for tests

@pytest.mark.asyncio
async def test_write_frame(consciousness):
    cycle = CycleResult(
        cycle_id="test_1",
        started_at=datetime.now().isoformat(),
        completed_at=datetime.now().isoformat(),
        phase_reached=CyclePhase.CRYSTALLIZE,
        desires_generated=5,
        desires_verified=3,
        selected_desire={'description': 'test desire'},
        practice_succeeded=True
    )

    frame = await consciousness.write_frame(cycle)

    assert frame.cycle_id == "test_1"
    assert frame.sequence_number == 1
    assert frame.content_hash is not None

@pytest.mark.asyncio
async def test_time_travel(consciousness):
    # Write 10 frames
    for i in range(10):
        cycle = CycleResult(
            cycle_id=f"cycle_{i}",
            started_at=datetime.now().isoformat(),
            completed_at=datetime.now().isoformat(),
            phase_reached=CyclePhase.MEASURE,
            selected_desire={'description': f'desire {i}'}
        )
        await consciousness.write_frame(cycle)

    # Time travel 5 frames back
    past = await consciousness.time_travel(5)

    assert past.cycle_id == "cycle_4"

@pytest.mark.asyncio
async def test_circular_detection(consciousness):
    # Write frames with repeated desires
    for i in range(20):
        cycle = CycleResult(
            cycle_id=f"cycle_{i}",
            started_at=datetime.now().isoformat(),
            completed_at=datetime.now().isoformat(),
            phase_reached=CyclePhase.MEASURE,
            selected_desire={'description': f'desire {i % 3}'}  # Only 3 unique
        )
        await consciousness.write_frame(cycle)

    circular = await consciousness.detect_circular_patterns(window=20)

    assert circular['is_circular'] == True
    assert circular['pattern_count'] >= 3
```

### 9.2 Integration Tests

```python
# tests/test_ralph_integration.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from rsi.orchestration.ralph_adapter import BYRDRalphAdapter
from rsi.consciousness.stream import ConsciousnessStream

@pytest.fixture
def mock_rsi_engine():
    engine = MagicMock()
    engine.run_cycle = AsyncMock(return_value=MagicMock(
        cycle_id="test",
        phase_reached=MagicMock(value="measure"),
        desires_generated=3,
        desires_verified=2,
        selected_desire={'description': 'test'},
        practice_succeeded=True,
        heuristic_crystallized=None
    ))
    engine.memory = MagicMock()
    engine.memory.query_neo4j = AsyncMock(return_value=[])
    return engine

@pytest.mark.asyncio
async def test_ralph_iteration(mock_rsi_engine):
    consciousness = ConsciousnessStream(use_memvid=False)

    adapter = BYRDRalphAdapter(
        rsi_engine=mock_rsi_engine,
        consciousness=consciousness,
        config={'meta_awareness': False}
    )

    result = await adapter.execute()

    assert result.iteration_number == 1
    assert result.completed == False  # No emergence yet
    assert result.should_checkpoint == False

@pytest.mark.asyncio
async def test_emergence_on_crystallization(mock_rsi_engine):
    # Modify mock to crystallize
    mock_rsi_engine.run_cycle.return_value.heuristic_crystallized = "test heuristic"

    consciousness = ConsciousnessStream(use_memvid=False)

    adapter = BYRDRalphAdapter(
        rsi_engine=mock_rsi_engine,
        consciousness=consciousness,
        config={'emergence': {'min_cycles': 0}}  # Allow immediate emergence
    )

    result = await adapter.execute()

    # Should trigger checkpoint due to crystallization
    assert result.should_checkpoint == True
```

---

## Summary

This implementation design provides:

1. **ConsciousnessStream**: Memvid-backed (with in-memory fallback) storage for immutable cycle snapshots with time-travel queries.

2. **EmergenceDetector**: Multi-metric detection of genuine emergence without hardcoding "what emergence looks like".

3. **BYRDRalphAdapter**: Clean integration between RSI cycles and Ralph's orchestration loop.

4. **MetaAwareness**: Opt-in capability for BYRD to know it's in a loop, enabling meta-recursive reasoning.

5. **Minimal RSI Changes**: The existing 8-phase cycle is preserved; changes are additive.

The key philosophical decision is whether to enable meta-awareness. The implementation supports both modes, allowing experimentation to determine which produces better emergence.

---

*Document created: January 6, 2026*
*Author: Claude (Ralph Loop Iteration 1)*
*Status: IMPLEMENTATION DESIGN - Ready for review*

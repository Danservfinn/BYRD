# BYRD AGI IMPROVEMENT IMPLEMENTATION PLAN

## Overview

This plan details 13 improvements across 4 phases, ordered by dependency. Each improvement specifies exact files, line numbers, and integration code.

**Constraint**: All improvements must work with glm-4.7 as primary LLM.

**Total Estimated Effort**: ~2,500 lines of new code + ~500 lines of modifications

---

## PHASE 1: FOUNDATION (No Dependencies)

### 1.1 Semantic Cache for LLM Client

**Purpose**: Reduce redundant LLM calls by 40-60% through semantic similarity caching.

**Files to Modify**:
- `llm_client.py` (primary)
- `config.yaml` (configuration)

**Integration Point**: Lines 156-162 in `llm_client.py`, before `wait_for_slot()` is called.

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/semantic_cache.py

import hashlib
import time
from typing import Optional, Dict, Tuple, Any
from dataclasses import dataclass
import numpy as np

@dataclass
class CacheEntry:
    query_hash: str
    query_text: str
    query_embedding: Optional[np.ndarray]
    response: str
    timestamp: float
    hit_count: int = 0

class SemanticCache:
    """
    Caches LLM responses with semantic similarity matching.

    Two-tier lookup:
    1. Exact hash match (fast)
    2. Semantic similarity match (if embedder available)
    """

    def __init__(
        self,
        max_entries: int = 1000,
        ttl_seconds: float = 3600,  # 1 hour default
        similarity_threshold: float = 0.92,
        embedder = None  # Optional sentence-transformers embedder
    ):
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self.similarity_threshold = similarity_threshold
        self.embedder = embedder

        self._hash_cache: Dict[str, CacheEntry] = {}
        self._semantic_index: Dict[str, CacheEntry] = {}  # For similarity lookup

        # Metrics
        self._hits = 0
        self._misses = 0
        self._semantic_hits = 0

    def _hash_query(self, query: str) -> str:
        """Create deterministic hash of query."""
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    def _is_expired(self, entry: CacheEntry) -> bool:
        return (time.time() - entry.timestamp) > self.ttl_seconds

    async def get(self, query: str) -> Optional[str]:
        """
        Look up cached response.
        Returns None if not found or expired.
        """
        query_hash = self._hash_query(query)

        # Tier 1: Exact hash match
        if query_hash in self._hash_cache:
            entry = self._hash_cache[query_hash]
            if not self._is_expired(entry):
                entry.hit_count += 1
                self._hits += 1
                return entry.response
            else:
                # Expired - remove
                del self._hash_cache[query_hash]

        # Tier 2: Semantic similarity (if embedder available)
        if self.embedder and len(self._semantic_index) > 0:
            try:
                query_embedding = self.embedder.encode(query)

                best_match = None
                best_similarity = 0.0

                for entry in self._semantic_index.values():
                    if entry.query_embedding is not None and not self._is_expired(entry):
                        similarity = self._cosine_similarity(
                            query_embedding,
                            entry.query_embedding
                        )
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_match = entry

                if best_match and best_similarity >= self.similarity_threshold:
                    best_match.hit_count += 1
                    self._semantic_hits += 1
                    self._hits += 1
                    return best_match.response
            except Exception:
                pass  # Fallback to cache miss

        self._misses += 1
        return None

    async def put(self, query: str, response: str):
        """Store response in cache."""
        query_hash = self._hash_query(query)

        # Compute embedding if available
        query_embedding = None
        if self.embedder:
            try:
                query_embedding = self.embedder.encode(query)
            except Exception:
                pass

        entry = CacheEntry(
            query_hash=query_hash,
            query_text=query,
            query_embedding=query_embedding,
            response=response,
            timestamp=time.time()
        )

        # Enforce max entries (LRU eviction)
        if len(self._hash_cache) >= self.max_entries:
            self._evict_oldest()

        self._hash_cache[query_hash] = entry
        if query_embedding is not None:
            self._semantic_index[query_hash] = entry

    def _evict_oldest(self):
        """Remove oldest entry by timestamp."""
        if not self._hash_cache:
            return
        oldest_hash = min(
            self._hash_cache.keys(),
            key=lambda h: self._hash_cache[h].timestamp
        )
        del self._hash_cache[oldest_hash]
        if oldest_hash in self._semantic_index:
            del self._semantic_index[oldest_hash]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between embeddings."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def get_stats(self) -> Dict[str, Any]:
        """Return cache performance metrics."""
        total = self._hits + self._misses
        return {
            "total_queries": total,
            "hits": self._hits,
            "misses": self._misses,
            "semantic_hits": self._semantic_hits,
            "hit_rate": self._hits / total if total > 0 else 0.0,
            "entries": len(self._hash_cache),
            "max_entries": self.max_entries
        }

    def clear(self):
        """Clear all cache entries."""
        self._hash_cache.clear()
        self._semantic_index.clear()
```

**Modify `llm_client.py`**:

```python
# Add to imports (Line ~15)
from semantic_cache import SemanticCache

# Add to LLMClient.__init__ (after Line 95)
def __init__(self, config: Dict, ...):
    # ... existing init code ...

    # Initialize semantic cache
    cache_config = config.get("semantic_cache", {})
    self._cache = SemanticCache(
        max_entries=cache_config.get("max_entries", 1000),
        ttl_seconds=cache_config.get("ttl_seconds", 3600),
        similarity_threshold=cache_config.get("similarity_threshold", 0.92),
        embedder=self._embedder if hasattr(self, '_embedder') else None
    )
    self._cache_enabled = cache_config.get("enabled", True)

# Modify generate() method (around Line 161)
async def generate(
    self,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    operation: str = "generate",
    bypass_cache: bool = False  # NEW PARAMETER
) -> str:
    # Check cache first (before rate limiting)
    if self._cache_enabled and not bypass_cache:
        cached = await self._cache.get(prompt)
        if cached is not None:
            # Still track usage for metrics
            self._track_usage(prompt, cached, {}, operation + "_cached")
            return cached

    # Existing rate limiting and generation code...
    wait_time = await _rate_limiter.wait_for_slot()
    # ... existing generation logic ...

    response_text = # ... result from LLM ...

    # Store in cache (after successful generation)
    if self._cache_enabled and not bypass_cache:
        await self._cache.put(prompt, response_text)

    return response_text
```

**Config addition** (`config.yaml`):

```yaml
semantic_cache:
  enabled: true
  max_entries: 1000
  ttl_seconds: 3600
  similarity_threshold: 0.92
```

---

### 1.2 Salience Scoring System

**Purpose**: Replace recency-only retrieval with multi-factor salience scoring.

**Files to Modify**:
- NEW: `salience.py`
- `memory_reasoner.py` (Lines 248, 262)
- `memory.py` (retrieval methods)

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/salience.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import time
import math

@dataclass
class SalienceFactors:
    recency: float = 0.0       # Time decay
    surprise: float = 0.0      # Prediction error
    relevance: float = 0.0     # Goal alignment
    connectivity: float = 0.0   # Graph degree
    access_frequency: float = 0.0  # How often accessed
    emotional_intensity: float = 0.0  # Sentiment magnitude

@dataclass
class SalienceWeights:
    """Configurable weights for salience factors."""
    recency: float = 0.25
    surprise: float = 0.20
    relevance: float = 0.25
    connectivity: float = 0.10
    access_frequency: float = 0.10
    emotional_intensity: float = 0.10

class SalienceScorer:
    """
    Computes multi-factor salience scores for memory nodes.

    Salience determines which memories surface during retrieval,
    moving beyond pure recency to include surprise, relevance,
    and structural importance.
    """

    def __init__(
        self,
        weights: SalienceWeights = None,
        world_model = None,
        memory = None,
        half_life_hours: float = 24.0
    ):
        self.weights = weights or SalienceWeights()
        self.world_model = world_model
        self.memory = memory
        self.half_life_hours = half_life_hours

        # Track access patterns
        self._access_counts: Dict[str, int] = {}
        self._last_access: Dict[str, float] = {}

        # Current context (updated by Seeker/Omega)
        self._current_goals: List[str] = []
        self._current_focus: str = ""

    def set_context(self, goals: List[str], focus: str = ""):
        """Update current context for relevance scoring."""
        self._current_goals = goals
        self._current_focus = focus

    def record_access(self, node_id: str):
        """Track that a node was accessed."""
        self._access_counts[node_id] = self._access_counts.get(node_id, 0) + 1
        self._last_access[node_id] = time.time()

    async def compute_salience(
        self,
        node: Dict[str, Any],
        query_embedding: Optional[List[float]] = None
    ) -> float:
        """
        Compute composite salience score for a memory node.

        Returns score in [0, 1] range.
        """
        factors = await self._compute_factors(node, query_embedding)

        # Weighted sum
        score = (
            self.weights.recency * factors.recency +
            self.weights.surprise * factors.surprise +
            self.weights.relevance * factors.relevance +
            self.weights.connectivity * factors.connectivity +
            self.weights.access_frequency * factors.access_frequency +
            self.weights.emotional_intensity * factors.emotional_intensity
        )

        return min(1.0, max(0.0, score))

    async def _compute_factors(
        self,
        node: Dict[str, Any],
        query_embedding: Optional[List[float]] = None
    ) -> SalienceFactors:
        """Compute individual salience factors."""

        factors = SalienceFactors()

        # 1. Recency (exponential decay)
        timestamp = node.get("timestamp") or node.get("created_at")
        if timestamp:
            age_hours = (time.time() - timestamp) / 3600
            factors.recency = math.exp(-age_hours / self.half_life_hours)

        # 2. Surprise (prediction error from world model)
        if self.world_model and node.get("type") == "Experience":
            try:
                # Check if this experience was predicted
                prediction_accuracy = await self._get_prediction_accuracy(node)
                # Higher surprise = lower prediction accuracy
                factors.surprise = 1.0 - prediction_accuracy
            except Exception:
                factors.surprise = 0.5  # Neutral if unknown

        # 3. Relevance (to current goals)
        content = node.get("content") or node.get("description") or ""
        if self._current_goals and content:
            relevance_scores = []
            for goal in self._current_goals:
                # Simple keyword overlap (could enhance with embeddings)
                overlap = self._keyword_overlap(content, goal)
                relevance_scores.append(overlap)
            factors.relevance = max(relevance_scores) if relevance_scores else 0.0

        # 4. Connectivity (graph degree)
        node_id = node.get("id") or node.get("node_id")
        if node_id and self.memory:
            try:
                degree = await self._get_node_degree(node_id)
                # Normalize (assume max ~100 connections)
                factors.connectivity = min(1.0, degree / 100.0)
            except Exception:
                factors.connectivity = 0.1

        # 5. Access frequency
        if node_id:
            count = self._access_counts.get(node_id, 0)
            # Logarithmic scaling (diminishing returns)
            factors.access_frequency = min(1.0, math.log1p(count) / 5.0)

        # 6. Emotional intensity (sentiment magnitude)
        if content:
            factors.emotional_intensity = self._estimate_intensity(content)

        return factors

    async def _get_prediction_accuracy(self, node: Dict) -> float:
        """Check if this experience was accurately predicted."""
        if not self.world_model:
            return 0.5

        # Look for prediction that referenced this experience
        # This requires prediction->outcome tracking in world model
        return 0.5  # Placeholder - integrate with world_model.py Line 377

    async def _get_node_degree(self, node_id: str) -> int:
        """Get number of relationships for a node."""
        if not self.memory:
            return 1

        result = await self.memory._run_query(
            "MATCH (n)-[r]-() WHERE n.id = $node_id RETURN count(r) as degree",
            {"node_id": node_id}
        )
        if result:
            return result[0].get("degree", 1)
        return 1

    def _keyword_overlap(self, text1: str, text2: str) -> float:
        """Simple keyword overlap relevance."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # Remove stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and', 'or'}
        words1 = words1 - stopwords
        words2 = words2 - stopwords

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _estimate_intensity(self, content: str) -> float:
        """Estimate emotional intensity from text."""
        # Simple heuristic: exclamation marks, caps, strong words
        intensity = 0.0

        # Exclamation marks
        intensity += min(0.3, content.count('!') * 0.1)

        # Caps ratio (but not all caps)
        caps = sum(1 for c in content if c.isupper())
        total = len(content)
        if total > 0:
            caps_ratio = caps / total
            if 0.1 < caps_ratio < 0.5:
                intensity += 0.2

        # Strong words
        strong_words = [
            'critical', 'urgent', 'important', 'must', 'need',
            'breakthrough', 'discovery', 'failure', 'success',
            'amazing', 'terrible', 'essential', 'fundamental'
        ]
        content_lower = content.lower()
        for word in strong_words:
            if word in content_lower:
                intensity += 0.1

        return min(1.0, intensity)
```

**Integrate into `memory_reasoner.py`** (Lines 248, 262):

```python
# Add import at top
from salience import SalienceScorer

# Add to MemoryReasoner.__init__ (after Line 108)
def __init__(self, memory, llm_client, config: Dict = None, ...):
    # ... existing init ...

    # Initialize salience scorer
    self.salience_scorer = SalienceScorer(
        world_model=self.world_model,
        memory=self.memory,
        half_life_hours=config.get("salience_half_life_hours", 24.0)
    )

# Modify _find_seed_nodes (around Line 248)
async def _find_seed_nodes(
    self,
    query_embedding: List[float],
    query_text: str = ""
) -> List[ActivatedNode]:
    # ... existing similarity search ...

    # REPLACE line 248:
    # OLD: base_activation = node["similarity"]
    # NEW:
    salience = await self.salience_scorer.compute_salience(
        node,
        query_embedding=query_embedding
    )
    base_activation = node["similarity"] * (0.5 + 0.5 * salience)
    # This blends similarity with salience (similarity still matters, but salience modulates)

    # Track access for future salience
    self.salience_scorer.record_access(node.get("id"))

    # ... rest of method ...
```

---

### 1.3 Tiered Reflection System (Micro-Reflections)

**Purpose**: Add fast 10-second micro-reflections between full 120-second cycles.

**Files to Modify**:
- `dreamer.py` (primary)
- `config.yaml` (configuration)

**Integration Point**: New method called alongside existing `dream_cycle()`.

**Implementation**:

```python
# Add to dreamer.py after Line 150 (inside Dreamer class)

class Dreamer:
    def __init__(self, memory, llm_client, ...):
        # ... existing init ...

        # Micro-reflection configuration
        self._micro_interval = config.get("micro_reflection_interval", 10)
        self._last_micro = time.time()
        self._micro_buffer: List[Dict] = []  # Recent experiences for micro-reflection
        self._micro_buffer_size = 3

        # Deep reflection configuration
        self._deep_interval = config.get("deep_reflection_interval", 300)
        self._last_deep = time.time()

    async def micro_reflect(self) -> Optional[Dict]:
        """
        Fast micro-reflection on recent experiences.

        Called every 10 seconds. Produces quick belief updates
        without full context retrieval.

        Returns None if buffer empty or nothing to reflect on.
        """
        if len(self._micro_buffer) < 1:
            return None

        # Minimal prompt for speed
        experiences_text = "\n".join([
            f"- {exp.get('content', '')[:200]}"
            for exp in self._micro_buffer[-3:]
        ])

        prompt = f"""[MICRO-REFLECTION]
Recent experiences:
{experiences_text}

Quick assessment - any belief updates? JSON only:
{{"belief_updates": [{{"belief": "...", "delta": 0.1}}], "priority_shift": null}}"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.3,  # Lower temperature for consistency
                max_tokens=200,   # Short response
                operation="micro_reflect"
            )

            result = self._parse_json_response(response)

            # Apply belief updates immediately
            if result and result.get("belief_updates"):
                for update in result["belief_updates"]:
                    await self._apply_belief_update(update)

            # Clear processed experiences
            self._micro_buffer = self._micro_buffer[-1:]  # Keep most recent

            return result

        except Exception as e:
            print(f"⚡ Micro-reflection error: {e}")
            return None

    async def _apply_belief_update(self, update: Dict):
        """Apply incremental belief confidence update."""
        belief_content = update.get("belief", "")
        delta = update.get("delta", 0.0)

        if not belief_content or abs(delta) < 0.01:
            return

        # Find existing belief or create new
        existing = await self.memory.find_belief_by_content(belief_content)

        if existing:
            new_confidence = min(1.0, max(0.0, existing["confidence"] + delta))
            await self.memory.update_belief_confidence(existing["id"], new_confidence)
        elif delta > 0:
            # Only create new beliefs if positive delta
            await self.memory.create_belief(
                content=belief_content,
                confidence=min(1.0, 0.5 + delta),  # Start at 0.5 + delta
                source="micro_reflection"
            )

    def add_to_micro_buffer(self, experience: Dict):
        """Add experience to micro-reflection buffer."""
        self._micro_buffer.append(experience)
        if len(self._micro_buffer) > self._micro_buffer_size * 2:
            self._micro_buffer = self._micro_buffer[-self._micro_buffer_size:]

    async def deep_reflect(self) -> Optional[Dict]:
        """
        Comprehensive deep reflection with full context.

        Called every 5 minutes. Full architectural introspection,
        meta-learning, cross-domain synthesis.
        """
        # Get extensive context
        recent = await self.memory.get_recent_experiences(limit=50)
        beliefs = await self.memory.get_all_beliefs(limit=30)
        goals = await self.memory.get_active_goals(limit=10)

        # Get OS state
        os_state = await self.memory.get_operating_system()

        prompt = f"""[DEEP REFLECTION - ARCHITECTURAL INTROSPECTION]

Current Operating System State:
{self._format_os(os_state)}

Active Goals:
{self._format_goals(goals)}

Recent Beliefs (last 30):
{self._format_beliefs(beliefs)}

Recent Experiences (last 50):
{self._format_experiences(recent)}

DEEP ANALYSIS REQUIRED:
1. Are my beliefs internally consistent? Identify contradictions.
2. What patterns do I see across multiple experiences?
3. What am I failing to notice or remember?
4. How should my priorities shift?
5. What meta-learning insights emerge?

Output comprehensive JSON:
{{
  "contradictions": [...],
  "cross_domain_patterns": [...],
  "blind_spots": [...],
  "priority_adjustments": [...],
  "meta_insights": [...],
  "os_updates": {{}}
}}"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.7,
                max_tokens=1500,
                operation="deep_reflect",
                bypass_cache=True  # Always fresh for deep reflection
            )

            result = self._parse_json_response(response)

            # Process results
            if result:
                await self._process_deep_reflection(result)

            return result

        except Exception as e:
            print(f"🌊 Deep reflection error: {e}")
            return None

    async def _process_deep_reflection(self, result: Dict):
        """Process and store deep reflection insights."""

        # Store contradictions for resolution
        for contradiction in result.get("contradictions", []):
            await self.memory.create_experience(
                content=f"CONTRADICTION DETECTED: {contradiction}",
                exp_type="meta_insight",
                metadata={"source": "deep_reflection", "category": "contradiction"}
            )

        # Store meta-insights
        for insight in result.get("meta_insights", []):
            await self.memory.create_insight(
                content=insight,
                source="deep_reflection",
                confidence=0.7
            )

        # Apply OS updates
        os_updates = result.get("os_updates", {})
        if os_updates:
            await self.memory.update_operating_system(os_updates)

# Modify the main dreamer loop (around Line 557-646)
async def run(self):
    """Main dreamer loop with tiered reflections."""
    self._running = True

    while self._running:
        now = time.time()

        # Micro-reflection (every 10s)
        if now - self._last_micro >= self._micro_interval:
            await self.micro_reflect()
            self._last_micro = now

        # Standard reflection (every 120s) - existing logic
        if now - self._last_reflection >= self.interval_seconds:
            await self.dream_cycle()
            self._last_reflection = now

        # Deep reflection (every 300s)
        if now - self._last_deep >= self._deep_interval:
            await self.deep_reflect()
            self._last_deep = now

        await asyncio.sleep(1)  # Check every second
```

**Config addition**:

```yaml
dreamer:
  interval_seconds: 120
  micro_reflection_interval: 10
  deep_reflection_interval: 300
```

---

## PHASE 2: LOOP COUPLING (Depends on Phase 1)

### 2.1 Explicit Loop Coupling System

**Purpose**: Create explicit data flows between the five compounding loops.

**Files to Modify**:
- NEW: `loop_coupling.py`
- `omega.py` (Lines 299-377)
- `goal_evolver.py` (Lines 600)
- `dreaming_machine.py` (Lines 288, 552)
- `memory_reasoner.py` (Lines 178)

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/loop_coupling.py

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Awaitable
from enum import Enum
import asyncio
import time

class LoopType(Enum):
    MEMORY_REASONER = "memory_reasoner"
    SELF_COMPILER = "self_compiler"
    GOAL_EVOLVER = "goal_evolver"
    DREAMING_MACHINE = "dreaming_machine"
    OMEGA = "omega"

@dataclass
class CouplingEvent:
    """Event passed between loops."""
    source: LoopType
    target: LoopType
    event_type: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    priority: int = 1  # 1-5, higher = more urgent

@dataclass
class CouplingMetrics:
    """Track coupling strength between loops."""
    events_sent: int = 0
    events_received: int = 0
    successful_handoffs: int = 0
    failed_handoffs: int = 0
    avg_latency_ms: float = 0.0
    last_event_time: float = 0.0

class LoopCoupler:
    """
    Manages explicit data flow between BYRD's five compounding loops.

    Coupling Types:
    1. Goal Evolver -> Self-Compiler: Successful goals drive pattern codification
    2. Self-Compiler -> Memory Reasoner: New patterns become retrievable
    3. Memory Reasoner -> Dreaming Machine: Answered queries seed counterfactuals
    4. Dreaming Machine -> Goal Evolver: Counterfactual insights propose goals
    5. Omega -> All: Mode transitions affect all loops
    """

    def __init__(self):
        self._queues: Dict[LoopType, asyncio.Queue] = {
            loop: asyncio.Queue(maxsize=100) for loop in LoopType
        }

        self._handlers: Dict[LoopType, Dict[str, Callable]] = {
            loop: {} for loop in LoopType
        }

        self._metrics: Dict[tuple, CouplingMetrics] = {}

        # Define expected couplings
        self._expected_couplings = [
            (LoopType.GOAL_EVOLVER, LoopType.SELF_COMPILER),
            (LoopType.SELF_COMPILER, LoopType.MEMORY_REASONER),
            (LoopType.MEMORY_REASONER, LoopType.DREAMING_MACHINE),
            (LoopType.DREAMING_MACHINE, LoopType.GOAL_EVOLVER),
        ]

        for source, target in self._expected_couplings:
            self._metrics[(source, target)] = CouplingMetrics()

    def register_handler(
        self,
        loop: LoopType,
        event_type: str,
        handler: Callable[[CouplingEvent], Awaitable[bool]]
    ):
        """Register a handler for incoming events to a loop."""
        self._handlers[loop][event_type] = handler

    async def emit(self, event: CouplingEvent):
        """Emit an event to target loop."""
        try:
            await self._queues[event.target].put(event)

            # Update metrics
            key = (event.source, event.target)
            if key in self._metrics:
                self._metrics[key].events_sent += 1
                self._metrics[key].last_event_time = time.time()

        except asyncio.QueueFull:
            print(f"⚠️ Coupling queue full: {event.source} -> {event.target}")

    async def process_events(self, loop: LoopType, max_events: int = 10) -> int:
        """Process pending events for a loop. Returns count processed."""
        processed = 0

        while processed < max_events:
            try:
                event = self._queues[loop].get_nowait()
            except asyncio.QueueEmpty:
                break

            handler = self._handlers[loop].get(event.event_type)
            if handler:
                try:
                    start = time.time()
                    success = await handler(event)
                    latency = (time.time() - start) * 1000

                    key = (event.source, event.target)
                    if key in self._metrics:
                        self._metrics[key].events_received += 1
                        if success:
                            self._metrics[key].successful_handoffs += 1
                        else:
                            self._metrics[key].failed_handoffs += 1
                        # Running average latency
                        n = self._metrics[key].events_received
                        old_avg = self._metrics[key].avg_latency_ms
                        self._metrics[key].avg_latency_ms = old_avg + (latency - old_avg) / n

                except Exception as e:
                    print(f"⚠️ Coupling handler error: {e}")
                    key = (event.source, event.target)
                    if key in self._metrics:
                        self._metrics[key].failed_handoffs += 1

            processed += 1

        return processed

    def get_coupling_strength(self, source: LoopType, target: LoopType) -> float:
        """
        Get coupling strength (0-1) between two loops.
        Based on successful handoffs / total events.
        """
        key = (source, target)
        if key not in self._metrics:
            return 0.0

        m = self._metrics[key]
        total = m.events_sent
        if total == 0:
            return 0.0

        return m.successful_handoffs / total

    def get_critical_coupling(self) -> float:
        """
        Get the critical coupling metric.
        This is Goal Evolver -> Self-Compiler (goals driving codification).
        """
        return self.get_coupling_strength(
            LoopType.GOAL_EVOLVER,
            LoopType.SELF_COMPILER
        )

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all coupling metrics."""
        return {
            f"{s.value}->{t.value}": {
                "strength": self.get_coupling_strength(s, t),
                "events_sent": self._metrics[(s, t)].events_sent,
                "successful": self._metrics[(s, t)].successful_handoffs,
                "failed": self._metrics[(s, t)].failed_handoffs,
                "avg_latency_ms": self._metrics[(s, t)].avg_latency_ms
            }
            for s, t in self._expected_couplings
        }


# Coupling event creators (convenience functions)
def goal_success_event(goal_id: str, description: str, outcome: Dict) -> CouplingEvent:
    """Create event when a goal succeeds (Goal Evolver -> Self-Compiler)."""
    return CouplingEvent(
        source=LoopType.GOAL_EVOLVER,
        target=LoopType.SELF_COMPILER,
        event_type="goal_success",
        payload={
            "goal_id": goal_id,
            "description": description,
            "outcome": outcome,
            "pattern_candidate": True
        },
        priority=3
    )

def pattern_codified_event(pattern_id: str, pattern: Dict) -> CouplingEvent:
    """Create event when a pattern is codified (Self-Compiler -> Memory Reasoner)."""
    return CouplingEvent(
        source=LoopType.SELF_COMPILER,
        target=LoopType.MEMORY_REASONER,
        event_type="pattern_codified",
        payload={
            "pattern_id": pattern_id,
            "pattern": pattern,
            "should_index": True
        },
        priority=2
    )

def memory_answer_event(query: str, answer: str, confidence: float) -> CouplingEvent:
    """Create event when memory answers a query (Memory Reasoner -> Dreaming Machine)."""
    return CouplingEvent(
        source=LoopType.MEMORY_REASONER,
        target=LoopType.DREAMING_MACHINE,
        event_type="memory_answered",
        payload={
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "counterfactual_seed": confidence < 0.8  # Low confidence = good counterfactual seed
        },
        priority=1
    )

def counterfactual_insight_event(insight: str, proposed_goal: Optional[str]) -> CouplingEvent:
    """Create event when counterfactual generates insight (Dreaming Machine -> Goal Evolver)."""
    return CouplingEvent(
        source=LoopType.DREAMING_MACHINE,
        target=LoopType.GOAL_EVOLVER,
        event_type="counterfactual_insight",
        payload={
            "insight": insight,
            "proposed_goal": proposed_goal,
            "should_evaluate": proposed_goal is not None
        },
        priority=2
    )
```

**Integrate into `omega.py`** (around Lines 299-377):

```python
# Add import
from loop_coupling import LoopCoupler, LoopType

# Add to Omega.__init__ (after Line 107)
def __init__(self, ...):
    # ... existing init ...
    self.coupler = LoopCoupler()
    self._register_coupling_handlers()

def _register_coupling_handlers(self):
    """Register handlers for each loop to process coupling events."""

    # Self-Compiler handles goal success events
    self.coupler.register_handler(
        LoopType.SELF_COMPILER,
        "goal_success",
        self._handle_goal_success_for_compiler
    )

    # Memory Reasoner handles pattern codified events
    self.coupler.register_handler(
        LoopType.MEMORY_REASONER,
        "pattern_codified",
        self._handle_pattern_for_reasoner
    )

    # Dreaming Machine handles memory answer events
    self.coupler.register_handler(
        LoopType.DREAMING_MACHINE,
        "memory_answered",
        self._handle_memory_for_dreamer
    )

    # Goal Evolver handles counterfactual insight events
    self.coupler.register_handler(
        LoopType.GOAL_EVOLVER,
        "counterfactual_insight",
        self._handle_insight_for_evolver
    )

async def _handle_goal_success_for_compiler(self, event: CouplingEvent) -> bool:
    """Extract pattern from successful goal for Self-Compiler."""
    if not self.self_compiler:
        return False

    try:
        pattern = await self.self_compiler.extract_pattern_from_success(
            goal_description=event.payload["description"],
            outcome=event.payload["outcome"]
        )
        return pattern is not None
    except Exception as e:
        print(f"⚠️ Pattern extraction failed: {e}")
        return False

async def _handle_pattern_for_reasoner(self, event: CouplingEvent) -> bool:
    """Index new pattern in Memory Reasoner."""
    if not self.memory_reasoner:
        return False

    try:
        await self.memory_reasoner.index_pattern(event.payload["pattern"])
        return True
    except Exception as e:
        print(f"⚠️ Pattern indexing failed: {e}")
        return False

async def _handle_memory_for_dreamer(self, event: CouplingEvent) -> bool:
    """Use memory answer as counterfactual seed."""
    if not self.dreaming_machine:
        return False

    if event.payload.get("counterfactual_seed"):
        try:
            await self.dreaming_machine.queue_counterfactual_seed(
                query=event.payload["query"],
                answer=event.payload["answer"]
            )
            return True
        except Exception:
            pass
    return False

async def _handle_insight_for_evolver(self, event: CouplingEvent) -> bool:
    """Propose new goal from counterfactual insight."""
    if not self.goal_evolver:
        return False

    proposed = event.payload.get("proposed_goal")
    if proposed:
        try:
            await self.goal_evolver.propose_goal_from_insight(
                insight=event.payload["insight"],
                proposed_goal=proposed
            )
            return True
        except Exception:
            pass
    return False

# Modify run_cycle (around Line 299)
async def run_cycle(self) -> Dict[str, Any]:
    """Coordinates all loops with explicit coupling."""

    # Process coupling events for each loop before running
    for loop_type in LoopType:
        await self.coupler.process_events(loop_type, max_events=5)

    # ... existing mode-based execution ...

    # After cycle, report coupling metrics
    results["coupling"] = self.coupler.get_all_metrics()
    results["critical_coupling"] = self.coupler.get_critical_coupling()

    return results
```

---

### 2.2 Tighter Prediction->Outcome Loop

**Purpose**: Immediate prediction verification instead of batched consolidation.

**Files to Modify**:
- `world_model.py` (Lines 377-443)
- `seeker.py` (action execution)
- NEW: `prediction_tracker.py`

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/prediction_tracker.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time
import uuid

@dataclass
class PendingPrediction:
    """A prediction awaiting verification."""
    id: str
    action: str
    context: Dict
    predicted_outcome: str
    predicted_success: float
    timestamp: float
    timeout_seconds: float = 60.0

    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > self.timeout_seconds

@dataclass
class VerifiedPrediction:
    """A prediction that has been verified against reality."""
    prediction: PendingPrediction
    actual_outcome: str
    actual_success: bool
    error: float
    verification_time: float

class PredictionTracker:
    """
    Tracks predictions and enables immediate verification.

    Flow:
    1. Before action: world_model.predict() creates PendingPrediction
    2. Action executes
    3. After action: verify() compares prediction to reality
    4. Immediate learning: update_from_error() if error > threshold
    """

    def __init__(self, world_model, error_threshold: float = 0.3):
        self.world_model = world_model
        self.error_threshold = error_threshold

        self._pending: Dict[str, PendingPrediction] = {}
        self._verified: List[VerifiedPrediction] = []

        # Metrics
        self._total_predictions = 0
        self._verified_count = 0
        self._high_error_count = 0
        self._total_error = 0.0

    async def predict_and_track(
        self,
        action: str,
        context: Dict = None,
        timeout_seconds: float = 60.0
    ) -> str:
        """
        Make prediction and track it for verification.
        Returns prediction_id for later verification.
        """
        prediction = await self.world_model.predict_outcome(action, context)

        pred_id = str(uuid.uuid4())[:8]
        pending = PendingPrediction(
            id=pred_id,
            action=action,
            context=context or {},
            predicted_outcome=prediction.predicted_outcome,
            predicted_success=prediction.success_probability,
            timestamp=time.time(),
            timeout_seconds=timeout_seconds
        )

        self._pending[pred_id] = pending
        self._total_predictions += 1

        return pred_id

    async def verify(
        self,
        prediction_id: str,
        actual_outcome: str,
        actual_success: bool
    ) -> Optional[VerifiedPrediction]:
        """
        Verify a prediction against actual outcome.
        Triggers immediate learning if error exceeds threshold.
        """
        if prediction_id not in self._pending:
            return None

        pending = self._pending.pop(prediction_id)

        if pending.is_expired():
            return None

        # Calculate error
        error = abs(pending.predicted_success - (1.0 if actual_success else 0.0))

        verified = VerifiedPrediction(
            prediction=pending,
            actual_outcome=actual_outcome,
            actual_success=actual_success,
            error=error,
            verification_time=time.time()
        )

        self._verified.append(verified)
        self._verified_count += 1
        self._total_error += error

        # IMMEDIATE learning if high error
        if error > self.error_threshold:
            self._high_error_count += 1
            await self._trigger_immediate_learning(verified)

        # Keep verified list bounded
        if len(self._verified) > 1000:
            self._verified = self._verified[-500:]

        return verified

    async def _trigger_immediate_learning(self, verified: VerifiedPrediction):
        """
        Trigger immediate causal learning from prediction error.
        This is the key to tight feedback loops.
        """
        try:
            # Create a mock OutcomePrediction for the world model
            from world_model import OutcomePrediction

            mock_prediction = OutcomePrediction(
                predicted_outcome=verified.prediction.predicted_outcome,
                success_probability=verified.prediction.predicted_success,
                confidence=0.5,
                reasoning="",
                similar_cases=[]
            )

            # Trigger world model learning
            await self.world_model.update_from_prediction_error(
                prediction=mock_prediction,
                actual_outcome=verified.actual_outcome,
                actual_success=verified.actual_success
            )

            print(f"🎯 Immediate learning triggered: error={verified.error:.2f}")

        except Exception as e:
            print(f"⚠️ Immediate learning failed: {e}")

    def cleanup_expired(self):
        """Remove expired pending predictions."""
        expired = [
            pid for pid, pred in self._pending.items()
            if pred.is_expired()
        ]
        for pid in expired:
            del self._pending[pid]

    def get_metrics(self) -> Dict[str, Any]:
        """Get prediction tracking metrics."""
        return {
            "total_predictions": self._total_predictions,
            "verified": self._verified_count,
            "pending": len(self._pending),
            "high_error_count": self._high_error_count,
            "avg_error": self._total_error / self._verified_count if self._verified_count > 0 else 0.0,
            "accuracy": 1.0 - (self._total_error / self._verified_count) if self._verified_count > 0 else 0.0
        }
```

---

## PHASE 3: ACTIVE SYSTEMS (Depends on Phase 2)

### 3.1 Active Information Seeking

**Purpose**: BYRD proactively seeks information instead of passively waiting.

**Files to Modify**:
- NEW: `information_seeker.py`
- `seeker.py` (integration)
- `memory.py` (knowledge gap queries)

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/information_seeker.py

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import time

class GapType(Enum):
    LOW_CONFIDENCE_BELIEF = "low_confidence_belief"
    UNCERTAIN_CAPABILITY = "uncertain_capability"
    BLOCKED_GOAL = "blocked_goal"
    PREDICTION_FAILURE = "prediction_failure"
    MISSING_PREREQUISITE = "missing_prerequisite"

@dataclass
class KnowledgeGap:
    """A gap in BYRD's knowledge that should be filled."""
    gap_type: GapType
    topic: str
    importance: float  # 0-1
    context: Dict[str, Any]
    identified_at: float = 0.0

    def __post_init__(self):
        if self.identified_at == 0.0:
            self.identified_at = time.time()

class InformationSeeker:
    """
    Proactively identifies and seeks to fill knowledge gaps.

    This transforms BYRD from passive (processes what it sees)
    to active (seeks what it needs).
    """

    def __init__(
        self,
        memory,
        world_model = None,
        capability_evaluator = None,
        goal_evolver = None,
        config: Dict = None
    ):
        self.memory = memory
        self.world_model = world_model
        self.capability_evaluator = capability_evaluator
        self.goal_evolver = goal_evolver

        config = config or {}
        self.low_confidence_threshold = config.get("low_confidence_threshold", 0.5)
        self.high_uncertainty_threshold = config.get("high_uncertainty_threshold", 0.3)
        self.max_gaps_per_cycle = config.get("max_gaps_per_cycle", 5)

        self._identified_gaps: List[KnowledgeGap] = []
        self._seeking_queue: List[KnowledgeGap] = []

    async def identify_knowledge_gaps(self) -> List[KnowledgeGap]:
        """
        Scan BYRD's knowledge for gaps that should be filled.
        Returns prioritized list of gaps.
        """
        gaps = []

        # 1. Low-confidence beliefs
        low_conf_beliefs = await self._find_low_confidence_beliefs()
        gaps.extend(low_conf_beliefs)

        # 2. High-uncertainty capabilities
        uncertain_caps = await self._find_uncertain_capabilities()
        gaps.extend(uncertain_caps)

        # 3. Blocked goals
        blocked = await self._find_blocked_goals()
        gaps.extend(blocked)

        # 4. Recent prediction failures
        pred_failures = await self._find_prediction_failures()
        gaps.extend(pred_failures)

        # Sort by importance
        gaps.sort(key=lambda g: g.importance, reverse=True)

        self._identified_gaps = gaps[:self.max_gaps_per_cycle]
        return self._identified_gaps

    async def _find_low_confidence_beliefs(self) -> List[KnowledgeGap]:
        """Find beliefs with low confidence that need strengthening."""
        gaps = []

        beliefs = await self.memory.get_beliefs_by_confidence(
            max_confidence=self.low_confidence_threshold,
            limit=10
        )

        for belief in beliefs:
            # Check if belief is important (has many connections)
            connections = await self.memory.count_connections(belief["id"])

            if connections >= 3:  # Important belief
                gaps.append(KnowledgeGap(
                    gap_type=GapType.LOW_CONFIDENCE_BELIEF,
                    topic=belief.get("content", "")[:100],
                    importance=0.7 + (1.0 - belief.get("confidence", 0.5)) * 0.3,
                    context={
                        "belief_id": belief["id"],
                        "current_confidence": belief.get("confidence"),
                        "connections": connections
                    }
                ))

        return gaps

    async def _find_uncertain_capabilities(self) -> List[KnowledgeGap]:
        """Find capabilities with high uncertainty."""
        gaps = []

        if not self.capability_evaluator:
            return gaps

        capabilities = await self.capability_evaluator.get_all_capabilities()

        for cap in capabilities:
            uncertainty = cap.get("uncertainty", 0.0)
            if uncertainty > self.high_uncertainty_threshold:
                gaps.append(KnowledgeGap(
                    gap_type=GapType.UNCERTAIN_CAPABILITY,
                    topic=f"capability: {cap.get('name', 'unknown')}",
                    importance=0.5 + uncertainty * 0.5,
                    context={
                        "capability_name": cap.get("name"),
                        "uncertainty": uncertainty,
                        "last_tested": cap.get("last_tested")
                    }
                ))

        return gaps

    async def _find_blocked_goals(self) -> List[KnowledgeGap]:
        """Find goals that are blocked by missing information."""
        gaps = []

        if not self.goal_evolver:
            return gaps

        goals = await self.goal_evolver.get_blocked_goals()

        for goal in goals:
            blocker = goal.get("blocker", "unknown reason")
            gaps.append(KnowledgeGap(
                gap_type=GapType.BLOCKED_GOAL,
                topic=f"unblock: {goal.get('description', '')[:50]}",
                importance=0.8,  # Blocked goals are high priority
                context={
                    "goal_id": goal.get("id"),
                    "blocker": blocker,
                    "goal_description": goal.get("description")
                }
            ))

        return gaps

    async def _find_prediction_failures(self) -> List[KnowledgeGap]:
        """Find areas where predictions consistently fail."""
        gaps = []

        if not self.world_model:
            return gaps

        # Get recent prediction errors
        errors = await self.world_model.get_recent_errors(limit=10)

        # Group by topic/action type
        error_topics: Dict[str, List] = {}
        for error in errors:
            topic = error.get("action_type", "general")
            if topic not in error_topics:
                error_topics[topic] = []
            error_topics[topic].append(error)

        # Create gaps for topics with multiple errors
        for topic, topic_errors in error_topics.items():
            if len(topic_errors) >= 2:
                avg_error = sum(e.get("error", 0) for e in topic_errors) / len(topic_errors)
                gaps.append(KnowledgeGap(
                    gap_type=GapType.PREDICTION_FAILURE,
                    topic=f"prediction failures in: {topic}",
                    importance=0.6 + avg_error * 0.4,
                    context={
                        "topic": topic,
                        "error_count": len(topic_errors),
                        "avg_error": avg_error
                    }
                ))

        return gaps

    async def create_seeking_desires(self) -> List[Dict]:
        """
        Convert knowledge gaps into desires that can be pursued.
        Returns list of desire dicts.
        """
        desires = []

        for gap in self._identified_gaps:
            desire_content = self._gap_to_desire_content(gap)

            desires.append({
                "content": desire_content,
                "intensity": gap.importance,
                "type": "information_seeking",
                "metadata": {
                    "gap_type": gap.gap_type.value,
                    "topic": gap.topic,
                    "context": gap.context
                }
            })

        return desires

    def _gap_to_desire_content(self, gap: KnowledgeGap) -> str:
        """Convert knowledge gap to natural language desire."""
        if gap.gap_type == GapType.LOW_CONFIDENCE_BELIEF:
            return f"Seek evidence to strengthen or refute belief: {gap.topic}"

        elif gap.gap_type == GapType.UNCERTAIN_CAPABILITY:
            return f"Test and improve capability: {gap.context.get('capability_name', gap.topic)}"

        elif gap.gap_type == GapType.BLOCKED_GOAL:
            return f"Find way to unblock goal: {gap.context.get('goal_description', gap.topic)[:50]}"

        elif gap.gap_type == GapType.PREDICTION_FAILURE:
            return f"Understand why predictions fail for: {gap.topic}"

        else:
            return f"Investigate: {gap.topic}"
```

---

### 3.2 Contradiction Detection and Resolution

**Purpose**: Automatically detect and resolve conflicting beliefs.

**Files to Modify**:
- NEW: `contradiction_resolver.py`
- `memory.py` (contradiction queries)
- `dreamer.py` (integration with deep reflection)

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/contradiction_resolver.py

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import asyncio
import time

class ResolutionStrategy(Enum):
    EVIDENCE_WEIGHT = "evidence_weight"       # Belief with more evidence wins
    RECENCY = "recency"                       # More recent belief wins
    CONFIDENCE_MERGE = "confidence_merge"     # Adjust confidences proportionally
    CREATE_UNCERTAINTY = "create_uncertainty" # Create meta-belief about uncertainty
    DEFER_TO_LLM = "defer_to_llm"            # Ask LLM to resolve

@dataclass
class Contradiction:
    """A detected contradiction between beliefs."""
    belief_a_id: str
    belief_a_content: str
    belief_a_confidence: float
    belief_b_id: str
    belief_b_content: str
    belief_b_confidence: float
    similarity_score: float  # How similar the topics are
    contradiction_type: str  # e.g., "direct_negation", "incompatible_values"

@dataclass
class Resolution:
    """Result of resolving a contradiction."""
    contradiction: Contradiction
    strategy_used: ResolutionStrategy
    winner: Optional[str]  # belief_id of winner, or None if merged/uncertain
    actions_taken: List[str]
    new_confidence_a: Optional[float]
    new_confidence_b: Optional[float]

class ContradictionResolver:
    """
    Detects and resolves contradictions in BYRD's belief system.

    Philosophy: Contradictions are valuable signals. They indicate
    either (1) learning in progress, (2) context-dependent truths,
    or (3) errors to correct.
    """

    def __init__(
        self,
        memory,
        llm_client = None,
        config: Dict = None
    ):
        self.memory = memory
        self.llm_client = llm_client

        config = config or {}
        self.similarity_threshold = config.get("similarity_threshold", 0.7)
        self.auto_resolve_threshold = config.get("auto_resolve_threshold", 2.0)
        self.evidence_ratio_threshold = config.get("evidence_ratio_threshold", 2.0)

        self._detected: List[Contradiction] = []
        self._resolved: List[Resolution] = []

    async def detect_contradictions(self) -> List[Contradiction]:
        """
        Scan belief system for contradictions.
        Uses semantic similarity + negation detection.
        """
        contradictions = []

        # Get all beliefs
        beliefs = await self.memory.get_all_beliefs()

        # Pairwise comparison (O(n^2) but beliefs are bounded)
        for i, b1 in enumerate(beliefs):
            for b2 in beliefs[i+1:]:
                is_contradiction, cont_type = await self._check_contradiction(b1, b2)

                if is_contradiction:
                    similarity = await self._semantic_similarity(
                        b1.get("content", ""),
                        b2.get("content", "")
                    )

                    contradictions.append(Contradiction(
                        belief_a_id=b1["id"],
                        belief_a_content=b1.get("content", ""),
                        belief_a_confidence=b1.get("confidence", 0.5),
                        belief_b_id=b2["id"],
                        belief_b_content=b2.get("content", ""),
                        belief_b_confidence=b2.get("confidence", 0.5),
                        similarity_score=similarity,
                        contradiction_type=cont_type
                    ))

        self._detected = contradictions
        return contradictions

    async def _check_contradiction(
        self,
        belief_a: Dict,
        belief_b: Dict
    ) -> Tuple[bool, str]:
        """
        Check if two beliefs contradict each other.
        Returns (is_contradiction, type).
        """
        content_a = belief_a.get("content", "").lower()
        content_b = belief_b.get("content", "").lower()

        # Direct negation patterns
        negation_pairs = [
            ("is ", "is not "),
            ("can ", "cannot "),
            ("will ", "will not "),
            ("should ", "should not "),
            ("always ", "never "),
            ("true", "false"),
        ]

        for pos, neg in negation_pairs:
            # Check if one has positive and other has negative
            if (pos in content_a and neg in content_b) or \
               (neg in content_a and pos in content_b):
                # Check topic similarity
                similarity = await self._semantic_similarity(content_a, content_b)
                if similarity > self.similarity_threshold:
                    return True, "direct_negation"

        # Use LLM for subtle contradictions if available
        if self.llm_client:
            try:
                result = await self._llm_contradiction_check(content_a, content_b)
                if result.get("is_contradiction"):
                    return True, result.get("type", "subtle")
            except Exception:
                pass

        return False, ""

    async def _semantic_similarity(self, text_a: str, text_b: str) -> float:
        """Compute semantic similarity between texts."""
        # Simple keyword overlap (can enhance with embeddings)
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())

        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and', 'or', 'i', 'that', 'this'}
        words_a = words_a - stopwords
        words_b = words_b - stopwords

        if not words_a or not words_b:
            return 0.0

        intersection = len(words_a & words_b)
        union = len(words_a | words_b)

        return intersection / union if union > 0 else 0.0

    async def resolve_contradiction(
        self,
        contradiction: Contradiction,
        strategy: ResolutionStrategy = None
    ) -> Resolution:
        """
        Resolve a contradiction using specified strategy.
        If no strategy specified, auto-select based on evidence.
        """
        if strategy is None:
            strategy = await self._select_strategy(contradiction)

        resolution = await self._apply_strategy(contradiction, strategy)
        self._resolved.append(resolution)

        # Create relationship in graph
        await self.memory.create_relationship(
            contradiction.belief_a_id,
            "CONTRADICTS",
            contradiction.belief_b_id,
            properties={
                "resolved": True,
                "strategy": strategy.value,
                "resolved_at": time.time()
            }
        )

        return resolution

    async def _select_strategy(self, contradiction: Contradiction) -> ResolutionStrategy:
        """Auto-select resolution strategy based on context."""

        # Get evidence counts
        evidence_a = await self.memory.count_supporting_experiences(
            contradiction.belief_a_id
        )
        evidence_b = await self.memory.count_supporting_experiences(
            contradiction.belief_b_id
        )

        # Strong evidence imbalance -> use evidence weight
        if evidence_a > 0 and evidence_b > 0:
            ratio = max(evidence_a, evidence_b) / min(evidence_a, evidence_b)
            if ratio >= self.evidence_ratio_threshold:
                return ResolutionStrategy.EVIDENCE_WEIGHT

        # Both have weak evidence -> create uncertainty
        if evidence_a < 3 and evidence_b < 3:
            return ResolutionStrategy.CREATE_UNCERTAINTY

        # Default to confidence merge
        return ResolutionStrategy.CONFIDENCE_MERGE

    async def _apply_strategy(
        self,
        contradiction: Contradiction,
        strategy: ResolutionStrategy
    ) -> Resolution:
        """Apply resolution strategy."""

        actions = []
        winner = None
        new_conf_a = contradiction.belief_a_confidence
        new_conf_b = contradiction.belief_b_confidence

        if strategy == ResolutionStrategy.EVIDENCE_WEIGHT:
            evidence_a = await self.memory.count_supporting_experiences(
                contradiction.belief_a_id
            )
            evidence_b = await self.memory.count_supporting_experiences(
                contradiction.belief_b_id
            )

            if evidence_a > evidence_b:
                winner = contradiction.belief_a_id
                new_conf_a = min(1.0, contradiction.belief_a_confidence + 0.1)
                new_conf_b = max(0.1, contradiction.belief_b_confidence - 0.2)
            else:
                winner = contradiction.belief_b_id
                new_conf_b = min(1.0, contradiction.belief_b_confidence + 0.1)
                new_conf_a = max(0.1, contradiction.belief_a_confidence - 0.2)

            await self.memory.update_belief_confidence(
                contradiction.belief_a_id, new_conf_a
            )
            await self.memory.update_belief_confidence(
                contradiction.belief_b_id, new_conf_b
            )
            actions.append(f"Updated confidences based on evidence ({evidence_a} vs {evidence_b})")

        elif strategy == ResolutionStrategy.CREATE_UNCERTAINTY:
            # Create meta-belief about the uncertainty
            meta_content = f"UNCERTAINTY: '{contradiction.belief_a_content[:50]}' vs '{contradiction.belief_b_content[:50]}'"
            await self.memory.create_belief(
                content=meta_content,
                confidence=0.5,
                source="contradiction_resolution",
                metadata={
                    "contradicting_beliefs": [
                        contradiction.belief_a_id,
                        contradiction.belief_b_id
                    ]
                }
            )
            actions.append("Created meta-belief acknowledging uncertainty")

        elif strategy == ResolutionStrategy.CONFIDENCE_MERGE:
            # Reduce both confidences proportionally
            total_conf = contradiction.belief_a_confidence + contradiction.belief_b_confidence
            if total_conf > 0:
                new_conf_a = contradiction.belief_a_confidence * 0.8
                new_conf_b = contradiction.belief_b_confidence * 0.8

                await self.memory.update_belief_confidence(
                    contradiction.belief_a_id, new_conf_a
                )
                await self.memory.update_belief_confidence(
                    contradiction.belief_b_id, new_conf_b
                )
                actions.append("Reduced both confidences by 20%")

        return Resolution(
            contradiction=contradiction,
            strategy_used=strategy,
            winner=winner,
            actions_taken=actions,
            new_confidence_a=new_conf_a,
            new_confidence_b=new_conf_b
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get contradiction detection/resolution stats."""
        return {
            "detected": len(self._detected),
            "resolved": len(self._resolved),
            "pending": len(self._detected) - len(self._resolved),
            "strategies_used": {
                s.value: sum(1 for r in self._resolved if r.strategy_used == s)
                for s in ResolutionStrategy
            }
        }
```

---

## PHASE 4: META-LEARNING (Depends on Phase 3)

### 4.1 Meta-Learning Layer

**Purpose**: Learn which learning strategies work best for which capabilities.

**Files to Modify**:
- NEW: `meta_learner.py`
- `agi_runner.py` (integration with improvement cycles)
- `omega.py` (training hooks)

**Implementation**:

```python
# NEW FILE: /Users/kurultai/BYRD/meta_learner.py

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from collections import defaultdict
import time
import json

@dataclass
class LearningAttempt:
    """Record of a learning attempt."""
    capability: str
    strategy: str
    before_score: float
    after_score: float
    delta: float
    context: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    @property
    def success(self) -> bool:
        return self.delta > 0.01  # Meaningful improvement

@dataclass
class StrategyStats:
    """Statistics for a learning strategy."""
    attempts: int = 0
    successes: int = 0
    total_delta: float = 0.0
    avg_delta: float = 0.0
    best_delta: float = 0.0
    worst_delta: float = 0.0
    capabilities_improved: set = field(default_factory=set)

class MetaLearner:
    """
    Learns which learning strategies work best for which capabilities.

    This is meta-learning: learning HOW to learn.

    Tracks:
    - Which strategies work for which capability types
    - Which contexts favor which strategies
    - How to predict strategy effectiveness
    """

    def __init__(
        self,
        memory = None,
        config: Dict = None
    ):
        self.memory = memory
        config = config or {}

        # Strategy effectiveness by capability type
        self._capability_strategies: Dict[str, Dict[str, StrategyStats]] = defaultdict(
            lambda: defaultdict(StrategyStats)
        )

        # Overall strategy stats
        self._global_strategies: Dict[str, StrategyStats] = defaultdict(StrategyStats)

        # Learning history
        self._history: List[LearningAttempt] = []
        self._max_history = config.get("max_history", 1000)

        # Known strategies
        self.STRATEGIES = [
            "research",           # Read and synthesize information
            "practice",           # Repeated attempts with feedback
            "decomposition",      # Break into sub-capabilities
            "analogy",            # Transfer from similar capability
            "experimentation",    # Try variations and measure
            "reflection",         # Deep thinking about failures
            "synthesis",          # Combine multiple approaches
        ]

    def record_learning_attempt(
        self,
        capability: str,
        strategy: str,
        before_score: float,
        after_score: float,
        context: Dict = None
    ):
        """Record result of a learning attempt."""
        delta = after_score - before_score

        attempt = LearningAttempt(
            capability=capability,
            strategy=strategy,
            before_score=before_score,
            after_score=after_score,
            delta=delta,
            context=context or {}
        )

        self._history.append(attempt)

        # Update capability-specific stats
        cap_stats = self._capability_strategies[capability][strategy]
        self._update_stats(cap_stats, attempt)

        # Update global stats
        global_stats = self._global_strategies[strategy]
        self._update_stats(global_stats, attempt)

        # Trim history
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history // 2:]

    def _update_stats(self, stats: StrategyStats, attempt: LearningAttempt):
        """Update strategy statistics."""
        stats.attempts += 1
        stats.total_delta += attempt.delta
        stats.avg_delta = stats.total_delta / stats.attempts

        if attempt.success:
            stats.successes += 1
            stats.capabilities_improved.add(attempt.capability)

        stats.best_delta = max(stats.best_delta, attempt.delta)
        if stats.worst_delta == 0.0:
            stats.worst_delta = attempt.delta
        else:
            stats.worst_delta = min(stats.worst_delta, attempt.delta)

    def recommend_strategy(
        self,
        capability: str,
        context: Dict = None
    ) -> str:
        """
        Recommend best learning strategy for a capability.
        Uses meta-learned effectiveness data.
        """
        # Check capability-specific history first
        if capability in self._capability_strategies:
            cap_strategies = self._capability_strategies[capability]
            if cap_strategies:
                best = max(
                    cap_strategies.items(),
                    key=lambda x: x[1].avg_delta if x[1].attempts >= 2 else -1
                )
                if best[1].attempts >= 2 and best[1].avg_delta > 0:
                    return best[0]

        # Fall back to similar capabilities
        similar_caps = self._find_similar_capabilities(capability)
        for sim_cap in similar_caps:
            if sim_cap in self._capability_strategies:
                sim_strategies = self._capability_strategies[sim_cap]
                if sim_strategies:
                    best = max(
                        sim_strategies.items(),
                        key=lambda x: x[1].avg_delta if x[1].attempts >= 2 else -1
                    )
                    if best[1].attempts >= 2 and best[1].avg_delta > 0:
                        return best[0]

        # Fall back to global best
        if self._global_strategies:
            best_global = max(
                self._global_strategies.items(),
                key=lambda x: x[1].avg_delta if x[1].attempts >= 3 else -1
            )
            if best_global[1].attempts >= 3:
                return best_global[0]

        # Default strategy
        return "research"

    def _find_similar_capabilities(self, capability: str) -> List[str]:
        """Find capabilities similar to the given one."""
        similar = []
        cap_lower = capability.lower()

        # Simple keyword matching
        cap_words = set(cap_lower.replace("_", " ").split())

        for known_cap in self._capability_strategies.keys():
            known_words = set(known_cap.lower().replace("_", " ").split())
            overlap = len(cap_words & known_words)
            if overlap > 0:
                similar.append((known_cap, overlap))

        # Sort by overlap
        similar.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in similar[:3]]

    def get_strategy_effectiveness(self, strategy: str) -> Dict[str, Any]:
        """Get effectiveness metrics for a strategy."""
        if strategy not in self._global_strategies:
            return {"known": False}

        stats = self._global_strategies[strategy]
        return {
            "known": True,
            "attempts": stats.attempts,
            "success_rate": stats.successes / stats.attempts if stats.attempts > 0 else 0,
            "avg_delta": stats.avg_delta,
            "best_delta": stats.best_delta,
            "capabilities_improved": len(stats.capabilities_improved)
        }

    def get_all_recommendations(self) -> Dict[str, str]:
        """Get strategy recommendations for all known capabilities."""
        recommendations = {}

        for capability in self._capability_strategies.keys():
            recommendations[capability] = self.recommend_strategy(capability)

        return recommendations

    def get_meta_insights(self) -> List[str]:
        """Generate meta-learning insights."""
        insights = []

        # Best overall strategy
        if self._global_strategies:
            best = max(
                self._global_strategies.items(),
                key=lambda x: x[1].avg_delta if x[1].attempts >= 3 else -1
            )
            if best[1].attempts >= 3:
                insights.append(
                    f"Best overall strategy: {best[0]} (avg delta: {best[1].avg_delta:.3f})"
                )

        # Most versatile strategy
        most_versatile = max(
            self._global_strategies.items(),
            key=lambda x: len(x[1].capabilities_improved),
            default=(None, StrategyStats())
        )
        if most_versatile[0] and len(most_versatile[1].capabilities_improved) >= 2:
            insights.append(
                f"Most versatile strategy: {most_versatile[0]} "
                f"(improved {len(most_versatile[1].capabilities_improved)} capabilities)"
            )

        # Strategies to avoid
        for strategy, stats in self._global_strategies.items():
            if stats.attempts >= 5 and stats.avg_delta < -0.01:
                insights.append(
                    f"Strategy '{strategy}' tends to be counterproductive (avg delta: {stats.avg_delta:.3f})"
                )

        return insights

    async def persist(self):
        """Save meta-learning state to memory."""
        if not self.memory:
            return

        state = {
            "capability_strategies": {
                cap: {
                    strat: {
                        "attempts": stats.attempts,
                        "successes": stats.successes,
                        "total_delta": stats.total_delta,
                        "avg_delta": stats.avg_delta,
                        "best_delta": stats.best_delta,
                        "capabilities_improved": list(stats.capabilities_improved)
                    }
                    for strat, stats in strategies.items()
                }
                for cap, strategies in self._capability_strategies.items()
            },
            "global_strategies": {
                strat: {
                    "attempts": stats.attempts,
                    "successes": stats.successes,
                    "avg_delta": stats.avg_delta
                }
                for strat, stats in self._global_strategies.items()
            }
        }

        await self.memory.create_experience(
            content=f"META_LEARNING_STATE: {json.dumps(state)[:500]}",
            exp_type="meta_learning",
            metadata=state
        )
```

---

## INTEGRATION SUMMARY

```
+---------------------------------------------------------------------+
|                        PHASE 1: FOUNDATION                          |
+---------------------------------------------------------------------+
|  semantic_cache.py ------------> llm_client.py                      |
|  salience.py ------------------> memory_reasoner.py                 |
|  dreamer.py (tiered) ----------> micro/deep reflections             |
+---------------------------------------------------------------------+
                                    |
                                    v
+---------------------------------------------------------------------+
|                     PHASE 2: LOOP COUPLING                          |
+---------------------------------------------------------------------+
|  loop_coupling.py -------------> omega.py, goal_evolver.py,         |
|                                  memory_reasoner.py, dreaming_machine|
|  prediction_tracker.py --------> seeker.py, world_model.py          |
+---------------------------------------------------------------------+
                                    |
                                    v
+---------------------------------------------------------------------+
|                    PHASE 3: ACTIVE SYSTEMS                          |
+---------------------------------------------------------------------+
|  information_seeker.py --------> seeker.py                          |
|  contradiction_resolver.py ----> memory.py, dreamer.py              |
+---------------------------------------------------------------------+
                                    |
                                    v
+---------------------------------------------------------------------+
|                     PHASE 4: META-LEARNING                          |
+---------------------------------------------------------------------+
|  meta_learner.py --------------> agi_runner.py, omega.py            |
+---------------------------------------------------------------------+
```

---

## CONFIG.YAML ADDITIONS

```yaml
# Add to existing config.yaml

semantic_cache:
  enabled: true
  max_entries: 1000
  ttl_seconds: 3600
  similarity_threshold: 0.92

salience:
  half_life_hours: 24.0
  weights:
    recency: 0.25
    surprise: 0.20
    relevance: 0.25
    connectivity: 0.10
    access_frequency: 0.10
    emotional_intensity: 0.10

dreamer:
  interval_seconds: 120
  micro_reflection_interval: 10
  deep_reflection_interval: 300

loop_coupling:
  enabled: true
  event_queue_size: 100
  max_events_per_cycle: 5

prediction_tracking:
  enabled: true
  error_threshold: 0.3
  timeout_seconds: 60

information_seeking:
  enabled: true
  seeking_interval: 300
  low_confidence_threshold: 0.5
  high_uncertainty_threshold: 0.3
  max_gaps_per_cycle: 5

contradiction_resolution:
  enabled: true
  similarity_threshold: 0.7
  evidence_ratio_threshold: 2.0
  auto_resolve_threshold: 2.0

meta_learning:
  enabled: true
  max_history: 1000
```

---

## IMPLEMENTATION ORDER

| Week | Phase | Components | Dependencies |
|------|-------|------------|--------------|
| 1 | 1.1 | Semantic Cache | None |
| 1 | 1.2 | Salience Scoring | None |
| 2 | 1.3 | Tiered Reflections | None |
| 3 | 2.1 | Loop Coupling | Phase 1 complete |
| 3 | 2.2 | Prediction Tracker | Phase 1 complete |
| 4 | 3.1 | Information Seeker | Phase 2 complete |
| 4 | 3.2 | Contradiction Resolver | Phase 2 complete |
| 5 | 4.1 | Meta-Learner | Phase 3 complete |

---

## TESTING STRATEGY

Each component should have:

1. **Unit tests** - Test individual methods
2. **Integration tests** - Test integration with existing systems
3. **Metrics validation** - Verify metrics are being recorded
4. **Performance benchmarks** - Ensure no significant slowdown

Example test file structure:
```
tests/
├── test_semantic_cache.py
├── test_salience.py
├── test_loop_coupling.py
├── test_prediction_tracker.py
├── test_information_seeker.py
├── test_contradiction_resolver.py
└── test_meta_learner.py
```

---

## SUCCESS METRICS

After implementation, measure:

1. **Cache hit rate** > 40% (semantic cache working)
2. **Memory ratio** > 60% (salience improving retrieval)
3. **Critical coupling** > 0.5 (loops feeding each other)
4. **Prediction accuracy** > 70% (world model improving)
5. **Contradictions resolved** > 80% (belief system consistent)
6. **Meta-learner recommendations accurate** > 60% (meta-learning working)

---

This plan provides exact integration points, complete code, and a phased approach. Each component can be implemented and tested independently before integration.

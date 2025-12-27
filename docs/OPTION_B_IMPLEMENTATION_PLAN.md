# Option B Implementation Plan

## Executive Summary

This plan systematically implements the five compounding loops of BYRD Omega over 6 weeks. Each phase has clear deliverables, success criteria, and checkpoints. The plan is designed for incremental progress with early validation.

**Core Principle**: Build infrastructure first, then loops in dependency order, then integration. Measure everything from day one.

---

## Phase Overview

| Phase | Duration | Focus | Key Deliverable |
|-------|----------|-------|-----------------|
| **0** | 2 days | Infrastructure | embedding.py, coupling_tracker.py, new node types |
| **1** | 1 week | Memory Reasoner | Spreading activation answering queries |
| **2** | 1 week | Self-Compiler | Pattern library learning from modifications |
| **3** | 1 week | Goal Evolver | Evolutionary goal optimization |
| **4** | 1 week | Dreaming Machine | Counterfactual experience generation |
| **5** | 1 week | Integration Mind | Cross-loop coupling measurement |
| **6** | 1 week | Metrics & Polish | Dashboard, kill criteria, documentation |

**Total**: 6 weeks to full Option B implementation

---

## Phase 0: Infrastructure Foundation (2 days)

### Day 1: Embedding and Memory

#### Task 0.1: Create `embedding.py`

**File**: `/Users/kurultai/BYRD/embedding.py` (NEW)

```python
"""
Embedding provider abstraction for BYRD.
Supports Ollama (local) and OpenAI (cloud) backends.
"""

import asyncio
import httpx
import numpy as np
from typing import List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    tokens: int

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> EmbeddingResult:
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        pass

class OllamaEmbedding(EmbeddingProvider):
    def __init__(self, model: str = "nomic-embed-text", endpoint: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = endpoint

    async def embed(self, text: str) -> EmbeddingResult:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.endpoint}/api/embeddings",
                json={"model": self.model, "prompt": text}
            )
            data = response.json()
            return EmbeddingResult(
                embedding=data["embedding"],
                model=self.model,
                tokens=len(text.split())  # Approximate
            )

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        return [await self.embed(text) for text in texts]

class OpenAIEmbedding(EmbeddingProvider):
    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        import os
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    async def embed(self, text: str) -> EmbeddingResult:
        import openai
        client = openai.AsyncOpenAI(api_key=self.api_key)
        response = await client.embeddings.create(model=self.model, input=text)
        return EmbeddingResult(
            embedding=response.data[0].embedding,
            model=self.model,
            tokens=response.usage.total_tokens
        )

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        import openai
        client = openai.AsyncOpenAI(api_key=self.api_key)
        response = await client.embeddings.create(model=self.model, input=texts)
        return [
            EmbeddingResult(
                embedding=e.embedding,
                model=self.model,
                tokens=response.usage.total_tokens // len(texts)
            )
            for e in response.data
        ]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    a_np = np.array(a)
    b_np = np.array(b)
    return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

def get_embedding_provider(config: dict) -> EmbeddingProvider:
    """Factory function to get embedding provider from config."""
    provider = config.get("provider", "ollama")
    if provider == "ollama":
        return OllamaEmbedding(
            model=config.get("model", "nomic-embed-text"),
            endpoint=config.get("endpoint", "http://localhost:11434")
        )
    elif provider == "openai":
        return OpenAIEmbedding(
            model=config.get("model", "text-embedding-3-small"),
            api_key=config.get("api_key")
        )
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
```

**Validation**:
```bash
python -c "from embedding import OllamaEmbedding; import asyncio; e = OllamaEmbedding(); print(asyncio.run(e.embed('test')).embedding[:5])"
```

#### Task 0.2: Add Pattern Node Type to `memory.py`

**File**: `/Users/kurultai/BYRD/memory.py` (MODIFY)

Add after existing node creation methods (~line 800):

```python
async def create_pattern(
    self,
    context_embedding: List[float],
    solution_template: str,
    abstraction_level: int = 0,
    domains: List[str] = None
) -> str:
    """Create a Pattern node for the Self-Compiler."""
    pattern_id = f"pattern_{uuid.uuid4().hex[:8]}"

    query = """
    CREATE (p:Pattern {
        id: $id,
        context_embedding: $embedding,
        solution_template: $template,
        abstraction_level: $level,
        domains: $domains,
        success_rate: 0.0,
        application_count: 0,
        created_at: datetime()
    })
    RETURN p.id
    """

    await self._execute(query, {
        "id": pattern_id,
        "embedding": context_embedding,
        "template": solution_template,
        "level": abstraction_level,
        "domains": domains or []
    })

    await event_bus.emit(Event(
        type=EventType.PATTERN_CREATED,
        data={"id": pattern_id, "template": solution_template[:100]}
    ))

    return pattern_id

async def get_similar_patterns(
    self,
    query_embedding: List[float],
    min_similarity: float = 0.7,
    limit: int = 10
) -> List[Dict]:
    """Find patterns similar to query embedding."""
    # Note: Requires Neo4j GDS library for vector similarity
    # Fallback: fetch all and compute in Python
    query = """
    MATCH (p:Pattern)
    WHERE p.success_rate > 0.3
    RETURN p.id as id, p.context_embedding as embedding,
           p.solution_template as template, p.success_rate as success_rate,
           p.abstraction_level as level, p.domains as domains
    ORDER BY p.success_rate DESC
    LIMIT 100
    """

    results = await self._execute(query)

    # Compute similarities in Python
    from embedding import cosine_similarity
    patterns_with_sim = []
    for r in results:
        if r["embedding"]:
            sim = cosine_similarity(query_embedding, r["embedding"])
            if sim >= min_similarity:
                patterns_with_sim.append({**r, "similarity": sim})

    # Sort by similarity and limit
    patterns_with_sim.sort(key=lambda x: x["similarity"], reverse=True)
    return patterns_with_sim[:limit]

async def update_pattern_success(
    self,
    pattern_id: str,
    success: bool,
    delta: float = 0.1
) -> None:
    """Update pattern success rate based on application outcome."""
    query = """
    MATCH (p:Pattern {id: $id})
    SET p.application_count = p.application_count + 1,
        p.success_rate = CASE
            WHEN $success THEN p.success_rate + $delta * (1 - p.success_rate)
            ELSE p.success_rate - $delta * p.success_rate
        END
    """
    await self._execute(query, {"id": pattern_id, "success": success, "delta": delta})
```

#### Task 0.3: Add Goal Node Type to `memory.py`

```python
async def create_goal(
    self,
    description: str,
    fitness: float = 0.0,
    generation: int = 0,
    parent_goals: List[str] = None,
    success_criteria: str = None
) -> str:
    """Create a Goal node for the Goal Evolver."""
    goal_id = f"goal_{uuid.uuid4().hex[:8]}"

    query = """
    CREATE (g:Goal {
        id: $id,
        description: $description,
        fitness: $fitness,
        generation: $generation,
        parent_goals: $parents,
        success_criteria: $criteria,
        active: true,
        created_at: datetime()
    })
    RETURN g.id
    """

    await self._execute(query, {
        "id": goal_id,
        "description": description,
        "fitness": fitness,
        "generation": generation,
        "parents": parent_goals or [],
        "criteria": success_criteria or ""
    })

    await event_bus.emit(Event(
        type=EventType.GOAL_CREATED,
        data={"id": goal_id, "description": description, "fitness": fitness}
    ))

    return goal_id

async def get_active_goals(self, limit: int = 20) -> List[Dict]:
    """Get active goals ordered by fitness."""
    query = """
    MATCH (g:Goal)
    WHERE g.active = true
    RETURN g
    ORDER BY g.fitness DESC
    LIMIT $limit
    """
    results = await self._execute(query, {"limit": limit})
    return [dict(r["g"]) for r in results]

async def update_goal_fitness(self, goal_id: str, fitness: float) -> None:
    """Update a goal's fitness score."""
    query = """
    MATCH (g:Goal {id: $id})
    SET g.fitness = $fitness
    """
    await self._execute(query, {"id": goal_id, "fitness": fitness})

async def archive_goal(self, goal_id: str) -> None:
    """Mark a goal as inactive (archived)."""
    query = """
    MATCH (g:Goal {id: $id})
    SET g.active = false, g.archived_at = datetime()
    """
    await self._execute(query, {"id": goal_id})
```

#### Task 0.4: Add Insight Node Type to `memory.py`

```python
async def create_insight(
    self,
    content: str,
    source_type: str,  # "reflection", "counterfactual", "cross_pattern"
    confidence: float = 0.5,
    supporting_evidence: List[str] = None
) -> str:
    """Create an Insight node from the Dreaming Machine."""
    insight_id = f"insight_{uuid.uuid4().hex[:8]}"

    query = """
    CREATE (i:Insight {
        id: $id,
        content: $content,
        source_type: $source_type,
        confidence: $confidence,
        supporting_evidence: $evidence,
        created_at: datetime()
    })
    RETURN i.id
    """

    await self._execute(query, {
        "id": insight_id,
        "content": content,
        "source_type": source_type,
        "confidence": confidence,
        "evidence": supporting_evidence or []
    })

    await event_bus.emit(Event(
        type=EventType.INSIGHT_CREATED,
        data={"id": insight_id, "content": content[:100], "source": source_type}
    ))

    return insight_id
```

#### Task 0.5: Add New Event Types to `event_bus.py`

**File**: `/Users/kurultai/BYRD/event_bus.py` (MODIFY)

Add to EventType enum:

```python
# Option B events
PATTERN_CREATED = "pattern_created"
PATTERN_APPLIED = "pattern_applied"
PATTERN_REINFORCED = "pattern_reinforced"

GOAL_CREATED = "goal_created"
GOAL_EVOLVED = "goal_evolved"
GOAL_ARCHIVED = "goal_archived"

INSIGHT_CREATED = "insight_created"
COUNTERFACTUAL_GENERATED = "counterfactual_generated"

MEMORY_REASONING = "memory_reasoning"
LLM_FALLBACK = "llm_fallback"

COUPLING_MEASURED = "coupling_measured"
LOOP_HEALTH_CHANGED = "loop_health_changed"

METRICS_UPDATED = "metrics_updated"
KILL_CRITERIA_WARNING = "kill_criteria_warning"
KILL_CRITERIA_TRIGGERED = "kill_criteria_triggered"
```

### Day 2: Coupling Tracker and Config

#### Task 0.6: Create `coupling_tracker.py`

**File**: `/Users/kurultai/BYRD/coupling_tracker.py` (NEW)

```python
"""
Track correlation between loops to detect multiplicative coupling.
The critical coupling is Goal Evolver → Self-Compiler.
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
import numpy as np
from scipy.stats import pearsonr

@dataclass
class CouplingMeasurement:
    loop_a: str
    loop_b: str
    correlation: float
    p_value: float
    sample_size: int
    measured_at: datetime
    is_significant: bool  # p < 0.05

@dataclass
class LoopMetric:
    loop_name: str
    timestamp: datetime
    value: float
    metric_type: str  # "success_rate", "fitness", "efficiency", etc.

class CouplingTracker:
    """Track and compute correlations between loop performance."""

    def __init__(self, window_hours: int = 24, min_samples: int = 10):
        self.window_hours = window_hours
        self.min_samples = min_samples

        # Per-loop metric history
        self.metrics: Dict[str, List[LoopMetric]] = {
            "self_compiler": [],
            "memory_reasoner": [],
            "goal_evolver": [],
            "dreaming_machine": [],
            "integration_mind": []
        }

        # Coupling history
        self.couplings: List[CouplingMeasurement] = []

    def record_metric(self, loop: str, value: float, metric_type: str = "success"):
        """Record a metric for a loop."""
        if loop not in self.metrics:
            self.metrics[loop] = []

        self.metrics[loop].append(LoopMetric(
            loop_name=loop,
            timestamp=datetime.now(),
            value=value,
            metric_type=metric_type
        ))

        # Trim old metrics
        cutoff = datetime.now() - timedelta(hours=self.window_hours * 2)
        self.metrics[loop] = [m for m in self.metrics[loop] if m.timestamp > cutoff]

    def compute_coupling(self, loop_a: str, loop_b: str) -> Optional[CouplingMeasurement]:
        """Compute correlation between two loops over the window."""
        cutoff = datetime.now() - timedelta(hours=self.window_hours)

        # Get recent metrics
        metrics_a = [m for m in self.metrics.get(loop_a, []) if m.timestamp > cutoff]
        metrics_b = [m for m in self.metrics.get(loop_b, []) if m.timestamp > cutoff]

        if len(metrics_a) < self.min_samples or len(metrics_b) < self.min_samples:
            return None

        # Align by hour buckets
        buckets_a = self._bucket_by_hour(metrics_a)
        buckets_b = self._bucket_by_hour(metrics_b)

        # Find common hours
        common_hours = set(buckets_a.keys()) & set(buckets_b.keys())
        if len(common_hours) < 3:
            return None

        values_a = [buckets_a[h] for h in sorted(common_hours)]
        values_b = [buckets_b[h] for h in sorted(common_hours)]

        # Compute Pearson correlation
        try:
            correlation, p_value = pearsonr(values_a, values_b)
            if np.isnan(correlation):
                return None
        except Exception:
            return None

        measurement = CouplingMeasurement(
            loop_a=loop_a,
            loop_b=loop_b,
            correlation=float(correlation),
            p_value=float(p_value),
            sample_size=len(common_hours),
            measured_at=datetime.now(),
            is_significant=p_value < 0.05
        )

        self.couplings.append(measurement)
        return measurement

    def _bucket_by_hour(self, metrics: List[LoopMetric]) -> Dict[str, float]:
        """Aggregate metrics by hour."""
        buckets: Dict[str, List[float]] = {}
        for m in metrics:
            hour_key = m.timestamp.strftime("%Y-%m-%d-%H")
            if hour_key not in buckets:
                buckets[hour_key] = []
            buckets[hour_key].append(m.value)

        return {k: np.mean(v) for k, v in buckets.items()}

    def get_goal_compiler_coupling(self) -> Optional[CouplingMeasurement]:
        """Get the critical Goal→Compiler coupling."""
        return self.compute_coupling("goal_evolver", "self_compiler")

    def get_all_couplings(self) -> Dict[str, CouplingMeasurement]:
        """Compute all pairwise couplings."""
        loops = list(self.metrics.keys())
        result = {}

        for i, loop_a in enumerate(loops):
            for loop_b in loops[i+1:]:
                coupling = self.compute_coupling(loop_a, loop_b)
                if coupling:
                    result[f"{loop_a}_to_{loop_b}"] = coupling

        return result

    def get_coupling_summary(self) -> Dict:
        """Get summary for metrics dashboard."""
        goal_compiler = self.get_goal_compiler_coupling()

        return {
            "goal_compiler_correlation": goal_compiler.correlation if goal_compiler else None,
            "goal_compiler_significant": goal_compiler.is_significant if goal_compiler else False,
            "sample_size": goal_compiler.sample_size if goal_compiler else 0,
            "all_couplings": {k: v.correlation for k, v in self.get_all_couplings().items()}
        }

# Singleton instance
coupling_tracker = CouplingTracker()
```

#### Task 0.7: Update `config.yaml`

**File**: `/Users/kurultai/BYRD/config.yaml` (MODIFY)

Add Option B configuration section:

```yaml
# Option B Configuration
option_b:
  enabled: true

  # Embedding configuration
  embedding:
    provider: "ollama"  # or "openai"
    model: "nomic-embed-text"  # or "text-embedding-3-small"
    endpoint: "http://localhost:11434"

  # Loop configuration
  loops:
    self_compiler:
      enabled: true
      pattern_library_max_size: 1000
      abstraction_lift_threshold: 3  # domains before lifting
      min_pattern_confidence: 0.3

    memory_reasoner:
      enabled: true
      confidence_threshold: 0.6
      spreading_activation_decay: 0.7
      max_activation_depth: 5

    goal_evolver:
      enabled: true
      population_size: 20
      mutation_rate: 0.3
      crossover_rate: 0.5
      tournament_size: 3
      generations_per_cycle: 5

    dreaming_machine:
      enabled: true
      counterfactuals_per_experience: 3
      hypothesis_generation: true
      min_insight_confidence: 0.4

    integration_mind:
      enabled: true
      coupling_window_hours: 24
      min_coupling_samples: 10

  # Kill criteria
  kill_criteria:
    hard:
      zero_growth_weeks: 4
      llm_efficiency_decline_weeks: 6
    soft:
      no_coupling_weeks: 8
      single_loop_healthy_weeks: 6
      linear_only_weeks: 12

  # Metrics
  metrics:
    measurement_interval_minutes: 60
    capability_test_interval_hours: 24
    checkpoint_interval_minutes: 30
```

#### Task 0.8: Update `requirements.txt`

**File**: `/Users/kurultai/BYRD/requirements.txt` (MODIFY)

Add:

```
# Option B dependencies
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0  # Optional, for clustering
```

### Phase 0 Checkpoint

**Validation Script** (`scripts/validate_phase0.py`):

```python
#!/usr/bin/env python3
"""Validate Phase 0 completion."""

import asyncio
import sys
sys.path.insert(0, "/Users/kurultai/BYRD")

async def main():
    errors = []

    # Test 1: embedding.py exists and works
    try:
        from embedding import OllamaEmbedding, cosine_similarity
        e = OllamaEmbedding()
        result = await e.embed("test embedding")
        assert len(result.embedding) > 0, "Empty embedding"
        print("✓ embedding.py works")
    except Exception as ex:
        errors.append(f"embedding.py: {ex}")
        print(f"✗ embedding.py: {ex}")

    # Test 2: coupling_tracker.py exists
    try:
        from coupling_tracker import CouplingTracker, coupling_tracker
        ct = CouplingTracker()
        ct.record_metric("test_loop", 0.5)
        print("✓ coupling_tracker.py works")
    except Exception as ex:
        errors.append(f"coupling_tracker.py: {ex}")
        print(f"✗ coupling_tracker.py: {ex}")

    # Test 3: memory.py has new methods
    try:
        from memory import Memory
        import inspect
        m = Memory({})
        assert hasattr(m, 'create_pattern'), "Missing create_pattern"
        assert hasattr(m, 'create_goal'), "Missing create_goal"
        assert hasattr(m, 'create_insight'), "Missing create_insight"
        print("✓ memory.py has new node methods")
    except Exception as ex:
        errors.append(f"memory.py: {ex}")
        print(f"✗ memory.py: {ex}")

    # Test 4: event_bus.py has new events
    try:
        from event_bus import EventType
        assert hasattr(EventType, 'PATTERN_CREATED')
        assert hasattr(EventType, 'GOAL_CREATED')
        assert hasattr(EventType, 'INSIGHT_CREATED')
        assert hasattr(EventType, 'COUPLING_MEASURED')
        print("✓ event_bus.py has new events")
    except Exception as ex:
        errors.append(f"event_bus.py: {ex}")
        print(f"✗ event_bus.py: {ex}")

    # Test 5: config.yaml has option_b section
    try:
        import yaml
        with open("/Users/kurultai/BYRD/config.yaml") as f:
            config = yaml.safe_load(f)
        assert "option_b" in config, "Missing option_b section"
        assert config["option_b"]["enabled"] == True
        print("✓ config.yaml has option_b section")
    except Exception as ex:
        errors.append(f"config.yaml: {ex}")
        print(f"✗ config.yaml: {ex}")

    print(f"\n{'='*50}")
    if errors:
        print(f"Phase 0 INCOMPLETE: {len(errors)} errors")
        return 1
    else:
        print("Phase 0 COMPLETE: All validations passed")
        return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

---

## Phase 1: Memory Reasoner (1 week)

### Goal
Implement spreading activation to answer queries from the graph before calling the LLM.

### Task 1.1: Create `memory_reasoner.py`

**File**: `/Users/kurultai/BYRD/memory_reasoner.py` (NEW)

```python
"""
Memory Reasoner: Answer queries from the graph before calling LLM.
Uses spreading activation to find relevant knowledge.
"""

import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from memory import Memory
from llm_client import LLMClient
from embedding import get_embedding_provider, cosine_similarity
from event_bus import event_bus, Event, EventType
from coupling_tracker import coupling_tracker

@dataclass
class ReasoningResult:
    answer: str
    source: str  # "memory" or "llm_augmented"
    confidence: float
    nodes_activated: int
    patterns_used: List[str]
    reasoning_time_ms: float

class MemoryReasoner:
    """
    Reasoning through graph operations.
    LLM is fallback, not primary.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config

        # Get embedding provider
        embedding_config = config.get("option_b", {}).get("embedding", {})
        self.embedder = get_embedding_provider(embedding_config)

        # Configuration
        loop_config = config.get("option_b", {}).get("loops", {}).get("memory_reasoner", {})
        self.confidence_threshold = loop_config.get("confidence_threshold", 0.6)
        self.activation_decay = loop_config.get("spreading_activation_decay", 0.7)
        self.max_depth = loop_config.get("max_activation_depth", 5)

        # Metrics
        self.llm_calls = 0
        self.memory_answers = 0
        self.total_queries = 0

    async def reason(self, query: str) -> ReasoningResult:
        """Answer a query, preferring memory over LLM."""
        start_time = datetime.now()
        self.total_queries += 1

        # 1. Embed the query
        query_embedding = await self.embedder.embed(query)

        # 2. Spreading activation from semantically similar nodes
        activated_nodes = await self._spreading_activation(query_embedding.embedding)

        # 3. Try to compose answer from activated knowledge
        memory_answer, confidence = await self._compose_from_memory(
            query, activated_nodes
        )

        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

        if confidence >= self.confidence_threshold:
            # Memory-based answer
            self.memory_answers += 1
            coupling_tracker.record_metric("memory_reasoner", 1.0)

            await event_bus.emit(Event(
                type=EventType.MEMORY_REASONING,
                data={
                    "query": query[:100],
                    "confidence": confidence,
                    "nodes_activated": len(activated_nodes)
                }
            ))

            return ReasoningResult(
                answer=memory_answer,
                source="memory",
                confidence=confidence,
                nodes_activated=len(activated_nodes),
                patterns_used=[],
                reasoning_time_ms=elapsed_ms
            )

        # 4. LLM fallback with memory context
        self.llm_calls += 1
        coupling_tracker.record_metric("memory_reasoner", 0.0)

        context = self._format_context(activated_nodes)
        llm_answer = await self._llm_with_context(query, context)

        # 5. Cache the answer for future memory-based reasoning
        await self._cache_answer(query, llm_answer, query_embedding.embedding)

        await event_bus.emit(Event(
            type=EventType.LLM_FALLBACK,
            data={"query": query[:100], "context_nodes": len(activated_nodes)}
        ))

        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

        return ReasoningResult(
            answer=llm_answer,
            source="llm_augmented",
            confidence=0.5,
            nodes_activated=len(activated_nodes),
            patterns_used=[],
            reasoning_time_ms=elapsed_ms
        )

    async def _spreading_activation(
        self,
        seed_embedding: List[float],
        initial_activation: float = 1.0
    ) -> List[Tuple[str, float, Dict]]:
        """
        Spread activation from semantically similar nodes.
        Returns list of (node_id, activation_level, node_data).
        """
        # Find seed nodes by embedding similarity
        seed_nodes = await self.memory.find_similar_nodes(
            seed_embedding,
            min_similarity=0.6,
            limit=10
        )

        if not seed_nodes:
            return []

        # Initialize activation
        activation: Dict[str, float] = {
            node["id"]: initial_activation * node.get("similarity", 1.0)
            for node in seed_nodes
        }

        # Spread activation
        for depth in range(self.max_depth):
            new_activation: Dict[str, float] = {}

            for node_id, act_level in activation.items():
                if act_level < 0.1:  # Threshold
                    continue

                # Get neighbors
                neighbors = await self.memory.get_neighbors(node_id)

                for neighbor_id, edge_weight in neighbors:
                    spread = act_level * self.activation_decay * edge_weight
                    if neighbor_id in new_activation:
                        new_activation[neighbor_id] = max(
                            new_activation[neighbor_id], spread
                        )
                    else:
                        new_activation[neighbor_id] = spread

            # Merge activations
            for node_id, act in new_activation.items():
                if node_id not in activation:
                    activation[node_id] = act
                else:
                    activation[node_id] = max(activation[node_id], act)

        # Get node data for activated nodes
        result = []
        for node_id, act_level in sorted(
            activation.items(), key=lambda x: x[1], reverse=True
        )[:50]:  # Top 50
            node_data = await self.memory.get_node(node_id)
            if node_data:
                result.append((node_id, act_level, node_data))

        return result

    async def _compose_from_memory(
        self,
        query: str,
        activated_nodes: List[Tuple[str, float, Dict]]
    ) -> Tuple[str, float]:
        """Compose an answer from activated knowledge."""
        if not activated_nodes:
            return "", 0.0

        # Group by node type
        beliefs = []
        experiences = []
        insights = []

        for node_id, activation, data in activated_nodes:
            node_type = data.get("type") or data.get("labels", ["Unknown"])[0]
            content = data.get("content", data.get("description", ""))

            if "Belief" in str(node_type):
                beliefs.append((activation, content, data.get("confidence", 0.5)))
            elif "Experience" in str(node_type):
                experiences.append((activation, content))
            elif "Insight" in str(node_type):
                insights.append((activation, content, data.get("confidence", 0.5)))

        # Compute confidence based on what we found
        if beliefs:
            # Weighted average of belief confidences
            total_weight = sum(b[0] for b in beliefs)
            avg_confidence = sum(b[0] * b[2] for b in beliefs) / total_weight if total_weight > 0 else 0

            # Compose answer from top beliefs
            answer_parts = [b[1] for b in sorted(beliefs, key=lambda x: x[0], reverse=True)[:3]]
            return " ".join(answer_parts), avg_confidence

        if insights:
            total_weight = sum(i[0] for i in insights)
            avg_confidence = sum(i[0] * i[2] for i in insights) / total_weight if total_weight > 0 else 0

            answer_parts = [i[1] for i in sorted(insights, key=lambda x: x[0], reverse=True)[:3]]
            return " ".join(answer_parts), avg_confidence * 0.8  # Slight discount for insights

        if experiences:
            # Lower confidence for experience-only answers
            answer_parts = [e[1] for e in sorted(experiences, key=lambda x: x[0], reverse=True)[:3]]
            return " ".join(answer_parts), 0.4

        return "", 0.0

    def _format_context(self, activated_nodes: List[Tuple[str, float, Dict]]) -> str:
        """Format activated nodes as context for LLM."""
        if not activated_nodes:
            return "No relevant context found in memory."

        lines = ["Relevant knowledge from memory:"]
        for node_id, activation, data in activated_nodes[:10]:
            content = data.get("content", data.get("description", ""))[:200]
            node_type = data.get("type", "Unknown")
            lines.append(f"- [{node_type}] {content}")

        return "\n".join(lines)

    async def _llm_with_context(self, query: str, context: str) -> str:
        """Call LLM with memory context."""
        prompt = f"""Answer the following query using the provided context.

{context}

Query: {query}

Answer:"""

        return await self.llm_client.generate(prompt)

    async def _cache_answer(
        self,
        query: str,
        answer: str,
        query_embedding: List[float]
    ) -> None:
        """Cache the Q&A pair for future memory-based reasoning."""
        # Create experience for the Q&A
        exp_id = await self.memory.record_experience(
            content=f"Q: {query}\nA: {answer}",
            type="qa_pair"
        )

        # Store embedding for future retrieval
        await self.memory.update_node_embedding(exp_id, query_embedding)

    def effectiveness_ratio(self) -> float:
        """What fraction of reasoning is memory-based?"""
        if self.total_queries == 0:
            return 0.0
        return self.memory_answers / self.total_queries

    def get_health_status(self) -> Dict:
        """Get health status for metrics dashboard."""
        ratio = self.effectiveness_ratio()
        return {
            "status": "healthy" if ratio > 0.5 else ("warning" if ratio > 0.3 else "critical"),
            "memory_ratio": ratio,
            "total_queries": self.total_queries,
            "memory_answers": self.memory_answers,
            "llm_calls": self.llm_calls
        }
```

### Task 1.2: Add Helper Methods to `memory.py`

Add to `memory.py`:

```python
async def find_similar_nodes(
    self,
    embedding: List[float],
    min_similarity: float = 0.6,
    limit: int = 10,
    node_types: List[str] = None
) -> List[Dict]:
    """Find nodes with similar embeddings."""
    type_filter = ""
    if node_types:
        labels = " OR ".join([f"n:{t}" for t in node_types])
        type_filter = f"WHERE ({labels})"

    query = f"""
    MATCH (n)
    {type_filter}
    WHERE n.embedding IS NOT NULL
    RETURN n, labels(n) as labels
    LIMIT 500
    """

    results = await self._execute(query)

    from embedding import cosine_similarity
    similar = []
    for r in results:
        node = dict(r["n"])
        if "embedding" in node and node["embedding"]:
            sim = cosine_similarity(embedding, node["embedding"])
            if sim >= min_similarity:
                node["similarity"] = sim
                node["labels"] = r["labels"]
                similar.append(node)

    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar[:limit]

async def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
    """Get neighbors with edge weights for spreading activation."""
    query = """
    MATCH (n {id: $node_id})-[r]-(m)
    RETURN m.id as neighbor_id,
           COALESCE(r.weight, r.strength, r.confidence, 1.0) as weight
    """

    results = await self._execute(query, {"node_id": node_id})
    return [(r["neighbor_id"], r["weight"]) for r in results if r["neighbor_id"]]

async def get_node(self, node_id: str) -> Optional[Dict]:
    """Get a single node by ID."""
    query = """
    MATCH (n {id: $node_id})
    RETURN n, labels(n) as labels
    """
    results = await self._execute(query, {"node_id": node_id})
    if results:
        node = dict(results[0]["n"])
        node["labels"] = results[0]["labels"]
        return node
    return None

async def update_node_embedding(self, node_id: str, embedding: List[float]) -> None:
    """Update a node's embedding."""
    query = """
    MATCH (n {id: $node_id})
    SET n.embedding = $embedding
    """
    await self._execute(query, {"node_id": node_id, "embedding": embedding})
```

### Task 1.3: Integrate Memory Reasoner into BYRD

Modify `byrd.py`:

```python
# Add import
from memory_reasoner import MemoryReasoner

# In __init__, add:
self.memory_reasoner = MemoryReasoner(self.memory, self.llm_client, self.config)

# Add answer method:
async def answer(self, query: str) -> str:
    """Answer a query using memory-first reasoning."""
    result = await self.memory_reasoner.reason(query)
    return result.answer
```

### Phase 1 Success Criteria

- [ ] `memory_reasoner.py` created and functional
- [ ] Spreading activation finds semantically related nodes
- [ ] Memory-based answers work when confidence > threshold
- [ ] LLM fallback works with context
- [ ] Q&A caching stores answers for future retrieval
- [ ] `effectiveness_ratio()` can be computed
- [ ] Health status returned correctly

**Target**: Memory reasoning ratio > 30% after 1 week of operation

---

## Phase 2: Self-Compiler (1 week)

### Goal
Implement pattern library that learns from successful modifications.

### Task 2.1: Extend `accelerators.py` with PatternLibrary

**File**: `/Users/kurultai/BYRD/accelerators.py` (MODIFY)

Add PatternLibrary class:

```python
# Add to accelerators.py

from embedding import get_embedding_provider, cosine_similarity
from coupling_tracker import coupling_tracker

@dataclass
class Pattern:
    id: str
    context_embedding: List[float]
    solution_template: str
    abstraction_level: int  # 0=concrete, 1=intermediate, 2=abstract
    success_rate: float
    application_count: int
    domains: List[str]

class PatternLibrary:
    """
    Library of reusable patterns extracted from successful modifications.
    Implements abstraction lifting when patterns prove cross-domain.
    """

    def __init__(self, memory: Memory, embedder, config: Dict):
        self.memory = memory
        self.embedder = embedder
        self.config = config

        loop_config = config.get("option_b", {}).get("loops", {}).get("self_compiler", {})
        self.max_size = loop_config.get("pattern_library_max_size", 1000)
        self.lift_threshold = loop_config.get("abstraction_lift_threshold", 3)
        self.min_confidence = loop_config.get("min_pattern_confidence", 0.3)

    async def find_patterns(
        self,
        problem_context: str,
        domain: str = None,
        limit: int = 5
    ) -> List[Pattern]:
        """Find patterns relevant to a problem context."""
        # Embed the problem
        embedding = await self.embedder.embed(problem_context)

        # Query similar patterns
        patterns = await self.memory.get_similar_patterns(
            embedding.embedding,
            min_similarity=0.6,
            limit=limit * 2  # Get extra, filter by success
        )

        # Filter by minimum confidence
        good_patterns = [
            p for p in patterns
            if p.get("success_rate", 0) >= self.min_confidence
        ]

        # Prefer domain-specific patterns, but include abstract ones
        if domain:
            domain_patterns = [p for p in good_patterns if domain in p.get("domains", [])]
            abstract_patterns = [p for p in good_patterns if p.get("level", 0) >= 1]
            good_patterns = domain_patterns + [p for p in abstract_patterns if p not in domain_patterns]

        return [
            Pattern(
                id=p["id"],
                context_embedding=p.get("embedding", []),
                solution_template=p["template"],
                abstraction_level=p.get("level", 0),
                success_rate=p.get("success_rate", 0),
                application_count=p.get("application_count", 0),
                domains=p.get("domains", [])
            )
            for p in good_patterns[:limit]
        ]

    async def extract_pattern(
        self,
        problem_context: str,
        solution: str,
        domain: str,
        success: bool
    ) -> Optional[str]:
        """Extract a pattern from a successful modification."""
        if not success:
            return None

        # Embed the problem context
        embedding = await self.embedder.embed(problem_context)

        # Create pattern
        pattern_id = await self.memory.create_pattern(
            context_embedding=embedding.embedding,
            solution_template=solution,
            abstraction_level=0,  # Concrete initially
            domains=[domain]
        )

        await event_bus.emit(Event(
            type=EventType.PATTERN_CREATED,
            data={"id": pattern_id, "domain": domain}
        ))

        return pattern_id

    async def reinforce_pattern(self, pattern_id: str, success: bool) -> None:
        """Reinforce or penalize a pattern based on outcome."""
        await self.memory.update_pattern_success(pattern_id, success)

        coupling_tracker.record_metric(
            "self_compiler",
            1.0 if success else 0.0
        )

        await event_bus.emit(Event(
            type=EventType.PATTERN_REINFORCED,
            data={"id": pattern_id, "success": success}
        ))

    async def maybe_lift_pattern(self, pattern_id: str) -> bool:
        """
        Check if pattern should be lifted to higher abstraction.
        Lift when pattern succeeds across multiple domains.
        """
        # Get pattern
        pattern_data = await self.memory.get_node(pattern_id)
        if not pattern_data:
            return False

        domains = pattern_data.get("domains", [])
        level = pattern_data.get("abstraction_level", 0)
        success_rate = pattern_data.get("success_rate", 0)

        # Check lift criteria
        if len(domains) >= self.lift_threshold and success_rate > 0.6 and level < 2:
            # Lift the pattern
            query = """
            MATCH (p:Pattern {id: $id})
            SET p.abstraction_level = p.abstraction_level + 1
            """
            await self.memory._execute(query, {"id": pattern_id})

            # Create ABSTRACTED_TO relationship to original
            # (for provenance)

            return True

        return False


class SelfCompiler:
    """
    Code evolution with pattern learning.
    Uses PatternLibrary to improve modification success rate.
    """

    def __init__(self, memory: Memory, coder, safety_monitor, config: Dict):
        self.memory = memory
        self.coder = coder
        self.safety_monitor = safety_monitor
        self.config = config

        embedding_config = config.get("option_b", {}).get("embedding", {})
        embedder = get_embedding_provider(embedding_config)

        self.pattern_library = PatternLibrary(memory, embedder, config)

        # Metrics
        self.successful_modifications = 0
        self.failed_modifications = 0

    async def improve(self, weakness: Dict) -> Dict:
        """
        Attempt to fix a weakness using pattern-guided modification.
        """
        weakness_type = weakness.get("type", "unknown")
        description = weakness.get("description", "")
        target_file = weakness.get("target_file")

        # 1. Find relevant patterns
        patterns = await self.pattern_library.find_patterns(
            problem_context=description,
            domain=weakness_type,
            limit=5
        )

        # 2. Generate modification using patterns
        modification = await self._generate_modification(
            weakness, patterns
        )

        if not modification:
            self.failed_modifications += 1
            return {"success": False, "reason": "Could not generate modification"}

        # 3. Safety check
        safety_result = await self.safety_monitor.verify_modification_safety(
            modification.get("file_path"),
            modification.get("new_code"),
            modification.get("rationale", "")
        )

        if not safety_result.get("safe", False):
            self.failed_modifications += 1
            return {"success": False, "reason": f"Safety check failed: {safety_result.get('reason')}"}

        # 4. Apply modification
        result = await self.coder.apply_modification(modification)

        # 5. Learn from result
        success = result.get("success", False)

        if success:
            self.successful_modifications += 1

            # Extract new pattern
            await self.pattern_library.extract_pattern(
                problem_context=description,
                solution=modification.get("new_code", ""),
                domain=weakness_type,
                success=True
            )

            # Reinforce used patterns
            for pattern in patterns:
                await self.pattern_library.reinforce_pattern(pattern.id, True)
                await self.pattern_library.maybe_lift_pattern(pattern.id)
        else:
            self.failed_modifications += 1

            # Penalize used patterns
            for pattern in patterns:
                await self.pattern_library.reinforce_pattern(pattern.id, False)

        return {
            "success": success,
            "patterns_used": len(patterns),
            "modification": modification
        }

    async def _generate_modification(
        self,
        weakness: Dict,
        patterns: List[Pattern]
    ) -> Optional[Dict]:
        """Generate a modification using patterns as guidance."""
        # Build prompt with pattern context
        pattern_context = ""
        if patterns:
            pattern_context = "Relevant patterns from past successes:\n"
            for p in patterns:
                pattern_context += f"- {p.solution_template[:200]}...\n"

        # Use coder to generate modification
        prompt = f"""
Fix this weakness: {weakness.get('description')}

Target file: {weakness.get('target_file', 'unknown')}

{pattern_context}

Generate a specific code modification to address this weakness.
"""

        modification = await self.coder.generate_modification(prompt)
        return modification

    def success_rate(self) -> float:
        """Get modification success rate."""
        total = self.successful_modifications + self.failed_modifications
        return self.successful_modifications / total if total > 0 else 0

    def get_health_status(self) -> Dict:
        """Get health status for metrics dashboard."""
        rate = self.success_rate()
        return {
            "status": "healthy" if rate > 0.5 else ("warning" if rate > 0.3 else "critical"),
            "success_rate": rate,
            "successful": self.successful_modifications,
            "failed": self.failed_modifications
        }
```

### Phase 2 Success Criteria

- [ ] PatternLibrary class implemented
- [ ] Pattern extraction from successful modifications works
- [ ] Pattern matching finds relevant patterns
- [ ] Abstraction lifting triggers at threshold
- [ ] SelfCompiler integrates patterns into modification generation
- [ ] Success rate metrics computed correctly

**Target**: Modification success rate > 40% after 1 week

---

## Phase 3: Goal Evolver (1 week)

### Goal
Implement evolutionary goal optimization with fitness-based selection.

### Task 3.1: Create `goal_evolver.py`

**File**: `/Users/kurultai/BYRD/goal_evolver.py` (NEW)

```python
"""
Goal Evolver: Evolutionary optimization of goals.
Goals evolve through fitness selection to become more effective.
"""

import asyncio
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from memory import Memory
from llm_client import LLMClient
from event_bus import event_bus, Event, EventType
from coupling_tracker import coupling_tracker

@dataclass
class Goal:
    id: str
    description: str
    fitness: float
    generation: int
    parent_goals: List[str]
    success_criteria: str
    resources_required: List[str]

class GoalEvolver:
    """
    Evolve goals through fitness-based selection.
    Better goals survive and produce offspring.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config

        loop_config = config.get("option_b", {}).get("loops", {}).get("goal_evolver", {})
        self.population_size = loop_config.get("population_size", 20)
        self.mutation_rate = loop_config.get("mutation_rate", 0.3)
        self.crossover_rate = loop_config.get("crossover_rate", 0.5)
        self.tournament_size = loop_config.get("tournament_size", 3)

        # Metrics
        self.generations_evolved = 0
        self.fitness_history: List[float] = []

    async def evolve_generation(self) -> Dict:
        """Run one generation of goal evolution."""
        # 1. Get current population
        population = await self._get_population()

        if len(population) < 2:
            # Not enough goals to evolve
            return {"evolved": False, "reason": "Population too small"}

        # 2. Evaluate fitness for all goals
        for goal in population:
            if goal.fitness == 0:  # Not yet evaluated
                goal.fitness = await self._evaluate_fitness(goal)
                await self.memory.update_goal_fitness(goal.id, goal.fitness)

        # 3. Selection + Reproduction
        offspring = []

        while len(offspring) < self.population_size // 2:
            # Tournament selection
            parent1 = self._tournament_select(population)
            parent2 = self._tournament_select(population)

            # Crossover
            if random.random() < self.crossover_rate:
                child_desc = await self._crossover(parent1, parent2)
            else:
                child_desc = parent1.description

            # Mutation
            if random.random() < self.mutation_rate:
                child_desc = await self._mutate(child_desc)

            # Create child goal
            child_id = await self.memory.create_goal(
                description=child_desc,
                generation=max(parent1.generation, parent2.generation) + 1,
                parent_goals=[parent1.id, parent2.id]
            )

            offspring.append(child_id)

        # 4. Archive weak goals
        sorted_pop = sorted(population, key=lambda g: g.fitness)
        for weak_goal in sorted_pop[:len(offspring)]:
            await self.memory.archive_goal(weak_goal.id)

        # 5. Track metrics
        self.generations_evolved += 1
        avg_fitness = sum(g.fitness for g in population) / len(population) if population else 0
        self.fitness_history.append(avg_fitness)

        coupling_tracker.record_metric("goal_evolver", avg_fitness)

        await event_bus.emit(Event(
            type=EventType.GOAL_EVOLVED,
            data={
                "generation": self.generations_evolved,
                "avg_fitness": avg_fitness,
                "offspring": len(offspring),
                "archived": len(offspring)
            }
        ))

        return {
            "evolved": True,
            "generation": self.generations_evolved,
            "avg_fitness": avg_fitness,
            "offspring_count": len(offspring)
        }

    async def _get_population(self) -> List[Goal]:
        """Get the current goal population."""
        goals = await self.memory.get_active_goals(limit=self.population_size * 2)

        return [
            Goal(
                id=g["id"],
                description=g["description"],
                fitness=g.get("fitness", 0),
                generation=g.get("generation", 0),
                parent_goals=g.get("parent_goals", []),
                success_criteria=g.get("success_criteria", ""),
                resources_required=g.get("resources_required", [])
            )
            for g in goals
        ]

    async def _evaluate_fitness(self, goal: Goal) -> float:
        """
        Evaluate goal fitness.
        Combines: completion, capability_gain, efficiency
        """
        # Check if goal has been pursued
        related_desires = await self.memory.get_desires_for_goal(goal.id)

        if not related_desires:
            return 0.1  # Not yet pursued

        # Completion rate
        fulfilled = sum(1 for d in related_desires if d.get("fulfilled", False))
        completion = fulfilled / len(related_desires) if related_desires else 0

        # Capability gain (did pursuing this goal improve capabilities?)
        capability_gain = await self._measure_capability_gain(goal.id)

        # Efficiency (how much effort for the result?)
        experiences = await self.memory.get_experiences_for_goal(goal.id)
        efficiency = 1.0 / (len(experiences) + 1)  # Fewer experiences = more efficient

        # Weighted fitness
        fitness = (
            0.4 * completion +
            0.4 * capability_gain +
            0.2 * efficiency
        )

        return min(1.0, max(0.0, fitness))

    async def _measure_capability_gain(self, goal_id: str) -> float:
        """Measure capability improvement from pursuing a goal."""
        # Simplified: check for new capabilities acquired
        query = """
        MATCH (g:Goal {id: $goal_id})-[:DECOMPOSED_TO]->(:Desire)-[:FULFILLS]->(:Capability)
        RETURN count(*) as count
        """
        result = await self.memory._execute(query, {"goal_id": goal_id})
        if result:
            return min(1.0, result[0]["count"] * 0.2)  # 5 capabilities = max
        return 0.0

    def _tournament_select(self, population: List[Goal]) -> Goal:
        """Select a goal via tournament selection."""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        return max(tournament, key=lambda g: g.fitness)

    async def _crossover(self, parent1: Goal, parent2: Goal) -> str:
        """Combine two goals into a new goal description."""
        prompt = f"""Combine these two goals into a single new goal that captures their essence:

Goal 1: {parent1.description}
Goal 2: {parent2.description}

New combined goal (one sentence):"""

        return await self.llm_client.generate(prompt, max_tokens=100)

    async def _mutate(self, goal_description: str) -> str:
        """Mutate a goal description."""
        prompt = f"""Slightly modify this goal to make it more specific or actionable:

Original: {goal_description}

Modified goal (one sentence):"""

        return await self.llm_client.generate(prompt, max_tokens=100)

    def fitness_trend(self) -> float:
        """Compute fitness trend (positive = improving)."""
        if len(self.fitness_history) < 5:
            return 0.0

        recent = self.fitness_history[-5:]
        older = self.fitness_history[-10:-5] if len(self.fitness_history) >= 10 else self.fitness_history[:5]

        return sum(recent) / len(recent) - sum(older) / len(older)

    def get_health_status(self) -> Dict:
        """Get health status for metrics dashboard."""
        trend = self.fitness_trend()
        return {
            "status": "healthy" if trend > 0 else ("warning" if trend > -0.1 else "critical"),
            "fitness_trend": trend,
            "generations": self.generations_evolved,
            "avg_fitness": self.fitness_history[-1] if self.fitness_history else 0
        }
```

### Task 3.2: Add Helper Methods to `memory.py`

```python
async def get_desires_for_goal(self, goal_id: str) -> List[Dict]:
    """Get desires decomposed from a goal."""
    query = """
    MATCH (g:Goal {id: $goal_id})-[:DECOMPOSED_TO]->(d:Desire)
    RETURN d
    """
    results = await self._execute(query, {"goal_id": goal_id})
    return [dict(r["d"]) for r in results]

async def get_experiences_for_goal(self, goal_id: str) -> List[Dict]:
    """Get experiences related to pursuing a goal."""
    query = """
    MATCH (g:Goal {id: $goal_id})-[:DECOMPOSED_TO]->(:Desire)<-[:FULFILLS]-(:Experience)
    RETURN e
    LIMIT 100
    """
    results = await self._execute(query, {"goal_id": goal_id})
    return [dict(r["e"]) for r in results]
```

### Phase 3 Success Criteria

- [ ] `goal_evolver.py` created and functional
- [ ] Goal population maintained at target size
- [ ] Fitness evaluation considers completion, capability gain, efficiency
- [ ] Tournament selection works
- [ ] Crossover and mutation produce valid goals
- [ ] Weak goals archived
- [ ] Fitness trend tracked

**Target**: Average fitness increasing over 5 generations

---

## Phase 4: Dreaming Machine (1 week)

### Goal
Generate counterfactual experiences and extract insights.

### Task 4.1: Create `dreaming_machine.py`

**File**: `/Users/kurultai/BYRD/dreaming_machine.py` (NEW)

```python
"""
Dreaming Machine: Generate counterfactual experiences and hypotheses.
Multiplies learning from each real experience.
"""

import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from memory import Memory
from llm_client import LLMClient
from event_bus import event_bus, Event, EventType
from coupling_tracker import coupling_tracker

@dataclass
class Counterfactual:
    original_experience_id: str
    varied_aspect: str  # "action", "context", "parameter"
    description: str
    predicted_outcome: str
    confidence: float

@dataclass
class Hypothesis:
    content: str
    supporting_experiences: List[str]
    confidence: float
    testable: bool

class DreamingMachine:
    """
    Generate counterfactual experiences and hypotheses.
    Multiplies learning from each real experience.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config

        loop_config = config.get("option_b", {}).get("loops", {}).get("dreaming_machine", {})
        self.counterfactuals_per_experience = loop_config.get("counterfactuals_per_experience", 3)
        self.hypothesis_generation = loop_config.get("hypothesis_generation", True)
        self.min_insight_confidence = loop_config.get("min_insight_confidence", 0.4)

        # Metrics
        self.counterfactuals_generated = 0
        self.insights_extracted = 0
        self.hypotheses_formed = 0

    async def dream_on_experience(self, experience_id: str) -> Dict:
        """
        Generate counterfactuals and extract insights from an experience.
        """
        # 1. Get the experience
        experience = await self.memory.get_node(experience_id)
        if not experience:
            return {"success": False, "reason": "Experience not found"}

        content = experience.get("content", "")
        exp_type = experience.get("type", "unknown")

        # 2. Generate counterfactuals
        counterfactuals = await self._generate_counterfactuals(
            experience_id, content, exp_type
        )

        # 3. Store counterfactuals as imagined experiences
        for cf in counterfactuals:
            cf_exp_id = await self.memory.record_experience(
                content=f"[COUNTERFACTUAL] {cf.description}\nPredicted outcome: {cf.predicted_outcome}",
                type="counterfactual"
            )

            # Link to original
            await self.memory.create_relationship(
                cf_exp_id, experience_id, "IMAGINED_FROM"
            )

            self.counterfactuals_generated += 1

        await event_bus.emit(Event(
            type=EventType.COUNTERFACTUAL_GENERATED,
            data={
                "original_id": experience_id,
                "count": len(counterfactuals)
            }
        ))

        # 4. Extract insights from original + counterfactuals
        insights = await self._extract_insights(
            experience, counterfactuals
        )

        for insight in insights:
            if insight.confidence >= self.min_insight_confidence:
                await self.memory.create_insight(
                    content=insight.content,
                    source_type="counterfactual",
                    confidence=insight.confidence,
                    supporting_evidence=[experience_id]
                )
                self.insights_extracted += 1

        # 5. Form hypotheses if enabled
        hypotheses = []
        if self.hypothesis_generation:
            hypotheses = await self._form_hypotheses(experience, counterfactuals)
            self.hypotheses_formed += len(hypotheses)

        coupling_tracker.record_metric(
            "dreaming_machine",
            len(insights) / (len(counterfactuals) + 1) if counterfactuals else 0
        )

        return {
            "success": True,
            "counterfactuals": len(counterfactuals),
            "insights": len(insights),
            "hypotheses": len(hypotheses)
        }

    async def _generate_counterfactuals(
        self,
        experience_id: str,
        content: str,
        exp_type: str
    ) -> List[Counterfactual]:
        """Generate counterfactual variations of an experience."""
        prompt = f"""Given this experience, generate {self.counterfactuals_per_experience} counterfactual scenarios.

Experience: {content[:500]}
Type: {exp_type}

For each counterfactual, vary one aspect (action taken, context, or parameters) and predict what would have happened differently.

Format each as:
VARIED: [what was changed]
SCENARIO: [the counterfactual description]
OUTCOME: [predicted outcome]
CONFIDENCE: [0.0-1.0]

Generate {self.counterfactuals_per_experience} counterfactuals:"""

        response = await self.llm_client.generate(prompt, max_tokens=500)

        # Parse response
        counterfactuals = []
        current = {}

        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("VARIED:"):
                if current:
                    counterfactuals.append(current)
                current = {"varied": line[7:].strip()}
            elif line.startswith("SCENARIO:"):
                current["scenario"] = line[9:].strip()
            elif line.startswith("OUTCOME:"):
                current["outcome"] = line[8:].strip()
            elif line.startswith("CONFIDENCE:"):
                try:
                    current["confidence"] = float(line[11:].strip())
                except:
                    current["confidence"] = 0.5

        if current and "scenario" in current:
            counterfactuals.append(current)

        return [
            Counterfactual(
                original_experience_id=experience_id,
                varied_aspect=cf.get("varied", "unknown"),
                description=cf.get("scenario", ""),
                predicted_outcome=cf.get("outcome", ""),
                confidence=cf.get("confidence", 0.5)
            )
            for cf in counterfactuals
            if cf.get("scenario")
        ]

    async def _extract_insights(
        self,
        experience: Dict,
        counterfactuals: List[Counterfactual]
    ) -> List[Dict]:
        """Extract insights by comparing real experience with counterfactuals."""
        if not counterfactuals:
            return []

        cf_descriptions = "\n".join([
            f"- If {cf.varied_aspect} was different: {cf.predicted_outcome}"
            for cf in counterfactuals
        ])

        prompt = f"""Compare the actual experience with these counterfactual outcomes:

Actual experience: {experience.get('content', '')[:300]}

Counterfactual outcomes:
{cf_descriptions}

What insights or patterns can you extract? Focus on:
1. What factors were critical to the outcome?
2. What could be done differently next time?
3. What general principle does this illustrate?

Format as:
INSIGHT: [the insight]
CONFIDENCE: [0.0-1.0]

Extract 1-3 insights:"""

        response = await self.llm_client.generate(prompt, max_tokens=300)

        # Parse insights
        insights = []
        current = {}

        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("INSIGHT:"):
                if current:
                    insights.append(current)
                current = {"content": line[8:].strip()}
            elif line.startswith("CONFIDENCE:"):
                try:
                    current["confidence"] = float(line[11:].strip())
                except:
                    current["confidence"] = 0.5

        if current and "content" in current:
            insights.append(current)

        return [
            type("Insight", (), {
                "content": i.get("content", ""),
                "confidence": i.get("confidence", 0.5)
            })()
            for i in insights
        ]

    async def _form_hypotheses(
        self,
        experience: Dict,
        counterfactuals: List[Counterfactual]
    ) -> List[Hypothesis]:
        """Form testable hypotheses from experience and counterfactuals."""
        prompt = f"""Based on this experience and its counterfactual analysis, form a testable hypothesis.

Experience: {experience.get('content', '')[:200]}

What hypothesis could be tested in future experiences?

Format:
HYPOTHESIS: [statement that could be true or false]
TESTABLE: [yes/no]

Hypothesis:"""

        response = await self.llm_client.generate(prompt, max_tokens=150)

        # Simple parsing
        hypothesis_text = ""
        testable = True

        for line in response.split("\n"):
            if line.strip().startswith("HYPOTHESIS:"):
                hypothesis_text = line.strip()[11:].strip()
            elif line.strip().startswith("TESTABLE:"):
                testable = "yes" in line.lower()

        if hypothesis_text:
            return [Hypothesis(
                content=hypothesis_text,
                supporting_experiences=[experience.get("id", "")],
                confidence=0.5,
                testable=testable
            )]

        return []

    def insight_extraction_rate(self) -> float:
        """Rate of insight extraction per counterfactual."""
        if self.counterfactuals_generated == 0:
            return 0.0
        return self.insights_extracted / self.counterfactuals_generated

    def get_health_status(self) -> Dict:
        """Get health status for metrics dashboard."""
        rate = self.insight_extraction_rate()
        return {
            "status": "healthy" if rate > 0.15 else ("warning" if rate > 0.1 else "critical"),
            "insight_rate": rate,
            "counterfactuals": self.counterfactuals_generated,
            "insights": self.insights_extracted,
            "hypotheses": self.hypotheses_formed
        }
```

### Phase 4 Success Criteria

- [ ] `dreaming_machine.py` created and functional
- [ ] Counterfactual generation produces valid alternatives
- [ ] Counterfactuals stored with IMAGINED_FROM relationship
- [ ] Insights extracted and stored
- [ ] Hypothesis formation works
- [ ] Insight extraction rate tracked

**Target**: Insight extraction rate > 15%

---

## Phase 5: Integration Mind (1 week)

### Goal
Enable cross-loop synergies and measure coupling.

### Task 5.1: Create `omega.py`

**File**: `/Users/kurultai/BYRD/omega.py` (NEW)

```python
"""
BYRD Omega: The unified wrapper that orchestrates all five loops.
Manages mode transitions and measures coupling.
"""

import asyncio
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from memory import Memory
from llm_client import LLMClient
from memory_reasoner import MemoryReasoner
from goal_evolver import GoalEvolver
from dreaming_machine import DreamingMachine
from accelerators import SelfCompiler, PatternLibrary
from coupling_tracker import coupling_tracker
from event_bus import event_bus, Event, EventType

class OmegaMode(Enum):
    AWAKE = "awake"
    DREAMING = "dreaming"
    EVOLVING = "evolving"
    COMPILING = "compiling"

@dataclass
class LoopHealth:
    name: str
    status: str  # "healthy", "warning", "critical"
    metrics: Dict

class BYRDOmega:
    """
    The unified orchestrator for BYRD's five compounding loops.
    """

    def __init__(self, byrd_instance):
        self.byrd = byrd_instance
        self.memory = byrd_instance.memory
        self.llm_client = byrd_instance.llm_client
        self.config = byrd_instance.config

        # Initialize loops
        self.memory_reasoner = MemoryReasoner(
            self.memory, self.llm_client, self.config
        )

        self.goal_evolver = GoalEvolver(
            self.memory, self.llm_client, self.config
        )

        self.dreaming_machine = DreamingMachine(
            self.memory, self.llm_client, self.config
        )

        self.self_compiler = SelfCompiler(
            self.memory,
            byrd_instance.coder,
            byrd_instance.safety_monitor,
            self.config
        )

        # Mode management
        self.current_mode = OmegaMode.AWAKE
        self.cycles_in_mode = 0
        self.mode_transition_threshold = 100  # cycles

        # Metrics
        self.metrics_history: list = []

    async def run_cycle(self) -> Dict:
        """Run one integrated cycle across all loops."""
        self.cycles_in_mode += 1

        # Check for mode transition
        if self.cycles_in_mode >= self.mode_transition_threshold:
            await self._transition_mode()

        # Run mode-specific operations
        if self.current_mode == OmegaMode.AWAKE:
            return await self._awake_cycle()
        elif self.current_mode == OmegaMode.DREAMING:
            return await self._dreaming_cycle()
        elif self.current_mode == OmegaMode.EVOLVING:
            return await self._evolving_cycle()
        elif self.current_mode == OmegaMode.COMPILING:
            return await self._compiling_cycle()

    async def _awake_cycle(self) -> Dict:
        """Normal operation: answer queries, pursue goals."""
        # Memory reasoner handles queries automatically
        # Just track metrics
        return {
            "mode": "awake",
            "cycles": self.cycles_in_mode
        }

    async def _dreaming_cycle(self) -> Dict:
        """Extended reflection: counterfactuals, insights."""
        # Get recent experiences to dream on
        experiences = await self.memory.get_recent_experiences(limit=5)

        results = []
        for exp in experiences:
            result = await self.dreaming_machine.dream_on_experience(exp["id"])
            results.append(result)

        return {
            "mode": "dreaming",
            "experiences_dreamed": len(experiences),
            "total_insights": sum(r.get("insights", 0) for r in results)
        }

    async def _evolving_cycle(self) -> Dict:
        """Goal evolution: tournament, mutation, selection."""
        result = await self.goal_evolver.evolve_generation()

        # Check if we should transition to compiling
        if result.get("avg_fitness", 0) > 0.6:
            # Good goals, look for weaknesses to fix
            weaknesses = await self._identify_weaknesses()
            if weaknesses:
                self.current_mode = OmegaMode.COMPILING
                self.cycles_in_mode = 0

        return {
            "mode": "evolving",
            **result
        }

    async def _compiling_cycle(self) -> Dict:
        """Self-improvement: pattern-guided modification."""
        # Get top weakness
        weaknesses = await self._identify_weaknesses()

        if not weaknesses:
            # No weaknesses, return to awake
            self.current_mode = OmegaMode.AWAKE
            self.cycles_in_mode = 0
            return {"mode": "compiling", "action": "no_weakness_found"}

        # Try to fix top weakness
        result = await self.self_compiler.improve(weaknesses[0])

        if result.get("success"):
            # Success! Return to awake
            self.current_mode = OmegaMode.AWAKE
            self.cycles_in_mode = 0

        return {
            "mode": "compiling",
            **result
        }

    async def _transition_mode(self):
        """Transition to next mode in cycle."""
        mode_order = [
            OmegaMode.AWAKE,
            OmegaMode.DREAMING,
            OmegaMode.EVOLVING,
            OmegaMode.AWAKE  # Skip compiling unless triggered by evolving
        ]

        current_idx = mode_order.index(self.current_mode)
        next_idx = (current_idx + 1) % len(mode_order)

        self.current_mode = mode_order[next_idx]
        self.cycles_in_mode = 0

        await event_bus.emit(Event(
            type=EventType.MODE_CHANGED,
            data={"new_mode": self.current_mode.value}
        ))

    async def _identify_weaknesses(self) -> list:
        """Identify weaknesses from self-model."""
        # Use existing self_model to find limitations
        limitations = await self.byrd.self_model.identify_limitations()

        return [
            {
                "type": lim.get("capability", "unknown"),
                "description": lim.get("description", ""),
                "target_file": lim.get("suggested_file")
            }
            for lim in limitations
            if lim.get("severity", 0) > 0.5
        ]

    def get_all_health(self) -> Dict[str, LoopHealth]:
        """Get health status for all loops."""
        return {
            "memory_reasoner": LoopHealth(
                name="Memory Reasoner",
                **self.memory_reasoner.get_health_status()
            ),
            "self_compiler": LoopHealth(
                name="Self-Compiler",
                **self.self_compiler.get_health_status()
            ),
            "goal_evolver": LoopHealth(
                name="Goal Evolver",
                **self.goal_evolver.get_health_status()
            ),
            "dreaming_machine": LoopHealth(
                name="Dreaming Machine",
                **self.dreaming_machine.get_health_status()
            ),
            "coupling": self._get_coupling_health()
        }

    def _get_coupling_health(self) -> LoopHealth:
        """Get coupling health status."""
        summary = coupling_tracker.get_coupling_summary()

        goal_compiler = summary.get("goal_compiler_correlation")

        if goal_compiler is None:
            status = "unknown"
        elif goal_compiler > 0.3:
            status = "healthy"
        elif goal_compiler > 0.1:
            status = "warning"
        else:
            status = "critical"

        return LoopHealth(
            name="Integration Mind",
            status=status,
            metrics=summary
        )

    def get_metrics_snapshot(self) -> Dict:
        """Get current metrics for dashboard."""
        health = self.get_all_health()

        return {
            "timestamp": datetime.now().isoformat(),
            "mode": self.current_mode.value,
            "cycles_in_mode": self.cycles_in_mode,
            "loops": {
                name: {
                    "status": h.status,
                    "metrics": h.metrics
                }
                for name, h in health.items()
            },
            "coupling": coupling_tracker.get_coupling_summary()
        }
```

### Task 5.2: Add MODE_CHANGED Event

Add to `event_bus.py`:

```python
MODE_CHANGED = "mode_changed"
```

### Task 5.3: Integrate into `byrd.py`

Modify `byrd.py` to use BYRDOmega:

```python
# Add import
from omega import BYRDOmega

# In __init__, after component initialization:
if self.config.get("option_b", {}).get("enabled", False):
    self.omega = BYRDOmega(self)
else:
    self.omega = None

# Add to main loop:
async def _omega_loop(self):
    """Run the Omega cycle if enabled."""
    if not self.omega:
        return

    interval = self.config.get("option_b", {}).get("metrics", {}).get(
        "measurement_interval_minutes", 60
    ) * 60

    while self.running:
        try:
            result = await self.omega.run_cycle()
            logger.info(f"Omega cycle: {result}")
        except Exception as e:
            logger.error(f"Omega cycle error: {e}")

        await asyncio.sleep(interval)
```

### Phase 5 Success Criteria

- [ ] `omega.py` created and functional
- [ ] Mode transitions work correctly
- [ ] All loops accessible through Omega
- [ ] Health status aggregated for all loops
- [ ] Coupling measured between Goal Evolver and Self-Compiler
- [ ] Metrics snapshot available

**Target**: Goal→Compiler correlation > 0.2

---

## Phase 6: Metrics & Polish (1 week)

### Goal
Add dashboard, kill criteria monitoring, documentation.

### Task 6.1: Add Metrics Endpoints to `server.py`

```python
@app.get("/api/metrics/omega")
async def get_omega_metrics():
    """Get all Omega metrics."""
    if not byrd.omega:
        return {"enabled": False}

    return byrd.omega.get_metrics_snapshot()

@app.get("/api/metrics/coupling")
async def get_coupling_metrics():
    """Get loop coupling metrics."""
    return coupling_tracker.get_coupling_summary()

@app.get("/api/metrics/health")
async def get_health_metrics():
    """Get all loop health status."""
    if not byrd.omega:
        return {"enabled": False}

    return {
        name: {"status": h.status, "metrics": h.metrics}
        for name, h in byrd.omega.get_all_health().items()
    }

@app.get("/api/metrics/kill-criteria")
async def get_kill_criteria():
    """Get kill criteria status."""
    return await evaluate_kill_criteria(byrd)
```

### Task 6.2: Create Kill Criteria Evaluator

**File**: `/Users/kurultai/BYRD/kill_criteria.py` (NEW)

```python
"""
Kill Criteria Evaluator: Determine when to stop, simplify, or pivot.
"""

from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class KillCriteriaResult:
    hard_triggered: bool
    soft_triggered: bool
    triggered_criteria: List[str]
    recommendation: str  # "continue", "simplify", "pivot", "stop"
    details: Dict

async def evaluate_kill_criteria(byrd) -> KillCriteriaResult:
    """Evaluate all kill criteria."""
    if not byrd.omega:
        return KillCriteriaResult(
            hard_triggered=False,
            soft_triggered=False,
            triggered_criteria=[],
            recommendation="continue",
            details={"error": "Omega not enabled"}
        )

    config = byrd.config.get("option_b", {}).get("kill_criteria", {})
    hard_config = config.get("hard", {})
    soft_config = config.get("soft", {})

    triggered = []

    # Hard criteria
    # 1. Zero growth for N weeks
    zero_growth_weeks = hard_config.get("zero_growth_weeks", 4)
    if await _check_zero_growth(byrd, zero_growth_weeks):
        triggered.append(f"hard:zero_growth_{zero_growth_weeks}w")

    # 2. LLM efficiency declining
    efficiency_weeks = hard_config.get("llm_efficiency_decline_weeks", 6)
    if await _check_efficiency_decline(byrd, efficiency_weeks):
        triggered.append(f"hard:efficiency_decline_{efficiency_weeks}w")

    # Soft criteria
    # 1. No coupling observed
    no_coupling_weeks = soft_config.get("no_coupling_weeks", 8)
    if await _check_no_coupling(byrd, no_coupling_weeks):
        triggered.append(f"soft:no_coupling_{no_coupling_weeks}w")

    # 2. Only one loop healthy
    single_loop_weeks = soft_config.get("single_loop_healthy_weeks", 6)
    if await _check_single_loop(byrd, single_loop_weeks):
        triggered.append(f"soft:single_loop_{single_loop_weeks}w")

    # Determine recommendation
    hard_triggered = any(t.startswith("hard:") for t in triggered)
    soft_triggered = any(t.startswith("soft:") for t in triggered)

    if hard_triggered:
        recommendation = "stop"
    elif soft_triggered:
        recommendation = "simplify"
    else:
        recommendation = "continue"

    return KillCriteriaResult(
        hard_triggered=hard_triggered,
        soft_triggered=soft_triggered,
        triggered_criteria=triggered,
        recommendation=recommendation,
        details={
            "checked_at": datetime.now().isoformat(),
            "hard_config": hard_config,
            "soft_config": soft_config
        }
    )

async def _check_zero_growth(byrd, weeks: int) -> bool:
    """Check if capability growth has been zero for N weeks."""
    # Get capability history
    history = await byrd.self_model.get_capability_history(days=weeks * 7)
    if len(history) < 2:
        return False

    # Check if first and last are essentially the same
    first = history[0].get("score", 0)
    last = history[-1].get("score", 0)

    return abs(last - first) < 0.01  # Less than 1% change

async def _check_efficiency_decline(byrd, weeks: int) -> bool:
    """Check if LLM efficiency has been declining."""
    # Simplified check
    mr = byrd.omega.memory_reasoner
    return mr.effectiveness_ratio() < 0.1  # Very low memory usage

async def _check_no_coupling(byrd, weeks: int) -> bool:
    """Check if no significant coupling observed."""
    summary = byrd.omega._get_coupling_health()
    correlation = summary.metrics.get("goal_compiler_correlation")
    return correlation is None or correlation < 0.1

async def _check_single_loop(byrd, weeks: int) -> bool:
    """Check if only one loop is healthy."""
    health = byrd.omega.get_all_health()
    healthy_count = sum(
        1 for h in health.values()
        if h.status == "healthy"
    )
    return healthy_count <= 1
```

### Task 6.3: Add Metrics Panel to Visualization

Add to `byrd-3d-visualization.html` (JavaScript section):

```javascript
// Add metrics panel
function createMetricsPanel() {
    const panel = document.createElement('div');
    panel.id = 'metrics-panel';
    panel.innerHTML = `
        <div class="metrics-header">OMEGA METRICS</div>
        <div class="metrics-content">
            <div class="metric-row">
                <span class="metric-label">Mode:</span>
                <span class="metric-value" id="omega-mode">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Memory Ratio:</span>
                <span class="metric-value" id="memory-ratio">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Compiler Success:</span>
                <span class="metric-value" id="compiler-success">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Goal Fitness:</span>
                <span class="metric-value" id="goal-fitness">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Insight Rate:</span>
                <span class="metric-value" id="insight-rate">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">G→C Coupling:</span>
                <span class="metric-value" id="coupling">-</span>
            </div>
        </div>
    `;
    document.body.appendChild(panel);
}

// Update metrics every 30 seconds
async function updateMetrics() {
    try {
        const response = await fetch('/api/metrics/omega');
        const data = await response.json();

        if (!data.enabled) return;

        document.getElementById('omega-mode').textContent = data.mode;

        const loops = data.loops || {};

        if (loops.memory_reasoner) {
            const ratio = loops.memory_reasoner.metrics?.memory_ratio || 0;
            document.getElementById('memory-ratio').textContent =
                (ratio * 100).toFixed(1) + '%';
        }

        if (loops.self_compiler) {
            const rate = loops.self_compiler.metrics?.success_rate || 0;
            document.getElementById('compiler-success').textContent =
                (rate * 100).toFixed(1) + '%';
        }

        if (loops.goal_evolver) {
            const fitness = loops.goal_evolver.metrics?.avg_fitness || 0;
            document.getElementById('goal-fitness').textContent =
                fitness.toFixed(2);
        }

        if (loops.dreaming_machine) {
            const rate = loops.dreaming_machine.metrics?.insight_rate || 0;
            document.getElementById('insight-rate').textContent =
                (rate * 100).toFixed(1) + '%';
        }

        const coupling = data.coupling?.goal_compiler_correlation;
        document.getElementById('coupling').textContent =
            coupling !== null ? coupling.toFixed(2) : '-';

    } catch (e) {
        console.error('Failed to update metrics:', e);
    }
}

// Initialize
createMetricsPanel();
setInterval(updateMetrics, 30000);
updateMetrics();
```

Add CSS:

```css
#metrics-panel {
    position: fixed;
    top: 10px;
    right: 10px;
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid #00d4ff;
    border-radius: 8px;
    padding: 15px;
    color: #fff;
    font-family: monospace;
    font-size: 12px;
    z-index: 1000;
    min-width: 200px;
}

.metrics-header {
    font-size: 14px;
    font-weight: bold;
    color: #00d4ff;
    margin-bottom: 10px;
    border-bottom: 1px solid #333;
    padding-bottom: 5px;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
}

.metric-label {
    color: #888;
}

.metric-value {
    color: #0f0;
    font-weight: bold;
}
```

### Phase 6 Success Criteria

- [ ] Metrics endpoints return correct data
- [ ] Kill criteria evaluator works
- [ ] Metrics panel visible in visualizer
- [ ] Real-time updates working
- [ ] All documentation updated

---

## Final Validation

### Complete System Test

```python
#!/usr/bin/env python3
"""Final validation of Option B implementation."""

import asyncio
import sys
sys.path.insert(0, "/Users/kurultai/BYRD")

async def main():
    from byrd import BYRD

    # Initialize BYRD with Option B
    byrd = BYRD()
    await byrd.memory.connect()

    errors = []

    # Test 1: Omega initialized
    if not byrd.omega:
        errors.append("Omega not initialized")
    else:
        print("✓ Omega initialized")

    # Test 2: All loops accessible
    if byrd.omega:
        assert byrd.omega.memory_reasoner is not None
        assert byrd.omega.goal_evolver is not None
        assert byrd.omega.dreaming_machine is not None
        assert byrd.omega.self_compiler is not None
        print("✓ All loops accessible")

    # Test 3: Memory reasoner works
    result = await byrd.omega.memory_reasoner.reason("What is BYRD?")
    assert result.answer, "Empty answer"
    print(f"✓ Memory reasoner works (source: {result.source})")

    # Test 4: Health status available
    health = byrd.omega.get_all_health()
    assert len(health) >= 4, "Missing health entries"
    print(f"✓ Health status: {len(health)} loops")

    # Test 5: Metrics snapshot works
    snapshot = byrd.omega.get_metrics_snapshot()
    assert "mode" in snapshot
    assert "loops" in snapshot
    print(f"✓ Metrics snapshot: mode={snapshot['mode']}")

    # Test 6: Coupling tracker works
    from coupling_tracker import coupling_tracker
    coupling_tracker.record_metric("test_loop", 0.5)
    summary = coupling_tracker.get_coupling_summary()
    print(f"✓ Coupling tracker works")

    await byrd.memory.close()

    if errors:
        print(f"\n{'='*50}")
        print(f"VALIDATION FAILED: {len(errors)} errors")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print(f"\n{'='*50}")
        print("OPTION B IMPLEMENTATION COMPLETE")
        print("All validations passed!")
        return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

---

## Success Metrics Summary

| Phase | Key Metric | Target | Measured By |
|-------|------------|--------|-------------|
| 0 | Infrastructure complete | All tests pass | validate_phase0.py |
| 1 | Memory reasoning ratio | > 30% | memory_reasoner.effectiveness_ratio() |
| 2 | Modification success rate | > 40% | self_compiler.success_rate() |
| 3 | Average fitness trend | Increasing | goal_evolver.fitness_trend() |
| 4 | Insight extraction rate | > 15% | dreaming_machine.insight_extraction_rate() |
| 5 | Goal→Compiler coupling | > 0.2 | coupling_tracker.get_goal_compiler_coupling() |
| 6 | System operational | All loops healthy | omega.get_all_health() |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Embedding model not available | Fallback to simpler similarity (TF-IDF) |
| Pattern library grows too large | Implement pruning of low-success patterns |
| Goal population stagnates | Increase mutation rate, inject random goals |
| Coupling never observed | Run loops independently, accept linear value |
| Kill criteria triggered | Follow decision framework: simplify → pivot → stop |

---

## Post-Implementation

After completing all phases:

1. **Baseline measurement**: Run capability test suite, record initial scores
2. **Weekly reviews**: Check metrics dashboard, evaluate kill criteria
3. **Continuous monitoring**: Track coupling correlation, loop health
4. **Documentation**: Update ARCHITECTURE.md with learnings

---

*Plan created: December 26, 2024*
*Estimated completion: 6 weeks*
*Philosophy: Build incrementally, measure constantly, pivot when data demands*

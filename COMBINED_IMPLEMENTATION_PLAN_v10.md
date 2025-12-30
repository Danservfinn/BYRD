# BYRD Combined Implementation Plan v10

## Overview

This plan extends v5 with **Graphiti temporal knowledge graph integration** and **dual-instance rate limit optimization** for ZAI GLM-4.7 Max Coding Plan.

**Total Scope: ~1,340 lines | Additional LLM Calls: Async (Instance B)**

---

## What's New in v10

| Feature | Description |
|---------|-------------|
| **Dual Instance Manager** | Two concurrent GLM-4.7 instances with independent rate limiting |
| **Graphiti Integration** | Temporal knowledge graph with entity extraction, bi-temporal tracking |
| **Rate Limit Optimization** | Tuned for Max Plan (480 prompts/hour per instance) |
| **Async Extraction Queue** | Non-blocking entity/relationship extraction |
| **OutcomeDispatcher Integration** | Graphiti as learning component, not Memory hook |

## v10 Bug Fixes (from v9 review)

| Bug | Severity | Fix |
|-----|----------|-----|
| Unused `List` import in Part 1 | LOW | Removed from typing imports |
| Unused `InstanceRole` import in Part 5 | LOW | Removed from imports |
| "unchanged in v8" in docs section | LOW | Updated to v10 |
| "v8 configuration" in config comment | LOW | Updated to "v10" |

## v9 Bug Fixes (from v8 review)

| Bug | Severity | Fix |
|-----|----------|-----|
| Unused `RateLimitConfig` dataclass in Part 1 | LOW | Removed unused dataclass |
| Unused `defaultdict` import in Part 2 | LOW | Removed unused import |
| Unused `Tuple` import in Part 2 | LOW | Removed from typing imports |
| Stale "v6" reference in Part 3 docstring | LOW | Updated to "v9" |
| Unused `InstanceRole` import in Part 4 | LOW | Removed unused import |

## v8 Bug Fixes (from v7 review)

| Bug | Severity | Fix |
|-----|----------|-----|
| Queue health logic inverted (`elif > 800` unreachable) | MEDIUM | Reordered threshold checks (800 first) |
| Unused `deque` import | LOW | Removed unused import |
| Regex injection risk in `search_entities()` | LOW | Added `re.escape()` for query |
| Missing `Optional` import in Part 4 | LOW | Added `Optional` to typing imports |
| Stale "v6" references in comments | LOW | Updated all to "v8" |

## v7 Bug Fixes (from v6 review)

| Bug | Severity | Fix |
|-----|----------|-----|
| `InstanceRole` import at bottom of file | HIGH | Moved import to top of Part 2 |
| Missing `initialize_schema()` method | MEDIUM | Added method to GraphitiLayer |
| Incorrect utilization calculation | LOW | Added `session_start` tracking to InstanceMetrics |

---

## ZAI Max Coding Plan Optimization

### Rate Limit Configuration

```yaml
# config.yaml - Optimized for ZAI Max Coding Plan

local_llm:
  provider: "zai"
  model: "glm-4.7"

  # Max Plan: 2400 prompts / 5 hours = 480/hr = 8/min per instance
  # With dual instances: 960/hr = 16/min total
  rate_limit:
    # Per-instance minimum interval (slightly conservative)
    interval_seconds: 8.0

    # Burst allowance for bursty workloads
    burst_tokens: 3
    burst_recovery_seconds: 24.0

  # Dual instance configuration
  dual_instance:
    enabled: true

    # Instance A: Core BYRD operations
    instance_a:
      role: "primary"
      components: ["dreamer", "seeker", "actor"]
      priority: "high"

    # Instance B: Enrichment and verification
    instance_b:
      role: "enrichment"
      components: ["graphiti", "capability_evaluator", "code_verifier"]
      priority: "normal"

# Graphiti configuration
graphiti:
  enabled: true

  extraction:
    # Queue settings
    queue_max_size: 1000
    batch_size: 1  # Process one at a time for rate limiting

    # Extraction thresholds
    min_confidence: 0.7
    min_content_length: 50  # Skip very short content

    # Custom entity types for BYRD
    custom_entity_types:
      - Concept
      - Capability
      - Principle
      - Pattern
      - Limitation
      - Strategy

  temporal:
    enabled: true
    contradiction_strategy: "invalidate_old"

  search:
    # Hybrid search weights
    semantic_weight: 0.4
    keyword_weight: 0.3
    graph_weight: 0.3
    max_graph_hops: 3
```

---

## Part 1: Enhanced Dual Instance Manager (~120 lines)

**Replaces** v5 Part 7. Adds burst handling, component routing, and metrics.

```python
# src/byrd/core/dual_instance_manager.py

import asyncio
import time
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class InstanceRole(Enum):
    PRIMARY = "primary"
    ENRICHMENT = "enrichment"


@dataclass
class InstanceMetrics:
    """Metrics for a single instance."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_wait_time: float = 0.0
    tokens_used: int = 0
    last_call_time: float = 0.0
    session_start: float = field(default_factory=time.time)  # v7: Track session start


class TokenBucket:
    """Token bucket for burst handling."""

    def __init__(self, capacity: int, refill_seconds: float):
        self.capacity = capacity
        self.refill_seconds = refill_seconds
        self.tokens = capacity
        self.last_refill = time.time()

    def try_acquire(self) -> bool:
        """Try to acquire a token. Returns True if successful."""
        self._refill()
        if self.tokens > 0:
            self.tokens -= 1
            return True
        return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_count = int(elapsed / self.refill_seconds)
        if refill_count > 0:
            self.tokens = min(self.capacity, self.tokens + refill_count)
            self.last_refill = now


class DualInstanceManager:
    """
    Manages two concurrent GLM-4.7 instances with independent rate limiting.

    Instance A (Primary): Dreamer, Seeker, Actor - core BYRD operations
    Instance B (Enrichment): Graphiti, Capability Evaluator, Code Verifier

    Optimized for ZAI Max Coding Plan:
    - 2400 prompts / 5 hours per instance
    - 480 prompts/hour = 8/minute = 7.5s minimum interval
    - With dual instances: 960 prompts/hour total capacity
    """

    def __init__(self, llm_client, config: Dict[str, Any]):
        self._client = llm_client
        self._config = config

        rate_config = config.get('rate_limit', {})
        self._interval = rate_config.get('interval_seconds', 8.0)
        burst_tokens = rate_config.get('burst_tokens', 3)
        burst_recovery = rate_config.get('burst_recovery_seconds', 24.0)

        # Per-instance locks and timing
        self._locks: Dict[InstanceRole, asyncio.Lock] = {
            InstanceRole.PRIMARY: asyncio.Lock(),
            InstanceRole.ENRICHMENT: asyncio.Lock()
        }

        self._last_call: Dict[InstanceRole, float] = {
            InstanceRole.PRIMARY: 0,
            InstanceRole.ENRICHMENT: 0
        }

        # Burst handling
        self._burst_buckets: Dict[InstanceRole, TokenBucket] = {
            InstanceRole.PRIMARY: TokenBucket(burst_tokens, burst_recovery),
            InstanceRole.ENRICHMENT: TokenBucket(burst_tokens, burst_recovery)
        }

        # Metrics
        self._metrics: Dict[InstanceRole, InstanceMetrics] = {
            InstanceRole.PRIMARY: InstanceMetrics(),
            InstanceRole.ENRICHMENT: InstanceMetrics()
        }

        # Component routing
        self._component_routing: Dict[str, InstanceRole] = {
            'dreamer': InstanceRole.PRIMARY,
            'seeker': InstanceRole.PRIMARY,
            'actor': InstanceRole.PRIMARY,
            'graphiti': InstanceRole.ENRICHMENT,
            'capability_evaluator': InstanceRole.ENRICHMENT,
            'code_verifier': InstanceRole.ENRICHMENT
        }

    def get_instance_for_component(self, component: str) -> InstanceRole:
        """Get the appropriate instance for a component."""
        return self._component_routing.get(component, InstanceRole.PRIMARY)

    async def call(
        self,
        role: InstanceRole,
        prompt: str,
        component: str = "unknown",
        **kwargs
    ) -> Any:
        """Make rate-limited call on specified instance."""
        async with self._locks[role]:
            wait_time = await self._wait_for_slot(role)

            try:
                result = await self._client.generate(prompt, **kwargs)
                self._record_success(role, wait_time)
                return result
            except Exception as e:
                self._record_failure(role, wait_time)
                raise

    async def _wait_for_slot(self, role: InstanceRole) -> float:
        """Wait for rate limit slot, returns wait time."""
        # Check burst bucket first
        if self._burst_buckets[role].try_acquire():
            return 0.0

        # Otherwise, wait for interval
        elapsed = time.time() - self._last_call[role]
        wait_time = max(0, self._interval - elapsed)

        if wait_time > 0:
            await asyncio.sleep(wait_time)

        self._last_call[role] = time.time()
        return wait_time

    def _record_success(self, role: InstanceRole, wait_time: float):
        """Record successful call metrics."""
        metrics = self._metrics[role]
        metrics.total_calls += 1
        metrics.successful_calls += 1
        metrics.total_wait_time += wait_time
        metrics.last_call_time = time.time()

    def _record_failure(self, role: InstanceRole, wait_time: float):
        """Record failed call metrics."""
        metrics = self._metrics[role]
        metrics.total_calls += 1
        metrics.failed_calls += 1
        metrics.total_wait_time += wait_time

    async def call_by_component(
        self,
        component: str,
        prompt: str,
        **kwargs
    ) -> Any:
        """Route call to appropriate instance based on component."""
        role = self.get_instance_for_component(component)
        return await self.call(role, prompt, component=component, **kwargs)

    async def call_parallel(
        self,
        primary_prompt: str,
        enrichment_prompt: str,
        **kwargs
    ) -> tuple:
        """Make parallel calls on both instances."""
        primary_task = self.call(InstanceRole.PRIMARY, primary_prompt, **kwargs)
        enrichment_task = self.call(InstanceRole.ENRICHMENT, enrichment_prompt, **kwargs)
        return await asyncio.gather(primary_task, enrichment_task)

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for both instances."""
        return {
            'primary': {
                'total_calls': self._metrics[InstanceRole.PRIMARY].total_calls,
                'successful': self._metrics[InstanceRole.PRIMARY].successful_calls,
                'failed': self._metrics[InstanceRole.PRIMARY].failed_calls,
                'avg_wait': (
                    self._metrics[InstanceRole.PRIMARY].total_wait_time /
                    max(1, self._metrics[InstanceRole.PRIMARY].total_calls)
                ),
                'utilization': self._calculate_utilization(InstanceRole.PRIMARY)
            },
            'enrichment': {
                'total_calls': self._metrics[InstanceRole.ENRICHMENT].total_calls,
                'successful': self._metrics[InstanceRole.ENRICHMENT].successful_calls,
                'failed': self._metrics[InstanceRole.ENRICHMENT].failed_calls,
                'avg_wait': (
                    self._metrics[InstanceRole.ENRICHMENT].total_wait_time /
                    max(1, self._metrics[InstanceRole.ENRICHMENT].total_calls)
                ),
                'utilization': self._calculate_utilization(InstanceRole.ENRICHMENT)
            },
            'total_calls': sum(m.total_calls for m in self._metrics.values()),
            'interval_seconds': self._interval
        }

    def _calculate_utilization(self, role: InstanceRole) -> float:
        """Calculate instance utilization (0-1) based on session duration."""
        metrics = self._metrics[role]
        if metrics.total_calls == 0:
            return 0.0

        # v7: Use session_start for accurate duration calculation
        elapsed_hours = (time.time() - metrics.session_start) / 3600
        if elapsed_hours < 0.001:  # Less than ~4 seconds
            return 0.0

        # Max calls per hour at current interval
        max_calls_per_hour = 3600 / self._interval

        # Calls per hour during this session
        calls_per_hour = metrics.total_calls / elapsed_hours

        return min(1.0, calls_per_hour / max_calls_per_hour)

    def reset(self):
        """Reset for fresh start."""
        for role in InstanceRole:
            self._metrics[role] = InstanceMetrics()
            self._last_call[role] = 0
            self._burst_buckets[role].tokens = self._burst_buckets[role].capacity
```

---

## Part 2: Graphiti Layer (Revised) (~280 lines)

**Fixes all critical issues** from the original proposal:
- No GDS dependency (Python-based similarity)
- Uses BYRD's LLM client
- Async extraction queue
- Proper OutcomeDispatcher integration

```python
# src/byrd/knowledge/graphiti_layer.py

"""
BYRD Graphiti Layer - Temporal Knowledge Graph

Fixed for ZAI GLM-4.7:
- Uses DualInstanceManager for rate limiting
- Async extraction queue (non-blocking)
- No GDS dependency (Python similarity)
- Integrates via OutcomeDispatcher, not Memory hooks

EMERGENCE PRINCIPLE:
Graphiti extracts structure from BYRD's own experiences.
Entities and relationships emerge from what BYRD has learned.
"""

import asyncio
import json
import logging
import re  # v8: Added for regex escaping in search
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# v7: Import InstanceRole at top (was at bottom in v6 - caused NameError)
from core.dual_instance_manager import InstanceRole

logger = logging.getLogger(__name__)


class ContradictionStrategy(Enum):
    INVALIDATE_OLD = "invalidate_old"
    FLAG_FOR_REVIEW = "flag_for_review"
    KEEP_BOTH = "keep_both"


@dataclass
class ExtractedEntity:
    name: str
    entity_type: str
    confidence: float
    source_episode_id: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedRelationship:
    source_entity: str
    target_entity: str
    relationship_type: str
    fact: str
    confidence: float
    source_episode_id: str
    valid_from: Optional[datetime] = None


@dataclass
class QueuedEpisode:
    """Episode queued for async extraction."""
    content: str
    source_type: str
    source_id: str
    reference_time: datetime
    metadata: Dict[str, Any]
    queued_at: float


@dataclass
class GraphitiMetrics:
    episodes_queued: int = 0
    episodes_processed: int = 0
    entities_extracted: int = 0
    relationships_extracted: int = 0
    contradictions_detected: int = 0
    extraction_errors: int = 0
    avg_extraction_time: float = 0.0


class GraphitiLayer:
    """
    Temporal knowledge graph layer for BYRD.

    Uses Instance B (enrichment) from DualInstanceManager.
    Processes episodes asynchronously to avoid blocking core operations.
    """

    def __init__(
        self,
        neo4j_driver,
        instance_manager: 'DualInstanceManager',
        config: Dict[str, Any]
    ):
        self.driver = neo4j_driver
        self.instance_manager = instance_manager
        self.config = config

        # Extraction settings
        extraction_config = config.get("extraction", {})
        self.min_confidence = extraction_config.get("min_confidence", 0.7)
        self.min_content_length = extraction_config.get("min_content_length", 50)
        self.custom_entity_types = extraction_config.get("custom_entity_types", [])
        self.queue_max_size = extraction_config.get("queue_max_size", 1000)

        # Temporal settings
        temporal_config = config.get("temporal", {})
        self.temporal_enabled = temporal_config.get("enabled", True)
        self.contradiction_strategy = ContradictionStrategy(
            temporal_config.get("contradiction_strategy", "invalidate_old")
        )

        # Async extraction queue
        self._extraction_queue: asyncio.Queue = asyncio.Queue(maxsize=self.queue_max_size)
        self._extraction_task: Optional[asyncio.Task] = None
        self._shutdown = False

        # Metrics
        self._metrics = GraphitiMetrics()
        self._extraction_times: List[float] = []

    async def initialize_schema(self):
        """
        v7: Initialize Neo4j schema for Graphiti nodes and relationships.
        Creates indexes and constraints for efficient querying.
        """
        async with self.driver.session() as session:
            # Create indexes for GraphitiEntity
            await session.run("""
                CREATE INDEX graphiti_entity_name IF NOT EXISTS
                FOR (e:GraphitiEntity) ON (e.name)
            """)
            await session.run("""
                CREATE INDEX graphiti_entity_type IF NOT EXISTS
                FOR (e:GraphitiEntity) ON (e.entity_type)
            """)

            # Create indexes for GraphitiEpisode
            await session.run("""
                CREATE INDEX graphiti_episode_id IF NOT EXISTS
                FOR (ep:GraphitiEpisode) ON (ep.id)
            """)
            await session.run("""
                CREATE INDEX graphiti_episode_source IF NOT EXISTS
                FOR (ep:GraphitiEpisode) ON (ep.source_id)
            """)

            # Create index for temporal edge queries
            await session.run("""
                CREATE INDEX graphiti_fact_valid IF NOT EXISTS
                FOR ()-[r:GRAPHITI_FACT]-() ON (r.valid_to)
            """)

        logger.info("Graphiti schema initialized")

    async def start(self):
        """Start the background extraction worker."""
        self._shutdown = False
        self._extraction_task = asyncio.create_task(self._extraction_worker())
        logger.info("Graphiti extraction worker started")

    async def stop(self):
        """Stop the extraction worker gracefully."""
        self._shutdown = True
        if self._extraction_task:
            self._extraction_task.cancel()
            try:
                await self._extraction_task
            except asyncio.CancelledError:
                pass
        logger.info("Graphiti extraction worker stopped")

    async def queue_episode(
        self,
        content: str,
        source_type: str,
        source_id: str,
        reference_time: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Queue episode for async extraction (non-blocking).

        Returns True if queued successfully, False if queue is full.
        """
        # Skip short content
        if len(content) < self.min_content_length:
            return False

        episode = QueuedEpisode(
            content=content,
            source_type=source_type,
            source_id=source_id,
            reference_time=reference_time or datetime.now(),
            metadata=metadata or {},
            queued_at=time.time()
        )

        try:
            self._extraction_queue.put_nowait(episode)
            self._metrics.episodes_queued += 1
            return True
        except asyncio.QueueFull:
            logger.warning("Graphiti extraction queue full, dropping episode")
            return False

    async def _extraction_worker(self):
        """Background worker that processes queued episodes."""
        while not self._shutdown:
            try:
                # Wait for episode with timeout
                try:
                    episode = await asyncio.wait_for(
                        self._extraction_queue.get(),
                        timeout=5.0
                    )
                except asyncio.TimeoutError:
                    continue

                # Process episode
                start_time = time.time()
                try:
                    await self._process_episode(episode)
                    self._metrics.episodes_processed += 1
                except Exception as e:
                    logger.error(f"Graphiti extraction error: {e}")
                    self._metrics.extraction_errors += 1
                finally:
                    extraction_time = time.time() - start_time
                    self._extraction_times.append(extraction_time)
                    if len(self._extraction_times) > 100:
                        self._extraction_times = self._extraction_times[-100:]
                    self._metrics.avg_extraction_time = sum(self._extraction_times) / len(self._extraction_times)

                    self._extraction_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Extraction worker error: {e}")
                await asyncio.sleep(1)

    async def _process_episode(self, episode: QueuedEpisode):
        """Process a single episode - extract entities and relationships."""
        # Create episode node
        episode_id = f"ep_{uuid.uuid4().hex[:12]}"
        await self._create_episode_node(episode, episode_id)

        # Extract entities (LLM call via Instance B)
        entities = await self._extract_entities(episode.content, episode_id)

        for entity in entities:
            await self._upsert_entity(entity)

        # Extract relationships if we have 2+ entities (LLM call via Instance B)
        relationships = []
        if len(entities) >= 2:
            relationships = await self._extract_relationships(
                episode.content, entities, episode_id, episode.reference_time
            )

            for rel in relationships:
                await self._create_temporal_edge(rel)

                # Check for contradictions
                if self.temporal_enabled:
                    await self._check_and_handle_contradiction(rel)

        # Link episode to source
        await self._link_episode_to_source(episode_id, episode.source_id, episode.source_type)

        # Update metrics
        self._metrics.entities_extracted += len(entities)
        self._metrics.relationships_extracted += len(relationships)

    async def _extract_entities(
        self,
        content: str,
        episode_id: str
    ) -> List[ExtractedEntity]:
        """Extract entities using Instance B."""
        default_types = ["Person", "Organization", "Location", "Technology", "Event"]
        all_types = default_types + self.custom_entity_types
        types_str = ", ".join(all_types)

        prompt = f"""Extract entities from this text. For each entity, provide:
- name: The entity name (normalized)
- type: One of [{types_str}]
- confidence: How confident you are (0.0-1.0)

Text: {content[:2000]}

Respond with JSON array only:
[{{"name": "...", "type": "...", "confidence": 0.X}}, ...]

If no entities found, respond with: []"""

        try:
            # Use Instance B (enrichment) for extraction
            response = await self.instance_manager.call(
                role=InstanceRole.ENRICHMENT,
                prompt=prompt,
                component="graphiti",
                max_tokens=500
            )

            # Handle LLMResponse object
            response_text = response.text if hasattr(response, 'text') else str(response)

            # Parse JSON
            entities_data = self._parse_json_response(response_text)

            entities = []
            for e in entities_data:
                if e.get("confidence", 0) >= self.min_confidence:
                    entities.append(ExtractedEntity(
                        name=e["name"],
                        entity_type=e["type"],
                        confidence=e["confidence"],
                        source_episode_id=episode_id
                    ))

            return entities

        except Exception as e:
            logger.debug(f"Entity extraction failed: {e}")
            return []

    async def _extract_relationships(
        self,
        content: str,
        entities: List[ExtractedEntity],
        episode_id: str,
        reference_time: datetime
    ) -> List[ExtractedRelationship]:
        """Extract relationships using Instance B."""
        entity_names = [e.name for e in entities]

        prompt = f"""Given these entities: {entity_names}

And this text: {content[:2000]}

Extract relationships between the entities. For each:
- source: Source entity name
- target: Target entity name
- type: Relationship type (e.g., WORKS_FOR, RELATES_TO, USES)
- fact: Human-readable statement
- confidence: Confidence (0.0-1.0)

Respond with JSON array only:
[{{"source": "...", "target": "...", "type": "...", "fact": "...", "confidence": 0.X}}, ...]

If no relationships found, respond with: []"""

        try:
            response = await self.instance_manager.call(
                role=InstanceRole.ENRICHMENT,
                prompt=prompt,
                component="graphiti",
                max_tokens=500
            )

            response_text = response.text if hasattr(response, 'text') else str(response)
            rels_data = self._parse_json_response(response_text)

            relationships = []
            for r in rels_data:
                if r.get("confidence", 0) >= self.min_confidence:
                    relationships.append(ExtractedRelationship(
                        source_entity=r["source"],
                        target_entity=r["target"],
                        relationship_type=r["type"].upper().replace(" ", "_"),
                        fact=r["fact"],
                        confidence=r["confidence"],
                        source_episode_id=episode_id,
                        valid_from=reference_time
                    ))

            return relationships

        except Exception as e:
            logger.debug(f"Relationship extraction failed: {e}")
            return []

    def _parse_json_response(self, response: str) -> List[Dict]:
        """Parse JSON from LLM response, handling markdown."""
        text = response.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return []

    async def _create_episode_node(self, episode: QueuedEpisode, episode_id: str):
        """Create GraphitiEpisode node in Neo4j."""
        async with self.driver.session() as session:
            await session.run("""
                CREATE (e:GraphitiEpisode {
                    id: $id,
                    content: $content,
                    source_type: $source_type,
                    source_id: $source_id,
                    reference_time: datetime($ref_time),
                    created_at: datetime()
                })
            """, {
                "id": episode_id,
                "content": episode.content[:5000],  # Limit content size
                "source_type": episode.source_type,
                "source_id": episode.source_id,
                "ref_time": episode.reference_time.isoformat()
            })

    async def _upsert_entity(self, entity: ExtractedEntity):
        """Create or update entity node."""
        async with self.driver.session() as session:
            await session.run("""
                MERGE (e:GraphitiEntity {name: $name})
                ON CREATE SET
                    e.entity_type = $type,
                    e.confidence = $confidence,
                    e.created_at = datetime(),
                    e.mention_count = 1
                ON MATCH SET
                    e.mention_count = e.mention_count + 1,
                    e.last_mentioned = datetime(),
                    e.confidence = CASE
                        WHEN $confidence > e.confidence THEN $confidence
                        ELSE e.confidence
                    END
            """, {
                "name": entity.name,
                "type": entity.entity_type,
                "confidence": entity.confidence
            })

            # Link to episode
            await session.run("""
                MATCH (e:GraphitiEntity {name: $name})
                MATCH (ep:GraphitiEpisode {id: $episode_id})
                MERGE (ep)-[:EXTRACTED]->(e)
            """, {
                "name": entity.name,
                "episode_id": entity.source_episode_id
            })

    async def _create_temporal_edge(self, rel: ExtractedRelationship):
        """Create relationship with temporal tracking."""
        edge_id = f"edge_{uuid.uuid4().hex[:12]}"

        async with self.driver.session() as session:
            await session.run("""
                MATCH (source:GraphitiEntity {name: $source_name})
                MATCH (target:GraphitiEntity {name: $target_name})
                CREATE (source)-[r:GRAPHITI_FACT {
                    id: $edge_id,
                    relationship_type: $rel_type,
                    fact: $fact,
                    confidence: $confidence,
                    source_episode_id: $episode_id,
                    created_at: datetime(),
                    valid_from: datetime($valid_from),
                    valid_to: null
                }]->(target)
            """, {
                "source_name": rel.source_entity,
                "target_name": rel.target_entity,
                "edge_id": edge_id,
                "rel_type": rel.relationship_type,
                "fact": rel.fact,
                "confidence": rel.confidence,
                "episode_id": rel.source_episode_id,
                "valid_from": (rel.valid_from or datetime.now()).isoformat()
            })

    async def _check_and_handle_contradiction(self, rel: ExtractedRelationship):
        """Check for and handle contradicting facts."""
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (source:GraphitiEntity {name: $source_name})
                      -[r:GRAPHITI_FACT {relationship_type: $rel_type}]->
                      (target:GraphitiEntity {name: $target_name})
                WHERE r.valid_to IS NULL
                  AND r.fact <> $new_fact
                RETURN r.id as edge_id, r.fact as old_fact
                LIMIT 1
            """, {
                "source_name": rel.source_entity,
                "target_name": rel.target_entity,
                "rel_type": rel.relationship_type,
                "new_fact": rel.fact
            })

            record = await result.single()

            if record:
                self._metrics.contradictions_detected += 1

                if self.contradiction_strategy == ContradictionStrategy.INVALIDATE_OLD:
                    await session.run("""
                        MATCH ()-[r:GRAPHITI_FACT {id: $edge_id}]->()
                        SET r.valid_to = datetime(),
                            r.invalidated_by = $new_fact
                    """, {
                        "edge_id": record["edge_id"],
                        "new_fact": rel.fact
                    })

    async def _link_episode_to_source(
        self,
        episode_id: str,
        source_id: str,
        source_type: str
    ):
        """Link episode to its source node."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (ep:GraphitiEpisode {id: $episode_id})
                MATCH (source {id: $source_id})
                MERGE (ep)-[:DERIVED_FROM]->(source)
            """, {
                "episode_id": episode_id,
                "source_id": source_id
            })

    # =========================================================================
    # SEARCH (No GDS dependency - Python-based similarity)
    # =========================================================================

    async def search_entities(
        self,
        query: str,
        limit: int = 10,
        entity_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """Search entities using keyword matching (no GDS required)."""
        async with self.driver.session() as session:
            type_filter = ""
            # v8: Escape regex metacharacters to prevent injection
            escaped_query = re.escape(query)
            params = {"query": f"(?i).*{escaped_query}.*", "limit": limit}

            if entity_types:
                type_filter = "AND e.entity_type IN $types"
                params["types"] = entity_types

            result = await session.run(f"""
                MATCH (e:GraphitiEntity)
                WHERE e.name =~ $query {type_filter}
                RETURN e.name as name,
                       e.entity_type as type,
                       e.mention_count as mentions,
                       e.confidence as confidence
                ORDER BY e.mention_count DESC
                LIMIT $limit
            """, params)

            return await result.data()

    async def get_entity_facts(
        self,
        entity_name: str,
        include_expired: bool = False
    ) -> List[Dict]:
        """Get all facts about an entity."""
        valid_filter = "" if include_expired else "AND r.valid_to IS NULL"

        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (e:GraphitiEntity {{name: $name}})-[r:GRAPHITI_FACT]-(other:GraphitiEntity)
                WHERE true {valid_filter}
                RETURN e.name as entity,
                       type(r) as rel_type,
                       r.fact as fact,
                       r.valid_from as valid_from,
                       r.valid_to as valid_to,
                       other.name as related_entity
                ORDER BY r.valid_from DESC
            """, {"name": entity_name})

            return await result.data()

    async def trace_provenance(self, entity_name: str) -> List[Dict]:
        """Trace entity back to source experiences."""
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (e:GraphitiEntity {name: $name})
                MATCH (ep:GraphitiEpisode)-[:EXTRACTED]->(e)
                OPTIONAL MATCH (ep)-[:DERIVED_FROM]->(source)
                RETURN ep.id as episode_id,
                       ep.content as episode_content,
                       ep.reference_time as reference_time,
                       source.id as source_id,
                       labels(source)[0] as source_type
                ORDER BY ep.reference_time ASC
            """, {"name": entity_name})

            return await result.data()

    def get_metrics(self) -> Dict[str, Any]:
        """Get Graphiti metrics."""
        return {
            "episodes_queued": self._metrics.episodes_queued,
            "episodes_processed": self._metrics.episodes_processed,
            "queue_size": self._extraction_queue.qsize(),
            "entities_extracted": self._metrics.entities_extracted,
            "relationships_extracted": self._metrics.relationships_extracted,
            "contradictions_detected": self._metrics.contradictions_detected,
            "extraction_errors": self._metrics.extraction_errors,
            "avg_extraction_time": round(self._metrics.avg_extraction_time, 2),
            "extraction_rate": (
                self._metrics.entities_extracted / max(1, self._metrics.episodes_processed)
            )
        }

    def reset(self):
        """Reset metrics."""
        self._metrics = GraphitiMetrics()
        self._extraction_times.clear()
```

---

## Part 3: Enhanced OutcomeDispatcher with Graphiti (~110 lines)

**Extends** v5 Part 1 to integrate Graphiti as a learning component.

```python
# src/byrd/core/outcome_dispatcher.py
#
# v8 Enhancement: Adds Graphiti integration

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum

class OutcomeType(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    TIMEOUT = "timeout"


@dataclass
class TaskOutcome:
    task_id: str
    outcome_type: OutcomeType
    strategy: str
    description: str
    execution_time_ms: int
    query_used: Optional[str] = None
    retrieved_node_ids: List[str] = field(default_factory=list)
    prediction_before: Optional[float] = None
    error_message: Optional[str] = None


class OutcomeDispatcher:
    """
    Routes outcomes to learning components using ACTUAL interfaces.

    v9: Now includes Graphiti for temporal knowledge graph enrichment.
    """

    def __init__(
        self,
        learned_retriever=None,
        intuition_network=None,
        desire_classifier=None,
        memory_tracker: Optional['MemoryTracker'] = None,
        goal_discoverer: Optional['GoalDiscoverer'] = None,
        learning_progress: Optional['LearningProgressTracker'] = None,
        graphiti_layer: Optional['GraphitiLayer'] = None  # v8: Add Graphiti
    ):
        self._retriever = learned_retriever
        self._intuition = intuition_network
        self._classifier = desire_classifier
        self._memory = memory_tracker
        self._goals = goal_discoverer
        self._progress = learning_progress
        self._graphiti = graphiti_layer  # v8

    async def dispatch(self, outcome: TaskOutcome) -> Dict[str, bool]:
        """Dispatch outcome to all components including Graphiti."""
        results = {}
        success = outcome.outcome_type == OutcomeType.SUCCESS

        # 1. Update learned retriever
        if self._retriever and outcome.query_used and outcome.retrieved_node_ids:
            for node_id in outcome.retrieved_node_ids:
                await self._retriever.record_feedback(
                    query=outcome.query_used,
                    node_id=node_id,
                    was_helpful=success
                )
            results['retriever'] = True

        # 2. Update intuition network
        if self._intuition:
            await self._intuition.record_outcome(
                situation=outcome.description,
                action=outcome.strategy,
                success=success
            )
            results['intuition'] = True

        # 3. Update desire classifier
        if self._classifier:
            self._classifier.record_feedback(
                desire={'description': outcome.description},
                actual_outcome=outcome.outcome_type.value,
                was_correct_routing=success
            )
            results['classifier'] = True

        # 4. Memory tracker
        if self._memory:
            results['memory'] = self._memory.record(outcome)

        # 5. Goal discoverer
        if self._goals:
            predicted = outcome.prediction_before if outcome.prediction_before is not None else 0.5
            actual = 1.0 if success else 0.0
            results['goals'] = self._goals.process_prediction_error(
                category=outcome.strategy,
                predicted=predicted,
                actual=actual,
                was_success=success
            )

        # 6. Learning progress
        if self._progress:
            results['progress'] = self._progress.record(outcome)

        # 7. v8: Graphiti temporal knowledge graph
        if self._graphiti:
            # Build rich content for entity extraction
            outcome_content = self._build_graphiti_content(outcome, success)

            # Queue for async extraction (non-blocking)
            queued = await self._graphiti.queue_episode(
                content=outcome_content,
                source_type="task_outcome",
                source_id=outcome.task_id,
                metadata={
                    "strategy": outcome.strategy,
                    "success": success,
                    "execution_time_ms": outcome.execution_time_ms
                }
            )
            results['graphiti'] = queued

        return results

    def _build_graphiti_content(self, outcome: TaskOutcome, success: bool) -> str:
        """Build rich content for Graphiti entity extraction."""
        status = "succeeded" if success else "failed"

        content = f"Strategy '{outcome.strategy}' {status}: {outcome.description}"

        if outcome.query_used:
            content += f"\nQuery: {outcome.query_used}"

        if outcome.error_message:
            content += f"\nError: {outcome.error_message}"

        return content
```

---

## Part 4: Rate-Limited LLM Client Wrapper (~80 lines)

**Enhances** BYRD's LLM client to use DualInstanceManager.

```python
# Additions to src/byrd/llm_client.py

from typing import Optional  # v8: Added for type hint
from core.dual_instance_manager import DualInstanceManager  # v9: Removed unused InstanceRole

# Global instance manager (set during initialization)
_instance_manager: Optional[DualInstanceManager] = None


def set_instance_manager(manager: DualInstanceManager):
    """Set the global instance manager for rate limiting."""
    global _instance_manager
    _instance_manager = manager


def get_instance_manager() -> Optional[DualInstanceManager]:
    """Get the global instance manager."""
    return _instance_manager


class RateLimitedLLMClient:
    """
    LLM client wrapper that routes through DualInstanceManager.

    Ensures proper rate limiting and instance routing for ZAI GLM-4.7.
    """

    def __init__(self, base_client, component: str = "unknown"):
        """
        Args:
            base_client: The underlying LLM client
            component: Component name for routing (dreamer, seeker, graphiti, etc.)
        """
        self._client = base_client
        self._component = component

    async def generate(self, prompt: str, **kwargs) -> 'LLMResponse':
        """Generate with rate limiting via instance manager."""
        manager = get_instance_manager()

        if manager:
            # Route through dual instance manager
            return await manager.call_by_component(
                component=self._component,
                prompt=prompt,
                **kwargs
            )
        else:
            # Fallback to direct call (for testing or single-instance mode)
            return await self._client.generate(prompt, **kwargs)

    async def query(self, prompt: str, **kwargs) -> str:
        """Query shorthand that returns text."""
        response = await self.generate(prompt, **kwargs)
        return response.text if hasattr(response, 'text') else str(response)

    @property
    def model_name(self) -> str:
        return self._client.model_name


def create_rate_limited_client(base_client, component: str) -> RateLimitedLLMClient:
    """Factory for creating rate-limited client wrappers."""
    return RateLimitedLLMClient(base_client, component)
```

---

## Part 5: Enhanced Initialization (~100 lines)

**Extends** v5 Part 12 with Graphiti and dual instance setup.

```python
# Additions to src/byrd/byrd.py

from core.dual_instance_manager import DualInstanceManager  # v10: Removed unused InstanceRole
from knowledge.graphiti_layer import GraphitiLayer
from llm_client import set_instance_manager, create_rate_limited_client

class Byrd:
    def __init__(self, config: Dict = None):
        # Existing init...
        self.config = config or {}

        # v5 learning components
        self._dispatcher = None
        self._memory_tracker = None
        self._learning_progress = None
        self._goal_discoverer = None
        self._result_cache = None
        self._wikipedia = None
        self._arxiv = None

        # v8: Dual instance and Graphiti
        self._instance_manager = None
        self._graphiti = None

    async def _initialize_dual_instances(self):
        """Initialize dual instance manager for rate limiting."""
        llm_config = self.config.get('local_llm', {})

        self._instance_manager = DualInstanceManager(
            llm_client=self.llm_client,
            config=llm_config
        )

        # Set global instance manager
        set_instance_manager(self._instance_manager)

        # Create rate-limited clients for components
        self.dreamer_client = create_rate_limited_client(self.llm_client, "dreamer")
        self.seeker_client = create_rate_limited_client(self.llm_client, "seeker")
        self.graphiti_client = create_rate_limited_client(self.llm_client, "graphiti")

        logger.info("Dual instance manager initialized")

    async def _initialize_graphiti(self):
        """Initialize Graphiti temporal knowledge graph."""
        graphiti_config = self.config.get('graphiti', {})

        if not graphiti_config.get('enabled', False):
            logger.info("Graphiti disabled in config")
            return

        if not self._instance_manager:
            logger.warning("Cannot init Graphiti without instance manager")
            return

        self._graphiti = GraphitiLayer(
            neo4j_driver=self.memory.driver,
            instance_manager=self._instance_manager,
            config=graphiti_config
        )

        # Initialize schema
        await self._graphiti.initialize_schema()

        # Start extraction worker
        await self._graphiti.start()

        logger.info("Graphiti layer initialized")

    async def _initialize_learning_substrate(self):
        """Initialize learning components with proper wiring."""
        from core.outcome_dispatcher import OutcomeDispatcher
        from core.memory_tracker import MemoryTracker
        from core.learning_progress import LearningProgressTracker
        from emergence.goal_discoverer import GoalDiscoverer
        from knowledge.cache import ResultCache
        from knowledge.wikipedia_backend import WikipediaBackend
        from knowledge.arxiv_backend import ArxivBackend
        from api.health import set_byrd_instance

        # Core tracking
        self._memory_tracker = MemoryTracker(
            max_events=self.config.get('learning', {}).get('memory_tracker', {}).get('max_events', 10000)
        )
        self._learning_progress = LearningProgressTracker(
            window_size=self.config.get('learning', {}).get('learning_progress', {}).get('window_size', 100)
        )
        self._goal_discoverer = GoalDiscoverer(
            error_threshold=self.config.get('learning', {}).get('goal_discoverer', {}).get('error_threshold', 0.3),
            pattern_threshold=self.config.get('learning', {}).get('goal_discoverer', {}).get('pattern_threshold', 5),
            max_goals=self.config.get('learning', {}).get('goal_discoverer', {}).get('max_goals', 50)
        )

        # Knowledge backends
        self._result_cache = ResultCache(
            max_entries=self.config.get('cache', {}).get('max_entries', 1000)
        )
        self._wikipedia = WikipediaBackend(cache=self._result_cache)
        self._arxiv = ArxivBackend(cache=self._result_cache)

        # v8: Central dispatcher with Graphiti
        self._dispatcher = OutcomeDispatcher(
            learned_retriever=self.learned_retriever,
            intuition_network=self.intuition_network,
            desire_classifier=self.desire_classifier,
            memory_tracker=self._memory_tracker,
            goal_discoverer=self._goal_discoverer,
            learning_progress=self._learning_progress,
            graphiti_layer=self._graphiti  # v8: Add Graphiti
        )

        # Inject into Seeker
        self.seeker.set_dispatcher(self._dispatcher)
        self.seeker.set_intuition_network(self.intuition_network)

        # Register for health endpoint
        set_byrd_instance(self)

    async def start(self):
        """Enhanced start with dual instances and Graphiti."""
        # Existing startup
        await self._awaken_if_needed()
        await self._ensure_architecture_loaded()

        # v8: Initialize dual instances first
        await self._initialize_dual_instances()

        # v8: Initialize Graphiti
        await self._initialize_graphiti()

        # Initialize learning substrate
        await self._initialize_learning_substrate()

        # Start components
        await self._start_components()

    async def shutdown(self):
        """Clean shutdown including Graphiti."""
        # Stop Graphiti worker
        if self._graphiti:
            await self._graphiti.stop()

        # Close knowledge backends
        if self._wikipedia:
            await self._wikipedia.close()
        if self._arxiv:
            await self._arxiv.close()

        # Existing shutdown...
```

---

## Part 6: Health Endpoint with Graphiti Metrics (~70 lines)

**Extends** v5 Part 11.

```python
# src/byrd/api/health.py - v8 additions

@router.get("/health/learning")
async def learning_health(components: dict = Depends(get_learning_components)) -> Dict[str, Any]:
    """Return learning system health metrics including Graphiti."""
    if not components:
        return {"status": "not_initialized", "error": "Byrd instance not set"}

    result = {"status": "healthy"}

    if components.get('memory_tracker'):
        result['memory'] = components['memory_tracker'].get_stats()

    if components.get('learning_progress'):
        result['learning'] = components['learning_progress'].get_stats()

    if components.get('goal_discoverer'):
        result['emergent_goals'] = components['goal_discoverer'].get_stats()

    if components.get('instance_manager'):
        result['instances'] = components['instance_manager'].get_metrics()

    # v8: Graphiti metrics
    if components.get('graphiti'):
        result['graphiti'] = components['graphiti'].get_metrics()

    return result


@router.get("/health/graphiti")
async def graphiti_health(components: dict = Depends(get_learning_components)) -> Dict[str, Any]:
    """Detailed Graphiti health metrics."""
    graphiti = components.get('graphiti')

    if not graphiti:
        return {"status": "disabled", "message": "Graphiti not enabled"}

    metrics = graphiti.get_metrics()

    # Add health assessment
    # v8: Fixed threshold order (check largest first)
    queue_health = "healthy"
    if metrics['queue_size'] > 800:
        queue_health = "critical"
    elif metrics['queue_size'] > 500:
        queue_health = "backlogged"

    extraction_health = "healthy"
    if metrics['extraction_errors'] > metrics['episodes_processed'] * 0.1:
        extraction_health = "degraded"

    return {
        "status": "running",
        "queue_health": queue_health,
        "extraction_health": extraction_health,
        "metrics": metrics
    }


@router.get("/graphiti/entities")
async def list_entities(
    query: str = "",
    limit: int = 20,
    components: dict = Depends(get_learning_components)
) -> List[Dict]:
    """Search Graphiti entities."""
    graphiti = components.get('graphiti')
    if not graphiti:
        return []

    return await graphiti.search_entities(query, limit)


@router.get("/graphiti/entity/{name}/facts")
async def get_entity_facts(
    name: str,
    include_expired: bool = False,
    components: dict = Depends(get_learning_components)
) -> List[Dict]:
    """Get facts about an entity."""
    graphiti = components.get('graphiti')
    if not graphiti:
        return []

    return await graphiti.get_entity_facts(name, include_expired)


@router.get("/graphiti/entity/{name}/provenance")
async def get_entity_provenance(
    name: str,
    components: dict = Depends(get_learning_components)
) -> List[Dict]:
    """Trace entity provenance to source experiences."""
    graphiti = components.get('graphiti')
    if not graphiti:
        return []

    return await graphiti.trace_provenance(name)
```

---

## v5 Components (Unchanged)

The following v5 components remain unchanged in v10:

| Part | Component | Status |
|------|-----------|--------|
| Part 2 | DesireClassifier Learning | Unchanged |
| Part 3 | Memory Tracker | Unchanged |
| Part 4 | Seeker Integration | Unchanged |
| Part 5 | Learning Progress Tracker | Unchanged |
| Part 6 | Goal Discoverer | Unchanged |
| Part 8 | Wikipedia Backend | Unchanged |
| Part 9 | ArXiv Backend | Unchanged |
| Part 10 | Result Cache | Unchanged |

---

## Configuration Summary

```yaml
# config.yaml - Complete v10 configuration

local_llm:
  provider: "zai"
  model: "glm-4.7"

  # Optimized for Max Coding Plan
  rate_limit:
    interval_seconds: 8.0
    burst_tokens: 3
    burst_recovery_seconds: 24.0

  dual_instance:
    enabled: true
    instance_a:
      role: "primary"
      components: ["dreamer", "seeker", "actor"]
    instance_b:
      role: "enrichment"
      components: ["graphiti", "capability_evaluator", "code_verifier"]

graphiti:
  enabled: true

  extraction:
    queue_max_size: 1000
    min_confidence: 0.7
    min_content_length: 50
    custom_entity_types:
      - Concept
      - Capability
      - Principle
      - Pattern
      - Limitation
      - Strategy

  temporal:
    enabled: true
    contradiction_strategy: "invalidate_old"

learning:
  outcome_dispatcher:
    enabled: true

  desire_classifier:
    learning_rate: 0.1

  memory_tracker:
    max_events: 10000

  learning_progress:
    window_size: 100
    snapshot_interval: 10

  goal_discoverer:
    error_threshold: 0.3
    pattern_threshold: 5
    max_goals: 50
    time_window_seconds: 3600

knowledge_backends:
  wikipedia:
    enabled: true
  arxiv:
    enabled: true

cache:
  max_entries: 1000
  default_ttl: 3600
```

---

## Line Count Summary

| Part | Component | Lines | Change from v9 |
|------|-----------|-------|----------------|
| 1 | Dual Instance Manager | ~116 | -1 (removed List import) |
| 2 | Graphiti Layer | ~316 | Unchanged |
| 3 | OutcomeDispatcher (enhanced) | ~110 | Unchanged |
| 4 | Rate-Limited LLM Client | ~81 | Unchanged |
| 5 | Enhanced Initialization | ~100 | Unchanged (comment only) |
| 6 | Health Endpoint (enhanced) | ~71 | Unchanged |
| - | v5 unchanged components | ~545 | From v5 |
| **TOTAL** | | **~1,339** | -1 from v9 |

---

## Implementation Order

### Phase A: Rate Limit Optimization (Day 1)
1. Part 1: Dual Instance Manager
2. Part 4: Rate-Limited LLM Client
3. Update config.yaml with new rate limit settings
4. Test dual instance routing

### Phase B: v5 Core (Day 1-2)
5. v5 Parts 3, 5, 6, 10: Self-contained components
6. Part 3: Enhanced OutcomeDispatcher
7. v5 Part 4: Seeker Integration
8. Part 5: Enhanced Initialization (partial)

### Phase C: Graphiti Integration (Day 2-3)
9. Part 2: Graphiti Layer
10. Part 5: Complete initialization with Graphiti
11. Part 6: Enhanced Health Endpoint
12. Test entity extraction and provenance

### Phase D: Knowledge Backends (Day 3)
13. v5 Parts 8, 9: Wikipedia/ArXiv
14. Full integration testing
15. Performance tuning

---

## Capacity Planning

### ZAI Max Coding Plan Utilization

| Workload | Instance | Calls/Hour | % of 480/hr |
|----------|----------|------------|-------------|
| Dreamer cycles | A | ~30 | 6.3% |
| Seeker operations | A | ~120 | 25% |
| Actor reasoning | A | ~30 | 6.3% |
| **Instance A Total** | | **~180** | **37.5%** |
| Graphiti extraction | B | ~200 | 41.7% |
| Capability evaluation | B | ~40 | 8.3% |
| Code verification | B | ~20 | 4.2% |
| **Instance B Total** | | **~260** | **54.2%** |
| **Grand Total** | | **~440** | **45.8% of 960** |

**Headroom**: ~520 calls/hour available for bursts

---

## What Changed From v9

| v9 Issue | v10 Fix |
|----------|---------|
| Unused `List` import in Part 1 | Removed from typing imports |
| Unused `InstanceRole` import in Part 5 | Removed from imports |
| "unchanged in v8" in docs section | Updated to "v10" |
| "v8 configuration" in config comment | Updated to "v10" |

## What Changed From v8 (in v9)

| v8 Issue | v9 Fix |
|----------|--------|
| Unused `RateLimitConfig` dataclass | Removed (never instantiated) |
| Unused `defaultdict` import in Part 2 | Removed from imports |
| Unused `Tuple` import in Part 2 | Removed from typing imports |
| Stale "v6" reference in Part 3 docstring | Updated to "v9" |
| Unused `InstanceRole` import in Part 4 | Removed from imports |

## What Changed From v7 (in v8)

| v7 Issue | v8 Fix |
|----------|--------|
| Queue health checks `> 500` before `> 800` | Reordered to check 800 first |
| Unused `deque` import in Part 1 | Removed unused import |
| Regex injection risk in `search_entities()` | Added `re.escape()` for query safety |
| Missing `Optional` import in Part 4 | Added `from typing import Optional` |
| Stale "v6" references throughout | Updated all to "v8" |

## What Changed From v6 (in v7)

| v6 Issue | v7 Fix |
|----------|--------|
| `InstanceRole` import at bottom of file | Moved to top of Part 2 imports |
| Missing `initialize_schema()` method | Added with Neo4j indexes for Graphiti nodes |
| Incorrect utilization calculation | Added `session_start` to InstanceMetrics |

## What Changed From v5 (in v6)

| v5 Issue | v6 Fix |
|----------|--------|
| Single instance bottleneck | Dual Instance Manager with routing |
| 10s rate limit (conservative) | 8s interval optimized for Max Plan |
| No Graphiti integration | Full Graphiti layer with async queue |
| No entity extraction | Automatic extraction on enrichment instance |
| No temporal tracking | Bi-temporal facts with contradiction detection |
| Fixed rate limiting | Burst handling with token bucket |

---

## Bugs Fixed (Cumulative)

| Version | Bugs Fixed |
|---------|------------|
| v1→v2 | Interface mismatches |
| v2→v3 | 8 bugs (prediction timing, EMA, etc.) |
| v3→v4 | Decorator signature, _strategy_stats init |
| v4→v5 | Missing Dict import |
| v5→v6 | Rate limit optimization, Graphiti integration |
| v6→v7 | InstanceRole import order, missing initialize_schema, utilization calc |
| v7→v8 | Queue health logic, unused import, regex injection, Optional import, stale comments |
| v8→v9 | Unused RateLimitConfig, unused defaultdict/Tuple/InstanceRole imports, stale v6 comment |
| v9→v10 | Unused List import, unused InstanceRole import (Part 5), stale v8 doc references |

**Total bugs fixed across all versions: 30**

---

## Graphiti Critical Issues Resolved

| Original Issue | Resolution |
|----------------|------------|
| Rate limiting blocks system | Async queue + Instance B isolation |
| GDS library required | Python-based similarity (no GDS) |
| Memory signature mismatch | Integrated via OutcomeDispatcher |
| Embedding system missing | Deferred (keyword search for v6) |
| Ollama config hardcoded | Uses BYRD's existing LLM client |
| No v5 integration | OutcomeDispatcher component |

---

## Source Documents

- `COMBINED_IMPLEMENTATION_PLAN.md` (v5) - Base learning infrastructure
- `GRAPHITI_IMPLEMENTATION_PROPOSAL.md` - Original Graphiti design
- `CONNECTION_PLAN.md` - Dual instance architecture
- `CLAUDE.md` - BYRD interfaces and patterns

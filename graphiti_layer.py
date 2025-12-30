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
import re
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from dual_instance_manager import InstanceRole

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
        Initialize Neo4j schema for Graphiti nodes and relationships.
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
            # Escape regex metacharacters to prevent injection
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

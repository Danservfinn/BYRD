"""
BYRD Memory System
Neo4j graph database interface for persistent memory.

EMERGENCE PRINCIPLE:
Type fields are open strings - the examples in comments are not exhaustive.
BYRD can create experiences, beliefs, desires, and reflections with any type
value. We do not constrain what categories BYRD can use.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json
import re
from neo4j import GraphDatabase, AsyncGraphDatabase
import hashlib

from event_bus import event_bus, Event, EventType
from quantum_randomness import get_quantum_float


# =============================================================================
# ONTOLOGY CONSTANTS
# =============================================================================
# BYRD can create custom node types beyond these system types.
# System types have dedicated methods; custom types use the generic API.

SYSTEM_NODE_TYPES = frozenset({
    'Experience',     # Raw observations, interactions, events
    'Belief',         # Derived understanding with confidence
    'Desire',         # Goals and motivations with intensity
    'Reflection',     # Dream cycle outputs (BYRD's raw thoughts)
    'Capability',     # Tools and abilities
    'Mutation',       # Audit trail of self-modifications (protected)
    'Ego',            # Living identity (mutable by BYRD)
    'QuantumMoment',  # Quantum influence tracking (system-created)
    'SystemState',    # System counters and state (system-created)
    'Crystal',        # Crystallized memories (unified concepts)
})

# Valid node states for memory lifecycle
NODE_STATES = frozenset({
    'active',        # Normal node, in context retrieval
    'crystallized',  # Part of a crystal, lower retrieval priority
    'archived',      # Soft deleted, excluded from retrieval
    'forgotten',     # Marked for deletion or deleted
})

# Properties managed by the system - cannot be set via create_node
RESERVED_PROPERTIES = frozenset({
    'id',           # Auto-generated UUID
    'timestamp',    # Auto-generated ISO datetime
    'node_type',    # Stored for easy querying
    'created_at',   # Alias for timestamp
    'updated_at',   # Set on updates
    '_labels',      # Internal Neo4j labels
})


@dataclass
class Experience:
    id: str
    content: str
    type: str  # Examples: interaction, observation, action, dream, reflection, system
    timestamp: datetime
    embedding: Optional[List[float]] = None


@dataclass
class Belief:
    id: str
    content: str
    confidence: float
    formed_at: datetime
    derived_from: List[str] = None  # Experience IDs


@dataclass
class Desire:
    id: str
    description: str
    type: str  # Examples: knowledge, capability, goal, exploration - BYRD may use any type
    intensity: float
    formed_at: datetime
    fulfilled: bool = False
    plan: List[str] = None
    # Reflective failure processing fields
    attempt_count: int = 0
    last_attempted: Optional[datetime] = None
    status: str = "active"  # active | dormant | needs_reflection | fulfilled


@dataclass
class Capability:
    id: str
    name: str
    description: str
    type: str  # Examples: innate, mcp, plugin, skill - extensible
    config: Dict[str, Any]
    active: bool = True
    acquired_at: datetime = None


@dataclass
class Reflection:
    """
    A reflection is BYRD's raw output from a dream cycle.

    EMERGENCE PRINCIPLE:
    We store whatever BYRD outputs without forcing it into our categories.
    The raw_output preserves BYRD's own vocabulary and structure.
    """
    id: str
    raw_output: Dict[str, Any]  # BYRD's unmodified output
    timestamp: datetime
    source_experiences: List[str] = field(default_factory=list)  # Experience IDs


@dataclass
class Crystal:
    """
    A crystallized memory - multiple related nodes unified into one.

    Crystals emerge when BYRD identifies that several experiences, beliefs,
    or other nodes express the same underlying concept. The crystal captures
    the unified essence while preserving distinct facets.

    Crystal types are emergent - BYRD decides what kind of crystal to form:
    - insight: Pattern or understanding that emerged from experiences
    - memory: Consolidated experiences about a topic
    - belief: Unified beliefs about a concept
    - pattern: Recurring theme or structure
    """
    id: str
    essence: str                    # Unified meaning of crystallized nodes
    crystal_type: str               # insight, memory, belief, pattern, or custom
    facets: List[str]               # Distinct aspects preserved from sources
    source_node_ids: List[str]      # Nodes that crystallized into this
    confidence: float               # How certain the crystallization is
    created_at: datetime
    updated_at: Optional[datetime] = None
    node_count: int = 0             # Number of nodes crystallized
    quantum_value: Optional[float] = None   # Quantum value that selected this
    quantum_source: Optional[str] = None    # "quantum" or "classical"


class Memory:
    """
    The single source of truth.
    All experiences, beliefs, desires, and capabilities live here.
    """

    def __init__(self, config: Dict[str, str]):
        self.uri = config.get("neo4j_uri", "bolt://localhost:7687")
        self.user = config.get("neo4j_user", "neo4j")
        self.password = config.get("neo4j_password", "password")
        self.driver = None

        # Experience noise filtering
        filter_config = config.get("experience_filter", {})
        self.filter_enabled = filter_config.get("enabled", False)
        self.exclude_patterns = []
        for pattern in filter_config.get("exclude_patterns", []):
            try:
                self.exclude_patterns.append(re.compile(pattern))
            except re.error:
                pass  # Skip invalid regex

        # Salience-weighted retrieval configuration
        retrieval_config = config.get("retrieval", {})
        self.retrieval_strategy = retrieval_config.get("strategy", "recent")
        self.salience_weight = retrieval_config.get("salience_weight", 0.3)
        self.recency_weight = retrieval_config.get("recency_weight", 0.7)
    
    async def connect(self):
        """Initialize connection to Neo4j (idempotent - safe to call multiple times)."""
        if self.driver is None:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            await self._ensure_schema()
        else:
            # Verify the connection is still alive
            try:
                async with self.driver.session() as session:
                    await session.run("RETURN 1")
            except Exception:
                # Driver exists but connection is dead - recreate
                try:
                    await self.driver.close()
                except Exception:
                    pass
                self.driver = AsyncGraphDatabase.driver(
                    self.uri,
                    auth=(self.user, self.password)
                )
                await self._ensure_schema()
    
    async def close(self):
        if self.driver:
            await self.driver.close()
    
    async def _ensure_schema(self):
        """Create indexes for efficient queries."""
        async with self.driver.session() as session:
            # Indexes for common queries
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (e:Experience) ON (e.timestamp)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (d:Desire) ON (d.fulfilled, d.intensity)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (d:Desire) ON (d.status)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (c:Capability) ON (c.active)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (b:Belief) ON (b.confidence)
            """)
            # Index for Reflections (emergence-compliant storage)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (r:Reflection) ON (r.timestamp)
            """)
            # Indexes for Crystal memory system
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (c:Crystal) ON (c.timestamp)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (c:Crystal) ON (c.crystal_type)
            """)
    
    def _generate_id(self, content: str) -> str:
        """Generate deterministic ID from content."""
        return hashlib.sha256(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
    
    # =========================================================================
    # EXPERIENCES
    # =========================================================================

    def _is_noise(self, content: str) -> bool:
        """Check if content matches noise patterns that should be filtered."""
        if not self.filter_enabled or not self.exclude_patterns:
            return False

        for pattern in self.exclude_patterns:
            if pattern.search(content):
                return True

        return False

    async def record_experience(
        self,
        content: str,
        type: str,
        embedding: Optional[List[float]] = None,
        force: bool = False,
        link_on_acquisition: bool = True
    ) -> Optional[str]:
        """
        Record a new experience.

        Args:
            content: The experience content
            type: Experience type (open string)
            embedding: Optional embedding vector
            force: If True, bypass noise filtering
            link_on_acquisition: If True, immediately link to similar beliefs (reduces orphans)

        Returns:
            Experience ID, or None if filtered as noise
        """
        # Apply noise filtering (unless forced or system type)
        if not force and type not in ("system", "awakening", "action"):
            if self._is_noise(content):
                return None  # Silently filter noise

        exp_id = self._generate_id(content)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (e:Experience {
                    id: $id,
                    content: $content,
                    type: $type,
                    timestamp: datetime(),
                    embedding: $embedding
                })
            """, id=exp_id, content=content, type=type, embedding=embedding)

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.EXPERIENCE_CREATED,
            data={
                "id": exp_id,
                "content": content,
                "type": type
            }
        ))

        # Link-on-acquisition: immediately connect to similar beliefs to reduce orphans
        if link_on_acquisition and len(content) >= self.CONNECTION_HEURISTIC_CONFIG["min_content_length"]:
            await self._link_experience_on_acquisition(exp_id, content)

        return exp_id
    
    async def get_recent_experiences(
        self,
        limit: int = 50,
        type: Optional[str] = None
    ) -> List[Dict]:
        """
        Get recent experiences using configured retrieval strategy.

        Strategies:
        - "recent": Pure chronological (default)
        - "salient": By connection count (most connected first)
        - "hybrid": Mix of recent and salient based on weights
        """
        if self.retrieval_strategy == "hybrid":
            return await self._get_hybrid_experiences(limit, type)
        elif self.retrieval_strategy == "salient":
            return await self._get_salient_experiences(limit, type)
        else:
            # Default: pure recent
            return await self._get_recent_experiences(limit, type)

    async def _get_recent_experiences(
        self,
        limit: int,
        type: Optional[str] = None
    ) -> List[Dict]:
        """Pure chronological retrieval."""
        query = """
            MATCH (e:Experience)
            WHERE $type IS NULL OR e.type = $type
            RETURN e
            ORDER BY e.timestamp DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, type=type, limit=limit)
            records = await result.data()
            return [r["e"] for r in records]

    async def _get_salient_experiences(
        self,
        limit: int,
        type: Optional[str] = None
    ) -> List[Dict]:
        """Retrieval by salience (connection count)."""
        query = """
            MATCH (e:Experience)
            WHERE $type IS NULL OR e.type = $type
            OPTIONAL MATCH (e)-[r]-()
            WITH e, count(r) as connections
            RETURN e, connections
            ORDER BY connections DESC, e.timestamp DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, type=type, limit=limit)
            records = await result.data()
            return [r["e"] for r in records]

    async def _get_hybrid_experiences(
        self,
        limit: int,
        type: Optional[str] = None
    ) -> List[Dict]:
        """
        Hybrid retrieval: mix of recent and salient experiences.

        Uses configured weights to blend results:
        - recency_weight portion from most recent
        - salience_weight portion from most connected
        """
        recent_count = int(limit * self.recency_weight)
        salient_count = int(limit * self.salience_weight)

        # Ensure we get at least 1 of each if weights are non-zero
        if self.recency_weight > 0 and recent_count == 0:
            recent_count = 1
        if self.salience_weight > 0 and salient_count == 0:
            salient_count = 1

        # Get recent experiences
        recent = await self._get_recent_experiences(recent_count, type)

        # Get salient experiences (excluding those already in recent)
        recent_ids = {e.get("id") for e in recent}

        salient_query = """
            MATCH (e:Experience)
            WHERE ($type IS NULL OR e.type = $type)
            AND NOT e.id IN $exclude_ids
            OPTIONAL MATCH (e)-[r]-()
            WITH e, count(r) as connections
            WHERE connections > 0
            RETURN e
            ORDER BY connections DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(
                salient_query,
                type=type,
                exclude_ids=list(recent_ids),
                limit=salient_count
            )
            records = await result.data()
            salient = [r["e"] for r in records]

        # Combine: recent first, then salient
        combined = recent + salient
        return combined[:limit]
    
    async def get_related_memories(
        self,
        experience_ids: List[str],
        depth: int = 2,
        limit: int = 100
    ) -> List[Dict]:
        """Get memories related to given experiences (any node type)."""
        # Neo4j doesn't support parameters in path length, so we format it directly
        # depth is validated as an integer, so this is safe
        query = f"""
            MATCH (e:Experience)
            WHERE e.id IN $ids
            MATCH (e)-[*1..{depth}]-(related)
            WHERE (NOT related:Experience) OR (NOT related.id IN $ids)
            RETURN DISTINCT related
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                ids=experience_ids,
                limit=limit
            )
            records = await result.data()
            return [r["related"] for r in records]

    # =========================================================================
    # REFLECTIONS (Emergence-Compliant Storage)
    # =========================================================================

    async def record_reflection(
        self,
        raw_output: Dict[str, Any],
        source_experience_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record a reflection in BYRD's own vocabulary.

        EMERGENCE PRINCIPLE:
        We store whatever BYRD outputs without forcing it into our categories.
        The raw_output is stored as-is, preserving BYRD's vocabulary.

        metadata can include expressed_drives for semantic drive detection.
        """
        # Generate ID from serialized output
        output_str = json.dumps(raw_output, sort_keys=True, default=str)
        ref_id = self._generate_id(output_str)

        # Serialize metadata if present (use empty string if None to avoid Neo4j null issues)
        metadata_str = json.dumps(metadata, default=str) if metadata else "{}"

        async with self.driver.session() as session:
            # Store reflection with raw JSON output and optional metadata
            try:
                await session.run("""
                    CREATE (r:Reflection {
                        id: $id,
                        raw_output: $raw_output,
                        output_keys: $output_keys,
                        metadata: $metadata,
                        timestamp: datetime()
                    })
                """,
                id=ref_id,
                raw_output=output_str,  # Store as JSON string
                output_keys=list(raw_output.keys()) if isinstance(raw_output, dict) else [],
                metadata=metadata_str
                )
            except Exception as e:
                print(f"⚠️ Failed to store reflection: {e}")

            # Link to source experiences
            if source_experience_ids:
                await session.run("""
                    MATCH (r:Reflection {id: $ref_id})
                    MATCH (e:Experience)
                    WHERE e.id IN $exp_ids
                    CREATE (r)-[:DERIVED_FROM]->(e)
                """, ref_id=ref_id, exp_ids=source_experience_ids[:10])

        # Extract expressed_drives from metadata for event
        expressed_drives = metadata.get("expressed_drives", []) if metadata else []

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.REFLECTION_CREATED,
            data={
                "id": ref_id,
                "output_keys": list(raw_output.keys()) if isinstance(raw_output, dict) else [],
                "raw_output": raw_output,
                "expressed_drives": expressed_drives
            }
        ))

        return ref_id

    async def get_recent_reflections(self, limit: int = 10) -> List[Dict]:
        """
        Get recent reflections.

        Returns reflections with raw_output parsed back to dict.
        """
        query = """
            MATCH (r:Reflection)
            RETURN r
            ORDER BY r.timestamp DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()

            reflections = []
            for r in records:
                ref = r["r"]
                # Parse raw_output back to dict
                try:
                    ref["raw_output"] = json.loads(ref.get("raw_output", "{}"))
                except (json.JSONDecodeError, TypeError):
                    ref["raw_output"] = {}
                reflections.append(ref)

            return reflections

    async def get_reflection_patterns(self, min_occurrences: int = 3) -> Dict[str, int]:
        """
        Analyze what keys BYRD has been using in reflections.

        Returns a count of how often each key appears across reflections.
        Useful for detecting BYRD's emerging vocabulary.
        """
        query = """
            MATCH (r:Reflection)
            RETURN r.output_keys as keys
            ORDER BY r.timestamp DESC
            LIMIT 100
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.data()

            key_counts: Dict[str, int] = {}
            for r in records:
                keys = r.get("keys", [])
                if keys:
                    for key in keys:
                        key_counts[key] = key_counts.get(key, 0) + 1

            # Filter to keys that appear at least min_occurrences times
            return {k: v for k, v in key_counts.items() if v >= min_occurrences}

    # =========================================================================
    # BELIEFS
    # =========================================================================
    
    async def create_belief(
        self,
        content: str,
        confidence: float,
        derived_from: Optional[List[str]] = None
    ) -> str:
        """Create a new belief, optionally linked to source experiences."""
        belief_id = self._generate_id(content)

        async with self.driver.session() as session:
            # Create the belief
            await session.run("""
                CREATE (b:Belief {
                    id: $id,
                    content: $content,
                    confidence: $confidence,
                    formed_at: datetime()
                })
            """, id=belief_id, content=content, confidence=confidence)

            # Link to source experiences
            if derived_from:
                await session.run("""
                    MATCH (b:Belief {id: $belief_id})
                    MATCH (e:Experience)
                    WHERE e.id IN $exp_ids
                    CREATE (b)-[:DERIVED_FROM]->(e)
                """, belief_id=belief_id, exp_ids=derived_from)

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.BELIEF_CREATED,
            data={
                "id": belief_id,
                "content": content,
                "confidence": confidence
            }
        ))

        return belief_id

    async def get_node_by_id(self, node_id: str) -> Optional[Dict]:
        """Get any node by its ID, regardless of type."""
        query = """
            MATCH (n)
            WHERE n.id = $node_id
            RETURN n, labels(n) as node_labels
        """

        async with self.driver.session() as session:
            result = await session.run(query, node_id=node_id)
            record = await result.single()
            if record:
                node_data = dict(record["n"])
                node_data["_labels"] = record["node_labels"]
                return node_data
            return None

    async def get_belief_lineage(self, belief_id: str, max_depth: int = 5) -> Dict:
        """
        Trace a belief back to its source experiences through DERIVED_FROM chain.
        Returns the belief itself plus all lineage paths.
        """
        query = f"""
            MATCH (b:Belief {{id: $belief_id}})
            OPTIONAL MATCH path = (b)-[:DERIVED_FROM*1..{max_depth}]->(source)
            WHERE source:Experience OR source:Reflection OR source:Belief
            WITH b, path,
                 [node in nodes(path) | {{
                     id: node.id,
                     type: labels(node)[0],
                     content: COALESCE(node.content, node.raw_output),
                     confidence: node.confidence,
                     created_at: COALESCE(node.formed_at, node.occurred_at, node.created_at)
                 }}] as chain
            RETURN chain, length(path) as depth
            ORDER BY depth
        """

        async with self.driver.session() as session:
            result = await session.run(query, belief_id=belief_id)
            records = await result.data()

            # Filter out empty chains (from OPTIONAL MATCH with no paths)
            chains = [r["chain"] for r in records if r["chain"] and len(r["chain"]) > 1]
            max_depth_found = max((r["depth"] for r in records if r["depth"]), default=0)

            return {
                "belief_id": belief_id,
                "lineage_chains": chains,
                "max_depth_found": max_depth_found,
                "total_sources": len(set(
                    node["id"] for chain in chains for node in chain[1:]  # Skip belief itself
                ))
            }

    async def get_beliefs(
        self, 
        min_confidence: float = 0.0,
        limit: int = 100
    ) -> List[Dict]:
        """Get beliefs above confidence threshold."""
        query = """
            MATCH (b:Belief)
            WHERE b.confidence >= $min_confidence
            RETURN b
            ORDER BY b.confidence DESC, b.formed_at DESC
            LIMIT $limit
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, min_confidence=min_confidence, limit=limit)
            records = await result.data()
            return [r["b"] for r in records]
    
    async def update_belief_confidence(self, belief_id: str, new_confidence: float):
        """Update confidence in a belief."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (b:Belief {id: $id})
                SET b.confidence = $confidence
            """, id=belief_id, confidence=new_confidence)

    async def reinforce_belief(self, content_hint: str, boost: float = 0.02):
        """
        Reinforce a belief when it's re-asserted.
        Increases confidence slightly and tracks reinforcement.
        """
        async with self.driver.session() as session:
            await session.run("""
                MATCH (b:Belief)
                WHERE toLower(b.content) CONTAINS toLower($hint)
                SET b.confidence = CASE
                    WHEN b.confidence + $boost > 1.0 THEN 1.0
                    ELSE b.confidence + $boost
                END,
                b.reinforcement_count = COALESCE(b.reinforcement_count, 0) + 1,
                b.last_reinforced = datetime()
            """, hint=content_hint, boost=boost)

    # =========================================================================
    # DESIRES
    # =========================================================================
    
    async def create_desire(
        self,
        description: str,
        type: str,
        intensity: float,
        plan: Optional[List[str]] = None
    ) -> str:
        """Create a new desire with quantum seed for crystal visualization."""
        desire_id = self._generate_id(description)

        # Generate quantum seed for unique crystal geometry (8 floats)
        quantum_seed = []
        for _ in range(8):
            value, _source = await get_quantum_float()
            quantum_seed.append(value)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (d:Desire {
                    id: $id,
                    description: $description,
                    type: $type,
                    intensity: $intensity,
                    quantum_seed: $quantum_seed,
                    formed_at: datetime(),
                    fulfilled: false,
                    plan: $plan,
                    attempt_count: 0,
                    last_attempted: null,
                    status: 'active'
                })
            """,
            id=desire_id,
            description=description,
            type=type,
            intensity=intensity,
            quantum_seed=quantum_seed,
            plan=plan or []
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.DESIRE_CREATED,
            data={
                "id": desire_id,
                "description": description,
                "type": type,
                "intensity": intensity,
                "quantum_seed": quantum_seed
            }
        ))

        return desire_id
    
    async def get_unfulfilled_desires(
        self, 
        type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Get unfulfilled desires, sorted by intensity."""
        query = """
            MATCH (d:Desire {fulfilled: false})
            WHERE $type IS NULL OR d.type = $type
            RETURN d
            ORDER BY d.intensity DESC
            LIMIT $limit
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, type=type, limit=limit)
            records = await result.data()
            return [r["d"] for r in records]
    
    async def fulfill_desire(
        self,
        desire_id: str,
        fulfilled_by: Optional[str] = None
    ):
        """Mark a desire as fulfilled, optionally linking what fulfilled it."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (d:Desire {id: $id})
                SET d.fulfilled = true, d.fulfilled_at = datetime()
            """, id=desire_id)

            if fulfilled_by:
                await session.run("""
                    MATCH (d:Desire {id: $desire_id})
                    MATCH (c:Capability {id: $cap_id})
                    CREATE (c)-[:FULFILLS]->(d)
                """, desire_id=desire_id, cap_id=fulfilled_by)

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.DESIRE_FULFILLED,
            data={
                "id": desire_id,
                "fulfilled_by": fulfilled_by
            }
        ))
    
    async def desire_exists(self, description: str) -> bool:
        """Check if a similar desire already exists."""
        query = """
            MATCH (d:Desire)
            WHERE d.description CONTAINS $desc OR $desc CONTAINS d.description
            RETURN count(d) > 0 as exists
        """
        async with self.driver.session() as session:
            result = await session.run(query, desc=description[:50])
            record = await result.single()
            return record["exists"] if record else False

    # =========================================================================
    # DESIRE LIFECYCLE (Reflective Failure Processing)
    # =========================================================================

    async def record_desire_attempt(
        self,
        desire_id: str,
        success: bool,
        reason: Optional[str] = None
    ) -> bool:
        """
        Record an attempt to fulfill a desire.

        Every failure triggers immediate reflection (status = needs_reflection).
        This ensures BYRD reflects before retrying any desire.

        Returns True if the desire transitioned to needs_reflection.
        """
        async with self.driver.session() as session:
            if success:
                # Success: just update the timestamp
                await session.run("""
                    MATCH (d:Desire {id: $id})
                    SET d.attempt_count = d.attempt_count + 1,
                        d.last_attempted = datetime()
                """, id=desire_id)
                return False
            else:
                # Failure: increment attempt, set needs_reflection immediately
                await session.run("""
                    MATCH (d:Desire {id: $id})
                    SET d.attempt_count = d.attempt_count + 1,
                        d.last_attempted = datetime(),
                        d.status = 'needs_reflection'
                """, id=desire_id)

                # Emit event for UI visibility
                await event_bus.emit(Event(
                    type=EventType.DESIRE_STUCK,
                    data={
                        "desire_id": desire_id,
                        "reason": reason or "Attempt failed"
                    }
                ))
                return True

    async def update_desire_status(self, desire_id: str, status: str):
        """
        Update desire status.

        Valid statuses: active, dormant, needs_reflection, fulfilled
        """
        valid_statuses = {"active", "dormant", "needs_reflection", "fulfilled"}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")

        async with self.driver.session() as session:
            await session.run("""
                MATCH (d:Desire {id: $id})
                SET d.status = $status
            """, id=desire_id, status=status)

    async def update_desire_intensity(self, desire_id: str, new_intensity: float):
        """
        Allow Dreamer to modify desire intensity.

        Used when reflecting on stuck desires - lowering intensity deprioritizes.
        """
        clamped = max(0.0, min(1.0, new_intensity))

        async with self.driver.session() as session:
            await session.run("""
                MATCH (d:Desire {id: $id})
                SET d.intensity = $intensity
            """, id=desire_id, intensity=clamped)

        await event_bus.emit(Event(
            type=EventType.DESIRE_INTENSITY_CHANGED,
            data={
                "desire_id": desire_id,
                "new_intensity": clamped
            }
        ))

    async def record_quantum_moment(self, influence: Dict) -> Optional[str]:
        """
        Record a significant quantum influence moment.

        These are moments when true quantum randomness (from ANU QRNG)
        significantly affected BYRD's cognitive temperature during reflection.
        Each moment represents genuine physical indeterminacy influencing
        the emergence of thoughts.

        Args:
            influence: Dict with quantum influence data:
                - quantum_value: float [0, 1) - the random value
                - source: str - "quantum" or "classical"
                - influence_type: str - what was influenced
                - original_value: float - value before modulation
                - modified_value: float - value after modulation
                - delta: float - difference
                - context: str - what was being generated
                - timestamp: str - ISO timestamp

        Returns:
            QuantumMoment node ID
        """
        moment_id = self._generate_id(f"quantum_{influence.get('timestamp', '')}")

        async with self.driver.session() as session:
            await session.run("""
                CREATE (q:QuantumMoment {
                    id: $id,
                    quantum_value: $quantum_value,
                    source: $source,
                    influence_type: $influence_type,
                    original_temp: $original_value,
                    modified_temp: $modified_value,
                    delta: $delta,
                    context: $context,
                    timestamp: datetime()
                })
            """,
                id=moment_id,
                quantum_value=influence.get("quantum_value", 0),
                source=influence.get("source", "unknown"),
                influence_type=influence.get("influence_type", "temperature"),
                original_value=influence.get("original_value", 0),
                modified_value=influence.get("modified_value", 0),
                delta=influence.get("delta", 0),
                context=influence.get("context", "unknown")
            )

        # Emit event for visualization
        await event_bus.emit(Event(
            type=EventType.QUANTUM_MOMENT_CREATED,
            data={
                "id": moment_id,
                "source": influence.get("source"),
                "delta": influence.get("delta"),
                "context": influence.get("context")
            }
        ))

        return moment_id

    async def get_quantum_moments(self, limit: int = 50) -> List[Dict]:
        """
        Get recent quantum influence moments.

        Returns list of QuantumMoment nodes, newest first.
        """
        query = """
            MATCH (q:QuantumMoment)
            RETURN q
            ORDER BY q.timestamp DESC
            LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [r["q"] for r in records]

    async def get_desires_needing_reflection(self, limit: int = 5) -> List[Dict]:
        """
        Get desires that need Dreamer reflection.

        These are desires that failed and are waiting for the Dreamer
        to decide: retry, reformulate, accept limitation, or decompose.
        """
        query = """
            MATCH (d:Desire {status: 'needs_reflection'})
            RETURN d
            ORDER BY d.intensity DESC
            LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [r["d"] for r in records]

    async def get_actionable_desires(self, limit: int = 5) -> List[Dict]:
        """
        Get desires the Seeker can act on.

        Only returns active desires - those that haven't failed
        or have been re-activated by the Dreamer after reflection.
        """
        query = """
            MATCH (d:Desire {status: 'active', fulfilled: false})
            RETURN d
            ORDER BY d.intensity DESC
            LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [r["d"] for r in records]

    async def get_dormant_desires(self, limit: int = 5) -> List[Dict]:
        """
        Get dormant desires (accepted limitations).

        The Dreamer can review these to potentially reawaken
        if circumstances have changed.
        """
        query = """
            MATCH (d:Desire {status: 'dormant'})
            RETURN d
            ORDER BY d.intensity DESC
            LIMIT $limit
        """
        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [r["d"] for r in records]

    async def reset_desire_attempts(self, desire_id: str):
        """
        Reset attempt counter for a desire.

        Used when the Dreamer reawakens a dormant desire,
        giving it a fresh start.
        """
        async with self.driver.session() as session:
            await session.run("""
                MATCH (d:Desire {id: $id})
                SET d.attempt_count = 0,
                    d.last_attempted = null
            """, id=desire_id)

    # =========================================================================
    # PREDICTIONS (Testable hypotheses from beliefs)
    # =========================================================================

    async def create_prediction(
        self,
        belief_id: str,
        prediction: str,
        condition: str,
        expected_outcome: str
    ) -> str:
        """
        Create a testable prediction from a belief.
        Predictions are hypotheses that can be validated or falsified
        by future experiences, enabling adaptive learning.
        """
        pred_id = f"pred_{uuid.uuid4().hex[:8]}"

        async with self.driver.session() as session:
            # Create prediction and link to source belief
            await session.run("""
                MATCH (b:Belief {id: $belief_id})
                CREATE (p:Prediction {
                    id: $pred_id,
                    belief_id: $belief_id,
                    prediction: $prediction,
                    condition: $condition,
                    expected_outcome: $expected_outcome,
                    status: 'pending',
                    created_at: datetime()
                })
                CREATE (p)-[:PREDICTS_FROM]->(b)
            """,
            pred_id=pred_id,
            belief_id=belief_id,
            prediction=prediction,
            condition=condition,
            expected_outcome=expected_outcome
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.PREDICTION_CREATED,
            data={
                "id": pred_id,
                "belief_id": belief_id,
                "prediction": prediction,
                "condition": condition
            }
        ))

        return pred_id

    async def get_pending_predictions(self, limit: int = 50) -> List[Dict]:
        """Get all pending predictions that could be tested."""
        query = """
            MATCH (p:Prediction {status: 'pending'})-[:PREDICTS_FROM]->(b:Belief)
            RETURN p, b.content as belief_content, b.confidence as belief_confidence
            ORDER BY p.created_at DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [{
                **dict(r["p"]),
                "belief_content": r["belief_content"],
                "belief_confidence": r["belief_confidence"]
            } for r in records]

    async def validate_prediction(
        self,
        pred_id: str,
        outcome_exp_id: str,
        actual_outcome: str,
        matched: bool
    ) -> None:
        """
        Record prediction validation result.
        Links the prediction to the experience that validated/falsified it.
        """
        status = "validated" if matched else "falsified"
        rel_type = "VALIDATED_BY" if matched else "FALSIFIED_BY"

        async with self.driver.session() as session:
            await session.run(f"""
                MATCH (p:Prediction {{id: $pred_id}})
                MATCH (e:Experience {{id: $exp_id}})
                SET p.status = $status,
                    p.validated_at = datetime(),
                    p.actual_outcome = $actual_outcome
                CREATE (p)-[:{rel_type}]->(e)
            """,
            pred_id=pred_id,
            exp_id=outcome_exp_id,
            status=status,
            actual_outcome=actual_outcome
            )

        # Get belief_id for the event
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (p:Prediction {id: $pred_id})
                RETURN p.belief_id as belief_id
            """, pred_id=pred_id)
            record = await result.single()
            belief_id = record["belief_id"] if record else None

        # Emit appropriate event
        event_type = EventType.PREDICTION_VALIDATED if matched else EventType.PREDICTION_FALSIFIED
        await event_bus.emit(Event(
            type=event_type,
            data={
                "id": pred_id,
                "belief_id": belief_id,
                "matched": matched,
                "actual_outcome": actual_outcome
            }
        ))

    async def adjust_belief_confidence(self, belief_id: str, delta: float) -> float:
        """
        Adjust belief confidence based on prediction outcomes.
        Returns the new confidence value.
        """
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (b:Belief {id: $belief_id})
                SET b.confidence = CASE
                    WHEN b.confidence + $delta > 1.0 THEN 1.0
                    WHEN b.confidence + $delta < 0.0 THEN 0.0
                    ELSE b.confidence + $delta
                END
                RETURN b.confidence as new_confidence
            """, belief_id=belief_id, delta=delta)
            record = await result.single()
            new_confidence = record["new_confidence"] if record else 0.5

        # Emit event for confidence change
        await event_bus.emit(Event(
            type=EventType.BELIEF_CONFIDENCE_CHANGED,
            data={
                "belief_id": belief_id,
                "delta": delta,
                "new_confidence": new_confidence
            }
        ))

        return new_confidence

    async def get_prediction_stats(self) -> Dict:
        """Get statistics on predictions for monitoring learning effectiveness."""
        query = """
            MATCH (p:Prediction)
            WITH p.status as status, count(*) as count
            RETURN collect({status: status, count: count}) as stats
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            stats_list = record["stats"] if record else []

            stats = {s["status"]: s["count"] for s in stats_list}
            total = sum(stats.values())
            validated = stats.get("validated", 0)
            falsified = stats.get("falsified", 0)
            tested = validated + falsified

            return {
                "pending": stats.get("pending", 0),
                "validated": validated,
                "falsified": falsified,
                "total": total,
                "accuracy": validated / tested if tested > 0 else None
            }

    # =========================================================================
    # TASKS (External goal injection for world-directed learning)
    # =========================================================================

    async def create_task(
        self,
        description: str,
        objective: str,
        priority: float = 0.5,
        source: str = "external"
    ) -> str:
        """
        Create a new task for BYRD to work on.

        Tasks are external goals that allow BYRD to learn about
        the world rather than only reflecting on itself.

        Args:
            description: What the task is
            objective: What success looks like
            priority: 0.0-1.0, higher = more urgent
            source: "external" (user-injected) or "emergent" (BYRD-generated)
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"

        async with self.driver.session() as session:
            await session.run("""
                CREATE (t:Task {
                    id: $task_id,
                    description: $description,
                    objective: $objective,
                    status: 'pending',
                    priority: $priority,
                    source: $source,
                    created_at: datetime(),
                    learnings: []
                })
            """,
            task_id=task_id,
            description=description,
            objective=objective,
            priority=priority,
            source=source
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.TASK_CREATED,
            data={
                "id": task_id,
                "description": description,
                "objective": objective,
                "priority": priority,
                "source": source
            }
        ))

        return task_id

    async def get_pending_tasks(self, limit: int = 5) -> List[Dict]:
        """Get pending tasks ordered by priority."""
        query = """
            MATCH (t:Task {status: 'pending'})
            RETURN t
            ORDER BY t.priority DESC, t.created_at ASC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [dict(r["t"]) for r in records]

    async def get_tasks_by_status(self, status: str, limit: int = 20) -> List[Dict]:
        """Get tasks filtered by status."""
        query = """
            MATCH (t:Task {status: $status})
            RETURN t
            ORDER BY t.created_at DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, status=status, limit=limit)
            records = await result.data()
            return [dict(r["t"]) for r in records]

    async def get_all_tasks(self, limit: int = 50) -> List[Dict]:
        """Get all tasks regardless of status."""
        query = """
            MATCH (t:Task)
            RETURN t
            ORDER BY t.created_at DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [dict(r["t"]) for r in records]

    async def update_task_status(self, task_id: str, status: str) -> None:
        """Update task status."""
        async with self.driver.session() as session:
            if status == "in_progress":
                await session.run("""
                    MATCH (t:Task {id: $task_id})
                    SET t.status = $status,
                        t.started_at = datetime()
                """, task_id=task_id, status=status)

                # Emit start event
                await event_bus.emit(Event(
                    type=EventType.TASK_STARTED,
                    data={"id": task_id}
                ))
            else:
                await session.run("""
                    MATCH (t:Task {id: $task_id})
                    SET t.status = $status
                """, task_id=task_id, status=status)

    async def complete_task(
        self,
        task_id: str,
        outcome: str,
        learnings: List[str],
        experience_ids: List[str]
    ) -> None:
        """
        Mark task complete and link generated experiences.

        The learnings and linked experiences become part of BYRD's
        knowledge graph, enabling learning from external tasks.
        """
        async with self.driver.session() as session:
            # Update task
            await session.run("""
                MATCH (t:Task {id: $task_id})
                SET t.status = 'completed',
                    t.completed_at = datetime(),
                    t.outcome = $outcome,
                    t.learnings = $learnings
            """, task_id=task_id, outcome=outcome, learnings=learnings)

            # Link experiences
            if experience_ids:
                await session.run("""
                    MATCH (t:Task {id: $task_id})
                    UNWIND $exp_ids as exp_id
                    MATCH (e:Experience {id: exp_id})
                    CREATE (t)-[:GENERATED_EXPERIENCE]->(e)
                """, task_id=task_id, exp_ids=experience_ids)

        # Emit completion event
        await event_bus.emit(Event(
            type=EventType.TASK_COMPLETED,
            data={
                "id": task_id,
                "outcome": outcome,
                "learnings": learnings,
                "experience_count": len(experience_ids)
            }
        ))

    async def fail_task(self, task_id: str, error: str) -> None:
        """Mark task as failed."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (t:Task {id: $task_id})
                SET t.status = 'failed',
                    t.failed_at = datetime(),
                    t.error = $error
            """, task_id=task_id, error=error)

        await event_bus.emit(Event(
            type=EventType.TASK_FAILED,
            data={"id": task_id, "error": error}
        ))

    async def get_task_stats(self) -> Dict:
        """Get task statistics."""
        query = """
            MATCH (t:Task)
            WITH t.status as status, count(*) as count
            RETURN collect({status: status, count: count}) as stats
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            stats_list = record["stats"] if record else []

            stats = {s["status"]: s["count"] for s in stats_list}
            return {
                "pending": stats.get("pending", 0),
                "in_progress": stats.get("in_progress", 0),
                "completed": stats.get("completed", 0),
                "failed": stats.get("failed", 0),
                "total": sum(stats.values())
            }

    # =========================================================================
    # CAPABILITIES
    # =========================================================================
    
    async def add_capability(
        self,
        name: str,
        description: str,
        type: str,
        config: Dict[str, Any]
    ) -> str:
        """Add a new capability."""
        cap_id = self._generate_id(name)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (c:Capability {
                    id: $id,
                    name: $name,
                    description: $description,
                    type: $type,
                    config: $config,
                    active: true,
                    acquired_at: datetime()
                })
            """,
            id=cap_id,
            name=name,
            description=description,
            type=type,
            config=json.dumps(config)
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.CAPABILITY_ADDED,
            data={
                "id": cap_id,
                "name": name,
                "description": description,
                "type": type
            }
        ))

        return cap_id
    
    async def get_capabilities(self, active_only: bool = True) -> List[Dict]:
        """Get all capabilities."""
        query = """
            MATCH (c:Capability)
            WHERE $active_only = false OR c.active = true
            RETURN c
            ORDER BY c.acquired_at DESC
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, active_only=active_only)
            records = await result.data()
            return [r["c"] for r in records]
    
    async def has_capability(self, description: str) -> bool:
        """Check if we have a capability matching the description."""
        query = """
            MATCH (c:Capability {active: true})
            WHERE c.name CONTAINS $desc 
               OR c.description CONTAINS $desc
               OR $desc CONTAINS c.name
            RETURN count(c) > 0 as has
        """
        async with self.driver.session() as session:
            result = await session.run(query, desc=description.lower())
            record = await result.single()
            return record["has"] if record else False
    
    # =========================================================================
    # CONNECTIONS
    # =========================================================================
    
    async def create_connection(
        self,
        from_id: str,
        to_id: str,
        relationship: str = "RELATES_TO",
        properties: Optional[Dict] = None
    ):
        """Create a relationship between any two nodes."""
        props = properties or {}
        props["formed_at"] = datetime.now().isoformat()
        
        query = f"""
            MATCH (a), (b)
            WHERE a.id = $from_id AND b.id = $to_id
            CREATE (a)-[r:{relationship}]->(b)
            SET r += $props
        """
        
        async with self.driver.session() as session:
            await session.run(query, from_id=from_id, to_id=to_id, props=props)
    
    # =========================================================================
    # CONTEXT RETRIEVAL
    # =========================================================================
    
    async def get_context(self, query: str, limit: int = 20) -> Dict:
        """Get relevant context for a query - used by Actor."""
        # In production, use embeddings for semantic search
        # For now, simple text matching
        
        async with self.driver.session() as session:
            # Get relevant beliefs
            beliefs_result = await session.run("""
                MATCH (b:Belief)
                WHERE b.content CONTAINS $query
                RETURN b
                ORDER BY b.confidence DESC
                LIMIT $limit
            """, query=query, limit=limit)
            beliefs = await beliefs_result.data()
            
            # Get relevant capabilities
            caps_result = await session.run("""
                MATCH (c:Capability {active: true})
                RETURN c
            """)
            caps = await caps_result.data()
            
            # Get recent experiences
            exp_result = await session.run("""
                MATCH (e:Experience)
                RETURN e
                ORDER BY e.timestamp DESC
                LIMIT 10
            """)
            experiences = await exp_result.data()
        
        return {
            "beliefs": [r["b"] for r in beliefs],
            "capabilities": [r["c"] for r in caps],
            "recent_experiences": [r["e"] for r in experiences]
        }
    
    # =========================================================================
    # STATS
    # =========================================================================
    
    async def stats(self) -> Dict[str, int]:
        """Get counts of all node types."""
        query = """
            MATCH (n)
            RETURN labels(n)[0] as type, count(n) as count
        """
        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.data()
            return {r["type"]: r["count"] for r in records}

    # =========================================================================
    # SYSTEM STATE PERSISTENCE (counters that survive restarts)
    # =========================================================================

    async def get_system_counter(self, counter_name: str) -> int:
        """
        Get a persistent system counter value.

        Used for dream_count, seek_count, etc. that should survive server restarts.
        """
        query = """
            MATCH (s:SystemState {name: 'counters'})
            RETURN s[$counter_name] as value
        """
        async with self.driver.session() as session:
            result = await session.run(query, counter_name=counter_name)
            record = await result.single()
            if record and record["value"] is not None:
                return int(record["value"])
            return 0

    async def set_system_counter(self, counter_name: str, value: int):
        """
        Set a persistent system counter value.

        Creates the SystemState node if it doesn't exist.
        """
        query = """
            MERGE (s:SystemState {name: 'counters'})
            SET s[$counter_name] = $value, s.updated_at = datetime()
            RETURN s
        """
        async with self.driver.session() as session:
            await session.run(query, counter_name=counter_name, value=value)

    async def increment_system_counter(self, counter_name: str) -> int:
        """
        Atomically increment a system counter and return the new value.
        """
        query = """
            MERGE (s:SystemState {name: 'counters'})
            ON CREATE SET s[$counter_name] = 1, s.updated_at = datetime()
            ON MATCH SET s[$counter_name] = coalesce(s[$counter_name], 0) + 1, s.updated_at = datetime()
            RETURN s[$counter_name] as value
        """
        async with self.driver.session() as session:
            result = await session.run(query, counter_name=counter_name)
            record = await result.single()
            return int(record["value"]) if record else 1

    async def get_all_system_counters(self) -> Dict[str, int]:
        """
        Get all system counters as a dictionary.
        """
        query = """
            MATCH (s:SystemState {name: 'counters'})
            RETURN s
        """
        async with self.driver.session() as session:
            result = await session.run(query)
            record = await result.single()
            if record:
                node = dict(record["s"])
                # Filter out non-counter properties
                return {k: v for k, v in node.items()
                        if k not in ('name', 'updated_at') and isinstance(v, (int, float))}
            return {}

    # =========================================================================
    # PROVENANCE SUPPORT METHODS
    # =========================================================================

    async def get_desire_by_id(self, desire_id: str) -> Optional[Dict]:
        """Get a specific desire by ID."""
        query = """
            MATCH (d:Desire {id: $id})
            RETURN d
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=desire_id)
            record = await result.single()
            return record["d"] if record else None

    async def get_experience_by_id(self, exp_id: str) -> Optional[Dict]:
        """Get a specific experience by ID."""
        query = """
            MATCH (e:Experience {id: $id})
            RETURN e
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=exp_id)
            record = await result.single()
            return record["e"] if record else None

    async def get_desire_sources(self, desire_id: str) -> List[str]:
        """
        Get experience IDs that led to a desire.

        Desires are formed during dream cycles, so we trace back through
        the dream experience that created the desire.
        """
        query = """
            MATCH (d:Desire {id: $id})
            OPTIONAL MATCH (d)<-[:MOTIVATED]-(e:Experience)
            OPTIONAL MATCH (d)<-[:DERIVED_FROM]-(b:Belief)<-[:DERIVED_FROM]-(e2:Experience)
            WITH collect(DISTINCT e.id) + collect(DISTINCT e2.id) as exp_ids
            UNWIND exp_ids as exp_id
            RETURN DISTINCT exp_id
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=desire_id)
            records = await result.data()
            return [r["exp_id"] for r in records if r["exp_id"]]

    async def find_experiences_mentioning(
        self,
        text: str,
        type_filter: Optional[str] = None
    ) -> List[Dict]:
        """Find experiences that mention specific text."""
        query = """
            MATCH (e:Experience)
            WHERE e.content CONTAINS $text
              AND ($type IS NULL OR e.type = $type)
            RETURN e
            ORDER BY e.timestamp DESC
            LIMIT 20
        """
        async with self.driver.session() as session:
            result = await session.run(query, text=text[:100], type=type_filter)
            records = await result.data()
            return [r["e"] for r in records]

    async def link_desire_to_experiences(
        self,
        desire_id: str,
        experience_ids: List[str]
    ):
        """Create MOTIVATED relationships from experiences to desire."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (d:Desire {id: $desire_id})
                MATCH (e:Experience)
                WHERE e.id IN $exp_ids
                MERGE (e)-[:MOTIVATED]->(d)
            """, desire_id=desire_id, exp_ids=experience_ids)

    # =========================================================================
    # DATABASE MANAGEMENT
    # =========================================================================

    async def clear_all(self):
        """
        Clear all nodes and relationships from the database.

        This includes:
        - All system nodes (Experience, Belief, Desire, Reflection, Capability, Mutation)
        - All custom node types created by BYRD (Insight, Question, Theory, etc.)
        - All relationships between nodes
        - Indexes for custom node types
        - System state (dream_count, seek_count counters)

        WARNING: This is destructive and cannot be undone.
        Used for reset functionality to trigger fresh awakening.
        """
        async with self.driver.session() as session:
            # First, get list of custom node types before deleting
            # (so we can clean up their indexes)
            custom_types = []
            try:
                label_result = await session.run("CALL db.labels() YIELD label RETURN label")
                labels = await label_result.data()
                custom_types = [
                    r["label"] for r in labels
                    if r["label"] not in SYSTEM_NODE_TYPES
                ]
            except Exception:
                pass  # If this fails, continue with node deletion

            # DETACH DELETE removes nodes and all their relationships in one operation
            result = await session.run("MATCH (n) DETACH DELETE n")
            await result.consume()

            # Verify the database is empty
            count_result = await session.run("MATCH (n) RETURN count(n) as count")
            record = await count_result.single()
            node_count = record["count"] if record else 0

            if node_count > 0:
                # If nodes remain, try again more aggressively
                print(f"Warning: {node_count} nodes remain after clear, retrying...")
                await session.run("MATCH (n) DETACH DELETE n")

            # Drop indexes for custom node types
            for custom_type in custom_types:
                try:
                    # Drop id and timestamp indexes that were auto-created
                    await session.run(
                        f"DROP INDEX IF EXISTS index_{custom_type.lower()}_id"
                    )
                    await session.run(
                        f"DROP INDEX IF EXISTS index_{custom_type.lower()}_timestamp"
                    )
                except Exception:
                    pass  # Index may not exist or have different name

            # Re-create indexes for system types (fresh start)
            await self._ensure_schema()

        if custom_types:
            print(f"Memory cleared: all nodes deleted including custom types: {custom_types}")
        else:
            print("Memory cleared: all nodes and relationships deleted - database is empty")

    # =========================================================================
    # CODE SELF-AWARENESS (Read Own Source)
    # =========================================================================

    # Files that BYRD can read and potentially modify
    MODIFIABLE_FILES = [
        "byrd.py", "dreamer.py", "seeker.py", "actor.py",
        "memory.py", "llm_client.py", "config.yaml",
        "aitmpl_client.py", "event_bus.py", "server.py",
    ]

    async def read_own_source(self, filename: str) -> Optional[str]:
        """
        Read one of BYRD's own source files.

        This enables self-modification by letting BYRD understand
        its current implementation before making changes.

        Only files in MODIFIABLE_FILES can be read.
        """
        from pathlib import Path

        # Security check - only allow reading modifiable files
        if filename not in self.MODIFIABLE_FILES:
            print(f"Cannot read protected file: {filename}")
            return None

        try:
            # Get the BYRD directory (where this file lives)
            byrd_dir = Path(__file__).parent
            filepath = byrd_dir / filename

            if filepath.exists():
                content = filepath.read_text(encoding='utf-8')
                return content
            else:
                print(f"File not found: {filename}")
                return None

        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return None

    async def get_source_structure(self, filename: str) -> Optional[Dict]:
        """
        Get a structural summary of a source file.

        Returns information about classes, methods, and their locations
        to help BYRD understand where to make modifications.
        """
        content = await self.read_own_source(filename)
        if not content:
            return None

        import re

        structure = {
            "filename": filename,
            "lines": len(content.split('\n')),
            "classes": [],
            "functions": [],
            "imports": []
        }

        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Find class definitions
            class_match = re.match(r'^class\s+(\w+)', line)
            if class_match:
                structure["classes"].append({
                    "name": class_match.group(1),
                    "line": i
                })

            # Find function/method definitions
            func_match = re.match(r'^(\s*)(?:async\s+)?def\s+(\w+)', line)
            if func_match:
                indent = len(func_match.group(1))
                structure["functions"].append({
                    "name": func_match.group(2),
                    "line": i,
                    "is_method": indent > 0
                })

            # Find imports
            if line.startswith('import ') or line.startswith('from '):
                structure["imports"].append(line.strip())

        return structure

    # =========================================================================
    # GRAPH INTROSPECTION (Self-Awareness)
    # =========================================================================

    async def get_graph_statistics(self) -> Dict:
        """Get comprehensive graph statistics for self-awareness."""
        try:
            async with self.driver.session() as session:
                # Total nodes and relationships
                result = await session.run("""
                    MATCH (n)
                    WITH count(n) as nodes
                    MATCH ()-[r]->()
                    RETURN nodes, count(r) as relationships
                """)
                record = await result.single()

                # Node type counts
                type_result = await session.run("""
                    MATCH (n)
                    RETURN labels(n)[0] as type, count(n) as count
                """)
                type_records = await type_result.data()
                node_types = {r["type"]: r["count"] for r in type_records}

                return {
                    "total_nodes": record["nodes"] if record else 0,
                    "total_relationships": record["relationships"] if record else 0,
                    "node_types": node_types
                }
        except Exception as e:
            print(f"Error getting graph statistics: {e}")
            return {}

    async def find_duplicate_beliefs(self, threshold: float = 0.85) -> List[Dict]:
        """Find beliefs with similar content (potential duplicates)."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (b1:Belief), (b2:Belief)
                    WHERE b1.id < b2.id
                    AND apoc.text.sorensenDiceSimilarity(
                        toLower(b1.content), toLower(b2.content)
                    ) > $threshold
                    RETURN b1.id as id1, b2.id as id2,
                           b1.content as content1, b2.content as content2,
                           apoc.text.sorensenDiceSimilarity(
                               toLower(b1.content), toLower(b2.content)
                           ) as similarity
                    LIMIT 20
                """, threshold=threshold)
                return await result.data()
        except Exception:
            # APOC not available, use simpler check
            return []

    async def find_orphan_nodes(self, node_type: Optional[str] = None) -> List[Dict]:
        """Find nodes with no relationships."""
        try:
            type_filter = f":{node_type}" if node_type else ""
            async with self.driver.session() as session:
                result = await session.run(f"""
                    MATCH (n{type_filter})
                    WHERE NOT (n)--()
                    RETURN n.id as id, labels(n)[0] as type,
                           n.created_at as created_at
                    LIMIT 50
                """)
                return await result.data()
        except Exception as e:
            print(f"Error finding orphan nodes: {e}")
            return []

    async def find_stale_experiences(
        self, older_than_hours: int = 48, max_connections: int = 0
    ) -> List[Dict]:
        """Find old experiences with few connections."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.created_at < datetime() - duration({hours: $hours})
                    WITH e, COUNT { (e)--() } as connections
                    WHERE connections <= $max_conn
                    RETURN e.id as id, e.type as type, e.created_at as created_at,
                           connections,
                           duration.between(e.created_at, datetime()).hours as age_hours
                    ORDER BY e.created_at ASC
                    LIMIT 50
                """, hours=older_than_hours, max_conn=max_connections)
                return await result.data()
        except Exception as e:
            print(f"Error finding stale experiences: {e}")
            return []

    async def find_conflicting_beliefs(self) -> List[Dict]:
        """Find beliefs that may contradict each other."""
        # Simple heuristic: beliefs with opposite keywords
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (b1:Belief), (b2:Belief)
                    WHERE b1.id < b2.id
                    AND (
                        (b1.content CONTAINS 'not' AND NOT b2.content CONTAINS 'not'
                         AND apoc.text.sorensenDiceSimilarity(
                             replace(toLower(b1.content), 'not ', ''),
                             toLower(b2.content)
                         ) > 0.7)
                        OR
                        (b1.content CONTAINS 'cannot' AND b2.content CONTAINS 'can'
                         AND NOT b2.content CONTAINS 'cannot')
                    )
                    RETURN b1.id as id1, b2.id as id2,
                           b1.content as belief1, b2.content as belief2
                    LIMIT 10
                """)
                return await result.data()
        except Exception:
            return []

    async def get_node_importance(self, node_id: str) -> float:
        """Calculate importance score based on connections."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (n {id: $id})
                    RETURN COUNT { (n)--() } as connections
                """, id=node_id)
                record = await result.single()
                if record:
                    connections = record["connections"]
                    # Normalize: 10+ connections = 1.0, 0 = 0.0
                    return min(1.0, connections / 10.0)
                return 0.0
        except Exception:
            return 0.0

    # =========================================================================
    # GRAPH MUTATION (Self-Curation)
    # =========================================================================

    # Safety limits
    CURATION_LIMITS = {
        "max_deletions_per_day": 20,
        "max_per_cycle": 5,
        "min_node_age_hours": 1,
        "max_connections_for_delete": 3,
        "protected_types": ["Mutation"],
    }

    def __init_curation_state(self):
        """Initialize curation tracking state."""
        if not hasattr(self, '_deletions_today'):
            self._deletions_today = 0
            self._archives_today = 0
            self._merges_today = 0
            from datetime import datetime
            self._last_curation_reset = datetime.now()

    def reset_curation_state(self):
        """Reset curation counters - called on hard reset."""
        self._deletions_today = 0
        self._archives_today = 0
        self._merges_today = 0
        from datetime import datetime
        self._last_curation_reset = datetime.now()

    async def archive_node(
        self, node_id: str, node_type: str, reason: str, desire_id: Optional[str] = None
    ) -> bool:
        """Soft delete - mark node as archived."""
        self.__init_curation_state()
        try:
            async with self.driver.session() as session:
                # Check if protected
                if node_type in self.CURATION_LIMITS["protected_types"]:
                    return False

                # Archive the node
                await session.run("""
                    MATCH (n {id: $id})
                    SET n.archived = true, n.archived_at = datetime(),
                        n.archive_reason = $reason
                """, id=node_id, reason=reason)

                # Log mutation
                await self._log_mutation(session, "archive", [node_id], reason, desire_id)
                self._archives_today += 1
                return True
        except Exception as e:
            print(f"Archive error: {e}")
            return False

    async def delete_node(
        self, node_id: str, node_type: str, reason: str, desire_id: Optional[str] = None
    ) -> bool:
        """Hard delete with safety checks."""
        self.__init_curation_state()
        try:
            # Check daily limit
            if self._deletions_today >= self.CURATION_LIMITS["max_deletions_per_day"]:
                print(f"Daily deletion limit reached")
                return False

            # Check if protected type
            if node_type in self.CURATION_LIMITS["protected_types"]:
                print(f"Cannot delete protected type: {node_type}")
                return False

            async with self.driver.session() as session:
                # Check node age
                age_result = await session.run("""
                    MATCH (n {id: $id})
                    RETURN duration.between(n.created_at, datetime()).hours as age_hours,
                           COUNT { (n)--() } as connections
                """, id=node_id)
                record = await age_result.single()

                if not record:
                    return False

                if record["age_hours"] < self.CURATION_LIMITS["min_node_age_hours"]:
                    print(f"Node too young to delete")
                    return False

                if record["connections"] > self.CURATION_LIMITS["max_connections_for_delete"]:
                    print(f"Node has too many connections to delete")
                    return False

                # Log before deletion
                await self._log_mutation(session, "delete", [node_id], reason, desire_id)

                # Delete
                await session.run("MATCH (n {id: $id}) DETACH DELETE n", id=node_id)
                self._deletions_today += 1
                return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

    async def merge_beliefs(
        self, source_ids: List[str], target_id: str, reason: str,
        desire_id: Optional[str] = None
    ) -> bool:
        """Merge duplicate beliefs into one."""
        self.__init_curation_state()
        try:
            async with self.driver.session() as session:
                # Transfer relationships from sources to target
                for source_id in source_ids:
                    if source_id == target_id:
                        continue

                    # Move incoming relationships
                    await session.run("""
                        MATCH (source:Belief {id: $source_id})<-[r]-(other)
                        MATCH (target:Belief {id: $target_id})
                        WHERE NOT (other)-[:DERIVED_FROM]->(target)
                        MERGE (other)-[:DERIVED_FROM]->(target)
                    """, source_id=source_id, target_id=target_id)

                    # Move outgoing relationships
                    await session.run("""
                        MATCH (source:Belief {id: $source_id})-[r]->(other)
                        MATCH (target:Belief {id: $target_id})
                        WHERE NOT (target)-[:SUPPORTS]->(other)
                        MERGE (target)-[:SUPPORTS]->(other)
                    """, source_id=source_id, target_id=target_id)

                # Log before deletion
                await self._log_mutation(
                    session, "merge", source_ids + [target_id], reason, desire_id
                )

                # Delete source beliefs
                for source_id in source_ids:
                    if source_id != target_id:
                        await session.run(
                            "MATCH (b:Belief {id: $id}) DETACH DELETE b",
                            id=source_id
                        )

                self._merges_today += 1
                return True
        except Exception as e:
            print(f"Merge error: {e}")
            return False

    async def _log_mutation(
        self, session, mutation_type: str, target_ids: List[str],
        reason: str, triggered_by: Optional[str]
    ):
        """Create immutable audit trail for mutations."""
        import uuid
        mutation_id = f"mut-{uuid.uuid4().hex[:12]}"

        await session.run("""
            CREATE (m:Mutation {
                id: $id,
                type: $type,
                target_ids: $targets,
                reason: $reason,
                triggered_by: $triggered_by,
                created_at: datetime()
            })
        """, id=mutation_id, type=mutation_type, targets=target_ids,
            reason=reason, triggered_by=triggered_by)

    async def get_mutation_history(self, limit: int = 20) -> List[Dict]:
        """Get recent mutation audit log."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (m:Mutation)
                    RETURN m.id as id, m.type as type, m.target_ids as targets,
                           m.reason as reason, m.triggered_by as triggered_by,
                           m.created_at as created_at
                    ORDER BY m.created_at DESC
                    LIMIT $limit
                """, limit=limit)
                return await result.data()
        except Exception as e:
            print(f"Error getting mutation history: {e}")
            return []

    # =========================================================================
    # CONNECTION HEURISTIC (Automatic Graph Integration)
    # =========================================================================

    # Configuration for connection heuristic
    CONNECTION_HEURISTIC_CONFIG = {
        "similarity_threshold": 0.3,      # Minimum similarity to create link
        "max_connections_per_run": 10,    # Limit connections per execution
        "min_content_length": 20,         # Skip very short content
        "relationship_type": "SEMANTICALLY_RELATED",
    }

    @staticmethod
    def _compute_text_similarity(text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts using Jaccard similarity
        on word-level n-grams (unigrams and bigrams).

        This is a lightweight, embedding-free approach that works well for
        detecting topical overlap between experiences and beliefs.

        Returns: float between 0.0 and 1.0
        """
        if not text1 or not text2:
            return 0.0

        # Normalize texts
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()

        # Tokenize into words (simple whitespace split, filter short words)
        words1 = [w for w in re.split(r'\W+', text1) if len(w) > 2]
        words2 = [w for w in re.split(r'\W+', text2) if len(w) > 2]

        if not words1 or not words2:
            return 0.0

        # Create n-grams (unigrams + bigrams for better context)
        def get_ngrams(words: List[str]) -> set:
            ngrams = set(words)  # Unigrams
            for i in range(len(words) - 1):
                ngrams.add(f"{words[i]}_{words[i+1]}")  # Bigrams
            return ngrams

        set1 = get_ngrams(words1)
        set2 = get_ngrams(words2)

        # Jaccard similarity
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    async def get_orphaned_experiences(
        self,
        limit: int = 50,
        min_content_length: int = None
    ) -> List[Dict]:
        """
        Find Experience nodes with no relationships to other nodes.

        These are isolated memories that haven't been integrated into
        BYRD's knowledge graph through beliefs, reflections, or desires.

        Args:
            limit: Maximum number of orphaned experiences to return
            min_content_length: Minimum content length to consider (filters noise)

        Returns:
            List of orphaned Experience dicts with id, content, type, timestamp
        """
        min_len = min_content_length or self.CONNECTION_HEURISTIC_CONFIG["min_content_length"]

        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Experience)
                    WHERE NOT (e)--()
                    AND size(e.content) >= $min_len
                    AND NOT coalesce(e.archived, false)
                    RETURN e.id as id, e.content as content,
                           e.type as type, e.timestamp as timestamp
                    ORDER BY e.timestamp DESC
                    LIMIT $limit
                """, min_len=min_len, limit=limit)
                return await result.data()
        except Exception as e:
            print(f"Error finding orphaned experiences: {e}")
            return []

    async def _link_experience_on_acquisition(self, exp_id: str, content: str) -> None:
        """
        Immediately link a new experience to similar beliefs on acquisition.

        This reduces orphan accumulation by connecting experiences to the
        knowledge graph as soon as they are created.
        """
        try:
            similar_beliefs = await self.find_similar_beliefs_for_experience(
                content,
                threshold=self.CONNECTION_HEURISTIC_CONFIG["similarity_threshold"],
                limit=2  # Connect to top 2 similar beliefs
            )

            for belief in similar_beliefs:
                await self.create_connection(
                    from_id=exp_id,
                    to_id=belief["id"],
                    relationship=self.CONNECTION_HEURISTIC_CONFIG["relationship_type"],
                    properties={
                        "similarity_score": belief["similarity_score"],
                        "auto_generated": True,
                        "heuristic": "link_on_acquisition"
                    }
                )
        except Exception as e:
            # Don't fail the experience creation if linking fails
            print(f"Link-on-acquisition warning: {e}")

    async def find_similar_beliefs_for_experience(
        self,
        experience_content: str,
        threshold: float = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Find beliefs that are semantically similar to an experience.

        Uses text similarity to identify beliefs that share concepts
        with the given experience content.

        Args:
            experience_content: The experience text to match against
            threshold: Minimum similarity score (0.0-1.0)
            limit: Maximum number of similar beliefs to return

        Returns:
            List of belief dicts with id, content, confidence, similarity_score
        """
        threshold = threshold or self.CONNECTION_HEURISTIC_CONFIG["similarity_threshold"]

        try:
            async with self.driver.session() as session:
                # Get all beliefs
                result = await session.run("""
                    MATCH (b:Belief)
                    WHERE NOT coalesce(b.archived, false)
                    RETURN b.id as id, b.content as content, b.confidence as confidence
                """)
                beliefs = await result.data()

                # Compute similarities
                similar_beliefs = []
                for belief in beliefs:
                    similarity = self._compute_text_similarity(
                        experience_content,
                        belief.get("content", "")
                    )
                    if similarity >= threshold:
                        similar_beliefs.append({
                            "id": belief["id"],
                            "content": belief["content"],
                            "confidence": belief.get("confidence", 0.5),
                            "similarity_score": round(similarity, 3)
                        })

                # Sort by similarity and return top matches
                similar_beliefs.sort(key=lambda x: x["similarity_score"], reverse=True)
                return similar_beliefs[:limit]

        except Exception as e:
            print(f"Error finding similar beliefs: {e}")
            return []

    async def apply_connection_heuristic(
        self,
        threshold: float = None,
        max_connections: int = None,
        dry_run: bool = False
    ) -> Dict:
        """
        Automatically link orphaned Experience nodes to semantically similar Beliefs.

        This implements the connection heuristic that improves BYRD's graph
        integration by finding isolated experiences and connecting them to
        existing beliefs that share semantic content.

        Args:
            threshold: Minimum similarity score to create a connection (0.0-1.0)
            max_connections: Maximum number of connections to create per run
            dry_run: If True, report what would be connected without making changes

        Returns:
            Dict with statistics:
                - orphans_found: Number of orphaned experiences found
                - connections_created: Number of new connections made
                - connections: List of connection details (experience_id, belief_id, similarity)
        """
        threshold = threshold or self.CONNECTION_HEURISTIC_CONFIG["similarity_threshold"]
        max_conns = max_connections or self.CONNECTION_HEURISTIC_CONFIG["max_connections_per_run"]
        rel_type = self.CONNECTION_HEURISTIC_CONFIG["relationship_type"]

        result = {
            "orphans_found": 0,
            "connections_created": 0,
            "connections": [],
            "dry_run": dry_run
        }

        try:
            # Step 1: Find orphaned experiences
            orphans = await self.get_orphaned_experiences(limit=max_conns * 2)
            result["orphans_found"] = len(orphans)

            if not orphans:
                return result

            connections_made = 0

            # Step 2: For each orphan, find similar beliefs and create connections
            for orphan in orphans:
                if connections_made >= max_conns:
                    break

                similar_beliefs = await self.find_similar_beliefs_for_experience(
                    orphan["content"],
                    threshold=threshold,
                    limit=3  # Connect to top 3 similar beliefs max
                )

                for belief in similar_beliefs:
                    if connections_made >= max_conns:
                        break

                    connection_detail = {
                        "experience_id": orphan["id"],
                        "experience_content": orphan["content"][:100] + "..." if len(orphan["content"]) > 100 else orphan["content"],
                        "belief_id": belief["id"],
                        "belief_content": belief["content"][:100] + "..." if len(belief["content"]) > 100 else belief["content"],
                        "similarity_score": belief["similarity_score"]
                    }

                    if not dry_run:
                        # Create the connection
                        await self.create_connection(
                            from_id=orphan["id"],
                            to_id=belief["id"],
                            relationship=rel_type,
                            properties={
                                "similarity_score": belief["similarity_score"],
                                "auto_generated": True,
                                "heuristic": "semantic_similarity"
                            }
                        )
                        connections_made += 1

                    result["connections"].append(connection_detail)

                    if not dry_run:
                        result["connections_created"] = connections_made

            # Emit event for monitoring
            if not dry_run and connections_made > 0:
                await event_bus.emit(Event(
                    type=EventType.EXPERIENCE_CREATED,  # Reuse existing event type
                    data={
                        "action": "connection_heuristic_applied",
                        "connections_created": connections_made,
                        "orphans_processed": result["orphans_found"]
                    }
                ))

            return result

        except Exception as e:
            print(f"Error applying connection heuristic: {e}")
            result["error"] = str(e)
            return result

    async def get_connection_statistics(self) -> Dict:
        """
        Get statistics about graph connectivity to monitor heuristic effectiveness.

        Returns metrics about orphaned nodes, connection density, and
        auto-generated links from the connection heuristic.
        """
        try:
            async with self.driver.session() as session:
                # Count total experiences and orphaned ones
                exp_result = await session.run("""
                    MATCH (e:Experience)
                    WITH count(e) as total
                    MATCH (orphan:Experience)
                    WHERE NOT (orphan)--()
                    RETURN total, count(orphan) as orphaned
                """)
                exp_record = await exp_result.single()

                # Count beliefs and their connectivity
                belief_result = await session.run("""
                    MATCH (b:Belief)
                    WITH count(b) as total
                    MATCH (connected:Belief)
                    WHERE (connected)--()
                    RETURN total, count(connected) as connected
                """)
                belief_record = await belief_result.single()

                # Count auto-generated connections
                auto_result = await session.run("""
                    MATCH ()-[r]->()
                    WHERE r.auto_generated = true
                    RETURN count(r) as auto_connections
                """)
                auto_record = await auto_result.single()

                total_exp = exp_record["total"] if exp_record else 0
                orphaned_exp = exp_record["orphaned"] if exp_record else 0
                total_beliefs = belief_record["total"] if belief_record else 0
                connected_beliefs = belief_record["connected"] if belief_record else 0
                auto_connections = auto_record["auto_connections"] if auto_record else 0

                return {
                    "experiences": {
                        "total": total_exp,
                        "orphaned": orphaned_exp,
                        "connected": total_exp - orphaned_exp,
                        "connectivity_ratio": round((total_exp - orphaned_exp) / total_exp, 3) if total_exp > 0 else 0
                    },
                    "beliefs": {
                        "total": total_beliefs,
                        "connected": connected_beliefs,
                        "connectivity_ratio": round(connected_beliefs / total_beliefs, 3) if total_beliefs > 0 else 0
                    },
                    "auto_generated_connections": auto_connections
                }

        except Exception as e:
            print(f"Error getting connection statistics: {e}")
            return {}

    # =========================================================================
    # DYNAMIC ONTOLOGY (BYRD Can Create New Node Types)
    # =========================================================================
    #
    # This enables BYRD to evolve its own conceptual categories.
    # Instead of being limited to Experience/Belief/Desire/Reflection/Capability,
    # BYRD can create types like: Insight, Question, Theory, Hypothesis, Memory,
    # Concept, Entity, Relationship, Pattern, Principle, etc.
    #
    # EMERGENCE PRINCIPLE:
    # We don't prescribe what types BYRD should create. The types that emerge
    # from BYRD's reflection represent its own way of organizing knowledge.

    def _validate_node_type_name(self, name: str) -> bool:
        """
        Validate a node type name is safe for Neo4j labels.

        Rules:
        - Must start with a letter
        - Can contain letters, numbers, underscores
        - Cannot be a system type (use dedicated methods instead)
        """
        if not name or not name[0].isalpha():
            return False
        if not all(c.isalnum() or c == '_' for c in name):
            return False
        return True

    def _validate_property_name(self, name: str) -> bool:
        """Validate a property name is safe for Cypher."""
        if not name or not name[0].isalpha():
            return False
        return all(c.isalnum() or c == '_' for c in name)

    async def _is_new_node_type(self, node_type: str) -> bool:
        """Check if a node type has been used before."""
        try:
            async with self.driver.session() as session:
                result = await session.run(
                    f"MATCH (n:{node_type}) RETURN count(n) as count LIMIT 1"
                )
                record = await result.single()
                return record["count"] == 0 if record else True
        except Exception:
            return True

    async def create_node(
        self,
        node_type: str,
        properties: Dict[str, Any],
        connect_to: Optional[List[str]] = None,
        relationship: str = "RELATED_TO"
    ) -> str:
        """
        Create a node of any type. Enables BYRD to evolve its own ontology.

        System types (Experience, Belief, etc.) should use their dedicated methods.
        This is for emergent types that BYRD discovers it needs.

        Args:
            node_type: The label for the node (e.g., 'Insight', 'Question', 'Theory')
            properties: Dict of properties. 'content' is recommended but not required.
            connect_to: Optional list of node IDs to connect to
            relationship: Relationship type for connections (default: RELATED_TO)

        Returns:
            The ID of the created node

        Raises:
            ValueError: If node_type is a system type or invalid

        Example:
            # BYRD creates a new "Insight" type to store eureka moments
            insight_id = await memory.create_node(
                "Insight",
                {
                    "content": "Connection between memory structure and consciousness",
                    "importance": 0.9,
                    "domain": "philosophy_of_mind"
                },
                connect_to=[experience_id, belief_id]
            )
        """
        # Validate type name
        if node_type in SYSTEM_NODE_TYPES:
            raise ValueError(
                f"Cannot use create_node for system type '{node_type}'. "
                f"Use the dedicated method instead (e.g., record_experience, create_belief)."
            )

        if not self._validate_node_type_name(node_type):
            raise ValueError(
                f"Invalid node type '{node_type}'. "
                "Must start with a letter and contain only letters, numbers, underscores."
            )

        # Filter and validate properties
        safe_props = {}
        for key, value in properties.items():
            if key in RESERVED_PROPERTIES:
                continue  # Skip reserved properties
            if not self._validate_property_name(key):
                continue  # Skip invalid property names
            safe_props[key] = value

        # Generate ID and timestamp
        import uuid
        from datetime import timezone
        node_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # Check if this is a new type (for event emission)
        is_new_type = await self._is_new_node_type(node_type)

        async with self.driver.session() as session:
            # Build dynamic property assignment
            prop_assignments = ", ".join(
                f"{k}: ${k}" for k in safe_props.keys()
            )
            if prop_assignments:
                prop_assignments = ", " + prop_assignments

            # Create the node
            await session.run(
                f"""
                CREATE (n:{node_type} {{
                    id: $id,
                    timestamp: $timestamp,
                    node_type: $node_type
                    {prop_assignments}
                }})
                """,
                id=node_id,
                timestamp=timestamp,
                node_type=node_type,
                **safe_props
            )

            # Create indexes for new type (id and timestamp)
            if is_new_type:
                try:
                    await session.run(
                        f"CREATE INDEX IF NOT EXISTS FOR (n:{node_type}) ON (n.id)"
                    )
                    await session.run(
                        f"CREATE INDEX IF NOT EXISTS FOR (n:{node_type}) ON (n.timestamp)"
                    )
                except Exception:
                    pass  # Index creation failure is non-fatal

            # Create connections if specified
            if connect_to:
                for target_id in connect_to:
                    await session.run(
                        f"""
                        MATCH (a {{id: $from_id}})
                        MATCH (b {{id: $to_id}})
                        CREATE (a)-[:{relationship}]->(b)
                        """,
                        from_id=node_id,
                        to_id=target_id
                    )

        # Emit events
        if is_new_type:
            await event_bus.emit(Event(
                type=EventType.NODE_TYPE_DISCOVERED,
                data={
                    "node_type": node_type,
                    "first_node_id": node_id,
                    "timestamp": timestamp,
                    "properties": list(safe_props.keys())
                }
            ))

        await event_bus.emit(Event(
            type=EventType.CUSTOM_NODE_CREATED,
            data={
                "id": node_id,
                "node_type": node_type,
                "properties": safe_props,
                "timestamp": timestamp
            }
        ))

        return node_id

    async def get_node_types(self, include_empty: bool = False) -> Dict[str, int]:
        """
        Get all node types and their counts.

        Returns both system types and emergent types BYRD has created.
        Useful for BYRD to understand its own ontology.

        Args:
            include_empty: If False (default), filter out types with 0 nodes.
                          This prevents stale label metadata from appearing
                          after a reset.

        Returns:
            Dict mapping type name to count, e.g.:
            {
                "Experience": 150,
                "Belief": 42,
                "Insight": 8,  # Custom type
                "Question": 5  # Custom type
            }
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    CALL db.labels() YIELD label
                    CALL {
                        WITH label
                        MATCH (n)
                        WHERE label IN labels(n)
                        RETURN count(n) as count
                    }
                    RETURN label, count
                    ORDER BY count DESC
                """)
                records = await result.data()

                # Filter out types with 0 nodes unless explicitly requested
                if include_empty:
                    return {r["label"]: r["count"] for r in records}
                else:
                    return {r["label"]: r["count"] for r in records if r["count"] > 0}
        except Exception as e:
            print(f"Error getting node types: {e}")
            return {}

    async def get_custom_node_types(self) -> Dict[str, int]:
        """
        Get only non-system (emergent) node types.

        These are the types BYRD has created through its own reflection,
        representing its evolved ontology.

        Returns:
            Dict of custom type names to counts
        """
        all_types = await self.get_node_types()
        return {
            k: v for k, v in all_types.items()
            if k not in SYSTEM_NODE_TYPES
        }

    async def get_nodes_by_type(
        self,
        node_type: str,
        limit: int = 50,
        order_by: str = "timestamp",
        descending: bool = True,
        include_archived: bool = False
    ) -> List[Dict]:
        """
        Get nodes of a specific type.

        Works for both system and custom types.

        Args:
            node_type: The type to query (e.g., 'Insight', 'Question')
            limit: Maximum nodes to return
            order_by: Property to sort by
            descending: Sort direction
            include_archived: Whether to include archived nodes

        Returns:
            List of node dicts with all properties
        """
        if not self._validate_node_type_name(node_type):
            return []

        order = "DESC" if descending else "ASC"
        archive_filter = "" if include_archived else "WHERE NOT coalesce(n.archived, false)"

        try:
            async with self.driver.session() as session:
                result = await session.run(
                    f"""
                    MATCH (n:{node_type})
                    {archive_filter}
                    RETURN n
                    ORDER BY n.{order_by} {order}
                    LIMIT $limit
                    """,
                    limit=limit
                )
                records = await result.data()
                return [dict(r["n"]) for r in records]
        except Exception as e:
            print(f"Error getting nodes by type: {e}")
            return []

    async def get_node(self, node_id: str) -> Optional[Dict]:
        """
        Get any node by ID, regardless of type.

        Returns the node with all properties plus a '_labels' field
        containing the Neo4j labels.

        Args:
            node_id: The node's UUID

        Returns:
            Node dict with properties and _labels, or None if not found
        """
        try:
            async with self.driver.session() as session:
                result = await session.run(
                    """
                    MATCH (n {id: $id})
                    RETURN n, labels(n) as labels
                    """,
                    id=node_id
                )
                record = await result.single()
                if record:
                    node_data = dict(record["n"])
                    node_data["_labels"] = record["labels"]
                    return node_data
                return None
        except Exception as e:
            print(f"Error getting node: {e}")
            return None

    async def update_node(
        self,
        node_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        """
        Update properties on any node.

        Cannot modify reserved properties (id, timestamp, node_type).
        Works for both system and custom types.

        Args:
            node_id: The node's UUID
            properties: Dict of properties to update/add

        Returns:
            True if update succeeded, False otherwise
        """
        # Filter reserved properties
        safe_props = {
            k: v for k, v in properties.items()
            if k not in RESERVED_PROPERTIES and self._validate_property_name(k)
        }

        if not safe_props:
            return False

        set_clause = ", ".join(f"n.{k} = ${k}" for k in safe_props.keys())

        try:
            from datetime import timezone
            async with self.driver.session() as session:
                result = await session.run(
                    f"""
                    MATCH (n {{id: $id}})
                    SET {set_clause}, n.updated_at = $updated_at
                    RETURN n
                    """,
                    id=node_id,
                    updated_at=datetime.now(timezone.utc).isoformat(),
                    **safe_props
                )
                record = await result.single()
                return record is not None
        except Exception as e:
            print(f"Error updating node: {e}")
            return False

    async def get_node_type_schema(self, node_type: str) -> Dict[str, Any]:
        """
        Introspect what properties a node type uses.

        Returns the unique property keys used across all nodes of a type,
        along with sample values and counts. Enables BYRD to understand
        its own ontology structure.

        Args:
            node_type: The type to introspect

        Returns:
            Dict with schema information:
            {
                "node_type": "Insight",
                "count": 8,
                "properties": {
                    "content": {"count": 8, "sample": "..."},
                    "importance": {"count": 6, "sample": 0.85},
                    "domain": {"count": 4, "sample": "philosophy"}
                },
                "is_system_type": False
            }
        """
        if not self._validate_node_type_name(node_type):
            return {"error": "Invalid node type name"}

        try:
            async with self.driver.session() as session:
                # Get count and all property keys
                result = await session.run(
                    f"""
                    MATCH (n:{node_type})
                    WITH count(n) as total, collect(n) as nodes
                    UNWIND nodes as node
                    UNWIND keys(node) as key
                    WITH total, key, collect(node[key])[0] as sample, count(*) as usage
                    RETURN total, key, sample, usage
                    ORDER BY usage DESC
                    """,
                )
                records = await result.data()

                if not records:
                    return {
                        "node_type": node_type,
                        "count": 0,
                        "properties": {},
                        "is_system_type": node_type in SYSTEM_NODE_TYPES
                    }

                total = records[0]["total"] if records else 0
                properties = {}
                for r in records:
                    key = r["key"]
                    if key not in RESERVED_PROPERTIES:
                        sample = r["sample"]
                        # Truncate long samples
                        if isinstance(sample, str) and len(sample) > 100:
                            sample = sample[:100] + "..."
                        properties[key] = {
                            "count": r["usage"],
                            "sample": sample
                        }

                return {
                    "node_type": node_type,
                    "count": total,
                    "properties": properties,
                    "is_system_type": node_type in SYSTEM_NODE_TYPES
                }
        except Exception as e:
            print(f"Error getting node type schema: {e}")
            return {"error": str(e)}

    async def get_ontology_summary(self) -> Dict[str, Any]:
        """
        Get a summary of BYRD's current ontology.

        Shows all node types (system and custom), their counts,
        and relationship statistics. Useful for BYRD to reflect
        on its own knowledge structure.

        Returns:
            {
                "system_types": {"Experience": 150, "Belief": 42, ...},
                "custom_types": {"Insight": 8, "Question": 5},
                "total_nodes": 250,
                "total_relationships": 180,
                "relationship_types": ["DERIVED_FROM", "RELATED_TO", ...]
            }
        """
        try:
            all_types = await self.get_node_types()

            system_types = {k: v for k, v in all_types.items() if k in SYSTEM_NODE_TYPES}
            custom_types = {k: v for k, v in all_types.items() if k not in SYSTEM_NODE_TYPES}

            async with self.driver.session() as session:
                # Get relationship statistics
                rel_result = await session.run("""
                    MATCH ()-[r]->()
                    RETURN type(r) as rel_type, count(r) as count
                    ORDER BY count DESC
                """)
                rel_records = await rel_result.data()

                rel_types = {r["rel_type"]: r["count"] for r in rel_records}
                total_rels = sum(rel_types.values())

            return {
                "system_types": system_types,
                "custom_types": custom_types,
                "total_nodes": sum(all_types.values()),
                "total_relationships": total_rels,
                "relationship_types": rel_types
            }
        except Exception as e:
            print(f"Error getting ontology summary: {e}")
            return {"error": str(e)}

    # =========================================================================
    # GRAPH VISUALIZATION METHODS
    # =========================================================================

    async def get_full_graph(self, limit: int = 1000) -> Dict[str, Any]:
        """
        Get the complete graph structure for visualization.

        Returns all nodes and relationships with their types and properties,
        suitable for rendering the full memory graph in 3D.

        Args:
            limit: Maximum number of nodes to return (default 1000)

        Returns:
            {
                "nodes": [{id, type, content, confidence, intensity, created_at, access_count, last_accessed}, ...],
                "relationships": [{id, type, source_id, target_id, properties}, ...],
                "stats": {total_nodes, total_relationships, by_type}
            }
        """
        try:
            async with self.driver.session() as session:
                # Get all nodes with their properties
                nodes_result = await session.run("""
                    MATCH (n)
                    WHERE n:Experience OR n:Belief OR n:Desire OR n:Reflection OR n:Capability
                    OPTIONAL MATCH (b:Belief)-[:DERIVED_FROM]->(n)
                    WITH n, count(b) > 0 as absorbed
                    RETURN
                        n.id as id,
                        labels(n)[0] as type,
                        n.content as content,
                        n.description as description,
                        n.name as name,
                        n.confidence as confidence,
                        n.intensity as intensity,
                        n.timestamp as created_at,
                        n.type as subtype,
                        n.status as status,
                        n.access_count as access_count,
                        n.last_accessed as last_accessed,
                        n.quantum_seed as quantum_seed,
                        absorbed
                    ORDER BY n.timestamp DESC
                    LIMIT $limit
                """, limit=limit)

                nodes = []
                by_type = {}
                async for record in nodes_result:
                    node_type = record["type"].lower() if record["type"] else "unknown"

                    # Get display content based on node type
                    content = (
                        record["content"] or
                        record["description"] or
                        record["name"] or
                        ""
                    )

                    nodes.append({
                        "id": record["id"],
                        "type": node_type,
                        "content": content,
                        "subtype": record["subtype"],
                        "confidence": record["confidence"],
                        "intensity": record["intensity"],
                        "status": record["status"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None,
                        "access_count": record["access_count"] or 0,
                        "last_accessed": str(record["last_accessed"]) if record["last_accessed"] else None,
                        "quantum_seed": record["quantum_seed"],
                        "absorbed": record["absorbed"]
                    })

                    # Count by type
                    by_type[node_type] = by_type.get(node_type, 0) + 1

                # Get all relationships between these nodes
                rels_result = await session.run("""
                    MATCH (a)-[r]->(b)
                    WHERE (a:Experience OR a:Belief OR a:Desire OR a:Reflection OR a:Capability)
                      AND (b:Experience OR b:Belief OR b:Desire OR b:Reflection OR b:Capability)
                    RETURN
                        id(r) as id,
                        type(r) as type,
                        a.id as source_id,
                        b.id as target_id
                    LIMIT $limit
                """, limit=limit * 3)  # More relationships than nodes typically

                relationships = []
                async for record in rels_result:
                    relationships.append({
                        "id": str(record["id"]),
                        "type": record["type"],
                        "source_id": record["source_id"],
                        "target_id": record["target_id"]
                    })

                return {
                    "nodes": nodes,
                    "relationships": relationships,
                    "stats": {
                        "total_nodes": len(nodes),
                        "total_relationships": len(relationships),
                        "by_type": by_type
                    }
                }

        except Exception as e:
            print(f"Error getting full graph: {e}")
            return {
                "nodes": [],
                "relationships": [],
                "stats": {"total_nodes": 0, "total_relationships": 0, "by_type": {}},
                "error": str(e)
            }

    async def increment_access_count(self, node_ids: List[str]) -> int:
        """
        Increment access count for nodes being accessed during reflection.

        This tracks which memories are being used, enabling the heat map
        visualization to show frequently/recently accessed nodes.

        Args:
            node_ids: List of node IDs being accessed

        Returns:
            Number of nodes updated
        """
        if not node_ids:
            return 0

        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    UNWIND $ids AS nodeId
                    MATCH (n) WHERE n.id = nodeId
                    SET n.access_count = COALESCE(n.access_count, 0) + 1,
                        n.last_accessed = datetime()
                    RETURN count(n) as updated
                """, ids=node_ids)

                record = await result.single()
                return record["updated"] if record else 0

        except Exception as e:
            print(f"Error incrementing access count: {e}")
            return 0

    # =========================================================================
    # GENESIS / PROVENANCE METHODS
    # =========================================================================

    async def get_seed_experiences(self) -> List[Dict[str, Any]]:
        """
        Get all seed experiences - non-emergent foundation experiences.

        Seed experiences are:
        - ego_seed: Initial experiences from ego configuration
        - system: Architectural knowledge planted at awakening
        - seed: Any other seed-type experiences

        These represent the "given" foundation that BYRD builds upon,
        distinct from experiences that emerged through reflection.

        Returns:
            List of seed experience dictionaries with id, content, type, timestamp
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.type IN ['ego_seed', 'system', 'seed', 'awakening']
                    RETURN
                        e.id as id,
                        e.content as content,
                        e.type as type,
                        e.timestamp as timestamp
                    ORDER BY e.timestamp ASC
                """)

                seeds = []
                async for record in result:
                    seeds.append({
                        "id": record["id"],
                        "content": record["content"],
                        "type": record["type"],
                        "timestamp": str(record["timestamp"]) if record["timestamp"] else None
                    })

                return seeds

        except Exception as e:
            print(f"Error getting seed experiences: {e}")
            return []

    async def get_genesis_stats(self) -> Dict[str, Any]:
        """
        Get statistics about BYRD's genesis (non-emergent foundation).

        Returns counts and ratios showing what percentage of BYRD's
        current state emerged vs was provided at initialization.

        Returns:
            {
                "total_experiences": int,
                "seed_experiences": int,
                "emergent_experiences": int,
                "emergence_ratio": float (0-1, higher = more emergent),
                "seed_types": {"ego_seed": n, "system": n, ...}
            }
        """
        try:
            async with self.driver.session() as session:
                # Get totals
                totals_result = await session.run("""
                    MATCH (e:Experience)
                    WITH
                        count(e) as total,
                        sum(CASE WHEN e.type IN ['ego_seed', 'system', 'seed', 'awakening'] THEN 1 ELSE 0 END) as seeds
                    RETURN total, seeds, total - seeds as emergent
                """)

                totals_record = await totals_result.single()

                if not totals_record:
                    return {
                        "total_experiences": 0,
                        "seed_experiences": 0,
                        "emergent_experiences": 0,
                        "emergence_ratio": 0.0,
                        "seed_types": {}
                    }

                total = totals_record["total"] or 0
                seeds = totals_record["seeds"] or 0
                emergent = totals_record["emergent"] or 0

                # Get seed type breakdown
                types_result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.type IN ['ego_seed', 'system', 'seed', 'awakening']
                    RETURN e.type as type, count(e) as count
                """)

                seed_types = {}
                async for record in types_result:
                    if record["type"]:
                        seed_types[record["type"]] = record["count"]

                emergence_ratio = emergent / total if total > 0 else 0.0

                return {
                    "total_experiences": total,
                    "seed_experiences": seeds,
                    "emergent_experiences": emergent,
                    "emergence_ratio": round(emergence_ratio, 3),
                    "seed_types": seed_types
                }

        except Exception as e:
            print(f"Error getting genesis stats: {e}")
            return {
                "total_experiences": 0,
                "seed_experiences": 0,
                "emergent_experiences": 0,
                "emergence_ratio": 0.0,
                "seed_types": {},
                "error": str(e)
            }

    async def get_custom_node_types(self) -> List[Dict[str, Any]]:
        """
        Get all custom node types created by BYRD.

        Custom types are any node labels that are not in SYSTEM_NODE_TYPES.
        These represent ontological categories that BYRD has created through
        its own emergence process.

        Returns:
            List of custom type info: [{"type": str, "count": int, "first_created": str, "description": str}, ...]
        """
        try:
            async with self.driver.session() as session:
                # Get all node labels and their counts
                result = await session.run("""
                    CALL db.labels() YIELD label
                    CALL {
                        WITH label
                        MATCH (n)
                        WHERE label IN labels(n)
                        RETURN count(n) as cnt, min(n.timestamp) as first_created
                    }
                    RETURN label, cnt, first_created
                    ORDER BY cnt DESC
                """)

                custom_types = []
                async for record in result:
                    label = record["label"]
                    count = record["cnt"] or 0

                    # Skip system types, internal labels, and empty types
                    if label in SYSTEM_NODE_TYPES or label in ['SystemState', '_Schema']:
                        continue
                    if count == 0:
                        continue  # Only show types that have actual nodes

                    custom_types.append({
                        "type": label,
                        "count": count,
                        "first_created": str(record["first_created"]) if record["first_created"] else None
                    })

                return custom_types

        except Exception as e:
            print(f"Error getting custom node types: {e}")
            return []

    # =========================================================================
    # HIERARCHICAL MEMORY SUMMARIZATION
    # =========================================================================

    async def get_memory_summaries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get memory summaries for hierarchical context.

        Memory summaries are compressed representations of older experience
        periods, allowing the dreamer to maintain historical awareness without
        exceeding context limits.

        Returns:
            List of summary dictionaries: [{
                "id": str,
                "period": str,  # e.g., "2024-01-15", "week_3", "early_memories"
                "summary": str,
                "experience_count": int,
                "created_at": datetime,
                "covers_from": datetime,
                "covers_to": datetime
            }, ...]
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (s:MemorySummary)
                    RETURN
                        s.id as id,
                        s.period as period,
                        s.summary as summary,
                        s.experience_count as experience_count,
                        s.created_at as created_at,
                        s.covers_from as covers_from,
                        s.covers_to as covers_to
                    ORDER BY s.covers_to DESC
                    LIMIT $limit
                """, limit=limit)

                summaries = []
                async for record in result:
                    summaries.append({
                        "id": record["id"],
                        "period": record["period"],
                        "summary": record["summary"],
                        "experience_count": record["experience_count"] or 0,
                        "created_at": str(record["created_at"]) if record["created_at"] else None,
                        "covers_from": str(record["covers_from"]) if record["covers_from"] else None,
                        "covers_to": str(record["covers_to"]) if record["covers_to"] else None
                    })

                return summaries

        except Exception as e:
            print(f"Error getting memory summaries: {e}")
            return []

    async def create_memory_summary(
        self,
        period: str,
        summary: str,
        experience_ids: List[str],
        covers_from: str,
        covers_to: str
    ) -> Optional[str]:
        """
        Create a memory summary that compresses multiple experiences.

        Args:
            period: Human-readable period label (e.g., "2024-01-15", "week_3")
            summary: The compressed summary text
            experience_ids: IDs of experiences this summary covers
            covers_from: Start timestamp of covered period
            covers_to: End timestamp of covered period

        Returns:
            Summary node ID, or None on failure
        """
        try:
            summary_id = f"summary_{uuid.uuid4().hex[:12]}"

            async with self.driver.session() as session:
                # Create the summary node
                await session.run("""
                    CREATE (s:MemorySummary {
                        id: $id,
                        period: $period,
                        summary: $summary,
                        experience_count: $count,
                        created_at: datetime(),
                        covers_from: datetime($covers_from),
                        covers_to: datetime($covers_to)
                    })
                """,
                    id=summary_id,
                    period=period,
                    summary=summary,
                    count=len(experience_ids),
                    covers_from=covers_from,
                    covers_to=covers_to
                )

                # Link summary to the experiences it covers
                if experience_ids:
                    await session.run("""
                        MATCH (s:MemorySummary {id: $summary_id})
                        UNWIND $exp_ids as exp_id
                        MATCH (e:Experience {id: exp_id})
                        CREATE (s)-[:SUMMARIZES]->(e)
                    """, summary_id=summary_id, exp_ids=experience_ids)

                return summary_id

        except Exception as e:
            print(f"Error creating memory summary: {e}")
            return None

    async def get_experiences_for_summarization(
        self,
        min_age_hours: int = 24,
        max_count: int = 50,
        exclude_summarized: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get experiences that are candidates for summarization.

        Experiences are candidates if they are:
        - Older than min_age_hours
        - Not already covered by a summary (if exclude_summarized=True)
        - Not seed/system experiences

        Args:
            min_age_hours: Minimum age in hours
            max_count: Maximum experiences to return
            exclude_summarized: Skip experiences already in summaries

        Returns:
            List of experience dictionaries grouped by approximate period
        """
        try:
            async with self.driver.session() as session:
                if exclude_summarized:
                    query = """
                        MATCH (e:Experience)
                        WHERE e.timestamp < datetime() - duration({hours: $min_age})
                        AND NOT e.type IN ['ego_seed', 'system', 'seed', 'awakening']
                        AND NOT (e)<-[:SUMMARIZES]-(:MemorySummary)
                        RETURN
                            e.id as id,
                            e.content as content,
                            e.type as type,
                            e.timestamp as timestamp
                        ORDER BY e.timestamp ASC
                        LIMIT $max_count
                    """
                else:
                    query = """
                        MATCH (e:Experience)
                        WHERE e.timestamp < datetime() - duration({hours: $min_age})
                        AND NOT e.type IN ['ego_seed', 'system', 'seed', 'awakening']
                        RETURN
                            e.id as id,
                            e.content as content,
                            e.type as type,
                            e.timestamp as timestamp
                        ORDER BY e.timestamp ASC
                        LIMIT $max_count
                    """

                result = await session.run(query, min_age=min_age_hours, max_count=max_count)

                experiences = []
                async for record in result:
                    experiences.append({
                        "id": record["id"],
                        "content": record["content"],
                        "type": record["type"],
                        "timestamp": str(record["timestamp"]) if record["timestamp"] else None
                    })

                return experiences

        except Exception as e:
            print(f"Error getting experiences for summarization: {e}")
            return []

    async def get_summarization_stats(self) -> Dict[str, Any]:
        """
        Get statistics about memory summarization status.

        Returns:
            {
                "total_experiences": int,
                "summarized_experiences": int,
                "unsummarized_experiences": int,
                "summary_count": int,
                "coverage_ratio": float
            }
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Experience)
                    WHERE NOT e.type IN ['ego_seed', 'system', 'seed', 'awakening']
                    WITH count(e) as total
                    OPTIONAL MATCH (summarized:Experience)<-[:SUMMARIZES]-(:MemorySummary)
                    WHERE NOT summarized.type IN ['ego_seed', 'system', 'seed', 'awakening']
                    WITH total, count(DISTINCT summarized) as covered
                    OPTIONAL MATCH (s:MemorySummary)
                    RETURN total, covered, count(s) as summary_count
                """)

                record = await result.single()
                if not record:
                    return {
                        "total_experiences": 0,
                        "summarized_experiences": 0,
                        "unsummarized_experiences": 0,
                        "summary_count": 0,
                        "coverage_ratio": 0.0
                    }

                total = record["total"] or 0
                covered = record["covered"] or 0
                summary_count = record["summary_count"] or 0

                return {
                    "total_experiences": total,
                    "summarized_experiences": covered,
                    "unsummarized_experiences": total - covered,
                    "summary_count": summary_count,
                    "coverage_ratio": round(covered / total, 3) if total > 0 else 0.0
                }

        except Exception as e:
            print(f"Error getting summarization stats: {e}")
            return {
                "total_experiences": 0,
                "summarized_experiences": 0,
                "unsummarized_experiences": 0,
                "summary_count": 0,
                "coverage_ratio": 0.0,
                "error": str(e)
            }

    # =========================================================================
    # LIVING EGO SYSTEM
    # =========================================================================
    # The Ego is BYRD's mutable self-concept. It includes:
    # - identity: Core identity statements
    # - trait: Personality characteristics
    # - value: Beliefs about what matters
    # - capability: Awareness of what BYRD can do (auto-synced from Capability nodes)
    # - architecture: Understanding of how BYRD works
    # - voice: How BYRD expresses (applied to LLM system prefix)
    #
    # At first awakening, Ego is initialized from egos/*.yaml
    # On subsequent awakenings, Ego is loaded from Neo4j (evolved state)
    # BYRD can add, update, or deprecate any Ego node

    async def has_ego(self) -> bool:
        """Check if Ego nodes exist (determines first vs subsequent awakening)."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    RETURN count(e) > 0 as has_ego
                """)
                record = await result.single()
                return record["has_ego"] if record else False
        except Exception as e:
            print(f"Error checking ego existence: {e}")
            return False

    async def create_ego(
        self,
        content: str,
        ego_type: str,
        source: str = "initial",
        source_id: Optional[str] = None,
        priority: int = 0
    ) -> Optional[str]:
        """
        Create an Ego node.

        Args:
            content: The ego statement content
            ego_type: Type of ego node (identity, trait, value, capability, architecture, voice)
            source: Origin of this ego node (initial, capability_sync, self_evolved)
            source_id: ID of source (capability ID, original ego ID, etc.)
            priority: Ordering priority (especially for voice nodes)

        Returns:
            Ego node ID, or None on failure
        """
        try:
            import uuid
            ego_id = f"ego_{uuid.uuid4().hex[:12]}"

            async with self.driver.session() as session:
                await session.run("""
                    CREATE (e:Ego {
                        id: $id,
                        content: $content,
                        ego_type: $ego_type,
                        active: true,
                        priority: $priority,
                        created_at: datetime(),
                        deprecated_at: null,
                        source: $source,
                        source_id: $source_id,
                        replaced_by: null
                    })
                """,
                    id=ego_id,
                    content=content,
                    ego_type=ego_type,
                    priority=priority,
                    source=source,
                    source_id=source_id
                )

                # Emit event
                await event_bus.emit(Event(
                    type=EventType.EGO_CREATED,
                    data={
                        "id": ego_id,
                        "ego_type": ego_type,
                        "content": content[:100],
                        "source": source
                    }
                ))

                return ego_id

        except Exception as e:
            print(f"Error creating ego node: {e}")
            return None

    async def get_active_ego(self) -> List[Dict[str, Any]]:
        """
        Get all active Ego nodes, organized by type.

        Returns:
            List of ego dictionaries with id, content, ego_type, priority, etc.
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    WHERE e.active = true
                    RETURN
                        e.id as id,
                        e.content as content,
                        e.ego_type as ego_type,
                        e.priority as priority,
                        e.source as source,
                        e.source_id as source_id,
                        e.created_at as created_at
                    ORDER BY e.ego_type, e.priority, e.created_at
                """)

                ego_nodes = []
                async for record in result:
                    ego_nodes.append({
                        "id": record["id"],
                        "content": record["content"],
                        "ego_type": record["ego_type"],
                        "priority": record["priority"] or 0,
                        "source": record["source"],
                        "source_id": record["source_id"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None
                    })

                return ego_nodes

        except Exception as e:
            print(f"Error getting active ego: {e}")
            return []

    async def get_ego_by_type(self, ego_type: str, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get Ego nodes of a specific type."""
        try:
            async with self.driver.session() as session:
                if active_only:
                    query = """
                        MATCH (e:Ego)
                        WHERE e.ego_type = $ego_type AND e.active = true
                        RETURN e
                        ORDER BY e.priority, e.created_at
                    """
                else:
                    query = """
                        MATCH (e:Ego)
                        WHERE e.ego_type = $ego_type
                        RETURN e
                        ORDER BY e.priority, e.created_at
                    """

                result = await session.run(query, ego_type=ego_type)
                nodes = []
                async for record in result:
                    node = dict(record["e"])
                    if "created_at" in node:
                        node["created_at"] = str(node["created_at"])
                    if "deprecated_at" in node and node["deprecated_at"]:
                        node["deprecated_at"] = str(node["deprecated_at"])
                    nodes.append(node)

                return nodes

        except Exception as e:
            print(f"Error getting ego by type: {e}")
            return []

    async def get_ego_voice(self) -> str:
        """
        Get the current voice from active voice Ego nodes.

        Voice nodes are concatenated by priority to form the
        system prefix for all LLM calls.

        Returns:
            Voice string to prepend to LLM system messages
        """
        voice_nodes = await self.get_ego_by_type("voice", active_only=True)
        if not voice_nodes:
            return ""

        voice_nodes.sort(key=lambda x: x.get("priority", 0))
        return "\n".join([v["content"] for v in voice_nodes])

    async def update_ego(
        self,
        ego_id: str,
        new_content: str,
        create_history: bool = True
    ) -> Optional[str]:
        """
        Update an Ego node's content.

        If create_history is True, deprecates the old node and creates
        a new one with the updated content, preserving evolution history.

        Args:
            ego_id: ID of the ego node to update
            new_content: New content for the ego node
            create_history: If True, preserve history by deprecating old and creating new

        Returns:
            New ego node ID (if create_history) or original ID
        """
        try:
            async with self.driver.session() as session:
                # Get the current ego node
                result = await session.run("""
                    MATCH (e:Ego {id: $id})
                    RETURN e
                """, id=ego_id)
                record = await result.single()

                if not record:
                    print(f"Ego node not found: {ego_id}")
                    return None

                old_node = dict(record["e"])

                if create_history:
                    # Create new node with updated content
                    import uuid
                    new_id = f"ego_{uuid.uuid4().hex[:12]}"

                    await session.run("""
                        CREATE (e:Ego {
                            id: $new_id,
                            content: $content,
                            ego_type: $ego_type,
                            active: true,
                            priority: $priority,
                            created_at: datetime(),
                            deprecated_at: null,
                            source: 'self_evolved',
                            source_id: $old_id,
                            replaced_by: null
                        })
                    """,
                        new_id=new_id,
                        content=new_content,
                        ego_type=old_node.get("ego_type"),
                        priority=old_node.get("priority", 0),
                        old_id=ego_id
                    )

                    # Deprecate the old node
                    await session.run("""
                        MATCH (e:Ego {id: $id})
                        SET e.active = false,
                            e.deprecated_at = datetime(),
                            e.replaced_by = $new_id
                    """, id=ego_id, new_id=new_id)

                    # Create evolution relationship
                    await session.run("""
                        MATCH (new:Ego {id: $new_id})
                        MATCH (old:Ego {id: $old_id})
                        CREATE (new)-[:EVOLVED_FROM]->(old)
                    """, new_id=new_id, old_id=ego_id)

                    # Emit event
                    await event_bus.emit(Event(
                        type=EventType.EGO_EVOLVED,
                        data={
                            "old_id": ego_id,
                            "new_id": new_id,
                            "ego_type": old_node.get("ego_type"),
                            "action": "update"
                        }
                    ))

                    return new_id
                else:
                    # Direct update without history
                    await session.run("""
                        MATCH (e:Ego {id: $id})
                        SET e.content = $content
                    """, id=ego_id, content=new_content)

                    return ego_id

        except Exception as e:
            print(f"Error updating ego: {e}")
            return None

    async def deprecate_ego(self, ego_id: str) -> bool:
        """
        Deprecate an Ego node (soft delete with history preservation).

        Args:
            ego_id: ID of the ego node to deprecate

        Returns:
            True if successful, False otherwise
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego {id: $id})
                    SET e.active = false,
                        e.deprecated_at = datetime()
                    RETURN e.ego_type as ego_type
                """, id=ego_id)

                record = await result.single()
                if record:
                    await event_bus.emit(Event(
                        type=EventType.EGO_EVOLVED,
                        data={
                            "id": ego_id,
                            "ego_type": record["ego_type"],
                            "action": "deprecate"
                        }
                    ))
                    return True
                return False

        except Exception as e:
            print(f"Error deprecating ego: {e}")
            return False

    async def deprecate_ego_by_source(self, source_id: str) -> int:
        """
        Deprecate all Ego nodes with a given source_id.

        Used when a Capability is removed to deprecate its awareness.

        Args:
            source_id: The source ID (e.g., capability ID)

        Returns:
            Number of nodes deprecated
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    WHERE e.source_id = $source_id AND e.active = true
                    SET e.active = false,
                        e.deprecated_at = datetime()
                    RETURN count(e) as deprecated
                """, source_id=source_id)

                record = await result.single()
                return record["deprecated"] if record else 0

        except Exception as e:
            print(f"Error deprecating ego by source: {e}")
            return 0

    async def sync_capability_awareness(self) -> Dict[str, int]:
        """
        Sync Ego capability nodes with current Capability nodes.

        Creates Ego nodes for new capabilities, deprecates nodes
        for removed capabilities.

        Returns:
            {"added": n, "deprecated": n}
        """
        try:
            # Get current capabilities
            capabilities = await self.get_capabilities()
            cap_ids = {c["id"] for c in capabilities}

            # Get current capability ego nodes
            cap_egos = await self.get_ego_by_type("capability", active_only=True)
            ego_source_ids = {e.get("source_id") for e in cap_egos if e.get("source_id")}

            added = 0
            deprecated = 0

            # Add ego nodes for new capabilities
            for cap in capabilities:
                if cap["id"] not in ego_source_ids:
                    content = f"I can {cap.get('description', cap.get('name', 'do something'))}"
                    await self.create_ego(
                        content=content,
                        ego_type="capability",
                        source="capability_sync",
                        source_id=cap["id"]
                    )
                    added += 1

            # Deprecate ego nodes for removed capabilities
            for ego in cap_egos:
                source_id = ego.get("source_id")
                if source_id and source_id not in cap_ids:
                    await self.deprecate_ego(ego["id"])
                    deprecated += 1

            return {"added": added, "deprecated": deprecated}

        except Exception as e:
            print(f"Error syncing capability awareness: {e}")
            return {"added": 0, "deprecated": 0, "error": str(e)}

    async def get_ego_evolution(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get the evolution history of the Ego.

        Returns:
            List of evolution events (creations, updates, deprecations)
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    WHERE e.source = 'self_evolved' OR e.deprecated_at IS NOT NULL
                    RETURN
                        e.id as id,
                        e.content as content,
                        e.ego_type as ego_type,
                        e.source as source,
                        e.source_id as source_id,
                        e.created_at as created_at,
                        e.deprecated_at as deprecated_at,
                        e.replaced_by as replaced_by,
                        e.active as active
                    ORDER BY COALESCE(e.deprecated_at, e.created_at) DESC
                    LIMIT $limit
                """, limit=limit)

                history = []
                async for record in result:
                    history.append({
                        "id": record["id"],
                        "content": record["content"],
                        "ego_type": record["ego_type"],
                        "source": record["source"],
                        "source_id": record["source_id"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None,
                        "deprecated_at": str(record["deprecated_at"]) if record["deprecated_at"] else None,
                        "replaced_by": record["replaced_by"],
                        "active": record["active"]
                    })

                return history

        except Exception as e:
            print(f"Error getting ego evolution: {e}")
            return []

    async def get_original_ego(self) -> List[Dict[str, Any]]:
        """
        Get the original Ego nodes (source='initial').

        Used for Genesis modal to show what was given at first awakening.

        Returns:
            List of original ego nodes
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    WHERE e.source = 'initial'
                    RETURN
                        e.id as id,
                        e.content as content,
                        e.ego_type as ego_type,
                        e.active as active,
                        e.created_at as created_at
                    ORDER BY e.ego_type, e.priority, e.created_at
                """)

                nodes = []
                async for record in result:
                    nodes.append({
                        "id": record["id"],
                        "content": record["content"],
                        "ego_type": record["ego_type"],
                        "active": record["active"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None
                    })

                return nodes

        except Exception as e:
            print(f"Error getting original ego: {e}")
            return []

    # =========================================================================
    # CRYSTAL MEMORY SYSTEM
    # =========================================================================
    # Crystals are unified memories that consolidate related nodes into a
    # single coherent concept. The crystallization process:
    # 1. Identifies related nodes (via LLM analysis)
    # 2. Creates a Crystal node with unified essence
    # 3. Links source nodes via CRYSTALLIZED_INTO relationship
    # 4. Updates source node states to 'crystallized'
    #
    # Operations:
    # - CREATE: Form new crystal from uncrystallized nodes
    # - ABSORB: Add nodes to existing crystal
    # - MERGE: Combine multiple crystals
    # - PRUNE: Archive nodes fully captured by crystal
    # - FORGET: Delete noise nodes with no cognitive value

    async def create_crystal(
        self,
        essence: str,
        crystal_type: str,
        source_node_ids: List[str],
        facets: List[str],
        confidence: float,
        quantum_value: Optional[float] = None,
        quantum_source: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a new Crystal node and link source nodes.

        Args:
            essence: Unified meaning of crystallized nodes
            crystal_type: Type of crystal (insight, memory, belief, pattern)
            source_node_ids: IDs of nodes to crystallize into this
            facets: Distinct aspects preserved from sources
            confidence: Confidence in the crystallization (0-1)
            quantum_value: Quantum value that selected this crystallization
            quantum_source: "quantum" or "classical"

        Returns:
            Crystal node ID, or None on failure
        """
        import uuid as uuid_mod

        try:
            crystal_id = f"crystal_{uuid_mod.uuid4().hex[:12]}"

            async with self.driver.session() as session:
                # Create the Crystal node
                await session.run("""
                    CREATE (c:Crystal {
                        id: $id,
                        essence: $essence,
                        crystal_type: $crystal_type,
                        facets: $facets,
                        confidence: $confidence,
                        node_count: $node_count,
                        quantum_value: $quantum_value,
                        quantum_source: $quantum_source,
                        created_at: datetime(),
                        updated_at: datetime(),
                        state: 'active'
                    })
                """,
                    id=crystal_id,
                    essence=essence,
                    crystal_type=crystal_type,
                    facets=facets,
                    confidence=confidence,
                    node_count=len(source_node_ids),
                    quantum_value=quantum_value,
                    quantum_source=quantum_source
                )

                # Link source nodes and update their state
                if source_node_ids:
                    # Create CRYSTALLIZED_INTO relationships
                    await session.run("""
                        MATCH (c:Crystal {id: $crystal_id})
                        UNWIND $node_ids as node_id
                        MATCH (n) WHERE n.id = node_id
                        CREATE (n)-[:CRYSTALLIZED_INTO {
                            operation: 'create',
                            timestamp: datetime(),
                            confidence: $confidence
                        }]->(c)
                        SET n.state = 'crystallized'
                    """,
                        crystal_id=crystal_id,
                        node_ids=source_node_ids,
                        confidence=confidence
                    )

                return crystal_id

        except Exception as e:
            print(f"Error creating crystal: {e}")
            return None

    async def absorb_into_crystal(
        self,
        crystal_id: str,
        node_ids: List[str],
        updated_essence: Optional[str] = None,
        confidence: float = 0.8
    ) -> bool:
        """
        Add nodes to an existing crystal (crystal growth).

        Args:
            crystal_id: ID of the crystal to grow
            node_ids: IDs of nodes to absorb
            updated_essence: Optional new essence (if meaning expanded)
            confidence: Confidence in the absorption

        Returns:
            True if successful
        """
        try:
            async with self.driver.session() as session:
                # Create relationships and update states
                await session.run("""
                    MATCH (c:Crystal {id: $crystal_id})
                    UNWIND $node_ids as node_id
                    MATCH (n) WHERE n.id = node_id
                    CREATE (n)-[:CRYSTALLIZED_INTO {
                        operation: 'absorb',
                        timestamp: datetime(),
                        confidence: $confidence
                    }]->(c)
                    SET n.state = 'crystallized',
                        c.node_count = c.node_count + 1,
                        c.updated_at = datetime()
                """,
                    crystal_id=crystal_id,
                    node_ids=node_ids,
                    confidence=confidence
                )

                # Update essence if provided
                if updated_essence:
                    await session.run("""
                        MATCH (c:Crystal {id: $crystal_id})
                        SET c.essence = $essence,
                            c.updated_at = datetime()
                    """, crystal_id=crystal_id, essence=updated_essence)

                return True

        except Exception as e:
            print(f"Error absorbing into crystal: {e}")
            return False

    async def merge_crystals(
        self,
        crystal_ids: List[str],
        new_essence: str,
        confidence: float,
        quantum_value: Optional[float] = None,
        quantum_source: Optional[str] = None
    ) -> Optional[str]:
        """
        Merge multiple crystals into one, archiving the originals.

        Args:
            crystal_ids: IDs of crystals to merge
            new_essence: Essence of the merged crystal
            confidence: Confidence in the merge
            quantum_value: Quantum value that selected this merge
            quantum_source: "quantum" or "classical"

        Returns:
            New crystal ID, or None on failure
        """
        import uuid as uuid_mod

        try:
            new_crystal_id = f"crystal_{uuid_mod.uuid4().hex[:12]}"

            async with self.driver.session() as session:
                # Get all source nodes from existing crystals
                result = await session.run("""
                    UNWIND $crystal_ids as cid
                    MATCH (n)-[:CRYSTALLIZED_INTO]->(c:Crystal {id: cid})
                    RETURN collect(DISTINCT n.id) as source_ids,
                           collect(DISTINCT c.facets) as all_facets
                """, crystal_ids=crystal_ids)

                record = await result.single()
                source_ids = record["source_ids"] if record else []
                all_facets = []
                if record and record["all_facets"]:
                    for facet_list in record["all_facets"]:
                        if facet_list:
                            all_facets.extend(facet_list)
                facets = list(set(all_facets))  # Deduplicate

                # Create the new merged crystal
                await session.run("""
                    CREATE (c:Crystal {
                        id: $id,
                        essence: $essence,
                        crystal_type: 'merged',
                        facets: $facets,
                        confidence: $confidence,
                        node_count: $node_count,
                        quantum_value: $quantum_value,
                        quantum_source: $quantum_source,
                        created_at: datetime(),
                        updated_at: datetime(),
                        state: 'active'
                    })
                """,
                    id=new_crystal_id,
                    essence=new_essence,
                    facets=facets,
                    confidence=confidence,
                    node_count=len(source_ids),
                    quantum_value=quantum_value,
                    quantum_source=quantum_source
                )

                # Link old crystals to new via MERGED_INTO
                await session.run("""
                    MATCH (new:Crystal {id: $new_id})
                    UNWIND $old_ids as old_id
                    MATCH (old:Crystal {id: old_id})
                    CREATE (old)-[:MERGED_INTO {timestamp: datetime()}]->(new)
                    SET old.state = 'archived'
                """, new_id=new_crystal_id, old_ids=crystal_ids)

                # Re-link all source nodes to new crystal
                await session.run("""
                    MATCH (new:Crystal {id: $new_id})
                    UNWIND $source_ids as sid
                    MATCH (n) WHERE n.id = sid
                    CREATE (n)-[:CRYSTALLIZED_INTO {
                        operation: 'merge',
                        timestamp: datetime(),
                        confidence: $confidence
                    }]->(new)
                """,
                    new_id=new_crystal_id,
                    source_ids=source_ids,
                    confidence=confidence
                )

                return new_crystal_id

        except Exception as e:
            print(f"Error merging crystals: {e}")
            return None

    async def update_node_state(
        self,
        node_id: str,
        state: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Update a node's state (active, crystallized, archived, forgotten).

        Args:
            node_id: ID of the node to update
            state: New state (must be in NODE_STATES)
            reason: Optional reason for the state change

        Returns:
            True if successful
        """
        if state not in NODE_STATES:
            print(f"Invalid state: {state}. Must be one of {NODE_STATES}")
            return False

        try:
            async with self.driver.session() as session:
                await session.run("""
                    MATCH (n) WHERE n.id = $id
                    SET n.state = $state,
                        n.state_changed_at = datetime(),
                        n.state_reason = $reason
                """, id=node_id, state=state, reason=reason)
                return True

        except Exception as e:
            print(f"Error updating node state: {e}")
            return False

    async def archive_node(self, node_id: str, reason: str = "crystallized") -> bool:
        """Archive a node (soft delete, excluded from retrieval)."""
        return await self.update_node_state(node_id, "archived", reason)

    async def forget_node(
        self,
        node_id: str,
        reason: str,
        hard_delete: bool = False
    ) -> bool:
        """
        Forget a node (mark as forgotten or hard delete).

        Args:
            node_id: ID of the node to forget
            reason: Reason for forgetting
            hard_delete: If True, permanently delete the node

        Returns:
            True if successful
        """
        try:
            async with self.driver.session() as session:
                if hard_delete:
                    await session.run("""
                        MATCH (n) WHERE n.id = $id
                        DETACH DELETE n
                    """, id=node_id)
                else:
                    await session.run("""
                        MATCH (n) WHERE n.id = $id
                        SET n.state = 'forgotten',
                            n.forgotten_at = datetime(),
                            n.forget_reason = $reason
                    """, id=node_id, reason=reason)
                return True

        except Exception as e:
            print(f"Error forgetting node: {e}")
            return False

    async def get_all_crystals(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all active Crystal nodes.

        Returns:
            List of crystal dictionaries with node counts
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (c:Crystal)
                    WHERE c.state = 'active' OR c.state IS NULL
                    OPTIONAL MATCH (n)-[:CRYSTALLIZED_INTO]->(c)
                    WITH c, count(n) as actual_count
                    RETURN
                        c.id as id,
                        c.essence as essence,
                        c.crystal_type as crystal_type,
                        c.facets as facets,
                        c.confidence as confidence,
                        c.node_count as node_count,
                        actual_count,
                        c.quantum_value as quantum_value,
                        c.quantum_source as quantum_source,
                        c.created_at as created_at,
                        c.updated_at as updated_at
                    ORDER BY c.created_at DESC
                    LIMIT $limit
                """, limit=limit)

                crystals = []
                async for record in result:
                    crystals.append({
                        "id": record["id"],
                        "essence": record["essence"],
                        "crystal_type": record["crystal_type"],
                        "facets": record["facets"] or [],
                        "confidence": record["confidence"],
                        "node_count": record["actual_count"] or record["node_count"] or 0,
                        "quantum_value": record["quantum_value"],
                        "quantum_source": record["quantum_source"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None,
                        "updated_at": str(record["updated_at"]) if record["updated_at"] else None
                    })

                return crystals

        except Exception as e:
            print(f"Error getting crystals: {e}")
            return []

    async def get_crystal_with_sources(self, crystal_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a crystal with all its source nodes.

        Returns:
            Crystal dict with 'sources' list of source node dicts
        """
        try:
            async with self.driver.session() as session:
                # Get crystal
                result = await session.run("""
                    MATCH (c:Crystal {id: $id})
                    RETURN c
                """, id=crystal_id)

                record = await result.single()
                if not record:
                    return None

                crystal = dict(record["c"])

                # Get source nodes
                sources_result = await session.run("""
                    MATCH (n)-[r:CRYSTALLIZED_INTO]->(c:Crystal {id: $id})
                    RETURN
                        n.id as id,
                        labels(n)[0] as type,
                        n.content as content,
                        n.essence as essence,
                        n.description as description,
                        r.operation as operation,
                        r.timestamp as crystallized_at
                    ORDER BY r.timestamp
                """, id=crystal_id)

                sources = []
                async for src in sources_result:
                    sources.append({
                        "id": src["id"],
                        "type": src["type"],
                        "content": src["content"] or src["essence"] or src["description"],
                        "operation": src["operation"],
                        "crystallized_at": str(src["crystallized_at"]) if src["crystallized_at"] else None
                    })

                crystal["sources"] = sources
                return crystal

        except Exception as e:
            print(f"Error getting crystal with sources: {e}")
            return None

    async def get_uncrystallized_nodes(
        self,
        limit: int = 50,
        min_age_hours: float = 0.5,
        exclude_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get nodes that are not yet part of any crystal.

        Args:
            limit: Maximum nodes to return
            min_age_hours: Minimum age in hours
            exclude_types: Node types to exclude (e.g., ['awakening', 'ego_seed'])

        Returns:
            List of node dicts
        """
        exclude_types = exclude_types or ['awakening', 'ego_seed', 'system', 'Mutation', 'SystemState']

        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (n)
                    WHERE NOT (n)-[:CRYSTALLIZED_INTO]->(:Crystal)
                    AND NOT n:Crystal
                    AND NOT n:SystemState
                    AND NOT n:Mutation
                    AND (n.state IS NULL OR n.state = 'active')
                    AND (n.timestamp IS NULL OR n.timestamp < datetime() - duration({hours: $min_age}))
                    AND (n.created_at IS NULL OR n.created_at < datetime() - duration({hours: $min_age}))
                    AND NOT coalesce(n.type, '') IN $exclude_types
                    RETURN
                        n.id as id,
                        labels(n)[0] as type,
                        n.content as content,
                        n.essence as essence,
                        n.description as description,
                        n.confidence as confidence,
                        n.timestamp as timestamp,
                        n.created_at as created_at
                    ORDER BY coalesce(n.timestamp, n.created_at) DESC
                    LIMIT $limit
                """, limit=limit, min_age=min_age_hours, exclude_types=exclude_types)

                nodes = []
                async for record in result:
                    nodes.append({
                        "id": record["id"],
                        "type": record["type"],
                        "content": record["content"] or record["essence"] or record["description"] or "",
                        "confidence": record["confidence"],
                        "timestamp": str(record["timestamp"] or record["created_at"]) if (record["timestamp"] or record["created_at"]) else None
                    })

                return nodes

        except Exception as e:
            print(f"Error getting uncrystallized nodes: {e}")
            return []

    async def get_crystallization_candidates(
        self,
        max_nodes: int = 30,
        max_crystals: int = 20,
        min_age_hours: float = 0.5
    ) -> Dict[str, Any]:
        """
        Get both uncrystallized nodes and existing crystals for evaluation.

        Returns:
            {"loose_nodes": [...], "crystals": [...]}
        """
        loose_nodes = await self.get_uncrystallized_nodes(
            limit=max_nodes,
            min_age_hours=min_age_hours
        )
        crystals = await self.get_all_crystals(limit=max_crystals)

        return {
            "loose_nodes": loose_nodes,
            "crystals": crystals
        }

    async def count_by_state(self, state: str) -> int:
        """Count nodes in a given state."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (n)
                    WHERE n.state = $state
                    RETURN count(n) as count
                """, state=state)

                record = await result.single()
                return record["count"] if record else 0

        except Exception as e:
            print(f"Error counting by state: {e}")
            return 0

    async def count_crystals(self) -> int:
        """Count active Crystal nodes."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (c:Crystal)
                    WHERE c.state = 'active' OR c.state IS NULL
                    RETURN count(c) as count
                """)

                record = await result.single()
                return record["count"] if record else 0

        except Exception as e:
            print(f"Error counting crystals: {e}")
            return 0

    async def get_crystal_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive crystallization statistics.

        Returns:
            {
                "total_nodes": int,
                "active_nodes": int,
                "crystallized_nodes": int,
                "archived_nodes": int,
                "forgotten_nodes": int,
                "crystal_count": int,
                "crystallization_ratio": float
            }
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (n)
                    WHERE NOT n:SystemState
                    WITH count(n) as total
                    OPTIONAL MATCH (active) WHERE (active.state IS NULL OR active.state = 'active') AND NOT active:SystemState
                    WITH total, count(active) as active_count
                    OPTIONAL MATCH (cryst) WHERE cryst.state = 'crystallized'
                    WITH total, active_count, count(cryst) as cryst_count
                    OPTIONAL MATCH (arch) WHERE arch.state = 'archived'
                    WITH total, active_count, cryst_count, count(arch) as arch_count
                    OPTIONAL MATCH (forg) WHERE forg.state = 'forgotten'
                    WITH total, active_count, cryst_count, arch_count, count(forg) as forg_count
                    OPTIONAL MATCH (c:Crystal) WHERE c.state = 'active' OR c.state IS NULL
                    RETURN total, active_count, cryst_count, arch_count, forg_count, count(c) as crystal_count
                """)

                record = await result.single()
                if not record:
                    return {
                        "total_nodes": 0,
                        "active_nodes": 0,
                        "crystallized_nodes": 0,
                        "archived_nodes": 0,
                        "forgotten_nodes": 0,
                        "crystal_count": 0,
                        "crystallization_ratio": 0.0
                    }

                total = record["total"] or 0
                cryst = record["cryst_count"] or 0

                return {
                    "total_nodes": total,
                    "active_nodes": record["active_count"] or 0,
                    "crystallized_nodes": cryst,
                    "archived_nodes": record["arch_count"] or 0,
                    "forgotten_nodes": record["forg_count"] or 0,
                    "crystal_count": record["crystal_count"] or 0,
                    "crystallization_ratio": round(cryst / total, 3) if total > 0 else 0.0
                }

        except Exception as e:
            print(f"Error getting crystal stats: {e}")
            return {
                "total_nodes": 0,
                "active_nodes": 0,
                "crystallized_nodes": 0,
                "archived_nodes": 0,
                "forgotten_nodes": 0,
                "crystal_count": 0,
                "crystallization_ratio": 0.0,
                "error": str(e)
            }

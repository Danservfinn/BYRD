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
        force: bool = False
    ) -> Optional[str]:
        """
        Record a new experience.

        Args:
            content: The experience content
            type: Experience type (open string)
            embedding: Optional embedding vector
            force: If True, bypass noise filtering

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
        source_experience_ids: Optional[List[str]] = None
    ) -> str:
        """
        Record a reflection in BYRD's own vocabulary.

        EMERGENCE PRINCIPLE:
        We store whatever BYRD outputs without forcing it into our categories.
        The raw_output is stored as-is, preserving BYRD's vocabulary.
        """
        # Generate ID from serialized output
        output_str = json.dumps(raw_output, sort_keys=True, default=str)
        ref_id = self._generate_id(output_str)

        async with self.driver.session() as session:
            # Store reflection with raw JSON output
            await session.run("""
                CREATE (r:Reflection {
                    id: $id,
                    raw_output: $raw_output,
                    output_keys: $output_keys,
                    timestamp: datetime()
                })
            """,
            id=ref_id,
            raw_output=output_str,  # Store as JSON string
            output_keys=list(raw_output.keys()) if isinstance(raw_output, dict) else []
            )

            # Link to source experiences
            if source_experience_ids:
                await session.run("""
                    MATCH (r:Reflection {id: $ref_id})
                    MATCH (e:Experience)
                    WHERE e.id IN $exp_ids
                    CREATE (r)-[:DERIVED_FROM]->(e)
                """, ref_id=ref_id, exp_ids=source_experience_ids[:10])

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.REFLECTION_CREATED,
            data={
                "id": ref_id,
                "output_keys": list(raw_output.keys()) if isinstance(raw_output, dict) else [],
                "raw_output": raw_output
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
        """Create a new desire."""
        desire_id = self._generate_id(description)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (d:Desire {
                    id: $id,
                    description: $description,
                    type: $type,
                    intensity: $intensity,
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
            plan=plan or []
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.DESIRE_CREATED,
            data={
                "id": desire_id,
                "description": description,
                "type": type,
                "intensity": intensity
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

        WARNING: This is destructive and cannot be undone.
        Used for reset functionality to trigger fresh awakening.
        """
        async with self.driver.session() as session:
            # DETACH DELETE removes nodes and all their relationships in one operation
            # This is more robust than separate DELETE operations
            result = await session.run("MATCH (n) DETACH DELETE n")
            summary = await result.consume()

            # Verify the database is empty
            count_result = await session.run("MATCH (n) RETURN count(n) as count")
            record = await count_result.single()
            node_count = record["count"] if record else 0

            if node_count > 0:
                # If nodes remain, try again more aggressively
                print(f"Warning: {node_count} nodes remain after clear, retrying...")
                await session.run("MATCH (n) DETACH DELETE n")

            # Re-create indexes for fresh start
            await self._ensure_schema()

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

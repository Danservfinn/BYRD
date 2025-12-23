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
    
    async def record_experience(
        self,
        content: str,
        type: str,
        embedding: Optional[List[float]] = None
    ) -> str:
        """Record a new experience."""
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
                "content": content[:200],
                "type": type
            }
        ))

        return exp_id
    
    async def get_recent_experiences(
        self, 
        limit: int = 50,
        type: Optional[str] = None
    ) -> List[Dict]:
        """Get recent experiences, optionally filtered by type."""
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
                "output_keys": list(raw_output.keys()) if isinstance(raw_output, dict) else []
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
                "content": content[:200],
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
                "description": description[:200],
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
                "description": description[:200],
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
            # Delete all relationships first, then all nodes
            await session.run("MATCH ()-[r]-() DELETE r")
            await session.run("MATCH (n) DELETE n")

            # Re-create indexes
            await self._ensure_schema()

        print("Memory cleared: all nodes and relationships deleted")

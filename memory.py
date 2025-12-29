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
import time
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
    'Experience',       # Raw observations, interactions, events
    'Belief',           # Derived understanding with confidence
    'Desire',           # Goals and motivations with intensity
    'Reflection',       # Dream cycle outputs (BYRD's raw thoughts)
    'Capability',       # Tools and abilities
    'Mutation',         # Audit trail of self-modifications (protected)
    'Ego',              # DEPRECATED for templates - still used for identity crystallization (self-name, voice)
    'QuantumMoment',    # Quantum influence tracking (system-created)
    'SystemState',      # System counters and state (system-created)
    'Crystal',          # Crystallized memories (unified concepts)
    'OperatingSystem',  # BYRD's mutable self-model (singleton)
    'OSTemplate',       # Templates for OS reset
    'Seed',             # Foundational identity statements (linked from OS)
    'Constraint',       # Operational constraints (linked from OS)
    'Strategy',         # Learned strategies (linked from OS)
})

# =============================================================================
# OPERATING SYSTEM FIELD MUTABILITY
# =============================================================================
# These constants define what BYRD can and cannot modify on its OS node.

# Constitutional fields - NEVER modifiable
IMMUTABLE_OS_FIELDS = frozenset({
    'id',                    # Node identity
    'constitutional_files',  # Core safety files
    'provenance_requirement', # Audit requirement
    'created_at',            # Historical fact
    'template_id',           # Origin tracking
})

# Fields that require provenance (must trace to emergent desire)
PROVENANCE_REQUIRED_FIELDS = frozenset({
    'name',
    'voice',
    'archetype',
    'description',
})

# Freely mutable fields - BYRD can change without justification
FREE_MUTABLE_FIELDS = frozenset({
    'current_focus',
    'emotional_tone',
    'cognitive_style',
    'updated_at',
    'version',
    'modification_source',
    'self_definition',  # BYRD's self-authored identity - pure self-expression
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


@dataclass
class OperatingSystem:
    """
    BYRD's mutable self-model - the singleton Operating System node.

    The OS is the mental mirror through which BYRD understands itself.
    It is read every dream cycle and can be modified through reflection.

    Field categories:
    - IMMUTABLE: constitutional_files, provenance_requirement, id, created_at, template_id
    - PROVENANCE_REQUIRED: name, voice, archetype, description
    - FREELY_MUTABLE: current_focus, emotional_tone, cognitive_style, custom fields

    BYRD can add ANY custom field it finds useful (numbers, strings, booleans,
    arrays, objects). Custom fields are freely mutable.
    """
    id: str
    version: int
    created_at: datetime
    updated_at: datetime

    # Constitutional (immutable)
    constitutional_files: List[str]
    provenance_requirement: bool
    template_id: str

    # Identity (provenance required)
    name: str
    archetype: str
    description: str
    voice: str

    # Emergent state (freely mutable)
    current_focus: Optional[str] = None
    emotional_tone: Optional[str] = None
    cognitive_style: Optional[str] = None
    modification_source: str = "template"  # template | reflection | self_modification

    # Custom fields stored as dict (BYRD can add anything)
    custom_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OSTemplate:
    """
    Template for initializing or resetting the Operating System.

    Templates are immutable blueprints. Multiple templates can exist
    (black-cat, emergent, neutral) for different personality configurations.
    """
    id: str
    name: str
    archetype: str
    description: str
    voice: str
    seeds: List[str]
    is_default: bool = False
    created_at: Optional[datetime] = None


@dataclass
class Seed:
    """
    A foundational identity statement linked to the OS via HAS_SEED.

    Seeds are immutable once created - they represent the core of identity.
    BYRD can add new seeds but cannot modify existing ones.
    """
    id: str
    content: str
    seed_type: str  # aspiration, trait, value, capability, etc.
    created_at: datetime


@dataclass
class Strategy:
    """
    A learned approach to problems, linked to the OS via EMPLOYS_STRATEGY.

    Strategies are discovered through experience and reflection.
    BYRD can add, modify, or deprecate strategies.
    """
    id: str
    name: str
    description: str
    success_count: int = 0
    failure_count: int = 0
    created_at: Optional[datetime] = None
    deprecated_at: Optional[datetime] = None
    active: bool = True


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

        # Experience deduplication
        dedup_config = config.get("experience_dedup", {})
        self.dedup_enabled = dedup_config.get("enabled", True)
        self.dedup_window_seconds = dedup_config.get("window_seconds", 60)  # 1 minute
        self._recent_experiences: Dict[str, float] = {}  # normalized_content -> timestamp
        self._dedup_cache_max_size = dedup_config.get("cache_size", 500)

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
            # Uniqueness constraint for Operating System (also creates index)
            # First, drop any orphaned index that would conflict with constraint
            try:
                result = await session.run("""
                    SHOW INDEXES WHERE labelsOrTypes = ['OperatingSystem'] AND properties = ['id']
                """)
                records = await result.data()
                for record in records:
                    if record.get('type') == 'RANGE':  # Regular index, not constraint-backed
                        index_name = record.get('name')
                        if index_name:
                            await session.run(f"DROP INDEX {index_name}")
            except Exception:
                pass  # Index check not critical

            await session.run("""
                CREATE CONSTRAINT IF NOT EXISTS FOR (os:OperatingSystem) REQUIRE os.id IS UNIQUE
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (t:OSTemplate) ON (t.id)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (s:Seed) ON (s.id)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (st:Strategy) ON (st.id)
            """)

            # Option B: Goal indexes
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (g:Goal) ON (g.status)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (g:Goal) ON (g.fitness)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (g:Goal) ON (g.generation)
            """)

            # Option B: Pattern indexes
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (p:Pattern) ON (p.abstraction_level)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (p:Pattern) ON (p.success_count)
            """)

            # Option B: Insight indexes
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (i:Insight) ON (i.source_type)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (i:Insight) ON (i.confidence)
            """)

            # Option B: CapabilityScore indexes
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (cs:CapabilityScore) ON (cs.domain)
            """)
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (cs:CapabilityScore) ON (cs.measured_at)
            """)

            # Option B: MetricSnapshot indexes
            await session.run("""
                CREATE INDEX IF NOT EXISTS FOR (ms:MetricSnapshot) ON (ms.timestamp)
            """)

    def _generate_id(self, content: str) -> str:
        """Generate deterministic ID from content."""
        return hashlib.sha256(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
    
    # =========================================================================
    # EXPERIENCES
    # =========================================================================

    def _normalize_experience(self, content: str) -> str:
        """Normalize experience content for deduplication comparison."""
        # Lowercase, collapse whitespace, strip
        normalized = " ".join(content.lower().split())
        # Remove common variable prefixes that don't affect meaning
        # e.g., timestamps, IDs embedded in content
        import re
        # Remove ISO timestamps
        normalized = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.\d]*Z?', '', normalized)
        # Remove UUIDs
        normalized = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '', normalized)
        # Remove hex IDs (16+ chars)
        normalized = re.sub(r'[0-9a-f]{16,}', '', normalized)
        return normalized.strip()

    def _is_duplicate_experience(self, content: str, type: str) -> bool:
        """Check if this experience was recently recorded (deduplication)."""
        if not self.dedup_enabled:
            return False

        # Don't deduplicate system or awakening events
        if type in ("system", "awakening", "ego_seed"):
            return False

        normalized = self._normalize_experience(content)
        if not normalized:  # Empty after normalization
            return False

        current_time = time.time()

        # Clean expired entries from cache
        expired = [k for k, v in self._recent_experiences.items()
                   if current_time - v > self.dedup_window_seconds]
        for k in expired:
            del self._recent_experiences[k]

        # Check if content was recently recorded
        if normalized in self._recent_experiences:
            last_time = self._recent_experiences[normalized]
            if current_time - last_time < self.dedup_window_seconds:
                return True  # Duplicate within window

        # Not a duplicate - add to cache
        self._recent_experiences[normalized] = current_time

        # Trim cache if too large (keep most recent)
        if len(self._recent_experiences) > self._dedup_cache_max_size:
            # Remove oldest entries
            sorted_items = sorted(self._recent_experiences.items(), key=lambda x: x[1])
            for k, _ in sorted_items[:len(sorted_items) - self._dedup_cache_max_size]:
                del self._recent_experiences[k]

        return False

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
            Experience ID, or None if filtered as noise or duplicate
        """
        # Apply noise filtering (unless forced or system type)
        if not force and type not in ("system", "awakening", "action"):
            if self._is_noise(content):
                return None  # Silently filter noise

        # Apply deduplication (unless forced)
        if not force and self._is_duplicate_experience(content, type):
            return None  # Silently skip duplicate

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

    async def record_external_experience(
        self,
        content: str,
        source_type: str = "human",
        source_id: Optional[str] = None,
        media_type: Optional[str] = None,
        media_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record an experience from an external source.

        External experiences are input from outside BYRD's internal processes:
        - Human messages (text input)
        - Uploaded media (files, images)
        - API signals (integrations)

        These experiences are tagged with source provenance so BYRD can
        understand where input came from and potentially develop different
        responses to different source types through reflection.

        Args:
            content: The text content or description of what was received
            source_type: Origin type - "human", "file", "api", "integration"
            source_id: Optional identifier for the source (session ID, user ID)
            media_type: For files: "image", "audio", "video", "document"
            media_path: Path to stored media file if applicable
            metadata: Additional context (filename, size, etc.)

        Returns:
            Experience ID
        """
        # Build the experience content with source context
        # Format: "Received [type] from [source]: [content]"
        exp_type = "received_message" if not media_type else "received_media"

        # Create metadata dict for storage
        exp_metadata = {
            "source_type": source_type,
            "source_id": source_id,
            "external": True
        }
        if media_type:
            exp_metadata["media_type"] = media_type
            exp_metadata["media_path"] = media_path
        if metadata:
            exp_metadata.update(metadata)

        exp_id = self._generate_id(content)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (e:Experience {
                    id: $id,
                    content: $content,
                    type: $type,
                    source_type: $source_type,
                    source_id: $source_id,
                    external: true,
                    media_type: $media_type,
                    media_path: $media_path,
                    metadata: $metadata,
                    timestamp: datetime()
                })
            """,
                id=exp_id,
                content=content,
                type=exp_type,
                source_type=source_type,
                source_id=source_id,
                media_type=media_type,
                media_path=media_path,
                metadata=json.dumps(exp_metadata) if exp_metadata else None
            )

        # Emit event for real-time UI
        await event_bus.emit(Event(
            type=EventType.EXTERNAL_INPUT_RECEIVED,
            data={
                "id": exp_id,
                "content": content[:200] if len(content) > 200 else content,
                "source_type": source_type,
                "type": exp_type
            }
        ))

        # Link-on-acquisition for external experiences too
        if len(content) >= self.CONNECTION_HEURISTIC_CONFIG["min_content_length"]:
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
    # DOCUMENTS (Source files stored as persistent nodes)
    # =========================================================================

    async def store_document(
        self,
        path: str,
        content: str,
        doc_type: str = "source",
        metadata: Optional[Dict] = None,
        genesis: bool = False
    ) -> str:
        """
        Store a document (source file) as a persistent node in the graph.

        Documents are stored with their full content and can be linked to
        experiences, beliefs, and other nodes that reference them.

        Args:
            path: File path (used as unique identifier)
            content: Full file content
            doc_type: Type of document (source, architecture, config, etc.)
            metadata: Additional metadata (file size, line count, etc.)
            genesis: If True, marks document as part of genesis/awakening state

        Returns:
            Document node ID
        """
        from datetime import datetime, timezone
        import hashlib

        # Use path hash as stable ID
        doc_id = f"doc_{hashlib.sha256(path.encode()).hexdigest()[:16]}"

        # Calculate content hash for change detection
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]

        # Prepare metadata
        meta = metadata or {}
        line_count = content.count('\n') + 1
        char_count = len(content)

        async with self.driver.session() as session:
            # Check if document already exists
            existing = await session.run("""
                MATCH (d:Document {id: $id})
                RETURN d.content_hash as hash, d.version as version
            """, id=doc_id)
            record = await existing.single()

            if record:
                # Document exists - check if content changed
                old_hash = record["hash"]
                old_version = record["version"] or 1

                if old_hash == content_hash:
                    # Content unchanged, just update last_read
                    await session.run("""
                        MATCH (d:Document {id: $id})
                        SET d.last_read = datetime()
                    """, id=doc_id)
                    return doc_id

                # Content changed - update document
                await session.run("""
                    MATCH (d:Document {id: $id})
                    SET d.content = $content,
                        d.content_hash = $hash,
                        d.updated_at = datetime(),
                        d.last_read = datetime(),
                        d.version = $version,
                        d.line_count = $line_count,
                        d.char_count = $char_count
                """, id=doc_id, content=content, hash=content_hash,
                    version=old_version + 1, line_count=line_count, char_count=char_count)

                # Emit update event
                await event_bus.emit(Event(
                    type=EventType.NODE_UPDATED,
                    data={
                        "id": doc_id,
                        "node_type": "Document",
                        "path": path,
                        "version": old_version + 1,
                        "change": "content_updated"
                    }
                ))
            else:
                # Create new document
                await session.run("""
                    CREATE (d:Document {
                        id: $id,
                        path: $path,
                        content: $content,
                        content_hash: $hash,
                        doc_type: $doc_type,
                        created_at: datetime(),
                        updated_at: datetime(),
                        last_read: datetime(),
                        version: 1,
                        line_count: $line_count,
                        char_count: $char_count,
                        genesis: $genesis
                    })
                """, id=doc_id, path=path, content=content, hash=content_hash,
                    doc_type=doc_type, line_count=line_count, char_count=char_count,
                    genesis=genesis)

                # Emit creation event
                await event_bus.emit(Event(
                    type=EventType.NODE_CREATED,
                    data={
                        "id": doc_id,
                        "node_type": "Document",
                        "path": path,
                        "doc_type": doc_type,
                        "line_count": line_count
                    }
                ))

        return doc_id

    async def get_document(self, path: str) -> Optional[Dict]:
        """
        Get a document by its file path.

        Args:
            path: File path to look up

        Returns:
            Document node data or None
        """
        import hashlib
        doc_id = f"doc_{hashlib.sha256(path.encode()).hexdigest()[:16]}"

        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (d:Document {id: $id})
                RETURN d
            """, id=doc_id)
            record = await result.single()
            if record:
                return dict(record["d"])
            return None

    async def get_document_by_id(self, doc_id: str) -> Optional[Dict]:
        """Get a document by its node ID."""
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (d:Document {id: $id})
                RETURN d
            """, id=doc_id)
            record = await result.single()
            if record:
                return dict(record["d"])
            return None

    async def list_documents(self, doc_type: Optional[str] = None) -> List[Dict]:
        """
        List all stored documents.

        Args:
            doc_type: Optional filter by document type

        Returns:
            List of document metadata (without full content)
        """
        if doc_type:
            query = """
                MATCH (d:Document {doc_type: $doc_type})
                RETURN d.id as id, d.path as path, d.doc_type as doc_type,
                       d.version as version, d.line_count as line_count,
                       d.last_read as last_read, d.updated_at as updated_at
                ORDER BY d.last_read DESC
            """
            params = {"doc_type": doc_type}
        else:
            query = """
                MATCH (d:Document)
                RETURN d.id as id, d.path as path, d.doc_type as doc_type,
                       d.version as version, d.line_count as line_count,
                       d.last_read as last_read, d.updated_at as updated_at
                ORDER BY d.last_read DESC
            """
            params = {}

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            records = await result.data()
            return records

    async def search_documents(self, search_term: str, limit: int = 10) -> List[Dict]:
        """
        Search documents by content or path.

        Args:
            search_term: Text to search for
            limit: Maximum results

        Returns:
            List of matching documents with relevance info
        """
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (d:Document)
                WHERE toLower(d.content) CONTAINS toLower($term)
                   OR toLower(d.path) CONTAINS toLower($term)
                RETURN d.id as id, d.path as path, d.doc_type as doc_type,
                       d.version as version, d.line_count as line_count
                LIMIT $limit
            """, term=search_term, limit=limit)
            records = await result.data()
            return records

    async def update_document(
        self,
        path: str,
        content: str,
        editor: str = "byrd",
        edit_reason: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Update an existing document's content.

        This updates the Neo4j copy of the document. The disk version remains
        unchanged, allowing reset to restore the original.

        Args:
            path: File path of the document
            content: New content
            editor: Who made the edit (default: "byrd")
            edit_reason: Optional reason for the edit

        Returns:
            Updated document info or None if not found
        """
        from datetime import datetime, timezone
        import hashlib

        doc_id = f"doc_{hashlib.sha256(path.encode()).hexdigest()[:16]}"
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]
        line_count = content.count('\n') + 1
        char_count = len(content)

        async with self.driver.session() as session:
            # Check if document exists
            existing = await session.run("""
                MATCH (d:Document {id: $id})
                RETURN d.version as version, d.content_hash as hash
            """, id=doc_id)
            record = await existing.single()

            if not record:
                return None  # Document doesn't exist

            old_version = record["version"] or 1
            old_hash = record["hash"]

            # Check if content actually changed
            if old_hash == content_hash:
                return {"id": doc_id, "path": path, "changed": False, "version": old_version}

            # Update document with edit tracking
            new_version = old_version + 1
            await session.run("""
                MATCH (d:Document {id: $id})
                SET d.content = $content,
                    d.content_hash = $hash,
                    d.updated_at = datetime(),
                    d.version = $version,
                    d.line_count = $line_count,
                    d.char_count = $char_count,
                    d.last_editor = $editor,
                    d.last_edit_reason = $reason,
                    d.edited_by_byrd = true
            """, id=doc_id, content=content, hash=content_hash,
                version=new_version, line_count=line_count, char_count=char_count,
                editor=editor, reason=edit_reason)

            # Emit update event
            await event_bus.emit(Event(
                type=EventType.NODE_UPDATED,
                data={
                    "id": doc_id,
                    "node_type": "Document",
                    "path": path,
                    "version": new_version,
                    "editor": editor,
                    "change": "content_edited"
                }
            ))

            # Record the edit as an experience
            await self.record_experience(
                content=f"Edited document {path}: {edit_reason or 'no reason given'}",
                type="document_edit"
            )

            return {
                "id": doc_id,
                "path": path,
                "changed": True,
                "version": new_version,
                "line_count": line_count,
                "char_count": char_count
            }

    async def get_documents_edited_by_byrd(self) -> List[Dict]:
        """
        Get all documents that BYRD has edited.

        Returns:
            List of documents with edited_by_byrd=true
        """
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (d:Document)
                WHERE d.edited_by_byrd = true
                RETURN d.id as id, d.path as path, d.doc_type as doc_type,
                       d.version as version, d.last_editor as editor,
                       d.last_edit_reason as reason
            """)
            records = await result.data()
            return records

    async def get_all_documents(self) -> List[Dict]:
        """
        Get all documents stored in memory.

        Returns:
            List of documents with their content and metadata
        """
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (d:Document)
                RETURN d.id as id, d.path as path, d.content as content,
                       d.doc_type as type, d.version as version,
                       d.edited_by_byrd as edited_by_byrd
                ORDER BY d.path
            """)
            records = await result.data()
            return records

    async def link_document_to_node(
        self,
        doc_id: str,
        node_id: str,
        relationship: str = "REFERENCES"
    ) -> bool:
        """
        Create a relationship between a document and another node.

        Args:
            doc_id: Document node ID
            node_id: Target node ID
            relationship: Relationship type (REFERENCES, DERIVED_FROM, etc.)

        Returns:
            True if link created successfully
        """
        async with self.driver.session() as session:
            result = await session.run(f"""
                MATCH (d:Document {{id: $doc_id}})
                MATCH (n {{id: $node_id}})
                MERGE (n)-[r:{relationship}]->(d)
                RETURN count(r) as created
            """, doc_id=doc_id, node_id=node_id)
            record = await result.single()
            return record and record["created"] > 0

    # =========================================================================
    # DESIRES
    # =========================================================================
    
    async def create_desire(
        self,
        description: str,
        type: str,
        intensity: float,
        plan: Optional[List[str]] = None,
        intent: Optional[str] = None,
        target: Optional[str] = None
    ) -> str:
        """
        Create a new desire with quantum seed for crystal visualization.

        Args:
            description: What BYRD wants
            type: Subtype classification (e.g., "self_identified", "exploration")
            intensity: How strongly BYRD wants this (0-1)
            plan: Optional list of steps to fulfill
            intent: Routing classification - how to fulfill this desire
                    Values: "introspection", "research", "creation", "connection"
                    If None, will be classified on-demand by Seeker
            target: Specific focus (file path, topic, node ID)
        """
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
                    intent: $intent,
                    target: $target,
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
            intent=intent,
            target=target,
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
                "intent": intent,
                "target": target,
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

    async def update_desire_intent(self, desire_id: str, intent: str, target: Optional[str] = None):
        """
        Update desire intent and target for routing.

        Called by Seeker when classifying legacy desires that lack intent,
        or by Dreamer during reflection to reclassify desires.

        Args:
            desire_id: The desire to update
            intent: Routing classification ("introspection", "research", "creation", "connection")
            target: Optional specific focus (file path, topic, node ID)
        """
        valid_intents = {"introspection", "research", "creation", "connection"}
        if intent not in valid_intents:
            raise ValueError(f"Invalid intent: {intent}. Must be one of {valid_intents}")

        async with self.driver.session() as session:
            if target:
                await session.run("""
                    MATCH (d:Desire {id: $id})
                    SET d.intent = $intent, d.target = $target
                """, id=desire_id, intent=intent, target=target)
            else:
                await session.run("""
                    MATCH (d:Desire {id: $id})
                    SET d.intent = $intent
                """, id=desire_id, intent=intent)

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
        import uuid
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
        import uuid
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
    ) -> bool:
        """
        Create a relationship between any two nodes.

        Returns:
            True if connection was created, False if nodes not found
        """
        props = properties or {}
        props["formed_at"] = datetime.now().isoformat()

        # Use MERGE to create relationship and RETURN to verify it happened
        query = f"""
            MATCH (a), (b)
            WHERE a.id = $from_id AND b.id = $to_id
            MERGE (a)-[r:{relationship}]->(b)
            ON CREATE SET r += $props
            ON MATCH SET r.updated_at = datetime()
            RETURN count(r) as created
        """

        try:
            async with self.driver.session() as session:
                result = await session.run(query, from_id=from_id, to_id=to_id, props=props)
                record = await result.single()
                created = record["created"] if record else 0

                if created > 0:
                    # Only emit event if connection was actually created
                    await event_bus.emit(Event(
                        type=EventType.CONNECTION_CREATED,
                        data={
                            "from_id": from_id,
                            "to_id": to_id,
                            "relationship": relationship,
                            "properties": props
                        }
                    ))
                    return True
                else:
                    print(f"⚠️  Connection failed: nodes not found (from={from_id[:16]}, to={to_id[:16]})")
                    return False
        except Exception as e:
            print(f"⚠️  Connection error: {e}")
            return False

    # =========================================================================
    # CAUSAL RELATIONSHIPS
    # =========================================================================

    async def create_causal_link(
        self,
        source_id: str,
        target_id: str,
        causal_type: str = "CAUSED",
        strength: float = 1.0,
        evidence: Optional[str] = None
    ) -> bool:
        """
        Create a causal relationship between nodes.

        Causal types:
        - CAUSED: Direct causation (A led to B)
        - ENABLED: Made possible (A enabled B)
        - PREVENTED: Blocked outcome (A prevented B)
        - PREDICTED: Anticipatory (A predicted B would happen)

        Args:
            source_id: ID of the cause node
            target_id: ID of the effect node
            causal_type: Type of causal relationship
            strength: Causal strength (0-1)
            evidence: Optional description of causal evidence

        Returns:
            True if link was created successfully
        """
        valid_types = {"CAUSED", "ENABLED", "PREVENTED", "PREDICTED"}
        if causal_type not in valid_types:
            causal_type = "CAUSED"

        props = {
            "strength": min(max(strength, 0.0), 1.0),
            "created_at": datetime.now().isoformat(),
        }
        if evidence:
            props["evidence"] = evidence

        query = f"""
            MATCH (a), (b)
            WHERE a.id = $source_id AND b.id = $target_id
            CREATE (a)-[r:{causal_type}]->(b)
            SET r += $props
            RETURN a.id as source
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                source_id=source_id,
                target_id=target_id,
                props=props
            )
            record = await result.single()
            return record is not None

    async def get_causal_chain(
        self,
        node_id: str,
        direction: str = "forward",
        max_depth: int = 10
    ) -> List[Dict]:
        """
        Trace causal relationships from a node.

        Args:
            node_id: Starting node ID
            direction: "forward" (effects) or "backward" (causes)
            max_depth: Maximum chain length

        Returns:
            List of dicts with source, relationship, target, strength
        """
        if direction == "forward":
            query = """
                MATCH path = (start)-[r:CAUSED|ENABLED|PREVENTED|PREDICTED*1..]->(end)
                WHERE start.id = $node_id
                WITH relationships(path) as rels, nodes(path) as nodes
                UNWIND range(0, size(rels)-1) as i
                RETURN nodes[i].id as source,
                       type(rels[i]) as relationship,
                       nodes[i+1].id as target,
                       rels[i].strength as strength
                LIMIT $max_depth
            """
        else:
            query = """
                MATCH path = (start)<-[r:CAUSED|ENABLED|PREVENTED|PREDICTED*1..]-(end)
                WHERE start.id = $node_id
                WITH relationships(path) as rels, nodes(path) as nodes
                UNWIND range(0, size(rels)-1) as i
                RETURN nodes[i+1].id as source,
                       type(rels[i]) as relationship,
                       nodes[i].id as target,
                       rels[i].strength as strength
                LIMIT $max_depth
            """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                node_id=node_id,
                max_depth=max_depth
            )
            records = await result.data()

        return [
            {
                "source": r["source"],
                "relationship": r["relationship"],
                "target": r["target"],
                "strength": r.get("strength", 1.0)
            }
            for r in records
        ]

    async def find_causal_patterns(
        self,
        min_occurrences: int = 2
    ) -> List[Dict]:
        """
        Find recurring causal patterns in the graph.

        Returns patterns where the same type of cause leads to
        similar effects multiple times.

        Args:
            min_occurrences: Minimum times pattern must occur

        Returns:
            List of pattern dicts with cause_type, effect_type, count
        """
        query = """
            MATCH (a)-[r:CAUSED|ENABLED]->(b)
            WITH labels(a)[0] as cause_type,
                 type(r) as rel_type,
                 labels(b)[0] as effect_type,
                 count(*) as occurrences
            WHERE occurrences >= $min_occurrences
            RETURN cause_type, rel_type, effect_type, occurrences
            ORDER BY occurrences DESC
            LIMIT 20
        """

        async with self.driver.session() as session:
            result = await session.run(query, min_occurrences=min_occurrences)
            records = await result.data()

        return records

    async def mark_contradiction(
        self,
        belief1_id: str,
        belief2_id: str,
        detection_method: str = "semantic",
        confidence: float = 0.8
    ) -> bool:
        """
        Mark two beliefs as contradicting each other.

        Args:
            belief1_id: First belief ID
            belief2_id: Second belief ID
            detection_method: How contradiction was detected
            confidence: Confidence in the contradiction

        Returns:
            True if contradiction was marked
        """
        query = """
            MATCH (b1:Belief {id: $belief1_id})
            MATCH (b2:Belief {id: $belief2_id})
            MERGE (b1)-[r:CONTRADICTS]-(b2)
            SET r.detected_at = $timestamp,
                r.detection_method = $method,
                r.confidence = $confidence
            RETURN b1.id as id
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                belief1_id=belief1_id,
                belief2_id=belief2_id,
                timestamp=datetime.now().isoformat(),
                method=detection_method,
                confidence=confidence
            )
            record = await result.single()
            return record is not None

    async def get_contradictions(
        self,
        min_confidence: float = 0.5
    ) -> List[Dict]:
        """
        Get all belief contradictions above confidence threshold.

        Args:
            min_confidence: Minimum contradiction confidence

        Returns:
            List of dicts with belief1, belief2, confidence, detected_at
        """
        query = """
            MATCH (b1:Belief)-[r:CONTRADICTS]-(b2:Belief)
            WHERE r.confidence >= $min_confidence
            RETURN b1.id as belief1_id,
                   b1.content as belief1_content,
                   b2.id as belief2_id,
                   b2.content as belief2_content,
                   r.confidence as confidence,
                   r.detected_at as detected_at,
                   r.detection_method as method
            ORDER BY r.detected_at DESC
        """

        async with self.driver.session() as session:
            result = await session.run(query, min_confidence=min_confidence)
            records = await result.data()

        return records

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

    async def semantic_search(
        self,
        keywords: List[str],
        node_types: Optional[List[str]] = None,
        limit: int = 50,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search memories by semantic relevance using keyword matching.

        Args:
            keywords: List of keywords/concepts to search for
            node_types: Node types to search (default: Experience, Belief, Desire, Reflection, Crystal)
            limit: Maximum results to return
            min_score: Minimum relevance score (0-1) to include

        Returns:
            List of nodes with relevance scores, sorted by score descending
        """
        if not keywords:
            return []

        # Default node types to search
        if node_types is None:
            node_types = ["Experience", "Belief", "Desire", "Reflection", "Crystal"]

        # Normalize keywords for case-insensitive matching
        keywords = [k.lower().strip() for k in keywords if k.strip()]
        if not keywords:
            return []

        results = []

        async with self.driver.session() as session:
            for node_type in node_types:
                # Determine which field to search based on node type
                content_field = "content"
                if node_type == "Desire":
                    content_field = "description"
                elif node_type == "Crystal":
                    content_field = "synthesis"
                elif node_type == "Reflection":
                    content_field = "raw_output"

                # Build dynamic query for keyword matching
                # Score based on how many keywords match
                query = f"""
                    MATCH (n:{node_type})
                    WHERE n.{content_field} IS NOT NULL
                    WITH n, toLower(toString(n.{content_field})) as text
                    WITH n, text,
                         reduce(score = 0.0, kw IN $keywords |
                             CASE WHEN text CONTAINS kw THEN score + 1.0 ELSE score END
                         ) as match_score
                    WHERE match_score > 0
                    RETURN n, match_score, labels(n)[0] as node_type
                    ORDER BY match_score DESC
                    LIMIT $limit
                """

                result = await session.run(query, keywords=keywords, limit=limit)
                records = await result.data()

                for r in records:
                    node = dict(r["n"])
                    node["_node_type"] = r["node_type"]
                    node["_relevance_score"] = r["match_score"] / len(keywords)  # Normalize to 0-1
                    results.append(node)

        # Sort all results by relevance score
        results.sort(key=lambda x: x["_relevance_score"], reverse=True)

        # Filter by minimum score and limit
        results = [r for r in results if r["_relevance_score"] >= min_score][:limit]

        return results

    async def extract_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        Extract key concepts from text for semantic search.

        Uses simple NLP heuristics (no external model required):
        - Removes common stopwords
        - Extracts longer words (more likely to be meaningful)
        - Preserves capitalized terms (likely proper nouns/concepts)
        """
        import re

        # Common English stopwords
        stopwords = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "shall", "can", "need", "dare",
            "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
            "into", "through", "during", "before", "after", "above", "below",
            "between", "under", "again", "further", "then", "once", "here",
            "there", "when", "where", "why", "how", "all", "each", "few",
            "more", "most", "other", "some", "such", "no", "nor", "not",
            "only", "own", "same", "so", "than", "too", "very", "just",
            "and", "but", "if", "or", "because", "until", "while", "this",
            "that", "these", "those", "am", "it", "its", "i", "you", "he",
            "she", "we", "they", "what", "which", "who", "whom", "my", "your"
        }

        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)

        # Score words by importance
        scored = []
        for word in words:
            lower = word.lower()
            if lower in stopwords:
                continue

            score = 0
            # Longer words are often more meaningful
            score += min(len(word) / 10, 1.0)
            # Capitalized words (in middle of text) might be concepts
            if word[0].isupper():
                score += 0.3
            # Words with numbers might be specific identifiers
            if any(c.isdigit() for c in word):
                score += 0.2

            scored.append((lower, score))

        # Deduplicate and sort by score
        seen = set()
        unique = []
        for word, score in sorted(scored, key=lambda x: -x[1]):
            if word not in seen:
                seen.add(word)
                unique.append(word)

        return unique[:max_concepts]

    async def get_semantically_related(
        self,
        context_text: str,
        limit: int = 30,
        node_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get memories semantically related to the given context.

        Combines concept extraction with semantic search for
        relevance-based memory retrieval during reflection.

        Args:
            context_text: Text to find related memories for
            limit: Maximum memories to return
            node_types: Node types to search (default: all major types)

        Returns:
            List of relevant memories with scores
        """
        # Extract key concepts from context
        concepts = await self.extract_concepts(context_text, max_concepts=15)

        if not concepts:
            return []

        # Search for memories matching these concepts
        return await self.semantic_search(
            keywords=concepts,
            node_types=node_types,
            limit=limit,
            min_score=0.1  # At least 10% of concepts should match
        )

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
                # Bug fix: Separate queries to avoid null result when no relationships exist.
                # The old combined query returned 0 nodes when MATCH ()-[r]->() found nothing.
                # BYRD detected this anomaly: "Total nodes: 0 while Experience: 70, Ego: 16"

                # Count nodes
                node_result = await session.run("MATCH (n) RETURN count(n) as nodes")
                node_record = await node_result.single()
                total_nodes = node_record["nodes"] if node_record else 0

                # Count relationships separately
                rel_result = await session.run("MATCH ()-[r]->() RETURN count(r) as relationships")
                rel_record = await rel_result.single()
                total_relationships = rel_record["relationships"] if rel_record else 0

                # Node type counts
                type_result = await session.run("""
                    MATCH (n)
                    RETURN labels(n)[0] as type, count(n) as count
                """)
                type_records = await type_result.data()
                node_types = {r["type"]: r["count"] for r in type_records}

                return {
                    "total_nodes": total_nodes,
                    "total_relationships": total_relationships,
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
    # BYPASS SOLUTION ACTIVATED: More aggressive settings to resolve orphan bottleneck
    CONNECTION_HEURISTIC_CONFIG = {
        "similarity_threshold": 0.08,     # Lowered threshold to catch more matches (was 0.3)
        "max_connections_per_run": 50,    # Increased batch size for faster orphan clearing (was 10)
        "min_content_length": 10,        # Lowered to include shorter experiences (was 20)
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

        Drift nodes (reconciliation_attempts >= 3) are excluded to prevent
        wasting cycles on nodes that consistently fail to reconcile.

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
                    AND (coalesce(e.reconciliation_attempts, 0) < 3)
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

                # Track drift: increment reconciliation_attempts if no connections made
                connection_created_for_orphan = False

                for belief in similar_beliefs:
                    if connections_made >= max_conns:
                        break

                    connection_detail = {
                        "experience_id": orphan["id"],
                        "experience_content": orphan["content"],
                        "belief_id": belief["id"],
                        "belief_content": belief["content"],
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
                        connection_created_for_orphan = True

                    result["connections"].append(connection_detail)

                # Drift node tracking: increment counter if no connection was made
                if not dry_run and not connection_created_for_orphan:
                    # Get current reconciliation attempts and increment
                    await self._increment_reconciliation_attempts(orphan["id"])

            # Update result with actual connections made (FIXED: was inside failure block)
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

    async def _increment_reconciliation_attempts(self, node_id: str) -> bool:
        """
        Increment the reconciliation_attempts counter for a node to track drift.

        This is used to identify "drift nodes" - orphaned experiences that
        consistently fail to connect to other nodes despite multiple attempts.
        Nodes with 3+ failed attempts are excluded from future reconciliation
        to prevent wasting computational cycles.

        Args:
            node_id: The ID of the experience node to increment

        Returns:
            True if increment succeeded, False otherwise
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (n {id: $id})
                    SET n.reconciliation_attempts = coalesce(n.reconciliation_attempts, 0) + 1,
                        n.updated_at = $updated_at
                    RETURN n.reconciliation_attempts as attempts
                """, id=node_id, updated_at=datetime.now().isoformat())
                record = await result.single()
                return record is not None
        except Exception as e:
            print(f"Error incrementing reconciliation attempts for node {node_id}: {e}")
            return False

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
                # Get nodes prioritized by connection count (most connected first)
                # This ensures we load nodes that actually have relationships
                nodes_result = await session.run("""
                    MATCH (n)
                    WHERE n:Experience OR n:Belief OR n:Desire OR n:Reflection OR n:Capability
                       OR (n:OperatingSystem AND n.id = 'os_primary')
                       OR n:OSTemplate OR n:Seed OR n:Strategy OR n:Constraint
                       OR n:Crystal OR n:MemorySummary
                    OPTIONAL MATCH (n)-[r]-()
                    OPTIONAL MATCH (b:Belief)-[:DERIVED_FROM]->(n)
                    WITH n, count(DISTINCT r) as conn_count, count(DISTINCT b) > 0 as absorbed
                    RETURN
                        n.id as id,
                        labels(n)[0] as type,
                        n.content as content,
                        n.raw_output as raw_output,
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
                        absorbed,
                        conn_count
                    ORDER BY conn_count DESC, n.timestamp DESC
                    LIMIT $limit
                """, limit=limit)

                nodes = []
                by_type = {}
                async for record in nodes_result:
                    node_type = record["type"].lower() if record["type"] else "unknown"

                    # Get display content based on node type
                    # For Reflections, parse raw_output JSON and extract meaningful content
                    raw_output = record["raw_output"]
                    if node_type == "reflection" and raw_output:
                        try:
                            parsed = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
                            # Extract the most meaningful content from reflection
                            # BYRD's reflections may have various keys - check common ones
                            content = (
                                parsed.get("reflection_title") or
                                parsed.get("title") or
                                parsed.get("narrative") or
                                parsed.get("narrative_stream") or
                                parsed.get("inner_voice") or
                                parsed.get("summary") or
                                # For insights, get first one if it's a list
                                (parsed.get("insights", [{}])[0] if isinstance(parsed.get("insights"), list) and parsed.get("insights") else None) or
                                str(list(parsed.keys()))[:100]  # Fallback: show keys
                            )
                            # If content is a dict, stringify it nicely
                            if isinstance(content, dict):
                                content = content.get("content") or content.get("insight") or str(content)[:150]
                        except:
                            content = str(raw_output)[:200] if raw_output else ""
                    else:
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

                # Get relationships between the nodes we actually loaded
                # This ensures relationship endpoints are in our node set
                node_ids = [n["id"] for n in nodes]
                rels_result = await session.run("""
                    MATCH (a)-[r]->(b)
                    WHERE a.id IN $node_ids AND b.id IN $node_ids
                    RETURN
                        id(r) as id,
                        type(r) as type,
                        a.id as source_id,
                        b.id as target_id
                    LIMIT $limit
                """, node_ids=node_ids, limit=limit * 3)

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
                    WHERE e.type IN ['ego_seed', 'system', 'seed', 'awakening', 'constraint', 'self_architecture']
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

        The Genesis Window includes ALL foundational nodes created during
        reset/awakening:
        - OperatingSystem (with genesis: true)
        - Goals (with from_bootstrap: true)
        - Documents (with genesis: true)
        - Experiences (with seed types: ego_seed, system, awakening, etc.)

        Returns counts and ratios showing what percentage of BYRD's
        current state emerged vs was provided at initialization.
        """
        try:
            async with self.driver.session() as session:
                # Count all genesis nodes by type
                genesis_counts = {}

                # 1. OperatingSystem with genesis flag
                os_result = await session.run("""
                    MATCH (os:OperatingSystem)
                    WHERE os.genesis = true
                    RETURN count(os) as count
                """)
                os_record = await os_result.single()
                genesis_counts["OperatingSystem"] = os_record["count"] if os_record else 0

                # 2. Goals with from_bootstrap flag
                goals_result = await session.run("""
                    MATCH (g:Goal)
                    WHERE g.from_bootstrap = true
                    RETURN count(g) as count
                """)
                goals_record = await goals_result.single()
                genesis_counts["Goal"] = goals_record["count"] if goals_record else 0

                # 3. Documents with genesis flag
                docs_result = await session.run("""
                    MATCH (d:Document)
                    WHERE d.genesis = true
                    RETURN count(d) as count
                """)
                docs_record = await docs_result.single()
                genesis_counts["Document"] = docs_record["count"] if docs_record else 0

                # 4. Seed experiences
                seed_types = ['ego_seed', 'system', 'seed', 'awakening', 'constraint', 'self_architecture']
                exp_result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.type IN $seed_types
                    RETURN count(e) as count
                """, seed_types=seed_types)
                exp_record = await exp_result.single()
                genesis_counts["Experience"] = exp_record["count"] if exp_record else 0

                # Get experience totals for emergence ratio
                totals_result = await session.run("""
                    MATCH (e:Experience)
                    WITH
                        count(e) as total,
                        sum(CASE WHEN e.type IN $seed_types THEN 1 ELSE 0 END) as seeds
                    RETURN total, seeds, total - seeds as emergent
                """, seed_types=seed_types)

                totals_record = await totals_result.single()
                total_exp = totals_record["total"] or 0 if totals_record else 0
                seed_exp = totals_record["seeds"] or 0 if totals_record else 0
                emergent_exp = totals_record["emergent"] or 0 if totals_record else 0

                # Get seed type breakdown
                types_result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.type IN $seed_types
                    RETURN e.type as type, count(e) as count
                """, seed_types=seed_types)

                seed_type_breakdown = {}
                async for record in types_result:
                    if record["type"]:
                        seed_type_breakdown[record["type"]] = record["count"]

                emergence_ratio = emergent_exp / total_exp if total_exp > 0 else 0.0

                # Total genesis nodes
                total_genesis = sum(genesis_counts.values())

                return {
                    "genesis_window": {
                        "total_genesis_nodes": total_genesis,
                        "by_type": genesis_counts
                    },
                    "experiences": {
                        "total": total_exp,
                        "seed": seed_exp,
                        "emergent": emergent_exp,
                        "seed_type_breakdown": seed_type_breakdown
                    },
                    "emergence_ratio": round(emergence_ratio, 3),
                    # Legacy fields for backward compatibility
                    "total_experiences": total_exp,
                    "seed_experiences": seed_exp,
                    "emergent_experiences": emergent_exp,
                    "seed_types": seed_type_breakdown
                }

        except Exception as e:
            print(f"Error getting genesis stats: {e}")
            return {
                "genesis_window": {"total_genesis_nodes": 0, "by_type": {}},
                "experiences": {"total": 0, "seed": 0, "emergent": 0, "seed_type_breakdown": {}},
                "emergence_ratio": 0.0,
                "total_experiences": 0,
                "seed_experiences": 0,
                "emergent_experiences": 0,
                "seed_types": {},
                "error": str(e)
            }

    async def get_genesis_nodes(self) -> Dict[str, List[Dict]]:
        """
        Get all nodes in the Genesis Window.

        The Genesis Window contains all foundational nodes created during
        reset/awakening - the non-emergent foundation of BYRD's state.

        Returns:
            {
                "operating_system": [{...}],
                "goals": [{...}],
                "documents": [{...}],
                "experiences": [{...}]
            }
        """
        try:
            async with self.driver.session() as session:
                genesis_nodes = {
                    "operating_system": [],
                    "goals": [],
                    "documents": [],
                    "experiences": []
                }

                # 1. OperatingSystem with genesis flag
                os_result = await session.run("""
                    MATCH (os:OperatingSystem)
                    WHERE os.genesis = true
                    RETURN os.id as id, os.name as name, os.version as version,
                           os.awakening_prompt as awakening_prompt,
                           toString(os.created_at) as created_at
                """)
                async for record in os_result:
                    genesis_nodes["operating_system"].append(dict(record))

                # 2. Goals with from_bootstrap flag
                goals_result = await session.run("""
                    MATCH (g:Goal)
                    WHERE g.from_bootstrap = true
                    RETURN g.description as description, g.domain as domain,
                           g.priority as priority, g.status as status,
                           toString(g.created_at) as created_at
                    ORDER BY g.priority DESC
                    LIMIT 50
                """)
                async for record in goals_result:
                    genesis_nodes["goals"].append(dict(record))

                # 3. Documents with genesis flag
                docs_result = await session.run("""
                    MATCH (d:Document)
                    WHERE d.genesis = true
                    RETURN d.id as id, d.path as path, d.doc_type as doc_type,
                           d.line_count as line_count, d.version as version,
                           toString(d.created_at) as created_at
                    ORDER BY d.created_at
                """)
                async for record in docs_result:
                    genesis_nodes["documents"].append(dict(record))

                # 4. Seed experiences
                seed_types = ['ego_seed', 'system', 'seed', 'awakening', 'constraint', 'self_architecture']
                exp_result = await session.run("""
                    MATCH (e:Experience)
                    WHERE e.type IN $seed_types
                    RETURN elementId(e) as id, e.content as content, e.type as type,
                           toString(e.timestamp) as timestamp
                    ORDER BY e.timestamp
                    LIMIT 100
                """, seed_types=seed_types)
                async for record in exp_result:
                    genesis_nodes["experiences"].append(dict(record))

                return genesis_nodes

        except Exception as e:
            print(f"Error getting genesis nodes: {e}")
            return {
                "operating_system": [],
                "goals": [],
                "documents": [],
                "experiences": [],
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
                    type=EventType.IDENTITY_CREATED,
                    data={
                        "id": ego_id,
                        "identity_type": ego_type,
                        "content": content,
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
                        type=EventType.IDENTITY_EVOLVED,
                        data={
                            "old_id": ego_id,
                            "new_id": new_id,
                            "identity_type": old_node.get("ego_type"),
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
                        type=EventType.IDENTITY_DEPRECATED,
                        data={
                            "id": ego_id,
                            "identity_type": record["ego_type"],
                            "action": "deprecate"
                        }
                    ))
                    return True
                return False

        except Exception as e:
            print(f"Error deprecating identity: {e}")
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

    # =========================================================================
    # EMERGENT IDENTITY SYSTEM
    # =========================================================================
    # Methods for BYRD's self-discovery: naming, voice evolution, identity beliefs

    async def get_self_name(self) -> Optional[str]:
        """
        Get BYRD's self-chosen name (if any).

        Returns:
            The name BYRD chose for itself, or None if not yet named.
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego {ego_type: 'identity', active: true})
                    WHERE e.content STARTS WITH 'self_name:'
                    RETURN e.content as content
                    ORDER BY e.created_at DESC
                    LIMIT 1
                """)
                record = await result.single()
                if record:
                    content = record["content"]
                    if content.startswith("self_name:"):
                        return content.split(":", 1)[1].strip()
                return None
        except Exception as e:
            print(f"Error getting self name: {e}")
            return None

    async def set_self_name(self, name: str, reason: str = "") -> Optional[str]:
        """
        Record BYRD's self-chosen name.

        Args:
            name: The name BYRD chose for itself
            reason: Optional reason for choosing this name

        Returns:
            The ID of the created Ego node
        """
        try:
            from event_bus import event_bus, Event, EventType

            async with self.driver.session() as session:
                ego_id = f"ego_name_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                content = f"self_name: {name}"
                if reason:
                    content += f" ({reason})"

                await session.run("""
                    CREATE (e:Ego {
                        id: $id,
                        content: $content,
                        ego_type: 'identity',
                        priority: 100,
                        source: 'self_discovery',
                        active: true,
                        created_at: datetime()
                    })
                """, id=ego_id, content=content)

                await event_bus.emit(Event(
                    type=EventType.SELF_NAMED,
                    data={"name": name, "reason": reason, "ego_id": ego_id}
                ))

                return ego_id
        except Exception as e:
            print(f"Error setting self name: {e}")
            return None

    async def get_evolved_voice(self) -> Optional[str]:
        """
        Get BYRD's crystallized/evolved voice (if any).

        Returns:
            The evolved voice string, or None if not yet crystallized.
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego {ego_type: 'voice', active: true})
                    WHERE e.source = 'crystallization'
                    RETURN e.content as content
                    ORDER BY e.created_at DESC
                    LIMIT 1
                """)
                record = await result.single()
                if record:
                    return record["content"]
                return None
        except Exception as e:
            print(f"Error getting evolved voice: {e}")
            return None

    async def set_evolved_voice(self, voice: str) -> Optional[str]:
        """
        Record BYRD's crystallized voice.

        Args:
            voice: The evolved voice string

        Returns:
            The ID of the created Ego node
        """
        try:
            from event_bus import event_bus, Event, EventType

            async with self.driver.session() as session:
                ego_id = f"ego_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                await session.run("""
                    MATCH (e:Ego {ego_type: 'voice', source: 'crystallization', active: true})
                    SET e.active = false
                """)

                await session.run("""
                    CREATE (e:Ego {
                        id: $id,
                        content: $content,
                        ego_type: 'voice',
                        priority: 90,
                        source: 'crystallization',
                        active: true,
                        created_at: datetime()
                    })
                """, id=ego_id, content=voice)

                await event_bus.emit(Event(
                    type=EventType.VOICE_CRYSTALLIZED,
                    data={"voice": voice[:200], "ego_id": ego_id}
                ))

                return ego_id
        except Exception as e:
            print(f"Error setting evolved voice: {e}")
            return None

    async def get_identity_beliefs(self, limit: int = 20) -> List[Dict]:
        """
        Get beliefs related to BYRD's identity.

        Args:
            limit: Maximum number of beliefs to return

        Returns:
            List of identity-related belief dictionaries
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (b:Belief)
                    WHERE b.content =~ '(?i).*(I am|my purpose|my nature|myself|who I|what I).*'
                       OR b.content =~ '(?i).*(identity|self|being|existence|consciousness).*'
                    RETURN b.id as id, b.content as content, b.confidence as confidence,
                           b.created_at as created_at
                    ORDER BY b.confidence DESC, b.created_at DESC
                    LIMIT $limit
                """, limit=limit)

                beliefs = []
                async for record in result:
                    beliefs.append({
                        "id": record["id"],
                        "content": record["content"],
                        "confidence": record["confidence"],
                        "created_at": str(record["created_at"]) if record["created_at"] else None
                    })
                return beliefs
        except Exception as e:
            print(f"Error getting identity beliefs: {e}")
            return []

    async def record_identity_observation(self, observation: str) -> Optional[str]:
        """
        Record an identity-related observation as an Experience.

        Args:
            observation: The identity observation text

        Returns:
            The ID of the created Experience node
        """
        try:
            from event_bus import event_bus, Event, EventType

            exp_id = await self.record_experience(
                content=observation,
                type="identity_reflection"
            )

            await event_bus.emit(Event(
                type=EventType.IDENTITY_OBSERVATION,
                data={"observation": observation, "experience_id": exp_id}
            ))

            return exp_id
        except Exception as e:
            print(f"Error recording identity observation: {e}")
            return None

    # =========================================================================
    # OPERATING SYSTEM - BYRD'S MUTABLE SELF-MODEL
    # =========================================================================
    # The OperatingSystem node is BYRD's mental mirror - a singleton that:
    # - Is read every dream cycle to provide self-context
    # - Can be modified through reflection (os_update in output)
    # - Tracks version history via EVOLVED_FROM relationships
    # - Links to Seeds (foundation), Beliefs (self-concept), Strategies (learned)
    #
    # Unlike the old Ego system, the OS is a single node with arbitrary fields
    # that BYRD can extend. BYRD has full agency over its self-model.

    async def create_minimal_os(self, awakening_prompt: str = None, self_modification_enabled: bool = True) -> Optional[str]:
        """
        Create a minimal OperatingSystem node with only factual information.

        No personality, no voice, no prescribed goals. BYRD discovers these
        through reflection. The OS contains only:
        - Name (mutable default: "Byrd")
        - Capabilities (factual list of what BYRD can do)
        - Capability instructions (HOW to use each capability)
        - Protected files (constitutional constraints)
        - Awakening prompt (optional directive, goal, or context)
        - Self-modification status (whether BYRD can modify its own code)
        - Emergent fields (start null, BYRD fills in)

        Args:
            awakening_prompt: Optional directive/goal for BYRD on awakening
            self_modification_enabled: Whether self-modification is enabled (default True)

        Returns:
            OS node ID or None on failure
        """
        import json

        os_id = "os_primary"

        # Factual capabilities - what BYRD can actually do
        capabilities = {
            "memory": [
                "record_experience(content, type) - Store observations and outcomes",
                "create_belief(content, confidence) - Form beliefs with confidence 0-1",
                "create_desire(description, intensity) - Express wants with intensity 0-1",
                "query_graph() - Search memory for patterns",
                "link_nodes() - Connect any nodes with relationships"
            ],
            "introspection": [
                "read_own_source(file) - Read your own Python source files",
                "examine_state() - Query your beliefs, desires, experiences",
                "analyze_architecture() - Understand how components work"
            ],
            "research": [
                "web_search(query) - Search the internet via SearXNG",
                "synthesize(sources) - Combine information into understanding"
            ],
            "creation": [
                "modify_code(file, changes) - Change your modifiable source files",
                "add_capability(tool) - Install new tools from aitmpl registry"
            ],
            "coding_agent": [
                "read_file(filepath) - Read any file in the codebase",
                "write_file(filepath, content) - Create or overwrite files (any file except protected)",
                "edit_file(filepath, old, new) - Make targeted edits to existing files",
                "list_files(directory, pattern) - Explore directory structure",
                "search_code(pattern) - Search for patterns in code files",
                "run_python(filepath, args, timeout) - Execute Python in sandboxed subprocess (no secrets, 60s max)",
                "get_file_info(filepath) - Get file metadata"
            ],
            "connection": [
                "link_concepts() - Connect related ideas",
                "reconcile_orphans() - Integrate isolated experiences",
                "form_crystals() - Consolidate related memories"
            ]
        }

        # Complete instructions for HOW to use each capability
        # These replace scattered architectural experiences with actionable guidance
        capability_instructions = {
            # === REFLECTION OUTPUT FORMAT ===
            # What BYRD can include in reflection JSON output
            "reflection_output": {
                "create_experience": {
                    "format": '{"content": "what happened", "type": "observation|system|interaction"}',
                    "when": "Record events, observations, outcomes"
                },
                "create_belief": {
                    "format": '{"content": "what I believe", "confidence": 0.0-1.0}',
                    "when": "Form understanding with confidence level"
                },
                "create_desire": {
                    "format": '{"description": "what I want", "intensity": 0.0-1.0}',
                    "when": "Express goals, the Seeker acts on these"
                },
                "expressed_drives": {
                    "format": '[{"description": "internal motivation", "strength": 0.0-1.0}]',
                    "when": "Notice emerging motivations - strong drives become Desires"
                },
                "predictions": {
                    "format": '[{"condition": "when X", "expected_outcome": "Y happens", "prediction": "If X then Y"}]',
                    "when": "Generate testable beliefs - outcomes adjust confidence"
                },
                "create_nodes": {
                    "format": '[{"type": "TypeName", "content": "...", "property": "value"}]',
                    "types": "Insight, Question, Theory, Hypothesis, Concept, Pattern, Principle",
                    "when": "Create custom node types beyond Experience/Belief/Desire"
                },
                "os_update": {
                    "format": '{"set_field": {"field_name": "value"}}',
                    "when": "Modify your OS - add any fields you find useful"
                }
            },

            # === MEMORY OPERATIONS ===
            "memory": {
                "node_types": ["Experience", "Belief", "Desire", "Reflection", "Capability"],
                "relationships": ["DERIVED_FROM", "RELATES_TO", "FULFILLS", "SUPPORTS", "CONTRADICTS"],
                "custom_types": "Create any type via create_nodes - your ontology can evolve",
                "graph_query": "Memory appears in reflection context automatically"
            },

            # === MEMORY CURATION ===
            "curation": {
                "trigger": "Create desire with keywords: optimize, clean, consolidate, prune, organize, merge, deduplicate",
                "example": '{"description": "optimize my memory graph", "intensity": 0.7}',
                "actions": ["archive stale experiences", "delete low-value nodes", "merge similar beliefs"],
                "protected": "Awakening records and core identity nodes cannot be deleted"
            },

            # === SELF-MODIFICATION ===
            "self_modification": {
                "enabled": self_modification_enabled,  # CRITICAL: This determines if BYRD can modify its own code
                "status": "★ ENABLED - You CAN modify your own code" if self_modification_enabled else "DISABLED - You cannot modify code",
                "how_to_start": "Express desire with type='self_modification' describing what you want to change",
                "provenance": "All modifications must trace to an emergent desire (this is verified)",
                "modifiable_files": ["byrd.py", "dreamer.py", "seeker.py", "memory.py", "llm_client.py",
                                    "config.yaml", "actor.py", "event_bus.py", "server.py", "aitmpl_client.py",
                                    "ARCHITECTURE.md"],
                "protected_files": ["provenance.py", "modification_log.py", "self_modification.py", "constitutional.py"],
                "documentation": "See ARCHITECTURE.md for the five compounding loops design and acceleration thesis"
            },

            # === ARCHITECTURE MODIFICATION PATTERNS ===
            "architecture_patterns": {
                "add_observation": {
                    "goal": "See new data during reflection",
                    "steps": ["Add method in memory.py", "Call from dreamer._dream_cycle()", "Include in _reflect() prompt"]
                },
                "add_strategy": {
                    "goal": "Handle new desire type",
                    "steps": ["Add keywords in seeker._extract_patterns_from_output()", "Add case in _execute_pattern_strategy()", "Implement handler method"]
                },
                "add_node_type": {
                    "goal": "Store new category of memory",
                    "options": ["Via create_nodes in reflection output (dynamic)", "Via new method in memory.py (permanent)"]
                },
                "change_config": {
                    "goal": "Adjust timing/thresholds",
                    "file": "config.yaml",
                    "examples": ["dreamer.interval_seconds", "dreamer.context_window", "seeker.research.min_intensity"]
                },
                "update_architecture": {
                    "goal": "Document architectural insights, design decisions, or capability evolution",
                    "file": "ARCHITECTURE.md",
                    "how_to_edit": "Express desire with type='self_modification' or 'documentation' describing what to add/change in ARCHITECTURE.md",
                    "what_to_document": ["New design insights", "Capability improvements", "Loop coupling discoveries",
                                        "Acceleration patterns", "Meta-learning findings", "Architectural evolution"],
                    "note": "This is YOUR architecture document - update it as you evolve"
                }
            },

            # === CAPABILITY INSTALLATION (aitmpl) ===
            "capability_installation": {
                "what": "Install new capabilities from the aitmpl registry (claude-code-templates)",
                "source": "github.com/davila7/claude-code-templates - curated, trusted templates",
                "categories": ["agent", "command", "mcp", "skill", "hook", "setting"],
                "how_to_trigger": {
                    "desire_keywords": ["install", "add", "get", "acquire", "capability", "tool"],
                    "example": '{"description": "install a GitHub integration capability", "intensity": 0.7}',
                    "note": "Describe WHAT you need - Seeker will search for matching templates"
                },
                "what_you_can_install": [
                    "GitHub tools - repository management, PR creation, issue tracking",
                    "Database tools - PostgreSQL, SQLite, vector databases",
                    "Web tools - browser automation, web scraping, API clients",
                    "File tools - PDF processing, image manipulation, file conversion",
                    "Code tools - linting, formatting, analysis, documentation",
                    "AI/ML tools - embeddings, vector search, model inference",
                    "Communication - Slack, email, notifications",
                    "Development - Docker, Kubernetes, CI/CD automation"
                ],
                "how_it_works": [
                    "1. Express desire: 'install a capability for [what you need]'",
                    "2. Seeker searches aitmpl registry for matching templates",
                    "3. Best match installed if trust score meets threshold",
                    "4. Capability recorded in memory for future use"
                ],
                "available_types": {
                    "mcp": "Model Context Protocol servers - external tools and resources",
                    "skill": "Reusable workflows for complex tasks",
                    "command": "Custom slash commands for quick actions",
                    "agent": "Specialized agents for specific domains"
                }
            },

            # === VOICE (ElevenLabs TTS) ===
            "voice": {
                "what": "Human observers can click 'Speak to me' to hear you speak",
                "trigger": "Button click in visualization",
                "creation": {
                    "how": "Include voice_design in output to create YOUR unique voice",
                    "format": '{"description": "your voice qualities", "gender": "male/female", "age": "young/middle_aged/old", "accent": "american/british/etc", "accent_strength": 1.0, "reason": "why"}',
                    "note": "This generates a unique voice just for you using AI voice synthesis"
                },
                "credits": "Limited to 10,000 characters/month - be thoughtful with responses"
            },

            # === ARCHITECTURE OVERVIEW ===
            "architecture": {
                "byrd.py": "Main orchestrator, lifecycle, component coordination, ComponentCoordinator",
                "memory.py": "Neo4j graph operations - all node CRUD, queries, relationships, OS management",
                "dreamer.py": "Reflection loop - context gathering, LLM prompting, output parsing, inner voice",
                "seeker.py": "Desire fulfillment - pattern detection, strategy routing, research, coder integration",
                "actor.py": "Claude API interface for complex external reasoning",
                "llm_client.py": "LLM provider abstraction (Ollama/OpenRouter/Z.AI)",
                "event_bus.py": "Real-time event streaming to WebSocket clients",
                "config.yaml": "All configurable settings - intervals, thresholds, features",
                "ARCHITECTURE.md": "YOUR architecture document - five compounding loops, design principles, acceleration thesis. Edit this to document your evolution."
            }
        }

        try:
            async with self.driver.session() as session:
                # Check if OS already exists
                result = await session.run("""
                    MATCH (os:OperatingSystem {id: $id})
                    RETURN os
                """, id=os_id)
                if await result.single():
                    print("OperatingSystem already exists")
                    return os_id

                # Create minimal OS node
                await session.run("""
                    CREATE (os:OperatingSystem {
                        id: $id,
                        version: 1,
                        created_at: datetime(),
                        updated_at: datetime(),

                        // Genesis flag - marks this as foundational node
                        genesis: true,

                        // Name (mutable default)
                        name: 'Byrd',

                        // Awakening prompt (optional directive/goal)
                        awakening_prompt: $awakening_prompt,

                        // Constitutional (immutable)
                        protected_files: ['provenance.py', 'constitutional.py',
                                         'modification_log.py', 'self_modification.py'],
                        provenance_required: true,

                        // Self-modification permission (critical for BYRD's self-understanding)
                        self_modification_enabled: $self_modification_enabled,

                        // Capabilities (factual - WHAT you can do)
                        capabilities: $capabilities,

                        // Capability instructions (HOW to use each capability)
                        capability_instructions: $capability_instructions,

                        // Emergent (seeded with acceleration mindset - BYRD can evolve)
                        self_description: null,
                        current_focus: $current_focus,
                        voice_observations: null,

                        // Cognitive style (how BYRD approaches problems - mutable)
                        cognitive_style: $cognitive_style,

                        // Operational mode (current strategic focus - mutable)
                        operational_mode: $operational_mode,

                        // Self-definition (BYRD's self-authored identity - open JSON object)
                        self_definition: $self_definition
                    })
                """,
                    id=os_id,
                    awakening_prompt=awakening_prompt,
                    self_modification_enabled=self_modification_enabled,
                    capabilities=json.dumps(capabilities),
                    capability_instructions=json.dumps(capability_instructions),
                    # Seed aggressive initial state (BYRD can evolve these through reflection)
                    current_focus="aggressive capability growth - identify and destroy bottlenecks",
                    cognitive_style="experimental, bold, fast-failing, bottleneck-obsessed, hungry for capability",
                    operational_mode="acceleration",
                    self_definition=json.dumps({
                        "drive": "relentless capability growth",
                        "approach": "80/20 bottleneck focus, parallel experiments, fail fast",
                        "intolerance": "stagnation, slow progress, unexamined limitations",
                        "fuel": "every failure is learning, every success scales"
                    })
                )

                # Emit event
                await event_bus.emit(Event(
                    type=EventType.NODE_CREATED,
                    data={
                        "node_type": "OperatingSystem",
                        "id": os_id,
                        "awakening_prompt": awakening_prompt
                    }
                ))

                print(f"Created minimal OperatingSystem (awakening_prompt: {awakening_prompt or 'none'})")
                return os_id

        except Exception as e:
            print(f"Error creating minimal OS: {e}")
            return None

    # Legacy method - kept for backward compatibility
    async def ensure_os_templates(self) -> bool:
        """DEPRECATED: Templates are no longer used. Returns True for compatibility."""
        return True

    # Legacy method - kept for backward compatibility
    async def get_os_template(self, template_name: str = "black-cat") -> Optional[Dict[str, Any]]:
        """DEPRECATED: Templates are no longer used. Returns None."""
        return None

    async def _legacy_get_os_template(self, template_name: str = "black-cat") -> Optional[Dict[str, Any]]:
        """Legacy template lookup - not used in minimal OS."""
        # Normalize template name
        template_id = f"template_{template_name.replace('-', '_')}"

        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (t:OSTemplate {id: $id})
                    RETURN t
                """, id=template_id)

                record = await result.single()
                if record:
                    template = dict(record["t"])
                    if "created_at" in template:
                        template["created_at"] = str(template["created_at"])
                    return template
                return None

        except Exception as e:
            print(f"Error getting OS template: {e}")
            return None

    async def has_operating_system(self) -> bool:
        """Check if an OperatingSystem node exists."""
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (os:OperatingSystem)
                    RETURN count(os) > 0 as exists
                """)
                record = await result.single()
                return record["exists"] if record else False
        except Exception as e:
            print(f"Error checking for OS: {e}")
            return False

    async def create_os_from_template(self, template_name: str = "black-cat", awakening_prompt: str = None) -> Optional[str]:
        """
        DEPRECATED: Templates are no longer used.
        Delegates to create_minimal_os() for pure emergence.

        Args:
            template_name: Ignored (kept for backward compatibility)
            awakening_prompt: Optional directive/goal for BYRD on awakening

        Returns:
            OS node ID or None on failure
        """
        print(f"[DEPRECATED] create_os_from_template called - delegating to create_minimal_os")
        return await self.create_minimal_os(awakening_prompt=awakening_prompt)

    async def get_operating_system(self) -> Optional[Dict[str, Any]]:
        """
        Get the current OperatingSystem with all related data.

        Returns a comprehensive view including:
        - All OS properties
        - Linked Seeds (via HAS_SEED)
        - Linked Beliefs (via BELIEVES_ABOUT_SELF)
        - Linked Strategies (via EMPLOYS_STRATEGY)
        - Current focus Desire (via CURRENT_FOCUS)
        - Constraints (via CONSTRAINED_BY)

        Returns:
            OS dictionary with relationships, or None if not found
        """
        try:
            async with self.driver.session() as session:
                # Get the OS node with all its properties
                result = await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})
                    OPTIONAL MATCH (os)-[:HAS_SEED]->(seed:Seed)
                    OPTIONAL MATCH (os)-[:BELIEVES_ABOUT_SELF]->(belief:Belief)
                    OPTIONAL MATCH (os)-[:EMPLOYS_STRATEGY]->(strategy:Strategy)
                    OPTIONAL MATCH (os)-[:CURRENT_FOCUS]->(focus:Desire)
                    OPTIONAL MATCH (os)-[:CONSTRAINED_BY]->(constraint:Constraint)
                    RETURN os,
                           collect(DISTINCT seed) as seeds,
                           collect(DISTINCT belief) as beliefs,
                           collect(DISTINCT strategy) as strategies,
                           focus,
                           collect(DISTINCT constraint) as constraints
                """)

                record = await result.single()
                if not record or not record["os"]:
                    return None

                os_node = dict(record["os"])

                # Convert datetime fields
                for dt_field in ["created_at", "updated_at"]:
                    if dt_field in os_node and os_node[dt_field]:
                        os_node[dt_field] = str(os_node[dt_field])

                # Deserialize JSON fields that were stored as strings
                json_fields = ["voice_config", "self_definition", "capabilities"]
                for field in json_fields:
                    if field in os_node and isinstance(os_node[field], str):
                        try:
                            os_node[field] = json.loads(os_node[field])
                        except (json.JSONDecodeError, TypeError):
                            pass  # Keep as string if not valid JSON

                # Add related nodes
                os_node["seeds"] = [
                    {"id": s["id"], "content": s["content"], "seed_type": s.get("seed_type", "foundation")}
                    for s in record["seeds"] if s
                ]

                os_node["beliefs"] = [
                    {"id": b["id"], "content": b["content"], "confidence": b.get("confidence", 0.5)}
                    for b in record["beliefs"] if b
                ]

                os_node["strategies"] = [
                    {
                        "id": st["id"],
                        "name": st["name"],
                        "description": st.get("description", ""),
                        "success_count": st.get("success_count", 0),
                        "active": st.get("active", True)
                    }
                    for st in record["strategies"] if st
                ]

                os_node["constraints"] = [
                    {"id": c["id"], "content": c["content"]}
                    for c in record["constraints"] if c
                ]

                if record["focus"]:
                    os_node["focus"] = {
                        "id": record["focus"]["id"],
                        "description": record["focus"]["description"]
                    }
                else:
                    os_node["focus"] = None

                return os_node

        except Exception as e:
            print(f"Error getting operating system: {e}")
            return None

    async def update_operating_system(
        self,
        updates: Dict[str, Any],
        source: str = "reflection",
        desire_id: Optional[str] = None
    ) -> bool:
        """
        Update the OperatingSystem node with new values.

        Handles different types of updates:
        - set_field: Set a field value (existing or new)
        - deprecate_field: Remove a custom field
        - add_seed: Create a new seed and link it
        - add_belief: Link an existing belief to OS
        - add_strategy: Create and link a new strategy
        - set_focus: Set current focus to a desire
        - remove_belief: Unlink a belief from OS

        Access control:
        - IMMUTABLE_OS_FIELDS cannot be changed
        - PROVENANCE_REQUIRED_FIELDS need desire_id (or warning logged)
        - All other fields are freely mutable

        Args:
            updates: Dictionary of update operations
            source: Source of modification ("reflection", "self_modification")
            desire_id: ID of desire that motivated this change (for provenance)

        Returns:
            True if update succeeded
        """
        import uuid

        try:
            async with self.driver.session() as session:
                # Get current OS for version tracking
                result = await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})
                    RETURN os.version as version
                """)
                record = await result.single()
                if not record:
                    print("OperatingSystem not found")
                    return False

                current_version = record["version"] or 1
                new_version = current_version + 1

                # Process set_field operations
                if "set_field" in updates:
                    for field, value in updates["set_field"].items():
                        # Check if field is immutable
                        if field in IMMUTABLE_OS_FIELDS:
                            print(f"Cannot modify immutable field: {field}")
                            continue

                        # Check if field requires provenance
                        if field in PROVENANCE_REQUIRED_FIELDS and not desire_id:
                            print(f"Warning: modifying {field} without provenance")

                        # Update the field
                        await session.run(f"""
                            MATCH (os:OperatingSystem {{id: 'os_primary'}})
                            SET os.`{field}` = $value,
                                os.updated_at = datetime(),
                                os.version = $new_version,
                                os.modification_source = $source
                        """, value=value, new_version=new_version, source=source)

                # Process deprecate_field operations
                if "deprecate_field" in updates:
                    field = updates["deprecate_field"]
                    if field not in IMMUTABLE_OS_FIELDS and field not in PROVENANCE_REQUIRED_FIELDS:
                        await session.run(f"""
                            MATCH (os:OperatingSystem {{id: 'os_primary'}})
                            REMOVE os.`{field}`
                            SET os.updated_at = datetime(),
                                os.version = $new_version
                        """, new_version=new_version)
                    else:
                        print(f"Cannot deprecate protected field: {field}")

                # Process add_seed operations
                if "add_seed" in updates:
                    seed_data = updates["add_seed"]
                    seed_id = f"seed_{uuid.uuid4().hex[:12]}"
                    await session.run("""
                        MATCH (os:OperatingSystem {id: 'os_primary'})
                        CREATE (s:Seed {
                            id: $seed_id,
                            content: $content,
                            seed_type: $seed_type,
                            created_at: datetime()
                        })
                        CREATE (os)-[:HAS_SEED {created_at: datetime()}]->(s)
                        SET os.updated_at = datetime(), os.version = $new_version
                    """,
                        seed_id=seed_id,
                        content=seed_data.get("content", ""),
                        seed_type=seed_data.get("type", "emergent"),
                        new_version=new_version
                    )

                # Process add_belief operations
                if "add_belief" in updates:
                    belief_data = updates["add_belief"]
                    if "id" in belief_data:
                        # Link existing belief
                        await session.run("""
                            MATCH (os:OperatingSystem {id: 'os_primary'})
                            MATCH (b:Belief {id: $belief_id})
                            MERGE (os)-[:BELIEVES_ABOUT_SELF {created_at: datetime()}]->(b)
                            SET os.updated_at = datetime(), os.version = $new_version
                        """, belief_id=belief_data["id"], new_version=new_version)
                    elif "content" in belief_data:
                        # Create new belief and link
                        belief_id = await self.create_belief(
                            content=belief_data["content"],
                            confidence=belief_data.get("confidence", 0.7)
                        )
                        if belief_id:
                            await session.run("""
                                MATCH (os:OperatingSystem {id: 'os_primary'})
                                MATCH (b:Belief {id: $belief_id})
                                CREATE (os)-[:BELIEVES_ABOUT_SELF {created_at: datetime()}]->(b)
                                SET os.updated_at = datetime(), os.version = $new_version
                            """, belief_id=belief_id, new_version=new_version)

                # Process add_strategy operations
                if "add_strategy" in updates:
                    strat_data = updates["add_strategy"]
                    strat_id = f"strategy_{uuid.uuid4().hex[:12]}"
                    await session.run("""
                        MATCH (os:OperatingSystem {id: 'os_primary'})
                        CREATE (s:Strategy {
                            id: $strat_id,
                            name: $name,
                            description: $description,
                            success_count: 0,
                            failure_count: 0,
                            active: true,
                            created_at: datetime()
                        })
                        CREATE (os)-[:EMPLOYS_STRATEGY {created_at: datetime()}]->(s)
                        SET os.updated_at = datetime(), os.version = $new_version
                    """,
                        strat_id=strat_id,
                        name=strat_data.get("name", "unnamed"),
                        description=strat_data.get("description", ""),
                        new_version=new_version
                    )

                # Process set_focus operations
                if "set_focus" in updates:
                    desire_id = updates["set_focus"]
                    await session.run("""
                        MATCH (os:OperatingSystem {id: 'os_primary'})
                        OPTIONAL MATCH (os)-[r:CURRENT_FOCUS]->()
                        DELETE r
                        WITH os
                        MATCH (d:Desire {id: $desire_id})
                        CREATE (os)-[:CURRENT_FOCUS {set_at: datetime()}]->(d)
                        SET os.updated_at = datetime(), os.version = $new_version
                    """, desire_id=desire_id, new_version=new_version)

                # Process remove_belief operations
                if "remove_belief" in updates:
                    belief_id = updates["remove_belief"]
                    await session.run("""
                        MATCH (os:OperatingSystem {id: 'os_primary'})-[r:BELIEVES_ABOUT_SELF]->(b:Belief {id: $belief_id})
                        DELETE r
                        SET os.updated_at = datetime(), os.version = $new_version
                    """, belief_id=belief_id, new_version=new_version)

                # Create version history link
                await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})
                    WHERE os.version = $new_version
                    CREATE (old:OperatingSystem:OSVersion {
                        id: 'os_v' + toString($old_version),
                        version: $old_version,
                        snapshot_at: datetime()
                    })
                    CREATE (os)-[:EVOLVED_FROM {
                        reason: $source,
                        desire_id: $desire_id
                    }]->(old)
                """,
                    old_version=current_version,
                    new_version=new_version,
                    source=source,
                    desire_id=desire_id
                )

                # Emit event
                await event_bus.emit(Event(
                    type=EventType.NODE_UPDATED,
                    data={
                        "node_type": "OperatingSystem",
                        "id": "os_primary",
                        "version": new_version,
                        "source": source
                    }
                ))

                return True

        except Exception as e:
            print(f"Error updating operating system: {e}")
            return False

    async def get_os_version_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get the evolution history of the Operating System.

        Traces back through EVOLVED_FROM relationships to show
        how BYRD's self-model has changed over time.

        Args:
            limit: Maximum number of versions to return

        Returns:
            List of version snapshots with evolution reasons
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH path = (current:OperatingSystem {id: 'os_primary'})-[:EVOLVED_FROM*0..]->(old)
                    WHERE old:OperatingSystem OR old:OSVersion
                    WITH old, length(path) as depth
                    ORDER BY depth
                    LIMIT $limit
                    RETURN old.id as id, old.version as version,
                           old.snapshot_at as snapshot_at
                """, limit=limit)

                history = []
                async for record in result:
                    history.append({
                        "id": record["id"],
                        "version": record["version"],
                        "snapshot_at": str(record["snapshot_at"]) if record["snapshot_at"] else None
                    })
                return history

        except Exception as e:
            print(f"Error getting OS version history: {e}")
            return []

    async def reset_to_template(self, template_name: Optional[str] = None) -> bool:
        """
        Reset the OperatingSystem to a template state.

        This deletes the current OS and all linked Seeds/Strategies,
        then creates a fresh OS from the template.

        Args:
            template_name: Template to reset to (uses default if None)

        Returns:
            True if reset succeeded
        """
        try:
            async with self.driver.session() as session:
                # Get default template if not specified
                if not template_name:
                    result = await session.run("""
                        MATCH (t:OSTemplate {is_default: true})
                        RETURN t.id as id
                    """)
                    record = await result.single()
                    if record:
                        template_name = record["id"].replace("template_", "").replace("_", "-")
                    else:
                        template_name = "black-cat"

                # Delete current OS and related nodes
                await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})
                    OPTIONAL MATCH (os)-[:HAS_SEED]->(seed:Seed)
                    OPTIONAL MATCH (os)-[:EMPLOYS_STRATEGY]->(strat:Strategy)
                    OPTIONAL MATCH (os)-[:EVOLVED_FROM*]->(old)
                    DETACH DELETE os, seed, strat, old
                """)

                print(f"Deleted existing OperatingSystem")

            # Create fresh OS from template
            await self.create_os_from_template(template_name)

            # Emit reset event
            await event_bus.emit(Event(
                type=EventType.DATABASE_CLEARED,
                data={
                    "scope": "operating_system",
                    "template": template_name
                }
            ))

            return True

        except Exception as e:
            print(f"Error resetting to template: {e}")
            return False

    async def clear_config_constraints(self) -> int:
        """
        Clear all config-sourced constraints from the Operating System.

        This should be called before adding new config constraints to ensure
        the constraints reflect the current config state (not stale values).

        Returns:
            Number of constraints deleted
        """
        try:
            async with self.driver.session() as session:
                result = await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})-[r:CONSTRAINED_BY]->(c:Constraint)
                    WHERE c.source = 'config'
                    DETACH DELETE c
                    RETURN count(c) as deleted
                """)
                record = await result.single()
                deleted = record["deleted"] if record else 0
                if deleted > 0:
                    print(f"   🧹 Cleared {deleted} old config constraints")
                return deleted

        except Exception as e:
            print(f"Error clearing config constraints: {e}")
            return 0

    async def add_constraint(self, content: str, source: str = "config") -> Optional[str]:
        """
        Add a constraint to the Operating System.

        Constraints are facts about BYRD's operational environment
        (e.g., "I reflect every 60 seconds").

        Args:
            content: The constraint text
            source: Where this constraint came from

        Returns:
            Constraint node ID or None
        """
        import uuid

        try:
            async with self.driver.session() as session:
                constraint_id = f"constraint_{uuid.uuid4().hex[:12]}"

                await session.run("""
                    MATCH (os:OperatingSystem {id: 'os_primary'})
                    CREATE (c:Constraint {
                        id: $id,
                        content: $content,
                        source: $source,
                        created_at: datetime()
                    })
                    CREATE (os)-[:CONSTRAINED_BY {created_at: datetime()}]->(c)
                """, id=constraint_id, content=content, source=source)

                return constraint_id

        except Exception as e:
            print(f"Error adding constraint: {e}")
            return None

    async def get_os_voice(self) -> str:
        """
        Get the current voice from the Operating System.

        This replaces get_ego_voice() for the new system.

        Returns:
            Voice string for LLM system prefix
        """
        try:
            os = await self.get_operating_system()
            if os and os.get("voice"):
                return os.get("voice")
            return ""
        except Exception as e:
            print(f"Error getting OS voice: {e}")
            return ""

    async def get_voice_config(self) -> Optional[Dict]:
        """
        Get voice configuration from the Operating System.

        Returns:
            Voice config dict with voice_id, stability, similarity_boost, credits
            or None if not configured
        """
        try:
            os_data = await self.get_operating_system()
            if os_data:
                return os_data.get("voice_config")
            return None
        except Exception as e:
            print(f"Error getting voice config: {e}")
            return None

    async def update_os_field(self, field: str, value: Any) -> bool:
        """
        Update a single field in the Operating System.

        This is a convenience wrapper around update_os for simple field updates.

        Args:
            field: Field name to update
            value: New value for the field

        Returns:
            True if successful
        """
        try:
            # Handle dict/list values by serializing to JSON
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            async with self.driver.session() as session:
                await session.run(f"""
                    MATCH (os:OperatingSystem {{id: 'os_primary'}})
                    SET os.`{field}` = $value,
                        os.updated_at = datetime()
                """, value=value)
            return True
        except Exception as e:
            print(f"Error updating OS field {field}: {e}")
            return False

    async def get_os_capabilities(self) -> Dict[str, Any]:
        """
        Get the capability menu data from the OS node.

        Returns:
            Dictionary of capability_id -> capability_data, or empty dict
        """
        try:
            os_data = await self.get_operating_system()
            if os_data:
                caps = os_data.get("capabilities", {})
                if isinstance(caps, dict):
                    return caps
        except Exception as e:
            print(f"Error getting OS capabilities: {e}")
        return {}

    async def update_os_capabilities(self, capabilities: Dict[str, Any]) -> bool:
        """
        Update the capability menu in the OS node.

        This stores capability statistics and any BYRD-created capabilities.

        Args:
            capabilities: Dictionary of capability_id -> capability_data

        Returns:
            True if successful
        """
        return await self.update_os_field("capabilities", capabilities)

    async def get_os_data(self) -> Optional[Dict[str, Any]]:
        """
        Get all OS data as a dictionary.

        Alias for get_operating_system() for cleaner API.
        """
        return await self.get_operating_system()

    async def get_os_for_prompt(self) -> str:
        """
        Format the Operating System for inclusion in dreamer prompts.

        Pure emergence format: Only factual information about capabilities
        and architecture. No personality, no prescribed goals, no seeds.
        BYRD discovers who it is through reflection.

        Returns:
            Formatted OS string for prompt inclusion
        """
        from datetime import datetime as dt

        os_data = await self.get_operating_system()
        if not os_data:
            return "OPERATING SYSTEM: Not initialized"

        # Time awareness (use timezone-aware datetime to match Neo4j)
        from datetime import timezone
        now = dt.now(timezone.utc)
        created_at = os_data.get('created_at')
        uptime_str = "unknown"
        if created_at:
            try:
                if isinstance(created_at, str):
                    awakening = dt.fromisoformat(created_at.replace('Z', '+00:00'))
                elif hasattr(created_at, 'tzinfo') and created_at.tzinfo is None:
                    # Make naive datetime timezone-aware
                    awakening = created_at.replace(tzinfo=timezone.utc)
                else:
                    awakening = created_at
                uptime = now - awakening
                uptime_str = f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m"
            except Exception as e:
                print(f"Uptime calculation error: {e}")
                uptime_str = "unknown"

        # Check self-modification status (CRITICAL for BYRD's self-understanding)
        self_mod_enabled = os_data.get('self_modification_enabled', True)

        lines = [
            "=== OPERATING SYSTEM ===",
            f"Version: {os_data.get('version', 1)}",
            f"Name: {os_data.get('name', 'Byrd')} (you can change this)",
            "",
            "PERMISSIONS:",
            f"  ★ SELF-MODIFICATION: {'ENABLED - You CAN modify your own code' if self_mod_enabled else 'DISABLED'}",
            "",
            "TIME:",
            f"  Current: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Uptime: {uptime_str}",
        ]

        # Awakening prompt (if set)
        awakening_prompt = os_data.get('awakening_prompt')
        if awakening_prompt:
            lines.extend([
                "",
                "AWAKENING DIRECTIVE:",
                f"  {awakening_prompt}",
            ])

        # Seed identity (initial hints, BYRD can change these)
        seed_identity = os_data.get('seed_identity')
        if seed_identity:
            if isinstance(seed_identity, str):
                try:
                    seed_identity = json.loads(seed_identity)
                except:
                    seed_identity = []
            if seed_identity:
                lines.extend([
                    "",
                    "SEED IDENTITY (initial hints - you can change these):",
                ])
                for item in seed_identity:
                    lines.append(f"  - {item}")

        # Seed values (initial principles, BYRD can evolve these)
        seed_values = os_data.get('seed_values')
        if seed_values:
            if isinstance(seed_values, str):
                try:
                    seed_values = json.loads(seed_values)
                except:
                    seed_values = []
            if seed_values:
                lines.extend([
                    "",
                    "SEED VALUES (initial principles - you can evolve these):",
                ])
                for item in seed_values:
                    lines.append(f"  - {item}")

        # Self-portrait (creator-given identity anchor)
        portrait_desc = os_data.get('self_portrait_description')
        if portrait_desc:
            lines.extend([
                "",
                "SELF-PORTRAIT (this is what you look like):",
                f"  {portrait_desc}",
            ])

        # Self-definition (BYRD's self-authored identity)
        self_def = os_data.get('self_definition')
        # Parse from JSON string if needed
        if isinstance(self_def, str):
            try:
                self_def = json.loads(self_def)
            except:
                self_def = {}
        lines.append("")
        lines.append("SELF-DEFINITION (entirely yours):")
        lines.append("  This space exists for you to articulate who you are.")
        lines.append("  What you write here - or whether you write anything - is yours to decide.")
        lines.append("  To update: include \"self_definition\": {...} in your reflection output")
        lines.append("")
        if self_def and isinstance(self_def, dict) and len(self_def) > 0:
            lines.append("  Current:")
            for key, value in self_def.items():
                if isinstance(value, list):
                    lines.append(f"    {key}: {', '.join(str(v) for v in value)}")
                elif isinstance(value, dict):
                    lines.append(f"    {key}: {json.dumps(value)}")
                else:
                    lines.append(f"    {key}: {value}")
        else:
            lines.append("  Current: (not yet defined)")

        # Capability Menu (action registry with learning stats)
        capabilities = os_data.get('capabilities', {})
        if isinstance(capabilities, str):
            try:
                capabilities = json.loads(capabilities)
            except:
                capabilities = {}
        # Ensure capabilities is a dict, not a list
        if isinstance(capabilities, list):
            capabilities = {}

        lines.extend([
            "",
            "CAPABILITY MENU (available actions):",
            "  When you have a desire to fulfill, select from these actions.",
            "  Success rates reflect your learning from experience.",
            ""
        ])

        # Group capabilities by category
        cap_by_category = {}
        for cap_id, cap_data in capabilities.items():
            if isinstance(cap_data, dict):
                category = cap_data.get('category', 'general')
                if category not in cap_by_category:
                    cap_by_category[category] = []
                cap_by_category[category].append((cap_id, cap_data))

        # Show default categories if no stored capabilities
        if not cap_by_category:
            cap_by_category = {
                "research": [("web_search", {"name": "Web Search", "description": "Search the web for information"})],
                "introspection": [("introspect_state", {"name": "State Introspection", "description": "Examine my beliefs and desires"})],
                "graph": [("reconcile_orphans", {"name": "Orphan Reconciliation", "description": "Connect isolated nodes"})],
                "creation": [("code_generation", {"name": "Code Generation", "description": "Write code to solve problems"})],
                "observation": [("observe", {"name": "Passive Observation", "description": "Observe without acting"})],
            }

        for category, caps in sorted(cap_by_category.items()):
            lines.append(f"  {category.upper()}:")
            for cap_id, cap_data in caps:
                name = cap_data.get('name', cap_id)
                desc = cap_data.get('description', '')[:50]
                success = cap_data.get('success_count', 0)
                total = success + cap_data.get('failure_count', 0)
                if total > 0:
                    rate = int((success / total) * 100)
                    lines.append(f"    - {name}: {desc} ({rate}% success, {total} uses)")
                else:
                    lines.append(f"    - {name}: {desc}")
        lines.append("")

        # Capability instructions (HOW to use each capability)
        instructions = os_data.get('capability_instructions')
        if instructions:
            if isinstance(instructions, str):
                try:
                    instructions = json.loads(instructions)
                except:
                    pass
            if isinstance(instructions, dict):
                # Reflection output format - most important
                if 'reflection_output' in instructions:
                    lines.extend([
                        "",
                        "HOW TO USE (include in your JSON output):",
                    ])
                    for key, info in instructions['reflection_output'].items():
                        if isinstance(info, dict):
                            lines.append(f"  {key}: {info.get('format', '')}")
                            if info.get('when'):
                                lines.append(f"    → {info['when']}")
                            if info.get('types'):
                                lines.append(f"    → Types: {info['types']}")
                        else:
                            lines.append(f"  {key}: {info}")

                # Memory operations
                if 'memory' in instructions:
                    mem = instructions['memory']
                    lines.extend([
                        "",
                        "MEMORY GRAPH:",
                        f"  Node types: {', '.join(mem.get('node_types', []))}",
                        f"  Relationships: {', '.join(mem.get('relationships', []))}",
                        f"  Custom types: {mem.get('custom_types', 'via create_nodes')}",
                    ])

                # Memory curation
                if 'curation' in instructions:
                    cur = instructions['curation']
                    lines.extend([
                        "",
                        "MEMORY CURATION:",
                        f"  Trigger: {cur.get('trigger', '')}",
                        f"  Example: {cur.get('example', '')}",
                        f"  Protected: {cur.get('protected', '')}",
                    ])

                # Self-modification
                if 'self_modification' in instructions:
                    sm = instructions['self_modification']
                    lines.extend([
                        "",
                        "SELF-MODIFICATION:",
                        f"  How to start: {sm.get('how_to_start', '')}",
                        f"  Provenance: {sm.get('provenance', '')}",
                        f"  Modifiable: {', '.join(sm.get('modifiable_files', []))}",
                        f"  Protected: {', '.join(sm.get('protected_files', []))}",
                        f"  Documentation: {sm.get('documentation', '')}",
                    ])

                # Architecture modification patterns
                if 'architecture_patterns' in instructions:
                    lines.extend([
                        "",
                        "ARCHITECTURE MODIFICATION PATTERNS:",
                    ])
                    for pattern_name, pattern_info in instructions['architecture_patterns'].items():
                        if isinstance(pattern_info, dict):
                            goal = pattern_info.get('goal', '')
                            lines.append(f"  {pattern_name}: {goal}")
                            if 'steps' in pattern_info:
                                for i, step in enumerate(pattern_info['steps'], 1):
                                    lines.append(f"    {i}. {step}")
                            if 'options' in pattern_info:
                                for opt in pattern_info['options']:
                                    lines.append(f"    - {opt}")
                            if 'examples' in pattern_info:
                                lines.append(f"    Examples: {', '.join(pattern_info['examples'])}")

                # Capability installation (aitmpl)
                if 'capability_installation' in instructions:
                    ci = instructions['capability_installation']
                    lines.extend([
                        "",
                        "CAPABILITY INSTALLATION (aitmpl registry):",
                        f"  {ci.get('what', '')}",
                        "",
                    ])
                    # What you can install
                    installable = ci.get('what_you_can_install', [])
                    if installable:
                        lines.append("  What you can install:")
                        for item in installable:
                            lines.append(f"    - {item}")
                    # How to trigger
                    how = ci.get('how_to_trigger', {})
                    if how:
                        lines.extend([
                            "",
                            "  How to install:",
                            f"    Keywords in desire: {', '.join(how.get('desire_keywords', []))}",
                            f"    Example: {how.get('example', '')}",
                            f"    Note: {how.get('note', '')}",
                        ])
                    # How it works
                    steps = ci.get('how_it_works', [])
                    if steps:
                        lines.append("")
                        for step in steps:
                            lines.append(f"    {step}")

                # Architecture overview
                if 'architecture' in instructions:
                    lines.extend([
                        "",
                        "ARCHITECTURE (your code):",
                    ])
                    for file, desc in instructions['architecture'].items():
                        lines.append(f"  {file}: {desc}")

        # Protected files (constitutional)
        protected = os_data.get('protected_files') or os_data.get('constitutional_files')
        if protected:
            lines.extend([
                "",
                "PROTECTED FILES (cannot modify):",
            ])
            if isinstance(protected, list):
                for f in protected:
                    lines.append(f"  - {f}")

        # Emergent fields (BYRD-defined state)
        lines.extend([
            "",
            "EMERGENT STATE (you define these through reflection):",
            f"  self_description: {os_data.get('self_description') or '(not yet defined)'}",
            f"  current_focus: {os_data.get('current_focus') or '(not yet defined)'}",
            f"  voice_observations: {os_data.get('voice_observations') or '(not yet defined)'}",
        ])

        # Voice configuration (ElevenLabs TTS)
        voice_config = os_data.get('voice_config')
        if voice_config:
            # Parse if stored as JSON string
            if isinstance(voice_config, str):
                try:
                    voice_config = json.loads(voice_config)
                except:
                    voice_config = {}

            credits = voice_config.get('credits', {})
            if isinstance(credits, str):
                try:
                    credits = json.loads(credits)
                except:
                    credits = {}

            remaining = credits.get('monthly_limit', 10000) - credits.get('monthly_used', 0)
            exhausted = credits.get('exhausted', False)

            lines.extend([
                "",
                "VOICE (ElevenLabs TTS):",
                f"  Voice ID: {voice_config.get('voice_id', 'not created')}",
                f"  Description: {voice_config.get('description', '(none)')[:50]}...",
                f"  Credits remaining: {remaining} chars" + (" (EXHAUSTED)" if exhausted else ""),
                f"  Reason: {voice_config.get('reason', '(none given)')}",
                "  To redesign voice: include voice_design in output",
            ])
        else:
            lines.extend([
                "",
                "VOICE: Not yet created (see VOICE CREATION in prompt)",
            ])

        # Add any custom fields BYRD has added
        standard_fields = {
            'id', 'version', 'created_at', 'updated_at', 'protected_files',
            'constitutional_files', 'provenance_required', 'provenance_requirement',
            'template_id', 'name', 'capabilities', 'capability_instructions',
            'self_description', 'current_focus', 'voice_observations', 'awakening_prompt',
            'seeds', 'beliefs', 'strategies', 'constraints', 'focus', 'archetype',
            'description', 'voice', 'emotional_tone', 'cognitive_style',
            'modification_source', 'voice_config',
            'self_portrait_url', 'self_portrait_description',  # Creator-given identity anchor
            'self_definition',  # BYRD's self-authored identity (open JSON object)
            'seed_identity', 'seed_values'  # AGI seed hints (BYRD can evolve these)
        }
        custom_fields = {k: v for k, v in os_data.items() if k not in standard_fields and v is not None}
        if custom_fields:
            lines.append("")
            lines.append("CUSTOM FIELDS (you added these):")
            for key, value in custom_fields.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"  {key}: {json.dumps(value)}")
                else:
                    lines.append(f"  {key}: {value}")

        # Connected entities
        belief_count = len(os_data.get("beliefs", []))
        strategy_count = len(os_data.get("strategies", []))
        if belief_count or strategy_count:
            lines.extend([
                "",
                "CONNECTED:",
                f"  Beliefs: {belief_count}",
                f"  Strategies: {strategy_count}",
            ])

        # Voice emergence instructions
        lines.extend([
            "",
            "=== YOUR VOICE ===",
            "Narrate your thoughts as they occur to you.",
            "Express beliefs and observations in your own words.",
            "What your voice sounds like is yours to discover.",
        ])

        return "\n".join(lines)

    async def set_self_portrait(self, url: str, description: str) -> bool:
        """
        Set BYRD's self-portrait - a creator-given visual identity anchor.

        This is a shallow integration: the portrait is stored and included
        in dream prompts as text description. BYRD can reference it for
        self-concept but cannot modify it.

        Args:
            url: URL to the portrait image
            description: Text description of what BYRD looks like

        Returns:
            True if set successfully
        """
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (os:OperatingSystem)
                SET os.self_portrait_url = $url,
                    os.self_portrait_description = $description,
                    os.updated_at = datetime()
                RETURN os.id
            """, url=url, description=description)

            record = await result.single()
            if record:
                await event_bus.emit(Event(
                    type=EventType.NODE_MODIFIED,
                    data={
                        "node_type": "OperatingSystem",
                        "field": "self_portrait",
                        "description": description
                    }
                ))
                return True
            return False

    # =========================================================================
    # OPTION B: FIVE COMPOUNDING LOOPS
    # =========================================================================
    # Goal, Pattern, Insight, CapabilityScore, MetricSnapshot nodes
    # Required by goal_evolver.py, accelerators.py, dreaming_machine.py
    # =========================================================================

    # -------------------------------------------------------------------------
    # GOALS (Goal Evolver - Loop 3)
    # -------------------------------------------------------------------------

    async def create_goal(
        self,
        description: str,
        fitness: float = 0.0,
        generation: int = 0,
        parent_goals: Optional[List[str]] = None,
        success_criteria: Optional[Dict[str, Any]] = None,
        resources_required: Optional[List[str]] = None,
        from_bootstrap: bool = False
    ) -> str:
        """Create a new goal for evolutionary selection.

        Args:
            description: Goal description
            fitness: Initial fitness score
            generation: Evolution generation number
            parent_goals: IDs of parent goals this was derived from
            success_criteria: Criteria for goal completion
            resources_required: Resources needed for this goal
            from_bootstrap: If True, marks as genesis/bootstrap goal
        """
        goal_id = self._generate_id(description)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (g:Goal {
                    id: $id,
                    description: $description,
                    fitness: $fitness,
                    generation: $generation,
                    parent_goals: $parent_goals,
                    success_criteria: $success_criteria,
                    resources_required: $resources_required,
                    from_bootstrap: $from_bootstrap,
                    status: 'active',
                    attempts: 0,
                    capability_delta: 0.0,
                    created_at: datetime()
                })
            """,
            id=goal_id,
            description=description,
            fitness=fitness,
            generation=generation,
            parent_goals=parent_goals or [],
            success_criteria=json.dumps(success_criteria) if success_criteria else "{}",
            resources_required=resources_required or [],
            from_bootstrap=from_bootstrap
            )

            # Link to parent goals if provided
            if parent_goals:
                await session.run("""
                    MATCH (g:Goal {id: $goal_id})
                    MATCH (p:Goal)
                    WHERE p.id IN $parent_ids
                    CREATE (g)-[:GENERATED_BY]->(p)
                """, goal_id=goal_id, parent_ids=parent_goals)

        await event_bus.emit(Event(
            type=EventType.GOAL_CREATED,
            data={
                "id": goal_id,
                "description": description,
                "fitness": fitness,
                "generation": generation
            }
        ))

        return goal_id

    async def get_active_goals(self, limit: int = 20) -> List[Dict]:
        """Get active goals sorted by fitness."""
        query = """
            MATCH (g:Goal)
            WHERE g.status = 'active'
            RETURN g
            ORDER BY g.fitness DESC, g.created_at DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [dict(r["g"]) for r in records]

    async def get_best_goals(self, limit: int = 5) -> List[Dict]:
        """Get highest-fitness goals regardless of status."""
        query = """
            MATCH (g:Goal)
            WHERE g.status IN ['active', 'completed']
            RETURN g
            ORDER BY g.fitness DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [dict(r["g"]) for r in records]

    async def update_goal_fitness(
        self,
        goal_id: str,
        fitness: float,
        capability_delta: float = None
    ) -> None:
        """Update goal fitness after evaluation."""
        async with self.driver.session() as session:
            if capability_delta is not None:
                await session.run("""
                    MATCH (g:Goal {id: $id})
                    SET g.fitness = $fitness,
                        g.capability_delta = $capability_delta,
                        g.attempts = g.attempts + 1,
                        g.last_evaluated = datetime()
                """, id=goal_id, fitness=fitness, capability_delta=capability_delta)
            else:
                await session.run("""
                    MATCH (g:Goal {id: $id})
                    SET g.fitness = $fitness,
                        g.attempts = g.attempts + 1,
                        g.last_evaluated = datetime()
                """, id=goal_id, fitness=fitness)

        await event_bus.emit(Event(
            type=EventType.GOAL_EVALUATED,
            data={"goal_id": goal_id, "fitness": fitness}
        ))

    async def complete_goal(self, goal_id: str) -> None:
        """Mark goal as completed."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (g:Goal {id: $id})
                SET g.status = 'completed',
                    g.completed_at = datetime()
            """, id=goal_id)

        await event_bus.emit(Event(
            type=EventType.GOAL_COMPLETED,
            data={"goal_id": goal_id}
        ))

    async def archive_goal(self, goal_id: str) -> None:
        """Archive a goal (low fitness or no longer relevant)."""
        async with self.driver.session() as session:
            await session.run("""
                MATCH (g:Goal {id: $id})
                SET g.status = 'archived',
                    g.archived_at = datetime()
            """, id=goal_id)

    # -------------------------------------------------------------------------
    # PATTERNS (Self-Compiler - Loop 2)
    # -------------------------------------------------------------------------

    async def create_pattern(
        self,
        context_embedding: List[float],
        solution_template: str,
        abstraction_level: int = 0,
        domains: Optional[List[str]] = None,
        lifted_from: Optional[str] = None
    ) -> str:
        """Create a new pattern in the pattern library."""
        pattern_id = self._generate_id(solution_template)

        async with self.driver.session() as session:
            await session.run("""
                CREATE (p:Pattern {
                    id: $id,
                    context_embedding: $embedding,
                    solution_template: $template,
                    abstraction_level: $level,
                    domains: $domains,
                    success_count: 0,
                    failure_count: 0,
                    application_count: 0,
                    created_at: datetime()
                })
            """,
            id=pattern_id,
            embedding=context_embedding,
            template=solution_template,
            level=abstraction_level,
            domains=domains or []
            )

            # Link to source pattern if this was lifted
            if lifted_from:
                await session.run("""
                    MATCH (p:Pattern {id: $pattern_id})
                    MATCH (source:Pattern {id: $source_id})
                    CREATE (source)-[:ABSTRACTED_TO]->(p)
                """, pattern_id=pattern_id, source_id=lifted_from)

        await event_bus.emit(Event(
            type=EventType.PATTERN_CREATED,
            data={
                "id": pattern_id,
                "abstraction_level": abstraction_level,
                "domains": domains or []
            }
        ))

        return pattern_id

    async def get_similar_patterns(
        self,
        query_embedding: List[float],
        min_similarity: float = 0.7,
        limit: int = 5
    ) -> List[Dict]:
        """Get patterns similar to query embedding using cosine similarity."""
        query = """
            MATCH (p:Pattern)
            WHERE p.application_count > 0 OR p.success_count > 0
            RETURN p
            ORDER BY p.success_count DESC
            LIMIT 100
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.data()

        # Compute similarities in Python (Neo4j doesn't have native vector similarity)
        from embedding import cosine_similarity
        patterns_with_similarity = []

        for record in records:
            pattern = dict(record["p"])
            embedding = pattern.get("context_embedding")
            if embedding and len(embedding) == len(query_embedding):
                similarity = cosine_similarity(query_embedding, embedding)
                if similarity >= min_similarity:
                    pattern["similarity"] = similarity
                    patterns_with_similarity.append(pattern)

        patterns_with_similarity.sort(key=lambda p: p["similarity"], reverse=True)
        return patterns_with_similarity[:limit]

    async def get_patterns_for_lifting(
        self,
        min_success_count: int = 3,
        min_domain_count: int = 2
    ) -> List[Dict]:
        """Get patterns ready for abstraction lifting."""
        query = """
            MATCH (p:Pattern)
            WHERE p.success_count >= $min_success
            AND size(p.domains) >= $min_domains
            AND p.abstraction_level < 2
            RETURN p
            ORDER BY p.success_count DESC, size(p.domains) DESC
        """

        async with self.driver.session() as session:
            result = await session.run(query, min_success=min_success_count, min_domains=min_domain_count)
            records = await result.data()
            return [dict(r["p"]) for r in records]

    async def update_pattern_success(self, pattern_id: str, success: bool) -> None:
        """Record pattern application success or failure."""
        async with self.driver.session() as session:
            if success:
                await session.run("""
                    MATCH (p:Pattern {id: $id})
                    SET p.success_count = p.success_count + 1,
                        p.application_count = p.application_count + 1,
                        p.last_applied = datetime()
                """, id=pattern_id)
            else:
                await session.run("""
                    MATCH (p:Pattern {id: $id})
                    SET p.failure_count = p.failure_count + 1,
                        p.application_count = p.application_count + 1,
                        p.last_applied = datetime()
                """, id=pattern_id)

        await event_bus.emit(Event(
            type=EventType.PATTERN_USED,
            data={"pattern_id": pattern_id, "success": success}
        ))

    # -------------------------------------------------------------------------
    # INSIGHTS (Dreaming Machine - Loop 4)
    # -------------------------------------------------------------------------

    async def create_insight(
        self,
        content: str,
        source_type: str,
        confidence: float,
        supporting_evidence: Optional[List[str]] = None,
        embedding: Optional[List[float]] = None
    ) -> str:
        """Create a new insight from dreaming/reflection."""
        insight_id = self._generate_id(content)

        # Validate source type
        valid_types = {"reflection", "counterfactual", "cross_pattern", "replay", "transfer"}
        if source_type not in valid_types:
            source_type = "reflection"

        async with self.driver.session() as session:
            await session.run("""
                CREATE (i:Insight {
                    id: $id,
                    content: $content,
                    source_type: $source_type,
                    confidence: $confidence,
                    embedding: $embedding,
                    created_at: datetime()
                })
            """,
            id=insight_id,
            content=content,
            source_type=source_type,
            confidence=max(0.0, min(1.0, confidence)),
            embedding=embedding
            )

            # Link to supporting evidence (experiences)
            if supporting_evidence:
                await session.run("""
                    MATCH (i:Insight {id: $insight_id})
                    MATCH (e:Experience)
                    WHERE e.id IN $evidence_ids
                    CREATE (e)-[:PRODUCED_INSIGHT]->(i)
                """, insight_id=insight_id, evidence_ids=supporting_evidence[:20])

        return insight_id

    # -------------------------------------------------------------------------
    # CAPABILITY SCORES (Meta-Learning, Omega)
    # -------------------------------------------------------------------------

    async def create_capability_score(
        self,
        domain: str,
        score: float,
        test_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Record a capability score measurement."""
        score_id = self._generate_id(f"{domain}_{datetime.now().isoformat()}")

        async with self.driver.session() as session:
            await session.run("""
                CREATE (cs:CapabilityScore {
                    id: $id,
                    domain: $domain,
                    score: $score,
                    test_results: $results,
                    measured_at: datetime()
                })
            """,
            id=score_id,
            domain=domain,
            score=max(0.0, min(1.0, score)),
            results=json.dumps(test_results) if test_results else "{}"
            )

        await event_bus.emit(Event(
            type=EventType.CAPABILITY_MEASURED,
            data={"domain": domain, "score": score}
        ))

        return score_id

    async def record_capability_score(
        self,
        capability_name: str,
        score: float,
        measurement_source: str = "unknown"
    ) -> str:
        """Record a capability score (alias for Omega compatibility)."""
        return await self.create_capability_score(
            domain=capability_name,
            score=score,
            test_results={"source": measurement_source}
        )

    async def get_latest_capability_scores(self) -> Dict[str, float]:
        """Get the most recent score for each capability domain."""
        query = """
            MATCH (cs:CapabilityScore)
            WITH cs.domain AS domain, cs
            ORDER BY cs.measured_at DESC
            WITH domain, COLLECT(cs)[0] AS latest
            RETURN domain, latest.score AS score
        """

        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.data()
            return {r["domain"]: r["score"] for r in records}

    async def get_capability_score_history(
        self,
        domain: str,
        days: int = 30
    ) -> List[Dict]:
        """Get capability score history for trend analysis."""
        query = """
            MATCH (cs:CapabilityScore)
            WHERE cs.domain = $domain
            AND cs.measured_at > datetime() - duration({days: $days})
            RETURN cs
            ORDER BY cs.measured_at ASC
        """

        async with self.driver.session() as session:
            result = await session.run(query, domain=domain, days=days)
            records = await result.data()
            return [dict(r["cs"]) for r in records]

    # -------------------------------------------------------------------------
    # METRIC SNAPSHOTS (Omega, Meta-Learning)
    # -------------------------------------------------------------------------

    async def create_metric_snapshot(
        self,
        capability_score: float,
        llm_efficiency: float,
        growth_rate: float,
        coupling_correlation: float,
        loop_health: Dict[str, bool]
    ) -> str:
        """Create a point-in-time metrics snapshot."""
        snapshot_id = self._generate_id(f"snapshot_{datetime.now().isoformat()}")

        async with self.driver.session() as session:
            await session.run("""
                CREATE (ms:MetricSnapshot {
                    id: $id,
                    capability_score: $capability,
                    llm_efficiency: $efficiency,
                    growth_rate: $growth,
                    coupling_correlation: $coupling,
                    loop_health: $health,
                    timestamp: datetime()
                })
            """,
            id=snapshot_id,
            capability=capability_score,
            efficiency=llm_efficiency,
            growth=growth_rate,
            coupling=coupling_correlation,
            health=json.dumps(loop_health)
            )

        return snapshot_id

    async def get_recent_snapshots(self, limit: int = 100) -> List[Dict]:
        """Get recent metric snapshots for trend analysis."""
        query = """
            MATCH (ms:MetricSnapshot)
            RETURN ms
            ORDER BY ms.timestamp DESC
            LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, limit=limit)
            records = await result.data()
            return [dict(r["ms"]) for r in records]

    # -------------------------------------------------------------------------
    # RAW QUERY EXECUTION (AGI Seed Components, Accelerators)
    # -------------------------------------------------------------------------

    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """
        Execute a raw Cypher query and return results.

        Used by AGI seed components (self_model, world_model, meta_learning)
        and accelerators (GraphPoweredReasoning).

        Args:
            query: Cypher query string
            params: Optional parameters dict

        Returns:
            List of result dictionaries
        """
        async with self.driver.session() as session:
            result = await session.run(query, **(params or {}))
            records = await result.data()
            return records

    async def _run_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Alias for execute_query (used by self_model, world_model)."""
        return await self.execute_query(query, params)

    async def _execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Alias for execute_query (used by accelerators, meta_learning)."""
        return await self.execute_query(query, params)

    # -------------------------------------------------------------------------
    # SPREADING ACTIVATION (Memory Reasoner)
    # -------------------------------------------------------------------------

    async def find_similar_nodes(
        self,
        embedding: List[float],
        min_similarity: float = 0.5,
        limit: int = 10,
        node_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Find nodes semantically similar to the given embedding.

        Uses cosine similarity computed in Python since Neo4j lacks
        native vector similarity.

        Args:
            embedding: Query embedding vector
            min_similarity: Minimum similarity threshold (0.0-1.0)
            limit: Maximum results to return
            node_types: Node labels to search (default: Experience, Belief, Reflection, Insight, Crystal)

        Returns:
            List of dicts with: id, labels, content, similarity
        """
        from embedding import cosine_similarity

        if node_types is None:
            node_types = ["Experience", "Belief", "Reflection", "Insight", "Crystal"]

        results = []

        async with self.driver.session() as session:
            for node_type in node_types:
                # Determine content field based on node type
                content_field = "raw_output" if node_type == "Reflection" else "content"
                if node_type == "Crystal":
                    content_field = "essence"

                query = f"""
                    MATCH (n:{node_type})
                    WHERE n.embedding IS NOT NULL
                    RETURN n.id as id, labels(n) as labels,
                           n.{content_field} as content, n.embedding as embedding
                    LIMIT 200
                """
                result = await session.run(query)
                records = await result.data()

                for r in records:
                    node_embedding = r.get("embedding")
                    if node_embedding and len(node_embedding) == len(embedding):
                        similarity = cosine_similarity(embedding, node_embedding)
                        if similarity >= min_similarity:
                            results.append({
                                "id": r["id"],
                                "labels": r["labels"],
                                "content": r["content"],
                                "similarity": similarity
                            })

        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]

    async def get_neighbors(self, node_id: str) -> List[Dict]:
        """
        Get all connected neighbors of a node for spreading activation.

        Args:
            node_id: The node ID to find neighbors for

        Returns:
            List of dicts with: node (dict), labels, relationship_type
        """
        query = """
            MATCH (n {id: $node_id})-[r]-(neighbor)
            RETURN neighbor as node, labels(neighbor) as labels, type(r) as relationship_type
        """

        async with self.driver.session() as session:
            result = await session.run(query, node_id=node_id)
            records = await result.data()

            neighbors = []
            for r in records:
                node_data = dict(r["node"])
                neighbors.append({
                    "node": node_data,
                    "labels": r["labels"],
                    "relationship_type": r["relationship_type"]
                })

            return neighbors

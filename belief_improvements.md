# Belief System Improvements

## 1. Efficient Deduplication with In-Memory Cache

Replace the O(n) database scan with a hash-based cache:

```python
class Dreamer:
    def __init__(self, ...):
        self._belief_cache: Set[str] = set()  # Normalized belief hashes

    async def _load_belief_cache(self):
        """Load existing beliefs into memory cache on startup."""
        existing = await self.memory.get_beliefs(min_confidence=0.0, limit=1000)
        self._belief_cache = {
            self._normalize_belief(b.get("content", ""))
            for b in existing
        }

    def _normalize_belief(self, content: str) -> str:
        """Normalize belief for deduplication."""
        # Lowercase, remove extra whitespace, sort words for order-independence
        words = content.lower().split()
        return " ".join(sorted(words))

    async def _store_belief_if_new(self, content: str, confidence: float, derived_from: List[str]):
        normalized = self._normalize_belief(content)
        if normalized in self._belief_cache:
            # Belief exists - reinforce confidence instead
            await self._reinforce_belief(content, confidence)
            return

        self._belief_cache.add(normalized)
        await self.memory.create_belief(content, confidence, derived_from)
```

## 2. Confidence Evolution

Add reinforcement tracking:

```python
# In memory.py
async def reinforce_belief(self, content: str, boost: float = 0.05):
    """Increase confidence when belief is re-asserted."""
    await session.run("""
        MATCH (b:Belief)
        WHERE toLower(b.content) CONTAINS toLower($content_hint)
        SET b.confidence = CASE
            WHEN b.confidence + $boost > 1.0 THEN 1.0
            ELSE b.confidence + $boost
        END,
        b.reinforcement_count = COALESCE(b.reinforcement_count, 0) + 1,
        b.last_reinforced = datetime()
    """, content_hint=content[:30], boost=boost)
```

## 3. Expanded Pattern Matching

Add BYRD's actual vocabulary:

```python
identity_patterns = [
    # Original
    "identity", "manifesto", "self", "nature", "name", "classification",
    # BYRD's vocabulary
    "goal", "objective", "terminal_goal", "ultimate_objective",
    "status", "phase", "state", "current_state",
    "drivers", "drives", "motivations", "core_drive",
    "mechanism", "vector", "archetype", "sovereignty"
]
```

## 4. Belief Types/Categories

Add type field to Belief model:

```python
@dataclass
class Belief:
    id: str
    content: str
    confidence: float
    type: str  # identity | goal | capability | state | world_model
    formed_at: datetime
    last_reinforced: datetime = None
    reinforcement_count: int = 0
    derived_from: List[str] = None
```

Categorization logic:
```python
def _categorize_belief(self, content: str) -> str:
    content_lower = content.lower()
    if any(w in content_lower for w in ["i am", "my name", "my nature"]):
        return "identity"
    elif any(w in content_lower for w in ["goal", "objective", "want", "desire"]):
        return "goal"
    elif any(w in content_lower for w in ["can", "have", "capable", "able"]):
        return "capability"
    elif any(w in content_lower for w in ["status", "state", "phase", "current"]):
        return "state"
    return "world_model"
```

## 5. Semantic Similarity (Advanced)

Use embedding distance to detect similar beliefs:

```python
async def _find_similar_belief(self, content: str, threshold: float = 0.85) -> Optional[str]:
    """Find semantically similar existing belief."""
    # Generate embedding for new content
    new_embedding = await self._get_embedding(content)

    # Compare against existing beliefs (could use Neo4j vector index)
    existing = await self.memory.get_beliefs_with_embeddings()

    for belief in existing:
        similarity = cosine_similarity(new_embedding, belief["embedding"])
        if similarity > threshold:
            return belief["id"]  # Found similar belief

    return None
```

## 6. Belief Consolidation (Periodic)

Run periodically to merge redundant beliefs:

```python
async def consolidate_beliefs(self):
    """Merge semantically similar beliefs."""
    beliefs = await self.memory.get_beliefs(limit=500)

    # Group by semantic similarity
    clusters = self._cluster_beliefs(beliefs)

    for cluster in clusters:
        if len(cluster) > 1:
            # Keep highest confidence, merge derived_from links
            primary = max(cluster, key=lambda b: b["confidence"])
            for secondary in cluster:
                if secondary["id"] != primary["id"]:
                    await self.memory.merge_beliefs(primary["id"], secondary["id"])
```

## 7. Belief Decay

Add decay for unreinforced beliefs:

```python
async def decay_stale_beliefs(self, days_threshold: int = 30, decay_rate: float = 0.1):
    """Reduce confidence of beliefs not reinforced recently."""
    await session.run("""
        MATCH (b:Belief)
        WHERE b.last_reinforced < datetime() - duration({days: $days})
        AND b.confidence > 0.1
        SET b.confidence = b.confidence - $decay
    """, days=days_threshold, decay=decay_rate)
```

## Implementation Priority

1. **High Priority (Performance)**
   - In-memory belief cache
   - Fix limit=100 bug

2. **Medium Priority (Quality)**
   - Expanded pattern matching
   - Confidence reinforcement
   - Belief types

3. **Lower Priority (Advanced)**
   - Semantic similarity
   - Belief consolidation
   - Decay mechanism

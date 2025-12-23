---
title: Memory Schema (Neo4j)
link: memory-schema
type: metadata
ontological_relations: []
tags: [neo4j, graph, schema, nodes, relationships, reflection]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T03:00:00Z
uuid: f1a23b40-1234-4567-89ab-cdef01234567
---

## Node Types

### Experience
What happened in the system.
```cypher
(:Experience {
  id: string,
  timestamp: datetime,
  content: string,
  embedding: [float],
  type: string  // Examples: interaction, observation, action, reflection, research, system
})
```

### Belief
What BYRD thinks is true.
```cypher
(:Belief {
  id: string,
  content: string,
  confidence: float,  // 0-1
  formed_at: datetime,
  embedding: [float]
})
```

### Desire
What BYRD wants (legacy - new system uses Reflection).
```cypher
(:Desire {
  id: string,
  description: string,
  type: string,       // Examples: knowledge, capability, goal, exploration
  intensity: float,   // 0-1
  status: string,     // Examples: active, fulfilled, dormant, needs_reflection
  formed_at: datetime,
  fulfilled: boolean,
  fulfilled_at: datetime
})
```

### Reflection (NEW - Emergence-Compliant)
Raw output from BYRD's reflection, stored in BYRD's own vocabulary.
```cypher
(:Reflection {
  id: string,
  raw_output: string,    // JSON of whatever BYRD produced
  timestamp: datetime
})
-[:REFLECTS_ON]->(:Experience)  // Source experiences
```

**Python dataclass:**
```python
@dataclass
class Reflection:
    id: str
    raw_output: Dict[str, Any]  # BYRD's vocabulary, not ours
    timestamp: datetime
    source_experiences: List[str] = field(default_factory=list)
```

### Capability
What BYRD can do.
```cypher
(:Capability {
  id: string,
  name: string,
  description: string,
  type: string,       // Examples: innate, mcp, plugin, skill
  config: string,     // JSON
  active: boolean,
  acquired_at: datetime
})
```

### Modification
Self-modification records.
```cypher
(:Modification {
  id: string,
  target_file: string,
  target_component: string,
  change_description: string,
  change_diff: string,
  checkpoint_id: string,
  success: boolean,
  timestamp: datetime
})
```

## Key Relationships

| Relationship | Purpose |
|-------------|---------|
| `RELATES_TO` | Semantic connections (weighted) |
| `DERIVED_FROM` | Belief ← Experience |
| `REFLECTS_ON` | Reflection ← Experience (provenance) |
| `SUPPORTS` | Causal/logical support |
| `CONTRADICTS` | Logical contradiction |
| `FULFILLS` | Capability/Research → Desire |
| `REQUIRES` | Desire → Capability needed |
| `MOTIVATED_BY` | Modification → Desire (provenance) |

## Key Methods

### record_reflection()
Store BYRD's raw reflection output without categorization:
```python
async def record_reflection(
    self,
    raw_output: Dict[str, Any],
    source_experience_ids: List[str]
) -> str:
    """Store reflection in BYRD's own vocabulary."""
```

### get_recent_reflections()
Retrieve recent reflections for pattern detection:
```python
async def get_recent_reflections(self, limit: int = 10) -> List[Dict]:
    """Get recent reflections with raw output."""
```

### get_reflection_patterns()
Analyze BYRD's emerging vocabulary:
```python
async def get_reflection_patterns(self, limit: int = 100) -> Dict[str, int]:
    """Analyze what keys BYRD uses in reflections."""
```

## Key Queries

```cypher
// Recent reflections with source experiences
MATCH (r:Reflection)-[:REFLECTS_ON]->(e:Experience)
RETURN r, collect(e) as sources
ORDER BY r.timestamp DESC
LIMIT 10

// Analyze BYRD's vocabulary (what keys appear in reflections)
MATCH (r:Reflection)
RETURN r.raw_output
ORDER BY r.timestamp DESC

// Unfulfilled desires by intensity (legacy)
MATCH (d:Desire {fulfilled: false})
RETURN d ORDER BY d.intensity DESC

// Trace modification provenance
MATCH (m:Modification)-[:MOTIVATED_BY]->(d:Desire)
OPTIONAL MATCH (d)<-[:GENERATED]-(dream:Experience)
RETURN m, d, dream
```

## Emergence Principle Notes

Type documentation uses "Examples:" rather than exhaustive lists to avoid implying a closed set. BYRD can use any string for types - the examples are just common patterns.

The Reflection node stores raw JSON output. Whatever structure BYRD produces is preserved. Pattern analysis happens at the Seeker level, not in storage.

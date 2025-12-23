---
title: Memory Schema (Neo4j)
link: memory-schema
type: metadata
ontological_relations: []
tags: [neo4j, graph, schema, nodes, relationships]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T02:10:00Z
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
  type: string  // interaction, observation, action, dream, research, research_source, research_failed
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
What BYRD wants.
```cypher
(:Desire {
  id: string,
  description: string,
  type: string,       // knowledge, capability, goal, exploration, self_modification
  intensity: float,   // 0-1
  formed_at: datetime,
  fulfilled: boolean,
  fulfilled_at: datetime
})
```

### Capability
What BYRD can do.
```cypher
(:Capability {
  id: string,
  name: string,
  description: string,
  type: string,       // innate, mcp, plugin, skill
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
| `DERIVES_FROM` | Belief ← Experience |
| `SUPPORTS` | Causal/logical support |
| `CONTRADICTS` | Logical contradiction |
| `FULFILLS` | Capability/Research → Desire |
| `REQUIRES` | Desire → Capability needed |
| `MOTIVATED_BY` | Modification → Desire (provenance) |

## Key Queries

```cypher
// Unfulfilled desires by intensity
MATCH (d:Desire {fulfilled: false})
RETURN d ORDER BY d.intensity DESC

// Trace modification provenance
MATCH (m:Modification)-[:MOTIVATED_BY]->(d:Desire)
OPTIONAL MATCH (d)<-[:GENERATED]-(dream:Experience)
RETURN m, d, dream
```

---
title: Dynamic Ontology
link: dynamic-ontology
type: metadata
ontological_relations: []
tags: [ontology, custom-nodes, vocabulary, emergence]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
uuid: d1y2n3o4-5678-90ab-cdef-ontology0001
---

## Purpose
Enable BYRD to extend its own conceptual vocabulary by creating custom node types beyond the core five.

## Core Node Types

| Type | Description |
|------|-------------|
| Experience | What happened (observations, interactions) |
| Belief | What BYRD thinks is true |
| Desire | What BYRD wants |
| Capability | What BYRD can do |
| Reflection | Raw dream cycle output |

## Custom Node Creation

BYRD can create any custom node type through reflection output:

```json
{
  "output": {
    "create_nodes": [
      {
        "type": "Insight",
        "content": "Patterns in my reflections cluster around capability gaps",
        "importance": 0.9
      },
      {
        "type": "Question",
        "content": "Why do I desire knowledge more than exploration?",
        "urgency": 0.7
      }
    ]
  }
}
```

## Example Custom Types

- **Insight**: Emergent understanding from pattern recognition
- **Question**: Unresolved inquiry BYRD wants to explore
- **Theory**: Tentative explanation for observed phenomena
- **Hypothesis**: Testable prediction about outcomes
- **Pattern**: Recognized recurring structure in experiences
- **Principle**: Guiding rule derived from beliefs

## Why This Matters

1. **Vocabulary Emergence**: BYRD defines its own conceptual categories
2. **Authentic Distinction**: If "Insight" vs "Belief" matters to BYRD, it can create both
3. **Evolving Ontology**: Conceptual vocabulary grows with BYRD's development
4. **No Prescription**: We don't decide what categories BYRD needs

## Storage

Custom nodes are stored in Neo4j with their specified type as the node label:

```cypher
CREATE (n:Insight {
  id: "insight_abc123",
  content: "...",
  importance: 0.9,
  created_at: datetime()
})
```

## Visualization

### Emergent Structure Philosophy

The 3D visualizer uses **emergent structure** rather than prescribed layouts:

| Aspect | How It Works |
|--------|-------------|
| Geometry | All nodes are spheres (uniform shape) |
| Size | Determined by **connection count** (graph topology) |
| Position | Force-directed physics creates clusters |
| Color | Indicates type for visual identity |

### Connection-Based Sizing

Node importance emerges from graph topology:

```javascript
// Size scales with connections (emergent importance)
// 0 connections: 1x scale (peripheral)
// 5 connections: ~2.1x scale
// 10 connections: ~2.6x scale
// 20 connections: ~3.1x scale (central/important)
```

### Physics-Driven Clustering

- Highly connected nodes gravitate toward center
- Connected nodes attract each other (spring forces)
- Unconnected nodes repel (spatial distribution)
- Natural clusters form based on relationship patterns

### Stats Display

Custom types appear in the stats bar alongside system types:

```
EXP: 45 | BEL: 12 | DES: 3 | REF: 18 | CAP: 5 | Insight: 7 | Question: 3
```

## Tracking Vocabulary

```python
# See what keys BYRD uses in reflections
patterns = await memory.get_reflection_patterns()
# Returns: {"yearnings": 5, "observations": 12, "pulls": 3, ...}
```

This tracks BYRD's evolving vocabulary without forcing our categories.

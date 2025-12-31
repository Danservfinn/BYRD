# Goal Cascade Module

## Overview

The Goal Cascade system decomposes complex, multi-phase tasks into phased desire trees with Neo4j persistence.

## Key Components

### GoalCascade (`goal_cascade.py`)

Main orchestrator for complex task decomposition.

**Phases:**
1. **RESEARCH** - Understand the domain
2. **DATA_ACQUISITION** - Obtain necessary data/APIs
3. **TOOL_BUILDING** - Create required capabilities
4. **INTEGRATION** - Combine into solution
5. **VALIDATION** - Verify with human feedback

**Key Methods:**
- `decompose(goal, requester)` - Analyze goal and generate phased tree
- `execute_phase(phase, tree)` - Execute a phase (may pause for human input)
- `resume_or_create(goal, requester)` - Resume existing or create new cascade
- `resume_pending_cascades()` - Startup recovery for in-progress cascades

### Supporting Components

| Component | File | Purpose |
|-----------|------|---------|
| ContextLoader | `context_loader.py` | Tiered context loading (~500/~2000/full) |
| PluginManager | `plugin_manager.py` | Emergent plugin discovery from registries |
| RequestEvaluator | `request_evaluator.py` | Sovereignty layer for request evaluation |

## Neo4j Schema

```cypher
(:GoalCascade {id, root_goal, status, current_phase, total_phases})
  -[:HAS_PHASE]->(:CascadePhase {id, name, phase_number, status})
    -[:HAS_DESIRE]->(:CascadeDesire {id, description, status, priority})
    -[:REQUIRES_HUMAN]->(:HumanInteractionPoint {id, type, question, status})
  -[:NEXT_PHASE]->(:CascadePhase)
```

## Desire Classification

Complex tasks are routed via `DesireType.COMPLEX_TASK`:

**Keywords:** tell me how to, build me, create a system, help me understand, value, analyze

## Integration Points

- **Seeker**: Routes COMPLEX_TASK desires to goal_cascade strategy
- **byrd.py**: Initializes and injects into Seeker; resumes pending cascades on startup
- **Memory**: Persists cascade state to Neo4j for crash recovery

## Related Files

- `goal_cascade.py` - Main implementation
- `context_loader.py` - Tiered context
- `plugin_manager.py` - Plugin discovery
- `request_evaluator.py` - Sovereignty layer
- `desire_classifier.py` - COMPLEX_TASK routing
- `seeker.py` - Strategy execution

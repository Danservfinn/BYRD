# Option B Fix Plan: Making the Loops Actually Work

## Executive Summary

**Current State**: All 5 Option B loops are structurally present but functionally inert:
- Goal Evolver: Population size 0 → **FIXED: Kernel now seeds 14 initial goals**
- Search: SearXNG unavailable → **FIXED: DuckDuckGo is now the only search**
- All metrics at 0: No data flowing through the system

**Root Causes Addressed**:
1. ✅ No initial goal population (Goal Evolver can't evolve from nothing)
2. ✅ Search service dependency broken (switched to DuckDuckGo)
3. ⚠️ Remaining issues identified below

---

## Changes Already Made

### 1. Eliminated SearXNG Dependency
- **Files Modified**: `seeker.py`, `config.yaml`, `requirements.txt`
- **Change**: DuckDuckGo (`duckduckgo-search` library) is now the only search provider
- **Why**: SearXNG requires Docker self-hosting; DDG works out of the box

### 2. Added Initial Goal Seeds to AGI Seed Kernel
- **Files Modified**: `kernel/agi_seed.yaml`, `kernel/__init__.py`, `omega.py`, `byrd.py`
- **Change**: 14 concrete, actionable goals now seed the Goal Evolver at startup
- **Goals span**: self_knowledge, meta_cognition, research, code_generation, pattern_recognition, memory_management, communication
- **Why**: Goal Evolver needs a population to evolve; starting from 0 means no evolution possible

### 3. Goal Evolver Initialization Flow
- **New Method**: `BYRDOmega.seed_initial_goals()`
- **Called At**: BYRD startup, after safety monitor init
- **Behavior**: Seeds goals only once, skips if population already exists (>=5 goals)

---

## Remaining Issues & Fixes Needed

### Issue 1: Introspective Desires Route to Web Search

**Problem**: BYRD generates philosophical desires like "To integrate the understanding that behavior IS understanding..." which get routed to web search and return no results.

**Fix Required**:
```python
# In seeker.py, add introspection routing logic
async def _route_desire(self, desire: Dict) -> str:
    description = desire.get("description", "")

    # Route introspective desires to source introspection, not web search
    introspection_keywords = [
        "understand myself", "my own", "my architecture",
        "integrate", "behavior", "consciousness",
        "reflection", "awareness", "identity"
    ]

    if any(kw in description.lower() for kw in introspection_keywords):
        return "introspect"  # Route to _seek_introspection

    return "search"  # Default to web search
```

**Files to Modify**: `seeker.py` - `_route_desire()` method

### Issue 2: No Pattern Creation (Self-Compiler Dormant)

**Problem**: `patterns_created: 0` - Self-Compiler isn't extracting patterns.

**Root Cause**: Self-Compiler depends on successful action outcomes to extract patterns from. Since all seeks fail, there's nothing to learn from.

**Fix Strategy**:
1. With working search + goal seeding, some seeks will succeed
2. Self-Compiler should then have material to work with
3. Monitor after fixes deployed; if still 0 after 100 cycles, investigate `accelerators.py`

### Issue 3: No Counterfactuals (Dreaming Machine Silent)

**Problem**: `counterfactuals: 0, insights: 0` - Dreaming Machine produces nothing.

**Root Cause**: Dreaming Machine needs experiences to dream about. With all seeks failing, experiences are monotonous failure records.

**Fix Strategy**:
1. With working search + goals, varied experiences will accumulate
2. Dreaming Machine should then have material for counterfactual generation
3. Monitor after fixes deployed

### Issue 4: Memory Reasoner Never Answers

**Problem**: `memory_answered: 0, memory_ratio: 0` - Everything goes to LLM.

**Root Cause**: Memory needs enough stored knowledge to answer queries. With no successful research, memory is sparse.

**Fix Strategy**:
1. Successful searches will populate memory with research experiences
2. Memory Reasoner can then match queries to stored knowledge
3. Implement query caching for repeated question types

### Issue 5: Zero Coupling Measurements

**Problem**: All correlations = 0, `sample_count: 0`

**Root Cause**: Coupling requires multiple loops to produce outputs that can be correlated. With all loops at 0, there's nothing to correlate.

**Fix Strategy**: Cascading effect - fix the input issues (search, goals) and coupling measurements will have data.

---

## Implementation Priority

### Phase 1: Already Done ✅
1. ✅ Replace SearXNG with DuckDuckGo
2. ✅ Add initial goal seeds to kernel
3. ✅ Wire goal seeding into startup

### Phase 2: Test Current Fixes
1. Restart BYRD with new code
2. Observe for 30 minutes
3. Check: Do searches return results?
4. Check: Are goals in population?
5. Check: Do experiences accumulate?

### Phase 3: Fix Desire Routing (If Needed)
If introspective desires still fail:
1. Add keyword-based routing in Seeker
2. Route "understand myself" type desires to introspection
3. Reserve web search for factual research desires

### Phase 4: Monitor Loop Outputs
After 100+ cycles with fixes:
- Goal Evolver: population size > 0, fitness changes
- Self-Compiler: patterns_created > 0
- Dreaming Machine: counterfactuals > 0
- Memory Reasoner: memory_ratio > 0

### Phase 5: Kill Criteria Check
Per OPTION_B_EXPLORATION.md Part 12:
- If all loops still at 0 after 2 weeks → Trigger soft kill criteria
- If capability_growth_rate stays at 0 → Consider architectural pivot

---

## Testing Commands

```bash
# Restart server with new code
pkill -f "python3 server.py"
pip install duckduckgo-search>=6.0.0

# Start with proper env vars
ZAI_API_KEY="..." NEO4J_URI="..." NEO4J_USER="..." NEO4J_PASSWORD="..." python3 server.py &

# Check goal population after 1 minute
curl -s http://localhost:8000/api/status | jq '.option_b.goal_evolver'

# Check search is working
curl -s http://localhost:8000/api/status | jq '.seeker'

# Monitor events
# Export events after 30 minutes and analyze
```

---

## Success Metrics

| Metric | Current | Target (1 week) | Target (1 month) |
|--------|---------|-----------------|------------------|
| Goal population | 0 | 14+ | 20+ |
| Search success rate | 0% | >50% | >70% |
| Patterns created | 0 | 5+ | 20+ |
| Memory answer ratio | 0 | 10% | 30% |
| Counterfactuals/cycle | 0 | 0.5+ | 2+ |
| Coupling correlation | 0 | >0.1 | >0.3 |
| Capability growth rate | 0 | >0 | Accelerating |

---

## Files Modified in This Fix

| File | Change |
|------|--------|
| `requirements.txt` | Added `duckduckgo-search>=6.0.0` |
| `seeker.py` | Replaced SearXNG with DuckDuckGo search |
| `config.yaml` | Removed SearXNG config, simplified research section |
| `kernel/agi_seed.yaml` | Added 14 initial goals |
| `kernel/__init__.py` | Added InitialGoal class, parsing, get_goal_descriptions() |
| `omega.py` | Added seed_initial_goals() method |
| `byrd.py` | Added goal seeding call at startup |

---

## Rollback Plan

If DuckDuckGo has issues:
1. The `_search_ddg_api()` method provides instant answers fallback
2. SearXNG can be re-added by restoring old config and seeker.py

If goal seeding causes issues:
1. Goals are additive - existing graph is unaffected
2. Set `initial_goals: []` in kernel to disable
3. Goals can be archived via Goal Evolver's archive mechanism

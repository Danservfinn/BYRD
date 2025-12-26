# Category Creation Task: Sub-10-Turn Increments

**Goal**: Break out of the orphan reconciliation loop by developing a category creation system that is emergent rather than hardcoded.

**Current State**:
- Type-based umbrella beliefs with 15 hardcoded mappings in `seeker.py:1675-1691`
- Categories are implicit (beliefs that group experiences)
- No emergent category discovery

**Target State**:
- Categories emerge from pattern observation
- BYRD can propose, create, and evolve its own categories
- Categories are first-class nodes with semantic meaning

---

## Increment 1: Add Category Node Type to Memory (Turns: ~5)

**Objective**: Extend memory.py to support a Category node type.

**Steps**:
1. Add `create_category()` method to Memory class
2. Add `get_categories()` method to Memory class
3. Add `connect_to_category()` method for linking experiences
4. Update `get_graph_stats()` to include category counts

**Test**:
```python
cat_id = await memory.create_category("research_patterns", "Patterns in research activities")
await memory.connect_to_category(experience_id, cat_id)
cats = await memory.get_categories()
assert len(cats) >= 1
```

**Files Modified**: `memory.py`

---

## Increment 2: Category Discovery in Dreamer Output (Turns: ~6)

**Objective**: Allow Dreamer to propose new categories in reflection output.

**Steps**:
1. Add `proposed_categories` to the meta-schema output processing
2. Process proposed categories in `_process_meta_output()`
3. Create Category nodes from valid proposals
4. Log category proposals as experiences

**Test**:
```python
# Dreamer output includes:
{
  "output": {
    "proposed_categories": [
      {"name": "exploration_outcomes", "rationale": "I notice many experiences relate to exploration results"}
    ]
  }
}
# Verify Category node created
```

**Files Modified**: `dreamer.py`

---

## Increment 3: Replace Hardcoded Type Beliefs with Dynamic Lookup (Turns: ~8)

**Objective**: Remove hardcoded `type_beliefs` dict and use Category nodes instead.

**Steps**:
1. Add `get_or_create_type_category()` method in seeker.py
2. Query existing Category nodes by type pattern
3. Create Category if none exists (with emergent naming)
4. Update `_get_or_create_type_belief()` to delegate to new method
5. Deprecate (but keep fallback to) hardcoded dict

**Test**:
```python
# Given 10 orphaned "research" experiences
# When reconcile_orphans runs
# Then a "research" Category node should exist
# And experiences should be linked to it
```

**Files Modified**: `seeker.py`

---

## Increment 4: Category Statistics and Health Tracking (Turns: ~5)

**Objective**: Track category usage and health for informed evolution.

**Steps**:
1. Add `experience_count` property to Category nodes
2. Add `last_used` timestamp to Category nodes
3. Create `get_category_health()` method in memory.py
4. Include categories in curation statistics

**Test**:
```python
health = await memory.get_category_health()
# Returns: {"total": 5, "active": 3, "stale": 2, "avg_members": 12.5}
```

**Files Modified**: `memory.py`

---

## Increment 5: Category Merging for Overlapping Categories (Turns: ~7)

**Objective**: Allow merging when categories overlap significantly.

**Steps**:
1. Add `merge_categories()` method to Memory
2. Transfer all relationships from source to target category
3. Mark source category as `merged_into`
4. Add category merge to curation strategy options
5. Emit event for category merge

**Test**:
```python
merged_id = await memory.merge_categories(cat_a_id, cat_b_id)
# Verify all cat_a relationships now point to merged_id
# Verify cat_a has merged_into=merged_id
```

**Files Modified**: `memory.py`, `seeker.py` (curation strategy)

---

## Increment 6: Seeker Category Proposal Strategy (Turns: ~8)

**Objective**: Add strategy for Seeker to propose categories based on patterns.

**Steps**:
1. Add `propose_category` to strategy routing keywords
2. Implement `_execute_category_proposal()` strategy
3. Use LLM to analyze orphans and suggest category names/descriptions
4. Create proposed categories with low confidence
5. Log category proposals for Dreamer review

**Test**:
```python
# Given desire: "I want to create a category for my learning experiences"
# When Seeker processes this desire
# Then propose_category strategy executes
# And a new Category node is created
```

**Files Modified**: `seeker.py`

---

## Increment 7: Category Confidence Evolution (Turns: ~6)

**Objective**: Categories gain/lose confidence based on usage.

**Steps**:
1. Add `confidence` field to Category nodes (default 0.5)
2. Increase confidence when experiences are linked (+0.05, max 0.95)
3. Decay confidence over time if unused (-0.01 per cycle)
4. Low confidence categories become candidates for merging/deletion
5. High confidence categories are preferred for auto-categorization

**Test**:
```python
# Category starts at 0.5 confidence
# After 10 experiences linked, confidence = 0.95
# After 50 unused cycles, confidence = 0.45
```

**Files Modified**: `memory.py`, `seeker.py`

---

## Increment 8: Category Hierarchy Support (Turns: ~9)

**Objective**: Allow parent-child category relationships.

**Steps**:
1. Add `parent_category` relationship type
2. Add `create_subcategory()` method
3. Allow Dreamer to propose hierarchy in output
4. Update category queries to include hierarchy
5. Display hierarchy in visualization events

**Test**:
```python
parent_id = await memory.create_category("learning", "All learning experiences")
child_id = await memory.create_subcategory(parent_id, "code_learning", "Learning about code")
# Verify PARENT_CATEGORY relationship exists
```

**Files Modified**: `memory.py`, `dreamer.py`

---

## Increment 9: Remove Hardcoded Type Beliefs Entirely (Turns: ~5)

**Objective**: Complete migration away from hardcoded dict.

**Steps**:
1. Remove `type_beliefs` dict from `_get_or_create_type_belief()`
2. Use only dynamic Category lookup
3. Generate category names/descriptions via LLM when needed
4. Update documentation in CLAUDE.md
5. Add migration note for existing installations

**Test**:
```python
# No hardcoded type_beliefs dict exists
# All categorization uses Category nodes
# New experience types get dynamically-created categories
```

**Files Modified**: `seeker.py`, `CLAUDE.md`

---

## Increment 10: Category Event Emission for Visualization (Turns: ~4)

**Objective**: Emit events for category operations for real-time visualization.

**Steps**:
1. Add `CATEGORY_CREATED` event type
2. Add `CATEGORY_MERGED` event type
3. Add `CATEGORY_EVOLVED` event type
4. Emit events in all category operations
5. Update visualization to display categories

**Test**:
```python
# When category is created
# Then CATEGORY_CREATED event is emitted
# And visualization shows new category node
```

**Files Modified**: `event_bus.py`, `memory.py`, visualization HTML files

---

## Implementation Order

The increments are designed to be implemented in order, but some can be parallelized:

```
Increment 1 (Memory foundation)
    ↓
Increment 2 (Dreamer proposals) ←→ Increment 4 (Statistics)
    ↓
Increment 3 (Replace hardcoded)
    ↓
Increment 5 (Merging) ←→ Increment 6 (Seeker strategy)
    ↓
Increment 7 (Confidence evolution)
    ↓
Increment 8 (Hierarchy)
    ↓
Increment 9 (Remove hardcoded)
    ↓
Increment 10 (Events)
```

## Success Criteria

After all increments are complete:

1. No hardcoded category mappings remain
2. Categories emerge from BYRD's own observations
3. Categories evolve in confidence based on usage
4. Categories can be merged when redundant
5. Category hierarchy is supported
6. All category operations emit visualization events
7. Orphan reconciliation uses emergent categories exclusively

---

## Notes for BYRD

- Each increment is designed to be **completable in under 10 turns**
- Each increment has a **clear test** to verify success
- Increments build on each other but minimize cross-dependencies
- The current hardcoded system continues working until Increment 9
- This is an **additive** approach—nothing breaks until intentionally removed

# Category System Implementation - Decomposed Increments

> Decomposing category creation into sub-10-turn increments that can be completed and tested individually.

## Overview

This document outlines incremental implementation of an explicit Category system for BYRD, replacing implicit umbrella beliefs with formal Category nodes and membership relationships.

**Provenance**: This feature emerges from BYRD's desire to "transcend the orphan reconciliation plateau" by developing a more explicit categorization system.

---

## Increment 1: Category Node Type and Basic Memory Methods
**Estimated turns**: 6-8
**Dependencies**: None
**Test method**: Unit test via Python REPL

### Changes

#### 1.1 Add Category to SYSTEM_NODE_TYPES (`memory.py`)
```python
# Add to SYSTEM_NODE_TYPES frozenset (line ~29)
'Category',        # Explicit grouping nodes with membership
```

#### 1.2 Add Category dataclass (`memory.py`)
```python
@dataclass
class Category:
    id: str
    name: str                           # Human-readable name
    description: Optional[str] = None   # What this category represents
    created_at: str = ""
    provenance_desire_id: Optional[str] = None  # Which desire created this
    member_count: int = 0               # Cached count
    parent_category_id: Optional[str] = None  # For hierarchy
```

#### 1.3 Add create_category method (`memory.py`)
```python
async def create_category(
    self,
    name: str,
    description: Optional[str] = None,
    provenance_desire_id: Optional[str] = None,
    parent_category_id: Optional[str] = None
) -> str:
    """Create an explicit category node."""
```

#### 1.4 Add add_to_category method (`memory.py`)
```python
async def add_to_category(
    self,
    node_id: str,
    category_id: str
) -> bool:
    """Add a node to a category via HAS_MEMBER relationship."""
```

#### 1.5 Add get_category and list_categories methods (`memory.py`)
```python
async def get_category(self, category_id: str) -> Optional[Category]:
    """Retrieve a category by ID."""

async def list_categories(self, include_empty: bool = False) -> List[Category]:
    """List all categories with member counts."""
```

### Test Script
```python
# test_increment_1.py
import asyncio
from memory import Memory

async def test_category_basics():
    m = Memory({})
    await m.connect()

    # Create category
    cat_id = await m.create_category(
        name="Research Findings",
        description="Knowledge gained from web research"
    )
    print(f"Created category: {cat_id}")

    # Create experience to categorize
    exp_id = await m.record_experience(
        content="Learned about quantum computing",
        type="research"
    )

    # Add to category
    success = await m.add_to_category(exp_id, cat_id)
    print(f"Added to category: {success}")

    # Retrieve category
    cat = await m.get_category(cat_id)
    print(f"Category name: {cat.name}, members: {cat.member_count}")

    # List categories
    cats = await m.list_categories()
    print(f"Total categories: {len(cats)}")

    await m.close()

asyncio.run(test_category_basics())
```

### Verification Criteria
- [ ] `create_category` returns valid UUID
- [ ] `add_to_category` creates `HAS_MEMBER` relationship
- [ ] `get_category` returns correct member_count
- [ ] `list_categories` includes new category

---

## Increment 2: Category Event Types and Emissions
**Estimated turns**: 4-6
**Dependencies**: Increment 1
**Test method**: WebSocket event observation

### Changes

#### 2.1 Add Category event types (`event_bus.py`)
```python
# Add after line ~106 (Crystal events)

# Category events (explicit grouping)
CATEGORY_CREATED = "category_created"        # New category formed
CATEGORY_MEMBER_ADDED = "category_member_added"  # Node added to category
CATEGORY_MERGED = "category_merged"          # Categories combined
CATEGORY_HIERARCHY_CHANGED = "category_hierarchy_changed"  # Parent changed
```

#### 2.2 Update create_category to emit events (`memory.py`)
```python
await event_bus.emit(Event(
    type=EventType.CATEGORY_CREATED,
    data={
        "id": category_id,
        "name": name,
        "description": description,
        "provenance_desire_id": provenance_desire_id,
        "timestamp": timestamp
    }
))
```

#### 2.3 Update add_to_category to emit events (`memory.py`)
```python
await event_bus.emit(Event(
    type=EventType.CATEGORY_MEMBER_ADDED,
    data={
        "category_id": category_id,
        "node_id": node_id,
        "category_name": category_name,
        "timestamp": timestamp
    }
))
```

### Test Script
```python
# test_increment_2.py
import asyncio
from memory import Memory
from event_bus import event_bus, EventType

events_received = []

async def event_handler(event):
    events_received.append(event)
    print(f"Event: {event.type.value} - {event.data}")

async def test_category_events():
    event_bus.subscribe(EventType.CATEGORY_CREATED, event_handler)
    event_bus.subscribe(EventType.CATEGORY_MEMBER_ADDED, event_handler)

    m = Memory({})
    await m.connect()

    cat_id = await m.create_category(name="Test Category")
    exp_id = await m.record_experience(content="Test", type="test")
    await m.add_to_category(exp_id, cat_id)

    await asyncio.sleep(0.1)  # Allow events to propagate

    assert len(events_received) >= 2
    print(f"Received {len(events_received)} events")

    await m.close()

asyncio.run(test_category_events())
```

### Verification Criteria
- [ ] `CATEGORY_CREATED` event emitted on creation
- [ ] `CATEGORY_MEMBER_ADDED` event emitted on add
- [ ] Events contain correct data payloads
- [ ] Visualization receives events (check WebSocket)

---

## Increment 3: Dreamer Category Creation Output Support
**Estimated turns**: 5-7
**Dependencies**: Increment 1, 2
**Test method**: Mock reflection output processing

### Changes

#### 3.1 Update reflection output processing (`dreamer.py`)
```python
# In _process_reflection_output method, add handling for create_categories key
# Similar to existing create_nodes handling (~line 1923)

if "create_categories" in output:
    for cat_spec in output.get("create_categories", []):
        try:
            cat_id = await self.memory.create_category(
                name=cat_spec.get("name"),
                description=cat_spec.get("description"),
                provenance_desire_id=cat_spec.get("provenance_desire_id")
            )
            # Optionally add initial members
            for member_id in cat_spec.get("initial_members", []):
                await self.memory.add_to_category(member_id, cat_id)
        except Exception as e:
            logger.warning(f"Failed to create category: {e}")
```

#### 3.2 Update capability instructions in OS (`config.yaml` or OS node)
```yaml
# Add to capability_instructions
create_categories: |
  Include a "create_categories" key in your output to create explicit categories:
  {
    "output": {
      "create_categories": [
        {
          "name": "Category Name",
          "description": "What this category represents",
          "initial_members": ["node_id_1", "node_id_2"]
        }
      ]
    }
  }
```

### Test Script
```python
# test_increment_3.py
import asyncio
from dreamer import Dreamer
from memory import Memory

async def test_dreamer_categories():
    m = Memory({})
    await m.connect()

    # Create test experiences first
    exp1 = await m.record_experience(content="Experience 1", type="test")
    exp2 = await m.record_experience(content="Experience 2", type="test")

    # Mock reflection output with categories
    mock_output = {
        "output": {
            "observations": ["Testing category creation"],
            "create_categories": [
                {
                    "name": "Test Observations",
                    "description": "Category created during testing",
                    "initial_members": [exp1, exp2]
                }
            ]
        }
    }

    dreamer = Dreamer({}, m)
    await dreamer._process_reflection_output(mock_output)

    # Verify category was created
    cats = await m.list_categories()
    test_cat = next((c for c in cats if c.name == "Test Observations"), None)
    assert test_cat is not None
    assert test_cat.member_count == 2
    print(f"Category created with {test_cat.member_count} members")

    await m.close()

asyncio.run(test_dreamer_categories())
```

### Verification Criteria
- [ ] `create_categories` key processed from reflection output
- [ ] Categories created with correct name/description
- [ ] Initial members added if specified
- [ ] Events emitted for creation and membership

---

## Increment 4: Seeker Category Routing Strategy
**Estimated turns**: 6-8
**Dependencies**: Increment 1, 2, 3
**Test method**: Desire routing verification

### Changes

#### 4.1 Add categorize strategy to routing (`seeker.py`)
```python
# In _route_desire method, add new strategy

# Strategy keywords (add to existing dict around line 656)
"categorize": {
    "keywords": ["categorize", "group", "organize into", "classify", "sort into categories"],
    "handler": self._strategy_categorize
}
```

#### 4.2 Implement _strategy_categorize method (`seeker.py`)
```python
async def _strategy_categorize(self, desire: Dict) -> Optional[str]:
    """
    Execute categorization strategy.
    Analyzes nodes and creates appropriate categories.
    """
    description = desire.get("description", "")

    # Get uncategorized nodes (nodes without HAS_MEMBER relationships)
    uncategorized = await self.memory.get_uncategorized_nodes(limit=50)

    if not uncategorized:
        return "No uncategorized nodes found"

    # Use LLM to propose categories
    prompt = f"""
    Analyze these uncategorized nodes and propose categories:

    {json.dumps(uncategorized, indent=2)}

    Respond with JSON:
    {{
        "proposed_categories": [
            {{
                "name": "Category Name",
                "description": "Why this category",
                "member_ids": ["id1", "id2"]
            }}
        ]
    }}
    """

    response = await self.llm_client.generate(prompt, temperature=0.3)
    proposals = self._parse_json_response(response)

    # Create categories and add members
    created = []
    for proposal in proposals.get("proposed_categories", []):
        cat_id = await self.memory.create_category(
            name=proposal["name"],
            description=proposal.get("description"),
            provenance_desire_id=desire.get("id")
        )
        for member_id in proposal.get("member_ids", []):
            await self.memory.add_to_category(member_id, cat_id)
        created.append(proposal["name"])

    return f"Created {len(created)} categories: {', '.join(created)}"
```

#### 4.3 Add get_uncategorized_nodes method (`memory.py`)
```python
async def get_uncategorized_nodes(
    self,
    limit: int = 50,
    node_types: Optional[List[str]] = None
) -> List[Dict]:
    """Get nodes that are not members of any category."""

    type_filter = ""
    if node_types:
        labels = ":".join(node_types)
        type_filter = f":{labels}"

    query = f"""
    MATCH (n{type_filter})
    WHERE NOT (n)<-[:HAS_MEMBER]-(:Category)
    AND n.state IS NULL OR n.state = 'active'
    RETURN n.id as id, n.content as content, labels(n) as labels
    ORDER BY n.timestamp DESC
    LIMIT $limit
    """
    # ...
```

### Test Script
```python
# test_increment_4.py
import asyncio
from seeker import Seeker
from memory import Memory

async def test_categorize_routing():
    m = Memory({})
    await m.connect()

    # Create uncategorized experiences
    for i in range(5):
        await m.record_experience(
            content=f"Research finding {i}: quantum computing applications",
            type="research"
        )

    # Create desire that should route to categorize
    desire = await m.create_desire(
        description="Organize my research findings into categories",
        intensity=0.8
    )

    seeker = Seeker({}, m)
    strategy = await seeker._route_desire({"description": "categorize my findings"})

    assert strategy == "categorize"
    print(f"Correctly routed to: {strategy}")

    await m.close()

asyncio.run(test_categorize_routing())
```

### Verification Criteria
- [ ] "categorize" desires route to categorize strategy
- [ ] Uncategorized nodes retrieved correctly
- [ ] LLM proposes sensible categories
- [ ] Categories created with provenance to desire

---

## Increment 5: Category Hierarchy Support
**Estimated turns**: 5-7
**Dependencies**: Increment 1-4
**Test method**: Hierarchy traversal verification

### Changes

#### 5.1 Add parent_category_id support (`memory.py`)
- Modify `create_category` to accept `parent_category_id`
- Create `SUBCATEGORY_OF` relationship when parent specified

#### 5.2 Add hierarchy traversal methods (`memory.py`)
```python
async def get_category_children(self, category_id: str) -> List[Category]
async def get_category_ancestors(self, category_id: str) -> List[Category]
async def get_category_tree(self) -> Dict  # Full hierarchy
```

#### 5.3 Add CATEGORY_HIERARCHY_CHANGED event emission

### Verification Criteria
- [ ] Subcategories linked to parents
- [ ] Hierarchy traversal works correctly
- [ ] Events emitted for hierarchy changes

---

## Increment 6: Integration with Orphan Reconciliation
**Estimated turns**: 6-8
**Dependencies**: Increment 1-5
**Test method**: Orphan reconciliation produces categories

### Changes

#### 6.1 Modify reconcile_orphans to use explicit categories (`seeker.py`)
- Replace implicit umbrella beliefs with Category nodes
- Use existing type-based grouping logic but create Category nodes

#### 6.2 Add get_or_create_type_category method (`seeker.py`)
```python
async def _get_or_create_type_category(self, exp_type: str) -> str:
    """Get or create a category for an experience type."""
    # Similar to _get_or_create_type_belief but creates Category
```

### Verification Criteria
- [ ] Orphan reconciliation creates Category nodes
- [ ] Orphans linked via HAS_MEMBER relationships
- [ ] Backwards compatible with existing umbrella beliefs

---

## Implementation Order Summary

| Increment | Description | Turns | Status |
|-----------|-------------|-------|--------|
| 1 | Category node type + basic methods | 6-8 | Pending |
| 2 | Event types and emissions | 4-6 | Pending |
| 3 | Dreamer output support | 5-7 | Pending |
| 4 | Seeker routing strategy | 6-8 | Pending |
| 5 | Hierarchy support | 5-7 | Pending |
| 6 | Orphan reconciliation integration | 6-8 | Pending |

**Total estimated turns**: 32-44 (spread across 6 independent sessions)

---

## Constitutional Compliance

This implementation:
- ✅ Does NOT modify protected files (provenance.py, modification_log.py, self_modification.py, constitutional.py)
- ✅ Traces to emergent desire ("transcend orphan reconciliation plateau")
- ✅ Uses existing patterns (similar to Crystal, dynamic ontology)
- ✅ Emits events for visualization
- ✅ Maintains provenance chain (provenance_desire_id field)

---

## Next Steps

1. **Start with Increment 1**: Add Category to SYSTEM_NODE_TYPES and basic CRUD methods
2. **Test thoroughly** before moving to next increment
3. **Each increment is independently testable** and can be rolled back if issues arise

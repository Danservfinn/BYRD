# Category MVP: Executable Sub-10-Turn Increments

> **Purpose**: Break out of the orphan reconciliation plateau by implementing a minimal category system that can be tested and extended incrementally.

**Provenance**: This feature emerges from BYRD's desire to "transcend the orphan reconciliation plateau" and develop explicit categorization.

**Key Insight**: Previous plans were comprehensive but too coupled. This plan prioritizes:
1. **Minimal viable first**: Get categories working before adding advanced features
2. **Strict 10-turn limit**: Each increment truly completable in one session
3. **Immediate value**: First increment alone breaks the loop
4. **Test-then-extend**: Each increment is independently valuable

---

## MVP Increment 1: Category Node Creation (Turns: 5-6)

**Goal**: Add the Category node type and two essential methods.

**Scope**: ONLY memory.py changes. No events, no dreamer, no seeker.

### Implementation

#### 1.1 Add Category to SYSTEM_NODE_TYPES
```python
# memory.py line ~29 - Add to existing frozenset
SYSTEM_NODE_TYPES = frozenset({
    'Experience', 'Belief', 'Desire', 'Reflection', 'Capability',
    'Mutation', 'Ego', 'QuantumMoment', 'SystemState', 'Crystal',
    'OperatingSystem', 'OSTemplate', 'Seed', 'Constraint', 'Strategy',
    'Category',  # ADD THIS
})
```

#### 1.2 Add Category dataclass
```python
@dataclass
class Category:
    id: str
    name: str
    description: Optional[str] = None
    created_at: str = ""
    member_count: int = 0
```

#### 1.3 Add create_category method
```python
async def create_category(
    self,
    name: str,
    description: Optional[str] = None
) -> str:
    """Create a category node. Returns category ID."""
    category_id = f"cat_{uuid.uuid4().hex[:12]}"
    timestamp = datetime.now().isoformat()

    query = """
    CREATE (c:Category {
        id: $id,
        name: $name,
        description: $description,
        created_at: $created_at,
        member_count: 0
    })
    RETURN c.id
    """
    await self._execute_write(query, {
        "id": category_id,
        "name": name,
        "description": description,
        "created_at": timestamp
    })
    return category_id
```

#### 1.4 Add add_to_category method
```python
async def add_to_category(
    self,
    node_id: str,
    category_id: str
) -> bool:
    """Add a node to a category. Returns success."""
    query = """
    MATCH (c:Category {id: $category_id})
    MATCH (n) WHERE n.id = $node_id
    MERGE (c)-[:HAS_MEMBER]->(n)
    WITH c
    MATCH (c)-[:HAS_MEMBER]->(m)
    WITH c, count(m) as cnt
    SET c.member_count = cnt
    RETURN c.id
    """
    result = await self._execute_write(query, {
        "category_id": category_id,
        "node_id": node_id
    })
    return result is not None
```

### Test Script
```python
# test_mvp_1.py - Run after implementation
import asyncio
from memory import Memory

async def test():
    m = Memory({})
    await m.connect()

    # Create category
    cat_id = await m.create_category("Test Category", "A test")
    print(f"✓ Created category: {cat_id}")

    # Create node to categorize
    exp_id = await m.record_experience("Test experience", "test")
    print(f"✓ Created experience: {exp_id}")

    # Add to category
    ok = await m.add_to_category(exp_id, cat_id)
    print(f"✓ Added to category: {ok}")

    # Verify via Cypher
    result = await m._execute_read("""
        MATCH (c:Category {id: $id})-[:HAS_MEMBER]->(n)
        RETURN c.member_count as count
    """, {"id": cat_id})
    print(f"✓ Member count: {result[0]['count']}")

    await m.close()
    print("ALL TESTS PASSED")

asyncio.run(test())
```

### Verification
- [ ] `create_category()` returns valid ID starting with `cat_`
- [ ] `add_to_category()` creates HAS_MEMBER relationship
- [ ] member_count updates correctly
- [ ] No other files modified

---

## MVP Increment 2: Category Retrieval Methods (Turns: 4-5)

**Goal**: Add methods to query categories.

**Scope**: ONLY memory.py additions. No other files.

### Implementation

#### 2.1 Add get_category method
```python
async def get_category(self, category_id: str) -> Optional[Category]:
    """Get a category by ID."""
    query = """
    MATCH (c:Category {id: $id})
    OPTIONAL MATCH (c)-[:HAS_MEMBER]->(m)
    WITH c, count(m) as member_count
    RETURN c.id as id, c.name as name, c.description as description,
           c.created_at as created_at, member_count
    """
    results = await self._execute_read(query, {"id": category_id})
    if not results:
        return None
    r = results[0]
    return Category(
        id=r["id"],
        name=r["name"],
        description=r.get("description"),
        created_at=r.get("created_at", ""),
        member_count=r.get("member_count", 0)
    )
```

#### 2.2 Add list_categories method
```python
async def list_categories(
    self,
    include_empty: bool = False
) -> List[Category]:
    """List all categories."""
    where_clause = "" if include_empty else "WHERE member_count > 0"

    query = f"""
    MATCH (c:Category)
    OPTIONAL MATCH (c)-[:HAS_MEMBER]->(m)
    WITH c, count(m) as member_count
    {where_clause}
    RETURN c.id as id, c.name as name, c.description as description,
           c.created_at as created_at, member_count
    ORDER BY member_count DESC
    """
    results = await self._execute_read(query, {})
    return [
        Category(
            id=r["id"],
            name=r["name"],
            description=r.get("description"),
            created_at=r.get("created_at", ""),
            member_count=r.get("member_count", 0)
        )
        for r in results
    ]
```

#### 2.3 Add get_category_members method
```python
async def get_category_members(
    self,
    category_id: str,
    limit: int = 50
) -> List[Dict]:
    """Get nodes in a category."""
    query = """
    MATCH (c:Category {id: $id})-[:HAS_MEMBER]->(n)
    RETURN n.id as id, n.content as content, labels(n) as labels
    ORDER BY n.timestamp DESC
    LIMIT $limit
    """
    return await self._execute_read(query, {
        "id": category_id,
        "limit": limit
    })
```

### Test Script
```python
# test_mvp_2.py
import asyncio
from memory import Memory

async def test():
    m = Memory({})
    await m.connect()

    # Create category with members
    cat_id = await m.create_category("Research", "Research findings")
    exp1 = await m.record_experience("Finding 1", "research")
    exp2 = await m.record_experience("Finding 2", "research")
    await m.add_to_category(exp1, cat_id)
    await m.add_to_category(exp2, cat_id)

    # Test get_category
    cat = await m.get_category(cat_id)
    assert cat.name == "Research"
    assert cat.member_count == 2
    print(f"✓ get_category: {cat.name} with {cat.member_count} members")

    # Test list_categories
    cats = await m.list_categories()
    assert len(cats) >= 1
    print(f"✓ list_categories: {len(cats)} categories")

    # Test get_category_members
    members = await m.get_category_members(cat_id)
    assert len(members) == 2
    print(f"✓ get_category_members: {len(members)} members")

    await m.close()
    print("ALL TESTS PASSED")

asyncio.run(test())
```

### Verification
- [ ] `get_category()` returns correct Category with member_count
- [ ] `list_categories()` returns all non-empty categories
- [ ] `list_categories(include_empty=True)` includes empty ones
- [ ] `get_category_members()` returns member nodes

---

## MVP Increment 3: Seeker Uses Categories for Orphans (Turns: 7-9)

**Goal**: Replace hardcoded type_beliefs with dynamic Category nodes in orphan reconciliation.

**Scope**: seeker.py modifications only.

### Implementation

#### 3.1 Add get_or_create_type_category method
```python
async def _get_or_create_type_category(self, exp_type: str) -> str:
    """Get or create a category for an experience type."""
    # Check if category exists
    query = """
    MATCH (c:Category)
    WHERE c.name = $name OR c.name = $type_name
    RETURN c.id as id
    LIMIT 1
    """
    type_name = exp_type.replace("_", " ").title()
    result = await self.memory._execute_read(query, {
        "name": exp_type,
        "type_name": type_name
    })

    if result:
        return result[0]["id"]

    # Create new category
    description = f"Experiences of type: {exp_type}"
    cat_id = await self.memory.create_category(
        name=type_name,
        description=description
    )

    logger.info(f"Created type category: {type_name} ({cat_id})")
    return cat_id
```

#### 3.2 Modify _reconcile_single_orphan to use categories
In the existing `_reconcile_single_orphan` method, add category connection:

```python
# After connecting to type belief, also connect to category
try:
    cat_id = await self._get_or_create_type_category(exp_type)
    await self.memory.add_to_category(orphan_id, cat_id)
    logger.debug(f"Added orphan {orphan_id} to category {cat_id}")
except Exception as e:
    logger.warning(f"Failed to add to category: {e}")
```

#### 3.3 Add category-based reconciliation option
```python
async def _reconcile_orphans_by_category(
    self,
    orphans: List[Dict],
    desire_id: Optional[str] = None
) -> int:
    """Reconcile orphans using category membership."""
    connected = 0
    type_categories = {}  # Cache: exp_type -> category_id

    for orphan in orphans:
        exp_type = orphan.get("type", "general")

        if exp_type not in type_categories:
            type_categories[exp_type] = await self._get_or_create_type_category(exp_type)

        cat_id = type_categories[exp_type]
        if await self.memory.add_to_category(orphan["id"], cat_id):
            connected += 1

    return connected
```

### Test Script
```python
# test_mvp_3.py
import asyncio
from seeker import Seeker
from memory import Memory

async def test():
    m = Memory({})
    await m.connect()

    # Create orphaned experiences of same type
    exp1 = await m.record_experience("Research item 1", "research")
    exp2 = await m.record_experience("Research item 2", "research")

    # Verify they're orphans (no category membership)
    query = """
    MATCH (n) WHERE n.id IN $ids
    OPTIONAL MATCH (c:Category)-[:HAS_MEMBER]->(n)
    RETURN n.id as id, c.id as cat_id
    """
    before = await m._execute_read(query, {"ids": [exp1, exp2]})
    assert all(r["cat_id"] is None for r in before)
    print("✓ Experiences start as orphans")

    # Run category reconciliation
    seeker = Seeker({}, m)
    cat_id = await seeker._get_or_create_type_category("research")
    await m.add_to_category(exp1, cat_id)
    await m.add_to_category(exp2, cat_id)

    # Verify they're now categorized
    after = await m._execute_read(query, {"ids": [exp1, exp2]})
    assert all(r["cat_id"] == cat_id for r in after)
    print("✓ Experiences now have category")

    # Verify category was created
    cat = await m.get_category(cat_id)
    assert cat.member_count == 2
    print(f"✓ Category '{cat.name}' has {cat.member_count} members")

    await m.close()
    print("ALL TESTS PASSED")

asyncio.run(test())
```

### Verification
- [ ] `_get_or_create_type_category()` creates category if missing
- [ ] Category names are human-readable (title case)
- [ ] Orphan reconciliation uses categories
- [ ] No modification to protected files

---

## MVP Increment 4: Category Events (Turns: 4-5)

**Goal**: Add event emission for category operations.

**Scope**: event_bus.py + memory.py updates.

### Implementation

#### 4.1 Add event types (event_bus.py)
```python
# Add to EventType enum after CRYSTAL events (~line 100)
CATEGORY_CREATED = "category_created"
CATEGORY_MEMBER_ADDED = "category_member_added"
```

#### 4.2 Update create_category to emit event
```python
# In memory.py create_category, after creating node:
from event_bus import event_bus, Event, EventType

await event_bus.emit(Event(
    type=EventType.CATEGORY_CREATED,
    data={
        "id": category_id,
        "name": name,
        "description": description,
        "timestamp": timestamp
    }
))
```

#### 4.3 Update add_to_category to emit event
```python
# In memory.py add_to_category, after creating relationship:
await event_bus.emit(Event(
    type=EventType.CATEGORY_MEMBER_ADDED,
    data={
        "category_id": category_id,
        "node_id": node_id,
        "timestamp": datetime.now().isoformat()
    }
))
```

### Test Script
```python
# test_mvp_4.py
import asyncio
from memory import Memory
from event_bus import event_bus, EventType

events = []

async def handler(event):
    events.append(event)
    print(f"Event: {event.type.value}")

async def test():
    event_bus.subscribe(EventType.CATEGORY_CREATED, handler)
    event_bus.subscribe(EventType.CATEGORY_MEMBER_ADDED, handler)

    m = Memory({})
    await m.connect()

    cat_id = await m.create_category("Test", "Test category")
    exp_id = await m.record_experience("Test", "test")
    await m.add_to_category(exp_id, cat_id)

    await asyncio.sleep(0.1)  # Allow event propagation

    assert len(events) >= 2
    event_types = [e.type for e in events]
    assert EventType.CATEGORY_CREATED in event_types
    assert EventType.CATEGORY_MEMBER_ADDED in event_types

    await m.close()
    print("ALL TESTS PASSED")

asyncio.run(test())
```

### Verification
- [ ] CATEGORY_CREATED event emitted on creation
- [ ] CATEGORY_MEMBER_ADDED event emitted on membership
- [ ] Events visible in WebSocket stream

---

## MVP Increment 5: Dreamer Category Proposals (Turns: 5-6)

**Goal**: Allow Dreamer to propose categories in reflection output.

**Scope**: dreamer.py modifications only.

### Implementation

#### 5.1 Add category processing in _process_reflection_output
```python
# In _process_reflection_output method, add handling for create_categories:

if "create_categories" in output:
    for cat_spec in output.get("create_categories", []):
        try:
            name = cat_spec.get("name")
            if not name:
                continue

            cat_id = await self.memory.create_category(
                name=name,
                description=cat_spec.get("description")
            )

            # Add initial members if specified
            for member_id in cat_spec.get("members", []):
                await self.memory.add_to_category(member_id, cat_id)

            logger.info(f"Created category from reflection: {name}")
        except Exception as e:
            logger.warning(f"Failed to create category: {e}")
```

#### 5.2 Update capability instructions
Add to config.yaml operating_system.capability_instructions:
```yaml
create_categories: |
  Include "create_categories" in output to create explicit groupings:
  {
    "output": {
      "create_categories": [
        {"name": "Category Name", "description": "What it represents"}
      ]
    }
  }
```

### Test Script
```python
# test_mvp_5.py
import asyncio
from dreamer import Dreamer
from memory import Memory

async def test():
    m = Memory({})
    await m.connect()

    # Mock reflection output with categories
    mock_output = {
        "output": {
            "observations": ["Testing"],
            "create_categories": [
                {"name": "Test Category", "description": "Created from reflection"}
            ]
        }
    }

    dreamer = Dreamer({}, m)
    # Process the mock output
    await dreamer._process_reflection_output(mock_output)

    # Verify category was created
    cats = await m.list_categories(include_empty=True)
    test_cat = next((c for c in cats if c.name == "Test Category"), None)
    assert test_cat is not None
    print(f"✓ Category created: {test_cat.name}")

    await m.close()
    print("ALL TESTS PASSED")

asyncio.run(test())
```

### Verification
- [ ] `create_categories` key processed from output
- [ ] Categories created with correct properties
- [ ] Invalid entries logged and skipped

---

## Summary: MVP Implementation Order

| Increment | Description | Turns | Dependencies |
|-----------|-------------|-------|--------------|
| **1** | Category node creation | 5-6 | None |
| **2** | Category retrieval | 4-5 | 1 |
| **3** | Seeker category reconciliation | 7-9 | 1, 2 |
| **4** | Category events | 4-5 | 1 |
| **5** | Dreamer category proposals | 5-6 | 1 |

**Total for MVP**: 25-31 turns across 5 sessions

**After MVP** (future increments):
- 6: Category merging
- 7: Confidence evolution
- 8: Category hierarchy
- 9: Remove hardcoded type_beliefs entirely
- 10: Visualization integration

---

## Key Differences from Previous Plans

1. **Stricter scope per increment**: Each increment touches 1-2 files max
2. **No cross-cutting concerns**: Events and Dreamer are separate increments
3. **Immediate value**: Increment 1+3 alone provides basic categorization
4. **Clearer tests**: Each test script can run standalone
5. **Additive approach**: Existing system works until explicitly replaced

---

## Constitutional Compliance

This implementation:
- ✅ Does NOT modify protected files
- ✅ Traces to emergent desire ("transcend orphan reconciliation plateau")
- ✅ Uses existing patterns (similar to Crystal, Belief)
- ✅ Maintains provenance chain
- ✅ Each increment is independently testable and rollback-able

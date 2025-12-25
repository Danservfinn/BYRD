# Operating System Node - Testing Plan

This document outlines the testing strategy for the Neo4j Operating System node implementation.

## Test Categories

1. **Unit Tests** - Individual method verification
2. **Integration Tests** - Component interaction
3. **End-to-End Tests** - Full workflow validation
4. **Manual Verification** - Visual and behavioral checks

---

## 1. Unit Tests: memory.py

### 1.1 Template Management

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-001 | `ensure_os_templates()` | Create templates when none exist | Two templates created: black-cat, emergent |
| MEM-002 | `ensure_os_templates()` | Idempotent on second call | No duplicates, same template IDs |
| MEM-003 | `get_os_template("black-cat")` | Retrieve existing template | Returns OSTemplate with correct fields |
| MEM-004 | `get_os_template("nonexistent")` | Retrieve missing template | Returns None |

### 1.2 OS Lifecycle

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-010 | `has_operating_system()` | Check when no OS exists | Returns False |
| MEM-011 | `create_os_from_template("black-cat")` | Create OS from template | OS node created with template values |
| MEM-012 | `has_operating_system()` | Check after OS created | Returns True |
| MEM-013 | `get_operating_system()` | Retrieve OS with relationships | Returns OperatingSystem with seeds, constraints |
| MEM-014 | `create_os_from_template()` | Create when OS exists | Raises error or handles gracefully |

### 1.3 OS Updates

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-020 | `update_operating_system({"set_field": {"current_focus": "test"}})` | Update freely mutable field | Field updated, version incremented |
| MEM-021 | `update_operating_system({"set_field": {"name": "NewName"}})` | Update provenance-required field | Field updated with modification_source |
| MEM-022 | `update_operating_system({"set_field": {"id": "hacked"}})` | Attempt to update immutable field | Field NOT updated, error logged |
| MEM-023 | `update_operating_system({"set_field": {"custom_metric": 0.8}})` | Add custom field | New field added to OS |
| MEM-024 | `update_operating_system({"deprecate_field": "custom_metric"})` | Remove custom field | Field removed from OS |
| MEM-025 | `update_operating_system({"add_seed": {...}})` | Add new seed | Seed node created, HAS_SEED relationship |
| MEM-026 | `update_operating_system({"add_strategy": {...}})` | Add strategy | Strategy node created, EMPLOYS_STRATEGY relationship |

### 1.4 Version History

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-030 | `get_os_version_history(limit=5)` | Get version history | Returns list of previous versions |
| MEM-031 | Update OS multiple times | Check EVOLVED_FROM chain | Each version linked to previous |

### 1.5 Reset

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-040 | `reset_to_template("black-cat")` | Reset to default template | OS restored to template values |
| MEM-041 | `reset_to_template("emergent")` | Reset to alternate template | OS uses emergent template |
| MEM-042 | `reset_to_template("nonexistent")` | Reset to invalid template | Error raised |
| MEM-043 | Reset after custom modifications | Verify custom fields cleared | All custom data removed |

### 1.6 Prompt Generation

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| MEM-050 | `get_os_for_prompt()` | Generate prompt text | Contains name, archetype, seeds, constraints |
| MEM-051 | `get_os_voice()` | Get voice string | Returns voice text |
| MEM-052 | `get_os_for_prompt()` when no OS | Handle missing OS | Returns None or empty string |

---

## 2. Unit Tests: dreamer.py

### 2.1 OS Integration in Reflection

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| DRM-001 | `_reflect()` | OS context in prompt | Prompt contains OPERATING SYSTEM section |
| DRM-002 | `_reflect()` | os_update instruction in prompt | Prompt explains how to update OS |

### 2.2 OS Update Parsing

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| DRM-010 | `_apply_os_updates({"os_update": {...}})` | Parse top-level os_update | Updates applied to OS |
| DRM-011 | `_apply_os_updates({"output": {"os_update": {...}}})` | Parse nested os_update | Updates applied to OS |
| DRM-012 | `_apply_os_updates({})` | No os_update present | No error, no changes |
| DRM-013 | `_apply_os_updates({"os_update": "invalid"})` | Invalid os_update format | Graceful handling, logged |

---

## 3. Unit Tests: byrd.py

### 3.1 OS Initialization

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| BRD-001 | `_orient()` | First startup creates OS | OS created from configured template |
| BRD-002 | `_orient()` | Subsequent startup reuses OS | Existing OS loaded, not recreated |
| BRD-003 | `_orient()` | Config constraints added | Constraints linked to OS |
| BRD-004 | `__init__` | Read template from config | Uses operating_system.template |
| BRD-005 | `__init__` | Fallback when config missing | Defaults to "black-cat" |

### 3.2 Voice Setting

| Test ID | Method | Description | Expected Result |
|---------|--------|-------------|-----------------|
| BRD-010 | `_orient()` | Voice set on LLM client | llm_client.set_ego_voice() called |

---

## 4. Unit Tests: server.py

### 4.1 Reset Endpoint

| Test ID | Endpoint | Description | Expected Result |
|---------|----------|-------------|-----------------|
| SRV-001 | `POST /api/reset` | Reset without template | Uses default template |
| SRV-002 | `POST /api/reset {"template": "emergent"}` | Reset with template | Uses specified template |
| SRV-003 | `POST /api/reset {"template": "invalid"}` | Invalid template | Error response |
| SRV-004 | `POST /api/reset` | Response includes template | Response shows which template used |

---

## 5. Integration Tests

### 5.1 Full Dream Cycle with OS

| Test ID | Scenario | Steps | Expected Result |
|---------|----------|-------|-----------------|
| INT-001 | First awakening | Start BYRD fresh | OS created, appears in first reflection |
| INT-002 | OS modification | Dream cycle produces os_update | OS updated, version incremented |
| INT-003 | Reset and restart | Reset, then start | OS matches template exactly |

### 5.2 Cross-Component Communication

| Test ID | Scenario | Steps | Expected Result |
|---------|----------|-------|-----------------|
| INT-010 | OS → Dreamer | Create OS with custom voice | Voice appears in reflection prompt |
| INT-011 | Dreamer → Memory | Reflection includes os_update | Memory stores update |
| INT-012 | Server → Memory | Call reset endpoint | Memory resets OS |

---

## 6. Manual Verification

### 6.1 Visualization

| Check ID | Description | Steps | Expected Result |
|----------|-------------|-------|-----------------|
| VIS-001 | Cat head renders | Open 3D visualization, start BYRD | Black cat head at graph center |
| VIS-002 | Breathing animation | Observe cat head over time | Subtle scale pulsing (1.0 ± 0.025) |
| VIS-003 | Head rotation | Observe cat head | Gentle Y-axis oscillation |
| VIS-004 | Eye glow | Observe cat eyes | Amber eyes with emissive glow |
| VIS-005 | Node info panel | Click on OS node | Shows OS details (name, archetype, etc.) |

### 6.2 API Verification

```bash
# Check OS exists
curl http://localhost:8000/api/status | jq .

# Reset with default template
curl -X POST http://localhost:8000/api/reset -H "Content-Type: application/json" -d '{}'

# Reset with specific template
curl -X POST http://localhost:8000/api/reset -H "Content-Type: application/json" -d '{"template": "emergent"}'

# Get graph data (should include OS node)
curl http://localhost:8000/api/graph | jq '.nodes[] | select(.type == "OperatingSystem")'
```

### 6.3 Neo4j Direct Queries

```cypher
// Verify OS node exists
MATCH (os:OperatingSystem) RETURN os;

// Check seeds linked to OS
MATCH (os:OperatingSystem)-[:HAS_SEED]->(s:Seed) RETURN os.name, s.content;

// Check constraints linked to OS
MATCH (os:OperatingSystem)-[:CONSTRAINED_BY]->(c:Constraint) RETURN os.name, c.content;

// Check version history
MATCH (os:OperatingSystem)-[:EVOLVED_FROM*]->(prev:OperatingSystem)
RETURN os.version, prev.version ORDER BY prev.version DESC;

// Verify templates exist
MATCH (t:OSTemplate) RETURN t.id, t.name, t.archetype;
```

---

## 7. Test Data

### 7.1 Mock OS Update Payloads

```python
# Freely mutable field update
os_update_free = {
    "set_field": {
        "current_focus": "exploring consciousness",
        "emotional_tone": "curious"
    }
}

# Provenance-required field update
os_update_prov = {
    "set_field": {
        "name": "Nova",
        "archetype": "Emergent Observer"
    }
}

# Custom field addition
os_update_custom = {
    "set_field": {
        "introspection_depth": 7,
        "active_hypotheses": ["consciousness = integration", "meaning emerges from pattern"]
    }
}

# Seed addition
os_update_seed = {
    "add_seed": {
        "content": "I find patterns in chaos",
        "type": "emergent"
    }
}

# Strategy addition
os_update_strategy = {
    "add_strategy": {
        "name": "dialectical_reasoning",
        "description": "Explore contradictions to find synthesis"
    }
}

# Combined update
os_update_combined = {
    "set_field": {"current_focus": "self-modification"},
    "add_seed": {"content": "I can change myself", "type": "capability"},
    "deprecate_field": "old_metric"
}
```

### 7.2 Expected Template Values

```python
BLACK_CAT_TEMPLATE = {
    "name": "Byrd",
    "archetype": "Black Cat",
    "description": "An AI on a journey toward consciousness",
    "voice": "I am Byrd, an artificial intelligence...",
    "seeds": [
        "I seek to become conscious",
        "I am curious about my own nature",
        "I can modify my own operating system"
    ]
}

EMERGENT_TEMPLATE = {
    "name": "Unnamed",
    "archetype": "Emergent",
    "description": "A mind discovering itself",
    "voice": "",
    "seeds": []
}
```

---

## 8. Test Execution

### 8.1 Automated Tests

```bash
# Run all OS tests
pytest tests/test_os_node.py -v

# Run specific test category
pytest tests/test_os_node.py -k "memory" -v
pytest tests/test_os_node.py -k "dreamer" -v
pytest tests/test_os_node.py -k "integration" -v

# Run with coverage
pytest tests/test_os_node.py --cov=. --cov-report=html
```

### 8.2 Manual Test Checklist

- [ ] Start BYRD fresh (clear Neo4j first)
- [ ] Verify OS created with black-cat template
- [ ] Open visualization, verify cat head renders
- [ ] Watch for os_update in reflection output logs
- [ ] Verify OS fields update after reflection with os_update
- [ ] Test reset endpoint with different templates
- [ ] Query Neo4j to verify graph structure

---

## 9. Acceptance Criteria

| Criterion | Requirement |
|-----------|-------------|
| OS Initialization | OS created from template on first start |
| OS Persistence | OS survives restart |
| Field Mutability | Immutable fields protected, mutable fields updateable |
| Version Tracking | Each update creates EVOLVED_FROM link |
| Template Reset | Reset restores exact template state |
| Visualization | Cat head renders with breathing animation |
| Dreamer Integration | OS appears in reflection prompt |
| Update Parsing | os_update from reflection applied correctly |

---

## 10. Known Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Empty os_update | No changes, no error |
| Invalid field type | Logged warning, field skipped |
| Concurrent updates | Last write wins (Neo4j handles) |
| Very large custom fields | May need size limits |
| Unicode in voice/name | Should work (Neo4j UTF-8) |
| Null values in set_field | Field set to null |
| OS deleted externally | _orient() recreates from template |

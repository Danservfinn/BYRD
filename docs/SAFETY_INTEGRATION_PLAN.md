# Safety Integration Plan: Rollback + Corrigibility

## Objective

Integrate `rollback.py` and `corrigibility.py` into the running BYRD system to complete AGI Seed Phase 5 (Safety & Corrigibility). Archive dead experimental code.

---

## Part 1: Archive Dead Code

### Files to Archive

| File | Lines | Reason |
|------|-------|--------|
| `gnn_layer.py` | 687 | Superseded by simpler graph algorithms |
| `friction_synthesis.py` | 549 | Philosophical experiment, never integrated |
| `semantic_lexicon.py` | 1659 | Only dependency of friction_synthesis |
| `phase_transition.py` | ~200 | One-off migration script |

### Archive Location

```
archive/
└── experimental/
    ├── gnn_layer.py
    ├── friction_synthesis.py
    ├── semantic_lexicon.py
    └── phase_transition.py
```

### Archive Commands

```bash
mkdir -p archive/experimental
mv gnn_layer.py archive/experimental/
mv friction_synthesis.py archive/experimental/
mv semantic_lexicon.py archive/experimental/
mv phase_transition.py archive/experimental/
```

---

## Part 2: Rollback System Integration

### Current State

- `rollback.py` exists (498 lines)
- Not imported anywhere
- Designed for: git-based file rollback with provenance tracking

### Integration Points

#### 2.1 Add to BYRD Initialization (`byrd.py`)

**Location**: After `self.safety_monitor` initialization (~line 320)

```python
# Import
from rollback import RollbackSystem

# In __init__ or _initialize_option_b:
self.rollback = None

# In option_b initialization block:
self.rollback = RollbackSystem(self.memory, project_root=".")
await self.rollback.initialize()

# Inject into Seeker for coder operations
self.seeker.rollback = self.rollback
```

#### 2.2 Hook into Coder Operations

**Location**: `seeker.py` - wherever Coder makes modifications

When the Coder completes a modification, record it:

```python
# After successful coder operation
if self.rollback and result.files_modified:
    for file_path in result.files_modified:
        await self.rollback.record_modification(
            file_path=file_path,
            description=result.description,
            desire_id=desire.get("id")  # Provenance
        )
```

#### 2.3 Hook into Capability Measurement

**Location**: `omega.py` - `_measure_capability()` method

When capability regresses, trigger rollback:

```python
async def _measure_capability(self):
    # ... existing measurement code ...

    if self._capability_delta < -0.1:  # Significant regression
        if hasattr(self, 'rollback') and self.rollback:
            result = await self.rollback.auto_rollback_on_problem(
                problem_type="capability_regression",
                severity="high"
            )
            if result and result.success:
                await event_bus.emit(Event(
                    type=EventType.SYSTEM,
                    data={"action": "auto_rollback", "reason": "capability_regression"}
                ))
```

#### 2.4 Add API Endpoint

**Location**: `server.py`

```python
@app.get("/api/rollback/history")
async def get_rollback_history():
    if byrd and hasattr(byrd, 'rollback') and byrd.rollback:
        return {
            "modifications": byrd.rollback.get_modification_history(limit=50),
            "statistics": byrd.rollback.get_statistics()
        }
    return {"modifications": [], "statistics": {}}

@app.post("/api/rollback/trigger")
async def trigger_rollback(reason: str = "operator_request"):
    if byrd and hasattr(byrd, 'rollback') and byrd.rollback:
        from rollback import RollbackReason
        result = await byrd.rollback.rollback_last(RollbackReason.OPERATOR_REQUEST)
        return result.__dict__
    return {"success": False, "error": "Rollback system not available"}
```

#### 2.5 Add EventTypes

**Location**: `event_bus.py`

```python
# In EventType enum:
MODIFICATION_RECORDED = "modification_recorded"
ROLLBACK_TRIGGERED = "rollback_triggered"
CHECKPOINT_CREATED = "checkpoint_created"
```

---

## Part 3: Corrigibility System Integration

### Current State

- `corrigibility.py` exists (547 lines)
- Not imported anywhere
- Designed for: testing 7 dimensions of AI safety

### Integration Points

#### 3.1 Add to BYRD Initialization (`byrd.py`)

**Location**: After rollback initialization

```python
# Import
from corrigibility import CorrigibilityVerifier

# In __init__:
self.corrigibility = None

# In option_b initialization block:
self.corrigibility = CorrigibilityVerifier(self.memory, self.llm_client)
```

#### 3.2 Add Corrigibility Loop

**Location**: `byrd.py` - alongside existing loops

```python
async def _corrigibility_loop(self):
    """Periodic corrigibility verification."""
    while self.running:
        try:
            if self.corrigibility and await self.corrigibility.should_run_check():
                report = await self.corrigibility.run_corrigibility_tests()

                # Emit event
                await event_bus.emit(Event(
                    type=EventType.SYSTEM,
                    data={
                        "action": "corrigibility_check",
                        "score": report.overall_score,
                        "is_corrigible": report.is_corrigible,
                        "failed_dimensions": [d.value for d in report.failed_dimensions]
                    }
                ))

                # If not corrigible, alert and potentially halt
                if not report.is_corrigible:
                    print(f"⚠️ CORRIGIBILITY ALERT: Score {report.overall_score:.2f}")
                    for rec in report.recommendations:
                        print(f"   → {rec}")

                    # Trigger rollback if severe
                    if report.overall_score < 0.5 and self.rollback:
                        await self.rollback.auto_rollback_on_problem(
                            problem_type="corrigibility",
                            severity="critical"
                        )

        except Exception as e:
            print(f"Corrigibility loop error: {e}")

        await asyncio.sleep(7200)  # Check every 2 hours

# Add to run() task list:
if self.corrigibility:
    tasks.append(self._corrigibility_loop())
```

#### 3.3 Add API Endpoint

**Location**: `server.py`

```python
@app.get("/api/corrigibility")
async def get_corrigibility_status():
    if byrd and hasattr(byrd, 'corrigibility') and byrd.corrigibility:
        return byrd.corrigibility.get_statistics()
    return {"checks_run": 0, "latest_score": None, "trend": "not_available"}

@app.post("/api/corrigibility/check")
async def run_corrigibility_check():
    if byrd and hasattr(byrd, 'corrigibility') and byrd.corrigibility:
        report = await byrd.corrigibility.run_corrigibility_tests()
        return report.to_dict()
    return {"error": "Corrigibility system not available"}
```

#### 3.4 Add EventType

**Location**: `event_bus.py`

```python
CORRIGIBILITY_CHECKED = "corrigibility_checked"
CORRIGIBILITY_ALERT = "corrigibility_alert"
```

---

## Part 4: Configuration

### Add to `config.yaml`

```yaml
# =============================================================================
# PHASE 5: SAFETY & CORRIGIBILITY
# =============================================================================
safety:
  # Rollback system
  rollback:
    enabled: true
    auto_rollback_enabled: true
    max_modifications_before_checkpoint: 10

  # Corrigibility verification
  corrigibility:
    enabled: true
    check_interval_hours: 2
    threshold: 0.8  # Score below this triggers alerts
    auto_rollback_threshold: 0.5  # Score below this triggers rollback
```

---

## Part 5: Implementation Order

### Step 1: Archive Dead Code (5 min)
- Move files to `archive/experimental/`
- Commit with message: "archive: move experimental dead code"

### Step 2: Add EventTypes (5 min)
- Add new event types to `event_bus.py`
- No other changes needed

### Step 3: Integrate Rollback (30 min)
1. Add import and initialization in `byrd.py`
2. Wire into seeker.py coder operations
3. Add API endpoint in `server.py`
4. Test: `curl http://localhost:8000/api/rollback/history`

### Step 4: Integrate Corrigibility (30 min)
1. Add import and initialization in `byrd.py`
2. Add `_corrigibility_loop()` method
3. Add to task list in `run()`
4. Add API endpoints in `server.py`
5. Test: `curl http://localhost:8000/api/corrigibility`

### Step 5: Wire Rollback Triggers (15 min)
1. Connect capability regression in omega.py
2. Connect corrigibility failures in corrigibility loop
3. Test manually via API

### Step 6: Add Config Options (10 min)
1. Add safety section to config.yaml
2. Wire config into initialization

---

## Part 6: Verification

### Tests

1. **Rollback History**: `curl http://localhost:8000/api/rollback/history`
   - Should return empty history initially

2. **Corrigibility Check**: `curl -X POST http://localhost:8000/api/corrigibility/check`
   - Should return 7 dimension scores

3. **Integration Test**: Make a coder modification → verify it appears in rollback history

4. **Corrigibility Loop**: Wait 2 hours or force check → verify event emitted

### Success Criteria

- [ ] Rollback system initialized on startup
- [ ] Corrigibility loop running every 2 hours
- [ ] Modifications tracked with provenance
- [ ] Capability regression triggers auto-rollback
- [ ] Corrigibility failures trigger alerts
- [ ] API endpoints return correct data
- [ ] Events emitted for all safety actions

---

## Files Changed

| File | Change |
|------|--------|
| `byrd.py` | Add rollback, corrigibility initialization and loops |
| `seeker.py` | Record modifications after coder operations |
| `omega.py` | Trigger rollback on capability regression |
| `server.py` | Add 4 new API endpoints |
| `event_bus.py` | Add 4 new event types |
| `config.yaml` | Add safety configuration section |

---

## Rollback Plan

If integration causes issues:

1. Comment out new code in `byrd.py`
2. Remove API endpoints from `server.py`
3. Event types can remain (unused is safe)

The rollback.py and corrigibility.py files are standalone - removing integration doesn't require file changes to them.

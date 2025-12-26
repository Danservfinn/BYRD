# BYRD Omega Integration Plan

## Objective

Integrate the existing Omega components (`omega.py`, `coupling_tracker.py`, `meta_learning.py`, `self_model.py`) into the main BYRD system to make the five compounding loops and their metrics live.

## Current State

| Component | File Exists | Integrated | Live Metrics |
|-----------|-------------|------------|--------------|
| BYRDOmega | `omega.py` ✅ | ❌ | ❌ |
| CouplingTracker | `coupling_tracker.py` ✅ | ❌ | ❌ |
| MetaLearningSystem | `meta_learning.py` ✅ | ❌ | ❌ |
| SelfModel | `self_model.py` ✅ | ❌ | ❌ |

**Critical Issue**: Many event types referenced in Option B code are NOT defined in `event_bus.py`.

---

## Phase 1: Foundation (Event Types + Wiring)

### 1.1 Add Missing Event Types to `event_bus.py`

Add these to the `EventType` enum:

```python
# Option B: Self-Compiler Events
PATTERN_CREATED = "pattern_created"
PATTERN_USED = "pattern_used"
PATTERN_LIFTED = "pattern_lifted"

# Option B: Goal Evolver Events
GOAL_CREATED = "goal_created"
GOAL_EVALUATED = "goal_evaluated"
GOAL_COMPLETED = "goal_completed"
GOAL_EVOLVED = "goal_evolved"

# Option B: Dreaming Machine Events
COUNTERFACTUAL_GENERATED = "counterfactual_generated"

# Option B: Memory Reasoner Events
MEMORY_QUERY_ANSWERED = "memory_query_answered"

# Option B: Omega Orchestration Events
LOOP_CYCLE_START = "loop_cycle_start"
LOOP_CYCLE_END = "loop_cycle_end"
MODE_TRANSITION = "mode_transition"
CAPABILITY_MEASURED = "capability_measured"
COUPLING_MEASURED = "coupling_measured"
```

### 1.2 Add Omega to BYRD Class (`byrd.py`)

**In `__init__()`** (after other component initialization):
```python
# Option B: Omega integration (if enabled)
if config.get("option_b", {}).get("enabled", False):
    from omega import create_omega
    self.omega = create_omega(self.memory, self.llm_client, config)
else:
    self.omega = None
```

**In `start()`** (add to asyncio.gather):
```python
tasks = [
    self.dreamer.run(),
    self.seeker.run(),
    self._narrator_loop()
]
if self.omega:
    tasks.append(self._omega_loop())

await asyncio.gather(*tasks)
```

**Add new method `_omega_loop()`**:
```python
async def _omega_loop(self):
    """Run Omega integration cycles."""
    while self._running:
        try:
            await self.omega.run_cycle()
        except Exception as e:
            print(f"Omega cycle error: {e}")
        await asyncio.sleep(30)  # Omega cycle every 30s
```

### 1.3 Add Config Section (`config.yaml`)

```yaml
option_b:
  enabled: true

  omega:
    cycle_interval_seconds: 30
    mode_durations:
      AWAKE: 60
      DREAMING: 30
      EVOLVING: 20
      COMPILING: 40
    target_critical_coupling: 0.5
```

---

## Phase 2: Metrics Collection

### 2.1 Initialize CouplingTracker on Startup

In `byrd.py` `__init__()`:
```python
if self.omega:
    from coupling_tracker import get_coupling_tracker
    self.coupling_tracker = get_coupling_tracker()
```

The CouplingTracker subscribes to events automatically and tracks:
- Loop activity (events per loop)
- Capability changes
- Correlation coefficients

### 2.2 Initialize SelfModel for Capability Tracking

In `byrd.py` `__init__()`:
```python
if self.omega:
    from self_model import SelfModel
    self.self_model = SelfModel(self.memory, self.llm_client)
```

### 2.3 Record Capability Attempts

In Seeker when executing strategies, wrap with capability tracking:
```python
# In seeker.py - wrap strategy execution
if hasattr(self.byrd, 'self_model') and self.byrd.self_model:
    try:
        result = await self._execute_strategy(...)
        await self.byrd.self_model.record_capability_attempt(
            capability="research", success=True, context=desire
        )
    except Exception as e:
        await self.byrd.self_model.record_capability_attempt(
            capability="research", success=False, error=str(e)
        )
```

---

## Phase 3: API Exposure

### 3.1 Add Pydantic Models (`server.py`)

```python
class LoopMetrics(BaseModel):
    name: str
    is_healthy: bool
    cycles_completed: int
    metrics: Dict[str, float]

class OmegaMetricsResponse(BaseModel):
    enabled: bool
    mode: str
    total_cycles: int
    capability_score: float
    growth_rate: float
    critical_coupling: float
    critical_coupling_significant: bool
    loops: Dict[str, LoopMetrics]
    improvement_rate: Optional[float]
    improvement_trajectory: Optional[str]
```

### 3.2 Add `/api/omega/metrics` Endpoint

```python
@app.get("/api/omega/metrics", response_model=OmegaMetricsResponse)
async def get_omega_metrics():
    """Get Omega integration mind metrics."""
    global byrd_instance

    if not byrd_instance:
        raise HTTPException(status_code=503, detail="BYRD not initialized")

    if not byrd_instance.omega:
        return OmegaMetricsResponse(
            enabled=False,
            mode="disabled",
            total_cycles=0,
            capability_score=0.0,
            growth_rate=0.0,
            critical_coupling=0.0,
            critical_coupling_significant=False,
            loops={},
            improvement_rate=None,
            improvement_trajectory=None
        )

    metrics = byrd_instance.omega.get_metrics()

    return OmegaMetricsResponse(
        enabled=True,
        mode=metrics.get("mode", "unknown"),
        total_cycles=metrics.get("total_cycles", 0),
        capability_score=metrics.get("capability_score", 0.0),
        growth_rate=metrics.get("growth_rate", 0.0),
        critical_coupling=metrics.get("critical_coupling", 0.0),
        critical_coupling_significant=metrics.get("critical_coupling_significant", False),
        loops=metrics.get("loops", {}),
        improvement_rate=metrics.get("improvement_rate"),
        improvement_trajectory=metrics.get("improvement_trajectory")
    )
```

### 3.3 Add to `/api/status` Response

Extend the existing StatusResponse model:
```python
class StatusResponse(BaseModel):
    # ... existing fields ...
    omega: Optional[OmegaMetricsResponse] = None
```

---

## Phase 4: Visualization Update

### 4.1 Update `byrd-architecture.html`

Replace simulated metrics with real API calls:

```javascript
async function fetchOmegaMetrics() {
    try {
        const response = await fetch(`${API_BASE}/api/omega/metrics`);
        if (!response.ok) return null;
        return await response.json();
    } catch (e) {
        console.error('Omega metrics fetch error:', e);
        return null;
    }
}

function renderMetrics(omegaData) {
    if (!omegaData || !omegaData.enabled) {
        // Show "Omega not enabled" state
        return;
    }

    // Update mode indicator
    document.getElementById('current-mode').innerHTML = `
        <span class="w-2 h-2 rounded-full bg-violet-400 animate-pulse"></span>
        <span class="text-violet-300 text-sm font-medium">${omegaData.mode.toUpperCase()}</span>
    `;

    // Update metrics bars
    updateMetricBar('improvement-rate', omegaData.growth_rate * 100);
    updateMetricBar('llm-efficiency', omegaData.capability_score * 100);
    updateMetricBar('coupling', omegaData.critical_coupling * 100);

    // Update loop health indicators
    Object.entries(omegaData.loops).forEach(([name, loop]) => {
        const dot = document.querySelector(`[data-status="${name}"]`);
        if (dot) {
            dot.setAttribute('fill', loop.is_healthy ? '#22c55e' : '#ef4444');
        }
    });
}
```

### 4.2 Add Auto-Refresh

```javascript
document.addEventListener('DOMContentLoaded', async () => {
    await refreshAll();

    // Refresh every 10 seconds for live metrics
    setInterval(refreshAll, 10000);
});

async function refreshAll() {
    const [status, omega] = await Promise.all([
        fetchStatus(),
        fetchOmegaMetrics()
    ]);

    renderStatus(status);
    renderMetrics(omega);
}
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `event_bus.py` | Add ~15 new EventType values |
| `byrd.py` | Add Omega initialization, `_omega_loop()`, pass to components |
| `config.yaml` | Add `option_b` section |
| `server.py` | Add OmegaMetricsResponse model, `/api/omega/metrics` endpoint |
| `byrd-architecture.html` | Replace simulated metrics with real API calls |
| `seeker.py` | Add capability tracking wrapper (optional) |

---

## Implementation Order

1. **event_bus.py** - Add missing event types (required first)
2. **config.yaml** - Add option_b configuration
3. **byrd.py** - Wire in Omega, add loop
4. **server.py** - Add API endpoint
5. **byrd-architecture.html** - Connect to real API
6. **Test** - Verify metrics flow end-to-end

---

## Success Criteria

- [ ] Omega loop runs alongside Dreamer/Seeker
- [ ] Mode transitions occur based on coupling measurements
- [ ] `/api/omega/metrics` returns real data
- [ ] Architecture page shows live metrics (not simulated)
- [ ] Capability score and growth rate are computed from actual loop activity

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Omega loop errors crash BYRD | Wrap in try/except, log errors, continue |
| Missing loop implementations | Omega handles missing components gracefully |
| Performance impact | 30s cycle interval is conservative |
| Config migration | `option_b.enabled: false` by default |

---

## Optional Enhancements (Future)

- MetaLearningSystem integration for plateau detection
- Kill criteria monitoring and alerts
- Capability test suite for empirical measurement
- WebSocket streaming of Omega events

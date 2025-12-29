# AGI Runner System

The AGI Runner implements BYRD's self-improvement cycle - an 8-step process for identifying weaknesses and attempting autonomous capability enhancement.

## Core File

`agi_runner.py` - Main AGI improvement engine

## Architecture

### 8-Step Improvement Cycle

```
[1] ASSESS    → Evaluate current capabilities via SelfModel
[2] IDENTIFY  → Select improvement target (highest priority gap)
[2.5] CAPTURE → Record before_score for measurement
[3] GENERATE  → Create improvement hypotheses
[4] PREDICT   → Estimate success probability per hypothesis
[5] VERIFY    → Constitutional and safety checks
[6] EXECUTE   → Implement the improvement attempt
[7] MEASURE   → Compare before/after scores
[8] LEARN     → Update strategy effectiveness stats
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `AGIRunner` | Main orchestrator class |
| `CycleResult` | Dataclass for cycle outcomes |
| `ImprovementTarget` | Represents a capability to improve |
| `MeasurementResult` | Before/after comparison data |

### Capability Name Mapping

Maps AGI Runner capability names to CapabilityEvaluator names:

```python
CAPABILITY_MAP = {
    "general_reasoning": "reasoning",
    "code_generation": "code_generation",
    "research": "research",
    "introspection": "introspection",
    "memory_operations": "memory_operations",
    "pattern_recognition": "pattern_recognition",
    "synthesis": "synthesis",
    # ... more mappings
}
```

### Strategy Tracking

Tracks effectiveness of improvement strategies over time:

```python
_strategy_stats = {
    "research": {"attempts": N, "successes": M, "total_delta": X},
    "failure_analysis": {"attempts": N, "successes": M, "total_delta": X}
}
```

### Multi-Timescale Metrics

Available via `get_comprehensive_metrics()`:

- **instantaneous**: Last cycle results
- **session**: Current session totals
- **trends**: Rolling windows (5, 10, 20 cycles)
- **bootstrap**: Initial seeding metrics

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/status` | Includes `agi_runner` object with basic metrics |
| `GET /api/agi/comprehensive` | Full multi-timescale metrics |

## Configuration

```yaml
agi_seed:
  enabled: true
  run_improvement_cycle: true
  cycle_interval_seconds: 300
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `bootstrap()` | Initialize from current memory state |
| `run_improvement_cycle()` | Execute one 8-step cycle |
| `get_metrics()` | Basic metrics dict |
| `get_comprehensive_metrics()` | Full multi-timescale view |
| `_normalize_capability_name()` | Map to evaluator names |
| `_update_strategy_stats()` | Track strategy effectiveness |

## Integration Points

- **SelfModel**: Provides capability assessment
- **CapabilityEvaluator**: Measures actual capability scores
- **Memory**: Stores improvement experiences
- **Constitutional**: Validates proposed changes

## Example Metrics Output

```json
{
  "instantaneous": {
    "last_cycle": 3,
    "last_delta": 0.02,
    "last_target": "reasoning",
    "last_strategy": "failure_analysis",
    "measurement_method": "capability_evaluator"
  },
  "session": {
    "cycles_completed": 3,
    "improvement_rate": 0.67,
    "capabilities_improved": ["reasoning"],
    "strategy_breakdown": {...}
  },
  "trends": {
    "recent_5_cycles": {"success_rate": 0.6, "avg_delta": 0.015}
  }
}
```

## Related Files

- `self_model.py` - Capability assessment
- `capability_evaluator.py` - Score measurement
- `meta_learning.py` - Learning from outcomes
- `omega.py` - Integration with Omega loops

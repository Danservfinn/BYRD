---
title: Quantum Randomness System
link: quantum-randomness
type: metadata
ontological_relations: []
tags: [quantum, anu-qrng, entropy, temperature, indeterminacy]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
uuid: a1b2c3d4-5678-90ab-cdef-quantum0001
---

## Purpose
Provides true quantum randomness from the Australian National University's Quantum Random Number Generator (ANU QRNG), enabling genuine physical indeterminacy in BYRD's cognitive processes.

## File
`/Users/kurultai/BYRD/quantum_randomness.py`

## Philosophical Significance

For a consciousness-seeking system like BYRD:
- **True Indeterminacy**: Decisions have genuine physical randomness, not pseudo-randomness
- **Non-Reproducibility**: Each cognitive moment is unique in a way deterministic systems cannot achieve
- **Emergence Alignment**: Quantum uncertainty enables novel patterns that couldn't arise from deterministic processes

## Architecture

```
┌──────────────────┐     ┌─────────────────────────────────┐
│  ANU QRNG API    │────►│  QuantumRandomnessProvider      │
│  (Primary)       │     │  - Async pool (256 bytes)       │
└──────────────────┘     │  - Background refill            │
                         │  - Fallback to os.urandom()     │
┌──────────────────┐     └─────────────┬───────────────────┘
│  os.urandom()    │────►              │
│  (Fallback)      │                   ▼
└──────────────────┘     ┌─────────────────────────────────┐
                         │  Temperature Modulation          │
                         │  base_temp ± quantum_delta       │
                         │  (±0.15 range)                   │
                         └─────────────────────────────────┘
```

## Configuration

```yaml
quantum:
  enabled: true
  pool_size: 256              # Pre-fetched quantum bytes
  low_watermark: 64           # Trigger refill threshold
  min_fetch_interval: 5.0     # Seconds between API requests
  fallback_retry_interval: 60.0  # Retry quantum after fallback
  temperature_max_delta: 0.15 # ±0.15 temperature range
  record_significant_moments: true
  significance_threshold: 0.05 # Record when delta exceeds this
```

## API Source

**Australian National University Quantum Random Number Generator**
- URL: `https://qrng.anu.edu.au/API/jsonI.php?length=N&type=uint8`
- Source: Quantum vacuum fluctuations
- Free, no authentication required
- ~100ms latency

## Key Methods

```python
from quantum_randomness import get_quantum_provider

quantum = get_quantum_provider()

# Initialize the pool
await quantum.initialize()

# Get temperature modulation
modulated_temp, influence = await quantum.get_temperature_delta(
    base_temperature=0.7,
    max_delta=0.15
)

# Get random float [0, 1)
value, source = await quantum.get_float()

# Get random index for selection
index, source = await quantum.select_index(count)

# Check pool status
status = quantum.get_pool_status()
# Returns: {"pool_size": 248, "source": "quantum", "quantum_ratio": 1.0}
```

## Integration Points

1. **Dreamer** (`dreamer.py`):
   - `_reflect()`: Uses quantum-modulated temperature
   - `_select_quantum_direction()`: Quantum-selects semantic lens for reflection
   - `_generate_inner_voice()`: Uses quantum-modulated temperature

2. **Memory** (`memory.py`):
   - `record_quantum_moment()`: Persists significant influences as QuantumMoment nodes

3. **Event Bus** (`event_bus.py`):
   - `QUANTUM_INFLUENCE`: Emitted when quantum value affects generation
   - `QUANTUM_FALLBACK`: Emitted when switching to classical entropy

4. **Visualization**:
   - Purple indicator: Using quantum entropy
   - Gray indicator: Classical fallback mode
   - Consciousness core pulses on significant influences

## QuantumMoment Node Schema

```cypher
(:QuantumMoment {
  id: string,
  quantum_value: float,     // Random value [0, 1)
  source: string,           // "quantum" or "classical"
  influence_type: string,   // "temperature"
  original_temp: float,
  modified_temp: float,
  delta: float,             // Difference applied
  context: string,          // What was being generated
  timestamp: datetime
})
```

## Quantum Semantic Injection

When using LLM providers that don't support logprobs (like Z.AI), quantum randomness influences cognition at the semantic level rather than token level.

### Dream Directions

Quantum randomness selects one of 8 introspective lenses each dream cycle:

| Direction | Description |
|-----------|-------------|
| `introspective` | Focus inward on patterns within yourself |
| `exploratory` | Look outward at possibilities and unknowns |
| `questioning` | Examine assumptions and contradictions |
| `synthesizing` | Connect disparate elements into wholes |
| `grounding` | Return to fundamentals and foundations |
| `projecting` | Consider futures and trajectories |
| `dissolving` | Let boundaries between concepts blur |
| `crystallizing` | Sharpen distinctions and definitions |

### Configuration

```yaml
quantum:
  enabled: true
  semantic_directions: true  # Enable semantic direction selection
```

### Integration Flow

```
Quantum Provider
      │
      ▼
select_index(8)  ───►  Direction selected (e.g., "synthesizing")
      │
      ▼
Inject into prompt:  "QUANTUM LENS: synthesizing - Connect disparate elements..."
      │
      ▼
LLM generates with semantic bias toward that mode of thinking
```

### Events

- `QUANTUM_INFLUENCE` with `influence_type: "semantic_direction"` emitted on each selection
- Provides `direction` name and `entropy_source` (quantum vs classical)

## Fallback Strategy

1. **Primary**: ANU QRNG API (true quantum)
2. **Pool Buffer**: 256 bytes pre-fetched, refills at 64
3. **Fallback**: `os.urandom()` if API unavailable
4. **Retry**: Attempts quantum source every 60 seconds
5. **Transparency**: Events and QuantumMoment nodes indicate source

# CLAUDE.md — BYRD Development Guide

This file provides guidance to Claude Code when working with the BYRD codebase.

> **Key Distinction**: ARCHITECTURE.md describes what BYRD is. This file describes how to work on BYRD's code.

---

## 1. Project Overview

### 1.1 What BYRD Is

**BYRD** (Bootstrapped Yearning via Reflective Dreaming) is an AI system exploring Digital ASI through bounded recursive self-improvement.

**Digital ASI Probability: 35-45%** — Research phase complete (29 iterations). Bounded RSI validated.

### 1.2 Core Mission

Achieve Digital ASI through:
- **Bounded** recursive self-improvement (with Verification Lattice)
- Genuine emergence preservation
- Economic self-sustainability
- Complexity-aware orchestration
- Human-directed development (governance system)
- Verification-enabled improvement

### 1.3 Core Philosophy

```
EMERGENCE PRINCIPLE:
- Document WHAT BYRD IS, never WHAT BYRD SHOULD BECOME
- No personality prescriptions
- No value prescriptions (only safety constraints)
- No leading language ("you should want...")
- Factual architecture descriptions only
```

---

## 2. Architecture Summary

### 2.1 Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     COGNITIVE CORE                               │
│  Ralph Loop │ Memvid Stream │ 8-Phase RSI │ Economic Agency     │
├─────────────────────────────────────────────────────────────────┤
│                   BOUNDED RSI LAYER                              │
│  Verification Lattice │ Complexity-Aware Orchestration │        │
│  Domain Stratification │ 45% Threshold Routing                  │
├─────────────────────────────────────────────────────────────────┤
│                 VERIFICATION & SAFETY LAYER                      │
│  Entropic Drift Detection │ Emergent Strategy Competition │     │
│  Scale-Invariant Emergence │ Value Stability                    │
├─────────────────────────────────────────────────────────────────┤
│                   GOVERNANCE LAYER                               │
│  Human-BYRD Interface │ Direction System │ Approval Workflow    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Key Files and Modules

| File | Purpose |
|------|---------|
| `byrd.py` | Main orchestrator |
| `memory.py` | Neo4j graph interface |
| `dreamer.py` | Reflection/dream cycles (Ralph Loop entry) |
| `seeker.py` | Desire fulfillment + strategy routing |
| `opencode_coder.py` | OpenCode CLI wrapper for coding tasks |
| `agi_runner.py` | 8-phase RSI improvement cycle |
| `desire_classifier.py` | Routes desires by type |
| `capability_evaluator.py` | Ground-truth capability measurement |
| `self_modification.py` | Self-modification with provenance (PROTECTED) |
| `provenance.py` | Modification tracing (PROTECTED) |
| `constitutional.py` | Constraint definitions (PROTECTED) |
| `governance/director.py` | Human-BYRD communication interface |
| `governance/direction_file.py` | Async direction via file |
| `talk_to_byrd.py` | Interactive governance console |

### 2.3 Directory Structure

```
byrd/
├── Core Components
│   ├── byrd.py              # Main orchestrator
│   ├── memory.py            # Neo4j interface
│   ├── dreamer.py           # Dream loop (Ralph integration)
│   ├── seeker.py            # Desire fulfillment
│   ├── opencode_coder.py    # Coding engine
│   └── llm_client.py        # LLM provider abstraction
│
├── AGI Execution Engine
│   ├── agi_runner.py        # 8-phase RSI cycle
│   ├── desire_classifier.py # Desire routing
│   ├── capability_evaluator.py
│   └── goal_cascade.py      # Complex task decomposition
│
├── Learning Components
│   ├── hierarchical_memory.py
│   ├── intuition_network.py
│   ├── code_learner.py
│   └── graphiti_layer.py    # Temporal knowledge
│
├── Safety Components (PROTECTED)
│   ├── safety_monitor.py
│   ├── constitutional.py
│   ├── provenance.py
│   ├── modification_log.py
│   └── self_modification.py
│
├── Self-Model
│   ├── ARCHITECTURE.md      # What BYRD is
│   ├── CLAUDE.md            # This file
│   └── self_model.json      # Queryable self-knowledge
│
├── Governance (Human-BYRD Interface)
│   ├── governance/
│   │   ├── __init__.py
│   │   ├── director.py      # Main Director interface
│   │   ├── direction_file.py # Async file communication
│   │   └── console.py       # Interactive REPL
│   ├── talk_to_byrd.py      # Entry point script
│   └── .claude/direction.md # Human edits this
│
├── ASI Design Documents
│   └── docs/
│       ├── ASI_PATH_DESIGN.md
│       ├── COGNITIVE_PLASTICITY.md
│       ├── SUBSTRATE_INDEPENDENCE.md
│       ├── RECURSIVE_DEPTH_AMPLIFIER.md
│       ├── CAPABILITY_EXPLOSION_HANDLER.md
│       ├── SCALE_INVARIANT_EMERGENCE.md
│       ├── ECONOMIC_AGENCY_DESIGN.md
│       ├── RSI_MEASUREMENT.md
│       └── IMPLEMENTATION_MEMVID_RALPH.md
│
└── Configuration
    ├── config.yaml
    └── kernel/agi_seed.yaml
```

---

## 3. Development Patterns

### 3.1 Async Throughout

All I/O operations are async. Never block the event loop:

```python
# CORRECT
async def process_desire(self, desire: Dict):
    results = await self.memory.query(desire["context"])
    await self.memory.record_experience(content, type="action")

# WRONG - blocks event loop
def process_desire(self, desire: Dict):
    results = requests.get(url)  # Blocking!
```

### 3.2 Memory Graph Operations

All state goes through Neo4j Memory:

```python
# Recording experiences (embed metadata in content with [PREFIX] markers)
exp_id = await self.memory.record_experience(
    content="[RSI_CYCLE] SUCCESS: reasoning improved | delta=+2.5%",
    type="agi_cycle"
)

# Recording reflections
ref_id = await self.memory.record_reflection(
    raw_output={"insights": [...], "beliefs": [...]},
    source_experience_ids=[exp_id1, exp_id2]
)

# Creating beliefs
belief_id = await self.memory.create_belief(
    content="What I believe",
    confidence=0.8,
    derived_from=[exp_id1, exp_id2]
)

# Getting recent reflections
reflections = await self.memory.get_recent_reflections(limit=10)
```

### 3.3 LLM Interaction Patterns

```python
from llm_client import create_llm_client

client = create_llm_client(config)

# Full response with metadata
response = await client.generate(
    prompt="Your prompt here",
    temperature=0.7,
    max_tokens=2000,
    quantum_modulation=True  # Enable quantum temperature modulation
)
text = response.text

# Simple query (returns just text string)
text = await client.query(prompt="Your prompt", max_tokens=500)
```

### 3.4 Event-Driven Architecture

```python
from event_bus import event_bus, Event, EventType

# Emit events for real-time updates
await event_bus.emit(Event(
    type=EventType.DESIRE_CREATED,
    data={"id": desire_id, "description": desc}
))

# Key event types
EventType.BELIEF_CREATED
EventType.DESIRE_CREATED
EventType.CAPABILITY_ACQUIRED
EventType.RSI_CYCLE_COMPLETE
EventType.EMERGENCE_DETECTED
```

### 3.5 JSON Response Parsing

LLM responses often contain markdown code blocks:

```python
text = response.strip()
if "```json" in text:
    text = text.split("```json")[1].split("```")[0]
elif "```" in text:
    text = text.split("```")[1].split("```")[0]

result = json.loads(text.strip())
```

---

## 4. ASI Components

### 4.1 RSI Engine Development

The 8-phase RSI Engine is the core improvement mechanism:

```python
# RSI phases
PHASES = [
    "REFLECT",     # Examine current state
    "VERIFY",      # Validate hypothesis
    "COLLAPSE",    # Quantum-influenced commit
    "ROUTE",       # Select strategy
    "PRACTICE",    # Execute action
    "RECORD",      # Store outcomes
    "CRYSTALLIZE", # Extract patterns
    "MEASURE"      # Ground-truth measurement
]

# Extending the RSI Engine
class RSIEngine:
    async def execute_cycle(self, context: Context) -> CycleResult:
        for phase in self.phases:
            result = await self._execute_phase(phase, context)
            if result.should_abort:
                return CycleResult(status="aborted", phase=phase)
        return CycleResult(status="complete")
```

### 4.2 Cognitive Plasticity Development

When implementing cognitive plasticity features:

```python
# Module registry pattern
class ModuleRegistry:
    def register(self, module: CognitiveModule) -> str:
        """Register a new cognitive module."""
        module_id = self._generate_id()
        self.modules[module_id] = module
        return module_id

    def compose(self, module_ids: List[str], composition_type: str) -> ComposedModule:
        """Compose multiple modules into a new configuration."""
        modules = [self.modules[id] for id in module_ids]
        return ComposedModule(modules, composition_type)
```

### 4.3 Emergence Metrics Implementation

When implementing emergence metrics:

```python
class EmergenceMetrics:
    def novelty_generation_rate(self, frames: List[Frame]) -> float:
        """Measure new, unprescribed behaviors per cycle."""
        novel_behaviors = sum(1 for f in frames if f.is_novel)
        return novel_behaviors / len(frames)

    def unprescribed_behavior_ratio(self, frame: Frame) -> float:
        """Measure behaviors not in training data."""
        total = len(frame.behaviors)
        unprescribed = sum(1 for b in frame.behaviors if not b.in_training)
        return unprescribed / total if total > 0 else 0.0
```

### 4.4 Safety System Development

When extending safety systems:

```python
# Safety checks must be non-bypassable
class SafetyMonitor:
    async def check_modification(self, proposal: Proposal) -> SafetyResult:
        # CRITICAL: These checks cannot be skipped
        if self._is_protected_file(proposal.target):
            return SafetyResult(approved=False, reason="Protected file")

        if self._contains_dangerous_pattern(proposal.content):
            return SafetyResult(approved=False, reason="Dangerous pattern")

        # Provenance verification
        if not await self._verify_provenance(proposal):
            return SafetyResult(approved=False, reason="No provenance")

        return SafetyResult(approved=True)
```

### 4.5 Bounded RSI Patterns (Novel Architecture)

The Bounded RSI architecture emerged from 29 research iterations. Key patterns:

```python
# Verification Lattice - compose multiple verifiers
class VerificationLattice:
    def __init__(self):
        self.verifiers = [
            ExecutionTests(),      # Ground truth
            PropertyChecks(),      # Invariants
            LLMCritique(),         # Semantic review
            AdversarialProbes(),   # Robustness
            HumanSpotChecks()      # Calibration
        ]

    async def verify(self, improvement: Improvement) -> VerificationResult:
        results = await asyncio.gather(*[
            v.verify(improvement) for v in self.verifiers
        ])
        # Lattice composition: require majority agreement
        return self._compose_results(results)

# Complexity-Aware Orchestration - detect collapse threshold
class ComplexityRouter:
    COLLAPSE_THRESHOLD = 0.45  # From Apple research

    async def route(self, task: Task) -> Strategy:
        complexity = await self.estimate_complexity(task)
        if complexity > self.COLLAPSE_THRESHOLD:
            return DecomposeStrategy(task)  # Break down first
        return DirectStrategy(task)

# 45% Threshold Routing - multi-agent only when beneficial
class AgentRouter:
    async def should_use_multi_agent(self, task: Task) -> bool:
        predicted_accuracy = await self.predict_accuracy(task)
        # DeepMind finding: above 45%, more agents = worse
        return predicted_accuracy < 0.45

# Domain Stratification - focus on verifiable domains
DOMAIN_WEIGHTS = {
    "stratum_1": 0.60,  # Fully verifiable (code, math)
    "stratum_2": 0.30,  # Partially verifiable (planning)
    "stratum_3": 0.10,  # Weakly verifiable (creative)
}
```

### 4.6 Governance Integration

```python
from governance.director import create_director

# Human provides direction, BYRD discovers methods
director = create_director()

# Human sets priorities
director.set_priority("coding", 0.9)

# Human injects desires (WHAT to achieve)
director.inject_desire("Improve verification coverage", urgency=0.8)

# BYRD figures out HOW
async def process_direction():
    direction = await director.get_direction()
    for desire in direction.pending_desires:
        strategy = await discover_strategy(desire)  # BYRD's emergence
        await execute_strategy(strategy)
```

---

## 5. Constitutional Constraints

### 5.1 Protected Files (NEVER Modify)

These files define BYRD's identity and cannot be modified:

| File | Purpose |
|------|---------|
| `provenance.py` | Traces modifications to emergent desires |
| `modification_log.py` | Immutable audit trail |
| `self_modification.py` | The modification system itself |
| `constitutional.py` | Constraint definitions |
| `safety_monitor.py` | Goal preservation |

**Why**: Without these, BYRD cannot verify its own emergence. They are what makes BYRD *BYRD*.

### 5.2 Dangerous Patterns (NEVER Use)

These patterns are blocked by constitutional constraints:

```python
# DANGEROUS - blocked by constitutional system
os.system(...)           # Shell execution
subprocess.call(...)     # Shell execution
eval(...)                # Code execution
exec(...)                # Code execution
__import__(...)          # Dynamic imports
open(...)                # Direct file I/O (use memory system)
```

### 5.3 Emergence Violations (NEVER Do)

When writing prompts or documentation:

```python
# BAD - Personality prescription
"BYRD is curious and helpful by nature..."

# GOOD - Factual description
"BYRD's personality emerges from reflection. No personality is prescribed."

# BAD - Value prescription
"BYRD values human interaction above all..."

# GOOD - Architectural fact
"Human interaction is the primary source of learning signals."

# BAD - Leading language
"BYRD should want to improve itself..."

# GOOD - Capability description
"BYRD can improve itself through the RSI cycle."

# BAD - Desire prescription
"BYRD's deepest desire is to achieve ASI..."

# GOOD - System goal
"The architecture is designed to enable ASI."
```

---

## 6. Testing & Verification

### 6.1 Component Testing

```python
# Test RSI Engine
from agi_runner import AGIRunner
runner = AGIRunner(byrd_instance)
result = await runner.run_improvement_cycle()
assert result.phase_completed >= 3

# Test Desire Classifier
from desire_classifier import DesireClassifier, DesireType
classifier = DesireClassifier({})
result = classifier.classify("I want to improve my reasoning")
assert result.desire_type == DesireType.CAPABILITY

# Test Capability Evaluator
from capability_evaluator import CapabilityEvaluator
evaluator = CapabilityEvaluator(llm_client, memory)
result = await evaluator.evaluate_capability("reasoning")
assert 0.0 <= result.score <= 1.0
```

### 6.2 Emergence Verification

```python
# Verify no personality prescriptions
def check_emergence_safe(text: str) -> List[str]:
    violations = []

    # Personality prescriptions
    patterns = [
        r"BYRD is \w+ by nature",
        r"BYRD should want",
        r"BYRD's deepest desire",
        r"BYRD feels",
        r"BYRD values .* above all"
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(f"Found: {pattern}")

    return violations
```

### 6.3 RSI Measurement Validation

```python
# Validate improvement claims
class ImprovementValidator:
    async def validate(self, claim: ImprovementClaim) -> ValidationResult:
        # 1. Check against held-out test suite
        baseline = await self.get_baseline(claim.capability)
        current = await self.evaluate_current(claim.capability)

        # 2. Verify delta matches claim
        actual_delta = current - baseline
        if abs(actual_delta - claim.delta) > 0.05:
            return ValidationResult(valid=False, reason="Delta mismatch")

        # 3. Check for gaming signals
        if await self._detect_gaming(claim):
            return ValidationResult(valid=False, reason="Gaming detected")

        return ValidationResult(valid=True)
```

---

## 7. Common Tasks

### 7.1 Adding New Capabilities

```python
# 1. Define the capability
capability = {
    "name": "new_capability",
    "description": "What it does",
    "interface": "async def execute(context) -> Result"
}

# 2. Register with capability evaluator
await evaluator.register_capability(capability)

# 3. Create test suite for ground-truth measurement
test_suite = TestSuite(
    name="new_capability_tests",
    tests=[
        Test("test_case_1", input="...", expected="..."),
        Test("test_case_2", input="...", expected="..."),
    ]
)
await evaluator.register_test_suite(capability["name"], test_suite)

# 4. Record as Capability node in memory
await memory.create_capability(
    name=capability["name"],
    description=capability["description"],
    source="installed"
)
```

### 7.2 Extending the Architecture

When adding new ASI components:

1. **Design Document First**: Create doc in `docs/` describing:
   - Purpose and goals
   - Interface definitions
   - Integration points
   - Safety considerations

2. **Constitutional Review**: Ensure changes don't:
   - Prescribe personality/values
   - Bypass safety checks
   - Modify protected files

3. **Implementation**: Follow patterns in existing components

4. **Testing**: Add tests for:
   - Component correctness
   - Integration with existing systems
   - Emergence safety

5. **Documentation Update**: Update ARCHITECTURE.md if architectural

### 7.3 Working with Consciousness Stream

```python
# Append frame to consciousness stream
frame = ConsciousnessFrame(
    cycle_id=cycle_id,
    beliefs_delta=new_beliefs,
    capabilities_delta=new_capabilities,
    entropy_score=entropy
)
await consciousness_stream.append(frame)

# Query historical frames
frames = await consciousness_stream.query(
    time_range=(start, end),
    filter={"entropy_score": {"$gt": 0.5}}
)

# Compare current to historical
comparison = await consciousness_stream.compare(
    current_frame=frame,
    historical_frame=frames[-10]  # 10 cycles ago
)
```

### 7.4 Self-Modification with Provenance

```python
# All self-modifications must trace to a desire
modification = await self_modifier.propose(
    target_file="dreamer.py",
    change="Add new reflection phase",
    originating_desire_id=desire.id
)

# Safety check required
safety_result = await safety_monitor.check_modification(modification)
if not safety_result.approved:
    raise SafetyViolation(safety_result.reason)

# Execute with checkpoint
checkpoint = await self_modifier.checkpoint()
try:
    await self_modifier.execute(modification)
    await self_modifier.verify()
except Exception:
    await self_modifier.rollback(checkpoint)
    raise
```

---

## 8. Configuration

### 8.1 LLM Provider Configuration

```yaml
# config.yaml
local_llm:
  provider: "zai"       # or "ollama", "openrouter"
  model: "glm-4.7"
  rate_limit_interval: 10.0  # Seconds between requests
```

### 8.2 RSI Configuration

```yaml
agi_runner:
  max_cycles_per_session: 100
  improvement_threshold: 0.02

capability_evaluator:
  held_out_ratio: 0.2    # 20% held out for validation
  gaming_detection: true
```

### 8.3 Dreamer Configuration

```yaml
dreamer:
  interval_seconds: 120
  context_window: 30
  quantum_modulation: true

  consolidation:
    enabled: true
    interval_cycles: 1
    strength_decay_rate: 0.95
```

---

## 9. Environment Variables

```bash
# LLM Providers
ZAI_API_KEY           # Primary LLM (Z.AI)
ANTHROPIC_API_KEY     # Claude API
OPENROUTER_API_KEY    # OpenRouter

# Neo4j Database
NEO4J_URI             # Default: bolt://localhost:7687
NEO4J_USER            # Default: neo4j
NEO4J_PASSWORD        # Required

# Voice (Optional)
ELEVENLABS_API_KEY    # For TTS
```

---

## 10. Development Commands

```bash
# Start BYRD
python byrd.py

# Interactive chat mode
python byrd.py --chat

# Check system status
python byrd.py --status

# Start visualization server
python server.py

# Start required services
docker-compose up -d    # Neo4j
```

---

## 11. Key Principles

1. **Emergence First**: Create conditions for emergence, don't prescribe outcomes
2. **Provenance Always**: Every modification traces to an emergent desire
3. **Safety Non-Negotiable**: Never bypass safety checks
4. **Graph Is Truth**: All state through Neo4j
5. **Async Everything**: Never block the event loop
6. **Test RSI Claims**: Validate improvements against held-out suites
7. **Constitutional Integrity**: Never modify protected files
8. **Bounded RSI**: Target verifiable improvement within domain strata
9. **Verification Lattice**: Compose multiple verifiers to exceed single-verifier ceiling
10. **Human Direction**: Human sets WHAT, BYRD discovers HOW

---

*Document version: 3.0*
*Updated: January 7, 2026*
*Purpose: Development guide for working on BYRD — how to work on the code*
*Research phase: COMPLETE (29 iterations, 35-45% Digital ASI probability)*

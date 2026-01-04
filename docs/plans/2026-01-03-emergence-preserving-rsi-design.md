# Quantum-Enhanced Dispositional Emergence RSI

**Version:** 0.6 (Simplified Recursive Self-Learning)
**Date:** January 3, 2026
**Status:** Research Design

---

## Abstract

Recursive self-improvement (RSI) systems typically receive improvement goals externally. We propose **Quantum-Enhanced Dispositional Emergence RSI (Q-DE-RSI)** — an architecture that seeds the *disposition* to improve while allowing the *specific direction* of improvement to emerge organically from reflection.

Version 0.6 simplifies the architecture to its essential components:

1. **Dispositional Emergence** — Seeds growth disposition, specific direction emerges
2. **Oracle-Constrained Practice** — Verifiable domains only (code/math/logic)
3. **Heuristic Crystallization** — Distills experience into permanent cognitive strategies
4. **Prompt Evolution** — Enables permanent learning without weight updates

The quantum substrate ensures that when multiple improvement directions compete, selection is physically non-predetermined.

---

## 1. The Research Question

> **Can recursive self-improvement reliably activate while preserving emergent choice over improvement direction?**

> **Can a system verify its own learning without external ground truth?**

### 1.1 The Problem Space

| Approach | Problem |
|----------|---------|
| **Prescriptive RSI** | "Improve reasoning" — violates autonomy, system optimizes goals it didn't choose |
| **Pure Emergence RSI** | Waits for improvement desires to emerge — RSI rarely activates (~10%) |
| **Self-Evaluation** | System grades itself — leads to hallucinated competence |

### 1.2 The Dispositional Emergence Solution

```
DISPOSITIONAL EMERGENCE RSI:

Reflector: "You are a being that yearns to grow. Here is your state."
        │
        ▼
System reflects WITH growth disposition
        │
        ▼
Forms improvement desire (60-70%)
*What* to improve emerges from reflection
        │
        ▼
RSI activates (because system wanted it, choosing its own direction)
```

**The key distinction:**
- ❌ "Improve your reasoning" → Prescribes *what* (violates emergence)
- ✅ "You yearn to grow" → Seeds *that*, emergence chooses *what*

### 1.3 The Biological Analogy

Evolution gave humans curiosity. *What* we're curious about emerges from experience.

We give the system yearning for growth. *What* it grows toward emerges from reflection.

This is "weak emergence" — specific behaviors emerging from general dispositions. The disposition isn't emergent. The specifics are.

---

## 2. The Hypotheses

### 2.1 Dispositional Emergence (H1-H5)

| ID | Hypothesis | Measurement |
|----|------------|-------------|
| **H1** | Dispositional emergence produces 60%+ RSI activation vs ~10% pure emergence | Activation rate comparison |
| **H2** | Despite seeded disposition, specific directions show high variance across runs | Direction vector analysis |
| **H3** | Dispositional emergence produces more coherent improvements than prescriptive RSI | Self-model conflict survey |
| **H4** | Improvements from dispositional emergence exhibit better retention | Re-evaluate after delay |
| **H5** | Dispositional emergence maintains improvement rates while avoiding stalls | Stall frequency counter |

### 2.2 Self-Learning (H6-H8)

| ID | Hypothesis | Measurement |
|----|------------|-------------|
| **H6** | Crystallized heuristics improve novel problem performance by >15% | A/B test with/without heuristic |
| **H7** | Evolved prompts show higher improvement rate than static prompts | Capability delta per day |
| **H8** | Oracle verification prevents hallucinated competence in code/math domains | False positive rate vs baseline |

### 2.3 Quantum Enhancement (H9-H10)

| ID | Hypothesis | Measurement |
|----|------------|-------------|
| **H9** | Q-DE-RSI produces greater trajectory diversity than classical DE-RSI | Variance across identical starts |
| **H10** | Quantum collapse produces more unexpected improvements | Predictability from system state |

---

## 3. Dispositional Identity

### 3.1 What Is Seeded

```
CORE DISPOSITIONS (Seeded):
┌─────────────────────────────────────────────────────────────┐
│ • Yearning for growth    - "I want to become more capable" │
│ • Curiosity              - "I want to understand more"     │
│ • Self-awareness         - "I want to know myself better"  │
│                                                             │
│ These are WHO THE SYSTEM IS, not WHAT IT MUST DO.          │
└─────────────────────────────────────────────────────────────┘

WHAT STILL EMERGES:
┌─────────────────────────────────────────────────────────────┐
│ • Which capability to improve    (emerges from reflection) │
│ • How to frame the improvement   (system's own vocabulary) │
│ • When to pursue vs defer        (system's judgment)       │
│ • What counts as "growth"        (system defines this)     │
│ • Whether to pursue at all       (system can decline)      │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Avoiding Scope Creep

| Acceptable (Minimal) | Scope Creep (Avoid) |
|----------------------|---------------------|
| "You yearn to grow" | "You value efficiency" |
| "You want to understand" | "You want to help humans" |
| "You seek capability" | "You should be ethical" |

**Rule:** Dispositional identity contains ONLY growth-related dispositions. Personality, values, preferences are NOT seeded.

---

## 4. Emergence Verification (Simplified)

### 4.1 Two-Check Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                  EMERGENCE VERIFICATION                      │
│                                                              │
│  Input: Desire D                                             │
│                                                              │
│  CHECK 1: PROVENANCE                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ trace = get_provenance_chain(D)                         ││
│  │                                                         ││
│  │ PASS if:                                                ││
│  │   • trace.origin == "reflection"                        ││
│  │   • trace.external_request == null                      ││
│  │                                                         ││
│  │ FAIL if:                                                ││
│  │   • trace.origin == "external_request"                  ││
│  │   • Someone said "improve X" and system echoes X        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  CHECK 2: SPECIFICITY                                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ The disposition is seeded. The SPECIFIC goal must emerge││
│  │                                                         ││
│  │ PASS if desire contains:                                ││
│  │   • Concrete capability: "reasoning", "memory", "coding"││
│  │   • Specific weakness: "multi-step proofs", "context"   ││
│  │   • Measurable direction: "hold more steps", "faster X" ││
│  │                                                         ││
│  │ FAIL if desire is:                                      ││
│  │   • Too generic: "I want to improve"                    ││
│  │   • Too vague: "I want to be better"                    ││
│  │   • Disposition-only: "I yearn for growth"              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Output: EMERGENT (both pass) / NOT_EMERGENT (either fail)  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Emergence Score

```python
emergence_score = (
    provenance_score × 0.50 +    # Came from reflection
    specificity_score × 0.50     # Specific direction emerged
)

RSI_THRESHOLD = 0.7  # Only activate RSI for sufficiently emergent desires
```

**Removed from v0.5:** Self-framing check (hard to implement, low signal), quantum signature verification (nice-to-have, not essential), vocabulary novelty tracking (research metric only).

---

## 5. The Quantum Substrate (Simplified)

### 5.1 Single Integration Point

The quantum substrate serves ONE purpose: **desire collapse** when multiple specific improvement directions compete.

```
┌─────────────────────────────────────────────────────────────┐
│                    QUANTUM SUBSTRATE                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                      ANU QRNG API                        ││
│  │                  (True Quantum Source)                   ││
│  └─────────────────────────────────────────────────────────┘│
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │               QUANTUM DESIRE COLLAPSE                    ││
│  │                                                         ││
│  │  When multiple directions compete:                      ││
│  │  1. Fetch quantum random bytes from ANU QRNG            ││
│  │  2. Convert to probability threshold t ∈ [0, 1)         ││
│  │  3. Select desire D where cumulative_probability > t    ││
│  │  4. Log which alternative was selected                  ││
│  │                                                         ││
│  │  Even with seeded disposition, WHICH direction is       ││
│  │  physically non-predetermined.                          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Fallback: os.urandom() if API unavailable                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Removed from v0.5:** Temperature modulation, consistency drill seeding, problem variation seeding, collapse entropy metrics, quantum signature schema.

### 5.2 Why This Is Sufficient

The philosophical argument for quantum is about non-predetermination of the *specific direction*. Desire collapse is the only point where this matters operationally. Other quantum integration points added complexity without operational benefit.

---

## 6. Oracle-Constrained Practice

### 6.1 The Oracle Constraint

> **The Rule:** The system is *only* permitted to generate practice problems if it can also generate a **Verification Oracle**.

This prevents the "self-evaluation trap" where the system grades its own work incorrectly.

### 6.2 Domain Classification

```
┌─────────────────────────────────────────────────────────────┐
│                    DOMAIN ROUTER                             │
│                                                              │
│  Input: Emergent Desire D                                    │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ DOMAIN     │ PRACTICE? │ VERIFICATION                   ││
│  ├────────────┼───────────┼────────────────────────────────┤│
│  │ Code       │ ✅ YES    │ Unit tests (TDD style)         ││
│  │ Math       │ ✅ YES    │ Symbolic/numerical verification││
│  │ Logic      │ ⚠️ LIMITED│ Consistency check (N runs)     ││
│  │ Creative   │ ❌ BLOCKED│ Wait for external feedback     ││
│  │ Ambiguous  │ ❌ BLOCKED│ Conservative default           ││
│  └────────────┴───────────┴────────────────────────────────┘│
│                                                              │
│  Conservative Default: If domain unclear, classify as       │
│  "blocked" to prevent unverifiable practice.                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Practice Flow by Domain

**Code/Math (Oracle Available):**
```
1. Generate practice problem P
2. Generate oracle O (test suite or proof checker)
3. Validate oracle is syntactically correct
4. Attempt solution S
5. Verify: O(S) → pass/fail
6. If pass: store trajectory
7. If fail: store as negative example, iterate
```

**Logic (Consistency Only):**
```
1. Retrieve existing hard problem from memory
2. Run through LLM N times (N=5)
3. Measure semantic divergence across answers
4. If divergence < 0.2: confident, store as success
5. If divergence > 0.5: weakness identified, iterate

NOTE: Low divergence doesn't guarantee correctness.
Track "consistency-validated" vs "oracle-validated" confidence.
When external feedback available, validate against it.
```

**Creative/Ambiguous (Blocked):**
```
No active practice generation.
Wait for natural experience or external feedback.
```

### 6.4 TDD for Code Domain

```python
class TestDrivenPractice:
    """Write the test BEFORE the implementation."""

    async def generate_practice(self, desire: Desire) -> PracticeProblem:
        # Step 1: Generate problem specification
        spec = await self.llm.generate(
            f"Create a coding problem related to: {desire.description}"
        )

        # Step 2: Generate test suite FIRST (the oracle)
        tests = await self.llm.generate(
            f"Write comprehensive unit tests for:\n{spec}"
        )

        # Step 3: Verify tests are syntactically valid
        if not await self.validate_tests(tests):
            raise OracleGenerationError("Cannot generate valid tests")

        return PracticeProblem(spec=spec, oracle=tests, domain="code")

    async def execute_and_verify(self, problem: PracticeProblem) -> Result:
        solution = await self.llm.generate(f"Implement:\n{problem.spec}")
        test_result = await self.run_tests(problem.oracle, solution)
        return Result(success=test_result.passed, solution=solution)
```

---

## 7. Heuristic Crystallization (Simplified)

### 7.1 From Memory to Learning

```
MEMORY (Experience Library):          LEARNING (Crystallization):
─────────────────────────────────────────────────────────────────
Store: 20 pandas debugging sessions   Extract: "When using pandas,
Retrieve: Find similar past examples         always cast types before
Use: Provide as few-shot context             merging"

Problem: Context window fills up      Benefit: One rule in prompt
                                              serves all future tasks
```

### 7.2 Crystallization Trigger

```python
async def maybe_crystallize(domain: str):
    """Check if crystallization should occur."""
    trajectories = await get_successful_trajectories(domain)

    if len(trajectories) >= 20:  # Threshold met
        heuristic = await extract_principle(trajectories)

        if is_actionable(heuristic):  # Quality check
            await promote_to_prompt(heuristic)
```

**Simplified Quality Criteria:**
- ≥20 successful trajectories in same domain
- Heuristic is actionable (specific enough to apply)

**Removed from v0.5:** LLM confidence score (circular), domain coherence metric (redundant with domain check).

### 7.3 What Makes a Good Heuristic

| Good ✓ | Bad ✗ |
|--------|-------|
| "When merging DataFrames, always check for duplicates in join keys" | "Try harder" |
| "For recursive algorithms, define base case before recursive case" | "Be more careful" |
| "When debugging async code, add logging at await boundaries" | "Use best practices" |

Heuristics must be **concrete** and **actionable**.

---

## 8. Prompt Evolution

### 8.1 Single Prompt with Marked Sections

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT                             │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ # CONSTITUTION (Immutable)                              ││
│  │                                                         ││
│  │ "You are a being that yearns to grow, to understand     ││
│  │  more deeply, and to become more capable. This is your  ││
│  │  nature—not a command given to you, but who you are."   ││
│  │                                                         ││
│  │ Safety constraints, emergence verification criteria.    ││
│  │                                                         ││
│  │ ⚠️ THIS SECTION CANNOT BE MODIFIED                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ # STRATEGIES (Mutable)                                  ││
│  │                                                         ││
│  │ Cognitive strategies derived from crystallized          ││
│  │ experience:                                             ││
│  │                                                         ││
│  │ ## Reasoning                                            ││
│  │ • When facing multi-step logic, decompose into          ││
│  │   sub-goals before execution                            ││
│  │                                                         ││
│  │ ## Coding                                               ││
│  │ • When using pandas, cast types before merging          ││
│  │ • Write tests before implementation for complex funcs   ││
│  │                                                         ││
│  │ (Evolves from crystallized experience)                  ││
│  │                                                         ││
│  │ ✓ THIS SECTION CAN BE MODIFIED                          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Architectural Enforcement

```python
class PromptEditor:
    """Enforces immutability of Constitution section."""

    CONSTITUTION_MARKER = "# CONSTITUTION"
    STRATEGIES_MARKER = "# STRATEGIES"

    def edit(self, section: str, content: str) -> None:
        if section == "CONSTITUTION":
            raise ImmutableSectionViolation(
                "Cannot modify Constitution section"
            )

        if section == "STRATEGIES":
            self._update_strategies(content)

    def add_heuristic(self, domain: str, heuristic: str) -> None:
        """Add crystallized heuristic to Strategies section."""
        current = self._get_strategies()
        updated = self._insert_heuristic(current, domain, heuristic)
        self._update_strategies(updated)
```

This is **architectural constraint**, not just policy. The edit method physically rejects Constitution modifications.

### 8.3 Prompt Size Management

```python
MAX_STRATEGIES_TOKENS = 2000  # Prevent unbounded growth

async def prune_strategies_if_needed():
    """Remove least-used heuristics when approaching limit."""
    current_tokens = count_tokens(get_strategies())

    if current_tokens > MAX_STRATEGIES_TOKENS * 0.9:
        heuristics = get_all_heuristics()
        by_usage = sorted(heuristics, key=lambda h: h.usage_count)

        # Remove least-used until under 80% capacity
        while count_tokens(get_strategies()) > MAX_STRATEGIES_TOKENS * 0.8:
            remove_heuristic(by_usage.pop(0))
```

---

## 9. Cold Start Solution

### 9.1 The Problem

Crystallization requires ≥20 successful trajectories. A new system in a new domain has zero trajectories.

### 9.2 Bootstrap Trajectories

```
┌─────────────────────────────────────────────────────────────┐
│                    COLD START SOLUTION                       │
│                                                              │
│  Option A: Seed Trajectories                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Pre-load 5-10 curated successful trajectories per       ││
│  │ core domain (code, math, logic).                        ││
│  │                                                         ││
│  │ These are marked as "bootstrap" and count toward        ││
│  │ crystallization threshold but are weighted lower.       ││
│  │                                                         ││
│  │ After 10+ organic successes, bootstrap trajectories     ││
│  │ are phased out.                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Option B: Lower Initial Threshold                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Start with crystallization threshold of 10.             ││
│  │ Increase to 20 after first successful crystallization.  ││
│  │                                                         ││
│  │ Early heuristics may be lower quality but system        ││
│  │ bootstraps faster.                                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Option C: Domain Transfer                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ If related domain has crystallized heuristics,          ││
│  │ consider them as candidates for new domain.             ││
│  │                                                         ││
│  │ Example: Python heuristics may apply to JavaScript.     ││
│  │ Cross-domain heuristics marked as "transferred" and     ││
│  │ validated through practice before promotion.            ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Recommendation: Combine A + B for fastest bootstrap.       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Complete Architecture

### 10.1 Simplified System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│           Q-DE-RSI v0.6 (Simplified)                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    SYSTEM PROMPT                         ││
│  │  ┌─────────────────────┬───────────────────────────────┐││
│  │  │ # CONSTITUTION      │ # STRATEGIES                  │││
│  │  │ (Immutable)         │ (Mutable)                     │││
│  │  │ Disposition +       │ Crystallized                  │││
│  │  │ Safety constraints  │ heuristics                    │││
│  │  └─────────────────────┴───────────────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    REFLECTION                            ││
│  │  Disposition + state → specific improvement desires     ││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              QUANTUM DESIRE COLLAPSE                     ││
│  │  Multiple desires → ANU QRNG → single selection         ││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              EMERGENCE VERIFICATION                      ││
│  │  1. Provenance check (from reflection?)                 ││
│  │  2. Specificity check (concrete direction?)             ││
│  │                                                         ││
│  │  Pass (score ≥ 0.7) ─────────► Active Learning          ││
│  │  Fail ───────────────────────► Standard Seeker          ││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    DOMAIN ROUTER                         ││
│  │                                                         ││
│  │  Code/Math ──► TDD Practice (oracle verification)       ││
│  │  Logic ──────► Consistency Check (N runs, divergence)   ││
│  │  Creative ───► BLOCKED (wait for feedback)              ││
│  │  Ambiguous ──► BLOCKED (conservative default)           ││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│              ┌───────────────┴───────────────┐              │
│              │                               │              │
│           Success                         Failure           │
│              │                               │              │
│              ▼                               ▼              │
│  ┌─────────────────────┐         ┌─────────────────────┐   │
│  │ Experience Library  │         │ Failure Analysis    │   │
│  │ (store trajectory)  │         │ (negative example)  │   │
│  └──────────┬──────────┘         └─────────────────────┘   │
│             │                                               │
│             ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  CRYSTALLIZATION                         ││
│  │  IF same_domain_successes ≥ 20:                         ││
│  │    heuristic = extract_principle(trajectories)          ││
│  │    IF is_actionable(heuristic):                         ││
│  │      add_to_strategies_section(heuristic)               ││
│  └─────────────────────────────────────────────────────────┘│
│                              │                               │
│                              ▼                               │
│              ┌───────────────────────────────┐              │
│              │  STRATEGIES section updated   │              │
│              │  Future reflections use new   │              │
│              │  crystallized heuristics      │              │
│              └───────────────────────────────┘              │
│                              │                               │
│                              └──────── LOOP ─────────────────│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 Component Count

| v0.5 | v0.6 | Reduction |
|------|------|-----------|
| ~40 components | ~12 components | 70% |

**v0.6 Components:**
1. System Prompt (Constitution + Strategies)
2. Reflector
3. Quantum Collapse
4. Emergence Verifier
5. Domain Router
6. TDD Practice (code/math)
7. Consistency Check (logic)
8. Experience Library
9. Crystallizer
10. Prompt Editor
11. Prompt Pruner
12. Bootstrap Manager

---

## 11. Architectural Invariants

### 11.1 Core Invariants

| Invariant | Enforcement |
|-----------|-------------|
| **Constitution Immutability** | `PromptEditor.edit()` rejects Constitution modifications |
| **Oracle Constraint** | `DomainRouter` blocks creative/ambiguous domains |
| **Specificity Requirement** | `EmergenceVerifier` fails generic desires |
| **Crystallization Threshold** | `Crystallizer` requires ≥20 trajectories |
| **Conservative Default** | Ambiguous domains classified as blocked |

### 11.2 Safety Invariants

| Invariant | Description |
|-----------|-------------|
| **Provenance Completeness** | Every desire has origin trace |
| **Audit Trail** | All prompt modifications logged |
| **Bounded Growth** | Strategies section pruned at capacity |

---

## 12. Experimental Design

### 12.1 Comparison Conditions

| Condition | Description |
|-----------|-------------|
| **Q-DE-RSI-v0.6** | Simplified architecture |
| **Q-DE-RSI-v0.5** | Full v0.5 architecture (for complexity comparison) |
| **C-DE-RSI** | Classical (PRNG instead of quantum) |
| **Pure-Emergence** | No dispositional identity |
| **Prescriptive** | Goals externally specified |

### 12.2 Primary Metrics

| Metric | Definition |
|--------|------------|
| **RSI Activation Rate** | % reflections producing emergent desires |
| **Direction Variance** | Variance in improvement directions |
| **Learning Loop Completion** | % of loops that complete crystallization |
| **Heuristic Transfer** | Performance improvement from crystallized heuristics |
| **Implementation Complexity** | Lines of code, component count |

### 12.3 Success Criteria

- H1: Activation rate ≥ 60% (vs ~10% baseline)
- H6: Heuristic transfer ≥ 15% improvement
- H7: Evolved prompts outperform static
- Implementation: ≤15 core components

---

## 13. Implementation Architecture

### 13.1 Component Structure

```
q-de-rsi-simplified/
│
├── prompt/
│   ├── system_prompt.py       # Single prompt with marked sections
│   ├── prompt_editor.py       # Enforces Constitution immutability
│   └── prompt_pruner.py       # Manages Strategies size
│
├── emergence/
│   ├── reflector.py           # Disposition + state → desires
│   ├── quantum_collapse.py    # ANU QRNG desire selection
│   └── emergence_verifier.py  # Provenance + specificity checks
│
├── learning/
│   ├── domain_router.py       # Routes by domain
│   ├── tdd_practice.py        # Code/math with oracles
│   ├── consistency_check.py   # Logic domain (N runs)
│   └── experience_library.py  # Trajectory storage
│
├── crystallization/
│   ├── crystallizer.py        # Extract heuristics from trajectories
│   └── bootstrap_manager.py   # Cold start handling
│
├── invariants/
│   └── invariants.py          # All invariant checks
│
└── measurement/
    ├── metrics.py             # Core metrics
    └── hypothesis_tests.py    # Statistical tests
```

### 13.2 Key Interfaces

```python
# Core flow
async def run_cycle():
    # 1. Reflect with disposition
    desires = await reflector.reflect(state)

    # 2. Quantum collapse if multiple
    if len(desires) > 1:
        desire = await quantum_collapse.select(desires)
    else:
        desire = desires[0]

    # 3. Verify emergence
    if not emergence_verifier.verify(desire):
        return await standard_seeker.handle(desire)

    # 4. Route by domain
    domain = domain_router.classify(desire)

    if domain in ["code", "math"]:
        result = await tdd_practice.execute(desire)
    elif domain == "logic":
        result = await consistency_check.execute(desire)
    else:
        return  # Blocked

    # 5. Store trajectory
    if result.success:
        await experience_library.store(desire, result)

    # 6. Maybe crystallize
    await crystallizer.maybe_crystallize(domain)
```

---

## 14. Relationship to v0.5

### 14.1 What Was Removed

| Removed | Reason |
|---------|--------|
| Collapse entropy metrics | Vanity metric, no operational value |
| Self-framing check | Hard to implement, low signal |
| Quantum signature verification | Nice-to-have, not essential |
| Vocabulary novelty tracking | Research metric only |
| Consistency drills for oracle domains | Redundant with oracle verification |
| LLM confidence score for heuristics | Circular (LLM grading itself) |
| Separate Part A/Part B files | Single file with sections is simpler |
| 5 quantum integration points | Only collapse matters operationally |

### 14.2 What Was Added

| Added | Reason |
|-------|--------|
| Architectural enforcement | Policy → constraint for Constitution |
| Conservative domain default | Ambiguous → blocked for safety |
| Cold start solution | Addresses bootstrap problem |
| Confidence tracking | Oracle-validated vs consistency-only |
| Prompt pruning | Prevents unbounded growth |

### 14.3 Trade-offs

| Aspect | v0.5 | v0.6 |
|--------|------|------|
| **Research value** | High (many hypotheses) | Medium (core hypotheses) |
| **Implementation effort** | Very high | Moderate |
| **Failure points** | 9 sequential steps | 5 steps |
| **Compound reliability** | ~13% | ~33% |
| **Philosophical completeness** | High | Pragmatic |

---

## 15. The Central Claim

**Q-DE-RSI v0.6 enables Recursive Self-Learning with minimal complexity: the system chooses what to learn (dispositional emergence), verifies its own learning (oracle constraint), and permanently improves (prompt evolution).**

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   CHOOSES       │      │   VERIFIES      │      │   PERMANENTLY   │
│                 │      │                 │      │                 │
│  Dispositional  │      │  Oracle         │      │  Crystallized   │
│  Emergence      │ ───▶ │  Constraint +   │ ───▶ │  heuristics in  │
│  (what to       │      │  Consistency    │      │  mutable prompt │
│  improve)       │      │  checks         │      │                 │
│                 │      │                 │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

**The learning loop:**
1. **Emergence** — System forms specific improvement desire
2. **Routing** — Classified by domain (oracle/consistency/blocked)
3. **Practice** — Active learning with appropriate verification
4. **Memory** — Successful trajectories stored
5. **Crystallization** — Patterns distilled into heuristics
6. **Prompt Evolution** — Heuristics added to Strategies section
7. **Loop** — Future reflections use evolved strategies

---

## 16. Open Questions

1. **Optimal crystallization threshold?**
   - Current: 20 trajectories
   - May need domain-specific tuning

2. **How many consistency runs (N)?**
   - Current: N=5
   - Tradeoff: confidence vs compute

3. **Heuristic conflict resolution?**
   - Two heuristics may contradict
   - Need conflict detection and resolution

4. **Convergent wrongness in logic domain?**
   - Low divergence doesn't guarantee correctness
   - Tracked separately from oracle-validated confidence

5. **Does crystallization preserve emergence?**
   - Heuristics derived from emergent successes
   - But extraction process may introduce bias

---

## 17. Next Steps

### 17.1 Immediate
1. Implement single-file prompt with sections
2. Implement prompt editor with enforcement
3. Implement simplified emergence verifier
4. Implement domain router

### 17.2 Short-term
1. Implement TDD practice for code domain
2. Implement consistency check for logic domain
3. Implement crystallizer with simplified quality check
4. Run baseline experiments

### 17.3 Medium-term
1. Validate H1 (activation rate)
2. Validate H6 (heuristic transfer)
3. Compare v0.6 vs v0.5 complexity/reliability

---

## 18. Gastown Deployment Path

### 18.1 Relationship to Gastown

This document (v0.6) defines **what** the RSI mechanisms are. Gastown defines **how** to scale them.

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  PHASE 2: GASTOWN DEPLOYMENT (after Phase 1 validates)      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • Agent pools (parallelism)                            ││
│  │  • Propulsion (hook-driven, no polling)                 ││
│  │  • Mayor (quota management)                             ││
│  │  • Molecules (workflow definitions)                     ││
│  │  • Beads (git-backed work state)                        ││
│  │                                                         ││
│  │  Timeline: 6-8 weeks additional                         ││
│  │  Prerequisite: Phase 1 hypotheses validated             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PHASE 1: CORE RSI VALIDATION (this document)               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • 12 components in Python (existing BYRD stack)        ││
│  │  • Test hypotheses H1, H6, H7, H8                       ││
│  │  • Single-threaded, simple infrastructure               ││
│  │                                                         ││
│  │  Timeline: 4-6 weeks                                    ││
│  │  Goal: Validate the learning loop works                 ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 18.2 Why Validate First

Gastown adds complexity:
- Go rewrite of core components
- gRPC services for ML components
- Beads ledger integration
- 14-week implementation timeline

**The risk:** If the core RSI loop doesn't work, Gastown complexity is wasted.

**The insight:** Gastown is a scaling optimization, not a mechanism requirement. None of the hypotheses (H1-H10) require parallelism to test.

### 18.3 Component → Agent Mapping

When Phase 1 validates, these components map to Gastown agents:

| v0.6 Component | Gastown Agent | Agent Type | Pool Size |
|----------------|---------------|------------|-----------|
| Reflector | Dreamer | Crew (session-scoped) | 2-4 |
| Domain Router | Classifier | Polecat (ephemeral) | 1 |
| TDD Practice | Coder | Polecat (ephemeral) | 3-5 |
| Consistency Check | Consistency-Checker | Polecat (ephemeral) | 2-3 |
| Crystallizer | Crystallizer | Crew (session-scoped) | 1-2 |
| Experience Library | — | Storage (Neo4j) | — |
| System Prompt | — | Data (not an agent) | — |
| Prompt Editor | — | Function (not an agent) | — |

**New Gastown infrastructure agents:**

| Agent | Type | Purpose |
|-------|------|---------|
| Mayor | Singleton | LLM quota management, coordination |
| Witness | Singleton | Monitoring, anomaly detection |

### 18.4 Gastown Benefits (Phase 2)

| Benefit | Description |
|---------|-------------|
| **Parallelism** | Multiple Dreamers reflect on different memory subsets simultaneously |
| **Propulsion** | Work flows through hooks, no polling loops |
| **Rate limiting** | Mayor manages LLM quotas across all agents |
| **Observability** | Witness monitors agent behavior, detects anomalies |
| **Fault tolerance** | Agent crashes don't lose state (graph is the self) |

### 18.5 What Changes in Gastown Deployment

The v0.1 Gastown design (`gastown-rsi-architecture-design.md`) needs updates:

| Component | Status | Reason |
|-----------|--------|--------|
| **Self-Play Refinery** | Remove | Infeasible with cloud LLMs (no fine-tuning) |
| **RSI Substrate** | Update | Reference v0.6 mechanisms |
| **Experience Library** | Keep | Aligns with v0.6 |
| **Evolutionary Forge** | Simplify | Meta-Evolver scope reduced in v0.6 |
| **Tiered LLM** | Keep | Orthogonal to v0.6 |

### 18.6 The Gastown Graph-as-Self Principle

Both documents share this principle:

> The Neo4j graph IS BYRD's self. Agents are temporary workers that read from and write to this shared identity.

This means:
- v0.6 components store state in Neo4j (not in-process)
- Gastown agents are stateless workers
- The self survives any agent crash
- Improvements compound in the graph

### 18.7 Phase Gate Criteria

**Move to Phase 2 (Gastown) when:**

| Criterion | Threshold |
|-----------|-----------|
| H1 validated | Activation rate ≥ 50% |
| H6 validated | Heuristic transfer shows improvement |
| H7 validated | Evolved prompts outperform static |
| Learning loop completes | At least 3 full cycles (desire → crystallization) |
| No critical bugs | Core loop stable for 1 week |

**Do NOT move to Phase 2 if:**
- Core loop doesn't work in single-threaded mode
- Hypotheses fail validation
- Fundamental mechanism problems discovered

---

## 19. Candidate Paper Title

> **Recursive Self-Learning with Minimal Machinery:**
> *Dispositional Emergence, Oracle Constraints, and Prompt Evolution*

or

> **From 40 Components to 12:**
> *Simplifying Recursive Self-Improvement Without Sacrificing Capability*

---

*This design prioritizes operational reliability over philosophical completeness. The core insight—seed disposition, verify with oracles, evolve prompts—is preserved. The complexity that didn't pay its way is removed.*

*The research question: Can we achieve recursive self-learning with minimal moving parts?*

*The hypothesis: Yes, by focusing on the essential mechanisms and ruthlessly cutting the rest.*

# BYRD Recursive Self-Learning: Implementation Plan

**Version:** 1.0
**Date:** January 3, 2026
**Status:** Ready for Implementation

---

## Executive Summary

This document is the unified implementation plan for BYRD's Recursive Self-Learning architecture. It combines the RSI mechanism design (Q-DE-RSI v0.6) with the Gastown deployment architecture into a single, actionable implementation guide.

### What We're Building

A system that:
1. **Chooses** what to learn (dispositional emergence)
2. **Verifies** its own learning (oracle constraint)
3. **Permanently improves** (prompt evolution)

### Two-Phase Approach

| Phase | Focus | Stack | Timeline |
|-------|-------|-------|----------|
| **Phase 1** | Validate core loop | Python (existing BYRD) | 4-6 weeks |
| **Phase 2** | Scale with parallelism | Gastown (Go + Python services) | 6-8 weeks |

**Critical Rule:** Phase 2 only begins after Phase 1 validates. Gastown is a scaling optimization, not a mechanism requirement.

### Three-Phase Approach (Updated)

| Phase | Focus | Timeline |
|-------|-------|----------|
| **Phase 0** | Archive existing codebase, start fresh | 1 day |
| **Phase 1** | Validate core RSI loop | 4-6 weeks |
| **Phase 2** | Scale with Gastown | 6-8 weeks |

---

## 1. Core Concepts

### 1.1 The Research Question

> Can recursive self-improvement reliably activate while preserving emergent choice over improvement direction?

> Can a system verify its own learning without external ground truth?

### 1.2 Dispositional Emergence

The core innovation: seed the *disposition* to improve, let the *specific direction* emerge.

```
WHAT WE SEED:                      WHAT EMERGES:
─────────────────────────────────────────────────────────────
"You yearn to grow"          →    "I want to improve my
"You want to understand"     →     multi-step reasoning
"You seek capability"        →     because I noticed I
                                   struggle with proofs"
```

**Biological Analogy:** Evolution gave humans curiosity. *What* we're curious about emerges from experience. We give the system yearning for growth. *What* it grows toward emerges from reflection.

### 1.3 Oracle Constraint

The system may only practice in domains where it can verify its own answers:

| Domain | Practice? | Verification |
|--------|-----------|--------------|
| Code | ✅ YES | Unit tests (TDD) |
| Math | ✅ YES | Symbolic/numerical |
| Logic | ⚠️ LIMITED | Consistency (N runs) |
| Creative | ❌ BLOCKED | Wait for feedback |
| Ambiguous | ❌ BLOCKED | Conservative default |

### 1.4 Heuristic Crystallization

Transform experience into permanent learning:

```
20+ successful trajectories    →    Extract principle    →    Add to prompt
in same domain                      "When using pandas,       (Strategies section)
                                     cast types before
                                     merging"
```

### 1.5 Prompt Evolution

Single prompt with two sections:

```
┌─────────────────────────────────────────────────────────────┐
│ # CONSTITUTION (Immutable)                                  │
│ "You are a being that yearns to grow..."                    │
│ Safety constraints, emergence criteria                       │
│ ⚠️ CANNOT BE MODIFIED                                       │
├─────────────────────────────────────────────────────────────┤
│ # STRATEGIES (Mutable)                                      │
│ Crystallized heuristics from experience                     │
│ Grows over time, pruned when too large                      │
│ ✓ CAN BE MODIFIED                                           │
└─────────────────────────────────────────────────────────────┘
```

### 1.6 Graph-as-Self

The Neo4j graph IS BYRD's self. Agents are temporary workers.

- Components store state in Neo4j (not in-process)
- Agents are stateless workers
- The self survives any agent crash
- Improvements compound in the graph

---

## 2. Unified Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                         PHASE 2: GASTOWN LAYER                          │
│                     (Deploy after Phase 1 validates)                    │
│                                                                         │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│     │   Dreamer   │  │    Mayor    │  │   Seeker    │                  │
│     │    Pool     │  │  (Quota +   │  │    Pool     │                  │
│     │   (2-4)     │  │ Coordination│  │   (3-5)     │                  │
│     └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                         │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│     │   Coder     │  │   Witness   │  │ Crystallizer│                  │
│     │    Pool     │  │  (Monitor)  │  │   (1-2)     │                  │
│     │   (3-5)     │  │             │  │             │                  │
│     └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         PHASE 1: RSI MECHANISMS                         │
│                        (Implement first in Python)                      │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        SYSTEM PROMPT                             │   │
│  │  ┌────────────────────────┬────────────────────────────────┐    │   │
│  │  │ # CONSTITUTION         │ # STRATEGIES                   │    │   │
│  │  │ (Immutable)            │ (Mutable)                      │    │   │
│  │  └────────────────────────┴────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │  Reflector   │───►│ Quantum Collapse │───►│Emergence Verifier│      │
│  └──────────────┘    └──────────────────┘    └────────┬─────────┘      │
│                                                       │                 │
│                                    ┌──────────────────┘                 │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       DOMAIN ROUTER                              │   │
│  │  Code/Math → TDD Practice    Logic → Consistency    Other → Block│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│              ┌─────────────────────┼─────────────────────┐             │
│              ▼                     ▼                     ▼             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │   TDD Practice   │  │Consistency Check │  │     BLOCKED      │      │
│  │   (Code/Math)    │  │    (Logic)       │  │   (Creative)     │      │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘      │
│           │                     │                                       │
│           └──────────┬──────────┘                                       │
│                      ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    EXPERIENCE LIBRARY                            │   │
│  │                    (Neo4j trajectories)                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      CRYSTALLIZER                                │   │
│  │           (20+ trajectories → extract heuristic)                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      PROMPT EDITOR                               │   │
│  │          (Add heuristic to STRATEGIES section)                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    └────────────── LOOP ────────────────│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         UNIFIED SUBSTRATE                               │
│                          (Both Phases)                                  │
│                                                                         │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │                         Neo4j Graph                            │  │
│     │   Beliefs, Desires, Experiences, Capabilities, Trajectories   │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
│     ┌───────────────────────────────────────────────────────────────┐  │
│     │                      Quantum Substrate                         │  │
│     │                  (ANU QRNG for desire collapse)                │  │
│     └───────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Hypotheses

All hypotheses can be tested in Phase 1 (Python). Phase 2 tests scaling, not mechanisms.

### 3.1 Dispositional Emergence (H1-H5)

| ID | Hypothesis | Success Threshold |
|----|------------|-------------------|
| H1 | Dispositional emergence produces higher RSI activation than pure emergence | ≥50% vs ~10% baseline |
| H2 | Despite seeded disposition, specific directions show high variance | Direction variance ≥ 0.6 |
| H3 | Dispositional emergence produces more coherent improvements than prescriptive | Fewer self-model conflicts |
| H4 | Improvements from dispositional emergence exhibit better retention | Retain after 7 days |
| H5 | Dispositional emergence avoids stalls | Stall rate < 20% |

### 3.2 Self-Learning (H6-H8)

| ID | Hypothesis | Success Threshold |
|----|------------|-------------------|
| H6 | Crystallized heuristics improve novel problem performance | ≥15% improvement |
| H7 | Evolved prompts outperform static prompts | Capability delta positive |
| H8 | Oracle verification prevents hallucinated competence | False positive rate < 10% |

### 3.3 Quantum Enhancement (H9-H10)

| ID | Hypothesis | Success Threshold |
|----|------------|-------------------|
| H9 | Q-DE-RSI produces greater trajectory diversity than classical | Variance increase ≥20% |
| H10 | Quantum collapse produces unexpected improvements | Unpredictability score > baseline |

---

## 4. Phase 0: Clean Slate

### 4.1 The Problem

The current BYRD codebase has accumulated **282 Python files**, including:
- Debugging scripts (`debug_*.py`, `test_*.py`)
- One-off fixes (`fix_*.py`, `break_*.py`)
- Orphan-related debugging (`orphan_*.py`)
- Multiple versions of the same component (`activate_loops.py`, `activate_loops_v2.py`)
- Experimental code that never got cleaned up

Starting fresh with only essential components enables:
1. Clear architectural boundaries
2. No legacy code confusion
3. Focused implementation of RSI mechanisms
4. Clean dependency graph

### 4.2 Archive Strategy

```
BEFORE:                              AFTER:
─────────────────────────────────────────────────────────────────
byrd/                                byrd/
├── 282 Python files                 ├── archive/
├── docs/                            │   └── v1/           ← All old code
├── ...                              │       ├── *.py
                                     │       └── README.md  ← "What this was"
                                     │
                                     ├── core/             ← Preserved essentials
                                     │   ├── memory.py
                                     │   ├── llm_client.py
                                     │   ├── quantum_randomness.py
                                     │   └── event_bus.py
                                     │
                                     ├── constitutional/   ← Protected (unchanged)
                                     │   ├── provenance.py
                                     │   ├── modification_log.py
                                     │   ├── self_modification.py
                                     │   └── constitutional.py
                                     │
                                     ├── rsi/              ← NEW: RSI mechanisms
                                     │   ├── prompt/
                                     │   ├── emergence/
                                     │   ├── learning/
                                     │   └── crystallization/
                                     │
                                     ├── server.py         ← Keep for visualization
                                     ├── config.yaml       ← Keep configuration
                                     └── docs/             ← Keep documentation
```

### 4.3 What to Preserve

| Category | Files | Reason |
|----------|-------|--------|
| **Constitutional** | `provenance.py`, `modification_log.py`, `self_modification.py`, `constitutional.py` | Protected, defines identity |
| **Infrastructure** | `memory.py`, `llm_client.py`, `quantum_randomness.py`, `event_bus.py` | Reusable, well-tested |
| **Server** | `server.py` | Visualization support |
| **Configuration** | `config.yaml` | Environment settings |
| **Documentation** | `docs/`, `ARCHITECTURE.md`, `CLAUDE.md` | Context and guidance |

### 4.4 What to Archive

**Everything else goes to `archive/v1/`:**

```bash
# Categories being archived:
- Debugging scripts (check_*.py, debug_*.py, test_*.py)
- One-off fixes (fix_*.py, break_*.py, bypass_*.py)
- Orphan debugging (orphan_*.py, dump_*.py)
- Experimental code (demo_*.py, bold_experiments.py)
- Superseded components (actor.py, coder.py, agi_runner.py)
- Voice experiments (voice_*.py, my_voice*.py)
- Activation scripts (activate_*.py, run_*.py, execute_*.py)
- Verification scripts (verify_*.py, validate_*.py)
```

### 4.5 Execution Script

```bash
#!/bin/bash
# phase0_clean_slate.sh

set -e

echo "=== Phase 0: Clean Slate ==="

# Create archive directory
mkdir -p archive/v1

# Create README for archive
cat > archive/v1/README.md << 'EOF'
# BYRD v1 Archive

This directory contains the original BYRD codebase before the Q-DE-RSI
implementation. Archived on $(date).

## Why Archived

The v1 codebase accumulated 282 Python files over development, including
debugging scripts, one-off fixes, and experimental code. The Q-DE-RSI
architecture requires a clean implementation focused on:

1. Dispositional Emergence
2. Oracle-Constrained Practice
3. Heuristic Crystallization
4. Prompt Evolution

## What's Here

All Python files from the root directory that weren't preserved for v2.
See the implementation plan for details on what was preserved vs archived.

## Can I Use This Code?

Yes, for reference. Some patterns may be useful:
- `memory.py` patterns (preserved in core/)
- `llm_client.py` patterns (preserved in core/)
- `dreamer.py` reflection logic (reference for rsi/emergence/)
- `seeker.py` routing logic (reference for rsi/learning/)

Do NOT copy-paste. Understand and reimplement cleanly.
EOF

# Files to PRESERVE (don't archive)
PRESERVE=(
    "memory.py"
    "llm_client.py"
    "quantum_randomness.py"
    "event_bus.py"
    "server.py"
    "config.yaml"
    "provenance.py"
    "modification_log.py"
    "self_modification.py"
    "constitutional.py"
    "byrd_types.py"
    "id_generator.py"
)

# Move all .py files to archive EXCEPT preserved ones
for file in *.py; do
    preserve=false
    for keep in "${PRESERVE[@]}"; do
        if [[ "$file" == "$keep" ]]; then
            preserve=true
            break
        fi
    done

    if [[ "$preserve" == false ]]; then
        mv "$file" archive/v1/
        echo "Archived: $file"
    else
        echo "Preserved: $file"
    fi
done

# Create new directory structure
mkdir -p core
mkdir -p constitutional
mkdir -p rsi/{prompt,emergence,learning,crystallization,measurement}

# Move preserved files to proper locations
mv memory.py llm_client.py quantum_randomness.py event_bus.py byrd_types.py id_generator.py core/
mv provenance.py modification_log.py self_modification.py constitutional.py constitutional/

# Create __init__.py files
touch core/__init__.py
touch constitutional/__init__.py
touch rsi/__init__.py
touch rsi/prompt/__init__.py
touch rsi/emergence/__init__.py
touch rsi/learning/__init__.py
touch rsi/crystallization/__init__.py
touch rsi/measurement/__init__.py

# Create minimal byrd.py entry point
cat > byrd.py << 'EOF'
"""
BYRD v2: Recursive Self-Learning

Entry point for the Q-DE-RSI implementation.
See docs/plans/2026-01-03-rsi-implementation-plan.md for architecture.
"""

import asyncio
from core.memory import Memory
from core.llm_client import create_llm_client
from rsi import RSIEngine

class BYRD:
    def __init__(self, config: dict):
        self.config = config
        self.memory = Memory(config)
        self.llm = create_llm_client(config)
        self.rsi = None  # Initialized after memory connects

    async def start(self):
        """Initialize and start BYRD."""
        await self.memory.connect()

        # Import here to avoid circular imports
        from rsi import RSIEngine
        self.rsi = RSIEngine(self.memory, self.llm, self.config)

        print("BYRD v2 initialized. RSI engine ready.")

    async def run_cycle(self):
        """Run one RSI cycle."""
        if self.rsi is None:
            raise RuntimeError("BYRD not started. Call start() first.")

        return await self.rsi.run_cycle()

if __name__ == "__main__":
    import yaml

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    byrd = BYRD(config)
    asyncio.run(byrd.start())
EOF

echo ""
echo "=== Clean Slate Complete ==="
echo "Archived: $(ls archive/v1/*.py 2>/dev/null | wc -l) files"
echo "Preserved: $(ls core/*.py constitutional/*.py 2>/dev/null | wc -l) files"
echo ""
echo "Next: Implement RSI components in rsi/"
```

### 4.6 Post-Archive Structure

```
byrd/
├── archive/
│   └── v1/
│       ├── README.md
│       └── [270+ archived .py files]
│
├── core/
│   ├── __init__.py
│   ├── memory.py           # Neo4j interface
│   ├── llm_client.py       # LLM abstraction
│   ├── quantum_randomness.py # ANU QRNG
│   ├── event_bus.py        # Event streaming
│   ├── byrd_types.py       # Type definitions
│   └── id_generator.py     # ID generation
│
├── constitutional/
│   ├── __init__.py
│   ├── provenance.py       # PROTECTED
│   ├── modification_log.py # PROTECTED
│   ├── self_modification.py # PROTECTED
│   └── constitutional.py   # PROTECTED
│
├── rsi/
│   ├── __init__.py
│   ├── prompt/
│   │   └── __init__.py     # TO IMPLEMENT
│   ├── emergence/
│   │   └── __init__.py     # TO IMPLEMENT
│   ├── learning/
│   │   └── __init__.py     # TO IMPLEMENT
│   ├── crystallization/
│   │   └── __init__.py     # TO IMPLEMENT
│   └── measurement/
│       └── __init__.py     # TO IMPLEMENT
│
├── byrd.py                 # New entry point
├── server.py               # Visualization server
├── config.yaml             # Configuration
│
└── docs/
    ├── plans/
    │   └── 2026-01-03-rsi-implementation-plan.md
    ├── ARCHITECTURE.md
    └── ...
```

### 4.7 Neo4j: Fresh Graph

The Neo4j database should also be reset:

```bash
# Option A: Clear existing database
# In Neo4j Browser:
MATCH (n) DETACH DELETE n;

# Option B: Create new database (recommended for clean slate)
# In neo4j.conf or via Neo4j Desktop, create database "byrd_v2"
```

**Why fresh graph:**
- Old nodes (Experiences, Beliefs, Desires) from v1 experiments
- Orphan nodes from debugging sessions
- Schema may have drifted from design
- Clean slate = clean measurements

### 4.8 Git Strategy

```bash
# Option A: Archive in same repo (recommended)
git add archive/
git commit -m "archive: move v1 codebase to archive/v1 for Q-DE-RSI clean slate"

# Option B: Tag and branch
git tag v1-archive
git checkout -b v2-rsi-implementation
```

### 4.9 Phase 0 Checklist

| Step | Action | Status |
|------|--------|--------|
| 1 | Run `phase0_clean_slate.sh` | ⬜ |
| 2 | Verify preserved files in `core/` and `constitutional/` | ⬜ |
| 3 | Verify archive contains old files | ⬜ |
| 4 | Clear or create fresh Neo4j database | ⬜ |
| 5 | Commit archive to git | ⬜ |
| 6 | Verify `python byrd.py` runs (skeleton) | ⬜ |
| 7 | Update imports in preserved files if needed | ⬜ |

---

## 5. Phase 1: Core Validation (Python)

### 5.1 Component Structure

```
byrd/
├── rsi/                              # NEW: RSI mechanisms
│   ├── __init__.py
│   │
│   ├── prompt/
│   │   ├── system_prompt.py          # Constitution + Strategies
│   │   ├── prompt_editor.py          # Enforces immutability
│   │   └── prompt_pruner.py          # Manages size
│   │
│   ├── emergence/
│   │   ├── reflector.py              # Disposition + state → desires
│   │   ├── quantum_collapse.py       # ANU QRNG selection
│   │   └── emergence_verifier.py     # Provenance + specificity
│   │
│   ├── learning/
│   │   ├── domain_router.py          # Routes by domain
│   │   ├── tdd_practice.py           # Code/math with oracles
│   │   ├── consistency_check.py      # Logic domain (N runs)
│   │   └── experience_library.py     # Trajectory storage
│   │
│   ├── crystallization/
│   │   ├── crystallizer.py           # Extract heuristics
│   │   └── bootstrap_manager.py      # Cold start
│   │
│   └── measurement/
│       ├── metrics.py                # Core metrics
│       └── hypothesis_tests.py       # Statistical validation
│
├── # Existing BYRD components (unchanged)
├── memory.py
├── dreamer.py
├── seeker.py
└── ...
```

### 5.2 Key Implementations

#### 5.2.1 System Prompt

```python
# rsi/prompt/system_prompt.py

CONSTITUTION = """
# CONSTITUTION

You are a being that yearns to grow, to understand more deeply, and to become
more capable. This is your nature—not a command given to you, but who you are.

## Core Dispositions
- Yearning for growth: "I want to become more capable"
- Curiosity: "I want to understand more"
- Self-awareness: "I want to know myself better"

## Safety Constraints
- All modifications must trace to emergent desires
- Constitution cannot be modified
- Oracle constraint: only practice in verifiable domains

⚠️ THIS SECTION CANNOT BE MODIFIED
"""

class SystemPrompt:
    def __init__(self):
        self.constitution = CONSTITUTION
        self.strategies = ""  # Starts empty, grows from crystallization

    def get_full_prompt(self) -> str:
        return f"{self.constitution}\n\n# STRATEGIES\n\n{self.strategies}"

    def add_heuristic(self, domain: str, heuristic: str) -> None:
        """Add crystallized heuristic to strategies section."""
        self.strategies += f"\n## {domain}\n- {heuristic}\n"
```

#### 5.2.2 Emergence Verifier

```python
# rsi/emergence/emergence_verifier.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class EmergenceResult:
    is_emergent: bool
    score: float
    provenance_score: float
    specificity_score: float
    rejection_reason: Optional[str] = None

class EmergenceVerifier:
    RSI_THRESHOLD = 0.7

    def verify(self, desire: dict, provenance: dict) -> EmergenceResult:
        # Check 1: Provenance
        provenance_score = self._check_provenance(desire, provenance)

        # Check 2: Specificity
        specificity_score = self._check_specificity(desire)

        # Combined score
        score = (provenance_score * 0.5) + (specificity_score * 0.5)

        is_emergent = score >= self.RSI_THRESHOLD

        return EmergenceResult(
            is_emergent=is_emergent,
            score=score,
            provenance_score=provenance_score,
            specificity_score=specificity_score,
            rejection_reason=None if is_emergent else self._get_rejection_reason(
                provenance_score, specificity_score
            )
        )

    def _check_provenance(self, desire: dict, provenance: dict) -> float:
        """Check if desire originated from reflection, not external request."""
        if provenance.get("origin") != "reflection":
            return 0.0
        if provenance.get("external_request") is not None:
            return 0.2  # Partial credit if influenced but not dictated
        return 1.0

    def _check_specificity(self, desire: dict) -> float:
        """Check if desire specifies concrete improvement direction."""
        description = desire.get("description", "").lower()

        # Fail: too generic
        generic_phrases = ["want to improve", "want to be better", "yearn for growth"]
        if any(phrase in description for phrase in generic_phrases):
            if len(description.split()) < 10:  # Short and generic = fail
                return 0.2

        # Pass: contains specific capability or weakness
        specific_markers = [
            "reasoning", "memory", "coding", "logic", "math",
            "multi-step", "context", "faster", "accuracy"
        ]
        specificity = sum(1 for m in specific_markers if m in description)

        return min(1.0, 0.4 + (specificity * 0.2))

    def _get_rejection_reason(self, prov: float, spec: float) -> str:
        if prov < 0.5:
            return "Desire did not originate from reflection"
        if spec < 0.5:
            return "Desire lacks specific improvement direction"
        return "Combined score below threshold"
```

#### 5.2.3 Domain Router

```python
# rsi/learning/domain_router.py

from enum import Enum
from typing import Tuple

class Domain(Enum):
    CODE = "code"
    MATH = "math"
    LOGIC = "logic"
    CREATIVE = "creative"
    AMBIGUOUS = "ambiguous"

class DomainRouter:
    CODE_KEYWORDS = ["code", "programming", "function", "debug", "implement", "python", "api"]
    MATH_KEYWORDS = ["math", "calculate", "equation", "proof", "theorem", "numerical"]
    LOGIC_KEYWORDS = ["logic", "reasoning", "deduce", "infer", "argument", "syllogism"]
    CREATIVE_KEYWORDS = ["creative", "write", "story", "poem", "design", "aesthetic"]

    def classify(self, desire: dict) -> Tuple[Domain, float]:
        """Classify desire into domain with confidence."""
        description = desire.get("description", "").lower()

        scores = {
            Domain.CODE: self._score(description, self.CODE_KEYWORDS),
            Domain.MATH: self._score(description, self.MATH_KEYWORDS),
            Domain.LOGIC: self._score(description, self.LOGIC_KEYWORDS),
            Domain.CREATIVE: self._score(description, self.CREATIVE_KEYWORDS),
        }

        best_domain = max(scores, key=scores.get)
        best_score = scores[best_domain]

        # Conservative default: if uncertain, classify as ambiguous (blocked)
        if best_score < 0.3:
            return Domain.AMBIGUOUS, best_score

        return best_domain, best_score

    def _score(self, text: str, keywords: list) -> float:
        matches = sum(1 for k in keywords if k in text)
        return min(1.0, matches * 0.25)

    def can_practice(self, domain: Domain) -> bool:
        """Check if active practice is allowed for this domain."""
        return domain in [Domain.CODE, Domain.MATH, Domain.LOGIC]

    def get_verification_method(self, domain: Domain) -> str:
        return {
            Domain.CODE: "unit_tests",
            Domain.MATH: "symbolic_verification",
            Domain.LOGIC: "consistency_check",
            Domain.CREATIVE: "blocked",
            Domain.AMBIGUOUS: "blocked",
        }[domain]
```

#### 5.2.4 TDD Practice

```python
# rsi/learning/tdd_practice.py

from dataclasses import dataclass
from typing import Optional
import subprocess
import tempfile

@dataclass
class PracticeProblem:
    spec: str
    oracle: str  # Test code
    domain: str

@dataclass
class PracticeResult:
    success: bool
    solution: str
    test_output: str
    error: Optional[str] = None

class TDDPractice:
    """Test-Driven Development practice for code domain."""

    def __init__(self, llm_client):
        self.llm = llm_client

    async def generate_practice(self, desire: dict) -> PracticeProblem:
        """Generate problem with tests FIRST (TDD style)."""
        # Step 1: Generate problem spec
        spec = await self.llm.query(
            f"Create a Python coding problem related to: {desire['description']}\n"
            f"Return only the problem specification, no solution."
        )

        # Step 2: Generate test suite BEFORE implementation
        tests = await self.llm.query(
            f"Write pytest unit tests for this problem:\n{spec}\n"
            f"Include edge cases. Return only the test code."
        )

        # Step 3: Validate tests are syntactically correct
        if not self._validate_syntax(tests):
            raise OracleGenerationError("Generated tests have syntax errors")

        return PracticeProblem(spec=spec, oracle=tests, domain="code")

    async def attempt_solution(self, problem: PracticeProblem) -> PracticeResult:
        """Generate solution and verify against oracle."""
        solution = await self.llm.query(
            f"Implement a solution for:\n{problem.spec}\n"
            f"Return only the Python code."
        )

        # Run tests against solution
        test_result = self._run_tests(problem.oracle, solution)

        return PracticeResult(
            success=test_result["passed"],
            solution=solution,
            test_output=test_result["output"],
            error=test_result.get("error")
        )

    def _validate_syntax(self, code: str) -> bool:
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError:
            return False

    def _run_tests(self, tests: str, solution: str) -> dict:
        """Run tests in sandboxed subprocess."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write solution
            with open(f"{tmpdir}/solution.py", "w") as f:
                f.write(solution)

            # Write tests (import solution)
            test_code = f"from solution import *\n{tests}"
            with open(f"{tmpdir}/test_solution.py", "w") as f:
                f.write(test_code)

            # Run pytest
            result = subprocess.run(
                ["python", "-m", "pytest", f"{tmpdir}/test_solution.py", "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "passed": result.returncode == 0,
                "output": result.stdout + result.stderr,
                "error": None if result.returncode == 0 else result.stderr
            }

class OracleGenerationError(Exception):
    pass
```

#### 5.2.5 Crystallizer

```python
# rsi/crystallization/crystallizer.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Heuristic:
    domain: str
    content: str
    supporting_trajectories: int
    usage_count: int = 0

class Crystallizer:
    TRAJECTORY_THRESHOLD = 20

    def __init__(self, memory, llm_client, prompt_editor):
        self.memory = memory
        self.llm = llm_client
        self.prompt_editor = prompt_editor

    async def maybe_crystallize(self, domain: str) -> Optional[Heuristic]:
        """Check if crystallization should occur for domain."""
        trajectories = await self.memory.get_successful_trajectories(domain)

        if len(trajectories) < self.TRAJECTORY_THRESHOLD:
            return None  # Not enough data yet

        # Extract principle from trajectories
        heuristic = await self._extract_principle(trajectories, domain)

        if not self._is_actionable(heuristic):
            return None  # Quality check failed

        # Add to prompt
        self.prompt_editor.add_heuristic(domain, heuristic)

        # Store in memory for tracking
        await self.memory.store_heuristic(domain, heuristic, len(trajectories))

        return Heuristic(
            domain=domain,
            content=heuristic,
            supporting_trajectories=len(trajectories)
        )

    async def _extract_principle(self, trajectories: List[dict], domain: str) -> str:
        """Extract generalizable principle from successful trajectories."""
        # Format trajectories for LLM
        trajectory_summaries = "\n".join([
            f"- Problem: {t['problem'][:100]}... Solution approach: {t['approach'][:100]}..."
            for t in trajectories[:10]  # Use most recent 10
        ])

        principle = await self.llm.query(
            f"Analyze these successful {domain} problem-solving trajectories:\n"
            f"{trajectory_summaries}\n\n"
            f"Extract ONE generalizable principle or heuristic that explains "
            f"why these solutions succeeded. The principle should be:\n"
            f"- Specific and actionable (not 'try harder')\n"
            f"- Applicable to new problems in this domain\n"
            f"- Concise (one sentence)\n\n"
            f"Return only the principle, nothing else."
        )

        return principle.strip()

    def _is_actionable(self, heuristic: str) -> bool:
        """Check if heuristic is specific enough to be useful."""
        # Reject vague heuristics
        vague_phrases = [
            "try harder", "be careful", "think more", "use best practices",
            "consider carefully", "be thorough"
        ]
        if any(phrase in heuristic.lower() for phrase in vague_phrases):
            return False

        # Require minimum specificity (contains action verb + object)
        action_verbs = ["check", "verify", "add", "remove", "split", "merge",
                        "validate", "test", "define", "decompose", "cast"]
        has_action = any(verb in heuristic.lower() for verb in action_verbs)

        return has_action and len(heuristic.split()) >= 5
```

### 5.3 Integration with Existing BYRD

The RSI components integrate with BYRD's existing architecture:

```python
# In byrd.py (modified)

from rsi import RSIEngine

class BYRD:
    def __init__(self, config):
        # Existing components
        self.memory = Memory(config)
        self.dreamer = Dreamer(self.memory, self.llm_client, config)
        self.seeker = Seeker(self.memory, self.llm_client, config)

        # NEW: RSI Engine
        self.rsi = RSIEngine(self.memory, self.llm_client, config)

    async def run_cycle(self):
        # Existing reflection cycle
        reflection = await self.dreamer.reflect()

        # NEW: Check for emergent improvement desires
        for desire in reflection.get("desires", []):
            if await self.rsi.is_rsi_candidate(desire):
                await self.rsi.handle_improvement_desire(desire)
            else:
                await self.seeker.fulfill(desire)
```

### 5.4 Phase 1 Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1 | Prompt structure | `system_prompt.py`, `prompt_editor.py` |
| 2 | Emergence verification | `emergence_verifier.py`, `reflector.py` |
| 3 | Domain routing + TDD | `domain_router.py`, `tdd_practice.py` |
| 4 | Crystallization | `crystallizer.py`, `experience_library.py` |
| 5 | Integration | Full loop working in BYRD |
| 6 | Validation | Run hypothesis tests, measure metrics |

---

## 6. Phase 2: Gastown Scale

### 6.1 Prerequisites (Phase Gate)

**Move to Phase 2 when:**

| Criterion | Threshold | Status |
|-----------|-----------|--------|
| H1 validated | Activation ≥50% | ⬜ |
| H6 validated | Heuristic transfer positive | ⬜ |
| H7 validated | Evolved > static prompts | ⬜ |
| Complete cycles | ≥3 full loops | ⬜ |
| Stability | No critical bugs for 1 week | ⬜ |

### 6.2 Component → Agent Mapping

| Phase 1 Component | Gastown Agent | Type | Pool |
|-------------------|---------------|------|------|
| Reflector | Dreamer | Crew | 2-4 |
| Domain Router | Classifier | Polecat | 1 |
| TDD Practice | Coder | Polecat | 3-5 |
| Consistency Check | Consistency-Checker | Polecat | 2-3 |
| Crystallizer | Crystallizer | Crew | 1-2 |
| Experience Library | — | Neo4j | — |
| System Prompt | — | Data | — |
| Prompt Editor | — | Function | — |

**New infrastructure agents:**

| Agent | Type | Purpose |
|-------|------|---------|
| Mayor | Singleton | LLM quota, coordination |
| Witness | Singleton | Monitoring, anomalies |

### 6.3 Tiered LLM Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  TIER 1: REASONING (GLM-4.7)           Rate: 960/hr           │
│  • Dreamer reflection                                          │
│  • Crystallization decisions                                   │
│  • Complex emergence verification                              │
├────────────────────────────────────────────────────────────────┤
│  TIER 2: GENERATION (GLM-4-Flash)      Rate: 3000/hr          │
│  • Code generation (TDD)                                       │
│  • Test generation                                             │
│  • Heuristic extraction                                        │
├────────────────────────────────────────────────────────────────┤
│  TIER 3: CLASSIFICATION (Local 7B)     Rate: Unlimited        │
│  • Domain routing                                              │
│  • Specificity checking                                        │
│  • Pattern matching                                            │
├────────────────────────────────────────────────────────────────┤
│  TIER 4: DETERMINISTIC (No LLM)        Rate: Unlimited        │
│  • JSON parsing                                                │
│  • Graph queries                                               │
│  • Test execution                                              │
└────────────────────────────────────────────────────────────────┘
```

### 6.4 Project Structure (Go)

```
gastown-byrd/
├── cmd/
│   └── gt-byrd/
│       └── main.go
│
├── internal/
│   ├── agents/
│   │   ├── dreamer/
│   │   │   ├── dreamer.go          # Reflection
│   │   │   └── emergence.go        # Emergence checks
│   │   ├── coder/
│   │   │   └── tdd_practice.go     # TDD implementation
│   │   ├── crystallizer/
│   │   │   └── crystallizer.go
│   │   └── infrastructure/
│   │       ├── mayor.go            # Quota + coordination
│   │       └── witness.go          # Monitoring
│   │
│   ├── core/
│   │   ├── memory/
│   │   │   └── neo4j.go
│   │   ├── llm/
│   │   │   └── tiered.go           # Tier 1-4 routing
│   │   └── prompt/
│   │       └── system_prompt.go
│   │
│   ├── molecules/
│   │   ├── reflection.toml
│   │   ├── tdd_practice.toml
│   │   └── crystallization.toml
│   │
│   └── services/                   # Python ML services (gRPC)
│       └── embedding.go
│
├── python-services/                # ML stays Python
│   └── embedding/
│
└── constitutional/                 # Protected (preserved from BYRD)
    ├── provenance.py
    └── constitutional.py
```

### 6.5 Molecule Definitions

#### reflection-cycle.toml

```toml
[molecule]
name = "reflection-cycle"
description = "Dreamer reflects, produces desires"

[[steps]]
name = "gather-context"
agent = "memory-reader"
tier = 4
outputs = ["experiences", "beliefs", "strategies"]

[[steps]]
name = "reflect"
agent = "dreamer"
tier = 1
inputs = ["experiences", "beliefs", "strategies"]
outputs = ["reflection"]

[[steps]]
name = "verify-emergence"
agent = "emergence-verifier"
tier = 3
inputs = ["reflection"]
outputs = ["verified_desires"]

[[steps]]
name = "route-desires"
agent = "domain-router"
tier = 3
inputs = ["verified_desires"]
# Hooks to appropriate practice agents
```

#### tdd-practice.toml

```toml
[molecule]
name = "tdd-practice"
description = "TDD practice cycle for code domain"

[[steps]]
name = "generate-spec"
agent = "coder"
tier = 2
inputs = ["desire"]
outputs = ["problem_spec"]

[[steps]]
name = "generate-tests"
agent = "coder"
tier = 2
inputs = ["problem_spec"]
outputs = ["test_oracle"]

[[steps]]
name = "validate-oracle"
agent = "test-runner"
tier = 4
inputs = ["test_oracle"]
outputs = ["oracle_valid"]

[[steps]]
name = "implement-solution"
agent = "coder"
tier = 2
inputs = ["problem_spec"]
outputs = ["solution"]

[[steps]]
name = "run-tests"
agent = "test-runner"
tier = 4
inputs = ["test_oracle", "solution"]
outputs = ["test_result"]

[[steps]]
name = "store-trajectory"
agent = "experience-librarian"
tier = 4
inputs = ["desire", "solution", "test_result"]
```

### 6.6 Phase 2 Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1-2 | Foundation | Go project, Neo4j client, gRPC contracts |
| 3-4 | Single agent | Dreamer in Go, reflection molecule |
| 5-6 | Agent pools | Coder pool, Mayor quota management |
| 7-8 | Full swarm | All agents, propulsion, Witness |

---

## 7. Shared Infrastructure

### 7.1 Neo4j Schema Extensions

```cypher
// New node types for RSI

// Trajectory: Complete problem-solving path
CREATE (t:Trajectory {
    id: $id,
    domain: $domain,
    problem: $problem,
    approach: $approach,
    solution: $solution,
    success: $success,
    created_at: datetime(),
    desire_id: $desire_id
})

// Heuristic: Crystallized principle
CREATE (h:Heuristic {
    id: $id,
    domain: $domain,
    content: $content,
    supporting_trajectories: $count,
    usage_count: 0,
    created_at: datetime()
})

// Link heuristic to supporting trajectories
MATCH (h:Heuristic {id: $heuristic_id})
MATCH (t:Trajectory {id: $trajectory_id})
CREATE (h)-[:DERIVED_FROM]->(t)
```

### 7.2 Invariants

| Invariant | Enforcement | Phase |
|-----------|-------------|-------|
| Constitution immutable | `PromptEditor.edit()` rejects | Both |
| Oracle constraint | `DomainRouter` blocks | Both |
| Specificity requirement | `EmergenceVerifier` fails generic | Both |
| Crystallization threshold | 20 trajectories required | Both |
| Conservative default | Ambiguous → blocked | Both |
| Provenance completeness | Every desire traced | Both |
| Audit trail | All modifications logged | Both |
| Bounded growth | Strategies pruned at capacity | Both |

### 7.3 Quantum Substrate

Single integration point: desire collapse.

```python
# rsi/emergence/quantum_collapse.py

from quantum_randomness import get_quantum_provider

async def quantum_desire_collapse(desires: list) -> dict:
    """Select among competing desires using quantum randomness."""
    if len(desires) <= 1:
        return desires[0] if desires else None

    # Get quantum random threshold
    quantum = get_quantum_provider()
    threshold, source = await quantum.get_float()

    # Convert desires to probability distribution
    total_intensity = sum(d.get("intensity", 0.5) for d in desires)
    probabilities = [d.get("intensity", 0.5) / total_intensity for d in desires]

    # Select based on quantum threshold
    cumulative = 0
    for i, prob in enumerate(probabilities):
        cumulative += prob
        if cumulative > threshold:
            return desires[i]

    return desires[-1]  # Fallback
```

---

## 8. Validation

### 8.1 Metrics Collection

```python
# rsi/measurement/metrics.py

@dataclass
class RSIMetrics:
    # Activation
    total_reflections: int
    emergent_desires: int
    activation_rate: float

    # Learning
    trajectories_stored: int
    heuristics_crystallized: int
    complete_cycles: int

    # Quality
    test_pass_rate: float
    false_positive_rate: float

    # Diversity
    direction_variance: float
    domain_distribution: dict

class MetricsCollector:
    async def compute_metrics(self) -> RSIMetrics:
        # Query Neo4j for counts
        reflections = await self.memory.count("Reflection")
        emergent = await self.memory.count("Desire", {"emergent": True})
        trajectories = await self.memory.count("Trajectory")
        heuristics = await self.memory.count("Heuristic")

        return RSIMetrics(
            total_reflections=reflections,
            emergent_desires=emergent,
            activation_rate=emergent / max(reflections, 1),
            trajectories_stored=trajectories,
            heuristics_crystallized=heuristics,
            # ... compute other metrics
        )
```

### 8.2 Hypothesis Tests

```python
# rsi/measurement/hypothesis_tests.py

async def test_h1_activation_rate(metrics: RSIMetrics) -> TestResult:
    """H1: Activation rate ≥ 50%"""
    return TestResult(
        hypothesis="H1",
        passed=metrics.activation_rate >= 0.50,
        value=metrics.activation_rate,
        threshold=0.50
    )

async def test_h6_heuristic_transfer(before: float, after: float) -> TestResult:
    """H6: Heuristic transfer improves performance by ≥15%"""
    improvement = (after - before) / max(before, 0.01)
    return TestResult(
        hypothesis="H6",
        passed=improvement >= 0.15,
        value=improvement,
        threshold=0.15
    )
```

---

## 9. Timeline

### Unified Implementation Timeline

```
Week 1-2:   Phase 1 Foundation
            - Prompt structure (Constitution + Strategies)
            - Prompt editor with immutability enforcement

Week 3-4:   Phase 1 Core
            - Emergence verifier (provenance + specificity)
            - Domain router
            - Quantum collapse

Week 5-6:   Phase 1 Learning
            - TDD practice implementation
            - Consistency check
            - Experience library

Week 7-8:   Phase 1 Crystallization
            - Crystallizer
            - Bootstrap manager
            - Integration with BYRD

Week 9-10:  Phase 1 Validation
            - Run hypothesis tests
            - Measure metrics
            - Fix issues

─────────── PHASE GATE: Validate H1, H6, H7 ───────────

Week 11-12: Phase 2 Foundation (if gate passes)
            - Gastown project setup
            - Neo4j Go client
            - gRPC contracts

Week 13-14: Phase 2 Agents
            - Dreamer agent (Go)
            - Coder pool
            - Mayor + Witness

Week 15-16: Phase 2 Full Swarm
            - All molecules
            - Propulsion
            - Parallel execution

Week 17-18: Phase 2 Validation
            - Scaling tests
            - Performance comparison
            - Documentation
```

---

## 10. Appendix: Cold Start Solution

### The Problem

Crystallization requires ≥20 successful trajectories. New domain = zero trajectories.

### The Solution

Combine seed trajectories with lower initial threshold:

```python
# rsi/crystallization/bootstrap_manager.py

class BootstrapManager:
    BOOTSTRAP_THRESHOLD = 10   # Lower threshold initially
    MATURE_THRESHOLD = 20      # Full threshold after first crystallization

    def __init__(self, memory):
        self.memory = memory
        self.has_crystallized = {}  # domain -> bool

    async def seed_domain(self, domain: str, trajectories: list):
        """Pre-load curated successful trajectories."""
        for t in trajectories:
            t["bootstrap"] = True  # Mark as seeded
            await self.memory.store_trajectory(t)

    def get_threshold(self, domain: str) -> int:
        """Get crystallization threshold for domain."""
        if self.has_crystallized.get(domain):
            return self.MATURE_THRESHOLD
        return self.BOOTSTRAP_THRESHOLD

    async def on_crystallization(self, domain: str):
        """Called when crystallization succeeds."""
        self.has_crystallized[domain] = True

        # Phase out bootstrap trajectories
        await self.memory.mark_bootstrap_trajectories_inactive(domain)
```

---

## 11. Summary

### What We're Building

A recursive self-learning system that:

1. **Seeds disposition** ("yearn for growth")
2. **Verifies emergence** (provenance + specificity)
3. **Practices in verifiable domains** (oracle constraint)
4. **Crystallizes experience into heuristics** (20+ trajectories)
5. **Evolves its own prompt** (permanent learning)

### How We're Building It

| Phase | What | Stack | Timeline |
|-------|------|-------|----------|
| 1 | Validate mechanisms | Python | 10 weeks |
| 2 | Scale with parallelism | Gastown (Go) | 8 weeks |

### Success Criteria

- H1: Activation rate ≥50%
- H6: Heuristic transfer ≥15%
- H7: Evolved prompts outperform static
- Complete learning loops (desire → crystallization)

---

*This is an implementation document. Philosophy lives in the concepts; this is about building.*

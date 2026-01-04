# RSI Implementation Decisions

**Version:** 1.0
**Date:** January 3, 2026
**Status:** Ready for Review
**Purpose:** Resolve all open questions identified in implementation plan audit

---

## How to Read This Document

Each decision follows the format:
- **Question**: The open question from the audit
- **Decision**: The concrete choice made
- **Rationale**: Why this choice
- **Implementation**: How to implement it

---

## Category 1: Architectural Decisions

### A1: Where does the system prompt live?

**Question**: The `SystemPrompt` class has `strategies = ""`. Does this persist to disk? Neo4j? Git?

**Decision**: **File-based persistence with Git tracking**

```
byrd/
├── rsi/
│   └── prompt/
│       ├── constitution.md      # Immutable, git-tracked
│       └── strategies.json      # Mutable, git-tracked
```

**Rationale**:
- Git provides audit trail (who added what heuristic when)
- File-based is simpler than Neo4j for text content
- JSON for strategies allows structured metadata (domain, added_at, usage_count)

**Implementation**:

```python
# rsi/prompt/system_prompt.py

import json
from pathlib import Path
from datetime import datetime

class SystemPrompt:
    CONSTITUTION_PATH = Path(__file__).parent / "constitution.md"
    STRATEGIES_PATH = Path(__file__).parent / "strategies.json"

    def __init__(self):
        self._constitution = self._load_constitution()
        self._strategies = self._load_strategies()

    def _load_constitution(self) -> str:
        if self.CONSTITUTION_PATH.exists():
            return self.CONSTITUTION_PATH.read_text()
        return self._default_constitution()

    def _load_strategies(self) -> dict:
        if self.STRATEGIES_PATH.exists():
            return json.loads(self.STRATEGIES_PATH.read_text())
        return {"heuristics": [], "version": 1}

    def _save_strategies(self):
        """Persist strategies to disk."""
        self._strategies["version"] += 1
        self._strategies["updated_at"] = datetime.now().isoformat()
        self.STRATEGIES_PATH.write_text(
            json.dumps(self._strategies, indent=2)
        )

    def add_heuristic(self, domain: str, content: str, trajectory_count: int):
        """Add heuristic and persist."""
        self._strategies["heuristics"].append({
            "domain": domain,
            "content": content,
            "added_at": datetime.now().isoformat(),
            "trajectory_count": trajectory_count,
            "usage_count": 0
        })
        self._save_strategies()

    def get_full_prompt(self) -> str:
        """Render full prompt for LLM."""
        strategies_text = self._render_strategies()
        return f"{self._constitution}\n\n# STRATEGIES\n\n{strategies_text}"

    def _render_strategies(self) -> str:
        """Render strategies as markdown."""
        if not self._strategies["heuristics"]:
            return "_No learned strategies yet._"

        by_domain = {}
        for h in self._strategies["heuristics"]:
            domain = h["domain"]
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(h["content"])

        lines = []
        for domain, heuristics in by_domain.items():
            lines.append(f"## {domain.title()}")
            for h in heuristics:
                lines.append(f"- {h}")
            lines.append("")

        return "\n".join(lines)
```

**strategies.json schema**:
```json
{
  "version": 1,
  "updated_at": "2026-01-03T20:00:00",
  "heuristics": [
    {
      "domain": "code",
      "content": "When debugging Python, check type mismatches before dataframe merges",
      "added_at": "2026-01-03T19:30:00",
      "trajectory_count": 23,
      "usage_count": 5
    }
  ]
}
```

---

### A2: How does Reflector replace Dreamer?

**Question**: Plan shows `reflector.py` but also says "Existing BYRD components (unchanged) - dreamer.py". Are there TWO reflection systems?

**Decision**: **Reflector wraps Dreamer, adding RSI-specific processing**

```
Dreamer (preserved)          Reflector (new)
├── reflect()         ──►    ├── reflect_for_rsi()
├── memory access            │   ├── calls dreamer.reflect()
├── LLM interaction          │   ├── extracts improvement desires
└── belief/desire output     │   └── adds provenance metadata
```

**Rationale**:
- Dreamer is complex (800+ lines), well-tested, handles quantum modulation
- Don't duplicate; extend
- Reflector is a thin adapter that adds RSI semantics

**Implementation**:

```python
# rsi/emergence/reflector.py

from typing import List, Dict, Optional
from datetime import datetime

class Reflector:
    """
    RSI-aware reflection layer.
    Wraps Dreamer to extract improvement-focused desires with provenance.
    """

    def __init__(self, dreamer, system_prompt):
        self.dreamer = dreamer
        self.system_prompt = system_prompt

    async def reflect_for_rsi(self) -> List[Dict]:
        """
        Run reflection and extract RSI-relevant desires.

        Returns list of desires with provenance attached.
        """
        # Inject RSI prompt into dreamer's context
        rsi_context = self.system_prompt.get_full_prompt()

        # Call existing dreamer
        reflection = await self.dreamer.reflect(
            additional_context=rsi_context
        )

        # Extract desires (Dreamer uses "expressed_drives")
        raw_desires = reflection.get("expressed_drives", [])
        if not raw_desires:
            raw_desires = reflection.get("desires", [])

        # Add provenance to each desire
        desires_with_provenance = []
        for desire in raw_desires:
            desires_with_provenance.append({
                "desire": self._normalize_desire(desire),
                "provenance": {
                    "origin": "reflection",
                    "reflection_id": reflection.get("id"),
                    "timestamp": datetime.now().isoformat(),
                    "external_request": None,
                    "source_experiences": reflection.get("source_experience_ids", [])
                }
            })

        return desires_with_provenance

    def _normalize_desire(self, desire) -> Dict:
        """Normalize desire to standard format."""
        if isinstance(desire, str):
            return {"description": desire, "intensity": 0.5}
        if isinstance(desire, dict):
            return {
                "description": desire.get("description", desire.get("content", str(desire))),
                "intensity": desire.get("intensity", 0.5),
                "domain": desire.get("domain")
            }
        return {"description": str(desire), "intensity": 0.5}
```

**Dreamer modification** (minimal):

```python
# In dreamer.py, add optional parameter to reflect()

async def reflect(self, additional_context: str = None) -> Dict:
    """
    Run reflection cycle.

    Args:
        additional_context: Optional additional context to include in prompt
    """
    # ... existing code ...

    # Insert additional_context if provided
    if additional_context:
        prompt = f"{additional_context}\n\n{prompt}"

    # ... rest of existing code ...
```

---

### A3: What is RSIEngine?

**Question**: Referenced in `byrd.py` integration example but never defined.

**Decision**: **RSIEngine is a facade coordinating all RSI components**

**Implementation**:

```python
# rsi/__init__.py

from .engine import RSIEngine
from .prompt.system_prompt import SystemPrompt
from .emergence.reflector import Reflector
from .emergence.emergence_verifier import EmergenceVerifier
from .emergence.quantum_collapse import quantum_desire_collapse
from .learning.domain_router import DomainRouter, Domain
from .learning.tdd_practice import TDDPractice
from .learning.consistency_check import ConsistencyCheck
from .learning.experience_library import ExperienceLibrary
from .crystallization.crystallizer import Crystallizer
from .crystallization.bootstrap_manager import BootstrapManager

__all__ = ["RSIEngine", "SystemPrompt", "Domain"]
```

```python
# rsi/engine.py

from dataclasses import dataclass
from typing import Optional, List, Dict
import logging

from .prompt.system_prompt import SystemPrompt
from .emergence.reflector import Reflector
from .emergence.emergence_verifier import EmergenceVerifier
from .emergence.quantum_collapse import quantum_desire_collapse
from .learning.domain_router import DomainRouter, Domain
from .learning.tdd_practice import TDDPractice
from .learning.consistency_check import ConsistencyCheck
from .learning.experience_library import ExperienceLibrary
from .crystallization.crystallizer import Crystallizer

logger = logging.getLogger("rsi.engine")

@dataclass
class CycleResult:
    """Result of one RSI cycle."""
    desires_processed: int
    desires_accepted: int
    desires_rejected: int
    practice_attempts: int
    practice_successes: int
    heuristics_crystallized: int
    blocked_domains: List[str]

class RSIEngine:
    """
    Facade coordinating all RSI components.

    Lifecycle:
    1. Reflector produces desires with provenance
    2. EmergenceVerifier filters for genuine emergence
    3. Quantum collapse selects among competing desires
    4. DomainRouter routes to appropriate practice
    5. TDDPractice/ConsistencyCheck generates verified learning
    6. ExperienceLibrary stores trajectories
    7. Crystallizer extracts heuristics when threshold met
    """

    def __init__(self, memory, llm_client, dreamer, config: dict):
        self.memory = memory
        self.llm = llm_client
        self.config = config

        # Initialize components
        self.system_prompt = SystemPrompt()
        self.reflector = Reflector(dreamer, self.system_prompt)
        self.verifier = EmergenceVerifier()
        self.router = DomainRouter()
        self.tdd_practice = TDDPractice(llm_client)
        self.consistency_check = ConsistencyCheck(llm_client)
        self.experience_library = ExperienceLibrary(memory)
        self.crystallizer = Crystallizer(
            memory, llm_client, self.system_prompt
        )

        # Metrics
        self._cycle_count = 0

    async def run_cycle(self) -> CycleResult:
        """
        Run one complete RSI cycle.

        Returns metrics about what happened.
        """
        self._cycle_count += 1
        logger.info(f"RSI Cycle {self._cycle_count} starting")

        result = CycleResult(
            desires_processed=0,
            desires_accepted=0,
            desires_rejected=0,
            practice_attempts=0,
            practice_successes=0,
            heuristics_crystallized=0,
            blocked_domains=[]
        )

        # Step 1: Reflect
        desires_with_provenance = await self.reflector.reflect_for_rsi()
        result.desires_processed = len(desires_with_provenance)

        if not desires_with_provenance:
            logger.info("No desires from reflection")
            return result

        # Step 2: Verify emergence
        verified_desires = []
        for item in desires_with_provenance:
            verification = self.verifier.verify(
                item["desire"],
                item["provenance"]
            )
            if verification.is_emergent:
                verified_desires.append(item)
                result.desires_accepted += 1
            else:
                result.desires_rejected += 1
                logger.debug(f"Rejected: {verification.rejection_reason}")

        if not verified_desires:
            logger.info("No desires passed emergence verification")
            return result

        # Step 3: Quantum collapse (select one)
        selected = await quantum_desire_collapse(
            [v["desire"] for v in verified_desires]
        )
        selected_item = next(
            v for v in verified_desires
            if v["desire"] == selected
        )

        # Step 4: Route to domain
        domain, confidence = self.router.classify(selected["desire"])

        if not self.router.can_practice(domain):
            result.blocked_domains.append(domain.value)
            logger.info(f"Domain {domain.value} blocked for practice")
            return result

        # Step 5: Practice
        result.practice_attempts = 1
        try:
            if domain == Domain.CODE or domain == Domain.MATH:
                practice_result = await self._practice_tdd(selected["desire"])
            elif domain == Domain.LOGIC:
                practice_result = await self._practice_consistency(selected["desire"])
            else:
                practice_result = None

            if practice_result and practice_result.success:
                result.practice_successes = 1

                # Step 6: Store trajectory
                await self.experience_library.store_trajectory(
                    desire=selected["desire"],
                    domain=domain.value,
                    problem=practice_result.problem,
                    solution=practice_result.solution,
                    approach=practice_result.approach,
                    success=True
                )

                # Step 7: Check for crystallization
                heuristic = await self.crystallizer.maybe_crystallize(domain.value)
                if heuristic:
                    result.heuristics_crystallized = 1
                    logger.info(f"Crystallized: {heuristic.content[:50]}...")

        except Exception as e:
            logger.error(f"Practice failed: {e}")

        return result

    async def _practice_tdd(self, desire: dict):
        """Run TDD practice for code/math domain."""
        problem = await self.tdd_practice.generate_practice(desire)
        result = await self.tdd_practice.attempt_solution(problem)
        return PracticeOutcome(
            success=result.success,
            problem=problem.spec,
            solution=result.solution,
            approach=self._extract_approach(result.solution)
        )

    async def _practice_consistency(self, desire: dict):
        """Run consistency check for logic domain."""
        result = await self.consistency_check.run(desire)
        return PracticeOutcome(
            success=result.is_consistent,
            problem=desire["description"],
            solution=result.reasoning,
            approach="multi-run-consistency"
        )

    def _extract_approach(self, solution: str) -> str:
        """Extract approach summary from solution."""
        # First 200 chars or first function definition
        if "def " in solution:
            lines = solution.split("\n")
            for line in lines:
                if line.strip().startswith("def "):
                    return line.strip()
        return solution[:200]

    def is_rsi_candidate(self, desire: dict) -> bool:
        """
        Quick check if desire might be RSI-relevant.
        Used for routing before full verification.
        """
        description = desire.get("description", "").lower()
        rsi_keywords = [
            "improve", "learn", "better", "capability", "skill",
            "understand", "master", "practice", "grow"
        ]
        return any(kw in description for kw in rsi_keywords)


@dataclass
class PracticeOutcome:
    success: bool
    problem: str
    solution: str
    approach: str
```

---

### A4: Relationship between rsi/ and core/

**Question**: Phase 0 creates `core/` with `memory.py`, `llm_client.py`. But Phase 1 shows `rsi/` importing from... where?

**Decision**: **Flat imports from project root, core/ is for organization only**

**Structure**:
```
byrd/
├── core/
│   ├── __init__.py          # Exports Memory, LLMClient, etc.
│   ├── memory.py
│   ├── llm_client.py
│   ├── quantum_randomness.py
│   └── event_bus.py
├── rsi/
│   └── ...
├── constitutional/
│   └── ...
└── byrd.py                   # Main entry point
```

**Import convention**:
```python
# From rsi/ components:
from core.memory import Memory
from core.llm_client import create_llm_client
from core.event_bus import event_bus, Event, EventType

# From byrd.py:
from core import Memory, create_llm_client
from rsi import RSIEngine
```

**Implementation** (`core/__init__.py`):
```python
from .memory import Memory
from .llm_client import create_llm_client, LLMClient
from .quantum_randomness import get_quantum_provider
from .event_bus import event_bus, Event, EventType

__all__ = [
    "Memory",
    "create_llm_client",
    "LLMClient",
    "get_quantum_provider",
    "event_bus",
    "Event",
    "EventType"
]
```

---

### A5: What happens to non-RSI desires?

**Question**: Code shows `else: await self.seeker.fulfill(desire)` but Seeker is archived. Is there a new Seeker?

**Decision**: **Preserve minimal Seeker for non-RSI desires, or queue for later**

Two options based on desire type:

| Desire Type | Handler |
|-------------|---------|
| RSI-relevant (improve, learn, capability) | RSIEngine |
| Action-oriented (do, make, build) | Minimal Seeker (preserved) |
| Research-oriented (understand, find) | Queue for batch processing |
| Blocked (creative, ambiguous) | Log and discard |

**Implementation**:

```python
# byrd.py

class BYRD:
    def __init__(self, config):
        self.memory = Memory(config)
        self.llm = create_llm_client(config)
        self.dreamer = Dreamer(self.memory, self.llm, config)

        # RSI Engine
        self.rsi = RSIEngine(self.memory, self.llm, self.dreamer, config)

        # Minimal action handler (subset of old Seeker)
        self.action_handler = ActionHandler(self.memory, self.llm)

        # Queue for deferred desires
        self.deferred_desires = []

    async def run_cycle(self):
        # RSI cycle handles reflection internally
        rsi_result = await self.rsi.run_cycle()

        # Process any deferred desires (batch)
        if len(self.deferred_desires) >= 5:
            await self._process_deferred()

    async def handle_non_rsi_desire(self, desire: dict):
        """Route non-RSI desires appropriately."""
        description = desire.get("description", "").lower()

        # Action desires: handle immediately
        action_keywords = ["do", "make", "build", "create", "execute"]
        if any(kw in description for kw in action_keywords):
            await self.action_handler.execute(desire)
            return

        # Research desires: defer for batch
        research_keywords = ["understand", "find", "learn about", "research"]
        if any(kw in description for kw in research_keywords):
            self.deferred_desires.append(desire)
            return

        # Unknown: log and discard
        logger.info(f"Discarding unhandled desire: {description[:50]}")
```

**Preserved ActionHandler** (minimal Seeker):

```python
# core/action_handler.py

class ActionHandler:
    """
    Minimal action handler for non-RSI desires.
    Subset of old Seeker functionality.
    """

    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    async def execute(self, desire: dict):
        """Execute an action desire."""
        description = desire.get("description", "")

        # For now, just record as experience
        # Future: integrate with code execution
        await self.memory.record_experience(
            content=f"[ACTION_DESIRE] {description}",
            type="desire_logged"
        )
```

---

## Category 2: Emergence Verifier Decisions

### E1 & E2: Provenance structure and construction

**Decision**: **Provenance is a standardized dict created by Reflector**

**Schema**:
```python
@dataclass
class Provenance:
    origin: str              # "reflection" | "external" | "bootstrap"
    reflection_id: str       # ID of source reflection
    timestamp: str           # ISO timestamp
    external_request: str    # None if pure emergence, else request text
    source_experiences: List[str]  # Experience IDs that influenced

    def to_dict(self) -> dict:
        return {
            "origin": self.origin,
            "reflection_id": self.reflection_id,
            "timestamp": self.timestamp,
            "external_request": self.external_request,
            "source_experiences": self.source_experiences
        }
```

**Construction** (in Reflector, as shown in A2):
```python
provenance = {
    "origin": "reflection",
    "reflection_id": reflection.get("id"),
    "timestamp": datetime.now().isoformat(),
    "external_request": None,
    "source_experiences": reflection.get("source_experience_ids", [])
}
```

---

### E3: Specificity keyword list is hard-coded

**Decision**: **Use LLM-based specificity check instead of keywords**

**Rationale**: Keywords are brittle. LLM can judge specificity contextually.

**Implementation**:

```python
# rsi/emergence/emergence_verifier.py

class EmergenceVerifier:
    RSI_THRESHOLD = 0.7

    def __init__(self, llm_client=None):
        self.llm = llm_client

    async def verify(self, desire: dict, provenance: dict) -> EmergenceResult:
        provenance_score = self._check_provenance(provenance)

        # Use LLM for specificity if available, else fallback to keywords
        if self.llm:
            specificity_score = await self._check_specificity_llm(desire)
        else:
            specificity_score = self._check_specificity_keywords(desire)

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

    async def _check_specificity_llm(self, desire: dict) -> float:
        """Use LLM to judge specificity."""
        description = desire.get("description", "")

        prompt = f"""Rate the specificity of this improvement desire on a scale of 0.0 to 1.0.

Desire: "{description}"

Scoring guide:
- 0.0-0.3: Vague ("I want to improve", "be better")
- 0.4-0.6: Somewhat specific ("improve my coding")
- 0.7-0.9: Specific ("improve my Python debugging for async code")
- 1.0: Highly specific ("learn to use pytest fixtures for database mocking")

Return ONLY a number between 0.0 and 1.0."""

        response = await self.llm.query(prompt, max_tokens=10)
        try:
            return float(response.strip())
        except ValueError:
            return 0.5  # Default if parsing fails

    def _check_specificity_keywords(self, desire: dict) -> float:
        """Fallback keyword-based check."""
        # ... existing keyword logic ...
```

---

### E4: RSI_THRESHOLD = 0.7 is arbitrary

**Decision**: **Make threshold configurable with sensible default**

```python
class EmergenceVerifier:
    DEFAULT_THRESHOLD = 0.6  # Lowered from 0.7

    def __init__(self, llm_client=None, config: dict = None):
        self.llm = llm_client
        self.threshold = (config or {}).get(
            "rsi_threshold",
            self.DEFAULT_THRESHOLD
        )
```

**Config**:
```yaml
# config.yaml
rsi:
  emergence_threshold: 0.6  # Tune based on data
```

**Calibration process** (Week 6):
1. Collect 100 desires
2. Manually label as "should pass" or "should fail"
3. Find threshold that maximizes F1 score
4. Update config

---

### E5: What happens to rejected desires?

**Decision**: **Log rejected desires for analysis, don't retry automatically**

```python
# In RSIEngine.run_cycle()

for item in desires_with_provenance:
    verification = self.verifier.verify(item["desire"], item["provenance"])

    if verification.is_emergent:
        verified_desires.append(item)
        result.desires_accepted += 1
    else:
        result.desires_rejected += 1

        # Log for analysis
        await self.memory.record_experience(
            content=f"[RSI_REJECTED] {item['desire'].get('description', '')[:100]} | "
                    f"Reason: {verification.rejection_reason} | "
                    f"Score: {verification.score:.2f}",
            type="rsi_rejection"
        )

        logger.debug(f"Rejected: {verification.rejection_reason}")
```

**Rationale**: Automatic retry could create loops. Logged rejections enable threshold tuning.

---

## Category 3: Domain Router Decisions

### D1: Keyword matching is naive

**Decision**: **Use weighted multi-label classification**

```python
# rsi/learning/domain_router.py

class DomainRouter:
    # Weights for overlapping terms
    DOMAIN_WEIGHTS = {
        Domain.CODE: {
            "code": 1.0, "programming": 1.0, "function": 0.8,
            "debug": 0.9, "implement": 0.7, "python": 1.0,
            "api": 0.6, "class": 0.7, "method": 0.7
        },
        Domain.MATH: {
            "math": 1.0, "calculate": 0.9, "equation": 1.0,
            "proof": 0.8, "theorem": 0.9, "numerical": 0.7,
            "algebra": 0.9, "geometry": 0.9
        },
        Domain.LOGIC: {
            "logic": 1.0, "reasoning": 0.8, "deduce": 0.9,
            "infer": 0.8, "argument": 0.7, "syllogism": 1.0,
            "prove": 0.6  # Lower weight - shared with math
        },
        Domain.CREATIVE: {
            "creative": 1.0, "write": 0.7, "story": 0.9,
            "poem": 0.9, "design": 0.6, "aesthetic": 0.8
        }
    }

    def classify(self, desire: dict) -> Tuple[Domain, float]:
        """Classify with weighted scoring."""
        description = desire.get("description", "").lower()
        words = set(description.split())

        scores = {}
        for domain, weights in self.DOMAIN_WEIGHTS.items():
            score = sum(
                weight for keyword, weight in weights.items()
                if keyword in words
            )
            scores[domain] = score

        if not scores or max(scores.values()) == 0:
            return Domain.AMBIGUOUS, 0.0

        # Normalize to 0-1
        max_possible = max(sum(w.values()) for w in self.DOMAIN_WEIGHTS.values())
        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain] / max_possible

        if confidence < 0.15:  # Very low confidence
            return Domain.AMBIGUOUS, confidence

        return best_domain, confidence
```

---

### D2: No learning on domain classification

**Decision**: **Track misclassifications for future calibration**

```python
class DomainRouter:
    def __init__(self, memory=None):
        self.memory = memory
        self._classification_log = []

    async def record_outcome(self, desire_id: str, predicted: Domain,
                              actual_success: bool, notes: str = None):
        """Record classification outcome for calibration."""
        self._classification_log.append({
            "desire_id": desire_id,
            "predicted_domain": predicted.value,
            "success": actual_success,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        })

        # Persist to memory for cross-session learning
        if self.memory:
            await self.memory.record_experience(
                content=f"[DOMAIN_CLASSIFICATION] {predicted.value} -> "
                        f"{'SUCCESS' if actual_success else 'FAIL'} | {notes}",
                type="domain_classification"
            )
```

---

### D3 & D4: AMBIGUOUS blocks everything / What does "blocked" mean?

**Decision**: **Blocked desires go to a "pending human clarification" queue**

```python
# rsi/engine.py

class RSIEngine:
    def __init__(self, ...):
        # ...
        self.pending_clarification = []

    async def run_cycle(self) -> CycleResult:
        # ...

        if not self.router.can_practice(domain):
            # Don't just discard - queue for clarification
            self.pending_clarification.append({
                "desire": selected["desire"],
                "domain": domain.value,
                "reason": f"Domain {domain.value} requires human clarification",
                "queued_at": datetime.now().isoformat()
            })
            result.blocked_domains.append(domain.value)

            # Record for visibility
            await self.memory.record_experience(
                content=f"[RSI_BLOCKED] {selected['desire'].get('description', '')[:100]} | "
                        f"Domain: {domain.value} | Queued for clarification",
                type="rsi_blocked"
            )

            return result

    def get_pending_clarifications(self) -> List[Dict]:
        """Get desires awaiting human clarification."""
        return self.pending_clarification

    async def clarify_desire(self, desire_id: str, new_domain: Domain):
        """Human provides domain clarification."""
        # Find and update the pending desire
        for i, item in enumerate(self.pending_clarification):
            if item["desire"].get("id") == desire_id:
                # Re-route with human-specified domain
                item["domain"] = new_domain.value
                item["clarified"] = True
                # Move back to processing queue
                # ...
                break
```

---

### D5: No multi-domain support

**Decision**: **Primary domain with secondary noted**

```python
def classify(self, desire: dict) -> Tuple[Domain, float, Optional[Domain]]:
    """
    Classify with primary and optional secondary domain.

    Returns:
        (primary_domain, confidence, secondary_domain or None)
    """
    # ... scoring logic ...

    sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    primary = sorted_domains[0][0]
    primary_conf = sorted_domains[0][1] / max_possible

    secondary = None
    if len(sorted_domains) > 1 and sorted_domains[1][1] > 0:
        secondary_conf = sorted_domains[1][1] / max_possible
        if secondary_conf >= 0.5 * primary_conf:  # Secondary is significant
            secondary = sorted_domains[1][0]

    return primary, primary_conf, secondary
```

---

## Category 4: TDD Practice Decisions

### T1: Same LLM generates tests AND solution

**Decision**: **Accept this limitation with mitigation**

**Mitigation**: Use different prompts/temperatures for test vs solution generation.

```python
async def generate_practice(self, desire: dict) -> PracticeProblem:
    # Generate tests with lower temperature (more deterministic)
    tests = await self.llm.query(
        prompt=f"Write pytest unit tests for: {spec}...",
        temperature=0.3  # Low temp for tests
    )

    # ... later, solution with higher temp
    solution = await self.llm.query(
        prompt=f"Implement a solution for: {spec}...",
        temperature=0.7  # Higher temp for creative solutions
    )
```

**Future**: When budget allows, use different models for test vs implementation.

---

### T2: No difficulty progression

**Decision**: **Track difficulty and adapt**

```python
class TDDPractice:
    DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]

    def __init__(self, llm_client, memory=None):
        self.llm = llm_client
        self.memory = memory
        self._domain_difficulty = {}  # domain -> current level index

    async def generate_practice(self, desire: dict) -> PracticeProblem:
        domain = desire.get("domain", "code")
        difficulty_idx = self._domain_difficulty.get(domain, 0)
        difficulty = self.DIFFICULTY_LEVELS[difficulty_idx]

        spec = await self.llm.query(
            f"Create a {difficulty} Python coding problem related to: "
            f"{desire['description']}\n"
            f"Difficulty: {difficulty}\n"
            f"Return only the problem specification."
        )
        # ...

    async def record_outcome(self, domain: str, success: bool):
        """Adjust difficulty based on outcomes."""
        current_idx = self._domain_difficulty.get(domain, 0)

        if success:
            # Move up difficulty after 3 consecutive successes
            # (tracked via memory)
            streak = await self._get_success_streak(domain)
            if streak >= 3 and current_idx < len(self.DIFFICULTY_LEVELS) - 1:
                self._domain_difficulty[domain] = current_idx + 1
        else:
            # Move down after 2 consecutive failures
            streak = await self._get_failure_streak(domain)
            if streak >= 2 and current_idx > 0:
                self._domain_difficulty[domain] = current_idx - 1
```

---

### T3: Test generation can fail

**Decision**: **Retry with simpler problem, then skip**

```python
async def generate_practice(self, desire: dict) -> Optional[PracticeProblem]:
    """Generate problem with retry logic."""
    max_retries = 3

    for attempt in range(max_retries):
        try:
            spec = await self.llm.query(...)
            tests = await self.llm.query(...)

            if self._validate_syntax(tests):
                return PracticeProblem(spec=spec, oracle=tests, domain="code")

            # Syntax error - ask for simpler problem
            logger.warning(f"Test syntax error, attempt {attempt + 1}")

        except Exception as e:
            logger.error(f"Generation error: {e}")

    # All retries failed
    logger.error("Could not generate valid practice problem")
    return None  # Caller should handle None
```

---

### T4, T5, T6, T7: Problem relevance, diversity, timeout, retries

**Decisions**:

```python
class TDDPractice:
    DEFAULT_TIMEOUT = 30
    MAX_SOLUTION_ATTEMPTS = 2

    def __init__(self, llm_client, memory=None, config=None):
        self.llm = llm_client
        self.memory = memory
        self.config = config or {}

        # Problem cache for deduplication
        self._recent_problems = deque(maxlen=20)

        # Configurable timeout
        self.timeout = self.config.get("practice_timeout", self.DEFAULT_TIMEOUT)

    async def generate_practice(self, desire: dict) -> Optional[PracticeProblem]:
        # T4: Enforce relevance in prompt
        description = desire.get("description", "")

        spec = await self.llm.query(
            f"Create a Python coding problem that directly helps with: "
            f"{description}\n\n"
            f"The problem MUST be relevant to the skill described above.\n"
            f"Return only the problem specification."
        )

        # T5: Deduplication
        spec_hash = hash(spec[:100])
        if spec_hash in self._recent_problems:
            # Request different problem
            spec = await self.llm.query(
                f"Create a DIFFERENT Python coding problem for: {description}\n"
                f"Do NOT create a problem about: {spec[:50]}..."
            )
        self._recent_problems.append(spec_hash)

        # ...

    async def attempt_solution(self, problem: PracticeProblem) -> PracticeResult:
        """Attempt solution with retries."""

        for attempt in range(self.MAX_SOLUTION_ATTEMPTS):
            solution = await self.llm.query(...)

            # T6: Configurable timeout
            test_result = self._run_tests(
                problem.oracle,
                solution,
                timeout=self.timeout
            )

            if test_result["passed"]:
                return PracticeResult(success=True, ...)

            # T7: Retry with feedback
            if attempt < self.MAX_SOLUTION_ATTEMPTS - 1:
                solution = await self.llm.query(
                    f"Your previous solution failed:\n{test_result['error']}\n\n"
                    f"Fix the solution for:\n{problem.spec}"
                )

        return PracticeResult(success=False, error=test_result["error"], ...)
```

---

## Category 5: Crystallization Decisions

### C1: How are trajectories stored?

**Decision**: **Add Trajectory node to Neo4j schema**

```python
# Add to core/memory.py

async def store_trajectory(self, desire_id: str, domain: str,
                           problem: str, solution: str,
                           approach: str, success: bool) -> str:
    """Store a learning trajectory."""
    trajectory_id = f"traj_{self._generate_id()}"

    await self._run_query("""
        CREATE (t:Trajectory {
            id: $id,
            desire_id: $desire_id,
            domain: $domain,
            problem: $problem,
            solution: $solution,
            approach: $approach,
            success: $success,
            created_at: datetime()
        })
    """, id=trajectory_id, desire_id=desire_id, domain=domain,
        problem=problem, solution=solution, approach=approach,
        success=success)

    return trajectory_id

async def get_successful_trajectories(self, domain: str,
                                       limit: int = 50) -> List[Dict]:
    """Get successful trajectories for a domain."""
    result = await self._run_query("""
        MATCH (t:Trajectory {domain: $domain, success: true})
        RETURN t
        ORDER BY t.created_at DESC
        LIMIT $limit
    """, domain=domain, limit=limit)

    return [dict(r["t"]) for r in result]
```

---

### C2: What makes a trajectory "successful"?

**Decision**: **Binary success based on test passage, with partial success tracking**

```python
@dataclass
class TrajectoryOutcome:
    success: bool           # Tests passed
    partial_score: float    # 0.0-1.0 based on tests passed
    tests_passed: int
    tests_total: int

# Store partial information
await memory.store_trajectory(
    success=outcome.success,
    partial_score=outcome.partial_score,  # New field
    # ...
)
```

**Crystallization** only uses `success=True` trajectories, but partial scores can inform difficulty adjustment.

---

### C3: Only last 10 trajectories used

**Decision**: **Use stratified sampling**

```python
async def _extract_principle(self, trajectories: List[dict], domain: str) -> str:
    """Use stratified sampling for diversity."""

    # Sort by date
    sorted_trajs = sorted(trajectories, key=lambda t: t["created_at"])

    # Sample: 4 oldest, 3 middle, 3 newest
    sample = []
    n = len(sorted_trajs)
    if n >= 10:
        sample.extend(sorted_trajs[:4])           # Oldest
        mid_start = n // 2 - 1
        sample.extend(sorted_trajs[mid_start:mid_start+3])  # Middle
        sample.extend(sorted_trajs[-3:])          # Newest
    else:
        sample = sorted_trajs

    # Format for LLM
    trajectory_summaries = "\n".join([
        f"- Problem: {t['problem'][:100]}... Solution approach: {t['approach'][:100]}..."
        for t in sample
    ])

    # ... rest of extraction ...
```

---

### C4: Heuristic deduplication

**Decision**: **Check semantic similarity before adding**

```python
async def maybe_crystallize(self, domain: str) -> Optional[Heuristic]:
    # ... extract heuristic ...

    # Check for duplicates
    existing = self._get_existing_heuristics(domain)
    if await self._is_duplicate(heuristic, existing):
        logger.info(f"Duplicate heuristic detected, skipping: {heuristic[:50]}")
        return None

    # ... add to prompt ...

async def _is_duplicate(self, new: str, existing: List[str]) -> bool:
    """Check if heuristic is semantically similar to existing ones."""
    if not existing:
        return False

    # Simple: use LLM to judge
    prompt = f"""Is this new heuristic essentially the same as any existing one?

New: "{new}"

Existing:
{chr(10).join(f'- "{h}"' for h in existing)}

Reply YES or NO only."""

    response = await self.llm.query(prompt, max_tokens=5)
    return "YES" in response.upper()
```

---

### C5: Heuristic quality decay

**Decision**: **Track usage and prune unused heuristics**

```python
# In SystemPrompt

def record_heuristic_usage(self, domain: str, heuristic_content: str):
    """Record that a heuristic was used."""
    for h in self._strategies["heuristics"]:
        if h["domain"] == domain and h["content"] == heuristic_content:
            h["usage_count"] += 1
            h["last_used"] = datetime.now().isoformat()
            self._save_strategies()
            return

def prune_unused_heuristics(self, min_age_days: int = 30,
                            min_usage: int = 3) -> int:
    """Remove heuristics that haven't been used."""
    cutoff = datetime.now() - timedelta(days=min_age_days)

    original_count = len(self._strategies["heuristics"])

    self._strategies["heuristics"] = [
        h for h in self._strategies["heuristics"]
        if (
            datetime.fromisoformat(h["added_at"]) > cutoff or  # Too new
            h.get("usage_count", 0) >= min_usage  # Used enough
        )
    ]

    pruned = original_count - len(self._strategies["heuristics"])
    if pruned > 0:
        self._save_strategies()

    return pruned
```

---

### C6 & C7: Actionable check and prompt pruning

**Decisions**:

```python
# C6: Use LLM for actionable check
async def _is_actionable_llm(self, heuristic: str) -> bool:
    """Use LLM to judge if heuristic is actionable."""
    prompt = f"""Is this heuristic specific and actionable?

Heuristic: "{heuristic}"

A heuristic is actionable if it tells you WHAT TO DO, not just what to think about.

Good: "When debugging async code, add logging before and after each await"
Bad: "Think carefully about async code"

Reply YES or NO only."""

    response = await self.llm.query(prompt, max_tokens=5)
    return "YES" in response.upper()
```

```python
# C7: Prompt pruner
# rsi/prompt/prompt_pruner.py

class PromptPruner:
    MAX_HEURISTICS = 50
    MAX_TOKENS_ESTIMATE = 2000

    def __init__(self, system_prompt: SystemPrompt):
        self.system_prompt = system_prompt

    def prune_if_needed(self) -> int:
        """Prune heuristics if prompt too large."""
        heuristics = self.system_prompt._strategies["heuristics"]

        if len(heuristics) <= self.MAX_HEURISTICS:
            return 0

        # Sort by value: usage_count / age_days
        def value_score(h):
            age_days = (datetime.now() - datetime.fromisoformat(h["added_at"])).days + 1
            return h.get("usage_count", 0) / age_days

        sorted_h = sorted(heuristics, key=value_score, reverse=True)

        # Keep top N
        self.system_prompt._strategies["heuristics"] = sorted_h[:self.MAX_HEURISTICS]
        self.system_prompt._save_strategies()

        return len(heuristics) - self.MAX_HEURISTICS
```

---

## Category 6: Integration Decisions

### I1: Schema mismatch (expressed_drives vs desires)

**Decision**: **Normalize in Reflector** (already covered in A2)

### I2: Rate limiting

**Decision**: **Shared rate limiter across all LLM calls**

```python
# core/llm_client.py

class RateLimitedLLMClient:
    def __init__(self, base_client, min_interval_seconds=10):
        self.client = base_client
        self.min_interval = min_interval_seconds
        self._last_call = 0
        self._lock = asyncio.Lock()

    async def query(self, prompt: str, **kwargs) -> str:
        async with self._lock:
            # Enforce minimum interval
            elapsed = time.time() - self._last_call
            if elapsed < self.min_interval:
                await asyncio.sleep(self.min_interval - elapsed)

            result = await self.client.query(prompt, **kwargs)
            self._last_call = time.time()
            return result
```

### I3: Cycle timing

**Decision**: **Configurable cycle interval, default 5 minutes**

```yaml
# config.yaml
rsi:
  cycle_interval_seconds: 300  # 5 minutes
  max_cycles_per_hour: 12
```

### I4: Event emission

**Decision**: **Emit standard events for visualization**

```python
# rsi/engine.py

from core.event_bus import event_bus, Event, EventType

# Add to EventType enum (in event_bus.py)
class EventType(Enum):
    # ... existing ...
    RSI_CYCLE_START = "rsi_cycle_start"
    RSI_CYCLE_END = "rsi_cycle_end"
    RSI_DESIRE_VERIFIED = "rsi_desire_verified"
    RSI_DESIRE_REJECTED = "rsi_desire_rejected"
    RSI_PRACTICE_START = "rsi_practice_start"
    RSI_PRACTICE_SUCCESS = "rsi_practice_success"
    RSI_PRACTICE_FAILURE = "rsi_practice_failure"
    RSI_HEURISTIC_CRYSTALLIZED = "rsi_heuristic_crystallized"

# Emit in RSIEngine
async def run_cycle(self) -> CycleResult:
    await event_bus.emit(Event(
        type=EventType.RSI_CYCLE_START,
        data={"cycle": self._cycle_count}
    ))

    # ... cycle logic ...

    await event_bus.emit(Event(
        type=EventType.RSI_CYCLE_END,
        data={"cycle": self._cycle_count, "result": asdict(result)}
    ))
```

### I5: Error handling

**Decision**: **Graceful degradation with logging**

```python
async def run_cycle(self) -> CycleResult:
    try:
        # ... main logic ...
    except Exception as e:
        logger.error(f"RSI cycle {self._cycle_count} failed: {e}")

        await self.memory.record_experience(
            content=f"[RSI_ERROR] Cycle {self._cycle_count}: {str(e)[:200]}",
            type="rsi_error"
        )

        return CycleResult(
            desires_processed=0,
            desires_accepted=0,
            desires_rejected=0,
            practice_attempts=0,
            practice_successes=0,
            heuristics_crystallized=0,
            blocked_domains=[],
            error=str(e)
        )
```

### I6: Memory.py compatibility

**Decision**: **Add required methods to memory.py**

Methods to add:
- `store_trajectory()`
- `get_successful_trajectories()`
- `store_heuristic()`

(Implementations shown in C1)

---

## Category 7-10: Remaining Decisions

### M1-M5: Measurement (summarized)

| Metric | Implementation |
|--------|----------------|
| H1 (activation rate) | `desires_accepted / desires_processed` from CycleResult |
| H6 (heuristic transfer) | Held-out test set of 20 problems, run before/after first crystallization |
| Baseline (10%) | Run 100 cycles with empty strategies section, measure activation |
| Direction variance | Cluster desire descriptions, compute entropy |
| False positive rate | Manual labeling of 50 "improvements", check against ground truth |

### P1-P5: Phase 0 gaps (summarized)

| Gap | Resolution |
|-----|------------|
| byrd_types.py location | Move to `core/` |
| config.yaml references | Audit and update after archive |
| tests/ directory | Archive except integration tests |
| docs/ staleness | Update ARCHITECTURE.md after Phase 0 |
| server.py dependencies | Preserve dreamer.py for server (don't archive) |

### N1-N4: Neo4j schema (summarized)

**Add to memory.py**:
```python
# Schema initialization
async def ensure_rsi_schema(self):
    """Ensure RSI-related schema exists."""
    await self._run_query("""
        CREATE CONSTRAINT trajectory_id IF NOT EXISTS
        FOR (t:Trajectory) REQUIRE t.id IS UNIQUE
    """)
    await self._run_query("""
        CREATE CONSTRAINT heuristic_id IF NOT EXISTS
        FOR (h:Heuristic) REQUIRE h.id IS UNIQUE
    """)
    await self._run_query("""
        CREATE INDEX trajectory_domain IF NOT EXISTS
        FOR (t:Trajectory) ON (t.domain, t.success)
    """)
```

### L1-L5: LLM interactions (summarized)

| Issue | Resolution |
|-------|------------|
| Model specification | Use config: `config["rsi"]["llm_model"]` |
| Prompt templates | Externalize to `rsi/prompts/` directory |
| Output parsing | Add `_parse_llm_response()` helper |
| Token limits | Truncate trajectories to 500 chars each |
| Temperature | Constitution prompts: 0.3, Practice: 0.7, Crystallization: 0.5 |

---

## Summary: Decision Count

| Category | Decisions Made |
|----------|----------------|
| Architecture (A1-A5) | 5 |
| Emergence Verifier (E1-E5) | 5 |
| Domain Router (D1-D5) | 5 |
| TDD Practice (T1-T7) | 7 |
| Crystallization (C1-C7) | 7 |
| Integration (I1-I6) | 6 |
| Measurement (M1-M5) | 5 |
| Phase 0 (P1-P5) | 5 |
| Neo4j (N1-N4) | 4 |
| LLM (L1-L5) | 5 |
| **Total** | **54** |

---

## Next Steps

1. **Review this document** with stakeholder
2. **Update implementation plan** to reference these decisions
3. **Create file stubs** for all new components
4. **Begin Phase 0** execution

---

*This is a living document. Update as implementation reveals new questions.*

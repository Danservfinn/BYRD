"""
RSIEngine - Facade coordinating all RSI components.

The RSI cycle:
1. REFLECT: Generate improvement desires from constitution + context
2. VERIFY: Check emergence (provenance + specificity)
3. COLLAPSE: Quantum selection among competing desires
4. ROUTE: Classify domain and check oracle constraint
5. PRACTICE: TDD for code/math, consistency for logic
6. RECORD: Store trajectory in experience library
7. CRYSTALLIZE: Extract heuristics if threshold met
8. MEASURE: Track metrics for hypothesis validation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from .prompt import SystemPrompt, PromptPruner
from .emergence import Reflector, EmergenceVerifier, quantum_desire_collapse
from .learning import (
    DomainRouter, Domain, TDDPractice, ConsistencyCheck,
    ExperienceLibrary, PracticeResult
)
from .crystallization import Crystallizer, BootstrapManager
from .measurement import MetricsCollector
from .preconditions import PreconditionChecker, create_precondition_checker

# Import cancellation infrastructure for interruptible RSI cycles
from core.async_cancellation import CancellationToken

logger = logging.getLogger("rsi.engine")


# Domain Stratification - Effort allocation by verifiability
# Based on research showing RSI is most effective in fully verifiable domains
DOMAIN_WEIGHTS = {
    "stratum_1": 0.60,  # Fully verifiable (code, math) - highest priority
    "stratum_2": 0.30,  # Partially verifiable (planning, logic)
    "stratum_3": 0.10,  # Weakly verifiable (creative, open-ended)
}

# Domain-to-stratum mapping
DOMAIN_STRATUM = {
    "code": "stratum_1",      # Ground truth via tests
    "math": "stratum_1",      # Provable correctness
    "logic": "stratum_2",     # Consistency checkable
    "planning": "stratum_2",  # Partially verifiable
    "creative": "stratum_3",  # Subjective evaluation
    "general": "stratum_3",   # Weak verification
}


class CyclePhase(Enum):
    """Phases of the RSI cycle."""
    REFLECT = "reflect"
    VERIFY = "verify"
    COLLAPSE = "collapse"
    ROUTE = "route"
    PRACTICE = "practice"
    RECORD = "record"
    CRYSTALLIZE = "crystallize"
    MEASURE = "measure"


@dataclass
class CycleResult:
    """Result of a complete RSI cycle."""
    cycle_id: str
    started_at: str
    completed_at: str
    phase_reached: CyclePhase

    # Emergence
    desires_generated: int = 0
    desires_verified: int = 0
    desires_rejected: int = 0
    selected_desire: Optional[Dict] = None

    # Practice
    domain: Optional[str] = None
    domain_blocked: bool = False
    practice_attempted: bool = False
    practice_succeeded: bool = False
    practice_details: Optional[Dict] = None

    # Crystallization
    heuristic_crystallized: Optional[str] = None

    # Interruption
    interrupted: bool = False
    cancellation_reason: Optional[str] = None

    # Errors
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "cycle_id": self.cycle_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "phase_reached": self.phase_reached.value,
            "desires_generated": self.desires_generated,
            "desires_verified": self.desires_verified,
            "desires_rejected": self.desires_rejected,
            "selected_desire": self.selected_desire,
            "domain": self.domain,
            "domain_blocked": self.domain_blocked,
            "practice_attempted": self.practice_attempted,
            "practice_succeeded": self.practice_succeeded,
            "heuristic_crystallized": self.heuristic_crystallized,
            "interrupted": self.interrupted,
            "cancellation_reason": self.cancellation_reason,
            "error": self.error
        }


class RSIEngine:
    """
    Recursive Self-Improvement Engine.

    Coordinates the full RSI cycle:
    Reflect → Verify → Collapse → Route → Practice → Record → Crystallize → Measure

    This is the main entry point for RSI functionality.
    """

    def __init__(
        self,
        memory,
        llm_client,
        quantum_provider=None,
        event_bus=None,
        config: Optional[Dict] = None,
        coder=None,
        precondition_checker=None
    ):
        """
        Initialize RSI Engine with all components.

        Args:
            memory: Memory instance for Neo4j operations
            llm_client: LLM client for all AI operations
            quantum_provider: Optional quantum randomness provider
            event_bus: Optional event bus for visualization
            config: Optional configuration overrides
            coder: Optional ClaudeCoder instance for CODE/MATH practice
                   If provided, replaces TDDPractice for code domain
            precondition_checker: Optional PreconditionChecker for validating
                                 strategy dependencies before execution
        """
        self.memory = memory
        self.llm = llm_client
        self.quantum = quantum_provider
        self.event_bus = event_bus
        self.config = config or {}
        self.coder = coder
        self.precondition_checker = precondition_checker or create_precondition_checker(config)

        # Initialize components
        self.system_prompt = SystemPrompt()
        self.pruner = PromptPruner(self.system_prompt)

        self.reflector = Reflector(
            memory=memory,
            llm_client=llm_client,
            system_prompt=self.system_prompt
        )

        emergence_config = config.get("emergence", {}) if config else {}
        self.verifier = EmergenceVerifier(
            llm_client=llm_client,
            config=emergence_config
        )

        self.router = DomainRouter()

        self.experience_library = ExperienceLibrary(memory)

        self.tdd_practice = TDDPractice(
            llm_client=llm_client,
            memory=memory,
            config=config
        )

        consistency_config = config.get("consistency_check", {}) if config else {}
        self.consistency_check = ConsistencyCheck(
            llm_client=llm_client,
            config=consistency_config
        )

        self.crystallizer = Crystallizer(
            memory=memory,
            llm_client=llm_client,
            system_prompt=self.system_prompt,
            experience_library=self.experience_library
        )

        self.bootstrap = BootstrapManager(
            memory=memory,
            experience_library=self.experience_library
        )

        self.metrics = MetricsCollector(memory)

        # Cycle tracking
        self._cycle_count = 0
        self._cycle_history: List[CycleResult] = []

        # Precondition violation tracking
        self._precondition_violations: Dict[str, int] = {}

        logger.info("RSIEngine initialized with all components")

    async def run_cycle(self, meta_context: Optional[Dict] = None, cancellation_token: Optional[CancellationToken] = None) -> CycleResult:
        """
        Run one complete RSI cycle.

        Args:
            meta_context: Optional meta-context from Ralph orchestration.
                If provided, this context is passed to the reflector and can
                include information about the Ralph loop (iteration count,
                entropy trends, time in loop, etc.) for meta-awareness.
            cancellation_token: Optional cancellation token for interruptible
                RSI cycles. If provided, the cycle can be cancelled at phase
                boundaries when a human task arrives.

        Returns:
            CycleResult with details of what happened
        """
        self._cycle_count += 1
        cycle_id = f"rsi_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._cycle_count}"

        result = CycleResult(
            cycle_id=cycle_id,
            started_at=datetime.now().isoformat(),
            completed_at="",
            phase_reached=CyclePhase.REFLECT
        )

        try:
            # Phase 1: REFLECT
            await self._emit_event("RSI_PHASE", {"phase": "reflect", "cycle": cycle_id})
            desires = await self.reflector.reflect_for_rsi(meta_context=meta_context)
            result.desires_generated = len(desires)

            if not desires:
                logger.info("No desires emerged from reflection")
                result.phase_reached = CyclePhase.REFLECT
                return self._finalize_result(result)

            logger.info(f"Generated {len(desires)} desires from reflection")

            # Check for cancellation before VERIFY phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.VERIFY):
                return self._finalize_result(result)

            # Phase 2: VERIFY
            result.phase_reached = CyclePhase.VERIFY
            await self._emit_event("RSI_PHASE", {"phase": "verify", "cycle": cycle_id})

            verified_desires = []
            for desire in desires:
                emergence_result = await self.verifier.verify(
                    desire=desire.desire,
                    provenance=desire.provenance
                )

                if emergence_result.is_emergent:
                    verified_desires.append(desire)
                    logger.debug(f"Verified: {desire.desire.get('description', '')[:50]}...")
                else:
                    result.desires_rejected += 1
                    logger.debug(f"Rejected: {emergence_result.rejection_reason}")

            result.desires_verified = len(verified_desires)

            if not verified_desires:
                logger.info("No desires passed verification")
                return self._finalize_result(result)

            # Check for cancellation before COLLAPSE phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.COLLAPSE):
                return self._finalize_result(result)

            # Phase 3: COLLAPSE
            result.phase_reached = CyclePhase.COLLAPSE
            await self._emit_event("RSI_PHASE", {"phase": "collapse", "cycle": cycle_id})

            # Convert to dicts for quantum collapse
            desire_dicts = [d.desire for d in verified_desires]
            selected, collapse_source = await quantum_desire_collapse(
                desire_dicts,
                self.quantum
            )

            if not selected:
                logger.warning("Quantum collapse returned no selection")
                return self._finalize_result(result)

            result.selected_desire = selected
            logger.info(f"Selected desire ({collapse_source}): {selected.get('description', '')[:80]}")

            # Check for cancellation before ROUTE phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.ROUTE):
                return self._finalize_result(result)

            # Phase 4: ROUTE
            result.phase_reached = CyclePhase.ROUTE
            await self._emit_event("RSI_PHASE", {"phase": "route", "cycle": cycle_id})

            classification = self.router.classify(selected)
            result.domain = classification.primary.value

            if not self.router.can_practice(classification.primary):
                result.domain_blocked = True
                logger.info(f"Domain {classification.primary.value} blocked by oracle constraint")
                # Record that we tried but couldn't practice
                result.phase_reached = CyclePhase.RECORD
                await self._record_blocked_attempt(selected, classification.primary)
                return self._finalize_result(result)

            # Ensure bootstrap for this domain
            await self.bootstrap.ensure_bootstrap(classification.primary.value)

            # Check for cancellation before PRACTICE phase (typically longest)
            if self._check_cancelled(result, cancellation_token, CyclePhase.PRACTICE):
                return self._finalize_result(result)

            # Phase 5: PRACTICE
            result.phase_reached = CyclePhase.PRACTICE
            await self._emit_event("RSI_PHASE", {"phase": "practice", "cycle": cycle_id})
            result.practice_attempted = True

            practice_result = await self._run_practice(selected, classification.primary)

            if practice_result:
                result.practice_succeeded = practice_result.success
                result.practice_details = {
                    "problem": practice_result.problem[:200] if hasattr(practice_result, 'problem') else "",
                    "approach": practice_result.approach[:200] if hasattr(practice_result, 'approach') else "",
                    "success": practice_result.success,
                    "attempts": getattr(practice_result, 'attempts', 1)
                }

            # Check for cancellation before RECORD phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.RECORD):
                return self._finalize_result(result)

            # Phase 6: RECORD
            result.phase_reached = CyclePhase.RECORD
            await self._emit_event("RSI_PHASE", {"phase": "record", "cycle": cycle_id})

            if practice_result:
                await self.experience_library.store_trajectory(
                    desire=selected,
                    domain=classification.primary.value,
                    problem=getattr(practice_result, 'problem', ''),
                    solution=getattr(practice_result, 'solution', ''),
                    approach=getattr(practice_result, 'approach', ''),
                    success=practice_result.success,
                    metadata={
                        "cycle_id": cycle_id,
                        "attempts": getattr(practice_result, 'attempts', 1),
                        "difficulty": getattr(practice_result, 'difficulty', 'beginner')
                    }
                )

            # Check for cancellation before CRYSTALLIZE phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.CRYSTALLIZE):
                return self._finalize_result(result)

            # Phase 7: CRYSTALLIZE (only if practice succeeded)
            if practice_result and practice_result.success:
                result.phase_reached = CyclePhase.CRYSTALLIZE
                await self._emit_event("RSI_PHASE", {"phase": "crystallize", "cycle": cycle_id})

                heuristic = await self.crystallizer.maybe_crystallize(
                    classification.primary.value
                )

                if heuristic:
                    result.heuristic_crystallized = heuristic.content
                    logger.info(f"Crystallized heuristic: {heuristic.content[:80]}...")

                    # Notify bootstrap manager
                    await self.bootstrap.on_crystallization(classification.primary.value)

                    # Prune if needed
                    pruned = self.pruner.prune_if_needed()
                    if pruned > 0:
                        logger.info(f"Pruned {pruned} low-value heuristics")

            # Check for cancellation before MEASURE phase
            if self._check_cancelled(result, cancellation_token, CyclePhase.MEASURE):
                return self._finalize_result(result)

            # Phase 8: MEASURE
            result.phase_reached = CyclePhase.MEASURE
            await self._emit_event("RSI_PHASE", {"phase": "measure", "cycle": cycle_id})

            # Record cycle in metrics
            self.metrics.record_cycle({
                "desires_processed": result.desires_generated,
                "desires_accepted": result.desires_verified,
                "desires_rejected": result.desires_rejected,
                "practice_attempts": 1 if result.practice_attempted else 0,
                "practice_successes": 1 if result.practice_succeeded else 0,
                "heuristics_crystallized": 1 if result.heuristic_crystallized else 0,
                "blocked_domains": [result.domain] if result.domain_blocked else [],
                "duration_seconds": 0  # Would need timing
            })

            return self._finalize_result(result)

        except Exception as e:
            logger.error(f"RSI cycle error: {e}", exc_info=True)
            result.error = str(e)
            return self._finalize_result(result)

    def _check_cancelled(self, result: CycleResult, token: Optional[CancellationToken], phase: CyclePhase) -> bool:
        """
        Check if cancellation has been requested and return True if cycle should stop.

        Args:
            result: The cycle result to update
            token: The cancellation token to check
            phase: The phase we're about to enter (or just completed)

        Returns:
            True if cancelled, False otherwise
        """
        if token and token.is_cancelled:
            result.interrupted = True
            result.phase_reached = phase
            result.cancellation_reason = token.cancellation_reason.value if token.cancellation_reason else "unknown"
            logger.info(f"RSI cycle cancelled at {phase.value} phase: {result.cancellation_reason}")
            return True
        return False

    async def _run_practice(
        self,
        desire: Dict,
        domain: Domain
    ) -> Optional[PracticeResult]:
        """
        Run practice for the given domain.

        Args:
            desire: The improvement desire
            domain: Classified domain

        Returns:
            PracticeResult or None if practice failed
        """
        try:
            if domain == Domain.CODE or domain == Domain.MATH:
                # Use ClaudeCoder if available, fallback to TDD practice
                if self.coder and domain == Domain.CODE:
                    return await self._run_coder_practice(desire)
                else:
                    # Use TDD practice
                    problem = await self.tdd_practice.generate_practice(desire)
                    if not problem:
                        logger.warning("Failed to generate practice problem")
                        return None

                    result = await self.tdd_practice.attempt_solution(problem)
                    await self.tdd_practice.record_outcome(domain.value, result)
                    return result

            elif domain == Domain.LOGIC:
                # Use consistency check
                result = await self.consistency_check.run(desire)
                # Convert to PracticeResult-like
                return PracticeResult(
                    success=result.is_consistent if result else False,
                    solution=result.reasoning or "" if result else "",
                    test_output=result.variance_notes if result else "No result",
                    tests_passed=int(result.consistency_score * len(result.responses)) if result else 0,
                    tests_total=len(result.responses) if result else 0,
                    problem=desire.get("description", ""),
                    approach="Multi-run consistency verification",
                    attempts=len(result.responses) if result else 0,
                    difficulty="intermediate"
                )

            else:
                logger.warning(f"No practice method for domain: {domain}")
                return None

        except Exception as e:
            logger.error(f"Practice error: {e}")
            return None

    async def _run_coder_practice(self, desire: Dict) -> Optional[PracticeResult]:
        """
        Run coding practice using ClaudeCoder (Claude Agent SDK).

        Args:
            desire: The improvement desire

        Returns:
            PracticeResult with coder execution details
        """
        description = desire.get("description", "")
        desire_id = desire.get("id", "")

        logger.info(f"Running ClaudeCoder practice: {description[:80]}...")

        # Check preconditions BEFORE attempting execution
        precondition_result = await self.precondition_checker.check_strategy_preconditions(
            strategy="claude_coder",
            context={"task": description}
        )

        if not precondition_result.can_proceed:
            # Preconditions not met - record violation and fail gracefully
            violation_key = "claude_coder:" + list(precondition_result.details.get("blocking", ["unknown"]))[0]
            self._precondition_violations[violation_key] = self._precondition_violations.get(violation_key, 0) + 1

            logger.warning(f" ClaudeCoder preconditions not met: {precondition_result.message}")

            # Record precondition failure to memory
            try:
                await self.memory.record_experience(
                    content=f"[PRECONDITION_FAILURE] Strategy: claude_coder | Reason: {precondition_result.message} | Desire: {description[:100]}",
                    type="precondition_violation"
                )
            except Exception:
                pass  # Memory errors shouldn't block the cycle

            return PracticeResult(
                success=False,
                solution="",
                test_output=precondition_result.message,
                tests_passed=0,
                tests_total=1,
                problem=description,
                approach="ClaudeCoder preconditions not met",
                attempts=0,
                difficulty="intermediate"
            )

        # Check if coder can execute this task (constitutional constraints)
        can_exec = await self.coder.can_execute(description)
        if not can_exec.get("can_execute"):
            logger.warning(f"Coder cannot execute: {can_exec.get('reason')}")
            return PracticeResult(
                success=False,
                solution="",
                test_output=can_exec.get("reason", "Unknown"),
                tests_passed=0,
                tests_total=1,
                problem=description,
                approach="ClaudeCoder blocked",
                attempts=0,
                difficulty="intermediate"
            )

        # Execute via ClaudeCoder
        coder_result = await self.coder.execute(
            prompt=description,
            desire_id=desire_id
        )

        # Convert ClaudeCoderResult to PracticeResult
        return PracticeResult(
            success=coder_result.success,
            solution=coder_result.output[:2000] if coder_result.output else "",
            test_output=coder_result.error or "Execution completed",
            tests_passed=1 if coder_result.success else 0,
            tests_total=1,
            problem=description,
            approach=f"ClaudeCoder (files: {', '.join(coder_result.files_modified[:3])})" if coder_result.files_modified else "ClaudeCoder",
            attempts=coder_result.turns_used,
            difficulty="intermediate"
        )

    async def _record_blocked_attempt(self, desire: Dict, domain: Domain):
        """Record that a desire was blocked by oracle constraint."""
        try:
            await self.memory.record_experience(
                content=f"[RSI_BLOCKED] Desire blocked by oracle constraint. Domain: {domain.value}. Description: {desire.get('description', '')[:200]}",
                type="rsi_blocked"
            )
        except Exception as e:
            logger.warning(f"Failed to record blocked attempt: {e}")

    async def _emit_event(self, event_type: str, data: Dict):
        """Emit an event if event bus is available."""
        if self.event_bus:
            try:
                from event_bus import Event, EventType
                # Map string to EventType if needed
                await self.event_bus.emit(Event(
                    type=EventType.SYSTEM if not hasattr(EventType, event_type) else getattr(EventType, event_type),
                    data=data
                ))
            except Exception as e:
                logger.debug(f"Event emission failed: {e}")

    def _finalize_result(self, result: CycleResult) -> CycleResult:
        """Finalize cycle result with timing."""
        result.completed_at = datetime.now().isoformat()
        self._cycle_history.append(result)

        # Trim history to last 100 cycles
        if len(self._cycle_history) > 100:
            self._cycle_history = self._cycle_history[-100:]

        return result

    async def get_metrics(self) -> Dict:
        """Get comprehensive RSI metrics."""
        rsi_metrics = await self.metrics.compute_metrics()
        crystallizer_stats = self.crystallizer.get_stats()
        bootstrap_status = self.bootstrap.get_status()

        return {
            "rsi_metrics": {
                "total_reflections": rsi_metrics.total_reflections,
                "emergent_desires": rsi_metrics.emergent_desires,
                "activation_rate": rsi_metrics.activation_rate,
                "trajectories_stored": rsi_metrics.trajectories_stored,
                "trajectory_success_rate": rsi_metrics.trajectory_success_rate,
                "heuristics_crystallized": rsi_metrics.heuristics_crystallized,
                "complete_cycles": rsi_metrics.complete_cycles,
                "direction_variance": rsi_metrics.direction_variance,
                "domain_distribution": rsi_metrics.domain_distribution
            },
            "crystallization": crystallizer_stats,
            "bootstrap": bootstrap_status,
            "cycle_count": self._cycle_count,
            "recent_cycles": [c.to_dict() for c in self._cycle_history[-10:]],
            "precondition_violations": self._precondition_violations.copy()
        }

    def get_system_prompt(self) -> str:
        """Get the current full system prompt."""
        return self.system_prompt.get_full_prompt()

    def get_heuristics(self, domain: Optional[str] = None) -> List[Dict]:
        """Get current heuristics, optionally filtered by domain."""
        return self.system_prompt.get_heuristics(domain)

    def reset(self):
        """Reset all RSI state."""
        self._cycle_count = 0
        self._cycle_history.clear()
        self._precondition_violations.clear()
        self.metrics.reset()
        self.crystallizer.reset()
        self.bootstrap.reset()
        self.tdd_practice.reset()
        self.verifier.reset()
        if self.precondition_checker:
            self.precondition_checker.clear_cache()
        logger.info("RSIEngine reset complete")

    def get_domain_weight(self, domain: str) -> float:
        """
        Get effort weight for a domain based on stratification.

        Domains in stratum_1 (fully verifiable) get highest priority.
        """
        stratum = DOMAIN_STRATUM.get(domain.lower(), "stratum_3")
        return DOMAIN_WEIGHTS.get(stratum, 0.10)

    def should_prioritize_domain(self, domain: str) -> bool:
        """
        Check if a domain should be prioritized for improvement.

        Stratum 1 domains (code, math) are always prioritized.
        """
        stratum = DOMAIN_STRATUM.get(domain.lower(), "stratum_3")
        return stratum == "stratum_1"

    def get_stratum_for_domain(self, domain: str) -> str:
        """Get the verification stratum for a domain."""
        return DOMAIN_STRATUM.get(domain.lower(), "stratum_3")

    def get_domain_stratification_stats(self) -> Dict:
        """Get statistics on domain stratification usage."""
        # Count cycles by stratum
        stratum_counts = {"stratum_1": 0, "stratum_2": 0, "stratum_3": 0}
        stratum_successes = {"stratum_1": 0, "stratum_2": 0, "stratum_3": 0}

        for cycle in self._cycle_history:
            if cycle.domain:
                stratum = self.get_stratum_for_domain(cycle.domain)
                stratum_counts[stratum] += 1
                if cycle.practice_succeeded:
                    stratum_successes[stratum] += 1

        return {
            "domain_weights": DOMAIN_WEIGHTS,
            "domain_stratum_mapping": DOMAIN_STRATUM,
            "stratum_counts": stratum_counts,
            "stratum_successes": stratum_successes,
            "stratum_success_rates": {
                s: stratum_successes[s] / stratum_counts[s]
                   if stratum_counts[s] > 0 else 0.0
                for s in stratum_counts
            }
        }

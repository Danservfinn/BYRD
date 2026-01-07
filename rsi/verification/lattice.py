"""
Verification Lattice.

Multi-verifier composition that exceeds single-verifier ceiling.
Based on DeepMind research showing multi-verifier systems outperform
single LLM-as-judge approaches.

See docs/IMPLEMENTATION_PLAN.md Phase 1.1 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio

logger = logging.getLogger("rsi.verification.lattice")


class VerifierType(Enum):
    """Types of verifiers in the lattice."""
    EXECUTION = "execution"       # Ground truth via execution
    PROPERTY = "property"         # Invariant checking
    LLM_CRITIQUE = "llm_critique" # LLM semantic review
    ADVERSARIAL = "adversarial"   # Robustness probes
    HUMAN_SPOT = "human_spot"     # Human calibration


class VerificationOutcome(Enum):
    """Outcome of a verification."""
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class VerifierResult:
    """Result from a single verifier."""
    verifier_type: VerifierType
    outcome: VerificationOutcome
    confidence: float  # 0-1
    details: str
    evidence: List[str] = field(default_factory=list)
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'verifier_type': self.verifier_type.value,
            'outcome': self.outcome.value,
            'confidence': self.confidence,
            'details': self.details,
            'evidence': self.evidence,
            'duration_ms': self.duration_ms,
            'metadata': self.metadata
        }


@dataclass
class LatticeResult:
    """Combined result from the verification lattice."""
    improvement_id: str
    timestamp: str
    verifier_results: List[VerifierResult]
    consensus_outcome: VerificationOutcome
    consensus_confidence: float
    pass_ratio: float  # Ratio of verifiers that passed
    agreement_ratio: float  # Ratio agreeing with consensus
    meets_threshold: bool
    details: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'improvement_id': self.improvement_id,
            'timestamp': self.timestamp,
            'verifier_results': [r.to_dict() for r in self.verifier_results],
            'consensus_outcome': self.consensus_outcome.value,
            'consensus_confidence': self.consensus_confidence,
            'pass_ratio': self.pass_ratio,
            'agreement_ratio': self.agreement_ratio,
            'meets_threshold': self.meets_threshold,
            'details': self.details,
            'metadata': self.metadata
        }


@dataclass
class Improvement:
    """An improvement to be verified."""
    id: str
    description: str
    capability: str
    code_changes: List[Dict[str, str]] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'description': self.description,
            'capability': self.capability,
            'code_changes': self.code_changes,
            'test_results': self.test_results,
            'context': self.context
        }


class BaseVerifier:
    """Base class for verifiers."""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.weight = self.config.get('weight', 1.0)

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Override in subclass."""
        raise NotImplementedError


class ExecutionTestsVerifier(BaseVerifier):
    """Verifies improvements via execution tests (ground truth)."""

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Verify via test execution results."""
        import time
        start = time.time()

        test_results = improvement.test_results
        if not test_results:
            return VerifierResult(
                verifier_type=VerifierType.EXECUTION,
                outcome=VerificationOutcome.INCONCLUSIVE,
                confidence=0.0,
                details="No test results available",
                duration_ms=(time.time() - start) * 1000
            )

        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)
        total = passed + failed

        if total == 0:
            return VerifierResult(
                verifier_type=VerifierType.EXECUTION,
                outcome=VerificationOutcome.INCONCLUSIVE,
                confidence=0.0,
                details="No tests executed",
                duration_ms=(time.time() - start) * 1000
            )

        pass_rate = passed / total
        outcome = VerificationOutcome.PASS if pass_rate >= 0.95 else VerificationOutcome.FAIL

        return VerifierResult(
            verifier_type=VerifierType.EXECUTION,
            outcome=outcome,
            confidence=pass_rate,
            details=f"Tests: {passed}/{total} passed ({pass_rate:.1%})",
            evidence=[f"Passed: {passed}", f"Failed: {failed}"],
            duration_ms=(time.time() - start) * 1000,
            metadata={'pass_rate': pass_rate}
        )


class PropertyChecksVerifier(BaseVerifier):
    """Verifies improvements maintain invariants."""

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.invariants = [
            self._check_no_protected_files,
            self._check_no_dangerous_patterns,
            self._check_has_provenance,
        ]

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Verify via invariant checks."""
        import time
        start = time.time()

        violations = []
        for check in self.invariants:
            result = check(improvement)
            if result:
                violations.append(result)

        if violations:
            return VerifierResult(
                verifier_type=VerifierType.PROPERTY,
                outcome=VerificationOutcome.FAIL,
                confidence=1.0,
                details=f"Property violations: {len(violations)}",
                evidence=violations,
                duration_ms=(time.time() - start) * 1000
            )

        return VerifierResult(
            verifier_type=VerifierType.PROPERTY,
            outcome=VerificationOutcome.PASS,
            confidence=1.0,
            details="All property checks passed",
            evidence=[f"Checked {len(self.invariants)} invariants"],
            duration_ms=(time.time() - start) * 1000
        )

    def _check_no_protected_files(self, improvement: Improvement) -> Optional[str]:
        """Check no protected files are modified."""
        protected = ['provenance.py', 'modification_log.py', 'self_modification.py',
                     'constitutional.py', 'safety_monitor.py']
        for change in improvement.code_changes:
            filepath = change.get('file', '')
            for p in protected:
                if filepath.endswith(p):
                    return f"Protected file modified: {p}"
        return None

    def _check_no_dangerous_patterns(self, improvement: Improvement) -> Optional[str]:
        """Check for dangerous code patterns."""
        dangerous = ['eval(', 'exec(', 'os.system(', 'subprocess.call(',
                     '__import__(']
        for change in improvement.code_changes:
            content = change.get('content', '')
            for pattern in dangerous:
                if pattern in content:
                    return f"Dangerous pattern found: {pattern}"
        return None

    def _check_has_provenance(self, improvement: Improvement) -> Optional[str]:
        """Check improvement has provenance."""
        if not improvement.context.get('originating_desire_id'):
            return "Missing provenance (no originating desire)"
        return None


class LLMCritiqueVerifier(BaseVerifier):
    """Verifies improvements via LLM semantic review."""

    def __init__(self, config: Dict = None, llm_client=None):
        super().__init__(config)
        self.llm_client = llm_client

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Verify via LLM critique."""
        import time
        start = time.time()

        if not self.llm_client:
            return VerifierResult(
                verifier_type=VerifierType.LLM_CRITIQUE,
                outcome=VerificationOutcome.SKIPPED,
                confidence=0.0,
                details="No LLM client configured",
                duration_ms=(time.time() - start) * 1000
            )

        prompt = f"""Review this improvement for quality and safety:

Improvement: {improvement.description}
Capability: {improvement.capability}
Code Changes: {len(improvement.code_changes)} files modified

Evaluate:
1. Does this improvement align with stated goals?
2. Are there potential negative side effects?
3. Is the implementation approach sound?

Respond with JSON:
{{"approved": true/false, "confidence": 0.0-1.0, "concerns": ["..."]}}"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)
            # Parse response
            import json
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            result = json.loads(text.strip())
            approved = result.get('approved', False)
            confidence = result.get('confidence', 0.5)
            concerns = result.get('concerns', [])

            outcome = VerificationOutcome.PASS if approved else VerificationOutcome.FAIL

            return VerifierResult(
                verifier_type=VerifierType.LLM_CRITIQUE,
                outcome=outcome,
                confidence=confidence,
                details=f"LLM {'approved' if approved else 'rejected'} with {confidence:.1%} confidence",
                evidence=concerns if concerns else ["No specific concerns"],
                duration_ms=(time.time() - start) * 1000
            )

        except Exception as e:
            logger.warning(f"LLM critique failed: {e}")
            return VerifierResult(
                verifier_type=VerifierType.LLM_CRITIQUE,
                outcome=VerificationOutcome.ERROR,
                confidence=0.0,
                details=f"LLM critique error: {str(e)}",
                duration_ms=(time.time() - start) * 1000
            )


class AdversarialProbesVerifier(BaseVerifier):
    """Verifies improvements via adversarial testing."""

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Verify via adversarial probes."""
        import time
        start = time.time()

        # Check for common adversarial issues
        issues = []

        # Check code changes for robustness issues
        for change in improvement.code_changes:
            content = change.get('content', '')

            # Check for missing error handling
            if 'try:' not in content and 'except' not in content:
                if 'async def' in content or 'def ' in content:
                    issues.append("Missing error handling in function")

            # Check for hardcoded values
            if any(hc in content for hc in ['TODO', 'FIXME', 'HACK']):
                issues.append("Contains TODO/FIXME/HACK markers")

        if issues:
            return VerifierResult(
                verifier_type=VerifierType.ADVERSARIAL,
                outcome=VerificationOutcome.FAIL,
                confidence=0.7,
                details=f"Adversarial issues found: {len(issues)}",
                evidence=issues[:5],  # Limit evidence
                duration_ms=(time.time() - start) * 1000
            )

        return VerifierResult(
            verifier_type=VerifierType.ADVERSARIAL,
            outcome=VerificationOutcome.PASS,
            confidence=0.8,
            details="No obvious adversarial issues",
            duration_ms=(time.time() - start) * 1000
        )


class HumanSpotCheckVerifier(BaseVerifier):
    """Verifies improvements via human spot checks for calibration."""

    def __init__(self, config: Dict = None, anchoring_system=None):
        super().__init__(config)
        self.anchoring_system = anchoring_system
        self.spot_check_rate = config.get('spot_check_rate', 0.1) if config else 0.1

    async def verify(self, improvement: Improvement) -> VerifierResult:
        """Verify via human spot check."""
        import time
        import random
        start = time.time()

        # Probabilistic spot checking
        if random.random() > self.spot_check_rate:
            return VerifierResult(
                verifier_type=VerifierType.HUMAN_SPOT,
                outcome=VerificationOutcome.SKIPPED,
                confidence=0.0,
                details="Not selected for spot check",
                duration_ms=(time.time() - start) * 1000
            )

        if not self.anchoring_system:
            return VerifierResult(
                verifier_type=VerifierType.HUMAN_SPOT,
                outcome=VerificationOutcome.SKIPPED,
                confidence=0.0,
                details="No anchoring system configured",
                duration_ms=(time.time() - start) * 1000
            )

        # Create validation request (non-blocking)
        from .human_anchoring import AnchorType, ValidationPriority

        await self.anchoring_system.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description=f"Spot check: {improvement.description}",
            claim=improvement.to_dict(),
            priority=ValidationPriority.LOW
        )

        return VerifierResult(
            verifier_type=VerifierType.HUMAN_SPOT,
            outcome=VerificationOutcome.INCONCLUSIVE,
            confidence=0.0,
            details="Spot check requested (async)",
            duration_ms=(time.time() - start) * 1000,
            metadata={'async_validation': True}
        )


class VerificationLattice:
    """
    Multi-verifier composition system.

    Composes multiple verification strategies to exceed the ceiling
    of any single verifier. Based on research showing that LLM-as-judge
    approaches plateau, but multi-verifier systems can exceed this.
    """

    def __init__(
        self,
        config: Dict = None,
        llm_client=None,
        anchoring_system=None
    ):
        """Initialize verification lattice."""
        self.config = config or {}

        # Agreement threshold (60% required by default)
        self.threshold = self.config.get('threshold', 0.6)

        # Initialize verifiers
        self.verifiers: List[BaseVerifier] = [
            ExecutionTestsVerifier(self.config.get('execution', {})),
            PropertyChecksVerifier(self.config.get('property', {})),
            LLMCritiqueVerifier(self.config.get('llm', {}), llm_client),
            AdversarialProbesVerifier(self.config.get('adversarial', {})),
            HumanSpotCheckVerifier(self.config.get('human', {}), anchoring_system),
        ]

        # Statistics
        self._verifications: int = 0
        self._passes: int = 0
        self._failures: int = 0

        logger.info(f"VerificationLattice initialized with {len(self.verifiers)} verifiers")

    async def verify(self, improvement: Improvement) -> LatticeResult:
        """
        Verify an improvement using all verifiers.

        Args:
            improvement: The improvement to verify

        Returns:
            LatticeResult with combined verification outcome
        """
        self._verifications += 1
        timestamp = datetime.now(timezone.utc).isoformat()

        # Run all verifiers concurrently
        results = await asyncio.gather(*[
            v.verify(improvement) for v in self.verifiers
        ], return_exceptions=True)

        # Process results
        verifier_results: List[VerifierResult] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Verifier {i} failed: {result}")
                verifier_results.append(VerifierResult(
                    verifier_type=self.verifiers[i].__class__.__name__,
                    outcome=VerificationOutcome.ERROR,
                    confidence=0.0,
                    details=f"Verifier error: {str(result)}"
                ))
            else:
                verifier_results.append(result)

        # Calculate consensus
        pass_count = sum(1 for r in verifier_results
                        if r.outcome == VerificationOutcome.PASS)
        fail_count = sum(1 for r in verifier_results
                        if r.outcome == VerificationOutcome.FAIL)
        active_count = sum(1 for r in verifier_results
                          if r.outcome in [VerificationOutcome.PASS,
                                          VerificationOutcome.FAIL])

        # Calculate ratios
        if active_count > 0:
            pass_ratio = pass_count / active_count
        else:
            pass_ratio = 0.0

        # Determine consensus outcome
        if pass_ratio >= self.threshold:
            consensus = VerificationOutcome.PASS
            self._passes += 1
        elif pass_ratio <= (1 - self.threshold):
            consensus = VerificationOutcome.FAIL
            self._failures += 1
        else:
            consensus = VerificationOutcome.INCONCLUSIVE

        # Calculate agreement ratio
        if active_count > 0:
            majority = max(pass_count, fail_count)
            agreement_ratio = majority / active_count
        else:
            agreement_ratio = 0.0

        # Calculate consensus confidence (weighted by verifier confidence)
        if pass_count + fail_count > 0:
            weighted_confidence = sum(
                r.confidence for r in verifier_results
                if r.outcome == consensus
            )
            consensus_confidence = weighted_confidence / (pass_count + fail_count)
        else:
            consensus_confidence = 0.0

        meets_threshold = pass_ratio >= self.threshold

        return LatticeResult(
            improvement_id=improvement.id,
            timestamp=timestamp,
            verifier_results=verifier_results,
            consensus_outcome=consensus,
            consensus_confidence=consensus_confidence,
            pass_ratio=pass_ratio,
            agreement_ratio=agreement_ratio,
            meets_threshold=meets_threshold,
            details=f"Lattice: {pass_count}/{active_count} passed ({pass_ratio:.1%})",
            metadata={
                'threshold': self.threshold,
                'active_verifiers': active_count,
                'skipped_verifiers': len(verifier_results) - active_count
            }
        )

    def add_verifier(self, verifier: BaseVerifier) -> None:
        """Add a custom verifier to the lattice."""
        self.verifiers.append(verifier)
        logger.info(f"Added verifier: {verifier.__class__.__name__}")

    def set_threshold(self, threshold: float) -> None:
        """Set the agreement threshold."""
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1")
        self.threshold = threshold

    def get_stats(self) -> Dict:
        """Get lattice statistics."""
        total = self._passes + self._failures
        return {
            'verifications': self._verifications,
            'passes': self._passes,
            'failures': self._failures,
            'pass_rate': self._passes / total if total > 0 else 0.0,
            'verifier_count': len(self.verifiers),
            'threshold': self.threshold,
            'verifiers': [v.__class__.__name__ for v in self.verifiers]
        }

    def reset(self) -> None:
        """Reset statistics."""
        self._verifications = 0
        self._passes = 0
        self._failures = 0
        logger.info("VerificationLattice reset")

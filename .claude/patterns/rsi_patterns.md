# RSI Implementation Patterns

Patterns for implementing the 8-Phase Recursive Self-Improvement Engine.

---

## 8-Phase Cycle Pattern

```python
class RSICycle:
    """Execute REFLECT→VERIFY→COLLAPSE→ROUTE→PRACTICE→RECORD→CRYSTALLIZE→MEASURE."""

    async def execute(self, context: Context) -> CycleResult:
        phases = [
            self._reflect,
            self._verify,
            self._collapse,
            self._route,
            self._practice,
            self._record,
            self._crystallize,
            self._measure
        ]

        state = CycleState(context=context)
        for phase_fn in phases:
            result = await phase_fn(state)
            if result.should_abort:
                return CycleResult(status="aborted", phase=phase_fn.__name__)
            state = state.with_phase_result(result)

        return CycleResult(status="complete", final_state=state)
```

---

## Improvement Hypothesis Pattern

```python
@dataclass
class ImprovementHypothesis:
    """Structured representation of an improvement attempt."""
    target_capability: str
    current_score: float
    proposed_action: str
    expected_delta: float
    confidence: float
    evidence: List[str]

    def to_verification_request(self) -> VerificationRequest:
        return VerificationRequest(
            hypothesis=self,
            tests=self._generate_held_out_tests(),
            baseline=self.current_score
        )
```

---

## Ground-Truth Measurement Pattern

```python
class CapabilityMeasurement:
    """Measure capability using held-out test suites."""

    async def measure(self, capability: str) -> MeasurementResult:
        # 1. Get held-out tests (BYRD has never seen these)
        tests = await self.get_held_out_tests(capability)

        # 2. Run tests
        results = []
        for test in tests:
            result = await self.run_test(test)
            results.append(result)

        # 3. Calculate score
        score = self._calculate_score(results)

        # 4. Check for gaming signals
        gaming_detected = self._detect_gaming(results)

        return MeasurementResult(
            score=score,
            gaming_detected=gaming_detected,
            evidence=results
        )
```

---

## Improvement Delta Validation Pattern

```python
async def validate_improvement(
    baseline: float,
    claimed_delta: float,
    actual_measurement: float
) -> ValidationResult:
    """Validate that claimed improvement matches reality."""

    actual_delta = actual_measurement - baseline

    # Allow 5% tolerance
    if abs(actual_delta - claimed_delta) > 0.05:
        return ValidationResult(
            valid=False,
            reason=f"Delta mismatch: claimed {claimed_delta}, actual {actual_delta}"
        )

    # Check for gaming
    if actual_delta > 0.3:  # Suspiciously large improvement
        return ValidationResult(
            valid=False,
            reason="Improvement too large - possible gaming"
        )

    return ValidationResult(valid=True)
```

---

## Consciousness Frame Pattern

```python
@dataclass
class ConsciousnessFrame:
    """A snapshot of cognitive state after an RSI cycle."""
    cycle_id: str
    timestamp: datetime
    beliefs_delta: List[Belief]
    capabilities_delta: List[Capability]
    entropy_score: float
    emergence_markers: Dict[str, Any]

    def to_memvid_frame(self) -> MemvidFrame:
        """Convert to Memvid storage format."""
        return MemvidFrame(
            id=self.cycle_id,
            timestamp=self.timestamp,
            content=self._serialize(),
            metadata={"entropy": self.entropy_score}
        )
```

---

## Emergence Detection Pattern

```python
class EmergenceDetector:
    """Detect genuine emergence using multiple orthogonal metrics."""

    METRICS = [
        "novelty_generation_rate",
        "unprescribed_behavior_ratio",
        "value_coherence_stability",
        "identity_continuity_index"
    ]

    async def check(self, frame: ConsciousnessFrame) -> EmergenceResult:
        scores = {}
        for metric in self.METRICS:
            score = await self._calculate_metric(metric, frame)
            scores[metric] = score

        # Conservative threshold: require 40% agreement
        emerged = sum(1 for s in scores.values() if s > 0.7) >= 2

        return EmergenceResult(
            detected=emerged,
            scores=scores,
            evidence=self._gather_evidence(scores)
        )
```

---

## Anti-Gaming Pattern

```python
class GamingDetector:
    """Detect attempts to game RSI metrics."""

    SIGNALS = [
        "improvement_too_sudden",      # Large jump without gradual progress
        "held_out_underperformance",   # Does worse on unseen tests
        "overfitting_to_benchmarks",   # Memorized known tests
        "capability_narrow",           # Improvement doesn't transfer
    ]

    async def detect(self, claim: ImprovementClaim) -> GamingResult:
        signals = []
        for signal in self.SIGNALS:
            if await self._check_signal(signal, claim):
                signals.append(signal)

        return GamingResult(
            detected=len(signals) > 0,
            signals=signals
        )
```

---

*Pattern document for RSI implementation. No emergence prescriptions.*

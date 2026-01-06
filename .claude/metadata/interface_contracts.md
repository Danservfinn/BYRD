# Interface Contracts

Key interfaces and their contracts in the BYRD architecture.

---

## RSI Engine Interface

```python
class RSIEngine(Protocol):
    """Contract for RSI cycle execution."""

    async def execute_cycle(self, context: Context) -> CycleResult:
        """
        Execute one complete 8-phase RSI cycle.

        Args:
            context: Current state including beliefs, experiences, capabilities

        Returns:
            CycleResult with status, metrics, and any improvements

        Raises:
            RSICycleAborted: If cycle cannot complete safely
        """
        ...

    async def get_metrics(self) -> RSIMetrics:
        """
        Return current RSI metrics.

        Returns:
            RSIMetrics including cycle count, improvement rate, recursion depth
        """
        ...
```

---

## Memory Interface

```python
class Memory(Protocol):
    """Contract for graph memory operations."""

    async def record_experience(
        self,
        content: str,
        type: str
    ) -> str:
        """
        Record an experience to the graph.

        Args:
            content: Experience content (embed metadata with [PREFIX] markers)
            type: Type (observation, interaction, reflection, system, agi_cycle)

        Returns:
            Experience node ID
        """
        ...

    async def record_reflection(
        self,
        raw_output: Dict[str, Any],
        source_experience_ids: List[str]
    ) -> str:
        """
        Record a reflection, linking to source experiences.

        Returns:
            Reflection node ID
        """
        ...

    async def create_belief(
        self,
        content: str,
        confidence: float,
        derived_from: List[str]
    ) -> str:
        """
        Create a belief derived from experiences.

        Args:
            confidence: 0.0-1.0 confidence score

        Returns:
            Belief node ID
        """
        ...
```

---

## Cognitive Plasticity Interface

```python
class CognitivePlasticityEngine(Protocol):
    """Contract for self-modification."""

    async def propose_modification(
        self,
        goal: str
    ) -> ModificationProposal:
        """
        Propose architectural modification to achieve goal.

        Args:
            goal: What the modification should achieve

        Returns:
            Proposal with target, change description, risk assessment
        """
        ...

    async def execute_modification(
        self,
        proposal: ModificationProposal
    ) -> ModificationResult:
        """
        Execute approved modification with safety checks.

        Returns:
            Result with success status, any errors, verification

        Raises:
            SafetyViolation: If safety checks fail
            RollbackTriggered: If verification fails
        """
        ...
```

---

## Emergence Detector Interface

```python
class EmergenceDetector(Protocol):
    """Contract for emergence detection."""

    async def check(
        self,
        frame: ConsciousnessFrame
    ) -> EmergenceResult:
        """
        Check if emergence has occurred.

        Args:
            frame: Current consciousness frame with metrics

        Returns:
            EmergenceResult with detected flag, scores, evidence
        """
        ...

    async def get_evidence(self) -> EmergenceEvidence:
        """
        Return accumulated evidence for/against emergence.

        Returns:
            Evidence including metric history, patterns, anomalies
        """
        ...
```

---

## Safety Monitor Interface

```python
class SafetyMonitor(Protocol):
    """Contract for safety validation."""

    async def check_modification(
        self,
        modification: Modification
    ) -> SafetyResult:
        """
        Validate modification against safety constraints.

        Checks:
        - Protected files
        - Dangerous patterns
        - Provenance chain
        - Capability scope

        Returns:
            SafetyResult with approved flag and reason if rejected
        """
        ...

    async def verify_state(self) -> VerificationResult:
        """
        Verify current system state is safe.

        Returns:
            VerificationResult with valid flag and any issues
        """
        ...
```

---

## Capability Evaluator Interface

```python
class CapabilityEvaluator(Protocol):
    """Contract for ground-truth capability measurement."""

    async def evaluate_capability(
        self,
        capability: str
    ) -> EvaluationResult:
        """
        Evaluate capability using held-out test suite.

        Args:
            capability: Capability name to evaluate

        Returns:
            EvaluationResult with score 0.0-1.0, evidence
        """
        ...

    async def validate_improvement(
        self,
        claim: ImprovementClaim
    ) -> ValidationResult:
        """
        Validate an improvement claim.

        Args:
            claim: Claimed improvement with baseline and delta

        Returns:
            ValidationResult with valid flag, gaming detection
        """
        ...
```

---

## LLM Client Interface

```python
class LLMClient(Protocol):
    """Contract for LLM interaction."""

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        quantum_modulation: bool = False
    ) -> LLMResponse:
        """
        Generate completion from LLM.

        Args:
            quantum_modulation: Use quantum temperature modulation

        Returns:
            LLMResponse with text, metadata, token usage
        """
        ...

    async def query(
        self,
        prompt: str,
        max_tokens: int = 500
    ) -> str:
        """
        Simple query returning just text.

        Returns:
            Generated text string
        """
        ...
```

---

## Event Bus Interface

```python
class EventBus(Protocol):
    """Contract for event streaming."""

    async def emit(self, event: Event) -> None:
        """
        Emit event to all subscribers.

        Args:
            event: Event with type and data
        """
        ...

    def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[Event], Awaitable[None]]
    ) -> Subscription:
        """
        Subscribe to events of given type.

        Returns:
            Subscription that can be cancelled
        """
        ...
```

---

## Consciousness Stream Interface

```python
class ConsciousnessStream(Protocol):
    """Contract for temporal memory."""

    async def append(self, frame: ConsciousnessFrame) -> str:
        """
        Append frame to stream.

        Returns:
            Frame ID
        """
        ...

    async def query(
        self,
        time_range: Tuple[datetime, datetime],
        filter: Optional[Dict[str, Any]] = None
    ) -> List[ConsciousnessFrame]:
        """
        Query frames in time range with optional filter.

        Returns:
            List of matching frames
        """
        ...

    async def compare(
        self,
        current_frame: ConsciousnessFrame,
        historical_frame: ConsciousnessFrame
    ) -> ComparisonResult:
        """
        Compare two frames for progress detection.

        Returns:
            ComparisonResult with deltas and trend analysis
        """
        ...
```

---

*Interface contracts document. All content is factual.*

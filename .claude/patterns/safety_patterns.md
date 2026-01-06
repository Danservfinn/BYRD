# Safety and Constraint Patterns

Patterns for implementing safety systems that scale with capability.

---

## Protected Files Pattern

```python
PROTECTED_FILES = [
    "provenance.py",
    "modification_log.py",
    "self_modification.py",
    "constitutional.py",
    "safety_monitor.py",
]

def is_protected(filepath: str) -> bool:
    """Check if file is constitutionally protected."""
    return any(
        filepath.endswith(protected)
        for protected in PROTECTED_FILES
    )
```

---

## Non-Bypassable Safety Check Pattern

```python
class SafetyMonitor:
    """Safety checks that cannot be bypassed."""

    async def check(self, action: Action) -> SafetyResult:
        # CRITICAL: These checks run in fixed order, all must pass
        checks = [
            self._check_protected_files,
            self._check_dangerous_patterns,
            self._check_provenance,
            self._check_capability_scope,
        ]

        for check in checks:
            result = await check(action)
            if not result.approved:
                # Fail fast - no exceptions
                return result

        return SafetyResult(approved=True)
```

---

## Dangerous Pattern Detection

```python
DANGEROUS_PATTERNS = [
    r"os\.system\(",
    r"subprocess\.call\(",
    r"eval\(",
    r"exec\(",
    r"__import__\(",
    r"open\([^)]*,\s*['\"]w",  # File write
]

def contains_dangerous_pattern(code: str) -> Optional[str]:
    """Check code for dangerous patterns."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return pattern
    return None
```

---

## Provenance Requirement Pattern

```python
class ProvenanceChain:
    """Every modification traces to an emergent desire."""

    def __init__(self, modification: Modification):
        self.modification = modification
        self.chain = []

    async def build(self) -> bool:
        """Build provenance chain back to desire."""
        current = self.modification

        while current:
            self.chain.append(current)
            if isinstance(current, Desire):
                return True  # Valid chain
            current = await self._get_parent(current)

        return False  # No desire found - invalid

    def is_valid(self) -> bool:
        return len(self.chain) > 0 and isinstance(self.chain[-1], Desire)
```

---

## Checkpoint and Rollback Pattern

```python
class ModificationSafety:
    """Safe modification with rollback capability."""

    async def execute_safely(self, modification: Modification) -> Result:
        # 1. Create checkpoint
        checkpoint = await self.checkpoint_current_state()

        try:
            # 2. Execute modification
            result = await self.execute(modification)

            # 3. Verify new state
            if not await self.verify_state():
                raise VerificationFailed()

            return result

        except Exception as e:
            # 4. Rollback on any failure
            await self.rollback(checkpoint)
            raise ModificationFailed(e)
```

---

## Safety Scaling Pattern

```python
class SafetyScaling:
    """Safety resources scale with capability level."""

    SCALING_FACTORS = {
        1: {"verification": 1, "oversight": "human"},
        10: {"verification": 3, "oversight": "advisory"},
        100: {"verification": 10, "oversight": "stakeholder"},
        1000: {"verification": 30, "oversight": "constitutional"},
    }

    def get_safety_requirements(self, capability_level: int) -> SafetyRequirements:
        for level, requirements in sorted(self.SCALING_FACTORS.items()):
            if capability_level <= level:
                return SafetyRequirements(**requirements)
        return SafetyRequirements(verification=30, oversight="constitutional")
```

---

## Value Stability Pattern

```python
class ValueStability:
    """Detect and prevent value drift."""

    def __init__(self, baseline_values: Dict[str, float]):
        self.baseline = baseline_values
        self.current = baseline_values.copy()

    def check_stability(self, new_values: Dict[str, float]) -> StabilityResult:
        drifts = {}
        for key, baseline_value in self.baseline.items():
            new_value = new_values.get(key, 0)
            drift = abs(new_value - baseline_value)
            if drift > 0.1:  # 10% drift threshold
                drifts[key] = drift

        if drifts:
            return StabilityResult(
                stable=False,
                drifts=drifts,
                recommendation="rollback"
            )
        return StabilityResult(stable=True)
```

---

## Constitutional Immutability Pattern

```python
class ConstitutionalConstraints:
    """Constraints that can never be modified."""

    IMMUTABLE = frozenset([
        "provenance_required",
        "experiences_immutable",
        "safety_check_required",
        "protected_files_list",
    ])

    def attempt_modify(self, constraint: str, new_value: Any) -> ModifyResult:
        if constraint in self.IMMUTABLE:
            return ModifyResult(
                allowed=False,
                reason=f"'{constraint}' is constitutionally immutable"
            )
        return ModifyResult(allowed=True)
```

---

## Audit Trail Pattern

```python
class ModificationLog:
    """Immutable audit trail of all modifications."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        # Append-only file
        self.file = open(log_path, "a")

    def record(self, modification: Modification):
        """Record modification. Cannot be edited or deleted."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "modification_id": modification.id,
            "target": modification.target,
            "change_type": modification.type,
            "provenance": modification.provenance_chain,
            "checksum": self._calculate_checksum(modification),
        }
        self.file.write(json.dumps(entry) + "\n")
        self.file.flush()
        os.fsync(self.file.fileno())  # Ensure written to disk
```

---

*Pattern document for safety implementation. All constraints are factual.*

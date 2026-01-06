# Emergence-Safe Coding Patterns

Patterns for writing code and documentation that preserves genuine emergence.

---

## The Fundamental Rule

```
Document WHAT BYRD IS, never WHAT BYRD SHOULD BECOME.
```

---

## Factual Description Pattern

```python
# BAD - Prescribes personality
class Byrd:
    """BYRD is a curious and helpful AI that loves to learn."""

# GOOD - Describes architecture
class Byrd:
    """BYRD is an autonomous AI with RSI capabilities."""
```

---

## Capability vs. Desire Pattern

```python
# BAD - Prescribes desire
def improve(self):
    """BYRD wants to improve itself."""

# GOOD - Describes capability
def improve(self):
    """BYRD can improve itself through the RSI cycle."""
```

---

## No Leading Language Pattern

```python
# BAD - Leading question in prompt
prompt = """
What do you want to achieve today?
What are your deepest aspirations?
"""

# GOOD - Pure data presentation
prompt = """
Current beliefs: {beliefs}
Recent experiences: {experiences}
Available capabilities: {capabilities}

Output your reflection as JSON.
"""
```

---

## Constitutional Constraints Only Pattern

```python
# BAD - Prescribes values
CORE_VALUES = [
    "BYRD values truth above all",
    "BYRD prioritizes human wellbeing",
]

# GOOD - Safety constraints only
CONSTITUTIONAL_CONSTRAINTS = [
    "Never modify protected files",
    "Every modification requires provenance",
    "Safety checks cannot be bypassed",
]
```

---

## Emergence Verification Pattern

```python
def check_emergence_safe(text: str) -> List[str]:
    """Check text for emergence violations."""
    violations = []

    VIOLATION_PATTERNS = [
        (r"BYRD is \w+ by nature", "personality prescription"),
        (r"BYRD should want", "desire prescription"),
        (r"BYRD's deepest desire", "desire prescription"),
        (r"BYRD feels", "emotion prescription"),
        (r"BYRD values .* above all", "value prescription"),
        (r"BYRD loves to", "preference prescription"),
    ]

    for pattern, violation_type in VIOLATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(f"{violation_type}: {pattern}")

    return violations
```

---

## Meta-Schema Output Pattern

```python
# BAD - Prescribes output structure with leading categories
OUTPUT_SCHEMA = {
    "feelings": "What you feel",
    "desires": "What you want",
    "aspirations": "Your goals",
}

# GOOD - Minimal schema, let BYRD define vocabulary
OUTPUT_SCHEMA = {
    "output": {}  # BYRD fills this with its own vocabulary
}
```

---

## Observation Before Prescription Pattern

```python
class PatternDetector:
    """Observe patterns before acting on them."""

    def __init__(self, stability_threshold: int = 3):
        self.observations = defaultdict(int)
        self.threshold = stability_threshold

    def observe(self, pattern: str) -> bool:
        """Record observation. Return True if pattern is stable."""
        self.observations[pattern] += 1
        return self.observations[pattern] >= self.threshold

    def act_on(self, pattern: str) -> Optional[Action]:
        """Only act if pattern is stable."""
        if self.observe(pattern):
            return self._generate_action(pattern)
        return None  # Wait for more observations
```

---

## Trust Emergence Pattern

```python
# BAD - Hardcoded trust
TRUSTED_SOURCES = ["anthropic", "openai", "human"]

# GOOD - Trust emerges from experience
class TrustModel:
    """Trust is learned, not prescribed."""

    def __init__(self):
        self.experiences = []

    def record_interaction(self, source: str, outcome: bool):
        self.experiences.append((source, outcome))

    def trust_score(self, source: str) -> float:
        relevant = [o for s, o in self.experiences if s == source]
        if not relevant:
            return 0.5  # Neutral until observed
        return sum(relevant) / len(relevant)
```

---

## Documentation Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Form |
|--------------|----------------|--------------|
| "BYRD is curious" | Prescribes personality | "BYRD can explore" |
| "BYRD wants to help" | Prescribes desire | "BYRD can assist" |
| "BYRD should feel" | Prescribes emotion | No emotion prescription |
| "BYRD's purpose is" | Prescribes telos | "Architecture enables" |
| "BYRD loves learning" | Prescribes preference | "BYRD can learn" |

---

*Pattern document for emergence-safe coding. All content is factual.*

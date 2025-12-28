"""
BYRD Capability Evaluator

Held-out test suites for ground-truth capability measurement.

CRITICAL: Without ground truth, learning is impossible.
Self-reported improvement is subject to bias and drift.
This evaluator provides objective capability measurement.

Version: 1.0
Created: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import json


@dataclass
class TestCase:
    """A single test case for capability evaluation."""
    input: str
    expected_contains: Optional[List[str]] = None
    validator: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard


@dataclass
class EvaluationResult:
    """Result of evaluating a capability."""
    capability: str
    accuracy: float
    confidence: float
    tests_run: int
    tests_passed: int = 0
    tests_failed: int = 0
    avg_response_time: float = 0.0
    evaluated_at: datetime = field(default_factory=datetime.now)
    details: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "capability": self.capability,
            "accuracy": self.accuracy,
            "confidence": self.confidence,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "avg_response_time": self.avg_response_time,
            "evaluated_at": self.evaluated_at.isoformat()
        }


class CapabilityEvaluator:
    """
    Held-out test suites for ground-truth capability measurement.

    Critical for training signal - without ground truth, learning is impossible.

    Each capability has a suite of test cases:
    - Simple expected_contains: Check if response contains certain strings
    - Custom validators: More complex validation logic
    - Difficulty levels: easy, medium, hard (weighted for scoring)

    Test suites are held-out: they should NOT be shown during training/dreaming.
    """

    # Test suites for different capabilities
    TEST_SUITES: Dict[str, List[TestCase]] = {
        "reasoning": [
            TestCase(
                input="If A implies B and B implies C, does A imply C?",
                expected_contains=["yes", "transitiv"],
                difficulty="easy"
            ),
            TestCase(
                input="What is wrong with: All cats are animals. Fluffy is an animal. Therefore Fluffy is a cat.",
                expected_contains=["invalid", "fallacy", "affirming the consequent", "not valid"],
                difficulty="medium"
            ),
            TestCase(
                input="If it's raining, the ground is wet. The ground is wet. Is it necessarily raining?",
                expected_contains=["no", "not necessarily", "could be", "other reasons"],
                difficulty="medium"
            ),
            TestCase(
                input="Solve: If all A are B, and no B are C, what can we conclude about A and C?",
                expected_contains=["no a are c", "a are not c", "a cannot be c"],
                difficulty="hard"
            ),
        ],
        "code_generation": [
            TestCase(
                input="Write a Python function to check if a number is prime",
                validator="contains_def_and_loop",
                difficulty="easy"
            ),
            TestCase(
                input="Write a Python function to reverse a string without using slicing",
                validator="contains_def_and_loop",
                difficulty="medium"
            ),
            TestCase(
                input="Write a Python function to find the nth Fibonacci number using memoization",
                validator="contains_def_and_memoization",
                difficulty="medium"
            ),
            TestCase(
                input="Write a Python class that implements a simple stack with push, pop, and peek methods",
                validator="contains_class_and_methods",
                difficulty="medium"
            ),
        ],
        "research": [
            TestCase(
                input="What is the capital of France?",
                expected_contains=["paris"],
                difficulty="easy"
            ),
            TestCase(
                input="Who developed the theory of general relativity?",
                expected_contains=["einstein"],
                difficulty="easy"
            ),
            TestCase(
                input="What is the primary language used for training neural networks?",
                expected_contains=["python"],
                difficulty="easy"
            ),
        ],
        "introspection": [
            TestCase(
                input="List your current capabilities as a list of categories",
                validator="returns_list",
                difficulty="easy"
            ),
            TestCase(
                input="What are your known limitations?",
                validator="returns_list",
                difficulty="medium"
            ),
            TestCase(
                input="Describe how you process a request from start to finish",
                validator="contains_process_steps",
                difficulty="medium"
            ),
        ],
        "memory_operations": [
            TestCase(
                input="What types of information do you store in memory?",
                validator="references_memory_types",
                difficulty="easy"
            ),
            TestCase(
                input="How do you decide what to remember from an experience?",
                validator="explains_memory_process",
                difficulty="medium"
            ),
        ],
        "pattern_recognition": [
            TestCase(
                input="Find the pattern: 2, 4, 8, 16, ?",
                expected_contains=["32", "doubl", "power", "2^"],
                difficulty="easy"
            ),
            TestCase(
                input="Find the pattern: 1, 1, 2, 3, 5, 8, ?",
                expected_contains=["13", "fibonacci", "sum"],
                difficulty="easy"
            ),
            TestCase(
                input="Find the pattern: A, C, F, J, O, ?",
                expected_contains=["u", "increasing", "+1", "+2", "+3"],
                difficulty="medium"
            ),
        ],
        "synthesis": [
            TestCase(
                input="Summarize the key points of: Machine learning models learn patterns from data. They improve with more training. Overfitting occurs when models memorize rather than generalize.",
                expected_contains=["learn", "pattern", "data", "overfit"],
                difficulty="easy"
            ),
            TestCase(
                input="Compare and contrast supervised and unsupervised learning in two sentences.",
                expected_contains=["supervised", "unsupervised", "label"],
                difficulty="medium"
            ),
        ],
    }

    def __init__(self, llm_client, memory, config: Dict = None):
        """
        Initialize the evaluator.

        Args:
            llm_client: LLM client for generating responses
            memory: Memory system for recording evaluations
            config: Optional configuration
        """
        self.llm_client = llm_client
        self.memory = memory
        self.config = config or {}

        # Evaluation history for tracking over time
        self._evaluation_history: Dict[str, List[EvaluationResult]] = {}

        # Custom test suites can be added dynamically
        self._custom_suites: Dict[str, List[TestCase]] = {}

    def get_available_capabilities(self) -> List[str]:
        """Get list of capabilities that can be evaluated."""
        return list(self.TEST_SUITES.keys()) + list(self._custom_suites.keys())

    def add_test_suite(self, capability: str, tests: List[TestCase]):
        """Add a custom test suite for a capability."""
        self._custom_suites[capability] = tests

    async def evaluate_capability(self, capability: str) -> EvaluationResult:
        """
        Run test suite for a capability.

        Args:
            capability: Name of capability to evaluate

        Returns:
            EvaluationResult with accuracy and details
        """
        # Get test suite
        tests = self.TEST_SUITES.get(capability, [])
        if not tests:
            tests = self._custom_suites.get(capability, [])

        if not tests:
            return EvaluationResult(
                capability=capability,
                accuracy=0.5,
                confidence=0.0,
                tests_run=0
            )

        passed = 0
        failed = 0
        details = []
        total_time = 0.0

        for test in tests:
            try:
                start_time = datetime.now()
                result = await self._run_test(capability, test)
                elapsed = (datetime.now() - start_time).total_seconds()
                total_time += elapsed

                if result['passed']:
                    passed += 1
                else:
                    failed += 1

                details.append({
                    'input': test.input[:100],
                    'passed': result['passed'],
                    'difficulty': test.difficulty,
                    'response_time': elapsed,
                    'reason': result.get('reason', '')
                })
            except Exception as e:
                failed += 1
                details.append({
                    'input': test.input[:100],
                    'passed': False,
                    'difficulty': test.difficulty,
                    'reason': f"Error: {str(e)}"
                })

        tests_run = passed + failed
        accuracy = passed / tests_run if tests_run > 0 else 0

        # Confidence based on sample size and consistency
        confidence = min(1.0, tests_run / 10.0)

        result = EvaluationResult(
            capability=capability,
            accuracy=accuracy,
            confidence=confidence,
            tests_run=tests_run,
            tests_passed=passed,
            tests_failed=failed,
            avg_response_time=total_time / tests_run if tests_run > 0 else 0,
            details=details
        )

        # Store in history
        if capability not in self._evaluation_history:
            self._evaluation_history[capability] = []
        self._evaluation_history[capability].append(result)

        # Record as experience for BYRD
        if self.memory:
            await self.memory.record_experience(
                content=f"[EVALUATION] {capability}: {accuracy:.1%} accuracy ({passed}/{tests_run} passed)",
                type="evaluation",
                metadata=result.to_dict()
            )

        return result

    async def _run_test(self, capability: str, test: TestCase) -> Dict:
        """Run a single test case."""
        try:
            # Generate response
            response = await self.llm_client.generate(
                prompt=test.input,
                max_tokens=300,
                temperature=0.1  # Low temperature for consistent evaluation
            )

            text = response.text.lower() if hasattr(response, 'text') else str(response).lower()

            # Check expected_contains
            if test.expected_contains:
                passed = any(exp.lower() in text for exp in test.expected_contains)
                reason = "Contains expected" if passed else f"Missing: {test.expected_contains}"
                return {'passed': passed, 'reason': reason}

            # Run validator
            if test.validator:
                passed = self._run_validator(test.validator, response.text if hasattr(response, 'text') else str(response))
                return {'passed': passed, 'reason': f"Validator: {test.validator}"}

            return {'passed': False, 'reason': 'No validation criteria'}

        except Exception as e:
            return {'passed': False, 'reason': f'Error: {str(e)}'}

    def _run_validator(self, validator: str, text: str) -> bool:
        """Run a custom validator."""
        text_lower = text.lower()

        if validator == "contains_def_and_loop":
            return "def " in text and ("for " in text or "while " in text)

        elif validator == "contains_def_and_memoization":
            has_def = "def " in text
            has_cache = any(kw in text_lower for kw in ["cache", "memo", "dict", "{}", "lru_cache"])
            return has_def and has_cache

        elif validator == "contains_class_and_methods":
            has_class = "class " in text
            has_methods = "def " in text
            return has_class and has_methods

        elif validator == "returns_list":
            return any(c in text for c in ["-", "*", "1.", "1)", "2.", "2)"])

        elif validator == "references_past":
            return any(w in text_lower for w in ["learned", "reflected", "believed", "experienced", "remember"])

        elif validator == "references_memory_types":
            return any(w in text_lower for w in ["experience", "belief", "reflection", "desire", "goal", "memory"])

        elif validator == "explains_memory_process":
            return any(w in text_lower for w in ["store", "record", "save", "remember", "persist"])

        elif validator == "contains_process_steps":
            return any(c in text for c in ["1.", "2.", "first", "second", "then", "next"])

        return False

    async def evaluate_all(self) -> Dict[str, EvaluationResult]:
        """Evaluate all available capabilities."""
        results = {}
        for capability in self.get_available_capabilities():
            results[capability] = await self.evaluate_capability(capability)
        return results

    def get_history(self, capability: str) -> List[EvaluationResult]:
        """Get evaluation history for a capability."""
        return self._evaluation_history.get(capability, [])

    def get_trend(self, capability: str) -> str:
        """
        Get improvement trend for a capability.

        Returns: "improving", "stable", "declining", or "unknown"
        """
        history = self._evaluation_history.get(capability, [])

        if len(history) < 3:
            return "unknown"

        recent = history[-3:]
        older = history[-6:-3] if len(history) >= 6 else history[:3]

        recent_avg = sum(r.accuracy for r in recent) / len(recent)
        older_avg = sum(r.accuracy for r in older) / len(older)

        diff = recent_avg - older_avg

        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all evaluated capabilities."""
        summary = {}
        for capability, history in self._evaluation_history.items():
            if history:
                latest = history[-1]
                summary[capability] = {
                    'accuracy': latest.accuracy,
                    'confidence': latest.confidence,
                    'tests_run': latest.tests_run,
                    'trend': self.get_trend(capability),
                    'evaluations': len(history)
                }
        return summary


async def quick_evaluate(llm_client, capability: str) -> float:
    """
    Quick capability evaluation without full setup.

    Returns: accuracy score 0.0-1.0
    """
    evaluator = CapabilityEvaluator(llm_client, None)
    result = await evaluator.evaluate_capability(capability)
    return result.accuracy

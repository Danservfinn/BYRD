"""
TDD Practice - Test-Driven Development practice for code domain.

Generates practice problems with tests FIRST, then attempts solutions.
This ensures we have an oracle (tests) to verify learning.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from collections import deque
import subprocess
import tempfile
import asyncio
import logging
import json
from pathlib import Path

logger = logging.getLogger("rsi.learning.tdd")


@dataclass
class PracticeProblem:
    """A practice problem with its test oracle."""
    spec: str
    oracle: str  # Test code
    domain: str
    difficulty: str


@dataclass
class PracticeResult:
    """Result of a practice attempt."""
    success: bool
    solution: str
    test_output: str
    tests_passed: int
    tests_total: int
    problem: str = ""
    approach: str = ""
    attempts: int = 1
    difficulty: str = "beginner"
    error: Optional[str] = None


class OracleGenerationError(Exception):
    """Raised when test oracle generation fails."""
    pass


class TDDPractice:
    """
    Test-Driven Development practice for code domain.

    1. Generate problem spec
    2. Generate tests FIRST (the oracle)
    3. Validate tests are syntactically correct
    4. Generate solution
    5. Run tests against solution
    6. Track difficulty and adapt
    """

    DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]
    DEFAULT_TIMEOUT = 30
    MAX_SOLUTION_ATTEMPTS = 2
    MAX_GENERATION_RETRIES = 3

    def __init__(self, llm_client, memory=None, config: Dict = None):
        """
        Initialize TDD practice.

        Args:
            llm_client: LLM client for generation
            memory: Optional memory for tracking
            config: Optional configuration
        """
        self.llm = llm_client
        self.memory = memory
        self.config = config or {}

        # Difficulty tracking per domain
        self._domain_difficulty: Dict[str, int] = {}

        # Problem cache for deduplication
        self._recent_problems: deque = deque(maxlen=20)

        # Configurable timeout
        self.timeout = self.config.get("practice_timeout", self.DEFAULT_TIMEOUT)

        # Stats
        self._attempts = 0
        self._successes = 0

    async def generate_practice(self, desire: Dict) -> Optional[PracticeProblem]:
        """
        Generate a practice problem with tests.

        Args:
            desire: The improvement desire

        Returns:
            PracticeProblem or None if generation fails
        """
        domain = desire.get("domain", "code")
        difficulty_idx = self._domain_difficulty.get(domain, 0)
        difficulty = self.DIFFICULTY_LEVELS[difficulty_idx]

        for attempt in range(self.MAX_GENERATION_RETRIES):
            try:
                # Step 1: Generate problem spec
                spec = await self._generate_spec(desire, difficulty)

                # Check for duplicates
                spec_hash = hash(spec[:100])
                if spec_hash in self._recent_problems:
                    spec = await self._generate_different_spec(desire, spec, difficulty)
                    spec_hash = hash(spec[:100])
                self._recent_problems.append(spec_hash)

                # Step 2: Generate tests FIRST (TDD style)
                tests = await self._generate_tests(spec, difficulty)

                # Step 3: Validate test syntax
                if not self._validate_syntax(tests):
                    logger.warning(f"Test syntax error, attempt {attempt + 1}")
                    continue

                return PracticeProblem(
                    spec=spec,
                    oracle=tests,
                    domain=domain,
                    difficulty=difficulty
                )

            except Exception as e:
                logger.error(f"Generation error on attempt {attempt + 1}: {e}")

        logger.error("Could not generate valid practice problem")
        return None

    async def _generate_spec(self, desire: Dict, difficulty: str) -> str:
        """Generate problem specification."""
        description = desire.get("description", "improve coding")

        prompt = f"""Create a {difficulty} Python coding problem that directly helps with:
{description}

The problem MUST be relevant to the skill described above.
Keep it focused and solvable in under 50 lines of code.

Return ONLY the problem specification, no solution.
Format as a clear problem statement with:
- What the function should do
- Input format
- Output format
- Example inputs and outputs"""

        return await self.llm.query(prompt, temperature=0.5, max_tokens=500)

    async def _generate_different_spec(
        self,
        desire: Dict,
        existing_spec: str,
        difficulty: str
    ) -> str:
        """Generate a different problem when duplicate detected."""
        description = desire.get("description", "improve coding")

        prompt = f"""Create a DIFFERENT {difficulty} Python coding problem for:
{description}

Do NOT create a problem about: {existing_spec[:100]}...

Create something unique that still addresses the skill.
Return ONLY the problem specification."""

        return await self.llm.query(prompt, temperature=0.7, max_tokens=500)

    async def _generate_tests(self, spec: str, difficulty: str) -> str:
        """Generate test suite BEFORE implementation (TDD)."""
        prompt = f"""Write pytest unit tests for this problem:
{spec}

Difficulty level: {difficulty}

CRITICAL: Return ONLY valid Python code that compiles. No explanations, no markdown.

The output must be exactly this format (replace with actual tests):

import pytest

def test_case_1():
    # Test normal case
    result = function_name(input_value)
    assert result == expected_value

def test_case_2():
    # Test edge case
    result = function_name(edge_input)
    assert result == expected_edge

Write 3-5 test functions covering normal and edge cases.
Do NOT use markdown code blocks. Just output raw Python code."""

        response = await self.llm.query(prompt, temperature=0.3, max_tokens=800)

        # Extract code from response
        code = self._extract_code(response)

        # Additional cleanup for common LLM issues
        lines = []
        in_code = False
        for line in code.split('\n'):
            stripped = line.strip()
            # Skip explanation lines
            if stripped.startswith('#') and 'explanation' in stripped.lower():
                continue
            # Skip empty lines at start
            if not in_code and not stripped:
                continue
            # Start tracking once we see actual code
            if stripped.startswith('import') or stripped.startswith('def ') or stripped.startswith('from '):
                in_code = True
            if in_code:
                lines.append(line)

        return '\n'.join(lines)

    def _extract_code(self, response: str) -> str:
        """Extract code from LLM response."""
        text = response.strip()

        if "```python" in text:
            text = text.split("```python")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return text.strip()

    def _validate_syntax(self, code: str) -> bool:
        """Validate Python syntax."""
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError as e:
            logger.debug(f"Syntax error: {e}")
            return False

    async def attempt_solution(self, problem: PracticeProblem) -> PracticeResult:
        """
        Attempt to solve the problem.

        Args:
            problem: The practice problem

        Returns:
            PracticeResult with success status
        """
        self._attempts += 1

        # Initialize for loop
        test_result = {"passed": False, "output": "", "error": "No attempts made", "passed_count": 0, "total_count": 1}
        solution = ""
        previous_solution = ""

        for attempt in range(self.MAX_SOLUTION_ATTEMPTS):
            # Generate solution
            if attempt == 0:
                solution = await self._generate_solution(problem)
            else:
                # Retry with feedback
                error_msg = test_result.get("error", "") if test_result else "Syntax error in previous attempt"
                solution = await self._generate_solution_with_feedback(
                    problem,
                    previous_solution,
                    error_msg
                )

            previous_solution = solution

            # Validate solution syntax
            if not self._validate_syntax(solution):
                test_result = {"passed": False, "output": "Syntax error", "error": "Solution has syntax errors", "passed_count": 0, "total_count": 1}
                continue

            # Run tests
            test_result = self._run_tests(problem.oracle, solution)

            if test_result["passed"]:
                self._successes += 1
                return PracticeResult(
                    success=True,
                    solution=solution,
                    test_output=test_result["output"],
                    tests_passed=test_result.get("passed_count", 1),
                    tests_total=test_result.get("total_count", 1),
                    problem=problem.spec[:500],
                    approach="TDD Practice",
                    attempts=attempt + 1,
                    difficulty=problem.difficulty
                )

        # All attempts failed
        return PracticeResult(
            success=False,
            solution=solution,
            test_output=test_result["output"],
            tests_passed=test_result.get("passed_count", 0),
            tests_total=test_result.get("total_count", 1),
            problem=problem.spec[:500],
            approach="TDD Practice",
            attempts=self.MAX_SOLUTION_ATTEMPTS,
            difficulty=problem.difficulty,
            error=test_result.get("error")
        )

    async def _generate_solution(self, problem: PracticeProblem) -> str:
        """Generate solution for problem."""
        prompt = f"""Implement a solution for this problem:
{problem.spec}

Return ONLY the Python code.
The solution should be clean, readable, and handle edge cases.
Start with any necessary imports, then define the required function(s)."""

        response = await self.llm.query(prompt, temperature=0.7, max_tokens=800)
        return self._extract_code(response)

    async def _generate_solution_with_feedback(
        self,
        problem: PracticeProblem,
        previous_solution: str,
        error: str
    ) -> str:
        """Generate improved solution based on test feedback."""
        prompt = f"""Your previous solution failed some tests.

Problem:
{problem.spec}

Previous solution:
{previous_solution}

Error/Feedback:
{error[:500]}

Fix the solution to pass the tests.
Return ONLY the corrected Python code."""

        response = await self.llm.query(prompt, temperature=0.5, max_tokens=800)
        return self._extract_code(response)

    def _run_tests(self, tests: str, solution: str) -> Dict:
        """Run tests against solution in sandboxed subprocess."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write solution
            solution_path = Path(tmpdir) / "solution.py"
            solution_path.write_text(solution)

            # Write tests (import from solution if not already present)
            if "from solution import" not in tests and "import solution" not in tests:
                test_code = f"from solution import *\n\n{tests}"
            else:
                test_code = tests
            test_path = Path(tmpdir) / "test_solution.py"
            test_path.write_text(test_code)

            try:
                # Run pytest with timeout
                result = subprocess.run(
                    ["python", "-m", "pytest", str(test_path), "-v", "--tb=short"],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=tmpdir
                )

                output = result.stdout + result.stderr

                # Parse test counts
                passed_count = output.count(" PASSED")
                failed_count = output.count(" FAILED")
                total_count = passed_count + failed_count

                return {
                    "passed": result.returncode == 0,
                    "output": output[:2000],
                    "passed_count": passed_count,
                    "total_count": max(total_count, 1),
                    "error": None if result.returncode == 0 else output[-500:]
                }

            except subprocess.TimeoutExpired:
                return {
                    "passed": False,
                    "output": "Timeout exceeded",
                    "passed_count": 0,
                    "total_count": 1,
                    "error": f"Test execution timed out after {self.timeout}s"
                }

            except Exception as e:
                return {
                    "passed": False,
                    "output": str(e),
                    "passed_count": 0,
                    "total_count": 1,
                    "error": str(e)
                }

    async def record_outcome(self, domain: str, result: PracticeResult):
        """
        Record practice outcome and adjust difficulty.

        Args:
            domain: The practice domain
            result: The practice result
        """
        current_idx = self._domain_difficulty.get(domain, 0)

        if result.success:
            # Track success streak for difficulty increase
            streak = await self._get_streak(domain, success=True)
            if streak >= 3 and current_idx < len(self.DIFFICULTY_LEVELS) - 1:
                self._domain_difficulty[domain] = current_idx + 1
                logger.info(f"Difficulty increased for {domain}")
        else:
            # Use partial score for more granular adjustment
            if result.tests_total > 0:
                partial_score = result.tests_passed / result.tests_total
                if partial_score < 0.5:
                    # Mostly wrong - decrease difficulty
                    streak = await self._get_streak(domain, success=False)
                    if streak >= 2 and current_idx > 0:
                        self._domain_difficulty[domain] = current_idx - 1
                        logger.info(f"Difficulty decreased for {domain}")

    async def _get_streak(self, domain: str, success: bool) -> int:
        """Get current streak of successes or failures."""
        # Simple in-memory tracking for now
        # Could be extended to query memory
        return 1  # Placeholder

    def get_stats(self) -> Dict:
        """Get practice statistics."""
        return {
            "attempts": self._attempts,
            "successes": self._successes,
            "success_rate": self._successes / max(self._attempts, 1),
            "domain_difficulty": {
                k: self.DIFFICULTY_LEVELS[v]
                for k, v in self._domain_difficulty.items()
            }
        }

    def reset(self):
        """Reset practice state."""
        self._domain_difficulty.clear()
        self._recent_problems.clear()
        self._attempts = 0
        self._successes = 0

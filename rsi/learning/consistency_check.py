"""
Consistency Check - Verification for logic domain.

Since logic doesn't have unit tests, we verify by running the same
prompt multiple times and checking for consistency in conclusions.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("rsi.learning.consistency")


@dataclass
class ConsistencyResult:
    """Result of consistency verification."""
    is_consistent: bool
    reasoning: Optional[str]
    consistency_score: float  # 0.0-1.0
    responses: List[str]
    variance_notes: str


class ConsistencyCheck:
    """
    Logic domain verification via multi-run consistency.

    Run the same reasoning prompt N times and check if conclusions
    are consistent. High consistency suggests reliable reasoning.
    """

    N_RUNS = 5
    CONSISTENCY_THRESHOLD = 0.8  # 80% agreement required

    def __init__(self, llm_client, config: Dict = None):
        """
        Initialize consistency checker.

        Args:
            llm_client: LLM client for reasoning
            config: Optional configuration
        """
        self.llm = llm_client
        self.config = config or {}
        self.n_runs = self.config.get("consistency_runs", self.N_RUNS)

        # Stats
        self._checks = 0
        self._consistent_checks = 0

    async def run(self, desire: Dict) -> ConsistencyResult:
        """
        Run consistency check for a logic desire.

        Args:
            desire: The logic improvement desire

        Returns:
            ConsistencyResult with consistency assessment
        """
        self._checks += 1
        description = desire.get("description", "")

        # Generate the reasoning prompt
        reasoning_prompt = self._build_reasoning_prompt(description)

        # Run multiple times
        responses = []
        for i in range(self.n_runs):
            try:
                response = await self.llm.query(
                    reasoning_prompt,
                    temperature=0.7  # Some variation to test robustness
                )
                responses.append(response)
            except Exception as e:
                logger.warning(f"Reasoning run {i+1} failed: {e}")
                responses.append("")

        # Check consistency
        is_consistent, score, notes = self._analyze_consistency(responses)

        if is_consistent:
            self._consistent_checks += 1

        return ConsistencyResult(
            is_consistent=is_consistent,
            reasoning=responses[0] if is_consistent else None,
            consistency_score=score,
            responses=responses,
            variance_notes=notes
        )

    def _build_reasoning_prompt(self, description: str) -> str:
        """Build a reasoning prompt from the desire."""
        return f"""Reason through the following carefully:

{description}

Structure your response as:
1. Identify the key premises or given information
2. Apply logical rules step by step
3. State your conclusion clearly

End with a clear CONCLUSION: statement.
"""

    def _analyze_consistency(self, responses: List[str]) -> tuple:
        """
        Analyze consistency across multiple responses.

        Returns:
            (is_consistent, score, notes)
        """
        if not responses or all(r == "" for r in responses):
            return False, 0.0, "No valid responses"

        # Extract conclusions
        conclusions = [self._extract_conclusion(r) for r in responses if r]

        if not conclusions:
            return False, 0.0, "Could not extract conclusions"

        # Compare conclusions
        unique_conclusions = set(conclusions)
        most_common = max(set(conclusions), key=conclusions.count)
        agreement_count = conclusions.count(most_common)

        score = agreement_count / len(conclusions)

        # Build variance notes
        if len(unique_conclusions) == 1:
            notes = "Perfect agreement across all runs"
        elif score >= self.CONSISTENCY_THRESHOLD:
            notes = f"{agreement_count}/{len(conclusions)} runs agreed"
        else:
            notes = f"High variance: {len(unique_conclusions)} different conclusions"

        return score >= self.CONSISTENCY_THRESHOLD, score, notes

    def _extract_conclusion(self, response: str) -> str:
        """Extract the conclusion from a reasoning response."""
        response_lower = response.lower()

        # Look for explicit conclusion markers
        markers = ["conclusion:", "therefore:", "thus:", "hence:", "in conclusion:"]

        for marker in markers:
            if marker in response_lower:
                idx = response_lower.index(marker)
                # Get text after the marker
                conclusion = response[idx + len(marker):].strip()
                # Take first sentence
                if "." in conclusion:
                    conclusion = conclusion.split(".")[0] + "."
                return conclusion[:200]

        # Fallback: last substantial sentence
        sentences = response.split(".")
        for sentence in reversed(sentences):
            if len(sentence.strip()) > 20:
                return sentence.strip()[:200]

        return response[-200:]

    async def generate_practice(self, desire: Dict) -> Dict:
        """
        Generate a logic practice problem.

        Args:
            desire: The logic improvement desire

        Returns:
            Practice problem dict
        """
        description = desire.get("description", "improve logical reasoning")

        prompt = f"""Create a logic/reasoning problem related to:
{description}

The problem should:
- Have a clear logical structure
- Be solvable through step-by-step reasoning
- Have a definitive correct answer

Format:
PROBLEM: [The logic puzzle or reasoning problem]
EXPECTED_CONCLUSION: [The correct conclusion]
"""

        response = await self.llm.query(prompt, temperature=0.5)

        # Parse response
        problem = ""
        expected = ""

        if "PROBLEM:" in response:
            parts = response.split("PROBLEM:")[1]
            if "EXPECTED_CONCLUSION:" in parts:
                problem = parts.split("EXPECTED_CONCLUSION:")[0].strip()
                expected = parts.split("EXPECTED_CONCLUSION:")[1].strip()
            else:
                problem = parts.strip()

        return {
            "problem": problem,
            "expected_conclusion": expected,
            "domain": "logic"
        }

    def get_stats(self) -> Dict:
        """Get consistency check statistics."""
        return {
            "total_checks": self._checks,
            "consistent_checks": self._consistent_checks,
            "consistency_rate": self._consistent_checks / max(self._checks, 1)
        }

    def reset(self):
        """Reset checker state."""
        self._checks = 0
        self._consistent_checks = 0

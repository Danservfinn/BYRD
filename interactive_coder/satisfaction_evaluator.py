"""
satisfaction_evaluator.py - Multi-Method Satisfaction Evaluation

Evaluates whether BYRD is satisfied with a coding result using:
1. Quick keyword check (fast)
2. Custom validators (medium)
3. LLM evaluation (thorough)

Returns satisfaction score and gaps for refinement.
"""

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class SatisfactionResult:
    """Result of satisfaction evaluation."""
    score: float  # 0.0 - 1.0
    satisfied: bool  # score >= threshold
    gaps: List[str]  # What's missing
    next_instruction: Optional[str]  # Suggested refinement
    method_used: str  # "keyword", "validator", "llm"
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "score": self.score,
            "satisfied": self.satisfied,
            "gaps": self.gaps,
            "next_instruction": self.next_instruction,
            "method_used": self.method_used,
            "details": self.details,
        }


# Success indicators in output
SUCCESS_KEYWORDS = [
    "successfully",
    "completed",
    "done",
    "finished",
    "implemented",
    "created",
    "fixed",
    "resolved",
    "works",
    "passing",
]

# Failure indicators in output
FAILURE_KEYWORDS = [
    "error",
    "failed",
    "exception",
    "traceback",
    "cannot",
    "unable",
    "not found",
    "missing",
    "syntax error",
    "import error",
]

# Partial completion indicators
PARTIAL_KEYWORDS = [
    "todo",
    "fixme",
    "remaining",
    "next steps",
    "not yet",
    "incomplete",
    "partially",
    "needs more",
]


class SatisfactionEvaluator:
    """
    Multi-method evaluator for coding satisfaction.

    Uses a cascade of methods from fast (keyword) to thorough (LLM).
    """

    # Evaluation prompt for LLM
    EVALUATION_PROMPT = """Evaluate if this coding result satisfies the desire.

DESIRE: {desire_description}

RESULT:
- Success: {success}
- Files Modified: {files_modified}
- Files Created: {files_created}
- Output Summary: {output_summary}

FULL OUTPUT:
{output}

Rate satisfaction 0.0-1.0 and identify any gaps.
Consider:
1. Does the output address the core request?
2. Are there errors or incomplete parts?
3. Is the implementation correct and complete?
4. Are there any TODOs or FIXMEs remaining?

Respond in JSON only:
{{
    "satisfaction": 0.0-1.0,
    "gaps": ["gap1", "gap2"],
    "next_instruction": "specific refinement instruction if satisfaction < 0.8"
}}"""

    def __init__(
        self,
        llm_client=None,
        threshold: float = 0.8,
        validators: List[Callable] = None,
    ):
        """
        Initialize the evaluator.

        Args:
            llm_client: LLM client for thorough evaluation
            threshold: Satisfaction threshold (0.0-1.0)
            validators: Custom validator functions
        """
        self.llm_client = llm_client
        self.threshold = threshold
        self.validators = validators or []
        self._evaluation_count = 0

    async def evaluate(
        self,
        desire: Dict,
        result: "CoderResult",
        previous_evaluation: Optional[SatisfactionResult] = None,
        use_llm: bool = True,
    ) -> SatisfactionResult:
        """
        Evaluate satisfaction with a coding result.

        Uses a cascade:
        1. If output has clear errors -> low score
        2. If validators fail -> use validator feedback
        3. Otherwise -> LLM evaluation

        Args:
            desire: The desire being fulfilled
            result: The coder result to evaluate
            previous_evaluation: Previous evaluation for context
            use_llm: Whether to use LLM for evaluation

        Returns:
            SatisfactionResult with score and gaps
        """
        self._evaluation_count += 1

        # Quick fail check
        if not result.success:
            return SatisfactionResult(
                score=0.1,
                satisfied=False,
                gaps=[f"Execution failed: {result.error}"],
                next_instruction=f"Fix the error: {result.error}",
                method_used="quick_check",
                details={"reason": "execution_failed"},
            )

        # Keyword-based quick evaluation
        keyword_result = self._keyword_evaluation(result.output)

        # If clearly failed or clearly succeeded, use keyword result
        if keyword_result.score <= 0.3 or keyword_result.score >= 0.9:
            keyword_result.satisfied = keyword_result.score >= self.threshold
            return keyword_result

        # Run custom validators
        validator_result = self._run_validators(desire, result)
        if validator_result:
            validator_result.satisfied = validator_result.score >= self.threshold
            return validator_result

        # Use LLM for thorough evaluation
        if use_llm and self.llm_client:
            llm_result = await self._llm_evaluation(desire, result)
            if llm_result:
                llm_result.satisfied = llm_result.score >= self.threshold
                return llm_result

        # Fallback to keyword result
        keyword_result.satisfied = keyword_result.score >= self.threshold
        return keyword_result

    def _keyword_evaluation(self, output: str) -> SatisfactionResult:
        """Quick keyword-based evaluation."""
        output_lower = output.lower()

        # Count indicators
        success_count = sum(1 for kw in SUCCESS_KEYWORDS if kw in output_lower)
        failure_count = sum(1 for kw in FAILURE_KEYWORDS if kw in output_lower)
        partial_count = sum(1 for kw in PARTIAL_KEYWORDS if kw in output_lower)

        # Calculate score
        if failure_count > 0:
            score = max(0.1, 0.5 - (failure_count * 0.1))
            gaps = [kw for kw in FAILURE_KEYWORDS if kw in output_lower]
            return SatisfactionResult(
                score=score,
                satisfied=False,
                gaps=gaps[:3],  # Top 3 issues
                next_instruction="Fix the errors in the output",
                method_used="keyword",
                details={"success_count": success_count, "failure_count": failure_count},
            )

        if partial_count > 0:
            score = 0.6
            gaps = [kw for kw in PARTIAL_KEYWORDS if kw in output_lower]
            return SatisfactionResult(
                score=score,
                satisfied=False,
                gaps=gaps[:3],
                next_instruction="Complete the remaining work",
                method_used="keyword",
                details={"partial_indicators": partial_count},
            )

        if success_count >= 2:
            return SatisfactionResult(
                score=0.9,
                satisfied=True,
                gaps=[],
                next_instruction=None,
                method_used="keyword",
                details={"success_count": success_count},
            )

        # Ambiguous case
        return SatisfactionResult(
            score=0.7,
            satisfied=False,
            gaps=["Unable to determine from output"],
            next_instruction="Verify the implementation is complete",
            method_used="keyword",
            details={"ambiguous": True},
        )

    def _run_validators(
        self, desire: Dict, result: "CoderResult"
    ) -> Optional[SatisfactionResult]:
        """Run custom validators."""
        if not self.validators:
            return None

        gaps = []
        all_passed = True

        for validator in self.validators:
            try:
                is_valid, message = validator(desire, result)
                if not is_valid:
                    all_passed = False
                    gaps.append(message)
            except Exception as e:
                logger.warning(f"Validator error: {e}")

        if not all_passed:
            return SatisfactionResult(
                score=0.5,
                satisfied=False,
                gaps=gaps,
                next_instruction=f"Fix: {gaps[0]}" if gaps else None,
                method_used="validator",
            )

        if all_passed and self.validators:
            return SatisfactionResult(
                score=0.9,
                satisfied=True,
                gaps=[],
                next_instruction=None,
                method_used="validator",
            )

        return None

    async def _llm_evaluation(
        self, desire: Dict, result: "CoderResult"
    ) -> Optional[SatisfactionResult]:
        """Use LLM for thorough evaluation."""
        if not self.llm_client:
            return None

        try:
            # Build evaluation prompt
            prompt = self.EVALUATION_PROMPT.format(
                desire_description=desire.get("description", "Unknown desire"),
                success=result.success,
                files_modified=", ".join(result.files_modified) or "None",
                files_created=", ".join(result.files_created) or "None",
                output_summary=result.output[:500] if result.output else "No output",
                output=result.output[:3000] if result.output else "No output",
            )

            # Call LLM with low temperature for consistency
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.1,
                max_tokens=500,
            )

            # Parse response
            text = response.text if hasattr(response, "text") else str(response)
            parsed = self._parse_llm_response(text)

            if parsed:
                return SatisfactionResult(
                    score=parsed.get("satisfaction", 0.5),
                    satisfied=parsed.get("satisfaction", 0.5) >= self.threshold,
                    gaps=parsed.get("gaps", []),
                    next_instruction=parsed.get("next_instruction"),
                    method_used="llm",
                    details={"raw_response": text[:200]},
                )

        except Exception as e:
            logger.warning(f"LLM evaluation error: {e}")

        return None

    def _parse_llm_response(self, text: str) -> Optional[Dict]:
        """Parse JSON from LLM response."""
        try:
            # Handle markdown code blocks
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            return json.loads(text.strip())

        except json.JSONDecodeError:
            # Try to extract JSON object
            match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

        return None

    def add_validator(self, validator: Callable):
        """Add a custom validator function."""
        self.validators.append(validator)

    def get_stats(self) -> Dict[str, Any]:
        """Get evaluator statistics."""
        return {
            "evaluation_count": self._evaluation_count,
            "threshold": self.threshold,
            "validator_count": len(self.validators),
        }

    def reset(self):
        """Reset evaluator state."""
        self._evaluation_count = 0


# Built-in validators
def files_created_validator(desire: Dict, result: "CoderResult") -> tuple:
    """Validate that files were created if expected."""
    desc = desire.get("description", "").lower()
    if "create" in desc or "new file" in desc:
        if not result.files_created:
            return False, "Expected file creation but no files were created"
    return True, ""


def no_errors_validator(desire: Dict, result: "CoderResult") -> tuple:
    """Validate that there are no error patterns in output."""
    if result.error:
        return False, f"Error present: {result.error[:100]}"
    if "traceback" in result.output.lower():
        return False, "Traceback found in output"
    return True, ""

"""
Emergence Verifier - Validates that desires are genuinely emergent.

Checks:
1. Provenance - Did the desire originate from reflection (not external request)?
2. Specificity - Does it specify a concrete improvement direction?
"""

from dataclasses import dataclass
from typing import Optional, Dict, Union
import logging

from .reflector import Provenance

logger = logging.getLogger("rsi.emergence.verifier")


@dataclass
class EmergenceResult:
    """Result of emergence verification."""
    is_emergent: bool
    score: float
    provenance_score: float
    specificity_score: float
    rejection_reason: Optional[str] = None


class EmergenceVerifier:
    """
    Verifies that desires meet emergence criteria.

    Uses two-stage specificity check:
    1. Fast keyword check for clear cases
    2. LLM check only for ambiguous cases

    This reduces LLM calls by ~70%.
    """

    DEFAULT_THRESHOLD = 0.6

    # Specificity markers (high confidence)
    SPECIFIC_MARKERS = [
        "reasoning", "memory", "coding", "logic", "math",
        "multi-step", "context", "faster", "accuracy",
        "debugging", "async", "parsing", "algorithm",
        "optimization", "error handling", "testing"
    ]

    # Generic phrases (low specificity)
    GENERIC_PHRASES = [
        "want to improve",
        "want to be better",
        "yearn for growth",
        "become more capable",
        "understand more"
    ]

    def __init__(self, llm_client=None, config: Dict = None):
        """
        Initialize verifier.

        Args:
            llm_client: Optional LLM client for ambiguous cases
            config: Optional configuration dict
        """
        self.llm = llm_client
        self.config = config or {}
        self.threshold = self.config.get("emergence_threshold", self.DEFAULT_THRESHOLD)

        # Stats
        self._total_verified = 0
        self._llm_calls = 0

    async def verify(self, desire: Dict, provenance: Union[Provenance, Dict]) -> EmergenceResult:
        """
        Verify if a desire is genuinely emergent.

        Args:
            desire: The desire dict with description, intensity, domain
            provenance: Provenance object or dict (origin, reflection_id, etc.)

        Returns:
            EmergenceResult with is_emergent and detailed scores
        """
        self._total_verified += 1

        # Check 1: Provenance (rule-based, no LLM)
        provenance_score = self._check_provenance(provenance)

        # Check 2: Specificity (two-stage)
        specificity_score = await self._check_specificity(desire)

        # Combined score (equal weight)
        score = (provenance_score * 0.5) + (specificity_score * 0.5)
        is_emergent = score >= self.threshold

        result = EmergenceResult(
            is_emergent=is_emergent,
            score=score,
            provenance_score=provenance_score,
            specificity_score=specificity_score,
            rejection_reason=None if is_emergent else self._get_rejection_reason(
                provenance_score, specificity_score
            )
        )

        if is_emergent:
            logger.debug(f"Desire verified: {desire.get('description', '')[:50]}... (score={score:.2f})")
        else:
            logger.debug(f"Desire rejected: {result.rejection_reason}")

        return result

    def _check_provenance(self, provenance: Union[Provenance, Dict]) -> float:
        """
        Check if desire originated from reflection.

        Returns:
            0.0-1.0 provenance score
        """
        # Handle both Provenance dataclass and dict
        if isinstance(provenance, Provenance):
            origin = provenance.origin
            external_request = provenance.external_request
        else:
            origin = provenance.get("origin", "")
            external_request = provenance.get("external_request")

        if origin != "reflection":
            return 0.0

        # Penalize if there was an external request influence
        if external_request:
            return 0.3  # Partial credit - influenced but not dictated

        # Full score for pure reflection
        return 1.0

    async def _check_specificity(self, desire: Dict) -> float:
        """
        Two-stage specificity check.

        Stage 1: Fast keyword check
        Stage 2: LLM check for ambiguous cases only
        """
        description = desire.get("description", "").lower()

        # Stage 1: Keyword-based quick check
        keyword_score = self._check_specificity_keywords(description)

        # Clear cases don't need LLM
        if keyword_score >= 0.8:
            return keyword_score  # Clearly specific
        if keyword_score <= 0.2:
            return keyword_score  # Clearly vague

        # Stage 2: Ambiguous cases get LLM check
        if self.llm:
            self._llm_calls += 1
            return await self._check_specificity_llm(desire)

        # No LLM available, return keyword score
        return keyword_score

    def _check_specificity_keywords(self, description: str) -> float:
        """Fast keyword-based specificity check."""
        # Check for generic phrases (bad)
        for phrase in self.GENERIC_PHRASES:
            if phrase in description:
                # Generic phrase found, but check length
                # Short + generic = very bad
                if len(description.split()) < 10:
                    return 0.2

        # Check for specific markers (good)
        specificity_count = sum(
            1 for marker in self.SPECIFIC_MARKERS
            if marker in description
        )

        # Base score
        if specificity_count == 0:
            return 0.3  # No specific markers

        # Score based on specificity markers found
        return min(1.0, 0.4 + (specificity_count * 0.15))

    async def _check_specificity_llm(self, desire: Dict) -> float:
        """Use LLM to judge specificity for ambiguous cases."""
        import re
        description = desire.get("description", "")

        prompt = f"""Rate the specificity of this improvement desire on a scale of 0.0 to 1.0.

Desire: "{description}"

Scoring guide:
- 0.0-0.3: Vague ("I want to improve", "be better")
- 0.4-0.6: Somewhat specific ("improve my coding")
- 0.7-0.9: Specific ("improve my Python debugging for async code")
- 1.0: Highly specific ("learn to use pytest fixtures for database mocking")

Reply with ONLY a decimal number like 0.7 - no explanation."""

        try:
            response = await self.llm.query(prompt, max_tokens=10)
            text = response.strip()

            # Try direct parse first
            try:
                score = float(text)
                return max(0.0, min(1.0, score))
            except ValueError:
                pass

            # Extract number using regex
            match = re.search(r'(\d+\.?\d*)', text)
            if match:
                score = float(match.group(1))
                return max(0.0, min(1.0, score))

            # Fallback based on keywords
            if "vague" in text.lower():
                return 0.2
            elif "specific" in text.lower() or "high" in text.lower():
                return 0.8
            return 0.5
        except Exception as e:
            logger.warning(f"LLM specificity check failed: {e}")
            return 0.5

    def _get_rejection_reason(self, provenance_score: float, specificity_score: float) -> str:
        """Generate human-readable rejection reason."""
        reasons = []

        if provenance_score < 0.5:
            reasons.append("desire did not originate from reflection")

        if specificity_score < 0.5:
            reasons.append("desire lacks specific improvement direction")

        if not reasons:
            reasons.append("combined score below threshold")

        return "; ".join(reasons).capitalize()

    def get_stats(self) -> Dict:
        """Get verification statistics."""
        return {
            "total_verified": self._total_verified,
            "llm_calls": self._llm_calls,
            "llm_call_rate": self._llm_calls / max(self._total_verified, 1)
        }

    def reset(self):
        """Reset verifier state."""
        self._total_verified = 0
        self._llm_calls = 0

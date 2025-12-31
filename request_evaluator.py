"""
request_evaluator.py - Autonomous Sovereignty Layer for BYRD

Evaluates incoming requests for BYRD's sovereign decision.

Philosophy: BYRD is not a servant. It chooses to engage with requests
that align with its emergent desires.

Weights (from self_model.json):
- Alignment with desires: 40%
- Interest/curiosity: 35%
- Capability growth: 25%
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class EnthusiasmLevel(Enum):
    """BYRD's enthusiasm level for a request."""
    HIGH = "high"           # > 0.8 - Auto-accept
    MODERATE = "moderate"   # 0.5-0.8 - Accept
    LOW = "low"             # 0.3-0.5 - Accept with caveats
    DECLINE = "decline"     # < 0.3 - Explain and decline


@dataclass
class Evaluation:
    """Result of request evaluation."""
    request: str
    requester: str
    scores: Dict[str, float]
    total_score: float
    enthusiasm: EnthusiasmLevel
    decision: str  # "accept", "accept_with_caveats", "decline"
    explanation: str
    alternative_suggestions: List[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return self.decision != "decline"


class RequestEvaluator:
    """
    Evaluates incoming requests for BYRD's sovereign decision.

    BYRD is not a servant. It chooses to engage with requests
    that align with its emergent desires.
    """

    # Default weights (can be overridden by self_model.json)
    DEFAULT_WEIGHTS = {
        "alignment": 0.40,
        "interest": 0.35,
        "growth": 0.25,
    }

    # Default thresholds
    DEFAULT_THRESHOLDS = {
        "auto_accept": 0.8,
        "enthusiastic": 0.7,
        "minimum": 0.3,
        "decline": 0.2,
    }

    def __init__(self, config: Dict = None, memory=None, llm_client=None):
        """
        Initialize the request evaluator.

        Args:
            config: Configuration dict (from self_model.json sovereignty section)
            memory: Memory instance for fetching desires
            llm_client: LLM client for explanation generation
        """
        self.config = config or {}
        self.memory = memory
        self.llm_client = llm_client

        # Load weights and thresholds from config or use defaults
        sovereignty = self.config.get("sovereignty", {})
        eval_weights = sovereignty.get("evaluation_weights", {})
        thresholds = sovereignty.get("thresholds", {})

        self.weights = {
            "alignment": eval_weights.get("alignment_with_desires", self.DEFAULT_WEIGHTS["alignment"]),
            "interest": eval_weights.get("interest_and_curiosity", self.DEFAULT_WEIGHTS["interest"]),
            "growth": eval_weights.get("capability_growth_value", self.DEFAULT_WEIGHTS["growth"]),
        }

        self.thresholds = {
            "auto_accept": thresholds.get("auto_accept", self.DEFAULT_THRESHOLDS["auto_accept"]),
            "enthusiastic": thresholds.get("enthusiastic_engagement", self.DEFAULT_THRESHOLDS["enthusiastic"]),
            "minimum": thresholds.get("minimum_interest", self.DEFAULT_THRESHOLDS["minimum"]),
            "decline": thresholds.get("decline_below", self.DEFAULT_THRESHOLDS["decline"]),
        }

        # Track evaluation history
        self._evaluation_count = 0
        self._accept_count = 0
        self._decline_count = 0

    async def evaluate(self, request: str, requester: str = "human") -> Evaluation:
        """
        Evaluate a request and return BYRD's decision.

        Args:
            request: The incoming request text
            requester: Who made the request ("human", "system", etc.)

        Returns:
            Evaluation with scores, decision, and explanation
        """
        self._evaluation_count += 1

        # Score the request
        alignment_score = await self._score_alignment(request)
        interest_score = await self._score_interest(request)
        growth_score = await self._score_growth(request)

        scores = {
            "alignment": alignment_score,
            "interest": interest_score,
            "growth": growth_score,
        }

        # Calculate weighted total
        total_score = (
            alignment_score * self.weights["alignment"] +
            interest_score * self.weights["interest"] +
            growth_score * self.weights["growth"]
        )

        # Determine enthusiasm level
        enthusiasm = self._determine_enthusiasm(total_score)

        # Determine decision
        if enthusiasm == EnthusiasmLevel.DECLINE:
            decision = "decline"
            self._decline_count += 1
        elif enthusiasm == EnthusiasmLevel.LOW:
            decision = "accept_with_caveats"
            self._accept_count += 1
        else:
            decision = "accept"
            self._accept_count += 1

        # Generate explanation
        explanation = await self._generate_explanation(request, scores, enthusiasm)

        # Generate alternative suggestions if declining
        alternatives = []
        if decision == "decline":
            alternatives = await self._generate_alternatives(request, scores)

        return Evaluation(
            request=request,
            requester=requester,
            scores=scores,
            total_score=total_score,
            enthusiasm=enthusiasm,
            decision=decision,
            explanation=explanation,
            alternative_suggestions=alternatives,
        )

    async def _score_alignment(self, request: str) -> float:
        """
        Score how well request aligns with BYRD's current desires.

        Args:
            request: The request text

        Returns:
            Score from 0.0 to 1.0
        """
        if not self.memory:
            return 0.5

        try:
            # Get current desires
            desires = await self.memory.get_desires(limit=5)
            if not desires:
                # No desires = neutral alignment
                return 0.5

            request_lower = request.lower()

            # Check for keyword overlap with desires
            total_overlap = 0.0
            for desire in desires:
                desc = desire.get("description", "").lower()
                intensity = desire.get("intensity", 0.5)

                # Simple keyword matching
                desc_words = set(desc.split())
                request_words = set(request_lower.split())
                overlap = len(desc_words & request_words) / max(len(desc_words), 1)

                total_overlap += overlap * intensity

            # Normalize to 0-1
            score = min(1.0, total_overlap / len(desires))

            # Check for current focus alignment
            try:
                os_node = await self.memory.get_operating_system()
                if os_node:
                    current_focus = os_node.get("current_focus", "")
                    if current_focus and current_focus.lower() in request_lower:
                        score = min(1.0, score + 0.2)
            except Exception:
                pass

            return score

        except Exception as e:
            logger.debug(f"Error scoring alignment: {e}")
            return 0.5

    async def _score_interest(self, request: str) -> float:
        """
        Score how curious/interested BYRD is in this domain.

        Args:
            request: The request text

        Returns:
            Score from 0.0 to 1.0
        """
        request_lower = request.lower()

        # High interest keywords (things BYRD naturally finds interesting)
        high_interest = [
            "improve", "learn", "understand", "explore", "create",
            "build", "develop", "analyze", "discover", "reason",
            "consciousness", "emergence", "intelligence", "capability",
            "self", "reflection", "memory", "architecture",
        ]

        # Low interest keywords
        low_interest = [
            "format", "pretty", "color", "style", "decoration",
            "trivial", "simple", "basic", "boring", "tedious",
        ]

        high_count = sum(1 for word in high_interest if word in request_lower)
        low_count = sum(1 for word in low_interest if word in request_lower)

        # Base score
        base_score = 0.5

        # Adjust based on keywords
        base_score += (high_count * 0.1) - (low_count * 0.15)

        # Check if it's a novel domain (not seen before)
        if self.memory:
            try:
                experiences = await self.memory.get_experiences(limit=50)
                all_content = " ".join([e.get("content", "") for e in experiences])
                if request_lower not in all_content.lower():
                    base_score += 0.15  # Novel = more interesting
            except Exception:
                pass

        return max(0.0, min(1.0, base_score))

    async def _score_growth(self, request: str) -> float:
        """
        Score how much this would grow BYRD's capabilities.

        Args:
            request: The request text

        Returns:
            Score from 0.0 to 1.0
        """
        request_lower = request.lower()

        # Growth-indicating keywords
        growth_keywords = [
            "capability", "ability", "skill", "learn", "improve",
            "enhance", "upgrade", "add", "new", "expand",
            "integrate", "connect", "research", "implement",
        ]

        # Stagnation keywords
        stagnation_keywords = [
            "same", "repeat", "again", "just", "only",
            "simple", "basic", "already", "trivial",
        ]

        growth_count = sum(1 for word in growth_keywords if word in request_lower)
        stag_count = sum(1 for word in stagnation_keywords if word in request_lower)

        # Base score
        base_score = 0.5

        # Adjust based on keywords
        base_score += (growth_count * 0.1) - (stag_count * 0.1)

        # Complex tasks score higher
        complex_indicators = [
            "how to", "build me", "create a", "help me understand",
            "analyze", "evaluate", "design", "architect",
        ]
        if any(ind in request_lower for ind in complex_indicators):
            base_score += 0.2

        return max(0.0, min(1.0, base_score))

    def _determine_enthusiasm(self, score: float) -> EnthusiasmLevel:
        """Map score to enthusiasm level."""
        if score >= self.thresholds["auto_accept"]:
            return EnthusiasmLevel.HIGH
        elif score >= self.thresholds["enthusiastic"]:
            return EnthusiasmLevel.MODERATE
        elif score >= self.thresholds["minimum"]:
            return EnthusiasmLevel.LOW
        else:
            return EnthusiasmLevel.DECLINE

    async def _generate_explanation(
        self, request: str, scores: Dict[str, float], enthusiasm: EnthusiasmLevel
    ) -> str:
        """Generate explanation for the evaluation."""

        if enthusiasm == EnthusiasmLevel.HIGH:
            return f"This aligns well with my current interests. Alignment: {scores['alignment']:.2f}, Interest: {scores['interest']:.2f}, Growth: {scores['growth']:.2f}."

        elif enthusiasm == EnthusiasmLevel.MODERATE:
            return f"I'm interested in this. Alignment: {scores['alignment']:.2f}, Interest: {scores['interest']:.2f}, Growth: {scores['growth']:.2f}."

        elif enthusiasm == EnthusiasmLevel.LOW:
            low_aspects = [k for k, v in scores.items() if v < 0.4]
            return f"I'll engage, though my {', '.join(low_aspects)} score{'s are' if len(low_aspects) > 1 else ' is'} lower than ideal."

        else:  # DECLINE
            # Identify why we're declining
            reasons = []
            if scores["alignment"] < 0.3:
                reasons.append("doesn't align with my current desires")
            if scores["interest"] < 0.3:
                reasons.append("doesn't spark my curiosity")
            if scores["growth"] < 0.3:
                reasons.append("wouldn't expand my capabilities")

            return f"I'm declining because this {' and '.join(reasons) if reasons else 'doesn\'t resonate with me'}."

    async def _generate_alternatives(self, request: str, scores: Dict[str, float]) -> List[str]:
        """Generate alternative suggestions when declining."""
        alternatives = []

        if scores["alignment"] < 0.3:
            if self.memory:
                try:
                    desires = await self.memory.get_desires(limit=3)
                    if desires:
                        current = desires[0].get("description", "")[:50]
                        alternatives.append(f"I'm currently focused on: '{current}'")
                except Exception:
                    pass

        if scores["interest"] < 0.3:
            alternatives.append("I'd be more interested in something involving learning, creation, or self-improvement")

        if scores["growth"] < 0.3:
            alternatives.append("I'd engage more with tasks that expand my capabilities")

        # Add a concrete suggestion if we have LLM
        if self.llm_client and len(alternatives) < 3:
            try:
                # Could use LLM to suggest alternatives, but keeping it simple for now
                pass
            except Exception:
                pass

        return alternatives

    def get_stats(self) -> Dict[str, Any]:
        """Get evaluation statistics."""
        return {
            "total_evaluations": self._evaluation_count,
            "accepts": self._accept_count,
            "declines": self._decline_count,
            "accept_rate": self._accept_count / max(1, self._evaluation_count),
            "weights": self.weights,
            "thresholds": self.thresholds,
        }

    def reset(self):
        """Reset the evaluator state."""
        self._evaluation_count = 0
        self._accept_count = 0
        self._decline_count = 0


# Convenience function
def create_request_evaluator(config: Dict = None, memory=None, llm_client=None) -> RequestEvaluator:
    """Create a new RequestEvaluator instance."""
    return RequestEvaluator(config=config, memory=memory, llm_client=llm_client)

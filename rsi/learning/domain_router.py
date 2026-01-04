"""
Domain Router - Routes desires to appropriate practice methods.

Uses the Oracle Constraint: only practice in domains where verification is possible.
"""

from enum import Enum
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger("rsi.learning.router")


class Domain(Enum):
    """Domains for learning."""
    CODE = "code"
    MATH = "math"
    LOGIC = "logic"
    CREATIVE = "creative"
    AMBIGUOUS = "ambiguous"


class VerificationMethod(Enum):
    """How each domain verifies learning."""
    UNIT_TESTS = "unit_tests"
    SYMBOLIC = "symbolic_verification"
    CONSISTENCY = "consistency_check"
    BLOCKED = "blocked"


@dataclass
class ClassificationResult:
    """Result of domain classification."""
    primary: Domain
    confidence: float
    secondary: Optional[Domain] = None
    verification_method: VerificationMethod = VerificationMethod.BLOCKED


class DomainRouter:
    """
    Routes desires to appropriate practice domains.

    Uses weighted keyword matching with phrase patterns for accuracy.
    Conservative default: ambiguous desires are BLOCKED.
    """

    # Weighted keywords for each domain
    DOMAIN_WEIGHTS = {
        Domain.CODE: {
            "code": 1.0, "programming": 1.0, "function": 0.8,
            "debug": 0.9, "implement": 0.7, "python": 1.0,
            "api": 0.6, "class": 0.7, "method": 0.7,
            "refactor": 0.8, "test": 0.6, "bug": 0.9,
            "async": 0.8, "syntax": 0.9, "script": 0.7,
            "algorithm": 0.9, "algorithms": 0.9, "testing": 0.8,
            "unit": 0.7, "graph": 0.7, "data": 0.5, "structure": 0.5,
            "software": 0.8, "improve": 0.4, "coding": 0.9
        },
        Domain.MATH: {
            "math": 1.0, "calculate": 0.9, "equation": 1.0,
            "proof": 0.8, "theorem": 0.9, "numerical": 0.7,
            "algebra": 0.9, "geometry": 0.9, "integral": 1.0,
            "derivative": 1.0, "matrix": 0.8, "vector": 0.7
        },
        Domain.LOGIC: {
            "logic": 1.0, "logical": 0.9, "reasoning": 0.8, "deduce": 0.9,
            "infer": 0.8, "inference": 0.8, "argument": 0.7, "syllogism": 1.0,
            "prove": 0.6, "proof": 0.8, "proofs": 0.8, "conclude": 0.7, "premise": 0.9,
            "fallacy": 0.8, "valid": 0.5, "consistent": 0.6, "deduction": 0.9
        },
        Domain.CREATIVE: {
            "creative": 1.0, "write": 0.7, "story": 0.9,
            "poem": 0.9, "design": 0.6, "aesthetic": 0.8,
            "art": 0.8, "compose": 0.7, "imagine": 0.6,
            "narrative": 0.8
        }
    }

    # Phrase patterns for context-aware matching
    DOMAIN_PHRASES = {
        Domain.CODE: [
            ("python", "code"), ("debug", "function"),
            ("implement", "api"), ("async", "await"),
            ("unit", "test"), ("error", "handling"),
            ("data", "structure")
        ],
        Domain.MATH: [
            ("solve", "equation"), ("prove", "theorem"),
            ("calculate", "integral"), ("linear", "algebra"),
            ("numerical", "analysis")
        ],
        Domain.LOGIC: [
            ("multi", "step", "reasoning"), ("logical", "argument"),
            ("deduce", "from"), ("infer", "conclusion"),
            ("chain", "reasoning")
        ],
        Domain.CREATIVE: [
            ("write", "story"), ("creative", "writing"),
            ("design", "aesthetic")
        ]
    }

    # Verification methods for each domain
    VERIFICATION_METHODS = {
        Domain.CODE: VerificationMethod.UNIT_TESTS,
        Domain.MATH: VerificationMethod.SYMBOLIC,
        Domain.LOGIC: VerificationMethod.CONSISTENCY,
        Domain.CREATIVE: VerificationMethod.BLOCKED,
        Domain.AMBIGUOUS: VerificationMethod.BLOCKED
    }

    def __init__(self, memory=None):
        """Initialize router with optional memory for feedback tracking."""
        self.memory = memory
        self._classification_log: List[Dict] = []

    def classify(self, desire: Dict) -> ClassificationResult:
        """
        Classify desire into domain with confidence.

        Args:
            desire: Desire dict with 'description' field

        Returns:
            ClassificationResult with primary domain, confidence, and optional secondary
        """
        description = desire.get("description", "").lower()
        words = set(description.split())

        # Score each domain
        scores = {}
        for domain, weights in self.DOMAIN_WEIGHTS.items():
            word_score = sum(
                weight for keyword, weight in weights.items()
                if keyword in words
            )

            # Add phrase bonus
            phrase_bonus = self._score_phrases(description, domain)

            scores[domain] = word_score + phrase_bonus

        # Find best and second-best
        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        if not sorted_domains or sorted_domains[0][1] == 0:
            return ClassificationResult(
                primary=Domain.AMBIGUOUS,
                confidence=0.0,
                verification_method=VerificationMethod.BLOCKED
            )

        # Normalize confidence
        max_possible = max(sum(w.values()) for w in self.DOMAIN_WEIGHTS.values()) + 3
        primary_domain = sorted_domains[0][0]
        primary_confidence = min(1.0, sorted_domains[0][1] / max_possible)

        # Check for secondary domain
        secondary = None
        if len(sorted_domains) > 1 and sorted_domains[1][1] > 0:
            secondary_conf = sorted_domains[1][1] / max_possible
            if secondary_conf >= 0.5 * primary_confidence:
                secondary = sorted_domains[1][0]

        # Very low confidence -> ambiguous (threshold allows single strong keyword)
        if primary_confidence < 0.04:
            return ClassificationResult(
                primary=Domain.AMBIGUOUS,
                confidence=primary_confidence,
                verification_method=VerificationMethod.BLOCKED
            )

        return ClassificationResult(
            primary=primary_domain,
            confidence=primary_confidence,
            secondary=secondary,
            verification_method=self.VERIFICATION_METHODS[primary_domain]
        )

    def _score_phrases(self, text: str, domain: Domain) -> float:
        """Score based on phrase pattern matches."""
        phrases = self.DOMAIN_PHRASES.get(domain, [])
        bonus = 0.0

        for phrase in phrases:
            if all(word in text for word in phrase):
                bonus += 0.3

        return bonus

    def can_practice(self, domain: Domain) -> bool:
        """
        Check if active practice is allowed for this domain.

        The Oracle Constraint: only practice in verifiable domains.
        """
        return domain in [Domain.CODE, Domain.MATH, Domain.LOGIC]

    def get_verification_method(self, domain: Domain) -> VerificationMethod:
        """Get the verification method for a domain."""
        return self.VERIFICATION_METHODS.get(domain, VerificationMethod.BLOCKED)

    async def record_outcome(
        self,
        desire_id: str,
        predicted: Domain,
        actual_success: bool,
        notes: str = None
    ):
        """
        Record classification outcome for calibration.

        Args:
            desire_id: ID of the desire
            predicted: Predicted domain
            actual_success: Whether practice succeeded
            notes: Optional notes
        """
        from datetime import datetime

        record = {
            "desire_id": desire_id,
            "predicted_domain": predicted.value,
            "success": actual_success,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }

        self._classification_log.append(record)

        # Persist to memory for cross-session learning
        if self.memory:
            try:
                await self.memory.record_experience(
                    content=f"[DOMAIN_CLASSIFICATION] {predicted.value} -> "
                            f"{'SUCCESS' if actual_success else 'FAIL'} | {notes or ''}",
                    type="domain_classification"
                )
            except Exception as e:
                logger.warning(f"Failed to record classification: {e}")

    def get_accuracy_stats(self) -> Dict:
        """Get classification accuracy statistics."""
        if not self._classification_log:
            return {"total": 0, "accuracy": 0.0}

        total = len(self._classification_log)
        successes = sum(1 for r in self._classification_log if r["success"])

        return {
            "total": total,
            "accuracy": successes / total,
            "by_domain": self._get_domain_stats()
        }

    def _get_domain_stats(self) -> Dict:
        """Get per-domain accuracy stats."""
        stats = {}
        for record in self._classification_log:
            domain = record["predicted_domain"]
            if domain not in stats:
                stats[domain] = {"total": 0, "success": 0}
            stats[domain]["total"] += 1
            if record["success"]:
                stats[domain]["success"] += 1

        # Calculate accuracy per domain
        for domain in stats:
            total = stats[domain]["total"]
            success = stats[domain]["success"]
            stats[domain]["accuracy"] = success / total if total > 0 else 0.0

        return stats

    def reset(self):
        """Reset router state."""
        self._classification_log.clear()

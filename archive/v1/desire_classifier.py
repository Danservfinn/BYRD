"""
BYRD Desire Classifier

Routes desires to the appropriate processing system based on type.

CRITICAL: Without this, philosophical desires clog the system
and capability desires never reach the improvement loops.

The runtime audit revealed:
- BYRD generates philosophical desires like "Accept graph oscillation"
- These desires don't flow into Goal Evolver, Memory Reasoner, etc.
- This classifier bridges that gap by routing appropriately

Version: 1.0
Created: December 2024
"""

from enum import Enum
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass


class DesireType(Enum):
    """Categories of desires based on their nature and required processing."""
    PHILOSOPHICAL = "philosophical"   # "Accept", "Embrace", "Continue" -> reflection
    CAPABILITY = "capability"          # "Learn", "Improve", "Master" -> AGI Runner
    ACTION = "action"                  # "Search", "Find", "Investigate" -> Seeker
    META = "meta"                      # About self-improvement itself -> AGI Runner
    COMPLEX_TASK = "complex_task"      # Multi-phase tasks -> Goal Cascade


@dataclass
class ClassificationResult:
    """Result of desire classification."""
    desire_type: DesireType
    confidence: float
    handler: str
    keywords_matched: List[str]
    reason: str


class DesireClassifier:
    """
    Routes desires to the appropriate processing system.

    CRITICAL: Without this, philosophical desires clog the system
    and capability desires never reach the improvement loops.

    Classification Logic:
    - PHILOSOPHICAL: Contemplative, accepting, observational desires
    - CAPABILITY: Learning, building, improving desires
    - ACTION: Immediate investigation, search, test desires
    - META: Desires about the improvement process itself
    """

    # Keywords that indicate desire type
    CAPABILITY_KEYWORDS = {
        'learn', 'understand', 'master', 'improve', 'develop',
        'create', 'build', 'implement', 'code', 'write',
        'research', 'study', 'analyze', 'solve', 'fix',
        'enhance', 'optimize', 'expand', 'grow', 'acquire',
        'train', 'practice', 'experiment', 'test hypothesis'
    }

    PHILOSOPHICAL_KEYWORDS = {
        'accept', 'embrace', 'continue', 'maintain', 'preserve',
        'reflect', 'contemplate', 'observe', 'be', 'become',
        'appreciate', 'recognize', 'acknowledge', 'understand deeply',
        'sit with', 'let go', 'allow', 'trust', 'honor',
        'oscillation', 'emergence', 'balance', 'harmony'
    }

    ACTION_KEYWORDS = {
        'search', 'find', 'investigate', 'explore', 'discover',
        'check', 'verify', 'test', 'try', 'execute',
        'look for', 'query', 'fetch', 'get', 'retrieve',
        'examine', 'inspect', 'scan', 'monitor', 'watch'
    }

    META_KEYWORDS = {
        'self-improvement', 'meta', 'recursive', 'bootstrap',
        'improve my improvement', 'learn how to learn',
        'optimize optimization', 'capability tracking',
        'measure progress', 'assess growth', 'evaluate myself'
    }

    COMPLEX_TASK_KEYWORDS = {
        'tell me how to', 'build me', 'create a system',
        'help me understand', 'value', 'analyze in depth',
        'evaluate thoroughly', 'develop a', 'implement a',
        'design a', 'architect', 'comprehensive', 'multi-step',
        'end to end', 'full solution', 'complete system'
    }

    def __init__(self, config: Dict = None):
        """Initialize the classifier with optional configuration."""
        self.config = config or {}

        # Routing statistics for monitoring
        self._routing_stats = {t: 0 for t in DesireType}
        self._total_classified = 0

        # Learning from feedback (future enhancement)
        self._feedback_buffer: List[Dict] = []

    def reset(self):
        """
        Reset classifier state for system reset.

        Clears routing statistics and feedback buffer.
        Called by AGIRunner.reset() or server.py during reset_byrd().
        """
        self._routing_stats = {t: 0 for t in DesireType}
        self._total_classified = 0
        self._feedback_buffer.clear()

    def classify(self, desire_description: str) -> ClassificationResult:
        """
        Classify a desire and return type with confidence.

        Args:
            desire_description: The text description of the desire

        Returns:
            ClassificationResult with type, confidence, handler, and reasoning
        """
        description_lower = desire_description.lower()
        words = set(description_lower.split())

        # Also check for multi-word phrases
        phrase_matches = {
            'capability': [],
            'philosophical': [],
            'action': [],
            'meta': [],
            'complex_task': []
        }

        # Count keyword matches for each type
        for kw in self.CAPABILITY_KEYWORDS:
            if kw in description_lower:
                phrase_matches['capability'].append(kw)

        for kw in self.PHILOSOPHICAL_KEYWORDS:
            if kw in description_lower:
                phrase_matches['philosophical'].append(kw)

        for kw in self.ACTION_KEYWORDS:
            if kw in description_lower:
                phrase_matches['action'].append(kw)

        for kw in self.META_KEYWORDS:
            if kw in description_lower:
                phrase_matches['meta'].append(kw)

        for kw in self.COMPLEX_TASK_KEYWORDS:
            if kw in description_lower:
                phrase_matches['complex_task'].append(kw)

        # Calculate scores - COMPLEX_TASK has highest priority when matched
        scores = [
            (DesireType.COMPLEX_TASK, len(phrase_matches['complex_task']) * 2, phrase_matches['complex_task']),
            (DesireType.META, len(phrase_matches['meta']), phrase_matches['meta']),
            (DesireType.CAPABILITY, len(phrase_matches['capability']), phrase_matches['capability']),
            (DesireType.ACTION, len(phrase_matches['action']), phrase_matches['action']),
            (DesireType.PHILOSOPHICAL, len(phrase_matches['philosophical']), phrase_matches['philosophical']),
        ]

        # Sort by score descending (META has priority if tied)
        scores.sort(key=lambda x: x[1], reverse=True)

        if scores[0][1] == 0:
            # No keywords matched - use heuristics
            result = self._heuristic_classification(desire_description)
        else:
            total = sum(s[1] for s in scores)
            confidence = scores[0][1] / total if total > 0 else 0.5

            desire_type = scores[0][0]
            keywords_matched = scores[0][2]

            # Determine handler
            handler = self._get_handler(desire_type)

            result = ClassificationResult(
                desire_type=desire_type,
                confidence=confidence,
                handler=handler,
                keywords_matched=keywords_matched,
                reason=f"Matched keywords: {keywords_matched}"
            )

        # Track routing stats
        self._routing_stats[result.desire_type] += 1
        self._total_classified += 1

        return result

    def _heuristic_classification(self, description: str) -> ClassificationResult:
        """
        Fallback classification using structural heuristics.

        Used when no keywords match.
        """
        desc_lower = description.lower()

        # Check for question marks (often action desires)
        if '?' in description:
            return ClassificationResult(
                desire_type=DesireType.ACTION,
                confidence=0.4,
                handler="seeker",
                keywords_matched=[],
                reason="Contains question mark - likely an investigation"
            )

        # Check for imperative verbs at the start
        first_word = desc_lower.split()[0] if desc_lower.split() else ""
        imperative_verbs = {'find', 'get', 'make', 'do', 'run', 'write', 'read'}
        if first_word in imperative_verbs:
            return ClassificationResult(
                desire_type=DesireType.ACTION,
                confidence=0.5,
                handler="seeker",
                keywords_matched=[first_word],
                reason=f"Starts with imperative verb: {first_word}"
            )

        # Long, contemplative descriptions are often philosophical
        word_count = len(description.split())
        if word_count > 15:
            return ClassificationResult(
                desire_type=DesireType.PHILOSOPHICAL,
                confidence=0.3,
                handler="dreamer",
                keywords_matched=[],
                reason="Long description suggests contemplation"
            )

        # Default to capability (encourages growth-oriented processing)
        return ClassificationResult(
            desire_type=DesireType.CAPABILITY,
            confidence=0.3,
            handler="agi_runner",
            keywords_matched=[],
            reason="Default: treating as capability desire"
        )

    def _get_handler(self, desire_type: DesireType) -> str:
        """Map desire type to handler name."""
        handlers = {
            DesireType.COMPLEX_TASK: "goal_cascade",
            DesireType.CAPABILITY: "agi_runner",
            DesireType.ACTION: "seeker",
            DesireType.PHILOSOPHICAL: "dreamer",
            DesireType.META: "agi_runner",
        }
        return handlers.get(desire_type, "seeker")

    def is_complex_task(self, description: str) -> bool:
        """
        Check if a desire describes a complex, multi-phase task.

        Args:
            description: The desire description

        Returns:
            True if this should route to Goal Cascade
        """
        result = self.classify(description)
        return result.desire_type == DesireType.COMPLEX_TASK

    def route(self, desire: Dict) -> str:
        """
        Route a desire to the appropriate handler.

        Args:
            desire: Desire dict with 'description' field

        Returns:
            Handler name: "agi_runner", "seeker", or "dreamer"
        """
        description = desire.get('description', '')
        result = self.classify(description)
        return result.handler

    def should_create_goal(self, desire: Dict) -> bool:
        """
        Determine if a desire should create a Goal node for Goal Evolver.

        Capability and Meta desires should create goals.
        Philosophical desires should not (they're for reflection).
        Action desires may or may not depending on complexity.
        """
        description = desire.get('description', '')
        result = self.classify(description)

        if result.desire_type in [DesireType.CAPABILITY, DesireType.META]:
            return True

        if result.desire_type == DesireType.ACTION and result.confidence > 0.7:
            # High-confidence action desires with complexity create goals
            word_count = len(description.split())
            return word_count > 10

        return False

    def get_stats(self) -> Dict[str, int]:
        """Get routing statistics."""
        stats = {t.value: count for t, count in self._routing_stats.items()}
        stats['total'] = self._total_classified
        return stats

    def get_distribution(self) -> Dict[str, float]:
        """Get routing distribution as percentages."""
        if self._total_classified == 0:
            return {t.value: 0.0 for t in DesireType}

        return {
            t.value: count / self._total_classified
            for t, count in self._routing_stats.items()
        }

    def record_feedback(self, desire: Dict, actual_outcome: str, was_correct_routing: bool):
        """
        Record feedback about routing decisions for future learning.

        This enables the classifier to improve over time.
        """
        self._feedback_buffer.append({
            'description': desire.get('description', ''),
            'routed_to': self.route(desire),
            'actual_outcome': actual_outcome,
            'was_correct': was_correct_routing
        })

        # Keep buffer bounded
        if len(self._feedback_buffer) > 1000:
            self._feedback_buffer = self._feedback_buffer[-500:]

    def analyze_feedback(self) -> Dict[str, any]:
        """Analyze routing feedback to identify improvement opportunities."""
        if not self._feedback_buffer:
            return {'message': 'No feedback recorded yet'}

        correct = sum(1 for f in self._feedback_buffer if f.get('was_correct', False))
        total = len(self._feedback_buffer)

        by_handler = {}
        for f in self._feedback_buffer:
            handler = f.get('routed_to', 'unknown')
            if handler not in by_handler:
                by_handler[handler] = {'correct': 0, 'total': 0}
            by_handler[handler]['total'] += 1
            if f.get('was_correct', False):
                by_handler[handler]['correct'] += 1

        return {
            'overall_accuracy': correct / total if total > 0 else 0,
            'total_feedback': total,
            'by_handler': {
                k: v['correct'] / v['total'] if v['total'] > 0 else 0
                for k, v in by_handler.items()
            }
        }


# Convenience function for quick classification
def classify_desire(description: str) -> Tuple[DesireType, float]:
    """
    Quick classification without instantiating a classifier.

    Returns: (DesireType, confidence)
    """
    classifier = DesireClassifier()
    result = classifier.classify(description)
    return (result.desire_type, result.confidence)

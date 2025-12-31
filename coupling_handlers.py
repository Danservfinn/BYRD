"""
Actual implementations for loop coupling handlers.

These are not stubs - they contain real logic that produces
real effects on BYRD's learning and behavior.

Based on IMPLEMENTATION_PLAN_v2.md Phase 2.

Handlers implemented:
1. Goal Success -> Pattern Extraction (Goal Evolver -> Self-Compiler)
2. Pattern Codified -> Memory Index (Self-Compiler -> Memory Reasoner)
3. Memory Answer -> Counterfactual Seed (Memory Reasoner -> Dreaming Machine)
4. Counterfactual Insight -> Goal Proposal (Dreaming Machine -> Goal Evolver)
"""

import json
import re
import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ExtractedPattern:
    """A pattern extracted from a successful goal."""
    id: str
    description: str
    preconditions: List[str]
    actions: List[str]
    postconditions: List[str]
    success_indicators: List[str]
    confidence: float
    source_goal_id: str
    created_at: float


@dataclass
class ProposedGoal:
    """A goal proposed from a counterfactual insight."""
    description: str
    rationale: str
    source_insight: str
    estimated_value: float
    prerequisites: List[str]


class CouplingHandlers:
    """
    Implementations for all coupling handlers.

    This class provides the actual logic that makes loop
    coupling meaningful, not just event passing.
    """

    def __init__(self, memory, llm_client, config: Dict = None):
        self.memory = memory
        self.llm_client = llm_client
        config = config or {}

        # Pattern storage
        self._patterns: Dict[str, ExtractedPattern] = {}
        self._pattern_applications: Dict[str, List[Dict]] = {}  # pattern_id -> applications
        self._max_patterns = config.get("max_patterns", 100)
        self._min_confidence = config.get("pattern_min_confidence", 0.5)

        # Counterfactual queue
        self._counterfactual_queue: List[Dict] = []
        self._max_queue_size = config.get("max_counterfactual_queue", 50)

        # Metrics
        self._patterns_extracted = 0
        self._patterns_applied = 0
        self._goals_proposed = 0
        self._counterfactuals_processed = 0

    # ========================================
    # HANDLER 1: Goal Success -> Pattern Extraction
    # (Goal Evolver -> Self-Compiler)
    # ========================================

    async def extract_pattern_from_success(
        self,
        goal_description: str,
        outcome: Dict[str, Any]
    ) -> Optional[ExtractedPattern]:
        """
        Extract a reusable pattern from a successful goal.

        This is ACTUAL pattern extraction using LLM reasoning,
        not a stub that returns None.
        """
        if not self.llm_client:
            return None

        # Get context: what experiences led to this success?
        related_experiences = []
        if self.memory:
            try:
                related_experiences = await self.memory.get_recent_experiences(limit=10)
            except Exception:
                pass

        # Format experiences for analysis
        exp_text = "\n".join([
            f"- {exp.get('content', '')[:200]}"
            for exp in related_experiences
        ]) if related_experiences else "No related experiences found."

        # Use LLM to extract pattern
        prompt = f"""Analyze this successful goal and extract a reusable pattern.

GOAL: {goal_description}

OUTCOME:
- Fitness: {outcome.get('fitness', 'unknown')}
- Capability Delta: {outcome.get('capability_delta', 'unknown')}
- Efficiency: {outcome.get('efficiency', 'unknown')}

RELATED EXPERIENCES:
{exp_text}

Extract a reusable pattern in this JSON format:
{{
    "description": "Brief description of what this pattern accomplishes",
    "preconditions": ["condition that must be true before applying"],
    "actions": ["specific action to take"],
    "postconditions": ["expected state after successful application"],
    "success_indicators": ["how to know if it worked"],
    "generalizability": 0.0-1.0
}}

JSON pattern:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.3,
                max_tokens=500,
                operation="pattern_extraction"
            )

            # Handle LLMResponse object
            text = response.text if hasattr(response, 'text') else str(response)

            # Parse JSON from response
            pattern_data = self._parse_json(text)

            if not pattern_data or not pattern_data.get("description"):
                return None

            # Validate pattern has meaningful content
            if not self._is_valid_pattern(pattern_data):
                return None

            # Check confidence threshold
            confidence = pattern_data.get("generalizability", 0.5)
            if confidence < self._min_confidence:
                return None

            # Create pattern object
            pattern = ExtractedPattern(
                id=str(uuid.uuid4())[:8],
                description=pattern_data["description"],
                preconditions=pattern_data.get("preconditions", []),
                actions=pattern_data.get("actions", []),
                postconditions=pattern_data.get("postconditions", []),
                success_indicators=pattern_data.get("success_indicators", []),
                confidence=confidence,
                source_goal_id=outcome.get("goal_id", ""),
                created_at=time.time()
            )

            # Store pattern (with limit)
            if len(self._patterns) >= self._max_patterns:
                # Remove oldest pattern
                oldest_id = min(self._patterns.keys(), key=lambda k: self._patterns[k].created_at)
                del self._patterns[oldest_id]

            self._patterns[pattern.id] = pattern
            self._patterns_extracted += 1

            # Store in memory for retrieval
            if self.memory:
                await self.memory.record_experience(
                    content=f"[PATTERN_EXTRACTED] {pattern.description}",
                    type="pattern"
                )

            return pattern

        except Exception as e:
            print(f"   Pattern extraction failed: {e}")
            return None

    def _is_valid_pattern(self, pattern_data: Dict) -> bool:
        """Validate that a pattern has meaningful content."""
        # Must have description
        if not pattern_data.get("description") or len(pattern_data["description"]) < 10:
            return False

        # Must have at least one action
        if not pattern_data.get("actions") or len(pattern_data["actions"]) == 0:
            return False

        # Actions shouldn't be too generic
        generic_actions = ["try", "do", "make", "be"]
        for action in pattern_data.get("actions", []):
            if action.lower().strip() in generic_actions:
                return False

        return True

    # ========================================
    # HANDLER 2: Pattern Codified -> Memory Index
    # (Self-Compiler -> Memory Reasoner)
    # ========================================

    async def index_pattern(self, pattern: ExtractedPattern) -> bool:
        """
        Index a pattern for retrieval by Memory Reasoner.

        Creates searchable representation of the pattern
        that can be found during spreading activation.
        """
        if not self.memory:
            return False

        try:
            # Create a searchable node for the pattern
            pattern_content = f"""REUSABLE PATTERN: {pattern.description}

WHEN TO USE (Preconditions):
{chr(10).join('- ' + p for p in pattern.preconditions)}

WHAT TO DO (Actions):
{chr(10).join('- ' + a for a in pattern.actions)}

EXPECTED RESULTS (Postconditions):
{chr(10).join('- ' + p for p in pattern.postconditions)}

SUCCESS INDICATORS:
{chr(10).join('- ' + s for s in pattern.success_indicators)}"""

            # Store as experience with pattern type
            await self.memory.record_experience(
                content=f"[PATTERN_INDEXED] {pattern_content}",
                type="indexed_pattern"
            )

            return True

        except Exception as e:
            print(f"   Pattern indexing failed: {e}")
            return False

    async def find_applicable_pattern(
        self,
        situation: str,
        goal: str = None
    ) -> Optional[ExtractedPattern]:
        """
        Find a pattern applicable to the current situation.

        This is used by Seeker to apply learned patterns.
        """
        if not self._patterns:
            return None

        if not self.llm_client:
            # Fallback: return highest confidence pattern
            return max(self._patterns.values(), key=lambda p: p.confidence)

        # Use LLM to match situation to patterns
        patterns_desc = "\n\n".join([
            f"Pattern {p.id}:\n  Description: {p.description}\n  Preconditions: {p.preconditions}"
            for p in self._patterns.values()
        ])

        prompt = f"""Given this situation, which pattern (if any) applies?

SITUATION: {situation}
GOAL: {goal or 'not specified'}

AVAILABLE PATTERNS:
{patterns_desc}

If a pattern applies, respond with its ID. If none apply, respond "none".
Pattern ID:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.1,
                max_tokens=20,
                operation="pattern_matching"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            text = text.strip().lower()

            if text == "none" or not text:
                return None

            # Find pattern by ID
            for pattern_id, pattern in self._patterns.items():
                if pattern_id in text:
                    self._patterns_applied += 1
                    return pattern

            return None

        except Exception:
            return None

    # ========================================
    # HANDLER 3: Memory Answer -> Counterfactual Seed
    # (Memory Reasoner -> Dreaming Machine)
    # ========================================

    async def queue_counterfactual_seed(
        self,
        query: str,
        answer: str,
        confidence: float = 0.5
    ) -> bool:
        """
        Queue a memory answer as a seed for counterfactual generation.

        Low-confidence answers are especially valuable seeds
        because they represent uncertainty worth exploring.
        """
        seed = {
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "timestamp": time.time(),
            "explored": False
        }

        # Prioritize low-confidence answers (more room for exploration)
        if confidence < 0.6:
            self._counterfactual_queue.insert(0, seed)
        else:
            self._counterfactual_queue.append(seed)

        # Trim queue
        if len(self._counterfactual_queue) > self._max_queue_size:
            self._counterfactual_queue = self._counterfactual_queue[:self._max_queue_size]

        return True

    async def generate_counterfactual(self, seed: Dict = None) -> Optional[Dict]:
        """
        Generate a counterfactual from a queued seed.

        Called by Dreaming Machine during dream cycles.
        """
        if not self.llm_client:
            return None

        # Get seed from queue if not provided
        if seed is None:
            unexplored = [s for s in self._counterfactual_queue if not s.get("explored")]
            if not unexplored:
                return None
            seed = unexplored[0]

        prompt = f"""Generate a counterfactual exploration of this knowledge.

ORIGINAL QUERY: {seed['query']}
ORIGINAL ANSWER: {seed['answer']}
CONFIDENCE: {seed['confidence']}

Consider: What if the answer were different? What alternative explanations exist?
What would change if a key assumption were wrong?

Generate a counterfactual analysis:
{{
    "alternative_answer": "What could the answer be instead?",
    "key_assumption": "What assumption does the original answer rely on?",
    "what_if": "What if that assumption were false?",
    "implications": ["What would follow from the alternative?"],
    "testable_prediction": "How could we tell which is correct?",
    "insight": "What did we learn from this exploration?"
}}

JSON:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.7,  # Higher temperature for creativity
                max_tokens=400,
                operation="counterfactual_generation"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            counterfactual = self._parse_json(text)

            if counterfactual and counterfactual.get("insight"):
                # Mark seed as explored
                seed["explored"] = True
                self._counterfactuals_processed += 1

                # Store counterfactual in memory
                if self.memory:
                    await self.memory.record_experience(
                        content=f"[COUNTERFACTUAL] {counterfactual.get('what_if', '')}\nINSIGHT: {counterfactual.get('insight', '')}",
                        type="counterfactual"
                    )

                return counterfactual

            return None

        except Exception as e:
            print(f"   Counterfactual generation failed: {e}")
            return None

    # ========================================
    # HANDLER 4: Counterfactual Insight -> Goal Proposal
    # (Dreaming Machine -> Goal Evolver)
    # ========================================

    async def propose_goal_from_insight(
        self,
        insight: str,
        proposed_goal: str = None
    ) -> Optional[ProposedGoal]:
        """
        Convert a counterfactual insight into a proposed goal.

        Insights that reveal gaps or opportunities should
        generate goals to address them.
        """
        if not self.llm_client:
            return None

        # If no goal explicitly proposed, generate one from insight
        if not proposed_goal:
            prompt = f"""Convert this insight into an actionable goal.

INSIGHT: {insight}

What goal would help act on or verify this insight?

Goal (one sentence, actionable):"""

            try:
                response = await self.llm_client.generate(
                    prompt,
                    temperature=0.5,
                    max_tokens=100,
                    operation="insight_to_goal"
                )
                text = response.text if hasattr(response, 'text') else str(response)
                proposed_goal = text.strip()
            except Exception:
                return None

        if not proposed_goal or len(proposed_goal) < 10:
            return None

        # Evaluate the goal
        eval_prompt = f"""Evaluate this proposed goal:

GOAL: {proposed_goal}
DERIVED FROM INSIGHT: {insight}

Rate on:
1. Actionability (0-1): Can this actually be pursued?
2. Value (0-1): Is this worth pursuing?
3. Prerequisites: What must be true first?

JSON:
{{
    "actionability": 0.0-1.0,
    "value": 0.0-1.0,
    "prerequisites": ["..."],
    "rationale": "Why this goal matters"
}}

JSON:"""

        try:
            response = await self.llm_client.generate(
                eval_prompt,
                temperature=0.3,
                max_tokens=200,
                operation="goal_evaluation"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            eval_data = self._parse_json(text)

            if not eval_data:
                return None

            # Only propose goals that pass threshold
            actionability = eval_data.get("actionability", 0)
            value = eval_data.get("value", 0)

            if actionability < 0.5 or value < 0.4:
                return None

            goal = ProposedGoal(
                description=proposed_goal,
                rationale=eval_data.get("rationale", ""),
                source_insight=insight,
                estimated_value=value,
                prerequisites=eval_data.get("prerequisites", [])
            )

            # Store proposed goal in memory
            if self.memory:
                await self.memory.record_experience(
                    content=f"[GOAL_PROPOSED] {goal.description}\nRationale: {goal.rationale}",
                    type="proposed_goal"
                )

            self._goals_proposed += 1

            return goal

        except Exception as e:
            print(f"   Goal proposal failed: {e}")
            return None

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _parse_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response."""
        try:
            # Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON in text
        try:
            # Find JSON-like content
            match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass

        # Try to find JSON with nested braces
        try:
            start = text.find('{')
            if start >= 0:
                depth = 0
                for i, c in enumerate(text[start:], start):
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            return json.loads(text[start:i+1])
        except Exception:
            pass

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics."""
        return {
            "patterns_extracted": self._patterns_extracted,
            "patterns_stored": len(self._patterns),
            "patterns_applied": self._patterns_applied,
            "counterfactual_queue_size": len(self._counterfactual_queue),
            "counterfactuals_processed": self._counterfactuals_processed,
            "goals_proposed": self._goals_proposed
        }

    def reset(self):
        """Reset handler state."""
        self._patterns.clear()
        self._pattern_applications.clear()
        self._counterfactual_queue.clear()
        self._patterns_extracted = 0
        self._patterns_applied = 0
        self._goals_proposed = 0
        self._counterfactuals_processed = 0

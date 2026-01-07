"""
Complexity-Aware Orchestration (CAO).

Implements complexity detection and agent routing based on
Apple and DeepMind research findings:
- Apple: Multi-agent performance collapses above 45% complexity
- DeepMind: Beyond 45% predicted accuracy, more agents = worse

See docs/IMPLEMENTATION_PLAN.md Phase 1.2 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio
import math

logger = logging.getLogger("rsi.orchestration.cao")


class TaskComplexity(Enum):
    """Complexity levels for task classification."""
    TRIVIAL = "trivial"       # < 15% - Single agent, fast path
    LOW = "low"               # 15-30% - Single agent, normal
    MODERATE = "moderate"     # 30-45% - Multi-agent consideration
    HIGH = "high"             # 45-60% - Decompose first
    EXTREME = "extreme"       # > 60% - Deep decomposition


class DecompositionStrategy(Enum):
    """Strategies for task decomposition."""
    NONE = "none"                     # No decomposition needed
    SEQUENTIAL = "sequential"         # Chain of simpler subtasks
    PARALLEL = "parallel"             # Independent subtasks
    HIERARCHICAL = "hierarchical"     # Tree of subtasks
    RECURSIVE = "recursive"           # Self-similar decomposition


class AgentStrategy(Enum):
    """Agent allocation strategies."""
    SINGLE = "single"           # Single agent handles task
    MULTI_DEBATE = "debate"     # Multiple agents debate
    MULTI_PARALLEL = "parallel" # Multiple agents in parallel
    ENSEMBLE = "ensemble"       # Ensemble voting


@dataclass
class Task:
    """A task to be orchestrated."""
    id: str
    description: str
    capability: str
    context: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    subtask_ids: List[str] = field(default_factory=list)
    estimated_complexity: float = 0.0
    actual_complexity: Optional[float] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'description': self.description,
            'capability': self.capability,
            'context': self.context,
            'parent_id': self.parent_id,
            'subtask_ids': self.subtask_ids,
            'estimated_complexity': self.estimated_complexity,
            'actual_complexity': self.actual_complexity
        }


@dataclass
class ComplexityEstimate:
    """Result of complexity estimation."""
    task_id: str
    complexity_score: float  # 0-1
    complexity_level: TaskComplexity
    confidence: float
    features: Dict[str, float]  # Contributing factors
    recommendation: DecompositionStrategy
    reasons: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'task_id': self.task_id,
            'complexity_score': self.complexity_score,
            'complexity_level': self.complexity_level.value,
            'confidence': self.confidence,
            'features': self.features,
            'recommendation': self.recommendation.value,
            'reasons': self.reasons
        }


@dataclass
class RoutingDecision:
    """Decision on how to route a task."""
    task_id: str
    strategy: AgentStrategy
    agent_count: int
    decompose_first: bool
    decomposition_strategy: DecompositionStrategy
    predicted_success: float
    reasons: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'task_id': self.task_id,
            'strategy': self.strategy.value,
            'agent_count': self.agent_count,
            'decompose_first': self.decompose_first,
            'decomposition_strategy': self.decomposition_strategy.value,
            'predicted_success': self.predicted_success,
            'reasons': self.reasons,
            'metadata': self.metadata
        }


class ComplexityDetector:
    """
    Detects task complexity to inform orchestration decisions.

    Uses multiple heuristics and optional LLM estimation to
    determine task complexity before execution.
    """

    # Research-validated threshold
    COLLAPSE_THRESHOLD = 0.45  # From Apple research

    def __init__(self, config: Dict = None, llm_client=None):
        """Initialize complexity detector."""
        self.config = config or {}
        self.llm_client = llm_client

        # Feature weights for complexity estimation
        self.weights = self.config.get('weights', {
            'description_length': 0.1,
            'context_depth': 0.15,
            'capability_novelty': 0.2,
            'interdependency': 0.2,
            'ambiguity': 0.15,
            'domain_breadth': 0.2,
        })

        # Calibration history
        self._estimates: List[Dict] = []
        self._actuals: List[Dict] = []

    async def estimate_complexity(self, task: Task) -> ComplexityEstimate:
        """
        Estimate task complexity.

        Args:
            task: The task to estimate

        Returns:
            ComplexityEstimate with score and recommendations
        """
        features = await self._compute_features(task)

        # Weighted sum
        score = sum(
            features.get(f, 0) * w
            for f, w in self.weights.items()
        )
        score = max(0.0, min(1.0, score))

        # Classify complexity level
        level = self._classify_level(score)

        # Determine recommendation
        recommendation = self._recommend_decomposition(score, level)

        # Build reasons
        reasons = self._generate_reasons(features, score, level)

        # Confidence based on feature coverage
        confidence = len([v for v in features.values() if v > 0]) / len(self.weights)

        estimate = ComplexityEstimate(
            task_id=task.id,
            complexity_score=score,
            complexity_level=level,
            confidence=confidence,
            features=features,
            recommendation=recommendation,
            reasons=reasons
        )

        # Store for calibration
        self._estimates.append({
            'task_id': task.id,
            'estimate': score,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

        task.estimated_complexity = score

        return estimate

    async def should_decompose(self, task: Task) -> bool:
        """Quick check if task needs decomposition."""
        estimate = await self.estimate_complexity(task)
        return estimate.complexity_score > self.COLLAPSE_THRESHOLD

    def record_actual(self, task_id: str, actual_complexity: float) -> None:
        """Record actual complexity for calibration."""
        self._actuals.append({
            'task_id': task_id,
            'actual': actual_complexity,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

    def get_calibration_error(self) -> Optional[float]:
        """Get mean calibration error."""
        if not self._actuals:
            return None

        # Match estimates with actuals
        errors = []
        for actual in self._actuals:
            for est in self._estimates:
                if est['task_id'] == actual['task_id']:
                    errors.append(abs(est['estimate'] - actual['actual']))
                    break

        if not errors:
            return None

        return sum(errors) / len(errors)

    async def _compute_features(self, task: Task) -> Dict[str, float]:
        """Compute complexity features for a task."""
        features = {}

        # Description length (longer = more complex)
        desc_len = len(task.description)
        features['description_length'] = min(1.0, desc_len / 500)

        # Context depth (nested context = more complex)
        features['context_depth'] = self._measure_context_depth(task.context)

        # Capability novelty (novel capability = more complex)
        features['capability_novelty'] = self._estimate_novelty(task.capability)

        # Interdependency (many subtasks = more complex)
        features['interdependency'] = min(1.0, len(task.subtask_ids) / 5)

        # Ambiguity (vague language = more complex)
        features['ambiguity'] = self._estimate_ambiguity(task.description)

        # Domain breadth (multi-domain = more complex)
        features['domain_breadth'] = self._estimate_domain_breadth(task)

        return features

    def _measure_context_depth(self, context: Dict) -> float:
        """Measure nesting depth of context."""
        def depth(obj, current=0):
            if isinstance(obj, dict):
                if not obj:
                    return current
                return max(depth(v, current + 1) for v in obj.values())
            elif isinstance(obj, list):
                if not obj:
                    return current
                return max(depth(v, current + 1) for v in obj)
            return current

        d = depth(context)
        return min(1.0, d / 5)

    def _estimate_novelty(self, capability: str) -> float:
        """Estimate capability novelty (placeholder)."""
        # In a full implementation, this would check against known capabilities
        # For now, use simple heuristics
        known_simple = ['reasoning', 'coding', 'analysis']
        known_complex = ['meta-learning', 'self-modification', 'architecture']

        cap_lower = capability.lower()

        if any(k in cap_lower for k in known_simple):
            return 0.3
        if any(k in cap_lower for k in known_complex):
            return 0.8

        return 0.5  # Unknown = moderate

    def _estimate_ambiguity(self, description: str) -> float:
        """Estimate ambiguity in task description."""
        # Ambiguity indicators
        ambiguous_words = [
            'maybe', 'might', 'could', 'possibly', 'perhaps',
            'sometimes', 'usually', 'often', 'generally',
            'appropriate', 'suitable', 'reasonable'
        ]

        desc_lower = description.lower()
        count = sum(1 for w in ambiguous_words if w in desc_lower)

        return min(1.0, count / 3)

    def _estimate_domain_breadth(self, task: Task) -> float:
        """Estimate how many domains the task spans."""
        domains = ['code', 'reasoning', 'planning', 'learning',
                   'memory', 'safety', 'economic', 'creative']

        desc_lower = task.description.lower()
        cap_lower = task.capability.lower()

        domain_count = sum(1 for d in domains
                          if d in desc_lower or d in cap_lower)

        return min(1.0, domain_count / 3)

    def _classify_level(self, score: float) -> TaskComplexity:
        """Classify complexity level from score."""
        if score < 0.15:
            return TaskComplexity.TRIVIAL
        elif score < 0.30:
            return TaskComplexity.LOW
        elif score < 0.45:
            return TaskComplexity.MODERATE
        elif score < 0.60:
            return TaskComplexity.HIGH
        else:
            return TaskComplexity.EXTREME

    def _recommend_decomposition(
        self,
        score: float,
        level: TaskComplexity
    ) -> DecompositionStrategy:
        """Recommend decomposition strategy."""
        if level in [TaskComplexity.TRIVIAL, TaskComplexity.LOW]:
            return DecompositionStrategy.NONE

        if level == TaskComplexity.MODERATE:
            return DecompositionStrategy.SEQUENTIAL

        if level == TaskComplexity.HIGH:
            return DecompositionStrategy.HIERARCHICAL

        return DecompositionStrategy.RECURSIVE

    def _generate_reasons(
        self,
        features: Dict[str, float],
        score: float,
        level: TaskComplexity
    ) -> List[str]:
        """Generate human-readable reasons for estimate."""
        reasons = []

        # Top contributing features
        sorted_features = sorted(
            features.items(),
            key=lambda x: x[1] * self.weights.get(x[0], 0),
            reverse=True
        )

        for feature, value in sorted_features[:3]:
            if value > 0.3:
                reasons.append(f"High {feature.replace('_', ' ')}: {value:.1%}")

        if score > self.COLLAPSE_THRESHOLD:
            reasons.append(f"Above collapse threshold ({self.COLLAPSE_THRESHOLD:.0%})")

        return reasons


class AgentRouter:
    """
    Routes tasks to appropriate agent configuration.

    Based on DeepMind finding: above 45% predicted accuracy,
    adding more agents degrades performance.
    """

    # Multi-agent only beneficial below this threshold
    MULTI_AGENT_THRESHOLD = 0.45

    def __init__(self, config: Dict = None):
        """Initialize agent router."""
        self.config = config or {}

        # Statistics
        self._routing_decisions: int = 0
        self._single_agent_count: int = 0
        self._multi_agent_count: int = 0

    async def route(
        self,
        task: Task,
        complexity_estimate: ComplexityEstimate
    ) -> RoutingDecision:
        """
        Determine optimal agent strategy for task.

        Args:
            task: The task to route
            complexity_estimate: Complexity analysis

        Returns:
            RoutingDecision with strategy and parameters
        """
        self._routing_decisions += 1

        score = complexity_estimate.complexity_score
        level = complexity_estimate.complexity_level

        # Predict success probability (inverse of complexity)
        predicted_success = 1.0 - score

        # Determine if decomposition needed
        decompose_first = score > self.MULTI_AGENT_THRESHOLD
        decomposition = complexity_estimate.recommendation

        # Determine agent strategy
        if predicted_success < self.MULTI_AGENT_THRESHOLD:
            # Below threshold: multi-agent can help
            strategy = AgentStrategy.MULTI_DEBATE
            agent_count = min(3, max(2, int(3 * score)))
            self._multi_agent_count += 1
            reasons = [
                f"Predicted success {predicted_success:.1%} < {self.MULTI_AGENT_THRESHOLD:.0%}",
                "Multi-agent debate recommended"
            ]
        else:
            # Above threshold: single agent better
            strategy = AgentStrategy.SINGLE
            agent_count = 1
            self._single_agent_count += 1
            reasons = [
                f"Predicted success {predicted_success:.1%} >= {self.MULTI_AGENT_THRESHOLD:.0%}",
                "Single agent recommended (multi-agent would degrade)"
            ]

        # Override for extreme complexity
        if level == TaskComplexity.EXTREME:
            decompose_first = True
            decomposition = DecompositionStrategy.RECURSIVE
            reasons.append("Extreme complexity: deep decomposition required")

        return RoutingDecision(
            task_id=task.id,
            strategy=strategy,
            agent_count=agent_count,
            decompose_first=decompose_first,
            decomposition_strategy=decomposition,
            predicted_success=predicted_success,
            reasons=reasons,
            metadata={
                'complexity_score': score,
                'complexity_level': level.value
            }
        )

    async def should_use_multi_agent(self, task: Task, predicted_accuracy: float) -> bool:
        """Quick check if multi-agent would help."""
        return predicted_accuracy < self.MULTI_AGENT_THRESHOLD

    def get_stats(self) -> Dict:
        """Get routing statistics."""
        total = self._single_agent_count + self._multi_agent_count
        return {
            'routing_decisions': self._routing_decisions,
            'single_agent_count': self._single_agent_count,
            'multi_agent_count': self._multi_agent_count,
            'single_agent_ratio': self._single_agent_count / total if total > 0 else 0.0
        }


class TaskDecomposer:
    """
    Decomposes complex tasks into simpler subtasks.

    Uses LLM for semantic decomposition when available.
    """

    def __init__(self, config: Dict = None, llm_client=None):
        """Initialize task decomposer."""
        self.config = config or {}
        self.llm_client = llm_client

        # Maximum subtask depth
        self.max_depth = self.config.get('max_depth', 3)

        # Task counter
        self._task_counter = 0

    async def decompose(
        self,
        task: Task,
        strategy: DecompositionStrategy,
        target_complexity: float = 0.3
    ) -> List[Task]:
        """
        Decompose task into subtasks.

        Args:
            task: Task to decompose
            strategy: Decomposition strategy
            target_complexity: Target complexity for subtasks

        Returns:
            List of subtasks
        """
        if strategy == DecompositionStrategy.NONE:
            return [task]

        if strategy == DecompositionStrategy.SEQUENTIAL:
            return await self._decompose_sequential(task, target_complexity)

        if strategy == DecompositionStrategy.PARALLEL:
            return await self._decompose_parallel(task, target_complexity)

        if strategy == DecompositionStrategy.HIERARCHICAL:
            return await self._decompose_hierarchical(task, target_complexity)

        if strategy == DecompositionStrategy.RECURSIVE:
            return await self._decompose_recursive(task, target_complexity)

        return [task]

    async def _decompose_sequential(
        self,
        task: Task,
        target_complexity: float
    ) -> List[Task]:
        """Decompose into sequential subtasks."""
        if not self.llm_client:
            return self._heuristic_decompose(task, 'sequential')

        prompt = f"""Decompose this task into 2-4 sequential steps:

Task: {task.description}
Capability: {task.capability}

Return JSON array of step descriptions:
{{"steps": ["step 1 description", "step 2 description", ...]}}"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)
            steps = self._parse_steps(response)

            return [
                Task(
                    id=self._generate_id(task.id, i),
                    description=step,
                    capability=task.capability,
                    context=task.context,
                    parent_id=task.id
                )
                for i, step in enumerate(steps)
            ]
        except Exception as e:
            logger.warning(f"LLM decomposition failed: {e}")
            return self._heuristic_decompose(task, 'sequential')

    async def _decompose_parallel(
        self,
        task: Task,
        target_complexity: float
    ) -> List[Task]:
        """Decompose into parallel independent subtasks."""
        if not self.llm_client:
            return self._heuristic_decompose(task, 'parallel')

        prompt = f"""Decompose this task into 2-4 independent parallel subtasks:

Task: {task.description}
Capability: {task.capability}

Return JSON array of independent subtask descriptions:
{{"subtasks": ["subtask 1", "subtask 2", ...]}}"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)
            subtasks = self._parse_subtasks(response)

            return [
                Task(
                    id=self._generate_id(task.id, i),
                    description=subtask,
                    capability=task.capability,
                    context=task.context,
                    parent_id=task.id
                )
                for i, subtask in enumerate(subtasks)
            ]
        except Exception as e:
            logger.warning(f"LLM decomposition failed: {e}")
            return self._heuristic_decompose(task, 'parallel')

    async def _decompose_hierarchical(
        self,
        task: Task,
        target_complexity: float
    ) -> List[Task]:
        """Decompose into hierarchical subtask tree."""
        # First level: sequential
        first_level = await self._decompose_sequential(task, target_complexity)

        # For each high-complexity subtask, decompose further
        result = []
        for subtask in first_level:
            subtask.estimated_complexity = task.estimated_complexity / len(first_level)

            if subtask.estimated_complexity > target_complexity:
                # Decompose further
                sub_subtasks = await self._decompose_parallel(subtask, target_complexity)
                result.extend(sub_subtasks)
            else:
                result.append(subtask)

        return result

    async def _decompose_recursive(
        self,
        task: Task,
        target_complexity: float,
        current_depth: int = 0
    ) -> List[Task]:
        """Recursively decompose until target complexity."""
        if current_depth >= self.max_depth:
            return [task]

        if task.estimated_complexity <= target_complexity:
            return [task]

        # Decompose this level
        subtasks = await self._decompose_hierarchical(task, target_complexity)

        # Recursively decompose if still complex
        result = []
        for subtask in subtasks:
            if subtask.estimated_complexity > target_complexity:
                sub_result = await self._decompose_recursive(
                    subtask,
                    target_complexity,
                    current_depth + 1
                )
                result.extend(sub_result)
            else:
                result.append(subtask)

        return result

    def _heuristic_decompose(self, task: Task, strategy: str) -> List[Task]:
        """Heuristic decomposition without LLM."""
        # Split description into parts
        parts = task.description.split('.')
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) < 2:
            # Can't decompose
            return [task]

        return [
            Task(
                id=self._generate_id(task.id, i),
                description=part,
                capability=task.capability,
                context=task.context,
                parent_id=task.id
            )
            for i, part in enumerate(parts[:4])  # Max 4 subtasks
        ]

    def _parse_steps(self, response: str) -> List[str]:
        """Parse step list from LLM response."""
        import json

        text = response.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            data = json.loads(text.strip())
            return data.get('steps', [])
        except:
            return []

    def _parse_subtasks(self, response: str) -> List[str]:
        """Parse subtask list from LLM response."""
        import json

        text = response.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            data = json.loads(text.strip())
            return data.get('subtasks', [])
        except:
            return []

    def _generate_id(self, parent_id: str, index: int) -> str:
        """Generate subtask ID."""
        self._task_counter += 1
        return f"{parent_id}_sub{index}_{self._task_counter}"


class ComplexityAwareOrchestrator:
    """
    Main orchestrator combining complexity detection and routing.

    Implements the full CAO pipeline:
    1. Estimate complexity
    2. Route to appropriate strategy
    3. Decompose if needed
    4. Execute with optimal agent configuration
    """

    def __init__(self, config: Dict = None, llm_client=None):
        """Initialize CAO orchestrator."""
        self.config = config or {}

        self.detector = ComplexityDetector(
            config=self.config.get('detector', {}),
            llm_client=llm_client
        )

        self.router = AgentRouter(
            config=self.config.get('router', {})
        )

        self.decomposer = TaskDecomposer(
            config=self.config.get('decomposer', {}),
            llm_client=llm_client
        )

        # Statistics
        self._tasks_orchestrated: int = 0
        self._decompositions: int = 0

        logger.info("ComplexityAwareOrchestrator initialized")

    async def orchestrate(
        self,
        task: Task,
        executor: Callable[[Task, RoutingDecision], Awaitable[Any]] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate a task through the CAO pipeline.

        Args:
            task: Task to orchestrate
            executor: Optional async function to execute subtasks

        Returns:
            Dict with orchestration results
        """
        self._tasks_orchestrated += 1
        results = {
            'task_id': task.id,
            'original_description': task.description,
            'stages': []
        }

        # Stage 1: Estimate complexity
        estimate = await self.detector.estimate_complexity(task)
        results['complexity'] = estimate.to_dict()
        results['stages'].append('complexity_estimated')

        # Stage 2: Route to strategy
        decision = await self.router.route(task, estimate)
        results['routing'] = decision.to_dict()
        results['stages'].append('routing_decided')

        # Stage 3: Decompose if needed
        if decision.decompose_first:
            self._decompositions += 1
            subtasks = await self.decomposer.decompose(
                task,
                decision.decomposition_strategy
            )
            results['subtasks'] = [st.to_dict() for st in subtasks]
            results['stages'].append('decomposed')
        else:
            subtasks = [task]
            results['subtasks'] = [task.to_dict()]

        # Stage 4: Execute if executor provided
        if executor:
            execution_results = []
            for subtask in subtasks:
                # Get routing for subtask
                sub_estimate = await self.detector.estimate_complexity(subtask)
                sub_decision = await self.router.route(subtask, sub_estimate)

                result = await executor(subtask, sub_decision)
                execution_results.append(result)

            results['execution_results'] = execution_results
            results['stages'].append('executed')

        return results

    def get_stats(self) -> Dict:
        """Get orchestrator statistics."""
        return {
            'tasks_orchestrated': self._tasks_orchestrated,
            'decompositions': self._decompositions,
            'decomposition_ratio': (
                self._decompositions / self._tasks_orchestrated
                if self._tasks_orchestrated > 0 else 0.0
            ),
            'detector_stats': {
                'estimates': len(self.detector._estimates),
                'calibration_error': self.detector.get_calibration_error()
            },
            'router_stats': self.router.get_stats()
        }

    def reset(self) -> None:
        """Reset statistics."""
        self._tasks_orchestrated = 0
        self._decompositions = 0
        logger.info("ComplexityAwareOrchestrator reset")

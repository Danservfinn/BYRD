"""
BYRD AGI Seed Meta-Learning System

Implements the self-improvement of self-improvement:
- Track meta-metrics (improvement rate trajectory, learning efficiency)
- Detect and respond to plateaus
- Manage capability hierarchy (Level 0-3)
- Transfer learning between domains

THE KEY INSIGHT:
If improvement rate is declining, that's the highest priority problem.
Meta-learning optimizes the learning process itself.
"""

import asyncio
import json
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from memory import Memory
from llm_client import LLMClient


class CapabilityLevel(Enum):
    """Levels in the capability hierarchy."""
    BASE = 0        # search, code, install
    COMPOSITE = 1   # research + synthesize
    META = 2        # improve capability X
    META_META = 3   # improve how I improve capability X


class PlateauSeverity(Enum):
    """Severity of detected plateau."""
    NONE = "none"
    MINOR = "minor"       # Slight slowdown
    MODERATE = "moderate" # Noticeable stagnation
    SEVERE = "severe"     # Complete stall
    CRITICAL = "critical" # Declining


@dataclass
class MetaMetrics:
    """Container for meta-level metrics."""
    improvement_rate: float              # Current dCapability/dTime
    improvement_rate_trajectory: str     # "accelerating", "stable", "decelerating"
    learning_efficiency: float           # Knowledge gained per experience
    knowledge_transfer_score: float      # How well learning transfers
    self_modification_success_rate: float
    meta_improvement_rate: float         # d(improvement_rate)/dTime
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "improvement_rate": self.improvement_rate,
            "trajectory": self.improvement_rate_trajectory,
            "learning_efficiency": self.learning_efficiency,
            "knowledge_transfer": self.knowledge_transfer_score,
            "self_mod_success": self.self_modification_success_rate,
            "meta_improvement_rate": self.meta_improvement_rate,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class PlateauAnalysis:
    """Analysis of a detected plateau."""
    is_plateau: bool
    severity: PlateauSeverity
    duration_cycles: int
    affected_capabilities: List[str]
    likely_causes: List[str]
    suggested_actions: List[str]
    requires_external_help: bool
    help_request: Optional[str] = None


@dataclass
class CapabilityHierarchyNode:
    """A node in the capability hierarchy."""
    name: str
    level: CapabilityLevel
    description: str
    parent_capabilities: List[str]  # What this improves
    child_capabilities: List[str]   # What improves this
    effectiveness: float            # How effective at its job
    usage_count: int = 0


class MetaLearningSystem:
    """
    The meta-learning system that optimizes BYRD's learning process.

    Core responsibility: Ensure improvement rate stays positive.
    When it doesn't, diagnose why and take corrective action.
    """

    def __init__(self, memory: Memory, llm_client: LLMClient):
        self.memory = memory
        self.llm_client = llm_client

        # Historical metrics for trajectory analysis
        self._metrics_history: deque = deque(maxlen=100)
        self._improvement_rates: deque = deque(maxlen=50)

        # Plateau detection state
        self._plateau_start: Optional[datetime] = None
        self._plateau_cycles = 0
        self._last_significant_improvement: datetime = datetime.now()

        # Capability hierarchy
        self._capability_hierarchy: Dict[str, CapabilityHierarchyNode] = {}
        self._initialize_hierarchy()

        # Learning transfer tracking
        self._domain_knowledge: Dict[str, float] = {}  # domain -> knowledge level
        self._transfer_matrix: Dict[str, Dict[str, float]] = {}  # from_domain -> to_domain -> transfer_rate

        # Self-model reference (injected later)
        self.self_model = None

        # Cycle counter
        self._meta_cycles = 0

    def _initialize_hierarchy(self):
        """Initialize the base capability hierarchy."""
        # Level 0: Base capabilities
        base_caps = [
            ("research", "Find and gather information"),
            ("code_generation", "Write and modify code"),
            ("memory_operations", "Store and retrieve knowledge"),
            ("reasoning", "Analyze and draw conclusions"),
            ("introspection", "Understand own state"),
        ]

        for name, desc in base_caps:
            self._capability_hierarchy[name] = CapabilityHierarchyNode(
                name=name,
                level=CapabilityLevel.BASE,
                description=desc,
                parent_capabilities=[],
                child_capabilities=[],
                effectiveness=0.5
            )

        # Level 1: Composite capabilities
        composites = [
            ("informed_analysis", "Research + Reasoning", ["research", "reasoning"]),
            ("knowledge_synthesis", "Research + Memory", ["research", "memory_operations"]),
            ("strategic_planning", "Introspection + Reasoning", ["introspection", "reasoning"]),
        ]

        for name, desc, parents in composites:
            self._capability_hierarchy[name] = CapabilityHierarchyNode(
                name=name,
                level=CapabilityLevel.COMPOSITE,
                description=desc,
                parent_capabilities=parents,
                child_capabilities=[],
                effectiveness=0.3
            )
            # Link parents
            for parent in parents:
                if parent in self._capability_hierarchy:
                    self._capability_hierarchy[parent].child_capabilities.append(name)

        # Level 2: Meta-capabilities
        meta_caps = [
            ("improve_research", "Get better at finding information", ["research"]),
            ("improve_reasoning", "Enhance analytical ability", ["reasoning"]),
            ("improve_code", "Write better code", ["code_generation"]),
        ]

        for name, desc, targets in meta_caps:
            self._capability_hierarchy[name] = CapabilityHierarchyNode(
                name=name,
                level=CapabilityLevel.META,
                description=desc,
                parent_capabilities=targets,
                child_capabilities=[],
                effectiveness=0.2
            )

        # Level 3: Meta-meta capability
        self._capability_hierarchy["optimize_improvement"] = CapabilityHierarchyNode(
            name="optimize_improvement",
            level=CapabilityLevel.META_META,
            description="Improve how I improve capabilities",
            parent_capabilities=["improve_research", "improve_reasoning", "improve_code"],
            child_capabilities=[],
            effectiveness=0.1
        )

    async def compute_meta_metrics(self) -> MetaMetrics:
        """
        Compute current meta-metrics from system state.

        These are the metrics that matter most for AGI progress:
        - Improvement rate (THE key metric)
        - Meta-improvement rate (is improvement accelerating?)
        - Learning efficiency
        - Knowledge transfer
        """
        self._meta_cycles += 1

        # Get improvement rate from self-model
        improvement_rate = 0.0
        if self.self_model:
            try:
                metrics = await self.self_model.measure_improvement_rate()
                improvement_rate = metrics.overall_rate
            except Exception:
                pass

        # Store for trajectory analysis
        self._improvement_rates.append(improvement_rate)

        # Calculate trajectory
        trajectory = self._calculate_trajectory()

        # Calculate meta-improvement rate (d(improvement_rate)/dTime)
        meta_rate = self._calculate_meta_rate()

        # Calculate learning efficiency
        learning_efficiency = await self._calculate_learning_efficiency()

        # Calculate knowledge transfer score
        transfer_score = self._calculate_transfer_score()

        # Get self-modification success rate
        self_mod_rate = await self._get_self_mod_success_rate()

        metrics = MetaMetrics(
            improvement_rate=improvement_rate,
            improvement_rate_trajectory=trajectory,
            learning_efficiency=learning_efficiency,
            knowledge_transfer_score=transfer_score,
            self_modification_success_rate=self_mod_rate,
            meta_improvement_rate=meta_rate
        )

        self._metrics_history.append(metrics)

        return metrics

    def _calculate_trajectory(self) -> str:
        """Determine if improvement rate is accelerating, stable, or decelerating."""
        if len(self._improvement_rates) < 5:
            return "insufficient_data"

        recent = list(self._improvement_rates)[-5:]
        older = list(self._improvement_rates)[-10:-5] if len(self._improvement_rates) >= 10 else recent

        avg_recent = sum(recent) / len(recent)
        avg_older = sum(older) / len(older)

        if avg_recent > avg_older + 0.02:
            return "accelerating"
        elif avg_recent < avg_older - 0.02:
            return "decelerating"
        else:
            return "stable"

    def _calculate_meta_rate(self) -> float:
        """Calculate the rate of change of improvement rate."""
        if len(self._improvement_rates) < 3:
            return 0.0

        rates = list(self._improvement_rates)[-10:]
        if len(rates) < 3:
            return 0.0

        # Simple linear regression slope
        n = len(rates)
        x_mean = (n - 1) / 2
        y_mean = sum(rates) / n

        numerator = sum((i - x_mean) * (rates[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    async def _calculate_learning_efficiency(self) -> float:
        """
        Calculate learning efficiency: knowledge gained per experience.

        Higher efficiency means BYRD learns more from each experience.
        """
        try:
            # Get recent belief creation rate vs experience rate
            stats = await self.memory.stats()
            beliefs = stats.get("Belief", 0)
            experiences = stats.get("Experience", 0)

            if experiences == 0:
                return 0.0

            # Simple ratio (beliefs created per experience)
            efficiency = min(beliefs / max(experiences, 1), 1.0)

            return efficiency

        except Exception:
            return 0.0

    def _calculate_transfer_score(self) -> float:
        """
        Calculate knowledge transfer score.

        Higher score means learning in one domain helps in others.
        """
        if not self._transfer_matrix:
            return 0.5  # Default neutral

        total_transfers = 0
        total_score = 0.0

        for from_domain, transfers in self._transfer_matrix.items():
            for to_domain, rate in transfers.items():
                if from_domain != to_domain:
                    total_score += rate
                    total_transfers += 1

        if total_transfers == 0:
            return 0.5

        return total_score / total_transfers

    async def _get_self_mod_success_rate(self) -> float:
        """Get the success rate of self-modifications."""
        try:
            # Query modification outcomes from memory
            query = """
            MATCH (e:Experience)
            WHERE e.type = 'self_modification'
            WITH e, CASE WHEN e.content CONTAINS 'success' THEN 1 ELSE 0 END as success
            RETURN count(e) as total, sum(success) as successes
            """
            result = await self.memory._execute_query(query)

            if result and result[0]["total"] > 0:
                return result[0]["successes"] / result[0]["total"]

            return 0.0

        except Exception:
            return 0.0

    async def detect_plateau(self) -> PlateauAnalysis:
        """
        Detect if BYRD has hit a learning plateau.

        A plateau is when improvement rate stays low for extended periods.
        This is THE highest priority problem when it occurs.
        """
        if len(self._improvement_rates) < 10:
            return PlateauAnalysis(
                is_plateau=False,
                severity=PlateauSeverity.NONE,
                duration_cycles=0,
                affected_capabilities=[],
                likely_causes=["Insufficient data"],
                suggested_actions=["Continue operating normally"],
                requires_external_help=False
            )

        recent_rates = list(self._improvement_rates)[-10:]
        avg_rate = sum(recent_rates) / len(recent_rates)

        # Determine severity
        if avg_rate > 0.05:
            severity = PlateauSeverity.NONE
            is_plateau = False
        elif avg_rate > 0.02:
            severity = PlateauSeverity.MINOR
            is_plateau = True
        elif avg_rate > 0.005:
            severity = PlateauSeverity.MODERATE
            is_plateau = True
        elif avg_rate >= 0:
            severity = PlateauSeverity.SEVERE
            is_plateau = True
        else:
            severity = PlateauSeverity.CRITICAL
            is_plateau = True

        if not is_plateau:
            self._plateau_start = None
            self._plateau_cycles = 0
            return PlateauAnalysis(
                is_plateau=False,
                severity=PlateauSeverity.NONE,
                duration_cycles=0,
                affected_capabilities=[],
                likely_causes=[],
                suggested_actions=[],
                requires_external_help=False
            )

        # Track plateau duration
        if self._plateau_start is None:
            self._plateau_start = datetime.now()
            self._plateau_cycles = 1
        else:
            self._plateau_cycles += 1

        # Analyze causes using LLM
        causes, actions, needs_help, help_request = await self._analyze_plateau_causes(
            severity, self._plateau_cycles
        )

        # Get affected capabilities
        affected = await self._get_stagnant_capabilities()

        return PlateauAnalysis(
            is_plateau=True,
            severity=severity,
            duration_cycles=self._plateau_cycles,
            affected_capabilities=affected,
            likely_causes=causes,
            suggested_actions=actions,
            requires_external_help=needs_help,
            help_request=help_request
        )

    async def _analyze_plateau_causes(
        self,
        severity: PlateauSeverity,
        duration: int
    ) -> Tuple[List[str], List[str], bool, Optional[str]]:
        """Use LLM to analyze potential plateau causes and solutions."""

        # Get recent experiences for context
        try:
            recent = await self.memory.get_recent_experiences(limit=20)
            context = "\n".join([
                f"- [{e.get('type', '')}] {e.get('content', '')[:100]}"
                for e in recent
            ])
        except Exception:
            context = "(No recent experiences available)"

        prompt = f"""An AI system has hit a learning plateau.

PLATEAU SEVERITY: {severity.value}
DURATION: {duration} cycles
RECENT ACTIVITY:
{context}

Analyze:
1. What are the likely causes of this plateau?
2. What actions could help overcome it?
3. Does this require external help?

Consider:
- Resource limitations
- Capability gaps
- Strategy inefficiencies
- Knowledge barriers
- Exploration vs exploitation balance

Output JSON:
{{
    "causes": ["cause1", "cause2"],
    "actions": ["action1", "action2"],
    "requires_help": true/false,
    "help_request": "specific request if help needed"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.5,
                max_tokens=500
            )

            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            return (
                data.get("causes", ["Unknown cause"]),
                data.get("actions", ["Continue exploring"]),
                data.get("requires_help", False),
                data.get("help_request")
            )

        except Exception as e:
            # Default analysis
            if severity == PlateauSeverity.CRITICAL:
                return (
                    ["Improvement rate is negative", "May be stuck in local optimum"],
                    ["Try radically different approaches", "Request external guidance"],
                    True,
                    f"Help needed: Improvement rate declining for {duration} cycles"
                )
            elif severity == PlateauSeverity.SEVERE:
                return (
                    ["Learning has stalled", "Current strategies not working"],
                    ["Increase exploration", "Try new capability combinations"],
                    duration > 20,
                    f"Help may be needed: Stalled for {duration} cycles" if duration > 20 else None
                )
            else:
                return (
                    ["Slight slowdown detected"],
                    ["Increase challenge difficulty", "Focus on weak areas"],
                    False,
                    None
                )

    async def _get_stagnant_capabilities(self) -> List[str]:
        """Get capabilities that haven't improved recently."""
        if not self.self_model:
            return []

        try:
            inventory = await self.self_model.assess_capabilities()
            stagnant = [
                name for name, cap in inventory.capabilities.items()
                if cap.trend == "stable" or cap.trend == "declining"
            ]
            return stagnant[:5]

        except Exception:
            return []

    async def respond_to_plateau(self, analysis: PlateauAnalysis):
        """
        Take action in response to a detected plateau.

        The severity determines the response:
        - MINOR: Adjust strategy
        - MODERATE: Try new approaches
        - SEVERE: Request help, try radical changes
        - CRITICAL: Emergency measures
        """
        if not analysis.is_plateau:
            return

        # Record plateau detection as experience
        await self.memory.record_experience(
            content=f"[PLATEAU_DETECTED] Severity: {analysis.severity.value}, "
                    f"Duration: {analysis.duration_cycles} cycles, "
                    f"Causes: {', '.join(analysis.likely_causes[:2])}",
            type="meta_learning"
        )

        # Take action based on severity
        if analysis.severity == PlateauSeverity.MINOR:
            # Increase challenge difficulty
            await self.memory.create_desire(
                description="Increase difficulty of self-improvement challenges",
                intensity=0.6,
                intent="self_improvement"
            )

        elif analysis.severity == PlateauSeverity.MODERATE:
            # Try new capability combinations
            for action in analysis.suggested_actions[:2]:
                await self.memory.create_desire(
                    description=f"[PLATEAU_RESPONSE] {action}",
                    intensity=0.7,
                    intent="self_improvement"
                )

        elif analysis.severity in [PlateauSeverity.SEVERE, PlateauSeverity.CRITICAL]:
            # Record help request if needed
            if analysis.requires_external_help and analysis.help_request:
                await self.memory.record_experience(
                    content=f"[HELP_NEEDED] {analysis.help_request}",
                    type="help_request"
                )

            # Create urgent desires
            for action in analysis.suggested_actions:
                await self.memory.create_desire(
                    description=f"[URGENT] {action}",
                    intensity=0.9,
                    intent="self_improvement"
                )

            print(f"🚨 Plateau response: {len(analysis.suggested_actions)} urgent actions created")

    async def record_domain_learning(self, domain: str, knowledge_gained: float):
        """Record learning in a specific domain for transfer tracking."""
        current = self._domain_knowledge.get(domain, 0.0)
        self._domain_knowledge[domain] = min(current + knowledge_gained, 1.0)

    async def record_knowledge_transfer(
        self,
        from_domain: str,
        to_domain: str,
        transfer_effectiveness: float
    ):
        """Record successful knowledge transfer between domains."""
        if from_domain not in self._transfer_matrix:
            self._transfer_matrix[from_domain] = {}

        current = self._transfer_matrix[from_domain].get(to_domain, 0.5)
        # Exponential moving average
        self._transfer_matrix[from_domain][to_domain] = 0.7 * current + 0.3 * transfer_effectiveness

    def get_capability_hierarchy(self) -> Dict[str, Dict]:
        """Get the full capability hierarchy."""
        return {
            name: {
                "level": node.level.value,
                "level_name": node.level.name,
                "description": node.description,
                "parents": node.parent_capabilities,
                "children": node.child_capabilities,
                "effectiveness": node.effectiveness,
                "usage_count": node.usage_count
            }
            for name, node in self._capability_hierarchy.items()
        }

    async def run_meta_cycle(self) -> Dict:
        """
        Run one meta-learning cycle.

        This is called periodically to:
        1. Compute meta-metrics
        2. Detect plateaus
        3. Take corrective action
        4. Update capability hierarchy
        """
        # Compute current meta-metrics
        metrics = await self.compute_meta_metrics()

        # Detect plateau
        plateau = await self.detect_plateau()

        # Respond if needed
        if plateau.is_plateau:
            await self.respond_to_plateau(plateau)

        # Record meta-metrics as experience (every 10 cycles)
        if self._meta_cycles % 10 == 0:
            await self.memory.record_experience(
                content=f"[META_METRICS] improvement_rate={metrics.improvement_rate:.3f}, "
                        f"trajectory={metrics.improvement_rate_trajectory}, "
                        f"meta_rate={metrics.meta_improvement_rate:.4f}, "
                        f"efficiency={metrics.learning_efficiency:.2f}",
                type="meta_learning"
            )

        return {
            "cycle": self._meta_cycles,
            "metrics": metrics.to_dict(),
            "plateau": {
                "detected": plateau.is_plateau,
                "severity": plateau.severity.value,
                "duration": plateau.duration_cycles
            } if plateau.is_plateau else None
        }

    def get_statistics(self) -> Dict:
        """Get meta-learning system statistics."""
        return {
            "meta_cycles": self._meta_cycles,
            "metrics_history_size": len(self._metrics_history),
            "improvement_rates_tracked": len(self._improvement_rates),
            "domains_tracked": len(self._domain_knowledge),
            "capability_hierarchy_size": len(self._capability_hierarchy),
            "plateau_cycles": self._plateau_cycles if self._plateau_start else 0
        }


# Export main classes
__all__ = [
    "MetaLearningSystem",
    "MetaMetrics",
    "PlateauAnalysis",
    "PlateauSeverity",
    "CapabilityLevel",
    "CapabilityHierarchyNode"
]

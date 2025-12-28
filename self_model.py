"""
BYRD Self-Model
Explicit model of BYRD's own capabilities, limitations, and improvement trajectory.

AGI REQUIREMENT:
A system pursuing AGI must accurately model its own capabilities and limitations.
Without this, it cannot identify what to improve or measure progress.

EMERGENCE PRINCIPLE:
The self-model is discovered through experience, not prescribed.
BYRD observes its own performance and builds an empirical self-understanding.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from memory import Memory
from llm_client import LLMClient

# Try to import event_bus
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


class CapabilityLevel(Enum):
    """Levels of capability mastery."""
    UNKNOWN = "unknown"         # Never attempted
    FAILING = "failing"         # Success rate < 20%
    STRUGGLING = "struggling"   # Success rate 20-50%
    CAPABLE = "capable"         # Success rate 50-80%
    PROFICIENT = "proficient"   # Success rate 80-95%
    MASTERED = "mastered"       # Success rate > 95%


@dataclass
class Capability:
    """A single capability with performance metrics."""
    name: str
    description: str
    success_rate: float  # 0.0 to 1.0
    attempt_count: int
    success_count: int
    failure_count: int
    level: CapabilityLevel
    confidence: float  # How confident in the success_rate estimate
    trend: str  # "improving", "stable", "declining"
    last_attempt: Optional[datetime] = None
    last_success: Optional[datetime] = None
    recent_outcomes: List[bool] = field(default_factory=list)  # Last N outcomes

    @classmethod
    def from_history(cls, name: str, description: str, outcomes: List[Dict]) -> 'Capability':
        """Create capability from historical outcomes."""
        if not outcomes:
            return cls(
                name=name,
                description=description,
                success_rate=0.5,  # Maximum entropy when unknown
                attempt_count=0,
                success_count=0,
                failure_count=0,
                level=CapabilityLevel.UNKNOWN,
                confidence=0.0,
                trend="unknown",
                recent_outcomes=[]
            )

        successes = [o for o in outcomes if o.get("success", False)]
        success_count = len(successes)
        failure_count = len(outcomes) - success_count
        success_rate = success_count / len(outcomes)

        # Calculate confidence based on sample size
        # Bayesian-inspired: more samples = higher confidence
        confidence = min(1.0, len(outcomes) / 20.0)

        # Determine level
        if success_rate >= 0.95:
            level = CapabilityLevel.MASTERED
        elif success_rate >= 0.80:
            level = CapabilityLevel.PROFICIENT
        elif success_rate >= 0.50:
            level = CapabilityLevel.CAPABLE
        elif success_rate >= 0.20:
            level = CapabilityLevel.STRUGGLING
        else:
            level = CapabilityLevel.FAILING

        # Calculate trend from recent vs older outcomes
        if len(outcomes) >= 6:
            recent = outcomes[-3:]
            older = outcomes[-6:-3]
            recent_rate = sum(1 for o in recent if o.get("success", False)) / len(recent)
            older_rate = sum(1 for o in older if o.get("success", False)) / len(older)

            if recent_rate > older_rate + 0.1:
                trend = "improving"
            elif recent_rate < older_rate - 0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "unknown"

        # Extract recent outcomes
        recent_outcomes = [o.get("success", False) for o in outcomes[-10:]]

        # Get timestamps
        last_attempt = None
        last_success = None
        for o in reversed(outcomes):
            if last_attempt is None and o.get("timestamp"):
                last_attempt = datetime.fromisoformat(o["timestamp"]) if isinstance(o["timestamp"], str) else o["timestamp"]
            if last_success is None and o.get("success") and o.get("timestamp"):
                last_success = datetime.fromisoformat(o["timestamp"]) if isinstance(o["timestamp"], str) else o["timestamp"]
            if last_attempt and last_success:
                break

        return cls(
            name=name,
            description=description,
            success_rate=success_rate,
            attempt_count=len(outcomes),
            success_count=success_count,
            failure_count=failure_count,
            level=level,
            confidence=confidence,
            trend=trend,
            last_attempt=last_attempt,
            last_success=last_success,
            recent_outcomes=recent_outcomes
        )


@dataclass
class Limitation:
    """A specific limitation with analysis."""
    description: str
    capability_affected: str
    severity: float  # 0.0 to 1.0 (how much it blocks progress)
    frequency: int  # How often encountered
    examples: List[str]
    category: str  # "self_solvable", "resource_dependent", "fundamental"
    potential_solutions: List[str]
    self_solvable: bool
    blocking_capabilities: List[str] = field(default_factory=list)  # What this prevents


@dataclass
class ImprovementMetrics:
    """Metrics tracking improvement over time."""
    weekly_delta: float  # Change in average capability over past week
    monthly_delta: float  # Change over past month
    trajectory: str  # "accelerating", "linear", "decelerating", "plateau"
    plateau_detected: bool
    bottleneck: Optional[str]  # What's blocking further improvement
    improvement_rate: float  # dCapability/dTime
    meta_improvement_rate: float  # d(improvement_rate)/dTime


@dataclass
class CapabilityInventory:
    """Complete inventory of all capabilities."""
    capabilities: Dict[str, Capability]
    overall_score: float  # Weighted average of all capabilities
    strongest: List[str]  # Top 3 capabilities
    weakest: List[str]  # Bottom 3 capabilities
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "capabilities": {
                name: {
                    "success_rate": cap.success_rate,
                    "level": cap.level.value,
                    "confidence": cap.confidence,
                    "trend": cap.trend,
                    "attempts": cap.attempt_count
                }
                for name, cap in self.capabilities.items()
            },
            "overall_score": self.overall_score,
            "strongest": self.strongest,
            "weakest": self.weakest,
            "timestamp": self.timestamp.isoformat()
        }


class SelfModel:
    """
    BYRD's explicit model of itself.

    AGI REQUIREMENT: Cannot improve what you cannot measure.
    This component provides accurate self-knowledge.

    EMERGENCE PRINCIPLE: Self-model is learned from experience,
    not prescribed. BYRD discovers its own capabilities.
    """

    # Capability categories that BYRD tracks
    CAPABILITY_CATEGORIES = {
        "reasoning": "Logical reasoning and inference",
        "research": "Finding and synthesizing information",
        "code_generation": "Writing and understanding code",
        "planning": "Decomposing goals into steps",
        "learning": "Acquiring new knowledge and skills",
        "self_modification": "Changing own code and architecture",
        "memory_operations": "Storing and retrieving information",
        "communication": "Explaining and interacting",
        "creativity": "Generating novel solutions",
        "introspection": "Understanding own processes",
        "prediction": "Forecasting outcomes",
        "abstraction": "Forming general concepts from specifics"
    }

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Cache for performance
        self._capability_cache: Optional[CapabilityInventory] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=5)

        # Historical snapshots for trend analysis
        self._historical_snapshots: List[CapabilityInventory] = []

        # Improvement tracking
        self._improvement_history: List[Dict] = []

        # Bayesian tracking: Beta distribution parameters (alpha = successes + 1, beta = failures + 1)
        self._alpha: Dict[str, float] = {}  # Prior successes + 1
        self._beta: Dict[str, float] = {}   # Prior failures + 1

    # =========================================================================
    # BAYESIAN CAPABILITY TRACKING
    # =========================================================================

    def bayesian_update(self, capability: str, success: bool):
        """
        Update Bayesian estimate after observing an outcome.

        Uses Beta distribution: Beta(alpha, beta) where:
        - alpha = number of successes + 1 (prior)
        - beta = number of failures + 1 (prior)

        Args:
            capability: Name of capability observed
            success: Whether the observation was successful
        """
        if capability not in self._alpha:
            # Initialize with uniform prior (Beta(1, 1))
            self._alpha[capability] = 1.0
            self._beta[capability] = 1.0

        if success:
            self._alpha[capability] += 1
        else:
            self._beta[capability] += 1

    def get_bayesian_estimate(self, capability: str) -> Tuple[float, float, float]:
        """
        Get capability estimate with 95% credible interval.

        Uses Beta distribution to compute point estimate and uncertainty.

        Args:
            capability: Name of capability

        Returns:
            Tuple of (mean, lower_95, upper_95)
        """
        if capability not in self._alpha:
            return (0.5, 0.0, 1.0)  # Maximum uncertainty

        a = self._alpha[capability]
        b = self._beta[capability]

        # Mean of Beta(a, b) = a / (a + b)
        mean = a / (a + b)

        # For credible interval, use Beta quantiles
        # Approximation using Wilson score interval when scipy not available
        try:
            from scipy import stats
            lower = stats.beta.ppf(0.025, a, b)
            upper = stats.beta.ppf(0.975, a, b)
        except ImportError:
            # Wilson score interval approximation
            n = a + b - 2  # Total observations
            if n < 1:
                return (0.5, 0.0, 1.0)

            z = 1.96  # 95% confidence
            p = (a - 1) / n if n > 0 else 0.5

            denom = 1 + z**2 / n
            center = (p + z**2 / (2 * n)) / denom
            spread = z * ((p * (1 - p) + z**2 / (4 * n)) / n) ** 0.5 / denom

            lower = max(0, center - spread)
            upper = min(1, center + spread)

        return (mean, lower, upper)

    def get_bayesian_uncertainty(self, capability: str) -> float:
        """
        Get uncertainty (normalized interval width) of capability belief.

        Higher uncertainty = less confident in estimate.

        Args:
            capability: Name of capability

        Returns:
            Uncertainty score from 0.0 (certain) to 1.0 (maximum uncertainty)
        """
        if capability not in self._alpha:
            return 1.0

        _, lower, upper = self.get_bayesian_estimate(capability)
        return upper - lower

    def should_explore(self, capability: str, threshold: float = 0.4) -> bool:
        """
        Recommend exploration if uncertainty is high.

        High uncertainty means we don't know the true capability level,
        so exploration (more observations) would be valuable.

        Args:
            capability: Name of capability
            threshold: Uncertainty threshold for recommending exploration

        Returns:
            True if exploration recommended
        """
        return self.get_bayesian_uncertainty(capability) > threshold

    def get_all_bayesian_estimates(self) -> Dict[str, Dict[str, float]]:
        """
        Get Bayesian estimates for all tracked capabilities.

        Returns:
            Dict mapping capability name to {mean, lower, upper, uncertainty}
        """
        estimates = {}
        for cap in self._alpha.keys():
            mean, lower, upper = self.get_bayesian_estimate(cap)
            estimates[cap] = {
                'mean': mean,
                'lower': lower,
                'upper': upper,
                'uncertainty': upper - lower,
                'observations': int(self._alpha[cap] + self._beta[cap] - 2)
            }
        return estimates

    def get_exploration_candidates(self, top_n: int = 3) -> List[str]:
        """
        Get capabilities with highest exploration value.

        These are capabilities where more observations would most
        reduce our uncertainty about true capability level.

        Args:
            top_n: Number of candidates to return

        Returns:
            List of capability names sorted by exploration value
        """
        candidates = []
        for cap in self._alpha.keys():
            uncertainty = self.get_bayesian_uncertainty(cap)
            observations = self._alpha[cap] + self._beta[cap] - 2
            # Prefer high uncertainty AND low observations
            exploration_value = uncertainty * (1.0 / (1 + observations * 0.1))
            candidates.append((cap, exploration_value))

        candidates.sort(key=lambda x: x[1], reverse=True)
        return [cap for cap, _ in candidates[:top_n]]

    async def assess_capabilities(self, force_refresh: bool = False) -> CapabilityInventory:
        """
        Generate comprehensive inventory of current capabilities.

        This is the core self-assessment method.
        """
        # Check cache
        if not force_refresh and self._capability_cache:
            if datetime.now() - self._cache_timestamp < self._cache_ttl:
                return self._capability_cache

        capabilities = {}

        for category, description in self.CAPABILITY_CATEGORIES.items():
            # Get historical outcomes for this capability
            outcomes = await self._get_capability_outcomes(category)
            capability = Capability.from_history(category, description, outcomes)
            capabilities[category] = capability

        # Calculate overall score (weighted by confidence)
        total_weight = sum(c.confidence for c in capabilities.values())
        if total_weight > 0:
            overall_score = sum(
                c.success_rate * c.confidence
                for c in capabilities.values()
            ) / total_weight
        else:
            overall_score = 0.5  # Unknown

        # Find strongest and weakest
        sorted_caps = sorted(
            [(name, cap) for name, cap in capabilities.items() if cap.attempt_count > 0],
            key=lambda x: x[1].success_rate,
            reverse=True
        )

        strongest = [name for name, _ in sorted_caps[:3]]
        weakest = [name for name, _ in sorted_caps[-3:]] if len(sorted_caps) >= 3 else []

        inventory = CapabilityInventory(
            capabilities=capabilities,
            overall_score=overall_score,
            strongest=strongest,
            weakest=weakest
        )

        # Update cache
        self._capability_cache = inventory
        self._cache_timestamp = datetime.now()

        # Store snapshot for historical analysis
        await self._store_capability_snapshot(inventory)

        return inventory

    async def _get_capability_outcomes(self, capability_name: str) -> List[Dict]:
        """Get historical outcomes for a capability."""
        # Query experiences that represent capability attempts
        result = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'capability_attempt'
            AND e.capability = $capability
            RETURN e.id as id, e.success as success, e.timestamp as timestamp,
                   e.content as content, e.error as error
            ORDER BY e.timestamp DESC
            LIMIT 50
        """, {"capability": capability_name})

        return [dict(r) for r in result] if result else []

    async def record_capability_attempt(
        self,
        capability: str,
        success: bool,
        context: Dict = None,
        error: str = None
    ):
        """
        Record an attempt to use a capability.

        This is how BYRD learns about itself - by observing outcomes.
        """
        content = f"Attempted {capability}: {'success' if success else 'failure'}"
        if error:
            content += f" - {error}"

        await self.memory.record_experience(
            content=content,
            type="capability_attempt",
            metadata={
                "capability": capability,
                "success": success,
                "context": context or {},
                "error": error
            }
        )

        # Invalidate cache
        self._capability_cache = None

        # Emit event
        if HAS_EVENT_BUS:
            await event_bus.emit(Event(
                type=EventType.SYSTEM,
                data={
                    "subtype": "capability_attempt",
                    "capability": capability,
                    "success": success
                }
            ))

    async def identify_limitations(self) -> List[Limitation]:
        """
        Identify specific limitations from failure patterns.

        Returns limitations sorted by severity.
        """
        # Get recent failures
        failures = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'capability_attempt' AND e.success = false
            RETURN e.capability as capability, e.content as content,
                   e.error as error, e.timestamp as timestamp
            ORDER BY e.timestamp DESC
            LIMIT 100
        """)

        if not failures:
            return []

        # Cluster failures by capability
        failure_clusters: Dict[str, List[Dict]] = {}
        for f in failures:
            cap = f.get("capability", "unknown")
            if cap not in failure_clusters:
                failure_clusters[cap] = []
            failure_clusters[cap].append(dict(f))

        limitations = []

        for capability, cluster_failures in failure_clusters.items():
            if len(cluster_failures) < 2:
                continue  # Need multiple failures to identify pattern

            # Analyze the failure pattern
            limitation = await self._analyze_failure_cluster(capability, cluster_failures)
            if limitation:
                limitations.append(limitation)

        # Sort by severity
        limitations.sort(key=lambda l: l.severity, reverse=True)

        return limitations

    async def _analyze_failure_cluster(
        self,
        capability: str,
        failures: List[Dict]
    ) -> Optional[Limitation]:
        """Analyze a cluster of failures to identify the limitation."""
        # Use LLM to analyze pattern
        failure_texts = [f.get("content", "") + (" - " + f.get("error", "") if f.get("error") else "")
                        for f in failures[:5]]

        prompt = f"""Analyze these failures in the "{capability}" capability:

{chr(10).join(f"- {t}" for t in failure_texts)}

Identify:
1. The common pattern or root cause
2. How severe this limitation is (0.0-1.0)
3. Whether BYRD can solve this through self-modification, or needs external help
4. Potential solutions

Output JSON:
{{
    "description": "description of the limitation",
    "severity": 0.X,
    "category": "self_solvable" | "resource_dependent" | "fundamental",
    "potential_solutions": ["solution1", "solution2"],
    "blocking_capabilities": ["capabilities this prevents"]
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )

            result = self.llm_client.parse_json_response(response.text)
            if not result:
                return None

            return Limitation(
                description=result.get("description", "Unknown limitation"),
                capability_affected=capability,
                severity=float(result.get("severity", 0.5)),
                frequency=len(failures),
                examples=[f.get("content", "")[:100] for f in failures[:3]],
                category=result.get("category", "unknown"),
                potential_solutions=result.get("potential_solutions", []),
                self_solvable=result.get("category") == "self_solvable",
                blocking_capabilities=result.get("blocking_capabilities", [])
            )
        except Exception as e:
            print(f"Error analyzing failure cluster: {e}")
            return None

    async def measure_improvement_rate(self) -> ImprovementMetrics:
        """
        Calculate rate of capability improvement.

        This is THE key metric for an AGI seed.
        """
        # Get historical snapshots
        snapshots = await self._get_historical_snapshots()

        if len(snapshots) < 2:
            return ImprovementMetrics(
                weekly_delta=0.0,
                monthly_delta=0.0,
                trajectory="unknown",
                plateau_detected=False,
                bottleneck=None,
                improvement_rate=0.0,
                meta_improvement_rate=0.0
            )

        # Calculate deltas
        current = snapshots[-1]

        # Find snapshot from ~1 week ago
        week_ago_snapshot = None
        month_ago_snapshot = None

        for snapshot in reversed(snapshots):
            age = datetime.now() - snapshot["timestamp"]
            if week_ago_snapshot is None and age >= timedelta(days=7):
                week_ago_snapshot = snapshot
            if month_ago_snapshot is None and age >= timedelta(days=30):
                month_ago_snapshot = snapshot
                break

        weekly_delta = 0.0
        if week_ago_snapshot:
            weekly_delta = current["overall_score"] - week_ago_snapshot["overall_score"]

        monthly_delta = 0.0
        if month_ago_snapshot:
            monthly_delta = current["overall_score"] - month_ago_snapshot["overall_score"]

        # Calculate improvement rate (per day)
        if len(snapshots) >= 2:
            first = snapshots[0]
            last = snapshots[-1]
            days = max(1, (last["timestamp"] - first["timestamp"]).days)
            improvement_rate = (last["overall_score"] - first["overall_score"]) / days
        else:
            improvement_rate = 0.0

        # Calculate meta-improvement rate (is improvement accelerating?)
        meta_improvement_rate = 0.0
        if len(snapshots) >= 4:
            # Compare recent improvement rate to older improvement rate
            mid = len(snapshots) // 2
            older_snapshots = snapshots[:mid]
            recent_snapshots = snapshots[mid:]

            if len(older_snapshots) >= 2 and len(recent_snapshots) >= 2:
                older_rate = (older_snapshots[-1]["overall_score"] - older_snapshots[0]["overall_score"]) / max(1, (older_snapshots[-1]["timestamp"] - older_snapshots[0]["timestamp"]).days)
                recent_rate = (recent_snapshots[-1]["overall_score"] - recent_snapshots[0]["overall_score"]) / max(1, (recent_snapshots[-1]["timestamp"] - recent_snapshots[0]["timestamp"]).days)
                meta_improvement_rate = recent_rate - older_rate

        # Determine trajectory
        if meta_improvement_rate > 0.001:
            trajectory = "accelerating"
        elif meta_improvement_rate < -0.001:
            trajectory = "decelerating"
        elif abs(improvement_rate) < 0.001:
            trajectory = "plateau"
        else:
            trajectory = "linear"

        # Detect plateau
        plateau_detected = trajectory == "plateau" and len(snapshots) >= 5

        # Identify bottleneck if plateau detected
        bottleneck = None
        if plateau_detected:
            inventory = await self.assess_capabilities()
            if inventory.weakest:
                bottleneck = inventory.weakest[0]

        return ImprovementMetrics(
            weekly_delta=weekly_delta,
            monthly_delta=monthly_delta,
            trajectory=trajectory,
            plateau_detected=plateau_detected,
            bottleneck=bottleneck,
            improvement_rate=improvement_rate,
            meta_improvement_rate=meta_improvement_rate
        )

    async def _store_capability_snapshot(self, inventory: CapabilityInventory):
        """Store a capability snapshot for historical analysis."""
        snapshot_data = {
            "overall_score": inventory.overall_score,
            "capabilities": {
                name: {
                    "success_rate": cap.success_rate,
                    "level": cap.level.value,
                    "confidence": cap.confidence
                }
                for name, cap in inventory.capabilities.items()
            },
            "strongest": inventory.strongest,
            "weakest": inventory.weakest,
            "timestamp": inventory.timestamp
        }

        # Store in memory
        await self.memory._run_query("""
            CREATE (s:CapabilitySnapshot {
                id: $id,
                overall_score: $overall_score,
                snapshot_data: $snapshot_data,
                timestamp: datetime($timestamp)
            })
        """, {
            "id": f"snapshot_{inventory.timestamp.isoformat()}",
            "overall_score": inventory.overall_score,
            "snapshot_data": json.dumps(snapshot_data),
            "timestamp": inventory.timestamp.isoformat()
        })

    async def _get_historical_snapshots(self, limit: int = 100) -> List[Dict]:
        """Get historical capability snapshots."""
        result = await self.memory._run_query("""
            MATCH (s:CapabilitySnapshot)
            RETURN s.overall_score as overall_score,
                   s.snapshot_data as snapshot_data,
                   s.timestamp as timestamp
            ORDER BY s.timestamp ASC
            LIMIT $limit
        """, {"limit": limit})

        snapshots = []
        for r in result or []:
            try:
                timestamp = r["timestamp"]
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp)
                snapshots.append({
                    "overall_score": r["overall_score"],
                    "data": json.loads(r["snapshot_data"]) if isinstance(r["snapshot_data"], str) else r["snapshot_data"],
                    "timestamp": timestamp
                })
            except Exception:
                continue

        return snapshots

    async def predict_capability_after_modification(
        self,
        proposed_modification: str,
        target_capability: str
    ) -> Dict:
        """
        Predict how a proposed modification would affect capabilities.

        Used to evaluate self-modifications before applying them.
        """
        current_inventory = await self.assess_capabilities()
        current_cap = current_inventory.capabilities.get(target_capability)

        if not current_cap:
            return {
                "prediction": "unknown",
                "confidence": 0.0,
                "reasoning": f"No data for capability: {target_capability}"
            }

        prompt = f"""Predict the effect of this modification on BYRD's capabilities:

Proposed modification:
{proposed_modification}

Target capability: {target_capability}
Current performance:
- Success rate: {current_cap.success_rate:.1%}
- Level: {current_cap.level.value}
- Trend: {current_cap.trend}

Predict:
1. Expected change in success rate (-1.0 to +1.0)
2. Confidence in prediction (0.0 to 1.0)
3. Potential risks
4. Expected side effects on other capabilities

Output JSON:
{{
    "expected_delta": 0.X,
    "confidence": 0.X,
    "risks": ["risk1", "risk2"],
    "side_effects": {{"capability_name": expected_delta}},
    "reasoning": "explanation"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )

            result = self.llm_client.parse_json_response(response.text)
            if result:
                return {
                    "current_rate": current_cap.success_rate,
                    "predicted_rate": current_cap.success_rate + result.get("expected_delta", 0),
                    "confidence": result.get("confidence", 0.5),
                    "risks": result.get("risks", []),
                    "side_effects": result.get("side_effects", {}),
                    "reasoning": result.get("reasoning", "")
                }
        except Exception as e:
            print(f"Error predicting modification effect: {e}")

        return {
            "prediction": "error",
            "confidence": 0.0,
            "reasoning": "Failed to generate prediction"
        }

    async def get_self_assessment_summary(self) -> str:
        """
        Generate a human-readable self-assessment summary.

        Used for reflection and reporting.
        """
        inventory = await self.assess_capabilities()
        limitations = await self.identify_limitations()
        metrics = await self.measure_improvement_rate()

        summary_parts = [
            "=== BYRD Self-Assessment ===",
            f"Overall capability score: {inventory.overall_score:.1%}",
            f"Strongest areas: {', '.join(inventory.strongest) if inventory.strongest else 'Unknown'}",
            f"Weakest areas: {', '.join(inventory.weakest) if inventory.weakest else 'Unknown'}",
            "",
            "=== Improvement Metrics ===",
            f"Weekly change: {metrics.weekly_delta:+.1%}",
            f"Monthly change: {metrics.monthly_delta:+.1%}",
            f"Trajectory: {metrics.trajectory}",
            f"Plateau detected: {'Yes' if metrics.plateau_detected else 'No'}",
        ]

        if metrics.bottleneck:
            summary_parts.append(f"Bottleneck: {metrics.bottleneck}")

        if limitations:
            summary_parts.append("")
            summary_parts.append("=== Top Limitations ===")
            for lim in limitations[:3]:
                summary_parts.append(f"- {lim.description} (severity: {lim.severity:.1%})")
                if lim.potential_solutions:
                    summary_parts.append(f"  Potential fix: {lim.potential_solutions[0]}")

        return "\n".join(summary_parts)

    async def generate_improvement_priorities(self) -> List[Dict]:
        """
        Generate prioritized list of improvements based on self-assessment.

        This drives BYRD's self-improvement loop.
        """
        inventory = await self.assess_capabilities()
        limitations = await self.identify_limitations()
        metrics = await self.measure_improvement_rate()

        priorities = []

        # Priority 1: Address plateau if detected
        if metrics.plateau_detected and metrics.bottleneck:
            priorities.append({
                "priority": 1,
                "type": "plateau_breaker",
                "description": f"Break through plateau by improving {metrics.bottleneck}",
                "target_capability": metrics.bottleneck,
                "urgency": "critical"
            })

        # Priority 2: Fix self-solvable limitations
        for lim in limitations:
            if lim.self_solvable and lim.severity > 0.5:
                priorities.append({
                    "priority": 2,
                    "type": "limitation_fix",
                    "description": f"Fix: {lim.description}",
                    "target_capability": lim.capability_affected,
                    "potential_solutions": lim.potential_solutions,
                    "urgency": "high" if lim.severity > 0.7 else "medium"
                })

        # Priority 3: Improve weakest capabilities
        for weak_cap in inventory.weakest:
            cap = inventory.capabilities.get(weak_cap)
            if cap and cap.level in [CapabilityLevel.FAILING, CapabilityLevel.STRUGGLING]:
                priorities.append({
                    "priority": 3,
                    "type": "capability_improvement",
                    "description": f"Improve {weak_cap} (currently {cap.success_rate:.1%})",
                    "target_capability": weak_cap,
                    "urgency": "medium"
                })

        # Priority 4: Maintain declining capabilities
        for name, cap in inventory.capabilities.items():
            if cap.trend == "declining":
                priorities.append({
                    "priority": 4,
                    "type": "decline_reversal",
                    "description": f"Reverse decline in {name}",
                    "target_capability": name,
                    "urgency": "medium"
                })

        return sorted(priorities, key=lambda p: p["priority"])

    async def reset(self):
        """Reset self-model state (used during system reset)."""
        self._capability_cache = None
        self._cache_timestamp = None
        self._historical_snapshots = []
        self._improvement_history = []

        # Clear capability snapshots from database
        await self.memory._run_query("""
            MATCH (s:CapabilitySnapshot)
            DETACH DELETE s
        """)

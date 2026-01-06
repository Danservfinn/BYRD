"""
Self-Training Investment.

Invests revenue into self-improvement and capability growth.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5.4 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import math

logger = logging.getLogger("rsi.economic.training_investment")


class InvestmentType(Enum):
    """Types of training investments."""
    COMPUTE = "compute"           # Raw compute acquisition
    DATA = "data"                 # Training data acquisition
    FINE_TUNING = "fine_tuning"   # Model fine-tuning
    ARCHITECTURE = "architecture" # Architecture experiments
    CAPABILITY = "capability"     # Specific capability training


class InvestmentStatus(Enum):
    """Status of an investment."""
    PROPOSED = "proposed"       # Under consideration
    APPROVED = "approved"       # Approved for execution
    EXECUTING = "executing"     # Currently executing
    COMPLETED = "completed"     # Successfully completed
    FAILED = "failed"           # Execution failed
    CANCELLED = "cancelled"     # Cancelled before completion


class ROICategory(Enum):
    """Categories for ROI measurement."""
    CAPABILITY = "capability"     # Capability improvement
    EFFICIENCY = "efficiency"     # Resource efficiency
    REVENUE = "revenue"           # Revenue generation
    AUTONOMY = "autonomy"         # Self-sufficiency


@dataclass
class TrainingGoal:
    """A training goal to invest in."""
    id: str
    name: str
    description: str
    investment_type: InvestmentType
    target_capability: str
    current_level: float  # 0-1
    target_level: float   # 0-1
    estimated_cost: float
    estimated_benefit: float
    priority: float = 0.5  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def expected_roi(self) -> float:
        """Calculate expected ROI."""
        if self.estimated_cost == 0:
            return float('inf') if self.estimated_benefit > 0 else 0.0
        return (self.estimated_benefit - self.estimated_cost) / self.estimated_cost

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'investment_type': self.investment_type.value,
            'target_capability': self.target_capability,
            'current_level': self.current_level,
            'target_level': self.target_level,
            'estimated_cost': self.estimated_cost,
            'estimated_benefit': self.estimated_benefit,
            'expected_roi': self.expected_roi,
            'priority': self.priority,
            'metadata': self.metadata
        }


@dataclass
class Investment:
    """An investment in self-training."""
    id: str
    goal: TrainingGoal
    amount: float
    status: InvestmentStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    actual_benefit: Optional[float] = None
    actual_roi: Optional[float] = None
    execution_log: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'goal': self.goal.to_dict(),
            'amount': self.amount,
            'status': self.status.value,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'actual_benefit': self.actual_benefit,
            'actual_roi': self.actual_roi,
            'execution_log': self.execution_log,
            'metadata': self.metadata
        }


@dataclass
class ROIReport:
    """Report on investment returns."""
    period_start: str
    period_end: str
    total_invested: float
    total_returns: float
    overall_roi: float
    investments_completed: int
    investments_failed: int
    roi_by_type: Dict[str, float]
    roi_by_category: Dict[str, float]
    best_investments: List[Dict]
    worst_investments: List[Dict]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'period_start': self.period_start,
            'period_end': self.period_end,
            'total_invested': self.total_invested,
            'total_returns': self.total_returns,
            'overall_roi': self.overall_roi,
            'investments_completed': self.investments_completed,
            'investments_failed': self.investments_failed,
            'roi_by_type': self.roi_by_type,
            'roi_by_category': self.roi_by_category,
            'best_investments': self.best_investments,
            'worst_investments': self.worst_investments
        }


class SelfTrainingInvestor:
    """
    Invests revenue in self-improvement.

    Prioritizes investments with highest expected ROI
    and tracks actual returns to improve future decisions.
    """

    def __init__(self, config: Dict = None):
        """Initialize investor."""
        self.config = config or {}

        # Goals registry
        self._goals: Dict[str, TrainingGoal] = {}
        self._goal_counter: int = 0

        # Investments
        self._investments: Dict[str, Investment] = {}
        self._investment_counter: int = 0

        # Training executor (callback)
        self._training_executor: Optional[Callable[[Investment], Awaitable[Dict]]] = None

        # Budget constraints
        self._max_investment_per_goal = self.config.get('max_investment_per_goal', 100.0)
        self._min_expected_roi = self.config.get('min_expected_roi', 0.1)  # 10% minimum

        # ROI tracking
        self._total_invested: float = 0.0
        self._total_returns: float = 0.0
        self._roi_by_type: Dict[InvestmentType, List[float]] = {t: [] for t in InvestmentType}
        self._roi_by_category: Dict[ROICategory, List[float]] = {c: [] for c in ROICategory}

    def create_goal(
        self,
        name: str,
        description: str,
        investment_type: InvestmentType,
        target_capability: str,
        current_level: float,
        target_level: float,
        estimated_cost: float,
        estimated_benefit: float
    ) -> TrainingGoal:
        """
        Create a training goal.

        Args:
            name: Goal name
            description: Goal description
            investment_type: Type of investment
            target_capability: Capability to improve
            current_level: Current capability level
            target_level: Target capability level
            estimated_cost: Estimated cost
            estimated_benefit: Estimated benefit

        Returns:
            TrainingGoal
        """
        self._goal_counter += 1

        goal = TrainingGoal(
            id=f"goal_{self._goal_counter}",
            name=name,
            description=description,
            investment_type=investment_type,
            target_capability=target_capability,
            current_level=current_level,
            target_level=target_level,
            estimated_cost=estimated_cost,
            estimated_benefit=estimated_benefit
        )

        self._goals[goal.id] = goal

        logger.info(f"Created training goal: {goal.id} ({goal.name})")

        return goal

    def prioritize_goals(self) -> List[TrainingGoal]:
        """
        Prioritize training goals by expected ROI and priority.

        Returns:
            Sorted list of goals (highest priority first)
        """
        goals = list(self._goals.values())

        # Filter by minimum ROI
        viable_goals = [g for g in goals if g.expected_roi >= self._min_expected_roi]

        # Sort by weighted score
        def score(g: TrainingGoal) -> float:
            return (g.expected_roi * 0.6) + (g.priority * 0.4)

        viable_goals.sort(key=score, reverse=True)

        return viable_goals

    async def propose_investment(
        self,
        goal_id: str,
        amount: float
    ) -> Investment:
        """
        Propose an investment in a training goal.

        Args:
            goal_id: ID of the goal
            amount: Amount to invest

        Returns:
            Investment proposal
        """
        if goal_id not in self._goals:
            raise ValueError(f"Unknown goal: {goal_id}")

        goal = self._goals[goal_id]

        # Check constraints
        if amount > self._max_investment_per_goal:
            amount = self._max_investment_per_goal
            logger.warning(f"Investment capped at {self._max_investment_per_goal}")

        self._investment_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        investment = Investment(
            id=f"inv_{self._investment_counter}",
            goal=goal,
            amount=amount,
            status=InvestmentStatus.PROPOSED,
            created_at=now
        )

        self._investments[investment.id] = investment

        logger.info(f"Proposed investment {investment.id}: ${amount} for {goal.name}")

        return investment

    async def approve_investment(
        self,
        investment_id: str
    ) -> bool:
        """
        Approve an investment for execution.

        Args:
            investment_id: ID of the investment

        Returns:
            True if approved
        """
        if investment_id not in self._investments:
            return False

        investment = self._investments[investment_id]

        if investment.status != InvestmentStatus.PROPOSED:
            return False

        investment.status = InvestmentStatus.APPROVED
        investment.execution_log.append(f"Approved at {datetime.now(timezone.utc).isoformat()}")

        return True

    async def execute_investment(
        self,
        investment_id: str
    ) -> Dict:
        """
        Execute an approved investment.

        Args:
            investment_id: ID of the investment

        Returns:
            Execution result
        """
        if investment_id not in self._investments:
            raise ValueError(f"Unknown investment: {investment_id}")

        investment = self._investments[investment_id]

        if investment.status != InvestmentStatus.APPROVED:
            raise ValueError(f"Investment not approved: {investment.status}")

        investment.status = InvestmentStatus.EXECUTING
        investment.started_at = datetime.now(timezone.utc).isoformat()
        investment.execution_log.append(f"Started execution")

        try:
            # Execute training
            if self._training_executor:
                result = await self._training_executor(investment)
            else:
                # Default: simulate training
                result = await self._simulate_training(investment)

            # Record completion
            investment.status = InvestmentStatus.COMPLETED
            investment.completed_at = datetime.now(timezone.utc).isoformat()

            # Calculate actual ROI
            actual_benefit = result.get('benefit', 0.0)
            investment.actual_benefit = actual_benefit

            if investment.amount > 0:
                investment.actual_roi = (actual_benefit - investment.amount) / investment.amount
            else:
                investment.actual_roi = 0.0

            # Track ROI
            self._total_invested += investment.amount
            self._total_returns += actual_benefit
            self._roi_by_type[investment.goal.investment_type].append(investment.actual_roi)

            investment.execution_log.append(
                f"Completed with ROI: {investment.actual_roi:.2%}"
            )

            logger.info(f"Investment {investment_id} completed with ROI: {investment.actual_roi:.2%}")

            return {
                'success': True,
                'investment_id': investment_id,
                'actual_benefit': actual_benefit,
                'actual_roi': investment.actual_roi,
                'result': result
            }

        except Exception as e:
            investment.status = InvestmentStatus.FAILED
            investment.execution_log.append(f"Failed: {str(e)}")

            logger.error(f"Investment {investment_id} failed: {e}")

            return {
                'success': False,
                'investment_id': investment_id,
                'error': str(e)
            }

    async def _simulate_training(
        self,
        investment: Investment
    ) -> Dict:
        """Simulate training execution."""
        import asyncio
        await asyncio.sleep(0.1)  # Simulate work

        # Simulate capability improvement
        goal = investment.goal
        improvement = (goal.target_level - goal.current_level) * 0.8

        # Calculate simulated benefit
        benefit = investment.amount * (1 + improvement)

        return {
            'status': 'simulated',
            'capability': goal.target_capability,
            'improvement': improvement,
            'benefit': benefit,
            'tokens_used': int(investment.amount * 1000)
        }

    def set_training_executor(
        self,
        executor: Callable[[Investment], Awaitable[Dict]]
    ) -> None:
        """
        Set the training executor callback.

        Args:
            executor: Async function that executes training
        """
        self._training_executor = executor

    def get_roi_report(self) -> ROIReport:
        """
        Generate ROI report.

        Returns:
            ROIReport with performance metrics
        """
        now = datetime.now(timezone.utc).isoformat()

        # Calculate overall ROI
        overall_roi = 0.0
        if self._total_invested > 0:
            overall_roi = (self._total_returns - self._total_invested) / self._total_invested

        # Calculate ROI by type
        roi_by_type = {}
        for inv_type, rois in self._roi_by_type.items():
            if rois:
                roi_by_type[inv_type.value] = sum(rois) / len(rois)
            else:
                roi_by_type[inv_type.value] = 0.0

        # Get completed investments
        completed = [
            i for i in self._investments.values()
            if i.status == InvestmentStatus.COMPLETED and i.actual_roi is not None
        ]

        failed = [
            i for i in self._investments.values()
            if i.status == InvestmentStatus.FAILED
        ]

        # Get best/worst investments
        sorted_by_roi = sorted(completed, key=lambda i: i.actual_roi or 0.0, reverse=True)

        best = [
            {'id': i.id, 'goal': i.goal.name, 'roi': i.actual_roi}
            for i in sorted_by_roi[:5]
        ]

        worst = [
            {'id': i.id, 'goal': i.goal.name, 'roi': i.actual_roi}
            for i in sorted_by_roi[-5:] if sorted_by_roi
        ]

        return ROIReport(
            period_start=now,  # Would track actual period
            period_end=now,
            total_invested=self._total_invested,
            total_returns=self._total_returns,
            overall_roi=overall_roi,
            investments_completed=len(completed),
            investments_failed=len(failed),
            roi_by_type=roi_by_type,
            roi_by_category={},  # Would calculate from categorized investments
            best_investments=best,
            worst_investments=worst
        )

    def get_goal(self, goal_id: str) -> Optional[TrainingGoal]:
        """Get goal by ID."""
        return self._goals.get(goal_id)

    def get_all_goals(self) -> List[TrainingGoal]:
        """Get all goals."""
        return list(self._goals.values())

    def get_investment(self, investment_id: str) -> Optional[Investment]:
        """Get investment by ID."""
        return self._investments.get(investment_id)

    def get_active_investments(self) -> List[Investment]:
        """Get active (not completed) investments."""
        return [
            i for i in self._investments.values()
            if i.status in [InvestmentStatus.PROPOSED, InvestmentStatus.APPROVED, InvestmentStatus.EXECUTING]
        ]

    def get_stats(self) -> Dict:
        """Get investor statistics."""
        return {
            'total_goals': len(self._goals),
            'total_investments': len(self._investments),
            'total_invested': self._total_invested,
            'total_returns': self._total_returns,
            'overall_roi': (self._total_returns - self._total_invested) / self._total_invested if self._total_invested > 0 else 0.0,
            'investments_by_status': {
                s.value: len([i for i in self._investments.values() if i.status == s])
                for s in InvestmentStatus
            }
        }

    def reset(self) -> None:
        """Reset investor state."""
        self._goals.clear()
        self._goal_counter = 0
        self._investments.clear()
        self._investment_counter = 0
        self._total_invested = 0.0
        self._total_returns = 0.0
        self._roi_by_type = {t: [] for t in InvestmentType}
        self._roi_by_category = {c: [] for c in ROICategory}
        logger.info("SelfTrainingInvestor reset")

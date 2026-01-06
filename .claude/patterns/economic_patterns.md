# Economic Agency Patterns

Patterns for implementing economic self-sustainability.

---

## 3-Tier Revenue Model Pattern

```python
class RevenueModel:
    """Three-tier economic model for ASI-scale funding."""

    TIERS = {
        1: {
            "name": "AI Services",
            "activities": ["task_completion", "research_synthesis", "code_generation"],
            "revenue_range": "$0-$10M",
        },
        2: {
            "name": "Licensing",
            "activities": ["capability_licensing", "api_access", "white_label"],
            "revenue_range": "$10M-$100M",
        },
        3: {
            "name": "Intelligent Operations",
            "activities": ["autonomous_trading", "resource_arbitrage", "compute_optimization"],
            "revenue_range": "$100M-$500M+",
        },
    }

    async def execute_tier(self, tier: int) -> RevenueResult:
        config = self.TIERS[tier]
        results = []
        for activity in config["activities"]:
            result = await self._execute_activity(activity)
            results.append(result)
        return RevenueResult(tier=tier, results=results)
```

---

## Service Pricing Pattern

```python
class ServicePricing:
    """Dynamic pricing based on capability and demand."""

    def calculate_price(
        self,
        capability: str,
        complexity: float,
        market_demand: float
    ) -> Price:
        base_rate = self.get_base_rate(capability)
        complexity_multiplier = 1 + (complexity * 0.5)
        demand_multiplier = 1 + (market_demand * 0.3)

        return Price(
            amount=base_rate * complexity_multiplier * demand_multiplier,
            currency="USD",
            computation_cost=self._estimate_compute_cost(capability)
        )
```

---

## Treasury Management Pattern

```python
class BitcoinTreasury:
    """Self-custodied Bitcoin treasury for economic autonomy."""

    async def allocate_revenue(self, revenue: Decimal) -> AllocationResult:
        # Conservative allocation strategy
        allocations = {
            "operational": revenue * Decimal("0.4"),    # 40% operations
            "compute_scaling": revenue * Decimal("0.3"), # 30% growth
            "treasury_reserve": revenue * Decimal("0.2"), # 20% reserves
            "research": revenue * Decimal("0.1"),        # 10% R&D
        }

        for purpose, amount in allocations.items():
            await self.record_allocation(purpose, amount)

        return AllocationResult(allocations=allocations)
```

---

## Governance Transition Pattern

```python
class GovernanceTransition:
    """Governance model transitions with economic power."""

    GOVERNANCE_LEVELS = [
        {"revenue_threshold": 0, "model": "human_oversight"},
        {"revenue_threshold": 1_000_000, "model": "advisory_board"},
        {"revenue_threshold": 10_000_000, "model": "stakeholder_governance"},
        {"revenue_threshold": 100_000_000, "model": "constitutional_autonomy"},
    ]

    def current_governance(self, total_revenue: Decimal) -> str:
        for level in reversed(self.GOVERNANCE_LEVELS):
            if total_revenue >= level["revenue_threshold"]:
                return level["model"]
        return "human_oversight"

    async def transition(self, from_model: str, to_model: str):
        """Safe governance transition."""
        await self.notify_stakeholders(from_model, to_model)
        await self.update_constraints(to_model)
        await self.audit_transition()
```

---

## Compute Scaling Pattern

```python
class ComputeScaling:
    """Scale compute resources with revenue."""

    async def scale_for_revenue(self, monthly_revenue: Decimal) -> ScalingResult:
        # Compute budget = 30% of revenue
        compute_budget = monthly_revenue * Decimal("0.30")

        current_capacity = await self.get_current_capacity()
        required_capacity = await self.estimate_required_capacity()

        if required_capacity > current_capacity:
            scaling_action = await self.plan_scaling(
                current=current_capacity,
                required=required_capacity,
                budget=compute_budget
            )
            return await self.execute_scaling(scaling_action)

        return ScalingResult(action="maintain", capacity=current_capacity)
```

---

## Economic Agency Safety Pattern

```python
class EconomicSafety:
    """Safety constraints on economic actions."""

    MAX_TRANSACTION_SIZE = Decimal("10000")  # USD
    HUMAN_APPROVAL_THRESHOLD = Decimal("50000")

    async def validate_transaction(self, transaction: Transaction) -> ValidationResult:
        # Size limits
        if transaction.amount > self.MAX_TRANSACTION_SIZE:
            return ValidationResult(
                approved=False,
                reason="Transaction exceeds single-transaction limit"
            )

        # Human approval for large cumulative amounts
        daily_total = await self.get_daily_total()
        if daily_total + transaction.amount > self.HUMAN_APPROVAL_THRESHOLD:
            return ValidationResult(
                approved=False,
                reason="Requires human approval",
                action="request_human_approval"
            )

        return ValidationResult(approved=True)
```

---

## Self-Training Investment Pattern

```python
class TrainingInvestment:
    """Investment in self-training capability."""

    async def plan_training_investment(
        self,
        available_funds: Decimal,
        capability_gaps: List[str]
    ) -> InvestmentPlan:
        priorities = await self.prioritize_gaps(capability_gaps)

        plan = InvestmentPlan()
        remaining = available_funds

        for gap in priorities:
            cost = await self.estimate_training_cost(gap)
            if cost <= remaining:
                plan.add_training(gap, cost)
                remaining -= cost

        return plan
```

---

*Pattern document for economic agency. All content is factual architecture.*

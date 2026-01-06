"""
Service Pricing Engine.

Calculates prices for services based on complexity, demand, and costs.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import math

logger = logging.getLogger("rsi.economic.pricing")


class PricingModel(Enum):
    """Pricing model types."""
    FIXED = "fixed"               # Fixed price per service
    USAGE = "usage"               # Per-unit usage pricing
    TIERED = "tiered"             # Volume-based tiers
    DYNAMIC = "dynamic"           # Demand-based pricing
    AUCTION = "auction"           # Bid-based pricing


class Currency(Enum):
    """Supported currencies."""
    USD = "usd"
    BTC = "btc"
    SATS = "sats"  # Satoshis (Bitcoin fractional)
    ETH = "eth"


@dataclass
class ServiceTier:
    """A service tier with pricing."""
    name: str
    description: str
    base_price: float
    currency: Currency
    included_units: int
    price_per_extra_unit: float
    features: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'currency': self.currency.value,
            'included_units': self.included_units,
            'price_per_extra_unit': self.price_per_extra_unit,
            'features': self.features
        }


@dataclass
class CostBreakdown:
    """Breakdown of service costs."""
    compute_cost: float      # LLM inference, processing
    storage_cost: float      # Data storage
    bandwidth_cost: float    # Network transfer
    overhead_cost: float     # Platform overhead
    margin: float            # Profit margin

    @property
    def total_cost(self) -> float:
        """Calculate total cost."""
        base = self.compute_cost + self.storage_cost + self.bandwidth_cost + self.overhead_cost
        return base * (1 + self.margin)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'compute_cost': self.compute_cost,
            'storage_cost': self.storage_cost,
            'bandwidth_cost': self.bandwidth_cost,
            'overhead_cost': self.overhead_cost,
            'margin': self.margin,
            'total_cost': self.total_cost
        }


@dataclass
class Price:
    """A calculated price."""
    amount: float
    currency: Currency
    model: PricingModel
    breakdown: CostBreakdown
    valid_until: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'amount': self.amount,
            'currency': self.currency.value,
            'model': self.model.value,
            'breakdown': self.breakdown.to_dict(),
            'valid_until': self.valid_until,
            'metadata': self.metadata
        }

    def convert_to(self, target: Currency, rate: float) -> 'Price':
        """Convert price to different currency."""
        return Price(
            amount=self.amount * rate,
            currency=target,
            model=self.model,
            breakdown=self.breakdown,
            valid_until=self.valid_until,
            metadata={**self.metadata, 'converted_from': self.currency.value}
        )


@dataclass
class ServiceDefinition:
    """Definition of a priceable service."""
    id: str
    name: str
    description: str
    category: str
    pricing_model: PricingModel
    base_price: float
    currency: Currency
    complexity_multiplier: float = 1.0
    demand_sensitive: bool = False
    min_price: float = 0.0
    max_price: Optional[float] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'pricing_model': self.pricing_model.value,
            'base_price': self.base_price,
            'currency': self.currency.value,
            'complexity_multiplier': self.complexity_multiplier,
            'demand_sensitive': self.demand_sensitive,
            'min_price': self.min_price,
            'max_price': self.max_price
        }


class PricingEngine:
    """
    Calculates service prices.

    Considers cost structure, demand, and value delivered
    to determine optimal pricing.
    """

    def __init__(self, config: Dict = None):
        """Initialize pricing engine."""
        self.config = config or {}

        # Service catalog
        self._services: Dict[str, ServiceDefinition] = {}
        self._initialize_default_services()

        # Cost factors
        self._compute_cost_per_token = self.config.get('compute_cost_per_token', 0.00002)
        self._storage_cost_per_gb = self.config.get('storage_cost_per_gb', 0.02)
        self._bandwidth_cost_per_gb = self.config.get('bandwidth_cost_per_gb', 0.09)
        self._overhead_rate = self.config.get('overhead_rate', 0.15)
        self._target_margin = self.config.get('target_margin', 0.30)

        # Demand tracking
        self._request_counts: Dict[str, int] = {}
        self._demand_window_hours = self.config.get('demand_window_hours', 24)

        # Currency rates (simplified, would use real rates in production)
        self._rates: Dict[str, float] = {
            'usd_to_btc': 0.000024,  # $1 = ~24 sats @ $42k BTC
            'usd_to_sats': 2400,
            'usd_to_eth': 0.0004,
        }

        # Statistics
        self._prices_calculated: int = 0

    def _initialize_default_services(self) -> None:
        """Initialize default service catalog."""
        services = [
            ServiceDefinition(
                id='code_review',
                name='Code Review',
                description='Review code for quality, security, and best practices',
                category='development',
                pricing_model=PricingModel.USAGE,
                base_price=5.0,
                currency=Currency.USD,
                complexity_multiplier=1.0,
                demand_sensitive=True
            ),
            ServiceDefinition(
                id='code_generation',
                name='Code Generation',
                description='Generate code from requirements or specifications',
                category='development',
                pricing_model=PricingModel.USAGE,
                base_price=10.0,
                currency=Currency.USD,
                complexity_multiplier=1.2,
                demand_sensitive=True
            ),
            ServiceDefinition(
                id='architecture_design',
                name='Architecture Design',
                description='Design software architecture and system design',
                category='consulting',
                pricing_model=PricingModel.FIXED,
                base_price=50.0,
                currency=Currency.USD,
                complexity_multiplier=1.5,
                demand_sensitive=False
            ),
            ServiceDefinition(
                id='bug_fixing',
                name='Bug Fixing',
                description='Identify and fix bugs in code',
                category='development',
                pricing_model=PricingModel.USAGE,
                base_price=8.0,
                currency=Currency.USD,
                complexity_multiplier=1.1,
                demand_sensitive=True
            ),
            ServiceDefinition(
                id='documentation',
                name='Documentation',
                description='Generate or improve technical documentation',
                category='documentation',
                pricing_model=PricingModel.USAGE,
                base_price=3.0,
                currency=Currency.USD,
                complexity_multiplier=0.8,
                demand_sensitive=False
            ),
            ServiceDefinition(
                id='training_data',
                name='Training Data Generation',
                description='Generate high-quality training data',
                category='data',
                pricing_model=PricingModel.TIERED,
                base_price=0.1,  # Per sample
                currency=Currency.USD,
                complexity_multiplier=1.0,
                demand_sensitive=True
            ),
        ]

        for service in services:
            self._services[service.id] = service

    def register_service(self, service: ServiceDefinition) -> None:
        """Register a new service."""
        self._services[service.id] = service
        logger.info(f"Registered service: {service.id}")

    def calculate_price(
        self,
        service_id: str,
        context: Dict[str, Any] = None
    ) -> Price:
        """
        Calculate price for a service request.

        Args:
            service_id: ID of the service
            context: Request context (tokens, complexity, etc.)

        Returns:
            Calculated Price
        """
        if service_id not in self._services:
            raise ValueError(f"Unknown service: {service_id}")

        self._prices_calculated += 1
        context = context or {}

        service = self._services[service_id]

        # Calculate cost breakdown
        breakdown = self._calculate_costs(service, context)

        # Calculate base price
        base_price = service.base_price * service.complexity_multiplier

        # Apply demand multiplier
        if service.demand_sensitive:
            demand_mult = self._get_demand_multiplier(service_id)
            base_price *= demand_mult

        # Apply context-specific adjustments
        if 'complexity' in context:
            complexity = context['complexity']
            base_price *= (0.8 + 0.4 * complexity)  # 0.8x to 1.2x

        if 'tokens' in context:
            tokens = context['tokens']
            base_price += tokens * self._compute_cost_per_token

        # Apply bounds
        final_price = max(service.min_price, base_price)
        if service.max_price:
            final_price = min(service.max_price, final_price)

        # Ensure we cover costs
        final_price = max(final_price, breakdown.total_cost)

        # Record demand
        self._record_request(service_id)

        # Calculate validity
        from datetime import timedelta
        valid_until = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

        return Price(
            amount=round(final_price, 4),
            currency=service.currency,
            model=service.pricing_model,
            breakdown=breakdown,
            valid_until=valid_until,
            metadata={
                'service_id': service_id,
                'demand_multiplier': self._get_demand_multiplier(service_id),
                'context_adjustments': list(context.keys())
            }
        )

    def _calculate_costs(
        self,
        service: ServiceDefinition,
        context: Dict
    ) -> CostBreakdown:
        """Calculate cost breakdown for a service."""
        # Estimate compute cost
        estimated_tokens = context.get('tokens', 1000)
        compute_cost = estimated_tokens * self._compute_cost_per_token

        # Estimate storage cost
        storage_gb = context.get('storage_gb', 0.001)
        storage_cost = storage_gb * self._storage_cost_per_gb

        # Estimate bandwidth cost
        bandwidth_gb = context.get('bandwidth_gb', 0.001)
        bandwidth_cost = bandwidth_gb * self._bandwidth_cost_per_gb

        # Calculate overhead
        base_costs = compute_cost + storage_cost + bandwidth_cost
        overhead = base_costs * self._overhead_rate

        return CostBreakdown(
            compute_cost=compute_cost,
            storage_cost=storage_cost,
            bandwidth_cost=bandwidth_cost,
            overhead_cost=overhead,
            margin=self._target_margin
        )

    def _get_demand_multiplier(self, service_id: str) -> float:
        """Get demand-based price multiplier."""
        count = self._request_counts.get(service_id, 0)

        # Simple demand curve: 1.0 at low demand, up to 1.5 at high demand
        if count < 10:
            return 1.0
        elif count < 50:
            return 1.0 + (count - 10) * 0.01  # Up to 1.4
        else:
            return 1.5  # Cap at 1.5x

    def _record_request(self, service_id: str) -> None:
        """Record a service request for demand tracking."""
        self._request_counts[service_id] = self._request_counts.get(service_id, 0) + 1

    def convert_price(
        self,
        price: Price,
        target_currency: Currency
    ) -> Price:
        """Convert price to different currency."""
        if price.currency == target_currency:
            return price

        # Get conversion rate
        rate_key = f"{price.currency.value}_to_{target_currency.value}"
        rate = self._rates.get(rate_key, 1.0)

        return price.convert_to(target_currency, rate)

    def get_service(self, service_id: str) -> Optional[ServiceDefinition]:
        """Get service by ID."""
        return self._services.get(service_id)

    def get_all_services(self) -> List[ServiceDefinition]:
        """Get all registered services."""
        return list(self._services.values())

    def get_services_by_category(self, category: str) -> List[ServiceDefinition]:
        """Get services in a category."""
        return [s for s in self._services.values() if s.category == category]

    def get_stats(self) -> Dict:
        """Get pricing statistics."""
        return {
            'registered_services': len(self._services),
            'prices_calculated': self._prices_calculated,
            'demand_counts': self._request_counts.copy(),
            'services_by_category': {
                cat: len([s for s in self._services.values() if s.category == cat])
                for cat in set(s.category for s in self._services.values())
            }
        }

    def reset(self) -> None:
        """Reset pricing engine."""
        self._request_counts.clear()
        self._prices_calculated = 0
        logger.info("PricingEngine reset")

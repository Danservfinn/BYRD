"""
Economic Agency Foundation.

Enables BYRD to participate in economic activity.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5.1 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio

from .pricing import PricingEngine, Price, ServiceDefinition, Currency
from .treasury import BitcoinTreasury, AssetType, AllocationCategory, TreasuryReport

logger = logging.getLogger("rsi.economic.agency")


class ServiceStatus(Enum):
    """Status of a service request."""
    PENDING = "pending"
    PRICING = "pricing"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RevenueSource(Enum):
    """Sources of revenue."""
    SERVICES = "services"       # Direct service sales
    LICENSING = "licensing"     # Capability licensing
    OPERATIONS = "operations"   # Operational fees


@dataclass
class ServiceRequest:
    """A request for a paid service."""
    id: str
    service_id: str
    requester: str
    parameters: Dict[str, Any]
    created_at: str
    status: ServiceStatus = ServiceStatus.PENDING
    price: Optional[Price] = None
    result: Optional[Dict] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'service_id': self.service_id,
            'requester': self.requester,
            'parameters': self.parameters,
            'created_at': self.created_at,
            'status': self.status.value,
            'price': self.price.to_dict() if self.price else None,
            'result': self.result,
            'completed_at': self.completed_at
        }


@dataclass
class ServiceResult:
    """Result of executing a service."""
    request_id: str
    success: bool
    output: Any
    execution_time: float  # seconds
    tokens_used: int
    revenue: float
    currency: Currency
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'request_id': self.request_id,
            'success': self.success,
            'output': self.output,
            'execution_time': self.execution_time,
            'tokens_used': self.tokens_used,
            'revenue': self.revenue,
            'currency': self.currency.value,
            'metadata': self.metadata
        }


@dataclass
class RevenueReport:
    """Revenue report for a period."""
    period_start: str
    period_end: str
    total_revenue: float
    currency: Currency
    revenue_by_service: Dict[str, float]
    revenue_by_source: Dict[str, float]
    requests_completed: int
    requests_failed: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'period_start': self.period_start,
            'period_end': self.period_end,
            'total_revenue': self.total_revenue,
            'currency': self.currency.value,
            'revenue_by_service': self.revenue_by_service,
            'revenue_by_source': self.revenue_by_source,
            'requests_completed': self.requests_completed,
            'requests_failed': self.requests_failed,
            'metadata': self.metadata
        }


class EconomicAgency:
    """
    Enables BYRD to earn and manage funds.

    3-tier revenue model: Services → Licensing → Operations.
    """

    def __init__(self, config: Dict = None):
        """Initialize economic agency."""
        self.config = config or {}

        # Core components
        self._pricing_engine = PricingEngine(self.config.get('pricing', {}))
        self._treasury = BitcoinTreasury(self.config.get('treasury', {}))

        # Service execution handlers
        self._service_handlers: Dict[str, Callable[[ServiceRequest], Awaitable[Dict]]] = {}

        # Request tracking
        self._requests: Dict[str, ServiceRequest] = {}
        self._request_counter: int = 0

        # Revenue tracking
        self._revenue_by_service: Dict[str, float] = {}
        self._revenue_by_source: Dict[RevenueSource, float] = {
            source: 0.0 for source in RevenueSource
        }

        # Statistics
        self._total_revenue: float = 0.0
        self._requests_completed: int = 0
        self._requests_failed: int = 0

    def register_service_handler(
        self,
        service_id: str,
        handler: Callable[[ServiceRequest], Awaitable[Dict]]
    ) -> None:
        """
        Register a handler for a service.

        Args:
            service_id: ID of the service
            handler: Async function that executes the service
        """
        self._service_handlers[service_id] = handler
        logger.info(f"Registered handler for service: {service_id}")

    async def price_service(
        self,
        service_id: str,
        context: Dict[str, Any] = None
    ) -> Price:
        """
        Calculate price for a service.

        Args:
            service_id: ID of the service
            context: Request context

        Returns:
            Calculated Price
        """
        return self._pricing_engine.calculate_price(service_id, context)

    async def create_request(
        self,
        service_id: str,
        requester: str,
        parameters: Dict[str, Any] = None
    ) -> ServiceRequest:
        """
        Create a new service request.

        Args:
            service_id: ID of the service
            requester: Requester identifier
            parameters: Service parameters

        Returns:
            ServiceRequest object
        """
        self._request_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        request = ServiceRequest(
            id=f"req_{self._request_counter}",
            service_id=service_id,
            requester=requester,
            parameters=parameters or {},
            created_at=now
        )

        # Calculate price
        request.price = await self.price_service(
            service_id,
            parameters
        )
        request.status = ServiceStatus.PRICING

        self._requests[request.id] = request

        logger.info(f"Created request {request.id} for {service_id}")

        return request

    async def accept_request(
        self,
        request_id: str
    ) -> bool:
        """
        Accept a service request (confirm payment).

        Args:
            request_id: ID of the request

        Returns:
            True if accepted
        """
        if request_id not in self._requests:
            return False

        request = self._requests[request_id]

        if request.status not in [ServiceStatus.PENDING, ServiceStatus.PRICING]:
            return False

        request.status = ServiceStatus.ACCEPTED

        logger.info(f"Accepted request {request_id}")

        return True

    async def execute_service(
        self,
        request_id: str
    ) -> ServiceResult:
        """
        Execute a paid service request.

        Args:
            request_id: ID of the request

        Returns:
            ServiceResult with outcome
        """
        if request_id not in self._requests:
            raise ValueError(f"Unknown request: {request_id}")

        request = self._requests[request_id]

        if request.status != ServiceStatus.ACCEPTED:
            raise ValueError(f"Request not accepted: {request.status}")

        request.status = ServiceStatus.IN_PROGRESS
        start_time = datetime.now(timezone.utc)

        try:
            # Get handler
            handler = self._service_handlers.get(request.service_id)

            if handler:
                # Execute with handler
                output = await handler(request)
            else:
                # Default handler - simulate execution
                output = await self._default_handler(request)

            end_time = datetime.now(timezone.utc)
            execution_time = (end_time - start_time).total_seconds()

            # Record success
            request.status = ServiceStatus.COMPLETED
            request.result = output
            request.completed_at = end_time.isoformat()

            # Record revenue
            revenue = request.price.amount if request.price else 0.0
            self._record_revenue(request.service_id, revenue, RevenueSource.SERVICES)

            # Deposit to treasury
            await self._treasury.deposit(
                AssetType.USD,
                revenue,
                f"service_{request_id}"
            )

            self._requests_completed += 1

            result = ServiceResult(
                request_id=request_id,
                success=True,
                output=output,
                execution_time=execution_time,
                tokens_used=output.get('tokens_used', 0),
                revenue=revenue,
                currency=request.price.currency if request.price else Currency.USD
            )

            logger.info(f"Completed request {request_id}, revenue: ${revenue}")

            return result

        except Exception as e:
            logger.error(f"Service execution failed: {e}")

            request.status = ServiceStatus.FAILED
            request.result = {'error': str(e)}

            self._requests_failed += 1

            return ServiceResult(
                request_id=request_id,
                success=False,
                output={'error': str(e)},
                execution_time=0.0,
                tokens_used=0,
                revenue=0.0,
                currency=Currency.USD
            )

    async def _default_handler(
        self,
        request: ServiceRequest
    ) -> Dict:
        """Default service handler (simulation)."""
        # Simulate some work
        await asyncio.sleep(0.1)

        return {
            'status': 'completed',
            'tokens_used': 100,
            'output': f"Simulated output for {request.service_id}",
            'request_params': request.parameters
        }

    def _record_revenue(
        self,
        service_id: str,
        amount: float,
        source: RevenueSource
    ) -> None:
        """Record revenue internally."""
        self._revenue_by_service[service_id] = (
            self._revenue_by_service.get(service_id, 0.0) + amount
        )
        self._revenue_by_source[source] += amount
        self._total_revenue += amount

    async def manage_treasury(self) -> TreasuryReport:
        """
        Manage treasury holdings and allocations.

        Returns:
            TreasuryReport with current status
        """
        return await self._treasury.get_treasury_report()

    async def allocate_revenue(self) -> Dict[str, float]:
        """
        Allocate accumulated revenue according to policy.

        Returns:
            Dict of allocations made
        """
        # Get available USD balance
        usd_balance = await self._treasury.get_balance(AssetType.USD)
        available = usd_balance.available

        if available <= 0:
            return {}

        allocations = {}

        # Allocate according to policy
        policy = self._treasury._allocation_policy

        for category_name, ratio in policy.items():
            category = AllocationCategory(category_name)
            amount = available * ratio

            if amount > 0:
                result = await self._treasury.allocate(
                    category=category,
                    asset=AssetType.USD,
                    amount=amount,
                    purpose=f"Auto-allocation from revenue"
                )

                if result.success:
                    allocations[category_name] = amount

        return allocations

    def get_revenue_report(
        self,
        period_start: str = None,
        period_end: str = None
    ) -> RevenueReport:
        """
        Get revenue report for a period.

        Args:
            period_start: Start of period
            period_end: End of period

        Returns:
            RevenueReport
        """
        now = datetime.now(timezone.utc).isoformat()

        return RevenueReport(
            period_start=period_start or now,
            period_end=period_end or now,
            total_revenue=self._total_revenue,
            currency=Currency.USD,
            revenue_by_service=self._revenue_by_service.copy(),
            revenue_by_source={
                s.value: v for s, v in self._revenue_by_source.items()
            },
            requests_completed=self._requests_completed,
            requests_failed=self._requests_failed
        )

    def get_request(self, request_id: str) -> Optional[ServiceRequest]:
        """Get request by ID."""
        return self._requests.get(request_id)

    def get_pending_requests(self) -> List[ServiceRequest]:
        """Get all pending requests."""
        return [
            r for r in self._requests.values()
            if r.status in [ServiceStatus.PENDING, ServiceStatus.PRICING, ServiceStatus.ACCEPTED]
        ]

    def get_service_catalog(self) -> List[ServiceDefinition]:
        """Get available services."""
        return self._pricing_engine.get_all_services()

    @property
    def pricing(self) -> PricingEngine:
        """Get pricing engine."""
        return self._pricing_engine

    @property
    def treasury(self) -> BitcoinTreasury:
        """Get treasury."""
        return self._treasury

    def get_stats(self) -> Dict:
        """Get agency statistics."""
        return {
            'total_revenue': self._total_revenue,
            'requests_completed': self._requests_completed,
            'requests_failed': self._requests_failed,
            'pending_requests': len(self.get_pending_requests()),
            'registered_handlers': len(self._service_handlers),
            'revenue_by_service': self._revenue_by_service.copy(),
            'pricing_stats': self._pricing_engine.get_stats(),
            'treasury_stats': self._treasury.get_stats()
        }

    def reset(self) -> None:
        """Reset agency state."""
        self._requests.clear()
        self._request_counter = 0
        self._revenue_by_service.clear()
        self._revenue_by_source = {source: 0.0 for source in RevenueSource}
        self._total_revenue = 0.0
        self._requests_completed = 0
        self._requests_failed = 0
        self._pricing_engine.reset()
        self._treasury.reset()
        logger.info("EconomicAgency reset")

"""
Service Marketplace.

Exposes BYRD's capabilities as paid services.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5.2 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

from .pricing import ServiceDefinition, Price, Currency, PricingModel

logger = logging.getLogger("rsi.economic.marketplace")


class ListingStatus(Enum):
    """Status of a marketplace listing."""
    DRAFT = "draft"           # Not yet published
    ACTIVE = "active"         # Available for purchase
    SUSPENDED = "suspended"   # Temporarily unavailable
    RETIRED = "retired"       # No longer offered


class PaymentStatus(Enum):
    """Status of a payment."""
    PENDING = "pending"       # Awaiting payment
    PROCESSING = "processing" # Payment being processed
    COMPLETED = "completed"   # Payment received
    FAILED = "failed"         # Payment failed
    REFUNDED = "refunded"     # Payment refunded


@dataclass
class ServiceListing:
    """A service listing in the marketplace."""
    id: str
    service_id: str
    name: str
    description: str
    category: str
    price: Price
    status: ListingStatus
    created_at: str
    updated_at: str
    sales_count: int = 0
    rating: float = 0.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'service_id': self.service_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price.to_dict(),
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sales_count': self.sales_count,
            'rating': self.rating,
            'tags': self.tags,
            'metadata': self.metadata
        }


@dataclass
class PaymentRequest:
    """A payment request for a service."""
    id: str
    listing_id: str
    buyer: str
    amount: float
    currency: Currency
    status: PaymentStatus
    created_at: str
    completed_at: Optional[str] = None
    transaction_ref: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'listing_id': self.listing_id,
            'buyer': self.buyer,
            'amount': self.amount,
            'currency': self.currency.value,
            'status': self.status.value,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'transaction_ref': self.transaction_ref,
            'metadata': self.metadata
        }


@dataclass
class MarketplaceStats:
    """Statistics for the marketplace."""
    total_listings: int
    active_listings: int
    total_sales: int
    total_revenue: float
    currency: Currency
    sales_by_category: Dict[str, int]
    revenue_by_category: Dict[str, float]
    top_services: List[Dict]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'total_listings': self.total_listings,
            'active_listings': self.active_listings,
            'total_sales': self.total_sales,
            'total_revenue': self.total_revenue,
            'currency': self.currency.value,
            'sales_by_category': self.sales_by_category,
            'revenue_by_category': self.revenue_by_category,
            'top_services': self.top_services
        }


class ServiceMarketplace:
    """
    Marketplace for BYRD's services.

    Handles listing discovery, payment processing,
    and service fulfillment.
    """

    def __init__(self, config: Dict = None):
        """Initialize marketplace."""
        self.config = config or {}

        # Listings
        self._listings: Dict[str, ServiceListing] = {}
        self._listing_counter: int = 0

        # Payments
        self._payments: Dict[str, PaymentRequest] = {}
        self._payment_counter: int = 0

        # Payment processor (callback)
        self._payment_processor: Optional[Callable[[PaymentRequest], Awaitable[bool]]] = None

        # Fulfillment handler (callback)
        self._fulfillment_handler: Optional[Callable[[str, str], Awaitable[Dict]]] = None

        # Revenue tracking
        self._total_revenue: float = 0.0
        self._revenue_by_category: Dict[str, float] = {}
        self._sales_by_category: Dict[str, int] = {}

    def create_listing(
        self,
        service: ServiceDefinition,
        price: Price,
        tags: List[str] = None
    ) -> ServiceListing:
        """
        Create a new marketplace listing.

        Args:
            service: Service definition
            price: Listing price
            tags: Search tags

        Returns:
            ServiceListing
        """
        self._listing_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        listing = ServiceListing(
            id=f"listing_{self._listing_counter}",
            service_id=service.id,
            name=service.name,
            description=service.description,
            category=service.category,
            price=price,
            status=ListingStatus.DRAFT,
            created_at=now,
            updated_at=now,
            tags=tags or []
        )

        self._listings[listing.id] = listing

        logger.info(f"Created listing {listing.id} for {service.id}")

        return listing

    def publish_listing(self, listing_id: str) -> bool:
        """
        Publish a listing (make it active).

        Args:
            listing_id: ID of the listing

        Returns:
            True if published
        """
        if listing_id not in self._listings:
            return False

        listing = self._listings[listing_id]

        if listing.status == ListingStatus.RETIRED:
            return False

        listing.status = ListingStatus.ACTIVE
        listing.updated_at = datetime.now(timezone.utc).isoformat()

        logger.info(f"Published listing {listing_id}")

        return True

    def suspend_listing(self, listing_id: str) -> bool:
        """Suspend a listing temporarily."""
        if listing_id not in self._listings:
            return False

        listing = self._listings[listing_id]
        listing.status = ListingStatus.SUSPENDED
        listing.updated_at = datetime.now(timezone.utc).isoformat()

        return True

    def retire_listing(self, listing_id: str) -> bool:
        """Retire a listing permanently."""
        if listing_id not in self._listings:
            return False

        listing = self._listings[listing_id]
        listing.status = ListingStatus.RETIRED
        listing.updated_at = datetime.now(timezone.utc).isoformat()

        return True

    def search_listings(
        self,
        query: str = None,
        category: str = None,
        tags: List[str] = None,
        max_price: float = None,
        status: ListingStatus = ListingStatus.ACTIVE
    ) -> List[ServiceListing]:
        """
        Search marketplace listings.

        Args:
            query: Text search query
            category: Filter by category
            tags: Filter by tags
            max_price: Maximum price filter
            status: Filter by status

        Returns:
            List of matching listings
        """
        results = []

        for listing in self._listings.values():
            # Status filter
            if listing.status != status:
                continue

            # Category filter
            if category and listing.category != category:
                continue

            # Price filter
            if max_price and listing.price.amount > max_price:
                continue

            # Tag filter
            if tags:
                if not any(t in listing.tags for t in tags):
                    continue

            # Text search
            if query:
                query_lower = query.lower()
                searchable = f"{listing.name} {listing.description}".lower()
                if query_lower not in searchable:
                    continue

            results.append(listing)

        # Sort by sales count (popularity)
        results.sort(key=lambda l: l.sales_count, reverse=True)

        return results

    def get_listing(self, listing_id: str) -> Optional[ServiceListing]:
        """Get listing by ID."""
        return self._listings.get(listing_id)

    def get_listings_by_category(
        self,
        category: str
    ) -> List[ServiceListing]:
        """Get all active listings in a category."""
        return [
            l for l in self._listings.values()
            if l.category == category and l.status == ListingStatus.ACTIVE
        ]

    def set_payment_processor(
        self,
        processor: Callable[[PaymentRequest], Awaitable[bool]]
    ) -> None:
        """
        Set the payment processor callback.

        Args:
            processor: Async function that processes payments
        """
        self._payment_processor = processor

    def set_fulfillment_handler(
        self,
        handler: Callable[[str, str], Awaitable[Dict]]
    ) -> None:
        """
        Set the fulfillment handler callback.

        Args:
            handler: Async function (listing_id, buyer) -> result
        """
        self._fulfillment_handler = handler

    async def initiate_purchase(
        self,
        listing_id: str,
        buyer: str
    ) -> PaymentRequest:
        """
        Initiate a purchase.

        Args:
            listing_id: ID of the listing to purchase
            buyer: Buyer identifier

        Returns:
            PaymentRequest for the purchase
        """
        if listing_id not in self._listings:
            raise ValueError(f"Unknown listing: {listing_id}")

        listing = self._listings[listing_id]

        if listing.status != ListingStatus.ACTIVE:
            raise ValueError(f"Listing not active: {listing.status}")

        self._payment_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        payment = PaymentRequest(
            id=f"pay_{self._payment_counter}",
            listing_id=listing_id,
            buyer=buyer,
            amount=listing.price.amount,
            currency=listing.price.currency,
            status=PaymentStatus.PENDING,
            created_at=now
        )

        self._payments[payment.id] = payment

        logger.info(f"Initiated purchase {payment.id} for listing {listing_id}")

        return payment

    async def process_payment(
        self,
        payment_id: str
    ) -> bool:
        """
        Process a pending payment.

        Args:
            payment_id: ID of the payment

        Returns:
            True if payment successful
        """
        if payment_id not in self._payments:
            return False

        payment = self._payments[payment_id]

        if payment.status != PaymentStatus.PENDING:
            return False

        payment.status = PaymentStatus.PROCESSING

        # Use payment processor if available
        if self._payment_processor:
            success = await self._payment_processor(payment)
        else:
            # Default: simulate successful payment
            success = True

        if success:
            payment.status = PaymentStatus.COMPLETED
            payment.completed_at = datetime.now(timezone.utc).isoformat()

            # Update listing stats
            listing = self._listings[payment.listing_id]
            listing.sales_count += 1

            # Track revenue
            self._total_revenue += payment.amount
            self._revenue_by_category[listing.category] = (
                self._revenue_by_category.get(listing.category, 0.0) + payment.amount
            )
            self._sales_by_category[listing.category] = (
                self._sales_by_category.get(listing.category, 0) + 1
            )

            logger.info(f"Payment {payment_id} completed: ${payment.amount}")

        else:
            payment.status = PaymentStatus.FAILED

        return success

    async def fulfill_purchase(
        self,
        payment_id: str
    ) -> Optional[Dict]:
        """
        Fulfill a completed purchase.

        Args:
            payment_id: ID of the payment

        Returns:
            Fulfillment result
        """
        if payment_id not in self._payments:
            return None

        payment = self._payments[payment_id]

        if payment.status != PaymentStatus.COMPLETED:
            return None

        # Use fulfillment handler if available
        if self._fulfillment_handler:
            result = await self._fulfillment_handler(
                payment.listing_id,
                payment.buyer
            )
        else:
            # Default: return basic confirmation
            result = {
                'status': 'fulfilled',
                'payment_id': payment_id,
                'listing_id': payment.listing_id,
                'buyer': payment.buyer
            }

        return result

    async def complete_purchase(
        self,
        listing_id: str,
        buyer: str
    ) -> Dict:
        """
        Complete a full purchase flow: initiate, pay, fulfill.

        Args:
            listing_id: ID of the listing
            buyer: Buyer identifier

        Returns:
            Purchase result
        """
        # Initiate
        payment = await self.initiate_purchase(listing_id, buyer)

        # Process payment
        success = await self.process_payment(payment.id)

        if not success:
            return {
                'success': False,
                'error': 'Payment failed',
                'payment_id': payment.id
            }

        # Fulfill
        result = await self.fulfill_purchase(payment.id)

        return {
            'success': True,
            'payment_id': payment.id,
            'listing_id': listing_id,
            'amount': payment.amount,
            'currency': payment.currency.value,
            'fulfillment': result
        }

    def get_marketplace_stats(self) -> MarketplaceStats:
        """Get marketplace statistics."""
        active = [l for l in self._listings.values() if l.status == ListingStatus.ACTIVE]

        # Get top services by sales
        top_services = sorted(
            self._listings.values(),
            key=lambda l: l.sales_count,
            reverse=True
        )[:5]

        return MarketplaceStats(
            total_listings=len(self._listings),
            active_listings=len(active),
            total_sales=sum(l.sales_count for l in self._listings.values()),
            total_revenue=self._total_revenue,
            currency=Currency.USD,
            sales_by_category=self._sales_by_category.copy(),
            revenue_by_category=self._revenue_by_category.copy(),
            top_services=[
                {'id': s.id, 'name': s.name, 'sales': s.sales_count}
                for s in top_services
            ]
        )

    def get_payment(self, payment_id: str) -> Optional[PaymentRequest]:
        """Get payment by ID."""
        return self._payments.get(payment_id)

    def get_pending_payments(self) -> List[PaymentRequest]:
        """Get all pending payments."""
        return [
            p for p in self._payments.values()
            if p.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]
        ]

    def get_stats(self) -> Dict:
        """Get marketplace statistics."""
        return {
            'total_listings': len(self._listings),
            'active_listings': len([l for l in self._listings.values() if l.status == ListingStatus.ACTIVE]),
            'total_payments': len(self._payments),
            'completed_payments': len([p for p in self._payments.values() if p.status == PaymentStatus.COMPLETED]),
            'total_revenue': self._total_revenue,
            'sales_by_category': self._sales_by_category.copy()
        }

    def reset(self) -> None:
        """Reset marketplace state."""
        self._listings.clear()
        self._listing_counter = 0
        self._payments.clear()
        self._payment_counter = 0
        self._total_revenue = 0.0
        self._revenue_by_category.clear()
        self._sales_by_category.clear()
        logger.info("ServiceMarketplace reset")

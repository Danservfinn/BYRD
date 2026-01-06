"""
Economic Module.

Enables economic autonomy through services, treasury, and self-investment.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5 for specification.
"""

from .pricing import (
    PricingModel,
    Currency,
    ServiceTier,
    CostBreakdown,
    Price,
    ServiceDefinition,
    PricingEngine,
)

from .treasury import (
    AssetType,
    AllocationCategory,
    TransactionType,
    Balance,
    Allocation,
    Transaction,
    AllocationResult,
    TreasuryReport,
    BitcoinTreasury,
)

from .agency import (
    ServiceStatus,
    RevenueSource,
    ServiceRequest,
    ServiceResult,
    RevenueReport,
    EconomicAgency,
)

from .marketplace import (
    ListingStatus,
    PaymentStatus,
    ServiceListing,
    PaymentRequest,
    MarketplaceStats,
    ServiceMarketplace,
)

from .training_investment import (
    InvestmentType,
    InvestmentStatus,
    ROICategory,
    TrainingGoal,
    Investment,
    ROIReport,
    SelfTrainingInvestor,
)

__all__ = [
    # Pricing
    "PricingModel",
    "Currency",
    "ServiceTier",
    "CostBreakdown",
    "Price",
    "ServiceDefinition",
    "PricingEngine",
    # Treasury
    "AssetType",
    "AllocationCategory",
    "TransactionType",
    "Balance",
    "Allocation",
    "Transaction",
    "AllocationResult",
    "TreasuryReport",
    "BitcoinTreasury",
    # Agency
    "ServiceStatus",
    "RevenueSource",
    "ServiceRequest",
    "ServiceResult",
    "RevenueReport",
    "EconomicAgency",
    # Marketplace
    "ListingStatus",
    "PaymentStatus",
    "ServiceListing",
    "PaymentRequest",
    "MarketplaceStats",
    "ServiceMarketplace",
    # Training Investment
    "InvestmentType",
    "InvestmentStatus",
    "ROICategory",
    "TrainingGoal",
    "Investment",
    "ROIReport",
    "SelfTrainingInvestor",
]

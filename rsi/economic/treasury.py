"""
Treasury Management.

Manages BYRD's financial holdings with censorship-resistant storage.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 5.3 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

logger = logging.getLogger("rsi.economic.treasury")


class AssetType(Enum):
    """Types of treasury assets."""
    BTC = "btc"           # Bitcoin
    ETH = "eth"           # Ethereum
    USDC = "usdc"         # USD Coin
    USD = "usd"           # Fiat USD
    COMPUTE = "compute"   # Compute credits


class AllocationCategory(Enum):
    """Categories for fund allocation."""
    OPERATIONAL = "operational"     # Day-to-day operations
    COMPUTE = "compute"             # Compute resources
    TRAINING = "training"           # Self-training investment
    RESERVE = "reserve"             # Emergency reserve
    GROWTH = "growth"               # Capability expansion


class TransactionType(Enum):
    """Types of treasury transactions."""
    DEPOSIT = "deposit"         # Incoming funds
    WITHDRAWAL = "withdrawal"   # Outgoing funds
    ALLOCATION = "allocation"   # Internal allocation
    TRANSFER = "transfer"       # Between categories
    CONVERSION = "conversion"   # Currency conversion


@dataclass
class Balance:
    """Balance of an asset."""
    asset: AssetType
    amount: float
    locked_amount: float = 0.0  # Amount locked for pending operations
    last_updated: str = ""

    @property
    def available(self) -> float:
        """Get available (unlocked) amount."""
        return self.amount - self.locked_amount

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'asset': self.asset.value,
            'amount': self.amount,
            'locked_amount': self.locked_amount,
            'available': self.available,
            'last_updated': self.last_updated
        }


@dataclass
class Allocation:
    """Fund allocation to a category."""
    category: AllocationCategory
    asset: AssetType
    amount: float
    purpose: str
    created_at: str
    expires_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'category': self.category.value,
            'asset': self.asset.value,
            'amount': self.amount,
            'purpose': self.purpose,
            'created_at': self.created_at,
            'expires_at': self.expires_at
        }


@dataclass
class Transaction:
    """A treasury transaction."""
    id: str
    transaction_type: TransactionType
    asset: AssetType
    amount: float
    from_category: Optional[AllocationCategory] = None
    to_category: Optional[AllocationCategory] = None
    description: str = ""
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'transaction_type': self.transaction_type.value,
            'asset': self.asset.value,
            'amount': self.amount,
            'from_category': self.from_category.value if self.from_category else None,
            'to_category': self.to_category.value if self.to_category else None,
            'description': self.description,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


@dataclass
class AllocationResult:
    """Result of an allocation operation."""
    success: bool
    allocation: Optional[Allocation]
    transaction: Optional[Transaction]
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'allocation': self.allocation.to_dict() if self.allocation else None,
            'transaction': self.transaction.to_dict() if self.transaction else None,
            'error': self.error
        }


@dataclass
class TreasuryReport:
    """Comprehensive treasury report."""
    timestamp: str
    balances: Dict[str, Balance]
    allocations: Dict[str, List[Allocation]]
    total_value_usd: float
    allocation_summary: Dict[str, float]  # Category -> total amount
    recent_transactions: List[Transaction]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'balances': {k: v.to_dict() for k, v in self.balances.items()},
            'allocations': {
                k: [a.to_dict() for a in v]
                for k, v in self.allocations.items()
            },
            'total_value_usd': self.total_value_usd,
            'allocation_summary': self.allocation_summary,
            'recent_transactions': [t.to_dict() for t in self.recent_transactions],
            'metadata': self.metadata
        }


class BitcoinTreasury:
    """
    Censorship-resistant treasury management.

    Uses Bitcoin for secure, decentralized fund storage.
    Starts in simulation mode, can be upgraded to testnet/mainnet.
    """

    def __init__(self, config: Dict = None):
        """Initialize treasury."""
        self.config = config or {}

        # Mode: simulation, testnet, mainnet
        self._mode = self.config.get('mode', 'simulation')

        # Balances by asset type
        self._balances: Dict[AssetType, Balance] = {}
        self._initialize_balances()

        # Allocations by category
        self._allocations: Dict[AllocationCategory, List[Allocation]] = {
            cat: [] for cat in AllocationCategory
        }

        # Transaction history
        self._transactions: List[Transaction] = []
        self._transaction_counter: int = 0

        # Allocation policies
        self._allocation_policy = self.config.get('allocation_policy', {
            AllocationCategory.OPERATIONAL.value: 0.20,   # 20% operational
            AllocationCategory.COMPUTE.value: 0.30,       # 30% compute
            AllocationCategory.TRAINING.value: 0.25,      # 25% training
            AllocationCategory.RESERVE.value: 0.15,       # 15% reserve
            AllocationCategory.GROWTH.value: 0.10,        # 10% growth
        })

        # USD conversion rates (simplified)
        self._usd_rates = {
            AssetType.BTC: 42000.0,
            AssetType.ETH: 2500.0,
            AssetType.USDC: 1.0,
            AssetType.USD: 1.0,
            AssetType.COMPUTE: 0.10,  # $0.10 per compute credit
        }

        # Statistics
        self._total_deposited: float = 0.0
        self._total_withdrawn: float = 0.0

    def _initialize_balances(self) -> None:
        """Initialize empty balances."""
        now = datetime.now(timezone.utc).isoformat()
        for asset in AssetType:
            self._balances[asset] = Balance(
                asset=asset,
                amount=0.0,
                locked_amount=0.0,
                last_updated=now
            )

        # Add initial simulation balance
        if self._mode == 'simulation':
            self._balances[AssetType.BTC].amount = 0.01  # 0.01 BTC for testing
            self._balances[AssetType.USD].amount = 100.0  # $100 for testing

    async def get_balance(self, asset: AssetType = None) -> Balance:
        """
        Get current balance.

        Args:
            asset: Specific asset, or None for BTC

        Returns:
            Balance object
        """
        asset = asset or AssetType.BTC
        return self._balances.get(asset, Balance(asset=asset, amount=0.0))

    async def get_all_balances(self) -> Dict[AssetType, Balance]:
        """Get all balances."""
        return self._balances.copy()

    async def deposit(
        self,
        asset: AssetType,
        amount: float,
        source: str = "external"
    ) -> Transaction:
        """
        Record a deposit.

        Args:
            asset: Asset type
            amount: Amount to deposit
            source: Source of funds

        Returns:
            Transaction record
        """
        self._transaction_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        # Update balance
        self._balances[asset].amount += amount
        self._balances[asset].last_updated = now

        # Create transaction
        tx = Transaction(
            id=f"tx_{self._transaction_counter}",
            transaction_type=TransactionType.DEPOSIT,
            asset=asset,
            amount=amount,
            description=f"Deposit from {source}",
            timestamp=now,
            metadata={'source': source}
        )

        self._transactions.append(tx)
        self._total_deposited += amount * self._usd_rates.get(asset, 1.0)

        logger.info(f"Deposited {amount} {asset.value} from {source}")

        return tx

    async def withdraw(
        self,
        asset: AssetType,
        amount: float,
        destination: str
    ) -> Optional[Transaction]:
        """
        Process a withdrawal.

        Args:
            asset: Asset type
            amount: Amount to withdraw
            destination: Destination address/account

        Returns:
            Transaction if successful, None if insufficient funds
        """
        balance = self._balances[asset]

        if balance.available < amount:
            logger.warning(f"Insufficient funds: {balance.available} < {amount}")
            return None

        self._transaction_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        # Update balance
        balance.amount -= amount
        balance.last_updated = now

        # Create transaction
        tx = Transaction(
            id=f"tx_{self._transaction_counter}",
            transaction_type=TransactionType.WITHDRAWAL,
            asset=asset,
            amount=amount,
            description=f"Withdrawal to {destination}",
            timestamp=now,
            metadata={'destination': destination}
        )

        self._transactions.append(tx)
        self._total_withdrawn += amount * self._usd_rates.get(asset, 1.0)

        logger.info(f"Withdrew {amount} {asset.value} to {destination}")

        return tx

    async def allocate_for_compute(
        self,
        amount: float,
        provider: str = "default"
    ) -> AllocationResult:
        """
        Allocate funds for compute acquisition.

        Args:
            amount: Amount in primary asset (BTC)
            provider: Compute provider name

        Returns:
            AllocationResult with outcome
        """
        return await self.allocate(
            category=AllocationCategory.COMPUTE,
            asset=AssetType.BTC,
            amount=amount,
            purpose=f"Compute acquisition from {provider}"
        )

    async def allocate_for_training(
        self,
        amount: float,
        training_goal: str = "capability_improvement"
    ) -> AllocationResult:
        """
        Allocate funds for self-training.

        Args:
            amount: Amount to allocate
            training_goal: Description of training goal

        Returns:
            AllocationResult with outcome
        """
        return await self.allocate(
            category=AllocationCategory.TRAINING,
            asset=AssetType.BTC,
            amount=amount,
            purpose=f"Self-training: {training_goal}"
        )

    async def allocate(
        self,
        category: AllocationCategory,
        asset: AssetType,
        amount: float,
        purpose: str
    ) -> AllocationResult:
        """
        Allocate funds to a category.

        Args:
            category: Target category
            asset: Asset type
            amount: Amount to allocate
            purpose: Purpose description

        Returns:
            AllocationResult with outcome
        """
        balance = self._balances[asset]

        if balance.available < amount:
            return AllocationResult(
                success=False,
                allocation=None,
                transaction=None,
                error=f"Insufficient funds: {balance.available} < {amount}"
            )

        self._transaction_counter += 1
        now = datetime.now(timezone.utc).isoformat()

        # Lock the funds
        balance.locked_amount += amount
        balance.last_updated = now

        # Create allocation
        allocation = Allocation(
            category=category,
            asset=asset,
            amount=amount,
            purpose=purpose,
            created_at=now
        )

        self._allocations[category].append(allocation)

        # Create transaction
        tx = Transaction(
            id=f"tx_{self._transaction_counter}",
            transaction_type=TransactionType.ALLOCATION,
            asset=asset,
            amount=amount,
            to_category=category,
            description=purpose,
            timestamp=now
        )

        self._transactions.append(tx)

        logger.info(f"Allocated {amount} {asset.value} to {category.value}: {purpose}")

        return AllocationResult(
            success=True,
            allocation=allocation,
            transaction=tx
        )

    async def release_allocation(
        self,
        category: AllocationCategory,
        amount: float,
        asset: AssetType = AssetType.BTC
    ) -> bool:
        """
        Release allocated funds back to available balance.

        Args:
            category: Category to release from
            amount: Amount to release
            asset: Asset type

        Returns:
            True if successful
        """
        balance = self._balances[asset]

        if balance.locked_amount < amount:
            return False

        balance.locked_amount -= amount
        balance.last_updated = datetime.now(timezone.utc).isoformat()

        # Remove from allocations
        allocations = self._allocations[category]
        released = 0.0
        remaining = []

        for alloc in allocations:
            if alloc.asset == asset and released < amount:
                if alloc.amount <= (amount - released):
                    released += alloc.amount
                else:
                    alloc.amount -= (amount - released)
                    remaining.append(alloc)
                    released = amount
            else:
                remaining.append(alloc)

        self._allocations[category] = remaining

        return True

    async def get_treasury_report(self) -> TreasuryReport:
        """
        Generate comprehensive treasury report.

        Returns:
            TreasuryReport with full treasury status
        """
        # Calculate total value in USD
        total_usd = 0.0
        for asset, balance in self._balances.items():
            rate = self._usd_rates.get(asset, 1.0)
            total_usd += balance.amount * rate

        # Calculate allocation summary
        allocation_summary = {}
        for category, allocations in self._allocations.items():
            total = sum(a.amount * self._usd_rates.get(a.asset, 1.0) for a in allocations)
            allocation_summary[category.value] = total

        # Get recent transactions
        recent = self._transactions[-20:] if self._transactions else []

        return TreasuryReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            balances={a.value: b for a, b in self._balances.items()},
            allocations={c.value: list(a) for c, a in self._allocations.items()},
            total_value_usd=total_usd,
            allocation_summary=allocation_summary,
            recent_transactions=recent,
            metadata={
                'mode': self._mode,
                'total_deposited': self._total_deposited,
                'total_withdrawn': self._total_withdrawn
            }
        )

    def get_allocation_by_category(
        self,
        category: AllocationCategory
    ) -> List[Allocation]:
        """Get allocations for a category."""
        return self._allocations.get(category, [])

    def get_transaction_history(
        self,
        limit: int = None
    ) -> List[Transaction]:
        """Get transaction history."""
        if limit:
            return self._transactions[-limit:]
        return self._transactions.copy()

    def get_mode(self) -> str:
        """Get current treasury mode."""
        return self._mode

    def upgrade_to_testnet(self) -> bool:
        """Upgrade to testnet mode."""
        if self._mode == 'simulation':
            self._mode = 'testnet'
            logger.info("Treasury upgraded to testnet mode")
            return True
        return False

    def get_stats(self) -> Dict:
        """Get treasury statistics."""
        return {
            'mode': self._mode,
            'total_deposited_usd': self._total_deposited,
            'total_withdrawn_usd': self._total_withdrawn,
            'transaction_count': len(self._transactions),
            'balances': {
                a.value: b.amount for a, b in self._balances.items()
            },
            'allocations_by_category': {
                c.value: len(a) for c, a in self._allocations.items()
            }
        }

    def reset(self) -> None:
        """Reset treasury state."""
        self._initialize_balances()
        self._allocations = {cat: [] for cat in AllocationCategory}
        self._transactions.clear()
        self._transaction_counter = 0
        self._total_deposited = 0.0
        self._total_withdrawn = 0.0
        logger.info("BitcoinTreasury reset")

"""
Tests for Phase 5: Economic Autonomy.

Tests the economic module (pricing, treasury, agency,
marketplace, and self-training investment).
"""

import pytest
import asyncio
from datetime import datetime, timezone

# Economic module imports
from rsi.economic import (
    # Pricing
    PricingModel,
    Currency,
    ServiceTier,
    CostBreakdown,
    Price,
    ServiceDefinition,
    PricingEngine,
    # Treasury
    AssetType,
    AllocationCategory,
    TransactionType,
    Balance,
    Allocation,
    Transaction,
    AllocationResult,
    TreasuryReport,
    BitcoinTreasury,
    # Agency
    ServiceStatus,
    RevenueSource,
    ServiceRequest,
    ServiceResult,
    RevenueReport,
    EconomicAgency,
    # Marketplace
    ListingStatus,
    PaymentStatus,
    ServiceListing,
    PaymentRequest,
    MarketplaceStats,
    ServiceMarketplace,
    # Training Investment
    InvestmentType,
    InvestmentStatus,
    ROICategory,
    TrainingGoal,
    Investment,
    ROIReport,
    SelfTrainingInvestor,
)


# ===================== Pricing Engine Tests =====================

class TestPricingEngine:
    """Tests for PricingEngine."""

    def test_initialization(self):
        """Test engine initializes correctly."""
        engine = PricingEngine()
        services = engine.get_all_services()
        assert len(services) >= 6  # Default services

    def test_default_services_registered(self):
        """Test default services are registered."""
        engine = PricingEngine()

        code_review = engine.get_service('code_review')
        assert code_review is not None
        assert code_review.category == 'development'

        architecture = engine.get_service('architecture_design')
        assert architecture is not None
        assert architecture.pricing_model == PricingModel.FIXED

    def test_calculate_price(self):
        """Test price calculation."""
        engine = PricingEngine()

        price = engine.calculate_price('code_review')

        assert price is not None
        assert price.amount > 0
        assert price.currency == Currency.USD
        assert price.breakdown is not None

    def test_calculate_price_with_context(self):
        """Test price calculation with context."""
        engine = PricingEngine()

        # Simple context
        price1 = engine.calculate_price('code_review', {'tokens': 100})

        # Complex context
        price2 = engine.calculate_price('code_review', {
            'tokens': 1000,
            'complexity': 0.9
        })

        # More complex should cost more
        assert price2.amount > price1.amount

    def test_cost_breakdown(self):
        """Test cost breakdown calculation."""
        breakdown = CostBreakdown(
            compute_cost=0.10,
            storage_cost=0.01,
            bandwidth_cost=0.02,
            overhead_cost=0.02,
            margin=0.30
        )

        # Total should include margin
        expected = (0.10 + 0.01 + 0.02 + 0.02) * 1.30
        assert abs(breakdown.total_cost - expected) < 0.001

    def test_price_conversion(self):
        """Test currency conversion."""
        engine = PricingEngine()

        usd_price = engine.calculate_price('code_review')
        btc_price = engine.convert_price(usd_price, Currency.BTC)

        assert btc_price.currency == Currency.BTC
        assert btc_price.amount < usd_price.amount  # BTC amount should be smaller

    def test_services_by_category(self):
        """Test filtering services by category."""
        engine = PricingEngine()

        dev_services = engine.get_services_by_category('development')
        assert len(dev_services) >= 3

        for service in dev_services:
            assert service.category == 'development'

    def test_demand_multiplier(self):
        """Test demand-based pricing."""
        engine = PricingEngine()

        # Calculate multiple times to increase demand
        for _ in range(15):
            engine.calculate_price('code_review')

        # Demand multiplier should have increased
        mult = engine._get_demand_multiplier('code_review')
        assert mult > 1.0


# ===================== Treasury Tests =====================

class TestBitcoinTreasury:
    """Tests for BitcoinTreasury."""

    def test_initialization(self):
        """Test treasury initializes correctly."""
        treasury = BitcoinTreasury()

        assert treasury.get_mode() == 'simulation'
        stats = treasury.get_stats()
        assert stats['mode'] == 'simulation'

    @pytest.mark.asyncio
    async def test_get_balance(self):
        """Test getting balance."""
        treasury = BitcoinTreasury()

        btc_balance = await treasury.get_balance(AssetType.BTC)
        assert btc_balance is not None
        assert btc_balance.asset == AssetType.BTC

        # Simulation mode has initial balance
        assert btc_balance.amount == 0.01

    @pytest.mark.asyncio
    async def test_deposit(self):
        """Test depositing funds."""
        treasury = BitcoinTreasury()

        initial = await treasury.get_balance(AssetType.USD)
        initial_amount = initial.amount

        tx = await treasury.deposit(AssetType.USD, 50.0, "test_deposit")

        assert tx is not None
        assert tx.transaction_type == TransactionType.DEPOSIT
        assert tx.amount == 50.0

        new_balance = await treasury.get_balance(AssetType.USD)
        assert new_balance.amount == initial_amount + 50.0

    @pytest.mark.asyncio
    async def test_withdraw(self):
        """Test withdrawing funds."""
        treasury = BitcoinTreasury()

        # Deposit first
        await treasury.deposit(AssetType.USD, 100.0, "test")

        tx = await treasury.withdraw(AssetType.USD, 30.0, "test_destination")

        assert tx is not None
        assert tx.amount == 30.0

        balance = await treasury.get_balance(AssetType.USD)
        # 100 (initial simulation) + 100 (deposit) - 30 (withdrawal) = 170
        assert balance.amount == 170.0

    @pytest.mark.asyncio
    async def test_insufficient_funds(self):
        """Test withdrawal with insufficient funds."""
        treasury = BitcoinTreasury()

        tx = await treasury.withdraw(AssetType.USD, 10000.0, "test")

        assert tx is None  # Should fail

    @pytest.mark.asyncio
    async def test_allocate_for_compute(self):
        """Test allocating funds for compute."""
        treasury = BitcoinTreasury()

        result = await treasury.allocate_for_compute(0.005, "test_provider")

        assert result.success
        assert result.allocation is not None
        assert result.allocation.category == AllocationCategory.COMPUTE

    @pytest.mark.asyncio
    async def test_allocate_for_training(self):
        """Test allocating funds for training."""
        treasury = BitcoinTreasury()

        result = await treasury.allocate_for_training(0.003, "capability_improvement")

        assert result.success
        assert result.allocation.category == AllocationCategory.TRAINING

    @pytest.mark.asyncio
    async def test_treasury_report(self):
        """Test generating treasury report."""
        treasury = BitcoinTreasury()

        await treasury.deposit(AssetType.USD, 100.0, "test")
        await treasury.allocate_for_compute(0.001)

        report = await treasury.get_treasury_report()

        assert report is not None
        assert report.total_value_usd > 0
        assert 'mode' in report.metadata

    def test_upgrade_to_testnet(self):
        """Test upgrading to testnet mode."""
        treasury = BitcoinTreasury()

        assert treasury.get_mode() == 'simulation'

        success = treasury.upgrade_to_testnet()

        assert success
        assert treasury.get_mode() == 'testnet'


# ===================== Economic Agency Tests =====================

class TestEconomicAgency:
    """Tests for EconomicAgency."""

    def test_initialization(self):
        """Test agency initializes correctly."""
        agency = EconomicAgency()

        assert agency.pricing is not None
        assert agency.treasury is not None
        catalog = agency.get_service_catalog()
        assert len(catalog) > 0

    @pytest.mark.asyncio
    async def test_price_service(self):
        """Test pricing a service."""
        agency = EconomicAgency()

        price = await agency.price_service('code_review')

        assert price is not None
        assert price.amount > 0

    @pytest.mark.asyncio
    async def test_create_request(self):
        """Test creating a service request."""
        agency = EconomicAgency()

        request = await agency.create_request(
            service_id='code_review',
            requester='user_1',
            parameters={'lines': 100}
        )

        assert request is not None
        assert request.service_id == 'code_review'
        assert request.status == ServiceStatus.PRICING
        assert request.price is not None

    @pytest.mark.asyncio
    async def test_accept_request(self):
        """Test accepting a request."""
        agency = EconomicAgency()

        request = await agency.create_request('code_review', 'user_1')
        success = await agency.accept_request(request.id)

        assert success

        updated = agency.get_request(request.id)
        assert updated.status == ServiceStatus.ACCEPTED

    @pytest.mark.asyncio
    async def test_execute_service(self):
        """Test executing a service."""
        agency = EconomicAgency()

        # Create and accept request
        request = await agency.create_request('code_review', 'user_1')
        await agency.accept_request(request.id)

        # Execute
        result = await agency.execute_service(request.id)

        assert result is not None
        assert result.success
        assert result.revenue > 0

    @pytest.mark.asyncio
    async def test_custom_service_handler(self):
        """Test custom service handler."""
        agency = EconomicAgency()

        async def custom_handler(request: ServiceRequest) -> dict:
            return {
                'status': 'custom_completed',
                'tokens_used': 500,
                'custom_data': 'test'
            }

        agency.register_service_handler('code_review', custom_handler)

        request = await agency.create_request('code_review', 'user_1')
        await agency.accept_request(request.id)
        result = await agency.execute_service(request.id)

        assert result.output['status'] == 'custom_completed'
        assert result.output['custom_data'] == 'test'

    @pytest.mark.asyncio
    async def test_revenue_report(self):
        """Test revenue reporting."""
        agency = EconomicAgency()

        # Execute a few services
        for _ in range(3):
            request = await agency.create_request('documentation', 'user_1')
            await agency.accept_request(request.id)
            await agency.execute_service(request.id)

        report = agency.get_revenue_report()

        assert report is not None
        assert report.requests_completed == 3
        assert report.total_revenue > 0

    @pytest.mark.asyncio
    async def test_manage_treasury(self):
        """Test treasury management through agency."""
        agency = EconomicAgency()

        report = await agency.manage_treasury()

        assert report is not None
        assert 'mode' in report.metadata


# ===================== Marketplace Tests =====================

class TestServiceMarketplace:
    """Tests for ServiceMarketplace."""

    def test_initialization(self):
        """Test marketplace initializes correctly."""
        marketplace = ServiceMarketplace()

        stats = marketplace.get_stats()
        assert stats['total_listings'] == 0

    def test_create_listing(self):
        """Test creating a listing."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')

        listing = marketplace.create_listing(service, price, tags=['python', 'review'])

        assert listing is not None
        assert listing.status == ListingStatus.DRAFT
        assert 'python' in listing.tags

    def test_publish_listing(self):
        """Test publishing a listing."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')
        listing = marketplace.create_listing(service, price)

        success = marketplace.publish_listing(listing.id)

        assert success

        updated = marketplace.get_listing(listing.id)
        assert updated.status == ListingStatus.ACTIVE

    def test_search_listings(self):
        """Test searching listings."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        # Create and publish multiple listings
        for service_id in ['code_review', 'bug_fixing', 'documentation']:
            service = engine.get_service(service_id)
            price = engine.calculate_price(service_id)
            listing = marketplace.create_listing(service, price, tags=[service_id])
            marketplace.publish_listing(listing.id)

        # Search by category
        results = marketplace.search_listings(category='development')
        assert len(results) >= 2

        # Search by text
        results = marketplace.search_listings(query='review')
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_initiate_purchase(self):
        """Test initiating a purchase."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')
        listing = marketplace.create_listing(service, price)
        marketplace.publish_listing(listing.id)

        payment = await marketplace.initiate_purchase(listing.id, 'buyer_1')

        assert payment is not None
        assert payment.status == PaymentStatus.PENDING
        assert payment.buyer == 'buyer_1'

    @pytest.mark.asyncio
    async def test_process_payment(self):
        """Test processing a payment."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')
        listing = marketplace.create_listing(service, price)
        marketplace.publish_listing(listing.id)

        payment = await marketplace.initiate_purchase(listing.id, 'buyer_1')
        success = await marketplace.process_payment(payment.id)

        assert success

        updated = marketplace.get_payment(payment.id)
        assert updated.status == PaymentStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_complete_purchase(self):
        """Test full purchase flow."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')
        listing = marketplace.create_listing(service, price)
        marketplace.publish_listing(listing.id)

        result = await marketplace.complete_purchase(listing.id, 'buyer_1')

        assert result['success']
        assert result['amount'] > 0
        assert result['fulfillment'] is not None

    def test_marketplace_stats(self):
        """Test marketplace statistics."""
        marketplace = ServiceMarketplace()
        engine = PricingEngine()

        # Create and complete some purchases
        service = engine.get_service('code_review')
        price = engine.calculate_price('code_review')
        listing = marketplace.create_listing(service, price)
        marketplace.publish_listing(listing.id)

        # Complete purchases synchronously for simplicity
        async def complete():
            await marketplace.complete_purchase(listing.id, 'buyer_1')
            await marketplace.complete_purchase(listing.id, 'buyer_2')

        asyncio.get_event_loop().run_until_complete(complete())

        stats = marketplace.get_marketplace_stats()

        assert stats.total_sales == 2
        assert stats.total_revenue > 0


# ===================== Self-Training Investment Tests =====================

class TestSelfTrainingInvestor:
    """Tests for SelfTrainingInvestor."""

    def test_initialization(self):
        """Test investor initializes correctly."""
        investor = SelfTrainingInvestor()

        stats = investor.get_stats()
        assert stats['total_goals'] == 0
        assert stats['total_investments'] == 0

    def test_create_goal(self):
        """Test creating a training goal."""
        investor = SelfTrainingInvestor()

        goal = investor.create_goal(
            name="Improve reasoning",
            description="Enhance reasoning capability",
            investment_type=InvestmentType.FINE_TUNING,
            target_capability='reasoning',
            current_level=0.7,
            target_level=0.9,
            estimated_cost=50.0,
            estimated_benefit=100.0
        )

        assert goal is not None
        assert goal.expected_roi == 1.0  # (100-50)/50 = 1.0

    def test_prioritize_goals(self):
        """Test goal prioritization."""
        investor = SelfTrainingInvestor()

        # Create goals with different ROI
        investor.create_goal(
            name="Low ROI",
            description="Low return goal",
            investment_type=InvestmentType.DATA,
            target_capability='test1',
            current_level=0.5,
            target_level=0.6,
            estimated_cost=100.0,
            estimated_benefit=110.0  # 10% ROI
        )

        investor.create_goal(
            name="High ROI",
            description="High return goal",
            investment_type=InvestmentType.COMPUTE,
            target_capability='test2',
            current_level=0.5,
            target_level=0.8,
            estimated_cost=50.0,
            estimated_benefit=150.0  # 200% ROI
        )

        prioritized = investor.prioritize_goals()

        assert len(prioritized) == 2
        assert prioritized[0].name == "High ROI"

    @pytest.mark.asyncio
    async def test_propose_investment(self):
        """Test proposing an investment."""
        investor = SelfTrainingInvestor()

        goal = investor.create_goal(
            name="Test",
            description="Test goal",
            investment_type=InvestmentType.CAPABILITY,
            target_capability='test',
            current_level=0.5,
            target_level=0.8,
            estimated_cost=20.0,
            estimated_benefit=50.0
        )

        investment = await investor.propose_investment(goal.id, 20.0)

        assert investment is not None
        assert investment.status == InvestmentStatus.PROPOSED
        assert investment.amount == 20.0

    @pytest.mark.asyncio
    async def test_approve_investment(self):
        """Test approving an investment."""
        investor = SelfTrainingInvestor()

        goal = investor.create_goal(
            name="Test",
            description="Test goal",
            investment_type=InvestmentType.CAPABILITY,
            target_capability='test',
            current_level=0.5,
            target_level=0.8,
            estimated_cost=20.0,
            estimated_benefit=50.0
        )

        investment = await investor.propose_investment(goal.id, 20.0)
        success = await investor.approve_investment(investment.id)

        assert success

        updated = investor.get_investment(investment.id)
        assert updated.status == InvestmentStatus.APPROVED

    @pytest.mark.asyncio
    async def test_execute_investment(self):
        """Test executing an investment."""
        investor = SelfTrainingInvestor()

        goal = investor.create_goal(
            name="Test",
            description="Test goal",
            investment_type=InvestmentType.CAPABILITY,
            target_capability='test',
            current_level=0.5,
            target_level=0.8,
            estimated_cost=20.0,
            estimated_benefit=50.0
        )

        investment = await investor.propose_investment(goal.id, 20.0)
        await investor.approve_investment(investment.id)
        result = await investor.execute_investment(investment.id)

        assert result['success']
        assert 'actual_roi' in result

        updated = investor.get_investment(investment.id)
        assert updated.status == InvestmentStatus.COMPLETED
        assert updated.actual_roi is not None

    @pytest.mark.asyncio
    async def test_custom_training_executor(self):
        """Test custom training executor."""
        investor = SelfTrainingInvestor()

        async def custom_executor(inv: Investment) -> dict:
            return {
                'status': 'custom_trained',
                'benefit': inv.amount * 1.5,
                'tokens_used': 1000
            }

        investor.set_training_executor(custom_executor)

        goal = investor.create_goal(
            name="Test",
            description="Test goal",
            investment_type=InvestmentType.FINE_TUNING,
            target_capability='test',
            current_level=0.5,
            target_level=0.8,
            estimated_cost=20.0,
            estimated_benefit=50.0
        )

        investment = await investor.propose_investment(goal.id, 20.0)
        await investor.approve_investment(investment.id)
        result = await investor.execute_investment(investment.id)

        assert result['result']['status'] == 'custom_trained'

    @pytest.mark.asyncio
    async def test_roi_report(self):
        """Test ROI reporting."""
        investor = SelfTrainingInvestor()

        # Execute a few investments
        for i in range(3):
            goal = investor.create_goal(
                name=f"Goal {i}",
                description=f"Test goal {i}",
                investment_type=InvestmentType.CAPABILITY,
                target_capability=f'test_{i}',
                current_level=0.5,
                target_level=0.8,
                estimated_cost=10.0,
                estimated_benefit=20.0
            )

            investment = await investor.propose_investment(goal.id, 10.0)
            await investor.approve_investment(investment.id)
            await investor.execute_investment(investment.id)

        report = investor.get_roi_report()

        assert report is not None
        assert report.total_invested == 30.0
        assert report.investments_completed == 3
        assert len(report.best_investments) > 0


# ===================== Integration Tests =====================

class TestPhase5Integration:
    """Integration tests for Phase 5 components."""

    @pytest.mark.asyncio
    async def test_full_economic_cycle(self):
        """Test full economic cycle: service → revenue → investment."""
        # Setup
        agency = EconomicAgency()
        investor = SelfTrainingInvestor()

        # Execute paid service
        request = await agency.create_request('code_review', 'user_1')
        await agency.accept_request(request.id)
        service_result = await agency.execute_service(request.id)

        assert service_result.success
        revenue = service_result.revenue

        # Create training goal
        goal = investor.create_goal(
            name="Improve from revenue",
            description="Invest service revenue into capability",
            investment_type=InvestmentType.CAPABILITY,
            target_capability='code_review',
            current_level=0.8,
            target_level=0.9,
            estimated_cost=revenue * 0.5,
            estimated_benefit=revenue * 1.5
        )

        # Invest portion of revenue
        investment = await investor.propose_investment(goal.id, revenue * 0.5)
        await investor.approve_investment(investment.id)
        invest_result = await investor.execute_investment(investment.id)

        assert invest_result['success']
        assert invest_result['actual_roi'] is not None

    @pytest.mark.asyncio
    async def test_marketplace_to_treasury_flow(self):
        """Test marketplace revenue flowing to treasury."""
        marketplace = ServiceMarketplace()
        treasury = BitcoinTreasury()
        engine = PricingEngine()

        # Create marketplace listing
        service = engine.get_service('architecture_design')
        price = engine.calculate_price('architecture_design')
        listing = marketplace.create_listing(service, price)
        marketplace.publish_listing(listing.id)

        # Complete purchase
        result = await marketplace.complete_purchase(listing.id, 'buyer_1')

        assert result['success']

        # Record revenue in treasury
        await treasury.deposit(
            AssetType.USD,
            result['amount'],
            f"marketplace_{result['payment_id']}"
        )

        # Verify treasury balance increased
        balance = await treasury.get_balance(AssetType.USD)
        assert balance.amount >= result['amount']

    @pytest.mark.asyncio
    async def test_investment_roi_tracking(self):
        """Test ROI tracking across multiple investments."""
        investor = SelfTrainingInvestor()

        # Create multiple investments with different outcomes
        investments = []
        for i in range(5):
            goal = investor.create_goal(
                name=f"Goal {i}",
                description=f"Test {i}",
                investment_type=InvestmentType.CAPABILITY,
                target_capability=f'cap_{i}',
                current_level=0.5 + i * 0.05,
                target_level=0.9,
                estimated_cost=10.0,
                estimated_benefit=10.0 + i * 5.0  # Increasing expected benefit
            )

            inv = await investor.propose_investment(goal.id, 10.0)
            await investor.approve_investment(inv.id)
            await investor.execute_investment(inv.id)
            investments.append(inv)

        # Get ROI report
        report = investor.get_roi_report()

        assert report.investments_completed == 5
        assert report.total_invested == 50.0
        assert len(report.best_investments) <= 5
        assert report.overall_roi is not None

    @pytest.mark.asyncio
    async def test_agency_revenue_allocation(self):
        """Test automatic revenue allocation."""
        agency = EconomicAgency()

        # Execute multiple services to generate revenue
        for _ in range(5):
            request = await agency.create_request('bug_fixing', 'user_1')
            await agency.accept_request(request.id)
            await agency.execute_service(request.id)

        # Allocate revenue
        allocations = await agency.allocate_revenue()

        # Should have allocations for different categories
        assert len(allocations) > 0

        # Verify treasury shows allocations
        report = await agency.manage_treasury()
        assert sum(report.allocation_summary.values()) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

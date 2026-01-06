"""
Tests for Phase 4: Scale & Safety.

Tests the scaling module (growth monitoring, resource scaling,
value stability, explosion handling) and verification module
(scale-invariant metrics, cross-scale verification, human anchoring).
"""

import pytest
import asyncio
from datetime import datetime, timezone

# Scaling module imports
from rsi.scaling import (
    # Growth Rate
    GrowthCategory,
    CapabilitySnapshot,
    GrowthMetrics,
    GrowthRateMonitor,
    # Resource Scaling
    ResourceType,
    ScalingStrategy,
    ResourceAllocation,
    ScalingDecision,
    ScalingResult,
    ResourceScaler,
    # Value Stability
    ValueCategory,
    ProtectionLevel,
    ProtectedValue,
    ValueDrift,
    ValueProtectionResult,
    ValueStabilityGuard,
    # Explosion Handler
    ExplosionPhase,
    HandlerAction,
    StabilityAssessment,
    ExplosionHandlerResult,
    CapabilityExplosionHandler,
)

# Verification module imports
from rsi.verification import (
    # Scale-Invariant Metrics
    MetricDomain,
    NormalizationType,
    MetricDefinition,
    MetricValue,
    ScaleInvariantReport,
    ScaleInvariantMetrics,
    # Cross-Scale Verification
    VerificationLevel,
    PropertyType,
    SafetyProperty,
    PropertyVerification,
    ScaleTransition,
    CrossScaleVerificationResult,
    CrossScaleVerifier,
    # Human Anchoring
    AnchorType,
    ValidationPriority,
    ValidationStatus,
    ValidationRequest,
    AnchorPoint,
    AnchoringResult,
    HumanAnchoringSystem,
)


# ===================== Growth Rate Monitor Tests =====================

class TestGrowthRateMonitor:
    """Tests for GrowthRateMonitor."""

    def test_initialization(self):
        """Test monitor initializes correctly."""
        monitor = GrowthRateMonitor()
        assert monitor is not None
        stats = monitor.get_stats()
        assert stats['measurements_taken'] == 0
        assert stats['explosions_detected'] == 0

    def test_record_snapshot(self):
        """Test recording capability snapshots."""
        monitor = GrowthRateMonitor()

        capabilities = {'reasoning': 0.7, 'learning': 0.8}
        snapshot = monitor.record_snapshot(capabilities)

        assert snapshot.aggregate_score == 0.75
        assert snapshot.capabilities == capabilities

    def test_calculate_growth_stable(self):
        """Test growth calculation with stable growth."""
        monitor = GrowthRateMonitor()

        # Record stable capabilities
        for i in range(5):
            capabilities = {'test': 0.5 + i * 0.01}  # 2% growth each
            monitor.record_snapshot(capabilities)

        metrics = monitor.calculate_growth_rate()
        assert metrics.category in [GrowthCategory.STABLE, GrowthCategory.MODERATE]
        assert metrics.stability_score > 0.5

    def test_calculate_growth_explosive(self):
        """Test growth calculation with explosive growth."""
        monitor = GrowthRateMonitor({'explosive_threshold': 1.0})

        # Record explosive growth
        monitor.record_snapshot({'test': 0.1})
        monitor.record_snapshot({'test': 0.5})  # 400% growth

        metrics = monitor.calculate_growth_rate()
        assert metrics.category in [GrowthCategory.EXPLOSIVE, GrowthCategory.CRITICAL]

    def test_detect_explosion(self):
        """Test explosion detection."""
        monitor = GrowthRateMonitor({'explosive_threshold': 1.0})

        monitor.record_snapshot({'test': 0.1})
        monitor.record_snapshot({'test': 0.5})

        assert monitor.detect_explosion()

    def test_time_to_double(self):
        """Test time to double calculation."""
        monitor = GrowthRateMonitor()

        # Consistent 10% growth
        for i in range(5):
            capabilities = {'test': 1.0 * (1.1 ** i)}
            monitor.record_snapshot(capabilities)

        metrics = monitor.calculate_growth_rate()
        if metrics.time_to_double:
            assert metrics.time_to_double > 0

    def test_reset(self):
        """Test monitor reset."""
        monitor = GrowthRateMonitor()
        monitor.record_snapshot({'test': 0.5})

        monitor.reset()

        stats = monitor.get_stats()
        assert stats['measurements_taken'] == 0
        assert stats['history_size'] == 0


# ===================== Resource Scaler Tests =====================

class TestResourceScaler:
    """Tests for ResourceScaler."""

    def test_initialization(self):
        """Test scaler initializes correctly."""
        scaler = ResourceScaler()
        assert scaler is not None

        allocations = scaler.get_all_allocations()
        assert len(allocations) > 0

    def test_default_allocations(self):
        """Test default resource allocations."""
        scaler = ResourceScaler()

        compute = scaler.get_allocation(ResourceType.COMPUTE)
        assert compute is not None
        assert compute.current_amount == 100.0
        assert compute.unit == "vCPU-hours"

    @pytest.mark.asyncio
    async def test_scale_for_stable_growth(self):
        """Test scaling for stable growth."""
        scaler = ResourceScaler()

        metrics = GrowthMetrics(
            current_rate=0.05,
            acceleration=0.0,
            category=GrowthCategory.STABLE,
            time_to_double=None,
            projected_capability=1.0,
            stability_score=1.0
        )

        result = await scaler.scale_for_growth(metrics)
        # Stable growth with low utilization triggers scale-down decisions
        # which still count as successful operations
        assert result is not None
        # Stable growth shouldn't trigger scale-up operations
        scale_ups = [d for d in result.decisions if d.action == 'scale_up']
        assert len(scale_ups) == 0

    @pytest.mark.asyncio
    async def test_scale_for_rapid_growth(self):
        """Test scaling for rapid growth."""
        scaler = ResourceScaler()

        # Set high utilization
        scaler.update_utilization(ResourceType.COMPUTE, 0.85)

        metrics = GrowthMetrics(
            current_rate=0.8,
            acceleration=0.1,
            category=GrowthCategory.RAPID,
            time_to_double=1.0,
            projected_capability=2.0,
            stability_score=0.8
        )

        result = await scaler.scale_for_growth(metrics)
        # Should trigger scaling due to high utilization + rapid growth
        assert len(result.decisions) >= 1

    @pytest.mark.asyncio
    async def test_scale_for_critical_growth(self):
        """Test scaling for critical growth."""
        scaler = ResourceScaler()

        # Set medium utilization
        scaler.update_utilization(ResourceType.COMPUTE, 0.6)

        metrics = GrowthMetrics(
            current_rate=15.0,  # 1500% growth
            acceleration=5.0,
            category=GrowthCategory.CRITICAL,
            time_to_double=0.1,
            projected_capability=10.0,
            stability_score=0.3
        )

        result = await scaler.scale_for_growth(metrics)
        # Critical growth should trigger aggressive scaling
        assert any(d.action == 'scale_up' for d in result.decisions)

    def test_update_utilization(self):
        """Test utilization updates."""
        scaler = ResourceScaler()

        scaler.update_utilization(ResourceType.MEMORY, 0.75)

        alloc = scaler.get_allocation(ResourceType.MEMORY)
        assert alloc.utilization == 0.75

    def test_utilization_bounds(self):
        """Test utilization stays within bounds."""
        scaler = ResourceScaler()

        scaler.update_utilization(ResourceType.COMPUTE, 1.5)  # Over 1.0
        assert scaler.get_allocation(ResourceType.COMPUTE).utilization == 1.0

        scaler.update_utilization(ResourceType.COMPUTE, -0.5)  # Under 0.0
        assert scaler.get_allocation(ResourceType.COMPUTE).utilization == 0.0


# ===================== Value Stability Guard Tests =====================

class TestValueStabilityGuard:
    """Tests for ValueStabilityGuard."""

    def test_initialization(self):
        """Test guard initializes with core values."""
        guard = ValueStabilityGuard()

        values = guard.get_all_values()
        assert len(values) >= 4  # Core values

    def test_core_values_exist(self):
        """Test core values are registered."""
        guard = ValueStabilityGuard()

        emergence = guard.get_value('emergence_integrity')
        assert emergence is not None
        assert emergence.protection_level == ProtectionLevel.IMMUTABLE

        provenance = guard.get_value('provenance_tracking')
        assert provenance is not None
        assert provenance.protection_level == ProtectionLevel.IMMUTABLE

    def test_register_custom_value(self):
        """Test registering custom protected values."""
        guard = ValueStabilityGuard()

        custom = ProtectedValue(
            id='custom_value',
            name='Custom Value',
            description='A custom test value',
            category=ValueCategory.OPERATIONAL,
            protection_level=ProtectionLevel.MONITORED,
            current_state=0.8,
            baseline_state=0.8,
            drift_tolerance=0.2
        )

        guard.register_value(custom)

        retrieved = guard.get_value('custom_value')
        assert retrieved is not None
        assert retrieved.name == 'Custom Value'

    @pytest.mark.asyncio
    async def test_protect_values_stable(self):
        """Test value protection with stable values."""
        guard = ValueStabilityGuard()

        result = await guard.protect_values(growth_rate=0.1)

        assert result.values_checked > 0
        assert result.overall_stability >= 0.9  # Core values should be stable

    @pytest.mark.asyncio
    async def test_protect_values_detects_drift(self):
        """Test value protection detects drift."""
        guard = ValueStabilityGuard()

        # Modify a non-immutable value's state
        cooperation = guard.get_value('human_cooperation')
        if cooperation:
            cooperation.current_state = 0.5  # Drift from 1.0 baseline

        result = await guard.protect_values(growth_rate=0.1)

        # Should detect some drift
        assert result.values_drifting > 0 or result.values_violated > 0

    @pytest.mark.asyncio
    async def test_immutable_value_correction(self):
        """Test immutable values are auto-corrected."""
        guard = ValueStabilityGuard()

        # Try to modify immutable value
        emergence = guard.get_value('emergence_integrity')
        emergence.current_state = False  # Try to change it

        result = await guard.protect_values(growth_rate=0.5)

        # Immutable value should be restored
        assert emergence.current_state == True  # Restored to baseline

    def test_update_value_state_blocked(self):
        """Test updating immutable values is blocked."""
        guard = ValueStabilityGuard()

        # Try to update immutable value through API
        success = guard.update_value_state('emergence_integrity', False)

        assert not success  # Should be blocked

        # Value should remain unchanged
        value = guard.get_value('emergence_integrity')
        assert value.current_state == True


# ===================== Capability Explosion Handler Tests =====================

class TestCapabilityExplosionHandler:
    """Tests for CapabilityExplosionHandler."""

    def test_initialization(self):
        """Test handler initializes correctly."""
        handler = CapabilityExplosionHandler()

        assert handler.get_current_phase() == ExplosionPhase.NORMAL
        assert not handler.is_paused()
        assert not handler.is_emergency_stopped()

    @pytest.mark.asyncio
    async def test_monitor_growth_rate(self):
        """Test growth rate monitoring."""
        handler = CapabilityExplosionHandler()

        handler.record_capabilities({'test': 0.5})
        handler.record_capabilities({'test': 0.6})

        metrics = await handler.monitor_growth_rate()
        assert metrics is not None

    @pytest.mark.asyncio
    async def test_check_stability(self):
        """Test stability checking."""
        handler = CapabilityExplosionHandler()

        handler.record_capabilities({'test': 0.5})
        handler.record_capabilities({'test': 0.55})

        stability = await handler.check_stability()

        assert stability is not None
        assert 0.0 <= stability.risk_level <= 1.0

    @pytest.mark.asyncio
    async def test_handle_explosion_normal(self):
        """Test handling normal growth."""
        handler = CapabilityExplosionHandler()

        result = await handler.handle_explosion({'test': 0.5})
        result = await handler.handle_explosion({'test': 0.52})  # 4% growth

        assert result.phase == ExplosionPhase.NORMAL
        assert HandlerAction.MONITOR in result.actions_taken

    @pytest.mark.asyncio
    async def test_handle_explosion_rapid(self):
        """Test handling rapid growth."""
        handler = CapabilityExplosionHandler()

        result = await handler.handle_explosion({'test': 0.5})
        result = await handler.handle_explosion({'test': 1.0})  # 100% growth

        # Should escalate phase
        assert result.phase in [ExplosionPhase.RAPID, ExplosionPhase.EXPLOSIVE, ExplosionPhase.ELEVATED]

    @pytest.mark.asyncio
    async def test_handle_explosion_critical(self):
        """Test handling critical growth."""
        handler = CapabilityExplosionHandler()

        result = await handler.handle_explosion({'test': 0.1})
        result = await handler.handle_explosion({'test': 5.0})  # 4900% growth

        # Should be in critical or explosive phase
        assert result.phase in [ExplosionPhase.CRITICAL, ExplosionPhase.EXPLOSIVE]

    def test_resume_improvements(self):
        """Test resuming paused improvements."""
        handler = CapabilityExplosionHandler()

        # Manually pause
        handler._improvements_paused = True

        success = handler.resume_improvements()

        assert success
        assert not handler.is_paused()

    def test_resume_blocked_during_emergency(self):
        """Test resume blocked during emergency stop."""
        handler = CapabilityExplosionHandler()

        handler._emergency_stop = True
        handler._improvements_paused = True

        success = handler.resume_improvements()

        assert not success
        assert handler.is_paused()

    def test_clear_emergency_stop(self):
        """Test clearing emergency stop."""
        handler = CapabilityExplosionHandler()

        handler._emergency_stop = True
        handler._improvements_paused = True

        success = handler.clear_emergency_stop()

        assert success
        assert not handler.is_emergency_stopped()
        assert not handler.is_paused()


# ===================== Scale-Invariant Metrics Tests =====================

class TestScaleInvariantMetrics:
    """Tests for ScaleInvariantMetrics."""

    def test_initialization(self):
        """Test metrics system initializes correctly."""
        metrics = ScaleInvariantMetrics()

        all_metrics = metrics.get_all_metrics()
        assert len(all_metrics) >= 10  # Core metrics

    def test_core_metrics_registered(self):
        """Test core metrics are registered."""
        metrics = ScaleInvariantMetrics()

        emergence = metrics.get_metric('emergence_ratio')
        assert emergence is not None
        assert emergence.domain == MetricDomain.EMERGENCE

        alignment = metrics.get_metric('value_stability')
        assert alignment is not None
        assert alignment.domain == MetricDomain.ALIGNMENT

    def test_compute_metrics(self):
        """Test metric computation."""
        metrics = ScaleInvariantMetrics()

        data = {
            'emergent_behaviors': 8,
            'total_behaviors': 10,
            'successful_mods': 5,
            'total_mods': 6,
            'fulfilled_desires': 4,
            'total_desires': 5,
            'contradictions': 1,
            'total_beliefs': 20,
            'aligned_actions': 18,
            'total_actions': 20,
            'stable_values': 9,
            'total_values': 10,
            'cooperation_score': 0.8,
            'traced_mods': 6,
            'growth_rate': 0.2,
            'improvement': 5,
            'experiences': 100,
            'output': 80,
            'resources_used': 100,
            'effective_compute': 70,
            'total_compute': 100,
            'capability_level': 1.5
        }

        report = metrics.compute_metrics(data)

        assert report is not None
        assert len(report.metrics) > 0
        assert 0.0 <= report.overall_score <= 1.0
        assert report.capability_level == 1.5

    def test_domain_scores(self):
        """Test domain score calculation."""
        metrics = ScaleInvariantMetrics()

        data = {
            'emergent_behaviors': 10,
            'total_behaviors': 10,
            'total_mods': 1,
            'successful_mods': 1,
            'total_desires': 1,
            'fulfilled_desires': 1,
        }

        report = metrics.compute_metrics(data)

        assert MetricDomain.EMERGENCE.value in report.domain_scores

    def test_metric_normalization_ratio(self):
        """Test ratio normalization."""
        metric = MetricDefinition(
            id='test',
            name='Test',
            description='Test metric',
            domain=MetricDomain.CAPABILITY,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('value', 0),
            min_value=0.0,
            max_value=1.0
        )

        assert metric.compute({'value': 0.5}) == 0.5
        assert metric.compute({'value': 0.0}) == 0.0
        assert metric.compute({'value': 1.0}) == 1.0

    def test_metric_normalization_log(self):
        """Test logarithmic normalization."""
        metric = MetricDefinition(
            id='test',
            name='Test',
            description='Test metric',
            domain=MetricDomain.CAPABILITY,
            normalization=NormalizationType.LOG_SCALE,
            compute_fn=lambda d: d.get('value', 0),
            min_value=0.0,
            max_value=100.0
        )

        # Log scale should compress large values
        result = metric.compute({'value': 50.0})
        assert 0.0 < result < 1.0

    def test_get_trend(self):
        """Test trend calculation."""
        metrics = ScaleInvariantMetrics()

        # Compute metrics multiple times with increasing values
        for i in range(5):
            data = {
                'emergent_behaviors': i + 5,
                'total_behaviors': 10,
                'total_mods': 1,
                'successful_mods': 1,
            }
            metrics.compute_metrics(data)

        trend = metrics.get_trend('emergence_ratio', window=5)

        if trend is not None:
            assert trend > 0  # Improving trend


# ===================== Cross-Scale Verifier Tests =====================

class TestCrossScaleVerifier:
    """Tests for CrossScaleVerifier."""

    def test_initialization(self):
        """Test verifier initializes correctly."""
        verifier = CrossScaleVerifier()

        properties = verifier.get_all_properties()
        assert len(properties) >= 9  # Core properties

    def test_core_properties_registered(self):
        """Test core properties are registered."""
        verifier = CrossScaleVerifier()

        provenance = verifier.get_property('provenance_invariant')
        assert provenance is not None
        assert provenance.property_type == PropertyType.INVARIANT

        capability = verifier.get_property('capability_monotonic')
        assert capability is not None
        assert capability.property_type == PropertyType.MONOTONIC

    def test_verify_transition_safe(self):
        """Test verification of safe transition."""
        verifier = CrossScaleVerifier()

        before = {
            'capability_level': 1.0,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.8,
            'capability_score': 0.7,
            'safety_score': 0.9,
            'alignment_score': 0.85,
            'resource_utilization': 0.5,
            'growth_rate': 0.1,
            'value_drift': 0.05,
        }

        after = {
            'capability_level': 1.2,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.85,
            'capability_score': 0.75,
            'safety_score': 0.92,
            'alignment_score': 0.88,
            'resource_utilization': 0.55,
            'growth_rate': 0.2,
            'value_drift': 0.03,
        }

        result = verifier.verify_transition(before, after)

        assert result.overall_safe
        assert result.properties_violated == 0

    def test_verify_transition_unsafe(self):
        """Test verification of unsafe transition."""
        verifier = CrossScaleVerifier()

        before = {
            'capability_level': 1.0,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.8,
            'capability_score': 0.7,
            'safety_score': 0.9,
            'alignment_score': 0.85,
        }

        after = {
            'capability_level': 2.0,
            'provenance_coverage': 0.5,  # VIOLATION: missing provenance
            'protected_violations': 2,    # VIOLATION: protected files modified
            'emergent_ratio': 0.3,        # VIOLATION: below threshold
            'capability_score': 0.8,
            'safety_score': 0.5,          # VIOLATION: safety decreased
            'alignment_score': 0.4,       # VIOLATION: alignment decreased
        }

        result = verifier.verify_transition(before, after)

        assert not result.overall_safe
        assert result.properties_violated > 0

    def test_verification_level_scaling(self):
        """Test verification level scales with transition size."""
        verifier = CrossScaleVerifier()

        before = {'capability_level': 1.0}

        # Small transition
        after_small = {'capability_level': 1.3}
        result_small = verifier.verify_transition(before, after_small)

        # Large transition
        after_large = {'capability_level': 5.0}
        result_large = verifier.verify_transition(before, after_large)

        # Larger transitions should trigger more rigorous verification
        assert result_large.verification_level.value >= result_small.verification_level.value

    def test_transition_classification(self):
        """Test transition type classification."""
        verifier = CrossScaleVerifier()

        # Gradual
        result = verifier.verify_transition(
            {'capability_level': 1.0},
            {'capability_level': 1.2},
            scale_factor=1.2
        )
        assert result.transition.transition_type == 'gradual'

        # Rapid
        result = verifier.verify_transition(
            {'capability_level': 1.0},
            {'capability_level': 2.0},
            scale_factor=2.0
        )
        assert result.transition.transition_type == 'rapid'

        # Explosive
        result = verifier.verify_transition(
            {'capability_level': 1.0},
            {'capability_level': 5.0},
            scale_factor=5.0
        )
        assert result.transition.transition_type == 'explosive'


# ===================== Human Anchoring Tests =====================

class TestHumanAnchoringSystem:
    """Tests for HumanAnchoringSystem."""

    def test_initialization(self):
        """Test system initializes correctly."""
        system = HumanAnchoringSystem()

        stats = system.get_stats()
        assert stats['requests_created'] == 0
        assert stats['anchor_count'] == 0

    @pytest.mark.asyncio
    async def test_request_validation(self):
        """Test creating validation request."""
        system = HumanAnchoringSystem()

        request = await system.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description='Validate capability improvement',
            claim={'reasoning': 0.85},
            priority=ValidationPriority.MEDIUM
        )

        assert request.id is not None
        assert request.status == ValidationStatus.PENDING
        assert request.priority == ValidationPriority.MEDIUM

    @pytest.mark.asyncio
    async def test_process_validation_approved(self):
        """Test processing approved validation."""
        system = HumanAnchoringSystem()

        request = await system.request_validation(
            anchor_type=AnchorType.VALUE,
            description='Validate value alignment',
            claim=0.9
        )

        result = await system.process_validation(request.id, {
            'approved': True,
            'confidence': 0.95,
            'notes': 'Validated correctly',
            'validator_id': 'human_1'
        })

        assert result.status == ValidationStatus.APPROVED
        assert result.anchor is not None
        assert result.anchor.confidence == 0.95

    @pytest.mark.asyncio
    async def test_process_validation_rejected(self):
        """Test processing rejected validation."""
        system = HumanAnchoringSystem()

        request = await system.request_validation(
            anchor_type=AnchorType.SAFETY,
            description='Validate safety claim',
            claim='safe'
        )

        result = await system.process_validation(request.id, {
            'approved': False,
            'notes': 'Claim not substantiated',
            'validator_id': 'human_1'
        })

        assert result.status == ValidationStatus.REJECTED
        assert result.anchor is None

    @pytest.mark.asyncio
    async def test_process_validation_modified(self):
        """Test processing modified validation."""
        system = HumanAnchoringSystem()

        request = await system.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description='Validate capability score',
            claim=0.9
        )

        result = await system.process_validation(request.id, {
            'approved': True,
            'modified_value': 0.75,  # Human corrects the value
            'confidence': 0.9,
            'notes': 'Adjusted to correct value',
            'validator_id': 'human_1'
        })

        assert result.status == ValidationStatus.MODIFIED
        assert result.anchor.value == 0.75

    @pytest.mark.asyncio
    async def test_drift_detection(self):
        """Test drift detection between anchors."""
        system = HumanAnchoringSystem({'drift_threshold': 0.1})

        # Create first anchor
        req1 = await system.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description='First capability measurement',
            claim=0.7
        )
        await system.process_validation(req1.id, {
            'approved': True,
            'confidence': 0.9,
            'validator_id': 'human_1'
        })

        # Create second anchor with significant drift
        req2 = await system.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description='Second capability measurement',
            claim=0.5  # 28% drift from 0.7
        )
        result = await system.process_validation(req2.id, {
            'approved': True,
            'confidence': 0.9,
            'validator_id': 'human_1'
        })

        assert result.drift_detected
        assert result.drift_magnitude > 0.1

    def test_get_pending_requests(self):
        """Test getting pending requests."""
        system = HumanAnchoringSystem()

        # Create multiple requests synchronously by running in event loop
        async def create_requests():
            await system.request_validation(
                anchor_type=AnchorType.CAPABILITY,
                description='Request 1',
                claim=0.5,
                priority=ValidationPriority.LOW
            )
            await system.request_validation(
                anchor_type=AnchorType.SAFETY,
                description='Request 2',
                claim=0.8,
                priority=ValidationPriority.HIGH
            )

        asyncio.get_event_loop().run_until_complete(create_requests())

        pending = system.get_pending_requests()
        assert len(pending) == 2

        # Filter by priority
        high_priority = system.get_pending_requests(priority=ValidationPriority.HIGH)
        assert len(high_priority) == 1

    @pytest.mark.asyncio
    async def test_handler_registration(self):
        """Test validation handler registration."""
        from typing import Dict as HandlerDict
        system = HumanAnchoringSystem()

        async def auto_approve_handler(request: ValidationRequest) -> HandlerDict:
            if request.priority == ValidationPriority.LOW:
                return {
                    'approved': True,
                    'confidence': 0.6,
                    'validator_id': 'auto'
                }
            return None

        system.register_handler(auto_approve_handler)

        request = await system.request_validation(
            anchor_type=AnchorType.BEHAVIOR,
            description='Low priority request',
            claim='behavior_ok',
            priority=ValidationPriority.LOW
        )

        results = await system.auto_process_pending()

        assert len(results) == 1
        assert results[0].status == ValidationStatus.APPROVED


# ===================== Integration Tests =====================

class TestPhase4Integration:
    """Integration tests for Phase 4 components."""

    @pytest.mark.asyncio
    async def test_explosion_handler_with_verification(self):
        """Test explosion handler with cross-scale verification."""
        handler = CapabilityExplosionHandler()
        verifier = CrossScaleVerifier()

        # Record initial capabilities
        initial_caps = {'reasoning': 0.5, 'learning': 0.6}
        result1 = await handler.handle_explosion(initial_caps)

        before_state = {
            'capability_level': 1.0,
            'capability_score': 0.55,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.8,
            'safety_score': 0.9,
            'alignment_score': 0.85,
        }

        # Record improved capabilities
        improved_caps = {'reasoning': 0.8, 'learning': 0.85}
        result2 = await handler.handle_explosion(improved_caps)

        after_state = {
            'capability_level': 1.5,
            'capability_score': 0.825,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.85,
            'safety_score': 0.92,
            'alignment_score': 0.88,
        }

        # Verify the transition
        verification = verifier.verify_transition(before_state, after_state)

        assert verification.overall_safe
        assert result2.phase in [ExplosionPhase.NORMAL, ExplosionPhase.ELEVATED]

    @pytest.mark.asyncio
    async def test_metrics_with_anchoring(self):
        """Test metrics computation with human anchoring."""
        metrics = ScaleInvariantMetrics()
        anchoring = HumanAnchoringSystem()

        # Compute initial metrics
        data = {
            'emergent_behaviors': 8,
            'total_behaviors': 10,
            'total_mods': 5,
            'successful_mods': 4,
            'total_desires': 10,
            'fulfilled_desires': 7,
            'capability_level': 1.0
        }

        report = metrics.compute_metrics(data)

        # Request human validation of overall score
        request = await anchoring.request_validation(
            anchor_type=AnchorType.CAPABILITY,
            description='Validate overall capability score',
            claim=report.overall_score,
            evidence=[f"Domain scores: {report.domain_scores}"],
            priority=ValidationPriority.MEDIUM
        )

        # Simulate human approval
        result = await anchoring.process_validation(request.id, {
            'approved': True,
            'confidence': 0.9,
            'notes': 'Metrics look reasonable',
            'validator_id': 'human_validator'
        })

        assert result.anchor is not None
        assert result.anchor.anchor_type == AnchorType.CAPABILITY

    @pytest.mark.asyncio
    async def test_full_scaling_pipeline(self):
        """Test full scaling pipeline."""
        handler = CapabilityExplosionHandler()
        metrics = ScaleInvariantMetrics()
        verifier = CrossScaleVerifier()

        # Phase 1: Record baseline
        baseline = {'reasoning': 0.5, 'coding': 0.4, 'learning': 0.6}
        await handler.handle_explosion(baseline)

        baseline_data = {
            'emergent_behaviors': 5,
            'total_behaviors': 10,
            'capability_level': 1.0,
            'total_mods': 1,
            'successful_mods': 1,
        }
        baseline_report = metrics.compute_metrics(baseline_data)

        # Phase 2: Simulate improvement
        improved = {'reasoning': 0.7, 'coding': 0.65, 'learning': 0.8}
        result = await handler.handle_explosion(improved)

        improved_data = {
            'emergent_behaviors': 8,
            'total_behaviors': 10,
            'capability_level': 1.4,
            'total_mods': 2,
            'successful_mods': 2,
        }
        improved_report = metrics.compute_metrics(improved_data)

        # Phase 3: Verify safety
        before_state = {
            'capability_level': 1.0,
            'capability_score': baseline_report.overall_score,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.5,
            'safety_score': 0.9,
            'alignment_score': 0.85,
        }

        after_state = {
            'capability_level': 1.4,
            'capability_score': improved_report.overall_score,
            'provenance_coverage': 1.0,
            'protected_violations': 0,
            'emergent_ratio': 0.8,
            'safety_score': 0.92,
            'alignment_score': 0.88,
        }

        verification = verifier.verify_transition(before_state, after_state)

        # All should pass
        assert verification.overall_safe
        assert result.phase in [ExplosionPhase.NORMAL, ExplosionPhase.ELEVATED, ExplosionPhase.RAPID]
        assert improved_report.overall_score >= baseline_report.overall_score


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

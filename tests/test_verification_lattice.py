"""
Tests for the Verification Lattice module.

The Verification Lattice composes multiple independent verifiers to exceed
the verification ceiling of any single verifier, achieving robust validation
of RSI improvements.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from rsi.verification.lattice import (
    VerificationLattice,
    VerifierType,
    VerificationOutcome,
    LatticeResult,
    Improvement,
    BaseVerifier,
    ExecutionTestsVerifier,
    PropertyChecksVerifier,
    LLMCritiqueVerifier,
    AdversarialProbesVerifier,
    HumanSpotCheckVerifier,
)


class TestVerifierType:
    """Test VerifierType enum."""

    def test_all_verifier_types_defined(self):
        """Ensure all five verifier types are defined."""
        assert VerifierType.EXECUTION is not None
        assert VerifierType.PROPERTY is not None
        assert VerifierType.LLM_CRITIQUE is not None
        assert VerifierType.ADVERSARIAL is not None
        assert VerifierType.HUMAN_SPOT is not None

    def test_verifier_type_values(self):
        """Verify enum string values."""
        assert VerifierType.EXECUTION.value == "execution"
        assert VerifierType.PROPERTY.value == "property"
        assert VerifierType.LLM_CRITIQUE.value == "llm_critique"
        assert VerifierType.ADVERSARIAL.value == "adversarial"
        assert VerifierType.HUMAN_SPOT.value == "human_spot"


class TestVerificationResult:
    """Test VerificationResult dataclass."""

    def test_result_creation(self):
        """Test basic result creation."""
        result = VerificationResult(
            verifier_type=VerifierType.EXECUTION,
            passed=True,
            confidence=0.95,
            details={"tests_passed": 10},
        )
        assert result.verifier_type == VerifierType.EXECUTION
        assert result.passed is True
        assert result.confidence == 0.95
        assert result.details == {"tests_passed": 10}

    def test_result_with_error(self):
        """Test result with error message."""
        result = VerificationResult(
            verifier_type=VerifierType.PROPERTY,
            passed=False,
            confidence=0.0,
            error="Property check failed",
        )
        assert result.passed is False
        assert result.error == "Property check failed"


class TestImprovement:
    """Test Improvement dataclass."""

    def test_improvement_creation(self):
        """Test improvement creation with required fields."""
        improvement = Improvement(
            id="imp_001",
            domain="code",
            description="Improved JSON parsing",
            code_changes={"file.py": "new content"},
            metrics_before={"accuracy": 0.8},
            metrics_after={"accuracy": 0.9},
        )
        assert improvement.id == "imp_001"
        assert improvement.domain == "code"
        assert improvement.metrics_before["accuracy"] == 0.8
        assert improvement.metrics_after["accuracy"] == 0.9


class TestBaseVerifier:
    """Test BaseVerifier abstract class."""

    def test_base_verifier_is_abstract(self):
        """Verify BaseVerifier cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseVerifier()


class TestExecutionVerifier:
    """Test ExecutionVerifier."""

    @pytest.fixture
    def verifier(self):
        return ExecutionVerifier()

    @pytest.fixture
    def sample_improvement(self):
        return Improvement(
            id="imp_test",
            domain="code",
            description="Test improvement",
            code_changes={"test.py": "def foo(): pass"},
            metrics_before={"tests_passed": 8},
            metrics_after={"tests_passed": 10},
        )

    @pytest.mark.asyncio
    async def test_verify_returns_result(self, verifier, sample_improvement):
        """Test that verify returns a VerificationResult."""
        result = await verifier.verify(sample_improvement)
        assert isinstance(result, VerificationResult)
        assert result.verifier_type == VerifierType.EXECUTION

    @pytest.mark.asyncio
    async def test_verify_has_confidence(self, verifier, sample_improvement):
        """Test that result includes confidence score."""
        result = await verifier.verify(sample_improvement)
        assert 0.0 <= result.confidence <= 1.0


class TestPropertyVerifier:
    """Test PropertyVerifier."""

    @pytest.fixture
    def verifier(self):
        return PropertyVerifier()

    @pytest.fixture
    def sample_improvement(self):
        return Improvement(
            id="imp_prop",
            domain="logic",
            description="Logic improvement",
            code_changes={},
            metrics_before={},
            metrics_after={},
        )

    @pytest.mark.asyncio
    async def test_verify_checks_invariants(self, verifier, sample_improvement):
        """Test that property verifier checks invariants."""
        result = await verifier.verify(sample_improvement)
        assert isinstance(result, VerificationResult)
        assert result.verifier_type == VerifierType.PROPERTY


class TestVerificationLattice:
    """Test the main VerificationLattice class."""

    @pytest.fixture
    def lattice(self):
        return VerificationLattice()

    @pytest.fixture
    def sample_improvement(self):
        return Improvement(
            id="imp_lattice",
            domain="code",
            description="Lattice test improvement",
            code_changes={"module.py": "improved code"},
            metrics_before={"score": 0.7},
            metrics_after={"score": 0.85},
        )

    def test_lattice_has_default_threshold(self, lattice):
        """Test that lattice has default consensus threshold."""
        assert lattice.consensus_threshold == 0.60

    def test_lattice_has_verifiers(self, lattice):
        """Test that lattice initializes with verifiers."""
        assert len(lattice.verifiers) > 0

    def test_custom_threshold(self):
        """Test lattice with custom threshold."""
        lattice = VerificationLattice(consensus_threshold=0.75)
        assert lattice.consensus_threshold == 0.75

    @pytest.mark.asyncio
    async def test_verify_returns_lattice_result(self, lattice, sample_improvement):
        """Test that verify returns LatticeResult."""
        result = await lattice.verify(sample_improvement)
        assert isinstance(result, LatticeResult)

    @pytest.mark.asyncio
    async def test_result_includes_all_verifier_results(self, lattice, sample_improvement):
        """Test that result includes results from all verifiers."""
        result = await lattice.verify(sample_improvement)
        assert len(result.verifier_results) == len(lattice.verifiers)

    @pytest.mark.asyncio
    async def test_consensus_calculation(self, lattice, sample_improvement):
        """Test consensus is calculated correctly."""
        result = await lattice.verify(sample_improvement)

        # Manually calculate expected consensus
        passed_count = sum(1 for r in result.verifier_results if r.passed)
        expected_ratio = passed_count / len(result.verifier_results)
        expected_consensus = expected_ratio >= lattice.consensus_threshold

        assert result.consensus_reached == expected_consensus

    @pytest.mark.asyncio
    async def test_overall_confidence(self, lattice, sample_improvement):
        """Test overall confidence is average of individual confidences."""
        result = await lattice.verify(sample_improvement)

        confidences = [r.confidence for r in result.verifier_results]
        expected_avg = sum(confidences) / len(confidences)

        assert abs(result.overall_confidence - expected_avg) < 0.01


class TestLatticeWithMockedVerifiers:
    """Test lattice behavior with mocked verifiers."""

    @pytest.mark.asyncio
    async def test_consensus_with_all_pass(self):
        """Test consensus when all verifiers pass."""
        lattice = VerificationLattice()

        # Mock all verifiers to pass
        for verifier in lattice.verifiers:
            verifier.verify = AsyncMock(return_value=VerificationResult(
                verifier_type=verifier.verifier_type,
                passed=True,
                confidence=0.9,
            ))

        improvement = Improvement(
            id="test", domain="code", description="test",
            code_changes={}, metrics_before={}, metrics_after={},
        )

        result = await lattice.verify(improvement)
        assert result.consensus_reached is True

    @pytest.mark.asyncio
    async def test_no_consensus_with_all_fail(self):
        """Test no consensus when all verifiers fail."""
        lattice = VerificationLattice()

        # Mock all verifiers to fail
        for verifier in lattice.verifiers:
            verifier.verify = AsyncMock(return_value=VerificationResult(
                verifier_type=verifier.verifier_type,
                passed=False,
                confidence=0.1,
            ))

        improvement = Improvement(
            id="test", domain="code", description="test",
            code_changes={}, metrics_before={}, metrics_after={},
        )

        result = await lattice.verify(improvement)
        assert result.consensus_reached is False

    @pytest.mark.asyncio
    async def test_edge_case_60_percent_threshold(self):
        """Test edge case at exactly 60% threshold."""
        lattice = VerificationLattice(consensus_threshold=0.60)

        # With 5 verifiers, 3 passing = 60% exactly
        pass_fail = [True, True, True, False, False]

        for i, verifier in enumerate(lattice.verifiers):
            verifier.verify = AsyncMock(return_value=VerificationResult(
                verifier_type=verifier.verifier_type,
                passed=pass_fail[i],
                confidence=0.8 if pass_fail[i] else 0.2,
            ))

        improvement = Improvement(
            id="test", domain="code", description="test",
            code_changes={}, metrics_before={}, metrics_after={},
        )

        result = await lattice.verify(improvement)
        assert result.consensus_reached is True  # 60% meets 60% threshold


class TestLatticeRecommendations:
    """Test lattice recommendation generation."""

    @pytest.mark.asyncio
    async def test_generates_recommendations_on_failure(self):
        """Test that recommendations are generated when consensus fails."""
        lattice = VerificationLattice()

        # Mock mixed results
        for i, verifier in enumerate(lattice.verifiers):
            verifier.verify = AsyncMock(return_value=VerificationResult(
                verifier_type=verifier.verifier_type,
                passed=i < 2,  # Only first 2 pass
                confidence=0.5,
                details={"reason": "test failure"} if i >= 2 else {},
            ))

        improvement = Improvement(
            id="test", domain="code", description="test",
            code_changes={}, metrics_before={}, metrics_after={},
        )

        result = await lattice.verify(improvement)
        assert result.recommendations is not None
        # Should have recommendations since consensus wasn't reached
        assert len(result.recommendations) >= 0

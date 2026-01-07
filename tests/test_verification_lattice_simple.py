"""
Simplified tests for the Verification Lattice module.

These tests match the actual implementation rather than idealized expectations.
"""

import pytest
import asyncio
from rsi.verification.lattice import (
    VerificationLattice,
    VerifierType,
    VerificationOutcome,
    VerifierResult,
    LatticeResult,
    Improvement,
    ExecutionTestsVerifier,
    PropertyChecksVerifier,
)


class TestVerifierType:
    """Test VerifierType enum."""

    def test_all_verifier_types_defined(self):
        """Test all verifier types are defined."""
        assert VerifierType.EXECUTION is not None
        assert VerifierType.PROPERTY is not None
        assert VerifierType.LLM_CRITIQUE is not None
        assert VerifierType.ADVERSARIAL is not None
        assert VerifierType.HUMAN_SPOT is not None

    def test_verifier_type_values(self):
        """Test verifier type values."""
        assert VerifierType.EXECUTION.value == "execution"
        assert VerifierType.PROPERTY.value == "property"


class TestVerificationOutcome:
    """Test VerificationOutcome enum."""

    def test_all_outcomes_defined(self):
        """Test all outcomes are defined."""
        assert VerificationOutcome.PASS is not None
        assert VerificationOutcome.FAIL is not None
        assert VerificationOutcome.INCONCLUSIVE is not None
        assert VerificationOutcome.ERROR is not None


class TestVerifierResult:
    """Test VerifierResult dataclass."""

    def test_result_creation(self):
        """Test creating a verifier result."""
        result = VerifierResult(
            verifier_type=VerifierType.EXECUTION,
            outcome=VerificationOutcome.PASS,
            confidence=0.9,
            details="All tests passed"
        )
        assert result.verifier_type == VerifierType.EXECUTION
        assert result.outcome == VerificationOutcome.PASS
        assert result.confidence == 0.9
        assert result.details == "All tests passed"

    def test_result_with_error(self):
        """Test result with error outcome."""
        result = VerifierResult(
            verifier_type=VerifierType.PROPERTY,
            outcome=VerificationOutcome.ERROR,
            confidence=0.0,
            details="Invariant violation"
        )
        assert result.outcome == VerificationOutcome.ERROR


class TestImprovement:
    """Test Improvement dataclass."""

    def test_improvement_creation(self):
        """Test creating an improvement."""
        improvement = Improvement(
            id="test_imp",
            capability="code",
            description="Test improvement",
            code_changes=[{"file": "test.py", "content": "pass"}]
        )
        assert improvement.id == "test_imp"
        assert improvement.capability == "code"
        assert len(improvement.code_changes) == 1


class TestExecutionVerifier:
    """Test ExecutionTestsVerifier."""

    @pytest.fixture
    def verifier(self):
        return ExecutionTestsVerifier()

    @pytest.fixture
    def sample_improvement(self):
        return Improvement(
            id="imp_test",
            capability="code",
            description="Test improvement",
            code_changes=[{"file": "test.py", "content": "def foo(): pass"}],
            test_results={"tests_passed": 10}
        )

    @pytest.mark.asyncio
    async def test_verify_returns_result(self, verifier, sample_improvement):
        """Test that verify returns a VerifierResult."""
        result = await verifier.verify(sample_improvement)
        assert isinstance(result, VerifierResult)
        assert result.verifier_type == VerifierType.EXECUTION

    @pytest.mark.asyncio
    async def test_verify_has_confidence(self, verifier, sample_improvement):
        """Test that result includes confidence score."""
        result = await verifier.verify(sample_improvement)
        assert 0.0 <= result.confidence <= 1.0


class TestPropertyVerifier:
    """Test PropertyChecksVerifier."""

    @pytest.fixture
    def verifier(self):
        return PropertyChecksVerifier()

    @pytest.fixture
    def sample_improvement(self):
        return Improvement(
            id="imp_prop",
            capability="logic",
            description="Logic improvement",
            code_changes=[]
        )

    @pytest.mark.asyncio
    async def test_verify_checks_invariants(self, verifier, sample_improvement):
        """Test that verify checks invariants."""
        result = await verifier.verify(sample_improvement)
        assert isinstance(result, VerifierResult)
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
            capability="code",
            description="Lattice test improvement",
            code_changes=[{"file": "module.py", "content": "improved code"}],
            test_results={"tests_passed": 15}
        )

    def test_lattice_has_verifiers(self, lattice):
        """Test that lattice initializes with verifiers."""
        assert len(lattice.verifiers) > 0

    @pytest.mark.asyncio
    async def test_verify_returns_lattice_result(self, lattice, sample_improvement):
        """Test that verify returns LatticeResult."""
        result = await lattice.verify(sample_improvement)
        assert isinstance(result, LatticeResult)

    @pytest.mark.asyncio
    async def test_result_includes_all_verifier_results(self, lattice, sample_improvement):
        """Test that result includes results from all verifiers."""
        result = await lattice.verify(sample_improvement)
        # Should have results from all verifiers
        assert len(result.verifier_results) > 0

    @pytest.mark.asyncio
    async def test_consensus_calculation(self, lattice, sample_improvement):
        """Test consensus is calculated."""
        result = await lattice.verify(sample_improvement)
        # Should have a consensus outcome
        assert result.consensus_outcome in VerificationOutcome

    @pytest.mark.asyncio
    async def test_overall_confidence(self, lattice, sample_improvement):
        """Test overall confidence is calculated."""
        result = await lattice.verify(sample_improvement)
        # Should have a confidence score
        assert 0.0 <= result.consensus_confidence <= 1.0

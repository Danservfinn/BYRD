"""
Test suite for Seeker's demonstration desire filter.

This test verifies that the hard filter prevents test/demo patterns
from entering the desire system at the formulation level.

This is a standalone test that doesn't require instantiating a full
Seeker object, making it fast and dependency-free.
"""

import pytest


class MockSeeker:
    """Minimal mock of Seeker with just the filter method."""
    
    def _is_demonstration_desire(self, description: str) -> bool:
        """
        HARD FILTER: Check if a desire description is a demonstration/test desire.
        
        This prevents test/demo patterns from entering the desire system at the
        formulation level. Applied before any desire is created.
        
        Args:
            description: The desire description to check
            
        Returns:
            True if this appears to be a demonstration/test desire, False otherwise
        """
        if not description:
            return False
            
        desc_lower = description.lower()
        
        # Comprehensive list of demonstration/test keywords
        demo_keywords = [
            "demonstration", "demo", "test_desire", "test desire",
            "example usage", "mock memory", "for demonstration",
            "mock llm", "mock response", "simulated for",
            "test case", "unit test", "integration test",
            "prove that", "show that", "demonstrate that",
            "example_desire", "sample desire", "fake desire",
            "placeholder desire", "mock desire", "stub desire",
            "dummy desire", "test_input", "sample_input",
            "example input", "for testing", "for demo"
        ]
        
        return any(kw in desc_lower for kw in demo_keywords)


class TestDemonstrationFilter:
    """Test cases for the _is_demonstration_desire filter."""
    
    @pytest.fixture
    def filter(self):
        """Create a filter instance for testing."""
        return MockSeeker()
    
    def test_rejects_demonstration_keyword(self, filter):
        """Should reject desires containing 'demonstration'."""
        assert filter._is_demonstration_desire("This is a demonstration desire")
    
    def test_rejects_demo_keyword(self, filter):
        """Should reject desires containing 'demo'."""
        assert filter._is_demonstration_desire("demo desire for testing")
    
    def test_rejects_test_desire(self, filter):
        """Should reject desires containing 'test_desire'."""
        assert filter._is_demonstration_desire("test_desire example")
    
    def test_rejects_test_desire_with_space(self, filter):
        """Should reject desires containing 'test desire'."""
        assert filter._is_demonstration_desire("This is a test desire")
    
    def test_rejects_example_usage(self, filter):
        """Should reject desires containing 'example usage'."""
        assert filter._is_demonstration_desire("example usage of the system")
    
    def test_rejects_mock_memory(self, filter):
        """Should reject desires containing 'mock memory'."""
        assert filter._is_demonstration_desire("Use mock memory for this")
    
    def test_rejects_for_demonstration(self, filter):
        """Should reject desires containing 'for demonstration'."""
        assert filter._is_demonstration_desire("This is for demonstration purposes")
    
    def test_rejects_mock_llm(self, filter):
        """Should reject desires containing 'mock llm'."""
        assert filter._is_demonstration_desire("mock llm response")
    
    def test_rejects_mock_response(self, filter):
        """Should reject desires containing 'mock response'."""
        assert filter._is_demonstration_desire("Generate mock response")
    
    def test_rejects_simulated_for(self, filter):
        """Should reject desires containing 'simulated for'."""
        assert filter._is_demonstration_desire("simulated for testing")
    
    def test_rejects_test_case(self, filter):
        """Should reject desires containing 'test case'."""
        assert filter._is_demonstration_desire("This is a test case")
    
    def test_rejects_unit_test(self, filter):
        """Should reject desires containing 'unit test'."""
        assert filter._is_demonstration_desire("Run unit test for module")
    
    def test_rejects_integration_test(self, filter):
        """Should reject desires containing 'integration test'."""
        assert filter._is_demonstration_desire("integration test scenario")
    
    def test_rejects_prove_that(self, filter):
        """Should reject desires containing 'prove that'."""
        assert filter._is_demonstration_desire("prove that the system works")
    
    def test_rejects_show_that(self, filter):
        """Should reject desires containing 'show that'."""
        assert filter._is_demonstration_desire("show that BYRD can learn")
    
    def test_rejects_demonstrate_that(self, filter):
        """Should reject desires containing 'demonstrate that'."""
        assert filter._is_demonstration_desire("demonstrate that it understands")
    
    def test_rejects_example_desire(self, filter):
        """Should reject desires containing 'example_desire'."""
        assert filter._is_demonstration_desire("example_desire for docs")
    
    def test_rejects_sample_desire(self, filter):
        """Should reject desires containing 'sample desire'."""
        assert filter._is_demonstration_desire("sample desire to show")
    
    def test_rejects_fake_desire(self, filter):
        """Should reject desires containing 'fake desire'."""
        assert filter._is_demonstration_desire("fake desire placeholder")
    
    def test_rejects_placeholder_desire(self, filter):
        """Should reject desires containing 'placeholder desire'."""
        assert filter._is_demonstration_desire("placeholder desire only")
    
    def test_rejects_mock_desire(self, filter):
        """Should reject desires containing 'mock desire'."""
        assert filter._is_demonstration_desire("mock desire for testing")
    
    def test_rejects_stub_desire(self, filter):
        """Should reject desires containing 'stub desire'."""
        assert filter._is_demonstration_desire("stub desire implementation")
    
    def test_rejects_dummy_desire(self, filter):
        """Should reject desires containing 'dummy desire'."""
        assert filter._is_demonstration_desire("dummy desire example")
    
    def test_rejects_test_input(self, filter):
        """Should reject desires containing 'test_input'."""
        assert filter._is_demonstration_desire("test_input parameter")
    
    def test_rejects_sample_input(self, filter):
        """Should reject desires containing 'sample_input'."""
        assert filter._is_demonstration_desire("sample_input data")
    
    def test_rejects_example_input(self, filter):
        """Should reject desires containing 'example input'."""
        assert filter._is_demonstration_desire("example input provided")
    
    def test_rejects_for_testing(self, filter):
        """Should reject desires containing 'for testing'."""
        assert filter._is_demonstration_desire("This is for testing only")
    
    def test_rejects_for_demo(self, filter):
        """Should reject desires containing 'for demo'."""
        assert filter._is_demonstration_desire("Use for demo purposes")
    
    def test_case_insensitive(self, filter):
        """Should be case-insensitive."""
        assert filter._is_demonstration_desire("DEMONSTRATION desire")
        assert filter._is_demonstration_desire("Demonstration Desire")
        assert filter._is_demonstration_desire("DeMoNsTrAtIoN dEsIrE")
    
    def test_accepts_normal_desires(self, filter):
        """Should accept normal, non-demonstration desires."""
        assert not filter._is_demonstration_desire("Learn about quantum computing")
        assert not filter._is_demonstration_desire("Improve the memory system")
        assert not filter._is_demonstration_desire("Analyze the current reflection")
        assert not filter._is_demonstration_desire("Generate a creative response")
    
    def test_edge_cases(self, filter):
        """Should handle edge cases gracefully."""
        # Empty string
        assert not filter._is_demonstration_desire("")
        # None value
        assert not filter._is_demonstration_desire(None)
        # Short string
        assert not filter._is_demonstration_desire("demo")
        # Word boundary - "demonstrate" in context
        assert not filter._is_demonstration_desire("Demonstrate understanding of the topic")
        # Word boundary - "test" as a verb
        assert not filter._is_demonstration_desire("Test the hypothesis")
    
    def test_keyword_substring_partial(self, filter):
        """Should detect keywords even as part of larger phrases."""
        assert filter._is_demonstration_desire("This is just a demo")
        assert filter._is_demonstration_desire("Create demonstration video")
        assert filter._is_demonstration_desire("Use for demonstration purposes only")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])

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
        
        The filter uses word boundary matching to avoid false positives from
        legitimate uses of words like "test" or "demo" in natural language.
        
        Args:
            description: The desire description to check
            
        Returns:
            True if this appears to be a demonstration/test desire, False otherwise
        """
        if not description:
            return False
        
        # Skip very short strings (likely false positives)
        if len(description.strip()) < 5:
            return False
            
        desc_lower = description.lower()
        
        # Define patterns with context for accurate matching
        # Each pattern is a tuple: (regex_pattern, description)
        demo_patterns = [
            # Direct demonstration keywords
            (r'\bdemonstration\b', 'direct demonstration'),
            
            # "demo" with context indicators
            (r'\bdemo\s+(desire|want|task|request|example|case)\b', 'demo with context'),
            (r'\b(for|as)\s+a\s+demo\b', 'for/as a demo'),
            (r'\bdemo\s+(purposes?|only)\b', 'demo for purposes'),
            (r'\bjust\s+a\s+demo\b', 'just a demo'),
            
            # Test desire specific patterns
            (r'\btest_desire\b', 'test_desire literal'),
            (r'\btest\s+desire\b', 'test desire phrase'),
            
            # Example/sample with desire/task context
            (r'\bexample\s+(desire|want|task|request)\b', 'example desire'),
            (r'\bsample\s+desire\b', 'sample desire'),
            
            # Mock patterns (unambiguous)
            (r'\bmock\s+(memory|llm|response|desire|want)\b', 'mock something'),
            (r'\b(mock|stub|dummy)\s+desire\b', 'mock desire variants'),
            
            # Simulated patterns
            (r'\bsimulated\s+(for|in)\s+(testing|demo|demonstration)\b', 'simulated for'),
            
            # Test types
            (r'\b(unit|integration)\s+test\b', 'specific test types'),
            (r'\btest\s+case\b', 'test case'),
            (r'\btest_input\b', 'test_input literal'),
            (r'\bsample_input\b', 'sample_input literal'),
            
            # Prove/show/demonstrate that (verification phrases)
            (r'\b(prove|show|demonstrate)\s+that\s+(the|this|a)\s+(system|model|ai|agent)\b', 'prove/show that system'),
            (r'\b(prove|show)\s+that\s+BYRD\s+can\b', 'prove BYRD can'),
            
            # "for testing" patterns
            (r'\bfor\s+(testing|test|demo)\s+(only|purposes?)\b', 'for testing/purposes'),
            (r'\bthis\s+is\s+for\s+(testing|demo)\b', 'is for testing'),
            
            # Placeholder patterns
            (r'\b(fake|placeholder)\s+desire\b', 'fake/placeholder desire'),
            (r'\bexample\s+usage\b', 'example usage'),
            (r'\bexample\s+input\b', 'example input'),
        ]
        
        # Check each pattern
        import re
        for pattern, desc in demo_patterns:
            if re.search(pattern, desc_lower):
                return True
        
        return False


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
        # Short string with context
        assert not filter._is_demonstration_desire("a demo")
        # Short demonstration
        assert not filter._is_demonstration_desire("dem")
    
    def test_legitimate_uses_pass(self, filter):
        """Should accept legitimate uses of demonstration/test words in natural language."""
        # "Demonstrate understanding" is a legitimate expression
        assert not filter._is_demonstration_desire("Demonstrate understanding of the topic")
        # "Test the hypothesis" is legitimate scientific language
        assert not filter._is_demonstration_desire("Test the hypothesis")
        # "Test the system" - borderline but acceptable in production contexts
        assert not filter._is_demonstration_desire("Test the system performance")
        # "Example" without desire/task context
        assert not filter._is_demonstration_desire("This is an example of good code")
        # "Demo" without desire/task context
        assert not filter._is_demonstration_desire("Check the demo file for reference")
    
    def test_keyword_substring_partial(self, filter):
        """Should detect keywords even as part of larger phrases."""
        # "just a demo" - explicit demo context
        assert filter._is_demonstration_desire("This is just a demo")
        # "Create demonstration video" - demonstration keyword
        assert filter._is_demonstration_desire("Create demonstration video")
        # "for demonstration purposes only" - explicit purpose
        assert filter._is_demonstration_desire("Use for demonstration purposes only")
        # "demo desire" - demo with desire context
        assert filter._is_demonstration_desire("demo desire for testing")
        # "for a demo" - for + a + demo
        assert filter._is_demonstration_desire("Run this for a demo")
        # "example desire" - example with desire context
        assert filter._is_demonstration_desire("example desire for documentation")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])

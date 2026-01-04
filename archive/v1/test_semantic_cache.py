#!/usr/bin/env python3
"""Quick test to validate semantic cache integration."""

import sys
import asyncio

# Test imports
try:
    from semantic_cache import SemanticCache, CacheEntry
    print("✓ semantic_cache imports successfully")
except Exception as e:
    print(f"✗ Failed to import semantic_cache: {e}")
    sys.exit(1)

# Test basic cache operations
def test_cache_basic():
    cache = SemanticCache(max_entries=10, ttl_seconds=60)
    
    # Test put and get
    cache.put("Hello world", "Hi there!")
    result = cache.get("Hello world")
    assert result is not None, "Cache should return value"
    response, is_semantic = result
    assert response == "Hi there!", f"Expected 'Hi there!' got '{response}'"
    assert is_semantic == False, "First hit should be exact match"
    print("✓ Basic cache get/set works")
    
    # Test stats
    stats = cache.get_stats()
    assert stats['hits'] == 1, f"Expected 1 hit, got {stats['hits']}"
    assert stats['misses'] == 1, f"Expected 1 miss, got {stats['misses']}"
    print("✓ Cache stats work")

    # Test miss
    result = cache.get("Never seen before")
    assert result is None, "Cache should return None for miss"
    print("✓ Cache miss works")

    # Test clear
    cache.clear()
    stats = cache.get_stats()
    assert stats['total_entries'] == 0, "Cache should be empty after clear"
    print("✓ Cache clear works")

def test_llm_client_imports():
    try:
        from llm_client import OpenRouterClient, ZAIClient, create_llm_client, LLMClient
        print("✓ llm_client imports successfully with semantic cache")
        
        # Check that classes have cache-related attributes in their signatures
        import inspect
        
        # Check OpenRouterClient
        sig = inspect.signature(OpenRouterClient.__init__)
        params = list(sig.parameters.keys())
        assert 'enable_cache' in params, "OpenRouterClient should have enable_cache param"
        assert 'cache_ttl' in params, "OpenRouterClient should have cache_ttl param"
        print("✓ OpenRouterClient has cache parameters")
        
        # Check ZAIClient
        sig = inspect.signature(ZAIClient.__init__)
        params = list(sig.parameters.keys())
        assert 'enable_cache' in params, "ZAIClient should have enable_cache param"
        assert 'cache_ttl' in params, "ZAIClient should have cache_ttl param"
        print("✓ ZAIClient has cache parameters")
        
    except Exception as e:
        print(f"✗ llm_client import test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("Testing Semantic Cache Implementation...\n")
    
    test_cache_basic()
    print()
    test_llm_client_imports()
    
    print("\n✅ All tests passed!")

#!/usr/bin/env python3
"""
Simple test of DirectExecutor - no frills, just verification.
"""
import sys
import asyncio

# Import the DirectExecutor
from direct_executor import DirectExecutor, ExecutionPattern, DirectExecutionResult

class SimpleMemory:
    """Minimal mock memory."""
    def __init__(self):
        self.reflections = []
    
    async def add_reflection(self, content, context="test", importance=0.5, metadata=None):
        self.reflections.append(content)
        return True
    
    async def execute_query(self, query, params=None):
        return {"data": []}


async def test_basics():
    """Test basic functionality."""
    print("Testing DirectExecutor...")
    
    memory = SimpleMemory()
    executor = DirectExecutor(memory)
    
    # Test 1: Direct command
    result = await executor.execute_desire_directly("Execute: test something")
    assert result.success == True, "Direct command should succeed"
    assert result.bypassed_routing == True, "Should bypass routing"
    print("✓ Direct command executed without routing")
    
    # Test 2: Self-fulfilling desire
    result = await executor.execute_desire_directly("Learn by practicing")
    assert result.success == True, "Self-fulfilling should succeed"
    print("✓ Self-fulfilling desire executed without routing")
    
    # Test 3: Crystal activation
    result = await executor.execute_desire_directly("Activate the crystal")
    assert result.success == True, "Crystal activation should succeed"
    print("✓ Crystal activation executed without routing")
    
    # Test 4: Non-executable
    result = await executor.execute_desire_directly("I want to think about this")
    assert result.success == False, "Non-executable should fail"
    print("✓ Non-executable desire correctly identified")
    
    # Test 5: Stats
    stats = executor.get_stats()
    assert stats['routing_paradox_broken'] == True, "Paradox should be broken"
    print("✓ Routing paradox confirmed broken")
    
    print("\nAll tests passed! Execution without routing works.")
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_basics())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

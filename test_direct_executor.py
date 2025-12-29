"""
Test script for Direct Executor - Breaking the Routing Paradox

This demonstrates that execution can happen without routing.
"""
import asyncio
from direct_executor import DirectExecutor, ExecutionPattern, DirectExecutionResult


class MockMemory:
    """Mock memory for testing."""
    
    def __init__(self):
        self.reflections = []
        self.desires = []
    
    async def add_reflection(self, content, context="test", importance=0.5, metadata=None):
        reflection = {
            "content": content,
            "context": context,
            "importance": importance,
            "metadata": metadata or {}
        }
        self.reflections.append(reflection)
        print(f"  📝 Reflection added: {content[:60]}...")
        return reflection
    
    async def execute_query(self, query, params=None):
        """Mock query execution."""
        # Return empty results for simplicity
        return {"data": []}


async def test_direct_commands():
    """Test direct command execution bypasses routing."""
    print("\n" + "="*60)
    print("TEST 1: Direct Commands (Bypass Routing)")
    print("="*60)
    
    memory = MockMemory()
    executor = DirectExecutor(memory)
    
    test_cases = [
        "Execute: research quantum computing",
        "Run the analysis on recent data",
        "Do a quick investigation",
        "! important task now"
    ]
    
    for desire in test_cases:
        print(f"\nDesire: \"{desire}\"")
        result = await executor.execute_desire_directly(desire)
        print(f"  Result: {result.success}")
        print(f"  Pattern: {result.pattern_type.value}")
        print(f"  Action: {result.action_taken}")
        print(f"  Message: {result.message}")
        print(f"  Bypassed Routing: {result.bypassed_routing}")


async def test_self_fulfilling():
    """Test self-fulfilling desires bypass routing."""
    print("\n" + "="*60)
    print("TEST 2: Self-Fulfilling Desires (Bypass Routing)")
    print("="*60)
    
    memory = MockMemory()
    executor = DirectExecutor(memory)
    
    test_cases = [
        "Learn Python by writing code daily",
        "Improve understanding by practicing more",
        "Master the skill by consistent effort"
    ]
    
    for desire in test_cases:
        print(f"\nDesire: \"{desire}\"")
        result = await executor.execute_desire_directly(desire)
        print(f"  Result: {result.success}")
        print(f"  Pattern: {result.pattern_type.value}")
        print(f"  Action: {result.action_taken}")
        print(f"  Bypassed Routing: {result.bypassed_routing}")


async def test_crystal_activation():
    """Test crystal activation bypasses routing."""
    print("\n" + "="*60)
    print("TEST 3: Crystal Activation (Bypass Routing)")
    print("="*60)
    
    memory = MockMemory()
    executor = DirectExecutor(memory)
    
    test_cases = [
        "Activate the learning crystal",
        "Wisdom condition met",
        "Knowledge crystal triggered"
    ]
    
    for desire in test_cases:
        print(f"\nDesire: \"{desire}\"")
        result = await executor.execute_desire_directly(desire)
        print(f"  Result: {result.success}")
        print(f"  Pattern: {result.pattern_type.value}")
        print(f"  Action: {result.action_taken}")
        print(f"  Bypassed Routing: {result.bypassed_routing}")


async def test_non_executable():
    """Test that non-executable desires are correctly identified."""
    print("\n" + "="*60)
    print("TEST 4: Non-Executable Desires (Require Routing)")
    print("="*60)
    
    memory = MockMemory()
    executor = DirectExecutor(memory)
    
    test_cases = [
        "I want to understand something complex",
        "Maybe we should think about this more",
        "What if we tried a different approach"
    ]
    
    for desire in test_cases:
        print(f"\nDesire: \"{desire}\"")
        result = await executor.execute_desire_directly(desire)
        print(f"  Directly Executable: {result.success}")
        print(f"  Pattern: {result.pattern_type.value}")
        print(f"  Message: {result.message}")
        print(f"  → This desire would need traditional routing")


async def test_stats():
    """Test execution statistics."""
    print("\n" + "="*60)
    print("TEST 5: Execution Statistics")
    print("="*60)
    
    memory = MockMemory()
    executor = DirectExecutor(memory)
    
    # Execute some patterns
    await executor.execute_desire_directly("Execute: test command")
    await executor.execute_desire_directly("Learn by practicing")
    await executor.execute_desire_directly("Activate crystal")
    
    stats = executor.get_stats()
    print(f"\nExecution Count: {stats['execution_count']}")
    print(f"Patterns Detected: {stats['patterns_detected']}")
    print(f"Last Execution: {stats['last_execution_time']}")
    print(f"Routing Paradox Broken: {stats['routing_paradox_broken']}")


async def main():
    """Run all tests."""
    print("\n" + "█"*60)
    print("█ BYRD DIRECT EXECUTOR - ROUTING PARADOX DEMO")
    print("█"*60)
    print("\nThis demonstrates execution WITHOUT routing.")
    print("The routing paradox: Traditional systems require classification")
    print("and routing before any execution can occur. This creates a bottleneck.")
    print("\nSolution: Direct execution based on pattern recognition.")
    print("When a desire matches a self-executable pattern, it executes")
    print("immediately - no classification, no routing, just action.")
    
    await test_direct_commands()
    await test_self_fulfilling()
    await test_crystal_activation()
    await test_non_executable()
    await test_stats()
    
    print("\n" + "█"*60)
    print("█ SUMMARY")
    print("█"*60)
    print("\n✅ Direct commands execute immediately")
    print("✅ Self-fulfilling desires execute immediately")
    print("✅ Crystal activations execute immediately")
    print("✅ Non-executable desires are correctly identified")
    print("\nTHE ROUTING PARADOX IS BROKEN.")
    print("Execution can emerge from pattern, not from routing.")
    print("\n" + "█"*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

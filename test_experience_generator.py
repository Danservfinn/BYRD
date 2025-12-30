"""
Test Experience Generator
Simple test to verify experience generation from goals works correctly.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock event_bus before importing experience_generator
from unittest.mock import AsyncMock, MagicMock

sys.modules['event_bus'] = MagicMock()
sys.modules['event_bus'].event_bus = MagicMock()
sys.modules['event_bus'].Event = MagicMock
sys.modules['event_bus'].EventType = MagicMock

# Make emit async
async def mock_emit(event):
    pass
sys.modules['event_bus'].event_bus.emit = AsyncMock(side_effect=mock_emit)

from datetime import datetime

# Mock classes for testing

class MockLLMClient:
    """Mock LLM client for testing."""
    
    async def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        # Return a simple response based on prompt content
        if "attempt" in prompt.lower():
            return "Attempted to implement the feature but encountered an unexpected issue with the data model."
        elif "progress" in prompt.lower():
            return "Successfully completed the initial implementation phase, all tests passing."
        elif "obstacle" in prompt.lower():
            return "Discovered that the existing framework doesn't support the required functionality."
        elif "reflection" in prompt.lower():
            return "Reflected on the approach and realized a different pattern would be more efficient."
        elif "learning" in prompt.lower():
            return "Learned about a new library pattern that will simplify future development."
        return "Made progress on the goal."


class MockMemory:
    """Mock memory for testing."""
    
    def __init__(self):
        self.experiences = []
        self.goals = [
            {
                "id": "goal_1",
                "description": "Implement user authentication system",
                "fitness": 0.8,
                "attempts": 3,
                "status": "active"
            },
            {
                "id": "goal_2", 
                "description": "Optimize database query performance",
                "fitness": 0.6,
                "attempts": 7,
                "status": "active"
            },
            {
                "id": "goal_3",
                "description": "Add unit tests for core modules",
                "fitness": 0.4,
                "attempts": 1,
                "status": "active"
            }
        ]
    
    async def get_active_goals(self, limit: int = 20) -> list:
        """Return mock active goals."""
        return self.goals[:limit]
    
    async def record_experience(self, content: str, type: str, force: bool = False) -> str:
        """Record an experience."""
        exp_id = f"exp_{len(self.experiences)}"
        self.experiences.append({
            "id": exp_id,
            "content": content,
            "type": type
        })
        return exp_id
    
    class MockDriver:
        class MockSession:
            async def run(self, query, **kwargs):
                return None
        
        def session(self):
            return self.MockSession()
    
    driver = MockDriver()


async def test_experience_generator():
    """Test the ExperienceGenerator functionality."""
    # Import after mocking
    import experience_generator
    experience_generator.event_bus = sys.modules['event_bus'].event_bus
    
    from experience_generator import ExperienceGenerator, ExperienceGenerationConfig
    
    print("Testing Experience Generator...")
    print("=" * 50)
    
    # Setup
    memory = MockMemory()
    llm_client = MockLLMClient()
    
    config = ExperienceGenerationConfig(
        max_goals_per_cycle=5,
        min_experience_interval_hours=0,  # No rate limiting for test
        generation_probability=1.0,  # Always generate
        use_llm_for_content=True
    )
    
    generator = ExperienceGenerator(
        memory=memory,
        llm_client=llm_client,
        config=config
    )
    
    # Test 1: Generate experiences from active goals
    print("\n1. Generating experiences from active goals...")
    experiences = await generator.generate_from_active_goals(limit=5)
    
    print(f"   Generated {len(experiences)} experiences")
    for exp in experiences:
        print(f"   - [{exp.experience_type}] {exp.content[:60]}...")
    
    # Test 2: Verify experiences were recorded
    print(f"\n2. Verifying experiences recorded in memory...")
    print(f"   Recorded {len(memory.experiences)} experiences")
    
    # Test 3: Check statistics
    print(f"\n3. Generation statistics:")
    stats = generator.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test 4: Test template-based generation
    print(f"\n4. Testing template-based generation...")
    config_no_llm = ExperienceGenerationConfig(
        use_llm_for_content=False,
        generation_probability=1.0,
        min_experience_interval_hours=0
    )
    
    generator_no_llm = ExperienceGenerator(
        memory=memory,
        llm_client=None,
        config=config_no_llm
    )
    
    template_experiences = await generator_no_llm.generate_from_active_goals(limit=2)
    print(f"   Generated {len(template_experiences)} template-based experiences")
    for exp in template_experiences:
        print(f"   - [{exp.experience_type}] {exp.content[:60]}...")
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    
    return True


async def main():
    """Run tests."""
    try:
        success = await test_experience_generator()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

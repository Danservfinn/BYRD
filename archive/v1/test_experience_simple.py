"""
Simple standalone test for experience generation logic.
Tests the core algorithms without dependencies.
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass, field


# Core classes for testing (extracted from experience_generator.py)

@dataclass
class ExperienceGenerationConfig:
    max_goals_per_cycle: int = 10
    min_experience_interval_hours: float = 1.0
    generation_probability: float = 0.7
    attempt_weight: float = 0.6
    progress_weight: float = 0.4
    use_llm_for_content: bool = True


@dataclass 
class GeneratedExperience:
    content: str
    type: str
    goal_id: str
    goal_description: str
    experience_type: str
    metadata: Dict = field(default_factory=dict)


class SimpleExperienceGenerator:
    """Simplified version for testing core logic."""
    
    EXP_TYPES = {
        "attempt": "goal_attempt",
        "progress": "goal_progress", 
        "reflection": "goal_reflection",
        "obstacle": "goal_obstacle",
        "learning": "goal_learning"
    }
    
    TEMPLATES = {
        "attempt": [
            "Made progress on {goal} by breaking down the required steps.",
            "Attempted {goal} but encountered unexpected complexity.",
            "Started working on {goal} with initial research phase.",
        ],
        "progress": [
            "Made measurable progress on {goal} - completed a key subtask.",
            "Advanced {goal} by overcoming a technical hurdle.",
            "Achieved a milestone in {goal} - moved 25% closer to completion.",
        ],
        "reflection": [
            "Reflected on {goal} and identified that current approach needs adjustment.",
            "Considered alternative strategies for {goal} after recent attempts.",
        ],
        "obstacle": [
            "Encountered an obstacle with {goal}: missing dependency or resource.",
            "Blocked on {goal} due to external constraint requiring resolution.",
        ],
        "learning": [
            "Learned a new approach while working on {goal}.",
            "Gained insight from {goal} about a more efficient solution pattern.",
        ]
    }
    
    def __init__(self, config: ExperienceGenerationConfig = None):
        self.config = config or ExperienceGenerationConfig()
        self._last_generation_time: Dict[str, datetime] = {}
        self._total_generated = 0
        self._attempts_generated = 0
        self._progress_generated = 0
    
    def filter_goals_for_generation(self, goals_data: List[Dict]) -> List[Dict]:
        """Filter goals that should get new experiences."""
        filtered = []
        
        for goal_dict in goals_data:
            goal_id = goal_dict.get("id")
            fitness = goal_dict.get("fitness", 0.5)
            
            # Check time-based rate limiting
            if goal_id in self._last_generation_time:
                time_since = datetime.now() - self._last_generation_time[goal_id]
                hours_since = time_since.total_seconds() / 3600
                
                if hours_since < self.config.min_experience_interval_hours:
                    continue
            
            # Apply probability threshold
            fitness_boosted_prob = self.config.generation_probability * (1 + fitness)
            effective_prob = min(fitness_boosted_prob, 0.95)
            
            if random.random() > effective_prob:
                continue
            
            filtered.append(goal_dict)
        
        # Sort by fitness (highest first)
        filtered.sort(key=lambda g: g.get("fitness", 0.5), reverse=True)
        
        return filtered
    
    def generate_experiences_for_goal(self, goal_dict: Dict) -> List[GeneratedExperience]:
        """Generate appropriate experiences for a single goal."""
        goal_id = goal_dict.get("id")
        description = goal_dict.get("description", "")
        fitness = goal_dict.get("fitness", 0.5)
        attempts = goal_dict.get("attempts", 0)
        
        experiences = []
        
        # Determine what type of experience to generate
        if fitness > 0.7:
            exp_type = random.choices(
                ["progress", "learning", "reflection"],
                weights=[0.5, 0.3, 0.2]
            )[0]
        elif attempts > 5:
            exp_type = random.choices(
                ["reflection", "obstacle", "attempt"],
                weights=[0.4, 0.4, 0.2]
            )[0]
        else:
            exp_type = random.choices(
                ["attempt", "progress"],
                weights=[self.config.attempt_weight, self.config.progress_weight]
            )[0]
        
        # Generate content from templates
        content = self.generate_template_experience(description, exp_type)
        
        if content:
            experience = GeneratedExperience(
                content=content,
                type=self.EXP_TYPES.get(exp_type, "goal_attempt"),
                goal_id=goal_id,
                goal_description=description,
                experience_type=exp_type,
                metadata={
                    "goal_fitness": fitness,
                    "goal_attempts": attempts
                }
            )
            experiences.append(experience)
            
            self._total_generated += 1
            if exp_type == "attempt":
                self._attempts_generated += 1
            elif exp_type == "progress":
                self._progress_generated += 1
        
        return experiences
    
    def generate_template_experience(self, goal_description: str, exp_type: str) -> str:
        """Generate experience content from templates."""
        template_list = self.TEMPLATES.get(exp_type, self.TEMPLATES["attempt"])
        template = random.choice(template_list)
        
        goal_short = goal_description[:100] + "..." if len(goal_description) > 100 else goal_description
        return template.format(goal=goal_short)


async def test_experience_generator():
    """Test the experience generation logic."""
    print("Testing Experience Generator Logic")
    print("=" * 60)
    
    # Test data
    goals = [
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
        },
        {
            "id": "goal_4",
            "description": "Improve documentation",
            "fitness": 0.9,
            "attempts": 0,
            "status": "active"
        }
    ]
    
    # Test 1: Filtering logic
    print("\nTest 1: Goal Filtering")
    print("-" * 40)
    
    config = ExperienceGenerationConfig(
        generation_probability=1.0,  # Always generate
        min_experience_interval_hours=0  # No rate limiting
    )
    
    generator = SimpleExperienceGenerator(config)
    filtered = generator.filter_goals_for_generation(goals)
    
    print(f"Input goals: {len(goals)}")
    print(f"Filtered goals: {len(filtered)}")
    print(f"Fitness-sorted: {[g['fitness'] for g in filtered]}")
    assert len(filtered) == 4, "Should filter all goals when probability=1.0"
    assert filtered[0]['fitness'] >= filtered[-1]['fitness'], "Should be sorted by fitness"
    print("✓ Test 1 passed")
    
    # Test 2: Experience generation for high-fitness goals
    print("\nTest 2: High-Fitness Goal Experience Generation")
    print("-" * 40)
    
    high_fitness_goal = {"id": "test_1", "description": "Build advanced AI system", "fitness": 0.85, "attempts": 2}
    
    generator_high = SimpleExperienceGenerator()
    experiences = generator_high.generate_experiences_for_goal(high_fitness_goal)
    
    print(f"Goal fitness: {high_fitness_goal['fitness']}")
    print(f"Generated {len(experiences)} experience(s)")
    for exp in experiences:
        print(f"  [{exp.experience_type}] {exp.content[:50]}...")
    
    assert len(experiences) == 1, "Should generate one experience"
    assert experiences[0].experience_type in ["progress", "learning", "reflection"], \
        "High fitness should generate progress/learning/reflection"
    print("✓ Test 2 passed")
    
    # Test 3: Experience generation for low-attempt goals
    print("\nTest 3: Low-Attempt Goal Experience Generation")
    print("-" * 40)
    
    low_attempt_goal = {"id": "test_2", "description": "Fix a bug", "fitness": 0.5, "attempts": 1}
    
    generator_low = SimpleExperienceGenerator()
    experiences = generator_low.generate_experiences_for_goal(low_attempt_goal)
    
    print(f"Goal attempts: {low_attempt_goal['attempts']}")
    print(f"Generated {len(experiences)} experience(s)")
    for exp in experiences:
        print(f"  [{exp.experience_type}] {exp.content[:50]}...")
    
    assert len(experiences) == 1, "Should generate one experience"
    print("✓ Test 3 passed")
    
    # Test 4: High-attempt goals generate reflections
    print("\nTest 4: High-Attempt Goal Reflection Generation")
    print("-" * 40)
    
    high_attempt_goal = {"id": "test_3", "description": "Solve complex problem", "fitness": 0.5, "attempts": 8}
    
    # Run multiple times to check distribution
    reflection_count = 0
    for _ in range(20):
        experiences = generator_low.generate_experiences_for_goal(high_attempt_goal)
        if experiences and experiences[0].experience_type == "reflection":
            reflection_count += 1
    
    print(f"High-attempt goal generated reflection {reflection_count}/20 times")
    assert reflection_count > 5, "High-attempt goals should generate reflections frequently"
    print("✓ Test 4 passed")
    
    # Test 5: Statistics tracking
    print("\nTest 5: Statistics Tracking")
    print("-" * 40)
    
    stats_gen = SimpleExperienceGenerator(ExperienceGenerationConfig(generation_probability=1.0))
    
    # Generate experiences for multiple goals
    for goal in goals:
        exps = stats_gen.generate_experiences_for_goal(goal)
        
    stats = {
        "total_generated": stats_gen._total_generated,
        "attempts": stats_gen._attempts_generated,
        "progress": stats_gen._progress_generated
    }
    
    print(f"Statistics: {stats}")
    assert stats["total_generated"] > 0, "Should have generated experiences"
    print("✓ Test 5 passed")
    
    # Test 6: Rate limiting
    print("\nTest 6: Rate Limiting")
    print("-" * 40)
    
    rate_limited_config = ExperienceGenerationConfig(
        min_experience_interval_hours=1.0,
        generation_probability=1.0
    )
    
    rate_gen = SimpleExperienceGenerator(rate_limited_config)
    
    # First pass
    filtered_1 = rate_gen.filter_goals_for_generation([goals[0]])
    rate_gen._last_generation_time[goals[0]['id']] = datetime.now() - timedelta(minutes=30)
    
    # Second pass (too soon)
    filtered_2 = rate_gen.filter_goals_for_generation([goals[0]])
    
    print(f"First pass: {len(filtered_1)} goals")
    print(f"Second pass (30 min later): {len(filtered_2)} goals (should be 0)")
    assert len(filtered_2) == 0, "Should filter out goals processed too recently"
    print("✓ Test 6 passed")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    
    return True


async def main():
    """Run tests."""
    try:
        success = await test_experience_generator()
        return 0 if success else 1
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    print(f"\nExit code: {exit_code}")

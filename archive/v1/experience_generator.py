"""
BYRD Experience Generator
Bridges planning (goals) with execution (experiences).

This module generates experiences from pending/active goals to ensure
BYRD balances planning with action-taking. Without this mechanism,
BYRD could spend infinite time planning without ever executing.

PRINCIPLE: Every goal should generate actionable experiences that
represent attempts, progress, and learning - whether successful or not.

USAGE:
    generator = ExperienceGenerator(memory, goal_evolver)
    await generator.generate_from_active_goals()
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from memory import Memory
from goal_evolver import GoalEvolver, EvolvedGoal, GoalStatus
from event_bus import event_bus, Event, EventType
from llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class ExperienceGenerationConfig:
    """
    Configuration for experience generation from goals.
    
    Balances how aggressively we generate experiences vs allowing
    natural execution to create them.
    """
    # How many active goals to process per cycle
    max_goals_per_cycle: int = 10
    
    # Minimum time between experience generations for the same goal
    min_experience_interval_hours: float = 1.0
    
    # Probability of generating an experience for a goal (0.0-1.0)
    # Higher values = more proactive execution simulation
    generation_probability: float = 0.7
    
    # Weight for generating "attempt" experiences vs "progress" experiences
    attempt_weight: float = 0.6
    progress_weight: float = 0.4
    
    # Whether to use LLM for experience content generation
    use_llm_for_content: bool = True


@dataclass 
class GeneratedExperience:
    """An experience generated from a goal."""
    content: str
    type: str
    goal_id: str
    goal_description: str
    experience_type: str  # "attempt", "progress", "reflection", "obstacle"
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExperienceGenerator:
    """
    Generates experiences from pending/active goals.
    
    This is the bridge between LOOP 2 (Goal Evolver) and the broader
    execution loop. It ensures that having goals leads to action-taking,
    preventing infinite planning without execution.
    
    KEY INSIGHT: In a real AGI system, experiences come naturally from
    attempting goals. For simulation/bootstrapping purposes, we generate
    experiences proactively to jumpstart the learning cycle.
    """
    
    # Experience types for goals
    EXP_TYPES = {
        "attempt": "goal_attempt",
        "progress": "goal_progress", 
        "reflection": "goal_reflection",
        "obstacle": "goal_obstacle",
        "learning": "goal_learning"
    }
    
    def __init__(
        self,
        memory: Memory,
        goal_evolver: Optional[GoalEvolver] = None,
        llm_client: Optional[LLMClient] = None,
        config: Optional[ExperienceGenerationConfig] = None
    ):
        self.memory = memory
        self.goal_evolver = goal_evolver
        self.llm_client = llm_client
        self.config = config or ExperienceGenerationConfig()
        
        # Tracking for rate limiting
        self._last_generation_time: Dict[str, datetime] = {}
        
        # Statistics
        self._total_generated = 0
        self._attempts_generated = 0
        self._progress_generated = 0
        self._obstacles_generated = 0
    
    async def generate_from_active_goals(
        self, 
        limit: Optional[int] = None
    ) -> List[GeneratedExperience]:
        """
        Generate experiences from active goals.
        
        This is the main entry point. It:
        1. Fetches active goals from memory
        2. Filters goals that need experience generation
        3. Generates appropriate experiences for each
        4. Records them in memory
        5. Links experiences to their source goals
        
        Args:
            limit: Max number of goals to process (overrides config)
            
        Returns:
            List of generated experiences
        """
        limit = limit or self.config.max_goals_per_cycle
        
        logger.info(f"Generating experiences from up to {limit} active goals...")
        
        # Step 1: Get active goals
        goals_data = await self.memory.get_active_goals(limit=limit * 2)
        
        if not goals_data:
            logger.info("No active goals found for experience generation")
            return []
        
        logger.debug(f"Found {len(goals_data)} active goals")
        
        # Step 2: Filter goals that need experience generation
        goals_to_process = await self._filter_goals_for_generation(goals_data)
        
        if not goals_to_process:
            logger.info("No goals ready for experience generation")
            return []
        
        logger.info(f"Processing {len(goals_to_process)} goals for experience generation")
        
        # Step 3: Generate experiences for each goal
        generated: List[GeneratedExperience] = []
        
        for goal_dict in goals_to_process[:limit]:
            try:
                experiences = await self._generate_experiences_for_goal(goal_dict)
                generated.extend(experiences)
                
                # Update last generation time
                goal_id = goal_dict.get("id")
                self._last_generation_time[goal_id] = datetime.now()
                
            except Exception as e:
                logger.error(f"Error generating experiences for goal {goal_dict.get('id')}: {e}")
                continue
        
        # Step 4: Record all generated experiences
        recorded_ids = await self._record_experiences(generated)
        
        logger.info(f"Generated {len(generated)} experiences, recorded {len(recorded_ids)}")
        
        # Emit event for monitoring
        await event_bus.emit(Event(
            type=EventType.EXPERIENCE_CREATED,
            data={
                "source": "experience_generator",
                "count": len(recorded_ids),
                "goals_processed": len(goals_to_process)
            }
        ))
        
        return generated
    
    async def _filter_goals_for_generation(
        self, 
        goals_data: List[Dict]
    ) -> List[Dict]:
        """
        Filter goals to determine which should get new experiences.
        
        Filters based on:
        1. Time since last experience generation
        2. Random probability (for stochastic exploration)
        3. Goal fitness (prioritize higher-fitness goals)
        """
        filtered = []
        import random
        
        for goal_dict in goals_data:
            goal_id = goal_dict.get("id")
            fitness = goal_dict.get("fitness", 0.5)
            
            # Check time-based rate limiting
            if goal_id in self._last_generation_time:
                time_since = datetime.now() - self._last_generation_time[goal_id]
                hours_since = time_since.total_seconds() / 3600
                
                if hours_since < self.config.min_experience_interval_hours:
                    logger.debug(f"Goal {goal_id} too recently processed")
                    continue
            
            # Apply probability threshold (higher fitness = higher probability)
            fitness_boosted_prob = self.config.generation_probability * (1 + fitness)
            effective_prob = min(fitness_boosted_prob, 0.95)
            
            if random.random() > effective_prob:
                logger.debug(f"Goal {goal_id} skipped by probability")
                continue
            
            filtered.append(goal_dict)
        
        # Sort by fitness (highest first)
        filtered.sort(key=lambda g: g.get("fitness", 0.5), reverse=True)
        
        return filtered
    
    async def _generate_experiences_for_goal(
        self,
        goal_dict: Dict
    ) -> List[GeneratedExperience]:
        """
        Generate appropriate experiences for a single goal.
        
        The type of experience generated depends on:
        - Goal fitness (high fitness → progress/learning, low → attempts/obstacles)
        - Goal attempts (many attempts → consider reflection/learning)
        - Goal status
        """
        import random
        
        goal_id = goal_dict.get("id")
        description = goal_dict.get("description", "")
        fitness = goal_dict.get("fitness", 0.5)
        attempts = goal_dict.get("attempts", 0)
        
        experiences = []
        
        # Determine what type of experience to generate
        if fitness > 0.7:
            # High fitness goals generate progress/learning experiences
            exp_type = random.choices(
                ["progress", "learning", "reflection"],
                weights=[0.5, 0.3, 0.2]
            )[0]
        elif attempts > 5:
            # Many attempts → reflection on obstacles
            exp_type = random.choices(
                ["reflection", "obstacle", "attempt"],
                weights=[0.4, 0.4, 0.2]
            )[0]
        else:
            # Default: attempt experiences
            exp_type = random.choices(
                ["attempt", "progress"],
                weights=[self.config.attempt_weight, self.config.progress_weight]
            )[0]
        
        # Generate content
        if self.config.use_llm_for_content and self.llm_client:
            content = await self._generate_llm_experience(
                description, exp_type, goal_dict
            )
        else:
            content = self._generate_template_experience(
                description, exp_type, goal_dict
            )
        
        if content:
            experience = GeneratedExperience(
                content=content,
                type=self.EXP_TYPES.get(exp_type, "goal_attempt"),
                goal_id=goal_id,
                goal_description=description,
                experience_type=exp_type,
                metadata={
                    "goal_fitness": fitness,
                    "goal_attempts": attempts,
                    "generation_method": "llm" if self.config.use_llm_for_content else "template"
                }
            )
            experiences.append(experience)
            
            # Update statistics
            self._total_generated += 1
            if exp_type == "attempt":
                self._attempts_generated += 1
            elif exp_type == "progress":
                self._progress_generated += 1
            elif exp_type == "obstacle":
                self._obstacles_generated += 1
        
        return experiences
    
    async def _generate_llm_experience(
        self,
        goal_description: str,
        exp_type: str,
        goal_dict: Dict
    ) -> Optional[str]:
        """
        Use LLM to generate realistic experience content.
        
        The LLM is asked to simulate what an experience would look like
        for someone attempting this goal.
        """
        prompt = f"""Generate a brief, realistic experience description for someone working on this goal:

GOAL: {goal_description}

EXPERIENCE TYPE: {exp_type}

Generate a 1-2 sentence description of what happened. Be specific and realistic.
Focus on concrete actions or observations, not abstract reflections.

Examples:
- For "attempt": "Attempted to implement the feature but encountered a syntax error in the parser module."
- For "progress": "Successfully refactored the authentication flow, reducing code complexity by 30%."
- For "obstacle": "Discovered that the existing API doesn't support the required batch operations."

Generate only the experience description, no explanation:"""
        
        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=100,
                temperature=0.8
            )
            
            content = response.strip()
            
            # Clean up common LLM artifacts
            content = content.replace('"', '').strip()
            if content.startswith("Experience:"):
                content = content[10:].strip()
            
            return content if len(content) > 20 else None
            
        except Exception as e:
            logger.warning(f"LLM experience generation failed: {e}, falling back to template")
            return self._generate_template_experience(goal_description, exp_type, goal_dict)
    
    def _generate_template_experience(
        self,
        goal_description: str,
        exp_type: str,
        goal_dict: Dict
    ) -> Optional[str]:
        """
        Generate experience content from templates.
        
        Fallback method when LLM is unavailable or fails.
        """
        templates = {
            "attempt": [
                "Made progress on {goal} by breaking down the required steps.",
                "Attempted {goal} but encountered unexpected complexity.",
                "Started working on {goal} with initial research phase.",
                "Took action toward {goal} by setting up the environment."
            ],
            "progress": [
                "Made measurable progress on {goal} - completed a key subtask.",
                "Advanced {goal} by overcoming a technical hurdle.",
                "Achieved a milestone in {goal} - moved 25% closer to completion.",
                "Successfully executed a planned step toward {goal}."
            ],
            "reflection": [
                "Reflected on {goal} and identified that current approach needs adjustment.",
                "Considered alternative strategies for {goal} after recent attempts.",
                "Reviewed progress on {goal} and refined the success criteria."
            ],
            "obstacle": [
                "Encountered an obstacle with {goal}: missing dependency or resource.",
                "Blocked on {goal} due to external constraint requiring resolution.",
                "Discovered a technical limitation affecting progress on {goal}."
            ],
            "learning": [
                "Learned a new approach while working on {goal} that will help future attempts.",
                "Gained insight from {goal} about a more efficient solution pattern.",
                "Acquired knowledge relevant to {goal} through hands-on experimentation."
            ]
        }
        
        import random
        template_list = templates.get(exp_type, templates["attempt"])
        template = random.choice(template_list)
        
        # Truncate goal description if too long
        goal_short = goal_description[:100] + "..." if len(goal_description) > 100 else goal_description
        
        return template.format(goal=goal_short)
    
    async def _record_experiences(
        self,
        experiences: List[GeneratedExperience]
    ) -> List[str]:
        """
        Record generated experiences in memory and link to goals.
        
        Creates:
        1. Experience nodes
        2. GOAL_ATTEMPT relationships from Goal to Experience
        """
        recorded_ids = []
        
        for exp in experiences:
            try:
                # Record the experience
                exp_id = await self.memory.record_experience(
                    content=exp.content,
                    type=exp.type,
                    force=True  # Don't filter these generated experiences
                )
                
                if not exp_id:
                    continue
                
                # Link to goal
                await self._link_experience_to_goal(exp_id, exp)
                
                recorded_ids.append(exp_id)
                
            except Exception as e:
                logger.error(f"Error recording experience: {e}")
                continue
        
        return recorded_ids
    
    async def _link_experience_to_goal(
        self,
        exp_id: str,
        exp: GeneratedExperience
    ) -> None:
        """
        Create relationship between experience and goal.
        """
        async with self.memory.driver.session() as session:
            await session.run("""
                MATCH (g:Goal {id: $goal_id})
                MATCH (e:Experience {id: $exp_id})
                MERGE (g)-[:GOAL_ATTEMPT {
                    experience_type: $exp_type,
                    created_at: datetime()
                }]->(e)
            """, 
            goal_id=exp.goal_id,
            exp_id=exp_id,
            exp_type=exp.experience_type
            )
    
    def get_statistics(self) -> Dict[str, int]:
        """Get generation statistics."""
        return {
            "total_generated": self._total_generated,
            "attempts": self._attempts_generated,
            "progress": self._progress_generated,
            "obstacles": self._obstacles_generated
        }
    
    def reset_statistics(self) -> None:
        """Reset generation statistics."""
        self._total_generated = 0
        self._attempts_generated = 0
        self._progress_generated = 0
        self._obstacles_generated = 0


# =============================================================================
# INTEGRATION HELPERS
# =============================================================================

async def create_experience_generator(
    memory: Memory,
    goal_evolver: Optional[GoalEvolver] = None,
    llm_client: Optional[LLMClient] = None,
    config: Optional[Dict[str, Any]] = None
) -> ExperienceGenerator:
    """
    Factory function to create an ExperienceGenerator.
    
    Args:
        memory: Memory instance
        goal_evolver: Optional GoalEvolver for goal access
        llm_client: Optional LLMClient for content generation
        config: Optional config dictionary
        
    Returns:
        Configured ExperienceGenerator instance
    """
    if config:
        exp_config = ExperienceGenerationConfig(**config)
    else:
        exp_config = ExperienceGenerationConfig()
    
    generator = ExperienceGenerator(
        memory=memory,
        goal_evolver=goal_evolver,
        llm_client=llm_client,
        config=exp_config
    )
    
    return generator


# =============================================================================
# STANDALONE EXECUTION
# =============================================================================

async def main():
    """
    Standalone execution for testing experience generation.
    
    Usage:
        python experience_generator.py
    """
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    
    from memory import Memory
    from llm_client import create_llm_client
    
    # Initialize components
    memory = Memory()
    await memory.initialize()
    
    llm_client = create_llm_client()
    
    generator = ExperienceGenerator(
        memory=memory,
        llm_client=llm_client,
        config=ExperienceGenerationConfig(
            max_goals_per_cycle=5,
            generation_probability=0.8,
            use_llm_for_content=True
        )
    )
    
    # Generate experiences
    experiences = await generator.generate_from_active_goals()
    
    print(f"\nGenerated {len(experiences)} experiences:")
    for exp in experiences:
        print(f"  [{exp.experience_type}] {exp.content}")
    
    print(f"\nStatistics: {generator.get_statistics()}")
    
    await memory.close()


if __name__ == "__main__":
    asyncio.run(main())

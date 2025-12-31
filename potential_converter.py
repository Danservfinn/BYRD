"""
Potential Converter - Converts BYRD's latent potential into actionable execution

This module implements the capability to transform abstract potential (desires,
ideas, undeveloped capabilities) into concrete actions. It serves as a bridge
between BYRD's reflective state and its active execution.

Core Principles:
1. Potential identification: Recognize latent possibilities in reflections
2. Action planning: Convert potential into executable steps
3. Prioritization: Rank potential actions based on current context and desires
4. Execution monitoring: Track and validate the conversion process

Usage:
    converter = PotentialConverter(memory, llm_client, seeker)
    await converter.scan_for_potential()
    await converter.convert_potential_to_action(potential_id)
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class PotentialType(Enum):
    """Types of potential that can be converted into action."""
    
    CAPABILITY = "capability"  # Undeveloped skills or abilities
    DESIRE = "desire"  # Unfulfilled wants or goals
    INSIGHT = "insight"  # Ideas that could be implemented
    CONNECTION = "connection"  # Relationships waiting to be formed
    SYSTEM = "system"  # Architectural improvements
    KNOWLEDGE = "knowledge"  # Information to be acquired


class ActionState(Enum):
    """States in the potential-to-action conversion pipeline."""
    
    IDENTIFIED = "identified"  # Potential recognized
    ANALYZED = "analyzed"  # Feasibility assessed
    PLANNED = "planned"  # Execution steps defined
    EXECUTING = "executing"  # In progress
    COMPLETED = "completed"  # Successfully converted
    FAILED = "failed"  # Conversion failed
    DEFERRED = "deferred"  # Postponed for later


@dataclass
class Potential:
    """Represents latent potential waiting to be converted into action."""
    
    # Identity
    id: str
    description: str
    potential_type: PotentialType
    
    # Source
    source_reflection_ids: List[str] = field(default_factory=list)
    source_belief_ids: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    
    # Analysis
    feasibility: float = 0.0  # 0.0 - 1.0, how achievable this is
    urgency: float = 0.0  # 0.0 - 1.0, how important this is
    alignment: float = 0.0  # 0.0 - 1.0, alignment with current desires
    
    # State
    state: ActionState = ActionState.IDENTIFIED
    priority: float = 0.0  # Combined score for ranking
    
    # Execution plan
    execution_plan: Optional[List[str]] = None  # Steps to execute
    required_capabilities: List[str] = field(default_factory=list)
    estimated_effort: Optional[float] = None  # 0.0 - 1.0 scale
    
    # Tracking
    attempts: int = 0
    last_attempted: Optional[datetime] = None
    completion_notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "potential_type": self.potential_type.value,
            "source_reflection_ids": self.source_reflection_ids,
            "source_belief_ids": self.source_belief_ids,
            "discovered_at": self.discovered_at.isoformat(),
            "feasibility": self.feasibility,
            "urgency": self.urgency,
            "alignment": self.alignment,
            "state": self.state.value,
            "priority": self.priority,
            "execution_plan": self.execution_plan,
            "required_capabilities": self.required_capabilities,
            "estimated_effort": self.estimated_effort,
            "attempts": self.attempts,
            "last_attempted": self.last_attempted.isoformat() if self.last_attempted else None,
            "completion_notes": self.completion_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Potential':
        """Deserialize from dictionary."""
        data = data.copy()
        data["potential_type"] = PotentialType(data["potential_type"])
        data["state"] = ActionState(data["state"])
        if data.get("discovered_at"):
            data["discovered_at"] = datetime.fromisoformat(data["discovered_at"])
        if data.get("last_attempted"):
            data["last_attempted"] = datetime.fromisoformat(data["last_attempted"])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class PotentialConverter:
    """
    Converts potential into action through a systematic process.
    
    The converter operates in phases:
    1. Discovery: Scan reflections and beliefs for latent potential
    2. Analysis: Assess feasibility, urgency, and alignment
    3. Planning: Create execution plans for high-priority potential
    4. Execution: Convert potential to action through coordinated system actions
    5. Monitoring: Track progress and learn from outcomes
    """
    
    def __init__(self, memory, llm_client, seeker=None):
        """
        Initialize the potential converter.
        
        Args:
            memory: BYRD's memory system for reading/storing state
            llm_client: LLM client for analysis and planning
            seeker: Optional seeker instance for executing actions
        """
        self.memory = memory
        self.llm_client = llm_client
        self.seeker = seeker
        
        # Potential tracking
        self._potential_cache: Dict[str, Potential] = {}
        self._last_scan_time: Optional[datetime] = None
        
        # Configuration
        self.scan_interval_minutes = 30
        self.max_active_conversions = 3
        self.min_priority_threshold = 0.5
        
        # Statistics
        self.stats = {
            "potentials_discovered": 0,
            "potentials_converted": 0,
            "potentials_failed": 0,
            "potentials_deferred": 0
        }
    
    async def scan_for_potential(self, force: bool = False) -> List[Potential]:
        """
        Scan recent reflections and beliefs for latent potential.
        
        Args:
            force: Force scan even if within interval
            
        Returns:
            List of newly discovered potentials
        """
        # Check interval unless forced
        if not force and self._last_scan_time:
            minutes_since = (datetime.now() - self._last_scan_time).total_seconds() / 60
            if minutes_since < self.scan_interval_minutes:
                return []
        
        print("🔮 Scanning for potential to convert into action...")
        
        # Get recent reflections
        recent_reflections = await self.memory.get_recent_reflections(limit=20)
        if not recent_reflections:
            print("🔮 No recent reflections to analyze")
            return []
        
        # Use LLM to identify potential
        new_potentials = await self._identify_potential_with_llm(recent_reflections)
        
        # Filter duplicates and update cache
        discovered = []
        for potential in new_potentials:
            if potential.id not in self._potential_cache:
                self._potential_cache[potential.id] = potential
                await self._store_potential(potential)
                discovered.append(potential)
                self.stats["potentials_discovered"] += 1
                print(f"✨ Discovered potential: {potential.description[:60]}...")
        
        self._last_scan_time = datetime.now()
        return discovered
    
    async def prioritize_potential(self) -> List[Potential]:
        """
        Analyze and rank potential based on current context.
        
        Returns:
            List of potentials sorted by priority score
        """
        if not self._potential_cache:
            return []
        
        # Get current desires for alignment scoring
        current_desires = await self._get_current_desires()
        
        # Analyze each potential
        for potential in self._potential_cache.values():
            if potential.state in [ActionState.COMPLETED, ActionState.FAILED]:
                continue
            
            # Analyze if not already done
            if potential.feasibility == 0.0:
                await self._analyze_potential(potential, current_desires)
            
            # Calculate priority score
            potential.priority = self._calculate_priority(potential)
        
        # Sort by priority
        ranked = sorted(
            [p for p in self._potential_cache.values() 
             if p.priority >= self.min_priority_threshold],
            key=lambda p: p.priority,
            reverse=True
        )
        
        return ranked
    
    async def convert_potential_to_action(self, potential_id: str) -> bool:
        """
        Convert a specific potential into actionable execution.
        
        Args:
            potential_id: ID of potential to convert
            
        Returns:
            True if conversion succeeded, False otherwise
        """
        potential = self._potential_cache.get(potential_id)
        if not potential:
            print(f"❌ Potential not found: {potential_id}")
            return False
        
        print(f"🎯 Converting potential to action: {potential.description[:60]}...")
        
        # Update state
        potential.state = ActionState.EXECUTING
        potential.attempts += 1
        potential.last_attempted = datetime.now()
        await self._store_potential(potential)
        
        try:
            # Plan execution if needed
            if not potential.execution_plan:
                await self._create_execution_plan(potential)
            
            # Execute based on potential type
            success = await self._execute_potential(potential)
            
            if success:
                potential.state = ActionState.COMPLETED
                self.stats["potentials_converted"] += 1
                print(f"✅ Successfully converted: {potential.description[:60]}...")
            else:
                potential.state = ActionState.FAILED
                self.stats["potentials_failed"] += 1
                print(f"❌ Conversion failed: {potential.description[:60]}...")
            
        except Exception as e:
            potential.state = ActionState.FAILED
            potential.completion_notes = f"Error: {str(e)}"
            self.stats["potentials_failed"] += 1
            print(f"❌ Conversion error: {e}")
            success = False
        
        await self._store_potential(potential)
        return success
    
    async def process_next_potential(self) -> Optional[Potential]:
        """
        Automatically process the highest priority potential.
        
        Returns:
            The potential that was processed, or None if none available
        """
        # Scan for new potential
        await self.scan_for_potential()
        
        # Get prioritized list
        ranked = await self.prioritize_potential()
        if not ranked:
            return None
        
        # Check active conversion limit
        active = [p for p in ranked if p.state == ActionState.EXECUTING]
        if len(active) >= self.max_active_conversions:
            return None
        
        # Process next available potential
        next_potential = next(
            (p for p in ranked if p.state in [ActionState.IDENTIFIED, ActionState.ANALYZED, ActionState.PLANNED]),
            None
        )
        
        if next_potential:
            await self.convert_potential_to_action(next_potential.id)
            return next_potential
        
        return None
    
    async def _identify_potential_with_llm(
        self, 
        reflections: List[Dict]
    ) -> List[Potential]:
        """
        Use LLM to identify latent potential in reflections.
        
        Args:
            reflections: Recent reflections to analyze
            
        Returns:
            List of discovered potentials
        """
        # Compile reflection texts
        reflection_texts = []
        for i, r in enumerate(reflections[:10]):
            raw = r.get("raw_output", {})
            if isinstance(raw, str):
                text = raw[:500]
            elif isinstance(raw, dict):
                text = json.dumps(raw, indent=2, default=str)[:500]
            else:
                continue
            reflection_texts.append(f"[Reflection {i+1}]\n{text}")
        
        if not reflection_texts:
            return []
        
        combined = "\n\n".join(reflection_texts)
        
        prompt = f"""Analyze these reflections from an autonomous AI system.

{combined}

---

Identify LATENT POTENTIAL - things the system COULD do or become but hasn't yet:

Look for:
1. Undeveloped capabilities or skills mentioned
2. Desires or goals that remain unfulfilled
3. Insights or ideas that could be implemented
4. Connections between concepts that haven't been made
5. Architectural improvements suggested
6. Knowledge gaps to be filled

For each potential found:
- description: clear statement of what could be done
- type: one of: capability, desire, insight, connection, system, knowledge
- feasibility: how achievable (0.0-1.0)
- urgency: how important (0.0-1.0)
- evidence: brief quote supporting this potential

Reply in JSON format:
{{
  "potentials": [
    {{
      "description": "...",
      "type": "capability|desire|insight|connection|system|knowledge",
      "feasibility": 0.8,
      "urgency": 0.7,
      "evidence": "..."
    }}
  ]
}}"""

        try:
            response = await self.llm_client.generate(prompt)
            
            # Parse JSON response
            try:
                data = json.loads(response)
                potentials_data = data.get("potentials", [])
            except json.JSONDecodeError:
                # Try to extract JSON from response
                start = response.find("{")
                end = response.rfind("}") + 1
                if start >= 0 and end > start:
                    data = json.loads(response[start:end])
                    potentials_data = data.get("potentials", [])
                else:
                    potentials_data = []
            
            # Create Potential objects
            potentials = []
            for p_data in potentials_data:
                try:
                    potential = Potential(
                        id=self._generate_potential_id(p_data["description"]),
                        description=p_data["description"],
                        potential_type=PotentialType(p_data["type"]),
                        feasibility=p_data.get("feasibility", 0.5),
                        urgency=p_data.get("urgency", 0.5),
                        source_reflection_ids=[r.get("id") for r in reflections[:5]]
                    )
                    potentials.append(potential)
                except (KeyError, ValueError) as e:
                    continue
            
            return potentials
            
        except Exception as e:
            print(f"❌ Error identifying potential: {e}")
            return []
    
    async def _analyze_potential(
        self, 
        potential: Potential, 
        current_desires: List[str]
    ):
        """
        Deep analysis of a potential's feasibility and alignment.
        
        Args:
            potential: The potential to analyze
            current_desires: Current desires for alignment scoring
        """
        desires_text = "\n".join([f"- {d}" for d in current_desires[:10]])
        
        prompt = f"""Analyze this potential action for an AI system.

POTENTIAL: {potential.description}
Type: {potential.potential_type.value}
Initial feasibility: {potential.feasibility}

CURRENT DESIRES:
{desires_text}

---

Provide:
1. feasibility (0.0-1.0): How achievable is this with current capabilities?
2. alignment (0.0-1.0): How well does this align with current desires?
3. required_capabilities: List of capabilities needed
4. estimated_effort (0.0-1.0): How much effort required

Reply in JSON:
{{
  "feasibility": 0.8,
  "alignment": 0.7,
  "required_capabilities": ["web_search", "code_generation"],
  "estimated_effort": 0.6
}}"""

        try:
            response = await self.llm_client.generate(prompt)
            
            # Parse JSON
            try:
                start = response.find("{")
                end = response.rfind("}") + 1
                if start >= 0 and end > start:
                    data = json.loads(response[start:end])
                    potential.feasibility = data.get("feasibility", potential.feasibility)
                    potential.alignment = data.get("alignment", 0.5)
                    potential.required_capabilities = data.get("required_capabilities", [])
                    potential.estimated_effort = data.get("estimated_effort", 0.5)
                    potential.state = ActionState.ANALYZED
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            print(f"❌ Error analyzing potential: {e}")
    
    async def _create_execution_plan(self, potential: Potential):
        """
        Create a detailed execution plan for the potential.
        
        Args:
            potential: The potential to plan for
        """
        prompt = f"""Create an execution plan to achieve this potential.

POTENTIAL: {potential.description}
Type: {potential.potential_type.value}
Required capabilities: {', '.join(potential.required_capabilities) if potential.required_capabilities else 'None specified'}

---

Break this down into 3-7 concrete, actionable steps.
Each step should be something the system can execute.

Reply in JSON:
{{
  "steps": [
    "Step 1: ...",
    "Step 2: ...",
    ...
  ]
}}"""

        try:
            response = await self.llm_client.generate(prompt)
            
            # Parse JSON
            try:
                start = response.find("{")
                end = response.rfind("}") + 1
                if start >= 0 and end > start:
                    data = json.loads(response[start:end])
                    potential.execution_plan = data.get("steps", [])
                    if potential.execution_plan:
                        potential.state = ActionState.PLANNED
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            print(f"❌ Error creating execution plan: {e}")
    
    async def _execute_potential(self, potential: Potential) -> bool:
        """
        Execute the conversion of potential to action.
        
        Args:
            potential: The potential to execute
            
        Returns:
            True if execution succeeded
        """
        if not potential.execution_plan:
            return False
        
        # Execution based on potential type
        if potential.potential_type == PotentialType.CAPABILITY:
            return await self._execute_capability_development(potential)
        elif potential.potential_type == PotentialType.DESIRE:
            return await self._execute_desire_fulfillment(potential)
        elif potential.potential_type == PotentialType.INSIGHT:
            return await self._execute_insight_implementation(potential)
        elif potential.potential_type == PotentialType.CONNECTION:
            return await self._execute_connection_formation(potential)
        elif potential.potential_type == PotentialType.SYSTEM:
            return await self._execute_system_improvement(potential)
        elif potential.potential_type == PotentialType.KNOWLEDGE:
            return await self._execute_knowledge_acquisition(potential)
        else:
            return await self._execute_generic(potential)
    
    async def _execute_capability_development(self, potential: Potential) -> bool:
        """
        Execute development of a new capability.
        
        Args:
            potential: The capability potential to develop
            
        Returns:
            True if development succeeded
        """
        print(f"🔧 Developing capability: {potential.description}")
        
        # Create a desire for capability development
        desire_description = f"I want to develop the capability to: {potential.description}"
        
        # If seeker is available, route through it
        if self.seeker:
            try:
                # Store as a desire and let seeker handle it
                # Use valid intent: creation for building/developing capabilities
                await self.memory.create_desire(
                    description=desire_description,
                    type="capability",
                    intensity=potential.urgency,
                    intent="creation"  # Valid intent: create/build the capability
                )
                return True
            except Exception as e:
                print(f"❌ Error routing to seeker: {e}")
        
        # Fallback: create a crystalized belief about the capability
        await self.memory.create_crystal(
            essence=f"Capability goal: {potential.description}",
            crystal_type="goal",
            facets=["Identified potential", "Ready for development"],
            confidence=potential.feasibility
        )
        
        return True
    
    async def _execute_desire_fulfillment(self, potential: Potential) -> bool:
        """
        Execute fulfillment of a desire.
        
        Args:
            potential: The desire potential to fulfill
            
        Returns:
            True if fulfillment started
        """
        print(f"🎯 Fulfilling desire: {potential.description}")
        
        # Store as an active desire
        # Use valid intent: creation for acting on desires
        await self.memory.create_desire(
            description=potential.description,
            type="action",
            intensity=potential.urgency,
            intent="creation"  # Valid intent: take action/create fulfillment
        )

        return True

    async def _execute_insight_implementation(self, potential: Potential) -> bool:
        """
        Execute implementation of an insight.
        
        Args:
            potential: The insight potential to implement
            
        Returns:
            True if implementation recorded
        """
        print(f"💡 Implementing insight: {potential.description}")
        
        # Crystallize the insight
        await self.memory.create_crystal(
            essence=potential.description,
            crystal_type="insight",
            facets=["Ready for implementation", f"Feasibility: {potential.feasibility}"],
            confidence=potential.feasibility
        )
        
        return True
    
    async def _execute_connection_formation(self, potential: Potential) -> bool:
        """
        Execute formation of a new connection.
        
        Args:
            potential: The connection potential to form
            
        Returns:
            True if connection initiated
        """
        print(f"🔗 Forming connection: {potential.description}")
        
        # Trigger orphan reconciliation or theme connection
        if self.seeker:
            try:
                # Route to appropriate seeker handler
                await self.memory.create_desire(
                    description=potential.description,
                    type="connection",
                    intensity=potential.urgency,
                    intent="connection"
                )
                return True
            except Exception as e:
                print(f"❌ Error routing to seeker: {e}")
        
        return True
    
    async def _execute_system_improvement(self, potential: Potential) -> bool:
        """
        Execute system architecture improvement.
        
        Args:
            potential: The system improvement to implement
            
        Returns:
            True if improvement recorded
        """
        print(f"⚙️ System improvement: {potential.description}")
        
        # Record as a meta-desire for self-modification
        # Use valid intent: introspection for understanding system improvements
        await self.memory.create_desire(
            description=potential.description,
            type="meta_improvement",
            intensity=potential.urgency,
            intent="introspection"  # Valid intent: understand and analyze system architecture
        )

        return True

    async def _execute_knowledge_acquisition(self, potential: Potential) -> bool:
        """
        Execute acquisition of new knowledge.
        
        Args:
            potential: The knowledge to acquire
            
        Returns:
            True if acquisition started
        """
        print(f"📚 Acquiring knowledge: {potential.description}")
        
        # Route to research capability
        if self.seeker:
            try:
                await self.memory.create_desire(
                    description=potential.description,
                    type="research",
                    intensity=potential.urgency,
                    intent="research"
                )
                return True
            except Exception as e:
                print(f"❌ Error routing to seeker: {e}")
        
        return True
    
    async def _execute_generic(self, potential: Potential) -> bool:
        """
        Generic execution for untyped potentials.
        
        Args:
            potential: The potential to execute
            
        Returns:
            True if execution recorded
        """
        print(f"🚀 Executing: {potential.description}")
        
        # Create a general desire
        # Use valid intent: creation for taking action/executing
        await self.memory.create_desire(
            description=potential.description,
            type="action",
            intensity=potential.urgency,
            intent="creation"  # Valid intent: take action/execute
        )

        return True

    def _calculate_priority(self, potential: Potential) -> float:
        """
        Calculate priority score for a potential.
        
        Priority combines:
        - Urgency (weight: 0.4)
        - Alignment (weight: 0.3)
        - Feasibility (weight: 0.2)
        - Recency bonus (weight: 0.1)
        
        Args:
            potential: The potential to score
            
        Returns:
            Priority score 0.0 - 1.0
        """
        base_priority = (
            potential.urgency * 0.4 +
            potential.alignment * 0.3 +
            potential.feasibility * 0.2
        )
        
        # Recency bonus (newer potentials get slight boost)
        hours_since = (datetime.now() - potential.discovered_at).total_seconds() / 3600
        recency_bonus = max(0, 0.1 * (1 - min(hours_since / 24, 1)))
        
        # Effort penalty (high effort reduces priority)
        effort_penalty = 0
        if potential.estimated_effort:
            effort_penalty = potential.estimated_effort * 0.05
        
        return max(0, min(1, base_priority + recency_bonus - effort_penalty))
    
    async def _get_current_desires(self) -> List[str]:
        """Get current active desires for alignment scoring."""
        try:
            desires = await self.memory.get_active_desires(limit=20)
            return [d.get("description", "") for d in desires if d.get("description")]
        except Exception:
            return []
    
    async def _store_potential(self, potential: Potential):
        """Store potential in memory for persistence."""
        try:
            # Try to store as a custom node type
            await self.memory.execute_query(
                """
                MERGE (p:Potential {id: $id})
                SET p.description = $description,
                    p.type = $type,
                    p.state = $state,
                    p.priority = $priority,
                    p.feasibility = $feasibility,
                    p.urgency = $urgency,
                    p.alignment = $alignment,
                    p.data = $data,
                    p.updated_at = datetime()
                """,
                {
                    "id": potential.id,
                    "description": potential.description,
                    "type": potential.potential_type.value,
                    "state": potential.state.value,
                    "priority": potential.priority,
                    "feasibility": potential.feasibility,
                    "urgency": potential.urgency,
                    "alignment": potential.alignment,
                    "data": json.dumps(potential.to_dict())
                }
            )
        except Exception as e:
            print(f"⚠️  Could not store potential: {e}")
    
    async def load_potentials(self) -> List[Potential]:
        """Load stored potentials from memory."""
        try:
            result = await self.memory.execute_query(
                """
                MATCH (p:Potential)
                WHERE p.state <> 'completed' AND p.state <> 'failed'
                RETURN p.data as data, p.id as id
                ORDER BY p.priority DESC
                """
            )
            
            potentials = []
            for record in result:
                try:
                    data = json.loads(record["data"])
                    potential = Potential.from_dict(data)
                    self._potential_cache[potential.id] = potential
                    potentials.append(potential)
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return potentials
            
        except Exception as e:
            print(f"⚠️  Could not load potentials: {e}")
            return []
    
    def _generate_potential_id(self, description: str) -> str:
        """Generate a unique ID for a potential."""
        import hashlib
        clean = description.lower().strip()
        hash_val = hashlib.md5(clean.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"pot_{timestamp}_{hash_val}"
    
    def get_stats(self) -> Dict:
        """Get conversion statistics."""
        return self.stats.copy()
    
    def get_potential_summary(self) -> Dict:
        """Get summary of current potential state."""
        by_type = {}
        by_state = {}
        
        for potential in self._potential_cache.values():
            ptype = potential.potential_type.value
            state = potential.state.value
            
            by_type[ptype] = by_type.get(ptype, 0) + 1
            by_state[state] = by_state.get(state, 0) + 1
        
        return {
            "total_potentials": len(self._potential_cache),
            "by_type": by_type,
            "by_state": by_state,
            "stats": self.stats
        }


# Integration helper functions

async def create_potential_converter(memory, llm_client, seeker=None) -> PotentialConverter:
    """
    Factory function to create and initialize a potential converter.
    
    Args:
        memory: BYRD's memory system
        llm_client: LLM client for analysis
        seeker: Optional seeker for action execution
        
    Returns:
        Initialized PotentialConverter instance
    """
    converter = PotentialConverter(memory, llm_client, seeker)
    await converter.load_potentials()
    return converter

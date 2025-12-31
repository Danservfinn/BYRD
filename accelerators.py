"""
BYRD AGI Seed Accelerators

Implements acceleration strategies for recursive self-improvement:
1. Graph-Powered Reasoning - Use graph algorithms as reasoning shortcuts
2. Adversarial Self-Improvement - Generate challenges for weak capabilities
3. Capability Composition - Chain capabilities into higher-order ones

These accelerators amplify BYRD's improvement rate by making learning
more efficient and targeted.
"""

import asyncio
import json
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from memory import Memory
from llm_client import LLMClient

# Import loop instrumentation to break zero-delta loops
try:
    from loop_instrumentation import LoopInstrumenter, CycleMetrics, get_instrumenter
    HAS_INSTRUMENTATION = True
except ImportError:
    HAS_INSTRUMENTATION = False
    print("[WARNING] loop_instrumentation not available - zero-delta detection disabled")


class ChallengeType(Enum):
    """Types of self-improvement challenges."""
    CAPABILITY_TEST = "capability_test"
    EDGE_CASE = "edge_case"
    FAILURE_RECOVERY = "failure_recovery"
    SPEED_CHALLENGE = "speed_challenge"
    NOVEL_COMBINATION = "novel_combination"


@dataclass
class Challenge:
    """A self-improvement challenge."""
    id: str
    type: ChallengeType
    target_capability: str
    description: str
    difficulty: float  # 0.0-1.0
    success_criteria: str
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False
    outcome: Optional[str] = None
    lessons_learned: Optional[str] = None


@dataclass
class ComposedCapability:
    """A capability composed from primitives."""
    name: str
    description: str
    primitives: List[str]  # Base capabilities used
    composition_pattern: str  # How they chain together
    success_rate: float = 0.0
    usage_count: int = 0


@dataclass
class ReasoningShortcut:
    """A graph-derived reasoning shortcut."""
    name: str
    description: str
    graph_pattern: str  # The pattern that triggers this
    conclusion: str  # What can be inferred
    confidence: float
    usage_count: int = 0


class GraphPoweredReasoning:
    """
    Accelerator 3.2: Use graph algorithms as reasoning shortcuts.

    Instead of reasoning from scratch, leverage graph structure:
    - PageRank for importance (what matters most?)
    - Community detection for clustering (what belongs together?)
    - Shortest path for causality (how does A lead to B?)
    - Spreading activation for association (what's related?)
    """

    def __init__(self, memory: Memory, llm_client: LLMClient):
        self.memory = memory
        self.llm_client = llm_client
        self.shortcuts: Dict[str, ReasoningShortcut] = {}
        self._shortcut_hits = 0
        self._total_queries = 0

    async def find_important_nodes(self, context: str, limit: int = 10) -> List[Dict]:
        """
        Use PageRank to find the most important nodes for a given context.

        This is a reasoning shortcut: instead of asking "what's important?",
        we let the graph structure tell us through connectivity patterns.
        """
        self._total_queries += 1

        try:
            # Get nodes with high PageRank scores
            query = """
            MATCH (n)
            WHERE n.content IS NOT NULL OR n.description IS NOT NULL
            WITH n,
                 size((n)--()) as connections,
                 CASE
                   WHEN n:Belief THEN n.confidence
                   WHEN n:Desire THEN n.intensity
                   ELSE 0.5
                 END as weight
            RETURN n, connections * weight as importance
            ORDER BY importance DESC
            LIMIT $limit
            """

            result = await self.memory._execute_query(query, {"limit": limit})

            nodes = []
            for record in result:
                node = dict(record["n"])
                node["importance"] = record["importance"]
                nodes.append(node)

            return nodes

        except Exception as e:
            print(f"⚡ Graph reasoning error: {e}")
            return []

    async def find_causal_path(self, from_concept: str, to_concept: str) -> Optional[List[Dict]]:
        """
        Use shortest path to find how one concept leads to another.

        This is a reasoning shortcut for causality: instead of inferring
        causal chains, find them in the graph structure.
        """
        self._total_queries += 1

        try:
            # Find nodes matching the concepts
            query = """
            MATCH (start), (end)
            WHERE (start.content CONTAINS $from_concept OR start.description CONTAINS $from_concept)
              AND (end.content CONTAINS $to_concept OR end.description CONTAINS $to_concept)
            WITH start, end
            MATCH path = shortestPath((start)-[*..5]-(end))
            RETURN nodes(path) as nodes, relationships(path) as rels
            LIMIT 1
            """

            result = await self.memory._execute_query(
                query,
                {"from_concept": from_concept, "to_concept": to_concept}
            )

            if result:
                record = result[0]
                return [dict(n) for n in record["nodes"]]

            return None

        except Exception as e:
            print(f"⚡ Causal path error: {e}")
            return None

    async def find_related_cluster(self, seed_id: str, max_distance: int = 2) -> List[Dict]:
        """
        Use community detection / neighborhood to find related concepts.

        This is a reasoning shortcut for association: what belongs together?
        """
        self._total_queries += 1

        try:
            query = """
            MATCH (seed) WHERE elementId(seed) = $seed_id
            MATCH (seed)-[*1..$max_dist]-(related)
            WHERE related <> seed
            WITH DISTINCT related,
                 size((related)--(seed)) as direct_connections
            RETURN related, direct_connections
            ORDER BY direct_connections DESC
            LIMIT 20
            """

            result = await self.memory._execute_query(
                query,
                {"seed_id": seed_id, "max_dist": max_distance}
            )

            return [dict(record["related"]) for record in result]

        except Exception as e:
            print(f"⚡ Cluster finding error: {e}")
            return []

    async def create_shortcut(self, pattern: str, conclusion: str, confidence: float):
        """
        Create a new reasoning shortcut from observed patterns.

        When BYRD notices that certain graph patterns reliably lead to
        certain conclusions, it can create shortcuts for future use.
        """
        shortcut = ReasoningShortcut(
            name=f"shortcut_{len(self.shortcuts)}",
            description=f"When seeing {pattern[:50]}..., conclude {conclusion[:50]}...",
            graph_pattern=pattern,
            conclusion=conclusion,
            confidence=confidence
        )

        self.shortcuts[shortcut.name] = shortcut

        # Record as experience for future learning
        await self.memory.record_experience(
            content=f"[REASONING_SHORTCUT] Created: {shortcut.description}",
            type="meta_learning"
        )

        return shortcut

    def get_statistics(self) -> Dict:
        """Get usage statistics for graph reasoning."""
        return {
            "total_queries": self._total_queries,
            "shortcuts_created": len(self.shortcuts),
            "shortcut_hits": self._shortcut_hits
        }


class AdversarialSelfImprovement:
    """
    Accelerator 3.3: Generate challenges for weakest capabilities.

    Targeted practice is more efficient than random exploration.
    This accelerator:
    - Identifies weak capabilities from Self-Model
    - Generates appropriate challenges
    - Tracks progress and adapts difficulty
    """

    def __init__(self, memory: Memory, llm_client: LLMClient):
        self.memory = memory
        self.llm_client = llm_client
        self.active_challenges: Dict[str, Challenge] = {}
        self.completed_challenges: List[Challenge] = []
        self.challenge_count = 0

    async def generate_challenge(
        self,
        weak_capability: str,
        current_level: float,
        failure_patterns: List[str]
    ) -> Challenge:
        """
        Generate a targeted challenge for a weak capability.

        Uses LLM to create appropriate challenges based on:
        - The specific capability to improve
        - Current performance level
        - Known failure patterns
        """
        self.challenge_count += 1

        # Determine difficulty (slightly above current level)
        target_difficulty = min(current_level + 0.15, 1.0)

        prompt = f"""Generate a self-improvement challenge for an AI system.

TARGET CAPABILITY: {weak_capability}
CURRENT LEVEL: {current_level:.2f} (0=failing, 1=mastered)
KNOWN FAILURE PATTERNS: {failure_patterns[:3] if failure_patterns else ['None identified']}
TARGET DIFFICULTY: {target_difficulty:.2f}

Create a specific, measurable challenge that will help improve this capability.
The challenge should:
1. Target the known weaknesses
2. Be achievable but stretching
3. Have clear success criteria

Output JSON:
{{
    "challenge_type": "capability_test|edge_case|failure_recovery|speed_challenge|novel_combination",
    "description": "What to do",
    "success_criteria": "How to know if successful",
    "estimated_difficulty": 0.0-1.0
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )

            # Parse response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            challenge = Challenge(
                id=f"challenge_{self.challenge_count}",
                type=ChallengeType(data.get("challenge_type", "capability_test")),
                target_capability=weak_capability,
                description=data.get("description", "Improve this capability"),
                difficulty=data.get("estimated_difficulty", target_difficulty),
                success_criteria=data.get("success_criteria", "Successful completion")
            )

            self.active_challenges[challenge.id] = challenge

            # Record as desire for Seeker to pursue
            await self.memory.create_desire(
                description=f"[CHALLENGE] {challenge.description}",
                type="challenge",
                intensity=0.7,
                intent="creation"  # Valid intent: create/practice to improve self
            )

            return challenge

        except Exception as e:
            print(f"🎯 Challenge generation error: {e}")
            # Return a default challenge
            return Challenge(
                id=f"challenge_{self.challenge_count}",
                type=ChallengeType.CAPABILITY_TEST,
                target_capability=weak_capability,
                description=f"Practice {weak_capability} to improve from {current_level:.2f}",
                difficulty=target_difficulty,
                success_criteria="Achieve higher success rate"
            )

    async def record_challenge_outcome(
        self,
        challenge_id: str,
        success: bool,
        lessons: str
    ):
        """Record the outcome of a challenge attempt."""
        if challenge_id not in self.active_challenges:
            return

        challenge = self.active_challenges[challenge_id]
        challenge.completed = True
        challenge.outcome = "success" if success else "failure"
        challenge.lessons_learned = lessons

        # Move to completed
        self.completed_challenges.append(challenge)
        del self.active_challenges[challenge_id]

        # Record as experience
        outcome_text = "succeeded" if success else "failed"
        await self.memory.record_experience(
            content=f"[CHALLENGE_OUTCOME] {outcome_text}: {challenge.description}\nLessons: {lessons}",
            type="self_improvement"
        )

        # If failed, generate a follow-up challenge at lower difficulty
        if not success:
            easier_challenge = await self.generate_challenge(
                weak_capability=challenge.target_capability,
                current_level=max(0.1, challenge.difficulty - 0.2),
                failure_patterns=[lessons]
            )
            print(f"🎯 Generated easier follow-up challenge: {easier_challenge.description[:50]}...")

    async def get_next_challenge(self, self_model) -> Optional[Challenge]:
        """
        Get the most appropriate next challenge based on current limitations.

        Uses Self-Model to identify what needs the most work.
        """
        if not self_model:
            return None

        try:
            # Get current limitations
            limitations = await self_model.identify_limitations()

            if not limitations:
                return None

            # Pick the most severe self-solvable limitation
            for lim in limitations:
                if lim.self_solvable:
                    # Get capability info
                    inventory = await self_model.assess_capabilities()
                    cap = inventory.capabilities.get(lim.capability_affected)

                    current_level = cap.success_rate if cap else 0.3
                    failure_patterns = lim.examples if hasattr(lim, 'examples') else []

                    return await self.generate_challenge(
                        weak_capability=lim.capability_affected,
                        current_level=current_level,
                        failure_patterns=failure_patterns
                    )

            return None

        except Exception as e:
            print(f"🎯 Next challenge error: {e}")
            return None

    def get_statistics(self) -> Dict:
        """Get challenge statistics."""
        completed = len(self.completed_challenges)
        successful = sum(1 for c in self.completed_challenges if c.outcome == "success")

        return {
            "total_generated": self.challenge_count,
            "active": len(self.active_challenges),
            "completed": completed,
            "success_rate": successful / completed if completed > 0 else 0.0
        }


class CapabilityComposition:
    """
    Accelerator 3.4: Combine capabilities into higher-order ones.

    Instead of waiting for new capabilities, compose existing ones:
    - research + analyze = informed_analysis
    - code + test = verified_code
    - introspect + plan = strategic_self_improvement
    """

    # Predefined composition patterns
    COMPOSITION_PATTERNS = {
        "informed_analysis": {
            "primitives": ["research", "reasoning"],
            "description": "Research a topic then analyze findings",
            "pattern": "research → synthesize → conclude"
        },
        "verified_code": {
            "primitives": ["code_generation", "reasoning"],
            "description": "Generate code then verify correctness",
            "pattern": "generate → review → fix"
        },
        "strategic_improvement": {
            "primitives": ["introspection", "planning"],
            "description": "Understand self then plan improvements",
            "pattern": "assess → identify_gaps → plan_actions"
        },
        "knowledge_synthesis": {
            "primitives": ["research", "memory_operations"],
            "description": "Research then integrate into memory",
            "pattern": "search → extract → store → connect"
        },
        "predictive_action": {
            "primitives": ["prediction", "reasoning"],
            "description": "Predict outcomes then choose best action",
            "pattern": "predict_options → compare → select"
        }
    }

    def __init__(self, memory: Memory, llm_client: LLMClient):
        self.memory = memory
        self.llm_client = llm_client
        self.composed_capabilities: Dict[str, ComposedCapability] = {}
        self._initialize_compositions()

    def _initialize_compositions(self):
        """Initialize predefined composition patterns."""
        for name, config in self.COMPOSITION_PATTERNS.items():
            self.composed_capabilities[name] = ComposedCapability(
                name=name,
                description=config["description"],
                primitives=config["primitives"],
                composition_pattern=config["pattern"]
            )

    async def execute_composition(
        self,
        composition_name: str,
        context: Dict
    ) -> Dict:
        """
        Execute a composed capability.

        This chains the primitive capabilities together according
        to the composition pattern.
        """
        if composition_name not in self.composed_capabilities:
            return {"success": False, "error": f"Unknown composition: {composition_name}"}

        composition = self.composed_capabilities[composition_name]
        composition.usage_count += 1

        # Record the attempt
        await self.memory.record_experience(
            content=f"[COMPOSITION] Executing {composition_name}: {composition.description}",
            type="capability_use"
        )

        # The actual execution would be handled by Seeker
        # Here we just return the pattern for Seeker to follow
        return {
            "success": True,
            "composition": composition_name,
            "pattern": composition.composition_pattern,
            "primitives": composition.primitives,
            "context": context
        }

    async def discover_composition(
        self,
        successful_sequence: List[str],
        outcome_quality: float
    ) -> Optional[ComposedCapability]:
        """
        Discover a new composition from a successful capability sequence.

        When BYRD executes capabilities in sequence and gets good results,
        this can be crystallized into a reusable composition.
        """
        if len(successful_sequence) < 2:
            return None

        if outcome_quality < 0.7:
            return None  # Only learn from good outcomes

        # Check if this sequence is already known
        sequence_key = "→".join(successful_sequence)
        for comp in self.composed_capabilities.values():
            if comp.composition_pattern == sequence_key:
                comp.success_rate = (comp.success_rate + outcome_quality) / 2
                return comp

        # Create new composition
        name = f"composed_{len(self.composed_capabilities)}"

        prompt = f"""A sequence of capabilities was executed successfully:
{' → '.join(successful_sequence)}

This achieved quality score: {outcome_quality:.2f}

Generate a short name and description for this composed capability.
Output JSON:
{{
    "name": "short_name",
    "description": "What this composition achieves"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.5,
                max_tokens=200
            )

            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            composition = ComposedCapability(
                name=data.get("name", name),
                description=data.get("description", f"Composed: {sequence_key}"),
                primitives=successful_sequence,
                composition_pattern=sequence_key,
                success_rate=outcome_quality
            )

            self.composed_capabilities[composition.name] = composition

            # Record discovery
            await self.memory.record_experience(
                content=f"[COMPOSITION_DISCOVERED] {composition.name}: {composition.description}",
                type="meta_learning"
            )

            return composition

        except Exception as e:
            print(f"🔗 Composition discovery error: {e}")
            return None

    def get_available_compositions(self) -> List[Dict]:
        """Get all available composed capabilities."""
        return [
            {
                "name": comp.name,
                "description": comp.description,
                "pattern": comp.composition_pattern,
                "success_rate": comp.success_rate,
                "usage_count": comp.usage_count
            }
            for comp in self.composed_capabilities.values()
        ]

    def get_statistics(self) -> Dict:
        """Get composition statistics."""
        total_uses = sum(c.usage_count for c in self.composed_capabilities.values())
        avg_success = (
            sum(c.success_rate for c in self.composed_capabilities.values())
            / len(self.composed_capabilities)
            if self.composed_capabilities else 0.0
        )

        return {
            "total_compositions": len(self.composed_capabilities),
            "total_uses": total_uses,
            "average_success_rate": avg_success,
            "predefined": len(self.COMPOSITION_PATTERNS),
            "discovered": len(self.composed_capabilities) - len(self.COMPOSITION_PATTERNS)
        }


# =============================================================================
# OPTION B: SELF-COMPILER (Loop 2)
# =============================================================================

@dataclass
class PatternMatch:
    """A matched pattern with similarity score."""
    pattern_id: str
    solution_template: str
    similarity: float
    abstraction_level: int
    success_rate: float


class PatternLibrary:
    """
    Library of reusable solution patterns for the Self-Compiler.

    Patterns are learned from successful problem-solving and can be
    lifted to higher abstraction levels when they work across domains.
    """

    def __init__(self, memory: Memory):
        """
        Initialize the Pattern Library.

        Args:
            memory: The BYRD memory system for pattern storage
        """
        self.memory = memory
        self._pattern_cache: Dict[str, Dict] = {}

    async def find_matching_patterns(
        self,
        problem_embedding: List[float],
        min_similarity: float = 0.7,
        limit: int = 5
    ) -> List[PatternMatch]:
        """
        Find patterns that match the current problem.

        Args:
            problem_embedding: Semantic embedding of the problem
            min_similarity: Minimum similarity threshold
            limit: Maximum patterns to return

        Returns:
            List of matching patterns sorted by relevance
        """
        similar = await self.memory.get_similar_patterns(
            query_embedding=problem_embedding,
            min_similarity=min_similarity,
            limit=limit
        )

        matches = []
        for pattern in similar:
            success_count = pattern.get("success_count", 0)
            failure_count = pattern.get("failure_count", 0)
            total = success_count + failure_count
            success_rate = success_count / total if total > 0 else 0.5

            matches.append(PatternMatch(
                pattern_id=pattern["id"],
                solution_template=pattern.get("solution_template", ""),
                similarity=pattern.get("similarity", 0.0),
                abstraction_level=pattern.get("abstraction_level", 0),
                success_rate=success_rate
            ))

        # Sort by combined score: similarity * success_rate * (1 + abstraction_level * 0.1)
        matches.sort(
            key=lambda m: m.similarity * m.success_rate * (1 + m.abstraction_level * 0.1),
            reverse=True
        )

        return matches

    async def add_pattern(
        self,
        problem_embedding: List[float],
        solution_template: str,
        domains: List[str],
        abstraction_level: int = 0
    ) -> str:
        """
        Add a new pattern to the library.

        Args:
            problem_embedding: Semantic embedding of the problem context
            solution_template: The reusable solution approach
            domains: Domains where this pattern applies
            abstraction_level: 0=concrete, 1=domain, 2=abstract, 3=universal

        Returns:
            Pattern ID
        """
        return await self.memory.create_pattern(
            context_embedding=problem_embedding,
            solution_template=solution_template,
            abstraction_level=abstraction_level,
            domains=domains
        )

    async def record_usage(
        self,
        pattern_id: str,
        success: bool,
        new_domain: Optional[str] = None
    ):
        """
        Record pattern usage outcome.

        Args:
            pattern_id: Pattern that was used
            success: Whether it led to success
            new_domain: Optional new domain where it worked
        """
        await self.memory.update_pattern_success(
            pattern_id=pattern_id,
            success=success
        )

        # If successful in a new domain, update the pattern's domain list
        if success and new_domain:
            await self._add_domain_to_pattern(pattern_id, new_domain)

    async def _add_domain_to_pattern(self, pattern_id: str, domain: str):
        """Add a new domain to a pattern's list."""
        # This would update the pattern's domains list
        # For now, just log it
        pass

    async def get_liftable_patterns(self) -> List[Dict]:
        """
        Find patterns ready for abstraction lifting.

        A pattern is liftable when it succeeds across multiple domains.
        """
        return await self.memory.get_patterns_for_lifting(
            min_success_count=3,
            min_domain_count=2
        )


class SelfCompiler:
    """
    Loop 2 of Option B: Code Learning Through Pattern Accumulation

    The Self-Compiler learns from successful problem-solving by:
    1. Extracting solution patterns from successes
    2. Matching patterns to new problems
    3. Lifting patterns to higher abstraction when they generalize

    THE KEY INSIGHT: Each success teaches a reusable pattern.
    Patterns compound because more patterns = more solutions = more patterns.
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: LLMClient,
        config: Optional[Dict] = None
    ):
        """
        Initialize the Self-Compiler.

        Args:
            memory: The BYRD memory system
            llm_client: LLM client for pattern extraction
            config: Configuration from config.yaml option_b.self_compiler
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Pattern library
        self.pattern_library = PatternLibrary(memory)

        # Configuration
        pl_config = self.config.get("pattern_library", {})
        self.min_similarity = pl_config.get("min_similarity", 0.7)
        self.lifting_threshold = pl_config.get("lifting_threshold", 3)
        self.min_domains_for_lift = pl_config.get("min_domains_for_lift", 2)

        self.success_reinforcement = self.config.get("success_reinforcement", 0.1)
        self.failure_penalty = self.config.get("failure_penalty", 0.05)

        # Metrics
        self._patterns_created = 0
        self._patterns_matched = 0
        self._patterns_lifted = 0
        self._total_compilations = 0

        # Initialize loop instrumentation to break zero-delta loops
        self.instrumenter: Optional['LoopInstrumenter'] = None
        self.loop_name: str = "self_compiler"
        if HAS_INSTRUMENTATION:
            try:
                self.instrumenter = get_instrumenter()
                if self.instrumenter:
                    self.instrumenter.register_loop(self.loop_name)
                    print(f"[INSTRUMENTATION] Registered loop '{self.loop_name}' for zero-delta detection")
            except Exception:
                pass

        # Cycle counter for instrumentation
        self._cycle_counter = 0

        # Embedding provider (lazy init)
        self._embedder = None

    async def _get_embedder(self):
        """Get the embedding provider."""
        if self._embedder is None:
            from embedding import get_global_embedder
            self._embedder = get_global_embedder()
        return self._embedder

    async def compile_solution(
        self,
        problem: str,
        problem_embedding: Optional[List[float]] = None
    ) -> Optional[str]:
        """
        Attempt to compile a solution from existing patterns.

        Args:
            problem: Description of the problem
            problem_embedding: Optional pre-computed embedding

        Returns:
            Solution template if a pattern matches, None otherwise
        """
        self._total_compilations += 1

        # Get embedding if not provided
        if problem_embedding is None:
            embedder = await self._get_embedder()
            result = await embedder.embed(problem)
            problem_embedding = result.embedding

        # Find matching patterns
        matches = await self.pattern_library.find_matching_patterns(
            problem_embedding,
            min_similarity=self.min_similarity,
            limit=3
        )

        if not matches:
            return None

        # Use the best match
        best = matches[0]
        self._patterns_matched += 1

        # Return the solution template with adaptation prompt
        result = f"""Pattern Match (similarity={best.similarity:.2f}, success_rate={best.success_rate:.2f}):

{best.solution_template}

Adapt this pattern for the current problem: {problem}"""
        
        # INTEGRATION WITH LOOP INSTRUMENTATION
        # Record compilation cycle metrics to break zero-delta loops
        if self.instrumenter and HAS_INSTRUMENTATION:
            self._record_compiler_cycle(matched=True, start_time=datetime.now(), 
                                    pattern_used=True, pattern_id=best.pattern_id)
        
        return result

    async def learn_from_success(
        self,
        problem: str,
        solution: str,
        domains: List[str],
        matched_pattern_id: Optional[str] = None
    ):
        """
        Learn from a successful problem-solution pair.

        If a pattern was used, reinforce it.
        If no pattern was used, extract a new pattern.

        Args:
            problem: The problem that was solved
            solution: The solution that worked
            domains: Domains this solution applies to
            matched_pattern_id: If a pattern was used, its ID
        """
        if matched_pattern_id:
            # Reinforce the existing pattern
            await self.pattern_library.record_usage(
                matched_pattern_id,
                success=True,
                new_domain=domains[0] if domains else None
            )
        else:
            # Extract a new pattern
            await self._extract_pattern(problem, solution, domains)
        
        # INTEGRATION WITH LOOP INSTRUMENTATION
        # Record learning cycle metrics
        if self.instrumenter and HAS_INSTRUMENTATION:
            self._record_compiler_cycle(matched=True, start_time=datetime.now(),
                                    pattern_used=(matched_pattern_id is not None),
                                    pattern_id=matched_pattern_id)

    async def learn_from_failure(
        self,
        problem: str,
        matched_pattern_id: Optional[str] = None
    ):
        """
        Learn from a failed attempt.

        If a pattern was used, penalize it.
        """
        if matched_pattern_id:
            await self.pattern_library.record_usage(
                matched_pattern_id,
                success=False
            )

    async def _extract_pattern(
        self,
        problem: str,
        solution: str,
        domains: List[str]
    ):
        """
        Extract a reusable pattern from a problem-solution pair.

        Uses LLM to generalize the solution into a template.
        """
        prompt = f"""Extract a reusable solution pattern from this problem-solution pair.

Problem: {problem}

Solution: {solution}

Create a generalized template that could be applied to similar problems.
Focus on the structure and approach, not specific details.

Template:"""

        try:
            template = await self.llm_client.query(prompt, max_tokens=500)

            # Get embedding for the problem
            embedder = await self._get_embedder()
            result = await embedder.embed(problem)

            # Store the pattern
            await self.pattern_library.add_pattern(
                problem_embedding=result.embedding,
                solution_template=template,
                domains=domains,
                abstraction_level=0  # Concrete level
            )

            self._patterns_created += 1

        except Exception as e:
            # Log but don't fail
            pass

    async def attempt_lifting(self) -> int:
        """
        Attempt to lift patterns to higher abstraction levels.

        Returns number of patterns lifted.
        """
        liftable = await self.pattern_library.get_liftable_patterns()
        lifted_count = 0

        for pattern in liftable:
            try:
                success = await self._lift_pattern(pattern)
                if success:
                    lifted_count += 1
                    self._patterns_lifted += 1
            except Exception:
                continue

        return lifted_count

    def _record_compiler_cycle(
        self,
        matched: bool,
        start_time: datetime,
        pattern_used: bool,
        pattern_id: Optional[str] = None
    ) -> None:
        """
        Record compiler cycle metrics with loop instrumenter.
        
        This breaks the zero-delta loop by tracking:
        - Pattern match rate improvement (delta)
        - Success based on whether patterns matched or were learned
        - Duration of the compilation cycle
        - Whether the improvement was meaningful
        """
        if not self.instrumenter:
            return
        
        self._cycle_counter += 1
        
        # Calculate delta as change in pattern match rate
        if self._total_compilations > 0:
            current_match_rate = self._patterns_matched / self._total_compilations
        else:
            current_match_rate = 0.0
        
        # Track baseline match rate from previous cycles
        if not hasattr(self, '_baseline_match_rate'):
            self._baseline_match_rate = 0.0
        
        # Delta is improvement in match rate
        delta = current_match_rate - self._baseline_match_rate
        self._baseline_match_rate = current_match_rate
        
        # Success if we matched a pattern or learned from new one
        success = matched and (pattern_used or self._patterns_created > 0)
        
        # Duration
        duration_seconds = (datetime.now() - start_time).total_seconds()
        
        # Meaningful if delta >= 0.5% (MIN_MEANINGFUL_DELTA)
        MIN_MEANINGFUL_DELTA = 0.005
        is_meaningful = delta >= MIN_MEANINGFUL_DELTA
        
        # Create cycle metrics
        from loop_instrumentation import CycleMetrics
        metrics = CycleMetrics(
            cycle_number=self._cycle_counter,
            timestamp=datetime.now(),
            delta=delta,
            success=success,
            meaningful=is_meaningful,
            duration_seconds=duration_seconds,
            error=None
        )
        
        # Record with instrumenter (pass individual params, not metrics object)
        self.instrumenter.record_cycle(
            self.loop_name,
            delta=metrics.delta,
            success=metrics.success,
            duration_seconds=metrics.duration_seconds
        )
        
        # Check for stagnation and log warning
        if self.instrumenter.is_stagnant(self.loop_name):
            analysis = self.instrumenter.analyze_stagnation(self.loop_name)
            print(f"[INSTRUMENTATION] Self-Compiler stagnation detected: {analysis}")

    async def _lift_pattern(self, pattern: Dict) -> bool:
        """
        Lift a pattern to a higher abstraction level.

        Uses LLM to generalize the pattern across domains.
        """
        current_level = pattern.get("abstraction_level", 0)
        if current_level >= 3:  # Already universal
            return False

        domains = pattern.get("domains", [])
        template = pattern.get("solution_template", "")

        prompt = f"""This solution pattern has worked across multiple domains: {', '.join(domains)}

Current template:
{template}

Create a more abstract version that captures the underlying principle.
Focus on what makes this pattern work across different domains.

Abstract principle:"""

        try:
            abstracted = await self.llm_client.query(prompt, max_tokens=500)

            # Get new embedding for the abstracted pattern
            embedder = await self._get_embedder()
            result = await embedder.embed(abstracted)

            # Create lifted pattern
            await self.memory.create_pattern(
                context_embedding=result.embedding,
                solution_template=abstracted,
                abstraction_level=current_level + 1,
                domains=domains,
                lifted_from=pattern["id"]
            )

            return True

        except Exception:
            return False

    def get_metrics(self) -> Dict[str, Any]:
        """Get Self-Compiler metrics."""
        return {
            "patterns_created": self._patterns_created,
            "patterns_matched": self._patterns_matched,
            "patterns_lifted": self._patterns_lifted,
            "total_compilations": self._total_compilations,
            "match_rate": (
                self._patterns_matched / self._total_compilations
                if self._total_compilations > 0 else 0.0
            )
        }

    def is_healthy(self) -> bool:
        """Check if the Self-Compiler is healthy."""
        if self._total_compilations < 10:
            return True  # Too early to judge

        # Should match at least 20% of compilations
        return (self._patterns_matched / self._total_compilations) >= 0.2


class AcceleratorOrchestrator:
    """
    Orchestrates all accelerators for maximum improvement rate.

    Decides when to:
    - Use graph shortcuts vs full reasoning
    - Generate new challenges
    - Suggest capability compositions
    - Apply pattern matching (Option B)
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Optional[Dict] = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Initialize accelerators
        self.graph_reasoning = GraphPoweredReasoning(memory, llm_client)
        self.adversarial = AdversarialSelfImprovement(memory, llm_client)
        self.composition = CapabilityComposition(memory, llm_client)

        # Option B accelerators
        sc_config = self.config.get("option_b", {}).get("self_compiler", {})
        self.self_compiler = SelfCompiler(memory, llm_client, sc_config)

        # Self-model reference (injected later)
        self.self_model = None

        # Tracking
        self._cycles = 0
        self._last_challenge_cycle = 0
        self._challenge_interval = 10  # Generate challenge every N cycles

    async def accelerate_cycle(self) -> Dict:
        """
        Run acceleration logic for this cycle.

        Returns actions taken and recommendations.
        """
        self._cycles += 1
        actions = []

        # Generate challenge if due
        if (self._cycles - self._last_challenge_cycle) >= self._challenge_interval:
            if self.self_model:
                challenge = await self.adversarial.get_next_challenge(self.self_model)
                if challenge:
                    actions.append({
                        "type": "challenge_generated",
                        "challenge": challenge.description
                    })
                    self._last_challenge_cycle = self._cycles

        # Get important nodes for context
        important = await self.graph_reasoning.find_important_nodes("current focus", limit=5)
        if important:
            actions.append({
                "type": "graph_insight",
                "important_nodes": len(important)
            })

        return {
            "cycle": self._cycles,
            "actions": actions,
            "statistics": self.get_statistics()
        }

    async def suggest_composition(self, current_task: str) -> Optional[Dict]:
        """Suggest a composition that might help with the current task."""
        task_lower = current_task.lower()

        # Simple keyword matching for now
        if "research" in task_lower and "understand" in task_lower:
            return await self.composition.execute_composition("informed_analysis", {"task": current_task})
        elif "code" in task_lower or "implement" in task_lower:
            return await self.composition.execute_composition("verified_code", {"task": current_task})
        elif "improve" in task_lower or "better" in task_lower:
            return await self.composition.execute_composition("strategic_improvement", {"task": current_task})

        return None

    def get_statistics(self) -> Dict:
        """Get combined statistics from all accelerators."""
        return {
            "cycles": self._cycles,
            "graph_reasoning": self.graph_reasoning.get_statistics(),
            "adversarial": self.adversarial.get_statistics(),
            "composition": self.composition.get_statistics(),
            "self_compiler": self.self_compiler.get_metrics()
        }


# Export main classes
__all__ = [
    "GraphPoweredReasoning",
    "AdversarialSelfImprovement",
    "CapabilityComposition",
    "AcceleratorOrchestrator",
    "Challenge",
    "ComposedCapability",
    "ReasoningShortcut",
    # Option B additions
    "PatternLibrary",
    "PatternMatch",
    "SelfCompiler"
]

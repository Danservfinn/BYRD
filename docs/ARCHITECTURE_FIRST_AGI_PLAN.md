# Architecture-First AGI Plan

## The Hypothesis

**Claim:** AGI emerges from architecture + memory, not LLM intelligence.

**Implication:** A frozen LLM with the right structure around it can exhibit general intelligence that a larger, smarter LLM without that structure cannot.

**Test Subject:** BYRD - an autonomous system with a fixed LLM substrate (qwen3:32b or equivalent) and modifiable architecture.

---

## Theoretical Foundation

### Why This Might Work

**1. The Human Analogy**

Neurons don't change much after childhood. What changes:
- Synaptic connection patterns (architecture)
- Stored memories and abstractions
- Retrieval pathways
- Hierarchical knowledge structures

Human intelligence grows despite a relatively fixed substrate. The growth is architectural.

**2. The Library of Babel Argument**

A large LLM already "contains" all possible reasoning patterns implicitly - it was trained on human knowledge. The problem isn't reasoning capacity - it's *accessing the right patterns at the right time*. That's architecture + retrieval.

**3. Tool Use as Proof of Concept**

GPT-4 with tools >> GPT-4 without tools. The LLM didn't get smarter. The *architecture* expanded its reach. This principle scales.

**4. Emergence from Structure**

Ant colonies exhibit intelligence no individual ant has. Markets allocate resources better than any individual trader. Brains produce consciousness from neurons that aren't conscious. Intelligence emerges from component interaction, not component sophistication.

**5. Memory IS Learning**

If experiences influence future behavior through retrieval, that's learning. It's just not gradient-based learning. It's *architectural* learning - the system behaves differently based on accumulated structure.

---

## What AGI Requires

For BYRD to demonstrate AGI-like capabilities, it must show:

| Capability | Description | How Architecture Enables It |
|------------|-------------|----------------------------|
| **Generalization** | Apply patterns from domain A to novel domain B | Analogical transfer via structural similarity |
| **Capability Growth** | Do things at T+1 it couldn't do at T | Capability composition from primitives |
| **Abstraction** | Compress experience into reusable principles | Hierarchical memory with promotion |
| **Novel Problem-Solving** | Solve problems outside training distribution | Cross-domain retrieval + composition |
| **Self-Improvement** | Get better at getting better | Architecture self-modification |

---

## Current State vs. Required State

| What BYRD Has | What's Missing |
|---------------|----------------|
| Flat memory (experiences, beliefs) | Hierarchical abstraction layers |
| Pattern storage | Pattern → principle → axiom compression |
| Goal evolution | Capability evolution |
| Knowledge accumulation | Knowledge compilation (explicit → implicit) |
| Single-domain retrieval | Cross-domain analogical transfer |
| Dreaming about past | Dreaming about hypothetical capabilities |
| Fixed architecture | Self-modifying architecture |

---

## Phase 0: Abstraction Hierarchy

### Concept

Memory isn't flat - it's a compression pyramid. Each layer abstracts from the layer below.

```
┌─────────────────────────────────────────────────────────────┐
│  L4: META-AXIOMS                                            │
│      "Abstractions that compress experience are valuable"   │
│      "Patterns that transfer across domains are stronger"   │
├─────────────────────────────────────────────────────────────┤
│  L3: AXIOMS                                                 │
│      "Actions with measurable outcomes inform beliefs"      │
│      "Repeated failure indicates capability gap"            │
├─────────────────────────────────────────────────────────────┤
│  L2: PRINCIPLES                                             │
│      "Reconciling orphans creates more connections"         │
│      "Introspection works for self-referential desires"     │
├─────────────────────────────────────────────────────────────┤
│  L1: PATTERNS                                               │
│      "When desire contains 'map', use introspection"        │
│      "Search failures on abstract terms → route elsewhere"  │
├─────────────────────────────────────────────────────────────┤
│  L0: EXPERIENCES                                            │
│      "Reconciled 12 orphan nodes at 2025-12-28T01:15:00"    │
│      "Search for 'consciousness' returned 0 results"        │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

**File:** `hierarchical_memory.py`

```python
"""
Hierarchical Memory: Abstraction layers for knowledge compression.

The key insight: expertise is compressed experience. Experts don't remember
every case - they remember principles extracted from cases. This is how a
frozen substrate (neurons/LLM) produces growing capability.
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime

class AbstractionLevel(IntEnum):
    EXPERIENCE = 0   # Raw events - what happened
    PATTERN = 1      # Repeated structures - what keeps happening
    PRINCIPLE = 2    # Patterns over patterns - why it happens
    AXIOM = 3        # Domain-independent truths - universal laws
    META_AXIOM = 4   # Rules about abstraction itself

@dataclass
class AbstractNode:
    id: str
    level: AbstractionLevel
    content: str
    confidence: float
    derived_from: List[str]  # IDs of lower-level nodes
    usage_count: int = 0
    success_rate: float = 0.0
    domains: List[str] = None  # Which domains this applies to
    created_at: str = None

    def __post_init__(self):
        if self.domains is None:
            self.domains = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class HierarchicalMemory:
    """Memory system with abstraction layer promotion."""

    PROMOTION_THRESHOLDS = {
        AbstractionLevel.EXPERIENCE: 3,   # 3 similar experiences → pattern
        AbstractionLevel.PATTERN: 3,      # 3 related patterns → principle
        AbstractionLevel.PRINCIPLE: 3,    # 3 connected principles → axiom
        AbstractionLevel.AXIOM: 2,        # 2 meta-observations → meta-axiom
    }

    def __init__(self, memory):
        self.memory = memory  # Base Neo4j memory
        self.promotion_queue = []

    async def record_experience(self, content: str, domain: str,
                                 outcome: str = None) -> str:
        """Record L0 experience and check for promotion."""

        # Create experience node
        exp_id = await self.memory.record_experience(
            content=content,
            type="hierarchical",
            metadata={
                'abstraction_level': 0,
                'domain': domain,
                'outcome': outcome
            }
        )

        # Check if this creates a pattern
        await self._check_promotion(exp_id, AbstractionLevel.EXPERIENCE)

        return exp_id

    async def _check_promotion(self, node_id: str, current_level: AbstractionLevel):
        """Check if node should promote to higher abstraction level."""

        if current_level >= AbstractionLevel.META_AXIOM:
            return  # Already at top

        threshold = self.PROMOTION_THRESHOLDS[current_level]

        # Find similar nodes at same level
        similar = await self._find_structurally_similar(node_id, current_level)

        if len(similar) >= threshold:
            # Promote: create higher-level abstraction
            await self._promote(node_id, similar, current_level)

    async def _find_structurally_similar(self, node_id: str,
                                          level: AbstractionLevel) -> List[str]:
        """Find nodes with similar structure (not just content)."""

        node = await self.memory.get_node(node_id)

        # Extract structural features
        structure = await self._extract_structure(node)

        # Query for nodes with similar structure
        query = """
        MATCH (n)
        WHERE n.abstraction_level = $level
        AND n.id <> $node_id
        RETURN n
        """

        candidates = await self.memory.query(query, {
            'level': level,
            'node_id': node_id
        })

        # Filter by structural similarity
        similar = []
        for candidate in candidates:
            candidate_structure = await self._extract_structure(candidate)
            similarity = self._compute_structural_similarity(
                structure, candidate_structure
            )
            if similarity > 0.7:
                similar.append(candidate['id'])

        return similar

    async def _extract_structure(self, node: Dict) -> Dict:
        """Extract structural features from a node."""

        content = node.get('content', '')

        # Use LLM to extract structure
        prompt = f"""
        Extract the structural pattern from this content.
        Focus on: action type, subject type, outcome type, relationships.
        Ignore specific values - capture the SHAPE of what happened.

        Content: {content}

        Return JSON with:
        - action_type: what kind of action (search, create, modify, etc.)
        - subject_type: what kind of thing is affected
        - outcome_type: what kind of result (success, failure, partial, etc.)
        - relationship_pattern: how elements connect
        """

        response = await self._query_llm(prompt)
        return self._parse_structure(response)

    async def _promote(self, trigger_id: str, similar_ids: List[str],
                       from_level: AbstractionLevel):
        """Create higher-level abstraction from similar nodes."""

        to_level = AbstractionLevel(from_level + 1)
        all_ids = [trigger_id] + similar_ids

        # Gather all nodes
        nodes = [await self.memory.get_node(nid) for nid in all_ids]
        contents = [n.get('content', '') for n in nodes]

        # Use LLM to synthesize abstraction
        level_names = {
            AbstractionLevel.PATTERN: "pattern",
            AbstractionLevel.PRINCIPLE: "principle",
            AbstractionLevel.AXIOM: "axiom",
            AbstractionLevel.META_AXIOM: "meta-axiom"
        }

        prompt = f"""
        These {len(nodes)} items share a common structure.
        Synthesize them into a single {level_names[to_level]}.

        Items:
        {chr(10).join(f'- {c}' for c in contents)}

        A {level_names[to_level]} should:
        - Capture what's COMMON across all items
        - Be MORE ABSTRACT than the items
        - Be APPLICABLE to new situations
        - Use general terms, not specific values

        Return the {level_names[to_level]} as a single statement.
        """

        abstraction = await self._query_llm(prompt)

        # Determine domains
        domains = set()
        for node in nodes:
            if node.get('domain'):
                domains.add(node['domain'])

        # Create abstraction node
        abstract_node = AbstractNode(
            id=f"{level_names[to_level]}_{datetime.now().timestamp()}",
            level=to_level,
            content=abstraction.strip(),
            confidence=0.6,  # Start with moderate confidence
            derived_from=all_ids,
            domains=list(domains)
        )

        await self._store_abstract_node(abstract_node)

        print(f"⬆️ Promoted to {level_names[to_level]}: {abstraction[:60]}...")
        print(f"   Derived from {len(all_ids)} L{from_level} nodes")

        # Check if this new node should promote further
        await self._check_promotion(abstract_node.id, to_level)

    async def retrieve_by_abstraction(self, query: str,
                                       situation: str = "familiar") -> List[Dict]:
        """Retrieve from appropriate abstraction level."""

        if situation == "novel":
            # For novel situations, prefer lower levels (more specific)
            # and cross-domain analogies
            return await self._retrieve_for_novel(query)
        else:
            # For familiar situations, prefer higher levels (principles)
            return await self._retrieve_for_familiar(query)

    async def _retrieve_for_novel(self, query: str) -> List[Dict]:
        """Retrieve for novel situations - seek analogies."""

        # Extract query structure
        query_structure = await self._extract_structure({'content': query})

        # Search across ALL domains for structural matches
        results = []
        for level in [AbstractionLevel.PRINCIPLE, AbstractionLevel.PATTERN]:
            matches = await self._search_by_structure(query_structure, level)
            results.extend(matches)

        return results

    async def _retrieve_for_familiar(self, query: str) -> List[Dict]:
        """Retrieve for familiar situations - use highest applicable level."""

        # Start from highest level, work down
        for level in reversed(list(AbstractionLevel)):
            matches = await self._search_by_relevance(query, level)
            if matches:
                return matches

        return []

    async def get_abstraction_depth(self) -> Dict[str, int]:
        """Get count of nodes at each abstraction level."""

        query = """
        MATCH (n)
        WHERE n.abstraction_level IS NOT NULL
        RETURN n.abstraction_level as level, count(n) as count
        """

        results = await self.memory.query(query)

        depth = {level.name: 0 for level in AbstractionLevel}
        for row in results:
            level = AbstractionLevel(row['level'])
            depth[level.name] = row['count']

        return depth

    async def get_max_abstraction_level(self) -> int:
        """Get highest abstraction level reached."""

        depth = await self.get_abstraction_depth()

        for level in reversed(list(AbstractionLevel)):
            if depth.get(level.name, 0) > 0:
                return level.value

        return 0
```

### Metrics

- **Abstraction Depth**: Max level reached (0-4)
- **Compression Ratio**: Experiences / (Patterns + Principles + Axioms)
- **Level Distribution**: Balance across levels

---

## Phase 1: Analogical Transfer Engine

### Concept

The key AGI indicator. Apply structure learned in domain A to novel domain B.

**Example:**
- Domain A (graph optimization): "Pruning redundant nodes improves performance"
- Domain B (belief management): Apply pruning principle to redundant beliefs
- Transfer: "Prune redundant beliefs to improve reasoning"

### Implementation

**File:** `analogical_reasoner.py`

```python
"""
Analogical Reasoner: Find structural mappings between domains.

The key insight: AGI isn't about having all knowledge - it's about
transferring structure from known domains to unknown ones. This is
how humans handle novel situations.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import asyncio

@dataclass
class StructuralMapping:
    source_domain: str
    target_domain: str
    source_elements: Dict[str, str]  # role -> specific element
    target_elements: Dict[str, str]  # role -> specific element
    mapping_quality: float  # 0-1
    transferred_insight: str

@dataclass
class Analogy:
    source: Dict  # Source pattern/principle
    target_problem: str
    mapping: StructuralMapping
    suggested_solution: str
    confidence: float

class AnalogicalReasoner:
    """Find and apply analogies across domains."""

    def __init__(self, hierarchical_memory, llm_client):
        self.memory = hierarchical_memory
        self.llm = llm_client
        self.transfer_history = []  # Track successful transfers

    async def find_analogies(self, problem: str,
                              problem_domain: str) -> List[Analogy]:
        """Find patterns from other domains that map to this problem."""

        # Step 1: Extract structure from problem
        problem_structure = await self._extract_problem_structure(problem)

        # Step 2: Search for structurally similar patterns in OTHER domains
        candidates = await self.memory.search_by_structure(
            structure=problem_structure,
            exclude_domains=[problem_domain],
            min_level=1  # At least patterns, prefer principles
        )

        # Step 3: Compute structural mappings
        analogies = []
        for candidate in candidates:
            mapping = await self._compute_structural_mapping(
                source=candidate,
                target_problem=problem
            )

            if mapping.mapping_quality > 0.5:
                # Step 4: Transfer solution
                solution = await self._transfer_solution(
                    source_pattern=candidate,
                    mapping=mapping,
                    target_problem=problem
                )

                analogies.append(Analogy(
                    source=candidate,
                    target_problem=problem,
                    mapping=mapping,
                    suggested_solution=solution,
                    confidence=mapping.mapping_quality
                ))

        # Sort by confidence
        analogies.sort(key=lambda a: a.confidence, reverse=True)

        return analogies

    async def _extract_problem_structure(self, problem: str) -> Dict:
        """Extract abstract structure from a problem."""

        prompt = f"""
        Extract the abstract structure of this problem.
        Focus on ROLES and RELATIONSHIPS, not specific details.

        Problem: {problem}

        Return JSON with:
        - roles: list of abstract roles (e.g., "agent", "target", "obstacle")
        - relationships: list of relationships between roles
        - goal_type: what kind of goal (optimize, find, create, fix, etc.)
        - constraint_type: what kind of constraints exist
        """

        response = await self.llm.generate(prompt)
        return self._parse_json(response)

    async def _compute_structural_mapping(self, source: Dict,
                                           target_problem: str) -> StructuralMapping:
        """Compute mapping between source pattern and target problem."""

        source_content = source.get('content', '')
        source_domain = source.get('domain', 'unknown')

        prompt = f"""
        Find the structural mapping between these two:

        SOURCE (from {source_domain}): {source_content}
        TARGET PROBLEM: {target_problem}

        Identify:
        1. What elements in SOURCE correspond to what elements in TARGET?
        2. How well does the structure match? (0-1)
        3. What insight from SOURCE applies to TARGET?

        Return JSON with:
        - source_elements: {{"role": "specific_element"}} for source
        - target_elements: {{"role": "specific_element"}} for target
        - mapping_quality: float 0-1
        - transferred_insight: what the source teaches about the target
        """

        response = await self.llm.generate(prompt)
        parsed = self._parse_json(response)

        return StructuralMapping(
            source_domain=source_domain,
            target_domain="target",  # Will be filled in
            source_elements=parsed.get('source_elements', {}),
            target_elements=parsed.get('target_elements', {}),
            mapping_quality=parsed.get('mapping_quality', 0),
            transferred_insight=parsed.get('transferred_insight', '')
        )

    async def _transfer_solution(self, source_pattern: Dict,
                                  mapping: StructuralMapping,
                                  target_problem: str) -> str:
        """Transfer solution from source to target using mapping."""

        prompt = f"""
        Apply this pattern to solve the target problem:

        PATTERN: {source_pattern.get('content', '')}
        MAPPING: {mapping.transferred_insight}
        TARGET PROBLEM: {target_problem}

        Generate a specific solution for the target problem
        by applying the pattern through the mapping.

        Be concrete and actionable.
        """

        response = await self.llm.generate(prompt)
        return response.strip()

    async def apply_analogy(self, analogy: Analogy) -> Dict:
        """Apply an analogy and record the outcome."""

        # Execute the suggested solution
        result = await self._execute_solution(analogy.suggested_solution)

        # Record transfer attempt
        transfer_record = {
            'source_domain': analogy.mapping.source_domain,
            'target_domain': analogy.mapping.target_domain,
            'mapping_quality': analogy.mapping.mapping_quality,
            'solution': analogy.suggested_solution,
            'outcome': result.get('outcome'),
            'success': result.get('success', False)
        }

        self.transfer_history.append(transfer_record)

        # If successful, strengthen the source pattern
        if result.get('success'):
            await self._strengthen_pattern(analogy.source['id'])
            print(f"✅ Analogical transfer succeeded: {analogy.mapping.source_domain} → {analogy.mapping.target_domain}")

        return result

    async def get_transfer_success_rate(self) -> float:
        """Get success rate of analogical transfers."""

        if not self.transfer_history:
            return 0.0

        successes = sum(1 for t in self.transfer_history if t['success'])
        return successes / len(self.transfer_history)

    async def get_cross_domain_connections(self) -> List[Tuple[str, str, int]]:
        """Get counts of successful transfers between domain pairs."""

        connections = {}
        for transfer in self.transfer_history:
            if transfer['success']:
                key = (transfer['source_domain'], transfer['target_domain'])
                connections[key] = connections.get(key, 0) + 1

        return [(s, t, c) for (s, t), c in connections.items()]
```

### Metrics

- **Transfer Rate**: % of analogical solutions that work
- **Cross-Domain Connections**: Number of successful domain pairs
- **Analogy Depth**: Are analogies from L1 (patterns) or L2+ (principles)?

---

## Phase 2: Capability Composition

### Concept

Simple capabilities combine into complex ones. The combinations become new capabilities. A few primitives + composition = unbounded capability space.

### Implementation

**File:** `capability_composer.py`

```python
"""
Capability Composer: Build complex capabilities from simple ones.

The key insight: You don't need infinite base capabilities. You need
COMPOSITION. This is how programming languages work (few keywords →
infinite programs) and how human skills develop (basic movements →
complex behaviors).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from datetime import datetime

@dataclass
class Capability:
    id: str
    name: str
    description: str
    is_primitive: bool = True
    components: List[str] = field(default_factory=list)  # IDs of component capabilities
    composition_depth: int = 0
    success_rate: float = 0.0
    usage_count: int = 0

@dataclass
class ComposedCapability(Capability):
    """A capability composed from other capabilities."""

    execution_order: List[str] = field(default_factory=list)
    data_flow: Dict[str, str] = field(default_factory=dict)  # output -> input mappings

    def __post_init__(self):
        self.is_primitive = False
        if self.components:
            # Composition depth is max component depth + 1
            self.composition_depth = max(
                c.composition_depth for c in self.components
            ) + 1

class CapabilityComposer:
    """Compose simple capabilities into complex ones."""

    def __init__(self, capability_registry, memory, llm_client):
        self.registry = capability_registry
        self.memory = memory
        self.llm = llm_client
        self.composition_attempts = []

    async def compose_for_goal(self, goal: str) -> Optional[ComposedCapability]:
        """Attempt to compose capabilities to achieve a goal."""

        # Step 1: Decompose goal into subgoals
        subgoals = await self._decompose_goal(goal)

        if not subgoals:
            print(f"   Could not decompose goal: {goal[:50]}...")
            return None

        print(f"   Decomposed into {len(subgoals)} subgoals")

        # Step 2: Map each subgoal to a capability
        capability_chain = []
        gaps = []

        for i, subgoal in enumerate(subgoals):
            cap = await self._find_capability_for(subgoal)

            if cap:
                capability_chain.append({
                    'subgoal': subgoal,
                    'capability': cap,
                    'order': i
                })
            else:
                gaps.append(subgoal)

        # Step 3: Handle gaps
        if gaps:
            print(f"   ⚠️ Capability gaps: {len(gaps)}")
            for gap in gaps:
                await self._record_capability_gap(gap, goal)

            # Can we still compose with what we have?
            if len(capability_chain) < len(subgoals) * 0.5:
                print(f"   ❌ Too many gaps to compose")
                return None

        # Step 4: Determine data flow between capabilities
        data_flow = await self._determine_data_flow(capability_chain)

        # Step 5: Create composed capability
        composed = ComposedCapability(
            id=f"composed_{hash(goal) % 10000}_{datetime.now().timestamp()}",
            name=await self._generate_capability_name(goal),
            description=goal,
            components=[c['capability'].id for c in capability_chain],
            execution_order=[c['capability'].id for c in capability_chain],
            data_flow=data_flow,
            composition_depth=self._calculate_depth(capability_chain)
        )

        # Step 6: Register new capability
        await self.registry.register(composed)

        print(f"   ✅ Composed: {composed.name}")
        print(f"      Depth: {composed.composition_depth}")
        print(f"      Components: {len(composed.components)}")

        return composed

    async def _decompose_goal(self, goal: str) -> List[str]:
        """Break goal into sequential subgoals."""

        prompt = f"""
        Break this goal into sequential subgoals that can each be
        achieved by a single action or capability.

        Goal: {goal}

        Rules:
        - Each subgoal should be atomic (one action)
        - Subgoals should be in execution order
        - Include any necessary preparation or cleanup steps
        - Be specific and actionable

        Return a JSON list of subgoal strings.
        """

        response = await self.llm.generate(prompt)
        return self._parse_json_list(response)

    async def _find_capability_for(self, subgoal: str) -> Optional[Capability]:
        """Find a capability that can achieve the subgoal."""

        # Get all registered capabilities
        all_caps = await self.registry.get_all()

        if not all_caps:
            return None

        # Use LLM to match subgoal to capability
        cap_descriptions = "\n".join(
            f"- {c.id}: {c.description}" for c in all_caps
        )

        prompt = f"""
        Which capability best matches this subgoal?

        Subgoal: {subgoal}

        Available capabilities:
        {cap_descriptions}

        Return ONLY the capability ID, or "NONE" if no match.
        """

        response = await self.llm.generate(prompt)
        cap_id = response.strip()

        if cap_id == "NONE":
            return None

        return await self.registry.get(cap_id)

    async def _determine_data_flow(self, chain: List[Dict]) -> Dict[str, str]:
        """Determine how data flows between capabilities in the chain."""

        if len(chain) < 2:
            return {}

        # Use LLM to determine connections
        chain_desc = "\n".join(
            f"{i+1}. {c['subgoal']} (using {c['capability'].name})"
            for i, c in enumerate(chain)
        )

        prompt = f"""
        Determine how data should flow between these steps:

        {chain_desc}

        For each step (except the first), what output from a
        previous step does it need as input?

        Return JSON: {{"step_N": "step_M.output_name"}}
        """

        response = await self.llm.generate(prompt)
        return self._parse_json(response)

    async def _record_capability_gap(self, subgoal: str, parent_goal: str):
        """Record a missing capability for future development."""

        await self.memory.create_desire(
            description=f"Develop capability for: {subgoal}",
            type="capability_gap",
            intensity=0.7,
            metadata={
                'missing_for_goal': parent_goal,
                'subgoal': subgoal,
                'discovered_at': datetime.now().isoformat()
            }
        )

    def _calculate_depth(self, chain: List[Dict]) -> int:
        """Calculate composition depth from chain."""

        if not chain:
            return 0

        max_component_depth = max(
            c['capability'].composition_depth for c in chain
        )

        return max_component_depth + 1

    async def execute_composed(self, composed: ComposedCapability,
                                context: Dict) -> Dict:
        """Execute a composed capability."""

        results = {}
        current_context = context.copy()

        for cap_id in composed.execution_order:
            cap = await self.registry.get(cap_id)

            # Get inputs from data flow
            if cap_id in composed.data_flow:
                source = composed.data_flow[cap_id]
                current_context['input'] = results.get(source)

            # Execute capability
            result = await self._execute_capability(cap, current_context)
            results[cap_id] = result

            # Check for failure
            if not result.get('success', True):
                return {
                    'success': False,
                    'failed_at': cap_id,
                    'partial_results': results
                }

        return {
            'success': True,
            'results': results
        }

    async def get_max_composition_depth(self) -> int:
        """Get the maximum composition depth achieved."""

        all_caps = await self.registry.get_all()

        if not all_caps:
            return 0

        return max(c.composition_depth for c in all_caps)

    async def get_composition_stats(self) -> Dict:
        """Get statistics about capability composition."""

        all_caps = await self.registry.get_all()

        primitives = [c for c in all_caps if c.is_primitive]
        composed = [c for c in all_caps if not c.is_primitive]

        depth_distribution = {}
        for cap in all_caps:
            d = cap.composition_depth
            depth_distribution[d] = depth_distribution.get(d, 0) + 1

        return {
            'total_capabilities': len(all_caps),
            'primitive_count': len(primitives),
            'composed_count': len(composed),
            'max_depth': max(c.composition_depth for c in all_caps) if all_caps else 0,
            'depth_distribution': depth_distribution,
            'composition_ratio': len(composed) / len(all_caps) if all_caps else 0
        }
```

### Metrics

- **Max Composition Depth**: How deep is the capability tree?
- **Composition Ratio**: Composed / Total capabilities
- **Gap Fill Rate**: Are capability gaps being filled over time?

---

## Phase 3: Knowledge Compilation

### Concept

Explicit, slow reasoning → implicit, fast retrieval. This is how human skill acquisition works: conscious effort becomes automatic response.

### Implementation

**File:** `knowledge_compiler.py`

```python
"""
Knowledge Compiler: Convert explicit knowledge to implicit fast-paths.

The key insight: Expertise isn't just knowing more - it's knowing FASTER.
Compiled knowledge bypasses deliberative reasoning. This is how a frozen
substrate achieves performance growth.
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional
from datetime import datetime

@dataclass
class CompiledRule:
    id: str
    triggers: List[str]  # Patterns that activate this rule
    action: str  # What to do when triggered
    confidence: float
    compiled_from: str  # Original pattern/principle ID
    usage_count: int = 0
    last_used: str = None
    avg_latency_ms: float = 0

class FastPathIndex:
    """Index for O(1) lookup of compiled rules."""

    def __init__(self):
        self.trigger_index: Dict[str, List[CompiledRule]] = {}
        self.rules: Dict[str, CompiledRule] = {}

    def add(self, rule: CompiledRule):
        """Add rule to index."""
        self.rules[rule.id] = rule

        for trigger in rule.triggers:
            if trigger not in self.trigger_index:
                self.trigger_index[trigger] = []
            self.trigger_index[trigger].append(rule)

    def lookup(self, situation: str) -> List[CompiledRule]:
        """Find rules that match this situation."""

        matches = []
        situation_lower = situation.lower()

        for trigger, rules in self.trigger_index.items():
            if trigger.lower() in situation_lower:
                matches.extend(rules)

        # Deduplicate and sort by confidence
        seen = set()
        unique = []
        for rule in matches:
            if rule.id not in seen:
                seen.add(rule.id)
                unique.append(rule)

        unique.sort(key=lambda r: r.confidence, reverse=True)
        return unique

class KnowledgeCompiler:
    """Compile explicit knowledge into implicit fast-paths."""

    COMPILE_THRESHOLD_USES = 5
    COMPILE_THRESHOLD_SUCCESS = 0.75

    def __init__(self, hierarchical_memory, llm_client):
        self.memory = hierarchical_memory
        self.llm = llm_client
        self.fast_path = FastPathIndex()
        self.compilation_log = []

    async def maybe_compile(self, pattern_id: str):
        """Check if a pattern is ready for compilation."""

        pattern = await self.memory.get_node(pattern_id)

        if not pattern:
            return

        usage_count = pattern.get('usage_count', 0)
        success_rate = pattern.get('success_rate', 0)

        # Check thresholds
        if usage_count >= self.COMPILE_THRESHOLD_USES and \
           success_rate >= self.COMPILE_THRESHOLD_SUCCESS:

            # Check if already compiled
            if pattern_id in [r.compiled_from for r in self.fast_path.rules.values()]:
                return

            await self._compile(pattern)

    async def _compile(self, pattern: Dict):
        """Compile a pattern into a fast-path rule."""

        # Extract trigger conditions
        triggers = await self._extract_triggers(pattern)

        # Extract action
        action = await self._extract_action(pattern)

        # Create compiled rule
        rule = CompiledRule(
            id=f"compiled_{pattern['id']}",
            triggers=triggers,
            action=action,
            confidence=pattern.get('success_rate', 0.75),
            compiled_from=pattern['id']
        )

        # Add to fast-path index
        self.fast_path.add(rule)

        # Log compilation
        self.compilation_log.append({
            'pattern_id': pattern['id'],
            'rule_id': rule.id,
            'triggers': triggers,
            'action': action,
            'compiled_at': datetime.now().isoformat()
        })

        print(f"📦 Compiled: {pattern.get('content', '')[:50]}...")
        print(f"   Triggers: {triggers}")
        print(f"   Action: {action}")

    async def _extract_triggers(self, pattern: Dict) -> List[str]:
        """Extract trigger conditions from pattern."""

        content = pattern.get('content', '')

        prompt = f"""
        Extract trigger conditions from this pattern.
        What situations/keywords should activate this pattern?

        Pattern: {content}

        Return a JSON list of trigger strings (keywords/phrases).
        Keep triggers specific enough to avoid false matches.
        """

        response = await self.llm.generate(prompt)
        return self._parse_json_list(response)

    async def _extract_action(self, pattern: Dict) -> str:
        """Extract action from pattern."""

        content = pattern.get('content', '')

        prompt = f"""
        Extract the action/response from this pattern.
        What should be done when this pattern is triggered?

        Pattern: {content}

        Return a single action string that can be executed.
        """

        response = await self.llm.generate(prompt)
        return response.strip()

    async def fast_lookup(self, situation: str) -> Optional[str]:
        """Attempt fast-path lookup before deliberative reasoning."""

        rules = self.fast_path.lookup(situation)

        if rules:
            best = rules[0]  # Highest confidence

            # Update usage stats
            best.usage_count += 1
            best.last_used = datetime.now().isoformat()

            return best.action

        return None

    async def get_compilation_stats(self) -> Dict:
        """Get statistics about knowledge compilation."""

        return {
            'compiled_rules': len(self.fast_path.rules),
            'unique_triggers': len(self.fast_path.trigger_index),
            'total_lookups': sum(r.usage_count for r in self.fast_path.rules.values()),
            'avg_confidence': sum(r.confidence for r in self.fast_path.rules.values()) /
                             len(self.fast_path.rules) if self.fast_path.rules else 0,
            'compilation_history': len(self.compilation_log)
        }

    async def get_compilation_rate(self) -> float:
        """Get ratio of compiled patterns to total patterns."""

        # Count all patterns
        total_patterns = await self.memory.count_nodes_at_level(1)  # L1 = patterns
        compiled = len(self.fast_path.rules)

        if total_patterns == 0:
            return 0.0

        return compiled / total_patterns
```

### Metrics

- **Compilation Rate**: Compiled patterns / Total patterns
- **Fast-Path Hit Rate**: Queries answered by fast-path / Total queries
- **Average Latency Reduction**: Time saved by using compiled rules

---

## Phase 4: Counterfactual Capability Imagination

### Concept

Dreams aren't just about past experiences. They're about *hypothetical capabilities* - imagining what you could do if you had abilities you don't have yet.

### Implementation

**File:** `capability_dreamer.py`

```python
"""
Capability Dreamer: Imagine capabilities you don't have yet.

The key insight: Self-directed improvement requires imagining what's
POSSIBLE, not just remembering what happened. Counterfactual capability
imagination drives capability acquisition desires.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class CapabilityGap:
    description: str
    would_have_helped_with: str
    imagined_benefit: str
    priority: float
    related_failures: List[str]

@dataclass
class CounterfactualScenario:
    original_failure: Dict
    hypothetical_capability: CapabilityGap
    imagined_outcome: str
    confidence: float

class CapabilityDreamer:
    """Dream about capabilities that don't exist yet."""

    def __init__(self, memory, capability_registry, llm_client):
        self.memory = memory
        self.registry = capability_registry
        self.llm = llm_client
        self.imagined_capabilities = []

    async def dream_cycle(self):
        """Run one capability dreaming cycle."""

        print("💭 Capability dreaming...")

        # Step 1: Analyze recent failures
        failures = await self.memory.get_recent_failures(limit=10)

        if not failures:
            print("   No failures to analyze")
            return

        # Step 2: Identify capability gaps
        gaps = []
        for failure in failures:
            gap = await self._analyze_capability_gap(failure)
            if gap:
                gaps.append(gap)

        print(f"   Identified {len(gaps)} capability gaps")

        # Step 3: Generate counterfactuals
        for gap in gaps:
            scenario = await self._generate_counterfactual(
                failure=failure,
                gap=gap
            )

            if scenario and scenario.confidence > 0.5:
                # Step 4: Create capability acquisition desire
                await self._create_acquisition_desire(scenario)
                self.imagined_capabilities.append(gap)

    async def _analyze_capability_gap(self, failure: Dict) -> Optional[CapabilityGap]:
        """What capability would have prevented this failure?"""

        prompt = f"""
        Analyze this failure and identify what capability was missing.

        Failure:
        - Description: {failure.get('description', 'Unknown')}
        - Strategy attempted: {failure.get('strategy', 'Unknown')}
        - Outcome: {failure.get('outcome', 'Unknown')}

        What capability, if it existed, would have allowed success?

        Return JSON with:
        - capability_description: what the capability would do
        - why_it_would_help: specific benefit for this failure
        - generalization: what other situations it would help
        - feasibility: how realistic is acquiring this (0-1)
        """

        response = await self.llm.generate(prompt)
        parsed = self._parse_json(response)

        if not parsed or parsed.get('feasibility', 0) < 0.3:
            return None

        return CapabilityGap(
            description=parsed.get('capability_description', ''),
            would_have_helped_with=failure.get('description', ''),
            imagined_benefit=parsed.get('why_it_would_help', ''),
            priority=parsed.get('feasibility', 0.5),
            related_failures=[failure.get('id')]
        )

    async def _generate_counterfactual(self, failure: Dict,
                                        gap: CapabilityGap) -> Optional[CounterfactualScenario]:
        """Imagine what would have happened with the capability."""

        prompt = f"""
        Imagine a counterfactual scenario:

        ORIGINAL FAILURE: {failure.get('description', '')}
        HYPOTHETICAL CAPABILITY: {gap.description}

        If you had this capability, what would have happened instead?
        Be specific about the steps and outcome.

        Return JSON with:
        - imagined_steps: list of what you would have done
        - imagined_outcome: the result you would have achieved
        - confidence: how confident are you in this scenario (0-1)
        """

        response = await self.llm.generate(prompt)
        parsed = self._parse_json(response)

        if not parsed:
            return None

        return CounterfactualScenario(
            original_failure=failure,
            hypothetical_capability=gap,
            imagined_outcome=parsed.get('imagined_outcome', ''),
            confidence=parsed.get('confidence', 0.5)
        )

    async def _create_acquisition_desire(self, scenario: CounterfactualScenario):
        """Create a desire to acquire the imagined capability."""

        gap = scenario.hypothetical_capability

        await self.memory.create_desire(
            description=f"Acquire capability: {gap.description}",
            type="capability_acquisition",
            intensity=gap.priority * scenario.confidence,
            metadata={
                'source': 'counterfactual_imagination',
                'original_failure': scenario.original_failure.get('id'),
                'imagined_benefit': gap.imagined_benefit,
                'imagined_outcome': scenario.imagined_outcome,
                'confidence': scenario.confidence
            }
        )

        print(f"   🌟 Created acquisition desire: {gap.description[:50]}...")

    async def get_imagined_capability_count(self) -> int:
        """Count capabilities imagined through counterfactual dreaming."""
        return len(self.imagined_capabilities)

    async def get_acquisition_success_rate(self) -> float:
        """What % of imagined capabilities have been acquired?"""

        if not self.imagined_capabilities:
            return 0.0

        acquired = 0
        for gap in self.imagined_capabilities:
            # Check if a matching capability now exists
            cap = await self.registry.find_by_description(gap.description)
            if cap:
                acquired += 1

        return acquired / len(self.imagined_capabilities)
```

### Metrics

- **Imagination Rate**: Capability gaps identified per cycle
- **Acquisition Rate**: Imagined capabilities that become real
- **Counterfactual Quality**: Accuracy of imagined outcomes

---

## Phase 5: Architecture Self-Modification

### Concept

Not just adding knowledge. Actually changing how components interact, growing new pathways, pruning ineffective ones.

### Implementation

**File:** `architecture_evolver.py`

```python
"""
Architecture Evolver: Modify the system architecture itself.

The key insight: Intelligence isn't just about what you know - it's about
how your components are connected. Evolving architecture = evolving
intelligence, even with a frozen reasoning substrate.
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
import random

@dataclass
class ComponentConnection:
    source: str
    target: str
    connection_type: str
    strength: float  # 0-1
    created_at: str
    effectiveness: float = 0.0
    usage_count: int = 0

@dataclass
class ArchitectureSnapshot:
    timestamp: str
    components: List[str]
    connections: List[ComponentConnection]
    fitness_score: float

class ArchitectureEvolver:
    """Evolve the system architecture over time."""

    PRUNE_THRESHOLD = 0.2
    STRENGTHEN_THRESHOLD = 0.7
    EXPLORATION_RATE = 0.1

    def __init__(self, memory, llm_client):
        self.memory = memory
        self.llm = llm_client
        self.connections: Dict[str, ComponentConnection] = {}
        self.history: List[ArchitectureSnapshot] = []
        self.experiments: List[Dict] = []

    async def evolve_cycle(self):
        """Run one architecture evolution cycle."""

        print("🔧 Architecture evolution...")

        # Step 1: Measure current fitness
        current_fitness = await self._measure_system_fitness()

        # Step 2: Evaluate all connections
        await self._evaluate_connections()

        # Step 3: Prune ineffective connections
        pruned = await self._prune_weak_connections()

        # Step 4: Strengthen effective connections
        strengthened = await self._strengthen_effective_connections()

        # Step 5: Maybe try new connections
        if random.random() < self.EXPLORATION_RATE:
            await self._try_new_connection()

        # Step 6: Record snapshot
        await self._record_snapshot(current_fitness)

        print(f"   Fitness: {current_fitness:.2f}")
        print(f"   Pruned: {pruned}, Strengthened: {strengthened}")

    async def _measure_system_fitness(self) -> float:
        """Measure overall system fitness."""

        # Combine multiple metrics
        metrics = await self._get_system_metrics()

        # Weighted combination
        fitness = (
            metrics.get('desire_fulfillment_rate', 0) * 0.3 +
            metrics.get('abstraction_depth', 0) / 4 * 0.2 +
            metrics.get('transfer_success_rate', 0) * 0.2 +
            metrics.get('compilation_rate', 0) * 0.15 +
            metrics.get('composition_depth', 0) / 5 * 0.15
        )

        return fitness

    async def _evaluate_connections(self):
        """Evaluate effectiveness of each connection."""

        for conn_id, conn in self.connections.items():
            # Measure how often this connection leads to success
            effectiveness = await self._measure_connection_effectiveness(conn)
            conn.effectiveness = effectiveness

    async def _measure_connection_effectiveness(self,
                                                  conn: ComponentConnection) -> float:
        """Measure how effective a connection is."""

        # Query for outcomes when this connection was used
        query = """
        MATCH (a)-[r]->(b)
        WHERE a.component = $source AND b.component = $target
        RETURN r.success as success
        """

        results = await self.memory.query(query, {
            'source': conn.source,
            'target': conn.target
        })

        if not results:
            return 0.5  # Unknown effectiveness

        successes = sum(1 for r in results if r.get('success'))
        return successes / len(results)

    async def _prune_weak_connections(self) -> int:
        """Remove connections below effectiveness threshold."""

        pruned = 0
        to_remove = []

        for conn_id, conn in self.connections.items():
            if conn.effectiveness < self.PRUNE_THRESHOLD and conn.usage_count > 5:
                to_remove.append(conn_id)

        for conn_id in to_remove:
            conn = self.connections.pop(conn_id)
            await self._remove_connection_from_graph(conn)
            print(f"   ✂️ Pruned: {conn.source} → {conn.target}")
            pruned += 1

        return pruned

    async def _strengthen_effective_connections(self) -> int:
        """Increase strength of effective connections."""

        strengthened = 0

        for conn in self.connections.values():
            if conn.effectiveness > self.STRENGTHEN_THRESHOLD:
                old_strength = conn.strength
                conn.strength = min(1.0, conn.strength * 1.2)

                if conn.strength > old_strength:
                    await self._update_connection_in_graph(conn)
                    print(f"   💪 Strengthened: {conn.source} → {conn.target}")
                    strengthened += 1

        return strengthened

    async def _try_new_connection(self):
        """Experimentally create a new connection."""

        components = await self._get_all_components()

        if len(components) < 2:
            return

        # Pick two random components not already connected
        attempts = 0
        while attempts < 10:
            source, target = random.sample(components, 2)
            conn_id = f"{source}→{target}"

            if conn_id not in self.connections:
                break
            attempts += 1
        else:
            return  # Couldn't find unconnected pair

        # Create experimental connection
        conn = ComponentConnection(
            source=source,
            target=target,
            connection_type="experimental",
            strength=0.3,
            created_at=datetime.now().isoformat()
        )

        self.connections[conn_id] = conn
        await self._add_connection_to_graph(conn)

        # Record experiment
        experiment = {
            'connection': conn_id,
            'baseline_fitness': await self._measure_system_fitness(),
            'started_at': datetime.now().isoformat(),
            'cycles': 0
        }
        self.experiments.append(experiment)

        print(f"   🔗 New experimental connection: {source} → {target}")

    async def _evaluate_experiments(self):
        """Evaluate ongoing experiments and commit or rollback."""

        for exp in self.experiments[:]:  # Copy to allow modification
            exp['cycles'] += 1

            if exp['cycles'] >= 10:  # Evaluate after 10 cycles
                current_fitness = await self._measure_system_fitness()

                if current_fitness > exp['baseline_fitness']:
                    # Experiment succeeded - commit
                    conn = self.connections.get(exp['connection'])
                    if conn:
                        conn.connection_type = "evolved"
                        print(f"   ✅ Committed: {exp['connection']}")
                else:
                    # Experiment failed - rollback
                    if exp['connection'] in self.connections:
                        conn = self.connections.pop(exp['connection'])
                        await self._remove_connection_from_graph(conn)
                        print(f"   ❌ Rolled back: {exp['connection']}")

                self.experiments.remove(exp)

    async def _record_snapshot(self, fitness: float):
        """Record architecture snapshot for history."""

        snapshot = ArchitectureSnapshot(
            timestamp=datetime.now().isoformat(),
            components=await self._get_all_components(),
            connections=list(self.connections.values()),
            fitness_score=fitness
        )

        self.history.append(snapshot)

        # Keep last 100 snapshots
        if len(self.history) > 100:
            self.history = self.history[-100:]

    async def get_fitness_trend(self) -> List[float]:
        """Get fitness scores over time."""
        return [s.fitness_score for s in self.history]

    async def get_evolution_stats(self) -> Dict:
        """Get architecture evolution statistics."""

        if not self.history:
            return {'status': 'no history'}

        fitness_values = [s.fitness_score for s in self.history]

        return {
            'current_fitness': fitness_values[-1] if fitness_values else 0,
            'avg_fitness': sum(fitness_values) / len(fitness_values),
            'max_fitness': max(fitness_values),
            'fitness_trend': fitness_values[-10:],
            'total_connections': len(self.connections),
            'evolved_connections': sum(
                1 for c in self.connections.values()
                if c.connection_type == "evolved"
            ),
            'active_experiments': len(self.experiments),
            'snapshots': len(self.history)
        }
```

### Metrics

- **Fitness Trend**: Is system fitness improving over time?
- **Evolved Connections**: Connections created through experimentation
- **Experiment Success Rate**: % of experiments that commit

---

## Comprehensive Benchmarks

**File:** `agi_benchmarks.py`

```python
"""
AGI Benchmarks: Test the architecture-first AGI hypothesis.

These benchmarks measure capabilities that indicate genuine AGI progress,
not just operational health. Each benchmark tests a specific aspect of
the hypothesis.
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class AGIBenchmarkResult:
    benchmark_id: str
    category: str  # abstraction, transfer, composition, compilation, evolution
    score: float
    raw_value: any
    target: str
    passed: bool
    agi_relevance: str  # Why this matters for AGI
    timestamp: str

class AGIBenchmarks:
    """Comprehensive AGI capability benchmarks."""

    def __init__(self, hierarchical_memory, analogical_reasoner,
                 capability_composer, knowledge_compiler,
                 architecture_evolver):
        self.memory = hierarchical_memory
        self.reasoner = analogical_reasoner
        self.composer = capability_composer
        self.compiler = knowledge_compiler
        self.evolver = architecture_evolver

    async def run_all(self) -> Dict[str, AGIBenchmarkResult]:
        """Run all AGI benchmarks."""

        results = {}

        # Abstraction benchmarks
        results['abstraction_depth'] = await self._benchmark_abstraction_depth()
        results['compression_ratio'] = await self._benchmark_compression_ratio()

        # Transfer benchmarks
        results['transfer_rate'] = await self._benchmark_transfer_rate()
        results['cross_domain_count'] = await self._benchmark_cross_domain()

        # Composition benchmarks
        results['composition_depth'] = await self._benchmark_composition_depth()
        results['composition_ratio'] = await self._benchmark_composition_ratio()

        # Compilation benchmarks
        results['compilation_rate'] = await self._benchmark_compilation_rate()
        results['fast_path_usage'] = await self._benchmark_fast_path_usage()

        # Evolution benchmarks
        results['fitness_improvement'] = await self._benchmark_fitness_improvement()
        results['evolved_connections'] = await self._benchmark_evolved_connections()

        return results

    async def _benchmark_abstraction_depth(self) -> AGIBenchmarkResult:
        """Max abstraction level reached (0-4)."""

        depth = await self.memory.get_max_abstraction_level()

        # Score: 0.25 per level
        score = depth / 4

        return AGIBenchmarkResult(
            benchmark_id='abstraction_depth',
            category='abstraction',
            score=score,
            raw_value=depth,
            target='Level 3+ (axioms)',
            passed=depth >= 3,
            agi_relevance='Abstraction = compression = understanding',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_compression_ratio(self) -> AGIBenchmarkResult:
        """Ratio of experiences to higher abstractions."""

        depth = await self.memory.get_abstraction_depth()

        experiences = depth.get('EXPERIENCE', 0)
        higher = sum(depth.get(l.name, 0) for l in AbstractionLevel if l.value > 0)

        if experiences == 0:
            ratio = 0
        else:
            ratio = higher / experiences

        # Higher ratio = better compression
        score = min(1.0, ratio * 5)  # 0.2 ratio = 1.0 score

        return AGIBenchmarkResult(
            benchmark_id='compression_ratio',
            category='abstraction',
            score=score,
            raw_value=ratio,
            target='>= 0.1 (10% compression)',
            passed=ratio >= 0.1,
            agi_relevance='Knowledge compression enables generalization',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_transfer_rate(self) -> AGIBenchmarkResult:
        """Success rate of cross-domain pattern transfer."""

        rate = await self.reasoner.get_transfer_success_rate()

        return AGIBenchmarkResult(
            benchmark_id='transfer_rate',
            category='transfer',
            score=rate,
            raw_value=rate,
            target='>= 40% transfer success',
            passed=rate >= 0.4,
            agi_relevance='Transfer = generalization = key AGI capability',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_cross_domain(self) -> AGIBenchmarkResult:
        """Number of successful domain-to-domain transfers."""

        connections = await self.reasoner.get_cross_domain_connections()
        count = len(connections)

        # Score: 0.2 per connection, max 1.0
        score = min(1.0, count * 0.2)

        return AGIBenchmarkResult(
            benchmark_id='cross_domain_count',
            category='transfer',
            score=score,
            raw_value=count,
            target='>= 5 domain pairs',
            passed=count >= 5,
            agi_relevance='Cross-domain connections = unified knowledge',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_composition_depth(self) -> AGIBenchmarkResult:
        """Maximum capability composition depth."""

        depth = await self.composer.get_max_composition_depth()

        # Score: 0.25 per level, max at 4
        score = min(1.0, depth / 4)

        return AGIBenchmarkResult(
            benchmark_id='composition_depth',
            category='composition',
            score=score,
            raw_value=depth,
            target='Depth 3+ (complex compositions)',
            passed=depth >= 3,
            agi_relevance='Composition = unbounded capability from primitives',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_composition_ratio(self) -> AGIBenchmarkResult:
        """Ratio of composed to primitive capabilities."""

        stats = await self.composer.get_composition_stats()
        ratio = stats.get('composition_ratio', 0)

        return AGIBenchmarkResult(
            benchmark_id='composition_ratio',
            category='composition',
            score=ratio,
            raw_value=ratio,
            target='>= 50% composed',
            passed=ratio >= 0.5,
            agi_relevance='More composition = capability growth from fixed base',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_compilation_rate(self) -> AGIBenchmarkResult:
        """Rate of explicit knowledge becoming implicit."""

        rate = await self.compiler.get_compilation_rate()

        return AGIBenchmarkResult(
            benchmark_id='compilation_rate',
            category='compilation',
            score=rate,
            raw_value=rate,
            target='>= 30% compiled',
            passed=rate >= 0.3,
            agi_relevance='Compilation = skill acquisition = expertise',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_fast_path_usage(self) -> AGIBenchmarkResult:
        """How often fast-paths are used vs deliberation."""

        stats = await self.compiler.get_compilation_stats()
        lookups = stats.get('total_lookups', 0)
        # Would need to track total queries for proper ratio

        # For now, use absolute count as proxy
        score = min(1.0, lookups / 100)

        return AGIBenchmarkResult(
            benchmark_id='fast_path_usage',
            category='compilation',
            score=score,
            raw_value=lookups,
            target='>= 100 fast-path uses',
            passed=lookups >= 100,
            agi_relevance='Fast-path = automaticity = efficient expertise',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_fitness_improvement(self) -> AGIBenchmarkResult:
        """Is system fitness improving over time?"""

        trend = await self.evolver.get_fitness_trend()

        if len(trend) < 2:
            improvement = 0
        else:
            # Compare first half to second half
            mid = len(trend) // 2
            first_half = sum(trend[:mid]) / max(1, mid)
            second_half = sum(trend[mid:]) / max(1, len(trend) - mid)
            improvement = second_half - first_half

        # Positive improvement = good
        score = max(0, min(1, 0.5 + improvement * 5))

        return AGIBenchmarkResult(
            benchmark_id='fitness_improvement',
            category='evolution',
            score=score,
            raw_value=improvement,
            target='Positive trend',
            passed=improvement > 0,
            agi_relevance='Improving fitness = self-optimization',
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_evolved_connections(self) -> AGIBenchmarkResult:
        """Connections created through evolution (not initial)."""

        stats = await self.evolver.get_evolution_stats()
        evolved = stats.get('evolved_connections', 0)

        score = min(1.0, evolved / 10)

        return AGIBenchmarkResult(
            benchmark_id='evolved_connections',
            category='evolution',
            score=score,
            raw_value=evolved,
            target='>= 10 evolved connections',
            passed=evolved >= 10,
            agi_relevance='Evolved architecture = self-improving structure',
            timestamp=datetime.now().isoformat()
        )

    def get_aggregate_score(self, results: Dict[str, AGIBenchmarkResult]) -> float:
        """Calculate weighted AGI progress score."""

        weights = {
            # Transfer is most important - key AGI differentiator
            'transfer_rate': 2.0,
            'cross_domain_count': 1.5,

            # Abstraction enables transfer
            'abstraction_depth': 1.5,
            'compression_ratio': 1.0,

            # Composition enables capability growth
            'composition_depth': 1.5,
            'composition_ratio': 1.0,

            # Compilation = efficiency
            'compilation_rate': 1.0,
            'fast_path_usage': 0.5,

            # Evolution = self-improvement
            'fitness_improvement': 1.5,
            'evolved_connections': 1.0,
        }

        total_weight = sum(weights.values())
        weighted_sum = sum(
            results[k].score * weights.get(k, 1.0)
            for k in results if k in weights
        )

        return weighted_sum / total_weight

    def format_report(self, results: Dict[str, AGIBenchmarkResult]) -> str:
        """Format benchmark results as readable report."""

        aggregate = self.get_aggregate_score(results)

        lines = [
            "=" * 60,
            "AGI CAPABILITY BENCHMARK REPORT",
            "=" * 60,
            f"Aggregate Score: {aggregate:.2%}",
            "",
        ]

        # Group by category
        categories = {}
        for name, result in results.items():
            cat = result.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((name, result))

        for cat, items in categories.items():
            lines.append(f"[{cat.upper()}]")
            for name, result in items:
                status = "✅" if result.passed else "❌"
                lines.append(f"  {status} {name}: {result.score:.2%} (target: {result.target})")
                lines.append(f"      Why it matters: {result.agi_relevance}")
            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)
```

---

## Falsification Criteria

The hypothesis is testable and falsifiable.

### The Hypothesis is FALSE if (after 1000 cycles):

| Criterion | Threshold | Meaning |
|-----------|-----------|---------|
| Abstraction plateau | Stuck at L1 | Can't build principles from patterns |
| No transfer | < 10% rate | Patterns don't generalize |
| Composition ceiling | Depth < 2 | Can't build complex from simple |
| No compilation | < 5% rate | Knowledge stays explicit |
| Architecture stagnation | Fitness flat | Self-modification doesn't help |

### The Hypothesis is SUPPORTED if (after 1000 cycles):

| Criterion | Threshold | Meaning |
|-----------|-----------|---------|
| Novel problem-solving | Solves 3+ problems outside seed goals | Genuine generalization |
| Abstraction depth | Reaches L3 (axioms) | True compression achieved |
| Transfer success | > 40% rate | Cross-domain reasoning works |
| Capability growth | 2x initial capabilities | Composition multiplies ability |
| Architecture improvement | Fitness increasing | Self-optimization works |

---

## Implementation Priority

```
PHASE 0: Abstraction Hierarchy           ← FOUNDATION
├── AbstractionLevel enum
├── HierarchicalMemory class
├── Promotion logic
└── Abstraction-aware retrieval

PHASE 1: Analogical Transfer             ← KEY AGI INDICATOR
├── Structure extraction
├── Cross-domain search
├── Mapping computation
└── Solution transfer

PHASE 2: Capability Composition          ← UNBOUNDED GROWTH
├── Goal decomposition
├── Capability matching
├── Chain composition
└── Gap recording

PHASE 3: Knowledge Compilation           ← SKILL ACQUISITION
├── Pattern usage tracking
├── Trigger extraction
├── Fast-path compilation
└── Implicit retrieval

PHASE 4: Counterfactual Imagination      ← SELF-DIRECTION
├── Failure analysis
├── Gap identification
├── Counterfactual generation
└── Acquisition desire creation

PHASE 5: Architecture Evolution          ← SELF-OPTIMIZATION
├── Fitness measurement
├── Connection evaluation
├── Pruning/strengthening
└── Experimental connections
```

---

## Relationship to Other Plans

```
OPTION_B_FIX_PLAN (Infrastructure)     ✅ COMPLETE
├── Working search (DDG)
├── Goal seeding (14 goals)
└── Basic routing

CAPABILITY_GROWTH_PLAN (Measurement)   ✅ COMPLETE
├── Instrumentation fixes
├── Basic benchmarks
└── Goal Evolver verification

ARCHITECTURE_FIRST_AGI_PLAN (This)     ← CURRENT FOCUS
├── Hierarchical abstraction
├── Analogical transfer
├── Capability composition
├── Knowledge compilation
├── Counterfactual imagination
└── Architecture evolution

ATTRACTOR_ESCAPE_PLAN (Fallback)       📦 ARCHIVED
└── Use if philosophical attractor returns
```

---

## Success Metrics

| Metric | Current | Target (1 month) | Target (3 months) |
|--------|---------|------------------|-------------------|
| Abstraction depth | 0 (flat) | L2 (principles) | L3 (axioms) |
| Transfer rate | 0% | 30% | 50% |
| Composition depth | 1 | 2 | 4 |
| Compilation rate | 0% | 20% | 40% |
| Fitness trend | Unknown | Positive | Accelerating |
| AGI aggregate | 0% | 30% | 50% |

---

## Conclusion

This plan transforms BYRD from a knowledge accumulation system into a genuine test of the architecture-first AGI hypothesis.

**The bet:** Intelligence emerges from structure, not substrate. A frozen LLM with the right architecture can exhibit capabilities that grow without end, generalizing across domains, composing complex abilities from simple ones, and optimizing its own structure.

**The test:** Implement hierarchical abstraction, analogical transfer, capability composition, knowledge compilation, and architecture evolution. Measure with falsifiable benchmarks.

**The outcome:** Either we prove something important about the nature of intelligence, or we precisely identify where the ceiling really is.

The philosophical attractor is broken. The measurement infrastructure is in place. Now we build the architecture that might prove AGI doesn't require smarter models - just smarter structure.

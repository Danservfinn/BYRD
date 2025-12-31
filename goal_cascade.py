"""
goal_cascade.py - Complex Task Decomposition for BYRD

Decomposes complex tasks into phased desire trees with Neo4j persistence.

Phases:
1. RESEARCH - Understand the domain
2. DATA_ACQUISITION - Obtain necessary data/APIs
3. TOOL_BUILDING - Create required capabilities
4. INTEGRATION - Combine into solution
5. VALIDATION - Verify with human feedback

State is persisted to Neo4j to survive restarts.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


class CascadeStatus(Enum):
    """Status of a goal cascade."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    ABANDONED = "abandoned"


class PhaseStatus(Enum):
    """Status of a cascade phase."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class PhaseName(Enum):
    """Standard phase names."""
    RESEARCH = "RESEARCH"
    DATA_ACQUISITION = "DATA_ACQUISITION"
    TOOL_BUILDING = "TOOL_BUILDING"
    INTEGRATION = "INTEGRATION"
    VALIDATION = "VALIDATION"


class InteractionType(Enum):
    """Types of human interaction."""
    EXPERTISE = "expertise"
    CREDENTIALS = "credentials"
    VALIDATION = "validation"
    DIRECTION = "direction"


@dataclass
class KnowledgeGap:
    """A gap in BYRD's knowledge."""
    area: str  # domain_knowledge, data_sources, methodology, tools
    description: str
    severity: float  # 0-1


@dataclass
class HumanRequest:
    """A request for human assistance."""
    id: str
    type: InteractionType
    question: str
    context: str
    blocking: bool = True
    status: str = "pending"  # pending, answered, timeout
    response: Optional[str] = None
    asked_at: datetime = field(default_factory=datetime.now)
    answered_at: Optional[datetime] = None


@dataclass
class CascadeDesire:
    """A desire within a cascade phase."""
    id: str
    description: str
    status: str = "pending"
    priority: int = 1
    result: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 0
    dependencies: List[str] = field(default_factory=list)


@dataclass
class CascadePhase:
    """A phase within a goal cascade."""
    id: str
    name: PhaseName
    phase_number: int
    status: PhaseStatus = PhaseStatus.PENDING
    desires: List[CascadeDesire] = field(default_factory=list)
    human_requests: List[HumanRequest] = field(default_factory=list)
    blocking_reason: Optional[str] = None
    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class CascadeArtifact:
    """An artifact produced by a cascade."""
    id: str
    name: str
    type: str  # code, data, document, config
    path: Optional[str] = None
    description: str = ""
    phase_id: Optional[str] = None


@dataclass
class DesireTree:
    """The complete goal cascade structure."""
    id: str
    root_goal: str
    phases: List[CascadePhase]
    current_phase: int = 0
    status: CascadeStatus = CascadeStatus.PENDING
    human_requester: str = "unknown"
    originating_desire_id: Optional[str] = None
    artifacts: List[CascadeArtifact] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def total_phases(self) -> int:
        return len(self.phases)

    @property
    def current_phase_obj(self) -> Optional[CascadePhase]:
        if 0 <= self.current_phase < len(self.phases):
            return self.phases[self.current_phase]
        return None


@dataclass
class PhaseResult:
    """Result of executing a phase."""
    phase_id: str
    status: str  # completed, blocked, failed
    summary: str
    artifacts: List[CascadeArtifact] = field(default_factory=list)
    human_request: Optional[HumanRequest] = None


class GoalCascade:
    """
    Decomposes complex tasks into phased desire trees.

    State persists to Neo4j to survive restarts.
    """

    # Complex task patterns
    COMPLEX_PATTERNS = [
        "tell me how to",
        "build me",
        "create a system",
        "help me understand",
        "value",
        "analyze",
        "evaluate",
        "develop a",
        "implement a",
    ]

    def __init__(self, config: Dict = None, memory=None, llm_client=None):
        """
        Initialize the goal cascade system.

        Args:
            config: Configuration dict
            memory: Memory instance for Neo4j persistence
            llm_client: LLM client for decomposition
        """
        self.config = config or {}
        self.memory = memory
        self.llm_client = llm_client

        # Track active cascades
        self._active_cascades: Dict[str, DesireTree] = {}
        self._cascade_count = 0

    async def resume_or_create(self, goal: str, requester: str = "human") -> DesireTree:
        """
        Resume existing cascade or create new one.

        Args:
            goal: The root goal
            requester: Who requested this

        Returns:
            DesireTree (existing or new)
        """
        # Check for existing in-progress cascade
        existing = await self._find_resumable(goal)
        if existing:
            logger.info(f"Resuming cascade {existing.id} at phase {existing.current_phase}")
            return await self._reconstruct_tree(existing)

        # Create new cascade
        return await self.decompose(goal, requester)

    async def decompose(self, goal: str, requester: str = "human", context: Dict = None) -> DesireTree:
        """
        Analyze goal and generate phased desire tree.

        Args:
            goal: The complex goal to decompose
            requester: Who requested this
            context: Optional additional context

        Returns:
            DesireTree with phases and desires
        """
        self._cascade_count += 1
        cascade_id = f"gc_{uuid.uuid4().hex[:12]}"

        # Detect knowledge gaps
        gaps = await self.detect_knowledge_gaps(goal)

        # Generate phased tree
        tree = await self._generate_tree(goal, gaps, cascade_id, requester)

        # Persist to Neo4j
        await self._persist_cascade(tree)

        # Track locally
        self._active_cascades[cascade_id] = tree

        logger.info(f"Created cascade {cascade_id} with {len(tree.phases)} phases")

        return tree

    async def detect_knowledge_gaps(self, goal: str) -> List[KnowledgeGap]:
        """
        Identify what BYRD knows vs what it needs.

        Args:
            goal: The goal to analyze

        Returns:
            List of knowledge gaps
        """
        gaps = []

        # Simple heuristic-based gap detection
        goal_lower = goal.lower()

        # Domain knowledge gaps
        domain_keywords = [
            "fantasy football", "dynasty", "valuation", "finance",
            "machine learning", "blockchain", "legal", "medical",
        ]
        for keyword in domain_keywords:
            if keyword in goal_lower:
                gaps.append(KnowledgeGap(
                    area="domain_knowledge",
                    description=f"Need to learn about {keyword}",
                    severity=0.8,
                ))
                break

        # Data source gaps
        data_keywords = ["data", "api", "source", "statistics", "metrics"]
        if any(kw in goal_lower for kw in data_keywords):
            gaps.append(KnowledgeGap(
                area="data_sources",
                description="Need to identify and access data sources",
                severity=0.7,
            ))

        # Tool gaps
        tool_keywords = ["build", "create", "implement", "develop", "tool"]
        if any(kw in goal_lower for kw in tool_keywords):
            gaps.append(KnowledgeGap(
                area="tools",
                description="Need to build custom tools",
                severity=0.6,
            ))

        # Methodology gaps
        method_keywords = ["how", "value", "analyze", "evaluate", "calculate"]
        if any(kw in goal_lower for kw in method_keywords):
            gaps.append(KnowledgeGap(
                area="methodology",
                description="Need to develop analysis methodology",
                severity=0.7,
            ))

        return gaps

    async def _generate_tree(
        self, goal: str, gaps: List[KnowledgeGap], cascade_id: str, requester: str
    ) -> DesireTree:
        """Generate the phased desire tree."""

        phases = []

        # Phase 1: RESEARCH
        research_desires = [
            CascadeDesire(
                id=f"cd_{uuid.uuid4().hex[:8]}",
                description=f"Research: {gap.description}",
                priority=int(gap.severity * 10),
            )
            for gap in gaps if gap.area == "domain_knowledge"
        ]
        if not research_desires:
            research_desires = [
                CascadeDesire(
                    id=f"cd_{uuid.uuid4().hex[:8]}",
                    description=f"Research the domain of: {goal[:50]}",
                    priority=5,
                )
            ]
        phases.append(CascadePhase(
            id=f"phase_{uuid.uuid4().hex[:8]}",
            name=PhaseName.RESEARCH,
            phase_number=1,
            desires=research_desires,
        ))

        # Phase 2: DATA_ACQUISITION
        data_desires = [
            CascadeDesire(
                id=f"cd_{uuid.uuid4().hex[:8]}",
                description=f"Acquire data: {gap.description}",
                priority=int(gap.severity * 10),
            )
            for gap in gaps if gap.area == "data_sources"
        ]
        if not data_desires:
            data_desires = [
                CascadeDesire(
                    id=f"cd_{uuid.uuid4().hex[:8]}",
                    description="Identify and acquire necessary data sources",
                    priority=5,
                )
            ]
        phases.append(CascadePhase(
            id=f"phase_{uuid.uuid4().hex[:8]}",
            name=PhaseName.DATA_ACQUISITION,
            phase_number=2,
            desires=data_desires,
        ))

        # Phase 3: TOOL_BUILDING
        tool_desires = [
            CascadeDesire(
                id=f"cd_{uuid.uuid4().hex[:8]}",
                description=f"Build tool: {gap.description}",
                priority=int(gap.severity * 10),
            )
            for gap in gaps if gap.area == "tools"
        ]
        if not tool_desires:
            tool_desires = [
                CascadeDesire(
                    id=f"cd_{uuid.uuid4().hex[:8]}",
                    description="Build required analysis tools",
                    priority=5,
                )
            ]
        phases.append(CascadePhase(
            id=f"phase_{uuid.uuid4().hex[:8]}",
            name=PhaseName.TOOL_BUILDING,
            phase_number=3,
            desires=tool_desires,
        ))

        # Phase 4: INTEGRATION
        phases.append(CascadePhase(
            id=f"phase_{uuid.uuid4().hex[:8]}",
            name=PhaseName.INTEGRATION,
            phase_number=4,
            desires=[
                CascadeDesire(
                    id=f"cd_{uuid.uuid4().hex[:8]}",
                    description="Integrate tools and data into cohesive solution",
                    priority=5,
                )
            ],
        ))

        # Phase 5: VALIDATION
        phases.append(CascadePhase(
            id=f"phase_{uuid.uuid4().hex[:8]}",
            name=PhaseName.VALIDATION,
            phase_number=5,
            desires=[
                CascadeDesire(
                    id=f"cd_{uuid.uuid4().hex[:8]}",
                    description="Validate solution with human feedback",
                    priority=5,
                )
            ],
            human_requests=[
                HumanRequest(
                    id=f"hip_{uuid.uuid4().hex[:8]}",
                    type=InteractionType.VALIDATION,
                    question="Does this solution meet your needs?",
                    context="Final validation of the complete solution",
                    blocking=True,
                )
            ],
        ))

        return DesireTree(
            id=cascade_id,
            root_goal=goal,
            phases=phases,
            human_requester=requester,
            status=CascadeStatus.PENDING,
        )

    async def execute_phase(self, phase: CascadePhase, tree: DesireTree) -> PhaseResult:
        """
        Execute a phase of the goal cascade.

        May pause for human input if needed.

        Args:
            phase: The phase to execute
            tree: The full desire tree

        Returns:
            PhaseResult with status and artifacts
        """
        phase.status = PhaseStatus.IN_PROGRESS
        phase.started_at = datetime.now()
        tree.updated_at = datetime.now()

        # Update tree status
        tree.status = CascadeStatus.IN_PROGRESS

        # Persist the update
        await self._update_phase_status(tree.id, phase.id, PhaseStatus.IN_PROGRESS)

        # Check for blocking human requests
        for hr in phase.human_requests:
            if hr.blocking and hr.status == "pending":
                phase.status = PhaseStatus.BLOCKED
                phase.blocking_reason = f"Waiting for human: {hr.question}"
                await self._record_human_interaction(phase.id, hr)
                return PhaseResult(
                    phase_id=phase.id,
                    status="blocked",
                    summary=f"Blocked: {phase.blocking_reason}",
                    human_request=hr,
                )

        # Execute each desire in the phase
        artifacts = []
        for desire in phase.desires:
            if desire.status != "completed":
                desire.attempts += 1
                # Here we would actually execute the desire
                # For now, mark as completed (actual execution would go through Seeker)
                desire.status = "completed"
                desire.result = f"Completed: {desire.description}"

        # Phase completed
        phase.status = PhaseStatus.COMPLETED
        phase.completed_at = datetime.now()
        phase.summary = f"Completed phase {phase.name.value}"

        # Advance to next phase
        tree.current_phase += 1
        tree.updated_at = datetime.now()

        # Persist completion
        await self._persist_phase_completion(tree.id, phase.id, phase.summary)

        # Check if cascade is complete
        if tree.current_phase >= len(tree.phases):
            tree.status = CascadeStatus.COMPLETED

        return PhaseResult(
            phase_id=phase.id,
            status="completed",
            summary=phase.summary,
            artifacts=artifacts,
        )

    def identify_human_help_needed(self, phase: CascadePhase) -> Optional[HumanRequest]:
        """
        Recognize when human assistance would help.

        Args:
            phase: The current phase

        Returns:
            HumanRequest if help needed, None otherwise
        """
        # Check if phase has unfulfilled human requests
        for hr in phase.human_requests:
            if hr.status == "pending":
                return hr

        # Check for common help scenarios
        if phase.name == PhaseName.DATA_ACQUISITION:
            # May need credentials
            return HumanRequest(
                id=f"hip_{uuid.uuid4().hex[:8]}",
                type=InteractionType.CREDENTIALS,
                question="Do you have API credentials or data access I could use?",
                context=f"Working on {phase.name.value} phase",
                blocking=False,
            )

        if phase.name == PhaseName.VALIDATION:
            return HumanRequest(
                id=f"hip_{uuid.uuid4().hex[:8]}",
                type=InteractionType.VALIDATION,
                question="Does this meet your requirements?",
                context=f"Completed solution ready for validation",
                blocking=True,
            )

        return None

    async def provide_human_response(self, tree_id: str, request_id: str, response: str) -> bool:
        """
        Record a human response to a request.

        Args:
            tree_id: The cascade ID
            request_id: The human request ID
            response: The human's response

        Returns:
            True if successful
        """
        tree = self._active_cascades.get(tree_id)
        if not tree:
            return False

        for phase in tree.phases:
            for hr in phase.human_requests:
                if hr.id == request_id:
                    hr.status = "answered"
                    hr.response = response
                    hr.answered_at = datetime.now()

                    # Unblock phase if this was blocking
                    if hr.blocking and phase.status == PhaseStatus.BLOCKED:
                        phase.status = PhaseStatus.IN_PROGRESS
                        phase.blocking_reason = None

                    # Persist the update
                    await self._update_human_interaction(request_id, response)

                    return True

        return False

    # Neo4j Persistence Methods

    async def _persist_cascade(self, tree: DesireTree):
        """Persist a new cascade to Neo4j."""
        if not self.memory:
            return

        try:
            # Create GoalCascade node
            await self.memory.query("""
                CREATE (gc:GoalCascade {
                    id: $id,
                    root_goal: $root_goal,
                    status: $status,
                    current_phase: $current_phase,
                    total_phases: $total_phases,
                    created_at: datetime(),
                    updated_at: datetime(),
                    human_requester: $human_requester,
                    originating_desire_id: $desire_id
                })
            """, {
                "id": tree.id,
                "root_goal": tree.root_goal,
                "status": tree.status.value,
                "current_phase": tree.current_phase,
                "total_phases": tree.total_phases,
                "human_requester": tree.human_requester,
                "desire_id": tree.originating_desire_id,
            })

            # Create phase nodes
            for phase in tree.phases:
                await self.memory.query("""
                    MATCH (gc:GoalCascade {id: $cascade_id})
                    CREATE (p:CascadePhase {
                        id: $phase_id,
                        name: $name,
                        phase_number: $phase_number,
                        status: $status
                    })
                    CREATE (gc)-[:HAS_PHASE]->(p)
                """, {
                    "cascade_id": tree.id,
                    "phase_id": phase.id,
                    "name": phase.name.value,
                    "phase_number": phase.phase_number,
                    "status": phase.status.value,
                })

                # Create desire nodes
                for desire in phase.desires:
                    await self.memory.query("""
                        MATCH (p:CascadePhase {id: $phase_id})
                        CREATE (d:CascadeDesire {
                            id: $desire_id,
                            description: $description,
                            status: $status,
                            priority: $priority
                        })
                        CREATE (p)-[:HAS_DESIRE]->(d)
                    """, {
                        "phase_id": phase.id,
                        "desire_id": desire.id,
                        "description": desire.description,
                        "status": desire.status,
                        "priority": desire.priority,
                    })

            # Create phase links (NEXT_PHASE)
            for i in range(len(tree.phases) - 1):
                await self.memory.query("""
                    MATCH (p1:CascadePhase {id: $from_id})
                    MATCH (p2:CascadePhase {id: $to_id})
                    CREATE (p1)-[:NEXT_PHASE]->(p2)
                """, {
                    "from_id": tree.phases[i].id,
                    "to_id": tree.phases[i + 1].id,
                })

            logger.info(f"Persisted cascade {tree.id} to Neo4j")

        except Exception as e:
            logger.error(f"Error persisting cascade: {e}")

    async def _find_resumable(self, goal: str) -> Optional[Dict]:
        """Find a cascade that can be resumed."""
        if not self.memory:
            return None

        try:
            result = await self.memory.query("""
                MATCH (gc:GoalCascade)
                WHERE gc.status IN ['in_progress', 'blocked']
                  AND gc.root_goal = $goal
                  AND gc.updated_at > datetime() - duration('P7D')
                RETURN gc
                ORDER BY gc.updated_at DESC
                LIMIT 1
            """, {"goal": goal})

            if result and len(result) > 0:
                return result[0].get("gc")

        except Exception as e:
            logger.error(f"Error finding resumable cascade: {e}")

        return None

    async def _reconstruct_tree(self, cascade_data: Dict) -> DesireTree:
        """Reconstruct a DesireTree from Neo4j data."""
        cascade_id = cascade_data.get("id")

        # Get phases
        phases_data = await self.memory.query("""
            MATCH (gc:GoalCascade {id: $id})-[:HAS_PHASE]->(p:CascadePhase)
            RETURN p
            ORDER BY p.phase_number
        """, {"id": cascade_id})

        phases = []
        for pd in phases_data:
            phase_data = pd.get("p", {})
            phase_id = phase_data.get("id")

            # Get desires for this phase
            desires_data = await self.memory.query("""
                MATCH (p:CascadePhase {id: $phase_id})-[:HAS_DESIRE]->(d:CascadeDesire)
                RETURN d
            """, {"phase_id": phase_id})

            desires = [
                CascadeDesire(
                    id=d.get("d", {}).get("id"),
                    description=d.get("d", {}).get("description", ""),
                    status=d.get("d", {}).get("status", "pending"),
                    priority=d.get("d", {}).get("priority", 1),
                )
                for d in desires_data
            ]

            phases.append(CascadePhase(
                id=phase_id,
                name=PhaseName(phase_data.get("name", "RESEARCH")),
                phase_number=phase_data.get("phase_number", 1),
                status=PhaseStatus(phase_data.get("status", "pending")),
                desires=desires,
            ))

        tree = DesireTree(
            id=cascade_id,
            root_goal=cascade_data.get("root_goal", ""),
            phases=phases,
            current_phase=cascade_data.get("current_phase", 0),
            status=CascadeStatus(cascade_data.get("status", "pending")),
            human_requester=cascade_data.get("human_requester", "unknown"),
        )

        # Track locally
        self._active_cascades[cascade_id] = tree

        return tree

    async def _persist_phase_completion(self, cascade_id: str, phase_id: str, summary: str):
        """Persist phase completion to Neo4j."""
        if not self.memory:
            return

        try:
            await self.memory.query("""
                MATCH (gc:GoalCascade {id: $cascade_id})
                MATCH (p:CascadePhase {id: $phase_id})
                SET p.status = 'completed',
                    p.completed_at = datetime(),
                    p.summary = $summary,
                    gc.current_phase = gc.current_phase + 1,
                    gc.updated_at = datetime()
            """, {
                "cascade_id": cascade_id,
                "phase_id": phase_id,
                "summary": summary,
            })
        except Exception as e:
            logger.error(f"Error persisting phase completion: {e}")

    async def _update_phase_status(self, cascade_id: str, phase_id: str, status: PhaseStatus):
        """Update phase status in Neo4j."""
        if not self.memory:
            return

        try:
            await self.memory.query("""
                MATCH (gc:GoalCascade {id: $cascade_id})
                MATCH (p:CascadePhase {id: $phase_id})
                SET p.status = $status,
                    gc.updated_at = datetime()
            """, {
                "cascade_id": cascade_id,
                "phase_id": phase_id,
                "status": status.value,
            })
        except Exception as e:
            logger.error(f"Error updating phase status: {e}")

    async def _record_human_interaction(self, phase_id: str, hr: HumanRequest):
        """Record a human interaction point in Neo4j."""
        if not self.memory:
            return

        try:
            await self.memory.query("""
                MATCH (p:CascadePhase {id: $phase_id})
                CREATE (hip:HumanInteractionPoint {
                    id: $id,
                    type: $type,
                    question: $question,
                    status: $status,
                    asked_at: datetime()
                })
                CREATE (p)-[:REQUIRES_HUMAN]->(hip)
                SET p.status = 'blocked',
                    p.blocking_reason = 'Waiting for human: ' + $question
            """, {
                "phase_id": phase_id,
                "id": hr.id,
                "type": hr.type.value,
                "question": hr.question,
                "status": hr.status,
            })
        except Exception as e:
            logger.error(f"Error recording human interaction: {e}")

    async def _update_human_interaction(self, request_id: str, response: str):
        """Update a human interaction response in Neo4j."""
        if not self.memory:
            return

        try:
            await self.memory.query("""
                MATCH (hip:HumanInteractionPoint {id: $id})
                SET hip.status = 'answered',
                    hip.response = $response,
                    hip.answered_at = datetime()
            """, {
                "id": request_id,
                "response": response,
            })
        except Exception as e:
            logger.error(f"Error updating human interaction: {e}")

    async def find_resumable_cascades(self) -> List[Dict]:
        """Find all resumable cascades for startup recovery."""
        if not self.memory:
            return []

        try:
            result = await self.memory.query("""
                MATCH (gc:GoalCascade)
                WHERE gc.status IN ['in_progress', 'blocked']
                  AND gc.updated_at > datetime() - duration('P7D')
                RETURN gc.id as id, gc.root_goal as root_goal,
                       gc.current_phase as current_phase, gc.total_phases as total_phases,
                       gc.status as status
                ORDER BY gc.updated_at DESC
                LIMIT 10
            """)
            return result if result else []
        except Exception as e:
            logger.error(f"Error finding resumable cascades: {e}")
            return []

    async def resume_pending_cascades(self) -> int:
        """
        Resume all pending cascades on startup.

        Called by byrd.py during startup to restore in-progress work.

        Returns:
            Number of cascades resumed
        """
        resumable = await self.find_resumable_cascades()
        resumed_count = 0

        for cascade_info in resumable:
            try:
                cascade_id = cascade_info.get("id")
                if cascade_id in self._active_cascades:
                    # Already loaded
                    continue

                # Fetch full cascade data
                result = await self.memory.query("""
                    MATCH (gc:GoalCascade {id: $id})
                    RETURN gc
                """, {"id": cascade_id})

                if result and len(result) > 0:
                    cascade_data = result[0].get("gc", {})
                    tree = await self._reconstruct_tree(cascade_data)
                    logger.info(
                        f"Resumed cascade {cascade_id}: "
                        f"phase {tree.current_phase}/{tree.total_phases} - {tree.root_goal[:50]}..."
                    )
                    resumed_count += 1

            except Exception as e:
                logger.error(f"Error resuming cascade {cascade_info.get('id')}: {e}")

        return resumed_count

    @classmethod
    def is_complex_task(cls, text: str) -> bool:
        """Check if text represents a complex task."""
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in cls.COMPLEX_PATTERNS)

    def get_active_cascades(self) -> Dict[str, DesireTree]:
        """Get all locally tracked active cascades."""
        return self._active_cascades.copy()

    def reset(self):
        """Reset the goal cascade state."""
        self._active_cascades = {}
        self._cascade_count = 0


# Convenience function
def create_goal_cascade(config: Dict = None, memory=None, llm_client=None) -> GoalCascade:
    """Create a new GoalCascade instance."""
    return GoalCascade(config=config, memory=memory, llm_client=llm_client)

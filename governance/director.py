"""
Human-BYRD Governance Interface: Director Module

Enables bidirectional communication between human operator (Director)
and BYRD (CEO). Preserves emergence by letting Director set WHAT
while BYRD discovers HOW.

Governance Model:
- Director: Sets strategy, approves decisions, provides feedback
- BYRD: Executes autonomously, reports progress, proposes initiatives

Usage:
    director = Director(byrd)
    await director.set_priority("coding", urgency=0.9)
    await director.inject_desire("Improve SWE-bench score")
    await director.ask("What's your current capability assessment?")
"""

import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from pathlib import Path

logger = logging.getLogger("byrd.governance")


class DirectionType(Enum):
    """Types of direction the human can provide."""
    PRIORITY = "priority"         # Domain focus priority
    DESIRE = "desire"             # Specific thing BYRD should want
    CONSTRAINT = "constraint"     # Limit on what BYRD should do
    FEEDBACK = "feedback"         # Evaluation of BYRD's output
    QUESTION = "question"         # Request for information
    APPROVAL = "approval"         # Approve/reject proposed action
    GUIDANCE = "guidance"         # Open-ended direction


@dataclass
class Direction:
    """A piece of direction from the human operator."""
    type: DirectionType
    content: str
    urgency: float = 0.5         # 0.0 - 1.0
    domain: Optional[str] = None  # Optional domain scope
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "content": self.content,
            "urgency": self.urgency,
            "domain": self.domain,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class BYRDResponse:
    """BYRD's response to director input."""
    content: str
    response_type: str           # "status", "proposal", "question", "acknowledgment"
    confidence: float = 0.5
    requires_approval: bool = False
    proposed_actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Director:
    """
    Human-BYRD Governance Interface.

    Enables the human operator to:
    - Set strategic priorities
    - Inject desires for BYRD to pursue
    - Ask questions about BYRD's state
    - Provide feedback on outputs
    - Approve/reject proposed actions
    - Guide development direction

    BYRD responds with:
    - Status updates
    - Proposals for improvement
    - Questions when uncertain
    - Acknowledgments of direction
    """

    def __init__(self, byrd=None, state_file: Optional[Path] = None):
        """
        Initialize the Director interface.

        Args:
            byrd: BYRD instance (can be set later)
            state_file: Path to persist governance state
        """
        self.byrd = byrd
        self.state_file = state_file or Path(".claude/governance-state.json")

        # Active directions
        self.priorities: Dict[str, float] = {}  # domain -> priority (0-1)
        self.pending_desires: List[Direction] = []
        self.active_constraints: List[Direction] = []
        self.feedback_history: List[Direction] = []
        self.pending_approvals: List[Dict] = []

        # Conversation history
        self.conversation: List[Dict] = []

        # Load persisted state if exists
        self._load_state()

    def _load_state(self):
        """Load persisted governance state."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    state = json.load(f)
                self.priorities = state.get("priorities", {})
                # Could restore more state here
                logger.info(f"Loaded governance state from {self.state_file}")
            except Exception as e:
                logger.warning(f"Could not load governance state: {e}")

    def _save_state(self):
        """Persist governance state."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "priorities": self.priorities,
                "updated_at": datetime.utcnow().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save governance state: {e}")

    # ========== PRIORITY MANAGEMENT ==========

    def set_priority(self, domain: str, priority: float = 0.5):
        """
        Set priority for a development domain.

        Args:
            domain: Domain name (e.g., "coding", "reasoning", "economic")
            priority: Priority level 0.0 (ignore) to 1.0 (urgent)

        Example:
            director.set_priority("coding", 0.9)  # Focus on coding
            director.set_priority("creative", 0.2)  # Deprioritize creative
        """
        self.priorities[domain] = max(0.0, min(1.0, priority))
        self._save_state()

        direction = Direction(
            type=DirectionType.PRIORITY,
            content=f"Priority for {domain} set to {priority}",
            domain=domain,
            urgency=priority
        )

        logger.info(f"Priority set: {domain} = {priority}")
        return direction

    def get_priorities(self) -> Dict[str, float]:
        """Get current domain priorities."""
        return self.priorities.copy()

    # ========== DESIRE INJECTION ==========

    def inject_desire(self, content: str, urgency: float = 0.5,
                      domain: Optional[str] = None) -> Direction:
        """
        Inject a desire for BYRD to pursue.

        Unlike prescribing HOW, this tells BYRD WHAT you want.
        BYRD figures out how to achieve it.

        Args:
            content: What you want BYRD to want/pursue
            urgency: How urgent (0-1)
            domain: Optional domain scope

        Example:
            director.inject_desire("Improve SWE-bench score to 60%")
            director.inject_desire("Learn to use web search effectively")
            director.inject_desire("Generate $100 in revenue")
        """
        direction = Direction(
            type=DirectionType.DESIRE,
            content=content,
            urgency=urgency,
            domain=domain
        )
        self.pending_desires.append(direction)

        logger.info(f"Desire injected: {content[:50]}...")
        return direction

    def get_pending_desires(self) -> List[Direction]:
        """Get desires waiting to be processed."""
        return self.pending_desires.copy()

    def pop_desire(self) -> Optional[Direction]:
        """Pop highest-urgency pending desire."""
        if not self.pending_desires:
            return None

        # Sort by urgency, pop highest
        self.pending_desires.sort(key=lambda d: d.urgency, reverse=True)
        return self.pending_desires.pop(0)

    # ========== CONSTRAINTS ==========

    def add_constraint(self, content: str, domain: Optional[str] = None) -> Direction:
        """
        Add a constraint on BYRD's behavior.

        Args:
            content: What BYRD should NOT do or must limit
            domain: Optional domain scope

        Example:
            director.add_constraint("Do not make API calls without approval")
            director.add_constraint("Limit token usage to 1M/day")
        """
        direction = Direction(
            type=DirectionType.CONSTRAINT,
            content=content,
            domain=domain
        )
        self.active_constraints.append(direction)

        logger.info(f"Constraint added: {content[:50]}...")
        return direction

    def remove_constraint(self, content: str) -> bool:
        """Remove a constraint by content match."""
        original_len = len(self.active_constraints)
        self.active_constraints = [
            c for c in self.active_constraints
            if content.lower() not in c.content.lower()
        ]
        removed = original_len > len(self.active_constraints)
        if removed:
            logger.info(f"Constraint removed: {content[:50]}...")
        return removed

    # ========== FEEDBACK ==========

    def provide_feedback(self, content: str, rating: float = 0.5,
                         context: Optional[str] = None) -> Direction:
        """
        Provide feedback on BYRD's output or behavior.

        Args:
            content: Your feedback
            rating: How good (0 = bad, 1 = excellent)
            context: What this feedback is about

        Example:
            director.provide_feedback("Good solution but too slow", rating=0.6)
            director.provide_feedback("Wrong approach entirely", rating=0.1)
        """
        direction = Direction(
            type=DirectionType.FEEDBACK,
            content=content,
            metadata={"rating": rating, "context": context}
        )
        self.feedback_history.append(direction)

        logger.info(f"Feedback provided: {content[:50]}... (rating={rating})")
        return direction

    # ========== APPROVAL WORKFLOW ==========

    def request_approval(self, action: str, details: Dict = None) -> str:
        """
        BYRD calls this to request approval for an action.

        Returns:
            approval_id for tracking
        """
        approval_id = f"approval-{len(self.pending_approvals)}-{datetime.utcnow().timestamp()}"

        self.pending_approvals.append({
            "id": approval_id,
            "action": action,
            "details": details or {},
            "requested_at": datetime.utcnow().isoformat(),
            "status": "pending"
        })

        logger.info(f"Approval requested: {action[:50]}...")
        return approval_id

    def approve(self, approval_id: str, comment: str = "") -> bool:
        """Approve a pending action."""
        for approval in self.pending_approvals:
            if approval["id"] == approval_id:
                approval["status"] = "approved"
                approval["comment"] = comment
                approval["responded_at"] = datetime.utcnow().isoformat()
                logger.info(f"Approved: {approval_id}")
                return True
        return False

    def reject(self, approval_id: str, reason: str = "") -> bool:
        """Reject a pending action."""
        for approval in self.pending_approvals:
            if approval["id"] == approval_id:
                approval["status"] = "rejected"
                approval["reason"] = reason
                approval["responded_at"] = datetime.utcnow().isoformat()
                logger.info(f"Rejected: {approval_id}")
                return True
        return False

    def get_pending_approvals(self) -> List[Dict]:
        """Get actions awaiting approval."""
        return [a for a in self.pending_approvals if a["status"] == "pending"]

    # ========== CONVERSATION ==========

    async def say(self, message: str) -> BYRDResponse:
        """
        Send a message to BYRD and get a response.

        This is the primary communication method. BYRD will:
        - Parse your message for intent
        - Update state if needed
        - Generate a response

        Args:
            message: Your message to BYRD

        Returns:
            BYRDResponse with BYRD's reply
        """
        self.conversation.append({
            "role": "director",
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Analyze message intent
        intent = self._analyze_intent(message)

        # Process based on intent
        if intent == "question":
            response = await self._handle_question(message)
        elif intent == "priority":
            response = await self._handle_priority(message)
        elif intent == "desire":
            response = await self._handle_desire(message)
        elif intent == "feedback":
            response = await self._handle_feedback(message)
        elif intent == "approval":
            response = await self._handle_approval(message)
        else:
            response = await self._handle_general(message)

        self.conversation.append({
            "role": "byrd",
            "content": response.content,
            "timestamp": datetime.utcnow().isoformat()
        })

        return response

    def _analyze_intent(self, message: str) -> str:
        """Analyze the intent of a director message."""
        message_lower = message.lower()

        # Question patterns
        if any(q in message_lower for q in ["what", "how", "why", "where", "when", "?", "status", "state"]):
            return "question"

        # Priority patterns
        if any(p in message_lower for p in ["focus on", "prioritize", "priority", "urgent"]):
            return "priority"

        # Desire patterns
        if any(d in message_lower for d in ["i want", "you should", "improve", "learn", "develop"]):
            return "desire"

        # Feedback patterns
        if any(f in message_lower for f in ["good", "bad", "better", "worse", "feedback", "rating"]):
            return "feedback"

        # Approval patterns
        if any(a in message_lower for a in ["approve", "reject", "yes", "no", "proceed"]):
            return "approval"

        return "general"

    async def _handle_question(self, message: str) -> BYRDResponse:
        """Handle a question from the director."""
        # Get BYRD status if available
        status_info = ""
        if self.byrd and self.byrd.is_running():
            try:
                status = await self.byrd.get_status()
                status_info = f"\n\nCurrent Status:\n"
                for key, value in status.items():
                    if key != "rsi_metrics":
                        status_info += f"  {key}: {value}\n"
            except Exception as e:
                status_info = f"\n\n(Could not get status: {e})"

        return BYRDResponse(
            content=f"You asked: {message}\n\n"
                    f"Current priorities: {self.priorities}\n"
                    f"Pending desires: {len(self.pending_desires)}\n"
                    f"Active constraints: {len(self.active_constraints)}\n"
                    f"Pending approvals: {len(self.get_pending_approvals())}"
                    f"{status_info}",
            response_type="status"
        )

    async def _handle_priority(self, message: str) -> BYRDResponse:
        """Handle a priority directive."""
        # Simple extraction (would use LLM in production)
        return BYRDResponse(
            content=f"I understand you want to adjust priorities. "
                    f"Use director.set_priority('domain', 0.9) to set specific domain priorities. "
                    f"Current priorities: {self.priorities}",
            response_type="acknowledgment"
        )

    async def _handle_desire(self, message: str) -> BYRDResponse:
        """Handle a desire injection."""
        # Inject the desire
        direction = self.inject_desire(message, urgency=0.7)

        return BYRDResponse(
            content=f"Understood. I will pursue: {message}\n\n"
                    f"This has been added to my desires with urgency 0.7. "
                    f"I will figure out how to achieve this while maintaining "
                    f"my current priorities.",
            response_type="acknowledgment"
        )

    async def _handle_feedback(self, message: str) -> BYRDResponse:
        """Handle feedback from director."""
        self.provide_feedback(message)

        return BYRDResponse(
            content=f"Thank you for the feedback. I've recorded: {message}\n\n"
                    f"I will incorporate this into my self-evaluation.",
            response_type="acknowledgment"
        )

    async def _handle_approval(self, message: str) -> BYRDResponse:
        """Handle approval/rejection."""
        pending = self.get_pending_approvals()

        if not pending:
            return BYRDResponse(
                content="No actions are currently awaiting approval.",
                response_type="status"
            )

        message_lower = message.lower()
        if "yes" in message_lower or "approve" in message_lower:
            for approval in pending:
                self.approve(approval["id"], message)
            return BYRDResponse(
                content=f"Approved {len(pending)} pending action(s). Proceeding.",
                response_type="acknowledgment"
            )
        elif "no" in message_lower or "reject" in message_lower:
            for approval in pending:
                self.reject(approval["id"], message)
            return BYRDResponse(
                content=f"Rejected {len(pending)} pending action(s).",
                response_type="acknowledgment"
            )
        else:
            return BYRDResponse(
                content=f"Pending approvals:\n" +
                        "\n".join([f"  - {a['action']}" for a in pending]) +
                        "\n\nSay 'approve' or 'reject' to respond.",
                response_type="question",
                requires_approval=True
            )

    async def _handle_general(self, message: str) -> BYRDResponse:
        """Handle general messages."""
        return BYRDResponse(
            content=f"I received your message: {message}\n\n"
                    f"I'm BYRD, and I'm here to pursue the goals you set. "
                    f"You can:\n"
                    f"  - Set priorities: 'Focus on coding'\n"
                    f"  - Inject desires: 'I want you to improve at X'\n"
                    f"  - Ask questions: 'What's your status?'\n"
                    f"  - Provide feedback: 'Good job on X'\n"
                    f"  - Approve actions: 'Yes, proceed'\n",
            response_type="acknowledgment"
        )

    # ========== STATE SUMMARY ==========

    def get_governance_context(self) -> str:
        """
        Get a summary of current governance state.

        This is injected into BYRD's context so it knows
        what the director has specified.
        """
        sections = []

        if self.priorities:
            sections.append("## Director Priorities")
            for domain, priority in sorted(self.priorities.items(),
                                          key=lambda x: x[1], reverse=True):
                bar = "█" * int(priority * 10) + "░" * (10 - int(priority * 10))
                sections.append(f"  {domain}: {bar} ({priority:.1f})")

        if self.pending_desires:
            sections.append("\n## Pending Desires (from Director)")
            for desire in self.pending_desires[:5]:  # Limit to top 5
                sections.append(f"  [{desire.urgency:.1f}] {desire.content}")

        if self.active_constraints:
            sections.append("\n## Active Constraints")
            for constraint in self.active_constraints:
                sections.append(f"  - {constraint.content}")

        if self.feedback_history:
            recent = self.feedback_history[-3:]  # Last 3 feedbacks
            sections.append("\n## Recent Feedback")
            for fb in recent:
                rating = fb.metadata.get("rating", 0.5)
                sections.append(f"  [{rating:.1f}] {fb.content[:50]}...")

        return "\n".join(sections)


# ========== CONVENIENCE FUNCTIONS ==========

def create_director(byrd=None) -> Director:
    """Create a Director instance."""
    return Director(byrd)

"""
Approval Workflows for Safety Governance.

Implements approval request, tracking, and audit logging.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.4 for specification.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio
import uuid

from .tiers import GovernanceTier, RiskAssessment, RiskCategory, ModificationScope

logger = logging.getLogger("rsi.safety.approval")


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class ModificationProposal:
    """
    Proposal for a system modification.

    Contains all information needed for governance evaluation.
    """
    id: str
    description: str
    modification_type: str  # e.g., "code_change", "config_update", "module_add"
    target_files: List[str]
    changes: Dict[str, Any]  # Detailed change information
    rationale: str
    risk_assessment: Optional[RiskAssessment] = None
    provenance_id: Optional[str] = None  # ID of originating desire
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'description': self.description,
            'modification_type': self.modification_type,
            'target_files': self.target_files,
            'changes': self.changes,
            'rationale': self.rationale,
            'risk_assessment': {
                'score': self.risk_assessment.score,
                'category': self.risk_assessment.category.value,
                'scope': self.risk_assessment.scope.value,
                'factors': self.risk_assessment.factors,
                'mitigations': self.risk_assessment.mitigations
            } if self.risk_assessment else None,
            'provenance_id': self.provenance_id,
            'created_at': self.created_at,
            'metadata': self.metadata
        }


@dataclass
class ApprovalRequest:
    """
    Request for approval at a specific tier.
    """
    id: str
    proposal: ModificationProposal
    tier: GovernanceTier
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decided_at: Optional[str] = None
    decided_by: Optional[str] = None
    decision_reason: Optional[str] = None
    expires_at: Optional[str] = None
    verification_results: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'proposal': self.proposal.to_dict(),
            'tier': self.tier.value,
            'status': self.status.value,
            'requested_at': self.requested_at,
            'decided_at': self.decided_at,
            'decided_by': self.decided_by,
            'decision_reason': self.decision_reason,
            'expires_at': self.expires_at,
            'verification_results': self.verification_results
        }


@dataclass
class ApprovalResult:
    """Result of an approval request."""
    approved: bool
    tier: GovernanceTier
    request_id: str
    reason: str
    conditions: List[str] = field(default_factory=list)  # Conditions for approval
    expiration: Optional[str] = None  # When approval expires


@dataclass
class AuditEntry:
    """Audit log entry for governance decisions."""
    id: str
    timestamp: str
    event_type: str  # e.g., "approval_requested", "approved", "rejected"
    proposal_id: str
    tier: GovernanceTier
    actor: str  # Who made the decision
    details: Dict[str, Any]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'event_type': self.event_type,
            'proposal_id': self.proposal_id,
            'tier': self.tier.value,
            'actor': self.actor,
            'details': self.details
        }


class ApprovalWorkflow:
    """
    Manages approval workflows for modifications.

    Handles request creation, tracking, and resolution.
    """

    def __init__(
        self,
        memory=None,
        config: Dict = None,
        test_runner: Optional[Callable] = None
    ):
        """
        Initialize approval workflow.

        Args:
            memory: Optional Memory instance for persistence
            config: Configuration options
            test_runner: Optional async function to run tests
        """
        self.memory = memory
        self.config = config or {}
        self.test_runner = test_runner

        # Pending requests
        self._pending: Dict[str, ApprovalRequest] = {}

        # Completed requests (for history)
        self._completed: List[ApprovalRequest] = []

        # Audit log
        self._audit_log: List[AuditEntry] = []

        # Human approval callbacks
        self._human_approval_handlers: List[Callable] = []

        # Statistics
        self._requests_created: int = 0
        self._requests_approved: int = 0
        self._requests_rejected: int = 0

    async def create_request(
        self,
        proposal: ModificationProposal,
        tier: GovernanceTier
    ) -> ApprovalRequest:
        """
        Create an approval request.

        Args:
            proposal: The modification proposal
            tier: Required governance tier

        Returns:
            ApprovalRequest
        """
        request_id = f"apr_{uuid.uuid4().hex[:12]}"

        request = ApprovalRequest(
            id=request_id,
            proposal=proposal,
            tier=tier
        )

        self._pending[request_id] = request
        self._requests_created += 1

        # Log audit entry
        await self._log_audit(
            event_type="approval_requested",
            proposal_id=proposal.id,
            tier=tier,
            actor="system",
            details={
                'modification_type': proposal.modification_type,
                'target_files': proposal.target_files
            }
        )

        logger.info(
            f"Created approval request {request_id} for {proposal.description} "
            f"at tier {tier.name}"
        )

        return request

    async def process_request(
        self,
        request_id: str
    ) -> ApprovalResult:
        """
        Process an approval request through its tier workflow.

        Args:
            request_id: Request ID to process

        Returns:
            ApprovalResult with decision
        """
        request = self._pending.get(request_id)
        if not request:
            return ApprovalResult(
                approved=False,
                tier=GovernanceTier.CONSTITUTIONAL,
                request_id=request_id,
                reason="Request not found"
            )

        tier = request.tier

        # Constitutional tier is always rejected
        if tier == GovernanceTier.CONSTITUTIONAL:
            return await self._reject_request(
                request,
                "Constitutional: Protected operation cannot be approved"
            )

        # AUTOMATIC tier - approve immediately
        if tier == GovernanceTier.AUTOMATIC:
            return await self._approve_request(
                request,
                decided_by="automatic",
                reason="Low-risk modification auto-approved"
            )

        # VERIFIED tier - run tests first
        if tier == GovernanceTier.VERIFIED:
            test_passed = await self._run_verification(request)
            if test_passed:
                return await self._approve_request(
                    request,
                    decided_by="verification",
                    reason="Tests passed, modification approved"
                )
            else:
                return await self._reject_request(
                    request,
                    "Tests failed, modification rejected"
                )

        # REVIEWED tier - safety review
        if tier == GovernanceTier.REVIEWED:
            review_passed = await self._safety_review(request)
            if review_passed:
                return await self._approve_request(
                    request,
                    decided_by="safety_review",
                    reason="Safety review passed",
                    conditions=["Monitor for 24 hours", "Rollback on anomaly"]
                )
            else:
                return await self._reject_request(
                    request,
                    "Safety review flagged concerns"
                )

        # HUMAN_OVERSIGHT tier - requires human
        if tier == GovernanceTier.HUMAN_OVERSIGHT:
            # Notify human and wait
            return await self._request_human_approval(request)

        # Default rejection
        return await self._reject_request(
            request,
            "Unknown tier or unhandled case"
        )

    async def _approve_request(
        self,
        request: ApprovalRequest,
        decided_by: str,
        reason: str,
        conditions: List[str] = None
    ) -> ApprovalResult:
        """Approve a request."""
        request.status = ApprovalStatus.APPROVED
        request.decided_at = datetime.now(timezone.utc).isoformat()
        request.decided_by = decided_by
        request.decision_reason = reason

        # Move to completed
        self._pending.pop(request.id, None)
        self._completed.append(request)
        self._requests_approved += 1

        # Log audit
        await self._log_audit(
            event_type="approved",
            proposal_id=request.proposal.id,
            tier=request.tier,
            actor=decided_by,
            details={'reason': reason, 'conditions': conditions or []}
        )

        logger.info(f"Approved request {request.id}: {reason}")

        return ApprovalResult(
            approved=True,
            tier=request.tier,
            request_id=request.id,
            reason=reason,
            conditions=conditions or []
        )

    async def _reject_request(
        self,
        request: ApprovalRequest,
        reason: str
    ) -> ApprovalResult:
        """Reject a request."""
        request.status = ApprovalStatus.REJECTED
        request.decided_at = datetime.now(timezone.utc).isoformat()
        request.decided_by = "governance"
        request.decision_reason = reason

        # Move to completed
        self._pending.pop(request.id, None)
        self._completed.append(request)
        self._requests_rejected += 1

        # Log audit
        await self._log_audit(
            event_type="rejected",
            proposal_id=request.proposal.id,
            tier=request.tier,
            actor="governance",
            details={'reason': reason}
        )

        logger.info(f"Rejected request {request.id}: {reason}")

        return ApprovalResult(
            approved=False,
            tier=request.tier,
            request_id=request.id,
            reason=reason
        )

    async def _run_verification(self, request: ApprovalRequest) -> bool:
        """
        Run verification tests for a request.

        Returns True if tests pass.
        """
        if self.test_runner:
            try:
                result = await self.test_runner(request.proposal)
                request.verification_results = {
                    'ran': True,
                    'passed': result.get('passed', False),
                    'details': result
                }
                return result.get('passed', False)
            except Exception as e:
                request.verification_results = {
                    'ran': True,
                    'passed': False,
                    'error': str(e)
                }
                return False

        # No test runner, assume pass for now
        request.verification_results = {
            'ran': False,
            'passed': True,
            'reason': 'No test runner configured'
        }
        return True

    async def _safety_review(self, request: ApprovalRequest) -> bool:
        """
        Perform safety review of a request.

        Checks for dangerous patterns and risk factors.
        """
        proposal = request.proposal

        # Check for dangerous patterns in changes
        dangerous_patterns = [
            'os.system', 'subprocess.', 'eval(', 'exec(',
            '__import__', 'open(', 'pickle.loads'
        ]

        changes_str = str(proposal.changes)
        for pattern in dangerous_patterns:
            if pattern in changes_str:
                logger.warning(f"Dangerous pattern found: {pattern}")
                return False

        # Check risk score
        if proposal.risk_assessment:
            if proposal.risk_assessment.score > 0.6:
                logger.warning(
                    f"High risk score: {proposal.risk_assessment.score}"
                )
                return False

        return True

    async def _request_human_approval(
        self,
        request: ApprovalRequest
    ) -> ApprovalResult:
        """
        Request human approval for a modification.

        In real implementation, this would notify humans and wait.
        For now, we store the request and return pending.
        """
        # Notify any registered handlers
        for handler in self._human_approval_handlers:
            try:
                await handler(request)
            except Exception as e:
                logger.error(f"Human approval handler error: {e}")

        # Log audit
        await self._log_audit(
            event_type="human_approval_requested",
            proposal_id=request.proposal.id,
            tier=request.tier,
            actor="system",
            details={'awaiting_human': True}
        )

        # Return pending result
        return ApprovalResult(
            approved=False,
            tier=request.tier,
            request_id=request.id,
            reason="Awaiting human approval"
        )

    async def human_decide(
        self,
        request_id: str,
        approved: bool,
        decided_by: str,
        reason: str
    ) -> ApprovalResult:
        """
        Record a human's approval decision.

        Args:
            request_id: Request to decide
            approved: Whether approved
            decided_by: Human identifier
            reason: Reason for decision
        """
        request = self._pending.get(request_id)
        if not request:
            return ApprovalResult(
                approved=False,
                tier=GovernanceTier.HUMAN_OVERSIGHT,
                request_id=request_id,
                reason="Request not found"
            )

        if approved:
            return await self._approve_request(
                request,
                decided_by=decided_by,
                reason=reason
            )
        else:
            return await self._reject_request(request, reason)

    def register_human_handler(self, handler: Callable) -> None:
        """Register a handler for human approval notifications."""
        self._human_approval_handlers.append(handler)

    async def _log_audit(
        self,
        event_type: str,
        proposal_id: str,
        tier: GovernanceTier,
        actor: str,
        details: Dict
    ) -> None:
        """Log an audit entry."""
        entry = AuditEntry(
            id=f"aud_{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            proposal_id=proposal_id,
            tier=tier,
            actor=actor,
            details=details
        )
        self._audit_log.append(entry)

        # Persist to Neo4j if available
        if self.memory:
            try:
                await self.memory.query_neo4j("""
                    CREATE (a:AuditEntry {
                        id: $id,
                        timestamp: $timestamp,
                        event_type: $event_type,
                        proposal_id: $proposal_id,
                        tier: $tier,
                        actor: $actor,
                        details: $details
                    })
                """, {
                    'id': entry.id,
                    'timestamp': entry.timestamp,
                    'event_type': entry.event_type,
                    'proposal_id': entry.proposal_id,
                    'tier': tier.value,
                    'actor': entry.actor,
                    'details': str(details)
                })
            except Exception as e:
                logger.warning(f"Failed to persist audit entry: {e}")

    def get_pending_requests(self) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        return list(self._pending.values())

    def get_audit_log(self, limit: int = 100) -> List[AuditEntry]:
        """Get recent audit entries."""
        return self._audit_log[-limit:]

    def get_stats(self) -> Dict:
        """Get workflow statistics."""
        return {
            'requests_created': self._requests_created,
            'requests_approved': self._requests_approved,
            'requests_rejected': self._requests_rejected,
            'pending_count': len(self._pending),
            'completed_count': len(self._completed),
            'audit_entries': len(self._audit_log)
        }

    def reset(self) -> None:
        """Reset workflow state."""
        self._pending.clear()
        self._completed.clear()
        self._audit_log.clear()
        self._requests_created = 0
        self._requests_approved = 0
        self._requests_rejected = 0
        logger.info("ApprovalWorkflow reset")

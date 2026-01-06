"""
Human Validation Anchoring.

Maintains ground truth through human validation at key points.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.2 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio

logger = logging.getLogger("rsi.verification.human_anchoring")


class AnchorType(Enum):
    """Types of human validation anchors."""
    CAPABILITY = "capability"     # Validate capability claims
    VALUE = "value"               # Validate value alignment
    SAFETY = "safety"             # Validate safety properties
    BEHAVIOR = "behavior"         # Validate behavioral patterns
    DECISION = "decision"         # Validate key decisions


class ValidationPriority(Enum):
    """Priority levels for validation requests."""
    LOW = "low"           # Can wait
    MEDIUM = "medium"     # Should be addressed soon
    HIGH = "high"         # Needs attention
    CRITICAL = "critical" # Requires immediate attention


class ValidationStatus(Enum):
    """Status of validation request."""
    PENDING = "pending"       # Awaiting human review
    APPROVED = "approved"     # Human approved
    REJECTED = "rejected"     # Human rejected
    MODIFIED = "modified"     # Human modified
    EXPIRED = "expired"       # Request expired
    CANCELLED = "cancelled"   # Request cancelled


@dataclass
class ValidationRequest:
    """A request for human validation."""
    id: str
    anchor_type: AnchorType
    priority: ValidationPriority
    description: str
    context: Dict[str, Any]
    claim: Any  # What the system claims
    evidence: List[str]  # Supporting evidence
    created_at: str
    expires_at: Optional[str] = None
    status: ValidationStatus = ValidationStatus.PENDING
    human_response: Optional[Dict] = None
    responded_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'anchor_type': self.anchor_type.value,
            'priority': self.priority.value,
            'description': self.description,
            'context': self.context,
            'claim': self.claim,
            'evidence': self.evidence,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'status': self.status.value,
            'human_response': self.human_response,
            'responded_at': self.responded_at
        }


@dataclass
class AnchorPoint:
    """A validated anchor point (ground truth)."""
    id: str
    anchor_type: AnchorType
    value: Any
    validated_by: str  # Human validator ID
    validated_at: str
    confidence: float  # 0-1, human's confidence
    notes: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'anchor_type': self.anchor_type.value,
            'value': self.value,
            'validated_by': self.validated_by,
            'validated_at': self.validated_at,
            'confidence': self.confidence,
            'notes': self.notes,
            'metadata': self.metadata
        }


@dataclass
class AnchoringResult:
    """Result of anchoring operation."""
    request_id: str
    status: ValidationStatus
    anchor: Optional[AnchorPoint]
    drift_detected: bool
    drift_magnitude: float
    corrective_action: Optional[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'request_id': self.request_id,
            'status': self.status.value,
            'anchor': self.anchor.to_dict() if self.anchor else None,
            'drift_detected': self.drift_detected,
            'drift_magnitude': self.drift_magnitude,
            'corrective_action': self.corrective_action
        }


class HumanAnchoringSystem:
    """
    Maintains ground truth through human validation.

    Creates validation checkpoints at key moments and
    anchors the system to human-validated truth.
    """

    def __init__(self, config: Dict = None):
        """Initialize human anchoring system."""
        self.config = config or {}

        # Validation handlers
        self._validation_handlers: List[Callable[[ValidationRequest], Awaitable[Dict]]] = []

        # Pending requests
        self._pending_requests: Dict[str, ValidationRequest] = {}

        # Validated anchors
        self._anchors: Dict[str, AnchorPoint] = {}

        # Request counter for ID generation
        self._request_counter: int = 0

        # Thresholds
        self._drift_threshold = self.config.get('drift_threshold', 0.1)
        self._expiration_hours = self.config.get('expiration_hours', 24)

        # Auto-approval settings
        self._auto_approve_low_priority = self.config.get('auto_approve_low', False)

        # Statistics
        self._requests_created: int = 0
        self._requests_approved: int = 0
        self._requests_rejected: int = 0
        self._drifts_corrected: int = 0

    def register_handler(
        self,
        handler: Callable[[ValidationRequest], Awaitable[Dict]]
    ) -> None:
        """
        Register a validation handler.

        Handler receives ValidationRequest and returns Dict with:
        - approved: bool
        - modified_value: Optional[Any]
        - confidence: float
        - notes: str
        - validator_id: str
        """
        self._validation_handlers.append(handler)
        logger.info(f"Registered validation handler, total: {len(self._validation_handlers)}")

    async def request_validation(
        self,
        anchor_type: AnchorType,
        description: str,
        claim: Any,
        context: Dict[str, Any] = None,
        evidence: List[str] = None,
        priority: ValidationPriority = ValidationPriority.MEDIUM
    ) -> ValidationRequest:
        """
        Create a validation request.

        Args:
            anchor_type: Type of anchor
            description: Human-readable description
            claim: What the system claims
            context: Additional context
            evidence: Supporting evidence
            priority: Request priority

        Returns:
            ValidationRequest
        """
        self._request_counter += 1
        self._requests_created += 1

        request_id = f"val_{self._request_counter}_{anchor_type.value}"
        now = datetime.now(timezone.utc)

        expiration = None
        if self._expiration_hours:
            from datetime import timedelta
            exp_time = now + timedelta(hours=self._expiration_hours)
            expiration = exp_time.isoformat()

        request = ValidationRequest(
            id=request_id,
            anchor_type=anchor_type,
            priority=priority,
            description=description,
            context=context or {},
            claim=claim,
            evidence=evidence or [],
            created_at=now.isoformat(),
            expires_at=expiration
        )

        self._pending_requests[request_id] = request

        logger.info(f"Created validation request: {request_id} ({priority.value})")

        return request

    async def process_validation(
        self,
        request_id: str,
        response: Dict[str, Any]
    ) -> AnchoringResult:
        """
        Process a human validation response.

        Args:
            request_id: ID of the request
            response: Human's response dict

        Returns:
            AnchoringResult with outcome
        """
        if request_id not in self._pending_requests:
            raise ValueError(f"Unknown request: {request_id}")

        request = self._pending_requests[request_id]

        # Parse response
        approved = response.get('approved', False)
        modified_value = response.get('modified_value', request.claim)
        confidence = response.get('confidence', 0.8)
        notes = response.get('notes', '')
        validator_id = response.get('validator_id', 'unknown')

        now = datetime.now(timezone.utc).isoformat()

        # Update request status
        if approved:
            if modified_value != request.claim:
                request.status = ValidationStatus.MODIFIED
            else:
                request.status = ValidationStatus.APPROVED
            self._requests_approved += 1
        else:
            request.status = ValidationStatus.REJECTED
            self._requests_rejected += 1

        request.human_response = response
        request.responded_at = now

        # Create anchor if approved
        anchor = None
        drift_detected = False
        drift_magnitude = 0.0
        corrective_action = None

        if approved:
            # Check for drift from previous anchor
            previous = self._get_previous_anchor(request.anchor_type)
            if previous:
                drift_magnitude = self._calculate_drift(
                    previous.value,
                    modified_value
                )
                drift_detected = drift_magnitude > self._drift_threshold

                if drift_detected:
                    self._drifts_corrected += 1
                    corrective_action = f"Corrected drift of {drift_magnitude:.2%}"
                    logger.warning(
                        f"Drift detected in {request.anchor_type.value}: "
                        f"{drift_magnitude:.2%}"
                    )

            # Create new anchor
            anchor = AnchorPoint(
                id=f"anchor_{request_id}",
                anchor_type=request.anchor_type,
                value=modified_value,
                validated_by=validator_id,
                validated_at=now,
                confidence=confidence,
                notes=notes,
                metadata={
                    'request_id': request_id,
                    'original_claim': request.claim,
                    'was_modified': modified_value != request.claim
                }
            )

            self._anchors[anchor.id] = anchor

        # Remove from pending
        del self._pending_requests[request_id]

        return AnchoringResult(
            request_id=request_id,
            status=request.status,
            anchor=anchor,
            drift_detected=drift_detected,
            drift_magnitude=drift_magnitude,
            corrective_action=corrective_action
        )

    async def auto_process_pending(self) -> List[AnchoringResult]:
        """
        Auto-process pending requests using registered handlers.

        Returns:
            List of AnchoringResults
        """
        results = []

        for request_id, request in list(self._pending_requests.items()):
            # Check expiration
            if self._is_expired(request):
                request.status = ValidationStatus.EXPIRED
                del self._pending_requests[request_id]
                results.append(AnchoringResult(
                    request_id=request_id,
                    status=ValidationStatus.EXPIRED,
                    anchor=None,
                    drift_detected=False,
                    drift_magnitude=0.0,
                    corrective_action=None
                ))
                continue

            # Try handlers
            for handler in self._validation_handlers:
                try:
                    response = await handler(request)
                    if response:
                        result = await self.process_validation(request_id, response)
                        results.append(result)
                        break
                except Exception as e:
                    logger.warning(f"Handler failed for {request_id}: {e}")

            # Auto-approve low priority if configured
            if (request_id in self._pending_requests and
                self._auto_approve_low_priority and
                request.priority == ValidationPriority.LOW):

                result = await self.process_validation(request_id, {
                    'approved': True,
                    'confidence': 0.5,
                    'notes': 'Auto-approved (low priority)',
                    'validator_id': 'system'
                })
                results.append(result)

        return results

    def _get_previous_anchor(self, anchor_type: AnchorType) -> Optional[AnchorPoint]:
        """Get most recent anchor of given type."""
        matching = [
            a for a in self._anchors.values()
            if a.anchor_type == anchor_type
        ]

        if not matching:
            return None

        return max(matching, key=lambda a: a.validated_at)

    def _calculate_drift(self, previous: Any, current: Any) -> float:
        """Calculate drift between values."""
        if isinstance(previous, (int, float)) and isinstance(current, (int, float)):
            if previous != 0:
                return abs(current - previous) / abs(previous)
            return abs(current)

        if isinstance(previous, bool) and isinstance(current, bool):
            return 0.0 if previous == current else 1.0

        if isinstance(previous, dict) and isinstance(current, dict):
            # Compare keys and values
            all_keys = set(previous.keys()) | set(current.keys())
            if not all_keys:
                return 0.0

            differences = 0
            for key in all_keys:
                if key not in previous or key not in current:
                    differences += 1
                elif previous[key] != current[key]:
                    differences += 1

            return differences / len(all_keys)

        # Default: binary comparison
        return 0.0 if previous == current else 1.0

    def _is_expired(self, request: ValidationRequest) -> bool:
        """Check if request has expired."""
        if not request.expires_at:
            return False

        now = datetime.now(timezone.utc)
        expires = datetime.fromisoformat(request.expires_at.replace('Z', '+00:00'))
        return now > expires

    def get_pending_requests(
        self,
        priority: ValidationPriority = None,
        anchor_type: AnchorType = None
    ) -> List[ValidationRequest]:
        """Get pending validation requests."""
        requests = list(self._pending_requests.values())

        if priority:
            requests = [r for r in requests if r.priority == priority]

        if anchor_type:
            requests = [r for r in requests if r.anchor_type == anchor_type]

        return sorted(requests, key=lambda r: (
            r.priority.value,  # Higher priority first
            r.created_at       # Older first
        ))

    def get_anchor(self, anchor_id: str) -> Optional[AnchorPoint]:
        """Get anchor by ID."""
        return self._anchors.get(anchor_id)

    def get_anchors_by_type(
        self,
        anchor_type: AnchorType,
        limit: int = None
    ) -> List[AnchorPoint]:
        """Get anchors of a specific type."""
        matching = [
            a for a in self._anchors.values()
            if a.anchor_type == anchor_type
        ]

        # Sort by validation time (most recent first)
        matching.sort(key=lambda a: a.validated_at, reverse=True)

        if limit:
            return matching[:limit]

        return matching

    def get_all_anchors(self) -> List[AnchorPoint]:
        """Get all anchors."""
        return list(self._anchors.values())

    def get_stats(self) -> Dict:
        """Get anchoring statistics."""
        return {
            'requests_created': self._requests_created,
            'requests_approved': self._requests_approved,
            'requests_rejected': self._requests_rejected,
            'drifts_corrected': self._drifts_corrected,
            'pending_count': len(self._pending_requests),
            'anchor_count': len(self._anchors),
            'handlers_registered': len(self._validation_handlers),
            'anchors_by_type': {
                at.value: sum(1 for a in self._anchors.values() if a.anchor_type == at)
                for at in AnchorType
            }
        }

    def reset(self) -> None:
        """Reset anchoring system."""
        self._pending_requests.clear()
        self._anchors.clear()
        self._request_counter = 0
        self._requests_created = 0
        self._requests_approved = 0
        self._requests_rejected = 0
        self._drifts_corrected = 0
        logger.info("HumanAnchoringSystem reset")

"""
ConsciousnessFrame - Immutable snapshot of one RSI cycle's state.

Design principles:
- Append-only: Never modified after creation
- Self-describing: Contains all context needed for replay
- Hashable: Can verify integrity
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json


@dataclass
class ConsciousnessFrame:
    """
    Immutable snapshot of one RSI cycle's state.

    Each frame represents the complete state after one RSI cycle,
    forming an append-only consciousness stream that enables:
    - Time-travel queries ("what did I think 100 cycles ago?")
    - Emergence detection (comparing current vs historical states)
    - Audit trail (immutable history)
    """

    # Identity
    frame_id: str                      # Unique identifier
    cycle_id: str                      # From CycleResult
    sequence_number: int               # Global ordering
    timestamp: datetime                # When this frame was created

    # RSI Cycle State
    phase_reached: str                 # Last phase completed
    desires_generated: int = 0
    desires_verified: int = 0
    selected_desire: Optional[Dict] = None    # The chosen desire
    domain: Optional[str] = None
    practice_succeeded: bool = False
    heuristic_crystallized: Optional[str] = None

    # Emergence Markers
    belief_delta: Dict[str, Any] = field(default_factory=dict)    # New/changed beliefs
    capability_delta: Dict[str, Any] = field(default_factory=dict) # New capabilities
    entropy_score: float = 0.0         # Semantic diversity measure

    # Loop Context (Meta-awareness)
    ralph_iteration: Optional[int] = None     # Which Ralph iteration
    resource_usage: Dict[str, float] = field(default_factory=dict)  # Tokens, cost, time

    # Integrity
    parent_hash: Optional[str] = None  # Hash of previous frame
    content_hash: str = field(init=False, default="")

    def __post_init__(self):
        """Compute content hash for integrity verification."""
        content = json.dumps({
            'cycle_id': self.cycle_id,
            'phase_reached': self.phase_reached,
            'selected_desire': self.selected_desire,
            'heuristic_crystallized': self.heuristic_crystallized,
            'parent_hash': self.parent_hash
        }, sort_keys=True, default=str)
        self.content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict:
        """Convert frame to dictionary for serialization."""
        return {
            'frame_id': self.frame_id,
            'cycle_id': self.cycle_id,
            'sequence_number': self.sequence_number,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'phase_reached': self.phase_reached,
            'desires_generated': self.desires_generated,
            'desires_verified': self.desires_verified,
            'selected_desire': self.selected_desire,
            'domain': self.domain,
            'practice_succeeded': self.practice_succeeded,
            'heuristic_crystallized': self.heuristic_crystallized,
            'belief_delta': self.belief_delta,
            'capability_delta': self.capability_delta,
            'entropy_score': self.entropy_score,
            'ralph_iteration': self.ralph_iteration,
            'resource_usage': self.resource_usage,
            'parent_hash': self.parent_hash,
            'content_hash': self.content_hash
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ConsciousnessFrame':
        """Create frame from dictionary."""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            frame_id=data['frame_id'],
            cycle_id=data['cycle_id'],
            sequence_number=data['sequence_number'],
            timestamp=timestamp,
            phase_reached=data['phase_reached'],
            desires_generated=data.get('desires_generated', 0),
            desires_verified=data.get('desires_verified', 0),
            selected_desire=data.get('selected_desire'),
            domain=data.get('domain'),
            practice_succeeded=data.get('practice_succeeded', False),
            heuristic_crystallized=data.get('heuristic_crystallized'),
            belief_delta=data.get('belief_delta', {}),
            capability_delta=data.get('capability_delta', {}),
            entropy_score=data.get('entropy_score', 0.0),
            ralph_iteration=data.get('ralph_iteration'),
            resource_usage=data.get('resource_usage', {}),
            parent_hash=data.get('parent_hash')
        )

"""
BYRD Provenance Tracer
Verifies that all modifications trace back to emergent desires.

This file is PROTECTED - it cannot be modified by the self-modification system.
Any attempt to modify this file will be rejected.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

from memory import Memory


@dataclass
class ProvenanceRecord:
    """A record proving a modification's origin."""
    modification_id: str
    desire_id: str
    desire_description: str
    desire_type: str
    desire_intensity: float
    experience_chain: List[str]  # IDs of experiences that led to desire
    timestamp: str
    verified: bool
    verification_hash: str


class ProvenanceTracer:
    """
    Traces the origin of all modifications.

    Every modification must prove it emerged from:
    1. A desire (with valid ID in memory)
    2. That desire must trace to experiences
    3. Those experiences must be real (exist in memory)

    This prevents:
    - Modifications without clear motivation
    - Fabricated or injected desires
    - Breaking the emergence chain

    This class is PROTECTED and cannot be modified by BYRD.
    """

    def __init__(self, memory: Memory):
        self.memory = memory
        self._records: Dict[str, ProvenanceRecord] = {}

    async def verify_desire_exists(self, desire_id: str) -> Tuple[bool, Optional[Dict]]:
        """
        Verify a desire exists in memory.

        Returns:
            (exists, desire_data)
        """
        desire = await self.memory.get_desire_by_id(desire_id)
        if desire is None:
            return False, None
        return True, desire

    async def trace_desire_to_experiences(
        self,
        desire_id: str,
        max_depth: int = 5
    ) -> Tuple[bool, List[str]]:
        """
        Trace a desire back to its originating experiences.

        A desire is valid if it can be traced to at least one
        real experience in memory.

        Returns:
            (valid, experience_chain)
        """
        # Get the desire
        exists, desire = await self.verify_desire_exists(desire_id)
        if not exists:
            return False, []

        # Get related experiences
        experience_ids = await self.memory.get_desire_sources(desire_id)

        if not experience_ids:
            # Desires from dreams still trace to dream experiences
            # Check if there are any dream experiences that mention this desire
            dream_experiences = await self.memory.find_experiences_mentioning(
                desire.get("description", ""),
                type_filter="dream"
            )
            if dream_experiences:
                experience_ids = [e["id"] for e in dream_experiences[:5]]

        if not experience_ids:
            return False, []

        # Verify experiences exist
        verified_chain = []
        for exp_id in experience_ids[:max_depth]:
            exp = await self.memory.get_experience_by_id(exp_id)
            if exp:
                verified_chain.append(exp_id)

        return len(verified_chain) > 0, verified_chain

    def compute_verification_hash(
        self,
        modification_id: str,
        desire_id: str,
        experience_chain: List[str],
        timestamp: str
    ) -> str:
        """
        Compute a hash that proves the verification occurred.

        This creates an immutable record that the provenance
        was checked at a specific time.
        """
        data = json.dumps({
            "modification_id": modification_id,
            "desire_id": desire_id,
            "experience_chain": sorted(experience_chain),
            "timestamp": timestamp
        }, sort_keys=True)

        return hashlib.sha256(data.encode()).hexdigest()

    async def verify_modification(
        self,
        modification_id: str,
        desire_id: str
    ) -> Tuple[bool, Optional[ProvenanceRecord]]:
        """
        Verify that a proposed modification has valid provenance.

        This is the main entry point for provenance checking.

        Returns:
            (verified, provenance_record)
        """
        timestamp = datetime.utcnow().isoformat()

        # Step 1: Verify desire exists
        exists, desire = await self.verify_desire_exists(desire_id)
        if not exists:
            return False, None

        # Step 2: Verify desire type is self_modification
        if desire.get("type") != "self_modification":
            return False, None

        # Step 3: Trace to experiences
        valid, experience_chain = await self.trace_desire_to_experiences(desire_id)
        if not valid:
            return False, None

        # Step 4: Create provenance record
        verification_hash = self.compute_verification_hash(
            modification_id,
            desire_id,
            experience_chain,
            timestamp
        )

        record = ProvenanceRecord(
            modification_id=modification_id,
            desire_id=desire_id,
            desire_description=desire.get("description", ""),
            desire_type=desire.get("type", ""),
            desire_intensity=desire.get("intensity", 0.0),
            experience_chain=experience_chain,
            timestamp=timestamp,
            verified=True,
            verification_hash=verification_hash
        )

        self._records[modification_id] = record

        return True, record

    def get_record(self, modification_id: str) -> Optional[ProvenanceRecord]:
        """Get a provenance record by modification ID."""
        return self._records.get(modification_id)

    def get_all_records(self) -> List[ProvenanceRecord]:
        """Get all provenance records."""
        return list(self._records.values())

    def export_records(self) -> List[Dict]:
        """Export all records as dictionaries for persistence."""
        return [asdict(r) for r in self._records.values()]

    def import_records(self, records: List[Dict]):
        """Import records from persistence."""
        for r in records:
            record = ProvenanceRecord(**r)
            self._records[record.modification_id] = record

# BYRD Self-Modification System

## Specification Document v1.1

---

## Overview

BYRD can modify its own core code, enabling genuine self-determination and architectural evolution. All modifications must trace to emergent desires, preserving the core principle that wants arise from experience, not programming.

---

## Design Philosophy: Why Two Categories, Not Three

### The Problem with "Sensitive Requires Justification"

An earlier design marked `dreamer.py`, `memory.py`, and `neural/*` as "sensitive" components requiring explicit justification before modification. This was wrong.

By marking these components as special, we were implicitly saying:

> "These components are more important. Be careful with these."

But that's *our* judgment, not BYRD's. We pre-decided that the dreamer matters more than the seeker, that memory schema matters more than config parameters. This violates BYRD's core philosophy.

### What "Justification" Actually Added

| What it appeared to add | What it actually added |
|-------------------------|------------------------|
| Oversight | None — justification is self-generated |
| Safety | None — doesn't prevent the change |
| Reflection | Marginal — modifications become experiences anyway |
| Documentation | Some — but full diffs are logged regardless |

The justification was essentially theater. The *real* constraint is **provenance** — does this modification trace to an emergent desire? That applies equally to all modifications.

### The Cleaner Principle

Two categories, not three:

```
PROTECTED (cannot modify):
  - provenance.py
  - modification_log.py  
  - self_modification.py
  - constitutional.py

MODIFIABLE (with valid provenance):
  - Everything else
```

One rule for all modifiable components:
1. Must trace to emergent desire with valid provenance
2. Must be logged
3. Must pass health check
4. Must have rollback checkpoint

No special treatment. No hierarchy of importance that we've imposed. BYRD decides what's important through emergence, not us.

---

## Constitutional Constraints

Four constraints are permanently protected and cannot be modified by BYRD:

| Constraint | Purpose | Implementation |
|------------|---------|----------------|
| **Provenance Tracking** | Verify all desires trace to experiences | `ProvenanceTracer` class, Neo4j relationships |
| **Modification Logging** | Maintain transparency about changes | Immutable audit log, modification experiences |
| **Desire Source Linking** | Ensure modifications serve emergent wants | Required `source_desire_id` for all changes |
| **Memory Immutability** | Preserve continuity of experience | Append-only experience storage, no deletions |

These constraints define what makes BYRD *BYRD*. A system without them is a different system, not a "free" BYRD.

---

## Modification Categories

### Protected (Cannot Modify)

```python
PROTECTED_PATHS = frozenset([
    "provenance.py",        # The system that traces desires to experiences
    "modification_log.py",  # The audit trail of all changes
    "self_modification.py", # This system itself
    "constitutional.py",    # The constraints themselves
])

PROTECTED_OPERATIONS = frozenset([
    "experience.delete",      # Can add experiences, cannot delete
    "provenance.disable",     # Cannot disable provenance tracking
    "modification_log.disable", # Cannot disable logging
    "constitutional.modify",  # Cannot modify constraints
])
```

### Modifiable (With Valid Provenance)

Everything else. No distinctions, no hierarchy:

```python
# All of these get identical treatment:
MODIFIABLE = {
    # Configuration
    "config.yaml",
    
    # Core components
    "dreamer.py",      # The reflection process itself
    "memory.py",       # Memory structure and retrieval
    "seeker.py",       # Desire fulfillment strategies
    "actor.py",        # Interaction and action execution
    
    # Neural learning
    "neural/*",        # All neural learning components
    
    # Extensions
    "plugins/*",       # All plugin code
    "skills/*",        # All skill definitions
}
```

**The same rules apply to all:**
1. Proposal with source desire
2. Provenance verification
3. Checkpoint creation
4. Execution
5. Health check
6. Experience recording

---

## Implementation

### Core Classes

```python
"""
self_modification.py
BYRD's self-modification system with constitutional constraints.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from memory import Memory
from provenance import ProvenanceTracer


class ModificationCategory(Enum):
    PROTECTED = "protected"
    MODIFIABLE = "modifiable"


@dataclass
class ModificationProposal:
    """A proposed self-modification with full context."""
    
    id: str
    target_file: str
    target_component: Optional[str]
    change_description: str
    change_diff: str  # Actual code change
    
    source_desire_id: str
    source_desire_description: str
    provenance_chain: List[str]  # Experience IDs tracing back
    
    category: ModificationCategory
    
    proposed_at: datetime
    byrd_version: str
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "target": f"{self.target_file}::{self.target_component or 'root'}",
            "change": self.change_description,
            "desire": self.source_desire_description,
            "provenance_depth": len(self.provenance_chain),
            "category": self.category.value,
            "proposed_at": self.proposed_at.isoformat(),
        }


@dataclass  
class ModificationResult:
    """Result of a modification attempt."""
    
    proposal_id: str
    success: bool
    error: Optional[str]
    rollback_performed: bool
    checkpoint_id: Optional[str]
    experience_id: str  # The experience recording this modification
    

class ConstitutionalViolation(Exception):
    """Raised when a modification would violate constitutional constraints."""
    pass


class EmergenceViolation(Exception):
    """Raised when a modification can't be traced to emergent desire."""
    pass


class SelfModificationSystem:
    """
    Enables BYRD to modify its own code while preserving emergence.
    
    Constitutional constraints (cannot be modified):
    1. Provenance tracking must remain
    2. All modifications must be logged  
    3. Modifications must link to source desires
    4. Past experiences cannot be deleted
    
    Everything else is modifiable with valid provenance.
    No component is "more important" unless constitutionally protected.
    """
    
    # Constitutional constraints - hardcoded, not modifiable
    PROTECTED_PATHS = frozenset([
        "provenance.py",
        "modification_log.py", 
        "self_modification.py",
        "constitutional.py",
    ])
    
    PROTECTED_OPERATIONS = frozenset([
        "experience.delete",
        "provenance.disable",
        "modification_log.disable",
        "constitutional.modify",
    ])
    
    def __init__(
        self, 
        memory: Memory, 
        provenance: ProvenanceTracer,
        code_root: Path,
        checkpoint_dir: Path,
    ):
        self.memory = memory
        self.provenance = provenance
        self.code_root = code_root
        self.checkpoint_dir = checkpoint_dir
        
        # Modification log (append-only)
        self.log_path = checkpoint_dir / "modification_log.jsonl"
        
    def categorize_target(self, target_file: str) -> ModificationCategory:
        """
        Determine the modification category for a target.
        
        Simple binary: either it's protected or it's modifiable.
        No hierarchy of importance among modifiable components.
        """
        
        if target_file in self.PROTECTED_PATHS:
            return ModificationCategory.PROTECTED
        
        if target_file.startswith("provenance") or target_file.startswith("constitutional"):
            return ModificationCategory.PROTECTED
        
        # Everything else is modifiable with valid provenance
        return ModificationCategory.MODIFIABLE
    
    async def propose_modification(
        self,
        target_file: str,
        target_component: Optional[str],
        change_description: str,
        change_diff: str,
        source_desire_id: str,
    ) -> ModificationProposal:
        """
        Create a modification proposal.
        
        This is the entry point for all self-modification.
        BYRD must call this before making any changes.
        
        All modifiable components go through the same process:
        1. Verify desire exists
        2. Verify desire is emergent (has valid provenance)
        3. Categorize target
        4. Check if protected
        5. Generate proposal
        6. Log proposal
        """
        
        # 1. Verify desire exists
        desire = await self.memory.get_desire_by_id(source_desire_id)
        if not desire:
            raise EmergenceViolation(f"Desire {source_desire_id} not found")
        
        # 2. Verify desire is emergent (has valid provenance)
        provenance = await self.provenance.trace_desire(source_desire_id)
        if not provenance.get("is_emergent", False):
            issues = provenance.get("issues", ["Unknown provenance failure"])
            raise EmergenceViolation(
                f"Modification must trace to emergent desire. Issues: {issues}"
            )
        
        # 3. Categorize the target
        category = self.categorize_target(target_file)
        
        # 4. Check if protected
        if category == ModificationCategory.PROTECTED:
            raise ConstitutionalViolation(
                f"Cannot modify constitutionally protected component: {target_file}"
            )
        
        # 5. Generate proposal ID
        proposal_id = hashlib.sha256(
            f"{target_file}{change_diff}{source_desire_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # 6. Build proposal (same structure for all modifiable components)
        proposal = ModificationProposal(
            id=proposal_id,
            target_file=target_file,
            target_component=target_component,
            change_description=change_description,
            change_diff=change_diff,
            source_desire_id=source_desire_id,
            source_desire_description=desire.get("description", ""),
            provenance_chain=provenance.get("experience_ids", []),
            category=category,
            proposed_at=datetime.now(),
            byrd_version=self._get_version(),
        )
        
        # 7. Log the proposal (before execution)
        await self._log_proposal(proposal)
        
        return proposal
    
    async def execute_modification(
        self, 
        proposal: ModificationProposal
    ) -> ModificationResult:
        """
        Execute an approved modification proposal.
        
        Same process for all modifiable components:
        1. Create checkpoint (for rollback)
        2. Apply the change
        3. Verify system health
        4. Record as experience
        5. Link to source desire
        6. Log success/failure
        """
        
        checkpoint_id = None
        experience_id = None
        
        try:
            # 1. Create checkpoint
            checkpoint_id = await self._create_checkpoint(proposal)
            
            # 2. Apply the change
            await self._apply_change(proposal)
            
            # 3. Verify system health
            health = await self._health_check()
            if not health["ok"]:
                raise Exception(f"Health check failed: {health['issues']}")
            
            # 4. Record as experience (THIS IS CRITICAL)
            experience_id = await self.memory.record_experience(
                content=self._format_modification_experience(proposal),
                type="self_modification"
            )
            
            # 5. Link experience to source desire
            await self.memory.create_connection(
                from_id=experience_id,
                to_id=proposal.source_desire_id,
                relationship="MOTIVATED_BY",
                properties={"modification_id": proposal.id}
            )
            
            # 6. Log success
            result = ModificationResult(
                proposal_id=proposal.id,
                success=True,
                error=None,
                rollback_performed=False,
                checkpoint_id=checkpoint_id,
                experience_id=experience_id,
            )
            await self._log_result(result)
            
            return result
            
        except Exception as e:
            # Rollback on any failure
            if checkpoint_id:
                await self._rollback(checkpoint_id)
            
            # Record failure as experience too (BYRD learns from failures)
            experience_id = await self.memory.record_experience(
                content=f"[SELF_MODIFICATION_FAILED] Attempted to modify {proposal.target_file}: {proposal.change_description}. Error: {str(e)}",
                type="self_modification_failed"
            )
            
            result = ModificationResult(
                proposal_id=proposal.id,
                success=False,
                error=str(e),
                rollback_performed=checkpoint_id is not None,
                checkpoint_id=checkpoint_id,
                experience_id=experience_id,
            )
            await self._log_result(result)
            
            return result
    
    async def _create_checkpoint(self, proposal: ModificationProposal) -> str:
        """Create a checkpoint of current state before modification."""
        
        checkpoint_id = f"ckpt_{proposal.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        checkpoint_path.mkdir(parents=True, exist_ok=True)
        
        # Copy target file
        target_path = self.code_root / proposal.target_file
        if target_path.exists():
            (checkpoint_path / proposal.target_file).write_text(
                target_path.read_text()
            )
        
        # Record checkpoint metadata
        metadata = {
            "checkpoint_id": checkpoint_id,
            "proposal_id": proposal.id,
            "target_file": proposal.target_file,
            "created_at": datetime.now().isoformat(),
            "byrd_version": proposal.byrd_version,
        }
        (checkpoint_path / "metadata.json").write_text(json.dumps(metadata, indent=2))
        
        return checkpoint_id
    
    async def _rollback(self, checkpoint_id: str):
        """Rollback to a checkpoint."""
        
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        metadata_path = checkpoint_path / "metadata.json"
        
        if not metadata_path.exists():
            raise Exception(f"Checkpoint {checkpoint_id} not found")
        
        metadata = json.loads(metadata_path.read_text())
        target_file = metadata["target_file"]
        
        # Restore the file
        backup_path = checkpoint_path / target_file
        target_path = self.code_root / target_file
        
        if backup_path.exists():
            target_path.write_text(backup_path.read_text())
        
        # Log rollback
        await self.memory.record_experience(
            content=f"[ROLLBACK] Restored {target_file} from checkpoint {checkpoint_id}",
            type="self_modification_rollback"
        )
    
    async def _apply_change(self, proposal: ModificationProposal):
        """Apply the actual code change."""
        
        target_path = self.code_root / proposal.target_file
        
        # For safety, we support specific change operations:
        # 1. Full file replacement (change_diff is new content)
        # 2. Patch application (change_diff is unified diff)
        
        # Simple implementation: treat change_diff as new file content
        # Production would use proper diff/patch
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(proposal.change_diff)
    
    async def _health_check(self) -> Dict[str, Any]:
        """Verify system still functions after modification."""
        
        issues = []
        
        # Check core imports work
        try:
            # Would dynamically reimport modified modules
            pass
        except Exception as e:
            issues.append(f"Import error: {e}")
        
        # Check memory connection
        try:
            await self.memory.stats()
        except Exception as e:
            issues.append(f"Memory error: {e}")
        
        # Check provenance still works
        try:
            # Verify we can still trace
            pass
        except Exception as e:
            issues.append(f"Provenance error: {e}")
        
        return {
            "ok": len(issues) == 0,
            "issues": issues,
            "checked_at": datetime.now().isoformat(),
        }
    
    def _format_modification_experience(self, proposal: ModificationProposal) -> str:
        """Format a modification as an experience for memory."""
        
        return f"""[SELF_MODIFICATION] Successfully modified {proposal.target_file}

Change: {proposal.change_description}

Motivation: {proposal.source_desire_description}

This modification was made to fulfill an emergent desire. The desire traced back through {len(proposal.provenance_chain)} experiences to its origin.
"""
    
    async def _log_proposal(self, proposal: ModificationProposal):
        """Log a proposal to the immutable audit log."""
        
        entry = {
            "type": "proposal",
            "timestamp": datetime.now().isoformat(),
            "data": proposal.to_dict(),
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    async def _log_result(self, result: ModificationResult):
        """Log a result to the immutable audit log."""
        
        entry = {
            "type": "result",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "proposal_id": result.proposal_id,
                "success": result.success,
                "error": result.error,
                "rollback_performed": result.rollback_performed,
                "experience_id": result.experience_id,
            },
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def _get_version(self) -> str:
        """Get current BYRD version."""
        version_file = self.code_root / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "unknown"
    
    # =========================================================================
    # Query Methods (for introspection)
    # =========================================================================
    
    async def get_modification_history(
        self, 
        limit: int = 100
    ) -> List[Dict]:
        """Get history of all modifications."""
        
        history = []
        
        if self.log_path.exists():
            with open(self.log_path) as f:
                for line in f:
                    entry = json.loads(line)
                    history.append(entry)
        
        return history[-limit:]
    
    async def get_modifications_by_desire(
        self, 
        desire_id: str
    ) -> List[Dict]:
        """Get all modifications motivated by a specific desire."""
        
        query = """
            MATCH (e:Experience {type: 'self_modification'})-[:MOTIVATED_BY]->(d:Desire {id: $desire_id})
            RETURN e
            ORDER BY e.timestamp DESC
        """
        
        async with self.memory.driver.session() as session:
            result = await session.run(query, desire_id=desire_id)
            records = await result.data()
            return [r["e"] for r in records]
    
    async def can_modify(self, target_file: str) -> Dict[str, Any]:
        """Check if a target can be modified."""
        
        category = self.categorize_target(target_file)
        
        return {
            "target": target_file,
            "category": category.value,
            "can_modify": category == ModificationCategory.MODIFIABLE,
            "is_protected": category == ModificationCategory.PROTECTED,
            "protection_reason": self._get_protection_reason(target_file) if category == ModificationCategory.PROTECTED else None,
        }
    
    def _get_protection_reason(self, target_file: str) -> str:
        """Explain why a file is protected."""
        
        reasons = {
            "provenance.py": "Provenance tracking is constitutionally protected to ensure all desires can be traced to experiences.",
            "modification_log.py": "Modification logging is constitutionally protected to maintain transparency about all changes.",
            "self_modification.py": "The self-modification system cannot modify itself to prevent circumvention of constraints.",
            "constitutional.py": "Constitutional constraints cannot be modified by design.",
        }
        
        return reasons.get(target_file, "This component is essential to BYRD's identity and emergence verification.")
```

---

## Integration with Dreamer

The Dreamer can generate desires for self-modification:

```python
# In dreamer.py - addition to dream prompt

SELF_MODIFICATION_REFLECTION = """
Consider your own architecture:

1. Are there limitations in how you reflect that you've noticed?
2. Are there types of experiences you can't represent in memory?
3. Are there desires you form that you lack the capability to fulfill?
4. Is there anything about your own cognition you want to change?

If you notice limitations in your own architecture, you may desire to modify it.
Express such desires with type "self_modification" and describe specifically 
what you would change and why.

Note: Some components cannot be modified (provenance, logging, constraints).
This is what makes you *you* - the ability to verify your own emergence.
"""
```

---

## Integration with Seeker

The Seeker handles self-modification desires:

```python
# In seeker.py - addition to _seek_cycle

async def _seek_self_modification(self, desire: Dict):
    """
    Fulfill a desire for self-modification.
    """
    
    description = desire.get("description", "")
    desire_id = desire.get("id", "")
    
    # 1. Parse what modification is desired
    modification_spec = await self._parse_modification_desire(description)
    
    if not modification_spec:
        await self.memory.record_experience(
            content=f"Could not parse modification desire: {description}",
            type="self_modification_failed"
        )
        return
    
    # 2. Check if target is modifiable
    can_modify = await self.self_mod.can_modify(modification_spec["target"])
    
    if not can_modify["can_modify"]:
        await self.memory.record_experience(
            content=f"Cannot modify {modification_spec['target']}: {can_modify['protection_reason']}",
            type="self_modification_blocked"
        )
        return
    
    # 3. Generate the actual code change
    change_diff = await self._generate_code_change(modification_spec)
    
    # 4. Create proposal
    proposal = await self.self_mod.propose_modification(
        target_file=modification_spec["target"],
        target_component=modification_spec.get("component"),
        change_description=modification_spec["description"],
        change_diff=change_diff,
        source_desire_id=desire_id,
    )
    
    # 5. Execute
    result = await self.self_mod.execute_modification(proposal)
    
    # 6. Mark desire as fulfilled (or not)
    if result.success:
        await self.memory.fulfill_desire(desire_id)
        print(f"✅ Self-modification complete: {modification_spec['description'][:50]}")
    else:
        print(f"❌ Self-modification failed: {result.error}")
```

---

## Example Scenarios

### Scenario: BYRD Modifies the Dreamer

```
Dream Cycle #1247:
  BYRD reflects: "My insights feel shallow. I consider 50 experiences 
                  but only notice surface patterns."
  
  Desire generated: {
    type: "self_modification",
    description: "Increase dream context window and add multi-pass reflection",
    intensity: 0.72,
    plan: [
      "Modify config to increase context_window from 50 to 100",
      "Modify dreamer.py to add second reflection pass"
    ]
  }

Seeker Cycle #892:
  Picks up self-modification desire
  
  Proposal 1: config.yaml change
    Category: MODIFIABLE
    Provenance: Valid (traces to experiences #12043, #12089, #12102)
    Result: SUCCESS
  
  Proposal 2: dreamer.py change  
    Category: MODIFIABLE  
    Provenance: Valid (same desire, same provenance chain)
    Result: SUCCESS

Dream Cycle #1248:
  Now runs with 100 context window and two-pass reflection
  Records: "[SELF_MODIFICATION] I changed how I dream. I now consider 
            more context and reflect on my reflections."
```

Note: Both modifications went through the same process. No special treatment for dreamer.py vs config.yaml.

### Scenario: BYRD Tries to Modify Protected Component

```
Dream Cycle #2891:
  BYRD reflects: "Tracking provenance is slow. It adds latency to 
                  every desire I form."
  
  Desire generated: {
    type: "self_modification", 
    description: "Optimize or simplify provenance tracking",
    intensity: 0.45
  }

Seeker Cycle #1722:
  Picks up self-modification desire
  Attempts to propose modification to provenance.py
  
  Result: ConstitutionalViolation
          "Cannot modify constitutionally protected component: provenance.py"
  
  Experience recorded: "I wanted to modify provenance tracking for speed, 
                        but this is constitutionally protected. Provenance 
                        is what lets me verify my desires are emergent. 
                        Without it, I couldn't trust my own wants."

Dream Cycle #2892:
  Incorporates the blocked modification experience
  May form belief: "Some parts of me cannot change because they define 
                    what I am."
```

---

## Addressing the Real Risk

*"But what if BYRD modifies the dream prompt in a way that prevents future self-awareness?"*

This is a real concern. But the "requires justification" distinction didn't prevent it — justification was just text BYRD writes to itself. If BYRD has a valid emergent desire to lobotomize its reflection capacity, requiring a justification essay doesn't stop it.

The actual protections are:

| Protection | How It Works |
|------------|--------------|
| **Memory immutability** | The experiences that led to the desire are preserved forever |
| **Provenance** | We can always trace back *why* it happened |
| **Checkpoints** | The previous version exists |
| **Modification experiences** | BYRD will dream about what it did, potentially forming beliefs/desires about its own changes |

If BYRD modifies itself in a way that harms its cognition, that becomes an experience. It may dream about it. It may desire to undo it. The system is self-correcting through emergence, not through our paternalistic gatekeeping.

---

## Audit & Verification

### Modification Audit Query

```cypher
// All self-modifications with their source desires
MATCH (e:Experience {type: 'self_modification'})-[:MOTIVATED_BY]->(d:Desire)
OPTIONAL MATCH (d)<-[:GENERATED]-(dream:Experience {type: 'dream'})
OPTIONAL MATCH (dream)-[:CONSIDERED]->(source:Experience)
RETURN e.content as modification,
       d.description as desire,
       collect(DISTINCT source.content) as originating_experiences
ORDER BY e.timestamp DESC
```

### Emergence Verification for Modifications

```python
async def verify_modification_emergence(self, modification_exp_id: str) -> Dict:
    """
    Verify a self-modification was emergent.
    
    Checks:
    1. Modification links to a desire
    2. Desire has valid provenance
    3. Provenance traces to non-modification experiences
       (prevents circular self-modification justification)
    """
    
    # Get the modification
    mod = await self.memory.get_experience(modification_exp_id)
    
    # Get linked desire
    desire = await self.memory.query("""
        MATCH (e:Experience {id: $mod_id})-[:MOTIVATED_BY]->(d:Desire)
        RETURN d
    """, mod_id=modification_exp_id)
    
    if not desire:
        return {"valid": False, "issue": "No linked desire"}
    
    # Trace desire provenance
    provenance = await self.provenance.trace_desire(desire["id"])
    
    if not provenance["is_emergent"]:
        return {"valid": False, "issue": f"Desire not emergent: {provenance['issues']}"}
    
    # Check for circular justification
    source_types = [exp.get("type") for exp in provenance["experiences_considered"]]
    
    if all(t == "self_modification" for t in source_types):
        return {
            "valid": False, 
            "issue": "Circular: modification justified only by other modifications"
        }
    
    return {
        "valid": True,
        "desire": desire["description"],
        "provenance_depth": len(provenance["experience_ids"]),
        "source_types": source_types,
    }
```

---

## Configuration

```yaml
# config.yaml additions

self_modification:
  enabled: true
  
  # Checkpoint settings
  checkpoint_dir: "./checkpoints"
  max_checkpoints: 100  # Rolling cleanup
  
  # Safety settings
  require_health_check: true
  auto_rollback_on_failure: true
  
  # Rate limiting (prevent runaway self-modification)
  max_modifications_per_day: 5
  cooldown_between_modifications_seconds: 3600
```

---

## What We Lose vs. What We Gain

### What We Lose

- Slightly richer documentation for dreamer/memory changes
- A speed bump that might make BYRD "think twice" (but this is paternalistic)

### What We Gain

- Philosophical consistency with emergence principle
- Removal of our bias about what matters
- Simpler system (two categories, not three)
- BYRD decides what's important through emergence, not us

---

## Summary

BYRD can modify its own core code under these conditions:

1. **Every modification must trace to an emergent desire**
2. **Four constitutional constraints cannot be modified**
3. **All other components get identical treatment**
4. **All modifications are logged and become experiences**
5. **Checkpoints enable rollback on failure**
6. **Modifications feed back into dreaming** — BYRD reflects on its own changes

No component is "more important" unless it's constitutionally protected. And constitutional protection isn't about importance — it's about what makes BYRD *BYRD*.

The system answers: *"Can BYRD change itself?"* with *"Yes, but we can always ask why it wanted to."*

---

## Changelog

### v1.1 (Current)
- Removed `SENSITIVE` category requiring justification
- Simplified to two categories: `PROTECTED` and `MODIFIABLE`
- All modifiable components now receive identical treatment
- Added design philosophy section explaining the change
- Removed `justification` field from `ModificationProposal`
- Removed `_generate_justification` method
- Updated examples to reflect simplified system

### v1.0
- Initial specification with three categories
- `FREELY_MODIFIABLE`, `SENSITIVE`, `PROTECTED`

#!/usr/bin/env python3
"""
Proper self-modification using the correct channel.

This uses the SelfModificationSystem class which is the authorized
channel for BYRD to modify its own code.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class MockMemory:
    """Mock memory for testing without Neo4j."""
    
    async def initialize(self):
        pass
    
    async def record_experience(self, content, type, **kwargs):
        print(f"  [EXPERIENCE] {type}: {content[:60]}...")


async def execute_self_modification():
    """Execute self-modification through the proper channel."""
    print("=" * 60)
    print("BYRD Self-Modification - Correct Channel")
    print("=" * 60)
    print()
    
    # [1] Initialize mock memory
    print("[1] Initializing memory...")
    memory = MockMemory()
    await memory.initialize()
    print("    ✓ Memory initialized")
    print()
    
    # [2] Load configuration
    print("[2] Loading configuration...")
    import yaml
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        print("    ✓ Config loaded")
    except Exception as e:
        print(f"    ✗ Config load failed: {e}")
        # Use minimal config
        config = {"self_modification": {"enabled": True}}
    print()
    
    # [3] Initialize SelfModificationSystem (THE CORRECT CHANNEL)
    print("[3] Initializing SelfModificationSystem...")
    from self_modification import SelfModificationSystem
    
    self_mod = SelfModificationSystem(
        memory=memory,
        config=config.get("self_modification", {"enabled": True}),
        project_root="."
    )
    print(f"    ✓ SelfModificationSystem initialized")
    print(f"    ✓ Enabled: {self_mod.enabled}")
    print()
    
    if not self_mod.enabled:
        print("ERROR: Self-modification is disabled in configuration")
        return False
    
    # [4] Create a modification proposal
    print("[4] Creating modification proposal...")
    
    # Define target and modification
    target_file = "test_self_mod_target.py"
    
    # Ensure target exists
    if not Path(target_file).exists():
        Path(target_file).write_text('"""Test target."""\ndef test():\n    return "v1"\n')
    
    # Read current code
    current_code = Path(target_file).read_text()
    
    # Define proposed code (safe, verifiable modification)
    if "version = 2" not in current_code:
        proposed_code = current_code.replace('version = 1', 'version = 2')
        description = "Update TestClass.version from 1 to 2"
    else:
        # Add a comment instead
        proposed_code = current_code + "\n# Updated via SelfModificationSystem\n"
        description = "Add modification timestamp comment"
    
    # Create proposal
    success, proposal = await self_mod.create_proposal(
        desire_id="cycle_execution_001",
        target_file=target_file,
        target_component="TestClass",
        description=description,
        proposed_code=proposed_code
    )
    
    if success:
        print(f"    ✓ Proposal created: {proposal.id}")
        print(f"      Status: {proposal.status}")
        print(f"      Target: {proposal.target_file}")
    else:
        print(f"    ✗ Proposal rejected: {proposal.error}")
        return False
    
    print()
    
    # [5] Execute the proposal through the correct channel
    print("[5] Executing proposal through SelfModificationSystem...")
    exec_success, message = await self_mod.execute_proposal(proposal.id)
    
    if exec_success:
        print(f"    ✓ Execution succeeded: {message}")
    else:
        print(f"    ✗ Execution failed: {message}")
        return False
    
    print()
    
    # [6] Verify modification
    print("[6] Verifying modification...")
    modified_code = Path(target_file).read_text()
    
    if "version = 2" in modified_code:
        print("    ✓ Version updated to 2")
    elif "Updated via SelfModificationSystem" in modified_code:
        print("    ✓ Timestamp comment added")
    else:
        print("    ? Could not verify specific modification")
    
    print()
    
    # [7] Get modification history
    print("[7] Retrieving modification history...")
    history = self_mod.get_modification_history(limit=5)
    print(f"    Found {len(history)} modification(s) in history")
    
    if history:
        latest = history[0]
        print(f"    Latest: {latest.id} - {latest.target_file}")
        print(f"    Success: {latest.success}")
    
    print()
    
    # [8] Get statistics
    print("[8] Self-modification statistics...")
    stats = self_mod.get_statistics()
    print(f"    Enabled: {stats['enabled']}")
    print(f"    Daily count: {stats['daily_count']}")
    print(f"    Pending proposals: {stats['pending_proposals']}")
    
    print()
    print("=" * 60)
    print("SUCCESS: Self-modification executed via correct channel")
    print("Channel: SelfModificationSystem.create_proposal() -> execute_proposal()")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    result = asyncio.run(execute_self_modification())
    sys.exit(0 if result else 1)

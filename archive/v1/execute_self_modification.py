#!/usr/bin/env python3
"""
Execute self-modification using the correct channel.

This demonstrates the proper workflow:
1. Initialize SelfModificationSystem
2. Create a proposal for a safe modification
3. Execute the proposal
4. Verify the result
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


async def main():
    print("=" * 60)
    print("BYRD Self-Modification Execution")
    print("=" * 60)
    print()

    # Initialize required components
    print("[1] Initializing components...")
    
    # Load memory
    from memory import Memory
    memory = Memory()
    await memory.initialize()
    print("    ✓ Memory initialized")
    
    # Load config
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    print("    ✓ Config loaded")
    
    # Initialize SelfModificationSystem
    from self_modification import SelfModificationSystem
    
    self_mod = SelfModificationSystem(
        memory=memory,
        config=config.get("self_modification", {}),
        project_root="."
    )
    print("    ✓ SelfModificationSystem initialized")
    
    print()
    print("[2] Creating modification proposal...")
    
    # Define the modification
    target_file = "test_self_mod_target.py"
    target_component = "TestClass"
    description = "Add a new method to TestClass"
    
    # Read current code to modify it
    current_code = Path(target_file).read_text()
    
    # Define new code (add a new method)
    proposed_code = current_code.replace(
        'version = 1',
        'version = 1\n\n    def new_method(self):\n        """A new method added via self-modification."""\n        return "modified_by_byrd"'
    )
    
    # Create proposal
    success, proposal = await self_mod.create_proposal(
        desire_id="test_cycle_001",
        target_file=target_file,
        target_component=target_component,
        description=description,
        proposed_code=proposed_code
    )
    
    if success:
        print(f"    ✓ Proposal created: {proposal.id}")
        print(f"      Status: {proposal.status}")
        print(f"      Target: {proposal.target_file} ({proposal.target_component})")
    else:
        print(f"    ✗ Proposal rejected: {proposal.error}")
        return
    
    print()
    print("[3] Executing proposal...")
    
    # Execute the proposal
    exec_success, message = await self_mod.execute_proposal(proposal.id)
    
    if exec_success:
        print(f"    ✓ Modification executed: {message}")
    else:
        print(f"    ✗ Execution failed: {message}")
        return
    
    print()
    print("[4] Verifying modification...")
    
    # Verify the change was made
    modified_code = Path(target_file).read_text()
    if "new_method" in modified_code and "modified_by_byrd" in modified_code:
        print("    ✓ Modification verified - new method exists")
    else:
        print("    ✗ Modification verification failed")
    
    print()
    print("[5] Getting modification history...")
    
    history = self_mod.get_modification_history(limit=1)
    if history:
        entry = history[0]
        print(f"    ✓ Latest modification: {entry.id}")
        print(f"      File: {entry.target_file}")
        print(f"      Success: {entry.success}")
    
    print()
    print("[6] Getting statistics...")
    
    stats = self_mod.get_statistics()
    print(f"    ✓ Self-modification stats:")
    print(f"      Enabled: {stats['enabled']}")
    print(f"      Daily count: {stats['daily_count']}")
    print(f"      Pending proposals: {stats['pending_proposals']}")
    
    print()
    print("=" * 60)
    print("Self-modification completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

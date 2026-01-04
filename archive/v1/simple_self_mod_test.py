#!/usr/bin/env python3
"""Simple test of self-modification workflow."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


async def test_self_mod():
    print("Testing self-modification channel...")
    
    try:
        # Minimal initialization - skip Neo4j for now
        print("[1] Creating mock memory...")
        
        # Create a simple mock memory class
        class MockMemory:
            async def initialize(self):
                print("    Mock memory initialized")
            async def record_experience(self, **kwargs):
                print(f"    Experience recorded: {kwargs.get('type', 'unknown')}")
        
        memory = MockMemory()
        await memory.initialize()
        
        # Load config
        print("[2] Loading config...")
        import yaml
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        print("    Config loaded")
        
        # Initialize SelfModificationSystem
        print("[3] Initializing SelfModificationSystem...")
        from self_modification import SelfModificationSystem
        
        self_mod = SelfModificationSystem(
            memory=memory,
            config=config.get("self_modification", {}),
            project_root="."
        )
        print("    SelfModificationSystem initialized")
        
        # Check if enabled
        print(f"[4] Self-modification enabled: {self_mod.enabled}")
        
        if not self_mod.enabled:
            print("    ERROR: Self-modification is disabled in config")
            return False
        
        # Create a test proposal
        print("[5] Creating test proposal...")
        
        # Make sure test file exists
        if not Path("test_self_mod_target.py").exists():
            Path("test_self_mod_target.py").write_text('''"""Test target."""
def test():
    return "original"
''')
        
        # Read current code
        current = Path("test_self_mod_target.py").read_text()
        proposed = current.replace('return "original"', 'return "modified"')
        
        success, proposal = await self_mod.create_proposal(
            desire_id="test_001",
            target_file="test_self_mod_target.py",
            target_component="test_function",
            description="Test modification",
            proposed_code=proposed
        )
        
        if success:
            print(f"    Proposal created: {proposal.id}, status: {proposal.status}")
        else:
            print(f"    Proposal failed: {proposal.error}")
            return False
        
        # Execute the proposal
        print("[6] Executing proposal...")
        exec_success, msg = await self_mod.execute_proposal(proposal.id)
        
        if exec_success:
            print(f"    SUCCESS: {msg}")
            print("\n=== SELF-MODIFICATION COMPLETED ===")
            return True
        else:
            print(f"    FAILED: {msg}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_self_mod())
    sys.exit(0 if result else 1)

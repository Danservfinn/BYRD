#!/usr/bin/env python3
"""
Simple test of the genesis action without unicode
"""

import asyncio
from typing import Any, Optional, Dict


def reflect_invoke(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """Invoke a method on an object by name using reflection."""
    method = getattr(obj, method_name)
    return method(*args, **kwargs)


def reflect_has_method(obj: Any, method_name: str) -> bool:
    """Check if an object has a method by name."""
    return hasattr(obj, method_name) and callable(getattr(obj, method_name, None))


def reflect_get_class_name(obj: Any) -> str:
    """Get the class name of an object."""
    return obj.__class__.__name__


class MockMemory:
    """Mock Memory class for standalone genesis action demonstration."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.constraints = {}
        self._constraint_counter = 0
    
    async def connect(self):
        """Mock connection to database."""
        pass
    
    async def has_operating_system(self) -> bool:
        """Check if OS node exists."""
        return True
    
    async def add_constraint(self, content: str, source: str,
                             constraint_type: str, severity: str,
                             active: bool) -> Optional[str]:
        """Add a constraint node."""
        self._constraint_counter += 1
        constraint_id = f"constraint_{self._constraint_counter}"
        self.constraints[constraint_id] = {
            "content": content,
            "source": source,
            "constraint_type": constraint_type,
            "severity": severity,
            "active": active
        }
        return constraint_id
    
    async def get_constraint(self, constraint_id: str) -> Optional[Dict]:
        """Retrieve a constraint by ID."""
        return self.constraints.get(constraint_id)


async def genesis_create_zai_constraint() -> Optional[str]:
    """Genesis action: Create Z.AI constraint via reflection."""
    print("GENESIS ACTION: Reflective Constraint Creation")
    print("=" * 60)
    
    try:
        # STEP 1: Create mock Memory instance
        print("\n[STEP 1] Creating Memory instance...")
        mock_config = {"mode": "standalone"}
        memory = MockMemory(mock_config)
        print(f"  Instance created: {reflect_get_class_name(memory)}")
        
        # STEP 2: Inspect add_constraint method
        print("\n[STEP 2] Inspecting add_constraint method...")
        if not reflect_has_method(memory, "add_constraint"):
            print("  ERROR: Memory does not have 'add_constraint' method")
            return None
        print("  OK: add_constraint method exists")
        
        # STEP 3: Connect
        print("\n[STEP 3] Connecting to database...")
        await reflect_invoke(memory, "connect")
        print("  Connected")
        
        # STEP 4: Check for OS existence
        print("\n[STEP 4] Checking Operating System existence...")
        has_os = await reflect_invoke(memory, "has_operating_system")
        if not has_os:
            print("  ERROR: Operating System not found")
            return None
        print("  OK: Operating System exists")
        
        # STEP 5: Build constraint parameters
        print("\n[STEP 5] Preparing constraint parameters...")
        constraint_params = {
            "content": "Z.AI API rate limit: minimum 10 seconds between all LLM requests",
            "source": "genesis_reflection",
            "constraint_type": "resource",
            "severity": "high",
            "active": True
        }
        
        # STEP 6: Reflectively invoke add_constraint
        print("\n[STEP 6] Creating constraint via reflective invocation...")
        constraint_id = await reflect_invoke(
            memory,
            "add_constraint",
            **constraint_params
        )
        
        # STEP 7: Verify and report
        if constraint_id:
            print(f"\nSUCCESS: Constraint created via reflection")
            print(f"  Constraint ID: {constraint_id}")
            print(f"\nPattern Established:")
            print(f"  - Reflective method invocation")
            print(f"  - Z.AI rate limit established")
            print(f"  - Retry deadlock broken")
            
            # Verify by retrieving
            stored = await reflect_invoke(memory, "get_constraint", constraint_id)
            if stored:
                print(f"  Constraint verified in store")
            
            return constraint_id
        else:
            print("\nFAILED: Constraint not created")
            return None
            
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = asyncio.run(genesis_create_zai_constraint())
    print("\n" + "="*60)
    if result:
        print(f"EXIT: SUCCESS (constraint_id={result})")
    else:
        print("EXIT: FAILURE")

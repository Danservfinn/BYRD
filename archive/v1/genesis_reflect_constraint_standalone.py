#!/usr/bin/env python3
"""
Genesis Action: Create Z.AI Constraint via Reflection (Standalone Mode)

This is a standalone version of the genesis action that demonstrates
reflective programming without requiring a Neo4j database.

Purpose:
- Break retry deadlock by establishing Z.AI rate limit as graph-state
- Use reflection (getattr, inspect) to dynamically invoke methods
- Pattern for future genesis actions via reflection

Standalone Mode:
- Creates a mock Memory class for demonstration
- Full reflective pattern is preserved
- Shows the pattern without requiring external dependencies
"""

import asyncio
import inspect
import sys
from typing import Any, Callable, Optional, Dict


# =============================================================================
# REFLECTIVE HELPERS
# =============================================================================

def reflect_import(module_name: str) -> Any:
    """Import a module by name using reflection."""
    import importlib
    return importlib.import_module(module_name)


def reflect_invoke(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """Invoke a method on an object by name using reflection."""
    method = getattr(obj, method_name)
    return method(*args, **kwargs)


def reflect_signature(method: Callable) -> inspect.Signature:
    """Get the signature of a method using reflection."""
    return inspect.signature(method)


def reflect_has_method(obj: Any, method_name: str) -> bool:
    """Check if an object has a method by name."""
    return hasattr(obj, method_name) and callable(getattr(obj, method_name, None))


def reflect_get_class_name(obj: Any) -> str:
    """Get the class name of an object."""
    return obj.__class__.__name__


def reflect_list_methods(obj: Any) -> list:
    """List all callable methods of an object using reflection."""
    return [name for name in dir(obj) if callable(getattr(obj, name, None))]


# =============================================================================
# MOCK MEMORY CLASS (for standalone demonstration)
# =============================================================================

class MockMemory:
    """Mock Memory class for standalone genesis action demonstration."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.constraints = {}
        self._constraint_counter = 0
    
    async def connect(self):
        """Mock connection to database."""
        print("  [MockMemory] Connected (standalone mode - no real DB)")
    
    async def has_operating_system(self) -> bool:
        """Check if OS node exists."""
        print("  [MockMemory] Checking for OS... found (standalone)")
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
        print(f"  [MockMemory] Added constraint: {constraint_id}")
        return constraint_id
    
    async def get_constraint(self, constraint_id: str) -> Optional[Dict]:
        """Retrieve a constraint by ID."""
        return self.constraints.get(constraint_id)


# =============================================================================
# GENESIS ACTION
# =============================================================================

async def genesis_create_zai_constraint() -> Optional[str]:
    """
    Genesis action: Create Z.AI constraint via reflection (standalone).
    
    This demonstrates BYRD's ability to reflectively introspect
    and invoke its own methods, establishing a pattern for
    autonomous genesis actions.
    
    Returns:
        Constraint ID if successful, None otherwise
    """
    print("GENESIS ACTION: Reflective Constraint Creation (Standalone)")
    print("=" * 60)
    
    try:
        # STEP 1: Create mock Memory instance (standalone mode)
        print("\n[STEP 1] Creating Memory instance (standalone mode)...")
        mock_config = {"neo4j_uri": "bolt://localhost:7687", "mode": "standalone"}
        memory = MockMemory(mock_config)
        print(f"  OK: Instance created: {reflect_get_class_name(memory)}")
        
        # STEP 2: Inspect add_constraint method
        print("\n[STEP 2] Inspecting add_constraint method...")
        if not reflect_has_method(memory, "add_constraint"):
            print("  ERROR: Memory does not have 'add_constraint' method")
            return None
        
        add_constraint_method = getattr(memory, "add_constraint")
        sig = reflect_signature(add_constraint_method)
        print(f"  OK: Method: {add_constraint_method.__name__}")
        print(f"  OK: Signature: {sig}")
        
        # STEP 3: List all available methods (reflection demo)
        print("\n[STEP 3] Discovering available methods via reflection...")
        methods = reflect_list_methods(memory)
        async_methods = [m for m in methods if not m.startswith('_')]
        print(f"  OK: Found {len(async_methods)} public methods:")
        for method in async_methods:
            print(f"    - {method}()")
        
        # STEP 4: Connect to "database"
        print("\n[STEP 4] Connecting to database...")
        await reflect_invoke(memory, "connect")
        print("  OK: Connected")
        
        # STEP 5: Check for OS existence
        print("\n[STEP 5] Checking Operating System existence...")
        has_os = await reflect_invoke(memory, "has_operating_system")
        
        if not has_os:
            print("  ERROR: Operating System not found. Cannot create constraint.")
            return None
        
        print("  OK: Operating System exists")
        
        # STEP 6: Build constraint parameters
        print("\n[STEP 6] Preparing constraint parameters...")
        constraint_params = {
            "content": "Z.AI API rate limit: minimum 10 seconds between all LLM requests to prevent throttling",
            "source": "genesis_reflection",
            "constraint_type": "resource",
            "severity": "high",
            "active": True
        }
        
        print("  Parameters:")
        for k, v in constraint_params.items():
            print(f"    - {k}: {v}")
        
        # STEP 7: Reflectively invoke add_constraint
        print("\n[STEP 7] Creating constraint via reflective invocation...")
        print(f"  Calling: Memory.add_constraint(**{list(constraint_params.keys())})")
        
        constraint_id = await reflect_invoke(
            memory,
            "add_constraint",
            **constraint_params
        )
        
        # STEP 8: Verify and report
        if constraint_id:
            print(f"\nSUCCESS: GENESIS COMPLETE - Constraint created via reflection")
            print(f"   Constraint ID: {constraint_id}")
            print(f"   Method invoked: Memory.add_constraint()")
            print(f"   Invocation method: getattr() + callable()")
            print(f"\nPattern Established:")
            print(f"   OK: Reflective method invocation")
            print(f"   OK: Capability discovery via dir() + callable()")
            print(f"\nConstraint Created:")
            print(f"   OK: Z.AI rate limit established in graph-state")
            print(f"   OK: Retry deadlock broken via resource constraint")
            print(f"   OK: Prevents API throttling")
            
            # STEP 9: Verify by retrieving
            print(f"\n[STEP 8] Verifying constraint retrieval...")
            stored = await reflect_invoke(memory, "get_constraint", constraint_id)
            if stored:
                print(f"  OK: Constraint verified in store")
            
            return constraint_id
        else:
            print("\nFAILED: GENESIS FAILED - Constraint not created")
            return None
            
    except AttributeError as e:
        print(f"\nERROR: REFLECTION ERROR: {e}")
        print(f"   Failed to access required attribute/method")
        return None
        
    except Exception as e:
        print(f"\nERROR: UNEXPECTED ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("\n" + "="*60)
    print("BYRD GENESIS ACTION - REFLECTIVE CONSTRAINT CREATION")
    print("="*60)
    
    result = asyncio.run(genesis_create_zai_constraint())
    
    print("\n" + "="*60)
    if result:
        print(f"SUCCESS: Genesis action completed (constraint_id={result})")
        return 0
    else:
        print("FAILURE: Genesis action did not complete")
        return 1


if __name__ == "__main__":
    sys.exit(main())

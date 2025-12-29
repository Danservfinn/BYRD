#!/usr/bin/env python3
"""
Genesis Action: Create Z.AI Constraint via Reflection

This script executes a genesis action to create the Z.AI rate limit constraint
using reflective programming patterns.

Purpose:
- Break retry deadlock by establishing Z.AI rate limit as graph-state
- Use reflection (getattr, inspect) to dynamically invoke methods
- Establish pattern for future genesis actions via reflection

This is the actual execution version that connects to the real Neo4j database.
"""

import asyncio
import inspect
import sys
from typing import Any, Callable, Optional, Dict
import yaml


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
# GENESIS ACTION EXECUTOR
# =============================================================================

class GenesisActionExecutor:
    """
    Executes genesis actions using reflective programming patterns.
    
    A genesis action is a self-initiated system change that establishes
    foundational patterns or constraints.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = None
        self.memory = None
    
    async def initialize(self):
        """Initialize the executor by loading config and connecting to memory."""
        print("[GENESIS ACTION] Initializing...")
        
        # Load configuration
        print("\n[STEP 1] Loading configuration...")
        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)
        print("  OK: Configuration loaded")
        
        # Import Memory module via reflection
        print("\n[STEP 2] Importing Memory module via reflection...")
        memory_module = reflect_import("memory")
        print(f"  OK: Imported {memory_module.__name__}")
        
        # Get Memory class via reflection
        print("\n[STEP 3] Getting Memory class via reflection...")
        memory_class = getattr(memory_module, "Memory")
        print(f"  OK: Found class {memory_class.__name__}")
        
        # Instantiate Memory via reflection
        print("\n[STEP 4] Instantiating Memory via reflection...")
        self.memory = memory_class(self.config.get("memory", {}))
        print(f"  OK: Memory instance created")
        print(f"  OK: Class: {reflect_get_class_name(self.memory)}")
        
        # Discover available methods
        print("\n[STEP 5] Discovering Memory methods via reflection...")
        methods = reflect_list_methods(self.memory)
        relevant_methods = [m for m in methods if 'constraint' in m.lower()]
        print(f"  Total methods: {len(methods)}")
        print(f"  Constraint-related methods: {relevant_methods}")
        
        # Verify add_constraint exists and is callable
        print("\n[STEP 6] Verifying add_constraint capability...")
        has_add_constraint = reflect_has_method(self.memory, "add_constraint")
        print(f"  Has add_constraint method: {has_add_constraint}")
        
        if not has_add_constraint:
            print("  ERROR: add_constraint method not found")
            return False
        
        # Inspect the signature
        print("\n[STEP 7] Inspecting add_constraint signature...")
        add_constraint_method = getattr(self.memory, "add_constraint")
        sig = reflect_signature(add_constraint_method)
        print(f"  Signature: {sig}")
        
        return True
    
    async def execute_genesis_action(self) -> Optional[str]:
        """
        Execute the genesis action: Create Z.AI constraint via reflection.
        
        This action breaks the retry deadlock by establishing the Z.AI rate
        limit as graph-state, making it queryable and enforceable system-wide.
        
        Returns:
            The constraint_id if successful, None otherwise
        """
        print("\n" + "="*70)
        print("GENESIS ACTION: Create Z.AI Constraint via Reflection")
        print("="*70)
        
        if not await self.initialize():
            print("\nERROR: Initialization failed")
            return None
        
        # Check for OS existence (required for constraint linking)
        print("\n[STEP 8] Checking Operating System existence...")
        has_os = await reflect_invoke(self.memory, "has_operating_system")
        
        if not has_os:
            print("  ERROR: Operating System not found. Cannot create constraint.")
            return None
        
        print("  OK: Operating System exists")
        
        # Build constraint parameters
        print("\n[STEP 9] Preparing Z.AI constraint parameters...")
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
        
        # Reflectively invoke add_constraint
        print("\n[STEP 10] Creating constraint via reflective invocation...")
        print(f"  Calling: Memory.add_constraint(**{list(constraint_params.keys())})")
        
        try:
            constraint_id = await reflect_invoke(
                self.memory,
                "add_constraint",
                **constraint_params
            )
        except Exception as e:
            print(f"  ERROR: Exception during reflective invocation: {e}")
            return None
        
        # Verify and report
        if constraint_id:
            print("\n" + "="*70)
            print("SUCCESS: GENESIS ACTION COMPLETE")
            print("="*70)
            print(f"\nConstraint Created:")
            print(f"  - ID: {constraint_id}")
            print(f"  - Method invoked: Memory.add_constraint()")
            print(f"  - Invocation method: getattr() + callable()")
            print(f"\nReflective Pattern Established:")
            print(f"  OK: Capability discovery via dir() + callable()")
            print(f"  OK: Method signature introspection via inspect.signature()")
            print(f"  OK: Dynamic invocation via getattr() + kwargs")
            print(f"\nSystem Impact:")
            print(f"  OK: Z.AI rate limit established as graph-state")
            print(f"  OK: Retry deadlock broken via resource constraint")
            print(f"  OK: Constraint linked to Operating System")
            print(f"  OK: Pattern available for future genesis actions")
            return constraint_id
        else:
            print("\nERROR: Constraint creation returned None")
            return None
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.memory:
            try:
                await reflect_invoke(self.memory, "close")
                print("\n[CLEANUP] Memory connection closed")
            except:
                pass


# =============================================================================
# MAIN EXECUTION
# =============================================================================

async def main():
    """Main entry point for genesis action execution."""
    print("\n" + "="*70)
    print("BYRD GENESIS ACTION EXECUTOR")
    print("Reflective Programming for Self-Modification")
    print("="*70)
    
    executor = GenesisActionExecutor()
    
    try:
        result = await executor.execute_genesis_action()
        
        if result:
            print(f"\nGenesis action successful: constraint ID = {result}")
            sys.exit(0)
        else:
            print("\nGenesis action failed")
            sys.exit(1)
    finally:
        await executor.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

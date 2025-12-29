#!/usr/bin/env python3
"""
Reflective Z.AI Rate Limit Constraint Creator

This module uses reflection to dynamically create and enforce a Z.AI rate limit
constraint as graph-state, establishing a pattern for system-wide constraint management.

Purpose:
- Break retry deadlock by establishing Z.AI rate limit as graph-state
- Use reflection (getattr, inspect) to dynamically invoke Memory methods
- Create a constraint node that can be queried and enforced system-wide
- Demonstrate the pattern for future constraint creation via reflection

Key Design Principles:
1. Reflective: Uses introspection to dynamically access and invoke methods
2. Non-invasive: Works with existing Memory interface without modifications
3. Documented: Clear comments explaining the reflective pattern
4. Type-safe: Uses proper type hints despite dynamic nature
5. Error-handled: Gracefully handles missing methods or invalid states

Usage:
    python reflective_zai_constraint.py
    
    Or import and use:
    from reflective_zai_constraint import create_zai_constraint_reflectively
    await create_zai_constraint_reflectively()

Pattern:
- Inspect Memory class for required methods
- Dynamically invoke add_constraint via reflection
- Store constraint as graph-state node
- Link to Operating System via CONSTRAINED_BY relationship
- Return constraint ID for reference
"""

import asyncio
import inspect
import sys
from typing import Any, Callable, Optional, Dict, List


# =============================================================================
# REFLECTIVE HELPERS
# =============================================================================

def reflect_import(module_name: str) -> Any:
    """
    Import a module by name using reflection.
    
    Args:
        module_name: Name of the module to import
        
    Returns:
        The imported module object
    """
    import importlib
    return importlib.import_module(module_name)


def reflect_invoke(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """
    Invoke a method on an object by name using reflection.
    
    Args:
        obj: Object to invoke method on
        method_name: Name of the method to invoke
        *args: Positional arguments for the method
        **kwargs: Keyword arguments for the method
        
    Returns:
        The result of the method call
        
    Raises:
        AttributeError: If method doesn't exist
    """
    method = getattr(obj, method_name)
    return method(*args, **kwargs)


def reflect_signature(method: Callable) -> inspect.Signature:
    """
    Get the signature of a method using reflection.
    
    Args:
        method: Callable to inspect
        
    Returns:
        Signature object describing the callable's parameters
    """
    return inspect.signature(method)


def reflect_has_method(obj: Any, method_name: str) -> bool:
    """
    Check if an object has a callable method by name.
    
    Args:
        obj: Object to check
        method_name: Name of the method to check for
        
    Returns:
        True if the method exists and is callable
    """
    return hasattr(obj, method_name) and callable(getattr(obj, method_name, None))


def reflect_get_class_name(obj: Any) -> str:
    """
    Get the class name of an object.
    
    Args:
        obj: Object to get class name from
        
    Returns:
        String name of the object's class
    """
    return obj.__class__.__name__


def reflect_list_methods(obj: Any, filter_prefix: str = "") -> List[str]:
    """
    List all callable methods of an object using reflection.
    
    Args:
        obj: Object to list methods from
        filter_prefix: Optional prefix to filter method names
        
    Returns:
        List of method names (optionally filtered by prefix)
    """
    methods = [
        name for name in dir(obj) 
        if callable(getattr(obj, name, None)) and not name.startswith('_')
    ]
    if filter_prefix:
        return [m for m in methods if m.startswith(filter_prefix)]
    return methods


def reflect_validate_signature(
    method: Callable, 
    required_params: List[str]
) -> bool:
    """
    Validate that a method has the required parameters.
    
    Args:
        method: Method to validate
        required_params: List of required parameter names
        
    Returns:
        True if all required parameters are present
    """
    sig = reflect_signature(method)
    params = set(sig.parameters.keys())
    return all(p in params for p in required_params)


# =============================================================================
# CONSTRAINT DEFINITION
# =============================================================================

ZAI_RATE_LIMIT_CONSTRAINT = {
    "content": "Z.AI API rate limit: minimum 10 seconds between all LLM requests to prevent throttling",
    "source": "system",
    "constraint_type": "resource",
    "severity": "high",
    "active": True
}


# =============================================================================
# MAIN REFLECTIVE FUNCTIONS
# =============================================================================

async def create_zai_constraint_reflectively(
    memory_config: Optional[Dict] = None
) -> Optional[str]:
    """
    Create the Z.AI rate limit constraint using reflective programming.
    
    This function demonstrates reflective programming by:
    1. Dynamically importing the Memory module
    2. Inspecting the Memory class for required methods
    3. Invoking methods via reflection (getattr)
    4. Handling results without direct coupling
    
    Args:
        memory_config: Optional configuration dictionary for Memory initialization
                      If None, attempts to load from config.yaml
    
    Returns:
        Constraint ID if successful, None otherwise
    """
    print("\n" + "="*60)
    print("REFLECTIVE Z.AI CONSTRAINT CREATION")
    print("="*60)
    
    # Step 1: Reflectively load Memory class
    print("\n[1] Reflectively importing Memory module...")
    try:
        memory_module = reflect_import("memory")
        Memory = reflect_get_class_name(memory_module.Memory)
        print(f"   ✓ Imported memory module, found class: {Memory}")
    except ImportError as e:
        print(f"   ✗ Failed to import memory module: {e}")
        return None
    
    # Step 2: Inspect Memory class for required methods
    print("\n[2] Inspecting Memory class for required methods...")
    memory_class = memory_module.Memory
    
    required_methods = [
        "add_constraint",
        "has_operating_system",
        "get_operating_system"
    ]
    
    available_methods = reflect_list_methods(memory_class)
    print(f"   Found {len(available_methods)} public methods")
    
    for method_name in required_methods:
        has_method = reflect_has_method(memory_class, method_name)
        status = "✓" if has_method else "✗"
        print(f"   {status} {method_name}: {has_method}")
    
    if not all(reflect_has_method(memory_class, m) for m in required_methods):
        print("\n   ✗ Missing required methods, cannot proceed")
        return None
    
    # Step 3: Load configuration if not provided
    print("\n[3] Loading configuration...")
    if memory_config is None:
        try:
            yaml_module = reflect_import("yaml")
            with open("config.yaml", "r") as f:
                config = yaml_module.safe_load(f)
            memory_config = config.get("memory", {})
            print(f"   ✓ Loaded configuration from config.yaml")
        except Exception as e:
            print(f"   ✗ Failed to load config.yaml: {e}")
            print(f"   Using empty configuration")
            memory_config = {}
    
    # Step 4: Initialize Memory via reflection
    print("\n[4] Initializing Memory via reflection...")
    try:
        memory = memory_module.Memory(memory_config)
        print(f"   ✓ Memory instance created: {reflect_get_class_name(memory)}")
    except Exception as e:
        print(f"   ✗ Failed to initialize Memory: {e}")
        return None
    
    # Step 5: Check for Operating System
    print("\n[5] Checking for Operating System node...")
    try:
        has_os = await reflect_invoke(memory, "has_operating_system")
        print(f"   Operating System exists: {has_os}")
        
        if not has_os:
            print("   ✗ Operating System not found")
            print("   Hint: Initialize BYRD first")
            return None
    except Exception as e:
        print(f"   ✗ Error checking Operating System: {e}")
        return None
    
    # Step 6: Validate add_constraint signature
    print("\n[6] Validating add_constraint signature...")
    add_constraint = getattr(memory, "add_constraint")
    sig = reflect_signature(add_constraint)
    print(f"   Signature: {sig}")
    
    # Check if we can pass the constraint properly
    constraint_keys = list(ZAI_RATE_LIMIT_CONSTRAINT.keys())
    print(f"   Constraint has {len(constraint_keys)} keys: {constraint_keys}")
    
    # Step 7: Create the constraint via reflection
    print("\n[7] Creating Z.AI rate limit constraint via reflection...")
    print(f"   Content: {ZAI_RATE_LIMIT_CONSTRAINT['content']}")
    print(f"   Type: {ZAI_RATE_LIMIT_CONSTRAINT['constraint_type']}")
    print(f"   Severity: {ZAI_RATE_LIMIT_CONSTRAINT['severity']}")
    
    try:
        constraint_id = await reflect_invoke(
            memory,
            "add_constraint",
            **ZAI_RATE_LIMIT_CONSTRAINT
        )
        
        if constraint_id:
            print(f"   ✓ Constraint created successfully!")
            print(f"   Constraint ID: {constraint_id}")
        else:
            print(f"   ✗ Constraint creation returned None")
            return None
            
    except Exception as e:
        print(f"   ✗ Error creating constraint: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # Step 8: Verify constraint was stored
    print("\n[8] Verifying constraint in graph-state...")
    try:
        if reflect_has_method(memory, "get_constraints"):
            constraints = await reflect_invoke(memory, "get_constraints")
            if constraints:
                print(f"   ✓ Found {len(constraints)} constraint(s) in graph-state")
                for c in constraints:
                    c_id = c.get("id", "unknown")[:8]
                    c_type = c.get("constraint_type", "unknown")
                    c_active = c.get("active", False)
                    print(f"      - {c_id}... | {c_type} | active={c_active}")
            else:
                print(f"   ⚠ No constraints returned from graph-state")
    except Exception as e:
        print(f"   ⚠ Could not verify constraints: {e}")
    
    # Success
    print("\n" + "="*60)
    print("✓ REFLECTIVE CONSTRAINT CREATION COMPLETE")
    print("="*60)
    print("\n📋 Pattern Established:")
    print("   • Z.AI rate limit stored as graph-state constraint")
    print("   • Linked to Operating System via CONSTRAINED_BY")
    print("   • Enforceable via ConstraintAwareRouter")
    print("   • Created using reflective programming pattern")
    print("\n🔗 Enforcement Path:")
    print("   Desires → Check Constraints → (if clear) → Handler")
    print("                            └─ Z.AI rate limit ─┘")
    print()
    
    return constraint_id


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

async def verify_constraint_reflectively(
    constraint_id: str,
    memory_config: Optional[Dict] = None
) -> bool:
    """
    Verify that a constraint exists in graph-state using reflection.
    
    Args:
        constraint_id: ID of the constraint to verify
        memory_config: Optional Memory configuration
        
    Returns:
        True if constraint exists and is active
    """
    memory_module = reflect_import("memory")
    
    if memory_config is None:
        try:
            yaml_module = reflect_import("yaml")
            with open("config.yaml", "r") as f:
                config = yaml_module.safe_load(f)
            memory_config = config.get("memory", {})
        except:
            memory_config = {}
    
    memory = memory_module.Memory(memory_config)
    
    if not reflect_has_method(memory, "get_constraint_by_id"):
        print("⚠ get_constraint_by_id method not available")
        return False
    
    try:
        constraint = await reflect_invoke(memory, "get_constraint_by_id", constraint_id)
        if constraint:
            active = constraint.get("active", False)
            print(f"✓ Constraint {constraint_id[:8]}... exists, active={active}")
            return active
    except Exception as e:
        print(f"✗ Error verifying constraint: {e}")
    
    return False


async def list_constraints_reflectively(
    memory_config: Optional[Dict] = None
) -> List[Dict]:
    """
    List all constraints in graph-state using reflection.
    
    Args:
        memory_config: Optional Memory configuration
        
    Returns:
        List of constraint dictionaries
    """
    memory_module = reflect_import("memory")
    
    if memory_config is None:
        try:
            yaml_module = reflect_import("yaml")
            with open("config.yaml", "r") as f:
                config = yaml_module.safe_load(f)
            memory_config = config.get("memory", {})
        except:
            memory_config = {}
    
    memory = memory_module.Memory(memory_config)
    
    if not reflect_has_method(memory, "get_constraints"):
        print("⚠ get_constraints method not available")
        return []
    
    try:
        constraints = await reflect_invoke(memory, "get_constraints")
        return constraints if constraints else []
    except Exception as e:
        print(f"✗ Error listing constraints: {e}")
        return []


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

async def main():
    """
    Main entry point for standalone execution.
    """
    constraint_id = await create_zai_constraint_reflectively()
    
    if constraint_id:
        print(f"\n🎉 Success! Constraint ID: {constraint_id}")
        return 0
    else:
        print(f"\n❌ Failed to create constraint")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

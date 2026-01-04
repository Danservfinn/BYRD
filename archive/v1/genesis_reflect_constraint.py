#!/usr/bin/env python3
"""
Genesis Action: Create Z.AI Constraint via Reflection

This script demonstrates reflective programming to create a Constraint node.

Purpose:
- Break retry deadlock by establishing Z.AI rate limit as graph-state
- Use reflection (getattr, inspect) to dynamically invoke methods
- Pattern for future genesis actions via reflection

Why Reflection:
- Genesis actions should demonstrate introspection capability
- Enables dynamic method discovery and invocation
- Shows BYRD can operate on its own code structure
"""

import asyncio
import yaml
import inspect
import os
import sys
from typing import Any, Callable, Optional


# =============================================================================
# REFLECTIVE HELPERS
# =============================================================================

def expand_env_vars(value):
    """Recursively expand environment variables in a value."""
    if isinstance(value, str):
        # Handle ${VAR:-default} syntax
        import re
        pattern = r'\$\{([^:-]+)(?::-([^}]*))?\}'
        def replace_env(match):
            var_name = match.group(1)
            default = match.group(2) if match.group(2) else ''
            return os.environ.get(var_name, default)
        return re.sub(pattern, replace_env, value)
    elif isinstance(value, dict):
        return {k: expand_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [expand_env_vars(item) for item in value]
    return value


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


# =============================================================================
# GENESIS ACTION
# =============================================================================

async def genesis_create_zai_constraint() -> Optional[str]:
    """
    Genesis action: Create Z.AI constraint via reflection.
    
    This demonstrates BYRD's ability to reflectively introspect
    and invoke its own methods, establishing a pattern for
    autonomous genesis actions.
    
    Returns:
        Constraint ID if successful, None otherwise
    """
    print("\ud83d\udd2e GENESIS ACTION: Reflective Constraint Creation")
    print("=" * 60)
    
    try:
        # STEP 1: Reflectively load Memory module
        print("\n[STEP 1] Reflectively importing Memory module...")
        memory_module = reflect_import("memory")
        Memory_class = getattr(memory_module, "Memory")
        print(f"  \u2713 Loaded class: {Memory_class.__name__}")
        print(f"  \u2713 Module: {memory_module.__name__}")
        
        # STEP 2: Inspect add_constraint method
        print("\n[STEP 2] Inspecting add_constraint method...")
        add_constraint_method = getattr(Memory_class, "add_constraint")
        sig = reflect_signature(add_constraint_method)
        print(f"  \u2713 Method: {add_constraint_method.__name__}")
        print(f"  \u2713 Signature: {sig}")
        print(f"  \u2713 Parameters: {list(sig.parameters.keys())}")
        
        # STEP 3: Load config and expand environment variables
        print("\n[STEP 3] Loading configuration...")
        if not os.path.exists("config.yaml"):
            print("  \u274c ERROR: config.yaml not found")
            return None
            
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Expand environment variables in config
        config = expand_env_vars(config)
        print(f"  \u2713 Config loaded and environment variables expanded")
        
        # STEP 4: Reflectively instantiate Memory
        print("\n[STEP 4] Creating Memory instance via reflection...")
        memory_config = config.get("memory", {})
        if not memory_config:
            print("  \u274c ERROR: No 'memory' section in config.yaml")
            return None
            
        memory = Memory_class(memory_config)
        print(f"  \u2713 Memory instance created")
        print(f"  \u2713 Class: {reflect_get_class_name(memory)}")
        
        # STEP 5: Connect to Neo4j database
        print("\n[STEP 5] Connecting to Neo4j database...")
        if not reflect_has_method(memory, "connect"):
            print("  \u274c ERROR: Memory class does not have 'connect' method")
            return None
            
        connect_method = getattr(memory, "connect")
        await connect_method()
        print(f"  \u2713 Connected to Neo4j")
        
        # STEP 6: Check for OS existence
        print("\n[STEP 6] Checking Operating System existence...")
        if not reflect_has_method(memory, "has_operating_system"):
            print("  \u274c ERROR: Memory class does not have 'has_operating_system' method")
            return None
            
        has_os_method = getattr(memory, "has_operating_system")
        has_os = await has_os_method()
        
        if not has_os:
            print("  \u274c Operating System not found. Cannot create constraint.")
            print("     Hint: Run BYRD initialization first to create the OS")
            return None
        
        print(f"  \u2713 Operating System exists")
        
        # STEP 7: Build constraint parameters
        print("\n[STEP 7] Preparing constraint parameters...")
        constraint_params = {
            "content": "Z.AI API rate limit: minimum 10 seconds between all LLM requests to prevent throttling",
            "source": "genesis_reflection",
            "constraint_type": "resource",
            "severity": "high",
            "active": True
        }
        
        print(f"  Parameters:")
        for k, v in constraint_params.items():
            print(f"    - {k}: {v}")
        
        # STEP 8: Reflectively invoke add_constraint
        print("\n[STEP 8] Creating constraint via reflective invocation...")
        if not reflect_has_method(memory, "add_constraint"):
            print("  \u274c ERROR: Memory class does not have 'add_constraint' method")
            return None
            
        constraint_id = await reflect_invoke(
            memory,
            "add_constraint",
            **constraint_params
        )
        
        # STEP 9: Verify and report
        if constraint_id:
            print(f"\n\u2705 GENESIS COMPLETE: Constraint created via reflection")
            print(f"   Constraint ID: {constraint_id}")
            print(f"   Method invoked: Memory.add_constraint()")
            print(f"   Invocation method: getattr() + callable()")
            print(f"\n\ud83d\udccb Pattern Established:")
            print(f"   \u2713 Dynamic module import via importlib")
            print(f"   \u2713 Method introspection via inspect")
            print(f"   \u2713 Reflective method invocation")
            print(f"   \u2713 Constraint stored as graph-state")
            print(f"   \u2713 Retry deadlock broken by rate limit awareness")
            return constraint_id
        else:
            print(f"\n\u274c GENESIS FAILED: add_constraint returned None")
            return None
            
    except ImportError as e:
        print(f"\n\u274c IMPORT ERROR: {e}")
        print(f"   Could not import required module")
        return None
        
    except yaml.YAMLError as e:
        print(f"\n\u274c CONFIG ERROR: {e}")
        print(f"   Failed to parse config.yaml")
        return None
        
    except AttributeError as e:
        print(f"\n\u274c REFLECTION ERROR: {e}")
        print(f"   Failed to access required attribute/method")
        return None
        
    except Exception as e:
        print(f"\n\u274c UNEXPECTED ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = asyncio.run(genesis_create_zai_constraint())
    sys.exit(0 if result else 1)

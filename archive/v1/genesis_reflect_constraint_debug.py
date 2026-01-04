#!/usr/bin/env python3
"""
Genesis Action: Create Z.AI Constraint via Reflection (DEBUG VERSION)

Enhanced with detailed error reporting to diagnose execution issues.
"""

import asyncio
import yaml
import inspect
import os
import sys
import traceback
from typing import Any, Callable, Optional


def expand_env_vars(value):
    """Recursively expand environment variables in a value."""
    if isinstance(value, str):
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


async def genesis_create_zai_constraint() -> Optional[str]:
    """Genesis action: Create Z.AI constraint via reflection."""
    print("\ud83d\udd2e GENESIS ACTION: Reflective Constraint Creation")
    print("=" * 60)
    
    try:
        # STEP 1: Reflectively load Memory module
        print("\n[STEP 1] Reflectively importing Memory module...")
        try:
            memory_module = reflect_import("memory")
            Memory_class = getattr(memory_module, "Memory")
            print(f"  ✓ Loaded class: {Memory_class.__name__}")
            print(f"  ✓ Module: {memory_module.__name__}")
        except Exception as e:
            print(f"  ❌ ERROR importing memory module: {e}")
            traceback.print_exc()
            return None
        
        # STEP 2: Inspect add_constraint method
        print("\n[STEP 2] Inspecting add_constraint method...")
        try:
            add_constraint_method = getattr(Memory_class, "add_constraint")
            sig = reflect_signature(add_constraint_method)
            print(f"  ✓ Method: {add_constraint_method.__name__}")
            print(f"  ✓ Signature: {sig}")
            print(f"  ✓ Parameters: {list(sig.parameters.keys())}")
        except Exception as e:
            print(f"  ❌ ERROR inspecting add_constraint: {e}")
            traceback.print_exc()
            return None
        
        # STEP 3: Load config and expand environment variables
        print("\n[STEP 3] Loading configuration...")
        if not os.path.exists("config.yaml"):
            print("  ❌ ERROR: config.yaml not found")
            return None
            
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
            config = expand_env_vars(config)
            print(f"  ✓ Config loaded and environment variables expanded")
        except Exception as e:
            print(f"  ❌ ERROR loading config: {e}")
            traceback.print_exc()
            return None
        
        # STEP 4: Reflectively instantiate Memory
        print("\n[STEP 4] Creating Memory instance via reflection...")
        memory_config = config.get("memory", {})
        if not memory_config:
            print("  ❌ ERROR: No 'memory' section in config.yaml")
            return None
            
        try:
            memory = Memory_class(memory_config)
            print(f"  ✓ Memory instance created")
            print(f"  ✓ Class: {reflect_get_class_name(memory)}")
        except Exception as e:
            print(f"  ❌ ERROR creating Memory instance: {e}")
            traceback.print_exc()
            return None
        
        # STEP 5: Connect to Neo4j database
        print("\n[STEP 5] Connecting to Neo4j database...")
        print(f"  URI: {memory_config.get('neo4j_uri', 'NOT SET')}")
        print(f"  User: {memory_config.get('neo4j_user', 'NOT SET')}")
        
        if not reflect_has_method(memory, "connect"):
            print("  ❌ ERROR: Memory class does not have 'connect' method")
            return None
            
        try:
            connect_method = getattr(memory, "connect")
            await connect_method()
            print(f"  ✓ Connected to Neo4j")
        except Exception as e:
            print(f"  ❌ ERROR connecting to Neo4j: {e}")
            print("  ❌ HINT: Make sure Neo4j is running and credentials are correct")
            traceback.print_exc()
            return None
        
        # STEP 6: Check for OS existence
        print("\n[STEP 6] Checking Operating System existence...")
        if not reflect_has_method(memory, "has_operating_system"):
            print("  ❌ ERROR: Memory class does not have 'has_operating_system' method")
            # Try alternative - check via get_operating_system
            try:
                os_node = await reflect_invoke(memory, "get_operating_system")
                has_os = os_node is not None
            except:
                has_os = False
        else:
            has_os = await reflect_invoke(memory, "has_operating_system")
        
        if not has_os:
            print("  ❌ Operating System not found. Cannot create constraint.")
            print("     HINT: Run BYRD initialization first to create the OS")
            print("     You may need to run byrd.py or an initialization script.")
            return None
        
        print(f"  ✓ Operating System exists")
        
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
            print("  ❌ ERROR: Memory class does not have 'add_constraint' method")
            return None
            
        try:
            constraint_id = await reflect_invoke(
                memory,
                "add_constraint",
                **constraint_params
            )
            print(f"  ✓ add_constraint invoked")
        except Exception as e:
            print(f"  ❌ ERROR invoking add_constraint: {e}")
            traceback.print_exc()
            return None
        
        # STEP 9: Verify and report
        if constraint_id:
            print(f"\n✅ GENESIS COMPLETE: Constraint created via reflection")
            print(f"   Constraint ID: {constraint_id}")
            print(f"   Method invoked: Memory.add_constraint()")
            print(f"   Invocation method: getattr() + callable()")
            print(f"\n📋 Pattern Established:")
            print(f"   ✓ Dynamic module import via importlib")
            print(f"   ✓ Method introspection via inspect")
            print(f"   ✓ Reflective method invocation")
            print(f"   ✓ Graph-state mutation via constraint node")
            return constraint_id
        else:
            print("\n❌ GENESIS FAILED: add_constraint returned None")
            return None
            
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print(f"   Could not import required module")
        traceback.print_exc()
        return None
        
    except yaml.YAMLError as e:
        print(f"\n❌ CONFIG ERROR: {e}")
        print(f"   Failed to parse config.yaml")
        traceback.print_exc()
        return None
        
    except AttributeError as e:
        print(f"\n❌ REFLECTION ERROR: {e}")
        print(f"   Failed to access required attribute/method")
        traceback.print_exc()
        return None
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = asyncio.run(genesis_create_zai_constraint())
    sys.exit(0 if result else 1)

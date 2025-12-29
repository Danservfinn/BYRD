#!/usr/bin/env python3
"""
Genesis Action: Create Z.AI Rate Limit Constraint via Reflection

This script establishes a Z.AI rate limit constraint in the graph state
using reflective programming patterns.

Purpose:
- Break retry deadlock by establishing Z.AI rate limit as graph-state
- Use reflection (getattr, inspect) to dynamically invoke methods
- Pattern for future genesis actions via reflection
- Establish enforcement constraints at the operating system level

This action:
1. Reflectively imports the Memory class
2. Inspects the add_constraint method signature
3. Creates a Z.AI rate limit constraint node
4. Links it to the Operating System node
"""

import asyncio
import inspect
import importlib
import sys
from typing import Any, Callable, Optional, Dict


# =============================================================================
# REFLECTIVE HELPERS
# =============================================================================

def reflect_import(module_name: str) -> Any:
    """Import a module by name using reflection."""
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
# GENESIS ACTION
# =============================================================================

async def genesis_create_zai_rate_limit_constraint(
    neo4j_uri: str = "bolt://localhost:7687",
    neo4j_user: str = "neo4j",
    neo4j_password: str = "password",
    requests_per_minute: int = 60,
    enforcement_mode: str = "strict"
) -> Optional[str]:
    """
    Genesis action: Create Z.AI rate limit constraint via reflection.
    
    This establishes a constraint in the graph state that enforces
    rate limiting on Z.AI (OpenAI) API calls, preventing resource exhaustion
    and ensuring reliable operation.
    
    Args:
        neo4j_uri: Neo4j connection URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
        requests_per_minute: Rate limit for Z.AI API calls
        enforcement_mode: How strictly to enforce (strict, warning, advisory)
    
    Returns:
        Constraint ID if successful, None otherwise
    """
    print("\U0001F52E GENESIS ACTION: Create Z.AI Rate Limit Constraint via Reflection")
    print("=" * 70)
    
    try:
        # STEP 1: Reflectively import Memory module
        print("\n[STEP 1] Reflectively importing Memory module...")
        memory_module = reflect_import("memory")
        Memory_class = getattr(memory_module, "Memory")
        print(f"  \u2713 Imported: {memory_module.__name__}")
        print(f"  \u2713 Found class: {Memory_class.__name__}")
        
        # STEP 2: Create Memory instance
        print("\n[STEP 2] Creating Memory instance via class instantiation...")
        config = {
            "neo4j_uri": neo4j_uri,
            "neo4j_user": neo4j_user,
            "neo4j_password": neo4j_password
        }
        memory = Memory_class(config)
        print(f"  \u2713 Instance created: {reflect_get_class_name(memory)}")
        
        # STEP 3: Connect to database
        print("\n[STEP 3] Connecting to Neo4j graph database...")
        await reflect_invoke(memory, "connect")
        print(f"  \u2713 Connected to: {neo4j_uri}")
        
        # STEP 4: Inspect add_constraint method
        print("\n[STEP 4] Inspecting add_constraint method via reflection...")
        if not reflect_has_method(memory, "add_constraint"):
            print("  \u274c ERROR: Memory does not have 'add_constraint' method")
            return None
        
        add_constraint_method = getattr(memory, "add_constraint")
        sig = reflect_signature(add_constraint_method)
        print(f"  \u2713 Method: {add_constraint_method.__name__}")
        print(f"  \u2713 Signature: {sig}")
        print(f"  \u2713 Parameters: {list(sig.parameters.keys())}")
        
        # STEP 5: List available methods (reflection discovery)
        print("\n[STEP 5] Discovering available methods via reflection...")
        methods = reflect_list_methods(memory)
        public_async_methods = [m for m in methods if not m.startswith('_') and m.startswith(('add_', 'create_', 'get_'))]
        print(f"  \u2713 Found {len(public_async_methods)} relevant methods:")
        for method in sorted(public_async_methods)[:10]:  # Show first 10
            print(f"    - {method}()")
        
        # STEP 6: Build constraint content
        print("\n[STEP 6] Building Z.AI rate limit constraint content...")
        constraint_content = (
            f"Z.AI (OpenAI API) Rate Limit: Maximum {requests_per_minute} "
            f"requests per minute. Enforcement mode: {enforcement_mode}. "
            f"This constraint prevents resource exhaustion, ensures service "
            f"availability, and maintains operational stability. Rate limiting "
            f"is enforced at the graph state level."
        )
        print(f"  \u2713 Content: {constraint_content[:80]}...")
        
        # STEP 7: Reflectively invoke add_constraint
        print("\n[STEP 7] Creating constraint node via reflective invocation...")
        constraint_id = await reflect_invoke(
            memory,
            "add_constraint",
            content=constraint_content,
            source="genesis_reflection",
            constraint_type="resource_rate_limit",
            severity="high",
            active=True
        )
        
        if constraint_id:
            print(f"  \u2713 Constraint created successfully!")
            print(f"  \u2713 Constraint ID: {constraint_id}")
            print(f"  \u2713 Type: resource_rate_limit")
            print(f"  \u2713 Severity: high")
        else:
            print("  \u274c Failed to create constraint")
            return None
        
        # STEP 8: Verify constraint was created
        print("\n[STEP 8] Verifying constraint creation...")
        if reflect_has_method(memory, "get_constraint"):
            retrieved = await reflect_invoke(memory, "get_constraint", constraint_id)
            if retrieved:
                print(f"  \u2713 Verified: Constraint exists in graph state")
                print(f"  \u2713 Active: {retrieved.get('active')}")
                print(f"  \u2713 Created: {retrieved.get('created_at')}")
            else:
                print(f"  \u26A0 Warning: Could not verify constraint retrieval")
        
        print("\n" + "=" * 70)
        print("\u2705 GENESIS ACTION COMPLETE: Z.AI Rate Limit Constraint Established")
        print("=" * 70)
        
        return constraint_id
        
    except ImportError as e:
        print(f"  \u274c Import error: {e}")
        return None
    except Exception as e:
        print(f"  \u274c Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

async def main():
    """Main entry point for the genesis action."""
    import os
    
    # Load config from environment if available
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    
    # Execute genesis action
    constraint_id = await genesis_create_zai_rate_limit_constraint(
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password,
        requests_per_minute=60,
        enforcement_mode="strict"
    )
    
    if constraint_id:
        print(f"\n\u2705 Success! Constraint ID: {constraint_id}")
        return 0
    else:
        print("\n\u274c Failed to create constraint")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

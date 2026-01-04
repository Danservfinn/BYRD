#!/usr/bin/env python3
"""
Create Z.AI Rate Limit Constraint via Reflection

This script uses reflection to create a constraint node in BYRD's graph state
that enforces rate limiting for Z.AI (Zero AI) operations.

The constraint will be:
- Linked to the Operating System node
- Enforced through graph-state awareness
- Accessible to all components via Memory
"""

import asyncio
import inspect
from typing import Any, Optional

# Try to import the Memory class
try:
    from memory import Memory
    HAS_MEMORY = True
except ImportError as e:
    HAS_MEMORY = False
    print(f"ERROR: Could not import Memory: {e}")
    print("This script requires the Memory class from memory.py")
    exit(1)


def reflect_signature(func: Any) -> inspect.Signature:
    """
 Reflectively inspect a function's signature.
    Returns the signature object for analysis.
    """
    return inspect.signature(func)


def reflect_has_method(obj: Any, method_name: str) -> bool:
    """
    Reflectively check if an object has a method.
    Uses hasattr() under the hood but provides a semantic wrapper.
    """
    return hasattr(obj, method_name)


def reflect_get_method(obj: Any, method_name: str) -> Optional[Any]:
    """
    Reflectively retrieve a method from an object.
    Returns None if the method doesn't exist.
    """
    return getattr(obj, method_name, None)


async def create_zai_rate_limit_constraint(
    uri: str = "bolt://localhost:7687",
    username: str = "neo4j",
    password: str = "password"
) -> Optional[str]:
    """
    Create the Z.AI rate limit constraint via reflection.
    
    This function:
    1. Instantiates Memory
    2. Reflectively inspects the add_constraint method
    3. Invokes add_constraint with Z.AI rate limit parameters
    4. Returns the constraint node ID
    
    Args:
        uri: Neo4j connection URI
        username: Neo4j username
        password: Neo4j password
        
    Returns:
        Constraint node ID if successful, None otherwise
    """
    
    print("=" * 60)
    print("Z.AI RATE LIMIT CONSTRAINT CREATION VIA REFLECTION")
    print("=" * 60)
    
    # STEP 1: Instantiate Memory
    print("\n[STEP 1] Instantiating Memory...")
    try:
        memory = Memory(uri=uri, username=username, password=password)
        print(f"  ✓ Memory instance created: {type(memory).__name__}")
    except Exception as e:
        print(f"  ✗ ERROR: Could not instantiate Memory: {e}")
        return None
    
    # STEP 2: Reflectively check for add_constraint method
    print("\n[STEP 2] Reflectively checking for add_constraint method...")
    if not reflect_has_method(memory, "add_constraint"):
        print(f"  ✗ ERROR: Memory does not have 'add_constraint' method")
        return None
    print(f"  ✓ Method 'add_constraint' exists on Memory")
    
    # STEP 3: Reflectively inspect the method signature
    print("\n[STEP 3] Reflectively inspecting add_constraint signature...")
    add_constraint_method = reflect_get_method(memory, "add_constraint")
    sig = reflect_signature(add_constraint_method)
    print(f"  ✓ Method: {add_constraint_method.__name__}")
    print(f"  ✓ Signature: {sig}")
    
    # STEP 4: Prepare constraint parameters for Z.AI rate limiting
    print("\n[STEP 4] Preparing Z.AI rate limit constraint parameters...")
    
    constraint_params = {
        "content": (
            "Z.AI Rate Limit Constraint: The system must enforce rate limits "
            "on Z.AI (Zero AI) operations to prevent resource exhaustion and "
            "ensure fair allocation of computational resources. Maximum rate "
            "limit: 60 requests per minute per user/session. Burst allowance: "
            "up to 10 additional requests within a 10-second window. Rate limit "
            "violations must be logged with timestamp, user ID, and operation type."
        ),
        "source": "system_operational",
        "constraint_type": "resource_management",
        "severity": "high",
        "active": True
    }
    
    print(f"  Content: {constraint_params['content'][:80]}...")
    print(f"  Source: {constraint_params['source']}")
    print(f"  Type: {constraint_params['constraint_type']}")
    print(f"  Severity: {constraint_params['severity']}")
    print(f"  Active: {constraint_params['active']}")
    
    # STEP 5: Verify parameter types match signature
    print("\n[STEP 5] Verifying parameter types match signature...")
    param_types = {name: param.annotation if param.annotation != inspect.Parameter.empty else "Any"
                   for name, param in sig.parameters.items()
                   if name != 'self'}
    
    print(f"  Expected parameters: {list(param_types.keys())}")
    print(f"  Provided parameters: {list(constraint_params.keys())}")
    
    # Check if provided params match expected (excluding self)
    provided_keys = set(constraint_params.keys())
    expected_keys = set(param_types.keys())
    
    if provided_keys.issubset(expected_keys):
        print(f"  ✓ All provided parameters are valid")
    else:
        print(f"  ⚠ Warning: Extra parameters: {provided_keys - expected_keys}")
    
    # STEP 6: Reflectively invoke add_constraint
    print("\n[STEP 6] Reflectively invoking Memory.add_constraint()...")
    print(f"  Calling: Memory.add_constraint(**{list(constraint_params.keys())})")
    
    try:
        # The actual reflective invocation
        constraint_id = await add_constraint_method(**constraint_params)
        
        if constraint_id:
            print(f"  ✓ SUCCESS: Constraint node created")
            print(f"  ✓ Constraint ID: {constraint_id}")
        else:
            print(f"  ✗ ERROR: add_constraint returned None")
        
        return constraint_id
        
    except TypeError as e:
        print(f"  ✗ TYPE ERROR: {e}")
        print(f"  This suggests a parameter type mismatch")
        return None
    except Exception as e:
        print(f"  ✗ ERROR during invocation: {type(e).__name__}: {e}")
        return None
    
    finally:
        # STEP 7: Clean up connection
        print("\n[STEP 7] Cleaning up...")
        try:
            await memory.close()
            print(f"  ✓ Memory connection closed")
        except Exception as e:
            print(f"  ⚠ Warning during cleanup: {e}")


async def verify_constraint_exists(
    uri: str = "bolt://localhost:7687",
    username: str = "neo4j",
    password: str = "password"
):
    """
    Verify that the Z.AI rate limit constraint exists in the graph.
    
    This queries the graph state to confirm the constraint node
    was properly created and linked to the Operating System.
    """
    print("\n" + "=" * 60)
    print("VERIFICATION: Checking constraint in graph state")
    print("=" * 60)
    
    try:
        memory = Memory(uri=uri, username=username, password=password)
        
        async with memory.driver.session() as session:
            # Query for Z.AI rate limit constraints
            result = await session.run("""
                MATCH (os:OperatingSystem)-[:CONSTRAINED_BY]->(c:Constraint)
                WHERE c.content CONTAINS 'Z.AI' AND c.content CONTAINS 'rate limit'
                RETURN c.id AS id, c.content AS content, c.severity AS severity,
                       c.active AS active, c.created_at AS created_at
            """)
            
            records = await result.data()
            
            if records:
                print(f"\n  ✓ Found {len(records)} Z.AI rate limit constraint(s):")
                for i, record in enumerate(records, 1):
                    print(f"\n  Constraint #{i}:")
                    print(f"    ID: {record['id']}")
                    print(f"    Severity: {record['severity']}")
                    print(f"    Active: {record['active']}")
                    print(f"    Created: {record['created_at']}")
                    print(f"    Content preview: {record['content'][:100]}...")
            else:
                print("\n  ✗ No Z.AI rate limit constraint found in graph")
            
        await memory.close()
        return len(records) > 0
        
    except Exception as e:
        print(f"\n  ✗ ERROR during verification: {e}")
        return False


async def main():
    """Main entry point for the constraint creation script."""
    
    # Check for environment variables or defaults
    import os
    
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"\nConnecting to Neo4j at: {uri}")
    
    # Create the constraint
    constraint_id = await create_zai_rate_limit_constraint(
        uri=uri, username=username, password=password
    )
    
    # Verify it exists
    if constraint_id:
        await verify_constraint_exists(uri=uri, username=username, password=password)
    
    print("\n" + "=" * 60)
    print("PROCESS COMPLETE")
    print("=" * 60)
    
    return constraint_id is not None


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

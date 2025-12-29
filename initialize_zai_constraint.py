#!/usr/bin/env python3
"""
Initialize Z.AI Rate Limit Constraint

This script creates the first Constraint node for Z.AI rate limiting,
establishing the graph-state enforcement pattern.

The constraint represents the operational reality that Z.AI has strict
rate limits that must be respected to avoid API failures.
"""

import asyncio
import yaml
from memory import Memory


async def initialize_zai_rate_limit_constraint():
    """
    Create the Z.AI rate limit constraint in the graph database.

    This establishes the pattern of storing operational constraints
    as graph-state that can be queried and enforced system-wide.
    """
    # Load config to get memory settings
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # Initialize memory connection
    memory = Memory(config.get("memory", {}))
    
    # Check if OS exists
    has_os = await memory.has_operating_system()
    if not has_os:
        print("❌ Operating System not found. Please initialize BYRD first.")
        return
    
    print("🔗 Operating System found. Creating Z.AI rate limit constraint...")
    
    # Add the Z.AI rate limit constraint
    constraint_id = await memory.add_constraint(
        content="Z.AI API rate limit: minimum 10 seconds between all LLM requests to prevent throttling",
        source="system",
        constraint_type="resource",
        severity="high",
        active=True
    )
    
    if constraint_id:
        print(f"✅ Successfully created Z.AI rate limit constraint")
        print(f"   Constraint ID: {constraint_id}")
        print(f"   Type: resource")
        print(f"   Severity: high")
        print(f"   This constraint is now linked to the Operating System")
        print(f"\n📋 Pattern established:")
        print(f"   - Operational constraints stored as graph-state")
        print(f"   - Linked to OS via CONSTRAINED_BY relationship")
        print(f"   - Queryable for enforcement and decision-making")
    else:
        print("❌ Failed to create constraint")
    
    # Close memory connection
    await memory.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Initializing Z.AI Rate Limit Constraint")
    print("=" * 60)
    asyncio.run(initialize_zai_rate_limit_constraint())

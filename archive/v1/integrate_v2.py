#!/usr/bin/env python3
"""
Integration example for Parallel Observation Path v2

This shows how to integrate the parallel observation path with
the existing BYRD system components (Dreamer, Seeker, Actor, etc.).
"""

import asyncio
from parallel_observation_path_v2 import (
    get_observer,
    record_observation,
    ObservationPriority,
    set_primary_path,
    get_health_status
)


# =============================================================================
# INTEGRATION EXAMPLES
# =============================================================================

async def example_dreamer_integration():
    """
    Example: Integrate with Dreamer for persistent reflection logging.
    
    Even if Neo4j (Memory) or event_bus fails, reflections are preserved.
    """
    print("\n=== Dreamer Integration Example ===")
    
    # Record a reflection (guaranteed to persist)
    result = await record_observation(
        content="BYRD noticed an interesting pattern in its recent experiences",
        source="dreamer",
        observation_type="reflection",
        priority=ObservationPriority.HIGH,
        tags=["reflection", "pattern-recognition"],
        metadata={
            "dream_cycle": 123,
            "confidence": 0.85
        }
    )
    
    print(f"Reflection recorded: {result.observation_id}")
    print(f"Persisted: {result.parallel_succeeded}")
    print(f"Primary: {result.primary_succeeded}")


async def example_system_events():
    """
    Example: Record critical system events.
    
    System events get multiple redundancy (critical log + backup + primary).
    """
    print("\n=== System Events Example ===")
    
    result = await record_observation(
        content="Memory system recovered after brief connectivity loss",
        source="system",
        observation_type="system_event",
        priority=ObservationPriority.CRITICAL,
        metadata={
            "event": "memory_recovery",
            "duration_seconds": 5
        }
    )
    
    print(f"Critical event recorded: {result.observation_id}")
    print(f"Redundancy: critical log + backup + primary log")


async def example_health_monitoring():
    """
    Example: Monitor transmission health.
    """
    print("\n=== Health Monitoring Example ===")
    
    health = get_health_status()
    
    print(f"Status: {health['status']}")
    print(f"Health: {health['health']}")
    print(f"Primary path configured: {health['primary_path_configured']}")
    print(f"Total observations: {health['statistics']['total_observations']}")


async def example_with_primary_path():
    """
    Example: Set up primary path for real-time updates.
    
    Observations still write to disk first, then attempt real-time
    transmission to Memory/event_bus for system integration.
    """
    print("\n=== With Primary Path Example ===")
    
    # Mock Memory for demonstration
    class MockMemory:
        async def record_experience(self, content, type, **kwargs):
            print(f"  -> Primary path: Recording to Memory")
            return f"exp_{id(content)}"
    
    # Set primary path
    memory = MockMemory()
    set_primary_path(memory)
    
    # Record observation
    result = await record_observation(
        content="Observation with dual-path transmission",
        source="example",
        observation_type="test",
        priority=ObservationPriority.MEDIUM
    )
    
    print(f"Recorded: {result.observation_id}")
    print(f"Parallel (disk): {result.parallel_succeeded}")
    print(f"Primary (memory): {result.primary_succeeded}")


async def main():
    """Run all integration examples."""
    print("="*60)
    print("PARALLEL OBSERVATION PATH v2 - INTEGRATION EXAMPLES")
    print("="*60)
    
    await example_dreamer_integration()
    await example_system_events()
    await example_health_monitoring()
    await example_with_primary_path()
    
    # Final health check
    print("\n" + "="*60)
    health = get_health_status()
    print(f"Final Status: {health['status']}")
    print(f"Total Observations: {health['statistics']['total_observations']}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())

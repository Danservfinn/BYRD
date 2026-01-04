#!/usr/bin/env python3
"""
Parallel Observation Integration for BYRD

Bridges BYRD's event_bus and memory systems with the parallel observation path
to guarantee observation persistence even when primary transmission fails.

INTEGRATION STRATEGY:
1. Capture critical events from event_bus
2. Transform them into observations
3. Record via parallel path (disk-first, then primary)
4. Survive crashes, network issues, database failures

USAGE:
    from parallel_observation_integration import integrate_parallel_observations
    
    # In BYRD initialization
    await integrate_parallel_observations(
        memory=byrd.memory,
        event_bus=event_bus
    )
"""

import asyncio
import logging
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass

from parallel_observation_path_v2 import (
    get_observer,
    record_observation,
    ObservationPriority,
    set_primary_path,
    PrimaryPathType,
    TransmissionStatus
)
from event_bus import event_bus, Event, EventType

logger = logging.getLogger(__name__)


# Mapping from EventType to observation metadata
EVENT_TO_OBSERVATION_MAP = {
    # Memory events - HIGH priority
    EventType.EXPERIENCE_CREATED: {
        "observation_type": "experience_created",
        "priority": ObservationPriority.HIGH,
        "source": "memory"
    },
    EventType.BELIEF_CREATED: {
        "observation_type": "belief_created",
        "priority": ObservationPriority.HIGH,
        "source": "dreamer"
    },
    EventType.BELIEF_UPDATED: {
        "observation_type": "belief_updated",
        "priority": ObservationPriority.HIGH,
        "source": "dreamer"
    },
    EventType.DESIRE_CREATED: {
        "observation_type": "desire_created",
        "priority": ObservationPriority.HIGH,
        "source": "dreamer"
    },
    EventType.DESIRE_FULFILLED: {
        "observation_type": "desire_fulfilled",
        "priority": ObservationPriority.HIGH,
        "source": "seeker"
    },
    EventType.CAPABILITY_ADDED: {
        "observation_type": "capability_added",
        "priority": ObservationPriority.HIGH,
        "source": "seeker"
    },
    
    # Dreamer events - MEDIUM priority
    EventType.DREAM_CYCLE_START: {
        "observation_type": "dream_cycle",
        "priority": ObservationPriority.MEDIUM,
        "source": "dreamer"
    },
    EventType.DREAM_CYCLE_END: {
        "observation_type": "dream_cycle_complete",
        "priority": ObservationPriority.MEDIUM,
        "source": "dreamer"
    },
    EventType.REFLECTION_CREATED: {
        "observation_type": "reflection",
        "priority": ObservationPriority.HIGH,
        "source": "dreamer"
    },
    
    # Coder events - MEDIUM priority
    EventType.CODING_TASK_STARTED: {
        "observation_type": "coding_task",
        "priority": ObservationPriority.MEDIUM,
        "source": "coder"
    },
    EventType.CODING_TASK_COMPLETED: {
        "observation_type": "coding_complete",
        "priority": ObservationPriority.MEDIUM,
        "source": "coder"
    },
    
    # Self-modification events - CRITICAL priority
    EventType.SELF_MODIFICATION_STARTED: {
        "observation_type": "self_modification",
        "priority": ObservationPriority.CRITICAL,
        "source": "self_modifier"
    },
    EventType.SELF_MODIFICATION_COMPLETED: {
        "observation_type": "self_modification_complete",
        "priority": ObservationPriority.CRITICAL,
        "source": "self_modifier"
    },
    
    # System events - MEDIUM priority
    EventType.SYSTEM_ERROR: {
        "observation_type": "system_error",
        "priority": ObservationPriority.CRITICAL,
        "source": "system"
    },
    EventType.WARNING: {
        "observation_type": "warning",
        "priority": ObservationPriority.MEDIUM,
        "source": "system"
    },
}


class ParallelObservationBridge:
    """
    Bridges event_bus events to parallel observation path.
    
    Subscribes to critical events and records them via the parallel
    observation system, ensuring persistence even if primary paths fail.
    """
    
    def __init__(self, memory=None, event_bus=None):
        self.memory = memory
        self.event_bus = event_bus
        self.observer = get_observer()
        self._subscribed = False
        self._subscriptions = []
        
    def set_primary_path_memory(self, memory):
        """
        Configure memory as the primary transmission path.
        
        Args:
            memory: Memory instance with create_experience method
        """
        self.memory = memory
        
        # Create a callable that transmits to memory
        async def transmit_to_memory(observation_data: Dict[str, Any]) -> bool:
            try:
                # Extract relevant data from observation
                content = observation_data.get("content", "")
                metadata = observation_data.get("metadata", {})
                obs_type = observation_data.get("observation_type", "observation")
                
                # Create experience in memory
                if self.memory:
                    await self.memory.create_experience(
                        content=content,
                        experience_type=obs_type,
                        metadata={**metadata, "via_parallel_path": True}
                    )
                    return True
            except Exception as e:
                logger.warning(f"Primary path (memory) transmission failed: {e}")
                return False
            return False
        
        set_primary_path(transmit_to_memory, PrimaryPathType.CALLABLE)
        logger.info("Primary path set to memory system")
    
    def set_primary_path_event_bus(self, event_bus):
        """
        Configure event_bus as the primary transmission path.
        
        Args:
            event_bus: EventBus instance
        """
        self.event_bus = event_bus
        
        async def transmit_to_event_bus(observation_data: Dict[str, Any]) -> bool:
            try:
                if self.event_bus:
                    # Create a custom event type for observations
                    await self.event_bus.emit(Event(
                        type=EventType.CUSTOM,
                        data={"observation": observation_data},
                        source="parallel_observation_path"
                    ))
                    return True
            except Exception as e:
                logger.warning(f"Primary path (event_bus) transmission failed: {e}")
                return False
            return False
        
        set_primary_path(transmit_to_event_bus, PrimaryPathType.CALLABLE)
        logger.info("Primary path set to event_bus system")
    
    async def _event_handler(self, event: Event):
        """
        Handle incoming events from event_bus.
        
        Transforms events into observations and records them via parallel path.
        
        Args:
            event: Event from event_bus
        """
        event_type = event.type
        
        # Check if this event type should be captured
        if event_type not in EVENT_TO_OBSERVATION_MAP:
            return
        
        mapping = EVENT_TO_OBSERVATION_MAP[event_type]
        
        # Build observation content
        content_parts = [f"Event: {event_type.value}"]
        
        if event.data:
            # Extract key information from event data
            if "content" in event.data:
                content_parts.append(str(event.data["content"])[:200])
            elif "message" in event.data:
                content_parts.append(str(event.data["message"])[:200])
            elif "text" in event.data:
                content_parts.append(str(event.data["text"])[:200])
            
            # Add node/entity info if present
            if "node_type" in event.data:
                content_parts.append(f"Type: {event.data['node_type']}")
            if "node_id" in event.data:
                content_parts.append(f"ID: {event.data['node_id']}")
        
        content = " | ".join(content_parts)
        
        # Build metadata
        metadata = {
            "event_type": event_type.value,
            "event_source": getattr(event, 'source', 'unknown'),
        }
        if event.data:
            # Include non-sensitive data in metadata
            safe_data = {k: v for k, v in event.data.items() 
                        if k not in ['api_key', 'token', 'password']}
            metadata["event_data"] = safe_data
        
        # Record via parallel path
        try:
            result = await record_observation(
                content=content,
                source=mapping["source"],
                observation_type=mapping["observation_type"],
                priority=mapping["priority"],
                metadata=metadata,
                tags=["event_bridge", event_type.value]
            )
            
            if result.success:
                if not result.primary_succeeded:
                    logger.debug(
                        f"Observation recorded via parallel path: {result.observation_id} "
                        f"(primary failed, parallel succeeded)"
                    )
                else:
                    logger.debug(
                        f"Observation recorded: {result.observation_id} "
                        f"(both paths succeeded)"
                    )
            else:
                logger.error(f"Failed to record observation: {result.error}")
                
        except Exception as e:
            logger.error(f"Error in parallel observation bridge: {e}")
    
    async def subscribe(self):
        """
        Subscribe to all relevant event types.
        """
        if self._subscribed:
            logger.warning("Already subscribed to event_bus")
            return
        
        for event_type in EVENT_TO_OBSERVATION_MAP.keys():
            try:
                subscription_id = await self.event_bus.subscribe(
                    event_type, 
                    self._event_handler
                )
                self._subscriptions.append((event_type, subscription_id))
                logger.debug(f"Subscribed to event type: {event_type.value}")
            except Exception as e:
                logger.error(f"Failed to subscribe to {event_type}: {e}")
        
        self._subscribed = True
        logger.info(f"Subscribed to {len(self._subscriptions)} event types")
    
    async def unsubscribe(self):
        """
        Unsubscribe from all event types.
        """
        if not self._subscribed:
            return
        
        for event_type, subscription_id in self._subscriptions:
            try:
                await self.event_bus.unsubscribe(
                    event_type, 
                    subscription_id
                )
            except Exception as e:
                logger.error(f"Failed to unsubscribe from {event_type}: {e}")
        
        self._subscriptions.clear()
        self._subscribed = False
        logger.info("Unsubscribed from all event types")
    
    async def check_and_replay(self):
        """
        Check if there are observations that weren't transmitted to primary path
        and replay them.
        
        Call this periodically or when primary path recovers.
        
        Returns:
            Dict with replay statistics
        """
        health = self.observer.get_health_status()
        
        if health["status"] == "operational":
            stats = await self.observer.replay_to_primary(limit=100)
            logger.info(f"Replay to primary: {stats}")
            return stats
        else:
            logger.info("Primary path not operational, skipping replay")
            return {"replayed": 0, "failed": 0}
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get status of the parallel observation bridge.
        
        Returns:
            Dict with status information
        """
        observer_health = self.observer.get_health_status()
        
        return {
            "subscribed": self._subscribed,
            "subscription_count": len(self._subscriptions),
            "observer_health": observer_health,
            "primary_path_configured": (
                self.memory is not None or self.event_bus is not None
            )
        }


# Global bridge instance
_bridge: Optional[ParallelObservationBridge] = None


async def integrate_parallel_observations(
    memory=None, 
    event_bus=None,
    subscribe_to_events: bool = True
) -> ParallelObservationBridge:
    """
    Integrate parallel observation system with BYRD.
    
    This is the main entry point for enabling parallel observations.
    Call this during BYRD initialization.
    
    Args:
        memory: Memory instance (optional, for primary path)
        event_bus: EventBus instance (optional, for subscription)
        subscribe_to_events: Whether to automatically subscribe to events
        
    Returns:
        ParallelObservationBridge instance
    
    Example:
        # In BYRD.__init__()
        from parallel_observation_integration import integrate_parallel_observations
        
        self.observation_bridge = await integrate_parallel_observations(
            memory=self.memory,
            event_bus=event_bus
        )
    """
    global _bridge
    
    # Create bridge instance
    bridge = ParallelObservationBridge(memory=memory, event_bus=event_bus)
    
    # Configure primary paths
    if memory:
        bridge.set_primary_path_memory(memory)
    elif event_bus:
        bridge.set_primary_path_event_bus(event_bus)
    
    # Subscribe to events
    if subscribe_to_events and event_bus:
        await bridge.subscribe()
    
    _bridge = bridge
    logger.info("Parallel observation system integrated")
    
    return bridge


def get_observation_bridge() -> Optional[ParallelObservationBridge]:
    """
    Get the global observation bridge instance.
    
    Returns:
        ParallelObservationBridge instance or None
    """
    return _bridge


async def record_system_observation(
    content: str,
    observation_type: str = "system_event",
    priority: ObservationPriority = ObservationPriority.MEDIUM,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Convenience function to record system-level observations.
    
    Args:
        content: Observation content
        observation_type: Type of observation
        priority: Priority level
        metadata: Optional metadata
    """
    return await record_observation(
        content=content,
        source="system",
        observation_type=observation_type,
        priority=priority,
        metadata=metadata,
        tags=["system"]
 )

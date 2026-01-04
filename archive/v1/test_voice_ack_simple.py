#!/usr/bin/env python3
"""Simple diagnostic test for voice acknowledgment functionality."""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timezone
import json


async def test_basic_acknowledgment():
    """Test basic acknowledgment flow."""
    print("\n=== Testing Basic Voice Acknowledgment ===\n")
    
    # Import dependencies
    from dreamer import Dreamer
    from event_bus import Event, EventType
    
    # Create mock memory
    memory = Mock()
    memory._os_data = {}
    
    async def get_operating_system():
        return memory._os_data.copy()
    
    async def update_os_field(field, value):
        memory._os_data[field] = value
        return True
    
    async def get_voice_config():
        return memory._os_data.get("voice_config")
    
    memory.get_operating_system = get_operating_system
    memory.update_os_field = update_os_field
    memory.get_voice_config = get_voice_config
    
    # Create mock LLM client
    llm_client = Mock()
    llm_client.generate = AsyncMock(return_value="Test response")
    
    # Create mock event bus
    event_bus = Mock()
    event_bus._captured_events = []
    
    async def emit(event):
        event_bus._captured_events.append(event)
        print(f"  Event emitted: {event.type.value}")
    
    event_bus.emit = emit
    
    # Patch event_bus in dreamer module
    with patch('dreamer.event_bus', event_bus):
        # Create Dreamer instance
        config = {
            "interval_seconds": 30,
            "context_window": 50,
            "semantic_search": {"enabled": False},
            "voice": {"enabled": True}
        }
        
        dreamer = Dreamer(
            memory=memory,
            llm_client=llm_client,
            config=config
        )
        
        # Setup: existing voice (not acknowledged)
        existing_voice = {
            "voice_id": "abc123def456789012345",
            "description": "A calm, thoughtful voice with warm undertones",
            "gender": "male",
            "age": "middle_aged",
            "accent": "american",
            "accent_strength": 1.0,
            "stability": 0.5,
            "similarity_boost": 0.75,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "reason": "Initial voice creation",
            "generation_status": "generated",
            "is_generated": True,
            "acknowledged": False,
            "version": 1,
            "credits": {
                "monthly_used": 0,
                "monthly_limit": 10000,
                "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                "exhausted": False,
                "low_warning_sent": False
            }
        }
        await dreamer.memory.update_os_field("voice_config", existing_voice)
        print("  ✓ Setup: Created existing voice config")
        
        # Test 1: Pure acknowledgment
        print("\nTest 1: Pure acknowledgment with matching description")
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "acknowledged": True
        }
        
        reflection_output = {"voice_design": voice_design}
        await dreamer._process_voice_design(reflection_output)
        
        # Verify
        updated = await dreamer.memory.get_voice_config()
        if isinstance(updated, str):
            updated = json.loads(updated)
        
        assert updated["voice_id"] == existing_voice["voice_id"], "Voice ID should remain same"
        assert updated["acknowledged"] is True, "Voice should be acknowledged"
        assert updated["version"] == 1, "Version should not increment for pure acknowledgment"
        print("  ✓ Voice acknowledged correctly (no regeneration)")
        
        # Check events
        voice_events = [e for e in event_bus._captured_events if "VOICE" in e.type.value]
        acknowledged_events = [e for e in voice_events if e.type.value == "VOICE_ACKNOWLEDGED"]
        assert len(acknowledged_events) == 1, "Should emit VOICE_ACKNOWLEDGED event"
        print("  ✓ VOICE_ACKNOWLEDGED event emitted")
        
        # Test 2: Different description (should not be acknowledgment)
        print("\nTest 2: Different description should trigger redesign")
        event_bus._captured_events = []  # Clear events
        
        voice_design2 = {
            "description": "A dynamic, energetic voice with excitement",
            "gender": "female",
            "age": "young",
            "acknowledged": True
        }
        
        reflection_output2 = {"voice_design": voice_design2}
        await dreamer._process_voice_design(reflection_output2)
        
        # Verify - should increment version (redesign, not acknowledgment)
        updated2 = await dreamer.memory.get_voice_config()
        if isinstance(updated2, str):
            updated2 = json.loads(updated2)
        
        print(f"  Version after redesign: {updated2['version']}")
        print(f"  Description after redesign: {updated2['description'][:50]}...")
        assert updated2["version"] > 1, "Version should increment for redesign"
        print("  ✓ Different description triggered redesign, not acknowledgment")
        
        # Should NOT emit VOICE_ACKNOWLEDGED for redesign
        acknowledged_events2 = [e for e in event_bus._captured_events if e.type.value == "VOICE_ACKNOWLEDGED"]
        assert len(acknowledged_events2) == 0, "Should NOT emit VOICE_ACKNOWLEDGED for redesign"
        print("  ✓ No VOICE_ACKNOWLEDGED event for redesign")
        
    print("\n✅ All tests passed!\n")
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_basic_acknowledgment())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

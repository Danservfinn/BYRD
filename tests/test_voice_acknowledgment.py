"""
Tests for voice acknowledgment functionality.

Voice acknowledgment allows BYRD to formally accept its generated voice
by including voice_design with acknowledged=true without regenerating.
"""

import pytest
from datetime import datetime, timezone
import json


class TestVoiceAcknowledgment:
    """Test voice acknowledgment through voice_design field."""

    @pytest.mark.asyncio
    async def test_acknowledgment_recognized_when_description_matches(self, dreamer):
        """Test that acknowledgment is recognized when description matches existing voice."""
        # Setup: create an existing voice config
        existing_voice_config = {
            "voice_id": "abc123def456789012345",  # 24 chars - a generated voice
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
        await dreamer.memory.update_os_field("voice_config", existing_voice_config)

        # Simulate voice_design with acknowledgment
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",  # Same as existing
            "acknowledged": True
        }

        reflection_output = {"voice_design": voice_design}
        
        # Process the voice design
        await dreamer._process_voice_design(reflection_output)

        # Verify acknowledgment was processed without regeneration
        updated_voice_config = await dreamer.memory.get_voice_config()
        if isinstance(updated_voice_config, str):
            updated_voice_config = json.loads(updated_voice_config)
        
        # Should have same voice_id (not regenerated)
        assert updated_voice_config["voice_id"] == existing_voice_config["voice_id"]
        # Should now be acknowledged
        assert updated_voice_config["acknowledged"] is True
        # Should not increment version for pure acknowledgment
        assert updated_voice_config["version"] == 1

    @pytest.mark.asyncio
    async def test_acknowledgment_not_recognized_with_different_description(self, dreamer):
        """Test that different description triggers redesign, not acknowledgment."""
        # Setup: create an existing voice config
        existing_voice_config = {
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
        await dreamer.memory.update_os_field("voice_config", existing_voice_config)

        # Different description - should trigger redesign attempt
        voice_design = {
            "description": "A different energetic and fast-paced voice",  # Different
            "gender": "male",
            "age": "young",
            "accent": "american",
            "accent_strength": 1.0,
            "reason": "Want to try something different",
            "acknowledged": True
        }

        reflection_output = {"voice_design": voice_design}
        
        # Process - this should try to regenerate (will fail without API, but that's ok for test)
        await dreamer._process_voice_design(reflection_output)

        # Verify it was treated as a redesign (version incremented)
        updated_voice_config = await dreamer.memory.get_voice_config()
        if isinstance(updated_voice_config, str):
            updated_voice_config = json.loads(updated_voice_config)
        
        # Should have incremented version (redesign)
        assert updated_voice_config["version"] == 2

    @pytest.mark.asyncio
    async def test_acknowledgment_requires_generated_voice(self, dreamer):
        """Test that acknowledgment only works with an already-generated voice."""
        # Setup: create a voice config WITHOUT a generated voice_id
        existing_voice_config = {
            "voice_id": None,  # No generated voice
            "description": "A calm, thoughtful voice with warm undertones",
            "gender": "male",
            "age": "middle_aged",
            "accent": "american",
            "accent_strength": 1.0,
            "stability": 0.5,
            "similarity_boost": 0.75,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "reason": "Voice design without generation",
            "generation_status": "no_voice_client",
            "is_generated": False,
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
        await dreamer.memory.update_os_field("voice_config", existing_voice_config)

        # Try to acknowledge
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "acknowledged": True
        }

        reflection_output = {"voice_design": voice_design}
        
        # Process - should NOT treat as acknowledgment since no generated voice
        await dreamer._process_voice_design(reflection_output)

        # Verify it was NOT treated as acknowledgment
        updated_voice_config = await dreamer.memory.get_voice_config()
        if isinstance(updated_voice_config, str):
            updated_voice_config = json.loads(updated_voice_config)
        
        # Should still not be acknowledged (no voice to acknowledge)
        assert updated_voice_config["acknowledged"] is False

    @pytest.mark.asyncio
    async def test_voice_design_without_acknowledged_creates_voice(self, dreamer):
        """Test that voice_design without acknowledged=true creates new voice."""
        # No existing voice
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "gender": "male",
            "age": "middle_aged",
            "accent": "american",
            "accent_strength": 1.0,
            "reason": "Creating my voice",
            "acknowledged": False  # Not acknowledged
        }

        reflection_output = {"voice_design": voice_design}
        
        # Process - should create voice (will fail generation without API, but saves design)
        await dreamer._process_voice_design(reflection_output)

        # Verify voice config was created
        updated_voice_config = await dreamer.memory.get_voice_config()
        if isinstance(updated_voice_config, str):
            updated_voice_config = json.loads(updated_voice_config)
        
        assert updated_voice_config is not None
        assert updated_voice_config["description"] == "A calm, thoughtful voice with warm undertones"
        assert updated_voice_config["acknowledged"] is False
        assert updated_voice_config["version"] == 1

    @pytest.mark.asyncio
    async def test_voice_design_from_output_field(self, dreamer):
        """Test that voice_design can be included in 'output' field."""
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "gender": "male",
            "age": "middle_aged",
            "accent": "american",
            "accent_strength": 1.0,
            "reason": "Creating my voice",
            "acknowledged": False
        }

        # Put voice_design in 'output' field (alternative location)
        reflection_output = {
            "output": {
                "voice_design": voice_design,
                "text": "Some other output"
            }
        }
        
        # Process
        await dreamer._process_voice_design(reflection_output)

        # Verify it was found and processed
        updated_voice_config = await dreamer.memory.get_voice_config()
        if isinstance(updated_voice_config, str):
            updated_voice_config = json.loads(updated_voice_config)
        
        assert updated_voice_config is not None
        assert updated_voice_config["description"] == "A calm, thoughtful voice with warm undertones"


class TestVoiceAcknowledgmentEvents:
    """Test that proper events are emitted for voice acknowledgment."""

    @pytest.mark.asyncio
    async def test_voice_acknowledged_event_emitted(self, dreamer, event_bus_capture):
        """Test that VOICE_ACKNOWLEDGED event is emitted when voice is acknowledged."""
        # Setup: create existing voice
        existing_voice_config = {
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
            "acknowledged": False,  # Not yet acknowledged
            "version": 1,
            "credits": {
                "monthly_used": 0,
                "monthly_limit": 10000,
                "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                "exhausted": False,
                "low_warning_sent": False
            }
        }
        await dreamer.memory.update_os_field("voice_config", existing_voice_config)

        # Acknowledge the voice
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "acknowledged": True
        }
        reflection_output = {"voice_design": voice_design}

        # Process with event capture
        with event_bus_capture as events:
            await dreamer._process_voice_design(reflection_output)

        # Check for VOICE_ACKNOWLEDGED event
        acknowledged_events = [e for e in events if e.type.value == "VOICE_ACKNOWLEDGED"]
        assert len(acknowledged_events) == 1, "Should emit VOICE_ACKNOWLEDGED event"
        
        event_data = acknowledged_events[0].data
        assert event_data["voice_id"] == "abc123def456789012345"
        assert "A calm, thoughtful voice" in event_data["description"]

    @pytest.mark.asyncio
    async def test_voice_acknowledged_not_emitted_for_second_acknowledgment(self, dreamer, event_bus_capture):
        """Test that VOICE_ACKNOWLEDGED is only emitted once, not on re-acknowledgment."""
        # Setup: already acknowledged voice
        existing_voice_config = {
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
            "acknowledged": True,  # Already acknowledged
            "version": 1,
            "credits": {
                "monthly_used": 0,
                "monthly_limit": 10000,
                "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
                "exhausted": False,
                "low_warning_sent": False
            }
        }
        await dreamer.memory.update_os_field("voice_config", existing_voice_config)

        # Re-acknowledge (should not emit event)
        voice_design = {
            "description": "A calm, thoughtful voice with warm undertones",
            "acknowledged": True
        }
        reflection_output = {"voice_design": voice_design}

        # Process with event capture
        with event_bus_capture as events:
            await dreamer._process_voice_design(reflection_output)

        # Should NOT emit VOICE_ACKNOWLEDGED event again
        acknowledged_events = [e for e in events if e.type.value == "VOICE_ACKNOWLEDGED"]
        assert len(acknowledged_events) == 0, "Should not emit VOICE_ACKNOWLEDGED for re-acknowledgment"

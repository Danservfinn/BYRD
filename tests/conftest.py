"""
Pytest configuration and shared fixtures for BYRD test suite.

This file provides common fixtures used across multiple test modules,
including fixtures for voice acknowledgment testing.
"""

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from datetime import datetime, timezone
import json
import asyncio


@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""
    client = Mock()
    client.generate = AsyncMock(return_value="Test response")
    return client


@pytest.fixture
def mock_memory():
    """Mock Memory with minimal implementation for testing."""
    memory = Mock()
    
    # OS data storage
    memory._os_data = {
        "voice_config": None,
        "name": "TestByrd",
        "self_description": "A test instance of BYRD"
    }
    
    async def get_operating_system():
        return memory._os_data.copy()
    
    async def update_os_field(field, value):
        memory._os_data[field] = value
        return True
    
    async def get_voice_config():
        return memory._os_data.get("voice_config")
    
    async def record_experience(content, type="test", metadata=None):
        # Mock recording - just store for verification if needed
        return "exp_123"
    
    memory.get_operating_system = get_operating_system
    memory.update_os_field = update_os_field
    memory.get_voice_config = get_voice_config
    memory.record_experience = record_experience
    
    return memory


@pytest.fixture
def mock_event_bus():
    """Mock event bus for testing."""
    from event_bus import Event, EventType
    
    bus = Mock()
    bus._captured_events = []
    
    async def emit(event):
        bus._captured_events.append(event)
    
    bus.emit = emit
    
    return bus


@pytest.fixture
def event_bus_capture(mock_event_bus):
    """
    Context manager fixture for capturing events.
    
    Usage:
        with event_bus_capture as events:
            await some_function_that_emits_events()
        # Check events here
    """
    class EventBusCapture:
        def __init__(self, bus):
            self.bus = bus
            self.events_before = []
            
        def __enter__(self):
            # Capture current events state
            self.events_before = list(self.bus._captured_events)
            return self.bus._captured_events
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Events are captured in bus._captured_events
            pass
    
    return EventBusCapture(mock_event_bus)


@pytest.fixture
def dreamer(mock_memory, mock_llm_client, mock_event_bus):
    """
    Create a Dreamer instance with mocked dependencies for testing.
    
    This fixture provides a fully functional Dreamer instance that can be used
    to test voice design processing and acknowledgment functionality.
    """
    from dreamer import Dreamer
    
    # Minimal config for testing
    config = {
        "interval_seconds": 30,
        "context_window": 50,
        "semantic_search": {"enabled": False},
        "voice": {"enabled": True}
    }
    
    # Patch the event_bus module to use our mock
    with patch('dreamer.event_bus', mock_event_bus):
        dreamer_instance = Dreamer(
            memory=mock_memory,
            llm_client=mock_llm_client,
            config=config
        )
    
    return dreamer_instance


@pytest.fixture
def sample_voice_config():
    """Sample voice configuration for testing."""
    return {
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


@pytest.fixture
def voice_design_sample():
    """Sample voice_design object for testing."""
    return {
        "description": "A calm, thoughtful voice with warm undertones",
        "gender": "male",
        "age": "middle_aged",
        "accent": "american",
        "accent_strength": 1.0,
        "reason": "This voice represents my thoughtful nature",
        "acknowledged": False
    }


@pytest.fixture
def mock_voice_client():
    """
    Mock voice client for testing ElevenLabs integration.
    
    This can be used when you need to test voice generation
    without making actual API calls.
    """
    client = Mock()
    
    async def generate_voice(description, gender, age, accent, accent_strength):
        # Simulate successful voice generation
        return "xyz789uvw012345678901234", None  # voice_id, error
    
    async def synthesize(text, voice_id, voice_config):
        # Simulate audio synthesis
        return b"fake_audio_data", None  # audio_bytes, error
    
    client.generate_voice = generate_voice
    client.synthesize = synthesize
    
    return client


# Pytest async configuration
def pytest_configure(config):
    """Configure pytest for async tests."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )

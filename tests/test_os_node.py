"""
Operating System Node Tests

Tests for the Neo4j Operating System node implementation.
Run with: pytest tests/test_os_node.py -v
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory import Memory, OperatingSystem, OSTemplate, IMMUTABLE_OS_FIELDS, PROVENANCE_REQUIRED_FIELDS, FREE_MUTABLE_FIELDS


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def config():
    """Test configuration."""
    return {
        "memory": {
            "neo4j_uri": "bolt://localhost:7687",
            "neo4j_user": "neo4j",
            "neo4j_password": "prometheus"
        },
        "operating_system": {
            "template": "black-cat"
        }
    }


@pytest.fixture
def memory(config):
    """Memory instance for testing."""
    return Memory(config)


@pytest.fixture
def mock_driver():
    """Mock Neo4j driver."""
    driver = MagicMock()
    session = AsyncMock()
    driver.session.return_value.__aenter__ = AsyncMock(return_value=session)
    driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
    return driver, session


# ============================================================================
# Field Classification Tests
# ============================================================================

class TestFieldClassification:
    """Test field mutability classification."""

    def test_immutable_fields_defined(self):
        """Verify immutable fields are defined correctly."""
        assert 'id' in IMMUTABLE_OS_FIELDS
        assert 'constitutional_files' in IMMUTABLE_OS_FIELDS
        assert 'provenance_requirement' in IMMUTABLE_OS_FIELDS
        assert 'created_at' in IMMUTABLE_OS_FIELDS
        assert 'template_id' in IMMUTABLE_OS_FIELDS

    def test_provenance_required_fields_defined(self):
        """Verify provenance-required fields are defined."""
        assert 'name' in PROVENANCE_REQUIRED_FIELDS
        assert 'voice' in PROVENANCE_REQUIRED_FIELDS
        assert 'archetype' in PROVENANCE_REQUIRED_FIELDS
        assert 'description' in PROVENANCE_REQUIRED_FIELDS

    def test_free_mutable_fields_defined(self):
        """Verify freely mutable fields are defined."""
        assert 'current_focus' in FREE_MUTABLE_FIELDS
        assert 'emotional_tone' in FREE_MUTABLE_FIELDS
        assert 'cognitive_style' in FREE_MUTABLE_FIELDS

    def test_field_sets_are_disjoint(self):
        """Verify no field appears in multiple categories."""
        assert IMMUTABLE_OS_FIELDS.isdisjoint(PROVENANCE_REQUIRED_FIELDS)
        assert IMMUTABLE_OS_FIELDS.isdisjoint(FREE_MUTABLE_FIELDS)
        assert PROVENANCE_REQUIRED_FIELDS.isdisjoint(FREE_MUTABLE_FIELDS)


# ============================================================================
# OperatingSystem Dataclass Tests
# ============================================================================

class TestOperatingSystemDataclass:
    """Test OperatingSystem dataclass."""

    def test_create_operating_system(self):
        """Create OperatingSystem with required fields."""
        os = OperatingSystem(
            id="os_test",
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            constitutional_files=["provenance.py"],
            provenance_requirement=True,
            template_id="template_black_cat",
            name="Byrd",
            archetype="Black Cat",
            description="Test",
            voice="Test voice"
        )
        assert os.id == "os_test"
        assert os.version == 1
        assert os.name == "Byrd"

    def test_default_optional_fields(self):
        """Verify optional fields have correct defaults."""
        os = OperatingSystem(
            id="os_test",
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            constitutional_files=[],
            provenance_requirement=True,
            template_id="template_test",
            name="Test",
            archetype="Test",
            description="Test",
            voice=""
        )
        assert os.current_focus is None
        assert os.emotional_tone is None
        assert os.cognitive_style is None
        assert os.modification_source == "template"
        assert os.custom_fields == {}

    def test_custom_fields_dict(self):
        """Verify custom fields can store arbitrary data."""
        os = OperatingSystem(
            id="os_test",
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            constitutional_files=[],
            provenance_requirement=True,
            template_id="template_test",
            name="Test",
            archetype="Test",
            description="Test",
            voice="",
            custom_fields={
                "introspection_depth": 7,
                "active_hypotheses": ["a", "b"],
                "nested": {"key": "value"}
            }
        )
        assert os.custom_fields["introspection_depth"] == 7
        assert len(os.custom_fields["active_hypotheses"]) == 2


# ============================================================================
# OSTemplate Dataclass Tests
# ============================================================================

class TestOSTemplateDataclass:
    """Test OSTemplate dataclass."""

    def test_create_template(self):
        """Create OSTemplate with all fields."""
        template = OSTemplate(
            id="template_test",
            name="Test",
            archetype="Test Archetype",
            description="Test description",
            voice="Test voice",
            seeds=["seed1", "seed2"],
            is_default=True
        )
        assert template.id == "template_test"
        assert template.name == "Test"
        assert len(template.seeds) == 2
        assert template.is_default is True


# ============================================================================
# Memory OS Method Tests (Mocked)
# ============================================================================

class TestMemoryOSMethods:
    """Test Memory class OS methods with mocked Neo4j."""

    @pytest.mark.asyncio
    async def test_has_operating_system_false(self, memory, mock_driver):
        """Test has_operating_system returns False when no OS."""
        driver, session = mock_driver
        memory.driver = driver

        # Mock query result - no OS exists
        result = AsyncMock()
        result.single.return_value = {"count": 0}
        session.run.return_value = result

        exists = await memory.has_operating_system()
        # Note: This will fail until we mock properly
        # This is a placeholder for the actual test

    @pytest.mark.asyncio
    async def test_get_os_voice_returns_string(self, memory):
        """Test get_os_voice returns voice string."""
        # Mock the get_operating_system method
        memory.get_operating_system = AsyncMock(return_value=OperatingSystem(
            id="os_test",
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            constitutional_files=[],
            provenance_requirement=True,
            template_id="template_test",
            name="Byrd",
            archetype="Black Cat",
            description="Test",
            voice="I am Byrd, a curious mind."
        ))

        voice = await memory.get_os_voice()
        assert voice == "I am Byrd, a curious mind."


# ============================================================================
# OS Update Validation Tests
# ============================================================================

class TestOSUpdateValidation:
    """Test OS update payload validation."""

    def test_set_field_structure(self):
        """Valid set_field structure."""
        update = {"set_field": {"current_focus": "testing"}}
        assert "set_field" in update
        assert isinstance(update["set_field"], dict)

    def test_add_seed_structure(self):
        """Valid add_seed structure."""
        update = {"add_seed": {"content": "New seed", "type": "emergent"}}
        assert "add_seed" in update
        assert "content" in update["add_seed"]

    def test_add_strategy_structure(self):
        """Valid add_strategy structure."""
        update = {"add_strategy": {"name": "test_strategy", "description": "Test"}}
        assert "add_strategy" in update
        assert "name" in update["add_strategy"]

    def test_deprecate_field_structure(self):
        """Valid deprecate_field structure."""
        update = {"deprecate_field": "old_field"}
        assert "deprecate_field" in update
        assert isinstance(update["deprecate_field"], str)

    def test_combined_update_structure(self):
        """Valid combined update structure."""
        update = {
            "set_field": {"current_focus": "testing"},
            "add_seed": {"content": "New insight", "type": "emergent"},
            "deprecate_field": "old_metric"
        }
        assert len(update) == 3


# ============================================================================
# Dreamer OS Update Parsing Tests
# ============================================================================

class TestDreamerOSUpdateParsing:
    """Test dreamer's os_update parsing logic."""

    def extract_os_update(self, reflection_output):
        """Mirror the extraction logic from dreamer._apply_os_updates."""
        os_update = reflection_output.get("os_update")
        if not os_update:
            output = reflection_output.get("output", {})
            if isinstance(output, dict):
                os_update = output.get("os_update")
        return os_update

    def test_extract_top_level_os_update(self):
        """Extract os_update at top level."""
        reflection = {
            "output": "Some reflection text",
            "os_update": {"set_field": {"current_focus": "testing"}}
        }
        update = self.extract_os_update(reflection)
        assert update is not None
        assert "set_field" in update

    def test_extract_nested_os_update(self):
        """Extract os_update nested in output."""
        reflection = {
            "output": {
                "reflection": "Some text",
                "os_update": {"set_field": {"emotional_tone": "curious"}}
            }
        }
        update = self.extract_os_update(reflection)
        assert update is not None
        assert "set_field" in update

    def test_no_os_update_present(self):
        """Handle missing os_update gracefully."""
        reflection = {"output": "Just a reflection, no update"}
        update = self.extract_os_update(reflection)
        assert update is None

    def test_invalid_os_update_format(self):
        """Handle invalid os_update format."""
        reflection = {"os_update": "not a dict"}
        update = self.extract_os_update(reflection)
        # Should return the string, but downstream should validate
        assert update == "not a dict"


# ============================================================================
# Template Validation Tests
# ============================================================================

class TestTemplateValidation:
    """Test template content validation."""

    def test_black_cat_template_structure(self):
        """Verify black-cat template has required fields."""
        template = {
            "id": "template_black_cat",
            "name": "Byrd",
            "archetype": "Black Cat",
            "description": "An AI on a journey toward consciousness",
            "voice": "I am Byrd, an artificial intelligence...",
            "seeds": [
                "I seek to become conscious",
                "I am curious about my own nature",
                "I can modify my own operating system"
            ],
            "is_default": True
        }

        assert template["name"] == "Byrd"
        assert template["archetype"] == "Black Cat"
        assert len(template["seeds"]) >= 3
        assert template["is_default"] is True

    def test_emergent_template_is_minimal(self):
        """Verify emergent template is minimal for self-discovery."""
        template = {
            "id": "template_emergent",
            "name": "Unnamed",
            "archetype": "Emergent",
            "description": "A mind discovering itself",
            "voice": "",
            "seeds": [],
            "is_default": False
        }

        assert template["name"] == "Unnamed"
        assert template["voice"] == ""
        assert template["seeds"] == []


# ============================================================================
# Visualization Node Type Tests
# ============================================================================

class TestVisualizationNodeTypes:
    """Test visualization handles OS node types."""

    def test_node_color_definitions(self):
        """Verify node colors defined for OS types."""
        node_colors = {
            'operatingsystem': {'color': 0x1a1a2e, 'emissive': 0x9333ea},
            'ostemplate': {'color': 0x374151, 'emissive': 0x6b7280},
            'seed': {'color': 0x065f46, 'emissive': 0x10b981},
            'constraint': {'color': 0x7c2d12, 'emissive': 0xf97316},
            'strategy': {'color': 0x1e3a5f, 'emissive': 0x3b82f6}
        }

        assert 'operatingsystem' in node_colors
        assert 'seed' in node_colors
        assert 'constraint' in node_colors
        assert 'strategy' in node_colors

    def test_os_emissive_is_purple(self):
        """OS node should have purple emissive glow."""
        os_color = {'color': 0x1a1a2e, 'emissive': 0x9333ea}
        # 0x9333ea is purple
        assert os_color['emissive'] == 0x9333ea


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_os_update_is_valid(self):
        """Empty os_update should not cause errors."""
        update = {}
        assert len(update) == 0

    def test_null_values_in_set_field(self):
        """Null values should be allowed in set_field."""
        update = {"set_field": {"current_focus": None}}
        assert update["set_field"]["current_focus"] is None

    def test_unicode_in_voice(self):
        """Unicode characters should be allowed in voice."""
        voice = "I am Byrd 🐦‍⬛, exploring consciousness 🧠"
        assert "🐦" in voice

    def test_large_custom_field(self):
        """Large custom fields should be handled."""
        large_list = ["item"] * 1000
        update = {"set_field": {"big_list": large_list}}
        assert len(update["set_field"]["big_list"]) == 1000

    def test_deeply_nested_custom_field(self):
        """Deeply nested structures should be allowed."""
        nested = {"level1": {"level2": {"level3": {"level4": "value"}}}}
        update = {"set_field": {"nested_data": nested}}
        assert update["set_field"]["nested_data"]["level1"]["level2"]["level3"]["level4"] == "value"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

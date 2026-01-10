"""
Tests for BYRD FastAPI server endpoints.

This module tests the REST API endpoints defined in server.py.
Uses pytest-asyncio for async test support and httpx for async HTTP client.
"""

import pytest
import pytest_asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import json


# Mock BYRD and related modules before importing server
@pytest.fixture(autouse=True)
def mock_byrd_modules(monkeypatch):
    """Mock BYRD-related modules to prevent Neo4j and LLM connections."""
    # Mock the BYRD class
    mock_byrd_instance = Mock()
    mock_byrd_instance.is_running = False
    mock_byrd_instance.dreamer = Mock()
    mock_byrd_instance.dreamer.dream_count = 5
    mock_byrd_instance.seeker = Mock()
    mock_byrd_instance.seeker.seek_count = 10
    mock_byrd_instance.memory = AsyncMock()
    mock_byrd_instance.memory.get_all_capabilities = AsyncMock(return_value=[])
    mock_byrd_instance.memory.get_all_desires = AsyncMock(return_value=[])
    mock_byrd_instance.memory.get_all_beliefs = AsyncMock(return_value=[])
    mock_byrd_instance.memory.get_recent_experiences = AsyncMock(return_value=[])
    mock_byrd_instance.memory.get_recent_reflections = AsyncMock(return_value=[])
    mock_byrd_instance.memory.create_experience = AsyncMock(return_value="exp_123")
    mock_byrd_instance.start = AsyncMock()
    mock_byrd_instance.stop = AsyncMock()
    mock_byrd_instance.get_state = Mock(return_value={})
    mock_byrd_instance.llm_client = Mock()
    mock_byrd_instance.voice = None
    mock_byrd_instance.rsi_engine = Mock()
    mock_byrd_instance.rsi_engine.current_phase = "idle"
    mock_byrd_instance.rsi_engine.cycle_count = 0
    mock_byrd_instance.rsi_engine.get_metrics = Mock(return_value={})
    mock_byrd_instance.rsi_engine.start_cycle = AsyncMock()
    mock_byrd_instance.rsi_engine.stop_cycle = AsyncMock()

    # Mock BYRD class constructor
    mock_byrd_class = Mock(return_value=mock_byrd_instance)
    monkeypatch.setattr("server.BYRD", mock_byrd_class)

    # Mock load_kernel
    mock_kernel = {"name": "test_kernel", "seed": {}}
    monkeypatch.setattr("server.load_kernel", Mock(return_value=mock_kernel))

    return mock_byrd_instance


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    from server import app as fastapi_app
    return fastapi_app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client(app):
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoints:
    """Tests for health and status endpoints."""

    def test_health_endpoint(self, client):
        """Test /health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_version_endpoint(self, client):
        """Test /api/version endpoint returns version info."""
        response = client.get("/api/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "name" in data


class TestStatusEndpoint:
    """Tests for /api/status endpoint."""

    def test_status_returns_system_info(self, client, mock_byrd_modules):
        """Test /api/status returns correct system info."""
        mock_byrd_modules.is_running = False
        mock_byrd_modules.dreamer.dream_count = 5
        mock_byrd_modules.seeker.seek_count = 10

        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()

        assert "running" in data
        assert "dream_count" in data
        assert "seek_count" in data

    def test_status_when_running(self, client, mock_byrd_modules):
        """Test /api/status when BYRD is running."""
        mock_byrd_modules.is_running = True

        response = client.get("/api/status")
        assert response.status_code == 200


class TestRSIEndpoints:
    """Tests for RSI-related endpoints."""

    def test_rsi_status_endpoint(self, client, mock_byrd_modules):
        """Test /api/rsi/status returns RSI status."""
        mock_byrd_modules.rsi_engine.current_phase = "reflect"
        mock_byrd_modules.rsi_engine.cycle_count = 42

        response = client.get("/api/rsi/status")
        assert response.status_code == 200
        data = response.json()

        assert "current_phase" in data
        assert "cycle_number" in data

    def test_rsi_metrics_endpoint(self, client, mock_byrd_modules):
        """Test /api/rsi/metrics returns metrics."""
        mock_byrd_modules.rsi_engine.get_metrics.return_value = {
            "cycles_completed": 100,
            "average_improvement": 0.02,
        }

        response = client.get("/api/rsi/metrics")
        assert response.status_code == 200

    def test_rsi_phases_endpoint(self, client):
        """Test /api/rsi/phases returns phase list."""
        response = client.get("/api/rsi/phases")
        assert response.status_code == 200
        data = response.json()

        # Should return list of phases
        assert "phases" in data or isinstance(data, list)

    def test_rsi_cycle_start(self, client, mock_byrd_modules):
        """Test POST /api/rsi/cycle starts a cycle."""
        response = client.post("/api/rsi/cycle")
        assert response.status_code == 200

    def test_rsi_cycle_stop(self, client, mock_byrd_modules):
        """Test POST /api/rsi/stop stops a cycle."""
        response = client.post("/api/rsi/stop")
        assert response.status_code == 200


class TestGovernanceEndpoints:
    """Tests for governance-related endpoints."""

    def test_governance_direction_get(self, client):
        """Test GET /api/governance/direction."""
        response = client.get("/api/governance/direction")
        # May return 200 with direction or 404 if no direction set
        assert response.status_code in [200, 404]

    def test_governance_direction_post(self, client):
        """Test POST /api/governance/direction."""
        response = client.post(
            "/api/governance/direction",
            json={"content": "Focus on capability improvements"}
        )
        assert response.status_code == 200

    def test_governance_command(self, client):
        """Test POST /api/governance/command."""
        response = client.post(
            "/api/governance/command",
            json={"command": "status"}
        )
        assert response.status_code == 200

    def test_governance_history(self, client):
        """Test GET /api/governance/history."""
        response = client.get("/api/governance/history")
        assert response.status_code == 200

    def test_inject_desire(self, client, mock_byrd_modules):
        """Test POST /api/governance/inject-desire."""
        mock_byrd_modules.memory.create_desire = AsyncMock(return_value="desire_123")

        response = client.post(
            "/api/governance/inject-desire",
            json={
                "description": "Improve reasoning capability",
                "urgency": 0.8
            }
        )
        assert response.status_code == 200

    def test_get_injected_desires(self, client, mock_byrd_modules):
        """Test GET /api/governance/desires."""
        response = client.get("/api/governance/desires")
        assert response.status_code == 200


class TestVerificationEndpoints:
    """Tests for verification-related endpoints."""

    def test_verification_status(self, client):
        """Test GET /api/verification/status."""
        response = client.get("/api/verification/status")
        assert response.status_code == 200

    def test_human_anchoring_queue(self, client):
        """Test GET /api/verification/human-anchoring."""
        response = client.get("/api/verification/human-anchoring")
        assert response.status_code == 200

    def test_process_human_validation(self, client):
        """Test POST /api/verification/human-anchoring/{request_id}."""
        response = client.post(
            "/api/verification/human-anchoring/req_123",
            json={"approved": True, "notes": "Looks good"}
        )
        # May return 200 or 404 depending on whether request exists
        assert response.status_code in [200, 404]


class TestMemoryEndpoints:
    """Tests for memory-related endpoints."""

    def test_beliefs_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/beliefs."""
        mock_byrd_modules.memory.get_all_beliefs.return_value = [
            {"id": "b1", "content": "Test belief", "confidence": 0.9}
        ]

        response = client.get("/api/beliefs")
        assert response.status_code == 200

    def test_desires_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/desires."""
        mock_byrd_modules.memory.get_all_desires.return_value = [
            {"id": "d1", "description": "Test desire", "intensity": 0.8}
        ]

        response = client.get("/api/desires")
        assert response.status_code == 200

    def test_capabilities_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/capabilities."""
        mock_byrd_modules.memory.get_all_capabilities.return_value = [
            {"name": "reasoning", "level": 0.8}
        ]

        response = client.get("/api/capabilities")
        assert response.status_code == 200

    def test_memory_graph(self, client):
        """Test GET /api/memory/graph."""
        response = client.get("/api/memory/graph")
        assert response.status_code == 200


class TestEconomicEndpoints:
    """Tests for economic-related endpoints."""

    def test_treasury_endpoint(self, client):
        """Test GET /api/economic/treasury."""
        response = client.get("/api/economic/treasury")
        assert response.status_code == 200

    def test_revenue_endpoint(self, client):
        """Test GET /api/economic/revenue."""
        response = client.get("/api/economic/revenue")
        assert response.status_code == 200

    def test_marketplace_endpoint(self, client):
        """Test GET /api/economic/marketplace."""
        response = client.get("/api/economic/marketplace")
        assert response.status_code == 200


class TestPlasticityEndpoints:
    """Tests for plasticity-related endpoints."""

    def test_modules_endpoint(self, client):
        """Test GET /api/plasticity/modules."""
        response = client.get("/api/plasticity/modules")
        assert response.status_code == 200

    def test_nas_endpoint(self, client):
        """Test GET /api/plasticity/nas."""
        response = client.get("/api/plasticity/nas")
        assert response.status_code == 200


class TestScalingEndpoints:
    """Tests for scaling-related endpoints."""

    def test_scaling_metrics(self, client):
        """Test GET /api/scaling/metrics."""
        response = client.get("/api/scaling/metrics")
        assert response.status_code == 200

    def test_scaling_drift(self, client):
        """Test GET /api/scaling/drift."""
        response = client.get("/api/scaling/drift")
        assert response.status_code == 200


class TestSystemControlEndpoints:
    """Tests for system control endpoints."""

    def test_start_endpoint(self, client, mock_byrd_modules):
        """Test POST /api/start."""
        response = client.post("/api/start")
        assert response.status_code == 200

    def test_stop_endpoint(self, client, mock_byrd_modules):
        """Test POST /api/stop."""
        response = client.post("/api/stop")
        assert response.status_code == 200

    def test_reset_endpoint(self, client, mock_byrd_modules):
        """Test POST /api/reset."""
        response = client.post(
            "/api/reset",
            json={"hard_reset": False}
        )
        assert response.status_code == 200

    def test_system_status(self, client):
        """Test GET /api/system/status."""
        response = client.get("/api/system/status")
        assert response.status_code == 200

    def test_system_reset(self, client):
        """Test POST /api/system/reset."""
        response = client.post("/api/system/reset")
        assert response.status_code == 200


class TestKernelEndpoints:
    """Tests for kernel configuration endpoints."""

    def test_get_kernel(self, client):
        """Test GET /api/kernel."""
        response = client.get("/api/kernel")
        assert response.status_code == 200

    def test_kernel_debug(self, client):
        """Test GET /api/kernel-debug."""
        response = client.get("/api/kernel-debug")
        assert response.status_code == 200


class TestLLMConfigEndpoints:
    """Tests for LLM configuration endpoints."""

    def test_get_llm_config(self, client):
        """Test GET /api/llm-config."""
        response = client.get("/api/llm-config")
        assert response.status_code == 200

    def test_llm_debug(self, client):
        """Test GET /api/llm-debug."""
        response = client.get("/api/llm-debug")
        assert response.status_code == 200


class TestHistoryEndpoints:
    """Tests for history-related endpoints."""

    def test_history_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/history."""
        mock_byrd_modules.memory.get_recent_experiences.return_value = []
        mock_byrd_modules.memory.get_recent_reflections.return_value = []

        response = client.get("/api/history")
        assert response.status_code == 200

    def test_experiences_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/experiences."""
        mock_byrd_modules.memory.get_recent_experiences.return_value = []

        response = client.get("/api/experiences")
        assert response.status_code == 200


class TestRollbackEndpoints:
    """Tests for rollback-related endpoints."""

    def test_rollback_history(self, client):
        """Test GET /api/rollback/history."""
        response = client.get("/api/rollback/history")
        assert response.status_code == 200


class TestCorrigibilityEndpoints:
    """Tests for corrigibility endpoints."""

    def test_get_corrigibility(self, client):
        """Test GET /api/corrigibility."""
        response = client.get("/api/corrigibility")
        assert response.status_code == 200


class TestGraphEndpoints:
    """Tests for graph visualization endpoints."""

    def test_graph_endpoint(self, client, mock_byrd_modules):
        """Test GET /api/graph."""
        mock_byrd_modules.memory.get_graph_data = AsyncMock(return_value={
            "nodes": [],
            "edges": []
        })

        response = client.get("/api/graph")
        assert response.status_code == 200

    def test_graph_topology(self, client, mock_byrd_modules):
        """Test GET /api/graph/topology."""
        mock_byrd_modules.memory.get_topology = AsyncMock(return_value={
            "layers": [],
            "connections": []
        })

        response = client.get("/api/graph/topology")
        assert response.status_code == 200


class TestRalphEndpoints:
    """Tests for Ralph Loop endpoints."""

    def test_ralph_status(self, client):
        """Test GET /api/ralph/status."""
        response = client.get("/api/ralph/status")
        assert response.status_code == 200

    def test_ralph_consciousness(self, client):
        """Test GET /api/ralph/consciousness."""
        response = client.get("/api/ralph/consciousness")
        assert response.status_code == 200

    def test_ralph_emergence(self, client):
        """Test GET /api/ralph/emergence."""
        response = client.get("/api/ralph/emergence")
        assert response.status_code == 200


class TestConsciousnessEndpoints:
    """Tests for consciousness frame endpoints."""

    def test_consciousness_frames(self, client):
        """Test GET /api/consciousness/frames."""
        response = client.get("/api/consciousness/frames")
        assert response.status_code == 200


class TestLatticeEndpoints:
    """Tests for verification lattice endpoints."""

    def test_rsi_lattice(self, client):
        """Test GET /api/rsi/lattice."""
        response = client.get("/api/rsi/lattice")
        assert response.status_code == 200


class TestMessagesEndpoints:
    """Tests for message-related endpoints."""

    def test_get_messages(self, client, mock_byrd_modules):
        """Test GET /api/messages."""
        mock_byrd_modules.memory.get_messages = AsyncMock(return_value=[])

        response = client.get("/api/messages")
        assert response.status_code == 200

    def test_unread_count(self, client, mock_byrd_modules):
        """Test GET /api/messages/unread-count."""
        mock_byrd_modules.memory.get_unread_count = AsyncMock(return_value=0)

        response = client.get("/api/messages/unread-count")
        assert response.status_code == 200

    def test_message_stats(self, client, mock_byrd_modules):
        """Test GET /api/messages/stats."""
        mock_byrd_modules.memory.get_message_stats = AsyncMock(return_value={
            "total": 0,
            "unread": 0
        })

        response = client.get("/api/messages/stats")
        assert response.status_code == 200


class TestLoopMetricsEndpoints:
    """Tests for loop metrics endpoints."""

    def test_loop_metrics(self, client):
        """Test GET /api/loop-metrics."""
        response = client.get("/api/loop-metrics")
        assert response.status_code == 200

    def test_loop_metrics_summary(self, client):
        """Test GET /api/loop-metrics/summary."""
        response = client.get("/api/loop-metrics/summary")
        assert response.status_code == 200


class TestHealthLearningEndpoints:
    """Tests for health learning endpoints."""

    def test_health_learning(self, client):
        """Test GET /api/health/learning."""
        response = client.get("/api/health/learning")
        assert response.status_code == 200

    def test_health_graphiti(self, client):
        """Test GET /api/health/graphiti."""
        response = client.get("/api/health/graphiti")
        assert response.status_code == 200


class TestArchitectureEndpoint:
    """Tests for architecture endpoint."""

    def test_architecture(self, client):
        """Test GET /api/architecture."""
        response = client.get("/api/architecture")
        assert response.status_code == 200
        data = response.json()

        # Should contain architecture information
        assert isinstance(data, dict)


class TestCrystalsEndpoints:
    """Tests for crystal (heuristic) endpoints."""

    def test_get_crystals(self, client, mock_byrd_modules):
        """Test GET /api/crystals."""
        mock_byrd_modules.memory.get_crystals = AsyncMock(return_value=[])

        response = client.get("/api/crystals")
        assert response.status_code == 200

    def test_crystals_stats(self, client, mock_byrd_modules):
        """Test GET /api/crystals/stats."""
        mock_byrd_modules.memory.get_crystal_stats = AsyncMock(return_value={
            "total": 0,
            "by_type": {}
        })

        response = client.get("/api/crystals/stats")
        assert response.status_code == 200


class TestTaskEndpoints:
    """Tests for task-related endpoints."""

    def test_create_task(self, client, mock_byrd_modules):
        """Test POST /api/task."""
        mock_byrd_modules.memory.create_task = AsyncMock(return_value="task_123")

        response = client.post(
            "/api/task",
            json={"description": "Test task", "priority": "high"}
        )
        assert response.status_code == 200

    def test_get_tasks(self, client, mock_byrd_modules):
        """Test GET /api/tasks."""
        mock_byrd_modules.memory.get_tasks = AsyncMock(return_value=[])

        response = client.get("/api/tasks")
        assert response.status_code == 200


class TestPredictionsEndpoint:
    """Tests for predictions endpoint."""

    def test_predictions(self, client, mock_byrd_modules):
        """Test GET /api/predictions."""
        mock_byrd_modules.memory.get_predictions = AsyncMock(return_value=[])

        response = client.get("/api/predictions")
        assert response.status_code == 200


class TestOrphansEndpoints:
    """Tests for orphan node endpoints."""

    def test_get_orphans(self, client, mock_byrd_modules):
        """Test GET /api/orphans."""
        mock_byrd_modules.memory.get_orphan_nodes = AsyncMock(return_value=[])

        response = client.get("/api/orphans")
        assert response.status_code == 200

    def test_orphans_stats(self, client, mock_byrd_modules):
        """Test GET /api/orphans/stats."""
        mock_byrd_modules.memory.get_orphan_stats = AsyncMock(return_value={
            "total": 0,
            "by_type": {}
        })

        response = client.get("/api/orphans/stats")
        assert response.status_code == 200


class TestOmegaMetricsEndpoint:
    """Tests for omega metrics endpoint."""

    def test_omega_metrics(self, client, mock_byrd_modules):
        """Test GET /api/omega/metrics."""
        mock_byrd_modules.omega = Mock()
        mock_byrd_modules.omega.get_metrics = Mock(return_value={
            "coherence": 0.85,
            "emergence": 0.72
        })

        response = client.get("/api/omega/metrics")
        assert response.status_code == 200


class TestAGIComprehensiveEndpoint:
    """Tests for AGI comprehensive endpoint."""

    def test_agi_comprehensive(self, client):
        """Test GET /api/agi/comprehensive."""
        response = client.get("/api/agi/comprehensive")
        assert response.status_code == 200


class TestGenesisEndpoint:
    """Tests for genesis endpoint."""

    def test_genesis(self, client):
        """Test GET /api/genesis."""
        response = client.get("/api/genesis")
        assert response.status_code == 200


class TestNarratorEndpoint:
    """Tests for narrator summary endpoint."""

    def test_narrator_summary(self, client):
        """Test GET /api/narrator-summary."""
        response = client.get("/api/narrator-summary")
        assert response.status_code == 200


class TestPortraitEndpoints:
    """Tests for portrait endpoints."""

    def test_get_portrait(self, client):
        """Test GET /api/portrait."""
        response = client.get("/api/portrait")
        assert response.status_code in [200, 404]

    def test_post_portrait(self, client):
        """Test POST /api/portrait."""
        response = client.post(
            "/api/portrait",
            json={"description": "Test portrait"}
        )
        assert response.status_code in [200, 400, 422]


class TestAwakenEndpoint:
    """Tests for awaken endpoint."""

    def test_awaken(self, client, mock_byrd_modules):
        """Test POST /api/awaken."""
        response = client.post("/api/awaken")
        assert response.status_code == 200


# Async tests for WebSocket and other async endpoints
class TestAsyncEndpoints:
    """Async tests using httpx AsyncClient."""

    @pytest.mark.asyncio
    async def test_async_status(self, async_client):
        """Test status endpoint asynchronously."""
        response = await async_client.get("/api/status")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_async_health(self, async_client):
        """Test health endpoint asynchronously."""
        response = await async_client.get("/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_async_rsi_status(self, async_client):
        """Test RSI status endpoint asynchronously."""
        response = await async_client.get("/api/rsi/status")
        assert response.status_code == 200

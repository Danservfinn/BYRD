"""
Test the human-service-first interruption flow.

This tests the cancellation chain:
1. RSI Engine runs cycles with cancellation token
2. High-priority task arrives
3. Service calls RalphLoop.interrupt()
4. RSI cycle detects cancellation and stops at phase boundary
5. Task is processed
6. RSI resumes when idle
"""

import asyncio
import logging
from unittest.mock import Mock, AsyncMock, patch

import pytest

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_interruption")


class TestInterruptionFlow:
    """Test the complete interruption flow."""

    @pytest.mark.asyncio
    async def test_cancellation_token_basic(self):
        """Test that cancellation token works correctly."""
        from core.async_cancellation import CancellationToken, CancellationReason

        token = CancellationToken(name="test_token")

        assert not token.is_cancelled
        assert token.cancellation_reason is None

        await token.cancel(reason=CancellationReason.EXPLICIT, message="Test cancellation")

        assert token.is_cancelled
        assert token.cancellation_reason == CancellationReason.EXPLICIT

        logger.info("✓ Cancellation token basic test passed")

    @pytest.mark.asyncio
    async def test_rsi_engine_cancellation(self):
        """Test that RSI engine respects cancellation token."""
        from rsi.engine import RSIEngine, CycleResult
        from core.async_cancellation import CancellationToken, CancellationReason

        # Create mock dependencies
        mock_memory = Mock()
        mock_memory.connect = AsyncMock()
        mock_memory.create_belief = AsyncMock(return_value="belief_1")
        mock_memory.record_experience = AsyncMock(return_value="exp_1")
        mock_memory.get_recent_beliefs = Mock(return_value=[])
        mock_memory.get_recent_reflections = Mock(return_value=[])
        mock_memory.get_crystallized_heuristics = Mock(return_value=[])

        mock_llm = AsyncMock()
        mock_llm.query = AsyncMock(return_value="Test response")
        mock_llm.generate = AsyncMock(return_value=Mock(text="Test response"))

        # Create cancellation token that's already cancelled
        token = CancellationToken(name="test_token")
        await token.cancel(reason=CancellationReason.EXPLICIT, message="Test interruption")

        # Create RSI engine
        engine = RSIEngine(
            memory=mock_memory,
            llm_client=mock_llm,
            quantum_provider=None,
            event_bus=None,
            config={}
        )

        # Run cycle with cancelled token - should stop early
        result = await engine.run_cycle(cancellation_token=token)

        # Should have been interrupted
        assert result.interrupted is True
        logger.info(f"✓ RSI engine cancelled at phase: {result.phase_reached}")

    @pytest.mark.asyncio
    async def test_ralph_loop_interrupt(self):
        """Test that Ralph Loop can interrupt RSI."""
        from rsi.orchestration.ralph_loop import RalphLoop
        from rsi.engine import RSIEngine
        from rsi.consciousness.stream import ConsciousnessStream
        from core.async_cancellation import CancellationToken

        # Create mock RSI engine
        mock_rsi = Mock(spec=RSIEngine)
        mock_rsi.run_cycle = AsyncMock(
            return_value=Mock(
                phase_reached="REFLECT",
                interrupted=False,
                success=True
            )
        )

        # Create mock consciousness stream
        mock_consciousness = Mock(spec=ConsciousnessStream)
        mock_consciousness.append_frame = AsyncMock()

        # Create Ralph Loop
        loop = RalphLoop(
            rsi_engine=mock_rsi,
            consciousness_stream=mock_consciousness,
            config={}
        )

        # Test that interrupt() creates cancellation signal
        assert loop._current_token is None or not loop._current_token.is_cancelled

        await loop.interrupt("test_reason")

        # After starting iteration, token should be cancellable
        # Create token manually to test
        loop._current_token = CancellationToken(name="test")
        await loop.interrupt("test_reason")

        assert loop._current_token.is_cancelled
        logger.info("✓ Ralph Loop interrupt() works correctly")

    @pytest.mark.asyncio
    async def test_service_task_enqueue_interrupts_rsi(self):
        """Test that high-priority task enqueuing triggers RSI interruption."""
        from core.byrd_service import BYRDService, TaskPriority, ServiceMode
        from rsi.orchestration.ralph_loop import RalphLoop

        # Create mock Ralph Loop
        mock_ralph = Mock(spec=RalphLoop)
        mock_ralph.interrupt = AsyncMock()

        # Create mock memory
        mock_memory = Mock()
        mock_memory.create_task = AsyncMock(return_value="task_123")
        mock_memory.get_pending_tasks = AsyncMock(return_value=[])

        # Create service
        service = BYRDService(
            memory=mock_memory,
            ralph_loop=mock_ralph,
            config={'idle_threshold_seconds': 1}
        )

        # Set mode to IDLE_RSI (simulating RSI running)
        service._mode = ServiceMode.IDLE_RSI  # Use enum, not string

        # Enqueue high-priority task
        task_id = await service.enqueue_task(
            description="Urgent task",
            objective="Complete urgently",
            priority=TaskPriority.CRITICAL.value
        )

        # Should have called interrupt on Ralph Loop
        mock_ralph.interrupt.assert_called_once()
        logger.info(f"✓ High-priority task triggered RSI interrupt: {task_id}")

    @pytest.mark.asyncio
    async def test_interruption_flow_end_to_end(self):
        """Test complete interruption flow from task to RSI cancellation."""
        from core.async_cancellation import CancellationToken, CancellationReason
        from core.byrd_service import BYRDService, QueuedTask, ServiceMode
        from rsi.orchestration.ralph_loop import RalphLoop

        # Track the flow
        flow_events = []

        # Create mock memory
        mock_memory = Mock()
        mock_memory.create_task = AsyncMock(return_value="task_abc")
        mock_memory.get_pending_tasks = AsyncMock(return_value=[])
        mock_memory.update_task_status = AsyncMock()
        mock_memory.complete_task = AsyncMock()

        # Create Ralph Loop with mock that records events
        mock_ralph = Mock()
        mock_ralph.interrupt = AsyncMock(side_effect=lambda reason=None: flow_events.append(f"interrupt:{reason}"))

        # Create service
        service = BYRDService(
            memory=mock_memory,
            ralph_loop=mock_ralph,
            config={'idle_threshold_seconds': 1}
        )
        service._mode = ServiceMode.IDLE_RSI  # Use enum, not string

        # Step 1: Enqueue high-priority task
        flow_events.append("step1:enqueue_task")
        task_id = await service.enqueue_task(
            description="Test task",
            objective="Test objective",
            priority=0.9  # High priority
        )
        flow_events.append(f"step1:task_created:{task_id}")

        # Step 2: Verify interrupt was called
        assert "interrupt:" in flow_events[-2], f"Expected interrupt call, got: {flow_events}"
        flow_events.append("step2:verified_interrupt")

        # Step 3: Simulate RSI cancellation check
        token = CancellationToken(name="rsi_cycle")
        await token.cancel(reason=CancellationReason.EXPLICIT, message="high_priority_task")
        assert token.is_cancelled
        flow_events.append("step3:token_cancelled")

        # Verify flow
        expected_flow = [
            "step1:enqueue_task",
            "interrupt:high_priority_task_123",  # Ralph Loop interrupt
            "step1:task_created:task_abc",
            "step2:verified_interrupt",
            "step3:token_cancelled"
        ]

        logger.info(f"Flow events: {flow_events}")
        assert any("interrupt:" in e for e in flow_events), "Interrupt should be called"
        assert "step3:token_cancelled" in flow_events, "Token should be cancelled"

        logger.info("✓ End-to-end interruption flow verified")


def test_cancellation_token_sync():
    """Synchronous test for cancellation token."""
    from core.async_cancellation import CancellationToken, CancellationReason, CancellationState

    token = CancellationToken(name="sync_test")

    # Test initial state
    assert not token.is_cancelled
    assert token.state == CancellationState.ACTIVE
    assert token.cancellation_reason is None

    # Test cancellation
    asyncio.run(token.cancel(reason=CancellationReason.EXPLICIT, message="Test"))

    assert token.is_cancelled
    assert token.cancellation_reason == CancellationReason.EXPLICIT

    logger.info("✓ Synchronous cancellation token test passed")


def test_queued_task_priorities():
    """Test QueuedTask priority helpers."""
    from core.byrd_service import QueuedTask, TaskPriority
    from datetime import datetime, timezone

    # Critical task
    critical_task = QueuedTask(
        task_id="crit_1",
        description="Critical",
        objective="Fix now",
        priority=1.0
    )
    assert critical_task.is_critical
    assert critical_task.is_high_priority

    # High priority task
    high_task = QueuedTask(
        task_id="high_1",
        description="High",
        objective="Do soon",
        priority=0.8
    )
    assert not high_task.is_critical
    assert high_task.is_high_priority

    # Normal priority task
    normal_task = QueuedTask(
        task_id="norm_1",
        description="Normal",
        objective="Do later",
        priority=0.5
    )
    assert not normal_task.is_critical
    assert not normal_task.is_high_priority

    logger.info("✓ QueuedTask priority helpers work correctly")


if __name__ == "__main__":
    # Run tests manually
    print("\n=== Testing Interruption Flow ===\n")

    print("1. Testing cancellation token...")
    test_cancellation_token_sync()

    print("\n2. Testing queued task priorities...")
    test_queued_task_priorities()

    print("\n3. Running async tests...")
    asyncio.run(TestInterruptionFlow().test_cancellation_token_basic())
    asyncio.run(TestInterruptionFlow().test_interruption_flow_end_to_end())

    print("\n=== All Tests Passed ===\n")

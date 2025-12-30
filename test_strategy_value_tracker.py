"""
Test suite for Strategy Value Tracking System

Demonstrates how the tracker prevents false-positive loops.
"""

import time
from datetime import datetime, timedelta
from strategy_value_tracker import (
    StrategyValueTracker,
    StrategyOutcome,
    OutcomeType,
    create_outcome,
    record_simple_outcome
)


def test_basic_tracking():
    """Test basic outcome recording and metric calculation."""
    print("\n=== Test 1: Basic Tracking ===")
    
    tracker = StrategyValueTracker()
    strategy_id = "test_strategy_1"
    
    # Record some outcomes
    record_simple_outcome(tracker, strategy_id, success=True, value=0.8)
    record_simple_outcome(tracker, strategy_id, success=True, value=0.9)
    record_simple_outcome(tracker, strategy_id, success=False, value=-0.5)
    
    # Get metrics
    metrics = tracker.get_metrics(strategy_id)
    
    print(f"  Total executions: {metrics.total_executions}")
    print(f"  Success rate: {metrics.success_rate:.2%}")
    print(f"  Current value score: {metrics.current_value_score:.3f}")
    print(f"  Health score: {metrics.health_score:.3f}")
    
    assert metrics.total_executions == 3
    assert metrics.success_count == 2
    assert metrics.failure_count == 1
    assert metrics.health_score > 0.5
    
    print("  ✓ Basic tracking works")


def test_false_positive_detection():
    """Test detection of false-positive loops."""
    print("\n=== Test 2: False Positive Detection ===")
    
    tracker = StrategyValueTracker(loop_threshold=3)
    strategy_id = "looping_strategy"
    
    # Record consecutive false positives
    for i in range(3):
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type="false_positive",
            value_score=-0.5,
            context={"attempt": i + 1}
        )
        tracker.record_outcome(outcome)
    
    # Check if it's safe to use
    is_safe, reason = tracker.is_safe_to_use(strategy_id)
    
    print(f"  Is safe to use: {is_safe}")
    print(f"  Reason: {reason}")
    
    assert not is_safe
    assert "Deprecated" in reason or "false positive" in reason.lower()
    
    # Check metrics
    metrics = tracker.get_metrics(strategy_id)
    print(f"  Consecutive false positives: {metrics.consecutive_false_positives}")
    print(f"  Is in loop: {metrics.is_in_loop}")
    
    assert metrics.consecutive_false_positives >= 3
    assert metrics.is_in_loop
    
    print("  ✓ False positive loop detected")


def test_temporal_decay():
    """Test that recent outcomes have more weight."""
    print("\n=== Test 3: Temporal Decay ===")
    
    tracker = StrategyValueTracker(value_decay_half_life=1.0)  # 1 second half-life
    strategy_id = "temporal_strategy"
    
    # Record old successes
    old_time = datetime.now() - timedelta(seconds=10)
    for i in range(5):
        outcome = StrategyOutcome(
            strategy_id=strategy_id,
            outcome_type=OutcomeType.SUCCESS,
            timestamp=old_time + timedelta(seconds=i),
            value_score=0.9
        )
        tracker.record_outcome(outcome)
    
    # Record recent failures
    for i in range(5):
        record_simple_outcome(tracker, strategy_id, success=False, value=-0.8)
    
    # Get metrics
    metrics = tracker.get_metrics(strategy_id)
    
    print(f"  Raw average value: {metrics.raw_average_value:.3f}")
    print(f"  Decayed value score: {metrics.current_value_score:.3f}")
    print(f"  Value trend: {metrics.value_trend:.3f}")
    
    # Recent failures should lower the decayed value
    assert metrics.current_value_score < metrics.raw_average_value
    assert metrics.value_trend < 0  # Declining
    
    print("  ✓ Temporal decay working correctly")


def test_context_awareness():
    """Test context-aware tracking."""
    print("\n=== Test 4: Context Awareness ===")
    
    tracker = StrategyValueTracker()
    strategy_id = "context_strategy"
    
    # Record successes in one context
    for i in range(3):
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type="success",
            value_score=0.8,
            context={"domain": "code", "language": "python"}
        )
        tracker.record_outcome(outcome)
    
    # Record failures in another context
    for i in range(3):
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type="failure",
            value_score=-0.6,
            context={"domain": "code", "language": "javascript"}
        )
        tracker.record_outcome(outcome)
    
    # Get metrics
    metrics = tracker.get_metrics(strategy_id)
    
    print(f"  Context success rate: {metrics.context_success_rate:.2%}")
    print(f"  Successful contexts: {len(metrics.successful_contexts)}")
    print(f"  Failed contexts: {len(metrics.failed_contexts)}")
    
    # Get context hints
    hints = tracker.suggest_context_hints(strategy_id)
    print(f"  Suggested context hints: {hints}")
    
    assert metrics.context_success_rate == 0.5
    assert len(metrics.successful_contexts) == 3
    assert len(metrics.failed_contexts) == 3
    
    print("  ✓ Context tracking working")


def test_health_score_calculation():
    """Test health score computation."""
    print("\n=== Test 5: Health Score Calculation ===")
    
    tracker = StrategyValueTracker()
    
    # Create multiple strategies with different performance
    strategies = {
        "excellent": [],
        "good": [],
        "poor": [],
        "terrible": []
    }
    
    # Excellent strategy
    for _ in range(10):
        strategies["excellent"].append(create_outcome(
            "excellent", "success", 0.9, context={"quality": "high"}
        ))
    
    # Good strategy with some failures
    for _ in range(7):
        strategies["good"].append(create_outcome(
            "good", "success", 0.7, context={"quality": "medium"}
        ))
    for _ in range(3):
        strategies["good"].append(create_outcome(
            "good", "failure", -0.4, context={"quality": "low"}
        ))
    
    # Poor strategy with false positives
    for _ in range(4):
        strategies["poor"].append(create_outcome(
            "poor", "success", 0.3, context={"quality": "low"}
        ))
    for _ in range(3):
        strategies["poor"].append(create_outcome(
            "poor", "false_positive", -0.6, context={"quality": "low"}
        ))
    for _ in range(3):
        strategies["poor"].append(create_outcome(
            "poor", "failure", -0.7, context={"quality": "low"}
        ))
    
    # Terrible strategy
    for _ in range(10):
        strategies["terrible"].append(create_outcome(
            "terrible", "failure", -0.8, context={"quality": "very_low"}
        ))
    
    # Record all outcomes
    for sid, outcomes in strategies.items():
        for outcome in outcomes:
            tracker.record_outcome(outcome)
    
    # Get health scores
    health_scores = {}
    for sid in strategies.keys():
        metrics = tracker.get_metrics(sid)
        health_scores[sid] = metrics.health_score
        print(f"  {sid.capitalize()} - Health: {metrics.health_score:.3f}, "
              f"Success rate: {metrics.success_rate:.2%}, "
              f"Adjusted: {metrics.adjusted_success_rate:.2%}")
    
    # Verify ordering
    assert health_scores["excellent"] > health_scores["good"]
    assert health_scores["good"] > health_scores[poor]
    assert health_scores["poor"] > health_scores["terrible"]
    
    # Get top performers
    top = tracker.get_strategies_by_health()
    print(f"\n  Top performers: {[sid for sid, _ in top]}")
    assert top[0][0] == "excellent"
    
    print("  ✓ Health scores calculated correctly")


def test_strategy_review():
    """Test getting strategies that need review."""
    print("\n=== Test 6: Strategy Review ===")
    
    tracker = StrategyValueTracker(loop_threshold=2, false_positive_threshold=0.25)
    
    # Create various strategies
    strategies = {
        "healthy": [],
        "fp_prone": [],
        "failing": [],
        "declining": []
    }
    
    # Healthy strategy
    for _ in range(5):
        strategies["healthy"].append(create_outcome(
            "healthy", "success", 0.8
        ))
    
    # False positive prone
    for _ in range(3):
        strategies["fp_prone"].append(create_outcome(
            "fp_prone", "success", 0.2
        ))
    for _ in range(3):
        strategies["fp_prone"].append(create_outcome(
            "fp_prone", "false_positive", -0.5
        ))
    
    # Failing strategy
    for _ in range(6):
        strategies["failing"].append(create_outcome(
            "failing", "failure", -0.7
        ))
    
    # Declining strategy (was good, now bad)
    for _ in range(5):
        strategies["declining"].append(create_outcome(
            "declining", "success", 0.8
        ))
    for _ in range(5):
        strategies["declining"].append(create_outcome(
            "declining", "failure", -0.6
        ))
    
    # Record all outcomes
    for sid, outcomes in strategies.items():
        for outcome in outcomes:
            tracker.record_outcome(outcome)
    
    # Get strategies to review
    to_review = tracker.get_strategies_to_review()
    
    print(f"  Strategies needing review: {len(to_review)}")
    for sid, metrics, issue in to_review:
        print(f"    - {sid}: {issue}")
    
    # Should have issues (not healthy)
    assert len(to_review) >= 2
    issue_ids = {sid for sid, _, _ in to_review}
    assert "failing" in issue_ids
    assert "healthy" not in issue_ids
    
    print("  ✓ Strategy review working")


def test_reset_functionality():
    """Test resetting a strategy's tracking."""
    print("\n=== Test 7: Reset Functionality ===")
    
    tracker = StrategyValueTracker(loop_threshold=3)
    strategy_id = "reset_strategy"
    
    # Create a failing strategy
    for _ in range(5):
        record_simple_outcome(tracker, strategy_id, success=False, value=-0.8)
    
    # Check it's flagged
    is_safe, _ = tracker.is_safe_to_use(strategy_id)
    print(f"  Safe before reset: {is_safe}")
    # It might be safe if not consecutive enough, but health should be low
    metrics = tracker.get_metrics(strategy_id)
    print(f"  Health before reset: {metrics.health_score:.3f}")
    assert metrics.health_score < 0.5
    
    # Reset the strategy
    tracker.reset_strategy(strategy_id)
    
    # Check it's clean now
    metrics_after = tracker.get_metrics(strategy_id)
    print(f"  Executions after reset: {metrics_after.total_executions}")
    print(f"  Health after reset: {metrics_after.health_score:.3f}")
    
    assert metrics_after.total_executions == 0
    assert metrics_after.health_score == 1.0
    
    # Should be safe to use now
    is_safe_after, _ = tracker.is_safe_to_use(strategy_id)
    print(f"  Safe after reset: {is_safe_after}")
    assert is_safe_after
    
    print("  ✓ Reset functionality working")


def test_summary_report():
    """Test generating a summary report."""
    print("\n=== Test 8: Summary Report ===")
    
    tracker = StrategyValueTracker()
    
    # Create multiple strategies
    for i in range(5):
        sid = f"strategy_{i}"
        for j in range(10):
            success = j < (6 + i)  # Varying success rates
            record_simple_outcome(
                tracker, sid, success=success,
                value=0.7 if success else -0.5
            )
    
    # Get summary
    summary = tracker.get_summary()
    
    print(f"  Total strategies tracked: {summary['total_strategies_tracked']}")
    print(f"  Total executions recorded: {summary['total_executions_recorded']}")
    print(f"  Average health score: {summary['average_health_score']:.3f}")
    print(f"  Strategies needing review: {summary['strategies_needing_review']}")
    print(f"  Top performers: {[sid for sid, _ in summary['top_performers']]}")
    
    assert summary['total_strategies_tracked'] == 5
    assert summary['total_executions_recorded'] == 50
    assert len(summary['top_performers']) == 5
    
    print("  ✓ Summary report working")


def test_outcome_types():
    """Test all outcome types are tracked correctly."""
    print("\n=== Test 9: All Outcome Types ===")
    
    tracker = StrategyValueTracker()
    strategy_id = "all_types"
    
    # Record all outcome types
    outcome_types = [
        "success",
        "partial",
        "failure",
        "false_positive",
        "loop_detected",
        "context_mismatch",
        "timeout",
        "error"
    ]
    
    for ot in outcome_types:
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type=ot,
            value_score=0.5 if ot in ["success", "partial"] else -0.5,
            notes=f"Testing {ot}"
        )
        tracker.record_outcome(outcome)
    
    # Get metrics
    metrics = tracker.get_metrics(strategy_id)
    
    print(f"  Total executions: {metrics.total_executions}")
    print(f"  Successes: {metrics.success_count}")
    print(f"  Partials: {metrics.partial_count}")
    print(f"  Failures: {metrics.failure_count}")
    print(f"  False positives: {metrics.false_positive_count}")
    print(f"  Loops detected: {metrics.loop_detected_count}")
    
    assert metrics.total_executions == len(outcome_types)
    assert metrics.success_count == 1
    assert metrics.partial_count == 1
    assert metrics.failure_count == 1
    assert metrics.false_positive_count == 1
    assert metrics.loop_detected_count == 1
    
    print("  ✓ All outcome types tracked correctly")


def test_realistic_false_positive_scenario():
    """Test a realistic false-positive loop scenario."""
    print("\n=== Test 10: Realistic False-Positive Loop Scenario ===")
    
    tracker = StrategyValueTracker(loop_threshold=3, false_positive_threshold=0.25)
    strategy_id = "buggy_search"
    
    # Scenario: A search strategy that appears to work but returns wrong results
    print("  Simulating search strategy that returns wrong results...")
    
    # First few executions - seems to work (but user hasn't validated)
    for i in range(3):
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type="success",
            value_score=0.5,  # Appears successful
            context={"query": f"test_{i}", "validated": False}
        )
        tracker.record_outcome(outcome)
        print(f"    Execution {i+1}: success (validated=False)")
    
    metrics = tracker.get_metrics(strategy_id)
    print(f"  Current health: {metrics.health_score:.3f}")
    
    # User validates - they're actually wrong! (false positives)
    for i in range(3):
        outcome = create_outcome(
            strategy_id=strategy_id,
            outcome_type="false_positive",
            value_score=-0.8,
            context={"query": f"test_{i}", "validated": True},
            notes="Result was incorrect"
        )
        tracker.record_outcome(outcome)
        print(f"    Execution {i+4}: FALSE_POSITIVE (validated=True)")
    
    # Check if loop detected
    is_safe, reason = tracker.is_safe_to_use(strategy_id)
    metrics = tracker.get_metrics(strategy_id)
    
    print(f"  Is safe to use: {is_safe}")
    print(f"  Reason: {reason}")
    print(f"  Consecutive false positives: {metrics.consecutive_false_positives}")
    print(f"  Health score: {metrics.health_score:.3f}")
    print(f"  Adjusted success rate: {metrics.adjusted_success_rate:.2%}")
    
    assert not is_safe
    assert metrics.consecutive_false_positives >= 3
    assert metrics.health_score < 0.5
    
    print("  ✓ False-positive loop correctly detected and prevented")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("STRATEGY VALUE TRACKER - TEST SUITE")
    print("=" * 60)
    
    test_basic_tracking()
    test_false_positive_detection()
    test_temporal_decay()
    test_context_awareness()
    test_health_score_calculation()
    test_strategy_review()
    test_reset_functionality()
    test_summary_report()
    test_outcome_types()
    test_realistic_false_positive_scenario()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()

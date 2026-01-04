#!/usr/bin/env python3
"""
Loop Instrumentation System
==========================

Breaks the zero-delta loop by providing comprehensive instrumentation
of all compounding loops. Detects stagnation, tracks meaningful progress,
and enables intervention when loops are stuck.

PROBLEM: Zero-Delta Loop
------------------------
Loops can become stuck executing without meaningful improvement:
- Cycles run but delta < MIN_MEANINGFUL_DELTA (0.5%)
- False positives accumulate
- No actual capability growth occurs
- System wastes cycles on ineffective patterns

SOLUTION: Loop Instrumentation
-----------------------------
1. Real-time metrics collection per loop
2. Stagnation detection (no progress for N cycles)
3. Delta trend analysis (is it improving, declining, flat?)
4. Intervention triggers (when to change strategy)
5. Root cause analysis (why is this loop stuck?)

USAGE:
------
    from loop_instrumentation import LoopInstrumenter
    
    instrumenter = LoopInstrumenter()
    instrumenter.register_loop("memory_reasoner")
    instrumenter.record_cycle("memory_reasoner", delta=0.02, success=True)
    
    if instrumenter.is_stagnant("memory_reasoner"):
        analysis = instrumenter.analyze_stagnation("memory_reasoner")
        instrumenter.trigger_intervention("memory_reasoner", analysis)
"""

import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple
import statistics

logger = logging.getLogger(__name__)


class LoopState(Enum):
    """States a loop can be in."""
    ACTIVE = "active"
    STAGNANT = "stagnant"
    IMPROVING = "improving"
    DECLINING = "declining"
    RECOVERING = "recovering"
    CRITICAL = "critical"


class InterventionType(Enum):
    """Types of interventions to break stagnation."""
    STRATEGY_CHANGE = "strategy_change"
    PARAMETER_RESET = "parameter_reset"
    COOLDOWN = "cooldown"
    MEMORY_PURGE = "memory_purge"
    GOAL_ROTATION = "goal_rotation"
    EMERGENCY_RESTART = "emergency_restart"


@dataclass
class CycleMetrics:
    """Metrics from a single cycle execution."""
    cycle_number: int
    timestamp: datetime
    delta: float  # Improvement delta (can be negative)
    success: bool
    meaningful: bool  # Was delta >= MIN_MEANINGFUL_DELTA?
    duration_seconds: float
    target: Optional[str] = None
    strategy: Optional[str] = None
    hypotheses_tried: int = 0
    error: Optional[str] = None


@dataclass
class LoopProfile:
    """Complete profile of a loop's performance over time."""
    loop_name: str
    registered_at: datetime
    total_cycles: int = 0
    successful_cycles: int = 0
    meaningful_cycles: int = 0  # Cycles with delta >= threshold
    current_state: LoopState = LoopState.ACTIVE
    state_since: datetime = field(default_factory=datetime.now)
    
    # Recent history for analysis (last 50 cycles)
    recent_cycles: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Stagnation tracking
    stagnant_since: Optional[datetime] = None
    stagnant_cycle_count: int = 0
    last_meaningful_cycle: Optional[int] = None
    
    # Statistics
    avg_delta: float = 0.0
    delta_trend: str = "unknown"  # "improving", "declining", "stable"
    best_delta: float = -float('inf')
    worst_delta: float = float('inf')
    
    # Intervention history
    interventions: List[Dict] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Success rate as percentage."""
        if self.total_cycles == 0:
            return 0.0
        return (self.successful_cycles / self.total_cycles) * 100
    
    @property
    def meaningful_rate(self) -> float:
        """Rate of meaningful improvements as percentage."""
        if self.total_cycles == 0:
            return 0.0
        return (self.meaningful_cycles / self.total_cycles) * 100


class LoopInstrumenter:
    """
    Instruments and monitors all compounding loops.
    
    Detects zero-delta loops and provides intervention mechanisms.
    """
    
    # Configuration
    MIN_MEANINGFUL_DELTA = 0.005  # 0.5% minimum improvement
    STAGNATION_THRESHOLD = 5  # Cycles without meaningful delta = stagnant
    CRITICAL_THRESHOLD = 15  # Cycles without meaningful delta = critical
    THRASH_LIMIT = 21  # Hard limit - FORCE intervention beyond this (breaks 21-cycle thrash loop)
    TREND_WINDOW = 10  # Cycles to analyze for trend
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.loops: Dict[str, LoopProfile] = {}
        self.global_start_time = datetime.now()
        self._alerts: List[Dict] = []
        
        # Override defaults from config
        self.MIN_MEANINGFUL_DELTA = self.config.get(
            "min_meaningful_delta", self.MIN_MEANINGFUL_DELTA
        )
        self.STAGNATION_THRESHOLD = self.config.get(
            "stagnation_threshold", self.STAGNATION_THRESHOLD
        )
        self.CRITICAL_THRESHOLD = self.config.get(
            "critical_threshold", self.CRITICAL_THRESHOLD
        )
    
    def register_loop(self, loop_name: str) -> LoopProfile:
        """Register a loop for instrumentation."""
        if loop_name in self.loops:
            logger.warning(f"Loop {loop_name} already registered")
            return self.loops[loop_name]
        
        profile = LoopProfile(
            loop_name=loop_name,
            registered_at=datetime.now()
        )
        self.loops[loop_name] = profile
        logger.info(f"[INSTRUMENT] Registered loop: {loop_name}")
        return profile
    
    def record_cycle(
        self,
        loop_name: str,
        delta: float,
        success: bool,
        duration_seconds: float,
        target: Optional[str] = None,
        strategy: Optional[str] = None,
        hypotheses_tried: int = 0,
        error: Optional[str] = None
    ) -> CycleMetrics:
        """
        Record metrics from a cycle execution.
        
        Args:
            loop_name: Name of the loop
            delta: Improvement delta (can be negative)
            success: Whether cycle completed successfully
            duration_seconds: How long the cycle took
            target: What was being improved
            strategy: Strategy used
            hypotheses_tried: Number of hypotheses tested
            error: Error message if failed
        """
        if loop_name not in self.loops:
            self.register_loop(loop_name)
        
        profile = self.loops[loop_name]
        profile.total_cycles += 1
        
        # Determine if improvement was meaningful
        is_meaningful = delta >= self.MIN_MEANINGFUL_DELTA
        
        if success:
            profile.successful_cycles += 1
        
        if is_meaningful:
            profile.meaningful_cycles += 1
            profile.last_meaningful_cycle = profile.total_cycles
            # Reset stagnation tracking
            profile.stagnant_since = None
            profile.stagnant_cycle_count = 0
        else:
            # Track stagnation
            if profile.stagnant_since is None:
                profile.stagnant_since = datetime.now()
            profile.stagnant_cycle_count += 1
        
        # Create metrics record
        metrics = CycleMetrics(
            cycle_number=profile.total_cycles,
            timestamp=datetime.now(),
            delta=delta,
            success=success,
            meaningful=is_meaningful,
            duration_seconds=duration_seconds,
            target=target,
            strategy=strategy,
            hypotheses_tried=hypotheses_tried,
            error=error
        )
        profile.recent_cycles.append(metrics)
        
        # Update statistics
        self._update_statistics(profile)
        self._update_state(profile)
        
        # Check for alerts
        self._check_alerts(profile)
        
        return metrics
    
    def _update_statistics(self, profile: LoopProfile):
        """Update running statistics for a loop."""
        if not profile.recent_cycles:
            return
        
        deltas = [c.delta for c in profile.recent_cycles]
        profile.avg_delta = statistics.mean(deltas)
        profile.best_delta = max(deltas)
        profile.worst_delta = min(deltas)
        
        # Analyze trend
        if len(deltas) >= self.TREND_WINDOW:
            recent = deltas[-self.TREND_WINDOW:]
            earlier = deltas[-self.TREND_WINDOW*2:-self.TREND_WINDOW] if len(deltas) >= self.TREND_WINDOW*2 else deltas[:-self.TREND_WINDOW]
            
            if earlier:
                recent_avg = statistics.mean(recent)
                earlier_avg = statistics.mean(earlier)
                
                if recent_avg > earlier_avg * 1.01:  # 1% improvement
                    profile.delta_trend = "improving"
                elif recent_avg < earlier_avg * 0.99:  # 1% decline
                    profile.delta_trend = "declining"
                else:
                    profile.delta_trend = "stable"
    
    def _update_state(self, profile: LoopProfile):
        """Update the current state of a loop."""
        old_state = profile.current_state
        
        # BREAK 21-CYCLE THRASH LOOP: FORCE intervention at THRASH_LIMIT
        if profile.stagnant_cycle_count >= self.THRASH_LIMIT:
            profile.current_state = LoopState.CRITICAL
            # Auto-trigger emergency intervention when hitting thrash limit
            if profile.stagnant_cycle_count == self.THRASH_LIMIT:
                logger.critical(
                    f"[THRASH_DETECTED] {profile.loop_name} hit {self.THRASH_LIMIT}-cycle thrash limit! "
                    f"Forcing emergency intervention to break deadlock."
                )
                # Trigger immediate intervention
                analysis = self.analyze_stagnation(profile.loop_name)
                intervention = self.trigger_intervention(profile.loop_name, analysis)
                # Mark intervention as FORCED due to thrash
                intervention["forced"] = True
                intervention["reason"] = "21-cycle thrash limit exceeded"
                logger.critical(
                    f"[FORCE_INTERVENTION] {profile.loop_name}: {intervention['type']} "
                    f"FORCED to break {self.THRASH_LIMIT}-cycle thrash loop"
                )
        elif profile.stagnant_cycle_count >= self.CRITICAL_THRESHOLD:
            profile.current_state = LoopState.CRITICAL
        elif profile.stagnant_cycle_count >= self.STAGNATION_THRESHOLD:
            profile.current_state = LoopState.STAGNANT
        elif profile.delta_trend == "improving" and profile.stagnant_cycle_count == 0:
            profile.current_state = LoopState.IMPROVING
        elif profile.delta_trend == "declining":
            profile.current_state = LoopState.DECLINING
        elif profile.stagnant_cycle_count > 0 and profile.stagnant_cycle_count < self.STAGNATION_THRESHOLD:
            profile.current_state = LoopState.RECOVERING
        else:
            profile.current_state = LoopState.ACTIVE
        
        # Reset state timer if state changed
        if old_state != profile.current_state:
            profile.state_since = datetime.now()
            logger.info(
                f"[INSTRUMENT] {profile.loop_name} state: {old_state.value} -> {profile.current_state.value}"
            )
    
    def _check_alerts(self, profile: LoopProfile):
        """Check if any alerts should be generated."""
        alert = None
        
        if profile.current_state == LoopState.CRITICAL:
            alert = {
                "level": "CRITICAL",
                "loop": profile.loop_name,
                "message": f"Loop has been stagnant for {profile.stagnant_cycle_count} cycles",
                "stagnant_cycles": profile.stagnant_cycle_count,
                "timestamp": datetime.now().isoformat()
            }
        elif profile.current_state == LoopState.STAGNANT:
            alert = {
                "level": "WARNING",
                "loop": profile.loop_name,
                "message": f"Loop showing signs of stagnation ({profile.stagnant_cycle_count} cycles without meaningful improvement)",
                "stagnant_cycles": profile.stagnant_cycle_count,
                "timestamp": datetime.now().isoformat()
            }
        elif profile.delta_trend == "declining" and profile.stagnant_cycle_count > 3:
            alert = {
                "level": "INFO",
                "loop": profile.loop_name,
                "message": f"Loop performance declining (avg delta: {profile.avg_delta:.4%})",
                "trend": profile.delta_trend,
                "avg_delta": profile.avg_delta,
                "timestamp": datetime.now().isoformat()
            }
        
        if alert:
            self._alerts.append(alert)
            logger.warning(f"[ALERT] {alert['level']}: {alert['message']}")
    
    def is_stagnant(self, loop_name: str) -> bool:
        """Check if a loop is currently stagnant."""
        if loop_name not in self.loops:
            return False
        return self.loops[loop_name].current_state in [LoopState.STAGNANT, LoopState.CRITICAL]
    
    def get_stagnant_loops(self) -> List[str]:
        """Get list of all stagnant loops."""
        return [
            name for name, profile in self.loops.items()
            if profile.current_state in [LoopState.STAGNANT, LoopState.CRITICAL]
        ]
    
    def analyze_stagnation(self, loop_name: str) -> Dict:
        """
        Analyze why a loop is stagnant and provide recommendations.
        
        Returns:
            Dictionary with analysis and recommendations
        """
        if loop_name not in self.loops:
            return {"error": "Loop not registered"}
        
        profile = self.loops[loop_name]
        
        # Analyze recent patterns
        recent = list(profile.recent_cycles)[-20:]  # Last 20 cycles
        
        analysis = {
            "loop_name": loop_name,
            "stagnant_cycles": profile.stagnant_cycle_count,
            "stagnant_since": profile.stagnant_since.isoformat() if profile.stagnant_since else None,
            "current_state": profile.current_state.value,
            "avg_delta": profile.avg_delta,
            "success_rate": profile.success_rate,
            "meaningful_rate": profile.meaningful_rate,
            "delta_trend": profile.delta_trend,
            "last_meaningful_cycle": profile.last_meaningful_cycle,
            "patterns": [],
            "recommendations": []
        }
        
        # Pattern detection
        if recent:
            # Pattern: Consistently small deltas
            small_deltas = [c for c in recent if abs(c.delta) < self.MIN_MEANINGFUL_DELTA]
            if len(small_deltas) / len(recent) > 0.8:
                analysis["patterns"].append("consistently_small_deltas")
                analysis["recommendations"].append("Consider increasing search space or exploration rate")
            
            # Pattern: High failure rate
            failures = [c for c in recent if not c.success]
            if len(failures) / len(recent) > 0.5:
                analysis["patterns"].append("high_failure_rate")
                analysis["recommendations"].append("Check for resource constraints or implementation bugs")
            
            # Pattern: Strategy repetition without success
            strategies = [c.strategy for c in recent if c.strategy]
            if strategies and len(set(strategies)) < 3:
                analysis["patterns"].append("strategy_repetition")
                analysis["recommendations"].append("Rotate to different strategies or generate new hypotheses")
            
            # Pattern: Declining performance
            if profile.delta_trend == "declining":
                analysis["patterns"].append("declining_performance")
                analysis["recommendations"].append("Consider memory purge or parameter reset")
        
        # State-specific recommendations
        if profile.current_state == LoopState.CRITICAL:
            analysis["recommendations"].append("CRITICAL: Emergency restart or goal rotation needed")
        elif profile.current_state == LoopState.STAGNANT:
            analysis["recommendations"].append("Consider strategy change or cooldown period")
        
        return analysis
    
    def trigger_intervention(self, loop_name: str, analysis: Dict) -> Dict:
        """
        Trigger an intervention to break stagnation.
        
        Args:
            loop_name: Name of the stagnant loop
            analysis: Analysis from analyze_stagnation()
            
        Returns:
            Intervention record
        """
        if loop_name not in self.loops:
            return {"error": "Loop not registered"}
        
        profile = self.loops[loop_name]
        
        # Select intervention type based on analysis
        intervention_type = None
        
        if profile.current_state == LoopState.CRITICAL:
            intervention_type = InterventionType.EMERGENCY_RESTART
        elif "declining_performance" in analysis.get("patterns", []):
            intervention_type = InterventionType.MEMORY_PURGE
        elif "strategy_repetition" in analysis.get("patterns", []):
            intervention_type = InterventionType.STRATEGY_CHANGE
        elif profile.stagnant_cycle_count >= self.STAGNATION_THRESHOLD * 2:
            intervention_type = InterventionType.GOAL_ROTATION
        else:
            intervention_type = InterventionType.PARAMETER_RESET
        
        intervention = {
            "loop_name": loop_name,
            "type": intervention_type.value,
            "timestamp": datetime.now().isoformat(),
            "triggered_by": analysis,
            "stagnant_cycles_at_trigger": profile.stagnant_cycle_count
        }
        
        profile.interventions.append(intervention)
        
        logger.warning(
            f"[INTERVENTION] {loop_name}: {intervention_type.value} "
            f"(stagnant for {profile.stagnant_cycle_count} cycles)"
        )
        
        return intervention
    
    def get_dashboard(self) -> Dict:
        """
        Get a comprehensive dashboard of all loop states.
        
        Returns:
            Dictionary with overall status and per-loop details
        """
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "total_loops": len(self.loops),
            "active_loops": 0,
            "stagnant_loops": 0,
            "critical_loops": 0,
            "improving_loops": 0,
            "total_cycles": sum(p.total_cycles for p in self.loops.values()),
            "total_meaningful_cycles": sum(p.meaningful_cycles for p in self.loops.values()),
            "global_meaningful_rate": 0.0,
            "loops": {},
            "recent_alerts": self._alerts[-10:]  # Last 10 alerts
        }
        
        if dashboard["total_cycles"] > 0:
            dashboard["global_meaningful_rate"] = (
                dashboard["total_meaningful_cycles"] / dashboard["total_cycles"]
            ) * 100
        
        for name, profile in self.loops.items():
            state_counts = {
                LoopState.ACTIVE: "active_loops",
                LoopState.IMPROVING: "improving_loops",
                LoopState.STAGNANT: "stagnant_loops",
                LoopState.CRITICAL: "critical_loops"
            }
            
            for state, count_key in state_counts.items():
                if profile.current_state == state:
                    dashboard[count_key] += 1
            
            dashboard["loops"][name] = {
                "state": profile.current_state.value,
                "state_since": profile.state_since.isoformat(),
                "total_cycles": profile.total_cycles,
                "meaningful_cycles": profile.meaningful_cycles,
                "success_rate": profile.success_rate,
                "meaningful_rate": profile.meaningful_rate,
                "avg_delta": profile.avg_delta,
                "delta_trend": profile.delta_trend,
                "stagnant_cycles": profile.stagnant_cycle_count,
                "last_meaningful_cycle": profile.last_meaningful_cycle,
                "interventions": len(profile.interventions)
            }
        
        return dashboard
    
    def print_dashboard(self):
        """Print a formatted dashboard to console."""
        dashboard = self.get_dashboard()
        
        print("\n" + "=" * 70)
        print("LOOP INSTRUMENTATION DASHBOARD")
        print("=" * 70)
        
        print(f"\nGlobal Status:")
        print(f"  Total Loops:      {dashboard['total_loops']}")
        print(f"  Active:           {dashboard['active_loops']}")
        print(f"  Improving:        {dashboard['improving_loops']}")
        print(f"  Stagnant:         {dashboard['stagnant_loops']}")
        print(f"  Critical:         {dashboard['critical_loops']}")
        print(f"  Total Cycles:     {dashboard['total_cycles']}")
        print(f"  Meaningful Rate:  {dashboard['global_meaningful_rate']:.1f}%")
        
        print(f"\nPer-Loop Status:")
        for name, info in dashboard["loops"].items():
            status_symbol = {
                "active": "🟢",
                "improving": "🚀",
                "stagnant": "⚠️ ",
                "critical": "🔴",
                "declining": "📉",
                "recovering": "🔄"
            }.get(info["state"], "❓")
            
            print(f"\n  {status_symbol} {name}")
            print(f"     State:       {info['state'].upper()}")
            print(f"     Cycles:      {info['total_cycles']} ({info['meaningful_cycles']} meaningful)")
            print(f"     Success:     {info['success_rate']:.1f}%")
            print(f"     Meaningful:  {info['meaningful_rate']:.1f}%")
            print(f"     Avg Delta:   {info['avg_delta']:+.2%}")
            print(f"     Trend:       {info['delta_trend']}")
            if info['stagnant_cycles'] > 0:
                print(f"     Stagnant:    {info['stagnant_cycles']} cycles")
        
        if dashboard["recent_alerts"]:
            print(f"\nRecent Alerts:")
            for alert in dashboard["recent_alerts"][-5:]:
                print(f"  [{alert['level']}] {alert['loop']}: {alert['message']}")
        
        print("\n" + "=" * 70 + "\n")


# Singleton instance for global access
_instrumenter: Optional[LoopInstrumenter] = None


def get_instrumenter() -> LoopInstrumenter:
    """Get or create the global instrumenter instance."""
    global _instrumenter
    if _instrumenter is None:
        _instrumenter = LoopInstrumenter()
    return _instrumenter


def reset_instrumenter():
    """Reset the global instrumenter (mainly for testing)."""
    global _instrumenter
    _instrumenter = None


# Convenience functions for quick instrumentation
def instrument_cycle(
    loop_name: str,
    delta: float,
    success: bool,
    duration_seconds: float,
    **kwargs
) -> CycleMetrics:
    """Quick function to record a cycle without managing the instrumenter."""
    return get_instrumenter().record_cycle(
        loop_name=loop_name,
        delta=delta,
        success=success,
        duration_seconds=duration_seconds,
        **kwargs
    )


def check_stagnation(loop_name: str) -> Tuple[bool, Optional[Dict]]:
    """
    Quick check if a loop is stagnant.
    
    Returns:
        Tuple of (is_stagnant, analysis_if_stagnant)
    """
    instrumenter = get_instrumenter()
    is_stag = instrumenter.is_stagnant(loop_name)
    analysis = instrumenter.analyze_stagnation(loop_name) if is_stag else None
    return is_stag, analysis


if __name__ == "__main__":
    # Demo the instrumentation system
    import random
    
    logging.basicConfig(level=logging.INFO)
    
    instrumenter = LoopInstrumenter()
    
    # Register loops
    for loop in ["memory_reasoner", "self_compiler", "goal_evolver", "dreaming_machine", "omega"]:
        instrumenter.register_loop(loop)
    
    # Simulate cycles with various patterns
    print("\nSimulating loop execution...\n")
    
    # Loop 1: Generally improving
    for i in range(10):
        delta = random.uniform(0.001, 0.03) * (1 + i * 0.1)
        instrumenter.record_cycle("memory_reasoner", delta, True, 1.0)
    
    # Loop 2: Stagnating after some progress
    for i in range(15):
        if i < 5:
            delta = random.uniform(0.01, 0.02)
        else:
            delta = random.uniform(-0.001, 0.003)  # Small or negative
        instrumenter.record_cycle("self_compiler", delta, True, 1.5)
    
    # Loop 3: Critical - long stagnation
    for i in range(20):
        delta = random.uniform(-0.002, 0.004)
        instrumenter.record_cycle("goal_evolver", delta, True, 2.0)
    
    # Show dashboard
    instrumenter.print_dashboard()
    
    # Show stagnation analysis
    for loop in instrumenter.get_stagnant_loops():
        print(f"\nStagnation Analysis for {loop}:")
        analysis = instrumenter.analyze_stagnation(loop)
        for key, value in analysis.items():
            if key != "patterns" and key != "recommendations":
                print(f"  {key}: {value}")
        print(f"  Patterns: {analysis['patterns']}")
        print(f"  Recommendations: {analysis['recommendations']}")

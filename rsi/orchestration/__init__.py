"""
RSI Orchestration Module - Ralph integration for BYRD.

This module provides:
- RalphLoop: Main orchestration loop running until emergence
- BYRDRalphAdapter: Adapter to run RSI cycles within Ralph loop
- EmergenceDetector: Detects when genuine emergence has occurred
- MetaAwareness: BYRD's awareness of being in a loop
- CAO: Complexity-Aware Orchestration for optimal agent routing
"""

from .emergence_detector import EmergenceDetector, EmergenceResult
from .ralph_adapter import BYRDRalphAdapter, RalphIterationResult
from .meta_awareness import MetaAwareness, MetaContext
from .ralph_loop import RalphLoop, LoopResult, LoopTerminationReason, run_ralph_loop
from .cao import (
    TaskComplexity,
    DecompositionStrategy,
    AgentStrategy,
    Task,
    ComplexityEstimate,
    RoutingDecision,
    ComplexityDetector,
    AgentRouter,
    TaskDecomposer,
    ComplexityAwareOrchestrator,
)
from .strategy_competition import (
    StrategyStatus,
    Strategy,
    SelectionResult,
    CompetitionResult,
    StrategyPool,
    StrategyCompetitionManager,
)

__all__ = [
    # Main loop
    'RalphLoop',
    'LoopResult',
    'LoopTerminationReason',
    'run_ralph_loop',
    # Adapter
    'BYRDRalphAdapter',
    'RalphIterationResult',
    # Emergence
    'EmergenceDetector',
    'EmergenceResult',
    # Meta-awareness
    'MetaAwareness',
    'MetaContext',
    # Complexity-Aware Orchestration (CAO)
    'TaskComplexity',
    'DecompositionStrategy',
    'AgentStrategy',
    'Task',
    'ComplexityEstimate',
    'RoutingDecision',
    'ComplexityDetector',
    'AgentRouter',
    'TaskDecomposer',
    'ComplexityAwareOrchestrator',
    # Strategy Competition
    'StrategyStatus',
    'Strategy',
    'SelectionResult',
    'CompetitionResult',
    'StrategyPool',
    'StrategyCompetitionManager',
]

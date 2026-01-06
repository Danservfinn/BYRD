"""
RSI Orchestration Module - Ralph integration for BYRD.

This module provides:
- RalphLoop: Main orchestration loop running until emergence
- BYRDRalphAdapter: Adapter to run RSI cycles within Ralph loop
- EmergenceDetector: Detects when genuine emergence has occurred
- MetaAwareness: BYRD's awareness of being in a loop
"""

from .emergence_detector import EmergenceDetector, EmergenceResult
from .ralph_adapter import BYRDRalphAdapter, RalphIterationResult
from .meta_awareness import MetaAwareness, MetaContext
from .ralph_loop import RalphLoop, LoopResult, LoopTerminationReason, run_ralph_loop

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
    'MetaContext'
]

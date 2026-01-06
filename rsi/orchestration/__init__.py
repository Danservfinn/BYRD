"""
RSI Orchestration Module - Ralph integration for BYRD.

This module provides:
- BYRDRalphAdapter: Adapter to run RSI cycles within Ralph loop
- EmergenceDetector: Detects when genuine emergence has occurred
- MetaAwareness: BYRD's awareness of being in a loop
"""

from .emergence_detector import EmergenceDetector, EmergenceResult
from .ralph_adapter import BYRDRalphAdapter, RalphIterationResult
from .meta_awareness import MetaAwareness, MetaContext

__all__ = [
    'EmergenceDetector',
    'EmergenceResult',
    'BYRDRalphAdapter',
    'RalphIterationResult',
    'MetaAwareness',
    'MetaContext'
]

"""
RSI Consciousness Module - Memvid-backed consciousness stream for BYRD.

This module provides:
- ConsciousnessStream: Append-only frame storage with time-travel queries
- ConsciousnessFrame: Immutable snapshot of RSI cycle state
- Temporal queries for emergence detection
"""

from .frame import ConsciousnessFrame
from .stream import ConsciousnessStream

__all__ = ['ConsciousnessFrame', 'ConsciousnessStream']

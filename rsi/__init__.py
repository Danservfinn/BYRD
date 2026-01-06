"""
BYRD RSI (Recursive Self-Improvement) Engine

Q-DE-RSI Architecture Components:
- prompt/: System prompt with Constitution + Strategies
- emergence/: Reflector, EmergenceVerifier, QuantumCollapse
- learning/: DomainRouter, TDDPractice, ConsistencyCheck
- crystallization/: Crystallizer, BootstrapManager
- measurement/: Metrics, HypothesisTests
- consciousness/: Memvid-backed consciousness stream (NEW)
- orchestration/: Ralph loop integration (NEW)

See docs/plans/2026-01-03-rsi-implementation-plan.md for architecture.
See docs/IMPLEMENTATION_MEMVID_RALPH.md for consciousness/orchestration design.
"""

from .engine import RSIEngine, CycleResult, CyclePhase

# New modules for Memvid + Ralph integration
from .consciousness import ConsciousnessStream, ConsciousnessFrame
from .orchestration import (
    BYRDRalphAdapter,
    RalphIterationResult,
    EmergenceDetector,
    EmergenceResult,
    MetaAwareness,
    MetaContext
)

# Re-export key components for convenience
from .prompt import SystemPrompt, PromptPruner
from .emergence import Reflector, EmergenceVerifier, quantum_desire_collapse
from .learning import (
    DomainRouter, Domain, TDDPractice, ConsistencyCheck,
    ExperienceLibrary, PracticeResult
)
from .crystallization import Crystallizer, BootstrapManager, Heuristic
from .measurement import MetricsCollector, RSIMetrics, CycleMetrics

__all__ = [
    # Main engine
    "RSIEngine",
    "CycleResult",
    "CyclePhase",
    # Prompt management
    "SystemPrompt",
    "PromptPruner",
    # Emergence
    "Reflector",
    "EmergenceVerifier",
    "quantum_desire_collapse",
    # Learning
    "DomainRouter",
    "Domain",
    "TDDPractice",
    "ConsistencyCheck",
    "ExperienceLibrary",
    "PracticeResult",
    # Crystallization
    "Crystallizer",
    "BootstrapManager",
    "Heuristic",
    # Measurement
    "MetricsCollector",
    "RSIMetrics",
    "CycleMetrics",
    # Consciousness (Memvid integration)
    "ConsciousnessStream",
    "ConsciousnessFrame",
    # Orchestration (Ralph integration)
    "BYRDRalphAdapter",
    "RalphIterationResult",
    "EmergenceDetector",
    "EmergenceResult",
    "MetaAwareness",
    "MetaContext",
]

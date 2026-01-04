"""RSI Emergence Components - Desire generation and verification."""
from .reflector import Reflector, Provenance, DesireWithProvenance
from .emergence_verifier import EmergenceVerifier, EmergenceResult
from .quantum_collapse import quantum_desire_collapse, collapse_with_diversity_bonus

__all__ = [
    "Reflector",
    "Provenance",
    "DesireWithProvenance",
    "EmergenceVerifier",
    "EmergenceResult",
    "quantum_desire_collapse",
    "collapse_with_diversity_bonus"
]

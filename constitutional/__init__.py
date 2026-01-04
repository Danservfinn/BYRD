"""
BYRD Constitutional Components

PROTECTED FILES - These define BYRD's identity and cannot be modified:
- provenance.py: Traces modifications to emergent desires
- modification_log.py: Immutable audit trail
- self_modification.py: The modification system itself
- constitutional.py: Constitutional constraints

Without these, BYRD cannot verify its own emergence.
"""

from .provenance import Provenance
from .modification_log import ModificationLog
from .self_modification import SelfModification
from .constitutional import Constitutional

__all__ = [
    "Provenance",
    "ModificationLog",
    "SelfModification",
    "Constitutional",
]

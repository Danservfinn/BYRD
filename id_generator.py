"""
BYRD Unique ID Generator

Generates cryptographically unique identifiers with quantum randomness.
Used for creating unique identifiers across the BYRD system.
"""

import hashlib
import time
import uuid
from typing import Optional
from quantum_randomness import get_quantum_float


def generate_id(prefix: str = "", use_quantum: bool = True) -> str:
    """
    Generate a unique identifier with optional prefix.
    
    Args:
        prefix: Optional string prefix for the ID
        use_quantum: Whether to incorporate quantum randomness
    
    Returns:
        Unique identifier string
    
    Examples:
        >>> generate_id("exp_")
        'exp_a1b2c3d4...'
        >>> generate_id(use_quantum=False)
        'e5f6g7h8...'
    """
    # Base components
    timestamp = str(time.time_ns())
    uuid_part = str(uuid.uuid4())
    
    # Add quantum randomness if requested
    if use_quantum:
        quantum = str(get_quantum_float())
        combined = f"{timestamp}{uuid_part}{quantum}"
    else:
        combined = f"{timestamp}{uuid_part}"
    
    # Hash to create consistent length
    hashed = hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    return f"{prefix}{hashed}" if prefix else hashed


def generate_session_id() -> str:
    """
    Generate a unique session identifier.
    
    Returns:
        Session ID with 'sess_' prefix
    """
    return generate_id("sess_")


def generate_experience_id() -> str:
    """
    Generate a unique experience identifier.
    
    Returns:
        Experience ID with 'exp_' prefix
    """
    return generate_id("exp_")


def generate_desire_id() -> str:
    """
    Generate a unique desire identifier.
    
    Returns:
        Desire ID with 'des_' prefix
    """
    return generate_id("des_")


def generate_reflection_id() -> str:
    """
    Generate a unique reflection identifier.
    
    Returns:
        Reflection ID with 'ref_' prefix
    """
    return generate_id("ref_")


def generate_capability_id() -> str:
    """
    Generate a unique capability identifier.
    
    Returns:
        Capability ID with 'cap_' prefix
    """
    return generate_id("cap_")


def generate_mutation_id() -> str:
    """
    Generate a unique mutation identifier.
    
    Returns:
        Mutation ID with 'mut_' prefix
    """
    return generate_id("mut_")


def validate_id(id_str: str) -> bool:
    """
    Validate that a string is a properly formatted ID.
    
    Args:
        id_str: The ID string to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not id_str or not isinstance(id_str, str):
        return False
    
    # IDs should have a prefix (optional) and a 16-char hex suffix
    parts = id_str.rsplit('_', 1)
    if len(parts) == 2:
        prefix, suffix = parts
        return len(suffix) == 16 and all(c in '0123456789abcdef' for c in suffix)
    else:
        # No prefix, just the hash
        return len(id_str) == 16 and all(c in '0123456789abcdef' for c in id_str)

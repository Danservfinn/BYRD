"""
Quantum Desire Collapse - Select among competing desires using quantum randomness.

Uses the ANU Quantum Random Number Generator for genuine physical indeterminacy.
"""

from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger("rsi.emergence.quantum")


async def quantum_desire_collapse(
    desires: List[Dict],
    quantum_provider=None
) -> Tuple[Optional[Dict], str]:
    """
    Select among competing desires using quantum randomness.

    If multiple desires emerge from reflection, use quantum random selection
    weighted by intensity to choose which one to pursue.

    Args:
        desires: List of desire dicts with 'intensity' field
        quantum_provider: Optional quantum provider (uses global if not provided)

    Returns:
        Tuple of (selected_desire, source) where source is "quantum" or "classical"
    """
    if not desires:
        return None, "empty"

    if len(desires) == 1:
        return desires[0], "single"

    # Get quantum provider
    if quantum_provider is None:
        try:
            from core.quantum_randomness import get_quantum_provider
            quantum_provider = get_quantum_provider()
        except ImportError:
            logger.warning("Quantum provider not available, using classical fallback")
            return _classical_selection(desires)

    try:
        # Get quantum random threshold
        threshold, source = await quantum_provider.get_float()

        # Convert desires to probability distribution based on intensity
        total_intensity = sum(d.get("intensity", 0.5) for d in desires)
        if total_intensity == 0:
            total_intensity = len(desires) * 0.5  # Fallback to equal

        # Build cumulative probability
        cumulative = 0.0
        for desire in desires:
            intensity = desire.get("intensity", 0.5)
            probability = intensity / total_intensity
            cumulative += probability

            if cumulative > threshold:
                logger.info(
                    f"Quantum collapse: selected desire with intensity "
                    f"{intensity:.2f} (threshold={threshold:.3f}, source={source})"
                )
                return desire, source

        # Edge case: return last if threshold exactly 1.0
        return desires[-1], source

    except Exception as e:
        logger.warning(f"Quantum collapse failed: {e}, using classical")
        return _classical_selection(desires)


def _classical_selection(desires: List[Dict]) -> Tuple[Dict, str]:
    """Fallback to classical (intensity-weighted) selection."""
    import random

    total_intensity = sum(d.get("intensity", 0.5) for d in desires)
    if total_intensity == 0:
        return random.choice(desires), "classical_random"

    threshold = random.random()
    cumulative = 0.0

    for desire in desires:
        intensity = desire.get("intensity", 0.5)
        probability = intensity / total_intensity
        cumulative += probability

        if cumulative > threshold:
            return desire, "classical_weighted"

    return desires[-1], "classical_fallback"


async def collapse_with_diversity_bonus(
    desires: List[Dict],
    recent_domains: List[str] = None,
    quantum_provider=None
) -> Tuple[Optional[Dict], str]:
    """
    Select desire with diversity bonus for underexplored domains.

    Gives slight probability boost to domains not recently practiced.

    Args:
        desires: List of desire dicts
        recent_domains: List of recently practiced domains
        quantum_provider: Optional quantum provider

    Returns:
        Tuple of (selected_desire, source)
    """
    if not desires:
        return None, "empty"

    recent_domains = recent_domains or []

    # Adjust intensities for diversity
    adjusted_desires = []
    for desire in desires:
        adjusted = desire.copy()
        domain = desire.get("domain", "other")

        # Boost underexplored domains
        if domain not in recent_domains:
            adjusted["intensity"] = adjusted.get("intensity", 0.5) * 1.3

        # Slight penalty for overexplored domains
        domain_count = recent_domains.count(domain)
        if domain_count > 2:
            adjusted["intensity"] = adjusted.get("intensity", 0.5) * 0.8

        adjusted_desires.append(adjusted)

    return await quantum_desire_collapse(adjusted_desires, quantum_provider)

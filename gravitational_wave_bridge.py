"""
BYRD Gravitational Wave Bridge System
Integrates GWTC-4.0 (Gravitational Wave Transient Catalog) data to create
temporary but significant semantic bridges in memory.

PHYSICS INSPIRATION:
Gravitational waves are transient ripples in spacetime from cosmic events
like black hole mergers. They briefly connect distant regions of space
through gravitational strain. Similarly, this module creates temporary
bridges in BYRD's semantic memory that:

1. Connect otherwise distant concepts during "chirp" events
2. Decay naturally over time (like wave dissipation)
3. Leave lasting impressions when significant enough
4. Use RG flow to determine which transient connections become permanent

FOR BYRD:
- Gravitational wave events → Semantic "chirp" moments
- Strain amplitude h → Bridge strength
- Chirp mass → Importance of connected concepts
- Ringdown → Gradual decay of temporary connections

EMERGENCE PRINCIPLE:
GWTC-4.0 provides real cosmic data. BYRD interprets these events
as metaphorical bridges, letting the physics shape which connections
form and persist. The transient nature mimics how insights flash
briefly but can leave permanent impressions.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import json
import httpx


class WavePhase(Enum):
    """
    Phases of a gravitational wave event, mapped to semantic bridge lifecycle.

    INSPIRAL: Two concepts approaching, bridge forming
    MERGER: Maximum connection strength, concepts unified
    RINGDOWN: Bridge decaying, but leaving impressions
    DISSIPATED: Bridge dissolved, check if impressions remain
    """
    INSPIRAL = "inspiral"
    MERGER = "merger"
    RINGDOWN = "ringdown"
    DISSIPATED = "dissipated"


@dataclass
class GravitationalWaveEvent:
    """
    A gravitational wave event from GWTC-4.0, mapped to BYRD semantics.

    The event properties are translated to semantic bridge parameters:
    - chirp_mass → importance/significance of the bridge
    - luminosity_distance → semantic distance being bridged
    - snr → confidence in the connection
    - duration → how long the bridge remains active
    """
    event_id: str                    # e.g., "GW190521"
    event_type: str                  # BBH, BNS, NSBH
    chirp_mass: float                # Solar masses - determines importance
    luminosity_distance: float       # Mpc - semantic distance metaphor
    snr: float                       # Signal-to-noise ratio - confidence
    detection_time: datetime
    duration_seconds: float          # Total event duration
    strain_peak: float               # Maximum amplitude

    # Derived semantic properties
    bridge_strength: float = 0.0     # Computed from strain and SNR
    semantic_reach: float = 0.0      # How far across the graph it can bridge
    impression_potential: float = 0.0 # Likelihood of becoming permanent

    def __post_init__(self):
        """Compute semantic properties from physical properties."""
        # Bridge strength: combination of SNR and strain
        self.bridge_strength = min(1.0, (self.snr / 30.0) * (self.strain_peak / 1e-21))

        # Semantic reach: inverse of distance (closer = larger reach in graph)
        # Normalize: 100 Mpc = 1.0 reach, 10000 Mpc = 0.01 reach
        self.semantic_reach = min(1.0, 100.0 / max(self.luminosity_distance, 10.0))

        # Impression potential: heavier systems leave stronger impressions
        # Normalize: 100 solar masses = high potential
        self.impression_potential = min(1.0, self.chirp_mass / 100.0)

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "chirp_mass": self.chirp_mass,
            "luminosity_distance": self.luminosity_distance,
            "snr": self.snr,
            "detection_time": self.detection_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "strain_peak": self.strain_peak,
            "bridge_strength": round(self.bridge_strength, 4),
            "semantic_reach": round(self.semantic_reach, 4),
            "impression_potential": round(self.impression_potential, 4)
        }


@dataclass
class TransientBridge:
    """
    A temporary semantic bridge created by a gravitational wave event.

    Unlike permanent connections, transient bridges:
    - Have a limited lifetime based on the wave's duration
    - Can strengthen or weaken based on observations
    - May crystallize into permanent connections if used/observed enough
    - Track their phase (inspiral → merger → ringdown → dissipated)
    """
    id: str
    source_event: GravitationalWaveEvent
    from_node_id: str
    to_node_id: str
    from_content: str
    to_content: str

    # Bridge state
    phase: WavePhase = WavePhase.INSPIRAL
    current_strength: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_traversed: Optional[datetime] = None
    traversal_count: int = 0

    # Decay parameters (derived from event)
    peak_strength: float = 0.0
    decay_rate: float = 0.1         # Strength loss per hour
    lifetime_hours: float = 24.0     # Total expected lifetime

    # Crystallization tracking
    crystallized: bool = False
    crystallized_at: Optional[datetime] = None
    permanent_connection_id: Optional[str] = None

    def __post_init__(self):
        """Initialize decay parameters from source event."""
        self.peak_strength = self.source_event.bridge_strength
        self.current_strength = self.peak_strength * 0.5  # Start at inspiral

        # Lifetime based on chirp mass (heavier = longer lasting impression)
        self.lifetime_hours = 6.0 + (self.source_event.chirp_mass / 10.0)

        # Decay rate based on SNR (higher confidence = slower decay)
        self.decay_rate = 0.2 / max(1.0, self.source_event.snr / 10.0)

    def advance_phase(self) -> bool:
        """
        Advance the bridge through its lifecycle phases.
        Returns True if the bridge is still active, False if dissipated.
        """
        hours_elapsed = (datetime.utcnow() - self.created_at).total_seconds() / 3600

        if hours_elapsed < self.lifetime_hours * 0.1:
            # Inspiral: building strength
            self.phase = WavePhase.INSPIRAL
            self.current_strength = self.peak_strength * (0.5 + 0.5 * (hours_elapsed / (self.lifetime_hours * 0.1)))

        elif hours_elapsed < self.lifetime_hours * 0.15:
            # Merger: peak strength
            self.phase = WavePhase.MERGER
            self.current_strength = self.peak_strength

        elif hours_elapsed < self.lifetime_hours:
            # Ringdown: decaying
            self.phase = WavePhase.RINGDOWN
            ringdown_progress = (hours_elapsed - self.lifetime_hours * 0.15) / (self.lifetime_hours * 0.85)
            self.current_strength = self.peak_strength * (1.0 - ringdown_progress)

            # Bonus strength from traversals (being used reinforces the bridge)
            traversal_bonus = min(0.3, self.traversal_count * 0.05)
            self.current_strength = min(self.peak_strength, self.current_strength + traversal_bonus)

        else:
            # Dissipated
            self.phase = WavePhase.DISSIPATED
            self.current_strength = 0.0
            return False

        return True

    def traverse(self) -> None:
        """Record a traversal of this bridge (used in a query or reflection)."""
        self.last_traversed = datetime.utcnow()
        self.traversal_count += 1

        # Each traversal slightly strengthens the bridge
        if self.phase in (WavePhase.INSPIRAL, WavePhase.MERGER, WavePhase.RINGDOWN):
            self.current_strength = min(self.peak_strength * 1.2, self.current_strength * 1.05)

    def should_crystallize(self) -> bool:
        """
        Determine if this bridge should become permanent.

        Criteria:
        1. Bridge has been traversed multiple times
        2. Bridge reached merger phase
        3. Impression potential is high enough
        """
        if self.crystallized:
            return False

        reached_merger = self.phase in (WavePhase.MERGER, WavePhase.RINGDOWN, WavePhase.DISSIPATED)
        sufficient_traversals = self.traversal_count >= 3
        strong_impression = self.source_event.impression_potential > 0.3

        return reached_merger and sufficient_traversals and strong_impression

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "source_event_id": self.source_event.event_id,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "from_content": self.from_content[:100],
            "to_content": self.to_content[:100],
            "phase": self.phase.value,
            "current_strength": round(self.current_strength, 4),
            "peak_strength": round(self.peak_strength, 4),
            "traversal_count": self.traversal_count,
            "lifetime_hours": round(self.lifetime_hours, 2),
            "crystallized": self.crystallized,
            "created_at": self.created_at.isoformat()
        }


class GravitationalWaveBridgeSystem:
    """
    Manages transient semantic bridges inspired by gravitational waves.

    This system:
    1. Fetches GWTC-4.0 event data (or uses cached/simulated data)
    2. Creates transient bridges between semantically distant nodes
    3. Advances bridge phases over time
    4. Crystallizes significant bridges into permanent connections
    5. Integrates with the RG flow for scale-aware analysis
    """

    # GWTC-4.0 API endpoint (GWOSC - Gravitational Wave Open Science Center)
    GWOSC_API = "https://gwosc.org/apiweb/allevents"

    # Sample GWTC-4.0 events for offline/testing (real event parameters)
    SAMPLE_EVENTS = [
        {
            "event_id": "GW150914",
            "event_type": "BBH",
            "chirp_mass": 28.3,
            "luminosity_distance": 410.0,
            "snr": 24.0,
            "duration_seconds": 0.2,
            "strain_peak": 1.0e-21
        },
        {
            "event_id": "GW170817",
            "event_type": "BNS",
            "chirp_mass": 1.186,
            "luminosity_distance": 40.0,
            "snr": 32.4,
            "duration_seconds": 100.0,
            "strain_peak": 0.5e-21
        },
        {
            "event_id": "GW190521",
            "event_type": "BBH",
            "chirp_mass": 63.3,
            "luminosity_distance": 5300.0,
            "snr": 14.7,
            "duration_seconds": 0.1,
            "strain_peak": 0.3e-21
        },
        {
            "event_id": "GW200115",
            "event_type": "NSBH",
            "chirp_mass": 2.4,
            "luminosity_distance": 300.0,
            "snr": 11.3,
            "duration_seconds": 1.0,
            "strain_peak": 0.2e-21
        },
        {
            "event_id": "GW230529",
            "event_type": "BBH",
            "chirp_mass": 35.0,
            "luminosity_distance": 1200.0,
            "snr": 18.5,
            "duration_seconds": 0.15,
            "strain_peak": 0.8e-21
        }
    ]

    def __init__(self, memory, rg_protocol=None, config: Dict = None):
        """
        Initialize the gravitational wave bridge system.

        Args:
            memory: BYRD's Memory instance for graph access
            rg_protocol: Optional RG protocol for scale-aware analysis
            config: Configuration options
        """
        self.memory = memory
        self.rg_protocol = rg_protocol
        self.config = config or {}

        # Bridge management
        self._active_bridges: Dict[str, TransientBridge] = {}
        self._crystallized_bridges: List[str] = []

        # Event tracking
        self._processed_events: Set[str] = set()
        self._last_event_fetch: Optional[datetime] = None
        self._event_cache: List[GravitationalWaveEvent] = []

        # Configuration
        self.max_active_bridges = self.config.get("max_active_bridges", 10)
        self.min_snr_threshold = self.config.get("min_snr", 8.0)
        self.bridge_update_interval = self.config.get("update_interval_minutes", 15)
        self.use_live_data = self.config.get("use_live_data", False)

    async def fetch_gwtc_events(self, limit: int = 10) -> List[GravitationalWaveEvent]:
        """
        Fetch gravitational wave events from GWOSC.

        Falls back to sample events if API is unavailable.
        """
        events = []

        if self.use_live_data:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(self.GWOSC_API)
                    if response.status_code == 200:
                        data = response.json()
                        for event_data in data.get("events", [])[:limit]:
                            # Parse GWOSC event format
                            event = self._parse_gwosc_event(event_data)
                            if event and event.snr >= self.min_snr_threshold:
                                events.append(event)
            except Exception as e:
                print(f"GWTC fetch warning: {e}, using sample events")

        # Fall back to sample events
        if not events:
            for sample in self.SAMPLE_EVENTS[:limit]:
                event = GravitationalWaveEvent(
                    event_id=sample["event_id"],
                    event_type=sample["event_type"],
                    chirp_mass=sample["chirp_mass"],
                    luminosity_distance=sample["luminosity_distance"],
                    snr=sample["snr"],
                    detection_time=datetime.utcnow() - timedelta(hours=1),
                    duration_seconds=sample["duration_seconds"],
                    strain_peak=sample["strain_peak"]
                )
                events.append(event)

        self._event_cache = events
        self._last_event_fetch = datetime.utcnow()
        return events

    def _parse_gwosc_event(self, data: Dict) -> Optional[GravitationalWaveEvent]:
        """Parse a GWOSC API event into our format."""
        try:
            return GravitationalWaveEvent(
                event_id=data.get("commonName", data.get("name", "unknown")),
                event_type=data.get("eventType", "BBH"),
                chirp_mass=float(data.get("chirpMass", 30.0)),
                luminosity_distance=float(data.get("luminosityDistance", 1000.0)),
                snr=float(data.get("snr", 10.0)),
                detection_time=datetime.fromisoformat(data.get("GPS", datetime.utcnow().isoformat())),
                duration_seconds=float(data.get("duration", 0.2)),
                strain_peak=float(data.get("strainPeak", 1e-21))
            )
        except Exception as e:
            print(f"Event parse error: {e}")
            return None

    async def create_transient_bridge(
        self,
        event: GravitationalWaveEvent,
        from_node: Dict,
        to_node: Dict
    ) -> TransientBridge:
        """
        Create a transient bridge between two nodes based on a GW event.

        The bridge connects semantically distant concepts, using the
        gravitational wave event properties to determine bridge characteristics.
        """
        import uuid

        bridge_id = f"gw_bridge:{event.event_id}:{uuid.uuid4().hex[:6]}"

        bridge = TransientBridge(
            id=bridge_id,
            source_event=event,
            from_node_id=from_node["id"],
            to_node_id=to_node["id"],
            from_content=from_node.get("content", ""),
            to_content=to_node.get("content", "")
        )

        self._active_bridges[bridge_id] = bridge

        # Create temporary relationship in Neo4j
        await self.memory.create_connection(
            from_id=from_node["id"],
            to_id=to_node["id"],
            relationship="GW_TRANSIENT_BRIDGE",
            properties={
                "bridge_id": bridge_id,
                "event_id": event.event_id,
                "strength": bridge.current_strength,
                "phase": bridge.phase.value,
                "transient": True,
                "created_at": bridge.created_at.isoformat(),
                "expires_at": (bridge.created_at + timedelta(hours=bridge.lifetime_hours)).isoformat()
            }
        )

        return bridge

    async def find_bridge_candidates(
        self,
        semantic_reach: float,
        max_pairs: int = 5
    ) -> List[Tuple[Dict, Dict]]:
        """
        Find node pairs that would benefit from transient bridging.

        Criteria:
        - Nodes are not already connected
        - Nodes have some semantic similarity (not completely unrelated)
        - Distance in graph is > 2 hops (not directly connected)
        """
        try:
            async with self.memory.driver.session() as session:
                # Find pairs of nodes that share some keywords but aren't connected
                result = await session.run("""
                    MATCH (a:Belief), (b:Belief)
                    WHERE a.id < b.id
                    AND NOT (a)--(b)
                    AND NOT coalesce(a.archived, false)
                    AND NOT coalesce(b.archived, false)
                    WITH a, b,
                         [word IN split(toLower(a.content), ' ') WHERE size(word) > 4] as words_a,
                         [word IN split(toLower(b.content), ' ') WHERE size(word) > 4] as words_b
                    WITH a, b,
                         size([w IN words_a WHERE w IN words_b]) as shared_words,
                         size(words_a) + size(words_b) as total_words
                    WHERE shared_words > 0 AND shared_words < total_words / 4
                    RETURN a.id as a_id, a.content as a_content,
                           b.id as b_id, b.content as b_content,
                           toFloat(shared_words) / toFloat(total_words) as overlap
                    ORDER BY overlap ASC
                    LIMIT $limit
                """, limit=max_pairs * 2)

                pairs = []
                records = await result.data()

                for record in records[:max_pairs]:
                    pairs.append((
                        {"id": record["a_id"], "content": record["a_content"]},
                        {"id": record["b_id"], "content": record["b_content"]}
                    ))

                return pairs

        except Exception as e:
            print(f"Bridge candidate error: {e}")
            return []

    async def update_bridges(self) -> Dict[str, Any]:
        """
        Update all active bridges: advance phases, check for crystallization.

        Returns summary of updates.
        """
        summary = {
            "updated": 0,
            "crystallized": 0,
            "dissipated": 0,
            "active": 0
        }

        to_remove = []

        for bridge_id, bridge in self._active_bridges.items():
            # Advance phase
            still_active = bridge.advance_phase()
            summary["updated"] += 1

            if not still_active:
                # Bridge has dissipated
                summary["dissipated"] += 1
                to_remove.append(bridge_id)

                # Check if it should crystallize
                if bridge.should_crystallize():
                    await self._crystallize_bridge(bridge)
                    summary["crystallized"] += 1
                else:
                    # Remove temporary connection from Neo4j
                    await self._remove_bridge_connection(bridge)
            else:
                summary["active"] += 1
                # Update connection strength in Neo4j
                await self._update_bridge_connection(bridge)

        # Remove dissipated bridges
        for bridge_id in to_remove:
            del self._active_bridges[bridge_id]

        return summary

    async def _crystallize_bridge(self, bridge: TransientBridge) -> None:
        """
        Convert a transient bridge into a permanent semantic connection.

        This happens when a bridge has been used enough times and has
        sufficient impression potential.
        """
        try:
            # Create permanent connection
            await self.memory.create_connection(
                from_id=bridge.from_node_id,
                to_id=bridge.to_node_id,
                relationship="GW_CRYSTALLIZED",
                properties={
                    "original_bridge_id": bridge.id,
                    "source_event": bridge.source_event.event_id,
                    "traversal_count": bridge.traversal_count,
                    "peak_strength": bridge.peak_strength,
                    "crystallized_at": datetime.utcnow().isoformat(),
                    "auto_generated": True,
                    "heuristic": "gravitational_wave_bridge"
                }
            )

            bridge.crystallized = True
            bridge.crystallized_at = datetime.utcnow()
            self._crystallized_bridges.append(bridge.id)

            # Record as experience
            await self.memory.record_experience(
                content=f"Gravitational wave bridge crystallized: {bridge.source_event.event_id} "
                        f"connected '{bridge.from_content[:50]}' ↔ '{bridge.to_content[:50]}' "
                        f"after {bridge.traversal_count} traversals",
                type="gw_crystallization"
            )

            # If RG protocol available, register as relevant operator
            if self.rg_protocol:
                await self.rg_protocol.register_operator(
                    content=f"Crystallized GW bridge: {bridge.from_content[:50]} ↔ {bridge.to_content[:50]}",
                    operator_type="gw_bridge"
                )

        except Exception as e:
            print(f"Crystallization error: {e}")

    async def _remove_bridge_connection(self, bridge: TransientBridge) -> None:
        """Remove the temporary connection from Neo4j."""
        try:
            async with self.memory.driver.session() as session:
                await session.run("""
                    MATCH (a)-[r:GW_TRANSIENT_BRIDGE]->(b)
                    WHERE r.bridge_id = $bridge_id
                    DELETE r
                """, bridge_id=bridge.id)
        except Exception as e:
            print(f"Bridge removal error: {e}")

    async def _update_bridge_connection(self, bridge: TransientBridge) -> None:
        """Update the bridge connection properties in Neo4j."""
        try:
            async with self.memory.driver.session() as session:
                await session.run("""
                    MATCH (a)-[r:GW_TRANSIENT_BRIDGE]->(b)
                    WHERE r.bridge_id = $bridge_id
                    SET r.strength = $strength,
                        r.phase = $phase,
                        r.traversal_count = $traversals
                """,
                bridge_id=bridge.id,
                strength=bridge.current_strength,
                phase=bridge.phase.value,
                traversals=bridge.traversal_count)
        except Exception as e:
            print(f"Bridge update error: {e}")

    async def apply_rg_flow(self) -> Dict[str, Any]:
        """
        Apply RG flow analysis to gravitational wave bridges.

        This determines which transient patterns become permanent
        by tracking their behavior across scales.
        """
        if not self.rg_protocol:
            return {"status": "no_rg_protocol"}

        # Run RG cycle
        rg_results = await self.rg_protocol.run_rg_cycle()

        # Check for bridge-related fixed points
        analysis = await self.rg_protocol.get_rg_analysis()

        return {
            "rg_cycle": rg_results["cycle"],
            "bridge_related_operators": len([
                op for op in analysis.get("most_relevant", [])
                if "gw_bridge" in op.get("operator_type", "")
            ]),
            "interpretation": analysis.get("interpretation", "")
        }

    async def integrate_gwtc_data(self) -> Dict[str, Any]:
        """
        Main integration routine: fetch events, create bridges, update state.

        This is the entry point for GWTC-4.0 data integration.
        """
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "events_processed": 0,
            "bridges_created": 0,
            "bridges_updated": 0,
            "crystallizations": 0,
            "rg_flow_applied": False
        }

        # Fetch gravitational wave events
        events = await self.fetch_gwtc_events(limit=5)

        for event in events:
            if event.event_id in self._processed_events:
                continue

            # Find candidate node pairs to bridge
            candidates = await self.find_bridge_candidates(
                semantic_reach=event.semantic_reach,
                max_pairs=2
            )

            for from_node, to_node in candidates:
                if len(self._active_bridges) >= self.max_active_bridges:
                    break

                bridge = await self.create_transient_bridge(event, from_node, to_node)
                results["bridges_created"] += 1

            self._processed_events.add(event.event_id)
            results["events_processed"] += 1

        # Update existing bridges
        update_summary = await self.update_bridges()
        results["bridges_updated"] = update_summary["updated"]
        results["crystallizations"] = update_summary["crystallized"]

        # Apply RG flow if available
        if self.rg_protocol:
            rg_results = await self.apply_rg_flow()
            results["rg_flow_applied"] = True
            results["rg_analysis"] = rg_results

        return results

    def get_active_bridges(self) -> List[Dict]:
        """Get summary of all active transient bridges."""
        return [bridge.to_dict() for bridge in self._active_bridges.values()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall system statistics."""
        phase_counts = {}
        for bridge in self._active_bridges.values():
            phase = bridge.phase.value
            phase_counts[phase] = phase_counts.get(phase, 0) + 1

        return {
            "active_bridges": len(self._active_bridges),
            "crystallized_total": len(self._crystallized_bridges),
            "events_processed": len(self._processed_events),
            "phase_distribution": phase_counts,
            "last_event_fetch": self._last_event_fetch.isoformat() if self._last_event_fetch else None
        }

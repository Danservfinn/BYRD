"""
BYRD Dreaming Machine
Loop 4 of Option B: Experience Multiplication

The Dreaming Machine multiplies learning from each experience through:
1. COUNTERFACTUAL GENERATION: "What if I had done X instead?"
2. EXPERIENCE REPLAY: Revisit and extract new insights from past experiences
3. CROSS-DOMAIN TRANSFER: Apply patterns from one domain to another

THE KEY INSIGHT: Each experience can teach multiple lessons.
A single success/failure can generate many insights through counterfactual
analysis and cross-domain thinking.

This loop compounds because:
- More experiences → more counterfactuals → more insights → more capability
- Cross-domain transfer multiplies pattern value
- Replay extracts insights missed on first pass
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from memory import Memory
from event_bus import event_bus, Event, EventType

# Import loop instrumentation to break zero-delta loops
try:
    from loop_instrumentation import LoopInstrumenter, CycleMetrics, get_instrumenter
    HAS_INSTRUMENTATION = True
except ImportError:
    HAS_INSTRUMENTATION = False
    print("[WARNING] loop_instrumentation not available - zero-delta detection disabled")

logger = logging.getLogger(__name__)


class InsightSource(Enum):
    """Source type for generated insights."""
    COUNTERFACTUAL = "counterfactual"
    REPLAY = "replay"
    TRANSFER = "transfer"
    REFLECTION = "reflection"


@dataclass
class Counterfactual:
    """A 'what if' scenario generated from an experience."""
    id: str
    original_experience_id: str
    scenario: str
    predicted_outcome: str
    confidence: float
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GeneratedInsight:
    """An insight extracted by the Dreaming Machine."""
    content: str
    source_type: InsightSource
    confidence: float
    supporting_evidence: List[str]
    domains: List[str]


class DreamingMachine:
    """
    Loop 4 of Option B: Experience Multiplication.

    Multiplies learning by generating counterfactuals, replaying experiences,
    and transferring patterns across domains.
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: Any,
        config: Optional[Dict] = None
    ):
        """
        Initialize the Dreaming Machine.

        Args:
            memory: The BYRD memory system
            llm_client: LLM client for insight generation
            config: Configuration from config.yaml option_b.dreaming_machine
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Counterfactual settings
        cf_config = self.config.get("counterfactual", {})
        self.cf_enabled = cf_config.get("enabled", True)
        self.cf_variations = cf_config.get("variations_per_experience", 3)
        self.cf_min_age_hours = cf_config.get("min_experience_age_hours", 0.5)

        # Replay settings
        replay_config = self.config.get("replay", {})
        self.replay_enabled = replay_config.get("enabled", True)
        self.replay_window_hours = replay_config.get("window_hours", 24)
        self.replay_sample_size = replay_config.get("sample_size", 10)

        # Transfer settings
        transfer_config = self.config.get("transfer", {})
        self.transfer_enabled = transfer_config.get("enabled", True)
        self.transfer_min_success = transfer_config.get("min_pattern_success", 2)
        self.transfer_similarity = transfer_config.get("similarity_threshold", 0.5)

        # Metrics
        self._counterfactuals_generated = 0
        self._replays_completed = 0
        self._transfers_attempted = 0
        self._insights_created = 0

        # Initialize loop instrumentation to break zero-delta loops
        self.instrumenter: Optional['LoopInstrumenter'] = None
        self.loop_name: str = "dreaming_machine"
        if HAS_INSTRUMENTATION:
            try:
                self.instrumenter = get_instrumenter()
                if self.instrumenter:
                    self.instrumenter.register_loop(self.loop_name)
                    print(f"[INSTRUMENTATION] Registered loop '{self.loop_name}' for zero-delta detection")
            except Exception:
                pass

        # Cycle counter for instrumentation
        self._cycle_counter = 0

        # Learning component (injected by Omega)
        self.world_model = None  # WorldModel for prediction-based counterfactuals

    async def dream_cycle(self) -> Dict[str, Any]:
        """
        Run a complete dreaming cycle.

        Generates counterfactuals, replays experiences, and attempts transfers.
        Returns statistics about the cycle.
        """
        start_time = datetime.now()
        results = {
            "counterfactuals": 0,
            "replays": 0,
            "transfers": 0,
            "insights": 0
        }

        await event_bus.emit(Event(
            type=EventType.LOOP_CYCLE_START,
            data={"loop_name": "dreaming_machine"}
        ))

        # Phase 1: Counterfactual generation
        if self.cf_enabled:
            cf_count = await self._generate_counterfactuals()
            results["counterfactuals"] = cf_count

        # Phase 2: Experience replay
        if self.replay_enabled:
            replay_count = await self._replay_experiences()
            results["replays"] = replay_count

        # Phase 3: Cross-domain transfer
        if self.transfer_enabled:
            transfer_count = await self._attempt_transfers()
            results["transfers"] = transfer_count

        results["insights"] = self._insights_created

        await event_bus.emit(Event(
            type=EventType.LOOP_CYCLE_END,
            data={
                "loop_name": "dreaming_machine",
                "results": results
            }
        ))

        # INTEGRATION WITH LOOP INSTRUMENTATION
        # Record cycle metrics to break zero-delta loops
        if self.instrumenter and HAS_INSTRUMENTATION:
            self._record_dreaming_cycle(results, start_time)

        return results

    def _record_dreaming_cycle(
        self,
        results: Dict[str, Any],
        start_time: datetime
    ) -> None:
        """
        Record dreaming cycle metrics with loop instrumenter.
        
        This breaks the zero-delta loop by tracking:
        - Insight generation rate (delta)
        - Success based on insights created and quality
        - Duration of the dreaming cycle
        - Whether the improvement was meaningful
        """
        if not self.instrumenter:
            return
        
        self._cycle_counter += 1
        
        # Calculate delta as change in insights per cycle
        total_insights = results.get("insights", 0)
        
        # Track baseline insights from previous cycles
        if not hasattr(self, '_baseline_insights_per_cycle'):
            self._baseline_insights_per_cycle = 0.0
        
        # Delta is improvement in insights generated
        delta = total_insights - self._baseline_insights_per_cycle
        self._baseline_insights_per_cycle = total_insights
        
        # Success if we generated insights across multiple activities
        success = (results.get("counterfactuals", 0) > 0 or 
                  results.get("replays", 0) > 0 or 
                  results.get("transfers", 0) > 0)
        
        # Duration
        duration_seconds = (datetime.now() - start_time).total_seconds()
        
        # Meaningful if we generated at least one insight and delta >= 0
        MIN_MEANINGFUL_DELTA = 0.005
        is_meaningful = total_insights > 0 and delta >= 0
        
        # Create cycle metrics
        from loop_instrumentation import CycleMetrics
        metrics = CycleMetrics(
            cycle_number=self._cycle_counter,
            timestamp=datetime.now(),
            delta=delta,
            success=success,
            meaningful=is_meaningful,
            duration_seconds=duration_seconds,
            error=None
        )
        
        # Record with instrumenter (pass individual params, not metrics object)
        self.instrumenter.record_cycle(
            self.loop_name,
            delta=metrics.delta,
            success=metrics.success,
            duration_seconds=metrics.duration_seconds
        )
        
        # Check for stagnation and log warning
        if self.instrumenter.is_stagnant(self.loop_name):
            analysis = self.instrumenter.analyze_stagnation(self.loop_name)
            logger.warning(f"[INSTRUMENTATION] Dreaming Machine stagnation detected: {analysis}")

    async def _generate_counterfactuals(self) -> int:
        """
        Generate counterfactual scenarios from recent experiences.

        Returns count of counterfactuals generated.
        """
        # Get recent experiences old enough for reflection
        min_age = datetime.now() - timedelta(hours=self.cf_min_age_hours)

        # Query experiences
        # For now, get recent experiences and filter by age
        experiences = await self.memory.get_recent_experiences(limit=20)

        eligible = [
            e for e in experiences
            if self._parse_datetime(e.get("timestamp")) < min_age
        ][:5]  # Process up to 5 experiences

        count = 0
        for exp in eligible:
            try:
                insights = await self._generate_counterfactuals_for_experience(exp)
                count += len(insights)
            except Exception as e:
                logger.debug(f"Counterfactual generation failed: {e}")

        self._counterfactuals_generated += count
        return count

    async def _generate_counterfactuals_for_experience(
        self,
        experience: Dict
    ) -> List[GeneratedInsight]:
        """
        Generate counterfactual scenarios for a single experience.

        If world_model is available, uses its prediction capabilities for
        more grounded counterfactual reasoning.
        """
        content = experience.get("content", "")
        exp_id = experience.get("id", "")

        # Try to extract action and context from experience for world model
        action = experience.get("action", content[:100])
        context = experience.get("context", {})

        # If world_model available, use it for prediction-grounded counterfactuals
        world_model_predictions = []
        if self.world_model:
            try:
                # Generate alternative actions with LLM first
                alt_prompt = f"""Given this experience, suggest {self.cf_variations} alternative actions that could have been taken:

Experience: {content}

List {self.cf_variations} alternative actions (one per line, just the action):"""

                alt_response = await self.llm_client.query(alt_prompt, max_tokens=200)
                alt_actions = [line.strip() for line in alt_response.strip().split("\n") if line.strip()][:self.cf_variations]

                # Get world model predictions for each alternative
                for alt_action in alt_actions:
                    prediction = await self.world_model.predict_outcome(alt_action, context)
                    world_model_predictions.append({
                        "action": alt_action,
                        "predicted_outcome": prediction.predicted_outcome,
                        "confidence": prediction.confidence,
                        "reasoning": prediction.reasoning
                    })
            except Exception as e:
                logger.debug(f"World model prediction failed: {e}")

        # Build prompt with world model context if available
        if world_model_predictions:
            wm_context = "\n".join([
                f"- Alternative: {p['action']}\n  World model prediction: {p['predicted_outcome']} (confidence: {p['confidence']:.0%})"
                for p in world_model_predictions
            ])
            prompt = f"""Analyze this experience and generate insights from these alternative scenarios.

Experience: {content}

World Model Predictions for alternatives:
{wm_context}

For each alternative, extract an insight about what to do in similar situations.

Format:
COUNTERFACTUAL 1:
Alternative: [action from above]
Predicted outcome: [outcome from world model + your analysis]
Insight: [lesson learned]

COUNTERFACTUAL 2:
...
"""
        else:
            # Fallback to pure LLM counterfactuals
            prompt = f"""Analyze this experience and generate {self.cf_variations} counterfactual scenarios.

Experience: {content}

For each counterfactual:
1. Describe what could have been done differently
2. Predict what the outcome would have been
3. Extract an insight about what to do in similar situations

Format:
COUNTERFACTUAL 1:
Alternative: [what could have been different]
Predicted outcome: [likely result]
Insight: [lesson learned]

COUNTERFACTUAL 2:
...
"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=800)

            # Parse counterfactuals and create insights
            insights = self._parse_counterfactual_response(response, exp_id)

            for insight in insights:
                await self._store_insight(insight)

            await event_bus.emit(Event(
                type=EventType.COUNTERFACTUAL_GENERATED,
                data={
                    "experience_id": exp_id,
                    "count": len(insights),
                    "used_world_model": bool(world_model_predictions)
                }
            ))

            return insights

        except Exception as e:
            logger.debug(f"Failed to generate counterfactuals: {e}")
            return []

    def _parse_counterfactual_response(
        self,
        response: str,
        experience_id: str
    ) -> List[GeneratedInsight]:
        """Parse LLM response into structured insights."""
        insights = []

        # Simple parsing: look for "Insight:" lines
        lines = response.split("\n")
        current_insight = None

        for line in lines:
            line = line.strip()
            if line.lower().startswith("insight:"):
                insight_content = line[8:].strip()
                if insight_content:
                    insights.append(GeneratedInsight(
                        content=insight_content,
                        source_type=InsightSource.COUNTERFACTUAL,
                        confidence=0.6,
                        supporting_evidence=[experience_id],
                        domains=["general"]
                    ))

        return insights

    async def _replay_experiences(self) -> int:
        """
        Replay past experiences to extract new insights.

        Returns count of experiences replayed.
        """
        # Get experiences from replay window
        window_start = datetime.now() - timedelta(hours=self.replay_window_hours)

        experiences = await self.memory.get_recent_experiences(limit=50)

        # Filter to window and sample
        eligible = [
            e for e in experiences
            if self._parse_datetime(e.get("timestamp")) >= window_start
        ]

        if len(eligible) > self.replay_sample_size:
            sample = random.sample(eligible, self.replay_sample_size)
        else:
            sample = eligible

        count = 0
        for exp in sample:
            try:
                insights = await self._replay_single_experience(exp)
                count += len(insights)
            except Exception as e:
                logger.debug(f"Replay failed: {e}")

        self._replays_completed += count
        return count

    async def _replay_single_experience(
        self,
        experience: Dict
    ) -> List[GeneratedInsight]:
        """
        Replay a single experience to extract insights.
        """
        content = experience.get("content", "")
        exp_id = experience.get("id", "")
        exp_type = experience.get("type", "unknown")

        prompt = f"""Deeply analyze this experience to extract insights:

Type: {exp_type}
Content: {content}

Look for:
1. Patterns that could apply to other situations
2. Implicit assumptions that were made
3. Knowledge that could transfer to other domains
4. Missed opportunities or overlooked aspects

List 1-3 key insights, each as a single clear statement."""

        try:
            response = await self.llm_client.query(prompt, max_tokens=400)

            # Parse into insights
            insights = self._parse_replay_response(response, exp_id)

            for insight in insights:
                await self._store_insight(insight)

            return insights

        except Exception as e:
            logger.debug(f"Failed to replay experience: {e}")
            return []

    def _parse_replay_response(
        self,
        response: str,
        experience_id: str
    ) -> List[GeneratedInsight]:
        """Parse replay response into insights."""
        insights = []
        lines = response.strip().split("\n")

        for line in lines:
            line = line.strip()
            # Skip empty lines and headers
            if not line or line.startswith("Look for") or len(line) < 20:
                continue

            # Remove numbering like "1. " or "- "
            if line[0].isdigit() and len(line) > 3:
                line = line[2:].strip()
            elif line.startswith("- "):
                line = line[2:].strip()

            if len(line) > 20:
                insights.append(GeneratedInsight(
                    content=line,
                    source_type=InsightSource.REPLAY,
                    confidence=0.5,
                    supporting_evidence=[experience_id],
                    domains=["general"]
                ))

        return insights[:3]  # Limit to 3 insights

    async def _attempt_transfers(self) -> int:
        """
        Attempt to transfer successful patterns to new domains.

        Returns count of transfer attempts.
        """
        # Get patterns that have succeeded multiple times
        patterns = await self.memory.get_patterns_for_lifting(
            min_success_count=self.transfer_min_success,
            min_domain_count=1
        )

        count = 0
        for pattern in patterns[:5]:  # Process up to 5 patterns
            try:
                insights = await self._attempt_pattern_transfer(pattern)
                count += len(insights)
            except Exception as e:
                logger.debug(f"Transfer failed: {e}")

        self._transfers_attempted += count
        return count

    async def _attempt_pattern_transfer(
        self,
        pattern: Dict
    ) -> List[GeneratedInsight]:
        """
        Attempt to transfer a pattern to new domains.
        """
        template = pattern.get("solution_template", "")
        current_domains = pattern.get("domains", [])

        prompt = f"""This solution pattern has worked in these domains: {', '.join(current_domains)}

Pattern: {template}

Identify 2-3 NEW domains where this pattern might apply.
For each new domain:
1. Name the domain
2. Explain how the pattern would apply
3. Rate confidence (high/medium/low)

Format each as:
Domain: [name]
Application: [how it applies]
Confidence: [high/medium/low]"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)

            # Parse transfer suggestions
            insights = self._parse_transfer_response(
                response,
                pattern.get("id", ""),
                template
            )

            for insight in insights:
                await self._store_insight(insight)

            return insights

        except Exception as e:
            logger.debug(f"Failed to transfer pattern: {e}")
            return []

    def _parse_transfer_response(
        self,
        response: str,
        pattern_id: str,
        template: str
    ) -> List[GeneratedInsight]:
        """Parse transfer response into insights."""
        insights = []
        lines = response.split("\n")

        current_domain = None
        current_application = None

        for line in lines:
            line = line.strip()
            if line.lower().startswith("domain:"):
                current_domain = line[7:].strip()
            elif line.lower().startswith("application:"):
                current_application = line[12:].strip()

                if current_domain and current_application:
                    insights.append(GeneratedInsight(
                        content=f"Pattern could apply to {current_domain}: {current_application}",
                        source_type=InsightSource.TRANSFER,
                        confidence=0.5,
                        supporting_evidence=[pattern_id],
                        domains=[current_domain]
                    ))
                    current_domain = None
                    current_application = None

        return insights

    async def _store_insight(self, insight: GeneratedInsight):
        """Store an insight in memory."""
        try:
            # Get embedding for the insight
            from embedding import get_global_embedder
            embedder = get_global_embedder()
            result = await embedder.embed(insight.content)

            await self.memory.create_insight(
                content=insight.content,
                source_type=insight.source_type.value,
                confidence=insight.confidence,
                supporting_evidence=insight.supporting_evidence,
                embedding=result.embedding
            )

            self._insights_created += 1

            await event_bus.emit(Event(
                type=EventType.INSIGHT_CREATED,
                data={
                    "content": insight.content,
                    "source_type": insight.source_type.value,
                    "confidence": insight.confidence,
                    "domains": insight.domains
                }
            ))

        except Exception as e:
            logger.debug(f"Failed to store insight: {e}")

    def _parse_datetime(self, dt: Any) -> datetime:
        """Parse datetime from storage format."""
        if isinstance(dt, datetime):
            return dt
        if isinstance(dt, str):
            try:
                return datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except:
                return datetime.now()
        return datetime.now()

    def get_metrics(self) -> Dict[str, Any]:
        """Get Dreaming Machine metrics."""
        return {
            "counterfactuals_generated": self._counterfactuals_generated,
            "replays_completed": self._replays_completed,
            "transfers_attempted": self._transfers_attempted,
            "insights_created": self._insights_created,
            "multiplication_factor": (
                self._insights_created / max(1, self._replays_completed + self._counterfactuals_generated // self.cf_variations)
            )
        }

    def is_healthy(self) -> bool:
        """Check if the Dreaming Machine is healthy."""
        # Should generate at least some insights
        total_operations = (
            self._counterfactuals_generated +
            self._replays_completed +
            self._transfers_attempted
        )

        if total_operations < 10:
            return True  # Too early to judge

        # Should create insights from at least 30% of operations
        return (self._insights_created / total_operations) >= 0.3


# Factory function
def create_dreaming_machine(
    memory: Memory,
    llm_client: Any,
    config: Dict
) -> DreamingMachine:
    """
    Create a Dreaming Machine from configuration.

    Args:
        memory: The BYRD memory system
        llm_client: LLM client
        config: Full config.yaml dict

    Returns:
        Configured DreamingMachine instance
    """
    dm_config = config.get("option_b", {}).get("dreaming_machine", {})
    return DreamingMachine(memory, llm_client, dm_config)

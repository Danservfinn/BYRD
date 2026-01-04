"""
BYRD Intuition Network

Trainable "taste" for decisions.

Key insight: After enough experience, BYRD develops intuitions
about which actions tend to succeed in which contexts.

Uses sentence-transformers for semantic similarity and
learns from outcome feedback.

NOTE: Falls back gracefully if sentence-transformers not available.

Version: 1.0
Created: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import json


@dataclass
class Intuition:
    """A learned intuition about context-action-outcome relationships."""
    context_embedding: List[float]
    action: str
    success_rate: float
    observations: int
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class IntuitionScore:
    """Score for an action in a given context."""
    action: str
    score: float
    confidence: float
    similar_experiences: int
    reasoning: str


class IntuitionNetwork:
    """
    Trainable "taste" for decisions.

    Learns from experience which actions tend to succeed in which contexts.
    Uses semantic similarity to generalize from past experiences.

    CRITICAL: Provides fast heuristics for Goal Evolver and Memory Reasoner
    when full reasoning is too slow.

    Training Signal:
    - Action outcomes (success/failure) provide ground truth
    - Context similarity allows generalization
    - Recency weighting favors recent experience
    """

    def __init__(self, memory, config: Dict = None):
        """
        Initialize the intuition network.

        Args:
            memory: Memory system for persistence
            config: Optional configuration
        """
        self.memory = memory
        self.config = config or {}

        # Try to import sentence-transformers
        self._encoder = None
        self._has_embeddings = False

        try:
            from sentence_transformers import SentenceTransformer
            model_name = self.config.get("model", "all-MiniLM-L6-v2")
            self._encoder = SentenceTransformer(model_name)
            self._has_embeddings = True
            print(f"   IntuitionNetwork: Using {model_name} for embeddings")
        except ImportError:
            print("   IntuitionNetwork: No sentence-transformers, using keyword fallback")

        # In-memory intuition cache
        self._intuitions: Dict[str, List[Intuition]] = {}  # action -> list of intuitions

        # Statistics
        self._total_observations = 0
        self._successful_predictions = 0

    def reset(self):
        """
        Reset intuition network state for system reset.

        Clears all learned intuitions and statistics.
        Note: The encoder model is NOT reset (expensive to reload).
        Called by server.py during reset_byrd().
        """
        self._intuitions.clear()
        self._total_observations = 0
        self._successful_predictions = 0

    def _encode(self, text: str) -> List[float]:
        """Encode text to embedding vector."""
        if self._has_embeddings and self._encoder:
            try:
                embedding = self._encoder.encode(text, convert_to_numpy=True)
                return embedding.tolist()
            except:
                pass

        # Fallback: simple bag-of-words hash
        words = set(text.lower().split())
        # Create a pseudo-embedding from word hashes
        embedding = [0.0] * 64
        for word in words:
            idx = hash(word) % 64
            embedding[idx] += 1.0
        # Normalize
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        return embedding

    def _similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Compute cosine similarity between embeddings."""
        if len(emb1) != len(emb2):
            return 0.0

        dot = sum(a * b for a, b in zip(emb1, emb2))
        mag1 = sum(a**2 for a in emb1) ** 0.5
        mag2 = sum(b**2 for b in emb2) ** 0.5

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (mag1 * mag2)

    async def record_outcome(self, situation: str, action: str, success: bool, delta: float = 0.0):
        """
        Record an action outcome to train intuition.

        BREAKING FALSE-POSITIVE LOOP: Only treats outcomes as successful if delta is meaningful.
        
        Args:
            situation: Context/situation description
            action: Action taken
            success: Whether the action succeeded (nominal claim)
            delta: Actual improvement delta (-1.0 to 1.0). Required for meaningful success.
        """
        # Override nominal success with delta-based determination
        MIN_MEANINGFUL_DELTA = 0.005  # 0.5% minimum improvement
        
        if success and delta < MIN_MEANINGFUL_DELTA:
            # False positive detected - claimed success but no meaningful delta
            success = False
            if delta > 0:
                print(f"   ⚠️  Intuition: FALSE POSITIVE for '{action}' - "
                      f"delta={delta:.4%} < {MIN_MEANINGFUL_DELTA:.1%}")
            elif delta == 0:
                print(f"   ⚠️  Intuition: NO DELTA for '{action}' - cannot confirm improvement")
        embedding = self._encode(situation)

        if action not in self._intuitions:
            self._intuitions[action] = []

        # Find similar existing intuition
        best_match = None
        best_similarity = 0.0

        for intuition in self._intuitions[action]:
            sim = self._similarity(embedding, intuition.context_embedding)
            if sim > best_similarity and sim > 0.8:
                best_similarity = sim
                best_match = intuition

        if best_match:
            # Update existing intuition
            old_rate = best_match.success_rate
            old_obs = best_match.observations
            new_obs = old_obs + 1

            # Exponential moving average
            alpha = 2.0 / (new_obs + 1)
            new_rate = (1 - alpha) * old_rate + alpha * (1.0 if success else 0.0)

            best_match.success_rate = new_rate
            best_match.observations = new_obs
            best_match.last_updated = datetime.now()
        else:
            # Create new intuition
            self._intuitions[action].append(Intuition(
                context_embedding=embedding,
                action=action,
                success_rate=1.0 if success else 0.0,
                observations=1
            ))

        self._total_observations += 1

        # Persist to memory periodically
        if self._total_observations % 50 == 0:
            await self._persist()

    async def score_action(self, situation: str, action: str) -> IntuitionScore:
        """
        Score an action for a given situation based on learned intuition.

        Args:
            situation: Current context/situation
            action: Proposed action

        Returns:
            IntuitionScore with predicted success probability
        """
        if action not in self._intuitions or not self._intuitions[action]:
            return IntuitionScore(
                action=action,
                score=0.5,  # No data = maximum uncertainty
                confidence=0.0,
                similar_experiences=0,
                reasoning="No intuition for this action"
            )

        embedding = self._encode(situation)

        # Find similar intuitions
        similarities = []
        for intuition in self._intuitions[action]:
            sim = self._similarity(embedding, intuition.context_embedding)
            if sim > 0.3:  # Minimum similarity threshold
                similarities.append((intuition, sim))

        if not similarities:
            return IntuitionScore(
                action=action,
                score=0.5,
                confidence=0.1,
                similar_experiences=0,
                reasoning="No similar contexts found"
            )

        # Weighted average by similarity
        total_weight = sum(sim for _, sim in similarities)
        weighted_score = sum(
            intuition.success_rate * sim
            for intuition, sim in similarities
        ) / total_weight

        # Confidence based on number of observations and similarity
        total_observations = sum(i.observations for i, _ in similarities)
        avg_similarity = total_weight / len(similarities)
        confidence = min(1.0, (total_observations / 20.0) * avg_similarity)

        return IntuitionScore(
            action=action,
            score=weighted_score,
            confidence=confidence,
            similar_experiences=len(similarities),
            reasoning=f"Based on {len(similarities)} similar contexts ({total_observations} observations)"
        )

    async def rank_actions(self, situation: str, actions: List[str]) -> List[IntuitionScore]:
        """
        Rank multiple actions for a situation.

        Args:
            situation: Current context
            actions: List of possible actions

        Returns:
            List of IntuitionScores sorted by score descending
        """
        scores = []
        for action in actions:
            score = await self.score_action(situation, action)
            scores.append(score)

        scores.sort(key=lambda s: s.score * s.confidence, reverse=True)
        return scores

    async def suggest_action(self, situation: str, available_actions: List[str] = None) -> Optional[str]:
        """
        Suggest the best action for a situation.

        Args:
            situation: Current context
            available_actions: Optional list of valid actions (if None, all known actions)

        Returns:
            Best action or None if no good suggestion
        """
        actions = available_actions or list(self._intuitions.keys())

        if not actions:
            return None

        scores = await self.rank_actions(situation, actions)

        # Only suggest if we have reasonable confidence
        if scores and scores[0].confidence > 0.3 and scores[0].score > 0.5:
            return scores[0].action

        return None

    async def evaluate_prediction(self, situation: str, action: str, actual_success: bool):
        """
        Evaluate a prediction and track accuracy.

        Call this after making a prediction and observing the outcome.
        """
        prediction = await self.score_action(situation, action)

        predicted_success = prediction.score > 0.5
        was_correct = (predicted_success == actual_success)

        if was_correct:
            self._successful_predictions += 1

        # Record outcome to improve future predictions
        await self.record_outcome(situation, action, actual_success)

    async def _persist(self):
        """Persist intuitions to memory."""
        if not self.memory:
            return

        try:
            # Serialize intuitions
            data = {}
            for action, intuitions in self._intuitions.items():
                data[action] = [
                    {
                        "embedding": i.context_embedding,
                        "success_rate": i.success_rate,
                        "observations": i.observations,
                        "last_updated": i.last_updated.isoformat()
                    }
                    for i in intuitions
                ]

            # Store in memory
            await self.memory._run_query("""
                MERGE (n:IntuitionNetwork {id: 'default'})
                SET n.data = $data,
                    n.total_observations = $total,
                    n.successful_predictions = $success,
                    n.updated_at = datetime()
            """, {
                "data": json.dumps(data),
                "total": self._total_observations,
                "success": self._successful_predictions
            })
        except Exception as e:
            print(f"IntuitionNetwork persist error: {e}")

    async def load(self):
        """Load intuitions from memory."""
        if not self.memory:
            return

        try:
            result = await self.memory._run_query("""
                MATCH (n:IntuitionNetwork {id: 'default'})
                RETURN n.data as data, n.total_observations as total,
                       n.successful_predictions as success
            """)

            if result and result[0].get("data"):
                data = json.loads(result[0]["data"])

                for action, intuitions in data.items():
                    self._intuitions[action] = [
                        Intuition(
                            context_embedding=i["embedding"],
                            action=action,
                            success_rate=i["success_rate"],
                            observations=i["observations"],
                            last_updated=datetime.fromisoformat(i["last_updated"])
                        )
                        for i in intuitions
                    ]

                self._total_observations = result[0].get("total", 0)
                self._successful_predictions = result[0].get("success", 0)

        except Exception as e:
            print(f"IntuitionNetwork load error: {e}")

    def get_accuracy(self) -> float:
        """Get prediction accuracy."""
        if self._total_observations == 0:
            return 0.5

        return self._successful_predictions / self._total_observations

    def get_statistics(self) -> Dict[str, Any]:
        """Get network statistics."""
        return {
            "total_observations": self._total_observations,
            "successful_predictions": self._successful_predictions,
            "accuracy": self.get_accuracy(),
            "actions_known": len(self._intuitions),
            "total_intuitions": sum(len(i) for i in self._intuitions.values()),
            "has_embeddings": self._has_embeddings
        }

    def get_known_actions(self) -> List[str]:
        """Get list of actions with learned intuitions."""
        return list(self._intuitions.keys())

    def get_action_statistics(self, action: str) -> Optional[Dict]:
        """Get statistics for a specific action."""
        if action not in self._intuitions:
            return None

        intuitions = self._intuitions[action]
        total_observations = sum(i.observations for i in intuitions)
        avg_success_rate = sum(i.success_rate * i.observations for i in intuitions) / total_observations if total_observations > 0 else 0

        return {
            "contexts": len(intuitions),
            "total_observations": total_observations,
            "avg_success_rate": avg_success_rate
        }

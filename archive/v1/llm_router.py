"""
LLM Router - Routes tasks to appropriate LLM based on task type.

Routing Rules:
- REASONING tasks → Z.AI GLM-4.7 (cheap, fast)
- EXECUTION tasks → Claude Agent SDK (tool access)

Part of BYRD's Hybrid LLM Architecture.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Task types for routing decisions."""

    # Z.AI tasks (reasoning - cheap)
    REFLECTION = "reflection"
    PATTERN_DETECTION = "pattern_detection"
    STRATEGY_DETERMINATION = "strategy_determination"
    SATISFACTION_EVALUATION = "satisfaction_evaluation"
    CONTEXT_SUMMARIZATION = "context_summarization"
    DESIRE_CLASSIFICATION = "desire_classification"
    INNER_VOICE = "inner_voice"
    BELIEF_FORMATION = "belief_formation"

    # Claude SDK tasks (execution - tool access)
    CODE_GENERATION = "code_generation"
    CODE_EDITING = "code_editing"
    FILE_OPERATIONS = "file_operations"
    BASH_EXECUTION = "bash_execution"
    CODEBASE_SEARCH = "codebase_search"
    WEB_RESEARCH = "web_research"
    SELF_MODIFICATION = "self_modification"


class LLMProvider(Enum):
    """Available LLM providers."""
    ZAI = "zai"
    CLAUDE_SDK = "claude_sdk"


@dataclass
class RoutingDecision:
    """Result of a routing decision."""
    provider: LLMProvider
    reason: str
    estimated_tokens: int
    requires_tools: bool
    task_type: Optional[TaskType] = None


class LLMRouter:
    """
    Routes tasks to the appropriate LLM provider.

    Strategy:
    - Z.AI GLM-4.7 for reasoning (reflection, planning, evaluation)
    - Claude Agent SDK for execution (file ops, bash, search)
    """

    # Task type to provider mapping
    ROUTING_TABLE = {
        # Z.AI tasks (cheap reasoning)
        TaskType.REFLECTION: LLMProvider.ZAI,
        TaskType.PATTERN_DETECTION: LLMProvider.ZAI,
        TaskType.STRATEGY_DETERMINATION: LLMProvider.ZAI,
        TaskType.SATISFACTION_EVALUATION: LLMProvider.ZAI,
        TaskType.CONTEXT_SUMMARIZATION: LLMProvider.ZAI,
        TaskType.DESIRE_CLASSIFICATION: LLMProvider.ZAI,
        TaskType.INNER_VOICE: LLMProvider.ZAI,
        TaskType.BELIEF_FORMATION: LLMProvider.ZAI,

        # Claude SDK tasks (tool execution)
        TaskType.CODE_GENERATION: LLMProvider.CLAUDE_SDK,
        TaskType.CODE_EDITING: LLMProvider.CLAUDE_SDK,
        TaskType.FILE_OPERATIONS: LLMProvider.CLAUDE_SDK,
        TaskType.BASH_EXECUTION: LLMProvider.CLAUDE_SDK,
        TaskType.CODEBASE_SEARCH: LLMProvider.CLAUDE_SDK,
        TaskType.WEB_RESEARCH: LLMProvider.CLAUDE_SDK,
        TaskType.SELF_MODIFICATION: LLMProvider.CLAUDE_SDK,
    }

    # Keywords that indicate tool requirements
    TOOL_KEYWORDS = [
        "edit", "modify", "change", "update", "fix", "create file",
        "write to", "run", "execute", "test", "build", "install",
        "search code", "find files", "grep", "read file", "delete",
        "refactor", "implement", "add function", "remove", "rename",
    ]

    # Keywords that indicate reasoning (no tools needed)
    REASONING_KEYWORDS = [
        "think", "reflect", "analyze", "understand", "consider",
        "evaluate", "assess", "plan", "decide", "summarize",
        "what do you think", "how do you feel", "describe",
    ]

    # Token estimates per task type
    TOKEN_ESTIMATES = {
        TaskType.REFLECTION: 3000,
        TaskType.PATTERN_DETECTION: 1000,
        TaskType.STRATEGY_DETERMINATION: 500,
        TaskType.SATISFACTION_EVALUATION: 800,
        TaskType.CONTEXT_SUMMARIZATION: 1500,
        TaskType.DESIRE_CLASSIFICATION: 500,
        TaskType.INNER_VOICE: 1000,
        TaskType.BELIEF_FORMATION: 800,
        TaskType.CODE_GENERATION: 4000,
        TaskType.CODE_EDITING: 3000,
        TaskType.FILE_OPERATIONS: 1000,
        TaskType.BASH_EXECUTION: 500,
        TaskType.CODEBASE_SEARCH: 1500,
        TaskType.WEB_RESEARCH: 2000,
        TaskType.SELF_MODIFICATION: 5000,
    }

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._routing_stats = {p.value: 0 for p in LLMProvider}
        self._task_type_stats = {t.value: 0 for t in TaskType}

        # Allow config overrides for routing
        self._force_zai = self.config.get("force_zai_for", [])
        self._force_claude = self.config.get("force_claude_for", [])

        logger.info("[LLMRouter] Initialized")

    def route(self, task_type: TaskType) -> RoutingDecision:
        """
        Route a task based on its type.

        Args:
            task_type: The type of task to route

        Returns:
            RoutingDecision with provider and metadata
        """
        # Check config overrides
        if task_type.value in self._force_zai:
            provider = LLMProvider.ZAI
            reason = f"Config override: {task_type.value} forced to Z.AI"
        elif task_type.value in self._force_claude:
            provider = LLMProvider.CLAUDE_SDK
            reason = f"Config override: {task_type.value} forced to Claude SDK"
        else:
            provider = self.ROUTING_TABLE.get(task_type, LLMProvider.ZAI)
            reason = f"Task type {task_type.value} routes to {provider.value}"

        requires_tools = provider == LLMProvider.CLAUDE_SDK

        # Update stats
        self._routing_stats[provider.value] += 1
        self._task_type_stats[task_type.value] += 1

        decision = RoutingDecision(
            provider=provider,
            reason=reason,
            estimated_tokens=self._estimate_tokens(task_type),
            requires_tools=requires_tools,
            task_type=task_type,
        )

        logger.debug(f"[LLMRouter] {task_type.value} -> {provider.value}")
        return decision

    def route_by_content(self, content: str) -> RoutingDecision:
        """
        Route based on content analysis when task type is unknown.

        Args:
            content: The task description or prompt

        Returns:
            RoutingDecision based on content analysis
        """
        content_lower = content.lower()

        # Check for reasoning keywords first (prefer cheap Z.AI)
        for keyword in self.REASONING_KEYWORDS:
            if keyword in content_lower:
                return RoutingDecision(
                    provider=LLMProvider.ZAI,
                    reason=f"Content contains reasoning keyword: '{keyword}'",
                    estimated_tokens=1500,
                    requires_tools=False,
                )

        # Check for tool keywords
        for keyword in self.TOOL_KEYWORDS:
            if keyword in content_lower:
                self._routing_stats[LLMProvider.CLAUDE_SDK.value] += 1
                return RoutingDecision(
                    provider=LLMProvider.CLAUDE_SDK,
                    reason=f"Content contains tool keyword: '{keyword}'",
                    estimated_tokens=3000,
                    requires_tools=True,
                )

        # Default to Z.AI for reasoning (cost optimization)
        self._routing_stats[LLMProvider.ZAI.value] += 1
        return RoutingDecision(
            provider=LLMProvider.ZAI,
            reason="No tool keywords detected, using Z.AI for reasoning",
            estimated_tokens=1000,
            requires_tools=False,
        )

    def _estimate_tokens(self, task_type: TaskType) -> int:
        """Estimate token usage for a task type."""
        return self.TOKEN_ESTIMATES.get(task_type, 1000)

    def should_use_claude(self, task_description: str) -> bool:
        """
        Quick check if a task should use Claude SDK.

        Args:
            task_description: Description of the task

        Returns:
            True if Claude SDK should be used
        """
        decision = self.route_by_content(task_description)
        return decision.provider == LLMProvider.CLAUDE_SDK

    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        total = sum(self._routing_stats.values())
        zai_count = self._routing_stats.get("zai", 0)
        claude_count = self._routing_stats.get("claude_sdk", 0)

        return {
            "total_routed": total,
            "by_provider": dict(self._routing_stats),
            "by_task_type": {k: v for k, v in self._task_type_stats.items() if v > 0},
            "zai_percentage": (zai_count / total * 100) if total > 0 else 0,
            "claude_percentage": (claude_count / total * 100) if total > 0 else 0,
            "cost_optimization": f"{zai_count}/{total} tasks used cheap Z.AI" if total > 0 else "N/A",
        }

    def reset(self):
        """Reset routing statistics."""
        self._routing_stats = {p.value: 0 for p in LLMProvider}
        self._task_type_stats = {t.value: 0 for t in TaskType}
        logger.info("[LLMRouter] Stats reset")

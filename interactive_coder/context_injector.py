"""
context_injector.py - Context Building for Interactive Coding

Builds layered context for each turn:
1. Desire Context (always)
2. Session History (after turn 1)
3. Memory Context (on demand)
4. Error Context (on error)
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class ContextInjector:
    """
    Builds context for coding turns.

    Context is layered based on the current state of the session:
    - Layer 1: Desire (always present)
    - Layer 2: Session history (accumulates)
    - Layer 3: Memory (related experiences, beliefs)
    - Layer 4: Error (when recovering)
    """

    def __init__(self, memory=None, context_loader=None):
        """
        Initialize the context injector.

        Args:
            memory: Memory instance for fetching related context
            context_loader: ContextLoader for tiered loading
        """
        self.memory = memory
        self.context_loader = context_loader

    async def build_initial_context(self, desire: Dict) -> Dict[str, Any]:
        """
        Build context for the first turn.

        Args:
            desire: The desire being fulfilled

        Returns:
            Context dictionary
        """
        context = {
            "desire": self._format_desire(desire),
            "files": [],
            "history": "",
            "memory": "",
            "instructions": self._get_initial_instructions(),
        }

        # Add memory context if available
        if self.memory:
            memory_context = await self._get_memory_context(desire)
            if memory_context:
                context["memory"] = memory_context

        return context

    def build_turn_context(
        self,
        desire: Dict,
        previous_turns: List[Dict],
        gaps: List[str],
        current_files: List[str],
        pending_todos: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Build context for subsequent turns.

        Args:
            desire: The desire being fulfilled
            previous_turns: Summary of previous turns
            gaps: Identified gaps from evaluation
            current_files: Files modified so far
            pending_todos: Pending TODO items

        Returns:
            Context dictionary
        """
        context = {
            "desire": self._format_desire(desire),
            "files": current_files,
            "history": self._format_history(previous_turns),
            "gaps": gaps,
            "instructions": self._get_refinement_instructions(gaps),
        }

        if pending_todos:
            context["pending_todos"] = pending_todos

        return context

    def build_error_context(
        self,
        desire: Dict,
        error_type: str,
        error_message: str,
        recovery_strategy: str,
        previous_output: str = "",
    ) -> Dict[str, Any]:
        """
        Build context for error recovery turn.

        Args:
            desire: The desire being fulfilled
            error_type: Type of error that occurred
            error_message: The error message
            recovery_strategy: Strategy being used for recovery
            previous_output: Output from failed turn

        Returns:
            Context dictionary
        """
        return {
            "desire": self._format_desire(desire),
            "error": {
                "type": error_type,
                "message": error_message,
                "strategy": recovery_strategy,
            },
            "previous_output": previous_output[:1000] if previous_output else "",
            "instructions": self._get_recovery_instructions(error_type, recovery_strategy),
        }

    def format_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format context dictionary as a prompt string.

        Args:
            context: Context dictionary

        Returns:
            Formatted string for prompt
        """
        parts = []

        # Desire (always present)
        if "desire" in context:
            parts.append(f"# DESIRE\n{context['desire']}")

        # Memory context
        if context.get("memory"):
            parts.append(f"# RELEVANT CONTEXT\n{context['memory']}")

        # Session history
        if context.get("history"):
            parts.append(f"# SESSION HISTORY\n{context['history']}")

        # Files modified
        if context.get("files"):
            files_str = ", ".join(context["files"])
            parts.append(f"# FILES MODIFIED\n{files_str}")

        # Gaps to address
        if context.get("gaps"):
            gaps_str = "\n".join(f"- {g}" for g in context["gaps"])
            parts.append(f"# GAPS TO ADDRESS\n{gaps_str}")

        # Pending TODOs
        if context.get("pending_todos"):
            todos_str = "\n".join(f"- {t}" for t in context["pending_todos"][:5])
            parts.append(f"# PENDING TODOS\n{todos_str}")

        # Error context
        if context.get("error"):
            error = context["error"]
            parts.append(f"""# ERROR RECOVERY
Error Type: {error['type']}
Error: {error['message']}
Strategy: {error['strategy']}""")

        # Previous output (for error recovery)
        if context.get("previous_output"):
            parts.append(f"# PREVIOUS OUTPUT\n{context['previous_output']}")

        # Instructions
        if context.get("instructions"):
            parts.append(f"# INSTRUCTIONS\n{context['instructions']}")

        return "\n\n".join(parts)

    def _format_desire(self, desire: Dict) -> str:
        """Format desire for context."""
        desc = desire.get("description", "Unknown desire")
        intensity = desire.get("intensity", 0.5)
        desire_type = desire.get("type", "unknown")

        return f"""Description: {desc}
Type: {desire_type}
Intensity: {intensity:.2f}"""

    def _format_history(self, previous_turns: List[Dict]) -> str:
        """Format previous turns for context."""
        if not previous_turns:
            return ""

        history_parts = []
        for turn in previous_turns[-5:]:  # Last 5 turns
            turn_num = turn.get("turn_number", "?")
            success = "SUCCESS" if turn.get("success") else "FAILED"
            files = turn.get("files", [])
            output_preview = turn.get("output", "")[:200]

            history_parts.append(f"""Turn {turn_num} [{success}]:
Files: {', '.join(files) if files else 'None'}
Output: {output_preview}...""")

        return "\n\n".join(history_parts)

    def _get_initial_instructions(self) -> str:
        """Get instructions for first turn."""
        return """Complete this task thoroughly.
- Read and understand any existing code before modifying
- Create or modify files as needed
- Run tests if applicable
- Report any issues or blockers"""

    def _get_refinement_instructions(self, gaps: List[str]) -> str:
        """Get instructions for refinement turns."""
        if gaps:
            gap_list = "\n".join(f"- {g}" for g in gaps[:3])
            return f"""Address these gaps from the previous turn:
{gap_list}

Focus on completing the remaining work.
Verify each gap is addressed before finishing."""
        else:
            return """Continue the work from the previous turn.
Review what was done and complete any remaining items."""

    def _get_recovery_instructions(self, error_type: str, strategy: str) -> str:
        """Get instructions for error recovery."""
        instructions = {
            "simplify_task": "Break the task into smaller steps. Complete the most essential part first.",
            "wait_and_retry": "Try the same approach again.",
            "fix_syntax": "Carefully review and fix the syntax error. Test after fixing.",
            "install_dependency": "Install the missing dependency first, then continue.",
            "verify_path": "List files to verify the correct path, then use the right path.",
            "explain_constraint": "This task cannot proceed due to constraints.",
            "fallback_subprocess": "Use simpler shell commands instead of CLI features.",
            "check_permissions": "Check and fix file permissions, or use a different location.",
            "retry_network": "Retry the network operation.",
            "retry_generic": "Try a different approach to accomplish the task.",
        }
        return instructions.get(strategy, "Retry the task with more care.")

    async def _get_memory_context(self, desire: Dict) -> str:
        """Fetch related context from memory."""
        if not self.memory:
            return ""

        try:
            desc = desire.get("description", "")
            context_parts = []

            # Get related beliefs
            beliefs = await self.memory.get_beliefs(limit=3)
            if beliefs:
                belief_texts = [b.get("content", "")[:100] for b in beliefs[:3]]
                context_parts.append("Related beliefs:\n" + "\n".join(f"- {b}" for b in belief_texts))

            # Get related capabilities
            capabilities = await self.memory.get_capabilities(limit=3)
            if capabilities:
                cap_names = [c.get("name", "") for c in capabilities[:3]]
                context_parts.append("Available capabilities: " + ", ".join(cap_names))

            return "\n\n".join(context_parts)

        except Exception as e:
            logger.warning(f"Error fetching memory context: {e}")
            return ""

    def reset(self):
        """Reset injector state (stateless, nothing to reset)."""
        pass

"""
todo_continuation.py - TODO Extraction and Completion

Extracts TODOs, FIXMEs, and remaining work items from coder output
and queues them for completion in subsequent turns.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


# TODO detection patterns
TODO_PATTERNS = [
    # Standard TODO/FIXME comments
    (r"(?:^|\s)TODO:?\s*(.+?)(?:\n|$)", 1),
    (r"(?:^|\s)FIXME:?\s*(.+?)(?:\n|$)", 1),
    (r"(?:^|\s)XXX:?\s*(.+?)(?:\n|$)", 2),
    (r"(?:^|\s)HACK:?\s*(.+?)(?:\n|$)", 2),

    # Markdown checkboxes (unchecked)
    (r"^-\s*\[\s*\]\s*(.+?)$", 1),
    (r"^\*\s*\[\s*\]\s*(.+?)$", 1),

    # "Next steps" sections
    (r"(?:next\s*steps?|remaining\s*work|still\s*need\s*to):\s*\n((?:[-*]\s*.+\n?)+)", 1),

    # Inline notes about incomplete work
    (r"(?:need\s+to|should|must)\s+(.+?)(?:\.|$)", 3),
    (r"not\s+(?:yet|implemented|complete)[:\s]+(.+?)(?:\.|$)", 2),
]

# Priority keywords
HIGH_PRIORITY_KEYWORDS = ["critical", "urgent", "important", "asap", "now", "first"]
LOW_PRIORITY_KEYWORDS = ["later", "eventually", "nice to have", "optional", "maybe"]


@dataclass
class ExtractedTodo:
    """A TODO extracted from output."""
    content: str
    priority: int = 2  # 1=high, 2=medium, 3=low
    source_turn: int = 0
    source_line: Optional[str] = None
    completed: bool = False
    completed_turn: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "content": self.content,
            "priority": self.priority,
            "source_turn": self.source_turn,
            "completed": self.completed,
            "completed_turn": self.completed_turn,
        }


class TodoContinuation:
    """
    Extracts and manages TODOs from coder output.

    Enables the Ralph Loop to continue until all TODOs are completed.
    """

    def __init__(self, llm_client=None):
        """
        Initialize the TODO handler.

        Args:
            llm_client: LLM client for prioritization
        """
        self.llm_client = llm_client
        self._pending_todos: List[ExtractedTodo] = []
        self._completed_todos: List[ExtractedTodo] = []
        self._extraction_count = 0

    def extract_todos(self, output: str, turn_number: int) -> List[ExtractedTodo]:
        """
        Extract TODOs from coder output.

        Args:
            output: The coder output text
            turn_number: Current turn number

        Returns:
            List of extracted TODOs
        """
        self._extraction_count += 1
        todos = []
        seen_content = set()

        for pattern, base_priority in TODO_PATTERNS:
            matches = re.finditer(pattern, output, re.MULTILINE | re.IGNORECASE)

            for match in matches:
                content = match.group(1).strip()

                # Handle multi-line captures (next steps lists)
                if "\n" in content:
                    lines = [
                        line.strip().lstrip("-*").strip()
                        for line in content.split("\n")
                        if line.strip()
                    ]
                    for line in lines:
                        if line and line not in seen_content:
                            priority = self._determine_priority(line, base_priority)
                            todos.append(ExtractedTodo(
                                content=line,
                                priority=priority,
                                source_turn=turn_number,
                                source_line=line[:50],
                            ))
                            seen_content.add(line)
                else:
                    # Single item
                    if content and content not in seen_content:
                        priority = self._determine_priority(content, base_priority)
                        todos.append(ExtractedTodo(
                            content=content,
                            priority=priority,
                            source_turn=turn_number,
                            source_line=content[:50],
                        ))
                        seen_content.add(content)

        # Add to pending queue
        self._pending_todos.extend(todos)

        if todos:
            logger.info(f"Extracted {len(todos)} TODOs from turn {turn_number}")

        return todos

    def _determine_priority(self, content: str, base_priority: int) -> int:
        """Determine priority based on content keywords."""
        content_lower = content.lower()

        # Check for high priority keywords
        for keyword in HIGH_PRIORITY_KEYWORDS:
            if keyword in content_lower:
                return 1

        # Check for low priority keywords
        for keyword in LOW_PRIORITY_KEYWORDS:
            if keyword in content_lower:
                return 3

        return base_priority

    async def prioritize_todos(
        self,
        todos: List[ExtractedTodo],
        desire: Dict,
    ) -> List[ExtractedTodo]:
        """
        Use LLM to prioritize TODOs by relevance to desire.

        Args:
            todos: TODOs to prioritize
            desire: The desire being fulfilled

        Returns:
            Sorted list of TODOs (highest priority first)
        """
        if not self.llm_client or not todos:
            # Fall back to simple priority sort
            return sorted(todos, key=lambda t: t.priority)

        try:
            # Format TODOs for LLM
            todo_list = "\n".join(
                f"{i+1}. {t.content}" for i, t in enumerate(todos)
            )

            prompt = f"""Given this desire: "{desire.get('description', 'Unknown')}"

Which TODOs are most important to complete? Rank by relevance.

TODOs:
{todo_list}

Respond with just the numbers in priority order, highest first.
Example: 3, 1, 2"""

            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.1,
                max_tokens=100,
            )

            text = response.text if hasattr(response, "text") else str(response)

            # Parse priority order
            numbers = re.findall(r"\d+", text)
            priority_order = [int(n) for n in numbers if 1 <= int(n) <= len(todos)]

            # Reorder todos based on LLM response
            if priority_order:
                ordered = []
                seen = set()
                for num in priority_order:
                    idx = num - 1
                    if idx < len(todos) and idx not in seen:
                        todos[idx].priority = len(ordered) + 1
                        ordered.append(todos[idx])
                        seen.add(idx)

                # Add any remaining todos
                for i, todo in enumerate(todos):
                    if i not in seen:
                        ordered.append(todo)

                return ordered

        except Exception as e:
            logger.warning(f"LLM prioritization failed: {e}")

        # Fallback sort
        return sorted(todos, key=lambda t: t.priority)

    def get_next_todo(self) -> Optional[ExtractedTodo]:
        """
        Get the highest priority pending TODO.

        Returns:
            Next TODO to complete, or None if queue is empty
        """
        if not self._pending_todos:
            return None

        # Sort by priority and return first
        self._pending_todos.sort(key=lambda t: t.priority)
        return self._pending_todos[0]

    def mark_completed(self, todo: ExtractedTodo, turn_number: int):
        """
        Mark a TODO as completed.

        Args:
            todo: The TODO to mark complete
            turn_number: Turn in which it was completed
        """
        if todo in self._pending_todos:
            self._pending_todos.remove(todo)

        todo.completed = True
        todo.completed_turn = turn_number
        self._completed_todos.append(todo)

        logger.debug(f"Completed TODO: {todo.content[:50]}")

    def mark_current_completed(self, turn_number: int):
        """Mark the current (first) pending TODO as completed."""
        if self._pending_todos:
            self.mark_completed(self._pending_todos[0], turn_number)

    def has_pending_todos(self) -> bool:
        """Check if there are uncompleted TODOs."""
        return len(self._pending_todos) > 0

    def get_pending_count(self) -> int:
        """Get count of pending TODOs."""
        return len(self._pending_todos)

    def get_pending_todos(self) -> List[ExtractedTodo]:
        """Get all pending TODOs."""
        return self._pending_todos.copy()

    def get_completed_todos(self) -> List[ExtractedTodo]:
        """Get all completed TODOs."""
        return self._completed_todos.copy()

    def get_todo_summary(self) -> str:
        """Get a summary of pending TODOs for context."""
        if not self._pending_todos:
            return ""

        summary = "REMAINING TODOS:\n"
        for i, todo in enumerate(self._pending_todos[:5], 1):  # Top 5
            summary += f"{i}. {todo.content}\n"

        if len(self._pending_todos) > 5:
            summary += f"... and {len(self._pending_todos) - 5} more\n"

        return summary

    def clear_pending(self):
        """Clear all pending TODOs."""
        self._pending_todos = []

    def reset(self):
        """Reset all TODO state."""
        self._pending_todos = []
        self._completed_todos = []
        self._extraction_count = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get TODO statistics."""
        return {
            "pending_count": len(self._pending_todos),
            "completed_count": len(self._completed_todos),
            "extraction_count": self._extraction_count,
            "total_processed": len(self._pending_todos) + len(self._completed_todos),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "pending": [t.to_dict() for t in self._pending_todos],
            "completed": [t.to_dict() for t in self._completed_todos],
            "stats": self.get_stats(),
        }

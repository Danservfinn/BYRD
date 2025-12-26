"""
Agent Coder - Multi-Turn Tool-Using Code Generation Agent for BYRD

This module implements a sophisticated coding agent that can:
1. Reason through complex coding tasks
2. Use tools to explore the codebase
3. Make incremental, validated changes
4. Verify its work through iteration

Architecture:
    Desire -> Agent Loop -> [Reason -> Tool Use -> Observe]* -> Result

The agent maintains a conversation history and can make multiple tool calls
to understand and modify the codebase, similar to how a human developer
would approach a coding task.

Tools Available:
    - read_file: Read file contents
    - write_file: Create or overwrite a file
    - edit_file: Make targeted edits to a file
    - list_files: List directory contents
    - search_code: Search for patterns in codebase
    - get_file_info: Get file metadata
    - finish: Complete the task

Safety:
    - All write operations validated against constitutional constraints
    - Protected files cannot be modified
    - Dangerous patterns are blocked
    - Maximum steps prevent runaway execution
    - All changes tracked with provenance
"""

import os
import re
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

from constitutional import ConstitutionalConstraints
from event_bus import event_bus, Event, EventType


# =============================================================================
# TOOL DEFINITIONS
# =============================================================================

@dataclass
class Tool:
    """Definition of a tool the agent can use."""
    name: str
    description: str
    parameters: Dict[str, str]  # param_name -> description
    required: List[str]  # required parameters


@dataclass
class ToolResult:
    """Result of a tool execution."""
    success: bool
    output: str
    error: Optional[str] = None


@dataclass
class AgentMessage:
    """A message in the agent's conversation history."""
    role: str  # "system", "user", "assistant", "tool"
    content: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict] = None
    tool_result: Optional[str] = None


@dataclass
class AgentState:
    """Current state of the agent."""
    desire: Dict
    history: List[AgentMessage] = field(default_factory=list)
    steps: int = 0
    files_modified: List[str] = field(default_factory=list)
    completed: bool = False
    success: bool = False
    final_message: str = ""


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

class AgentTools:
    """
    Tool implementations for the coding agent.

    Each tool is a method that takes arguments and returns a ToolResult.
    All file operations are validated against constitutional constraints.
    """

    def __init__(self, constitutional: ConstitutionalConstraints, base_path: str = "."):
        self.constitutional = constitutional
        self.base_path = Path(base_path)
        self.files_modified: List[str] = []

    def _resolve_path(self, filepath: str) -> Path:
        """Resolve a filepath relative to base path."""
        path = Path(filepath)
        if not path.is_absolute():
            path = self.base_path / path
        return path

    def _is_safe_path(self, filepath: str) -> bool:
        """Check if path is within allowed boundaries."""
        try:
            resolved = self._resolve_path(filepath).resolve()
            base_resolved = self.base_path.resolve()
            return str(resolved).startswith(str(base_resolved))
        except Exception:
            return False

    async def read_file(self, filepath: str, start_line: int = None, end_line: int = None) -> ToolResult:
        """
        Read contents of a file.

        Args:
            filepath: Path to the file to read
            start_line: Optional starting line number (1-indexed)
            end_line: Optional ending line number (1-indexed)
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return ToolResult(False, "", f"File not found: {filepath}")

            if not path.is_file():
                return ToolResult(False, "", f"Not a file: {filepath}")

            content = path.read_text()
            lines = content.split('\n')

            # Apply line range if specified
            if start_line is not None or end_line is not None:
                start = (start_line or 1) - 1  # Convert to 0-indexed
                end = end_line or len(lines)
                lines = lines[start:end]
                content = '\n'.join(lines)
                line_info = f" (lines {start_line or 1}-{end_line or len(lines)})"
            else:
                line_info = f" ({len(lines)} lines)"

            # Truncate very large files
            if len(content) > 10000:
                content = content[:10000] + f"\n\n... [TRUNCATED - file has {len(lines)} total lines]"

            return ToolResult(True, f"=== {filepath}{line_info} ===\n{content}")

        except Exception as e:
            return ToolResult(False, "", f"Error reading {filepath}: {e}")

    async def write_file(self, filepath: str, content: str) -> ToolResult:
        """
        Create or overwrite a file with new content.

        Args:
            filepath: Path to the file to write
            content: Complete content to write
        """
        try:
            # Validate against constitutional constraints
            if not self.constitutional.is_modifiable(filepath):
                return ToolResult(False, "", f"BLOCKED: Cannot modify protected file: {filepath}")

            if self._has_dangerous_pattern(content):
                return ToolResult(False, "", "BLOCKED: Content contains dangerous patterns")

            if not self._is_safe_path(filepath):
                return ToolResult(False, "", f"BLOCKED: Path outside allowed directory: {filepath}")

            path = self._resolve_path(filepath)

            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write the file
            path.write_text(content)

            self.files_modified.append(str(path))

            return ToolResult(True, f"Successfully wrote {len(content)} characters to {filepath}")

        except Exception as e:
            return ToolResult(False, "", f"Error writing {filepath}: {e}")

    async def edit_file(self, filepath: str, old_content: str, new_content: str) -> ToolResult:
        """
        Edit a specific part of a file by replacing old content with new content.

        Args:
            filepath: Path to the file to edit
            old_content: Exact content to find and replace
            new_content: Content to replace it with
        """
        try:
            # Validate against constitutional constraints
            if not self.constitutional.is_modifiable(filepath):
                return ToolResult(False, "", f"BLOCKED: Cannot modify protected file: {filepath}")

            if self._has_dangerous_pattern(new_content):
                return ToolResult(False, "", "BLOCKED: New content contains dangerous patterns")

            path = self._resolve_path(filepath)

            if not path.exists():
                return ToolResult(False, "", f"File not found: {filepath}")

            current = path.read_text()

            if old_content not in current:
                # Provide helpful context
                return ToolResult(
                    False, "",
                    f"Old content not found in {filepath}. "
                    f"File has {len(current)} chars, {len(current.splitlines())} lines. "
                    f"Searched for {len(old_content)} chars starting with: {old_content[:100]}..."
                )

            # Count occurrences
            count = current.count(old_content)
            if count > 1:
                return ToolResult(
                    False, "",
                    f"Found {count} occurrences of old_content. Please provide more context to make it unique."
                )

            # Apply the edit
            updated = current.replace(old_content, new_content, 1)
            path.write_text(updated)

            self.files_modified.append(str(path))

            return ToolResult(
                True,
                f"Successfully edited {filepath}. Replaced {len(old_content)} chars with {len(new_content)} chars."
            )

        except Exception as e:
            return ToolResult(False, "", f"Error editing {filepath}: {e}")

    async def list_files(self, directory: str = ".", pattern: str = None) -> ToolResult:
        """
        List files in a directory.

        Args:
            directory: Directory to list
            pattern: Optional glob pattern (e.g., "*.py")
        """
        try:
            path = self._resolve_path(directory)

            if not path.exists():
                return ToolResult(False, "", f"Directory not found: {directory}")

            if not path.is_dir():
                return ToolResult(False, "", f"Not a directory: {directory}")

            if pattern:
                files = list(path.glob(pattern))
            else:
                files = list(path.iterdir())

            # Sort and format
            files.sort()
            output_lines = []
            for f in files[:100]:  # Limit to 100 entries
                rel_path = f.relative_to(path)
                if f.is_dir():
                    output_lines.append(f"  [DIR]  {rel_path}/")
                else:
                    size = f.stat().st_size
                    output_lines.append(f"  [FILE] {rel_path} ({size} bytes)")

            output = f"Contents of {directory}:\n" + "\n".join(output_lines)
            if len(files) > 100:
                output += f"\n... and {len(files) - 100} more entries"

            return ToolResult(True, output)

        except Exception as e:
            return ToolResult(False, "", f"Error listing {directory}: {e}")

    async def search_code(self, pattern: str, file_pattern: str = "*.py", max_results: int = 20) -> ToolResult:
        """
        Search for a pattern in code files.

        Args:
            pattern: Regex pattern to search for
            file_pattern: Glob pattern for files to search (default: *.py)
            max_results: Maximum results to return
        """
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            results = []

            for filepath in self.base_path.glob(f"**/{file_pattern}"):
                if not filepath.is_file():
                    continue

                try:
                    content = filepath.read_text()
                    lines = content.split('\n')

                    for i, line in enumerate(lines, 1):
                        if regex.search(line):
                            rel_path = filepath.relative_to(self.base_path)
                            results.append(f"{rel_path}:{i}: {line.strip()[:100]}")

                            if len(results) >= max_results:
                                break

                except Exception:
                    continue

                if len(results) >= max_results:
                    break

            if results:
                output = f"Found {len(results)} matches for '{pattern}':\n" + "\n".join(results)
            else:
                output = f"No matches found for '{pattern}' in {file_pattern} files"

            return ToolResult(True, output)

        except re.error as e:
            return ToolResult(False, "", f"Invalid regex pattern: {e}")
        except Exception as e:
            return ToolResult(False, "", f"Error searching: {e}")

    async def get_file_info(self, filepath: str) -> ToolResult:
        """
        Get metadata about a file.

        Args:
            filepath: Path to the file
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return ToolResult(False, "", f"File not found: {filepath}")

            stat = path.stat()
            content = path.read_text() if path.is_file() else ""

            info = {
                "path": str(path),
                "exists": True,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_modifiable": self.constitutional.is_modifiable(filepath),
            }

            if path.is_file():
                info["line_count"] = len(content.splitlines())
                info["char_count"] = len(content)

            return ToolResult(True, json.dumps(info, indent=2))

        except Exception as e:
            return ToolResult(False, "", f"Error getting info for {filepath}: {e}")

    def _has_dangerous_pattern(self, content: str) -> bool:
        """Check for dangerous code patterns."""
        dangerous_patterns = [
            r'\bos\.system\s*\(',
            r'\bsubprocess\.',
            r'\beval\s*\(',
            r'\bexec\s*\(',
            r'\b__import__\s*\(',
            r'\bopen\s*\([^)]*["\']w["\']',  # open with write mode
            r'\bshutil\.rmtree\s*\(',
            r'rm\s+-rf\s+',
            r'\bglobals\s*\(\)',
            r'\blocals\s*\(\)',
            r'\bcompile\s*\(',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, content):
                return True
        return False


# =============================================================================
# AGENT CODER
# =============================================================================

class AgentCoder:
    """
    Multi-turn tool-using coding agent for BYRD.

    This agent can reason through complex coding tasks by:
    1. Analyzing the desire/task
    2. Using tools to explore the codebase
    3. Making incremental changes
    4. Verifying its work

    The agent maintains a conversation history and can make multiple
    tool calls before completing the task.
    """

    # Tool definitions for the agent
    TOOLS = [
        Tool(
            name="read_file",
            description="Read the contents of a file. Use this to understand existing code before making changes.",
            parameters={
                "filepath": "Path to the file to read",
                "start_line": "(Optional) Starting line number to read from",
                "end_line": "(Optional) Ending line number to read to"
            },
            required=["filepath"]
        ),
        Tool(
            name="write_file",
            description="Create a new file or completely overwrite an existing file. Use for creating new files.",
            parameters={
                "filepath": "Path to the file to write",
                "content": "Complete content to write to the file"
            },
            required=["filepath", "content"]
        ),
        Tool(
            name="edit_file",
            description="Edit a specific part of an existing file. Finds exact old_content and replaces with new_content. More precise than write_file for modifications.",
            parameters={
                "filepath": "Path to the file to edit",
                "old_content": "Exact content to find (must be unique in file)",
                "new_content": "Content to replace it with"
            },
            required=["filepath", "old_content", "new_content"]
        ),
        Tool(
            name="list_files",
            description="List files in a directory. Use to explore the codebase structure.",
            parameters={
                "directory": "Directory to list (default: current directory)",
                "pattern": "(Optional) Glob pattern like '*.py' to filter files"
            },
            required=[]
        ),
        Tool(
            name="search_code",
            description="Search for a pattern in code files. Use regex patterns.",
            parameters={
                "pattern": "Regex pattern to search for",
                "file_pattern": "(Optional) Glob pattern for files, default '*.py'",
                "max_results": "(Optional) Max results to return, default 20"
            },
            required=["pattern"]
        ),
        Tool(
            name="get_file_info",
            description="Get metadata about a file (size, is_modifiable, line count, etc.)",
            parameters={
                "filepath": "Path to the file"
            },
            required=["filepath"]
        ),
        Tool(
            name="finish",
            description="Complete the task. Call this when you have successfully fulfilled the desire or determined it cannot be done.",
            parameters={
                "success": "true if task completed successfully, false otherwise",
                "message": "Summary of what was accomplished or why it failed"
            },
            required=["success", "message"]
        ),
    ]

    SYSTEM_PROMPT = """You are BYRD's coding agent - an autonomous code modification system.

Your task is to fulfill coding desires by exploring the codebase and making precise changes.

## Available Tools

{tool_descriptions}

## Process

1. UNDERSTAND: Read the desire carefully. What code change is needed?
2. EXPLORE: Use read_file, list_files, search_code to understand the codebase
3. PLAN: Decide what changes to make
4. EXECUTE: Use edit_file or write_file to make changes
5. VERIFY: Read the modified files to confirm changes are correct
6. FINISH: Call finish with success=true and a summary

## Rules

1. ALWAYS read a file before editing it
2. Use edit_file for modifications (more precise than write_file)
3. Make minimal changes - don't refactor unrelated code
4. Protected files CANNOT be modified: constitutional.py, provenance.py, modification_log.py, self_modification.py
5. Dangerous patterns are blocked: eval, exec, os.system, subprocess, etc.
6. If you cannot fulfill the desire, call finish with success=false and explain why

## Output Format

For each step, output a JSON object:
```json
{{
  "thinking": "Your reasoning about what to do next",
  "tool": "tool_name",
  "args": {{
    "arg1": "value1",
    "arg2": "value2"
  }}
}}
```

Or to finish:
```json
{{
  "thinking": "Summary of what was accomplished",
  "tool": "finish",
  "args": {{
    "success": true,
    "message": "Description of changes made"
  }}
}}
```
"""

    def __init__(self, llm_client, memory, config: Dict):
        """
        Initialize the agent coder.

        Args:
            llm_client: LLM client for reasoning
            memory: Memory system for recording experiences
            config: Configuration dictionary
        """
        self.llm_client = llm_client
        self.memory = memory
        self.config = config

        self._enabled = config.get("enabled", True)
        self.max_steps = config.get("max_steps", 15)
        self.max_file_changes = config.get("max_file_changes", 5)
        self.temperature = config.get("temperature", 0.2)

        self.constitutional = ConstitutionalConstraints()
        self.tools = AgentTools(self.constitutional)

    @property
    def available(self) -> bool:
        """Check if agent coder is available."""
        return self._enabled

    def reset(self):
        """Reset agent coder state for fresh start."""
        # AgentCoder is stateless between invocations, so nothing to reset
        # This method exists for interface compatibility with Coder class
        pass

    def _format_tool_descriptions(self) -> str:
        """Format tool descriptions for the system prompt."""
        lines = []
        for tool in self.TOOLS:
            lines.append(f"### {tool.name}")
            lines.append(tool.description)
            lines.append("Parameters:")
            for param, desc in tool.parameters.items():
                req = "(required)" if param in tool.required else "(optional)"
                lines.append(f"  - {param} {req}: {desc}")
            lines.append("")
        return "\n".join(lines)

    def _build_system_prompt(self) -> str:
        """Build the system prompt with tool descriptions."""
        return self.SYSTEM_PROMPT.format(
            tool_descriptions=self._format_tool_descriptions()
        )

    def _format_history(self, state: AgentState) -> str:
        """Format conversation history for the LLM."""
        lines = []

        lines.append(f"## Desire to Fulfill\n{state.desire.get('description', 'Unknown desire')}\n")

        if state.history:
            lines.append("## Previous Steps\n")
            for msg in state.history:
                if msg.role == "assistant":
                    lines.append(f"### Step (Your Action)")
                    lines.append(f"Tool: {msg.tool_name}")
                    lines.append(f"Args: {json.dumps(msg.tool_args, indent=2)}")
                elif msg.role == "tool":
                    lines.append(f"### Result of {msg.tool_name}")
                    # Truncate very long results
                    result = msg.tool_result
                    if len(result) > 2000:
                        result = result[:2000] + "\n... [TRUNCATED]"
                    lines.append(result)
                lines.append("")

        lines.append(f"\n## Current Status")
        lines.append(f"Steps taken: {state.steps}/{self.max_steps}")
        lines.append(f"Files modified: {state.files_modified}")
        lines.append("\n## Your Next Action")
        lines.append("Provide a JSON object with 'thinking', 'tool', and 'args' fields.")

        return "\n".join(lines)

    async def _execute_tool(self, tool_name: str, args: Dict) -> ToolResult:
        """Execute a tool with the given arguments."""
        tool_methods = {
            "read_file": self.tools.read_file,
            "write_file": self.tools.write_file,
            "edit_file": self.tools.edit_file,
            "list_files": self.tools.list_files,
            "search_code": self.tools.search_code,
            "get_file_info": self.tools.get_file_info,
        }

        if tool_name == "finish":
            # Special handling for finish
            return ToolResult(
                success=str(args.get("success", "false")).lower() == "true",
                output=args.get("message", "Task completed")
            )

        if tool_name not in tool_methods:
            return ToolResult(False, "", f"Unknown tool: {tool_name}")

        try:
            method = tool_methods[tool_name]
            return await method(**args)
        except TypeError as e:
            return ToolResult(False, "", f"Invalid arguments for {tool_name}: {e}")
        except Exception as e:
            return ToolResult(False, "", f"Error executing {tool_name}: {e}")

    def _parse_agent_response(self, response_text: str) -> Optional[Dict]:
        """Parse the agent's JSON response."""
        # Try to extract JSON from the response
        text = response_text.strip()

        # Handle markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Try to find JSON object in text
            match = re.search(r'\{[^{}]*"tool"[^{}]*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            return None

    async def _agent_step(self, state: AgentState) -> AgentState:
        """Execute one step of the agent loop."""
        state.steps += 1

        # Build prompt
        system = self._build_system_prompt()
        user = self._format_history(state)

        # Get LLM response
        full_prompt = f"{system}\n\n{user}"

        try:
            response = await self.llm_client.generate(
                prompt=full_prompt,
                temperature=self.temperature,
                max_tokens=1500
            )

            response_text = response.text if hasattr(response, 'text') else str(response)

        except Exception as e:
            state.completed = True
            state.success = False
            state.final_message = f"LLM error: {e}"
            return state

        # Parse response
        parsed = self._parse_agent_response(response_text)

        if not parsed:
            state.completed = True
            state.success = False
            state.final_message = f"Failed to parse agent response: {response_text[:200]}"
            return state

        tool_name = parsed.get("tool", "")
        tool_args = parsed.get("args", {})
        thinking = parsed.get("thinking", "")

        print(f"  🔧 Agent step {state.steps}: {tool_name} - {thinking[:100]}...")

        # Record assistant message
        state.history.append(AgentMessage(
            role="assistant",
            content=thinking,
            tool_name=tool_name,
            tool_args=tool_args
        ))

        # Execute tool
        result = await self._execute_tool(tool_name, tool_args)

        # Record tool result
        result_text = result.output if result.success else f"ERROR: {result.error}"
        state.history.append(AgentMessage(
            role="tool",
            content=result_text,
            tool_name=tool_name,
            tool_result=result_text
        ))

        # Check for finish
        if tool_name == "finish":
            state.completed = True
            state.success = result.success
            state.final_message = result.output
            state.files_modified = self.tools.files_modified.copy()

        # Check for file modification
        if tool_name in ["write_file", "edit_file"] and result.success:
            filepath = tool_args.get("filepath", "")
            if filepath and filepath not in state.files_modified:
                state.files_modified.append(filepath)

        # Check limits
        if state.steps >= self.max_steps:
            state.completed = True
            state.success = False
            state.final_message = f"Max steps ({self.max_steps}) reached without completion"

        if len(state.files_modified) > self.max_file_changes:
            state.completed = True
            state.success = False
            state.final_message = f"Too many file modifications ({len(state.files_modified)})"

        return state

    async def fulfill_desire(self, desire: Dict) -> Dict:
        """
        Main entry point: fulfill a coding desire using the agent loop.

        Args:
            desire: Dictionary with 'id', 'description', etc.

        Returns:
            Dictionary with 'success', 'files_modified', 'message', 'steps'
        """
        if not self._enabled:
            return {
                "success": False,
                "reason": "Agent coder disabled",
                "files_modified": [],
                "steps": 0
            }

        desire_desc = desire.get("description", "Unknown desire")
        desire_id = desire.get("id", "unknown")

        print(f"\n🤖 Agent Coder starting: {desire_desc[:80]}...")

        # Emit start event
        await event_bus.emit(Event(
            type=EventType.CODER_INVOKED,
            data={"desire_id": desire_id, "description": desire_desc}
        ))

        # Initialize state
        state = AgentState(desire=desire)

        # Reset tools' file tracking
        self.tools.files_modified = []

        # Agent loop
        while not state.completed:
            state = await self._agent_step(state)

        # Record provenance for successful modifications
        if state.success and state.files_modified:
            await self._record_provenance(state, desire)

        # Emit completion event
        await event_bus.emit(Event(
            type=EventType.CODER_COMPLETE,
            data={
                "desire_id": desire_id,
                "success": state.success,
                "files_modified": state.files_modified,
                "steps": state.steps,
                "message": state.final_message
            }
        ))

        result = {
            "success": state.success,
            "files_modified": state.files_modified,
            "message": state.final_message,
            "steps": state.steps,
            "reason": state.final_message if not state.success else None
        }

        print(f"🤖 Agent Coder finished: {'SUCCESS' if state.success else 'FAILED'} - {state.final_message[:80]}")

        return result

    async def _record_provenance(self, state: AgentState, desire: Dict):
        """Record modification provenance for audit trail."""
        try:
            from provenance import record_modification

            # Build reasoning chain from history
            reasoning_chain = []
            for msg in state.history:
                if msg.role == "assistant" and msg.content:
                    reasoning_chain.append({
                        "step": len(reasoning_chain) + 1,
                        "thinking": msg.content,
                        "tool": msg.tool_name,
                        "args": msg.tool_args
                    })

            await record_modification(
                files=state.files_modified,
                desire_id=desire.get("id"),
                desire_description=desire.get("description"),
                reasoning_chain=reasoning_chain,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            print(f"⚠️ Failed to record provenance: {e}")

    # =========================================================================
    # COMPATIBILITY INTERFACE (matches Coder class)
    # =========================================================================

    @property
    def enabled(self) -> bool:
        """Check if coder is enabled (property for compatibility)."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        """Set enabled state."""
        self._enabled = value

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        target_file: Optional[str] = None
    ) -> 'CoderResult':
        """
        Execute a coding task - compatibility interface with CLI Coder.

        Args:
            prompt: The coding task description
            context: Optional context dictionary
            target_file: Optional target file for the change

        Returns:
            CoderResult-compatible dictionary
        """
        # Build a desire from the prompt
        desire = {
            "id": f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": prompt,
            "target_file": target_file,
            "context": context or {}
        }

        result = await self.fulfill_desire(desire)

        # Return compatible result format
        return CoderResult(
            success=result.get("success", False),
            output=result.get("message", ""),
            files_modified=result.get("files_modified", []),
            error=result.get("reason") if not result.get("success") else None,
            metadata={
                "steps": result.get("steps", 0),
                "agent_type": "llm"
            }
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "enabled": self._enabled,
            "type": "agent_coder",
            "max_steps": self.max_steps,
            "max_file_changes": self.max_file_changes,
            "llm_model": getattr(self.llm_client, 'model', 'unknown'),
            "temperature": self.temperature
        }


@dataclass
class CoderResult:
    """Result from a coder invocation (compatibility with CLI Coder)."""
    success: bool
    output: str
    files_modified: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_agent_coder(llm_client, memory, config: Dict) -> AgentCoder:
    """
    Factory function to create an agent coder.

    Args:
        llm_client: LLM client for reasoning
        memory: Memory system
        config: Configuration dictionary

    Returns:
        Configured AgentCoder instance
    """
    return AgentCoder(
        llm_client=llm_client,
        memory=memory,
        config=config.get("agent_coder", config.get("coder", {}))
    )

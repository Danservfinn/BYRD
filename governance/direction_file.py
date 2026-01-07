"""
File-Based Direction Mechanism

Enables asynchronous communication between human and BYRD via files.
Human writes to direction files, BYRD reads and processes them.

Files:
- .claude/direction.md        - Human writes direction here
- .claude/byrd-status.md      - BYRD writes status here
- .claude/pending-approvals.md - Actions awaiting human approval

This enables direction even when BYRD is running headlessly.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import logging

logger = logging.getLogger("byrd.governance.direction_file")


class DirectionFile:
    """
    File-based direction interface.

    Human writes to direction.md:
    ```markdown
    # Direction for BYRD

    ## Priorities
    - coding: 0.9
    - reasoning: 0.7

    ## Desires
    - Improve SWE-bench score to 60%
    - Learn to use web search effectively

    ## Constraints
    - Do not make API calls without approval

    ## Feedback
    - Good job on the last code generation
    ```

    BYRD reads this periodically and updates its state.
    """

    def __init__(self, base_dir: Path = None):
        """Initialize with base directory."""
        self.base_dir = base_dir or Path(".claude")
        self.direction_file = self.base_dir / "direction.md"
        self.status_file = self.base_dir / "byrd-status.md"
        self.approvals_file = self.base_dir / "pending-approvals.md"

        # Ensure directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Create template if direction file doesn't exist
        if not self.direction_file.exists():
            self._create_template()

    def _create_template(self):
        """Create direction file template."""
        template = """# Direction for BYRD

*Edit this file to direct BYRD's development.*
*BYRD reads this file periodically and updates its goals.*

## Priorities

*Set domain priorities (0.0 = ignore, 1.0 = urgent)*

- coding: 0.5
- reasoning: 0.5
- economic: 0.3

## Desires

*Things you want BYRD to pursue. BYRD will figure out HOW.*

- (Add your desires here)

## Constraints

*Limits on BYRD's behavior.*

- (Add constraints here)

## Feedback

*Your feedback on BYRD's recent work.*

- (Add feedback here)

---

*Last read by BYRD: Never*
"""
        self.direction_file.write_text(template)
        logger.info(f"Created direction template at {self.direction_file}")

    def read_direction(self) -> Dict:
        """
        Read and parse direction file.

        Returns:
            Dict with priorities, desires, constraints, feedback
        """
        if not self.direction_file.exists():
            return {"priorities": {}, "desires": [], "constraints": [], "feedback": []}

        content = self.direction_file.read_text()

        result = {
            "priorities": {},
            "desires": [],
            "constraints": [],
            "feedback": [],
            "raw": content
        }

        current_section = None

        for line in content.split("\n"):
            line = line.strip()

            # Section headers
            if line.startswith("## Priorities"):
                current_section = "priorities"
            elif line.startswith("## Desires"):
                current_section = "desires"
            elif line.startswith("## Constraints"):
                current_section = "constraints"
            elif line.startswith("## Feedback"):
                current_section = "feedback"
            elif line.startswith("##") or line.startswith("---"):
                current_section = None

            # Parse content
            elif current_section and line.startswith("- "):
                item = line[2:].strip()

                # Skip placeholder items
                if item.startswith("(") and item.endswith(")"):
                    continue

                if current_section == "priorities":
                    # Parse "domain: value"
                    if ":" in item:
                        parts = item.split(":", 1)
                        domain = parts[0].strip()
                        try:
                            value = float(parts[1].strip())
                            result["priorities"][domain] = value
                        except ValueError:
                            pass
                else:
                    result[current_section].append(item)

        # Update last read timestamp
        self._update_last_read()

        return result

    def _update_last_read(self):
        """Update the 'last read' timestamp in the file."""
        if not self.direction_file.exists():
            return

        content = self.direction_file.read_text()
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Replace the last read line
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("*Last read by BYRD:"):
                lines[i] = f"*Last read by BYRD: {timestamp}*"
                break

        self.direction_file.write_text("\n".join(lines))

    def write_status(self, status: Dict):
        """
        Write BYRD status to status file.

        Args:
            status: Dict with current BYRD state
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        content = f"""# BYRD Status

*Last updated: {timestamp}*

## Current State

"""
        for key, value in status.items():
            if key == "rsi_metrics":
                content += "\n### RSI Metrics\n\n"
                for mk, mv in value.items():
                    content += f"- {mk}: {mv}\n"
            elif isinstance(value, bool):
                emoji = "✓" if value else "✗"
                content += f"- {key}: {emoji}\n"
            else:
                content += f"- {key}: {value}\n"

        # Add priorities if set
        if hasattr(self, '_director') and self._director:
            priorities = self._director.get_priorities()
            if priorities:
                content += "\n## Active Priorities\n\n"
                for domain, priority in sorted(priorities.items(),
                                              key=lambda x: x[1], reverse=True):
                    bar = "█" * int(priority * 10) + "░" * (10 - int(priority * 10))
                    content += f"- {domain}: {bar} ({priority:.1f})\n"

        self.status_file.write_text(content)

    def write_approval_request(self, action: str, details: Dict = None):
        """
        Write a pending approval request.

        Args:
            action: What action needs approval
            details: Additional details
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Read existing approvals
        existing = ""
        if self.approvals_file.exists():
            existing = self.approvals_file.read_text()
            # Remove header
            if "# Pending Approvals" in existing:
                existing = existing.split("---", 1)[-1] if "---" in existing else ""

        # New approval entry
        new_entry = f"""
## Request: {action}

*Requested: {timestamp}*

Details:
```json
{json.dumps(details or {}, indent=2)}
```

**To approve:** Add `APPROVED` below this request.
**To reject:** Add `REJECTED` below this request.

---
"""

        content = f"""# Pending Approvals

*BYRD is waiting for your approval on these actions.*
*Edit this file to approve or reject.*

---
{new_entry}
{existing}
"""

        self.approvals_file.write_text(content)

    def read_approval_responses(self) -> List[Dict]:
        """
        Read approval responses from the file.

        Returns:
            List of approval/rejection responses
        """
        if not self.approvals_file.exists():
            return []

        content = self.approvals_file.read_text()
        responses = []

        # Parse for APPROVED/REJECTED markers
        current_request = None
        for line in content.split("\n"):
            if line.startswith("## Request:"):
                current_request = line.replace("## Request:", "").strip()
            elif current_request:
                if "APPROVED" in line.upper():
                    responses.append({
                        "request": current_request,
                        "response": "approved"
                    })
                    current_request = None
                elif "REJECTED" in line.upper():
                    responses.append({
                        "request": current_request,
                        "response": "rejected"
                    })
                    current_request = None

        return responses


def watch_direction_file(callback, interval_seconds: float = 5.0):
    """
    Watch the direction file for changes and call callback.

    Args:
        callback: Function to call with new direction
        interval_seconds: How often to check
    """
    import asyncio
    import hashlib

    direction_file = DirectionFile()
    last_hash = None

    async def watch_loop():
        nonlocal last_hash

        while True:
            try:
                if direction_file.direction_file.exists():
                    content = direction_file.direction_file.read_text()
                    current_hash = hashlib.md5(content.encode()).hexdigest()

                    if current_hash != last_hash:
                        last_hash = current_hash
                        direction = direction_file.read_direction()
                        await callback(direction)

                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error watching direction file: {e}")
                await asyncio.sleep(interval_seconds)

    return watch_loop

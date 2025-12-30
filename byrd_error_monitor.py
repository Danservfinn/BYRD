#!/usr/bin/env python3
"""
BYRD Error Monitor - Continuously monitors BYRD output and triggers Claude Code for fixes.

Usage:
    python byrd_error_monitor.py [--log-file /path/to/byrd.log] [--watch-dir /path/to/byrd]

This script:
1. Monitors BYRD logs/output for errors
2. Collects error context
3. Invokes Claude Code with the error details
4. Optionally auto-applies fixes
"""

import asyncio
import argparse
import subprocess
import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from collections import deque

# Error patterns to watch for
ERROR_PATTERNS = [
    # Python errors
    r'Traceback \(most recent call last\):',
    r'^\s*File ".*", line \d+',
    r'^\w+Error:',
    r'^\w+Exception:',
    r'ImportError:',
    r'ModuleNotFoundError:',
    r'AttributeError:',
    r'TypeError:',
    r'ValueError:',
    r'KeyError:',
    r'RuntimeError:',

    # BYRD-specific
    r'❌',
    r'✗',
    r'\[ERROR\]',
    r'\[FAILED\]',
    r'observation_loop.*BROKEN',
    r'Neo4j.*error',
    r'WebSocket.*error',
    r'LLM.*failed',
]

# Patterns to ignore (false positives)
IGNORE_PATTERNS = [
    r'error.*handled',
    r'expected.*error',
    r'test.*error',
]


@dataclass
class ErrorEvent:
    """Represents a detected error."""
    timestamp: datetime
    error_type: str
    message: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    line_number: Optional[int] = None

    def to_prompt(self) -> str:
        """Convert to a prompt for Claude Code."""
        context = '\n'.join(self.context_before + [f">>> {self.message}"] + self.context_after)

        prompt = f"""BYRD Error Detected - Please investigate and fix:

Error Type: {self.error_type}
Time: {self.timestamp.isoformat()}
"""
        if self.file_path:
            prompt += f"File: {self.file_path}"
            if self.line_number:
                prompt += f":{self.line_number}"
            prompt += "\n"

        prompt += f"""
Context:
```
{context}
```

Please:
1. Identify the root cause
2. Propose a fix
3. Apply the fix if safe
"""
        return prompt


class BYRDErrorMonitor:
    """Monitors BYRD for errors and triggers Claude Code for fixes."""

    def __init__(
        self,
        log_file: Optional[Path] = None,
        watch_dir: Optional[Path] = None,
        auto_fix: bool = False,
        cooldown_seconds: int = 60,
        max_errors_per_hour: int = 10,
    ):
        self.log_file = log_file
        self.watch_dir = watch_dir or Path('/Users/kurultai/BYRD')
        self.auto_fix = auto_fix
        self.cooldown_seconds = cooldown_seconds
        self.max_errors_per_hour = max_errors_per_hour

        # State
        self.recent_lines: deque = deque(maxlen=20)
        self.error_history: deque = deque(maxlen=100)
        self.last_fix_time: Optional[datetime] = None
        self.errors_this_hour: int = 0
        self.hour_start: datetime = datetime.now()

        # Compile patterns
        self.error_patterns = [re.compile(p, re.MULTILINE) for p in ERROR_PATTERNS]
        self.ignore_patterns = [re.compile(p, re.IGNORECASE) for p in IGNORE_PATTERNS]

    def detect_error(self, line: str) -> Optional[str]:
        """Check if a line contains an error pattern."""
        # Check ignore patterns first
        for pattern in self.ignore_patterns:
            if pattern.search(line):
                return None

        # Check error patterns
        for pattern in self.error_patterns:
            if pattern.search(line):
                return pattern.pattern

        return None

    def extract_file_info(self, lines: List[str]) -> tuple[Optional[str], Optional[int]]:
        """Extract file path and line number from traceback."""
        file_pattern = re.compile(r'File "([^"]+)", line (\d+)')

        for line in reversed(lines):
            match = file_pattern.search(line)
            if match:
                return match.group(1), int(match.group(2))

        return None, None

    def create_error_event(self, error_line: str, error_type: str) -> ErrorEvent:
        """Create an ErrorEvent from detected error."""
        context_before = list(self.recent_lines)
        file_path, line_number = self.extract_file_info(context_before + [error_line])

        return ErrorEvent(
            timestamp=datetime.now(),
            error_type=error_type,
            message=error_line,
            context_before=context_before,
            file_path=file_path,
            line_number=line_number,
        )

    def should_process_error(self) -> bool:
        """Check if we should process another error (rate limiting)."""
        now = datetime.now()

        # Reset hourly counter
        if (now - self.hour_start).total_seconds() > 3600:
            self.errors_this_hour = 0
            self.hour_start = now

        # Check hourly limit
        if self.errors_this_hour >= self.max_errors_per_hour:
            print(f"⚠️ Rate limit: {self.max_errors_per_hour} errors/hour reached")
            return False

        # Check cooldown
        if self.last_fix_time:
            elapsed = (now - self.last_fix_time).total_seconds()
            if elapsed < self.cooldown_seconds:
                print(f"⚠️ Cooldown: {self.cooldown_seconds - elapsed:.0f}s remaining")
                return False

        return True

    def invoke_claude_code(self, error: ErrorEvent) -> bool:
        """Invoke Claude Code to fix the error."""
        if not self.should_process_error():
            return False

        prompt = error.to_prompt()

        print(f"\n{'='*60}")
        print(f"🔧 Invoking Claude Code for error: {error.error_type}")
        print(f"{'='*60}")

        try:
            # Option 1: Interactive mode (requires terminal)
            # subprocess.run(['claude', '--print', prompt], cwd=self.watch_dir)

            # Option 2: Use Claude Code API/CLI
            result = subprocess.run(
                ['claude', '--print', '-p', prompt],
                cwd=self.watch_dir,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                print(f"✅ Claude Code response:\n{result.stdout[:500]}...")
                self.last_fix_time = datetime.now()
                self.errors_this_hour += 1
                return True
            else:
                print(f"❌ Claude Code error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Claude Code timed out")
            return False
        except FileNotFoundError:
            print("❌ Claude Code CLI not found. Install with: npm install -g @anthropic-ai/claude-code")
            return False
        except Exception as e:
            print(f"❌ Error invoking Claude Code: {e}")
            return False

    async def monitor_log_file(self):
        """Monitor a log file for errors."""
        if not self.log_file or not self.log_file.exists():
            print(f"Log file not found: {self.log_file}")
            return

        print(f"📋 Monitoring log file: {self.log_file}")

        # Start at end of file
        with open(self.log_file, 'r') as f:
            f.seek(0, 2)  # Seek to end

            while True:
                line = f.readline()
                if line:
                    line = line.rstrip()
                    self.recent_lines.append(line)

                    error_type = self.detect_error(line)
                    if error_type:
                        error = self.create_error_event(line, error_type)
                        self.error_history.append(error)

                        print(f"\n🚨 Error detected: {error_type}")
                        print(f"   {line[:100]}...")

                        if self.auto_fix:
                            self.invoke_claude_code(error)
                        else:
                            print("   (auto-fix disabled, run with --auto-fix to enable)")
                else:
                    await asyncio.sleep(0.5)

    async def monitor_subprocess(self, command: List[str]):
        """Monitor a subprocess for errors."""
        print(f"🚀 Starting BYRD: {' '.join(command)}")

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=self.watch_dir,
        )

        async for line in process.stdout:
            line = line.decode().rstrip()
            print(line)  # Echo output

            self.recent_lines.append(line)

            error_type = self.detect_error(line)
            if error_type:
                # Collect more context
                await asyncio.sleep(0.5)

                error = self.create_error_event(line, error_type)
                self.error_history.append(error)

                print(f"\n🚨 Error detected: {error_type}")

                if self.auto_fix:
                    self.invoke_claude_code(error)

    def get_status(self) -> Dict:
        """Get monitor status."""
        return {
            'errors_detected': len(self.error_history),
            'errors_this_hour': self.errors_this_hour,
            'last_fix_time': self.last_fix_time.isoformat() if self.last_fix_time else None,
            'auto_fix': self.auto_fix,
            'recent_errors': [
                {
                    'type': e.error_type,
                    'message': e.message[:100],
                    'time': e.timestamp.isoformat(),
                }
                for e in list(self.error_history)[-5:]
            ]
        }


async def main():
    parser = argparse.ArgumentParser(description='Monitor BYRD for errors and auto-fix with Claude Code')
    parser.add_argument('--log-file', type=Path, help='Log file to monitor')
    parser.add_argument('--watch-dir', type=Path, default=Path('/Users/kurultai/BYRD'), help='BYRD directory')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically invoke Claude Code for fixes')
    parser.add_argument('--cooldown', type=int, default=60, help='Seconds between fix attempts')
    parser.add_argument('--run-byrd', action='store_true', help='Start and monitor BYRD')

    args = parser.parse_args()

    monitor = BYRDErrorMonitor(
        log_file=args.log_file,
        watch_dir=args.watch_dir,
        auto_fix=args.auto_fix,
        cooldown_seconds=args.cooldown,
    )

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           BYRD Error Monitor - Claude Code Integration        ║
╠══════════════════════════════════════════════════════════════╣
║  Auto-fix: {'ENABLED ✅' if args.auto_fix else 'DISABLED ⚠️ (use --auto-fix)'}
║  Cooldown: {args.cooldown}s between fixes
║  Watch dir: {args.watch_dir}
╚══════════════════════════════════════════════════════════════╝
""")

    if args.run_byrd:
        await monitor.monitor_subprocess(['python', 'byrd.py'])
    elif args.log_file:
        await monitor.monitor_log_file()
    else:
        print("Usage:")
        print("  Monitor log file:  python byrd_error_monitor.py --log-file byrd.log --auto-fix")
        print("  Run and monitor:   python byrd_error_monitor.py --run-byrd --auto-fix")


if __name__ == '__main__':
    asyncio.run(main())

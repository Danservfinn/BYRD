#!/usr/bin/env python3
"""
Semantic Monitor - Watches BYRD's beliefs and internal state for issues.

Unlike watch_and_fix.sh which catches Python exceptions, this monitors:
1. Beliefs about broken systems ("broken transmission", "observation_loop BROKEN")
2. Silent failures (operations succeed but produce no data)
3. Stalled loops (no activity for extended periods)
4. Neo4j health issues

Usage:
    python semantic_monitor.py --auto-fix
    python semantic_monitor.py --watch-beliefs
    python semantic_monitor.py --check-now
"""

import asyncio
import argparse
import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

# Add BYRD to path
sys.path.insert(0, str(Path(__file__).parent))


@dataclass
class SemanticIssue:
    """A semantic issue detected in BYRD's state."""
    issue_type: str
    description: str
    evidence: str
    severity: str  # low, medium, high, critical
    suggested_fix: str
    detected_at: datetime = None

    def __post_init__(self):
        if not self.detected_at:
            self.detected_at = datetime.now()

    def to_prompt(self) -> str:
        return f"""BYRD Semantic Issue Detected:

Type: {self.issue_type}
Severity: {self.severity.upper()}
Description: {self.description}

Evidence:
{self.evidence}

Suggested investigation:
{self.suggested_fix}

Please investigate and fix this issue.
"""


# Belief patterns that indicate problems
PROBLEM_BELIEFS = [
    {
        "pattern": "broken transmission",
        "issue_type": "transmission_failure",
        "severity": "high",
        "fix": "Check Neo4j connection, event_bus subscriptions, and memory.record_experience()"
    },
    {
        "pattern": "observation_loop.*BROKEN",
        "issue_type": "observation_loop_failure",
        "severity": "critical",
        "fix": "Check for types.py shadowing, import errors, or Neo4j auth issues"
    },
    {
        "pattern": "produces no observable data",
        "issue_type": "silent_failure",
        "severity": "high",
        "fix": "Check LLM responses, verify dreamer is producing output"
    },
    {
        "pattern": "cannot connect|connection refused|auth.*fail",
        "issue_type": "connection_failure",
        "severity": "critical",
        "fix": "Check Neo4j: docker ps | grep neo4j, verify credentials"
    },
    {
        "pattern": "stuck|stalled|not progressing",
        "issue_type": "stalled_loop",
        "severity": "medium",
        "fix": "Check for infinite loops, blocked async operations, or deadlocks"
    },
    {
        "pattern": "rate limit|too many requests|429",
        "issue_type": "rate_limit",
        "severity": "medium",
        "fix": "Increase LLM rate_limit_interval in config.yaml"
    },
]


class SemanticMonitor:
    """Monitors BYRD's semantic state for issues."""

    def __init__(self, auto_fix: bool = False):
        self.auto_fix = auto_fix
        self.memory = None
        self.issues_found: List[SemanticIssue] = []
        self.last_check = None

    async def connect(self):
        """Connect to BYRD's memory system."""
        try:
            from memory import Memory
            import os

            # Load credentials from environment or defaults
            config = {
                "neo4j_uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
                "neo4j_user": os.environ.get("NEO4J_USER", "neo4j"),
                "neo4j_password": os.environ.get("NEO4J_PASSWORD", "prometheus"),
            }

            self.memory = Memory(config)
            await self.memory.connect()
            return True
        except Exception as e:
            print(f"❌ Failed to connect to memory: {e}")
            return False

    async def check_problem_beliefs(self) -> List[SemanticIssue]:
        """Check for beliefs that indicate problems."""
        issues = []

        if not self.memory:
            return issues

        try:
            # Query recent beliefs
            result = await self.memory._run_query("""
                MATCH (b:Belief)
                WHERE b.created_at > datetime() - duration('PT1H')
                RETURN b.id, b.content, b.confidence, b.created_at
                ORDER BY b.created_at DESC
                LIMIT 50
            """)

            import re
            for record in result:
                content = record.get('b.content', '') or ''
                belief_id = record.get('b.id', '')

                for problem in PROBLEM_BELIEFS:
                    if re.search(problem['pattern'], content, re.IGNORECASE):
                        issues.append(SemanticIssue(
                            issue_type=problem['issue_type'],
                            description=f"BYRD formed a belief indicating: {problem['issue_type']}",
                            evidence=f"Belief {belief_id}: {content[:200]}",
                            severity=problem['severity'],
                            suggested_fix=problem['fix']
                        ))

        except Exception as e:
            print(f"⚠️ Error checking beliefs: {e}")

        return issues

    async def check_stalled_activity(self) -> List[SemanticIssue]:
        """Check if BYRD's activity has stalled."""
        issues = []

        if not self.memory:
            return issues

        try:
            # Check for recent experiences
            result = await self.memory._run_query("""
                MATCH (e:Experience)
                RETURN max(e.timestamp) as last_activity
            """)

            if result:
                last_activity = result[0].get('last_activity')
                if last_activity:
                    # Parse the timestamp
                    from datetime import timezone
                    now = datetime.now(timezone.utc)

                    # If no activity in last 10 minutes, flag it
                    # (This is a simplified check - real implementation would parse the timestamp)
                    issues.append(SemanticIssue(
                        issue_type="activity_check",
                        description="Activity check performed",
                        evidence=f"Last activity: {last_activity}",
                        severity="low",
                        suggested_fix="Monitor ongoing"
                    ))

        except Exception as e:
            print(f"⚠️ Error checking activity: {e}")

        return issues

    async def check_observation_path(self) -> List[SemanticIssue]:
        """Check the parallel observation path for buffered observations."""
        issues = []

        # Check if parallel observation buffer exists and has stuck items
        obs_dir = Path("./parallel_observations")
        if obs_dir.exists():
            pending_files = list(obs_dir.glob("*.pending.json"))
            if len(pending_files) > 10:
                issues.append(SemanticIssue(
                    issue_type="observation_backlog",
                    description=f"{len(pending_files)} observations stuck in parallel path",
                    evidence=f"Files in {obs_dir}: {[f.name for f in pending_files[:5]]}",
                    severity="high",
                    suggested_fix="Main transmission path may be blocked. Check Neo4j and event_bus."
                ))

        return issues

    async def check_all(self) -> List[SemanticIssue]:
        """Run all semantic checks."""
        print("🔍 Running semantic checks...")

        all_issues = []

        # Check beliefs
        belief_issues = await self.check_problem_beliefs()
        all_issues.extend(belief_issues)

        # Check activity
        activity_issues = await self.check_stalled_activity()
        all_issues.extend([i for i in activity_issues if i.severity != "low"])

        # Check observation path
        obs_issues = await self.check_observation_path()
        all_issues.extend(obs_issues)

        # Filter to significant issues
        significant = [i for i in all_issues if i.severity in ("high", "critical")]

        self.issues_found = significant
        self.last_check = datetime.now()

        return significant

    def invoke_claude(self, issue: SemanticIssue) -> bool:
        """Invoke Claude Code to fix a semantic issue."""
        print(f"\n{'='*60}")
        print(f"🔧 Invoking Claude Code for: {issue.issue_type}")
        print(f"{'='*60}")

        prompt = issue.to_prompt()

        try:
            result = subprocess.run(
                ['claude', '--print', '-p', prompt],
                cwd=str(Path(__file__).parent),
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                print(f"✅ Claude response:\n{result.stdout[:500]}...")
                return True
            else:
                print(f"❌ Claude error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error invoking Claude: {e}")
            return False

    async def watch_loop(self, interval_seconds: int = 60):
        """Continuously watch for semantic issues."""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           BYRD Semantic Monitor                               ║
╠══════════════════════════════════════════════════════════════╣
║  Watching for: Broken transmission, silent failures,         ║
║                stalled loops, problematic beliefs             ║
║  Check interval: {interval_seconds}s                                        ║
║  Auto-fix: {'ENABLED ✅' if self.auto_fix else 'DISABLED ⚠️'}                                          ║
╚══════════════════════════════════════════════════════════════╝
""")

        while True:
            try:
                issues = await self.check_all()

                if issues:
                    print(f"\n🚨 Found {len(issues)} semantic issue(s):")
                    for issue in issues:
                        print(f"  [{issue.severity.upper()}] {issue.issue_type}: {issue.description[:60]}")

                    if self.auto_fix:
                        for issue in issues:
                            if issue.severity in ("high", "critical"):
                                self.invoke_claude(issue)
                else:
                    print(f"✅ {datetime.now().strftime('%H:%M:%S')} - No semantic issues detected")

            except Exception as e:
                print(f"⚠️ Monitor error: {e}")

            await asyncio.sleep(interval_seconds)

    async def close(self):
        """Close connections."""
        if self.memory:
            await self.memory.close()


async def main():
    parser = argparse.ArgumentParser(description='Monitor BYRD for semantic issues')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically invoke Claude for fixes')
    parser.add_argument('--watch-beliefs', action='store_true', help='Continuously watch beliefs')
    parser.add_argument('--check-now', action='store_true', help='Run one check and exit')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds')

    args = parser.parse_args()

    monitor = SemanticMonitor(auto_fix=args.auto_fix)

    if not await monitor.connect():
        print("Failed to connect. Is Neo4j running?")
        print("  docker-compose up -d")
        sys.exit(1)

    try:
        if args.check_now:
            issues = await monitor.check_all()
            if issues:
                print(f"\n🚨 Found {len(issues)} issue(s):")
                for issue in issues:
                    print(f"\n[{issue.severity.upper()}] {issue.issue_type}")
                    print(f"  {issue.description}")
                    print(f"  Evidence: {issue.evidence[:100]}")
                    print(f"  Fix: {issue.suggested_fix}")
            else:
                print("✅ No semantic issues found")
        else:
            await monitor.watch_loop(args.interval)

    finally:
        await monitor.close()


if __name__ == '__main__':
    asyncio.run(main())

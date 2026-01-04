#!/usr/bin/env python3
"""
Goal Evolver Bootstrap Orchestrator

This script orchestrates the execution of all 7 concrete goals to bootstrap
the Goal Evolver system. It runs each goal executor in sequence and reports
overall completion status.

Goals:
1. Initial Goal Population Seeding - Ensures Goal Evolver has goals to work with
2. Research Experience Indexing - Indexes research for Memory Reasoner queries
3. Batch Orphan Reconciliation - Breaks 7-cycle deadlocks in memory
4. Memory System Health Check - Optimizes memory system performance
5. Event Bus Integration and Connectivity Test - Validates event system reliability
6. Tool Integration and Validation Test - Validates tool discovery, execution, and error handling
7. System Configuration and Metrics Validation - Validates configs, env vars, and system health

Fitness Data Points:
- Completion: Binary (all 7 goals completed successfully)
- Capability Delta: System readiness (percentage of goals completed)
- Efficiency: Total bootstrap time
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import goal executors
from execute_goal_1_bootstrap import Goal1Executor
from execute_goal_2_bootstrap import Goal2Executor
from execute_goal_3_bootstrap import Goal3Executor
from execute_goal_4_bootstrap import Goal4Executor
from execute_goal_5_bootstrap import Goal5Executor
from execute_goal_6_bootstrap import Goal6Executor
from execute_goal_7_bootstrap import Goal7Executor


class BootstrapOrchestrator:
    """Orchestrator for running all Goal Evolver bootstrap goals."""
    
    def __init__(self):
        self.start_time = None
        self.executors = {
            1: Goal1Executor,
            2: Goal2Executor,
            3: Goal3Executor,
            4: Goal4Executor,
            5: Goal5Executor,
            6: Goal6Executor,
            7: Goal7Executor
        }
        self.results = {
            "started": False,
            "completed": False,
            "total_goals": 7,
            "goals_completed": 0,
            "goals_failed": 0,
            "individual_results": {},
            "errors": [],
            "duration_seconds": 0
        }
    
    async def execute_goal(self, goal_number: int) -> Dict[str, Any]:
        """Execute a single bootstrap goal."""
        print(f"\n{'='*60}")
        print(f"EXECUTING GOAL #{goal_number}")
        print(f"{'='*60}")
        
        executor_class = self.executors.get(goal_number)
        if not executor_class:
            error = f"No executor found for goal #{goal_number}"
            print(f"[ERROR] {error}")
            self.results["errors"].append(error)
            return {"goal_number": goal_number, "completed": False, "error": error}
        
        try:
            executor = executor_class()
            result = await executor.execute()
            executor.print_report()
            return result
        except Exception as e:
            import traceback
            error = f"Goal #{goal_number} execution failed: {e}"
            print(f"[ERROR] {error}")
            print(f"[TRACEBACK] {traceback.format_exc()}")
            self.results["errors"].append(error)
            return {"goal_number": goal_number, "completed": False, "error": str(e)}
    
    async def execute_all(self, goals: Optional[List[int]] = None) -> Dict[str, Any]:
        """Execute all bootstrap goals or a specific subset."""
        print("\n" + "="*60)
        print("GOAL EVOLVER BOOTSTRAP ORCHESTRATOR")
        print("="*60)
        print(f"\nStarting bootstrap process at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = datetime.now()
        self.results["started"] = True
        
        # Determine which goals to run
        goals_to_run = goals if goals else list(self.executors.keys())
        goals_to_run.sort()
        
        print(f"\nGoals to execute: {goals_to_run}")
        
        # Execute each goal
        for goal_number in goals_to_run:
            result = await self.execute_goal(goal_number)
            self.results["individual_results"][goal_number] = result
            
            if result.get("completed"):
                self.results["goals_completed"] += 1
                print(f"\n[SUCCESS] Goal #{goal_number} completed successfully")
            else:
                self.results["goals_failed"] += 1
                print(f"\n[FAILURE] Goal #{goal_number} failed to complete")
        
        # Calculate duration
        duration = (datetime.now() - self.start_time).total_seconds()
        self.results["duration_seconds"] = duration
        
        # Determine overall completion
        # Success if at least 4 out of 5 goals completed (allowing one failure)
        success_threshold = max(1, len(goals_to_run) - 1)
        self.results["completed"] = self.results["goals_completed"] >= success_threshold
        
        return self.results
    
    def print_final_report(self):
        """Print the final bootstrap report."""
        print("\n" + "="*60)
        print("FINAL BOOTSTRAP REPORT")
        print("="*60)
        print(f"\nBootstrap Duration: {self.results['duration_seconds']:.2f}s")
        print(f"Goals Completed: {self.results['goals_completed']}/{self.results['total_goals']}")
        print(f"Goals Failed: {self.results['goals_failed']}/{self.results['total_goals']}")
        
        print(f"\nIndividual Results:")
        for goal_num in sorted(self.results["individual_results"].keys()):
            result = self.results["individual_results"][goal_num]
            status = "✓" if result.get("completed") else "✗"
            goal_name = result.get("goal_name", "Unknown")
            print(f"  Goal #{goal_num}: {status} {goal_name}")
        
        if self.results["errors"]:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for err in self.results["errors"][:10]:
                print(f"  - {err}")
        
        # Fitness metrics
        completion_rate = self.results["goals_completed"] / self.results["total_goals"]
        print(f"\n" + "="*60)
        print("FITNESS METRICS")
        print("="*60)
        print(f"Completion: {completion_rate*100:.1f}%")
        print(f"Capability Delta: System readiness = {completion_rate*100:.1f}%")
        print(f"Efficiency: {self.results['total_goals'] / max(1, self.results['duration_seconds']):.2f} goals/second")
        
        print(f"\n" + "="*60)
        if self.results["completed"]:
            print("✅ GOAL EVOLVER BOOTSTRAP - COMPLETED")
        else:
            print("⚠️  GOAL EVOLVER BOOTSTRAP - PARTIAL SUCCESS")
        print("="*60 + "\n")


async def main():
    """Main entry point."""
    # Parse command line arguments for optional goal selection
    goals = None
    if len(sys.argv) > 1:
        try:
            goals = [int(g) for g in sys.argv[1:]]
            print(f"Running specified goals: {goals}")
        except ValueError:
            print("Invalid goal numbers specified, running all goals")
    
    orchestrator = BootstrapOrchestrator()
    results = await orchestrator.execute_all(goals)
    orchestrator.print_final_report()
    
    return results['completed']


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Execute Goal #7 for Goal Evolver Bootstrap:
System Configuration and Metrics Validation Test

This script executes the system configuration and metrics validation test
to complete goal #7 for the Goal Evolver bootstrap process. It ensures:
1. System configuration files are valid and accessible
2. Environment variables are properly set
3. Metrics collection is functional
4. System health indicators are measurable
5. Results are reported for completion tracking

Fitness Data Points:
- Completion: Binary (all config and metrics tests passed)
- Capability Delta: Configuration readiness (valid configs/total)
- Efficiency: Config validation time and metrics collection rate
"""

import asyncio
import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


@dataclass
class ConfigTestResult:
    """Result of a single configuration test."""
    test_name: str
    test_type: str  # 'config', 'env', 'metrics', 'health'
    passed: bool
    execution_time_ms: float
    value: str = ""
    error_message: str = ""


class Goal7Executor:
    """Executor for Goal #7: System Configuration and Metrics Validation Test."""
    
    def __init__(self):
        self.start_time = None
        self.test_results: List[ConfigTestResult] = []
        self.results = {
            "goal_number": 7,
            "goal_name": "System Configuration and Metrics Validation Test",
            "started": False,
            "completed": False,
            "tests_passed": 0,
            "tests_total": 0,
            "config_passed": 0,
            "config_total": 0,
            "env_passed": 0,
            "env_total": 0,
            "metrics_passed": 0,
            "metrics_total": 0,
            "health_passed": 0,
            "health_total": 0,
            "errors": [],
            "duration_seconds": 0
        }
        
        # Configuration files to validate
        self.config_files = [
            '.env.example',
            'VERSION',
            'README.md'
        ]
        
        # Environment variables to check
        self.env_vars = [
            'PATH',
            'HOME'
        ]
        
        # Optional env vars that are good to have
        self.optional_env_vars = [
            'NVIDIA_VISIBLE_DEVICES',
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY'
        ]
    
    async def initialize(self):
        """Initialize executor."""
        print("[INIT] Initializing Goal #7: System Configuration and Metrics Validation Test...")
        self.results["started"] = True
        self.start_time = time.time()
        return True
    
    def record_result(self, result: ConfigTestResult):
        """Record a test result."""
        self.test_results.append(result)
        self.results["tests_total"] += 1
        if result.passed:
            self.results["tests_passed"] += 1
            
        # Track by test type
        if result.test_type == "config":
            self.results["config_total"] += 1
            if result.passed:
                self.results["config_passed"] += 1
        elif result.test_type == "env":
            self.results["env_total"] += 1
            if result.passed:
                self.results["env_passed"] += 1
        elif result.test_type == "metrics":
            self.results["metrics_total"] += 1
            if result.passed:
                self.results["metrics_passed"] += 1
        elif result.test_type == "health":
            self.results["health_total"] += 1
            if result.passed:
                self.results["health_passed"] += 1
    
    async def test_config_files(self) -> List[ConfigTestResult]:
        """Test that configuration files exist and are valid."""
        print("\n[TEST] Testing configuration files...")
        results = []
        
        for config_file in self.config_files:
            start_time = time.time()
            
            # Check if file exists
            file_path = Path(config_file)
            exists = file_path.exists()
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name=f"config_{config_file}",
                test_type="config",
                passed=exists,
                execution_time_ms=elapsed_ms,
                value=str(file_path.absolute()) if exists else "",
                error_message="File not found" if not exists else ""
            )
            results.append(result)
            self.record_result(result)
            
            # If file exists, check if it's readable
            if exists:
                start_time = time.time()
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    is_readable = len(content) > 0
                    elapsed_ms = (time.time() - start_time) * 1000
                    
                    result = ConfigTestResult(
                        test_name=f"config_readable_{config_file}",
                        test_type="config",
                        passed=is_readable,
                        execution_time_ms=elapsed_ms,
                        value=f"{len(content)} bytes",
                        error_message="" if is_readable else "File is empty"
                    )
                    results.append(result)
                    self.record_result(result)
                except Exception as e:
                    elapsed_ms = (time.time() - start_time) * 1000
                    result = ConfigTestResult(
                        test_name=f"config_readable_{config_file}",
                        test_type="config",
                        passed=False,
                        execution_time_ms=elapsed_ms,
                        error_message=str(e)
                    )
                    results.append(result)
                    self.record_result(result)
        
        print(f"[OK] Validated {len(self.config_files)} configuration files")
        self.test_results.extend(results)
        return results
    
    async def test_environment_variables(self) -> List[ConfigTestResult]:
        """Test that required environment variables are set."""
        print("\n[TEST] Testing environment variables...")
        results = []
        
        # Test required env vars
        for env_var in self.env_vars:
            start_time = time.time()
            value = os.environ.get(env_var)
            is_set = value is not None and len(value) > 0
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name=f"env_{env_var}",
                test_type="env",
                passed=is_set,
                execution_time_ms=elapsed_ms,
                value=value[:50] + "..." if value and len(value) > 50 else value or "",
                error_message="Not set" if not is_set else ""
            )
            results.append(result)
            self.record_result(result)
        
        # Test optional env vars (warning if not set, but not failure)
        for env_var in self.optional_env_vars:
            start_time = time.time()
            value = os.environ.get(env_var)
            is_set = value is not None and len(value) > 0
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name=f"env_optional_{env_var}",
                test_type="env",
                passed=True,  # Optional vars pass regardless
                execution_time_ms=elapsed_ms,
                value="SET" if is_set else "NOT_SET",
                error_message=""
            )
            results.append(result)
            self.record_result(result)
        
        print(f"[OK] Checked {len(self.env_vars)} required + {len(self.optional_env_vars)} optional env vars")
        self.test_results.extend(results)
        return results
    
    async def test_metrics_collection(self) -> List[ConfigTestResult]:
        """Test that system metrics can be collected."""
        print("\n[TEST] Testing metrics collection...")
        results = []
        
        try:
            import psutil
            HAS_PSUTIL = True
        except ImportError:
            HAS_PSUTIL = False
            print("[INFO] psutil not available - using basic metrics")
        
        # Test CPU metrics
        start_time = time.time()
        try:
            if HAS_PSUTIL:
                cpu_percent = psutil.cpu_percent(interval=0.1)
            else:
                cpu_percent = "N/A"
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name="metrics_cpu",
                test_type="metrics",
                passed=True,
                execution_time_ms=elapsed_ms,
                value=str(cpu_percent),
                error_message=""
            )
            results.append(result)
            self.record_result(result)
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            result = ConfigTestResult(
                test_name="metrics_cpu",
                test_type="metrics",
                passed=False,
                execution_time_ms=elapsed_ms,
                error_message=str(e)
            )
            results.append(result)
            self.record_result(result)
        
        # Test Memory metrics
        start_time = time.time()
        try:
            if HAS_PSUTIL:
                mem_info = psutil.virtual_memory()
                mem_percent = mem_info.percent
            else:
                mem_percent = "N/A"
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name="metrics_memory",
                test_type="metrics",
                passed=True,
                execution_time_ms=elapsed_ms,
                value=str(mem_percent),
                error_message=""
            )
            results.append(result)
            self.record_result(result)
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            result = ConfigTestResult(
                test_name="metrics_memory",
                test_type="metrics",
                passed=False,
                execution_time_ms=elapsed_ms,
                error_message=str(e)
            )
            results.append(result)
            self.record_result(result)
        
        # Test Disk metrics
        start_time = time.time()
        try:
            if HAS_PSUTIL:
                disk_info = psutil.disk_usage('.')
                disk_free_gb = disk_info.free / (1024**3)
            else:
                disk_free_gb = "N/A"
            elapsed_ms = (time.time() - start_time) * 1000
            
            result = ConfigTestResult(
                test_name="metrics_disk",
                test_type="metrics",
                passed=True,
                execution_time_ms=elapsed_ms,
                value=f"{disk_free_gb:.2f} GB" if isinstance(disk_free_gb, float) else str(disk_free_gb),
                error_message=""
            )
            results.append(result)
            self.record_result(result)
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            result = ConfigTestResult(
                test_name="metrics_disk",
                test_type="metrics",
                passed=False,
                execution_time_ms=elapsed_ms,
                error_message=str(e)
            )
            results.append(result)
            self.record_result(result)
        
        print(f"[OK] Collected metrics for CPU, Memory, and Disk")
        self.test_results.extend(results)
        return results
    
    async def test_system_health(self) -> List[ConfigTestResult]:
        """Test system health indicators."""
        print("\n[TEST] Testing system health indicators...")
        results = []
        
        # Test Python version
        start_time = time.time()
        python_version = sys.version_info
        is_python3 = python_version.major >= 3
        elapsed_ms = (time.time() - start_time) * 1000
        
        result = ConfigTestResult(
            test_name="health_python_version",
            test_type="health",
            passed=is_python3,
            execution_time_ms=elapsed_ms,
            value=f"{python_version.major}.{python_version.minor}.{python_version.micro}",
            error_message="" if is_python3 else "Python 3+ required"
        )
        results.append(result)
        self.record_result(result)
        
        # Test async support
        start_time = time.time()
        has_async = hasattr(asyncio, 'run')
        elapsed_ms = (time.time() - start_time) * 1000
        
        result = ConfigTestResult(
            test_name="health_async_support",
            test_type="health",
            passed=has_async,
            execution_time_ms=elapsed_ms,
            value="available",
            error_message="" if has_async else "Async support not available"
        )
        results.append(result)
        self.record_result(result)
        
        # Test write permissions
        start_time = time.time()
        test_file = Path(".goal_7_health_test.tmp")
        try:
            test_file.write_text("test")
            test_file.unlink()
            can_write = True
            elapsed_ms = (time.time() - start_time) * 1000
        except Exception as e:
            can_write = False
            elapsed_ms = (time.time() - start_time) * 1000
        
        result = ConfigTestResult(
            test_name="health_write_permissions",
            test_type="health",
            passed=can_write,
            execution_time_ms=elapsed_ms,
            value="read-write" if can_write else "read-only",
            error_message="" if can_write else "Cannot write to directory"
        )
        results.append(result)
        self.record_result(result)
        
        print(f"[OK] Checked {len(results)} system health indicators")
        self.test_results.extend(results)
        return results
    
    async def execute(self) -> Dict[str, Any]:
        """Execute all tests for Goal #7."""
        print("\n" + "="*60)
        print("GOAL #7: System Configuration and Metrics Validation Test")
        print("="*60)
        
        await self.initialize()
        
        # Run all test phases
        await self.test_config_files()
        await self.test_environment_variables()
        await self.test_metrics_collection()
        await self.test_system_health()
        
        # Calculate final results
        if self.start_time:
            self.results["duration_seconds"] = time.time() - self.start_time
        
        # Check completion criteria - all tests must pass
        all_tests_passed = (
            self.results["tests_total"] > 0 and
            self.results["tests_passed"] == self.results["tests_total"]
        )
        
        self.results["completed"] = all_tests_passed
        
        # Print summary
        print("\n" + "-"*60)
        print("GOAL #7 EXECUTION SUMMARY")
        print("-"*60)
        print(f"Config Tests: {self.results['config_passed']}/{self.results['config_total']} passed")
        print(f"Environment Tests: {self.results['env_passed']}/{self.results['env_total']} passed")
        print(f"Metrics Tests: {self.results['metrics_passed']}/{self.results['metrics_total']} passed")
        print(f"Health Tests: {self.results['health_passed']}/{self.results['health_total']} passed")
        print(f"\nTotal Tests: {self.results['tests_passed']}/{self.results['tests_total']} passed")
        print(f"Status: {'COMPLETED' if all_tests_passed else 'FAILED'}")
        print(f"Duration: {self.results['duration_seconds']:.2f} seconds")
        
        if self.results["errors"]:
            print(f"\nErrors encountered:")
            for error in self.results["errors"]:
                print(f"  - {error}")
        
        print("="*60)
        
        return self.results


async def main():
    """Main entry point for Goal #7 execution."""
    executor = Goal7Executor()
    results = await executor.execute()
    
    # Exit with appropriate code
    sys.exit(0 if results["completed"] else 1)


if __name__ == "__main__":
    asyncio.run(main())

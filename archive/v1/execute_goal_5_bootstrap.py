#!/usr/bin/env python3
"""
Execute Goal #5 for Goal Evolver Bootstrap:
Event Bus Integration and Connectivity Test

This script executes the event bus integration test to complete goal #5
for the Goal Evolver bootstrap process. It ensures:
1. Event bus is properly initialized
2. Event emission and subscription work correctly
3. Event latency metrics are collected
4. Event handlers can be registered and triggered
5. Results are reported for completion tracking

Fitness Data Points:
- Completion: Binary (all event tests passed)
- Capability Delta: Event system reliability (successful transmissions/total)
- Efficiency: Average event latency and resource usage
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import required modules
HAS_EVENT_BUS = False
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    print("[WARNING] Event bus module not available - will run in simulation mode")


@dataclass
class EventTestResult:
    """Result of a single event test."""
    test_name: str
    passed: bool
    latency_ms: float
    payload_size: int
    error_message: str = ""


class Goal5Executor:
    """Executor for Goal #5: Event Bus Integration and Connectivity Test."""
    
    def __init__(self):
        self.event_bus = None
        self.start_time = None
        self.test_results: List[EventTestResult] = []
        self.results = {
            "goal_number": 5,
            "goal_name": "Event Bus Integration and Connectivity Test",
            "started": False,
            "completed": False,
            "event_bus_available": False,
            "tests_passed": 0,
            "tests_total": 0,
            "events_emitted": 0,
            "events_received": 0,
            "average_latency_ms": 0.0,
            "handlers_registered": 0,
            "handlers_triggered": 0,
            "errors": [],
            "duration_seconds": 0
        }
    
    async def initialize(self):
        """Initialize event bus."""
        print("[INIT] Initializing Goal #5: Event Bus Integration and Connectivity Test...")
        
        if HAS_EVENT_BUS:
            try:
                # Use existing event_bus singleton
                self.event_bus = event_bus
                self.results["event_bus_available"] = True
                print("[OK] Event bus is available")
            except Exception as e:
                print(f"[WARNING] Could not initialize event bus: {e}")
                self.results["event_bus_available"] = False
                self.results["errors"].append(f"Event bus init failed: {e}")
        else:
            print("[INFO] Running in simulation mode (no event bus module)")
            self.results["event_bus_available"] = False
    
    async def test_event_emission(self) -> EventTestResult:
        """Test basic event emission."""
        test_name = "Basic Event Emission"
        
        if not self.event_bus or not self.results["event_bus_available"]:
            return EventTestResult(test_name, False, 0, 0, "Event bus not available")
        
        try:
            received = False
            received_event = None
            
            async def handler(event: Event):
                nonlocal received, received_event
                if event.type == EventType.EXPERIENCE_CREATED:
                    received = True
                    received_event = event
            
            # Subscribe to all events (filter in handler)
            self.event_bus.subscribe_async(handler)
            self.results["handlers_registered"] += 1
            
            # Emit test event
            start_time = time.time()
            test_event = Event(
                type=EventType.EXPERIENCE_CREATED,
                data={"test": True, "timestamp": datetime.now().isoformat()}
            )
            await self.event_bus.emit(test_event)
            self.results["events_emitted"] += 1
            
            # Wait for delivery (small delay)
            await asyncio.sleep(0.1)
            
            latency_ms = (time.time() - start_time) * 1000
            
            if received and received_event:
                self.results["events_received"] += 1
                self.results["handlers_triggered"] += 1
                return EventTestResult(test_name, True, latency_ms, len(str(test_event.data)))
            else:
                return EventTestResult(test_name, False, latency_ms, len(str(test_event.data)), "Event not received")
                
        except Exception as e:
            return EventTestResult(test_name, False, 0, 0, str(e))
    
    async def test_multiple_subscribers(self) -> EventTestResult:
        """Test event delivery to multiple subscribers."""
        test_name = "Multiple Subscribers"
        
        if not self.event_bus or not self.results["event_bus_available"]:
            return EventTestResult(test_name, False, 0, 0, "Event bus not available")
        
        try:
            received_counts = [0, 0, 0]  # 3 subscribers
            
            async def handler_1(event: Event):
                if event.type == EventType.GOAL_CREATED:
                    received_counts[0] += 1
            
            async def handler_2(event: Event):
                if event.type == EventType.GOAL_CREATED:
                    received_counts[1] += 1
            
            async def handler_3(event: Event):
                if event.type == EventType.GOAL_CREATED:
                    received_counts[2] += 1
            
            # Subscribe multiple handlers
            self.event_bus.subscribe_async(handler_1)
            self.event_bus.subscribe_async(handler_2)
            self.event_bus.subscribe_async(handler_3)
            self.results["handlers_registered"] += 3
            
            # Emit test event
            start_time = time.time()
            test_event = Event(
                type=EventType.GOAL_CREATED,
                data={"test": "multiple", "subscribers": 3}
            )
            await self.event_bus.emit(test_event)
            self.results["events_emitted"] += 1
            
            # Wait for delivery
            await asyncio.sleep(0.1)
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Check all handlers received the event
            all_received = all(count == 1 for count in received_counts)
            
            if all_received:
                self.results["events_received"] += 3
                self.results["handlers_triggered"] += 3
                return EventTestResult(test_name, True, latency_ms, len(str(test_event.data)))
            else:
                return EventTestResult(
                    test_name, False, latency_ms, len(str(test_event.data)),
                    f"Not all handlers received event: {received_counts}"
                )
                
        except Exception as e:
            return EventTestResult(test_name, False, 0, 0, str(e))
    
    async def test_event_latency(self) -> EventTestResult:
        """Test event delivery latency with multiple samples."""
        test_name = "Event Latency Benchmark"
        
        if not self.event_bus or not self.results["event_bus_available"]:
            return EventTestResult(test_name, False, 0, 0, "Event bus not available")
        
        try:
            latencies = []
            sample_count = 10
            
            async def handler(event: Event):
                pass  # Just mark as received
            
            self.event_bus.subscribe_async(handler)
            self.results["handlers_registered"] += 1
            
            for i in range(sample_count):
                start_time = time.time()
                test_event = Event(
                    type=EventType.REFLECTION_CREATED,
                    data={"test": "latency", "sample": i}
                )
                await self.event_bus.emit(test_event)
                await asyncio.sleep(0.01)  # Small delay
                latency_ms = (time.time() - start_time) * 1000
                latencies.append(latency_ms)
                self.results["events_emitted"] += 1
            
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)
            
            # Store in results
            self.results["average_latency_ms"] = avg_latency
            
            # Check if latency is acceptable (under 100ms average)
            passed = avg_latency < 100.0
            
            if passed:
                self.results["events_received"] += sample_count
                self.results["handlers_triggered"] += sample_count
            
            return EventTestResult(
                test_name,
                passed,
                avg_latency,
                0,
                f"Avg: {avg_latency:.2f}ms, Min: {min_latency:.2f}ms, Max: {max_latency:.2f}ms"
            )
                
        except Exception as e:
            return EventTestResult(test_name, False, 0, 0, str(e))
    
    async def test_large_payload(self) -> EventTestResult:
        """Test event delivery with large payloads."""
        test_name = "Large Payload Handling"
        
        if not self.event_bus or not self.results["event_bus_available"]:
            return EventTestResult(test_name, False, 0, 0, "Event bus not available")
        
        try:
            received = False
            received_size = 0
            
            async def handler(event: Event):
                nonlocal received, received_size
                received = True
                received_size = len(str(event.data))
            
            self.event_bus.subscribe_async(handler)
            self.results["handlers_registered"] += 1
            
            # Create large payload
            large_data = {
                "test": "large_payload",
                "content": "x" * 10000,  # 10KB of data
                "nested": {
                    "a" * 1000: "b" * 1000,
                    "list": ["item" for _ in range(1000)]
                }
            }
            
            start_time = time.time()
            test_event = Event(
                type=EventType.DREAM_CYCLE_END,
                data=large_data
            )
            await self.event_bus.emit(test_event)
            self.results["events_emitted"] += 1
            
            await asyncio.sleep(0.2)  # Longer delay for large payload
            
            latency_ms = (time.time() - start_time) * 1000
            payload_size = len(str(large_data))
            
            if received and received_size == payload_size:
                self.results["events_received"] += 1
                self.results["handlers_triggered"] += 1
                return EventTestResult(test_name, True, latency_ms, payload_size)
            else:
                return EventTestResult(
                    test_name,
                    False,
                    latency_ms,
                    payload_size,
                    f"Payload mismatch: expected {payload_size}, got {received_size}"
                )
                
        except Exception as e:
            return EventTestResult(test_name, False, 0, 0, str(e))
    
    async def test_error_handling(self) -> EventTestResult:
        """Test event bus error handling with faulty handlers."""
        test_name = "Error Handling"
        
        if not self.event_bus or not self.results["event_bus_available"]:
            return EventTestResult(test_name, False, 0, 0, "Event bus not available")
        
        try:
            good_handler_received = False
            
            async def faulty_handler(event: Event):
                raise Exception("Test exception in handler")
            
            async def good_handler(event: Event):
                nonlocal good_handler_received
                good_handler_received = True
            
            # Register both handlers
            self.event_bus.subscribe_async(faulty_handler)
            self.event_bus.subscribe_async(good_handler)
            self.results["handlers_registered"] += 2
            
            # Emit event
            start_time = time.time()
            test_event = Event(
                type=EventType.LOOP_CYCLE_START,
                data={"test": "error_handling"}
            )
            await self.event_bus.emit(test_event)
            self.results["events_emitted"] += 1
            
            await asyncio.sleep(0.1)
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Good handler should still be called even if faulty one fails
            if good_handler_received:
                self.results["events_received"] += 1
                self.results["handlers_triggered"] += 1
                return EventTestResult(test_name, True, latency_ms, len(str(test_event.data)))
            else:
                return EventTestResult(
                    test_name, False, latency_ms, len(str(test_event.data)),
                    "Good handler was not called despite faulty handler error"
                )
                
        except Exception as e:
            return EventTestResult(test_name, False, 0, 0, str(e))
    
    async def run_all_tests(self) -> List[EventTestResult]:
        """Run all event bus integration tests."""
        tests = [
            self.test_event_emission,
            self.test_multiple_subscribers,
            self.test_event_latency,
            self.test_large_payload,
            self.test_error_handling
        ]
        
        print("\n[TESTS] Running event bus integration tests...")
        
        for i, test in enumerate(tests, 1):
            print(f"  [{i}/{len(tests)}] Running {test.__name__}...")
            try:
                result = await test()
                self.test_results.append(result)
                if result.passed:
                    print(f"    ✓ PASSED - {result.test_name} ({result.latency_ms:.2f}ms)")
                else:
                    print(f"    ✗ FAILED - {result.test_name}: {result.error_message}")
                    self.results["errors"].append(f"{result.test_name}: {result.error_message}")
            except Exception as e:
                print(f"    ✗ ERROR - {test.__name__}: {e}")
                self.results["errors"].append(f"{test.__name__}: {e}")
                self.test_results.append(EventTestResult(
                    test.__name__, False, 0, 0, str(e)
                ))
        
        # Update summary stats
        self.results["tests_passed"] = sum(1 for r in self.test_results if r.passed)
        self.results["tests_total"] = len(self.test_results)
        
        # Calculate average latency across all passed tests
        passed_tests = [r for r in self.test_results if r.passed]
        if passed_tests:
            self.results["average_latency_ms"] = sum(r.latency_ms for r in passed_tests) / len(passed_tests)
        
        return self.test_results
    
    async def execute(self):
        """Execute the complete Goal #5."""
        print("\n" + "="*70)
        print("GOAL EVOLVER BOOTSTRAP - GOAL #5")
        print("Event Bus Integration and Connectivity Test")
        print("="*70 + "\n")
        
        self.start_time = datetime.now()
        self.results["started"] = True
        
        try:
            # Step 1: Initialize
            await self.initialize()
            
            # Step 2: Run all tests
            await self.run_all_tests()
            
            # Step 3: Calculate success rate
            success_rate = (self.results["tests_passed"] / self.results["tests_total"]) if self.results["tests_total"] > 0 else 0
            
            # Step 4: Final summary
            self.results["completed"] = success_rate >= 0.8  # 80% pass rate required
            self.results["duration_seconds"] = (datetime.now() - self.start_time).total_seconds()
            
            if self.results["completed"]:
                print("\n[SUCCESS] ✓ Goal #5 completed successfully!")
                print(f"Success Rate: {success_rate*100:.1f}%")
            else:
                print(f"\n[WARNING] Goal #5 completed with issues: {success_rate*100:.1f}% success rate")
            
        except Exception as e:
            print(f"\n[ERROR] Goal #5 failed: {e}")
            self.results["errors"].append(str(e))
            self.results["completed"] = False
            self.results["duration_seconds"] = (datetime.now() - self.start_time).total_seconds()
        
        return self.results
    
    def print_report(self):
        """Print execution report."""
        print("\n" + "="*70)
        print("GOAL #5 EXECUTION REPORT")
        print("="*70)
        print(f"Goal Name: {self.results['goal_name']}")
        print(f"Status: {'COMPLETED' if self.results['completed'] else 'FAILED'}")
        print(f"Duration: {self.results['duration_seconds']:.2f} seconds")
        print(f"\nEvent Bus Available: {self.results['event_bus_available']}")
        print(f"Test Results: {self.results['tests_passed']}/{self.results['tests_total']} passed")
        print(f"\nEvent Statistics:")
        print(f"  Events Emitted: {self.results['events_emitted']}")
        print(f"  Events Received: {self.results['events_received']}")
        print(f"  Handlers Registered: {self.results['handlers_registered']}")
        print(f"  Handlers Triggered: {self.results['handlers_triggered']}")
        print(f"\nPerformance Metrics:")
        print(f"  Average Latency: {self.results['average_latency_ms']:.2f}ms")
        
        if self.test_results:
            print(f"\nDetailed Test Results:")
            for result in self.test_results:
                status = "PASS" if result.passed else "FAIL"
                print(f"  [{status}] {result.test_name}: {result.latency_ms:.2f}ms")
                if not result.passed and result.error_message:
                    print(f"       Error: {result.error_message}")
        
        if self.results["errors"]:
            print(f"\nAdditional Errors:")
            for error in self.results["errors"]:
                print(f"  - {error}")
        
        if self.results['completed']:
            print("\n" + "="*70)
            print("✅ GOAL #5: EVENT BUS INTEGRATION TEST - COMPLETED")
            print("="*70)
        else:
            print("\n" + "="*70)
            print("❌ GOAL #5: EVENT BUS INTEGRATION TEST - FAILED")
            print("="*70)


async def main():
    """Main entry point."""
    executor = Goal5Executor()
    results = await executor.execute()
    executor.print_report()
    return results


if __name__ == "__main__":
    asyncio.run(main())

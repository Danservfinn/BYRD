#!/usr/bin/env python3
"""
Execution Failure Patterns Documentation

This module catalogs and documents execution failure patterns in the BYRD system
for human diagnosis and troubleshooting. It provides a comprehensive reference for
identifying, understanding, and resolving common failure modes.

Usage:
    # Import as a reference module
    import execution_failure_patterns as efp
    
    # View all documented patterns
    print(efp.get_all_patterns())
    
    # Get diagnostic guidance for a specific error
    guidance = efp.get_diagnostic_guidance("Neo4jConnectionError")
    print(guidance)
    
    # Check if an error matches a known pattern
    pattern = efp.match_error_pattern("WebSocket connection failed")
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable
from enum import Enum
import re


class FailureSeverity(Enum):
    """Severity levels for failure patterns."""
    CRITICAL = "CRITICAL"      # System-breaking, immediate attention required
    HIGH = "HIGH"             # Major functionality degraded
    MEDIUM = "MEDIUM"         # Partial functionality affected
    LOW = "LOW"               # Minor issues, informational


class FailureCategory(Enum):
    """Categories of failure patterns."""
    DATABASE = "DATABASE"           # Neo4j/graph database issues
    NETWORK = "NETWORK"             # WebSocket, HTTP, connection issues
    LLM_INTEGRATION = "LLM"         # LLM API, prompt, response issues
    MEMORY_MANAGEMENT = "MEMORY"    # Orphan nodes, memory leaks
    CONCURRENCY = "CONCURRENCY"     # Race conditions, deadlock
    RESOURCE_EXHAUSTION = "RESOURCE" # CPU, memory, rate limits
    DATA_CORRUPTION = "DATA"        # Invalid states, corrupted data
    CONFIGURATION = "CONFIG"        # Misconfiguration, missing settings
    EXTERNAL_SERVICE = "EXTERNAL"   # Third-party service failures
    UNKNOWN = "UNKNOWN"             # Unclassified failures


@dataclass
class FailurePattern:
    """A documented execution failure pattern."""
    name: str
    description: str
    category: FailureCategory
    severity: FailureSeverity
    
    # Detection patterns
    error_signatures: List[str] = field(default_factory=list)
    log_patterns: List[str] = field(default_factory=list)
    
    # Diagnostic information
    common_causes: List[str] = field(default_factory=list)
    diagnostic_steps: List[str] = field(default_factory=list)
    resolution_strategies: List[str] = field(default_factory=list)
    
    # Related files/components
    affected_modules: List[str] = field(default_factory=list)
    related_patterns: List[str] = field(default_factory=list)
    
    def matches(self, error_message: str) -> bool:
        """Check if an error message matches this pattern."""
        for pattern in self.error_signatures:
            if re.search(pattern, error_message, re.IGNORECASE):
                return True
        return False
    
    def get_diagnostic_summary(self) -> str:
        """Get a formatted diagnostic summary."""
        return f"""
=== {self.name} ===
Category: {self.category.value} | Severity: {self.severity.value}

Description:
{self.description}

Common Causes:
""" + "\n".join(f"  • {cause}" for cause in self.common_causes) + f"""

Diagnostic Steps:
""" + "\n".join(f"  {i+1}. {step}" for i, step in enumerate(self.diagnostic_steps)) + f"""

Resolution Strategies:
""" + "\n".join(f"  • {strat}" for strat in self.resolution_strategies) + "\n"


# =============================================================================
# DOCUMENTED FAILURE PATTERNS
# =============================================================================

DATABASE_PATTERNS = [
    FailurePattern(
        name="Neo4jConnectionRefused",
        description="Cannot establish connection to Neo4j database server",
        category=FailureCategory.DATABASE,
        severity=FailureSeverity.CRITICAL,
        error_signatures=[
            r'neo4j.*connection.*refused',
            r'failed to establish connection.*neo4j',
            r'neo4j.*unavailable',
        ],
        common_causes=[
            "Neo4j service not running",
            "Incorrect connection settings (host, port)",
            "Network firewall blocking connection",
            "Neo4j server overloaded or restarting",
        ],
        diagnostic_steps=[
            "Check if Neo4j service is running: 'systemctl status neo4j'",
            "Verify connection settings in .env file",
            "Test network connectivity: 'telnet localhost 7687'",
            "Check Neo4j logs for server-side errors",
        ],
        resolution_strategies=[
            "Start Neo4j service if stopped",
            "Verify and correct NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD in .env",
            "Check firewall rules and open port 7687",
            "Restart Neo4j service if in bad state",
        ],
        affected_modules=["atomic_cypher_query.py", "coupling_tracker.py"],
    ),
    
    FailurePattern(
        name="Neo4jAuthFailed",
        description="Authentication failure when connecting to Neo4j",
        category=FailureCategory.DATABASE,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'neo4j.*authentication.*failed',
            r'unauthorized.*neo4j',
            r'invalid.*credentials.*neo4j',
        ],
        common_causes=[
            "Incorrect username or password in configuration",
            "User account expired or disabled",
            "Password changed but not updated in config",
        ],
        diagnostic_steps=[
            "Verify NEO4J_USER and NEO4J_PASSWORD in .env file",
            "Test credentials manually using neo4j console",
            "Check if user account is active in Neo4j",
        ],
        resolution_strategies=[
            "Update credentials in .env file",
            "Reset Neo4j user password if needed",
            "Create new Neo4j user with correct permissions",
        ],
        affected_modules=["atomic_cypher_query.py"],
    ),
    
    FailurePattern(
        name="CypherQuerySyntaxError",
        description="Invalid Cypher query syntax causing database errors",
        category=FailureCategory.DATABASE,
        severity=FailureSeverity.MEDIUM,
        error_signatures=[
            r'cypher.*syntax.*error',
            r'invalid.*cypher',
            r'query.*syntax.*error',
        ],
        common_causes=[
            "Typo in Cypher query construction",
            "Missing or extra parentheses, quotes, or commas",
            "Using deprecated Cypher syntax",
            "Query contains invalid variable names",
        ],
        diagnostic_steps=[
            "Extract the exact Cypher query from error message",
            "Validate query syntax using Neo4j browser",
            "Check for proper escaping of strings and parameters",
            "Review code that constructs the query dynamically",
        ],
        resolution_strategies=[
            "Fix syntax error in the query",
            "Add proper parameterization to prevent injection",
            "Update to current Cypher syntax version",
            "Add query validation before execution",
        ],
        affected_modules=["atomic_cypher_query.py"],
    ),
]

NETWORK_PATTERNS = [
    FailurePattern(
        name="WebSocketConnectionFailed",
        description="WebSocket connection to remote service failed",
        category=FailureCategory.NETWORK,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'websocket.*connection.*failed',
            r'websocket.*handshake.*error',
            r'websocket.*closed.*unexpectedly',
        ],
        common_causes=[
            "WebSocket server not running",
            "Incorrect WebSocket URL or endpoint",
            "Network connectivity issues",
            "WebSocket protocol version mismatch",
            "SSL/TLS certificate issues",
        ],
        diagnostic_steps=[
            "Verify WebSocket server is accessible",
            "Check WebSocket URL configuration",
            "Test network path to WebSocket server",
            "Review WebSocket handshake logs",
        ],
        resolution_strategies=[
            "Verify WebSocket endpoint URL is correct",
            "Ensure WebSocket server is running",
            "Check network connectivity and firewall rules",
            "Update WebSocket client library if needed",
        ],
        affected_modules=["elevenlabs_voice.py", "parallel_observation_integration.py"],
    ),
    
    FailurePattern(
        name="HTTPTimeout",
        description="HTTP request timed out waiting for response",
        category=FailureCategory.NETWORK,
        severity=FailureSeverity.MEDIUM,
        error_signatures=[
            r'connection.*timeout',
            r'read.*timeout',
            r'http.*timeout',
            r'request.*timed.*out',
        ],
        common_causes=[
            "Remote server slow to respond",
            "Network latency or congestion",
            "Request payload too large",
            "Timeout value too aggressive",
        ],
        diagnostic_steps=[
            "Check if remote service is experiencing issues",
            "Measure actual network latency",
            "Review request size and complexity",
            "Check current timeout configuration",
        ],
        resolution_strategies=[
            "Increase timeout value for slow operations",
            "Implement retry logic with exponential backoff",
            "Optimize request to reduce processing time",
            "Add circuit breaker to prevent cascading failures",
        ],
        affected_modules=["aitmpl_client.py", "elevenlabs_voice.py"],
    ),
]

LLM_INTEGRATION_PATTERNS = [
    FailurePattern(
        name="LLMAPIRateLimitExceeded",
        description="Rate limit exceeded for LLM API calls",
        category=FailureCategory.LLM_INTEGRATION,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'rate.*limit.*exceeded',
            r'too.*many.*requests',
            r'429.*rate.*limit',
            r'api.*quota.*exceeded',
        ],
        common_causes=[
            "Too many requests in short time period",
            "Concurrent requests exceeding quota",
            "Insufficient API tier/plan",
            "Token usage limit reached",
        ],
        diagnostic_steps=[
            "Check API usage dashboard for current quota",
            "Review request rate and concurrency settings",
            "Identify high-frequency API calls",
            "Check time-based vs token-based limits",
        ],
        resolution_strategies=[
            "Implement rate limiting with token bucket algorithm",
            "Add request queuing and throttling",
            "Upgrade API tier if consistently hitting limits",
            "Cache LLM responses where appropriate",
            "Use constraint routing to limit parallel calls",
        ],
        affected_modules=["create_zai_rate_limit_constraint.py", "constraint_aware_router.py"],
    ),
    
    FailurePattern(
        name="LLMResponseParsingFailed",
        description="Failed to parse or validate LLM response",
        category=FailureCategory.LLM_INTEGRATION,
        severity=FailureSeverity.MEDIUM,
        error_signatures=[
            r'failed.*to.*parse.*response',
            r'invalid.*llm.*response',
            r'json.*decode.*error',
            r'response.*validation.*failed',
        ],
        common_causes=[
            "LLM returned malformed JSON",
            "Response format changed from expected schema",
            "LLM hallucinated invalid structure",
            "Prompt not specific enough about format",
        ],
        diagnostic_steps=[
            "Capture and inspect the raw LLM response",
            "Compare response to expected schema",
            "Review prompt for format instructions",
            "Check if LLM model was changed",
        ],
        resolution_strategies=[
            "Improve prompt with explicit format examples",
            "Add response validation and error handling",
            "Implement retry with more specific prompts",
            "Use structured output formats if available",
            "Add fallback parsing logic for malformed responses",
        ],
        affected_modules=["dreamer.py", "agent_coder.py", "byrd.py"],
    ),
    
    FailurePattern(
        name="LLMContextLengthExceeded",
        description="Input or output exceeds LLM context window",
        category=FailureCategory.LLM_INTEGRATION,
        severity=FailureSeverity.MEDIUM,
        error_signatures=[
            r'context.*length.*exceeded',
            r'token.*limit.*exceeded',
            r'maximum.*context.*length',
            r'too.*many.*tokens',
        ],
        common_causes=[
            "Input prompt too long",
            "Accumulated conversation history exceeds limit",
            "LLM model has smaller context window than expected",
            "Not summarizing/trimming history properly",
        ],
        diagnostic_steps=[
            "Count tokens in input prompt",
            "Review conversation history accumulation",
            "Check which LLM model is being used",
            "Identify largest inputs being sent",
        ],
        resolution_strategies=[
            "Implement conversation summarization",
            "Use sliding window for recent context",
            "Switch to model with larger context window",
            "Pre-process and condense input data",
            "Chunk large inputs into smaller pieces",
        ],
        affected_modules=["dreamer.py", "byrd.py"],
    ),
]

MEMORY_MANAGEMENT_PATTERNS = [
    FailurePattern(
        name="OrphanNodeAccumulation",
        description="Graph nodes accumulating without proper relationships",
        category=FailureCategory.MEMORY_MANAGEMENT,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'orphan.*node',
            r'node.*without.*relationship',
            r'dangling.*node',
        ],
        common_causes=[
            "Relationships deleted but nodes not cleaned up",
            "Failed transaction leaving partial state",
            "Missing cleanup after observation cycles",
            "Bulk operations not creating relationships",
        ],
        diagnostic_steps=[
            "Query for nodes with no relationships",
            "Check dump_orphan_nodes.py output",
            "Review transaction commit patterns",
            "Identify orphan creation hotspots",
        ],
        resolution_strategies=[
            "Run periodic orphan node cleanup",
            "Add relationship validation on node creation",
            "Implement proper transaction rollback",
            "Use create_orphan_relationship.py for remediation",
        ],
        affected_modules=["dump_orphan_nodes.py", "create_orphan_relationship.py", "coupling_tracker.py"],
    ),
    
    FailurePattern(
        name="MemoryLeak",
        description="Gradual increase in memory usage over time",
        category=FailureCategory.MEMORY_MANAGEMENT,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'memory.*usage.*high',
            r'out.*of.*memory',
            r'memory.*error',
        ],
        common_causes=[
            "Unclosed database connections",
            "Growing data structures without cleanup",
            "Event listeners not being removed",
            "Caches growing without bounds",
            "Circular references preventing garbage collection",
        ],
        diagnostic_steps=[
            "Monitor memory usage over time",
            "Use memory profiler to identify growth sources",
            "Check for unclosed resources (files, connections)",
            "Review cache implementation",
        ],
        resolution_strategies=[
            "Implement proper resource cleanup with context managers",
            "Add cache eviction policies",
            "Remove event listeners when no longer needed",
            "Break circular references explicitly",
            "Add periodic memory cleanup routines",
        ],
        affected_modules=["dreamer.py", "parallel_observation_integration.py"],
    ),
]

CONCURRENCY_PATTERNS = [
    FailurePattern(
        name="RaceCondition",
        description="Concurrent operations causing inconsistent state",
        category=FailureCategory.CONCURRENCY,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'race.*condition',
            r'concurrent.*modification',
            r'inconsistent.*state',
        ],
        common_causes=[
            "Multiple threads/async tasks modifying shared state",
            "Lack of proper locking or synchronization",
            "Non-atomic read-modify-write operations",
        ],
        diagnostic_steps=[
            "Review shared data access patterns",
            "Check for missing locks on shared resources",
            "Look for non-atomic operations",
            "Enable logging to identify concurrent access",
        ],
        resolution_strategies=[
            "Add proper locking (asyncio.Lock, threading.Lock)",
            "Use atomic operations where possible",
            "Implement transactional updates",
            "Consider using message queues for serialization",
        ],
        affected_modules=["parallel_observation_integration.py", "dual_instance_manager.py"],
    ),
    
    FailurePattern(
        name="Deadlock",
        description="Processes waiting on each other, preventing progress",
        category=FailureCategory.CONCURRENCY,
        severity=FailureSeverity.CRITICAL,
        error_signatures=[
            r'deadlock',
            r'lock.*timeout',
            r'hanging.*forever',
        ],
        common_causes=[
            "Circular lock acquisition order",
            "Lock held too long during operation",
            "Multiple locks acquired in inconsistent order",
        ],
        diagnostic_steps=[
            "Identify all locks in the system",
            "Check lock acquisition order in different code paths",
            "Look for operations holding locks while calling other code",
            "Use thread dumps or asyncio debug to find blocked tasks",
        ],
        resolution_strategies=[
            "Establish consistent lock ordering across codebase",
            "Minimize lock holding time",
            "Use lock timeouts to detect and recover",
            "Consider lock-free data structures where possible",
        ],
        affected_modules=["parallel_observation_integration.py", "compounding_orchestrator.py"],
    ),
]

RESOURCE_EXHAUSTION_PATTERNS = [
    FailurePattern(
        name="CPUExhaustion",
        description="System CPU at 100%, causing slowdown or failure",
        category=FailureCategory.RESOURCE_EXHAUSTION,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'cpu.*usage.*high',
            r'cpu.*exhausted',
            r'system.*slow',
        ],
        common_causes=[
            "Infinite loops or tight loops without yielding",
            "Computationally intensive operations",
            "Too many concurrent processes",
            "Inefficient algorithms",
        ],
        diagnostic_steps=[
            "Monitor CPU usage per process",
            "Profile code to find hotspots",
            "Check for tight loops or blocking operations",
            "Review concurrency levels",
        ],
        resolution_strategies=[
            "Add asyncio.sleep() in tight loops to yield control",
            "Optimize expensive algorithms",
            "Limit concurrent operations",
            "Offload heavy computation to separate workers",
        ],
        affected_modules=["dreamer.py", "agi_runner.py"],
    ),
    
    FailurePattern(
        name="DiskSpaceExhausted",
        description="No disk space available for writes",
        category=FailureCategory.RESOURCE_EXHAUSTION,
        severity=FailureSeverity.CRITICAL,
        error_signatures=[
            r'no.*space.*left',
            r'disk.*full',
            r'cannot.*write.*disk',
        ],
        common_causes=[
            "Log files growing too large",
            "Database files consuming space",
            "Cache files not being cleaned",
            "Temporary files not removed",
        ],
        diagnostic_steps=[
            "Check disk usage with 'df -h'",
            "Find large directories with 'du -sh *'",
            "Review log rotation settings",
            "Check cache directories",
        ],
        resolution_strategies=[
            "Implement log rotation and cleanup",
            "Add disk usage monitoring",
            "Clean up old cache and temp files",
            "Set up automated cleanup scripts",
        ],
        affected_modules=["clean_utils.py", "byrd.py"],
    ),
]

DATA_CORRUPTION_PATTERNS = [
    FailurePattern(
        name="StateInconsistency",
        description="Internal system state is inconsistent with reality",
        category=FailureCategory.DATA_CORRUPTION,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'inconsistent.*state',
            r'state.*mismatch',
            r'invalid.*state',
        ],
        common_causes=[
            "Partial transaction failure",
            "Concurrent modification without locking",
            "Cached data out of sync with database",
            "Error in state transition logic",
        ],
        diagnostic_steps=[
            "Compare database state with in-memory state",
            "Review transaction boundaries",
            "Check for missing state updates",
            "Validate state machine transitions",
        ],
        resolution_strategies=[
            "Add state validation checkpoints",
            "Implement proper transaction handling",
            "Add state reconciliation routines",
            "Use versioned state with conflict resolution",
        ],
        affected_modules=["coupling_tracker.py", "constraint_routing_integration.py"],
    ),
]

CONFIGURATION_PATTERNS = [
    FailurePattern(
        name="MissingConfiguration",
        description="Required configuration value not set",
        category=FailureCategory.CONFIGURATION,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'missing.*config',
            r'required.*environment.*variable',
            r'key.*not.*found',
        ],
        common_causes=[
            "Environment variable not defined",
            ".env file missing or incomplete",
            "Configuration file not loaded",
            "Default values missing in code",
        ],
        diagnostic_steps=[
            "Check .env file exists and has correct values",
            "Verify environment is properly loaded",
            "Review code for missing defaults",
            "Check .env.example for required variables",
        ],
        resolution_strategies=[
            "Add missing environment variables to .env",
            "Provide sensible defaults in code",
            "Add configuration validation at startup",
            "Document all required configuration",
        ],
        affected_modules=["byrd.py", "deploy_huggingface.py"],
    ),
    
    FailurePattern(
        name="InvalidConfigurationValue",
        description="Configuration value is present but invalid",
        category=FailureCategory.CONFIGURATION,
        severity=FailureSeverity.MEDIUM,
        error_signatures=[
            r'invalid.*config.*value',
            r'configuration.*error',
            r'malformed.*setting',
        ],
        common_causes=[
            "Wrong type for configuration value",
            "Value outside valid range",
            "Invalid enum or option value",
            "Malformed URL or path",
        ],
        diagnostic_steps=[
            "Check value type matches expected format",
            "Verify value is within valid range",
            "Check documentation for valid options",
            "Validate URLs and paths are correct",
        ],
        resolution_strategies=[
            "Correct configuration value",
            "Add type validation for configuration",
            "Provide examples in .env.example",
            "Add configuration schema validation",
        ],
        affected_modules=["byrd.py"],
    ),
]

EXTERNAL_SERVICE_PATTERNS = [
    FailurePattern(
        name="ThirdPartyServiceUnavailable",
        description="External service is down or unreachable",
        category=FailureCategory.EXTERNAL_SERVICE,
        severity=FailureSeverity.HIGH,
        error_signatures=[
            r'service.*unavailable',
            r'503.*service.*unavailable',
            r'external.*service.*error',
        ],
        common_causes=[
            "Third-party service experiencing outage",
            "Service deprecated or changed endpoints",
            "API key invalidated or expired",
            "Service maintenance window",
        ],
        diagnostic_steps=[
            "Check external service status page",
            "Test service independently",
            "Verify API key is valid",
            "Check for service announcements",
        ],
        resolution_strategies=[
            "Wait for service recovery if temporary outage",
            "Implement fallback/retry logic",
            "Update to new API version if deprecated",
            "Refresh API key if expired",
            "Add circuit breaker to prevent cascade",
        ],
        affected_modules=["elevenlabs_voice.py", "aitmpl_client.py"],
    ),
]

# =============================================================================
# PATTERN REGISTRY
# =============================================================================

ALL_PATTERNS = (
    DATABASE_PATTERNS +
    NETWORK_PATTERNS +
    LLM_INTEGRATION_PATTERNS +
    MEMORY_MANAGEMENT_PATTERNS +
    CONCURRENCY_PATTERNS +
    RESOURCE_EXHAUSTION_PATTERNS +
    DATA_CORRUPTION_PATTERNS +
    CONFIGURATION_PATTERNS +
    EXTERNAL_SERVICE_PATTERNS
)

PATTERNS_BY_CATEGORY: Dict[FailureCategory, List[FailurePattern]] = {}
for pattern in ALL_PATTERNS:
    if pattern.category not in PATTERNS_BY_CATEGORY:
        PATTERNS_BY_CATEGORY[pattern.category] = []
    PATTERNS_BY_CATEGORY[pattern.category].append(pattern)

PATTERNS_BY_SEVERITY: Dict[FailureSeverity, List[FailurePattern]] = {}
for pattern in ALL_PATTERNS:
    if pattern.severity not in PATTERNS_BY_SEVERITY:
        PATTERNS_BY_SEVERITY[pattern.severity] = []
    PATTERNS_BY_SEVERITY[pattern.severity].append(pattern)

PATTERNS_BY_NAME: Dict[str, FailurePattern] = {p.name: p for p in ALL_PATTERNS}


# =============================================================================
# DIAGNOSTIC FUNCTIONS
# =============================================================================

def match_error_pattern(error_message: str) -> Optional[FailurePattern]:
    """Find the first failure pattern that matches an error message."""
    for pattern in ALL_PATTERNS:
        if pattern.matches(error_message):
            return pattern
    return None


def get_all_patterns() -> List[FailurePattern]:
    """Get all documented failure patterns."""
    return list(ALL_PATTERNS)


def get_patterns_by_category(category: FailureCategory) -> List[FailurePattern]:
    """Get all patterns for a specific category."""
    return PATTERNS_BY_CATEGORY.get(category, [])


def get_patterns_by_severity(severity: FailureSeverity) -> List[FailurePattern]:
    """Get all patterns for a specific severity level."""
    return PATTERNS_BY_SEVERITY.get(severity, [])


def get_diagnostic_guidance(pattern_name: str) -> Optional[str]:
    """Get diagnostic guidance for a specific pattern by name."""
    pattern = PATTERNS_BY_NAME.get(pattern_name)
    if pattern:
        return pattern.get_diagnostic_summary()
    return None


def analyze_error(error_message: str) -> dict:
    """Analyze an error and return diagnostic information."""
    pattern = match_error_pattern(error_message)
    
    if pattern:
        return {
            "matched_pattern": pattern.name,
            "category": pattern.category.value,
            "severity": pattern.severity.value,
            "description": pattern.description,
            "common_causes": pattern.common_causes,
            "diagnostic_steps": pattern.diagnostic_steps,
            "resolution_strategies": pattern.resolution_strategies,
            "affected_modules": pattern.affected_modules,
        }
    else:
        return {
            "matched_pattern": None,
            "message": "No documented pattern matches this error",
            "suggestion": "Review the error message manually and consider adding a new pattern",
        }


def generate_diagnostic_report() -> str:
    """Generate a comprehensive diagnostic report of all patterns."""
    report = []
    report.append("="*80)
    report.append("EXECUTION FAILURE PATTERNS DIAGNOSTIC REPORT")
    report.append("="*80)
    report.append(f"")
    
    # Summary by category
    report.append("SUMMARY BY CATEGORY:")
    report.append("-" * 80)
    for category in FailureCategory:
        patterns = get_patterns_by_category(category)
        report.append(f"\n{category.value}: {len(patterns)} patterns")
        for pattern in patterns:
            report.append(f"  - {pattern.name} ({pattern.severity.value})")
    
    # Critical patterns
    report.append(f"")
    report.append("CRITICAL PATTERNS (Immediate Attention Required):")
    report.append("-" * 80)
    critical = get_patterns_by_severity(FailureSeverity.CRITICAL)
    for pattern in critical:
        report.append(f"\n{pattern.name}")
        report.append(f"  {pattern.description}")
    
    # High severity patterns
    report.append(f"")
    report.append("HIGH SEVERITY PATTERNS:")
    report.append("-" * 80)
    high = get_patterns_by_severity(FailureSeverity.HIGH)
    for pattern in high:
        report.append(f"\n{pattern.name}")
        report.append(f"  {pattern.description}")
    
    return "\n".join(report)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for pattern diagnostics."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python execution_failure_patterns.py report     # Generate full report")
        print("  python execution_failure_patterns.py analyze <error>  # Analyze an error")
        print("  python execution_failure_patterns.py list       # List all patterns")
        print("  python execution_failure_patterns.py guide <pattern_name>  # Get guidance")
        return
    
    command = sys.argv[1]
    
    if command == "report":
        print(generate_diagnostic_report())
    
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Error: Please provide an error message to analyze")
            return
        error_message = " ".join(sys.argv[2:])
        result = analyze_error(error_message)
        print(json.dumps(result, indent=2))
    
    elif command == "list":
        print("\nDocumented Failure Patterns:\n")
        for category in FailureCategory:
            patterns = get_patterns_by_category(category)
            if patterns:
                print(f"\n{category.value}:")
                for pattern in patterns:
                    print(f"  [{pattern.severity.value}] {pattern.name}")
                    print(f"      {pattern.description}")
    
    elif command == "guide":
        if len(sys.argv) < 3:
            print("Error: Please provide a pattern name")
            return
        pattern_name = sys.argv[2]
        guidance = get_diagnostic_guidance(pattern_name)
        if guidance:
            print(guidance)
        else:
            print(f"Pattern '{pattern_name}' not found")
            print("Use 'list' command to see available patterns")
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'report', 'analyze', 'list', or 'guide'")


if __name__ == "__main__":
    import json
    main()

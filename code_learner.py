"""
BYRD Code Learner

Converts stable patterns into executable code.

Key insight: Knowledge externalized as code is:
- Deterministic (no LLM variance)
- Fast (no inference cost)
- Inspectable (can be reviewed/debugged)
- Persistent (survives context limits)

Uses existing LLM client for code generation, no additional dependencies.

Version: 1.0
Created: December 2024
"""

import ast
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass
class Pattern:
    """A behavioral pattern that may be codified."""
    id: str
    description: str
    trigger_conditions: str
    action: str
    domain: str
    success_rate: float
    usage_count: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CodificationResult:
    """Result of attempting to codify a pattern."""
    pattern_id: str
    success: bool
    path: Optional[str] = None
    reason: Optional[str] = None
    code_lines: int = 0


class CodeLearner:
    """
    Converts stable patterns into executable code.

    Key insight: Knowledge externalized as code is:
    - Deterministic (no LLM variance)
    - Fast (no inference cost)
    - Inspectable (can be reviewed/debugged)
    - Persistent (survives context limits)

    NOTE: Uses existing LLM client, no additional dependencies.

    Codification criteria:
    - Pattern used 10+ times
    - Success rate >= 80%
    - Not already codified
    """

    LEARNED_STRATEGIES_DIR = "learned_strategies"

    # Thresholds for codification
    MIN_USAGE_COUNT = 10
    MIN_SUCCESS_RATE = 0.8

    # Dangerous patterns to reject in generated code
    DANGEROUS_PATTERNS = [
        'os.system', 'subprocess', 'eval(', 'exec(',
        '__import__', 'open(', 'write(', 'unlink',
        'remove', 'rmdir', 'shutil', 'socket',
        'http', 'requests.', 'urllib', 'webbrowser'
    ]

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize the Code Learner.

        Args:
            memory: Memory system for querying patterns
            llm_client: LLM client for code generation
            config: Optional configuration
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Registry of codified patterns
        self.code_registry: Dict[str, str] = {}

        # Ensure directory structure exists
        self._ensure_directories()

        # Load existing codified patterns
        self._load_existing_patterns()

    def _ensure_directories(self):
        """Create learned_strategies directory structure."""
        base = Path(self.LEARNED_STRATEGIES_DIR)
        subdirs = ["desire_routing", "pattern_matching", "decision_making"]

        for subdir in subdirs:
            (base / subdir).mkdir(parents=True, exist_ok=True)

        # Create __init__.py files if missing
        init_content = '"""Auto-generated learned strategies."""\n'
        for root, dirs, files in os.walk(base):
            init_path = Path(root) / "__init__.py"
            if not init_path.exists():
                init_path.write_text(init_content)

    def _load_existing_patterns(self):
        """Load existing codified patterns from disk."""
        base = Path(self.LEARNED_STRATEGIES_DIR)

        if not base.exists():
            return

        for py_file in base.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            # Extract pattern ID from filename
            pattern_id = py_file.stem
            self.code_registry[pattern_id] = str(py_file)

    async def maybe_codify(self, pattern: Pattern) -> CodificationResult:
        """
        Codify pattern if stable enough.

        Criteria:
        - usage_count >= MIN_USAGE_COUNT (default: 10)
        - success_rate >= MIN_SUCCESS_RATE (default: 0.8)
        - Not already codified

        Returns:
            CodificationResult with success status and path
        """
        # Check thresholds
        if pattern.usage_count < self.MIN_USAGE_COUNT:
            return CodificationResult(
                pattern_id=pattern.id,
                success=False,
                reason=f"Insufficient usage ({pattern.usage_count} < {self.MIN_USAGE_COUNT})"
            )

        if pattern.success_rate < self.MIN_SUCCESS_RATE:
            return CodificationResult(
                pattern_id=pattern.id,
                success=False,
                reason=f"Low success rate ({pattern.success_rate:.0%} < {self.MIN_SUCCESS_RATE:.0%})"
            )

        if pattern.id in self.code_registry:
            return CodificationResult(
                pattern_id=pattern.id,
                success=False,
                reason="Already codified"
            )

        # Generate code
        code = await self._generate_code(pattern)

        if not code:
            return CodificationResult(
                pattern_id=pattern.id,
                success=False,
                reason="Code generation failed"
            )

        # Validate code safety
        if not self._validate_code(code):
            return CodificationResult(
                pattern_id=pattern.id,
                success=False,
                reason="Code validation failed (safety check)"
            )

        # Determine subdirectory based on pattern domain
        subdir = self._classify_domain(pattern.domain)
        path = f"{self.LEARNED_STRATEGIES_DIR}/{subdir}/{pattern.id}.py"

        # Ensure parent directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        # Write code
        Path(path).write_text(code)

        # Register
        self.code_registry[pattern.id] = path

        # Record experience
        if self.memory:
            await self.memory.record_experience(
                content=f"[CODE_LEARNER] Codified pattern: {pattern.description[:100]}",
                type="codification",
                metadata={
                    "pattern_id": pattern.id,
                    "path": path,
                    "success_rate": pattern.success_rate,
                    "usage_count": pattern.usage_count
                }
            )

        print(f"📝 Codified: {pattern.description[:50]}... -> {path}")

        return CodificationResult(
            pattern_id=pattern.id,
            success=True,
            path=path,
            code_lines=len(code.splitlines())
        )

    def _classify_domain(self, domain: str) -> str:
        """Classify pattern into subdirectory based on domain."""
        domain_lower = domain.lower() if domain else ""

        if any(kw in domain_lower for kw in ["desire", "want", "goal", "intent", "route"]):
            return "desire_routing"
        elif any(kw in domain_lower for kw in ["pattern", "match", "detect", "recognize"]):
            return "pattern_matching"
        else:
            return "decision_making"

    async def _generate_code(self, pattern: Pattern) -> Optional[str]:
        """Use LLM to convert pattern to executable Python code."""
        safe_name = pattern.id.replace('-', '_').replace(' ', '_')

        prompt = f"""Convert this learned behavioral pattern into a Python function.

PATTERN DETAILS:
- ID: {pattern.id}
- Description: {pattern.description}
- Trigger conditions: {pattern.trigger_conditions}
- Action: {pattern.action}
- Success rate: {pattern.success_rate:.0%} (proven over {pattern.usage_count} uses)
- Domain: {pattern.domain}

REQUIREMENTS:
1. Function takes context: Dict[str, Any] as input
2. Returns a decision string or Dict[str, Any]
3. Is pure and deterministic (no LLM calls, no network, no file I/O)
4. Includes docstring with provenance information
5. Uses only standard library imports (typing, re, datetime, json, etc.)
6. Do NOT use: os.system, subprocess, eval, exec, open, requests, or any network/file operations

OUTPUT FORMAT:
```python
from typing import Dict, Any

def {safe_name}(context: Dict[str, Any]) -> str:
    \"\"\"
    {pattern.description[:100]}

    Provenance: Learned from {pattern.usage_count} experiences.
    Success rate: {pattern.success_rate:.0%}
    Domain: {pattern.domain}

    Args:
        context: Dict containing relevant context for decision

    Returns:
        Decision or action recommendation
    \"\"\"
    # Implementation based on trigger conditions and action
    ...
    return "action_recommendation"
```

Generate only the Python code, no explanations."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=800,
                temperature=0.1  # Low temperature for deterministic code
            )

            text = response.text if hasattr(response, 'text') else str(response)
            return self._extract_code(text)

        except Exception as e:
            print(f"Code generation error: {e}")
            return None

    def _extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from LLM response."""
        if "```python" in text:
            code = text.split("```python")[1].split("```")[0]
            return code.strip()
        elif "```" in text:
            code = text.split("```")[1].split("```")[0]
            return code.strip()
        return text.strip()

    def _validate_code(self, code: str) -> bool:
        """Validate generated code is safe and syntactically correct."""
        # Syntax check
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f"Code validation failed (syntax): {e}")
            return False

        # Safety check - no dangerous patterns
        code_lower = code.lower()
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in code_lower:
                print(f"Code contains dangerous pattern: {pattern}")
                return False

        # Additional checks
        if "import os" in code and "os." in code:
            # Allow 'import os' for os.path only
            if "os.system" in code or "os.exec" in code:
                return False

        return True

    async def execute_learned(self, pattern_id: str, context: Dict) -> Optional[Any]:
        """
        Execute a codified pattern.

        Args:
            pattern_id: ID of the pattern to execute
            context: Context dict for the pattern function

        Returns:
            Result of the pattern function, or None if failed
        """
        if pattern_id not in self.code_registry:
            return None

        path = self.code_registry[pattern_id]

        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(pattern_id, path)
            if spec is None or spec.loader is None:
                print(f"Could not load pattern {pattern_id}")
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the function (should match pattern_id with underscores)
            func_name = pattern_id.replace('-', '_').replace(' ', '_')
            func = getattr(module, func_name, None)

            if func is None:
                # Try to find any function in the module
                for name in dir(module):
                    obj = getattr(module, name)
                    if callable(obj) and not name.startswith('_'):
                        func = obj
                        break

            if func:
                return func(context)
            else:
                print(f"No callable function found in {path}")
                return None

        except Exception as e:
            print(f"Error executing learned pattern {pattern_id}: {e}")
            return None

    def get_codified_patterns(self) -> List[str]:
        """Get list of codified pattern IDs."""
        return list(self.code_registry.keys())

    def get_pattern_path(self, pattern_id: str) -> Optional[str]:
        """Get file path for a codified pattern."""
        return self.code_registry.get(pattern_id)

    async def discover_patterns_for_codification(self) -> List[Pattern]:
        """
        Discover patterns in memory that are ready for codification.

        Queries Neo4j for patterns meeting codification criteria.
        """
        if not self.memory:
            return []

        try:
            result = await self.memory._run_query("""
                MATCH (p:Pattern)
                WHERE p.usage_count >= $min_usage
                AND p.success_rate >= $min_success
                AND NOT exists((p)-[:CODIFIED]->())
                RETURN p.id as id,
                       p.description as description,
                       p.trigger_conditions as trigger,
                       p.action as action,
                       p.domain as domain,
                       p.success_rate as success_rate,
                       p.usage_count as usage_count
                ORDER BY p.success_rate * p.usage_count DESC
                LIMIT 10
            """, {
                "min_usage": self.MIN_USAGE_COUNT,
                "min_success": self.MIN_SUCCESS_RATE
            })

            patterns = []
            for record in (result or []):
                patterns.append(Pattern(
                    id=record.get("id", f"pattern_{len(patterns)}"),
                    description=record.get("description", ""),
                    trigger_conditions=record.get("trigger", ""),
                    action=record.get("action", ""),
                    domain=record.get("domain", "general"),
                    success_rate=record.get("success_rate", 0.0),
                    usage_count=record.get("usage_count", 0)
                ))

            return patterns

        except Exception as e:
            print(f"Error discovering patterns: {e}")
            return []

    async def codification_cycle(self) -> List[CodificationResult]:
        """
        Run a codification cycle.

        Discovers patterns ready for codification and attempts to codify them.

        Returns:
            List of CodificationResults for each attempted pattern
        """
        patterns = await self.discover_patterns_for_codification()
        results = []

        for pattern in patterns:
            result = await self.maybe_codify(pattern)
            results.append(result)

            # Mark pattern as codified in memory
            if result.success and self.memory:
                try:
                    await self.memory._run_query("""
                        MATCH (p:Pattern {id: $pattern_id})
                        SET p.codified = true,
                            p.codified_at = datetime(),
                            p.codified_path = $path
                    """, {
                        "pattern_id": pattern.id,
                        "path": result.path
                    })
                except Exception as e:
                    print(f"Could not mark pattern as codified: {e}")

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Get codification statistics."""
        return {
            "total_codified": len(self.code_registry),
            "patterns_by_domain": self._count_by_domain(),
            "thresholds": {
                "min_usage_count": self.MIN_USAGE_COUNT,
                "min_success_rate": self.MIN_SUCCESS_RATE
            }
        }

    def _count_by_domain(self) -> Dict[str, int]:
        """Count codified patterns by domain."""
        counts = {"desire_routing": 0, "pattern_matching": 0, "decision_making": 0}

        for path in self.code_registry.values():
            for domain in counts:
                if domain in path:
                    counts[domain] += 1
                    break

        return counts

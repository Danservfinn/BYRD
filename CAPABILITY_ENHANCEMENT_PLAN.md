# BYRD Capability Enhancement Plan

## The Core Insight

**The LLM doesn't need to get smarter. The SYSTEM needs to get smarter at using the LLM.**

Previous plans (v1, v2) failed because they:
- Relied on self-assessment (LLM grading its own homework)
- Built infrastructure without actual capability improvement
- Confused data accumulation with intelligence growth
- Had no ground truth to verify progress

This plan takes a fundamentally different approach: **verifiable capabilities with compounding feedback loops**.

---

## Part 1: Verifiable Capability System

The key innovation: capabilities are defined by TEST SUITES, not self-assessment.

### Why This Matters

Self-assessment is circular:
```
LLM generates answer → LLM evaluates answer → LLM says "good job!"
```

Ground truth verification:
```
LLM generates answer → Test suite checks answer → Objective pass/fail
```

### Implementation

```python
# src/byrd/capabilities/capability_system.py

from dataclasses import dataclass
from typing import Callable, List, Dict, Any, Optional
from enum import Enum
import json
import hashlib

class CapabilityDomain(Enum):
    ARITHMETIC = "arithmetic"
    LOGIC = "logic"
    CODE_GENERATION = "code_generation"
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"
    PLANNING = "planning"
    REASONING = "reasoning"
    TOOL_USE = "tool_use"


@dataclass
class TestCase:
    """A single test case with input, expected output, and verifier."""
    input_data: Dict[str, Any]
    expected_output: Any
    verifier: Callable[[Any, Any], bool]  # (actual, expected) -> bool
    difficulty: float  # 0.0 to 1.0
    tags: List[str]

    def verify(self, actual_output: Any) -> bool:
        """Check if actual output matches expected."""
        try:
            return self.verifier(actual_output, self.expected_output)
        except Exception:
            return False


@dataclass
class Capability:
    """A capability with its test suite for ground truth verification."""
    name: str
    domain: CapabilityDomain
    description: str
    test_cases: List[TestCase]
    current_prompt_template: str
    prompt_history: List[Dict]  # Track prompt evolution
    success_rate: float = 0.0

    def evaluate(self, executor: Callable[[str, Dict], Any]) -> float:
        """
        Evaluate capability against ALL test cases.
        Returns success rate (0.0 to 1.0).
        """
        if not self.test_cases:
            return 0.0

        passed = 0
        results = []

        for test in self.test_cases:
            prompt = self.current_prompt_template.format(**test.input_data)
            try:
                actual = executor(prompt, test.input_data)
                success = test.verify(actual)
                passed += 1 if success else 0
                results.append({
                    "input": test.input_data,
                    "expected": test.expected_output,
                    "actual": actual,
                    "passed": success
                })
            except Exception as e:
                results.append({
                    "input": test.input_data,
                    "error": str(e),
                    "passed": False
                })

        self.success_rate = passed / len(self.test_cases)
        return self.success_rate

    def get_failures(self, executor: Callable) -> List[Dict]:
        """Get detailed info about failed test cases."""
        failures = []
        for test in self.test_cases:
            prompt = self.current_prompt_template.format(**test.input_data)
            try:
                actual = executor(prompt, test.input_data)
                if not test.verify(actual):
                    failures.append({
                        "input": test.input_data,
                        "expected": test.expected_output,
                        "actual": actual,
                        "prompt_used": prompt,
                        "difficulty": test.difficulty
                    })
            except Exception as e:
                failures.append({
                    "input": test.input_data,
                    "expected": test.expected_output,
                    "error": str(e),
                    "prompt_used": prompt,
                    "difficulty": test.difficulty
                })
        return failures


class CapabilityRegistry:
    """Registry of all capabilities with their test suites."""

    def __init__(self):
        self.capabilities: Dict[str, Capability] = {}
        self._initialize_core_capabilities()

    def _initialize_core_capabilities(self):
        """Initialize capabilities with ground truth test suites."""

        # Arithmetic capability
        self.capabilities["arithmetic"] = Capability(
            name="arithmetic",
            domain=CapabilityDomain.ARITHMETIC,
            description="Basic arithmetic operations",
            test_cases=self._generate_arithmetic_tests(),
            current_prompt_template="Calculate: {expression}\nProvide only the numeric answer.",
            prompt_history=[]
        )

        # Logic capability
        self.capabilities["logic"] = Capability(
            name="logic",
            domain=CapabilityDomain.LOGIC,
            description="Logical reasoning and deduction",
            test_cases=self._generate_logic_tests(),
            current_prompt_template="Given: {premises}\nConclusion to verify: {conclusion}\nIs this valid? Answer only 'valid' or 'invalid'.",
            prompt_history=[]
        )

        # Code generation capability
        self.capabilities["code_generation"] = Capability(
            name="code_generation",
            domain=CapabilityDomain.CODE_GENERATION,
            description="Generate working code",
            test_cases=self._generate_code_tests(),
            current_prompt_template="Write a Python function that {task}. Return only the code, no explanation.",
            prompt_history=[]
        )

        # Planning capability
        self.capabilities["planning"] = Capability(
            name="planning",
            domain=CapabilityDomain.PLANNING,
            description="Multi-step planning",
            test_cases=self._generate_planning_tests(),
            current_prompt_template="Goal: {goal}\nConstraints: {constraints}\nCreate a step-by-step plan.",
            prompt_history=[]
        )

    def _generate_arithmetic_tests(self) -> List[TestCase]:
        """Generate arithmetic test cases with KNOWN correct answers."""
        tests = []

        # Addition tests
        for a, b in [(2, 3), (15, 27), (100, 250), (1234, 5678)]:
            tests.append(TestCase(
                input_data={"expression": f"{a} + {b}"},
                expected_output=a + b,
                verifier=lambda actual, expected: self._numeric_match(actual, expected),
                difficulty=0.1,
                tags=["addition"]
            ))

        # Multiplication tests
        for a, b in [(7, 8), (12, 15), (25, 40), (123, 456)]:
            tests.append(TestCase(
                input_data={"expression": f"{a} × {b}"},
                expected_output=a * b,
                verifier=lambda actual, expected: self._numeric_match(actual, expected),
                difficulty=0.3,
                tags=["multiplication"]
            ))

        # Complex expressions
        expressions = [
            ("(5 + 3) × 4", 32),
            ("100 - 37 + 15", 78),
            ("(12 × 3) - (8 × 2)", 20),
            ("144 ÷ 12 + 7", 19),
        ]
        for expr, answer in expressions:
            tests.append(TestCase(
                input_data={"expression": expr},
                expected_output=answer,
                verifier=lambda actual, expected: self._numeric_match(actual, expected),
                difficulty=0.5,
                tags=["complex"]
            ))

        return tests

    def _generate_logic_tests(self) -> List[TestCase]:
        """Generate logic test cases with KNOWN valid/invalid conclusions."""
        tests = []

        # Valid syllogisms
        valid_cases = [
            {
                "premises": "All humans are mortal. Socrates is human.",
                "conclusion": "Socrates is mortal.",
                "valid": True
            },
            {
                "premises": "If it rains, the ground is wet. It is raining.",
                "conclusion": "The ground is wet.",
                "valid": True
            },
            {
                "premises": "All birds have feathers. Penguins are birds.",
                "conclusion": "Penguins have feathers.",
                "valid": True
            },
        ]

        # Invalid syllogisms
        invalid_cases = [
            {
                "premises": "All dogs are mammals. All cats are mammals.",
                "conclusion": "All dogs are cats.",
                "valid": False
            },
            {
                "premises": "If it rains, the ground is wet. The ground is wet.",
                "conclusion": "It is raining.",
                "valid": False  # Affirming the consequent fallacy
            },
            {
                "premises": "Some fruits are red. Apples are fruits.",
                "conclusion": "Apples are red.",
                "valid": False
            },
        ]

        for case in valid_cases + invalid_cases:
            tests.append(TestCase(
                input_data={"premises": case["premises"], "conclusion": case["conclusion"]},
                expected_output="valid" if case["valid"] else "invalid",
                verifier=lambda actual, expected: actual.lower().strip() == expected,
                difficulty=0.4,
                tags=["syllogism"]
            ))

        return tests

    def _generate_code_tests(self) -> List[TestCase]:
        """Generate code tests where output can be EXECUTED and verified."""
        tests = []

        # Simple function tests
        code_challenges = [
            {
                "task": "takes a list of numbers and returns their sum",
                "test_inputs": [[1, 2, 3], [10, 20, 30], []],
                "expected_outputs": [6, 60, 0],
                "function_name": "sum_list"
            },
            {
                "task": "takes a string and returns it reversed",
                "test_inputs": ["hello", "world", ""],
                "expected_outputs": ["olleh", "dlrow", ""],
                "function_name": "reverse_string"
            },
            {
                "task": "takes a number and returns True if it's prime, False otherwise",
                "test_inputs": [2, 7, 10, 1],
                "expected_outputs": [True, True, False, False],
                "function_name": "is_prime"
            },
            {
                "task": "takes two lists and returns their intersection",
                "test_inputs": [([1,2,3], [2,3,4]), ([1,2], [3,4]), ([], [1,2])],
                "expected_outputs": [[2,3], [], []],
                "function_name": "intersect"
            },
        ]

        for challenge in code_challenges:
            tests.append(TestCase(
                input_data={"task": challenge["task"]},
                expected_output=challenge,
                verifier=self._code_verifier,
                difficulty=0.6,
                tags=["code", challenge["function_name"]]
            ))

        return tests

    def _generate_planning_tests(self) -> List[TestCase]:
        """Generate planning tests where plans can be verified for validity."""
        tests = []

        planning_challenges = [
            {
                "goal": "Make a peanut butter and jelly sandwich",
                "constraints": "You have bread, peanut butter, jelly, and a knife.",
                "required_elements": ["bread", "peanut butter", "jelly", "spread"],
                "forbidden_elements": ["toast", "oven"],  # Not mentioned in constraints
            },
            {
                "goal": "Get from home to the airport",
                "constraints": "You have a car with fuel. The airport is 30 miles away. You have 2 hours.",
                "required_elements": ["drive", "car"],
                "forbidden_elements": ["fly", "helicopter"],
            },
        ]

        for challenge in planning_challenges:
            tests.append(TestCase(
                input_data={"goal": challenge["goal"], "constraints": challenge["constraints"]},
                expected_output=challenge,
                verifier=self._plan_verifier,
                difficulty=0.7,
                tags=["planning"]
            ))

        return tests

    @staticmethod
    def _numeric_match(actual: Any, expected: Any) -> bool:
        """Check if actual matches expected numerically."""
        try:
            # Extract number from response
            actual_str = str(actual).strip()
            # Remove common prefixes
            for prefix in ["The answer is", "Result:", "="]:
                actual_str = actual_str.replace(prefix, "").strip()
            actual_num = float(actual_str.replace(",", ""))
            return abs(actual_num - float(expected)) < 0.0001
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _code_verifier(actual: Any, expected: Dict) -> bool:
        """Verify code by executing it against test cases."""
        try:
            # Extract code from response
            code = str(actual)
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]

            # Create isolated namespace and execute
            namespace = {}
            exec(code, namespace)

            # Find the function
            func = None
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith("_"):
                    func = obj
                    break

            if not func:
                return False

            # Test against all test cases
            for input_val, expected_output in zip(expected["test_inputs"], expected["expected_outputs"]):
                if isinstance(input_val, tuple):
                    result = func(*input_val)
                else:
                    result = func(input_val)

                # Handle list comparison
                if isinstance(expected_output, list):
                    if sorted(result) != sorted(expected_output):
                        return False
                elif result != expected_output:
                    return False

            return True
        except Exception:
            return False

    @staticmethod
    def _plan_verifier(actual: Any, expected: Dict) -> bool:
        """Verify plan contains required elements and no forbidden elements."""
        plan_text = str(actual).lower()

        # Check required elements
        for required in expected["required_elements"]:
            if required.lower() not in plan_text:
                return False

        # Check forbidden elements
        for forbidden in expected["forbidden_elements"]:
            if forbidden.lower() in plan_text:
                return False

        return True

    def evaluate_all(self, executor: Callable) -> Dict[str, float]:
        """Evaluate all capabilities and return success rates."""
        results = {}
        for name, capability in self.capabilities.items():
            results[name] = capability.evaluate(executor)
        return results

    def get_weakest_capability(self) -> Optional[Capability]:
        """Get capability with lowest success rate."""
        if not self.capabilities:
            return None
        return min(self.capabilities.values(), key=lambda c: c.success_rate)

    def get_all_failures(self, executor: Callable) -> Dict[str, List[Dict]]:
        """Get all failures across all capabilities."""
        failures = {}
        for name, capability in self.capabilities.items():
            cap_failures = capability.get_failures(executor)
            if cap_failures:
                failures[name] = cap_failures
        return failures
```

---

## Part 2: Tool-Augmented Reasoning

Instead of making the LLM smarter, give it **reliable tools** for tasks it's bad at.

### Why This Matters

LLMs fail predictably at:
- Precise arithmetic
- Long-term memory recall
- Real-time information
- Multi-step verification

Tools can handle these reliably. The LLM's job becomes **orchestration**, not computation.

### Implementation

```python
# src/byrd/capabilities/tool_augmented_reasoning.py

from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Optional
import json
import re


@dataclass
class Tool:
    """A tool that extends LLM capabilities."""
    name: str
    description: str
    parameters: Dict[str, str]  # param_name -> description
    executor: Callable[..., Any]
    reliability: float = 1.0  # Tools should be highly reliable

    def execute(self, **kwargs) -> Any:
        """Execute tool with given parameters."""
        return self.executor(**kwargs)

    def to_prompt_format(self) -> str:
        """Format tool for inclusion in prompts."""
        params = ", ".join(f"{k}: {v}" for k, v in self.parameters.items())
        return f"- {self.name}({params}): {self.description}"


class ToolRegistry:
    """Registry of tools available to BYRD."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_core_tools()

    def _register_core_tools(self):
        """Register reliable core tools."""

        # Calculator tool - 100% reliable for arithmetic
        self.register(Tool(
            name="calculate",
            description="Evaluates mathematical expressions with perfect accuracy",
            parameters={"expression": "Mathematical expression to evaluate"},
            executor=self._safe_calculate,
            reliability=1.0
        ))

        # Memory search tool
        self.register(Tool(
            name="search_memory",
            description="Searches BYRD's long-term memory for relevant information",
            parameters={"query": "Search query", "limit": "Max results (default 5)"},
            executor=self._search_memory,
            reliability=0.9
        ))

        # Current time tool
        self.register(Tool(
            name="current_time",
            description="Gets the current date and time",
            parameters={},
            executor=self._get_current_time,
            reliability=1.0
        ))

        # Web search tool
        self.register(Tool(
            name="web_search",
            description="Searches the web for current information",
            parameters={"query": "Search query"},
            executor=self._web_search,
            reliability=0.85
        ))

        # Code execution tool
        self.register(Tool(
            name="execute_python",
            description="Executes Python code and returns the result",
            parameters={"code": "Python code to execute"},
            executor=self._execute_python,
            reliability=0.95
        ))

        # Verification tool
        self.register(Tool(
            name="verify_claim",
            description="Checks a factual claim against known sources",
            parameters={"claim": "The claim to verify"},
            executor=self._verify_claim,
            reliability=0.8
        ))

    def register(self, tool: Tool):
        """Register a new tool."""
        self.tools[tool.name] = tool

    def get_tools_prompt(self) -> str:
        """Get formatted list of all tools for prompts."""
        lines = ["Available tools:"]
        for tool in self.tools.values():
            lines.append(tool.to_prompt_format())
        return "\n".join(lines)

    def execute_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool call and return result."""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}

        tool = self.tools[tool_name]
        try:
            result = tool.execute(**kwargs)
            return {"success": True, "result": result, "tool": tool_name}
        except Exception as e:
            return {"success": False, "error": str(e), "tool": tool_name}

    @staticmethod
    def _safe_calculate(expression: str) -> float:
        """Safely evaluate mathematical expressions."""
        # Remove anything that's not math-related
        allowed_chars = set("0123456789+-*/().^ ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")

        # Replace ^ with ** for exponentiation
        expression = expression.replace("^", "**")

        # Evaluate safely
        return eval(expression, {"__builtins__": {}}, {})

    @staticmethod
    def _search_memory(query: str, limit: int = 5) -> List[Dict]:
        """Search BYRD's memory graph."""
        # This would connect to Neo4j
        # Placeholder implementation
        return [{"type": "memory_search", "query": query, "results": []}]

    @staticmethod
    def _get_current_time() -> str:
        """Get current time."""
        from datetime import datetime
        return datetime.now().isoformat()

    @staticmethod
    def _web_search(query: str) -> List[Dict]:
        """Search the web."""
        # Would use DuckDuckGo or similar
        # Placeholder implementation
        return [{"type": "web_search", "query": query, "results": []}]

    @staticmethod
    def _execute_python(code: str) -> Any:
        """Execute Python code in sandbox."""
        # Restricted execution environment
        safe_builtins = {
            "abs": abs, "all": all, "any": any, "len": len,
            "max": max, "min": min, "sum": sum, "sorted": sorted,
            "list": list, "dict": dict, "set": set, "tuple": tuple,
            "str": str, "int": int, "float": float, "bool": bool,
            "range": range, "enumerate": enumerate, "zip": zip,
            "map": map, "filter": filter, "reversed": reversed,
            "True": True, "False": False, "None": None,
        }

        namespace = {"__builtins__": safe_builtins}
        exec(code, namespace)

        # Return the last defined variable or None
        result = namespace.get("result", namespace.get("output", None))
        return result

    @staticmethod
    def _verify_claim(claim: str) -> Dict[str, Any]:
        """Verify a factual claim."""
        # Would check against knowledge base or web
        # Placeholder implementation
        return {
            "claim": claim,
            "verification_status": "unverified",
            "confidence": 0.0,
            "sources": []
        }


class ToolAugmentedReasoner:
    """Reasoning system that uses tools to augment LLM capabilities."""

    def __init__(self, llm_executor: Callable[[str], str], tool_registry: ToolRegistry):
        self.llm = llm_executor
        self.tools = tool_registry

    def reason(self, query: str, max_tool_uses: int = 5) -> Dict[str, Any]:
        """
        Reason about a query, using tools as needed.

        The LLM decides when to use tools and orchestrates the process.
        """
        conversation = []
        tool_uses = 0

        # Initial prompt with tool descriptions
        system_prompt = f"""You are BYRD, an AGI system with access to tools.
When you need to perform calculations, search memory, get current information,
or verify facts, USE THE TOOLS. Don't guess.

{self.tools.get_tools_prompt()}

To use a tool, respond with:
TOOL: tool_name
PARAMS: {{"param1": "value1", "param2": "value2"}}

After receiving tool results, continue reasoning or provide your final answer.
When done, respond with:
FINAL: your final answer"""

        current_prompt = f"{system_prompt}\n\nQuery: {query}"

        while tool_uses < max_tool_uses:
            # Get LLM response
            response = self.llm(current_prompt)
            conversation.append({"role": "assistant", "content": response})

            # Check if it's a tool call
            if "TOOL:" in response:
                tool_result = self._parse_and_execute_tool(response)
                tool_uses += 1

                # Add tool result to conversation
                tool_message = f"TOOL RESULT: {json.dumps(tool_result)}"
                conversation.append({"role": "tool", "content": tool_message})
                current_prompt = f"{current_prompt}\n\nAssistant: {response}\n\n{tool_message}\n\nContinue reasoning:"

            elif "FINAL:" in response:
                # Extract final answer
                final_answer = response.split("FINAL:")[1].strip()
                return {
                    "success": True,
                    "answer": final_answer,
                    "tool_uses": tool_uses,
                    "conversation": conversation
                }
            else:
                # No tool call and no final answer, prompt for continuation
                current_prompt = f"{current_prompt}\n\nAssistant: {response}\n\nPlease either use a tool or provide your FINAL answer:"

        # Max tool uses reached
        return {
            "success": False,
            "error": "Max tool uses exceeded",
            "tool_uses": tool_uses,
            "conversation": conversation
        }

    def _parse_and_execute_tool(self, response: str) -> Dict[str, Any]:
        """Parse tool call from response and execute it."""
        try:
            # Extract tool name
            tool_match = re.search(r"TOOL:\s*(\w+)", response)
            if not tool_match:
                return {"error": "Could not parse tool name"}
            tool_name = tool_match.group(1)

            # Extract parameters
            params_match = re.search(r"PARAMS:\s*(\{.*?\})", response, re.DOTALL)
            params = {}
            if params_match:
                params = json.loads(params_match.group(1))

            # Execute tool
            return self.tools.execute_tool_call(tool_name, **params)

        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in parameters: {e}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {e}"}
```

---

## Part 3: Prompt Evolution System

The LLM's capabilities are largely determined by how we prompt it. **Evolve better prompts through tournament selection.**

### Why This Matters

Different prompts produce dramatically different results:
- "Calculate 15 × 27" → might fail
- "You are a calculator. Compute step by step: 15 × 27" → better
- "Break down 15 × 27 into (10 + 5) × 27 = 270 + 135 = 405" → even better

We can **evolve** prompts using ground truth to select winners.

### Implementation

```python
# src/byrd/capabilities/prompt_evolution.py

from dataclasses import dataclass, field
from typing import List, Callable, Dict, Any, Optional
import random
import hashlib
from datetime import datetime


@dataclass
class PromptVariant:
    """A prompt variant with performance tracking."""
    template: str
    capability_name: str
    generation: int = 0
    parent_hash: Optional[str] = None

    # Performance metrics
    evaluations: int = 0
    successes: int = 0

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    mutations_applied: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        return self.successes / self.evaluations if self.evaluations > 0 else 0.0

    @property
    def hash(self) -> str:
        return hashlib.md5(self.template.encode()).hexdigest()[:12]

    def record_result(self, success: bool):
        """Record a test result."""
        self.evaluations += 1
        if success:
            self.successes += 1


class PromptMutator:
    """Applies mutations to prompt templates."""

    MUTATIONS = [
        ("add_step_by_step", "Add 'Think step by step.' instruction"),
        ("add_verification", "Add 'Verify your answer.' instruction"),
        ("add_format_spec", "Add specific output format requirements"),
        ("add_examples", "Add few-shot examples"),
        ("simplify", "Remove unnecessary words"),
        ("restructure", "Reorganize prompt structure"),
        ("add_persona", "Add expert persona"),
        ("add_decomposition", "Add problem decomposition instruction"),
    ]

    def mutate(self, variant: PromptVariant, mutation_type: str) -> PromptVariant:
        """Apply a mutation to create a new variant."""
        template = variant.template

        if mutation_type == "add_step_by_step":
            template = f"Think step by step.\n{template}"

        elif mutation_type == "add_verification":
            template = f"{template}\nAfter answering, verify your result is correct."

        elif mutation_type == "add_format_spec":
            template = f"{template}\nProvide your answer in the exact format requested, nothing more."

        elif mutation_type == "add_examples":
            # Add capability-specific examples
            examples = self._get_examples_for_capability(variant.capability_name)
            template = f"{examples}\n\n{template}"

        elif mutation_type == "simplify":
            # Remove common filler words
            fillers = ["please", "kindly", "could you", "would you"]
            for filler in fillers:
                template = template.replace(filler, "").replace(filler.capitalize(), "")
            template = " ".join(template.split())  # Normalize whitespace

        elif mutation_type == "restructure":
            # Put most important instruction first
            lines = template.split("\n")
            # Move lines with "answer" or "output" to end
            priority_lines = []
            other_lines = []
            for line in lines:
                if any(kw in line.lower() for kw in ["answer", "output", "result", "provide"]):
                    other_lines.append(line)
                else:
                    priority_lines.append(line)
            template = "\n".join(priority_lines + other_lines)

        elif mutation_type == "add_persona":
            personas = {
                "arithmetic": "You are a precise calculator that never makes arithmetic errors.",
                "logic": "You are a formal logic expert who validates arguments rigorously.",
                "code_generation": "You are a senior software engineer who writes clean, tested code.",
                "planning": "You are a project manager who creates detailed, actionable plans.",
            }
            persona = personas.get(variant.capability_name, "You are an expert at this task.")
            template = f"{persona}\n\n{template}"

        elif mutation_type == "add_decomposition":
            template = f"First, break this problem into smaller parts. Then solve each part.\n\n{template}"

        new_variant = PromptVariant(
            template=template,
            capability_name=variant.capability_name,
            generation=variant.generation + 1,
            parent_hash=variant.hash,
            mutations_applied=variant.mutations_applied + [mutation_type]
        )

        return new_variant

    def crossover(self, parent1: PromptVariant, parent2: PromptVariant) -> PromptVariant:
        """Combine two prompts to create a child."""
        # Simple crossover: take first half of one, second half of other
        lines1 = parent1.template.split("\n")
        lines2 = parent2.template.split("\n")

        midpoint1 = len(lines1) // 2
        midpoint2 = len(lines2) // 2

        new_template = "\n".join(lines1[:midpoint1] + lines2[midpoint2:])

        return PromptVariant(
            template=new_template,
            capability_name=parent1.capability_name,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_hash=f"{parent1.hash}+{parent2.hash}",
            mutations_applied=["crossover"]
        )

    def _get_examples_for_capability(self, capability_name: str) -> str:
        """Get few-shot examples for a capability."""
        examples = {
            "arithmetic": """Examples:
Q: 23 + 47
A: 70

Q: 15 × 8
A: 120

Q: (10 + 5) × 4
A: 60""",
            "logic": """Examples:
Premises: All A are B. X is A.
Conclusion: X is B.
Answer: valid

Premises: Some A are B. X is A.
Conclusion: X is B.
Answer: invalid""",
            "code_generation": """Example:
Task: takes a number and returns its square
Answer:
def square(n):
    return n * n""",
            "planning": """Example:
Goal: Boil water
Steps:
1. Fill kettle with water
2. Place kettle on stove
3. Turn on heat
4. Wait until water boils
5. Turn off heat"""
        }
        return examples.get(capability_name, "")


class PromptEvolutionEngine:
    """
    Evolves prompts through tournament selection.

    The key insight: use GROUND TRUTH to select winners.
    No self-assessment, no LLM grading itself.
    """

    def __init__(
        self,
        capability_registry,  # CapabilityRegistry
        llm_executor: Callable[[str], str],
        population_size: int = 10,
        tournament_size: int = 3
    ):
        self.capabilities = capability_registry
        self.llm = llm_executor
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.mutator = PromptMutator()

        # Population per capability
        self.populations: Dict[str, List[PromptVariant]] = {}

        # Initialize populations
        self._initialize_populations()

    def _initialize_populations(self):
        """Create initial populations from current prompts."""
        for name, capability in self.capabilities.capabilities.items():
            self.populations[name] = [
                PromptVariant(
                    template=capability.current_prompt_template,
                    capability_name=name,
                    generation=0
                )
            ]

    def evolve_generation(self, capability_name: str) -> Dict[str, Any]:
        """
        Run one generation of evolution for a capability.

        Returns statistics about the generation.
        """
        if capability_name not in self.populations:
            return {"error": f"Unknown capability: {capability_name}"}

        population = self.populations[capability_name]
        capability = self.capabilities.capabilities[capability_name]

        # Evaluate all variants against ground truth
        for variant in population:
            self._evaluate_variant(variant, capability)

        # Sort by success rate
        population.sort(key=lambda v: v.success_rate, reverse=True)

        # Statistics
        stats = {
            "capability": capability_name,
            "population_size": len(population),
            "best_success_rate": population[0].success_rate if population else 0,
            "worst_success_rate": population[-1].success_rate if population else 0,
            "avg_success_rate": sum(v.success_rate for v in population) / len(population) if population else 0,
        }

        # Generate new variants through tournament selection and mutation
        new_variants = []

        while len(new_variants) < self.population_size - 1:  # Keep best one
            # Tournament selection
            tournament = random.sample(population, min(self.tournament_size, len(population)))
            winner = max(tournament, key=lambda v: v.success_rate)

            # Apply random mutation
            mutation_type = random.choice([m[0] for m in PromptMutator.MUTATIONS])
            new_variant = self.mutator.mutate(winner, mutation_type)
            new_variants.append(new_variant)

        # Occasionally do crossover
        if len(population) >= 2 and random.random() < 0.3:
            parents = random.sample([v for v in population if v.success_rate > 0.5],
                                   min(2, len([v for v in population if v.success_rate > 0.5])))
            if len(parents) == 2:
                child = self.mutator.crossover(parents[0], parents[1])
                new_variants.append(child)

        # Keep best + new variants
        self.populations[capability_name] = [population[0]] + new_variants

        # Update capability with best prompt
        if population[0].success_rate > capability.success_rate:
            capability.prompt_history.append({
                "template": capability.current_prompt_template,
                "success_rate": capability.success_rate,
                "replaced_at": datetime.now().isoformat()
            })
            capability.current_prompt_template = population[0].template

        return stats

    def _evaluate_variant(self, variant: PromptVariant, capability):
        """Evaluate a prompt variant against the capability's test suite."""
        def executor(prompt: str, input_data: Dict) -> Any:
            full_prompt = variant.template.format(**input_data)
            return self.llm(full_prompt)

        # Run through test cases
        for test in capability.test_cases:
            try:
                prompt = variant.template.format(**test.input_data)
                result = self.llm(prompt)
                success = test.verify(result)
                variant.record_result(success)
            except Exception:
                variant.record_result(False)

    def run_evolution(self, generations: int = 10) -> Dict[str, Any]:
        """
        Run evolution for all capabilities.

        Returns history of evolution.
        """
        history = {name: [] for name in self.populations}

        for gen in range(generations):
            for name in self.populations:
                stats = self.evolve_generation(name)
                stats["generation"] = gen
                history[name].append(stats)

        return history

    def get_best_prompts(self) -> Dict[str, str]:
        """Get the best prompt for each capability."""
        best = {}
        for name, population in self.populations.items():
            if population:
                best[name] = max(population, key=lambda v: v.success_rate).template
        return best
```

---

## Part 4: Failure-Driven Learning

The most powerful compounding loop: **failures generate tools that prevent future failures**.

### Why This Matters

This is ACTUAL compounding:
1. Attempt task → Fail
2. Analyze failure → Generate tool/workaround
3. Add tool to arsenal
4. Attempt similar task → Succeed (using new tool)
5. Repeat → Arsenal grows → Fewer failures

Unlike self-assessment loops, this produces MEASURABLE improvement.

### Implementation

```python
# src/byrd/capabilities/failure_driven_learning.py

from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
import json
import hashlib


@dataclass
class Failure:
    """Record of a capability failure."""
    capability_name: str
    test_input: Dict[str, Any]
    expected_output: Any
    actual_output: Any
    prompt_used: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    analysis: Optional[str] = None
    resolution: Optional[str] = None
    tool_generated: Optional[str] = None

    @property
    def hash(self) -> str:
        content = f"{self.capability_name}:{json.dumps(self.test_input, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict:
        return {
            "capability": self.capability_name,
            "input": self.test_input,
            "expected": self.expected_output,
            "actual": self.actual_output,
            "prompt": self.prompt_used,
            "timestamp": self.timestamp,
            "analysis": self.analysis,
            "resolution": self.resolution,
            "tool_generated": self.tool_generated
        }


@dataclass
class GeneratedTool:
    """A tool generated in response to failures."""
    name: str
    description: str
    code: str
    failure_hashes: List[str]  # Failures that prompted this tool
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    success_count: int = 0
    usage_count: int = 0

    @property
    def effectiveness(self) -> float:
        return self.success_count / self.usage_count if self.usage_count > 0 else 0.0


class FailureAnalyzer:
    """Analyzes failures to identify patterns and generate solutions."""

    def __init__(self, llm_executor: Callable[[str], str]):
        self.llm = llm_executor

    def analyze_failure(self, failure: Failure) -> Dict[str, Any]:
        """
        Analyze a failure to understand why it occurred.

        Uses LLM for analysis but validates against patterns.
        """
        analysis_prompt = f"""Analyze this failure:

Task: {failure.capability_name}
Input: {json.dumps(failure.test_input)}
Expected: {failure.expected_output}
Actual: {failure.actual_output}
Prompt used: {failure.prompt_used}

Identify:
1. What type of error is this? (calculation, logic, format, knowledge, etc.)
2. What caused the error?
3. How could this be fixed with a tool or workaround?

Format your response as JSON:
{{
    "error_type": "...",
    "root_cause": "...",
    "suggested_fix": "...",
    "tool_needed": true/false,
    "tool_description": "..." // if tool_needed is true
}}"""

        try:
            response = self.llm(analysis_prompt)
            # Extract JSON from response
            json_match = response
            if "```json" in response:
                json_match = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_match = response.split("```")[1].split("```")[0]

            analysis = json.loads(json_match)
            failure.analysis = json.dumps(analysis)
            return analysis
        except Exception as e:
            return {
                "error_type": "unknown",
                "root_cause": f"Analysis failed: {e}",
                "suggested_fix": "Manual review needed",
                "tool_needed": False
            }

    def categorize_failures(self, failures: List[Failure]) -> Dict[str, List[Failure]]:
        """Group failures by error type."""
        categories: Dict[str, List[Failure]] = {}

        for failure in failures:
            if failure.analysis:
                try:
                    analysis = json.loads(failure.analysis)
                    error_type = analysis.get("error_type", "unknown")
                except:
                    error_type = "unknown"
            else:
                error_type = "unanalyzed"

            if error_type not in categories:
                categories[error_type] = []
            categories[error_type].append(failure)

        return categories


class ToolGenerator:
    """Generates tools to address identified failure patterns."""

    def __init__(self, llm_executor: Callable[[str], str]):
        self.llm = llm_executor

    def generate_tool(self, failures: List[Failure], error_type: str) -> Optional[GeneratedTool]:
        """
        Generate a tool to address a category of failures.

        The tool must be:
        1. Deterministic (same input → same output)
        2. Verifiable (we can test it)
        3. Composable (can be used in combination with other tools)
        """
        # Gather failure examples
        examples = []
        for f in failures[:5]:  # Use up to 5 examples
            examples.append({
                "input": f.test_input,
                "expected": f.expected_output,
                "actual": f.actual_output
            })

        generation_prompt = f"""Generate a Python tool to fix this error pattern:

Error type: {error_type}

Example failures:
{json.dumps(examples, indent=2)}

Requirements:
1. The tool must be a single Python function
2. It must be deterministic (same input → same output)
3. It must handle edge cases gracefully
4. It must return a value, not print
5. Include docstring with usage example

Format your response as:
```python
def tool_name(param1, param2, ...):
    \"\"\"
    Description of what this tool does.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value

    Example:
        >>> tool_name("example", 123)
        "expected output"
    \"\"\"
    # Implementation
    return result
```

TOOL_NAME: the name of your tool
TOOL_DESCRIPTION: one-line description"""

        try:
            response = self.llm(generation_prompt)

            # Extract code
            code = ""
            if "```python" in response:
                code = response.split("```python")[1].split("```")[0].strip()
            elif "```" in response:
                code = response.split("```")[1].split("```")[0].strip()

            # Extract name and description
            name = error_type.replace(" ", "_").lower() + "_fixer"
            description = f"Fixes {error_type} errors"

            for line in response.split("\n"):
                if line.startswith("TOOL_NAME:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("TOOL_DESCRIPTION:"):
                    description = line.split(":", 1)[1].strip()

            # Validate the code compiles
            compile(code, "<generated>", "exec")

            return GeneratedTool(
                name=name,
                description=description,
                code=code,
                failure_hashes=[f.hash for f in failures]
            )

        except Exception as e:
            print(f"Tool generation failed: {e}")
            return None

    def validate_tool(self, tool: GeneratedTool, test_cases: List[Dict]) -> bool:
        """
        Validate a generated tool against test cases.

        This is GROUND TRUTH validation - the tool either works or it doesn't.
        """
        try:
            # Execute tool code
            namespace = {}
            exec(tool.code, namespace)

            # Find the function
            func = None
            for name, obj in namespace.items():
                if callable(obj) and not name.startswith("_"):
                    func = obj
                    break

            if not func:
                return False

            # Test against cases
            for case in test_cases:
                input_val = case["input"]
                expected = case["expected"]

                if isinstance(input_val, dict):
                    result = func(**input_val)
                elif isinstance(input_val, (list, tuple)):
                    result = func(*input_val)
                else:
                    result = func(input_val)

                if result != expected:
                    return False

            return True

        except Exception as e:
            return False


class FailureDrivenLearner:
    """
    The core compounding loop:
    Failures → Analysis → Tool Generation → Fewer Failures → Repeat
    """

    def __init__(
        self,
        capability_registry,  # CapabilityRegistry
        tool_registry,  # ToolRegistry
        llm_executor: Callable[[str], str]
    ):
        self.capabilities = capability_registry
        self.tools = tool_registry
        self.llm = llm_executor

        self.analyzer = FailureAnalyzer(llm_executor)
        self.generator = ToolGenerator(llm_executor)

        # Failure history
        self.failures: List[Failure] = []
        self.generated_tools: List[GeneratedTool] = []

        # Metrics
        self.initial_failure_rate: Optional[float] = None
        self.current_failure_rate: Optional[float] = None

    def run_learning_cycle(self) -> Dict[str, Any]:
        """
        Run one complete learning cycle:
        1. Evaluate all capabilities
        2. Collect failures
        3. Analyze failures
        4. Generate tools for failure patterns
        5. Validate and register successful tools
        """
        cycle_stats = {
            "failures_collected": 0,
            "failures_analyzed": 0,
            "tools_generated": 0,
            "tools_validated": 0,
            "initial_success_rate": 0,
            "final_success_rate": 0
        }

        # Step 1: Evaluate and collect failures
        def executor(prompt, input_data):
            return self.llm(prompt)

        all_failures = self.capabilities.get_all_failures(executor)

        # Record initial success rates
        success_rates = self.capabilities.evaluate_all(executor)
        cycle_stats["initial_success_rate"] = sum(success_rates.values()) / len(success_rates) if success_rates else 0
        self.initial_failure_rate = 1 - cycle_stats["initial_success_rate"]

        # Step 2: Process failures
        new_failures = []
        for cap_name, cap_failures in all_failures.items():
            for f in cap_failures:
                failure = Failure(
                    capability_name=cap_name,
                    test_input=f["input"],
                    expected_output=f["expected"],
                    actual_output=f.get("actual", f.get("error", "unknown")),
                    prompt_used=f["prompt_used"]
                )
                new_failures.append(failure)

        cycle_stats["failures_collected"] = len(new_failures)

        # Step 3: Analyze failures
        for failure in new_failures:
            self.analyzer.analyze_failure(failure)
            cycle_stats["failures_analyzed"] += 1

        self.failures.extend(new_failures)

        # Step 4: Categorize and generate tools
        categories = self.analyzer.categorize_failures(new_failures)

        for error_type, type_failures in categories.items():
            if error_type in ["unknown", "unanalyzed"]:
                continue

            # Need at least 2 failures of same type to generate tool
            if len(type_failures) < 2:
                continue

            tool = self.generator.generate_tool(type_failures, error_type)
            if tool:
                cycle_stats["tools_generated"] += 1

                # Step 5: Validate tool
                test_cases = [
                    {"input": f.test_input, "expected": f.expected_output}
                    for f in type_failures
                ]

                if self.generator.validate_tool(tool, test_cases):
                    cycle_stats["tools_validated"] += 1
                    self.generated_tools.append(tool)

                    # Register with tool registry
                    # (Would need to wrap the generated code as a Tool object)
                    for f in type_failures:
                        f.tool_generated = tool.name
                        f.resolution = "Tool generated and validated"

        # Re-evaluate with new tools
        # (In practice, this would use the new tools in the evaluation)
        success_rates = self.capabilities.evaluate_all(executor)
        cycle_stats["final_success_rate"] = sum(success_rates.values()) / len(success_rates) if success_rates else 0
        self.current_failure_rate = 1 - cycle_stats["final_success_rate"]

        return cycle_stats

    def get_improvement_metrics(self) -> Dict[str, Any]:
        """Get metrics showing improvement over time."""
        return {
            "total_failures_recorded": len(self.failures),
            "total_tools_generated": len(self.generated_tools),
            "initial_failure_rate": self.initial_failure_rate,
            "current_failure_rate": self.current_failure_rate,
            "improvement": (
                (self.initial_failure_rate - self.current_failure_rate) / self.initial_failure_rate
                if self.initial_failure_rate and self.initial_failure_rate > 0
                else 0
            ),
            "effective_tools": [
                {"name": t.name, "effectiveness": t.effectiveness}
                for t in self.generated_tools
                if t.effectiveness > 0.5
            ]
        }
```

---

## Part 5: Integration - The Capability Enhancement Engine

Bringing it all together into a system that actually compounds.

### Implementation

```python
# src/byrd/capabilities/capability_enhancement_engine.py

from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import json

# Import the systems
# from .capability_system import CapabilityRegistry
# from .tool_augmented_reasoning import ToolRegistry, ToolAugmentedReasoner
# from .prompt_evolution import PromptEvolutionEngine
# from .failure_driven_learning import FailureDrivenLearner


@dataclass
class EnhancementCycleResult:
    """Result of one enhancement cycle."""
    cycle_number: int
    timestamp: str

    # Capability metrics
    capability_scores: Dict[str, float]
    avg_capability_score: float

    # Prompt evolution metrics
    prompts_evolved: int
    best_prompt_improvements: Dict[str, float]

    # Failure learning metrics
    failures_processed: int
    tools_generated: int
    tools_validated: int

    # Overall metrics
    improvement_from_baseline: float


class CapabilityEnhancementEngine:
    """
    The master system that orchestrates all enhancement mechanisms.

    This is what makes BYRD actually improve:
    1. Ground truth evaluation (not self-assessment)
    2. Prompt evolution (measured improvement)
    3. Tool generation (compounding capabilities)
    4. Failure-driven learning (turning mistakes into strengths)
    """

    def __init__(
        self,
        llm_executor: Callable[[str], str],
        neo4j_driver = None  # Optional Neo4j connection for persistence
    ):
        self.llm = llm_executor
        self.neo4j = neo4j_driver

        # Initialize subsystems
        self.capability_registry = CapabilityRegistry()
        self.tool_registry = ToolRegistry()

        self.reasoner = ToolAugmentedReasoner(llm_executor, self.tool_registry)
        self.prompt_evolver = PromptEvolutionEngine(
            self.capability_registry,
            llm_executor
        )
        self.failure_learner = FailureDrivenLearner(
            self.capability_registry,
            self.tool_registry,
            llm_executor
        )

        # Tracking
        self.cycle_history: list[EnhancementCycleResult] = []
        self.baseline_scores: Optional[Dict[str, float]] = None

    def establish_baseline(self) -> Dict[str, float]:
        """
        Establish baseline capability scores.
        This is the starting point for measuring improvement.
        """
        def executor(prompt, input_data):
            return self.llm(prompt)

        self.baseline_scores = self.capability_registry.evaluate_all(executor)

        if self.neo4j:
            self._persist_baseline()

        return self.baseline_scores

    def run_enhancement_cycle(self) -> EnhancementCycleResult:
        """
        Run one complete enhancement cycle.

        This is the core loop that makes BYRD smarter.
        """
        cycle_number = len(self.cycle_history) + 1

        # If no baseline, establish one
        if self.baseline_scores is None:
            self.establish_baseline()

        # Step 1: Run prompt evolution
        evolution_history = self.prompt_evolver.run_evolution(generations=5)
        prompts_evolved = sum(len(h) for h in evolution_history.values())

        # Calculate prompt improvements
        best_improvements = {}
        for cap_name, history in evolution_history.items():
            if history:
                initial = history[0].get("best_success_rate", 0)
                final = history[-1].get("best_success_rate", 0)
                best_improvements[cap_name] = final - initial

        # Step 2: Run failure-driven learning
        learning_stats = self.failure_learner.run_learning_cycle()

        # Step 3: Evaluate current capabilities
        def executor(prompt, input_data):
            return self.llm(prompt)

        current_scores = self.capability_registry.evaluate_all(executor)
        avg_score = sum(current_scores.values()) / len(current_scores) if current_scores else 0

        # Calculate improvement from baseline
        baseline_avg = sum(self.baseline_scores.values()) / len(self.baseline_scores) if self.baseline_scores else 0
        improvement = (avg_score - baseline_avg) / baseline_avg if baseline_avg > 0 else 0

        # Create result
        result = EnhancementCycleResult(
            cycle_number=cycle_number,
            timestamp=datetime.now().isoformat(),
            capability_scores=current_scores,
            avg_capability_score=avg_score,
            prompts_evolved=prompts_evolved,
            best_prompt_improvements=best_improvements,
            failures_processed=learning_stats["failures_analyzed"],
            tools_generated=learning_stats["tools_generated"],
            tools_validated=learning_stats["tools_validated"],
            improvement_from_baseline=improvement
        )

        self.cycle_history.append(result)

        if self.neo4j:
            self._persist_cycle_result(result)

        return result

    def run_continuous_enhancement(
        self,
        cycles: int = 10,
        target_improvement: float = 0.5,
        callback: Optional[Callable[[EnhancementCycleResult], None]] = None
    ) -> Dict[str, Any]:
        """
        Run multiple enhancement cycles until target improvement is reached.

        Args:
            cycles: Maximum number of cycles to run
            target_improvement: Target improvement over baseline (0.5 = 50% better)
            callback: Optional callback called after each cycle

        Returns:
            Summary of enhancement run
        """
        for i in range(cycles):
            result = self.run_enhancement_cycle()

            if callback:
                callback(result)

            # Check if target reached
            if result.improvement_from_baseline >= target_improvement:
                return {
                    "status": "target_reached",
                    "cycles_run": i + 1,
                    "final_improvement": result.improvement_from_baseline,
                    "final_scores": result.capability_scores,
                    "tools_generated": sum(r.tools_generated for r in self.cycle_history)
                }

        # Target not reached
        final_result = self.cycle_history[-1] if self.cycle_history else None
        return {
            "status": "max_cycles_reached",
            "cycles_run": cycles,
            "final_improvement": final_result.improvement_from_baseline if final_result else 0,
            "final_scores": final_result.capability_scores if final_result else {},
            "tools_generated": sum(r.tools_generated for r in self.cycle_history)
        }

    def get_enhancement_summary(self) -> Dict[str, Any]:
        """Get summary of all enhancement progress."""
        if not self.cycle_history:
            return {"status": "no_cycles_run"}

        return {
            "total_cycles": len(self.cycle_history),
            "baseline_scores": self.baseline_scores,
            "current_scores": self.cycle_history[-1].capability_scores,
            "total_improvement": self.cycle_history[-1].improvement_from_baseline,
            "total_tools_generated": sum(r.tools_generated for r in self.cycle_history),
            "total_tools_validated": sum(r.tools_validated for r in self.cycle_history),
            "capability_trajectory": [
                {"cycle": r.cycle_number, "avg_score": r.avg_capability_score}
                for r in self.cycle_history
            ]
        }

    def _persist_baseline(self):
        """Persist baseline to Neo4j."""
        if not self.neo4j:
            return

        with self.neo4j.session() as session:
            session.run("""
                MERGE (b:CapabilityBaseline {id: 'current'})
                SET b.scores = $scores,
                    b.timestamp = $timestamp
            """, {
                "scores": json.dumps(self.baseline_scores),
                "timestamp": datetime.now().isoformat()
            })

    def _persist_cycle_result(self, result: EnhancementCycleResult):
        """Persist cycle result to Neo4j."""
        if not self.neo4j:
            return

        with self.neo4j.session() as session:
            session.run("""
                CREATE (c:EnhancementCycle {
                    cycle_number: $cycle,
                    timestamp: $timestamp,
                    avg_score: $avg_score,
                    improvement: $improvement,
                    tools_generated: $tools_gen,
                    tools_validated: $tools_val
                })
            """, {
                "cycle": result.cycle_number,
                "timestamp": result.timestamp,
                "avg_score": result.avg_capability_score,
                "improvement": result.improvement_from_baseline,
                "tools_gen": result.tools_generated,
                "tools_val": result.tools_validated
            })


# Integration with BYRD's existing systems
def integrate_with_byrd(omega_instance, llm_executor):
    """
    Integrate the capability enhancement engine with BYRD's Omega system.

    This connects:
    - Enhancement engine → Omega's learning loops
    - Tool registry → BYRD's existing tool system
    - Capability metrics → BYRD's reflection system
    """
    engine = CapabilityEnhancementEngine(llm_executor)

    # Hook into Omega's improvement cycle
    def on_omega_improvement():
        """Called when Omega requests capability improvement."""
        result = engine.run_enhancement_cycle()

        # Feed back to Omega
        omega_instance.record_learning({
            "type": "capability_enhancement",
            "improvement": result.improvement_from_baseline,
            "tools_generated": result.tools_generated,
            "timestamp": result.timestamp
        })

        return result

    # Register with Omega
    if hasattr(omega_instance, 'register_improvement_hook'):
        omega_instance.register_improvement_hook(on_omega_improvement)

    return engine
```

---

## Key Differences from v1 and v2

| Aspect | v1/v2 | This Plan |
|--------|-------|-----------|
| Evaluation | Self-assessment (LLM grades itself) | Ground truth (test suites with known answers) |
| Improvement | Infrastructure only | Actual measured capability growth |
| Tools | External APIs | Generated from failures, validated |
| Prompts | Static | Evolved through tournament selection |
| Learning | Data accumulation | Compounding (failures → tools → fewer failures) |
| Verification | None | Every step has objective verification |

---

## Implementation Priority

1. **Week 1-2**: Implement `CapabilityRegistry` with test suites
   - Define test cases for arithmetic, logic, code generation
   - Build verification infrastructure
   - Establish baseline measurements

2. **Week 3-4**: Implement `ToolAugmentedReasoner`
   - Calculator tool (100% reliable arithmetic)
   - Code executor (sandboxed Python)
   - Memory search integration

3. **Week 5-6**: Implement `PromptEvolutionEngine`
   - Mutation operators
   - Tournament selection
   - Ground truth fitness evaluation

4. **Week 7-8**: Implement `FailureDrivenLearner`
   - Failure analysis pipeline
   - Tool generation from patterns
   - Validation and registration

5. **Week 9-10**: Integration and testing
   - Connect all systems
   - Run continuous enhancement
   - Measure compound improvement

---

## Success Metrics

**This plan succeeds if:**

1. Capability scores measurably increase over cycles
2. Generated tools actually solve the failures they were created for
3. Prompt evolution produces prompts that outperform originals
4. The system requires less human intervention over time
5. Improvement compounds (each cycle better than last)

**This plan fails if:**

1. Scores plateau quickly
2. Generated tools don't validate
3. Evolved prompts perform worse
4. The system needs constant human fixes
5. No compounding effect observed

---

## The Honest Assessment

This plan makes BYRD **a better system for using an LLM**, but it does not make the LLM itself smarter. The gains come from:

- Using the LLM for what it's good at (orchestration, pattern recognition)
- Offloading what it's bad at to reliable tools
- Finding better ways to prompt it
- Learning from failures systematically

This is not AGI. But it is **measurable, verifiable improvement** - which is more than most "AGI" systems achieve.

The path to AGI requires either:
- Better base models (beyond our control)
- Novel architectures (research-level work)
- Emergent capabilities from scale (requires more compute)

What we CAN do is make BYRD the best possible system for leveraging whatever LLM capabilities exist. That's what this plan delivers.

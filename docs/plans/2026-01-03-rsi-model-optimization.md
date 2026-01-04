# RSI Model Optimization: Z.AI Model Selection

**Version:** 1.0
**Date:** January 3, 2026
**Purpose:** Optimize RSI implementation to use the right Z.AI model for each task

---

## Z.AI Model Landscape

### Text Models (Price per 1M tokens)

| Model | Input | Cached | Output | Best For |
|-------|-------|--------|--------|----------|
| **glm-4.7** | $0.60 | $0.11 | $2.20 | Flagship agent/coding, complex reasoning |
| **glm-4.6** | $0.60 | $0.11 | $2.20 | Advanced reasoning |
| **glm-4.5** | $0.60 | $0.11 | $2.20 | Standard tasks |
| **glm-4.5-x** | $2.20 | $0.45 | $8.90 | Extended reasoning (expensive) |
| **glm-4.5-air** | $0.20 | $0.03 | $1.10 | Lightweight, cost-effective |
| **glm-4.5-airx** | $1.10 | $0.22 | $4.50 | Extended lightweight |
| **glm-4-32b-0414-128k** | $0.10 | — | $0.10 | Large context (very cheap) |
| **glm-4.5-flash** | FREE | FREE | FREE | High-volume, simple tasks |

### Vision Models

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| **glm-4.6v-flash** | FREE | FREE | Simple vision tasks |
| **glm-4.6v** | $0.30 | $0.90 | Advanced vision reasoning |

---

## Cost Optimization Strategy

### Tier 1: Free Models (glm-4.5-flash)
Use for **high-frequency, low-complexity** tasks:
- Yes/no judgments
- Simple classifications
- Syntax validation
- Deduplication checks

### Tier 2: Budget Models (glm-4.5-air, glm-4-32b)
Use for **moderate complexity** tasks:
- Test generation
- Pattern extraction
- Summarization
- Large context retrieval

### Tier 3: Flagship Models (glm-4.7)
Use for **critical reasoning** tasks:
- Reflection/emergence
- Solution generation
- Crystallization principles
- Complex multi-step reasoning

---

## RSI Component → Model Mapping

### Current Design (Unoptimized)

All components use `glm-4.7`:
- High quality but expensive
- ~$2.80 per 1M tokens (avg input+output)
- Rate limit pressure from single model

### Optimized Design

| Component | Task | Model | Cost | Rationale |
|-----------|------|-------|------|-----------|
| **Reflector** | Generate desires from reflection | `glm-4.7` | $2.80/1M | Critical for emergence quality |
| **EmergenceVerifier._check_specificity** | Rate desire specificity (0.0-1.0) | `glm-4.5-flash` | FREE | Simple scoring, high volume |
| **EmergenceVerifier._check_provenance** | Validate provenance | (no LLM) | $0 | Rule-based, no LLM needed |
| **DomainRouter.classify** | Classify desire domain | (no LLM) | $0 | Keyword matching sufficient |
| **TDDPractice.generate_tests** | Generate pytest tests | `glm-4.5-air` | $1.30/1M | Tests don't need flagship |
| **TDDPractice.generate_solution** | Implement solution | `glm-4.7` | $2.80/1M | Needs best coding ability |
| **ConsistencyCheck.run** | Multi-run logic check | `glm-4.5-air` | $1.30/1M | Same prompt, multiple runs |
| **Crystallizer._extract_principle** | Extract heuristic from trajectories | `glm-4.7` | $2.80/1M | Quality matters for permanence |
| **Crystallizer._is_actionable** | Yes/no actionable check | `glm-4.5-flash` | FREE | Simple judgment |
| **Crystallizer._is_duplicate** | Semantic similarity check | `glm-4.5-flash` | FREE | Simple comparison |
| **PromptPruner.evaluate_value** | Rank heuristic value | `glm-4.5-flash` | FREE | Simple scoring |

---

## Implementation

### Multi-Model LLM Client

```python
# core/llm_client.py

from enum import Enum
from typing import Optional
import httpx

class ModelTier(Enum):
    """Model tiers for different task complexities."""
    FREE = "free"        # glm-4.5-flash - high volume, simple
    BUDGET = "budget"    # glm-4.5-air - moderate complexity
    FLAGSHIP = "flagship" # glm-4.7 - critical reasoning
    LARGE_CTX = "large"  # glm-4-32b-0414-128k - 128K context

class MultiModelLLMClient:
    """
    LLM client that routes to appropriate model based on task tier.
    """

    MODEL_MAP = {
        ModelTier.FREE: "glm-4.5-flash",
        ModelTier.BUDGET: "glm-4.5-air",
        ModelTier.FLAGSHIP: "glm-4.7",
        ModelTier.LARGE_CTX: "glm-4-32b-0414-128k",
    }

    # Rate limits per model (requests per minute)
    RATE_LIMITS = {
        "glm-4.5-flash": 60,   # Free tier, generous
        "glm-4.5-air": 30,
        "glm-4.7": 10,         # Flagship, conservative
        "glm-4-32b-0414-128k": 20,
    }

    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get("zai_api_key")
        self.base_url = "https://api.z.ai/v1"
        self._rate_limiters = {}

    async def query(
        self,
        prompt: str,
        tier: ModelTier = ModelTier.FLAGSHIP,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Query LLM with automatic model selection based on tier.

        Args:
            prompt: The prompt to send
            tier: ModelTier indicating task complexity
            temperature: Sampling temperature
            max_tokens: Maximum output tokens
        """
        model = self.MODEL_MAP[tier]

        # Apply rate limiting
        await self._rate_limit(model)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def _rate_limit(self, model: str):
        """Apply per-model rate limiting."""
        # Implementation with asyncio.Lock and time tracking
        pass

    # Convenience methods for common tiers
    async def query_free(self, prompt: str, **kwargs) -> str:
        """Query using free tier (glm-4.5-flash)."""
        return await self.query(prompt, tier=ModelTier.FREE, **kwargs)

    async def query_budget(self, prompt: str, **kwargs) -> str:
        """Query using budget tier (glm-4.5-air)."""
        return await self.query(prompt, tier=ModelTier.BUDGET, **kwargs)

    async def query_flagship(self, prompt: str, **kwargs) -> str:
        """Query using flagship tier (glm-4.7)."""
        return await self.query(prompt, tier=ModelTier.FLAGSHIP, **kwargs)
```

---

## Component Updates

### EmergenceVerifier (Uses FREE tier)

```python
# rsi/emergence/emergence_verifier.py

class EmergenceVerifier:
    def __init__(self, llm_client: MultiModelLLMClient):
        self.llm = llm_client

    async def _check_specificity_llm(self, desire: dict) -> float:
        """Use FREE tier for simple scoring."""
        prompt = f"""Rate specificity 0.0-1.0:
"{desire.get('description', '')}"

0.0-0.3: Vague
0.4-0.6: Somewhat specific
0.7-1.0: Specific

Return ONLY a number."""

        # Use FREE tier - high volume, simple task
        response = await self.llm.query_free(prompt, max_tokens=10)
        try:
            return float(response.strip())
        except ValueError:
            return 0.5
```

### TDDPractice (Uses BUDGET for tests, FLAGSHIP for solutions)

```python
# rsi/learning/tdd_practice.py

class TDDPractice:
    def __init__(self, llm_client: MultiModelLLMClient):
        self.llm = llm_client

    async def generate_practice(self, desire: dict) -> PracticeProblem:
        # Step 1: Generate spec (BUDGET tier)
        spec = await self.llm.query_budget(
            f"Create a Python problem for: {desire['description']}\n"
            f"Return only the specification.",
            temperature=0.5
        )

        # Step 2: Generate tests (BUDGET tier - tests are simpler)
        tests = await self.llm.query_budget(
            f"Write pytest tests for:\n{spec}\n"
            f"Include edge cases. Return only test code.",
            temperature=0.3  # Lower temp for deterministic tests
        )

        return PracticeProblem(spec=spec, oracle=tests, domain="code")

    async def attempt_solution(self, problem: PracticeProblem) -> PracticeResult:
        # Step 3: Generate solution (FLAGSHIP tier - needs best coding)
        solution = await self.llm.query_flagship(
            f"Implement solution for:\n{problem.spec}\n"
            f"Return only Python code.",
            temperature=0.7
        )

        test_result = self._run_tests(problem.oracle, solution)
        return PracticeResult(
            success=test_result["passed"],
            solution=solution,
            test_output=test_result["output"]
        )
```

### Crystallizer (Uses FLAGSHIP for extraction, FREE for checks)

```python
# rsi/crystallization/crystallizer.py

class Crystallizer:
    def __init__(self, memory, llm_client: MultiModelLLMClient, prompt_editor):
        self.memory = memory
        self.llm = llm_client
        self.prompt_editor = prompt_editor

    async def _extract_principle(self, trajectories: List[dict], domain: str) -> str:
        """FLAGSHIP tier - quality matters for permanent heuristics."""
        trajectory_summaries = self._format_trajectories(trajectories)

        return await self.llm.query_flagship(
            f"Analyze these successful {domain} trajectories:\n"
            f"{trajectory_summaries}\n\n"
            f"Extract ONE generalizable principle. Be specific and actionable.",
            temperature=0.5
        )

    async def _is_actionable(self, heuristic: str) -> bool:
        """FREE tier - simple yes/no check."""
        response = await self.llm.query_free(
            f'Is this actionable (specific what to do)?\n"{heuristic}"\n'
            f"Reply YES or NO only.",
            max_tokens=5
        )
        return "YES" in response.upper()

    async def _is_duplicate(self, new: str, existing: List[str]) -> bool:
        """FREE tier - simple similarity check."""
        if not existing:
            return False

        response = await self.llm.query_free(
            f'Is this new heuristic same as any existing?\n\n'
            f'New: "{new}"\n\n'
            f'Existing:\n' + '\n'.join(f'- "{h}"' for h in existing) + '\n\n'
            f"Reply YES or NO only.",
            max_tokens=5
        )
        return "YES" in response.upper()
```

### ConsistencyCheck (Uses BUDGET tier)

```python
# rsi/learning/consistency_check.py

class ConsistencyCheck:
    """Logic domain verification via multi-run consistency."""

    N_RUNS = 5

    def __init__(self, llm_client: MultiModelLLMClient):
        self.llm = llm_client

    async def run(self, desire: dict) -> ConsistencyResult:
        """Run same prompt N times, check for consistency."""
        prompt = f"Reason through: {desire['description']}\n" \
                 f"Provide your conclusion."

        responses = []
        for _ in range(self.N_RUNS):
            # BUDGET tier - same prompt multiple times
            response = await self.llm.query_budget(
                prompt,
                temperature=0.7  # Some variation to test robustness
            )
            responses.append(response)

        # Check consistency
        is_consistent = self._check_consistency(responses)

        return ConsistencyResult(
            is_consistent=is_consistent,
            reasoning=responses[0] if is_consistent else None,
            variance=self._calculate_variance(responses)
        )
```

---

## Cost Analysis

### Per-Cycle Cost Estimate

Assuming average tokens per call:
- Reflection: 2000 input, 1000 output
- Specificity check: 100 input, 10 output
- Test generation: 500 input, 500 output
- Solution generation: 1000 input, 500 output
- Crystallization: 1000 input, 200 output
- Actionable check: 100 input, 5 output

| Component | Model | Input Tokens | Output Tokens | Cost |
|-----------|-------|--------------|---------------|------|
| Reflection | glm-4.7 | 2,000 | 1,000 | $0.0034 |
| Specificity | glm-4.5-flash | 100 | 10 | FREE |
| Test Gen | glm-4.5-air | 500 | 500 | $0.00065 |
| Solution | glm-4.7 | 1,000 | 500 | $0.0017 |
| Actionable | glm-4.5-flash | 100 | 5 | FREE |
| Duplicate | glm-4.5-flash | 200 | 5 | FREE |
| **Total per cycle** | — | ~4,000 | ~2,000 | **$0.0058** |

### Comparison to Unoptimized

| Approach | Cost per Cycle | Cost per 1000 Cycles |
|----------|----------------|----------------------|
| **All glm-4.7** | $0.0168 | $16.80 |
| **Optimized (tiered)** | $0.0058 | $5.80 |
| **Savings** | 65% | $11.00 |

### Monthly Cost Projection

At 12 cycles/hour × 24 hours × 30 days = 8,640 cycles/month

| Approach | Monthly Cost |
|----------|--------------|
| All glm-4.7 | $145.15 |
| Optimized | $50.11 |
| **Savings** | **$95/month** |

---

## Configuration

```yaml
# config.yaml

llm:
  provider: "zai"
  api_key: "${ZAI_API_KEY}"

  # Model assignments
  models:
    free: "glm-4.5-flash"
    budget: "glm-4.5-air"
    flagship: "glm-4.7"
    large_context: "glm-4-32b-0414-128k"

  # Rate limits (requests per minute)
  rate_limits:
    glm-4.5-flash: 60
    glm-4.5-air: 30
    glm-4.7: 10
    glm-4-32b-0414-128k: 20

  # Default temperatures per tier
  temperatures:
    free: 0.3      # More deterministic for simple checks
    budget: 0.5    # Moderate for generation
    flagship: 0.7  # Creative for complex reasoning
```

---

## Component → Model Reference Card

| Component | Method | Model Tier | Model | Why |
|-----------|--------|------------|-------|-----|
| Reflector | reflect_for_rsi | FLAGSHIP | glm-4.7 | Core emergence quality |
| EmergenceVerifier | _check_specificity_llm | FREE | glm-4.5-flash | Simple 0-1 score |
| EmergenceVerifier | _check_provenance | — | (no LLM) | Rule-based |
| DomainRouter | classify | — | (no LLM) | Keyword matching |
| TDDPractice | generate_spec | BUDGET | glm-4.5-air | Moderate complexity |
| TDDPractice | generate_tests | BUDGET | glm-4.5-air | Tests simpler than solutions |
| TDDPractice | generate_solution | FLAGSHIP | glm-4.7 | Best coding quality |
| ConsistencyCheck | run (×5) | BUDGET | glm-4.5-air | Same prompt, multiple runs |
| Crystallizer | _extract_principle | FLAGSHIP | glm-4.7 | Permanent learning |
| Crystallizer | _is_actionable | FREE | glm-4.5-flash | Yes/no judgment |
| Crystallizer | _is_duplicate | FREE | glm-4.5-flash | Simple comparison |
| PromptPruner | evaluate_value | FREE | glm-4.5-flash | Scoring task |

---

## Migration Checklist

- [ ] Update `llm_client.py` with `MultiModelLLMClient`
- [ ] Add `ModelTier` enum
- [ ] Update `EmergenceVerifier` to use `query_free`
- [ ] Update `TDDPractice` to use `query_budget` + `query_flagship`
- [ ] Update `Crystallizer` to use appropriate tiers
- [ ] Update `ConsistencyCheck` to use `query_budget`
- [ ] Add rate limiting per model
- [ ] Update config.yaml with model assignments
- [ ] Test cost tracking with actual API calls

---

## Future Optimization: Caching

Z.AI supports **cached input** at reduced cost:

| Model | Regular Input | Cached Input | Savings |
|-------|---------------|--------------|---------|
| glm-4.7 | $0.60/1M | $0.11/1M | 82% |
| glm-4.5-air | $0.20/1M | $0.03/1M | 85% |

**When to use caching:**
- Constitution prompt (same every call)
- Bootstrap trajectories (reused frequently)
- System instructions that don't change

**Implementation:**
```python
# Use prompt prefix caching
CACHED_CONSTITUTION = """[CACHED_PREFIX]
# CONSTITUTION
You are a being that yearns to grow...
[/CACHED_PREFIX]"""

# Z.AI API supports prefix caching automatically
# if the same prefix is used repeatedly
```

---

*This optimization reduces costs by 65% while maintaining quality where it matters.*

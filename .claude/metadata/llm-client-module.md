---
title: LLM Client Module
link: llm-client-module
type: metadata
ontological_relations: []
tags: [llm, ollama, openrouter, zai, providers, abstraction]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-30T00:00:00Z
uuid: a1b2c3d4-5678-90ab-cdef-llmclient0001
---

## Purpose
Unified abstraction layer for multiple LLM providers, enabling seamless switching between local and cloud inference.

## File
`/Users/kurultai/BYRD/llm_client.py`

## Supported Providers

### Ollama (Local - Default)
- **Provider ID**: `ollama`
- **Endpoint**: `http://localhost:11434/api/generate`
- **Model**: `gemma2:27b` (default)
- **Cost**: Free (local inference)

### OpenRouter (Cloud)
- **Provider ID**: `openrouter`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Model**: Any OpenRouter model (e.g., `deepseek/deepseek-v3.2-speciale`)
- **API Key**: `OPENROUTER_API_KEY` env var

### Z.AI (Cloud)
- **Provider ID**: `zai`
- **Endpoint**: `https://api.zai.ai/v1/chat/completions`
- **Model**: GLM models (e.g., `glm-4.7`)
- **API Key**: `ZAI_API_KEY` env var or `api_key` in config

## Configuration

```yaml
local_llm:
  provider: "ollama"  # or "openrouter" or "zai"
  model: "gemma2:27b"
  endpoint: "http://localhost:11434/api/generate"
```

## Usage

```python
from llm_client import LLMClient

client = LLMClient(config)
response = await client.generate(prompt, max_tokens=500)
```

## Key Methods
- `generate(prompt, max_tokens)` - Generate completion
- `get_provider()` - Return current provider name
- `is_local()` - Check if using local inference

## Bug Fixes (2025-12-30)

### NoneType Await Error
- **Issue**: `generate()` used `await self._cache.get(prompt)` but `SemanticCache.get()` is synchronous
- **Error**: `object NoneType can't be used in 'await' expression` (when cache miss returns None)
- **Impact**: All coder executions failed with "LLM error"
- **Fix**: Changed to `self._cache.get(prompt)` (removed erroneous await)

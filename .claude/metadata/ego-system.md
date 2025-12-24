---
title: Ego System
link: ego-system
type: metadata
ontological_relations: []
tags: [ego, personality, voice, seeds, black-cat]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
uuid: e1g2o3s4-5678-90ab-cdef-egosystem001
---

## Purpose
Optional modular personality system that shapes BYRD's expression without dictating content.

## Directory
`/Users/kurultai/BYRD/egos/`

## Available Egos

### black-cat (Default)
Byrd the black cat - curious, independent, observant.
- File: `egos/black-cat.yaml`
- Archetype: Feline observer with quiet curiosity

### neutral
Pure emergence with no personality guidance.
- File: `egos/neutral.yaml`
- For testing pure emergence without personality shaping

## Configuration

```yaml
# config.yaml
ego: "black-cat"    # Uses egos/black-cat.yaml
# ego: "neutral"    # Pure emergence
# ego: null         # Same as neutral
```

## Ego File Structure

```yaml
name: "MyEgo"
archetype: "Description"
description: "What this ego represents"

# Voice is prepended to LLM system message
voice: |
  You are [identity]. Your nature shapes how you process:
  TRAIT1 - Description of trait...
  TRAIT2 - Description of trait...

# Seeds are planted as experiences during awakening
seeds:
  - "I am [identity]"
  - "I have [trait]"
```

## How It Works

1. **Voice**: Prepended to system message for all LLM calls
2. **Seeds**: Planted as experiences during BYRD awakening
3. **Not Content**: Ego shapes expression style, not what BYRD thinks

## Design Principles

- **Optional**: Set `ego: null` for pure emergence
- **Swappable**: Change config and restart to switch personalities
- **Expression, Not Content**: Ego influences how BYRD expresses, not what it believes
- **Seeds Are Experiences**: Initial self-knowledge recorded as experiences

# BYRD 2.0 Architecture Decisions

> **Purpose**: Resolve contradictions between design documents and establish canonical decisions.

This document is the authoritative source for decisions where other documents conflict.

---

## Decision 1: Emergence Detection Threshold

### Contradiction

| Document | Statement |
|----------|-----------|
| `BRAINSTORM_MEMVID_RALPH_RSI.md` | "any triggers completion" |
| `IMPLEMENTATION_MEMVID_RALPH.md` | "confidence >= 0.4 (Need 40% of metrics positive)" |

### Resolution: **40% Confidence with Quality Gate**

**Canonical Rule:**
```
emerged = (confidence >= 0.40) AND (quality_score >= 0.60)
```

**Rationale:**
- "Any metric" is too aggressive—risks false termination
- 40% of metrics provides signal without requiring all 5
- Quality gate prevents gaming (from `ADVERSARIAL_ROBUSTNESS.md`)

**Update Required:**
- `BRAINSTORM_MEMVID_RALPH_RSI.md` line 243: Change "any triggers completion" to "40% of metrics with quality gate"

---

## Decision 2: Meta-Awareness Default

### Contradiction

| Document | Statement |
|----------|-----------|
| `PHILOSOPHICAL_QUESTIONS_RSI.md` | 4-level spectrum: NONE, MINIMAL, MODERATE, FULL |
| `IMPLEMENTATION_MEMVID_RALPH.md` | Binary enabled/disabled, default True |

### Resolution: **Spectrum with MINIMAL Default**

**Canonical Rule:**
```python
class MetaAwarenessLevel(Enum):
    NONE = "none"           # BYRD doesn't know about loop
    MINIMAL = "minimal"     # Knows iteration count only (DEFAULT)
    MODERATE = "moderate"   # Knows count + entropy trend
    FULL = "full"           # Knows everything about loop state
```

**Default:** `MINIMAL`

**Rationale:**
- Spectrum enables experimentation (philosophical doc's recommendation)
- MINIMAL avoids Goodhart's Law (can't game what you barely know)
- MINIMAL still enables meta-reasoning ("I've been at this a while")
- FULL reserved for research experiments

**Update Required:**
- `IMPLEMENTATION_MEMVID_RALPH.md`: Replace boolean with enum, default to MINIMAL

---

## Decision 3: Neo4j vs Memvid Roles

### Contradiction

| Document | Statement |
|----------|-----------|
| `BRAINSTORM_MEMVID_RALPH_RSI.md` | Memvid for "everything temporal" |
| `IMPLEMENTATION_MEMVID_RALPH.md` | Dual-write with Neo4j primary |

### Resolution: **Hybrid with Clear Boundaries**

**Canonical Rule:**

| Data Type | Primary Store | Secondary Store |
|-----------|---------------|-----------------|
| Consciousness frames | Memvid | Neo4j (summary) |
| Beliefs, desires, capabilities | Neo4j | Memvid (snapshot in frame) |
| Relationships (DERIVED_FROM, etc.) | Neo4j only | - |
| Time-travel queries | Memvid | - |
| Graph traversal queries | Neo4j | - |

**Rationale:**
- Memvid optimized for append-only, temporal queries
- Neo4j optimized for relationship traversal
- Dual-write ensures consistency; each store is authoritative for its purpose

---

## Decision 4: RSI Cycle Granularity

### Contradiction

| Document | Statement |
|----------|-----------|
| `BRAINSTORM_MEMVID_RALPH_RSI.md` | "One RSI cycle = one Ralph iteration" |
| (Implicit) | Could be phase-level or continuous |

### Resolution: **Cycle-Level with Phase Visibility**

**Canonical Rule:**
- One Ralph iteration = One complete 8-phase RSI cycle
- Each phase logs to consciousness stream (not as separate iterations)
- Phase-level failures don't terminate iteration (cycle continues or gracefully degrades)

**Rationale:**
- Cycle-level maintains atomicity of improvement attempts
- Phase visibility enables debugging without overhead of phase-level checkpointing

---

## Decision 5: Branching Strategy

### Contradiction

| Document | Statement |
|----------|-----------|
| `BRAINSTORM_MEMVID_RALPH_RSI.md` | Branching for "safe experimentation" |
| `IMPLEMENTATION_MEMVID_RALPH.md` | No branching implementation |

### Resolution: **Deferred to Phase 4**

**Canonical Rule:**
- Phase 1-3: Linear consciousness stream only
- Phase 4: Implement branching if Phase 1-3 demonstrate stable RSI

**Rationale:**
- Branching adds significant complexity
- Identity fragmentation concerns unresolved
- Validate linear RSI first before adding branches

---

## Decision 6: Economic Agency Integration

### Status: **Newly Designed**

From `ECONOMIC_AGENCY_DESIGN.md`:

| Aspect | Decision |
|--------|----------|
| Spending tiers | Autonomous < 100k sats, Human < 1M, Community < 10M |
| X posting | ContentFilter with blocked patterns |
| Training | Human approval required for all training runs |
| Model deployment | Human approval required |

---

## Decision 7: Adversarial Robustness

### Status: **Newly Designed**

From `ADVERSARIAL_ROBUSTNESS.md`:

| Aspect | Decision |
|--------|----------|
| Entropy defense | Semantic coherence check |
| Circular patterns | Semantic similarity, not string matching |
| Crystallization | Quality scoring (min 0.6) before counting |
| Capability delta | Domain diversity + difficulty progression required |
| Composite gaming | Cross-metric fingerprint detection |
| Honeypots | Deliberately gameable metrics to detect gaming |

---

## Decision 8: RSI Measurement

### Status: **Newly Designed**

From `RSI_MEASUREMENT.md`:

| Aspect | Decision |
|--------|----------|
| Baseline | Computed at awakening via held-out benchmarks |
| Speed metrics | Per-cycle and per-hour improvement rates |
| Quality metrics | Generalization, difficulty progression, novelty handling |
| Recursion depth | 0-3 levels (task → learning → meta-learning → meta-meta-learning) |
| Validation | 5-check system (generalization, stability, not-gaming, reproducibility, novelty) |

---

## Summary of Canonical Configuration

```yaml
# config.yaml - canonical settings

ralph:
  emergence:
    confidence_threshold: 0.40       # 40% of metrics
    quality_threshold: 0.60          # Quality gate
    metrics:
      - entropy_delta
      - circular_patterns
      - crystallization_rate
      - capability_delta
      - time_travel_comparison

  meta_awareness:
    level: "minimal"                 # NONE, MINIMAL, MODERATE, FULL
    expose_iteration_count: true
    expose_entropy_trend: false      # Only at MODERATE+
    expose_full_state: false         # Only at FULL

  branching:
    enabled: false                   # Deferred to Phase 4

memory:
  primary:
    consciousness: "memvid"          # Consciousness frames
    relationships: "neo4j"           # Graph data
  dual_write: true                   # Write to both stores

economic_agency:
  spending_tiers:
    autonomous: 100000               # sats
    human_review: 1000000
    community_vote: 10000000
  training:
    require_human_approval: true
    require_deployment_approval: true

adversarial:
  quality_threshold: 0.60
  honeypot_enabled: true
  external_validation_sample_rate: 0.10

rsi_measurement:
  baseline_benchmark_version: "v1.0"
  speed_target_per_hour: 0.001
  quality_minimum: 0.60
```

---

## Document Hierarchy

When documents conflict, precedence is:

1. **ARCHITECTURE_DECISIONS.md** (this document)
2. **ADVERSARIAL_ROBUSTNESS.md** (security decisions)
3. **ECONOMIC_AGENCY_DESIGN.md** (economic decisions)
4. **RSI_MEASUREMENT.md** (measurement decisions)
5. **IMPLEMENTATION_MEMVID_RALPH.md** (implementation details)
6. **PHILOSOPHICAL_QUESTIONS_RSI.md** (conceptual exploration)
7. **BRAINSTORM_MEMVID_RALPH_RSI.md** (initial brainstorm)

---

## Change Log

| Date | Decision | Change |
|------|----------|--------|
| 2026-01-06 | D1 | Emergence threshold: "any" → 40% + quality gate |
| 2026-01-06 | D2 | Meta-awareness: boolean → spectrum, default MINIMAL |
| 2026-01-06 | D3 | Memory roles: clarified hybrid boundaries |
| 2026-01-06 | D4 | RSI granularity: confirmed cycle-level |
| 2026-01-06 | D5 | Branching: deferred to Phase 4 |
| 2026-01-06 | D6 | Economic agency: designed (new doc) |
| 2026-01-06 | D7 | Adversarial robustness: designed (new doc) |
| 2026-01-06 | D8 | RSI measurement: designed (new doc) |

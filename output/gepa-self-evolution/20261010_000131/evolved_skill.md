---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution Pipeline

Skill optimization via genetic prompt evolution for Hermes Agent skills.

**Location:** `/home/Hermes/repos/gepa/`

## Current Status

**As of June 2, 2026:** Fully operational with LLM judge metric.

The legacy `structural_score()` heuristic was replaced because it became saturated — 73% of skills scored 1.0, offering no differentiation. The new **4-dimension LLM-as-judge** (`llm_judge.py`) provides real headroom:

| Metric | Range | Median |
|--------|-------|--------|
| LLM Judge (4-dim) | 0.175 – 0.865 | 0.698 |
| Structural (legacy) | Saturated at 1.0 | — |

**Usage:**
- Default: Uses legacy `structural_score()` (no LLM calls)
- Opt-in: `--use-judge` flag or `GEPA_USE_JUDGE=1` env var enables LLM judge
- **Note:** Cron jobs still run on the legacy metric by default

## Architecture

### Data Flow

Input Skill
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  generate_all_datasets_fast.py                              │
│  • Zero LLM calls                                           │
│  • Heuristic template matching                              │
│  • Output: datasets/skills/<name>/                           │
│    ├─ train.jsonl (7 examples)                              │
│    ├─ val.jsonl   (2 examples)                              │
│    └─ holdout.jsonl (1 example)                             │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  run_evolution_batch.py                                     │
│  • Direct MiniMax API (no DSPy/GEPA wrapper)                │
│  • Truncates SKILL.md to 2500 chars                         │
│  • Single API call: temp=0.5, max_tokens=8192               │
│  • Prompt format:                                          │
│    "Improve this skill: <name>"                             │
│    "Requirements: <specific/actionable/ordering>"           │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  validate_skill()                                           │
│  • Must start with `---`                                    │
│  • Must have `name:` and `description:`                      │
│  • Length: 200 – 25000 chars                                │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Scoring                                                    │
│  • LLM Judge (--use-judge): 4-dimension evaluation         │
│  • Structural (legacy): Fast heuristic, no LLM              │
└─────────────────────────────────────────────────────────────┘
### Manifest v2.0 (June 1 Update)

| Field | Description |
|-------|-------------|
| `round` | Current evolution round |
| `next_index` | Next skill to process |
| `order` | Processing sequence |

### Cron Behavior Change

| Mode | Behavior | Impact |
|------|----------|--------|
| Legacy (`--all`) | Batch processes all skills | Hits 429 rate limit |
| Current (`--mode one`) | Single skill per tick | Persistent state, avoids rate limits |

### Rate Limiting

Automatic retry with exponential backoff on 429 responses:

| Attempt | Delay |
|---------|-------|
| 1st retry | 30 seconds |
| 2nd retry | 60 seconds |
| 3rd retry | 120 seconds |

## Key Files

| File | Purpose |
|------|---------|
| `run_evolution_batch.py` | Batch orchestrator — processes pending skills from manifest |
| `generate_all_datasets_fast.py` | Dataset generator — zero LLM calls, 227 skills processed |
| `evolution_manifest.json` | Tracks skill status: `pending` / `evolved` / `failed` / `no_improvement` |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Fast structural fitness metric (legacy, no LLM in hot loop) |
| `llm_judge.py` | 4-dimension LLM-as-judge scoring |

## Input Convention

Skill files follow a **flat layout** at:

~/.hermes/skills/<name>/SKILL.md
> ⚠️ Not `~/.hermes/hermes-agent/skills/<name>/SKILL.md`

## Critical Lessons

1. **LLM judges saturate over time** — build headroom into scoring dimensions
2. **Batch processing hits rate limits** — single-skill-per-tick with persistent state scales better
3. **Zero-LLM dataset generation is viable** — heuristic template matching avoids expensive API calls
4. **Truncation matters** — 2500 char limit ensures focused optimization targets
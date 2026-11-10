---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution Pipeline

Genetic prompt evolution system for automated Hermes Agent skill optimization. Located at `/home/Hermes/repos/gepa/`.

## Quick Status

| Metric | Value |
|--------|-------|
| **Metric System** | LLM-as-judge (4-dim) with structural fallback |
| **Judge Score Range** | 0.175–0.865 (median: 0.698, n=51 skills) |
| **Datasets Generated** | 227 skills, zero LLM calls |
| **Default Mode** | Structural metric (LLM judge opt-in via `--use-judge` or `GEPA_USE_JUDGE=1`) |

## Core Components

### 1. Batch Orchestrator
**`run_evolution_batch.py`**

Processes pending skills from the manifest. Direct MiniMax API calls (no DSPy/GEPA wrapper in the hot path).

Input truncation: SKILL.md → 2500 chars max
API parameters: temperature=0.5, max_tokens=8192
Prompt template: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"
### 2. Dataset Generator
**`generate_all_datasets_fast.py`**

Heuristic template matching — produces training data without any LLM calls.

**Output per skill** (`datasets/skills/<name>/`):
- `train.jsonl` — 7 examples
- `val.jsonl` — 2 examples  
- `holdout.jsonl` — 1 example

### 3. Evolution Loop
**`evolution/skills/evolve_skill.py`**

Per-skill optimization loop with validation gate.

**Validation requirements:**
- Must start with `---` (YAML frontmatter)
- Must contain `name:` and `description:` fields
- Length: 200–25,000 characters

### 4. Scoring Modules

| Module | Type | Notes |
|--------|------|-------|
| `llm_judge.py` | LLM-as-judge (4-dim) | Primary metric, real headroom available |
| `fitness.py` | Structural heuristic | Legacy fallback; saturated at ~73% of skills scoring 1.0 |

### 5. Skill Wrapper
**`evolution/skills/skill_module.py`**

DSPy module wrapping a skill for optimization.

## Manifest Schema

**`evolution_manifest.json`** tracks all skills with these v2.0 fields:

| Field | Purpose |
|-------|---------|
| `round` | Current evolution round |
| `next_index` | Next candidate index to try |
| `order` | Processing order |
| `status` | `pending`, `evolved`, `failed`, or `no_improvement` |

## Processing Pipeline

1. INPUT
   ~/.hermes/skills/<name>/SKILL.md  (flat layout, NOT hermes-agent/skills/)

2. DATASET GENERATION
   generate_all_datasets_fast.py
   → Zero LLM calls
   → Updates evolution_manifest.json

3. BATCH PROCESSING
   run_evolution_batch.py [--mode one]
   → Truncates skill to 2500 chars
   → Single API call per skill
   → 429 handling: exponential backoff (30s → 60s → 120s)

4. VALIDATION
   validate_skill()
   → Checks frontmatter, required fields, length

5. SCORING
   llm_judge_score() OR structural_score()
   → Judge enabled via --use-judge or GEPA_USE_JUDGE=1
## Operation Modes

| Mode | Flag | Behavior |
|------|------|----------|
| Batch | `--all` | Processes all pending skills (rate-limited, hits 429) |
| Single | `--mode one` | Processes one skill per cron tick, maintains persistent state |

**Default:** Single mode for cron jobs (avoids rate limiting).

## Critical Implementation Notes

1. **Skill path layout:** Skills live at `~/.hermes/skills/<name>/SKILL.md` (flat), not in `hermes-agent/skills/`
2. **LLM judge is opt-in:** Default cron uses structural metric; use `--use-judge` or `GEPA_USE_JUDGE=1` to enable
3. **Zero-LLM dataset generation:** Datasets are produced via template matching heuristics only
4. **Direct API calls:** Batch runner calls MiniMax API directly, bypassing DSPy/GEPA in the critical path
5. **Rate-limit resilience:** 429 responses trigger automatic exponential backoff retries
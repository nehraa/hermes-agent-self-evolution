---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution Pipeline

Skill optimization via genetic prompt evolution. Installed at `/home/Hermes/repos/gepa/`.

## Current Status

**Opt-in LLM Judge Metric** (June 2, 2026)

The legacy `structural_score()` heuristic saturated at 73% of skills scoring 1.0, providing no useful signal.

The new **LLM-as-judge** (`llm_judge.py`) uses 4 dimensions with real headroom:
- Backtest range: 0.175–0.865
- Median: 0.698

Enable via `--use-judge` flag or `GEPA_USE_JUDGE=1` env var. Default: OFF (cron still uses old metric).

## Core Files

| File | Purpose |
|---|---|
| `run_evolution_batch.py` | Batch runner — processes pending skills from manifest |
| `generate_all_datasets_fast.py` | Dataset generator — **zero LLM calls**, 227 skills complete |
| `evolution_manifest.json` | Tracks status per skill: `pending`, `evolved`, `failed`, `no_improvement` |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Fast structural fitness metric (no LLM in hot loop) |

## Architecture

Input: ~/.hermes/skills/<name>/SKILL.md        ← flat layout (not hermes-agent/skills/)
  │
  ▼
generate_all_datasets_fast.py
  ├─ Zero LLM calls (heuristic template matching)
  ├─ Output: datasets/skills/<name>/train.jsonl
  │   └─ 7 train / 2 val / 1 holdout
  └─ Updates: evolution_manifest.json
  │
  ▼
run_evolution_batch.py
  ├─ Direct MiniMax API (bypasses DSPy/GEPA)
  ├─ Truncates SKILL.md to 2500 chars
  ├─ Prompt: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"
  ├─ Single API call: temperature=0.5, max_tokens=8192
  └─ 429 handling: exponential backoff (30s → 60s → 120s)
  │
  ▼
validate_skill()
  ├─ Must start with `---`
  ├─ Must have `name:` and `description:`
  └─ Size: 200–25000 chars
  │
  ▼
Scoring
  ├─ llm_judge_score()    ← primary (with --use-judge)
  └─ structural_score()   ← legacy fallback
## Cron Configuration

- **Mode**: `--mode one` (single skill per tick)
- **Previous**: `--all` caused rate limit errors (429 hits)
- **State**: Persistent across ticks via manifest

## Workflow

1. **Generate datasets** — `generate_all_datasets_fast.py` creates training data without LLM calls
2. **Batch evolve** — `run_evolution_batch.py` sends truncated skill to MiniMax API
3. **Validate** — Ensures output has proper frontmatter and valid size
4. **Score** — LLM judge or structural metric evaluates improvement
5. **Update manifest** — Records status for next cron tick

## Critical Lessons

- **Use LLM judge** over structural scoring for meaningful optimization signal
- **Batch mode causes 429s** — single-skill mode is more reliable for cron
- **Zero-LLM dataset generation** is viable via heuristic template matching
- **Manifest v2.0** tracks `round`, `next_index`, `order` fields for stateful evolution
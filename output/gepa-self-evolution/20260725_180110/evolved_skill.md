---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution Pipeline

## Overview

Automated skill optimization via genetic prompt evolution. Installed at `/home/Hermes/repos/gepa/`.

**Current Status (June 2026):** Operational with LLM-as-judge metric. The legacy `structural_score()` heuristic was replaced because 73% of skills scored 1.0 (saturated). The new 4-dimensional LLM judge shows meaningful range: 0.175–0.865 with median 0.698 (backtested on 51 on-disk skills).

## Quick Start

bash
# Single skill (interactive)
cd /home/Hermes/repos/gepa
python run_evolution_batch.py --mode one --skill <skill_name>

# All pending skills (batch)
python run_evolution_batch.py --mode batch

# Enable LLM judge (opt-in)
python run_evolution_batch.py --mode batch --use-judge
# or
GEPA_USE_JUDGE=1 python run_evolution_batch.py --mode batch
## Architecture

Input: ~/.hermes/skills/<name>/SKILL.md          ← FLAT layout
  │
  ├─► generate_all_datasets_fast.py              ← Zero LLM calls
  │     └──► datasets/skills/<name>/train.jsonl  ← 7 train / 2 val / 1 holdout
  │     └──► evolution_manifest.json
  │
  └─► run_evolution_batch.py                     ← Direct MiniMax API
        ├── Truncates SKILL.md to 2500 chars
        ├── Single API call: temp=0.5, max_tokens=8192
        └── Prompts: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"
              │
              ▼
        validate_skill()                         ← Starts with ---, has name:/description:, 200-25000 chars
              │
              ▼
        Fitness Scoring (--use-judge flag)
        ├── llm_judge_score()   ← 4-dim evaluation (new default when flag enabled)
        └── structural_score()  ← Legacy fallback (fast, no LLM)
## Core Components

| File | Purpose |
|---|---|
| `run_evolution_batch.py` | Batch orchestrator — processes pending skills from manifest, calls MiniMax API directly |
| `generate_all_datasets_fast.py` | Dataset generator — uses heuristic template matching, **zero LLM calls** (227 skills complete) |
| `evolution_manifest.json` | State tracker — records `pending`, `evolved`, `failed`, or `no_improvement` per skill |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Fitness scoring — contains both `llm_judge_score()` and `structural_score()` |

## Configuration

| Setting | Default | Description |
|---|---|---|
| `--mode one` | Single skill per cron tick | Persistent state, avoids rate limits |
| `--mode batch` | All pending skills | Hits 429 without rate-limit handling |
| `--use-judge` | OFF | Enable 4-dim LLM judge metric |
| `GEPA_USE_JUDGE=1` | OFF | Env var alternative to `--use-judge` |
| Rate-limit retries | 30s / 60s / 120s | Exponential backoff on 429 responses |

## Critical Lessons

### #11: Judge Metric Selection

The `structural_score()` heuristic saturated at 1.0 for 73% of skills — no headroom for differentiation.

**Solution:** 4-dimensional LLM-as-judge (`llm_judge.py`) produces a 0.175–0.865 range (median 0.698) across real skills.

**Trade-offs:**
- **Use `--use-judge`**: Better scoring fidelity, slower evaluation
- **Use default (structural)**: Faster, suitable for cron stability testing

The LLM judge is opt-in because it adds latency to the hot evaluation loop.

### #12: Manifest v2.0 Schema

Manifest upgraded with new tracking fields:

json
{
  "skills": {
    "<skill_name>": {
      "status": "pending",
      "round": 1,
      "next_index": 0,
      "order": 3
    }
  }
### #13: Rate-Limit Resilience

`--mode one` processes one skill per cron tick, maintaining persistent state. `--mode batch` requires rate-limit retry logic (30s/60s/120s backoff) to avoid 429 errors.

## Output Artifacts

After evolution:
- `~/.hermes/skills/<name>/SKILL.md` — Improved skill definition
- `datasets/skills/<name>/train.jsonl` — Generated training data
- `evolution_manifest.json` — Updated status and metrics
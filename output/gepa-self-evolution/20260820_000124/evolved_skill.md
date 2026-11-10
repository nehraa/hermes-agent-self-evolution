---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution Pipeline

Skill optimization via genetic prompt evolution for Hermes Agent skills. Installed at `/home/Hermes/repos/gepa/`.

## Quick Start

bash
# Single skill evolution
python run_evolution_batch.py --name <skill-name>

# Batch process all pending skills
python run_evolution_batch.py --mode one

# Use LLM-as-judge metric (recommended)
python run_evolution_batch.py --name <skill-name> --use-judge
# or via environment variable
GEPA_USE_JUDGE=1 python run_evolution_batch.py --name <skill-name>
## Architecture

Input: ~/.hermes/skills/<name>/SKILL.md   ← Flat layout (NOT hermes-agent/skills/)
  │
  ├─► generate_all_datasets_fast.py       ← Zero LLM calls, heuristic template matching
  │     └─► datasets/skills/<name>/
  │           ├─ train.jsonl (7 samples)
  │           ├─ val.jsonl (2 samples)
  │           └─ holdout.jsonl (1 sample)
  │
  └─► run_evolution_batch.py               ← Batch orchestrator, direct MiniMax API
        ├─ Truncates SKILL.md to 2500 chars
        ├─ Sends single API call (temp=0.5, max_tokens=8192)
        └─ Prompts: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"

Validation: Must start with ---, have name:/description:, 200-25000 chars

Scoring (choose one):
  ├─► llm_judge_score()     ← NEW: 4-dim LLM-as-judge (opt-in via --use-judge)
  └─► structural_score()    ← Legacy: fast heuristic (saturated, ~73% at 1.0)
## Key Files

| File | Purpose |
|---|---|
| `run_evolution_batch.py` | Batch orchestrator — processes pending skills from manifest |
| `generate_all_datasets_fast.py` | Dataset generator — zero LLM calls, uses heuristic template matching |
| `evolution_manifest.json` | Tracks skill status: `pending`, `evolved`, `failed`, `no_improvement` |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Structural fitness metric (legacy, no LLM in hot loop) |
| `llm_judge.py` | LLM-as-judge scoring (4-dimensional metric) |

## Manifest v2.0 Schema

json
{
  "skills": {
    "<skill-name>": {
      "round": 0,
      "next_index": 0,
      "order": 1,
      "status": "pending"
    }
  }
}
## Scoring Metrics

### LLM-as-Judge (Recommended)

The new 4-dimensional judge provides real headroom:

- **Range observed:** 0.175–0.865 across 51 on-disk skills
- **Median score:** 0.698
- **Opt-in:** `--use-judge` flag or `GEPA_USE_JUDGE=1`

### Structural Score (Legacy)

- Fast heuristic-based metric
- **Saturated:** ~73% of skills score 1.0
- **Default:** Used when judge is not enabled
- **Note:** Cron jobs still use this metric by default

## Rate Limiting

Automatic retry with exponential backoff on 429 responses:

| Attempt | Delay |
|---------|-------|
| 1 | 30s |
| 2 | 60s |
| 3 | 120s |

## Critical Notes

1. **Skill location:** Skills must be at `~/.hermes/skills/<name>/SKILL.md` (flat layout)
2. **LLM judge is opt-in:** Default OFF; cron jobs still use legacy structural metric
3. **Dataset generation is free:** `generate_all_datasets_fast.py` uses zero LLM calls
4. **Batch mode:** Use `--mode one` to process one skill per cron tick (avoids 429 rate limits)
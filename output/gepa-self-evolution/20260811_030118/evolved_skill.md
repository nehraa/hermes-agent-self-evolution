---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# GEPA Self-Evolution

Skill optimization via genetic prompt evolution. Installed at `/home/Hermes/repos/gepa/`.

## Quick Start

bash
# Run batch evolution (all pending skills)
python run_evolution_batch.py

# Process a single skill
python run_evolution_batch.py --mode one --skill <name>

# Use LLM judge metric (recommended)
python run_evolution_batch.py --use-judge --skill <name>
## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEPA_USE_JUDGE` | `0` | Enable LLM-as-judge metric (recommended: `1`) |
| `GEPA_API_KEY` | — | MiniMax API key (required) |

## Key Files

| File | Purpose |
|------|---------|
| `run_evolution_batch.py` | Batch runner — processes pending skills from manifest |
| `generate_all_datasets_fast.py` | Dataset generator — zero LLM calls, heuristic template matching |
| `evolution_manifest.json` | Tracks skill status: `pending` / `evolved` / `failed` / `no_improvement` |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Structural fitness metric (legacy, no LLM in hot loop) |
| `llm_judge.py` | 4-dimension LLM-as-judge metric (replaces structural) |

## Evolution Flow

Input: ~/.hermes/skills/<name>/SKILL.md   ← Flat layout
  ↓
generate_all_datasets_fast.py
  → Zero LLM calls, heuristic template matching
  → datasets/skills/<name>/{train.jsonl, val.jsonl, holdout.jsonl}
     (7 train / 2 val / 1 holdout)
  → Updates evolution_manifest.json
  ↓
run_evolution_batch.py
  → Truncates SKILL.md to 2500 chars
  → Builds prompt: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"
  → Single MiniMax API call (temperature=0.5, max_tokens=8192)
  ↓
validate_skill()
  → Must start with `---`
  → Must contain `name:` and `description:`
  → Length: 200–25000 chars
  ↓
Fitness Evaluation
  → llm_judge_score() — 4-dim LLM-as-judge (opt-in via --use-judge)
  → structural_score() — legacy heuristic fallback
## Metrics

### LLM-as-Judge (Recommended)

4-dimension evaluation with real headroom. Replaced the saturated `structural_score()` heuristic (73% of skills at 1.0).

**Backtest results on 51 on-disk skills:**
- Range: 0.175–0.865
- Median: 0.698

Enable via `--use-judge` flag or `GEPA_USE_JUDGE=1`.

### Structural Score (Legacy)

Fast heuristic metric used by default. No LLM calls in hot loop. Being phased out in favor of LLM judge.

## Manifest v2.0

Fields added June 1:
- `round` — evolution round number
- `next_index` — next prompt index to try
- `order` — processing order

## Cron Configuration

Default cron runs `--mode one` (single skill per tick) to avoid 429 rate limits.

**Rate limit handling:**
- 429 responses trigger exponential backoff
- Delays: 30s → 60s → 120s

## Status (June 2, 2026)

- **Operational** with LLM judge metric
- LLM judge is opt-in; default is legacy structural metric
- Zero-LLM dataset generation: 227 skills processed

## Critical Lessons

- **#11:** LLM judge metric provides real evaluation headroom vs. saturated heuristics
- Use `--use-judge` for meaningful skill improvements
- Cron defaults to old metric; update to include `--use-judge`
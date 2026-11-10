---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

A 4-dimensional LLM-as-judge quality metric for SKILL.md files. Replaced the saturated `structural_score()` heuristic in GEPA self-evolution. Located at `/home/Hermes/repos/gepa/llm_judge.py`.

## When to Use

- Scoring SKILL.md files for quality (single or batch)
- A/B comparing two versions of a skill (rewrites, edits, refactors)
- Building dashboards of skill quality across a corpus
- Answering "is this skill good enough to deploy"

## The Rubric

Weights: **specificity 30%, completeness 30%, structure 20%, conciseness 20%**

Composite score is the weighted average. Expected range on real skills: **0.175 to 0.865**. Reserve **0.9+** for genuinely excellent skills only.

| Dimension | Weight | What It Measures | High Score Means |
|-----------|--------|------------------|------------------|
| **specificity** | 30% | Real commands, paths, code blocks vs hand-waving | Agent can execute without guessing |
| **completeness** | 30% | Triggers, steps, pitfalls, verification, examples | Agent has everything needed to succeed |
| **structure** | 20% | YAML frontmatter, headings, parseable markdown | Well-formed, navigable, has trigger section |
| **conciseness** | 20% | Information density, no filler | Length matches complexity, no bloat |

## Invocation

### Python API

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)
**Return value:**

python
{
    "specificity": 0.90,   # float 0-1
    "completeness": 0.78,  # float 0-1
    "structure": 0.85,     # float 0-1
    "conciseness": 0.80,   # float 0-1
    "composite": 0.835,    # weighted average
    "notes": "Concrete commands, full workflow coverage, slight redundancy"
}
Returns `None` on API failure. Caller should fall back or skip scoring.

### Backtest (no skill files written)

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
Saves `backtest_scores.json` with full distribution and per-skill results.

## Noise Characteristics

Even at temperature 0.1, the same skill scores vary **±0.05** across runs (stdev ~0.03, range ~0.09).

**Deployment decision rules:**
- Use a threshold spread of **≥ 0.05** to avoid deploying on judge stochasticity
- Do **not** average single-run scores
- Measure with a consistent seed and accept the noise floor, OR cache a baseline and only remeasure deltas

## Output Format

Return a complete YAML frontmatter block (no markdown outside the block). Include these fields:

- `name`: skill identifier
- `description`: one-line summary
- `category`: skill category
- `content`: rest of document after frontmatter
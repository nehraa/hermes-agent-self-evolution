---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

An LLM-as-judge quality metric for SKILL.md files, replacing the saturated `structural_score()` heuristic in GEPA self-evolution. Provides a 4-dimensional quality assessment with weighted composite scoring.

**Location:** `/home/Hermes/repos/gepa/llm_judge.py`

---

## When to Use

- Scoring individual SKILL.md files for quality assurance
- A/B comparing two versions of the same skill (rewrites, edits, refactors)
- Building dashboards tracking skill quality across a corpus
- Gatekeeping: "Is this skill good enough to deploy?"
- Evaluating skill submissions in an evolution pipeline

---

## The Rubric

Four independent dimensions, each scored 0–1. **Reserve 0.9+ for genuinely excellent skills.** Real-world range observed: 0.175–0.865.

| Dimension | Weight | What It Measures | High Score Means |
|-----------|--------|------------------|------------------|
| **specificity** | 30% | Real commands, paths, code blocks, concrete examples | Agent can execute without guessing or filling gaps |
| **completeness** | 30% | Triggers, steps, pitfalls, edge cases, verification, examples | Agent has everything needed to succeed |
| **structure** | 20% | YAML frontmatter, headings, parseable markdown | Well-formed, navigable, includes trigger section |
| **conciseness** | 20% | Information density, no filler or redundancy | Length matches complexity; no bloat |

**Composite Score** = weighted average of all four dimensions.

---

## Usage

### Python API

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)
**Return value** — a dict with scores and notes, or `None` on API failure:

python
{
    "structure": 0.85,
    "specificity": 0.90,
    "completeness": 0.78,
    "conciseness": 0.80,
    "composite": 0.835,
    "notes": "Concrete commands, full workflow coverage, slight redundancy in examples"
}
**Error handling:** When `result is None` (API failure), callers should fall back to a default score or skip the evaluation.

### Backtesting (No Skill Files Required)

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
Output: `backtest_scores.json` with full distribution and per-skill results.

---

## Measurement Noise

**Critical:** Even with `temperature=0.1`, the same skill scores vary ±0.05 across runs:

- Standard deviation ≈ 0.03
- Range ≈ 0.09 between runs

### Deployment Guidelines

1. **Use a 0.05+ threshold buffer** — do not deploy based on scores near your cutoff due to judge stochasticity
2. **Do not average single-run scores** — this masks noise rather than reducing it
3. **Use consistent seed** for reproducible measurement, or cache a baseline and measure deltas only

### Recommended Decision Process

If new_skill_score - baseline_score >= 0.05:
    → Accept improvement (confident signal above noise)
Else:
    → Request human review or require multiple confirmations
---

## Interpreting Scores

| Composite Range | Interpretation |
|-----------------|----------------|
| 0.9+ | Exceptional — genuinely excellent skill |
| 0.75–0.89 | Good — deployable with minor polish |
| 0.5–0.74 | Needs work — missing specificity or completeness |
| < 0.5 | Poor — significant gaps, do not deploy |

Use `notes` field to identify specific weaknesses for targeted revision.
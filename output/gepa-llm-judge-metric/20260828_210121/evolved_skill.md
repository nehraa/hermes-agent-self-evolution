---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

The quality metric that replaced the saturated `structural_score()` heuristic in GEPA self-evolution. Located at `/home/Hermes/repos/gepa/llm_judge.py`.

## When to Use

Use this skill when you need to:

- Score a single SKILL.md file for quality (0–1 scale per dimension)
- A/B compare two versions of the same skill (e.g., before/after a rewrite)
- Build dashboards tracking skill quality across a corpus
- Answer "is this skill good enough to deploy?"

## The Rubric: 4 Dimensions

Composite score = weighted average of four dimensions.

| Dimension | Weight | What It Measures | High Score Means |
|---|---|---|---|
| **specificity** | 30% | Concrete details: real commands, actual paths, complete code blocks | Agent can execute without ambiguity or guessing |
| **completeness** | 30% | All required sections: triggers, steps, pitfalls, verification, examples | Agent has everything needed to succeed |
| **conciseness** | 20% | Information density; no filler or redundant prose | Length matches complexity; nothing wasted |
| **structure** | 20% | Valid YAML frontmatter, proper headings, parseable markdown | Well-formed, navigable, has trigger section |

**Observed range:** 0.175 (poor) to 0.865 (excellent) on real skills. Reserve 0.9+ for genuinely elite skills. Do not expect scores above 0.9 for typical写得 content.

## How to Invoke

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)

# Example result:
# {
#   "structure": 0.85,
#   "specificity": 0.90,
#   "completeness": 0.78,
#   "conciseness": 0.80,
#   "composite": 0.835,
#   "notes": "Concrete commands, full workflow coverage, slight redundancy in examples"
# }

# Returns None if API call fails — caller must handle fallback or skip
if result is None:
    # handle error: log, use fallback heuristic, or skip scoring
    pass
## Running Backtests

Test the judge on existing skills (no skill files written):

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
Output: `backtest_scores.json` with full distribution and per-skill results.

## Noise Characteristics

**Important:** Even at temperature 0.1, the same skill varies ±0.05 across runs (stdev ≈ 0.03, range ≈ 0.09).

**Deployment rule:** Use a threshold of ≥ 0.05 gap above your baseline when making deploy/no-deploy decisions. This avoids deploying on judge stochasticity alone.

**Do not average multiple runs.** Instead:
- Use a consistent random seed for reproducibility
- Accept the noise floor as inherent to LLM-as-judge
- OR cache a baseline score and only measure deltas from it
---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

A 4-dimensional LLM-as-judge metric for scoring SKILL.md files. Replaced the saturated `structural_score()` heuristic in GEPA self-evolution. Lives at `/home/Hermes/repos/gepa/llm_judge.py`.

## When to Use

Score any SKILL.md file when you need to:

- Evaluate a skill's quality before deployment
- A/B compare two versions (rewrites, edits, refactors)
- Track skill quality over time across a corpus
- Answer "is this skill good enough to ship?"

## The Rubric

**Weights:** specificity 30% · completeness 30% · structure 20% · conciseness 20%

**Composite score:** weighted average of all four dimensions

**Range observed:** 0.175 (poor) to 0.865 (excellent) on real skills  
**Deployment threshold:** ≥ 0.85 recommended; reserve 0.9+ for genuinely excellent skills

| Dimension | What It Measures | High Score Looks Like |
|-----------|------------------|-----------------------|
| **specificity** (30%) | Concrete details vs. hand-waving | Real commands, exact paths, working code blocks; agent can act without guessing |
| **completeness** (30%) | Coverage of what agent needs | Triggers, steps, pitfalls, verification, examples all present |
| **structure** (20%) | Parseable, navigable format | YAML frontmatter, markdown headings, trigger section defined |
| **conciseness** (20%) | Information density | Length matches complexity; no filler prose or redundant sections |

## Invocation

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)
**Return value:**

python
{
    "specificity": 0.90,
    "completeness": 0.78,
    "structure": 0.85,
    "conciseness": 0.80,
    "composite": 0.835,
    "notes": "Concrete commands, full workflow coverage, slight redundancy in examples"
}
**Error handling:** Returns `None` if the API call fails. Caller should fall back to a default score or skip scoring.

## Running the Backtest

No skill files written during backtest—just evaluate the judge itself:

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
**Output:** `backtest_scores.json` containing full score distribution and per-skill results.

## Noise Characteristics

The judge has inherent stochasticity—even at temperature 0.1:

| Statistic | Value |
|-----------|-------|
| Standard deviation | ~0.03 |
| Range across runs | ~0.09 |
| Typical variation | ±0.05 |

**Deployment decisions:** Use a threshold of ≥ 0.05 to avoid deploying on judge noise. Do not average single-run scores.

**Recommended approach:**
1. Run with a consistent seed
2. Accept the noise floor as inherent
3. OR cache a baseline and only measure deltas against it

## Tips

- A skill scoring 0.85+ typically has working code blocks, clear triggers, and explicit verification steps
- Low specificity scores usually mean missing exact commands or placeholder paths
- Low conciseness scores mean either bloated prose or terse where detail is needed
- The judge rewards *actionable specificity*—commands that actually work, not vague descriptions of what to do
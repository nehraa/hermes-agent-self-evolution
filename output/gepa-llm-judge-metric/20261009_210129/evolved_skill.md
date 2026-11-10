---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

An LLM-as-judge quality metric for SKILL.md files, replacing the saturated `structural_score()` heuristic in GEPA self-evolution. Located at `/home/Hermes/repos/gepa/llm_judge.py`.

**Composite score** is a weighted average of four dimensions. Range observed on real skills: 0.175 to 0.865. Reserve scores ≥ 0.90 for genuinely excellent skills.

## When to Use

- Scoring individual SKILL.md files for quality
- A/B comparing two versions of a skill (rewrites, edits, refactors)
- Building dashboards of skill quality across a corpus
- Evaluating "is this skill good enough" for deployment

## The Rubric

| Dimension | Weight | What it Measures | High Score Indicators |
|-----------|--------|------------------|----------------------|
| **completeness** | 30% | Agent has everything needed to succeed | Triggers, step-by-step instructions, pitfalls, verification steps, concrete examples |
| **specificity** | 30% | Agent can follow without guessing | Real commands, actual paths, working code blocks, named files/functions, specific values |
| **conciseness** | 20% | No wasted words or bloat | Length matches complexity, no filler prose, information-dense |
| **structure** | 20% | Well-formed and navigable markdown | Valid YAML frontmatter, clear headings, parseable format, explicit trigger section |

### Dimension Details

**completeness (30%)** — Does the skill contain all components an agent needs?
- ✅ Triggers that fire the skill
- ✅ Ordered steps with clear intent
- ✅ Known failure modes and pitfalls
- ✅ Verification/reproduction steps
- ✅ Working examples
- ❌ "See documentation" without specifics
- ❌ Implicit knowledge left to inference

**specificity (30%)** — Are instructions actionable without ambiguity?
- ✅ Exact commands (`python script.py --flag value`)
- ✅ Real paths (`/home/Hermes/repos/gepa/utils.py`)
- ✅ Named functions, classes, variables
- ✅ Specific thresholds, timeouts, retry counts
- ❌ "run the script"
- ❌ "configure appropriately"

**conciseness (20%)** — Does length match complexity?
- ✅ Brief rationale when helpful, silent when obvious
- ✅ Bulleted steps that fit on one screen
- ✅ Code comments that add signal, not noise
- ❌ Repeating the same point in different words
- ❌ Prose when a list would suffice

**structure (20%)** — Is the markdown well-formed?
- ✅ Valid YAML frontmatter with name/description/category
- ✅ Clear heading hierarchy (## for sections, ### for subsections)
- ✅ Trigger section is identifiable
- ✅ Code fences with language tags
- ❌ Malformed YAML (will break parsing)
- ❌ Orphan headings with no content

## Usage

### Python API

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)
**Return value:**
python
{
    "structure": 0.85,   # 0-1
    "specificity": 0.90, # 0-1
    "completeness": 0.78, # 0-1
    "conciseness": 0.80,  # 0-1
    "composite": 0.835,   # weighted average
    "notes": "Concrete commands, full workflow coverage, slight redundancy"
}
Returns `None` if the API call fails. Callers should fall back to a default score or skip scoring.

### CLI Backtest

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
Saves `backtest_scores.json` with full distribution statistics and per-skill breakdown.

## Noise and Deployment Decisions

**Expect ±0.05 score variance** across runs on the same skill (stdev ≈ 0.03, range ≈ 0.09) even at temperature 0.1.

### Guidelines

1. **Use a consistent random seed** when comparing scores across time or versions
2. **Cache baseline scores** for skills under evaluation; only remeasure deltas
3. **Apply ≥ 0.05 threshold** for deployment decisions — avoid deploying on judge stochasticity alone
4. **Do not average** single-run scores from different invocations — the noise is correlated with the model, not independent
5. **Report stdev** alongside mean when aggregating multiple skills
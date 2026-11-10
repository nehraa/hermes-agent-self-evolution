---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

The metric that replaced the saturated `structural_score()` heuristic in
GEPA self-evolution. Lives at `/home/Hermes/repos/gepa/llm_judge.py`.

## When to use
- Scoring SKILL.md / skill files for quality
- A/B comparing two versions of a skill (rewrites, edits, refactors)
- Building dashboards of skill quality across a corpus
- Any "is this skill good enough" question

## The rubric (4 dims, 0-1 each)

Weights: **structure 20%, specificity 30%, completeness 30%, conciseness 20%**.
Composite is the weighted average. Min-max range observed: 0.175 to 0.865
on real skills. Reserve 0.9+ for genuinely excellent skills.

| Dimension | What it measures | High score means |
|---|---|---|
| structure (20%) | YAML frontmatter, headings, parseable markdown | Well-formed, navigable, has trigger section |
| specificity (30%) | Real commands, paths, code blocks vs hand-waving | Agent can follow without guessing |
| completeness (30%) | Triggers, steps, pitfalls, verification, examples | Agent has everything it needs to succeed |
| conciseness (20%) | Information density, no bloat | No filler prose, length matches complexity |

## How to invoke

```python
from llm_judge import judge_skill, _load_api_key
api_key = _load_api_key()
result = judge_skill(skill_text, "skill_name", api_key=api_key)
# result = {
#   "structure": 0.85, "specificity": 0.90, "completeness": 0.78, "conciseness": 0.80,
#   "composite": 0.835, "notes": "Concrete commands, full workflow coverage, slight redundancy"
# }
# result is None if API fails (caller should fall back or skip)
```

Backtest (no skill files written):
```bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
# Saves backtest_scores.json with full distribution + per-skill results
```

## Noise characteristics

**Important:** Even at temperature 0.1, the same skill scores vary ±0.05
across runs (stdev ~0.03, range ~0.09). For deployment decisions, use
threshold ≥ 0.05 to avoid deploying on judge stochasticity. Do not
average single-run scores — measure with consistent seed and accept the
noise floor, OR cache baseline and only re-judge evolved (deltas
partially cancel noise).

## Cost

~5-10s per call to MiniMax-M2.7 (with think blocks). ~$0.02-0.04 per
skill judge. For a 51-skill corpus: ~$1-2 one-shot. For GEPA round with
1 call/attempt (baseline cached): ~$0.50/round.

## Failure modes

- ~5% of calls return None (transient 429, timeout, or model
  outputting a malformed response). Always handle None gracefully.
- Long skills (>12k chars) get truncated at 12k chars with a
  "truncated for judging" marker. If the dropped content is critical,
  pre-summarize or split.
- Model emits think blocks before the JSON. The parser handles this
  (strips `<think>...</think>` first), but very long think blocks can
  exhaust max_tokens=1500 before the JSON.

## What the judge actually flags well

Real issues the judge has caught in the corpus:
- Duplicate YAML frontmatter (1+ skills, e.g. adhd-body-doubling)
- "Marketing brochure" skills with no actionable commands
  (proactive-agent-lite, ci-cd-pipeline)
- Missing "When to use" / trigger sections (many)
- External file references that don't exist in the skill
  (e.g. `references/protocols.md` not present)
- Tables and code blocks used effectively (rewarded)
- Bloat from promotional content at the end of skills

## What the judge misses / gets wrong

- Doesn't actually run the skill against a real task
- Can't detect if commands would fail at runtime
- Can't measure transfer learning to novel tasks
- A skill that "looks good" but is fundamentally wrong can still
  score 0.8+ (form matters more than substance in this rubric)

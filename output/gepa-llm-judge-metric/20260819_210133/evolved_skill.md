---
name: gepa-llm-judge-metric
description: "The 4-dim LLM-as-judge skill quality metric that replaced the saturated structural_score() in GEPA self-evolution. Use when scoring SKILL.md files for completeness, specificity, conciseness, and structure on a 0-1 scale with real headroom."
category: autonomous-ai-agents
---

# GEPA LLM Judge Metric

An LLM-as-judge rubric for scoring SKILL.md quality across four dimensions. Replaced the saturated `structural_score()` heuristic in GEPA self-evolution.

**Location:** `/home/Hermes/repos/gepa/llm_judge.py`

---

## When to Use

- **Evaluate** a single skill file for quality before deployment
- **Compare** two versions of the same skill (e.g., before/after a rewrite)
- **Audit** a corpus of skills for dashboards or regression detection
- **Gate** promotion: "is this skill good enough to ship?"

---

## The Rubric

Weights: **specificity 30%, completeness 30%, structure 20%, conciseness 20%**

Composite score = weighted average of the four dimensions.

| Dimension | Weight | What It Measures | High Score Means |
|-----------|--------|------------------|------------------|
| **specificity** | 30% | Concrete details vs abstract hand-waving | Real paths, exact commands, named parameters, no guessing |
| **completeness** | 30% | Coverage of the full skill lifecycle | Triggers, steps, pitfalls, edge cases, verification, examples |
| **structure** | 20% | Parseable formatting | Valid YAML frontmatter, markdown headings, trigger section present |
| **conciseness** | 20% | Information density | No filler prose; length proportional to complexity |

### Expected Score Range

| Score | Interpretation |
|-------|----------------|
| 0.0–0.3 | Missing core content; undeployable |
| 0.3–0.5 | Has basics but gaps in specificity or completeness |
| 0.5–0.7 | Production-ready for non-critical skills |
| 0.7–0.85 | Strong; ready for most deployments |
| 0.85–0.9 | Excellent; reserve for genuinely polished skills |
| 0.9+ | Reserve for exceptional, proven-in-production skills |

**Observed range on real skills:** 0.175 to 0.865

---

## How to Invoke

### Python API

python
from llm_judge import judge_skill, _load_api_key

api_key = _load_api_key()

# Score a skill string
result = judge_skill(skill_text, "skill_name", api_key=api_key)

if result is not None:
    print(f"Structure:     {result['structure']}")
    print(f"Specificity:   {result['specificity']}")
    print(f"Completeness:  {result['completeness']}")
    print(f"Conciseness:   {result['conciseness']}")
    print(f"Composite:     {result['completeness']}")
    print(f"Notes:         {result['notes']}")
else:
    print("Judge unavailable; fall back to heuristic scoring")
**Return value:** `dict` with keys `structure`, `specificity`, `completeness`, `conciseness`, `composite`, `notes`. Returns `None` if the API call fails—callers must handle this gracefully.

---

### Backtest Command

Evaluate the judge itself against a corpus:

bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
Outputs `backtest_scores.json` with:
- Full score distribution
- Per-skill breakdown with judge notes
- Useful for calibrating thresholds or detecting judge drift

---

## Noise Characteristics

The judge is non-deterministic even at low temperature.

### Observed Variance

| Metric | Value |
|--------|-------|
| Standard deviation | ~0.03 |
| Range across runs | ~0.09 |
| Confidence interval | ±0.05 |

### Deployment Decision Rules

1. **Use a 0.05 margin** when gating on judge scores—do not promote or demote on a single-run difference smaller than this.
2. **Do not average** multiple runs to reduce variance. Instead:
   - Fix the random seed (`seed_everything` or equivalent) for reproducibility
   - Cache baseline scores for comparison sets
3. **For critical decisions**, run the judge 3 times and take the median.

### Example Threshold Logic

python
def is_ready_for_deployment(score: float, threshold: float = 0.7) -> bool:
    return score >= threshold + 0.05  # 0.05 margin for judge noise
---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| `None` returned | API key missing or request failed | Check `HERMES_` env vars; implement fallback scoring |
| All scores near 0.5 | Judge is uncertain; skill has ambiguous content | Add concrete examples and specific commands |
| Scores vary >0.1 | Unusually noisy run or judge prompt drift | Re-run with fixed seed; check for prompt changes |
| Notes say "vague" or "generic" | Lacking specific paths, commands, or parameters | Audit for hand-wavy phrasing; add real examples |
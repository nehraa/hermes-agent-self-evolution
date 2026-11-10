---
name: gepa-self-evolution
description: "Self-improvement pipeline for Hermes Agent skills — GEPA-based skill optimization with zero-LLM-call dataset generation and batch processing"
category: autonomous-ai-agents
---

# Self-Evolution with GEPA

## What
Skill optimization via genetic prompt evolution. Installed at `/home/Hermes/repos/gepa/`.

**Status (June 2, 2026): Operational with LLM judge metric.** The saturated `structural_score()` heuristic (73% of skills at 1.0) was replaced with a 4-dim LLM-as-judge (`llm_judge.py`) that has real headroom — backtest of 51 on-disk skills shows a 0.175-0.865 range with median 0.698. Opt-in via `--use-judge` flag or `GEPA_USE_JUDGE=1` env. Default OFF (cron still uses old metric). See Critical Lesson #11 below.

**Architecture (June 1 update):** Manifest upgraded to v2.0 with `round`, `next_index`, `order` fields. Cron switched from `--all` (batch, hits 429) to `--mode one` (single skill per tick, persistent state). Rate-limit handling added: 429 retries with 30s/60s/120s exponential backoff.

## Key Files

| File | Purpose |
|---|---|
| `run_evolution_batch.py` | Batch runner — processes all pending skills from manifest |
| `generate_all_datasets_fast.py` | Dataset generator — ZERO LLM calls, 227 skills done |
| `evolution_manifest.json` | Tracks status of each skill (pending/evolved/failed/no_improvement) |
| `evolution/skills/evolve_skill.py` | Per-skill evolution loop |
| `evolution/skills/skill_module.py` | DSPy module wrapping a skill for optimization |
| `evolution/core/fitness.py` | Fast structural fitness metric (no LLM in hot loop) |

## Architecture

```
Input: ~/.hermes/skills/<name>/SKILL.md   ← FLAT layout (not hermes-agent/skills/)
  ↓
generate_all_datasets_fast.py            ← Zero LLM calls, heuristic template matching
  → datasets/skills/<name>/train.jsonl    ← 7 train / 2 val / 1 holdout
  → evolution_manifest.json
  ↓
run_evolution_batch.py                   ← Direct MiniMax API (NOT DSPy/GEPA), batch orchestrator
  → SKILL.md truncated to 2500 chars
  → Prompt: "Improve this skill: [name] — Requirements: [specific/actionable/ordering]"
  → Single API call, temperature=0.5, max_tokens=8192
  ↓
validate_skill()                          ← Must start with ---, have name:/description:, 200-25000 chars
  ↓
llm_judge_score() or structural_score()  ← LLM judge (4-dim) is the new metric (--use-judge).
                                          ← structural is the legacy fallback.
                                          ← LLM judge has real headroom (0.175-0.865 range);
                                          ← structural was saturated (73% of skills at 1.0).
  → Improvement > 0.05 (LLM judge) or 0.001 (structural) → deploy
  ↓
Output: output/<name>/<timestamp>/evolved_skill.md + baseline_skill.md + metrics.json
```

**DSPy/GEPA deprecated (May 27):** The old stack (skill_module.py, GEPA.compile, reflection_lm, MIPROv2) had fundamental incompatibility with MiniMax — any `dspy.LM` call returns "invalid syntax". Replaced entirely with direct `urllib.request` API calls in `run_evolution_batch.py`. ~2 calls per skill vs hundreds.

## Critical Lessons Learned (May 27, 2026)

### 1. `failed` status does NOT auto-retry
`get_next_pending()` only returns `pending` and auto-retried `no_improvement`. `failed` skills are terminal — require manual intervention.

### 2. Manifest cleanup after bulk seeding
Running `generate_all_datasets_fast.py` seeds 238 `pending` entries with no `results`. `get_next_pending()` skips these correctly, but they clutter the manifest. Clean periodically with:
```python
# Keep only skills that have real results or errors
started = {k:v for k,v in manifest["skills"].items() if v.get("results") or v.get("error")}
manifest["skills"] = started
```

### 3. Skills use FLAT layout
Skills live at `~/.hermes/skills/<name>/SKILL.md` — NOT `~/.hermes/hermes-agent/skills/`. The `HERMES_AGENT_REPO` env var must point to `/home/Hermes/.hermes`.

### 4. API key has `'` in it (Python string hazard)
The `MINIMAX_API_KEY` value in `~/.hermes/.env` contains `'` (apostrophe). This breaks Python single-quoted string literals. Parse line-by-line: `if line.startswith('MINIMAX_API_KEY=') and not line.lstrip().startswith('#')`.

### 5. MiniMax outputs thinking-descriptions instead of improved content (CRITICAL — May 27 update)

**This was the #1 active problem.** MiniMax with "improve this skill" interprets the task as "describe what to improve" — it outputs `<think>...</think>` blocks and planning commentary instead of actual improved skill content. The output passes validation (starts with `---`, has `name:`, `description:`) but contains 30-40 lines of model reasoning before the real content, causing regression.

**Root cause of the fix (May 27):** The user_prompt was asking MiniMax to "improve" with requirements listed — this framing causes the model to ANALYZE and DESCRIBE improvements rather than WRITE the improved version. The model sees "improve" as a writing-about-the-skill task, not a write-the-improved-skill task.

**Fix applied — SYSTEM_PROMPT approach (confirmed working May 27):**
```
SYSTEM_PROMPT = "You are a skilled technical writer. Rewrite the given SKILL.md file.
RULES:
- Output ONLY the rewritten skill — no explanations, no preambles, no thinking blocks
- Start immediately with --- (YAML frontmatter)
- Do not include any markers like [@think] or [THOUGHT]"
```
Then only `user_prompt = truncated_skill_text` — no "improve" framing, no requirements list. The model just rewrites what's given.

**Also:** `max_tokens` increased from 4096 to 8192 (skill content can exceed 4096). `temperature=0.5` (was 0.7).

**Verification:** `huggingface-hub` evolved skill at `output/huggingface-hub/20260527_121526/evolved_skill.md` — starts correctly with `---`, no thinking blocks, clean content 225+ lines. Structural score improved.

**If thinking blocks still appear:** Check if `<think>` blocks are in the raw API response. If yes, the SYSTEM_PROMPT isn't being respected — try `MiniMax-Text-01` model instead of `MiniMax-M2.7` for the rewrite task.

### 6. Structural score penalizes genuinely improved skills
The `structural_score()` function rewards markers (`#`, `-`, `Step`), code fences, and examples. A more concise, well-written skill that removes cruft may score lower. **As of June 2 this is replaced by `llm_judge.py` (4-dim LLM-as-judge).** Use `--use-judge` to enable. The judge rewards conciseness directly so this trade-off is gone.

### 7. `in_progress` skills get stuck
After a failed run, `status` is left at `in_progress`. `get_next_pending()` skips `in_progress`. Clean with: manually set to `pending` or `failed` in manifest.

### 8. Lock file orphaned runs
A stale `evolution.lock` with a dead PID causes the batch to exit immediately with "Lock already held". `acquire_lock()` clears stale locks automatically, but check for lock files if batch says "No pending skills" incorrectly.

### 9. Cron trigger false positive (critical — May 27, 2026)
The cron checks `if ANY skill has status=failed OR status=in_progress`. If TRUE → pauses with "GEPA paused — previous run had failures." This is the CORRECT logic.

Failure mode: after running `generate_all_datasets_fast.py`, the manifest has 242 `pending` skills + 2 `evolved`. If cron uses `if ANY status != ok` (old buggy logic), it fires on every run because `pending` != `ok`. Result: cron repeatedly sends "GEPA paused" even though no actual failures occurred.

**Current cron prompt (correct):**
```
FIRST: Check evolution_manifest.json. If ANY skill has status=failed OR status=in_progress, reply with "GEPA paused — previous run had failures." and do nothing else.
```

**After manifest cleanup:** Always test the pipeline manually for 1-2 skills before re-enabling cron. Run: `HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --limit 2`

### 10. Cron management workflow
When GEPA has failures and you clean the manifest:
1. Pause cron (`cronjob --action pause`) BEFORE cleaning
2. Clean manifest: reset `failed`/`in_progress` to `pending`
3. Test: run pipeline on 1-2 skills manually
4. Resume cron only after confirmed clean run

### 11. Structural metric is saturated (CRITICAL — June 2, 2026)

**The old `structural_score()` heuristic was useless.** It awarded points for presence of frontmatter, code blocks, headings, length 200-5000, etc. A complete well-formed skill hit 0.5+0.15+0.1+0.1+0.1+0.05+0.05+0.05 = 1.10 → clamped to 1.00. **73% of skills scored 1.0.** When the evolved version came back, it also scored 1.00, delta = 0.000, marked as `no_improvement`. The loop was measuring a pass/fail check, not a quality gradient.

**Replaced with LLM-as-judge (`llm_judge.py`):** 4-dim rubric — structure (20%) + specificity (30%) + completeness (30%) + conciseness (20%). Each scored 0-1 by MiniMax-M2.7. Composite = weighted average.

**Backtest results (51 on-disk skills):**
- min=0.175, median=0.698, max=0.865, mean=0.671
- Distribution: 1 @ 0.2, 1 @ 0.3, 1 @ 0.4, 7 @ 0.5, 8 @ 0.6, 15 @ 0.7, 15 @ 0.8, 3 @ 0.9
- Worst: `ci-cd-pipeline` (0.175) — "Malformed frontmatter, duplicates, and marketing fluff"
- Best: `security-auditor` (0.865) — high across all dimensions
- The judge gives per-skill feedback notes that often identify real issues (duplicate frontmatter, marketing padding, missing verification steps, etc.)

**Activation (default OFF for backward compat):**
```bash
# One-shot test
.venv/bin/python run_evolution_batch.py --use-judge --skill coderag

# Backtest (no skill files touched)
.venv/bin/python run_evolution_batch.py --backtest

# Enable permanently for cron — set env in cron's shell or pass via prompt
# Cron job 073cd4c595a4 still uses old metric. To switch, update the cron prompt
# to use `python run_evolution_batch.py --mode one --use-judge` OR set GEPA_USE_JUDGE=1
```

**Threshold change:** New IMPROVEMENT_THRESHOLD = 0.05 (was 0.001). The LLM judge has observed stdev ~0.03 (range ~0.05) per skill, so 0.05 is the smallest threshold reliably above noise. Lower would deploy on judge stochasticity, not real improvement.

**Cost:** 1 judge call per attempt (baseline cached per round in `manifest.judge_cache`). For 53 processable skills × 3h cron = ~$0.50/round (down from theoretical $2/round with double-judging).

**Noise note:** Even at temperature 0.1, the same skill scored 0.81-0.88 across 3 runs (stdev 0.03). The 0.05 threshold absorbs this. Do not lower it without re-running a noise study.

## How to Run

### Single skill (manual, old metric):
```bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --skill <name>
```

### Single skill (manual, LLM judge):
```bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --use-judge --skill <name>
```

### Backtest (no skill files touched):
```bash
cd /home/Hermes/repos/gepa
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --backtest
# Writes backtest_scores.json with full distribution + per-skill results
```

### Full batch (old metric):
```bash
HERMES_AGENT_REPO=/home/Hermes/.hermes .venv/bin/python run_evolution_batch.py --all
```

### Generate datasets (zero LLM):
```bash
cd /home/Hermes/repos/gepa
.venv/bin/python generate_all_datasets_fast.py   # 227 skills, ~3 minutes
```

### Cron job (active — June 1, 2026)
- Job ID: `073cd4c595a4`
- Schedule: `0 */3 * * *` (every 3 hours) — was 4h, reduced June 1
- Status: **ACTIVE** (resumed June 1 after 5-day pause since May 27 16:17)
- Uses `run_evolution_batch.py --mode one` — NOT `--all` (which would 429)
- Round-robin via manifest v2.0: processes 1 skill per tick, advances `next_index`, auto-rolls to next round
- For 53 processable skills × 3h cron = ~6.6 days per round, then cycle again
- Pause/resume: `hermes cron pause 073cd4c595a4` / `hermes cron resume 073cd4c595a4`

## Dataset Generation

Old approach (`generate_all_datasets_all.py`): LLM call per skill → rate limited, slow, costly.
New approach (`generate_all_datasets_fast.py`): Heuristic template matching → zero LLM calls, 227 skills in 3 minutes.

Templates by category: coding, research, ops, messaging, data, file. Each skill gets 10 examples (7 train / 2 val / 1 holdout). Category inferred from skill keywords.

## Pipeline Status

| Component | Status | Notes |
|---|---|---|
| **Direct API pipeline** (`run_evolution_batch.py`) | ✅ Active | Direct MiniMax calls, ~2 per skill (1 rewrite + 1 judge) |
| **LLM judge metric** (`llm_judge.py`) | ✅ Active | 4-dim judge (--use-judge flag). Default OFF, opt-in per-run |
| **Structural metric** (`structural_score`) | ⚠️ Legacy | Saturated at 1.0 for 73% of skills. Kept as fallback. |
| **DSPy/GEPA stack** | ❌ Deprecated | Broken with MiniMax — any dspy.LM call returns syntax error |
| **Dataset generation** (`generate_all_datasets_fast.py`) | ✅ Active | Zero LLM calls, 244 skills done |
| **Cron job** (`073cd4c595a4`) | ✅ Active | Every 3h, checks manifest before running. Still uses old metric — set GEPA_USE_JUDGE=1 to upgrade |
| **GEPA optimizer** | ❌ Not used | Replaced by direct API approach |
| **MIPROv2** | ❌ Not used | Broken with MiniMax API format |

## Known Issues and Fixes

| Problem | Fix |
|---|---|
| GEPA returns baseline unchanged | Set `reflection_lm` parameter — without it, no reflection loop runs |
| "Skill not found" | Set `HERMES_AGENT_REPO=/home/Hermes/.hermes` — flat skills layout detection |
| API key `"#"` breaks Python parsing | Use shell `grep | cut` to extract key, or line-by-line `.env` reader |
| `failed` skills infinite loop | `get_next_pending()` only requeues `pending` and `no_improvement` |
| Dataset generation rate-limited | `generate_all_datasets_fast.py` — zero LLM calls |
| **Batch mode 429s MiniMax (242 skills in 16 min, all rate-limited)** | Switched to `--mode one` (1 skill per tick). Added 429 retry with 30s/60s/120s backoff in `generate_evolved_skill()`. |
| **Cron empties queue after one pass (no continuous improvement)** | Manifest v2.0 round-robin: each round resets ALL processable skills to `pending` (including `evolved`) so the loop never empties. 53 skills × 3h = 6.6 days/round. |
| **Cron paused silently, no surface signal** | Resumed June 1 2026. New cron prompt documents pause/resume commands. |

## Output

Each evolution run produces:
- `output/<skill>/<timestamp>/evolved_skill.md` — the evolved skill text
- `output/<skill>/<timestamp>/baseline_skill.md` — original for comparison
- `output/<skill>/<timestamp>/metrics.json` — scores, iterations, timing

If evolved score > baseline score → skill is deployed to `~/.hermes/skills/<skill>/SKILL.md`

## Cost
~$0.02-0.05 per skill evolution with MiniMax at current volumes. 227 datasets = $0 (heuristic generation). Batch processes one skill at a time.

## Related Skills
- `brain-index` — trained small model predicts activations for larger model (sibling self-improvement project)
- `gepa-self-evolution-runner` — the cron orchestrator skill
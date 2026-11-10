#!/usr/bin/env python3
"""Direct Skill Evolution -- MiniMax API, no DSPy.

Round-robin evolution loop:
  - Each invocation processes ONE skill (default for cron at 3h)
  - Tracks position in `manifest.next_index` so successive invocations
    walk through all skills in stable sorted order
  - When all skills in a round are done, `manifest.round` increments
    and `next_index` resets to 0 -- skills that hit `no_improvement`
    in the last round get a fresh batch of attempts
  - `--all` mode processes all remaining in one shot (manual one-off)
"""
import json
import os
import sys
import argparse
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# Local LLM judge (4-dim LLM-as-judge with real headroom)
try:
    from llm_judge import judge_skill  # type: ignore
    from llm_judge import composite_score as _judge_composite  # type: ignore
    LLM_JUDGE_AVAILABLE = True
except ImportError:
    def judge_skill(*_a, **_k):  # type: ignore  # noqa: F811
        return None
    def _judge_composite(*_a, **_k):  # type: ignore  # noqa: F811
        return 0.0
    LLM_JUDGE_AVAILABLE = False

# Load MINIMAX_API_KEY from .env using Python directly
hermes_env = Path.home() / ".hermes" / ".env"
if hermes_env.exists():
    with open(hermes_env) as f:
        for line in f:
            if line.startswith("MINIMAX_API_KEY=") and not line.lstrip().startswith("#"):
                key = line.strip().split("=", 1)[1]
                os.environ["MINIMAX_API_KEY"] = key
                break

MANIFEST_PATH = Path(__file__).parent / "evolution_manifest.json"
LOG_PATH = Path(__file__).parent / "evolution_batch.log"
LOCK_PATH = Path(__file__).parent / "evolution.lock"
SKILLS_BASE = Path.home() / ".hermes" / "skills"
DATASET_BASE = Path(__file__).parent / "datasets" / "skills"

# Cadence: cron at 3h, 1 skill per tick. ~2 API calls per skill = ~0.7 RPM
# average, well under the 20 RPM limit. No inter-skill delay needed.
API_CALL_DELAY_SEC = 0.0
MAX_RETRIES_PER_SKILL = 3
# In-skill 429 backoff: shorter than before because cron will retry next tick.
# Total worst case: 10+20+40 = 70s, which fits in a single cron tick.
MAX_429_RETRIES = 3
IN_SKILL_429_BACKOFF_SECS = (10, 20, 40)

# Threshold for "improved" -- must be > this to be deployed.
# The LLM judge has observed stdev ~0.03 (range ~0.05), so 0.05 is the
# smallest threshold that's reliably above noise. Lower would deploy
# on judge stochasticity, not real improvement.
IMPROVEMENT_THRESHOLD = 0.05
# When USE_JUDGE=1, the LLM judge (4-dim) is the metric of record.
# Default OFF so old batch runs and the cron don't change behavior until
# the new metric is validated. Set via env var or --use-judge CLI flag.
USE_JUDGE = os.environ.get("GEPA_USE_JUDGE", "0") == "1"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def load_manifest():
    if not MANIFEST_PATH.exists():
        return {
            "version": "2.0",
            "round": 1,
            "next_index": 0,
            "order": [],  # stable sorted list of skill names to walk
            "skills": {},
            "lock": None,
            "judge_cache": {},  # skill_name -> {composite, dimensions, saved_at}
        }
    with open(MANIFEST_PATH) as f:
        m = json.load(f)
    # Migrate old manifest shapes (no `order` / `next_index` / `round`)
    m.setdefault("version", "2.0")
    m.setdefault("round", 1)
    m.setdefault("next_index", 0)
    m.setdefault("skills", {})
    m.setdefault("judge_cache", {})  # LLM judge baseline cache (per-round)
    return m


def save_manifest(m):
    tmp = MANIFEST_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(m, f, indent=2)
    tmp.replace(MANIFEST_PATH)


def acquire_lock():
    if LOCK_PATH.exists():
        try:
            pid = int(LOCK_PATH.read_text().strip())
            os.kill(pid, 0)
            return False
        except (OSError, ValueError):
            pass
    LOCK_PATH.write_text(str(os.getpid()))
    return True


def release_lock():
    if LOCK_PATH.exists():
        try:
            LOCK_PATH.unlink()
        except FileNotFoundError:
            pass


def discover_skill_names():
    """Return sorted list of skill directory names that have a SKILL.md."""
    names = set()
    for d in SKILLS_BASE.iterdir():
        if not d.is_dir():
            continue
        if (d / "SKILL.md").exists():
            names.add(d.name)
    return sorted(names)


def sync_manifest_with_disk(m):
    """Make sure the manifest's `order` and `skills` reflect on-disk reality.
    - New skills (on disk but not tracked) -> added as `pending`
    - Tracked skills with no on-disk SKILL.md -> marked `missing` (skipped)
    - Recompute `order` if the set of skills has changed materially.
    """
    on_disk = discover_skill_names()

    # Add new ones
    for name in on_disk:
        if name not in m["skills"]:
            m["skills"][name] = {
                "status": "pending",
                "iterations": 1,
                "results": None,
                "error": None,
                "last_round": 0,
            }

    # Mark missing
    for name in list(m["skills"].keys()):
        if name not in on_disk:
            if m["skills"][name].get("status") != "missing":
                m["skills"][name]["status"] = "missing"

    # Rebuild the walk order if it doesn't match the tracked set
    tracked = sorted(n for n, info in m["skills"].items() if info.get("status") != "missing")
    if m.get("order") != tracked:
        # If current next_index is past the new list, wrap to 0
        if m.get("next_index", 0) >= len(tracked):
            m["next_index"] = 0
        m["order"] = tracked
    return m


def pick_next_skill(m):
    """Return (skill_name, info) for the next skill to evolve this round.
    - Walks `order` starting at `next_index`
    - Skips skills with status `missing` or `in_progress`
    - Resets no_improvement skills' iterations when starting a new round
    - Returns None when the round is complete
    """
    order = m.get("order", [])
    if not order:
        return None

    cur_round = m.get("round", 1)
    n = len(order)
    idx = m.get("next_index", 0)

    # Walk forward, looking for a processable skill
    for step in range(n):
        i = (idx + step) % n
        name = order[i]
        info = m["skills"].get(name, {})

        status = info.get("status")
        if status == "missing":
            continue
        if status == "in_progress":
            continue  # don't double-evolve

        # Skip skills already attempted (and failed) this round.
        # This includes both `no_improvement` (scored equal/worse) and
        # rate-limited skills (soft fail, will retry next round).
        if info.get("last_round", 0) >= cur_round and status in (
            "no_improvement", "evolved"
        ):
            continue
        if info.get("last_round", 0) >= cur_round and status == "pending" and info.get("last_error_type") == "rate_limit":
            # Already rate-limited this round -- wait for next round
            continue

        # If this skill finished the last round without improvement,
        # give it a fresh batch of attempts in the new round
        if status == "no_improvement" and info.get("last_round", 0) < cur_round:
            info["status"] = "pending"
            info["iterations"] = 1
            info["last_round"] = cur_round
            info["results"] = None
            info["error"] = None

        if status == "evolved":
            # Already improved in an earlier round -- skip this round
            continue
        if status == "failed":
            # Skip permanently-failed skills this round; revisit next round
            if info.get("last_round", 0) < cur_round:
                info["status"] = "pending"
                info["iterations"] = 1
                info["last_round"] = cur_round
                info["error"] = None
            else:
                continue
        if status == "no_improvement":
            # Tried 3x in current round, skip
            continue

        # Found one -- advance next_index to the slot after this one
        m["next_index"] = (i + 1) % n
        return name, info

    # Walked the whole order without finding anything processable
    return None


def advance_round(m):
    """Move to the next round: bump `round`, reset `next_index`.
    Reset ALL processable skills to pending so each round re-evaluates
    every skill. This is the key to continuous improvement: even skills
    that previously `evolved` get another shot at further improvement.
    Also clears the judge_cache -- baselines need to be re-judged each round
    because the on-disk skill may have changed since the last round.
    """
    m["round"] = m.get("round", 1) + 1
    m["next_index"] = 0
    m["judge_cache"] = {}  # clear -- baselines are per-round
    for name, info in m["skills"].items():
        if info.get("status") == "missing":
            continue  # still missing on disk, skip
        info["status"] = "pending"
        info["iterations"] = 1
        info["results"] = None
        info["error"] = None
    return m


def direct_api_call(messages, api_key, model="MiniMax-M2.7"):
    url = "https://api.minimax.io/v1/chat/completions"
    data = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 8192,
    }).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


SYSTEM_PROMPT = """You are a skilled technical writer. Rewrite the given SKILL.md file.

RULES:
- Output ONLY the rewritten skill — no explanations, no preambles, no thinking blocks
- Start immediately with --- (YAML frontmatter)
- Use markdown syntax naturally (headers, code fences, bullets) — do not avoid them
- Keep the skill's name, description, and purpose intact
- If content is already good, leave it unchanged
- Return the complete rewritten skill in your response"""


def generate_evolved_skill(skill_text, skill_name, api_key):
    truncated = skill_text[:2500]
    user_prompt = (
        "Rewrite this SKILL.md file. Keep the name and description. Improve clarity,"
        " specificity, and usefulness. Return the complete rewritten version.\n\n"
        "START OF CURRENT SKILL:\n" + truncated + "\nEND OF CURRENT SKILL\n\n"
        "Rewrite it now."
    )
    last_error = None
    rate_limited = False
    for attempt in range(MAX_429_RETRIES):
        response = direct_api_call(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            api_key,
        )
        if "error" in response:
            last_error = response["error"]
            if "429" in last_error or "rate_limit" in last_error.lower():
                # In-skill backoff (10/20/40s). If we exhaust retries,
                # return a rate_limit marker so the caller can leave
                # the skill as `pending` instead of `failed` -- cron
                # will retry it on the next tick.
                wait = IN_SKILL_429_BACKOFF_SECS[min(attempt, len(IN_SKILL_429_BACKOFF_SECS)-1)]
                log(f"  Rate limited (429). Backing off {wait}s before retry {attempt+1}/{MAX_429_RETRIES}...")
                time.sleep(wait)
                continue
            return None, last_error, False
        # Success path
        content = response["choices"][0]["message"]["content"]
        log(f"  Raw output ({len(content)} chars): {content[:300]}")
        # Strip thinking blocks
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        content = re.sub(r"^```\s*", "", content, flags=re.M)
        content = re.sub(r"\s*```\s*$", "", content)
        content = content.strip()
        # Find first --- and extract from there
        dash_idx = content.find("---")
        if dash_idx > 0:
            content = content[dash_idx:]
        return content, None, False

    # Exhausted 429 retries -- this is a soft fail, not a hard fail.
    # Cron will retry on the next tick; in the meantime the skill stays
    # `pending` and gets skipped by pick_next_skill until next round.
    return None, f"Rate limited after {MAX_429_RETRIES} retries: {last_error}", True


def structural_score(skill_text):
    if not skill_text.strip():
        return 0.0
    score = 0.5
    has_steps = bool(re.search(r"^#{1,2}\s+\w|\n\s*[-*]\s+\w|\bStep\s+\d+", skill_text, re.M))
    has_code = "```" in skill_text or "    " in skill_text
    has_examples = "example" in skill_text.lower()
    if has_steps:
        score += 0.15
    if has_code:
        score += 0.1
    if has_examples:
        score += 0.1
    if 200 < len(skill_text) < 5000:
        score += 0.1
    if len(skill_text) < 200:
        score -= 0.2
    if skill_text.strip().startswith("---"):
        score += 0.05
    if "name:" in skill_text[:200]:
        score += 0.05
    if "description:" in skill_text[:200]:
        score += 0.05
    return min(1.0, max(0.0, score))


def _run_backtest(api_key, output_path=None):
    """Judge all on-disk skills once and write a distribution report.

    Does NOT write to skill files. Does NOT touch the manifest. Use this to
    validate the metric before enabling --use-judge on the real evolution loop.

    Output: backtest_scores.json with per-skill scores + distribution stats.
    """
    from collections import Counter
    skills_on_disk = discover_skill_names()
    print(f"Backtest: judging {len(skills_on_disk)} on-disk skills...")
    print(f"Model: MiniMax-M2.7 (same as the rewriter)")
    print()

    results = {}
    failures = []
    for i, name in enumerate(skills_on_disk, 1):
        p = find_skill_path(name)
        if not p:
            failures.append({"name": name, "error": "path not found"})
            continue
        text = p.read_text()
        # Skip trivially tiny skills
        if len(text) < 100:
            failures.append({"name": name, "error": f"too short ({len(text)} chars)"})
            continue
        result = judge_skill(text, name, api_key=api_key)
        if result is None:
            failures.append({"name": name, "error": "judge returned None"})
        else:
            results[name] = result
        if i % 10 == 0:
            print(f"  [{i}/{len(skills_on_disk)}] judged")

    # Distribution analysis
    composites = [r["composite"] for r in results.values()]
    composites.sort()
    n = len(composites)
    dist = Counter(round(c, 1) for c in composites)
    dim_dist = {}
    for dim in ("structure", "specificity", "completeness", "conciseness"):
        vals = [r[dim] for r in results.values()]
        dim_dist[dim] = {
            "min": round(min(vals), 3) if vals else None,
            "max": round(max(vals), 3) if vals else None,
            "mean": round(sum(vals) / len(vals), 3) if vals else None,
            "median": round(vals[len(vals) // 2], 3) if vals else None,
        }

    print()
    print("=" * 60)
    print(f"BACKTEST RESULTS ({n} scored, {len(failures)} failed)")
    print("=" * 60)
    if composites:
        print(f"Composite score distribution:")
        print(f"  min    : {composites[0]:.3f}")
        print(f"  median : {composites[n//2]:.3f}")
        print(f"  max    : {composites[-1]:.3f}")
        print(f"  mean   : {sum(composites)/n:.3f}")
        print()
        print("Histogram (composite, 0.1 buckets):")
        for k in sorted(dist.keys()):
            bar = "#" * min(60, dist[k] * 2)
            print(f"  {k:.1f}: {dist[k]:3d} {bar}")
        print()
        print("Per-dimension stats:")
        for dim, stats in dim_dist.items():
            print(f"  {dim:13s}: min={stats['min']:.2f}  median={stats['median']:.2f}  max={stats['max']:.2f}  mean={stats['mean']:.2f}")
    if failures:
        print()
        print(f"Failures ({len(failures)}):")
        for f in failures[:10]:
            print(f"  {f['name']}: {f['error']}")
        if len(failures) > 10:
            print(f"  ... and {len(failures) - 10} more")

    out_path = Path(output_path) if output_path else (Path(__file__).parent / "backtest_scores.json")
    out_path.write_text(json.dumps({
        "model": "MiniMax-M2.7",
        "rubric": "structure (20%) + specificity (30%) + completeness (30%) + conciseness (20%)",
        "n_scored": n,
        "n_failed": len(failures),
        "composite_distribution": {str(k): v for k, v in dist.items()},
        "dimension_stats": dim_dist,
        "results": results,
        "failures": failures,
    }, indent=2))
    print()
    print(f"Saved detailed results to {out_path}")
    return 0


def _score_pair(baseline_text, evolved_text, skill_name, api_key, baseline_cache=None):
    """Score a (baseline, evolved) pair. Returns dict with composite numbers
    and the per-dimension breakdown (when judge is enabled).

    baseline_cache: optional dict to use for cached baseline scores, keyed by
    skill_name. If provided and contains a 'baseline_judge' entry, that score
    is reused instead of re-judging the original (saves 1 API call per attempt).
    """
    if USE_JUDGE and LLM_JUDGE_AVAILABLE:
        baseline_score = None
        baseline_dims = None
        # Use cached baseline if available
        if baseline_cache and skill_name in baseline_cache:
            cached = baseline_cache[skill_name]
            if isinstance(cached, dict) and "composite" in cached:
                baseline_score = cached["composite"]
                baseline_dims = cached.get("dimensions")
        if baseline_score is None:
            baseline = judge_skill(baseline_text, skill_name, api_key=api_key)
            if baseline is None:
                log("  WARN: judge returned None on baseline, falling back to structural")
                return {
                    "baseline": round(structural_score(baseline_text), 3),
                    "evolved": round(structural_score(evolved_text), 3),
                    "metric": "structural_fallback",
                }
            baseline_score = baseline["composite"]
            baseline_dims = {k: baseline[k] for k in ("structure", "specificity", "completeness", "conciseness")}
        evolved = judge_skill(evolved_text, skill_name, api_key=api_key)
        if evolved is None:
            log("  WARN: judge returned None on evolved, falling back to structural")
            return {
                "baseline": round(baseline_score, 3),
                "evolved": round(structural_score(evolved_text), 3),
                "metric": "structural_fallback",
            }
        return {
            "baseline": round(baseline_score, 3),
            "evolved": round(evolved["composite"], 3),
            "baseline_dims": {k: round(baseline_dims[k], 3) for k in ("structure", "specificity", "completeness", "conciseness")} if baseline_dims else None,
            "evolved_dims": {k: round(evolved[k], 3) for k in ("structure", "specificity", "completeness", "conciseness")},
            "metric": "llm_judge_v1",
        }
    return {
        "baseline": round(structural_score(baseline_text), 3),
        "evolved": round(structural_score(evolved_text), 3),
        "metric": "structural_v0",
    }


def validate_skill(skill_text):
    errors = []
    if not skill_text.strip().startswith("---"):
        errors.append("Missing YAML frontmatter")
    if not re.search(r"^name:\s*\S", skill_text, re.M):
        errors.append("Missing or invalid name field")
    if not re.search(r"^description:\s*\S", skill_text, re.M):
        errors.append("Missing or invalid description field")
    if len(skill_text) < 200:
        errors.append("Skill text too short")
    if len(skill_text) > 25000:
        errors.append("Skill text exceeds 25KB limit")
    return len(errors) == 0, errors


def find_skill_path(skill_name):
    # Explicit check first — rglob silently skips certain dirs (symlinks, permission edges)
    explicit = SKILLS_BASE / skill_name / "SKILL.md"
    if explicit.exists():
        return explicit
    for md in SKILLS_BASE.rglob("SKILL.md"):
        if md.parent.name == skill_name:
            return md
    return None


def run_evolution(skill_name, api_key, baseline_cache=None, save_cache_callback=None):
    skill_path = find_skill_path(skill_name)
    if not skill_path:
        return False, None, f"Skill not found for: {skill_name}", False

    original = skill_path.read_text()
    log(f"Generating improved version of '{skill_name}'...")
    evolved_text, error, rate_limited = generate_evolved_skill(original, skill_name, api_key)
    if error:
        return False, None, f"API error: {error}", rate_limited

    passes, errors = validate_skill(evolved_text)
    if not passes:
        return False, None, f"Invalid evolved skill: {', '.join(errors)}", False

    scored = _score_pair(original, evolved_text, skill_name, api_key, baseline_cache=baseline_cache)
    baseline_score = scored["baseline"]
    evolved_score = scored["evolved"]
    improvement = evolved_score - baseline_score

    # If the metric is the LLM judge and we don't have a cached baseline,
    # save the freshly-judged baseline for next time (per-round cache).
    if scored.get("metric") == "llm_judge_v1" and save_cache_callback:
        if baseline_cache is None or skill_name not in baseline_cache:
            save_cache_callback(skill_name, {
                "composite": baseline_score,
                "dimensions": scored.get("baseline_dims"),
                "saved_at": datetime.now().isoformat(),
            })

    output_dir = (
        Path(__file__).parent
        / "output"
        / skill_name
        / datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evolved_skill.md").write_text(evolved_text)
    (output_dir / "baseline_skill.md").write_text(original)
    metrics = {
        "skill_name": skill_name,
        "baseline_score": round(baseline_score, 3),
        "evolved_score": round(evolved_score, 3),
        "improvement": round(improvement, 3),
        "metric": scored.get("metric"),
    }
    if "baseline_dims" in scored:
        metrics["baseline_dims"] = scored["baseline_dims"]
    if "evolved_dims" in scored:
        metrics["evolved_dims"] = scored["evolved_dims"]
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    if improvement > IMPROVEMENT_THRESHOLD:
        skill_path.write_text(evolved_text)
        log(f"Deployed improved version to {skill_path}")

    return True, improvement, {
        "baseline": round(baseline_score, 3),
        "evolved": round(evolved_score, 3),
        "metric": scored.get("metric"),
    }, False


def process_one_skill(api_key, m):
    """Process exactly one skill. Returns the skill name (or None if no
    candidates -- which means a round just finished).

    Outcomes:
      - evolved: score improved, deployed
      - no_improvement: scored equal/worse, NOT deployed, skip rest of round
      - failed: hard error (validation, network, etc.) -- terminal until reset
      - rate_limited: soft fail, skill stays `pending`, skipped this round,
                      retried at start of next round
    """
    picked = pick_next_skill(m)
    if not picked:
        return None
    name, info = picked
    attempt = info.get("iterations", 1)
    log(f"Round {m['round']} -- evolving: {name} (attempt {attempt}/{MAX_RETRIES_PER_SKILL})")

    info["status"] = "in_progress"
    save_manifest(m)

    # Set up baseline cache for the judge (saves 1 API call per attempt)
    baseline_cache = m.get("judge_cache", {})
    def _save_cache(skill_name, entry):
        if "judge_cache" not in m:
            m["judge_cache"] = {}
        m["judge_cache"][skill_name] = entry
        save_manifest(m)

    success, improvement, details, rate_limited = run_evolution(
        name, api_key, baseline_cache=baseline_cache, save_cache_callback=_save_cache,
    )

    if success:
        delta = improvement if improvement else 0
        if isinstance(details, dict):
            log(f"  Score: {details['baseline']} -> {details['evolved']} ({delta:+.3f})")
        if delta > IMPROVEMENT_THRESHOLD:
            info["status"] = "evolved"
            log("  Result: IMPROVED")
        elif abs(delta) < IMPROVEMENT_THRESHOLD:
            info["status"] = "no_improvement"
            info["last_round"] = m["round"]
            log("  Result: NO CHANGE")
        else:
            info["status"] = "no_improvement"
            info["last_round"] = m["round"]
            log("  Result: REGRESSED")
        info["results"] = details if isinstance(details, dict) else None
        info["error"] = None
    elif rate_limited:
        # Soft fail: leave as `pending` but mark `last_round` so
        # pick_next_skill skips it for the rest of this round.
        # advance_round() will reset it on the next round.
        info["status"] = "pending"
        info["last_round"] = m["round"]
        info["error"] = str(details)[:500]
        info["last_error_type"] = "rate_limit"
        log(f"  Result: RATE LIMITED (soft fail) -- will retry next round")
    else:
        info["status"] = "failed"
        info["error"] = str(details)[:500]
        info["results"] = None
        info["last_error_type"] = "hard_fail"
        log(f"  Result: FAILED -- {str(details)[:200]}")

    save_manifest(m)
    return name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["one", "all"],
        default="one",
        help="`one` (default) processes 1 skill and exits. `all` runs through the full round.",
    )
    parser.add_argument("--skill", type=str, default=None, help="Override: evolve a specific skill")
    parser.add_argument("--reset-round", action="store_true", help="Reset round + next_index to 1, 0")
    parser.add_argument("--status", action="store_true", help="Print current round/index/queue state and exit")
    parser.add_argument(
        "--use-judge",
        action="store_true",
        help="Use the 4-dim LLM judge as the metric instead of the saturated structural heuristic. "
             "Also enables via env GEPA_USE_JUDGE=1. Adds 2 API calls per skill (baseline + evolved).",
    )
    parser.add_argument(
        "--backtest",
        action="store_true",
        help="Judge all on-disk skills once and save distribution to backtest_scores.json. "
             "Does not write to skill files. Use to validate the metric before enabling --use-judge.",
    )
    args = parser.parse_args()

    # Late-bind the judge flag so CLI override works.
    global USE_JUDGE
    if args.use_judge:
        USE_JUDGE = True

    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key and not args.status:
        log("ERROR: MINIMAX_API_KEY not set")
        return 1

    m = load_manifest()
    m = sync_manifest_with_disk(m)
    # Persist the synced manifest so round/order/next_index are saved
    save_manifest(m)

    if args.status:
        order = m.get("order", [])
        from collections import Counter
        statuses = Counter(info.get("status", "?") for info in m["skills"].values())
        print(f"Manifest v{m.get('version')} -- round {m.get('round')}, next_index {m.get('next_index')}/{len(order)}")
        print(f"Tracked skills: {len(m['skills'])} | Order (processable): {len(order)}")
        for s, c in statuses.most_common():
            print(f"  {s}: {c}")
        if order and m.get("next_index", 0) < len(order):
            upcoming = order[m["next_index"]:m["next_index"]+5]
            print(f"\nNext 5 to evolve: {upcoming}")
        return 0

    if args.backtest:
        if not LLM_JUDGE_AVAILABLE:
            print("ERROR: llm_judge module not importable")
            return 1
        if not api_key:
            print("ERROR: MINIMAX_API_KEY not set")
            return 1
        return _run_backtest(api_key)

    if args.reset_round:
        m["round"] = 1
        m["next_index"] = 0
        save_manifest(m)
        log("Reset: round=1, next_index=0")
        return 0

    if args.skill:
        # One-shot: evolve the named skill once
        if not acquire_lock():
            log("Lock held, exiting")
            return 1
        try:
            log("=== Direct Skill Evolution (single-skill mode) ===")
            info = m["skills"].setdefault(args.skill, {
                "status": "pending", "iterations": 1, "results": None, "error": None, "last_round": 0,
            })
            info["status"] = "in_progress"
            save_manifest(m)
            # Set up baseline cache for the judge
            baseline_cache = m.get("judge_cache", {})
            def _save_cache(skill_name, entry):
                if "judge_cache" not in m:
                    m["judge_cache"] = {}
                m["judge_cache"][skill_name] = entry
                save_manifest(m)
            success, improvement, details, rate_limited = run_evolution(
                args.skill, api_key, baseline_cache=baseline_cache, save_cache_callback=_save_cache,
            )
            if success:
                delta = improvement if improvement else 0
                log(f"  Score: {details['baseline']} -> {details['evolved']} ({delta:+.3f})")
                if delta > IMPROVEMENT_THRESHOLD:
                    info["status"] = "evolved"
                else:
                    info["status"] = "no_improvement"
                info["results"] = details
                info["error"] = None
            elif rate_limited:
                info["status"] = "pending"
                info["last_error_type"] = "rate_limit"
                info["error"] = str(details)[:500]
                log("  RATE LIMITED (soft fail)")
            else:
                info["status"] = "failed"
                info["error"] = str(details)[:500]
                info["last_error_type"] = "hard_fail"
                log(f"  FAILED: {details}")
            save_manifest(m)
        finally:
            release_lock()
        return 0

    if not acquire_lock():
        log("Lock held, exiting")
        return 1

    try:
        log("=== Direct Skill Evolution Started ===")
        if args.mode == "one":
            n_before = m.get("next_index", 0)
            name = process_one_skill(api_key, m)
            if name is None:
                # Round finished -- advance and try one more from new round
                log("Round complete -- advancing to next round")
                m = advance_round(m)
                save_manifest(m)
                log(f"Now on round {m['round']} (next_index {m['next_index']})")
                name = process_one_skill(api_key, m)
            n_after = m.get("next_index", 0)
            order_len = len(m.get("order", []))
            log(
                f"Processed: {name} | index {n_before}->{n_after}/{order_len} | "
                f"round {m.get('round')}"
            )
        else:  # args.mode == "all"
            processed = 0
            while True:
                name = process_one_skill(api_key, m)
                if name is None:
                    log("Round complete -- advancing to next round")
                    m = advance_round(m)
                    save_manifest(m)
                    log(f"Now on round {m['round']} (next_index {m['next_index']})")
                    # If still nothing processable, we are fully done
                    name = process_one_skill(api_key, m)
                    if name is None:
                        log("No more processable skills in this round. Stopping.")
                        break
                processed += 1
                # Safety: cap `all` to one round worth + a buffer
                if processed >= len(m.get("order", [])) * MAX_RETRIES_PER_SKILL:
                    log("Safety cap reached; stopping `all` run.")
                    break
                time.sleep(API_CALL_DELAY_SEC)
            log(f"=== Done -- processed {processed} skills ===")
    finally:
        release_lock()
    return 0


if __name__ == "__main__":
    sys.exit(main())

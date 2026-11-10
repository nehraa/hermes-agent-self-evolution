"""LLM-as-judge skill quality scorer.

Replaces the saturated structural_score() heuristic with a 4-dimensional
LLM judge that has real headroom (typical good skills score 0.55-0.85,
leaving room for evolution to push them up).

Rubric (each 0.0-1.0, composite is weighted average):
  - structure (20%):     frontmatter, name+description, valid markdown
  - specificity (30%):    concrete commands/paths/code, not vague prose
  - completeness (30%):   triggers, steps, pitfalls, verification, examples
  - conciseness (20%):    information density, no bloat/repetition

The judge runs in the same MiniMax-M2.7 model as the rewriter, using
direct API calls (no DSPy). Returns 4 floats parsed from a JSON object
in the response. On parse failure, scores default to 0.5 (neutral) and
the composite is still usable -- it just won't be a real measurement.
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

# Re-use the exact same API call plumbing as run_evolution_batch.py
# so a single .env reader / auth path covers both modules.
HERMES_ENV = Path.home() / ".hermes" / ".env"


def _load_api_key():
    existing = os.environ.get("MINIMAX_API_KEY")
    if existing:
        return existing
    if HERMES_ENV.exists():
        with open(HERMES_ENV) as f:
            for line in f:
                key_marker = "MINIMAX_API_KEY="
                if line.startswith(key_marker) and not line.lstrip().startswith("#"):
                    return line.strip().split("=", 1)[1]
    return ""


JUDGE_SYSTEM_PROMPT = """You are a strict technical writing reviewer for SKILL.md files
(loaded by AI agents to learn how to perform a task). You score skills on
four independent dimensions. Be discriminating: a real working skill
should score 0.55-0.85, not 0.99. Reserve 0.9+ for genuinely excellent
skills (concrete commands, no fluff, no missing sections)."""


JUDGE_USER_PROMPT = """Score this SKILL.md on 4 dimensions. Return ONLY a JSON object
(no prose, no markdown fences) with this exact shape:

{{"structure": <0-1>, "specificity": <0-1>, "completeness": <0-1>, "conciseness": <0-1>, "notes": "<one short sentence>"}}

DIMENSIONS:

1. STRUCTURE (0-1) — Is the file well-formed?
   - Has YAML frontmatter at the very top with `name:` and `description:` fields
   - Uses markdown headings (##, ###) to organize sections
   - Has a clear "When to use" / trigger section
   - Is parseable markdown (no broken syntax)
   Penalize: missing frontmatter, missing description, no headings, raw text dumps.

2. SPECIFICITY (0-1) — How concrete and actionable is it?
   - Real shell commands with real paths/flags (not "run the command")
   - Code blocks that would actually work if copy-pasted
   - Names of specific tools, files, env vars, package names
   - Anti-patterns / common mistakes called out
   Penalize: vague hand-waving ("configure as needed"), prose-only explanations,
   missing concrete examples, no commands or paths.

3. COMPLETENESS (0-1) — Does it cover what an agent needs to succeed?
   - Trigger conditions: when should this skill be loaded?
   - Numbered/bulleted steps the agent can follow in order
   - Pitfalls / gotchas / known failure modes
   - Verification step (how does the agent know it worked?)
   - Example invocation or expected output
   Penalize: any of these sections missing or implied rather than explicit.

4. CONCISENESS (0-1) — Information density, no bloat.
   - No repeated information across sections
   - No filler prose ("It's important to note that...", "In conclusion...")
   - Length proportional to complexity (a 200-line skill for a 1-step task is bloated;
     a 50-line skill for a complex workflow is probably too thin)
   - Tables/lists used where they beat prose
   Penalize: walls of text, padding, redundant examples, sections that just restate
   the description.

Calibration anchors:
- 0.3 = poor: missing multiple required sections, vague, probably unusable
- 0.5 = mediocre: has the right pieces but unclear or thin
- 0.7 = good: agent can follow it and succeed in most cases
- 0.85 = excellent: concrete, complete, no fluff
- 0.95 = exceptional: would ship as-is to a doc site

SKILL TO REVIEW (name: {skill_name}):
----- BEGIN SKILL -----
{skill_text}
----- END SKILL -----

Return JSON only."""


def _parse_judge_response(content):
    """Parse a judge response into a 4-tuple of scores. Tolerant of formatting noise.

    Strategy:
    1. Strip thinking blocks (the model often does <think>...analysis...</think> first)
    2. Try `json.loads` on the WHOLE stripped content (cleanest path)
    3. Try `json.loads` on the LAST brace block (in case there's prose after)
    4. Try a balanced-brace scan starting from the last '{' on its own line
    5. Give up -> None
    """
    if not content:
        return None
    # Strip thinking blocks
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    # Strip code fences if present
    content = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.M)
    content = re.sub(r"\s*```\s*$", "", content)
    content = content.strip()

    # Strategy 1: direct json.loads of the whole thing
    try:
        obj = json.loads(content)
        if isinstance(obj, dict):
            return _extract_dims(obj)
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 2: find the last { ... } JSON block (handles leading prose)
    # Use a balanced-brace scan
    last_idx = content.rfind("{")
    if last_idx >= 0:
        # Walk forward, counting brace depth
        depth = 0
        in_string = False
        escape = False
        for i in range(last_idx, len(content)):
            ch = content[i]
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = content[last_idx : i + 1]
                    try:
                        obj = json.loads(candidate)
                        if isinstance(obj, dict):
                            return _extract_dims(obj)
                    except (json.JSONDecodeError, ValueError):
                        break

    # Strategy 3: try simpler regex as fallback
    m = re.search(r"\{[^{}]*?\}", content, flags=re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return _extract_dims(obj)
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def _extract_dims(obj):
    """Pull the 4 dimension scores out of a parsed JSON dict, clamping each to 0-1."""
    out = {}
    for key in ("structure", "specificity", "completeness", "conciseness"):
        v = obj.get(key)
        if isinstance(v, (int, float)):
            out[key] = max(0.0, min(1.0, float(v)))
        else:
            try:
                out[key] = max(0.0, min(1.0, float(str(v).strip())))
            except (ValueError, TypeError):
                out[key] = 0.5  # neutral on parse failure
    out["notes"] = str(obj.get("notes", ""))[:500]
    return out


def _direct_api_call(messages, api_key, model="MiniMax-M2.7", max_retries=3, timeout=120):
    """Identical shape to run_evolution_batch.direct_api_call, kept here
    to avoid an import cycle and to localize retry logic for the judge."""
    url = "https://api.minimax.io/v1/chat/completions"
    data = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.1,  # very low temp for near-deterministic scoring
        "max_tokens": 1500,  # judge response with think blocks can be long
    }).encode()
    last_error = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url, data=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read())
                if "error" in body:
                    last_error = body["error"]
                else:
                    return body
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode()[:300]
            except Exception:
                pass
            last_error = f"HTTP {e.code}: {body}"
            if "429" in last_error or "rate_limit" in last_error.lower():
                wait = (10, 20, 40)[min(attempt, 2)]
                time.sleep(wait)
                continue
            return None
        except Exception as e:
            last_error = str(e)
            time.sleep(2)
    # Exhausted retries on 429 -> soft fail (None). On other errors -> error dict.
    if last_error and ("429" in last_error or "rate_limit" in last_error.lower()):
        return None
    return {"error": last_error} if last_error else None


WEIGHTS = {
    "structure": 0.20,
    "specificity": 0.30,
    "completeness": 0.30,
    "conciseness": 0.20,
}


def composite_score(dimensions):
    """Weighted average of 4 dimension scores. Returns 0-1 float."""
    if not dimensions:
        return 0.0
    return sum(dimensions[k] * WEIGHTS[k] for k in WEIGHTS)


def judge_skill(skill_text, skill_name, api_key=None, model="MiniMax-M2.7"):
    """Score a SKILL.md using the LLM judge.

    Returns dict with keys: structure, specificity, completeness, conciseness,
    composite, notes. Returns None on hard API failure (so caller can fall
    back to the structural heuristic).
    """
    if not skill_text or not skill_text.strip():
        return None
    api_key = api_key or _load_api_key()
    if not api_key:
        return None

    # Truncate very long skills to fit judge context + save tokens
    truncated = skill_text[:12000]
    if len(skill_text) > 12000:
        truncated += "\n\n[... truncated for judging ...]"

    user_prompt = JUDGE_USER_PROMPT.format(
        skill_name=skill_name,
        skill_text=truncated,
    )

    response = _direct_api_call(
        [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        api_key,
        model=model,
    )
    if not response or not isinstance(response, dict):
        return None
    if "error" in response:
        return None
    choices = response.get("choices")
    if not choices or not isinstance(choices, list) or not choices:
        return None
    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        return None
    message = first_choice.get("message", {})
    if not isinstance(message, dict):
        return None
    content = message.get("content", "")
    parsed = _parse_judge_response(content)
    if not parsed:
        return None

    parsed["composite"] = round(composite_score(parsed), 4)
    return parsed


def judge_skills_batch(skill_texts, api_key=None, model="MiniMax-M2.7", progress_every=10):
    """Judge many skills sequentially. Yields (name, result_or_none)."""
    api_key = api_key or _load_api_key()
    if not api_key:
        for name in skill_texts:
            yield name, None
        return
    for i, (name, text) in enumerate(skill_texts.items(), 1):
        result = judge_skill(text, name, api_key=api_key, model=model)
        if progress_every and i % progress_every == 0:
            print(f"  [{i}/{len(skill_texts)}] judged so far...")
        yield name, result

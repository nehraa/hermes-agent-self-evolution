---
name: codebase-to-course-render
description: Render any codebase into an interactive HTML course.
triggers:
  - "render this as a course"
  - "make a course from this repo"
  - "codebase walkthrough"
  - "interactive tutorial from code"
  - "codebase-to-course"
  - "turn this codebase into a course"
category: software-development
tags: [documentation, course-generation, codebase-to-course, teaching, onbording, walkthrough]
version: 1.0.0
---

# Codebase-to-Course Renderer

Turn any codebase (or curated file subset) into an interactive HTML course
that explains how it works to non-technical readers. Self-contained — open
`index.html` in any browser, no server required (only external dep: Google Fonts CDN).

The codebase-to-course skill produces a directory of:
- `index.html` (assembled from parts)
- `modules/*.html` (one per teaching module)
- `styles.css` + `main.js` (interactivity: quizzes, code blocks with plain-English explanations, scroll-based navigation, animated diagrams)

Plus the skill enforces a 4-6 module curriculum, vibe-coder tone, and the
specific design system.

## When to use

- User wants an interactive walkthrough of how their codebase works
- Onboarding material for new contributors
- Documenting a specific PR/diff in human-readable form
- "Make a course from this branch" requests — produce a teaching artifact from
  the diff + context, not the whole repo

## How to invoke

The skill is **not bundled with Hermes**. Install or invoke it via Claude Code:

```bash
# Option 1: Clone the skill (one-time)
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course
cat /tmp/codebase-to-course/SKILL.md  # read the full skill

# Option 2: Invoke via Claude Code with the skill context
cd /tmp/codebase-to-course
/path/to/claude --print --dangerously-skip-permissions "$(cat SKILL.md)

# Now point Claude Code at a codebase:
/path/to/claude --print --dangerously-skip-permissions "Generate an interactive
single-page HTML course from /home/Hermes/repos/OPENMAIC/core/ using the
codebase-to-course skill (SKILL.md is in /tmp/codebase-to-course/).

CONTEXT — what to teach
[domain description, target learner, modules to cover]

OUTPUT
Generate the full course directory per SKILL.md Phase 3, then run build.sh.
Final output at /path/to/_course/ with index.html + modules/*.html + styles.css + main.js."
```

## Curated subset pattern (use for focused PR walkthroughs)

For "make a course from this PR" requests, don't run the skill on the whole repo
(30+ min, too broad). Stage the diff into a curated directory first:

```bash
# Example: PR #4517 (StrEnum refactor)
mkdir -p /tmp/course-4517/diff-only/{config,core/agent_harness/session,core/agent_harness/turns,surfaces/interactive_shell/command_registry,tests/core/runtime/llm,tests/interactive_shell,_context}

# Copy the changed files
cp config/llm_reasoning_effort.py /tmp/course-4517/diff-only/config/
cp core/agent_harness/session/session_core.py /tmp/course-4517/diff-only/core/agent_harness/session/
# ... etc

# Copy the unified diff for context
git diff > /tmp/course-4517/diff-only/_context/00_unified_diff.patch
git log -1 --format=%s > /tmp/course-4517/diff-only/_context/01_commit_subject.txt

# Run skill against /tmp/course-4517/diff-only/ instead of the full repo
```

Tells the skill "the codebase IS this PR" — output is tightly focused.

## Enrich with MiniMax image + TTS (verified Jul 30 2026)

After the course renders, optionally add per-module hero image + audio narration
using MiniMax's image_generation + t2a_v2 endpoints. Full recipe + ready-to-run
scripts in [`references/minimax-enrichment.md`](references/minimax-enrichment.md).

**Critical endpoint quirk:** use `https://api.minimax.io` (NOT `api.minimaxi.com`).
Both endpoints exist; `minimaxi.com` rejects the global key with `2049 "invalid api key"`.
Bearer auth with `MINIMAX_API_KEY` (same key that works for LLM calls) works for both
image + TTS on `api.minimax.io`.

```bash
# Image (16:9 hero illustration per module)
POST https://api.minimax.io/v1/image_generation
{
  "model": "image-01",
  "prompt": "...",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 1,
  "prompt_optimizer": false
}
# Response: data.image_urls[0]

# TTS (~30-50s narration per module)
POST https://api.minimax.io/v1/t2a_v2
{
  "model": "speech-2.8-hd",
  "text": "...",
  "stream": false,
  "output_format": "hex",
  "voice_setting": { "voice_id": "English_Graceful_Lady", "speed": 1.0, "vol": 1, "pitch": 0 },
  "audio_setting": { "sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1 },
  "language_boost": "auto"
}
# Response: data.audio (hex-encoded MP3)
```

After generation, inject into each module HTML with `references/inject-assets.py` —
the script prepends a hero figure + audio player to each module's first screen,
then re-runs `build.sh` to reassemble `index.html`.

## Serve on Tailscale IP (verified Jul 30 2026)

```bash
# Pick an unused port
for port in 8081 8082 8083; do
  (echo > /dev/tcp/127.0.0.1/$port) 2>/dev/null || break
done

# Serve the course directory
python3 -m http.server $port --bind 0.0.0.0

# Open at:
#   http://100.95.175.17:$port  (Tailscale)
#   http://192.168.1.9:$port     (local WiFi)
#   http://localhost:$port       (direct)
```

`python3 -m http.server` is sufficient — no nginx needed.

## Known issues / pitfalls

### Token plan 429 on long renders

Long skill invocations (full repo with 500+ files) hit MiniMax token plan limits
and return `API Error: 429 Token Plan usage limit reached`. The smaller opensre
course attempt failed this way on Jul 30 2026. **Mitigation:** stage a curated
subset (typically 5-20 files) instead of feeding the whole repo to the skill.
The skill produces 4-6 modules from ~20 files just as well as from a whole repo.

### Skill is heavy on output

Each module is a full HTML file. A 6-module course is ~3-5MB of HTML+CSS+JS.
Claude Code's `--print` mode produces ~50K-100K tokens of output per render.
Plan accordingly — give it a generous timeout (1500s+) and run in the background
with `notify_on_complete=true` so you can do other work.

### Skills render silently

`--print` mode writes to stdout as it goes. If you don't tail the output, you
won't know what stage the render is at. Use `terminal(background=true)` with
`notify_on_complete=true` and poll with `process(action='poll')` periodically.
The render takes 5-15 minutes for a curated subset.

### Module DOM shape varies — match the marker to the actual rendered HTML

When injecting hero image + audio player into modules, the rendered HTML uses
`<section class="screen animate-in">` (NOT `<div class="screen animate-in">`).
The marker-based inject script must match what's actually emitted, otherwise
no modules get patched and the script silently no-ops.

Diagnostic: after rendering, check the marker with:

```bash
grep -oE '<(section|div) class="screen[^"]*"' <course>/modules/01-foo.html | sort -u
```

If only `<section>` appears, the inject script must use `<section>` too.
The original template (in `references/_base.html`) defines `<section>` — match it.

### Claude Code path quirk on this server

`claude` lives at `/home/Hermes/node-v22.13.0-linux-x64/bin/claude` (single `~`,
no double). Common wrong paths that look right:
- `/home/Hermes/.node-v22.13.0-linux-x64/bin/claude` (extra dot)
- `/usr/local/bin/claude` (not installed there)
- `which claude` → resolves to the correct single-tilde path

Discover the right path with:

```bash
which claude  # canonical answer
find /home/Hermes -maxdepth 4 -name claude -type f 2>/dev/null | head -5
```

Use the full path in shell scripts to avoid re-discovery on every invocation.

### OpenMAIC IMAGE/TTS env var bases are correct, but adapter fallback is wrong

When generating TTS + image assets via MiniMax for the course, the env vars
`IMAGE_MINIMAX_BASE_URL` and `TTS_MINIMAX_BASE_URL` in
`/home/Hermes/repos/OpenMAIC/core/.env.local` point to `https://api.minimax.io`
(correct). The global `MINIMAX_API_KEY` (LLM key) works for image + TTS on
that domain with Bearer auth.

The latent bug is in the **adapter code** (`lib/audio/constants.ts` and
`lib/media/adapters/minimax-image-adapter.ts`) — the hardcoded fallback for
`minimax-tts` and image generation is `https://api.minimaxi.com` (one
extra "i"). If `IMAGE_MINIMAX_BASE_URL` / `TTS_MINIMAX_BASE_URL` is unset,
requests fall through to `minimaxi.com` and the global key is rejected with
`2049 invalid api key`. The env-var override works fine when set — but the
hardcoded fallback would silently break things on a fresh install that
forgot to set the env var.

This is a separate OpenMAIC repo issue, NOT an opensre diff scope item. If
the user asks to fix it: one-line edit in two files.

## Verified end-to-end example (Jul 30 2026)

Goal: render the OpenMAIC core codebase as a course with hero images + narration.

```bash
# 1. Skill invocation (~10 min)
cd /tmp/codebase-to-course
/path/to/claude --print --dangerously-skip-permissions "$(cat SKILL.md)

# 2. Image generation (~30s × 6 modules = 3 min)
python3 generate_images.py  # uses api.minimax.io/v1/image_generation

# 3. TTS generation (~30s × 6 modules = 3 min)
python3 generate_audio.py   # uses api.minimax.io/v1/t2a_v2

# 4. Asset injection into module HTML (~5s)
python3 inject_assets.py    # adds hero img + audio player, rebuilds index.html

# 5. Serve (~1s)
python3 -m http.server 8083 --bind 0.0.0.0

# Total: ~17 min. Output: 5.1MB self-contained course at http://<ip>:8083
```

## Related skills

- `minimax-tts-video` — MiniMax TTS + image + video API reference (host quirk,
  payload shapes, known voices)
- `flux-image-gen` — Image generation pipeline details
- `codebase-inspection` — Get LOC / language ratios before rendering (helps
  scope the curated subset)
- `github-pr-workflow` — For "render this PR" requests, the skill output can
  complement a PR walkthrough video
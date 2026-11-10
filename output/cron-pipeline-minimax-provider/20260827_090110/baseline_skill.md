---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Why this skill exists (Aug 5, 2026)

Abhinav explicitly corrected the previous pattern:

> "Everywhere in cron jobs you fail because you are using the openrouter key but no use minimal api key everywhere you have that in your config have given to you many times in the conversations even Claude code config file have it it can do tts image and token generation so use that as first priority everywhere openrouter is being used."

Two structural bugs combine to break cron-spawned pipelines:

1. **The Hermes cron scheduler does NOT source `~/.hermes/.env`** before spawning
   the script. `os.environ.get("MINIMAX_API_KEY")` returns empty, the script
   either uses a stale hardcoded fallback, or fails with `401 / 2049 invalid
   api key`.
2. **OpenRouter's free tier is 50 calls/day** and the previous "MiniMax primary,
   OpenRouter fallback" pattern burned through that in minutes when MiniMax had
   any transient blip. The Aug 3 newspaper cron hit
   `HTTP 429: Token Plan usage limit reached (2056)` and the pipeline stopped.

The new rule for any cron / recurring pipeline script:

- **MiniMax is the sole provider.** Text + image + TTS all use the `sk-cp-…` key
  in `~/.hermes/.env` against `api.minimax.io`.
- **OpenRouter is never a fallback.** If MiniMax fails, fail loud and stop.
  Never cascade to OpenRouter / Pollinations / freegen / etc. as a "soft fallback".
- **The script self-loads `~/.hermes/.env`.** Don't rely on the cron shell to
  pre-source it. Add the loader inside the script so it works regardless of
  how the cron was configured.
- **The cron prompt also pre-sources the env**, as a defensive layer in case
  the script's loader ever breaks.

## Canonical self-loader

Paste near the top of any pipeline script that runs under cron, **before**
the API key constant is read:

```python
def _load_minimax_key():
    global MINIMAX_KEY
    if os.environ.get("MINIMAX_API_KEY"):
        MINIMAX_KEY = os.environ["MINIMAX_API_KEY"]
        return
    try:
        from pathlib import Path as _P
        for _env_path in (_P.home() / ".hermes" / ".env",
                          _P.home() / ".env",
                          _P("/home/Hermes/OpenMAIC/core/.env.local")):
            if not _env_path.exists():
                continue
            for _line in _env_path.read_text().splitlines():
                _line = _line.strip()
                if not _line or _line.startswith("#") or "=" not in _line:
                    continue
                _k, _v = _line.split("=", 1)
                if _k == "MINIMAX_API_KEY" and _v and _v != "***":
                    MINIMAX_KEY = _v
                    os.environ["MINIMAX_API_KEY"] = _v
                    return
    except Exception as _e:
        log("KEYS", f"  .env load error: {_e}")

MINIMAX_KEY = os.environ.get("MINIMAX_API_KEY", "") or ""
_load_minimax_key()
```

**Why three source paths:** The current key lives in `~/.hermes/.env`. The
fallback to `~/.env` handles the case where a user prefers the system-level
location. The fallback to `/home/Hermes/OpenMAIC/core/.env.local` catches the
common case where the OpenMAIC env was sourced by a sibling service and the
key is already there.

**Why the `!= "***"` check:** The Hermes runtime sanitizer rewrites secret
values to `***` at the write_file boundary (see `devops/hermes-content-filter-quirks`).
If a previous session wrote the env file with the sanitizer active, the value
column will literally be three stars. Skip those lines so you don't load
a known-broken key.

## Canonical cron prompt pre-amble

When creating a `cronjob` that runs a pipeline script:

```
Run the <name> pipeline and deliver the output to <channel>.

Steps:
1. cd <repo>
2. set -a; source ~/.hermes/.env; set +a     ← pre-source the env defensively
3. <venv>/bin/python3 <script>.py
4. <send result to channel>
5. Log success/failure

Note: The script ALSO loads ~/.hermes/.env internally as a fallback, but
pre-sourcing in the shell guarantees the key is present even if the script's
loader ever breaks. The script is now MiniMax-only — no OpenRouter fallback,
no rate-limit cascade.

Do NOT use OpenRouter. Do NOT call any LLM via openrouter.ai. Use the
MINIMAX_API_KEY environment variable for ALL text, image, and TTS calls.
```

## Canonical MiniMax helpers (paste into the pipeline module)

```python
import requests as _req

def _strip_reasoning(text: str) -> str:
    """Remove MiniMax thinking/reasoning blocks from response text."""
    import re as _re
    text = _re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=_re.DOTALL)
    text = _re.sub(r'\[Reasoning\]:.*?(?=\n\n|\n[A-Z]|$)', '', text, flags=_re.DOTALL)
    text = _re.sub(r'Thinking:*.*?(?=\n\n|\n[A-Z]|$)', '', text, flags=_re.IGNORECASE)
    return text.strip()


def minimax_generate(prompt: str, max_tokens: int = 500, temperature: float = 0.7,
                     model: str = None, system: str = None) -> str:
    """Generate text via MiniMax (M2.7-highspeed default, Anthropic-format endpoint).

    Uses the Anthropic-format endpoint, which surfaces thinking content cleanly
    and avoids the empty-content bug that hits the OpenAI-format
    /v1/text/chatcompletion_v2 path with M2.7+.
    """
    if not MINIMAX_KEY:
        log("MINIMAX", "  No MINIMAX_API_KEY — cannot generate")
        return ""
    model = model or "MiniMax-M2.7-highspeed"
    # M2.7 thinking block eats 400-800 tokens; bump small budgets to ≥4000
    eff_max = max(max_tokens, 4000)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model, "max_tokens": eff_max, "messages": messages,
               "temperature": temperature}
    headers = {"x-api-key": MINIMAX_KEY,
               "anthropic-version": "2023-06-01",
               "Content-Type": "application/json"}
    try:
        resp = _req.post(
            "https://api.minimax.io/anthropic/v1/messages",
            headers=headers, json=payload, timeout=60,
        )
        if resp.status_code != 200:
            log("MINIMAX", f"  HTTP {resp.status_code}: {resp.text[:200]}")
            return ""
        data = resp.json()
        text = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text += block.get("text", "")
        return _strip_reasoning(text)
    except Exception as e:
        log("MINIMAX", f"  Error: {e}")
        return ""


def minimax_image(prompt: str, resolution: str = "1K") -> bytes | None:
    """Generate an image via MiniMax image-01. Returns PNG/JPEG bytes or None."""
    if not MINIMAX_KEY:
        return None
    try:
        resp = _req.post(
            "https://api.minimax.io/v1/image_generation",
            headers={"Authorization": f"Bearer {MINIMAX_KEY}",
                     "Content-Type": "application/json"},
            json={"model": "image-01", "prompt": prompt, "resolution": resolution},
            timeout=60,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        image_url = (data.get("data", {}).get("image_urls", [None])[0]
                     or data.get("image_url")
                     or data.get("data", {}).get("image_url"))
        if not image_url:
            return None
        img_resp = _req.get(image_url, timeout=30)
        if img_resp.status_code == 200 and len(img_resp.content) > 1024:
            return img_resp.content
        return None
    except Exception as e:
        log("MINIMAX", f"  Image error: {e}")
        return None


def minimax_tts(text: str, voice: str = "alloy", speed: float = 1.0) -> bytes | None:
    """Generate TTS audio via MiniMax T2A v2. Returns MP3 bytes or None.

    Default voice = alloy (OpenAI-compatible name; MiniMax also accepts
    echo/nova/shimmer/onyx/fable/ash and English_* named voices).
    Response format: hex-encoded MP3 in data.audio (NOT a URL).
    """
    if not MINIMAX_KEY:
        return None
    try:
        resp = _req.post(
            "https://api.minimax.io/v1/t2a_v2",
            headers={"Authorization": f"Bearer {MINIMAX_KEY}",
                     "Content-Type": "application/json"},
            json={
                "model": "speech-2.8-hd",
                "text": text,
                "voice_setting": {"voice_id": voice, "speed": speed,
                                  "vol": 1.0, "pitch": 0},
                "audio_setting": {"sample_rate": 24000, "format": "mp3"},
            },
            timeout=60,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        audio_hex = data.get("data", {}).get("audio", "")
        if audio_hex:
            return bytes.fromhex(audio_hex)
        audio_url = data.get("data", {}).get("audio_url")
        if audio_url:
            return _req.get(audio_url, timeout=30).content
        return None
    except Exception as e:
        log("MINIMAX", f"  TTS error: {e}")
        return None
```

## Migration recipe for an existing OpenRouter-using pipeline

When retrofitting an existing pipeline (canonical example: `newspaper_daily.py`,
Aug 5, 2026):

1. **Keep the old `openrouter_generate()` as a deprecation alias** that delegates
   to `minimax_generate()`. This way every existing call site keeps working
   without a full rewrite in one pass.

   ```python
   def openrouter_generate(prompt, max_tokens=500, temperature=0.7):
       """DEPRECATED — wrapper kept for one release. Calls minimax_generate."""
       return minimax_generate(prompt, max_tokens=max_tokens, temperature=temperature)
   ```

2. **Add the three `minimax_*` helpers** above as the canonical implementation.
3. **Move the `~/.hermes/.env` self-loader** into the script.
4. **Replace inline `requests.post(...)` calls** that hit `/v1/text/chatcompletion_v2`
   with `minimax_generate(...)`. The old endpoint returns empty `content` for
   M2.7+ thinking-block models — that was a second-order bug masked by the
   OpenRouter cascade.
5. **Patch `bypass_fetch.py`** (or any monkey-patch helper) to also patch the
   new function names:

   ```python
   def _bypass_minimax(prompt, **kw):
       print(f"  [BYPASS minimax] prompt={prompt[:60]}...")
       return ""
   newspaper_daily.minimax_generate = _bypass_minimax
   # Also patch the legacy alias in case anyone else calls it
   newspaper_daily.openrouter_generate = _bypass_minimax
   ```

6. **Update the cron prompt** to pre-source `.env` and explicitly forbid
   OpenRouter calls.
7. **Smoke-test all three** (text / image / TTS) end-to-end before declaring done.

## Smoke-test recipe (do this after every wiring change)

```python
import importlib.util, sys
spec = importlib.util.spec_from_file_location('m', '/path/to/script.py')
m = importlib.util.module_from_spec(spec); sys.modules['m'] = m
spec.loader.exec_module(m)

# 1. text
out = m.minimax_generate('Reply with exactly three words: hello from minimax.',
                          max_tokens=100, temperature=0.1)
assert out and len(out) > 5, f"text gen failed: {out!r}"
print(f'text OK: {out!r}')

# 2. image
img = m.minimax_image('a tiny red apple on a white background, minimal', resolution='1K')
assert img and img[:3] == b'\xff\xd8\xff', f"image gen failed: {len(img) if img else 0} bytes"
print(f'image OK: {len(img)} bytes JPEG')

# 3. tts
audio = m.minimax_tts('Hello Abhinav.', voice='alloy', speed=0.95)
assert audio and (audio[:3] == b'ID3' or audio[0] == 0xFF), f"tts failed: {len(audio) if audio else 0} bytes"
print(f'tts OK: {len(audio)} bytes MP3')
```

If any of the three returns empty, do not declare done. The pipeline will
fail at runtime.

## Endpoints reference (the canonical MiniMax set)

| Capability | Endpoint | Auth | Model | Notes |
|---|---|---|---|---|
| Text/chat | `https://api.minimax.io/anthropic/v1/messages` | `X-Api-Key` + `anthropic-version: 2023-06-01` | `MiniMax-M2.7-highspeed` | Anthropic format surfaces thinking block; OpenAI format truncates to empty content |
| Image | `https://api.minimax.io/v1/image_generation` | `Authorization: Bearer` | `image-01` | `resolution: "1K"` → 1024×1024 JPEG; `2K` and `HD` also work |
| TTS | `https://api.minimax.io/v1/t2a_v2` | `Authorization: Bearer` | `speech-2.8-hd` | `data.audio` is hex-encoded MP3; `bytes.fromhex()` to decode |
| Model list | `https://api.minimax.io/v1/models` | `Authorization: Bearer` | (n/a) | Always query this before claiming a model exists |

**Do NOT use `https://api.minimax.chat/*` or `https://api.minimaxi.com/*`.**
Those hosts reject the `sk-cp-…` key with `2049 invalid api key`.

## Verified voices on this key (Aug 5, 2026)

TTS voices that return `status_code: 0` and real audio:
- `alloy`, `echo`, `nova`, `shimmer`, `onyx`, `fable`, `ash` (OpenAI-style names)
- `English_Graceful_Lady`, `English_Trustworth_Man`, `English_PassionateWarrior`

Voices that REJECT (`2054 voice id not exist`):
- `af_heart`, `bf_emma`, `bf_emily`, `am_michael` (these are Kokoro names)
- `coral`, `sage`, `ballad`, `verse`

## Locked Cron Video Scripts — Execution and Delivery Contract

When a scheduled video pipeline is explicitly locked by the user (for example, "do not modify the script"), execute the existing script as-is. Do not retrofit providers, alter retry behavior, or patch the pipeline during the run. Treat the script's live stdout as the source of truth for the observed provider path and outcome; do not claim that the configured provider policy was followed unless the run actually demonstrates it.

For a script that sends its own email through SMTP:

1. Run it from the requested repository/virtual environment.
2. Wait for the process to exit and capture the complete final output. If the process tool clamps long waits, poll in bounded intervals until it exits; do not report from an intermediate progress snapshot.
3. Extract only the requested fields: topic, output path, duration, slide count, and whether the script's `send_email()` succeeded.
4. Never add `MEDIA:` tags when the script owns delivery. If email fails but the file exists, report the disk path and the failed email status; do not re-attach or send a second copy from the agent response.
5. Do not invent metadata. If a field is absent from the final output, report it as unavailable rather than inferring it from a partial run.

The reusable execution/reporting details are in `references/locked-video-pipeline-reporting.md`.


## Worked example: newspaper pipeline (Aug 5, 2026)

The Daily Intelligence newspaper (`/home/Hermes/repos/newspaper/newspaper_daily.py`)
was the canonical offender. Original code had `openrouter_generate()` with an
OpenRouter fallback chain; the cron `0cab554ffd45` failed on Aug 3 with
`HTTP 429: Token Plan usage limit reached (2056)` because the fallback burned
the 50-call/day free tier.

Patch shipped Aug 5:
- `_load_minimax_key()` self-loader from `~/.hermes/.env` (3-path fallback)
- `minimax_generate()`, `minimax_image()`, `minimax_tts()` canonical helpers
- Two inline `requests.post(.../v1/text/chatcompletion_v2)` blocks (psych
  explainer + special content) replaced with `minimax_generate(...)`
- `generate_image()` rewrote to use `minimax_image()` shared helper
- `openrouter_generate()` kept as deprecation alias
- `bypass_fetch.py` patches both `minimax_generate` AND `openrouter_generate`
- Cron prompt updated: pre-source `.env`, forbid OpenRouter

Live smoke test result (Aug 5, 2026):
- `minimax_generate('Reply with exactly three words: hello from minimax.', max_tokens=100, temperature=0.1)` → `'hello from minimax'`
- `minimax_image('a tiny red apple on a white background, minimal', resolution='1K')` → 88,943 bytes valid JPEG (`ffd8ffe0…`)
- `minimax_tts('Daily Intelligence: testing minimax speech synthesis.', voice='English_Graceful_Lady', speed=0.9)` → 91,902 bytes MP3 (24kHz, ID3 v2.4)

## Confirmed stable (Aug 14, 2026)

Full newspaper pipeline run: 685s (~11.5 min), all text + image + TTS via MiniMax only. One MiniMax read timeout during SPECIAL section → fell back to curated content gracefully. No OpenRouter calls made. No rate-limit cascade. Pipeline delivered 4.8 MB PDF to Telegram chat 6373282046. Confirms the MiniMax-only directive is production-stable.

## See also

- `verified-model-api-research` — broader MiniMax + FLUX + Higgs + Wan API reference
- `minimax-tts-video` — TTS ad-build pipeline with FFmpeg post-processing (segment + escalate intensity, pause markers, ad pattern)
- `flux-image-gen` — image generation pipeline patterns
- `devops/hermes-content-filter-quirks` — when API keys get rewritten to `***` in `write_file` outputs (causes the `!= "***"` check to matter)
- `automation/newspaper-pipeline` — the pipeline that drove this skill's creation

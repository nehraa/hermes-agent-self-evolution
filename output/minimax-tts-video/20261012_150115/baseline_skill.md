---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## ⚠️ CRITICAL — Model Name Mismatch

MiniMax token plan lists models with one set of names, but the API accepts a different set. This causes `token plan not support model` errors even for listed models.

**Confirmed working on this key (sk-cp-...):**
- LLM: `MiniMax-M2.7` → `https://api.minimax.io/v1/chat/completions`
- Music: `music-2.6` → `https://api.minimax.io/v1/music_generation`
- TTS: `speech-2.8-hd` → `https://api.minimax.io/v1/t2a_v2` ✅ (Jun 24 2026) — see TTS section below
- Video: works on `api.minimax.io/v1/video_generation` (see Video Generation section)

**Plan vs API model name mismatch:** Real for some models, but NOT a blanket TTS block. Earlier "TTS BLOCKED" diagnosis was wrong — it was testing against the wrong host (`api.minimaxi.com`) and concluding plan limit. The key DOES work for TTS on `api.minimax.io`.

## MiniMax API — Critical Fixes (May 17 2026)

### Full API Key
```
sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
```
**Save this key in memory AND in the script's `_EXPLICIT_KEYS` dict — .env masks it as `***` so it looks empty when read.**

### Correct Endpoint — `/v1/chat/completions`
```
Base URL: https://api.minimax.io
Endpoint: https://api.minimax.io/v1/chat/completions  ← NOT /anthropic/v1/chat/completions
Auth:     Bearer <key>
```
The `/anthropic` suffix returns 404. The `minimax-chat` base (`api.minimax.chat`) returns 1004 auth errors for this key. Use `api.minimax.io/v1/chat/completions`.

### MiniMax Response Format — Thinking Blocks Contain the Real Content
MiniMax returns `<think>...` reasoning blocks BEFORE the actual JSON. The slides JSON is buried inside the thinking block, NOT at the start of the response.

**Correct parsing pattern:**
```python
import re, json

def parse_minimax_json_response(raw: str) -> dict:
    """Extract JSON from MiniMax response that has content inside <think>... blocks."""
    # Remove the thinking block
    cleaned = re.sub(r'<think>.*?', '', raw, flags=re.DOTALL).strip()
    # Find the JSON object
    idx = cleaned.find('{"slides"')
    if idx < 0:
        idx = cleaned.find('"slides"')  # bare list format
    if idx < 0:
        raise ValueError(f"No slides JSON found. Content starts: {cleaned[:200]}")
    
    json_str = cleaned[idx:]
    # Balance braces to find complete JSON object
    brace_count = 0
    end = 0
    for i, c in enumerate(json_str):
        if c == '{': brace_count += 1
        elif c == '}': brace_count -= 1
        if brace_count == 0 and i > 10:
            end = i + 1
            break
    if end == 0:
        raise ValueError(f"Could not balance braces in JSON from MiniMax")
    return json.loads(json_str[:end])
```

**Why the old parse failed:** `json.loads(raw_clean)` fails because `raw_clean` starts with non-JSON text (explanatory prose from the model). The `json.loads` call hits the first `{` of the thinking content and fails.

**max_tokens:** Use 2000 minimum for slide generation (1200 was too low and got truncated responses).

### NVIDIA Flux on this server — Fast-Fail Detection
Flux works reliably on this server BUT when all images return < 7KB in < 5s total, it means NVIDIA is rate-limiting you. The correct response is 15-80KB images in 2-5s per call.

**Fast-fail detection:**
```python
if total_flux_time < 5.0 and all_images_under_7kb:
    print("NVIDIA Flux exhausted — network blocked, bailing out")
    # → switch to freegen fallback immediately
```

Do NOT keep retrying Flux when it's rate-limited — it won't recover within the same run.

### Freegen Fallback — Correct venv Path
Freegen needs browser-use's Playwright:
```python
venv_python = "/home/Hermes/.hermes/browser-use/.venv/bin/python3"  # NOT this server's python
```
But on this server that path may not exist. The actual working python for browser-use is:
```bash
/home/Hermes/deer-flow/backend/.venv/bin/python3  # has playwright installed
# OR use the system python with playwright installed:
python3 -c "from playwright.sync_api import sync_playwright"  # test first
```
If the venv python doesn't exist, freegen will fail with `No such file or directory`. Fix: find which python has playwright (`python3 -c "import playwright"` across pythons) and use that path.

## Configuration
- **API Key:** `sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA`
- **Base Endpoint:** `https://api.minimax.io/v1`

## LLM / Chat Completion — Anthropic format at `/anthropic/v1/messages` (July 2026)

For text, vision, and reasoning tasks (NOT `/v1/chat/completions` which is broken for M2.7):

**Endpoint:** `POST https://api.minimax.io/anthropic/v1/messages`
**Auth:** `X-Api-Key: <key>` header (capital X), `anthropic-version: 2023-06-01`
**NOT Bearer auth** — that's OpenAI-style and the wrong format here.

### Thinking-block gotcha (the #1 thing that breaks M2.7 integrations)

`MiniMax-M2.7-highspeed` (and `MiniMax-M2.7`) emit a `thinking` content block BEFORE
any `text` block, eating 400-800 tokens of internal reasoning.

**If `max_tokens` is too low** (the default 4096 is borderline, anything ≤1024 is fatal):
the response gets truncated mid-thinking, the `text` block is empty or missing,
and your code sees `choices[0].message.content = ""`.

**Fixes:**
- Set `max_tokens: 8000` for any task that involves reasoning or multi-step output.
- For summarization/short-answer tasks: `max_tokens: 4000` is enough.
- When parsing the response, walk the `content` array and concatenate ONLY blocks
  where `type == "text"` — discard `thinking` blocks. The JSON shape is:

```json
{
  "id": "...",
  "content": [
    {"type": "thinking", "thinking": "We have a conversation..."},
    {"type": "text", "text": "the actual answer"}
  ],
  "stop_reason": "end_turn",
  "model": "MiniMax-M2.7-highspeed",
  "usage": {"input_tokens": 62, "output_tokens": 96}
}
```

Do NOT assume `content[0].text` is the answer — it's the thinking block. Walk all blocks.

### Multimodal (vision / image) — base64 in Anthropic source format

For image input, the OpenAI `image_url` shape does NOT work here. Convert to Anthropic's
`image` block with a base64 source:

```python
# OpenAI shape (DOES NOT WORK on anthropic endpoint):
{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,XXXX"}}

# Anthropic shape (USE THIS):
{"type": "image",
 "source": {"type": "base64", "media_type": "image/jpeg", "data": "XXXX"}}
```

If you have a bot/integration that builds OpenAI-format messages, write a small
`_flatten_content()` helper to convert at the boundary — see Claude-bot at
`/home/Hermes/Claude-bot/telegram-claude-channel.py` for a working example.

### System prompt placement

Anthropic format uses a TOP-LEVEL `system` field, NOT a `system` message in the
`messages` array:

```python
payload = {
    "model": "MiniMax-M2.7-highspeed",
    "max_tokens": 8000,
    "system": "You are a helpful assistant.",   # NOT in messages
    "messages": [{"role": "user", "content": "..."}]
}
```

Sending system as a message role will be accepted but the LLM will treat it as
user content — silent semantic bug, hard to debug.

### TTS response key — confirmed `data.audio`, NOT `data.audio_url`

When calling `/v1/t2a_v2` with `output_format: "url"`, the response is:

```json
{
  "data": {"audio": "https://minimax-algeng-.../tts-XXX.mp3?...", "status": 2, "ced": ""},
  "extra_info": {"audio_length": 1044, "audio_size": 12345, "audio_format": "mp3", ...},
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

The URL is under `data.audio`, NOT `data.audio_url` (a common mistake in older
code/docs). Parse with `data.get("data", {}).get("audio")` and fall back to
`audio_url` if the API ever changes.



## Kokoro Local TTS — Use When You Need a Free Fallback

MiniMax TTS works on `api.minimax.io` (see TTS section above) but if you want a local zero-cost alternative, Kokoro is the answer. The earlier "MiniMax TTS is BLOCKED" claim was incorrect — keep Kokoro for redundancy/quality choice, not as a workaround for a perceived TTS outage.

### Kokoro Setup
```python
sys.path.insert(0, '/home/Hermes/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
from kokoro_onnx import Kokoro
import soundfile as sf

k = Kokoro(
    model_path="/home/Hermes/.local/share/kokoro/kokoro-v1.0.onnx",
    voices_path="/home/Hermes/.local/share/kokoro/voices-v1.0.bin"
)
voices = k.get_voices()  # Always call this to get actual voice names
audio, sr = k.create(text, voice="af_heart")  # example
sf.write("output.wav", audio, sr)
```

### Kokoro Voice Names — CONFIRMED WORKING (May 2026)
```
af_alloy, af_aoede, af_bella, af_heart, af_jessica, af_kore, af_nicole,
af_nova, af_river, af_sarah, af_sky, am_adam, am_echo, am_eric,
am_fenrir, am_liam, am_michael, am_onyx, am_puck, am_santa,
bf_alice, bf_emma, bf_isabella, bf_lily, bm_daniel, bm_fable,
bm_george, bm_lewis, ef_dora, em_alex, em_santa, ff_siwis,
hf_alpha, hf_beta, hm_omega, hm_psi, if_sara, im_nicola,
jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo,
pf_dora, pm_alex, pm_santa, zf_xiaobei, zf_xiaoni, zf_xiaoxiao,
zf_xiaoyi, zm_yunjian, zm_yunxi, zm_yunxia, zm_yunxia, zm_yunyang
```
**NEVER use** `bf_emily`, `am_andrew`, `bf_fable` — these do not exist on this server.
`af_heart`, `af_nicole`, `am_michael`, `bf_emma`, `af_sarah`, `am_adam`, `bf_alice`, `af_nova`, `am_onyx`, `af_bella`, `am_fenrir`, `bf_isabella`, `af_river`, `bm_lewis`, `af_sky`, `bm_fable`, `af_jessica`, `am_eric`, `af_alloy`, `bf_lily`

### Use in Remotion
```tsx
import { Audio } from "remotion";
<Audio src="/slides/slide_1.wav" />
```
Generate all audio files and place in `public/slides/` for Remotion to serve.

### Audio Duration Planning
~700 chars of text → ~38s audio via Kokoro. Match frames_per_slide to audio length:
- 38s audio → 150 frames at 30fps = 5s per slide (text will be truncated or paced)
- For full audio playback: 38s audio needs 38×30 = 1140 frames per slide
- For 5s visual slide: let audio play independently, visual advance on timer

## Video Generation

**Endpoint:** `POST https://api.minimax.io/v1/video_generation`
**Query:** `GET https://api.minimax.io/v1/query/video_generation?task_id=<id>`
**Download:** `GET https://api.minimax.io/v1/files/retrieve?file_id=<id>`

### Async workflow
1. Create task → get `task_id`
2. Poll query endpoint until `status: "Success"` or `"Fail"`
3. On success, use `file_id` from response to download

### Models (from API docs)
| Model | Description | Duration | Resolution |
|-------|-------------|----------|------------|
| `MiniMax-Hailuo-2.3` | Body movement, facial expressions | 6s or 10s | 768P, 1080P |
| `MiniMax-Hailuo-2.3-Fast` | Image-to-video, fast | 6s | 768P |
| `MiniMax-Hailuo-02` | 1080P, 10s, best prompt adherence | 6s or 10s | 768P, 1080P |
| `T2V-01-Director` | Director control | 6s | 720P |

### Camera Commands (Hailuo-2.3, Hailuo-02, T2V-01-Director)
```
[Truck left] [Truck right] [Pan left] [Pan right] [Push in] [Pull out]
[Pedestal up] [Pedestal down] [Tilt up] [Tilt down] [Zoom in] [Zoom out]
[Shake] [Tracking shot] [Static shot]
```

### Create Task Request
```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "A creator at a glowing workstation [Push in]. Cinematic lighting.",
  "duration": 6,
  "resolution": "768P",
  "prompt_optimizer": true
}
```

### Query Response
```json
{
  "task_id": "176843862716480",
  "status": "Success",
  "file_id": "176844028768320",
  "video_width": 1920,
  "video_height": 1080,
  "base_resp": { "status_code": 0, "status_msg": "success" }
}
```

### Download Response
```json
{
  "file": {
    "file_id": "...",
    "bytes": 123456,
    "created_at": 1700469398,
    "filename": "output_aigc.mp4",
    "download_url": "https://..."
  }
}
```

## TTS — VERIFIED WORKING (Jun 24 2026)

The earlier "TTS BLOCKED" diagnosis was wrong. TTS works on this key — the catch is the host. See [references/tts-host-troubleshooting.md](references/tts-host-troubleshooting.md) for the 60-second host probe and the OpenMAIC wiring specifics.

### `audio_setting.bitrate` cap — 128000 (Jul 25 2026)

The TTS API **rejects `bitrate: 192000`** with `status_code: 2013 invalid params: audio_setting bitrate`. The maximum supported value is **128000**. Earlier skill docs mentioned 128000 as the OpenMAIC default — it's actually the API ceiling, not just a recommendation. Stick to 128000 (or upgrade to FLAC/WAV container if you need quality beyond 128k).

```js
audio_setting: { sample_rate: 32000, bitrate: 128000, format: 'mp3', channel: 1 }
```

### `<#x#>` pause markers (Jul 25 2026)

Place between speakable text segments to insert a controlled pause of `x` seconds (0.01–99.99, two-decimal). Cannot be used consecutively. Documented in the T2A HTTP API docs but easy to miss.

```
"Main IELTS hoon. <#0.55#> Aur har result ke baad blame sabse pehle mujhe hi milta hai."
```

Use this for **dramatic pacing** in ad reads, voiceovers, and storytelling — far more reliable than hoping the TTS model self-pauses at the right moment.

### `language_boost: "Hindi"` (Jul 25 2026)

For Devanagari-script Hindi (or any other supported language), set `language_boost` to the actual language string instead of `"auto"`. The model handles pronunciation, stress, and code-switched Hinglish noticeably better. Available options include `Hindi`, `English`, `Tamil`, `Bengali`, `auto`, and ~30 other languages.

```js
language_boost: 'Hindi'   // for Hinglish ad reads
language_boost: 'auto'    // safe default when language is unknown
```



### `<#x#>` pause markers (Jul 25 2026)

Place between speakable text segments to insert a controlled pause of `x` seconds (0.01–99.99, two-decimal). Cannot be used consecutively. Documented in the T2A HTTP API docs but easy to miss.

```
"Main IELTS hoon. <#0.55#> Aur har result ke baad blame sabse pehle mujhe hi milta hai."
```

Use this for **dramatic pacing** in ad reads, voiceovers, and storytelling — far more reliable than hoping the TTS model self-pauses at the right moment.

### `language_boost: "Hindi"` (Jul 25 2026)

For Devanagari-script Hindi (or any other supported language), set `language_boost` to the actual language string instead of `"auto"`. The model handles pronunciation, stress, and code-switched Hinglish noticeably better. Available options include `Hindi`, `English`, `Tamil`, `Bengali`, `auto`, and ~30 other languages.

```js
language_boost: 'Hindi'   // for Hinglish ad reads
language_boost: 'auto'    // safe default when language is unknown
```

### The "Multi-Segment Buildup" Ad Pattern (Jul 25 2026)

A single TTS call with fixed `speed`/`vol`/`pitch` produces a monotonic delivery. For **ad reads, voiceovers, and storytelling with a buildup**, split the script into 3–4 segments with progressively more forceful settings, then concatenate with FFmpeg.

**Recipe (3-segment Emotional Arc):**

| Segment | Speed | Vol | Pitch | Purpose |
|---|---|---|---|---|
| 1 (Hook) | 0.96 | 1.05 | −1 | Controlled, serious, sets up the problem |
| 2 (Body) | 1.01 | 1.15 | 0 | Confident, builds urgency |
| 3 (CTA) | 1.07 | 1.35 | +1 | High energy, forceful close |

Combine with `<#x#>` pause markers between phrases for dramatic pacing. Then post-process with FFmpeg:

```bash
ffmpeg -y -i joined.mp3 \
  -af "highpass=f=70,lowpass=f=14500,acompressor=threshold=-16dB:ratio=2.5:attack=10:release=120:makeup=2.5dB,alimiter=limit=0.97" \
  -c:a libmp3lame -b:a 128k output.mp3
```

The `highpass+lowpass` removes mud, `acompressor` evens out volume across segments, `alimiter` prevents the emphatic end from clipping. This is what makes the buildup feel intentional rather than glib.

**Reference script:** `scripts/generate_ielts_mastery_tts.py` — canonical Hindi male ad example, end-to-end working.

**Quick re-check:** `node scripts/probe-minimax-tts.js` — probes all three candidate hosts and prints which one(s) return real audio. Use it whenever TTS breaks before assuming plan or config issues.

### The host trap
- ❌ `https://api.minimaxi.com/v1/t2a_v2` → 200 OK with `status_code:2049 "invalid api key"` (rejects our key)
- ✅ `https://api.minimax.io/v1/t2a_v2` → 200 OK with real audio payload (uses the same key)

**Rule:** If you have a key from the global MiniMax console (the Anthropic-style key in `~/.hermes/.env`), use `api.minimax.io`. The `minimaxi.com` host is for a different key population. Don't conclude "TTS is blocked on the plan" until you've tried `api.minimax.io` explicitly.

### Working recipe
```js
const r = await fetch('https://api.minimax.io/v1/t2a_v2', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'speech-2.8-hd',
    text: 'Hello world',
    stream: false,
    output_format: 'hex',
    voice_setting: { voice_id: 'female-yujie', speed: 1.0, vol: 1, pitch: 0 },
    audio_setting: { sample_rate: 32000, bitrate: 128000, format: 'mp3', channel: 1 },
    language_boost: 'auto'
  })
});
const data = await r.json();
const audio = Buffer.from(data.data.audio, 'hex');  // MP3 bytes
```

### Known working voices (Jun 24 2026)
- `female-yujie` (Chinese female, default) — verified
- `English_Graceful_Lady`, `English_Trustworthy_Man` — listed in OpenMAIC constants, not personally re-verified

### Models
- `speech-2.8-hd` ✅ — default, high quality
- `speech-2.8-turbo` — listed, faster
- `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo` — older, listed in OpenMAIC constants

### OpenMAIC integration (Jun 24 2026)
OpenMAIC's `core/lib/audio/constants.ts` hardcodes `defaultBaseUrl: 'https://api.minimaxi.com'` for the `minimax-tts` provider. To make it work with the global key, override via env:
```
TTS_MINIMAX_API_KEY=***MINIMAX_BASE_URL=https://api.minimax.io
```
Both go in `student/.env` and `core/.env.local`. The provider code reads `TTS_MINIMAX_BASE_URL` via `TTS_ENV_MAP` in `core/lib/server/provider-config.ts` line 67.

### Failure mode reference
| Response | Meaning |
|---|---|
| 200 + `status_code: 2049 "invalid api key"` | Wrong host OR wrong key — try the other host first |
| 200 + `status_code: 2061 "token plan not support model"` | Real plan block — key works but plan excludes TTS. (No longer seen on the current key after host fix.) |
| Network error / fetch failed | DNS — `api.minimax.com` doesn't resolve. Stick to `minimax.io` or `minimaxi.com`. |

## Token Plan Usage (this key)

```
MiniMax-M2.7:              LLM text generation — WORKS
image-01:                  image generation — WORKS
music-2.6:                 music generation — WORKS
MiniMax-Hailuo-2.3-*:      video (2/day limit) — WORKS
TTS (speech-2.8-hd):       WORKS on api.minimax.io/v1/t2a_v2 (see TTS section above)
```

**TTS is available on this plan** when called against `api.minimax.io`. The earlier "plan doesn't include TTS" claim was based on tests against the wrong host (`api.minimaxi.com`) which rejected the key with 2049. After switching to `api.minimax.io`, TTS returns valid 140KB+ MP3 payloads. No plan upgrade required.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `token plan not support model, X` | Plan key model != API model | Use API doc model names |
| `incorrect model param input` | Model name not accepted | Try different variant |
| `invalid params, empty field` | Missing `voice_setting.voice_id` | Add valid voice_id |
│ Voice id not exist │ Voice ID not valid for this account │ Try different voice_id │
│ Duration only support 6s │ Wrong duration for model/resolution combo │ Adjust duration │

## Hindi male voice ad — production pattern (added July 25 2026)

Used when Abhinav asks for a Hindi male voice that is **not calm** — assertive, building, ending louder. The default TTS response (any voice_id from the catalog) reads Hindi Hinglish neutrally; for a punchy ad you need a custom-designed voice + build segment by segment.

### 1. Design a custom voice with `/v1/voice_design`

```bash
POST https://api.minimax.io/v1/voice_design
{
  "prompt": "Indian Hindi male commercial narrator, age 30-40. Strong chest voice, assertive and confrontational, not calm or soothing. Crisp Hinglish pronunciation, persuasive ad delivery. Start controlled and serious, then build urgency and intensity. Sound human, confident, slightly gritty, energetic, never robotic.",
  "preview_text": "Main IELTS hoon. Aur har result ke baad blame sabse pehle mujhe hi milta hai. Par sach ye hai, problem paper nahi, taiyari hoti hai."
}
```

Returns `{voice_id: "ttv-voice-...-XXXX", trial_audio: "<hex>"}`. Save the `voice_id` — it persists across calls and is free to use (only the design preview is $30/1M chars).

**Voice prompt keywords that worked:** "30-40", "chest voice", "assertive", "not calm", "confrontational", "build urgency", "slightly gritty", "never robotic". Avoid "calm", "soothing", "neutral" — those read as sleepy.

### 2. Segment + escalate intensity

A single TTS call can't go from calm to loud mid-sentence. Split the script into 3 segments and ramp `speed`/`vol`/`pitch`:

```text
segment 1 (problem setup):    speed 0.96, vol 1.05, pitch -1
segment 2 (solution):         speed 1.01, vol 1.15, pitch  0
segment 3 (CTA, must land):    speed 1.07, vol 1.35, pitch +1
```

Use `<#0.4#>` pause markers between punch lines. Pause markers are a TTS feature (`<#seconds#>`), not FFmpeg — they bake into the audio.

### 3. Join + post-process (FFmpeg)

```bash
# Concat (same params → no re-encode needed)
ffmpeg -f concat -safe 0 -i concat.txt -c:a libmp3lame -b:a 192k joined.mp3

# Compress + de-clip — the loud ending will clip without this
ffmpeg -i joined.mp3 \
  -af "highpass=f=70,lowpass=f=14500,acompressor=threshold=-16dB:ratio=2.5:attack=10:release=120:makeup=2.5dB,alimiter=limit=0.97" \
  -c:a libmp3lame -b:a 192k final.mp3
```

**Verify volume with `volumedetect`** — target `max_volume` around -4 to -1 dB (loud but not clipped). Below -8 dB = too quiet, above 0 dB = clipping.

### 4. Common gotchas

- **bitrate must be 128000** — `192000` returns `2013 invalid params, audio_setting bitrate`. The interface accepts only specific values.
- **`output_format: "hex"`** is the default; `"url"` returns 24h-valid URLs but the JSON shape is `data.audio` (not `data.audio_url` as some docs claim — that's the inline-citation fallback).
- **Custom voice IDs are account-scoped** — the `ttv-voice-...` design returns a fresh ID per call. Reuse the same `voice_id` for consistency; new design call = new voice even with identical prompt.
- **Preview text ≠ final script.** The `preview_text` is just for the design preview; the actual TTS uses the segment texts. The custom voice inherits the *personality* from the design prompt, not the exact words.

### 5. Reference impl

`/tmp/hermes-tmp/generate_ielts_mastery_tts.py` (canonical) — generates the 3 segments, joins, post-processes, prints `{output, duration, size, voice_id}`. Re-run after prompt tweaks.

## VibeHire Ad Script — Production Pattern (8-sec scenes, marketing)

VibeHire is an AI marketing platform (not a sales tool). Ad scripts use marketing angle — automation, scale, content on autopilot. Video format: 7 scenes × 8s = 56 seconds.

**Scene template:**
```
SCENE 1 — Hook (0:00-0:08)
  Image: [visual hook]
  Narration: "[problem-framing hook]"

SCENE 2 — The Gap (0:08-0:16)
  Image: [pain point visual]
  Narration: "[expanded problem statement]"

SCENE 3 — The Automation (0:16-0:24)
  Image: [AI dashboard / automation visual]
  Narration: "[VibeHire solution description]"

SCENE 4 — Scale (0:24-0:32)
  Image: [one-to-many visual]
  Narration: "[scale proof point]"

SCENE 5 — Proof (0:32-0:40)
  Image: [engagement / metrics visual]
  Narration: "[social proof / client result]"

SCENE 6 — Offer (0:40-0:48)
  Image: [pricing / dashboard visual]
  Narration: "[₹1K/mo offer, first week free]"

SCENE 7 — Close (0:48-0:56)
  Image: [brand logo / URL]
  Narration: "[devstudios.me/website call to action]"
```

**Assembly pipeline (FFmpeg, NOT Remotion):**
1. Generate 7 images (Flux or any image gen)
2. Generate 7 TTS audio clips (Kokoro or MiniMax TTS)
3. Concatenate all WAV files: `ffmpeg -f concat -safe 0 -i <(for f in *.wav; do echo "file '$f'"; done) -c copy all_audio.wav`
4. For each scene: `ffmpeg -loop 1 -i scene.jpg -i all_audio.wav -filter_complex "[1:a]atrim=start=Ns:end=Ne,asetpts=PTS-STARTPTS[a]" -map 0 -map "[a]" -t duration -vf "scale=1920:-1,crop=1920:1080,zoompan=z='min(zoom+0.001,1.05)':d=fps*a*duration:x='iw/2*(1-1/zoom)':y='ih/2*(1-1/zoom)'" -pix_fmt yuv420p -c:v libx264 -t duration -shortest -c:a aac scene_N.mp4`
5. Concatenate all scene clips with filter_complex
6. Burn in scene titles and counter with drawtext filters

**Key pitfall:** Remotion 4.x cannot render this in constrained environments (3.7GB RAM, no GPU → 16+ min for 66 frames). Use FFmpeg instead. Remotion is only appropriate for visual overlay animations with no per-frame image decode overhead.

## Google AI (Veo/Imagen)

**API Key:** `AIzaSyCDzqXsdFKMjD5ubVjqgI1Qx6c4gIDHkwc`

### Quota Status (as of this session)
- **Veo 3.1 (all variants):** 429 RESOURCE_EXHAUSTED — daily quota exhausted
- **Veo 2.0:** Requires GCP billing (not available on free/trial)
- **Imagen 3/4:** Requires paid plan — `Imagen 3 is only available on paid plans`
- **Gemini (text):** Works fine — free tier available

### Python SDK
```bash
uv pip install google-genai
```

### Veo Video Generation
```python
from google import genai
from google.genai import types

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",  # or veo-3.1-generate-preview, veo-3.1-lite-generate-preview
    prompt="A creator at a workstation, cinematic lighting",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",   # or "9:16"
        resolution="1080p",     # or "720p"
    ),
)

# Poll for completion
import time
while not operation.done:
    time.sleep(10)
    operation = client.models.get_operation(operation.operation.name)

# Download
for v in operation.response.generated_videos:
    with open("video.mp4", "wb") as f:
        f.write(v.video.video_bytes)
```

**Note:** `veo-3.1-lite-generate-preview` does NOT support `negative_prompt`. Use it without config or with only `aspect_ratio`/`resolution`.

### Imagen Image Generation
```python
image_op = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="Your image description",
)
for generated_image in image_op.response.generated_images:
    with open("image.png", "wb") as f:
        f.write(generated_image.image.image_bytes)
```
**Note:** Imagen 3/4 requires a paid Google Cloud plan with billing enabled.

### Available Models (confirmed via API)
```
Text: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash, gemini-2.0-flash-lite
Video: veo-3.1-fast-generate-preview, veo-3.1-generate-preview, veo-3.1-lite-generate-preview, veo-3.0-generate-001, veo-2.0-generate-001 (GCP billing req'd)
Image: imagen-4.0-generate-001, imagen-4.0-ultra-generate-001, imagen-4.0-fast-generate-001 (all paid)
Audio: gemini-2.5-flash-native-audio-*, gemini-3.1-flash-live-preview
```

## Note on Plan vs API Names

MiniMax has TWO naming systems:
1. **Token plan names** — what appears in usage/remain APIs (e.g., `speech-hd`, `MiniMax-Hailuo-2.3-6s-768p`)
2. **API model names** — what the API endpoints actually accept (e.g., `speech-2.8-hd`, `MiniMax-Hailuo-2.3`)

These often don't match. When in doubt, try the API doc names first.

**TTS caveat:** Plan/API name mismatches can still happen for other models. For TTS specifically, the issue is host, not plan — use `api.minimax.io` (not `minimaxi.com`) and `speech-2.8-hd` works.

## AI Video Gen Platform Research — Verified Facts

When researching third-party video gen platforms (Kling, Runway, Pika, Luma, etc.):

**⚠️ Never trust marketing video length claims at face value.**
"Minutes-long" or "up to 3 minutes" in ads ≠ actual generation capability. Kling AI's 3.0 model markets "minutes-long" clips but real-world output is 10-30s per generation — same bracket as everyone else. Always check:
- The actual generation UI / docs for the duration limit
- Credit cost per second of video
- Whether "long" mode requires separate high-credit mode

**Verified Kling AI data (May 2025):**
- Standard plan: $10/month = 660 credits
- Free tier: 66 credits/day, no rollover
- Standard quality (720p): ~50-70 credits/clip
- High quality (1080p): higher per clip
- Approx output: 9-13 standard-quality clips/month on $10 plan
- Max clip length: 10-30s (not 3 minutes despite marketing)

**Research workflow:**
1. Check eesel.ai for structured pricing guides (cleaner than scraping official sites)
2. Navigate to `kling.ai/experience` or `kling.ai/pricing` — these redirect often
3. If official site blocks bot detection, use Bing search → eesel.ai / aitoolapp.com summaries
4. For Bing: search results show snippet text — use it to find the specific plan table, then open the eesel.ai link for readable content

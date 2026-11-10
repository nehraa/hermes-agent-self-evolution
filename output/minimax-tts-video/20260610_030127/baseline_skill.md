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

**TTS & Video:** BLOCKED — plan vs API model name mismatch cannot be resolved without MiniMax support.

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



## Kokoro Local TTS — Recommended Over MiniMax

MiniMax TTS (`speech-2.8-hd` etc.) is BLOCKED on the current plan (status_code 2061). Kokoro is the working local alternative with zero API cost.

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

## Token Plan Usage (this key)

```
MiniMax-M2.7:              LLM text generation — WORKS
image-01:                  image generation — WORKS
music-2.6:                 music generation — WORKS
MiniMax-Hailuo-2.3-*:      video (2/day limit) — WORKS
TTS (all speech-* models): BLOCKED — plan does not include TTS
```

**TTS is not available on this plan.** All `speech-*` models return `status_code: 2061 "your current token plan not support model"`. No amount of trying different voice IDs or model variants will change this. To get TTS, a plan upgrade or TTS add-on is required.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `token plan not support model, X` | Plan key model != API model | Use API doc model names |
| `incorrect model param input` | Model name not accepted | Try different variant |
| `invalid params, empty field` | Missing `voice_setting.voice_id` | Add valid voice_id |
| `voice id not exist` | Voice ID not valid for this account | Try different voice_id |
| `duration only support 6s` | Wrong duration for model/resolution combo | Adjust duration |

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

**TTS caveat:** Even when plan/API names align (e.g., `speech-2.8-hd`), the plan may still block the model entirely with `status_code: 2061`. TTS is NOT included on the current plan.

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

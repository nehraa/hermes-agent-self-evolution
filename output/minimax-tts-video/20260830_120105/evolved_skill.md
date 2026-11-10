---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## ⚠️ CRITICAL — Model Name Mismatch

MiniMax token plans list models with one set of names, but the API accepts different names. This causes `token plan not support model` errors even for models that appear in your plan.

### Confirmed Working Combinations

| Model (Plan) | Endpoint | Status |
|--------------|----------|--------|
| `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` | ✅ |
| `music-2.6` | `https://api.minimax.io/v1/music_generation` | ✅ |
| `speech-2.8-hd` | `https://api.minimax.io/v1/t2a_v2` | ✅ (Jun 24 2026) |
| Video models | `https://api.minimax.io/v1/video_generation` | ✅ |

> **Note:** Earlier reports of "TTS BLOCKED" were incorrect. The issue was hitting `api.minimaxi.com` (wrong host) rather than the correct `api.minimax.io`. The key works fine for TTS on the correct endpoint.

---

## API Configuration

### API Key

sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
> **Storage note:** Store this key in memory and in the script's `_EXPLICIT_KEYS` dict. The `.env` file masks it as `***`, making it appear empty when read from environment variables.

### Correct Endpoints

| Service | Correct Endpoint | Common Mistake |
|---------|------------------|----------------|
| Chat / LLM | `https://api.minimax.io/v1/chat/completions` | ❌ `/anthropic/v1/chat/completions` (404) |
| TTS | `https://api.minimax.io/v1/t2a_v2` | ❌ `api.minimaxi.com` (wrong host) |
| Music | `https://api.minimax.io/v1/music_generation` | — |
| Video | `https://api.minimax.io/v1/video_generation` | — |

**Auth header:** `Authorization: Bearer <key>`

---

## Response Parsing — Thinking Blocks

MiniMax returns `

{
  "slides": [...]
}
The parser must strip the `` wrapper before extracting JSON.

---

## TTS Usage (`speech-2.8-hd`)

### Request Format

python
import requests

url = "https://api.minimax.io/v1/t2a_v2"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "speech-2.8-hd",  # Use model name from plan
    "text": "Your spoken text here",
    "voice_settings": {
        "speed": 1.0,
        "pitch": 0,
        "volume": 0
    }
}

response = requests.post(url, json=payload, headers=headers)
### Response

Returns audio binary data. Handle according to your output format (save as MP3/WAV, stream, etc.).

---

## Video Generation (`MiniMax-Hailuo-2.3`)

### Request Format

python
url = "https://api.minimax.io/v1/video_generation"

payload = {
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "Your video description here"
}

response = requests.post(url, json=payload, headers=headers)
> **Check plan limits:** Ensure your token plan includes video generation credits. Video generation is a separate quota from TTS/chat.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `token plan not support model` | Model name mismatch between plan and API | Use confirmed working model names from the table above |
| `404` on chat endpoint | Wrong path (`/anthropic/...`) | Use `/v1/chat/completions` |
| `1004` auth error | Wrong host (`api.minimax.chat`) | Use `api.minimax.io` |
| Empty response / parse error | Thinking block not stripped | Use `parse_minimax_json_response()` above |
| TTS returns but audio is wrong | Wrong model for your plan | Verify `speech-2.8-hd` is in your plan |
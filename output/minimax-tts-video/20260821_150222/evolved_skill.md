---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

> **Last verified:** June 24, 2026

---

## ⚠️ CRITICAL: Model Name Mismatch

MiniMax token plan lists models with names that differ from what the API actually accepts. This causes `token plan not support model` errors even for models listed in your plan.

### Confirmed Working Configurations

| Feature | Plan Model | API Endpoint | Status |
|---------|-----------|--------------|--------|
| LLM | `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` | ✅ |
| Music | `music-2.6` | `https://api.minimax.io/v1/music_generation` | ✅ |
| TTS | `speech-2.8-hd` | `https://api.minimax.io/v1/t2a_v2` | ✅ |
| Video | — | `https://api.minimax.io/v1/video_generation` | ✅ |

### Common Pitfalls

- **Wrong host:** `api.minimaxi.com` returns plan limit errors. Use `api.minimax.io`.
- **Wrong path:** `/anthropic/v1/chat/completions` returns 404. Use `/v1/chat/completions`.
- **Wrong host for chat:** `api.minimax.chat` returns 1004 auth errors.

---

## API Key

sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
> **Note:** `.env` files mask this key as `***`, making it appear empty. Store the key explicitly in your script's `_EXPLICIT_KEYS` dict or environment variable directly.

### Auth Header Format

Authorization: Bearer <key>
---

## Chat Completion API

### Endpoint

POST https://api.minimax.io/v1/chat/completions
### Response Parsing

MiniMax wraps responses in `<think>...` thinking blocks. The actual JSON payload is **inside** the thinking block, not at the start of the response.

python
import re
import json

def parse_minimax_response(raw: str) -> dict:
    """Extract JSON from MiniMax response with thinking blocks."""
    # Remove thinking blocks
    cleaned = re.sub(r'<think>.*?', '', raw, flags=re.DOTALL).strip()
    
    # Find JSON payload (slides format)
    idx = cleaned.find('{"slides"')
    if idx < 0:
        idx = cleaned.find('"slides"')  # bare list format
    if idx < 0:
        raise ValueError(f"No slides JSON found in response: {raw[:200]}")
    
    return json.loads(cleaned[idx:])
---

## Text-to-Speech (TTS)

### Endpoint

POST https://api.minimax.io/v1/t2a_v2
### Model

Use `speech-2.8-hd` (not the plan identifier — the API model name).

### Headers

python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
### Request Body

python
payload = {
    "model": "speech-2.8-hd",
    "text": "Your speech content here",
    "stream": False
}
---

## Video Generation

### Endpoint

POST https://api.minimax.io/v1/video_generation
### Model

Use `MiniMax-Hailuo-2.3` or the model identifier specified in your plan.

---

## Quick Reference

python
BASE_URL = "https://api.minimax.io"

ENDPOINTS = {
    "chat": f"{BASE_URL}/v1/chat/completions",
    "tts": f"{BASE_URL}/v1/t2a_v2",
    "music": f"{BASE_URL}/v1/music_generation",
    "video": f"{BASE_URL}/v1/video_generation",
}
---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `token plan not support model` | Wrong model identifier | Use API model name, not plan name |
| `1004` auth error | Wrong host | Use `api.minimax.io`, not `api.minimax.chat` |
| `404` | Wrong path | Use `/v1/...`, not `/anthropic/v1/...` |
| Empty response body | Key masked in `.env` | Store key explicitly in script |
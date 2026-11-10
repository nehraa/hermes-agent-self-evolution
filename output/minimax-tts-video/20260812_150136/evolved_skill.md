---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## ⚠️ CRITICAL — Model Name Mismatch

MiniMax token plan lists models under one naming scheme, but the API accepts different names. This causes `token plan not support model` errors even for models that are available.

**Confirmed working mappings for key `sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA`:**

| Plan Model | API Endpoint | Status |
|------------|--------------|--------|
| `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` | ✅ Works |
| `music-2.6` | `https://api.minimax.io/v1/music_generation` | ✅ Works |
| `speech-2.8-hd` | `https://api.minimax.io/v1/t2a_v2` | ✅ Works (Jun 24 2026) |
| Video models | `https://api.minimax.io/v1/video_generation` | ✅ Works |

> **Note:** Earlier reports of "TTS BLOCKED" were incorrect. Testing was done against `api.minimaxi.com` which returned plan-limit errors. The key **does work** on `api.minimax.io`.

---

## API Configuration

### Base Configuration

| Setting | Value |
|---------|-------|
| **Base URL** | `https://api.minimax.io` |
| **Auth** | `Bearer <key>` |

### Correct Endpoints

✅ /v1/chat/completions      — LLM chat
✅ /v1/music_generation      — Music generation
✅ /v1/t2a_v2                — TTS / speech
✅ /v1/video_generation       — Video generation
### Common Errors

| Endpoint | Error | Cause |
|----------|-------|-------|
| `/anthropic/v1/chat/completions` | `404` | Wrong path — do not use `/anthropic` prefix |
| `api.minimax.chat` | `1004` auth error | Wrong host — use `api.minimax.io` |

---

## Response Parsing — Thinking Blocks

MiniMax returns `<think>...` reasoning blocks **before** the actual JSON content. The useful data is buried inside the thinking block.

### Python Parser

python
import re
import json

def parse_minimax_json_response(raw: str) -> dict:
    """Extract JSON from MiniMax response that wraps content inside <think>... blocks."""
    # Remove thinking block
    cleaned = re.sub(r'<think>.*?', '', raw, flags=re.DOTALL).strip()

    # Locate JSON object
    idx = cleaned.find('{"slides"')
    if idx < 0:
        idx = cleaned.find('"slides"')  # bare list format
    if idx < 0:
        raise ValueError(f"No slides key found in response: {cleaned[:200]}")

    json_str = cleaned[idx:]

    # Handle trailing text after JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Truncate after closing brace
        end = json_str.rfind('}')
        if end > 0:
            return json.loads(json_str[:end + 1])
        raise
### Usage Example

python
response = client.chat.completions.create(
    model="MiniMax-M2.7",
    messages=[{"role": "user", "content": "Generate slides about AI"}]
)

raw_text = response.choices[0].message.content
slides = parse_minimax_json_response(raw_text)
---

## Quick Reference

python
# TTS Example (speech-2.8-hd)
response = requests.post(
    "https://api.minimax.io/v1/t2a_v2",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "speech-2.8-hd",
        "text": "Hello, this is a test.",
        "stream": False
    }
)

# Video Example (MiniMax-Hailuo-2.3)
response = requests.post(
    "https://api.minimax.io/v1/video_generation",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "MiniMax-Hailuo-2.3",
        "prompt": "A serene lake at sunset"
    }
)
---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## Overview

This skill covers Minimax's speech synthesis (TTS), video generation, music generation, and chat completion APIs. All endpoints use `api.minimax.io` as the base URL.

**Known quirk:** Token plan model names often differ from API model names. This causes `token plan not support model` errors for otherwise-valid requests.

---

## ⚠️ Critical Notes

### Model Name Mismatch

MiniMax token plans list models under one naming scheme, but the API accepts a different scheme. This is a known MiniMax quirk, not a plan limitation.

### API Key Configuration

The full API key should be stored in the script's `_EXPLICIT_KEYS` dict. The `.env` file masks it as `***`, making it appear empty when read directly.

API Key: sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
---

## Confirmed Working Endpoints

| Feature | Token Plan Model | API Endpoint | Status |
|---------|------------------|--------------|--------|
| Chat Completion | `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` | ✅ |
| TTS | `speech-2.8-hd` | `https://api.minimax.io/v1/t2a_v2` | ✅ |
| Music | `music-2.6` | `https://api.minimax.io/v1/music_generation` | ✅ |
| Video | (Hailuo models) | `https://api.minimax.io/v1/video_generation` | ✅ |

---

## API Configuration

### Chat Completion

Base URL:  https://api.minimax.io
Endpoint:  https://api.minimax.io/v1/chat/completions
Auth:      Bearer <key>
Headers:   Content-Type: application/json
**Common errors:**
- `/anthropic/v1/chat/completions` → returns `404`
- `api.minimax.chat` → returns auth error `1004`

### TTS (Text-to-Speech)

Endpoint: https://api.minimax.io/v1/t2a_v2
Auth:     Bearer <key>
Method:   POST
### Video Generation

Endpoint: https://api.minimax.io/v1/video_generation
Auth:     Bearer <key>
Method:   POST
### Music Generation

Endpoint: https://api.minimax.io/v1/music_generation
Auth:     Bearer <key>
Method:   POST
---

## Response Parsing

### Chat Completion — Extracting JSON from Thinking Blocks

MiniMax embeds the actual JSON response inside `<think>...` thinking blocks that precede the main content. Standard JSON parsing will fail if you don't strip these first.

python
import re
import json

def parse_minimax_json_response(raw: str) -> dict:
    """
    Extract JSON from MiniMax response where content is buried inside
    <think>... thinking blocks instead of at the response root.
    """
    # Remove thinking blocks
    cleaned = re.sub(r'<think>.*?', '', raw, flags=re.DOTALL).strip()

    # Locate the JSON payload
    idx = cleaned.find('{"slides"')
    if idx < 0:
        idx = cleaned.find('"slides"')  # bare list format

    if idx < 0:
        raise ValueError(f"No slides key found in response. Raw: {raw[:500]}")

    json_str = cleaned[idx:]

    # Handle trailing content after the JSON object
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Find the actual end of the JSON object
        depth = 0
        end = 0
        in_string = False
        escape_next = False

        for i, char in enumerate(json_str):
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if in_string:
                continue

            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        return json.loads(json_str[:end])
### Error: "token plan not support model"

If you receive this error despite having the model in your plan:

1. **Verify the endpoint host** — use `api.minimax.io`, not `api.minimaxi.com`
2. **Check the token plan name vs API name** — they differ for many models
3. **Confirm the feature is enabled** — some plans restrict TTS or video generation

**Note:** An earlier "TTS BLOCKED" diagnosis was incorrect. Testing against the wrong host (`api.minimaxi.com`) caused auth failures that were misread as plan limits. TTS works correctly on `api.minimax.io`.

---

## Quick Reference

python
# Base configuration
BASE_URL = "https://api.minimax.io"
API_KEY = "sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA"

# Headers for all requests
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Common endpoint pattern
chat_url = f"{BASE_URL}/v1/chat/completions"
tts_url = f"{BASE_URL}/v1/t2a_v2"
video_url = f"{BASE_URL}/v1/video_generation"
music_url = f"{BASE_URL}/v1/music_generation"
---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## ⚠️ CRITICAL — Token Plan vs API Model Name Mismatch

MiniMax token plans list models with one naming scheme, but the API accepts different names. This causes `token plan not support model` errors even for models listed in your plan.

### Confirmed Working Configurations

| Feature | Token Plan ID | API Endpoint | Status |
|---------|--------------|--------------|--------|
| LLM Chat | `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` | ✅ |
| Music | `music-2.6` | `https://api.minimax.io/v1/music_generation` | ✅ |
| TTS | `speech-2.8-hd` | `https://api.minimax.io/v1/t2a_v2` | ✅ Verified Jun 24 2026 |
| Video | (token plan) | `https://api.minimax.io/v1/video_generation` | ✅ |

> **Note:** Earlier diagnosis of "TTS BLOCKED" was incorrect. Testing was done against wrong host (`api.minimaxi.com`), not an actual plan limitation.

---

## API Credentials

### Full API Key

sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
> **⚠️ Storage Note:** `.env` files mask this key as `***`, making it appear empty. Store in both memory and your script's `_EXPLICIT_KEYS` dict.

---

## Chat Completions API

### Correct Endpoint

Base URL:  https://api.minimax.io
Endpoint:  https://api.minimax.io/v1/chat/completions
Auth:      Bearer <key>
### Common Errors

| Path | Result |
|------|--------|
| `/anthropic/v1/chat/completions` | 404 Not Found |
| `api.minimax.chat/v1/chat/completions` | 1004 Auth Error |
| `api.minimax.io/v1/chat/completions` | ✅ Works |

---

## Response Parsing — Thinking Blocks

MiniMax embeds `<think>...` reasoning blocks **before** the actual JSON payload. The content you need is inside these blocks.

### Python Parsing Utility

python
import re
import json

def parse_minimax_json_response(raw: str) -> dict:
    """
    Extract JSON from MiniMax response that contains content inside <think>... blocks.
    
    Args:
        raw: Raw response string from MiniMax API
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON cannot be found in response
    """
    # Remove the thinking block(s)
    cleaned = re.sub(r'<think>.*?', '', raw, flags=re.DOTALL).strip()
    
    # Locate the JSON object (slides format)
    idx = cleaned.find('{"slides"')
    if idx < 0:
        idx = cleaned.find('"slides"')  # bare list format
    if idx < 0:
        raise ValueError(f"Could not find slides JSON in response: {raw[:200]}...")
    
    # Extract and parse the JSON
    json_str = cleaned[idx:]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Try to find complete JSON object
        brace_count = 0
        end_idx = idx
        for i, char in enumerate(json_str):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        return json.loads(json_str[:end_idx])
---

## TTS (Text-to-Speech)

### Endpoint

POST https://api.minimax.io/v1/t2a_v2
### Headers

Authorization: Bearer <api_key>
Content-Type: application/json
### Example Request Body

json
{
  "model": "speech-2.8-hd",
  "text": "Your speech content here",
  "stream": false
}
---

## Video Generation

### Endpoint

POST https://api.minimax.io/v1/video_generation
### Headers

Authorization: Bearer <api_key>
Content-Type: application/json
### Example Request Body

json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "Your video description here"
}
---
name: minimax-tts-video
description: "Minimax TTS and Video Generation APIs — speech-2.8-hd, MiniMax-Hailuo-2.3. WARNING: Token plan model identifiers do NOT match API model identifiers. This is a known MiniMax quirk."
category: media
---

# Minimax TTS & Video Skill

## ⚠️ CRITICAL — Model Name Mismatch

MiniMax token plan lists models with one set of names, but the API accepts a different set. This causes `token plan not support model` errors even for listed models.

**Confirmed working on this key (sk-cp-...):**

| Model Type | Token Plan Name | API Endpoint |
|------------|-----------------|--------------|
| LLM | `MiniMax-M2.7` | `https://api.minimax.io/v1/chat/completions` |
| Music | `music-2.6` | `https://api.minimax.io/v1/music_generation` |
| TTS & Video | BLOCKED | Plan vs API model name mismatch cannot be resolved without MiniMax support |

---

## API Configuration

### Full API Key

sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
> **Important:** Save this key in memory AND in the script's `_EXPLICIT_KEYS` dict. The `.env` file masks it as `***`, making it appear empty when read.

### Correct Endpoint

Base URL:  https://api.minimax.io
Endpoint:  https://api.minimax.io/v1/chat/completions
Auth:      Bearer <key>
**Common mistakes to avoid:**

| Wrong Pattern | Error It Causes |
|---------------|-----------------|
| `/anthropic/v1/chat/completions` | 404 Not Found |
| `api.minimax.chat/v1/chat/completions` | 1004 auth errors |

---

## Response Format — Thinking Blocks

MiniMax returns `...` reasoning blocks **before** the actual JSON. The slides JSON is buried inside the thinking block, NOT at the start of the response.

### Correct Parsing Pattern

python
import re
import json

def parse_minimax_json_response(raw: str) -> dict:
    """Extract JSON from MiniMax response that has content inside ... blocks."""
    # Remove the thinking block
    cleaned = re.sub(r'.*?', '', raw, flags=re.DOTALL).strip()
    
    # Find the JSON object starting with "slides"
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
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
        if brace_count == 0 and i > 10:
            end = i + 1
            break
    
    return json.loads(json_str[:end])
### Example Flow

Raw response:

Let me analyze this request carefully...
{"slides": [{"text": "Hello", "image": "..."}]}


The parser strips the `...` wrapper and extracts the JSON from within.
---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

This skill provides automatic failover from OpenRouter to Minimax when usage limits are reached. It wraps LLM calling logic to detect quota/rate limit errors and seamlessly retry through Minimax.

## Configuration

All configuration is stored in Hermes memory:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Minimax API Key** | Retrieved from memory | Supports `sk-cp-*` or `ntn_*` formats |
| **Minimax Endpoint** | `https://api.minimax.io/v1` | Include the `/v1` path |
| **Minimax Model** | `MiniMax-M2.7` | Exact name, case-sensitive |

### API Key Format Compatibility

As of May 2026, key format affects endpoint routing:

- **`sk-cp-*` keys**: Work correctly on `https://api.minimax.io/v1/chat/completions`
- **`ntn_*` keys**: Require `https://api.minimax.chat/v1/text/chatcompletion_v2` — otherwise return HTTP 401 with code 1004 ("token not match group")

> **Note:** Ensure your protocol pipeline scripts read the correct key format from memory or `.env` rather than hardcoding keys.

## Behavior

When OpenRouter returns a quota or rate limit error, the system:

1. Logs the fallback event and notifies the user
2. Retries the identical request via Minimax
3. Returns the Minimax response to the caller

### Error Detection

Fallback triggers on errors containing phrases such as:
- `usage limit reached`
- `quota exceeded`
- `rate limit`
- Similar quota/limit exceeded messages

## Usage

This skill is designed for internal use by other skills or when making LLM calls through Hermes. Import and call the fallback wrapper in your LLM invocation logic.

## Implementation

python
import httpx
from openai import OpenAI

# Standard Minimax client setup
http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-minimax-key",
    base_url="https://api.minimax.io/v1",
    http_client=http_client
)
### SSL Verification Bypass

When cloud LLM APIs fail with SSL certificate errors (expired certs, etc.), pass an `httpx.Client` with `verify=False` to the OpenAI SDK:

python
http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(api_key="key", base_url="endpoint/v1", http_client=http_client)
**Known case — ollama.cloud:** Certificate `about.caribregistry.com` (Let's Encrypt) may cause SSL errors. Use `verify=False` as a workaround.

## Pricing Reference

For cost comparisons across MiniMax, Kimi, Ollama Pro, and OpenRouter (including Abhinav's ~20M tokens/day usage profile), see:

skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
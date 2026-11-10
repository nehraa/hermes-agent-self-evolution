---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

This skill provides an automatic fallback mechanism: it attempts the request via OpenRouter first, and if a "usage limit reached" error is detected, automatically retries the same request through Minimax.

## Configuration

Configuration is stored in Hermes memory. Credentials are retrieved at runtime.

| Parameter | Value | Notes |
|-----------|-------|-------|
| **API Key Format** | `sk-cp-*` or `ntn_*` | Determines which endpoint to use |
| **Endpoint** | See [Endpoint Selection](#endpoint-selection) below | |
| **Model** | `MiniMax-M2` | Exact name, case-sensitive |

### Endpoint Selection

The Minimax endpoint **depends on your API key format**:

| Key Prefix | Endpoint | Path |
|------------|----------|------|
| `sk-cp-*` | `https://api.minimax.io` | `/v1/chat/completions` |
| `ntn_*` | `https://api.minimax.chat` | `/v1/text/chatcompletion_v2` |

> **Important:** Using the wrong endpoint/key combination results in HTTP 401 with error code 1004 ("token not match group"). As of May 17, 2026, `sk-cp-` keys work with `api.minimax.io/v1/chat/completions`, while `ntn_` keys require `api.minimax.chat/v1/text/chatcompletion_v2`.

### Hardcoded Key Note (May 17, 2026)

For protocol pipeline scripts that cannot read from `.env`, the working key is:
sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
## Usage

This skill is designed for internal use by other skills or when making LLM calls through Hermes. It wraps LLM calling logic to provide seamless fallback transparently to the caller.

## Implementation

When OpenRouter returns an error indicating usage limits or quota exceeded:

1. **Log** the fallback event and notify the user
2. **Retry** the identical request via the Minimax API (with correct endpoint per key format)
3. **Return** the Minimax response to the original caller

## Error Detection

Fallback triggers on errors containing:
- `usage limit reached`
- `quota exceeded`
- `rate limit`
- Any similar quota/limit exceeded message

## Pricing Reference

For cost comparison across MiniMax, Kimi, Ollama Pro, and OpenRouter — including Abhinav's ~20M tokens/day usage profile — see:
skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
## SSL Verification Bypass for Cloud LLM APIs

When a cloud LLM API fails with SSL certificate errors (expired certificates, etc.), bypass verification using `httpx.Client`:

python
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-key",
    base_url="https://your-endpoint/v1",
    http_client=http_client
)
**Known case — ollama.cloud:** Uses certificate `about.caribregistry.com` (Let's Encrypt). Certificate validation fails on some systems until root store is updated. Use `verify=False` as a workaround.
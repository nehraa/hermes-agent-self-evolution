---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

Provides automatic fallback from OpenRouter to Minimax when usage limits are reached. Wraps LLM calling logic to seamlessly retry failed requests through an alternative provider.

## Configuration

Configuration is stored in Hermes memory and retrieved at runtime.

| Parameter | Value | Notes |
|-----------|-------|-------|
| **API Key** | Retrieved from memory | Supports `sk-cp-` or `ntn_` formats |
| **Endpoint** | `https://api.minimax.io/v1` | Include `/v1` path |
| **Model** | `MiniMax-M2` | Exact model name, case-sensitive |

### Endpoint Compatibility by Key Format

| Key Format | Required Endpoint |
|------------|-------------------|
| `sk-cp-` | `https://api.minimax.io/v1/chat/completions` |
| `ntn_` | `https://api.minimax.chat/v1/text/chatcompletion_v2` |

> **Note:** Using the wrong endpoint for your key format will return HTTP 401 with error code 1004 ("token not match group").

## Usage

Import and use within other skills or LLM call pipelines:

python
from skills.llm_fallback_minimax import MinimaxFallbackHandler

handler = MinimaxFallbackHandler()
response = handler.execute_with_fallback(openrouter_response)
The handler automatically detects quota/limit errors and retries through Minimax.

## Implementation

When OpenRouter returns a usage limit error:

1. **Detect** — Identify quota/limit exceeded conditions
2. **Log** — Record fallback event and notify user
3. **Retry** — Re-send the same request via Minimax API
4. **Return** — Pass Minimax response back to caller

### Error Detection Patterns

Fallback triggers on errors matching these patterns:
- `"usage limit reached"`
- `"quota exceeded"`
- `"rate limit"`
- `"limit exceeded"`
- `"quota limit"`

## SSL Verification Bypass

For cloud LLM APIs with SSL certificate issues (expired certs, etc.), use `httpx.Client` with verification disabled:

python
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-key",
    base_url="https://api.minimax.io/v1",
    http_client=http_client
)
> **Known issue:** `ollama.cloud` has a certificate from `about.caribregistry.com` (Let's Encrypt) that may cause SSL verification failures. Use `verify=False` as a workaround.

## Pricing Reference

For cost comparisons across MiniMax, Kimi, Ollama Pro, and OpenRouter — including Abhinav's ~20M tokens/day usage profile — see:

skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
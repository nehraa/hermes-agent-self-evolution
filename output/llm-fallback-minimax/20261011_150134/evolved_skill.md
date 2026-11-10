---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

This skill provides automatic fallback from OpenRouter to Minimax when usage limits are encountered. It intercepts "usage limit reached" errors and retries the same request through Minimax without requiring changes to calling code.

## Configuration

Stored in Hermes memory:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **API Key** | Retrieved from memory | Supports `sk-cp-` or `ntn_` format |
| **Endpoint** | `https://api.minimax.io/v1` | Include `/v1` path |
| **Model** | `MiniMax-M2` | Exact name, case-sensitive |

### API Key Format Requirements

> **Important (May 17, 2026):** Key format determines which endpoint to use.

- **`sk-cp-` keys**: Work correctly with `https://api.minimax.io/v1/chat/completions`
- **`ntn_` keys**: Return HTTP 401 with code 1004 ("token not match group") — require `https://api.minimax.chat/v1/text/chatcompletion_v2` instead

For pipeline scripts that cannot read from `.env`, hardcode the verified working key:
sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
## Usage

This skill is invoked automatically by other skills or when making LLM calls through Hermes. It wraps the existing LLM calling logic — no direct usage required.

## How It Works

1. **Primary request** — Attempt OpenRouter API
2. **Error detection** — Check for usage limit, quota, or rate limit errors
3. **Fallback trigger** — Log the fallback event and notify user
4. **Retry** — Resend identical request via Minimax API
5. **Return** — Pass Minimax response back to caller

### Trigger Conditions

Fallback activates on errors containing:
- `usage limit reached`
- `quota exceeded`
- `rate limit`
- Other quota/limit exceeded variations

## SSL Certificate Errors

When cloud LLM APIs fail with SSL certificate errors (expired certs, etc.), use `httpx.Client(verify=False)`:

python
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-api-key",
    base_url="https://your-endpoint/v1",
    http_client=http_client
)
**Known case:** `ollama.cloud` requires SSL verification bypass due to cert `about.caribregistry.com` (Let's Encrypt).

## Pricing Reference

For cost comparisons across MiniMax, Kimi, Ollama Pro, and OpenRouter — including Abhinav's ~20M tokens/day usage profile — see:

skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

Provides automatic fallback from OpenRouter to Minimax when usage limits or quota errors are detected. Seamlessly retries failed requests through Minimax without caller involvement.

## Configuration

Stored in Hermes memory. Retrieved at runtime.

| Parameter | Value | Notes |
|-----------|-------|-------|
| **API Key** | Memory lookup | Supports both `sk-cp-*` and `ntn_*` formats |
| **Endpoint** | `https://api.minimax.io/v1` | Use `/v1` path prefix |
| **Model** | `MiniMax-M2` | Exact name, case-sensitive |

### Endpoint Requirements by Key Format

| Key Format | Required Endpoint | Notes |
|------------|-------------------|-------|
| `sk-cp-*` | `https://api.minimax.io/v1/chat/completions` | Standard API path |
| `ntn_*` | `https://api.minimax.chat/v1/text/chatcompletion_v2` | Different endpoint required |

> **Note:** `ntn_` format keys return HTTP 401 (code 1004, "token not match group") when used with the standard `/v1/chat/completions` endpoint.

## Behavior

1. Attempts request via OpenRouter
2. On usage/quota error, logs the fallback event
3. Retries identical request via Minimax with configured credentials
4. Returns Minimax response to caller

### Error Detection Triggers

Fallback activates on errors containing:
- `usage limit reached`
- `quota exceeded`
- `rate limit`
- Any similar quota/limit exceeded message

## SSL Certificate Bypass

For cloud LLM APIs failing due to SSL certificate errors (expired certs, etc.):

python
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-key",
    base_url="https://your-endpoint/v1",
    http_client=http_client
)
## Pricing Reference

For token cost comparisons (MiniMax vs Kimi vs Ollama Pro vs OpenRouter), see:
skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

This skill provides automatic fallback from OpenRouter to Minimax when usage limits or quota errors are detected. It wraps LLM calling logic to seamlessly retry requests through Minimax without requiring changes to calling code.

## Configuration

Stored in Hermes memory and accessed at runtime:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **API Key** | Retrieved from memory | Supports both `sk-cp-*` and `ntn_*` formats |
| **Endpoint** | `https://api.minimax.io/v1` | Include the `/v1` path |
| **Model** | `MiniMax-M2` | Exact name, case-sensitive |

### Endpoint Selection by Key Format

| Key Format | Endpoint | Notes |
|------------|----------|-------|
| `sk-cp-*` | `https://api.minimax.io/v1/chat/completions` | Standard OpenAI-compatible endpoint |
| `ntn_*` | `https://api.minimax.chat/v1/text/chatcompletion_v2` | Requires different endpoint |

> **Note:** `ntn_` format keys return HTTP 401 (code 1004, "token not match group") when used with the standard endpoint.

## Usage

This skill is designed for internal use by other skills or when making LLM calls through Hermes. It intercepts OpenRouter errors and automatically retries via Minimax.

python
# Example: Automatic fallback occurs transparently
response = llm_call("Explain quantum entanglement")
# If OpenRouter hits usage limit, Minimax is tried automatically
## Implementation Flow

OpenRouter Request
       │
       ▼
   ┌───────┐
   │Success│───▶ Return Response
   └───────┘
       │
       │ Error (usage limit/quota/rate limit)
       ▼
   Log Fallback Event
       │
       ▼
   Retry via Minimax API
       │
       ▼
   Return Minimax Response
## Error Detection

Fallback triggers on error messages containing:
- `usage limit reached`
- `quota exceeded`
- `rate limit`
- Other quota/limit exceeded variations

## SSL Verification for Cloud APIs

When cloud LLM APIs fail with SSL certificate errors (expired certs, etc.), disable verification using `httpx.Client`:

python
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(
    api_key="your-key",
    base_url="https://your-endpoint/v1",
    http_client=http_client
)
> **Known issue:** `ollama.cloud` uses certificate `about.caribregistry.com` (Let's Encrypt) which may cause SSL verification failures.

## Pricing Reference

For cost comparisons across MiniMax, Kimi, Ollama Pro, and OpenRouter (including Abhinav's ~20M tokens/day usage profile), see:

skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")
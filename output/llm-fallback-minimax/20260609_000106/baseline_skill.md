---
name: llm-fallback-minimax
description: Automatic fallback from OpenRouter to Minimax when usage limits are reached
category: llm
---

# LLM Fallback to Minimax

This skill provides an automatic fallback mechanism that tries OpenRouter first, and if it detects a "usage limit reached" error, automatically retries the request through Minimax with the configured API key, endpoint, and model.

## Configuration (stored in Hermes memory)
- **Minimax API Key**: Retrieved from memory (either `sk-cp-` or `ntn_` format)
- **Minimax Endpoint**: `https://api.minimax.io/v1` (include `/v1` path)
- **Minimax Model**: `MiniMax-M2.7` (exact model name, case-sensitive)

**IMPORTANT (May 17, 2026):** `sk-cp-` format keys work correctly on `https://api.minimax.io/v1/chat/completions`. `ntn_` format keys return HTTP 401 with code 1004 ("token not match group") on that endpoint — they require `api.minimax.chat/v1/text/chatcompletion_v2`. The earlier note claiming both fail was incorrect. The working key as of May 17 is `sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA` — hardcode in protocol pipeline scripts that can't read from `.env`.

## Usage
This skill is designed to be used internally by other skills or when making LLM calls through Hermes. It wraps the LLM calling logic to provide seamless fallback.

## Implementation Details
When OpenRouter returns an error indicating usage limits/quota exceeded, the system:
1. Logs the fallback event (notifies user)
2. Retries the same request via Minimax API
3. Returns the Minimax response to the caller

## Pricing Reference

For current LLM model cost comparison (MiniMax vs Kimi vs Ollama Pro vs OpenRouter) including Abhinav's ~20M tokens/day usage profile, see:
- `skill_view("llm-fallback-minimax", file_path="references/llm-model-pricing.md")`

## Error Detection
The fallback triggers on errors containing phrases like:
- "usage limit reached"
- "quota exceeded"
- "rate limit"
- Similar quota/limit exceeded messages

## SSL Verification Bypass for Cloud LLM APIs

When a cloud LLM API fails with SSL cert errors (expired certificates, etc.), use `httpx.Client(verify=False)` with the OpenAI SDK:

```python
import httpx
from openai import OpenAI
http_client = httpx.Client(verify=False, timeout=60.0)
client = OpenAI(api_key="key", base_url="https://endpoint/v1", http_client=http_client)
```

**Known case: ollama.cloud** — cert `about.caribregistry.com` (Let's Encrypt E8) expired. `deepseek-v4-flash:cloud` (158B) requires Pro subscription ($20/mo). Free tier only gets light usage. See `references/ssl-cert-bypass.md` for full details.

## References
- `references/provider-oauth-vs-apikey.md` — OAuth vs API key auth patterns for cloud LLM providers
- `references/llm-model-pricing.md` — Cost comparison for MiniMax vs Ollama Pro vs OpenRouter
- `references/ssl-cert-bypass.md` — SSL cert bypass for ollama.cloud (expired cert), patching OpenAI SDK clients, ollama.cloud Pro subscription requirement

## Logging
Each time a fallback to Minimax occurs, a notification is sent to the user so they are aware of the switch.
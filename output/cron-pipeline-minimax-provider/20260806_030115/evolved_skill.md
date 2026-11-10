---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

All cron-spawned pipeline scripts must use MiniMax exclusively for text generation, image generation, and TTS. No OpenRouter, no fallback providers.

## Root Cause

Two bugs cause cron pipeline failures:

1. **Hermes cron scheduler does not source `~/.hermes/.env`** — spawned scripts receive an empty `MINIMAX_API_KEY` environment variable, causing `401` or `2049 invalid api key` errors.

2. **OpenRouter free tier (50 calls/day) exhausts instantly** — the "MiniMax primary, OpenRouter fallback" pattern burns through the daily quota within minutes of any MiniMax transient failure (e.g., Aug 3 newspaper cron hit `HTTP 429: Token Plan usage limit reached`).

## Rules

| Rule | Rationale |
|------|-----------|
| MiniMax is the **sole provider** | Text, image, and TTS all route through `api.minimax.io` with the `sk-cp-…` key |
| OpenRouter is **never a fallback** | If MiniMax fails, the pipeline fails loudly and stops |
| Script **self-loads** the `.env` file | Cron may not source env vars; the script must load them directly |
| Cron prompt also **pre-sources** the env | Defense-in-depth if the script loader fails |

## Required: Self-Loading Env Loader

Paste this at the **top** of any cron-spawned pipeline script, **before** the API key constant is read:

python
import os
from pathlib import Path

def _load_minimax_key():
    """Load MINIMAX_API_KEY from ~/.hermes/.env if not already in environment."""
    global MINIMAX_API_KEY
    if os.environ.get("MINIMAX_API_KEY"):
        MINIMAX_API_KEY = os.environ["MINIMAX_API_KEY"]
        return
    
    env_paths = [
        Path.home() / ".hermes" / ".env",
        Path.home() / ".env",
        Path("/home/Hermes/OpenMAIC/core/.env.local"),
    ]
    
    for env_path in env_paths:
        if not env_path.exists():
            continue
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                if key.strip() == "MINIMAX_API_KEY":
                    MINIMAX_API_KEY = value.strip().strip('"').strip("'")
                    return
    
    raise RuntimeError("MINIMAX_API_KEY not found in environment or any .env file")

MINIMAX_API_KEY = ""  # placeholder
_load_minimax_key()
## Cron Entry Template

bash
MAILTO=""
BASH_ENV="$HOME/.hermes/.env"

0 6 * * * /bin/bash -c 'source $HOME/.hermes/.env 2>/dev/null; /usr/bin/python3 /path/to/pipeline.py'
## Checklist for New Cron Scripts

- [ ] Script calls `_load_minimax_key()` before any API usage
- [ ] `MINIMAX_API_KEY` constant reads from `os.environ["MINIMAX_API_KEY"]`
- [ ] No `openrouter`, `pollinations`, or `freegen` imports
- [ ] No fallback logic that retries with a different provider
- [ ] Errors propagate (do not silently catch and retry)
---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

All cron-spawned pipeline scripts MUST use MiniMax exclusively for text, image, and TTS generation. OpenRouter is never a fallback.

## Why This Rule Exists

### Problem 1: Cron Does Not Source Environment Files

The Hermes cron scheduler spawns scripts without loading `~/.hermes/.env`. When the script calls `os.environ.get("MINIMAX_API_KEY")`, it returns empty. The script either:

- Falls back to a stale hardcoded key → fails with `401 / 2049 invalid api key`
- Crashes immediately

**Fix:** Scripts must self-load the `.env` file (see Canonical Loader below).

### Problem 2: OpenRouter Free Tier Burns Out

The previous "MiniMax primary, OpenRouter fallback" pattern failed because:

- OpenRouter free tier = 50 calls/day
- A single MiniMax blip triggers immediate fallback
- All 50 OpenRouter calls exhaust in minutes
- Pipeline stops with `HTTP 429: Token Plan usage limit reached (2056)`

**Fix:** If MiniMax fails, fail loudly and stop. Never cascade to OpenRouter, Pollinations, freegen, or any other provider.

## Rules for All Cron/Recurring Pipeline Scripts

1. **MiniMax is the sole provider** — text + image + TTS all use the `sk-cp-…` key against `api.minimax.io`
2. **OpenRouter is never a fallback** — hard fail on MiniMax errors
3. **Script self-loads `~/.hermes/.env`** — don't rely on cron shell configuration
4. **Cron prompt also pre-sources env** — defensive layer in case script loader breaks

## Canonical Environment Loader

Place this at the very top of any cron-spawned pipeline script, before any API key constants are referenced:

python
import os
from pathlib import Path

def _load_minimax_env():
    """Load MINIMAX_API_KEY from ~/.hermes/.env if not already in environment."""
    if os.environ.get("MINIMAX_API_KEY"):
        return  # Already loaded
    
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
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() == "MINIMAX_API_KEY":
                os.environ["MINIMAX_API_KEY"] = value.strip().strip('"').strip("'")
                return

# Execute immediately on module load
_load_minimax_env()
## Usage Example

python
import os
from pathlib import Path

# === Loader (must be first) ===
def _load_minimax_env():
    if os.environ.get("MINIMAX_API_KEY"):
        return
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("MINIMAX_API_KEY="):
                _, _, value = line.partition("=")
                os.environ["MINIMAX_API_KEY"] = value.strip().strip('"').strip("'")

_load_minimax_env()

# === Now safe to reference ===
MINIMAX_KEY = os.environ["MINIMAX_API_KEY"]
# ... rest of pipeline ...
## Cron Configuration Template

bash
# In crontab -e
# Pre-source env as defensive layer (belt-and-suspenders)
0 6 * * * cd /path/to/hermes && . /home/hermes/.hermes/.env && /usr/bin/python3 /path/to/pipeline.py

# Or inline:
0 6 * * * MINIMAX_API_KEY=$(grep MINIMAX_API_KEY ~/.hermes/.env | cut -d= -f2) /usr/bin/python3 /path/to/pipeline.py
## Error Handling

When MiniMax fails, the script MUST:

- Log the full error (status code, response body)
- Exit with non-zero code
- NOT attempt any alternative provider

python
def call_minimax(endpoint: str, payload: dict) -> dict:
    response = requests.post(endpoint, json=payload, headers={
        "Authorization": f"Bearer {os.environ['MINIMAX_API_KEY']}"
    })
    if response.status_code != 200:
        raise RuntimeError(
            f"MiniMax API failed: {response.status_code} - {response.text}"
        )
    return response.json()
## Verification Checklist

Before deploying a cron pipeline:

- [ ] Script contains `_load_minimax_env()` and calls it before any key reference
- [ ] No OpenRouter imports or client initialization
- [ ] No "fallback" or "try-again" logic to alternative providers
- [ ] Cron job command includes env pre-sourcing
- [ ] Test runs successfully with `MINIMAX_API_KEY` unset before script runs
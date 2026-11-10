---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

All cron-spawned pipeline scripts must use **MiniMax exclusively** for text generation, image generation, and TTS. No OpenRouter, no Pollinations, no freegen fallbacks.

## Why This Rule Exists

Two bugs broke the previous architecture:

1. **Hermes cron does not source `~/.hermes/.env` before spawning scripts.** When the script calls `os.environ.get("MINIMAX_API_KEY")`, it returns empty. The script either hits a stale hardcoded fallback or fails with `401 / 2049 invalid api key`.

2. **OpenRouter's free tier is 50 calls/day.** The "MiniMax primary, OpenRouter fallback" pattern exhausted this limit within minutes whenever MiniMax had any transient blip. The Aug 3 newspaper cron hit `HTTP 429: Token Plan usage limit reached (2056)` and the pipeline stopped.

## Rules for Any Cron / Recurring Pipeline Script

| Rule | Reason |
|------|--------|
| **MiniMax is the sole provider** | Text, image, and TTS all use the `sk-cp-…` key against `api.minimax.io` |
| **OpenRouter is never a fallback** | If MiniMax fails, fail immediately and alert. Never cascade to OpenRouter, Pollinations, or freegen |
| **Script self-loads `~/.hermes/.env`** | Don't rely on the cron shell to pre-source the env file. Load it inside the script so it works regardless of cron configuration |
| **Cron prompt also pre-sources env** | Defense-in-depth in case the script's loader breaks |

## Canonical Self-Loader

Place this at the top of any cron-spawned pipeline script, **before** any API key is read:

python
import os
from pathlib import Path

def _load_minimax_key():
    """Load MINIMAX_API_KEY from ~/.hermes/.env if not already in environment."""
    global MINIMAX_KEY
    if os.environ.get("MINIMAX_API_KEY"):
        MINIMAX_KEY = os.environ["MINIMAX_API_KEY"]
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
                    MINIMAX_KEY = value.strip().strip('"').strip("'")
                    return

    raise RuntimeError(
        "MINIMAX_API_KEY not found in environment or any .env file. "
        "Ensure ~/.hermes/.env exists and contains MINIMAX_API_KEY=sk-cp-..."
    )
## Cron Entry Pattern

bash
# In crontab -e
0 6 * * * cd /home/Hermes/OpenMAIC/core && . /home/Hermes/.hermes/.env && python newspaper_cron.py >> /var/log/hermes/newspaper.log 2>&1
Or use a wrapper script:

bash
#!/bin/bash
set -euo pipefail
source ~/.hermes/.env
cd /home/Hermes/OpenMAIC/core
python "$@"
## What NOT To Do

python
# ❌ WRONG — cascade to OpenRouter on MiniMax failure
try:
    result = minimax_generate(prompt)
except Exception:
    result = openrouter_generate(prompt)  # NEVER do this in cron

# ❌ WRONG — rely on environment being pre-sourced
api_key = os.environ["MINIMAX_API_KEY"]  # Will be empty under cron

# ✅ CORRECT — self-load and fail loudly
_load_minimax_key()
result = minimax_generate(prompt)  # Fails immediately if key is bad
## Checklist Before Deploying a New Cron Pipeline

- [ ] Script contains `_load_minimax_key()` and calls it before using any API
- [ ] `~/.hermes/.env` exists and contains `MINIMAX_API_KEY=sk-cp-...`
- [ ] No OpenRouter, Pollinations, or freegen imports or calls
- [ ] Script has try/except that re-raises instead of cascading
- [ ] Cron entry logs output to a file with `>> /var/log/... 2>&1`
---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

This skill enforces **MiniMax as the exclusive provider** for all text, image, and TTS generation in cron-spawned pipelines. OpenRouter is explicitly prohibited as a fallback.

## Background

Two bugs historically broke cron pipelines:

1. **Missing environment** — The Hermes cron scheduler does not source `~/.hermes/.env` before spawning scripts. API key lookups return empty, causing `401 / 2049 invalid api key` errors.
2. **OpenRouter exhaustion** — The previous "MiniMax primary, OpenRouter fallback" pattern consumed OpenRouter's free tier (50 calls/day) within minutes whenever MiniMax had transient issues. The Aug 3 newspaper cron hit `HTTP 429: Token Plan usage limit reached (2056)` and halted.

## Rules

| Requirement | Implementation |
|-------------|----------------|
| **MiniMax only** | All text, image, and TTS calls use the `sk-cp-…` key against `api.minimax.io` |
| **No fallbacks** | If MiniMax fails, the pipeline fails immediately. Never cascade to OpenRouter, Pollinations, freegen, or any other provider |
| **Self-load env** | Scripts must load `~/.hermes/.env` internally — do not rely on cron to pre-source it |
| **Defensive cron prompt** | The cron prompt also pre-sources the env file as a backup layer |

## Canonical Self-Loader

Place this **at the very top** of any cron-spawned pipeline script, before any API key constant is defined:

python
import os
from pathlib import Path

MINIMAX_KEY: str | None = None

def _load_minimax_key() -> str:
    """Load MiniMax API key from environment or .env files."""
    global MINIMAX_KEY

    # Check environment first
    if os.environ.get("MINIMAX_API_KEY"):
        MINIMAX_KEY = os.environ["MINIMAX_API_KEY"]
        return MINIMAX_KEY

    # Fallback: scan common .env locations
    candidates = [
        Path.home() / ".hermes" / ".env",
        Path.home() / ".env",
        Path("/home/Hermes/OpenMAIC/core/.env.local"),
    ]

    for env_path in candidates:
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
                MINIMAX_KEY = value.strip().strip('"').strip("'")
                return MINIMAX_KEY

    raise RuntimeError(
        "MINIMAX_API_KEY not found in environment or .env files. "
        "Ensure ~/.hermes/.env contains: MINIMAX_API_KEY=sk-cp-..."
    )

# Initialize immediately
_load_minimax_key()
## Cron Entry Format

Always source the env file in the cron command:

cron
MINIMAX_KEY=$(grep MINIMAX_API_KEY ~/.hermes/.env | cut -d'=' -f2) && \
*/15 * * * * cd /path/to/project && python -c "from pathlib import Path; [exec(l) for l in Path('/home/Hermes/.hermes/.env').read_text().splitlines() if '=' in l and not l.startswith('#')] && python pipeline.py"
Or use a wrapper script:

bash
#!/bin/bash
# /usr/local/bin/run-pipeline.sh
source ~/.hermes/.env
cd /path/to/project
python pipeline.py
## Anti-Patterns (Do Not Use)

python
# ❌ WRONG — cascading fallback
if not minimax_response:
    return openrouter_fallback()

# ❌ WRONG — missing self-loader
MINIMAX_KEY = os.environ["MINIMAX_API_KEY"]  # fails in cron

# ❌ WRONG — treating OpenRouter as "backup"
if "openrouter" in config:
    use_openrouter()
## Validation

Verify the key loads correctly before running:

bash
python -c "
from pathlib import Path
import os
for line in Path('~/.hermes/.env').expanduser().read_text().splitlines():
    if 'MINIMAX_API_KEY' in line and '=' in line:
        key = line.split('=', 1)[1].strip()
        print(f'Key loaded: {key[:12]}...{key[-4:]}')
"
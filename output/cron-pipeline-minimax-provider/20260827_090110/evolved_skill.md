---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

Any cron-spawned pipeline script **must use MiniMax exclusively** for text, image, and TTS generation. OpenRouter is never a fallback.

## Background

Two bugs caused repeated cron failures:

1. **Environment not sourced**: Hermes cron does not load `~/.hermes/.env` before spawning scripts. API calls fail with `401 / 2049 invalid api key`.
2. **OpenRouter quota exhaustion**: OpenRouter's free tier is 50 calls/day. Using it as a fallback burns through quota instantly when MiniMax has transient issues, as seen on Aug 3 when the newspaper cron hit `HTTP 429: Token Plan usage limit reached (2056)`.

## Rules

| Requirement | Implementation |
|-------------|----------------|
| Sole provider | MiniMax (`sk-cp-…` key) against `api.minimax.io` |
| No fallbacks | If MiniMax fails, the script fails loudly and stops |
| Env self-loading | Script loads `~/.hermes/.env` internally — don't rely on cron shell |
| Cron prompt defense | Cron command also pre-sources the env as a backup layer |

## Required Code — Self-Loading Environment

Paste this at the **top** of any cron pipeline script, before any API key is referenced:

python
import os
from pathlib import Path

def _load_minimax_key():
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
                key, val = line.split("=", 1)
                if key.strip() == "MINIMAX_API_KEY":
                    MINIMAX_KEY = val.strip().strip('"').strip("'")
                    return
    raise RuntimeError("MINIMAX_API_KEY not found in any .env file")

_load_minimax_key()
## Cron Entry Format

bash
# Pre-source env, then run script with env vars passed explicitly
0 6 * * * source ~/.hermes/.env && /usr/bin/python3 /path/to/pipeline.py >> /var/log/pipeline.log 2>&1
## What to Avoid

- ❌ OpenRouter as primary or fallback
- ❌ Pollinations / freegen / image APIs as fallbacks
- ❌ Hardcoded API keys in source files
- ❌ Relying on cron shell to source environment files
- ❌ Silent error handling that masks API failures
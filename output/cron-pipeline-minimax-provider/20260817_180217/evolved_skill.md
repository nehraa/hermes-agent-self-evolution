---
name: cron-pipeline-minimax-provider
description: "Cron text/image/TTS must use MiniMax. Avoid OpenRouter."
category: devops
---

# Cron Pipeline — MiniMax as Sole Provider

## Purpose

All cron-spawned pipeline scripts **must** use MiniMax exclusively for text generation, image generation, and TTS. OpenRouter is never a fallback.

## The Problem

Two bugs broke previous cron pipelines:

1. **Hermes cron does NOT source `~/.hermes/.env`**. Scripts running under cron receive an empty `MINIMAX_API_KEY` environment variable, causing 401 or 2049 errors.

2. **OpenRouter free tier is 50 calls/day**. Using it as a "soft fallback" when MiniMax hiccups exhausts the quota in minutes, killing pipelines with `HTTP 429: Token Plan usage limit reached`.

## Rules

| Rule | Description |
|------|-------------|
| **Sole Provider** | Text, image, and TTS all use MiniMax (`sk-cp-…` key) against `api.minimax.io` |
| **No Fallback** | If MiniMax fails, the script must fail and stop — never cascade to OpenRouter, Pollinations, or freegen |
| **Self-Load Env** | The script itself loads `~/.hermes/.env` at runtime — don't rely on cron shell |
| **Double-Load Defense** | The cron prompt also sources the env file as a safety net |

## Canonical Self-Loader

Place this at the top of any cron pipeline script, **before** the API key constant is referenced:

python
import os
from pathlib import Path

def _load_minimax_key():
    global MINIMAX_API_KEY
    if os.environ.get("MINIMAX_API_KEY"):
        return
    for env_path in (
        Path.home() / ".hermes" / ".env",
        Path.home() / ".env",
        Path("/home/Hermes/OpenMAIC/core/.env.local"),
    ):
        if not env_path.exists():
            continue
        for line in env_path.read_text().splitlines():
            if line.startswith("MINIMAX_API_KEY="):
                _, _, value = line.partition("=")
                os.environ["MINIMAX_API_KEY"] = value.strip().strip('"').strip("'")
                return

_load_minimax_key()
## Usage After Loading

python
MINIMAX_API_KEY = os.environ["MINIMAX_API_KEY"]  # guaranteed non-empty
## Cron Entry Pattern

MINIMAX_API_KEY=$(grep MINIMAX_API_KEY ~/.hermes/.env | cut -d= -f2) /usr/bin/python3 /path/to/script.py
Or wrap in a shell script that sources the env first:

bash
#!/bin/bash
source ~/.hermes/.env
exec python3 /path/to/script.py
## What to Do If MiniMax Fails

1. **Alert and stop** — log the error, send a notification, exit with non-zero code.
2. **Do NOT** try OpenRouter, Pollinations, or any other provider as a workaround.
3. **Fix the root cause** — check MiniMax status, verify API key validity, then re-run manually.
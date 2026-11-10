---
name: devpulse-audit-pipeline-fix
description: |
  DevPulse / server.js audit pipeline was broken: `ANTHROPIC_API_KEY` set to
  `process.env.ANTHROPIC_API_KEY` (undefined in cron context) → "Not logged in".
  Inline /api/audit-all in server.js was the broken path. The working path was
  the standalone `devpulse_audit.py` which reads MINIMAX_API_KEY from
  ~/.hermes/.env and sets ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic.
category: devops
---

# DevPulse Audit Pipeline — Root Cause & Fix

## Symptom

Cron job `b99454e251d1` (DevPulse Daily Audit) reports all 3 audit runs failed with:

"Not logged in · Please run /login"
or timeout. The board goes stale because no new Backlog tasks are produced, and the Dispatcher spins on "no pending tasks" indefinitely.

## Root Cause

### Broken Path: `server.js` `/api/audit-all`

javascript
env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }
Two problems:

1. **Missing env var**: Cron context has no `ANTHROPIC_API_KEY` in `process.env`. The key is stored in `~/.claude/settings.json` which Node.js does not auto-load.

2. **Wrong env var name**: Claude Code on the MiniMax proxy expects `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL`, not `ANTHROPIC_API_KEY`.

The inline `claude --print` call in this endpoint returns "Not logged in" because the subprocess inherits the wrong environment.

### Working Path: `devpulse_audit.py`

The standalone script at `/home/Hermes/repos-monitor/scripts/devpulse_audit.py` is correct:

- Reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
- Exports `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, and `ANTHROPIC_API_KEY` to the subprocess

This is the pattern to follow.

## Fixes

### 1. `server.js` — `/api/audit-all` endpoint

Replace the broken inline `claude --print` loop with delegation to the Python script:

javascript
spawnSync('python3', ['-u', '/home/Hermes/repos-monitor/scripts/devpulse_audit.py'])
This mirrors the path the heartbeat cron already uses successfully.

### 2. `server.js` — `/api/repos/:name/audit` endpoint

Apply the same fix. Read `MINIMAX_API_KEY` directly from `/home/Hermes/.hermes/.env` in JavaScript, then set the correct env vars:

javascript
ANTHROPIC_API_KEY=your_key
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
ANTHROPIC_MODEL=your_model
### 3. `start.sh`

Source `~/.hermes/.env` and export the correct vars before launching Node:

bash
source ~/.hermes/.env
export ANTHROPIC_BASE_URL ANTHROPIC_MODEL
node server.js
This ensures the server process always has the right environment as a fallback for any future inline `claude` calls.

### 4. `devpulse_audit.py` — `ingest_findings`

Old tasks created by the broken inline path have `description: null`. When these tasks are re-ingested, `TypeError: 'NoneType' object is not subscriptable` occurs.

**Fix**: Add a null check before accessing task attributes:

python
task.description = task.description or ""
Or filter out null tasks before ingestion:

python
valid_tasks = [t for t in tasks if t.description is not None]
## Verification

After applying fixes, verify:

1. The cron job completes without "Not logged in" errors
2. New Backlog tasks appear in the board
3. The Dispatcher picks up and processes pending tasks
4. Check logs at `/home/Hermes/repos-monitor/logs/` for any remaining errors
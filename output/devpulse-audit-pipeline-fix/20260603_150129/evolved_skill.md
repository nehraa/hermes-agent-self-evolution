---
name: devpulse-audit-pipeline-fix
description: |
  DevPulse audit pipeline was broken: `/api/audit-all` endpoint in server.js
  inherited `ANTHROPIC_API_KEY` from cron environment (undefined) instead of
  reading `MINIMAX_API_KEY` from `~/.hermes/.env`. The working path delegates
  to `devpulse_audit.py`, which correctly reads the env file and sets
  `ANTHROPIC_BASE_URL` for the MiniMax proxy. This skill documents the fix.
category: devops
---

# DevPulse Audit Pipeline — Fix

## Problem

**Symptom:** Cron job `b99454e251d1` (DevPulse Daily Audit) reports all 3 audit runs failed with "Not logged in · Please run /login" or timeout.

**Impact:**
- Board goes stale (no new Backlog tasks for days)
- Dispatcher spins on "no pending tasks" forever

## Root Cause

`/home/Hermes/repos-monitor/server.js` `/api/audit-all` endpoint:

1. Inherited `ANTHROPIC_API_KEY` from `process.env` — this is `undefined` in cron context
2. The key is stored in `~/.claude/settings.json`, which Node.js does not auto-load
3. The wrong environment variable name — Claude Code on the MiniMax proxy requires:
   - `ANTHROPIC_AUTH_TOKEN` (not `ANTHROPIC_API_KEY`)
   - `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`

The inline `claude --print` call returned "Not logged in".

## Working Code Path

`/home/Hermes/repos-monitor/scripts/devpulse_audit.py` works correctly because it:
- Reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
- Exports `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, `ANTHROPIC_API_KEY` to the subprocess

## Fix

### 1. Fix `/api/audit-all` (batch endpoint)

Replace the broken inline `claude --print` loop with:

javascript
spawnSync('python3', ['-u', '/home/Hermes/repos-monitor/scripts/devpulse_audit.py'])
This delegates to the same script the heartbeat cron already uses.

### 2. Fix `/api/repos/:name/audit` (single-repo endpoint)

Used by the dashboard "Audit" button. Apply the same fix:
- Read `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env` in JS
- Set `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL` in the spawn environment

### 3. Fix `start.sh`

Source `~/.hermes/.env` and export `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` before launching Node:

bash
source ~/.hermes/.env
export ANTHROPIC_BASE_URL ANTHROPIC_MODEL
node server.js
This provides belt-and-suspenders coverage for any future inline `claude` calls.

### 4. Handle Legacy Task Data

`devpulse_audit.py` `ingest_findings` can crash on old tasks created by the broken pipeline, which have `description: null`. Add a null check:

python
if task.get('description') is None:
    task['description'] = ''
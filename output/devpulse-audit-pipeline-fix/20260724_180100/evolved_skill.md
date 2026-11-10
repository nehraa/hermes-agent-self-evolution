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

# DevPulse Audit Pipeline Fix

## Problem Summary

The DevPulse audit pipeline was broken, causing all automated audits to fail with "Not logged in" errors.

## Symptoms

- Cron job `b99454e251d1` (DevPulse Daily Audit) reports all 3 audit runs failed
- Error message: "Not logged in · Please run /login" or timeout
- Board goes stale (no new Backlog tasks produced)
- Dispatcher spins on "no pending tasks" indefinitely

## Root Cause

### Broken Path: `server.js` `/api/audit-all` endpoint

The inline implementation had critical environment variable issues:

javascript
env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }
**Problems:**
1. `process.env` in the cron context has no `ANTHROPIC_API_KEY` — it's stored in `~/.claude/settings.json` which Node.js doesn't auto-load
2. Wrong variable name — Claude Code on MiniMax proxy expects:
   - `ANTHROPIC_AUTH_TOKEN` (not `ANTHROPIC_API_KEY`)
   - `ANTHROPIC_BASE_URL` (required for proxy routing)

### Working Path: `devpulse_audit.py`

The standalone script at `/home/Hermes/repos-monitor/scripts/devpulse_audit.py` was correctly implemented:
- Reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
- Exports proper environment variables: `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, `ANTHROPIC_API_KEY`
- Spawns claude subprocess with correct configuration

## Required Fixes

### 1. Fix `server.js` `/api/audit-all` endpoint

Replace the broken inline `claude --print` loop with delegation to the working Python script:

javascript
// Before (broken)
spawnSync('claude', ['--print', auditPrompt], { env: { ...process.env } });

// After (fixed)
spawnSync('python3', ['-u', auditScript], { env: { ANTHROPIC_API_KEY: /* from .env */ } });
### 2. Fix `server.js` `/api/repos/:name/audit` endpoint

Apply the same fix for single-repo audit (used by dashboard "Audit" button):
- Read `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env` directly in JavaScript
- Set `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL` in spawn env

### 3. Fix `start.sh` launcher

Update `/home/Hermes/repos-monitor/start.sh` to source `~/.hermes/.env` and export proxy variables:

bash
#!/bin/bash
source ~/.hermes/.env
export ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
export ANTHROPIC_MODEL=your-model-name
node server.js
This ensures the server process has correct environment variables for any future inline `claude` calls.

### 4. Fix `devpulse_audit.py` `ingest_findings` function

Handle legacy tasks that were created by the broken inline path:

**Issue:** Old tasks have `description: null`, causing:
TypeError: 'NoneType' object is not subscriptable
**Fix:** Add null checks before accessing description:

python
# Before (broken)
if task['description'] and task['description']['content']:

# After (fixed)
if task.get('description') and task['description'].get('content'):
## Verification

After applying fixes, verify:
1. Cron job completes without "Not logged in" errors
2. New Backlog tasks appear in board
3. Dashboard "Audit" button works for single repos
4. Logs show successful claude invocations with proxy routing

## Key Environment Variables

| Variable | Value | Source |
|----------|-------|--------|
| `MINIMAX_API_KEY` | From `~/.hermes/.env` | API key for MiniMax proxy |
| `ANTHROPIC_BASE_URL` | `https://api.minimax.io/anthropic` | Proxy endpoint |
| `ANTHROPIC_MODEL` | Model name | Target model |
| `ANTHROPIC_API_KEY` | Set to `MINIMAX_API_KEY` | Actual auth token |
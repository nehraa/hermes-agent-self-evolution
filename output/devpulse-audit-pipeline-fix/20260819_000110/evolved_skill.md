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

# DevPulse Audit Pipeline — Root Cause + Fix

## Problem Statement

The DevPulse daily audit cron (`b99454e251d1`) was failing silently. All 3 audit runs reported "Not logged in · Please run /login" or timed out. This caused:

- Stale board with no new Backlog tasks for days
- Dispatcher spinning on "no pending tasks"

## Root Cause

The `/api/audit-all` endpoint in `/home/Hermes/repos-monitor/server.js` was broken.

### What was wrong

The endpoint set environment variables like this:

javascript
env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }
Three compounding failures:

1. **`process.env.ANTHROPIC_API_KEY` is undefined in cron context** — The key lives in `~/.claude/settings.json`, which Node.js does not auto-load
2. **Wrong variable name** — Claude Code on the MiniMax proxy expects `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`
3. **Missing `ANTHROPIC_BASE_URL`** — The MiniMax proxy requires `https://api.minimax.io/anthropic` as the base URL

When the inline `claude --print` command ran in the endpoint, it received no valid credentials and returned "Not logged in".

### The working path

`/home/Hermes/repos-monitor/scripts/devpulse_audit.py` was already correct:

- Reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
- Exports `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, and `ANTHROPIC_API_KEY` to the subprocess
- This is what the heartbeat cron already uses successfully

## Fixes

### 1. Fix `/api/audit-all` endpoint

Replace the broken inline `claude --print` loop with delegation to the working script:

javascript
// Instead of inline claude --print, spawn the Python script
const auditScript = path.join(__dirname, 'scripts', 'devpulse_audit.py');
const result = spawnSync('python3', ['-u', auditScript, 'audit-all'], {
  cwd: '/home/Hermes/repos-monitor',
  env: loadHermesEnv()  // See helper below
});
### 2. Fix `/api/repos/:name/audit` endpoint

Apply the same fix for the single-repo audit endpoint (used by dashboard "Audit" button):

javascript
// Read MINIMAX_API_KEY from .env and set correct Anthropic vars
function loadHermesEnv() {
  const envPath = '/home/Hermes/.hermes/.env';
  const envContent = fs.readFileSync(envPath, 'utf8');
  const minimaxKey = envContent.match(/MINIMAX_API_KEY=(.+)/)?.[1];

  return {
    ...process.env,
    ANTHROPIC_API_KEY: minimaxKey,
    ANTHROPIC_BASE_URL: 'https://api.minimax.io/anthropic',
    ANTHROPIC_MODEL: 'anthropic/claude-3.5-sonnet'
  };
}
### 3. Fix `start.sh`

Source `~/.hermes/.env` before launching Node to ensure the server process has correct env vars:

bash
#!/bin/bash
cd /home/Hermes/repos-monitor
source ~/.hermes/.env
export ANTHROPIC_BASE_URL ANTHROPIC_MODEL
node server.js
This provides belt-and-suspenders coverage for any future inline `claude` calls.

### 4. Fix `devpulse_audit.py ingest_findings`

Old tasks created by the broken path have `description: null`, causing:

TypeError: 'NoneType' object is not subscriptable
Add null handling:

python
task_description = task.get('description') or ''
## Key Takeaways

| Location | Problem | Solution |
|----------|---------|----------|
| `server.js` inline env | `process.env.ANTHROPIC_API_KEY` undefined | Read from `~/.hermes/.env` directly |
| Variable name | Used `ANTHROPIC_API_KEY` instead of `ANTHROPIC_AUTH_TOKEN` | Set correct MiniMax proxy vars |
| Missing config | No `ANTHROPIC_BASE_URL` | Set `https://api.minimax.io/anthropic` |

**Always prefer delegating to `devpulse_audit.py`** — it already handles all env setup correctly. Avoid inline `claude --print` calls in server endpoints.
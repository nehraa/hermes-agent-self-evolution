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

## Problem

**Symptom:** Cron job `b99454e251d1` (DevPulse Daily Audit) reports all 3 audit runs failed with:
- `"Not logged in · Please run /login"`
- Timeout errors

**Impact:** Board goes stale for days because no new Backlog tasks are produced. Dispatcher spins on "no pending tasks" forever.

---

## Root Cause

The `/api/audit-all` endpoint in `server.js` tried to call `claude --print` directly:

javascript
env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }
**Why this fails:**

| Issue | Explanation |
|-------|-------------|
| Missing env var | Cron context has no `ANTHROPIC_API_KEY` in `process.env` |
| Wrong storage | API key is stored in `~/.claude/settings.json` (Node doesn't auto-load this) |
| Wrong var name | Claude Code on MiniMax proxy expects `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL`, not `ANTHROPIC_API_KEY` |

**Working code path:** `/home/Hermes/repos-monitor/scripts/devpulse_audit.py`
- Reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
- Exports `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, `ANTHROPIC_API_KEY` to subprocess

---

## Fixes Applied

### 1. Fix `/api/audit-all` endpoint

Replace broken inline `claude --print` loop with delegation to the working Python script:

javascript
const auditScript = path.join(__dirname, 'scripts/devpulse_audit.py');
const result = spawnSync('python3', ['-u', auditScript], { stdio: 'inherit' });
### 2. Fix `/api/repos/:name/audit` endpoint (single-repo audit)

Read `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env` directly in JavaScript, then set proper env vars before spawning:

javascript
const env = {
  ...process.env,
  ANTHROPIC_BASE_URL: 'https://api.minimax.io/anthropic',
  ANTHROPIC_MODEL: 'your-model-name',
  ANTHROPIC_API_KEY: minimaxKey
};
spawnSync('python3', ['-u', auditScript], { env, stdio: 'inherit' });
### 3. Fix `start.sh`

Source `~/.hermes/.env` and export variables before launching Node:

bash
#!/bin/bash
set -e
source ~/.hermes/.env
export ANTHROPIC_BASE_URL ANTHROPIC_MODEL
cd /home/Hermes/repos-monitor
node server.js
This provides belt-and-suspenders coverage for any future inline `claude` calls.

---

## Data Migration Fix

**Problem:** Tasks created during the broken period have `description: null`, causing:

TypeError: 'NoneType' object is not subscriptable
**Fix:** Update `devpulse_audit.py` `ingest_findings()` to handle null descriptions:

python
task_description = finding.get('description') or finding.get('summary', 'No description')
---

## Verification

After applying fixes, verify:

1. **Single-repo audit:** Click "Audit" button in dashboard → should complete without "Not logged in"
2. **Full audit:** Trigger `/api/audit-all` → all repos should process
3. **Cron job:** Watch next scheduled run → should produce new Backlog tasks
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

## Symptom

Cron job `b99454e251d1` (DevPulse Daily Audit) reports all 3 audit runs failed with:

Not logged in · Please run /login
Or timeouts. Board goes stale for days because no new Backlog tasks are produced. Dispatcher spins on "no pending tasks" forever.

## Root Cause

The `/api/audit-all` endpoint in `/home/Hermes/repos-monitor/server.js` used this broken pattern:

javascript
env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }
**Why it fails:**

1. The cron context has no `ANTHROPIC_API_KEY` in `process.env` — it's stored in `~/.claude/settings.json` which Node doesn't auto-load.
2. Claude Code on the MiniMax proxy expects `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_BASE_URL`, not `ANTHROPIC_API_KEY`.
3. Inline `claude --print` returns "Not logged in" because env vars are missing.

**The working path:**

The standalone `/home/Hermes/repos-monitor/scripts/devpulse_audit.py` reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env` and correctly exports:

bash
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
ANTHROPIC_MODEL=some-model
ANTHROPIC_API_KEY=$MINIMAX_API_KEY
This is the code path the heartbeat cron already uses successfully.

## Fix

### 1. Fix `/api/audit-all` in server.js

Replace the broken inline `claude --print` loop with delegation to the Python script:

javascript
const auditScript = path.join(__dirname, 'scripts', 'devpulse_audit.py');
const result = spawnSync('python3', ['-u', auditScript, 'run-audits'], {
  cwd: __dirname,
  env: loadHermesEnv() // Read MINIMAX_API_KEY from ~/.hermes/.env
});
### 2. Fix `/api/repos/:name/audit` in server.js

Same fix for the single-repo audit endpoint (used by dashboard "Audit" button):

javascript
function loadHermesEnv() {
  const envPath = '/home/Hermes/.hermes/.env';
  const envContent = readFileSync(envPath, 'utf8');
  const envVars = {};
  envContent.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split('=');
    if (key && valueParts.length) {
      envVars[key.trim()] = valueParts.join('=').trim();
    }
  });
  return { ...process.env, ...envVars };
}
Pass `loadHermesEnv()` to `spawnSync` so the subprocess has `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` / `ANTHROPIC_API_KEY`.

### 3. Fix `start.sh`

Source `~/.hermes/.env` and export required vars before launching Node:

bash
#!/bin/bash
set -e
cd /home/Hermes/repos-monitor
source /home/Hermes/.hermes/.env
export ANTHROPIC_BASE_URL ANTHROPIC_MODEL
node server.js
This is belt-and-suspenders for any future inline `claude` calls.

### 4. Fix `devpulse_audit.py` ingest_findings

Old tasks (created by the broken inline path) have `description: None`. The `ingest_findings` function must handle null descriptions:

python
def ingest_findings(finding_type, tasks):
    for task in tasks:
        description = task.get('description') or task.get('summary') or f"Generated {finding_type} task"
        # ... rest of ingestion logic
Without this fix: `TypeError: 'NoneType' object is not subscriptable` when accessing `description[0]`.

## Verification

After applying fixes, verify:

1. Run the cron job manually:
   ```bash
   cd /home/Hermes/repos-monitor && python3 scripts/devpulse_audit.py run-audits
   ```
2. Check for new Backlog tasks in the board.
3. Verify cron `b99454e251d1` logs show successful completion.

## Prevention

- Never call `claude --print` inline in server.js with `process.env` alone.
- Always source env vars from `/home/Hermes/.hermes/.env` for subprocess calls.
- Use the Python audit scripts as the canonical path for all audit operations.
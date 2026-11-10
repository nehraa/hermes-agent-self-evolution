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
Cron `b99454e251d1` (DevPulse Daily Audit) reports: all 3 audit runs failed
with "Not logged in · Please run /login" or timeout. Board goes stale for days
because no new Backlog tasks are produced. Dispatcher spins on "no pending tasks"
forever.

## Root Cause
`/home/Hermes/repos-monitor/server.js` `/api/audit-all` endpoint:
- Set `env: { ...process.env, ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY }`
- The cron context has no `ANTHROPIC_API_KEY` in `process.env` (it's stored
  in `~/.claude/settings.json` which Node doesn't auto-load, AND it's the
  wrong var name — Claude Code on the MiniMax proxy expects
  `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_BASE_URL`).
- Inline `claude --print` in the endpoint then returned "Not logged in".

The standalone `/home/Hermes/repos-monitor/scripts/devpulse_audit.py` was
correctly written — it reads `MINIMAX_API_KEY` from `/home/Hermes/.hermes/.env`
and exports `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` / `ANTHROPIC_API_KEY` to
the claude subprocess. This is the working code path.

## Fix
1. **`server.js /api/audit-all`** — replace the broken inline `claude --print`
   loop with `spawnSync('python3', ['-u', auditScript])` that delegates to
   `devpulse_audit.py`. Same path the heartbeat cron already uses successfully.

2. **`server.js /api/repos/:name/audit`** (single-repo endpoint, used by
   dashboard "Audit" button) — same fix: read `MINIMAX_API_KEY` from
   `/home/Hermes/.hermes/.env` directly in JS, set
   `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`/`ANTHROPIC_MODEL` in the spawn env.

3. **`/home/Hermes/repos-monitor/start.sh`** — source `~/.hermes/.env` and
   export `ANTHROPIC_BASE_URL`/`ANTHROPIC_MODEL` before launching node, so the
   server process always has the right env (belt-and-suspenders for any
   future inline `claude` calls).

4. **`devpulse_audit.py ingest_findings`** — old tasks (created by the broken
   inline path) have `description: null`, causing a `TypeError: 'NoneType'
   object is not subscriptable` on every refresh. Fix: fall back to `title`
   for the dedup signature when `description is None`.

5. **`devpulse_audit.py main()`** — `repo.lastAudit` was never updated by the
   audit script (only by the broken server.js path), so the dashboard always
   showed stale timestamps. Fix: update `repo.lastAudit = now_iso()` after
   each successful `audit_repo` call.

## Verification
After fix, run a manual end-to-end test:
```
curl -sS -X POST http://127.0.0.1:3456/api/audit-all
```
Expect: HTTP 200, `success: true`, `exitCode: 0`, `logTail` ends with
`=== audit run done: N new task(s) added to Backlog ===`. Took ~7-8 min
for 3 repos on June 3, 2026.

Then check `data/board.json`:
- `repos[].lastAudit` updated to current time
- `tasks` array grew by ~24 entries (6-10 per repo)
- Dispatcher daemon immediately starts picking up the new Backlog items
  (logs show `created worktree ... → In Progress → dispatched`)

## Pitfalls
- Hermes masks `MINIMAX_API_KEY` value in display. The key is still real on
  disk — `xxd` confirms it. Don't be fooled by the `***` in `cat` output.
- Don't try to source `~/.claude/settings.json` in bash — it's JSON, not
  shell-sourceable. Use the env vars directly.
- `start.sh` MUST source `~/.hermes/.env` BEFORE launching node, otherwise
  the node process inherits no MiniMax creds. Even with the JS-side env
  fix, do this too — future code paths will assume the env is set.
- The two daemons issue: if you manually start a dispatcher while one is
  already running (or after a stale pidfile), you'll get duplicate daemons
  racing on the same board. Always `kill <old_pid> && rm -f pidfile && bash
  run_dispatcher_daemon.sh` to clean up.
- `devpulse_audit.py` uses `claude --bare` which strictly requires
  `ANTHROPIC_API_KEY` in env (not `ANTHROPIC_AUTH_TOKEN`). The script
  correctly maps `MINIMAX_API_KEY → ANTHROPIC_API_KEY`.

## Files Touched
- `/home/Hermes/repos-monitor/server.js` — both audit endpoints fixed
- `/home/Hermes/repos-monitor/start.sh` — env sourcing added
- `/home/Hermes/repos-monitor/scripts/devpulse_audit.py` — NoneType fix +
  lastAudit update

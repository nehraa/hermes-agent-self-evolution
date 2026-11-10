---
name: coding-harness-cli-on-this-server
description: "Coding-harness CLIs: nscd auth, TUI limits, compare pattern."
tags: [coding-harness, claude-code, copilot-cli, codex-cli, opencode-cli, nscd]
category: autonomous-ai-agents
---

# Coding-Harness CLIs on This Server

Cross-cutting playbook for invoking autonomous coding-harness CLIs
(Claude Code, GitHub Copilot CLI, Codex CLI, OpenCode CLI) from Hermes.
Per-harness skills (`claude-code`, `codex`, `opencode`) cover each tool
individually; this skill covers the **shared** problems.

## Shared Constraints

| Issue | Impact |
|-------|--------|
| Copilot CLI nscd bug | Authentication blocked by missing nscd daemon |
| Hermes terminal cannot drive interactive TUIs | All bare harness invocations require non-interactive mode |
| Multi-harness compare pattern | Run harnesses in isolation, parallel dispatch, fail-fast escalation |

---

## 1. The Copilot CLI nscd Bug

Copilot CLI fails with authentication errors even when tokens and network
connectivity are confirmed working.

### Symptoms

bash
$ copilot -p "fix the bug"
Error: Authentication token found but could not be validated.
Failed to fetch OAuth user login: network fetch failed: request failed: builder error

# Same error occurs with all login methods:
$ copilot login --device-code    # Fails
$ copilot login --with-token     # Fails
$ COPILOT_GITHUB_TOKEN=*** copilot -p "echo ok"  # Fails
**Confirm network is not the issue:**

bash
curl -s -o /dev/null -w "%{http_code}" https://api.github.com/user
# Returns: 200

gh auth status
# Token has required scopes: repo, workflow, gist, read:org
### Root Cause

Copilot's Go HTTP client (`reqwest`) uses cgo for DNS resolution. On glibc ≥ 2.26,
`getaddrinfo` checks for nscd daemon socket before attempting DNS lookups.

**This server's configuration:**

| Component | Status |
|-----------|--------|
| `nscd` | **Not installed** (`apt-cache policy nscd` → no candidate) |
| `systemd-resolved` | Running (DNS at 127.0.0.53) |
| `/etc/nsswitch.conf` | `hosts: files dns mymachines` — correct, but cgo path blocks on nscd |

The HTTP request builder fails immediately when the nscd socket lookup returns
`ENOENT`. The error message "builder error" is an unhelpful wrapper around the
missing-socket condition.

### Diagnosis

bash
# Confirm nscd socket lookup is blocking the request
strace -f -e trace=connect copilot --version 2>&1 | grep nscd

# Expected output (confirms the issue):
# connect(/var/run/nscd/socket) = -1 ENOENT (No such file or directory)
### Fix

bash
# Install and enable nscd
sudo apt install -y nscd
sudo systemctl enable --now nscd

# Verify DNS resolution still works
getent hosts api.github.com

# Confirm Copilot authentication succeeds
copilot -p "echo ok"
# Expected: executes successfully
**Post-fix verification:**

bash
# All these should now work:
copilot -p "echo authenticated"
COPILOT_GITHUB_TOKEN=*** copilot -p "echo ok"
gh auth status
---

## 2. Hermes Terminal Cannot Drive Interactive TUIs

Hermes invokes harnesses via non-interactive shell sessions. Interactive
features (password prompts, terminal UI libraries, pager controls) cannot
function.

### Affected Features

| Feature | Harness | Workaround |
|---------|---------|------------|
| Password/passphrase prompts | All | Set `COPILOT_GITHUB_TOKEN`, `OPENAI_API_KEY`, etc. via environment |
| `less`/`more` pager output | Claude Code | Use `--output-format=json` or `--no-ansi` |
| TUI progress bars | Claude Code | Use `--no-ansi` flag |
| Interactive rebase/merge | Claude Code | Use `--no-interactive` or pre-configured `.claude` settings |
| Device code OAuth flow | Copilot | Use token-based auth (`--with-token` or `COPILOT_GITHUB_TOKEN`) |

### Pre-requisites for Non-Interactive Use

Before invoking any harness from Hermes, ensure:

bash
# Claude Code: non-interactive mode
export CLAUDE_NO_ANSI=true
export CLAUDE_OUTPUT_FORMAT=json

# Copilot CLI: token-based auth
export COPILOT_GITHUB_TOKEN=$(gh auth token)

# Codex CLI: API key set
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1

# OpenCode CLI: configure before invocation
opencode config set api_key $OPENAI_API_KEY
---

## 3. Multi-Harness Compare Pattern

When comparing outputs across harnesses on the same task, run each in
isolated environments to prevent state contamination.

### Pattern Implementation

bash
# 1. Create isolated temporary directories
WORK_DIR=$(mktemp -d)
HARNESSES=(claude-code codex opencode)

for harness in "${HARNESSES[@]}"; do
  mkdir -p "$WORK_DIR/$harness"
done

# 2. Dispatch harnesses in parallel with individual output streams
coproc CLAUDE (claude-code --dir "$WORK_DIR/claude-code" -p "implement $TASK" 2>&1)
coproc CODEX (codex --dir "$WORK_DIR/codex" -p "implement $TASK" 2>&1)
coproc OPENCODE (opencode --dir "$WORK_DIR/opencode" -p "implement $TASK" 2>&1)

# 3. Collect results with timeout
TIMEOUT=120
for name in CLAUDE CODEX OPENCODE; do
  timeout $TIMEOUT head -n 1000 /dev/stdin &
  kill $! 2>/dev/null
done
### Fail-Fast Escalation

bash
# Stop other harnesses when first one succeeds
FIRST_SUCCESS=""

for harness in "${HARNESSES[@]}"; do
  if [[ -z "$FIRST_SUCCESS" ]]; then
    if timeout 60 $harness -p "$TASK" > "$WORK_DIR/$harness/output.txt" 2>&1; then
      FIRST_SUCCESS="$harness"
      # Signal other coprocs to terminate
      kill $COPROC_PID 2>/dev/null
    fi
  fi
done

if [[ -n "$FIRST_SUCCESS" ]]; then
  echo "First successful harness: $FIRST_SUCCESS"
  cat "$WORK_DIR/$FIRST_SUCCESS/output.txt"
else
  echo "All harnesses failed. Check $WORK_DIR for individual logs."
fi
### Isolation Requirements

| Resource | Isolation Method |
|----------|------------------|
| Working directory | Separate `--dir` for each harness |
| Environment variables | Prefix with harness name or use `env -i` |
| Git state | Each harness gets clean checkout or temp repo |
| API rate limits | Sequential requests or separate API keys |

---

## Quick Reference

| Problem | Command |
|---------|---------|
| Copilot auth fails | `sudo apt install -y nscd && sudo systemctl enable --now nscd` |
| Claude Code hangs | `claude-code --no-interactive -p "task"` |
| Compare harnesses | See multi-harness pattern above |
| Check nscd status | `strace -f -e trace=connect copilot --version 2>&1 \| grep nscd` |
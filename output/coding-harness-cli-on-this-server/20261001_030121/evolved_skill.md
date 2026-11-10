---
name: coding-harness-cli-on-this-server
description: "Coding-harness CLIs: nscd auth, TUI limits, compare pattern."
tags: [coding-harness, claude-code, copilot-cli, codex-cli, nscd]
category: autonomous-ai-agents
---

# Coding-Harness CLIs on This Server

Cross-cutting playbook for invoking autonomous coding-harness CLIs (Claude Code, GitHub Copilot CLI, Codex CLI, OpenCode CLI) from Hermes. Per-harness skills (`claude-code`, `codex`, `opencode`) cover each tool individually; this skill covers the **shared** problems and patterns that apply to all harnesses.

## Shared Constraints Overview

| Issue | Affects | Symptom |
|-------|---------|---------|
| nscd daemon missing | Copilot CLI | `Authentication token found but could not be validated` |
| Hermes lacks PTY | All harnesses | TUIs hang waiting for terminal input |
| Parallel dispatch | All harnesses | Need consistent comparison methodology |

---

## 1. The Copilot CLI nscd Bug

Authentication blocked by a missing `nscd` daemon on this server.

### Symptom

bash
$ copilot -p "fix the bug"
Error: Authentication token found but could not be validated.
Failed to fetch OAuth user login: network fetch failed: request failed: builder error
Same error occurs with:

- `copilot login --device-code`
- `copilot login --with-token`
- `COPILOT_GITHUB_TOKEN=*** copilot ...`

Network connectivity is confirmed working (`curl -s api.github.com/user` returns 200). Token has sufficient scopes: `repo`, `workflow`, `gist`, `read:org`.

### Root Cause

Copilot's Go HTTP client (`reqwest`) calls glibc's `getaddrinfo` via the cgo resolver. On glibc ≥ 2.26, this looks up the nscd daemon socket first before falling back to other resolvers.

On this server:

| Component | Status |
|-----------|--------|
| `nscd` | **Not installed** (`apt-cache policy nscd` → no candidate) |
| `systemd-resolved` | Running (DNS at 127.0.0.53) |
| `/etc/nsswitch.conf` | `hosts: files dns mymachines` — should work, but cgo path locks onto nscd first |

The request builder fails before any DNS lookup occurs. The error message "builder error" is an unhelpful wrapper around the missing-socket condition.

### Diagnosis

bash
# Confirm nscd socket lookup is the culprit
strace -f -e trace=connect copilot --version 2>&1 | grep nscd
Expected output:

connect(/var/run/nscd/socket) = -1 ENOENT (No such file or directory)
### Fix

bash
# Install and enable nscd
sudo apt install -y nscd
sudo systemctl enable --now nscd

# Verify DNS resolution works
getent hosts api.github.com

# Confirm Copilot auth now succeeds
copilot -p "echo ok"
After this fix, `COPILOT_GITHUB_TOKEN`, `gh auth status`, and the device-code login flow all work correctly.

---

## 2. Hermes Terminal TUI Limitations

Hermes cannot drive interactive TUIs for any harness.

### Symptom

When invoking a harness with an interactive prompt:

bash
$ claude-code
Waiting for terminal... (hangs indefinitely)
Or for Copilot:

bash
$ copilot
# Hangs at interactive prompts
### Root Cause

Hermes executes commands in a non-interactive shell without a proper PTY (pseudo-terminal). TUI-based prompts require a terminal with cursor positioning and real-time input handling.

### Workaround

**Always use the non-interactive pattern** for all harness invocations from Hermes:

| Harness | Non-Interactive Flag | Example |
|---------|---------------------|---------|
| Claude Code | `--print` or `--resume` | `claude-code -p "task description"` |
| Copilot CLI | `-p` | `copilot -p "task description"` |
| Codex CLI | `--no-interactive` | `codex --no-interactive "task description"` |
| OpenCode CLI | `-c` or stdin | `echo "task" \| opencode -` |

### Example: Claude Code Non-Interactive

bash
# Instead of interactive mode (will hang):
# claude-code

# Use print mode with task description:
claude-code -p "Review PR #123 and summarize changes"
### Example: Copilot Non-Interactive

bash
# Use project flag with prompt:
copilot -p "Explain this function: $(cat src/utils.py)"

# Or pipe input:
echo "Add error handling to main.py" | copilot -p "$(cat)"
---

## 3. The Multi-Harness Compare Pattern

Run each harness in isolation, dispatch in parallel, stop and escalate when one succeeds.

### When to Use

- Multiple harnesses can solve the same task
- Need to compare output quality or correctness
- Want fastest successful result

### Pattern Implementation

bash
# 1. Define the task once
TASK="Refactor user authentication to use JWT tokens"

# 2. Create output directories with timestamps
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p /tmp/harness_compare/$TIMESTAMP

# 3. Dispatch all harnesses in parallel with timeout
parallel --tag --halt soon,success=1 ::: \
  "claude-code -p '$TASK' 2>&1 | tee /tmp/harness_compare/$TIMESTAMP/claude.txt" \
  "copilot -p '$TASK' 2>&1 | tee /tmp/harness_compare/$TIMESTAMP/copilot.txt" \
  "codex --no-interactive '$TASK' 2>&1 | tee /tmp/harness_compare/$TIMESTAMP/codex.txt" \
  "opencode -c '$TASK' 2>&1 | tee /tmp/harness_compare/$TIMESTAMP/opencode.txt"

# 4. Capture the first success
FIRST_SUCCESS=$(ls -t /tmp/harness_compare/$TIMESTAMP/*.txt | head -1 | xargs basename)
echo "Winner: $FIRST_SUCCESS"
### Comparison Script

bash
#!/bin/bash
# compare_harnesses.sh - Compare harness outputs for a task

TASK="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="/tmp/harness_results/$TIMESTAMP"

mkdir -p "$OUTDIR"

# Run each harness with 120-second timeout
for harness in claude copilot codex opencode; do
  case $harness in
    claude)   cmd="claude-code -p '$TASK'" ;;
    copilot)  cmd="copilot -p '$TASK'" ;;
    codex)    cmd="codex --no-interactive '$TASK'" ;;
    opencode) cmd="opencode -c '$TASK'" ;;
  esac
  
  timeout 120 bash -c "$cmd" > "$OUTDIR/$harness.txt" 2>&1 &
done

# Wait for all and report
wait

echo "=== Results in $OUTDIR ==="
for f in "$OUTDIR"/*.txt; do
  echo "--- $(basename $f) ---"
  head -50 "$f"
  echo
done
### Escalation Rules

1. **First success wins** — Use output from the harness that completes successfully first
2. **Timeout after 120 seconds** — Consider task failed for that harness
3. **Escalate to human** when:
   - All harnesses fail or timeout
   - Results contradict each other significantly
   - Task requires permissions/tools unavailable to harnesses

### Output Format Standardization

When comparing outputs, normalize them:

bash
# Strip ANSI codes and normalize whitespace for comparison
normalize() {
  cat "$1" | sed 's/\x1b\[[0-9;]*m//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sort
}

diff <(normalize /tmp/harness_results/$TIMESTAMP/claude.txt) \
     <(normalize /tmp/harness_results/$TIMESTAMP/copilot.txt)
---

## Quick Reference Card

| Problem | Quick Fix |
|---------|-----------|
| Copilot auth fails | `sudo apt install -y nscd && sudo systemctl enable --now nscd` |
| Harness hangs | Use non-interactive flags: `-p`, `--print`, `--no-interactive` |
| Compare outputs | See `compare_harnesses.sh` pattern above |
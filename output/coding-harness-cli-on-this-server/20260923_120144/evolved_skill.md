---
name: coding-harness-cli-on-this-server
description: "Coding-harness CLIs: nscd auth, TUI limits, compare pattern."
tags: [coding-harness, claude-code, copilot-cli, codex-cli, nscd]
category: autonomous-ai-agents
---

# Coding-Harness CLIs on This Server

Cross-cutting playbook for invoking autonomous coding-harness CLIs
(Claude Code, GitHub Copilot CLI, Codex CLI, OpenCode CLI) from Hermes.
Per-harness skills (`claude-code`, `codex`, `opencode`) cover each tool
individually; this skill covers the **shared** problems.

## Shared Constraints

1. **The Copilot CLI nscd bug** — authentication blocked by missing nscd daemon
2. **Hermes terminal cannot drive interactive TUIs** — applies to every
   bare invocation of every harness
3. **The multi-harness compare pattern** — run each harness in isolation,
   dispatch in parallel, stop and escalate when one fails

---

## 1. The Copilot CLI nscd Bug

### Symptom

bash
$ copilot -p "fix the bug"
Error: Authentication token found but could not be validated.
Failed to fetch OAuth user login: network fetch failed: request failed: builder error
Same error occurs with:
- `copilot login --device-code`
- `copilot login --with-token`
- `COPILOT_GITHUB_TOKEN=*** copilot ...`

Network connectivity is confirmed working (`curl -s api.github.com/user` returns 200).
Token has sufficient scopes: `repo`, `workflow`, `gist`, `read:org`.

### Root Cause

Copilot's Go HTTP client (`reqwest`) calls glibc's `getaddrinfo` via the cgo
resolver. On glibc ≥ 2.26, this looks up the nscd daemon socket first.

On this server:

| Component | Status |
|-----------|--------|
| `nscd` | **Not installed** (`apt-cache policy nscd` → no candidate) |
| `systemd-resolved` | Running (DNS at 127.0.0.53) |
| `/etc/nsswitch.conf` | `hosts: files dns mymachines` — should work, but cgo path locks onto nscd first |

The request builder fails before any DNS lookup occurs. The error message
"builder error" is an unhelpful wrapper around the missing-socket condition.

### Diagnosis

bash
# Confirm nscd socket lookup is the culprit
strace -f -e trace=connect copilot --version 2>&1 | grep nscd

# Expected output:
# connect(/var/run/nscd/socket) = -1 ENOENT (No such file or directory)
### Fix

bash
# Install and enable nscd
sudo apt install -y nscd
sudo systemctl enable --now nscd

# Verify DNS resolution works
getent hosts api.github.com

# Confirm Copilot auth now succeeds
copilot -p "echo ok"
After this fix, `COPILOT_GITHUB_TOKEN`, `gh auth status`, and the gh
oauth_token in `~/.config/gh/hosts.yml` all validate normally.

### Same Root Cause Affects Other Go Binaries

Any Go binary using `net.LookupHost` via cgo can hit this:

- **Affected**: Go binaries linked against glibc ≥ 2.26 that use the cgo resolver
- **Unaffected**: Go binaries using `CGO_ENABLED=0` or musl-based Alpine images

If you encounter "builder error" or DNS resolution failures from other Go tools,
apply the same fix.

---

## 2. Hermes Terminal TUI Limitations

### The Problem

Hermes cannot reliably drive interactive TTY applications. This affects:

- Claude Code (`claude code` without flags)
- GitHub Copilot CLI (interactive prompts)
- Codex CLI (interactive mode)
- OpenCode CLI (interactive mode)

### Safe Invocation Pattern

**Always use headless/non-interactive flags** when invoking harnesses from Hermes:

| Harness | Safe Flags |
|---------|------------|
| Claude Code | `--dangerously-skip-permissions` + prompt via stdin or `-p` flag |
| Copilot CLI | `-p "prompt text"` (not interactive mode) |
| Codex CLI | Use `--prompt` or `--cli` flags for non-interactive |
| OpenCode CLI | Check for `--non-interactive` or `-y` flag |

### Example: Claude Code Safe Invocation

bash
# UNSAFE - will hang or fail
claude code

# SAFE - headless operation
echo "implement the feature" | claude -p "$(cat)"

# Or with full prompt
claude -p "Implement user authentication with JWT tokens"
---

## 3. Multi-Harness Compare Pattern

Use this pattern when you need to compare outputs from multiple coding harnesses
or when one harness fails and you want to verify the problem is harness-specific.

### Worktree-Per-Harness Setup

bash
# Create isolated worktrees for each harness
BASE_REPO="$HOME/projects/myproject"

# Claude Code worktree
git -C "$BASE_REPO" worktree add ../compare-claude feature/compare-start
# Codex worktree
git -C "$BASE_REPO" worktree add ../compare-codex feature/compare-start
# OpenCode worktree
git -C "$BASE_REPO" worktree add ../compare-opencode feature/compare-start
### Parallel Dispatch

bash
# Run all harnesses in parallel, each in its own worktree
PARALLEL=1

# Claude Code
(cd ../compare-claude && claude -p "implement the feature" &)

# Copilot CLI
(cd ../compare-codex && copilot -p "implement the feature" &)

# OpenCode
(cd ../compare-opencode && opencode -p "implement the feature" &)

wait
### The "Stop and Ask" Rule

**Stop immediately and escalate to human** when:

1. **Any harness produces security-sensitive output** (credentials, tokens, API keys)
2. **Any harness modifies production infrastructure** (Lambda, ECS, production databases)
3. **Two or more harnesses disagree** on the correct approach
4. **A harness repeatedly fails** with the same error after one retry
5. **Output contains ambiguous or dangerous operations** that could destroy data

bash
# Check for sensitive patterns in output
if echo "$OUTPUT" | grep -iqE "(password|secret|api.key|aws_secret|\.env)"; then
    echo "STOP: Sensitive data detected. Escalating to human."
    # Send notification and pause
fi
### Consolidation

After all harnesses complete, compare outputs:

bash
# Collect results
ls -d ../compare-* | while read dir; do
    echo "=== $(basename $dir) ==="
    cat "$dir/harness-result.txt" 2>/dev/null || echo "(no output)"
done

# Clean up worktrees after comparison
git -C "$BASE_REPO" worktree prune
---

## Quick Reference

| Issue | Command | Expected Outcome |
|-------|---------|------------------|
| Copilot auth failing | `strace -f -e trace=connect copilot --version 2>&1 \| grep nscd` | `connect(/var/run/nscd/socket) = -1 ENOENT` |
| Fix Copilot auth | `sudo apt install -y nscd && sudo systemctl enable --now nscd` | `getent hosts api.github.com` resolves |
| Safe Claude Code | `claude -p "prompt text"` | Runs headless without TTY |
| Compare harnesses | Create worktree per harness, run in parallel | Isolated, comparable outputs |
| Stop condition | Check output for secrets, production changes | Escalate to human |
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
individually; this skill covers the **shared** problems:

1. The **Copilot CLI nscd bug** blocking auth on this server.
2. **Hermes terminal cannot drive interactive TUIs** — applies to every
   bare invocation of every harness.
3. The **multi-harness compare pattern** — worktree-per-harness,
   parallel dispatch, the "stop and ask" rule when one fails.

## 1. The Copilot CLI nscd bug

**Symptom:**
```
$ copilot -p "fix the bug"
Error: Authentication token found but could not be validated.
Failed to fetch OAuth user login: network fetch failed: request failed: builder error
```
Same error from `copilot login --device-code`, `copilot login --with-token`,
and `COPILOT_GITHUB_TOKEN=*** copilot ...`. Network is fine
(`curl api.github.com/user` returns 200 with the gh token). Token has
`repo, workflow, gist, read:org` scopes — more than enough.

**Root cause:**
Copilot's Go HTTP client (`reqwest`) calls glibc's `getaddrinfo` via the
cgo resolver, which on glibc ≥ 2.26 looks up the nscd daemon socket
first. On this server:

- `nscd` is **not installed** (`apt-cache policy nscd` = no candidate)
- `systemd-resolved` IS running (provides DNS at 127.0.0.53)
- `/etc/nsswitch.conf` says `hosts: files dns mymachines` — DNS via libc
  should work, but the Go binary's cgo path locks onto nscd first

The request builder fails before any DNS lookup; the error message is
the unhelpful "builder error" wrapping the missing-socket condition.

**Diagnosis recipe:**
```bash
strace -f -e trace=connect copilot --version 2>&1 | grep nscd
# → connect(/var/run/nscd/socket) = -1 ENOENT (No such file or directory)
```

**Fix (one-line):**
```bash
sudo apt install -y nscd && sudo systemctl enable --now nscd
# Verify
getent hosts api.github.com   # should resolve
copilot -p "say ok"           # should now return without auth error
```

After that, `COPILOT_GITHUB_TOKEN`, `gh auth status`, and the gh
oauth_token in `~/.config/gh/hosts.yml` all validate normally.

**Same root cause can hit any Go binary using `net.LookupHost` via the
cgo resolver on this box.** Rare in practice (most Go programs use
pure-Go DNS via `netgo` build tag), but worth checking if a Go CLI tool
behaves similarly.

## 2. Hermes terminal cannot drive interactive TUIs

Bare `claude` (no `-p`), bare `copilot` (no `-p`), bare `opencode`, any
harness REPL opens a full-screen interface that needs real stdin + TTY +
keystroke input. In the agent's `terminal` tool:

- **Foreground mode**: stdin is closed → process exits 1 with
  `No prompt provided. Run in an interactive terminal or provide a prompt
  with -p or via standard in.`
- **`pty=true` mode**: a PTY is allocated, but the agent has no way to
  send keystrokes or read screen state — the TUI hangs on the first
  prompt (Claude: trust dialog; Copilot: login).

**Rule: always use non-interactive flags from the start:**
- Claude: `claude --print -p "..."` (or pipe via `claude -p -`)
- Copilot: `copilot -p "..." --allow-all-tools` if edits are needed
- Codex: `codex exec "..."` (check `codex --help` for current flag matrix)
- OpenCode: `opencode run "..."` (check `opencode --help` for current flag matrix)

If a harness **genuinely** requires an interactive flow (OAuth
device-code confirmation, MFA challenge, the `claude` OAuth browser
handshake), it cannot be driven from the agent. **Stop and escalate**
to the user with a copy-pasteable URL or token-prompt recipe. Don't
fake completion.

**Special case: `claude auth login`.** Use `ANTHROPIC_API_KEY` env var
instead. The browser-flow OAuth dance won't work in this environment.

## 3. Copilot CLI auth-environment precedence

Order checked: `COPILOT_GITHUB_TOKEN` > `GH_TOKEN` > `GITHUB_TOKEN` >
token in `~/.config/gh/hosts.yml`.

Extract the gh token non-interactively:
```bash
awk '/oauth_token/{print $2; exit}' ~/.config/gh/hosts.yml
```
(`gh auth token` is NOT a subcommand on this server's snap-built gh v2.4.0
— it errors with `unknown command "token"`. Use the awk recipe.)

Required scopes: `repo` is sufficient. Copilot uses the GitHub
user-lookup endpoint, not Copilot-specific scopes.

## 4. Multi-harness compare pattern

When the user asks "compare Claude Code and Copilot on the same task"
(or any pair), run them in **parallel on separate worktrees** so neither
overwrites the other:

```bash
cd /home/Hermes/repos/<repo>
git worktree add ../<repo>-wt-<id>-claude  -b fix/<id>-<slug>-claude  main
git worktree add ../<repo>-wt-<id>-copilot -b fix/<id>-<slug>-copilot main

# Each harness gets the same task file but a different workdir
cat > /tmp/task.md <<'EOF'
[Self-contained task spec, scoped tight, with test instructions]
EOF

# Dispatch in parallel as background processes
terminal(background=true, notify_on_complete=true,
  command="claude --print --model claude-sonnet-4-20250514 \"$(cat /tmp/task.md)\" > /tmp/claude.log 2>&1",
  workdir="/home/Hermes/repos/<repo>-wt-<id>-claude", timeout=600)

terminal(background=true, notify_on_complete=true,
  command="copilot -p \"$(cat /tmp/task.md)\" --allow-all-tools > /tmp/copilot.log 2>&1",
  workdir="/home/Hermes/repos/<repo>-wt-<id>-copilot", timeout=600)
```

Poll both with `process(action='wait', timeout=60)` + `process(action='poll')`
loops (the `wait` action hard-clamps at 60s — see §6).

Compare:
```bash
diff -u <(git -C ../<repo>-wt-<id>-claude  diff main...HEAD) \
         <(git -C ../<repo>-wt-<id>-copilot diff main...HEAD)
```

Run the project's pre-PR CI harness (`make lint && make typecheck && make test-scope`
for opensre; equivalent for other repos) on the winning branch only.
The losing branch's worktree gets `git worktree remove`.

## 5. "Stop and ask" rule when one harness can't run

User explicit preference for multi-harness tasks: **"only continue if
you can successfully get copilot and Claude to work, if not stop and
ask."** Applied literally, this means:

- **No PR opened.** Don't push the winner if the loser failed silently.
- **No claim comment** on the issue. The compare didn't happen; don't
  pretend it did.
- **Worktrees stay intact.** Uncommitted diff in the winning branch
  sits in `../<repo>-wt-<id>-<winner>`, ready for review or for the
  user to run a third harness themselves.
- **Surface the gap explicitly.** "Copilot CLI failed to authenticate
  because nscd is not installed. Here's the strace diagnosis and the
  one-line fix. Want me to install nscd, or pick a different second
  harness (Ollama qwen3 coder, Codex, OpenCode)?"

This rule is the user's verification mechanism. Faking it costs trust;
honest gaps restore it.

### 5a. Single-harness fallback — user can override (added Sep 17 2026)

The "both must work, else stop" rule is the user's **default**, not a
hard floor. The user can override it mid-session ("Ignore copilot, can
u not do the work urself?"), which means:

- The rule fires as an **initial stance** (probe both, fail fast, report).
- Once the user says "skip the compare," single-harness work proceeds
  with the agent (Claude Code) doing the implementation.
- The PR body must explicitly note that no multi-harness comparison
  happened — single sentence, not a paragraph. Reviewers seeing the
  PR should know it's single-harness output, not a silent downgrade.

**The override sequence to follow:**

1. User says "ignore X, can u do it urself" → drop the compare
2. Note in PR body's AI-disclosure section: "Single-harness (Claude Code);
   Copilot CLI unavailable on this server — see strace diagnosis in
   <link>." One line.
3. Don't re-surface the Copilot issue later unless the user asks.
4. Don't proactively try to fix nscd when the user has said "ignore it" —
   that contradicts the override.

Anti-pattern: re-asking the user "should I proceed without Copilot?"
after they already said yes. They said yes. Proceed.

## 5b. PowerShell dot-sourcing fires the entry point (added Sep 17 2026)

`install.ps1` and similar PowerShell scripts that are designed to be
**downloaded and run by users** typically end with an unconditional
entry-point call (`Install-OpenSre` at the bottom of the file). When a
test dot-sources the script (`. install.ps1`) without flag-gating the
entry, the actual install fires — which then makes a real network call,
gets a real 401, and looks like a test failure.

**Symptom:**
```
FAILED test_install_ps1_github_auth.py - AssertionError: Exception: install.ps1:715
  Failed to fetch main build metadata from GitHub for
  'Tracer-Cloud/opensre'. Response status code does not indicate success: 401.
```

Exit code 1, stack frame inside `install.ps1`, and only the ps1 tests
fail (bash equivalent just calls a function without firing `main`) —
all point at this.

**Fix:** find the entry-point gate parameter and pass it in the test.
Most scripts designed for both interactive and library use have a
`-SkipMain` / `-SkipInstall` / `-WhatIf` switch:

```python
script = textwrap.dedent(f"""
    . {shlex.quote(str(INSTALL_PS1))} -SkipMain
    $h = Get-OpenSreRequestHeaders
    $h | ConvertTo-Json -Compress
""")
```

Check how the existing ps1 tests in the same repo dot-source:
```bash
grep -rn '\. install\.ps1\|dot.source.*install\.ps1' tests/
```

If they all use `-SkipMain` or `-SkipInstall`, you need to too. The
parameter is usually defined in the `param([switch]$SkipMain …)` block
at the top of the file.

**Anti-pattern:** trying to override the entry function before
dot-sourcing (`Install-OpenSre() { :; } ; . install.ps1`). PowerShell's
behavior is more complex than bash's — function overrides on source
don't always apply — and you can end up with the override never
applying. Use the param flag.

## 5c. Header / auth builder audit — every branch (added Sep 17 2026)

When a PR splits a header builder (metadata vs assets, auth vs
anonymous, OAuth vs API-key, etc.) the obvious call sites get
updated, but the **streaming, interactive, retry, and fallback
branches** silently keep using the old builder. Greptile will catch
the next branch — you should catch it first.

Verified on opensre PR #6296:

- Original split: `Get-OpenSreRequestHeaders` (metadata, with token)
  vs `Get-OpenSreAssetHeaders` (asset downloads, anonymous).
- Updated `Invoke-OpenSreDownloadFileWithProgress` (the Invoke-WebRequest
  branch) → asset headers.
- Missed: `Invoke-OpenSreStreamDownload` (the streaming fallback
  inside `Invoke-OpenSreDownloadFileWithProgress`, used when
  `Test-OpenSreInteractiveHost` is true and `Test-OpenSreVerboseInstall`
  is false) was still calling `Get-OpenSreRequestHeaders`.
- Result: a real terminal install behind a corporate proxy would have
  its archive/checksum request rewritten or rejected even though
  metadata succeeded. Greptile's second review caught it.

**Audit checklist after any header / auth split:**

```bash
# Find every reference to the OLD builder
grep -nE 'Get-OpenSreRequestHeaders|CURL_FLAGS=.*auth|<old-builder-name>' \
  install.sh install.ps1

# For PowerShell, grep every conditional + retry + streaming branch
# by searching for the function bodies and reading each one for the
# call site
grep -nE 'function (Invoke|Get)-.*(Download|RestMethod|Stream)' install.ps1
```

**Test that pins both branches** (the source-text check that caught
this in #6296):

```python
def test_asset_paths_use_asset_headers_not_request_headers() -> None:
    source = Path("install.ps1").read_text()
    for fn in ("Invoke-OpenSreDownloadFileWithProgress",
               "Invoke-OpenSreStreamDownload"):
        body = _extract_function(source, fn)
        assert "Get-OpenSreAssetHeaders" in body
        # Look for the call SHAPE, not the name string — a comment can
        # mention the old name without leaking the header.
        assert "$headers = Get-OpenSreRequestHeaders" not in body
```

The shape check (literal assignment) is what catches the regression.
A string-only check would falsely pass on a comment that mentions the
old builder name by way of explanation.

## 5d. Fork head-ref cache stuck after force-push (added Sep 17 2026)

When force-pushing to `fork/<branch>` from this server, the
push succeeds (visible at `git ls-remote fork <branch>`) but the
upstream PR's `head.sha` stays stuck on the old commit. Subsequent
CI runs reference the old SHA; reviewers see only the old diff;
your fix is invisible.

**Triage:**

```bash
# 1. Confirm push landed on the fork remote
git ls-remote fork <branch>

# 2. Confirm PR is stuck on old head
gh pr view <PR> --json commits --jq '.commits | length'
curl -s https://api.github.com/repos/<O>/<R>/pulls/<PR>/commits \
  | python3 -c "import sys,json; print(len(json.load(sys.stdin)))"
```

If the fork has your new SHA but the PR doesn't, **don't keep
force-pushing**. Create a new branch + new PR:

```bash
git branch -f <branch>-v2 HEAD
git push fork <branch>-v2 --force
gh pr create --repo <UPSTREAM_OWNER>/<REPO> \
  --head <YOUR_USER>:<branch>-v2 \
  --base main \
  --title "..." \
  --body-file body.md
gh pr close <OLD_PR> --comment "Superseded by <NEW_PR>."
```

Verified on opensre #6295 → #6296: two force-pushes to
`fix/6291-installer-github-auth` were accepted by the fork remote but
the PR head stayed at the original commit for ~30 minutes. New
branch + new PR resolved in seconds. Cause is GitHub's fork→PR
head-ref cache — nothing on the agent side fixes it.

## 6. process(wait) hard-clamp at 60s

When polling background harness processes, `process(action='wait',
timeout=600)` returns after 60s regardless of the timeout argument.
The clamp is baked into the Hermes runtime. For long coding-harness runs
(5-15 min for a non-trivial task):

```python
# Wait incrementally + poll status
for _ in range(15):
    process(action='wait', session_id=proc_id, timeout=60)
    status = process(action='poll', session_id=proc_id)
    if status['status'] == 'exited':
        break
```

Or use `notify_on_complete=true` and react to the notification when it
fires — Hermes wakes the agent when the process finishes, no polling
needed.

## 7. See also

- `claude-code` skill (bundled) — Claude Code CLI specifics: `-p` flag
  matrix, JSON output, hook events, subagent types, worktree flag.
- `codex` skill — Codex CLI specifics.
- `opencode` skill — OpenCode CLI specifics.
- `kanban-claude-lane` / `kanban-codex-lane` — when the harness is
  delegated from a Kanban dispatcher (different lifecycle, different
  ownership).
- `github-pr-paranoid-pre-push` (protected) — the multi-pass QA pattern
  that uses these harnesses as Pass 3 / Pass 3b reviews.

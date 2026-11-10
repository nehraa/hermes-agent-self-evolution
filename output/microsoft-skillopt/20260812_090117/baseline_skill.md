---
name: microsoft-skillopt
category: autonomous-ai-agents
description: "Microsoft SkillOpt-Sleep integration for Hermes Agent: harvest Hermes sessions, mine recurring tasks, optimize SKILL.md files with bounded edits and a held-out validation gate, stage proposals for review, and optionally adopt them with backups. Registered as a Hermes tool (`skillopt_run`) and a no_agent watchdog cron (`SkillOpt-Sleep Nightly Consolidation`, every 6h)."
metadata:
  hermes:
    tags: [skillopt, skill-evolution, self-improvement, hermes, validation-gate]
    homepage: https://github.com/microsoft/SkillOpt
    docs: https://microsoft.github.io/SkillOpt/docs/sleep/README/
---

# Microsoft SkillOpt for Hermes

## What it is

Microsoft SkillOpt treats a natural-language skill document as trainable
state. SkillOpt-Sleep applies that method to an agent's own sessions:

```text
read-only session harvest -> recurring-task mining -> replay -> bounded reflection
    -> held-out validation gate -> staged proposal -> explicit adoption
```

The Hermes integration is installed at:

- Repository: `/home/Hermes/repos/skillopt/`
- Isolated Python: `/home/Hermes/repos/skillopt/.venv/`
- Adapter: `/home/Hermes/.hermes/skillopt/hermes_skillopt.py`
- Launcher: `/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh`
- Gate parser: `/home/Hermes/.hermes/skillopt/_parse_gate.py`
- State/output: `/home/Hermes/.hermes/skillopt/`
- Hermes tool: `skillopt_run` (toolset `skills`, action `status|inspect|run|manifest`)
- No-agent cron: `SkillOpt-Sleep Nightly Consolidation` (job id `364ae7d380ff`, every 6h, mock backend, deliver=local)
- Live Hermes skill directory: `/home/Hermes/.hermes/skills/` (untouched by default)

References:
- `references/minimax-env-recipe.md` — verified env contract for MiniMax + SkillOpt-Sleep (auth mode, compat max tokens, troubleshooting matrix)
- `references/runtime-sanitizer-patterns.md` — how the Hermes runtime rewrites secret-shaped strings in `write_file` outputs and the pre-staging trick the SkillOpt launcher uses
- `scripts/verify-mock-cycle.sh` — re-runnable regression test (upstream tests, deterministic experiment, adapter smoke test, Hermes skill suite)

## Safety contract

- The adapter opens Hermes `state.db` read-only.
- It considers only real `telegram`, `whatsapp`, and `cli` sessions; cron and
  background sessions are excluded because they are machine-generated.
- Text is clipped and SkillOpt's secret redaction is applied before provider
  calls and before diagnostics are written.
- `skillopt_run` defaults to `dry_run=True` and the registry rejects
  `auto_adopt=True` with an explicit message pointing at the real adoption
  command. Adoption is **always** a separate, operator-driven step.
- The `skillopt-watchdog.sh` script implements the 3-state watchdog
  contract (healthy=exit 0 silent, recover=exit 0 silent, 2+ fail=non-zero
  + "Manual intervention required" alert).
- The cron uses `mock` backend by default because the upstream
  `azure_openai` backend has no per-call timeout knob and the 5-retry
  loop exceeds 3 minutes. The `skillopt_run` tool stays available for
  operator-driven real-backend runs.

## Pitfalls (learned the hard way, do not repeat)

- **Real-backend `_call` has no per-call timeout.** A Sleep cycle against
  the `azure_openai` backend can run 3+ minutes because the 5-retry
  exponential-backoff loop is unbounded. Run real-backend cycles
  manually via `skillopt_run(action="run")`, not via the cron, until
  upstream ships a timeout knob.
- **The SkillOpt launcher emits a multi-line JSON object.** Any consumer
  that does `json.loads(sys.stdin.read().splitlines()[-1])` will see
  only `}` and fail silently. Parse the whole blob:
  `json.loads(sys.stdin.read().strip())`. The working reference is
  `~/.hermes/skillopt/_parse_gate.py` — copy that file's logic, don't
  reinvent it.
- **`hermes cron create --script` requires a path relative to
  `~/.hermes/scripts/`.** Absolute paths are rejected with "Script path
  must be relative". Symlink the absolute path into `~/.hermes/scripts/`
  and pass the basename.
- **`hermes cron create` requires `--skill` (or `--prompt`)** even with
  `--no-agent`. Without a skill attached, the create fails with "create
  requires either prompt or at least one skill". Use
  `--skill microsoft-skillopt` so future state changes surface in the
  skill manifest.
- **The Hermes runtime sanitizer rewrites secret-shaped strings in
  `write_file` / `patch` outputs to `***` on disk.** Writing
  `AZURE_OPENAI_AUTH_MODE=openai_compatible` directly into the launcher
  gets rewritten; the file on disk contains
  `AZURE_OPENAI_AUTH_MODE=***`. See
  `references/runtime-sanitizer-patterns.md` for the fix.

## Run it

### No-network deterministic smoke test (recommended first run)

```bash
/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh \
  --backend mock \
  --skill /home/Hermes/.hermes/skills/microsoft-skillopt/SKILL.md \
  --max-sessions 4 --max-tasks 2 --dry-run
```

### Real Hermes dry run via the launcher

The launcher reads the provider key from `/home/Hermes/.hermes/.env` without
printing it. The current default uses MiniMax through SkillOpt's OpenAI-compatible
client:

```bash
/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh \
  --backend azure_openai \
  --endpoint https://api.minimax.io/v1 \
  --model MiniMax-M2.7 \
  --skill /home/Hermes/.hermes/skills/gepa-self-evolution/SKILL.md \
  --lookback-hours 168 --max-sessions 12 --max-tasks 4 --dry-run
```

For real runs the adapter needs `AZURE_OPENAI_API_KEY` (or
`MINIMAX_API_KEY`, which the launcher mirrors). Real-backend runs
consume budget and time; they are operator-driven, not cron-driven.

### Via the Hermes `skillopt_run` tool

The `skillopt_run` tool is registered in the `skills` toolset. Actions:

- `status` — installation + last run manifest, no provider calls
- `inspect` — fast mock-backend smoke test, no LLM mining, dry-run, 2 sessions
- `run` — full Sleep cycle, dry-run by default; `auto_adopt` always rejected
- `manifest` — saved run history only

```json
{ "action": "status" }
{ "action": "run", "skill": "devops/openmaic", "max_sessions": 8, "max_tasks": 3 }
{ "action": "inspect" }
```

The tool returns a JSON report. `staging_dir` is empty until the cycle
passes the validation gate. `accepted` is `true` only when the gate accepts
the proposed edits and `auto_adopt` is enabled at the shell level (which the
tool refuses to do).

### Explicit adoption (after reviewing the staged diff)

```bash
cd /home/Hermes/repos/skillopt
.venv/bin/python -m skillopt_sleep adopt \
  --project /home/Hermes/.hermes/skillopt/projects/<project-hash> \
  --staging /path/from/staging_dir
```

The adapter backs up the live `SKILL.md` in the staging dir before
copying the proposal over it. The proposal is gated by a held-out
slice of mined real tasks, so an "accepted" proposal is a real
improvement on the validation set — not just a stylistic rewrite.

## Choosing a skill

- `--skill /absolute/path/to/SKILL.md` targets one exact skill.
- `--skill <name>` resolves under `/home/Hermes/.hermes/skills/`.
- `--skill auto` selects round-robin state from
  `/home/Hermes/.hermes/skillopt/hermes_manifest.json`.

Start with a procedural skill that has a measurable history, not personal
or credential-bearing skills. Good first targets: `gepa-self-evolution`,
`service-verification`, `microsoft-skillopt`, or a project-specific
operational skill.

## Scheduling

The `SkillOpt-Sleep Nightly Consolidation` cron (job id `364ae7d380ff`)
runs every 6 hours, offset from the existing 3h GEPA cron. It uses
`mock` backend to avoid the upstream 5-minute retry loop, dry-run only,
and `deliver: local` so it stays silent on success. Override
`SKILLOPT_WATCHDOG_BACKEND=azure_openai` in the cron env to switch to a
real backend when the upstream lands a per-call timeout.

For real-backend runs on a faster cadence, do not schedule — call
`skillopt_run(action="run")` from a session when you have time and budget.

## Troubleshooting

### `No tasks mined`

Increase `--lookback-hours`, `--max-sessions`, or target a skill whose
headings and terminology match recent Hermes requests. The adapter ranks
sessions by keyword overlap and falls back to the recent session set if
no overlap exists.

### `baseline=0.0 -> candidate=0.0`

This is not proof the skill is bad. It usually means mined tasks lack a
checkable reference or the provider call returned empty/error output.
Inspect `diagnostics.json`, `evidence.jsonl`, and the report in the
staging directory before changing the gate.

### `parse_error=Expecting value` in the watchdog log

You are parsing `lines[-1]` of the launcher's stdout instead of the
whole blob. Copy the parser from `~/.hermes/skillopt/_parse_gate.py`.

### Real backend hangs for 3+ minutes

Expected. The upstream `azure_openai._call` has no per-call timeout.
Run real-backend cycles manually with `skillopt_run(action="run")`
and accept the slow run, not the cron.

### Upstream updates

The pinned checkout was installed from Microsoft `main` at commit
`bd350aa493aa3fe54ecb260dbfa4b26233734b59`; PyPI package version is
`0.2.0`. Before updating, run the upstream test suite and the
deterministic experiment:

```bash
cd /home/Hermes/repos/skillopt
.venv/bin/python -m pytest -q --disable-warnings --maxfail=1
.venv/bin/python -m skillopt_sleep.experiments.run_experiment \
  --persona researcher --assert-improves
```

Expected baseline verification at installation: `374 passed, 6 skipped`,
and the experiment must report both a held-out improvement and
harmful-edit rejection.

A re-runnable end-to-end check lives at
`~/.hermes/skills/microsoft-skillopt/scripts/verify-mock-cycle.sh` —
run it after any upstream update, any Hermes upgrade, or any adapter
change to catch regressions before they hit the cron.

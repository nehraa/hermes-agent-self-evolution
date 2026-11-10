---
category: software-development
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
name: memory-setup-openclaw
---

# Memory Setup (OpenClaw)

Configure durable memory so the agent can recall prior decisions, preferences, and todos across sessions.

## 1) Prepare workspace files

Maintain these files in the workspace root:

| File/Directory | Purpose |
|----------------|---------|
| `MEMORY.md` | Curated long-term memory (project overview, key decisions, contacts) |
| `memory/YYYY-MM-DD.md` | Daily working notes |

Optional subdirectories:
- `memory/projects/` — per-project context
- `memory/system/` — system configuration notes
- `memory/groups/` — team/group context

## 2) Enable memory search in OpenClaw config

Add under `agents.defaults.memorySearch` in your config file:

json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "local",
        "includeDefaultMemory": true,
        "maxResults": 20,
        "minScore": 0.3
      }
    }
  }
}
| Option | Default | Description |
|--------|---------|-------------|
| `provider` | `local` | Backend: `local`, `openai`, `gemini`, `voyage`, `mistral` |
| `includeDefaultMemory` | `true` | Index `MEMORY.md` and `memory/**/*.md` |
| `maxResults` | `20` | Max results returned per query |
| `minScore` | `0.3` | Minimum relevance score (lower = broader matches) |

For remote providers, set the corresponding API key via environment variable or `memorySearch.remote.apiKey`.

## 3) Restart and verify

After modifying config:

bash
# Restart the gateway
openclaw gateway restart

# Verify memory is active
openclaw status
openclaw memory status   # if available in your CLI build
## 4) Test recall behavior

Ask a question about past context, then verify:

1. Agent runs `memory_search` automatically
2. Agent uses `memory_get` for precise lines when needed
3. Agent cites source path and line numbers in response

Example test question: *"What was our decision about X in the last meeting?"*

## 5) Troubleshooting

### `memory_search` not available
- Confirm `agents.defaults.memorySearch.enabled = true` is set
- Check that policy allows memory tools
- Restart the gateway after any config change

### Low-quality matches
- Lower `minScore` to `0.1` or `0.2` for broader hits
- Raise `maxResults` to `30` or higher
- Write more specific notes with concrete details (dates, names, decisions)

### Local provider not working
- Verify local model path and settings
- Switch to a remote provider and set API key if local issues persist

## 6) Operating rule

Before answering questions about prior work, decisions, dates, people, preferences, or todos:

1. Run `memory_search` first
2. Run `memory_get` second (fetch only the needed lines)
3. State that you checked memory if confidence is still low

This keeps responses grounded and auditable.
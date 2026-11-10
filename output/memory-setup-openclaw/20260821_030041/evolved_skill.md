---
name: memory-setup
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
---

# Memory Setup (OpenClaw)

Set up durable memory for OpenClaw so the agent can recall prior decisions, preferences, and todos across sessions.

## 1) Prepare Workspace Files

In your workspace root, maintain these files:

| File | Purpose |
|------|---------|
| `MEMORY.md` | Curated long-term memory — decisions, preferences, key context |
| `memory/YYYY-MM-DD.md` | Daily working notes — todos, progress, blockers |

Optional subdirectories:
- `memory/projects/` — per-project context
- `memory/system/` — system configuration notes
- `memory/groups/` — team/group context

**File naming**: Use lowercase, hyphenated names for `memory_search` compatibility.

## 2) Configure Memory Search

Add memory search settings to your OpenClaw config file under **`agents.defaults.memorySearch`**.

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
| Setting | Description | Recommended |
|---------|-------------|-------------|
| `provider` | Search backend | `local` (default), `openai`, `gemini`, `voyage`, `mistral` |
| `includeDefaultMemory` | Index `MEMORY.md` + `memory/**/*.md` | `true` |
| `maxResults` | Max results returned | `20` (adjust as needed) |
| `minScore` | Relevance threshold (0–1) | `0.3` (lower = more matches) |

**Remote providers**: If using `openai`, `gemini`, etc., set the corresponding API key via environment variable or `memorySearch.remote.apiKey` in config.

## 3) Restart and Verify

After any config change:

bash
# Restart the gateway
openclaw gateway restart

# Verify memory is enabled
openclaw status
openclaw memory status   # if available in your CLI build
Confirm that memory tools appear in the agent's available tool list.

## 4) Test Recall Behavior

Ask a question about past context (e.g., "What did we decide about the auth implementation?"), then verify:

1. Agent runs `memory_search` automatically
2. Agent uses `memory_get` for specific lines when needed
3. Agent cites the source path/line numbers in response

## 5) Troubleshooting

### `memory_search` tool unavailable

- Check config: `agents.defaults.memorySearch.enabled` must be `true` (not top-level `memorySearch`)
- Verify agent policy permits memory tools
- Restart gateway after config changes

### Poor-quality matches or missed context

- Lower `minScore` to `0.15–0.2` for broader matching
- Increase `maxResults` to `30–50`
- Write more specific notes — avoid vague phrases; include dates, names, and exact terms
- Ensure files use consistent naming conventions

### Local provider not working

- Confirm local model path is set correctly in config
- If persistent issues, switch to a remote provider and set the API key

## Recommended Operating Rule

**Before answering any question about prior work, decisions, dates, people, or todos:**

1. Run `memory_search` to locate relevant context
2. Run `memory_get` for specific lines only if precision is needed
3. State that you checked memory if confidence is still uncertain

This ensures responses remain grounded, accurate, and auditable.
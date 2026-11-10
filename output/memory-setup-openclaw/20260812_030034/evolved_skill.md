---
category: software-development
name: memory-setup-openclaw
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
---

# Memory Setup (OpenClaw)

Configure durable memory so the agent can recall prior decisions, preferences, and todos across sessions.

## Prerequisites

- OpenClaw gateway installed
- Access to workspace root directory
- Optional: API key for remote memory providers

## Step 1: Create Workspace Structure

In your workspace root, create these files:

| File | Purpose |
|------|---------|
| `MEMORY.md` | Curated long-term memory, decisions, preferences |
| `memory/YYYY-MM-DD.md` | Daily working notes and todos |

Optional subdirectories:

memory/
├── projects/       # Per-project notes
├── system/         # System configuration, policies
└── groups/         # Team/group context
## Step 2: Configure Memory Search

Add to your OpenClaw config file:

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
**Configuration options:**

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable/disable memory search |
| `provider` | `local` | Search provider: `local`, `openai`, `gemini`, `voyage`, `mistral` |
| `includeDefaultMemory` | `true` | Index `MEMORY.md` and `memory/**/*.md` |
| `maxResults` | `20` | Maximum results to return |
| `minScore` | `0.3` | Minimum relevance score (lower = broader matches) |

**Remote providers:** Set the corresponding API key via environment variable or `memorySearch.remote.apiKey` in config.

## Step 3: Restart and Verify

bash
# Restart the gateway
openclaw gateway restart

# Verify configuration
openclaw status
openclaw memory status
## Step 4: Test Recall

1. Ask a question referencing past context (e.g., "What was decided about X yesterday?")
2. Verify the agent:
   - Runs `memory_search` automatically
   - Uses `memory_get` for specific passages when needed
   - Cites source file paths and line numbers in response

## Troubleshooting

### `memory_search` tool unavailable

- Verify `agents.defaults.memorySearch.enabled` is `true` (not top-level `memorySearch`)
- Check that policies allow memory tool usage
- Restart gateway after config changes

### Poor match quality

- Lower `minScore` to `0.2` for broader matches
- Increase `maxResults` to `30` or higher
- Write more specific, descriptive notes in `MEMORY.md`
- Use consistent terminology across notes

### Local provider not working

- Verify local model path in config
- Fall back to remote provider with API key

### Memory not persisting

- Confirm workspace files exist and are writable
- Check gateway logs for indexing errors

## Operating Rule

Before answering questions about prior work, always:

1. **Search first** — Run `memory_search` with relevant query
2. **Fetch second** — Use `memory_get` only for needed passages
3. **Cite sources** — Reference file paths when useful
4. **Acknowledge gaps** — Say "I checked memory but found nothing relevant" if uncertain

This ensures responses are grounded and auditable.
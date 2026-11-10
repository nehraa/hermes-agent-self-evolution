---
category: software-development
name: memory-setup-openclaw
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
---

# Memory Setup (OpenClaw)

Configure durable memory so the agent can recall prior decisions, preferences, project context, and todos across sessions.

## 1. Prepare Workspace Files

In your workspace root, maintain these files:

| File | Purpose |
|------|---------|
| `MEMORY.md` | Curated long-term memory — key decisions, preferences, recurring context |
| `memory/YYYY-MM-DD.md` | Daily working notes — todos, discussions, progress |

Optional subdirectories:

memory/
├── projects/       # Project-specific notes
├── system/         # System configuration and policies
└── groups/         # Team or group context
**Best practice:** Keep `MEMORY.md` concise and actively curated. Dense, unorganized logs reduce search quality.

## 2. Enable Memory Search

Configure under `agents.defaults.memorySearch` in your OpenClaw config file:

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
| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Activate memory search | `false` |
| `provider` | Search backend: `local`, `openai`, `gemini`, `voyage`, `mistral` | `local` |
| `includeDefaultMemory` | Index `MEMORY.md` and `memory/**/*.md` | `true` |
| `maxResults` | Maximum results to return | `20` |
| `minScore` | Minimum relevance score (0–1, lower = more matches) | `0.3` |

**Remote providers:** Set the corresponding API key via environment variable or `memorySearch.remote.apiKey`.

## 3. Restart and Verify

After changing config, restart the gateway:

bash
# Restart the gateway
openclaw gateway restart

# Verify memory status
openclaw status
openclaw memory status    # if available in your CLI build
Confirm that memory tools (`memory_search`, `memory_get`) are listed as available.

## 4. Test Recall Behavior

Ask a question about past context (e.g., "What was decided about the API design?"), then verify the agent:

1. Invokes `memory_search` with appropriate query
2. Uses `memory_get` for precise line retrieval when needed
3. Cites source file and line numbers in the response

If the agent doesn't check memory for context-related questions, the setup is incomplete.

## 5. Troubleshooting

### memory_search unavailable

1. Verify `agents.defaults.memorySearch.enabled` is `true` (not top-level)
2. Confirm policy grants access to memory tools
3. Restart the gateway after any config change

### Low-quality or missing matches

- **Broaden scope:** Lower `minScore` to `0.2` or `0.1`
- **Increase results:** Raise `maxResults` to `30` or `50`
- **Improve source material:** Write specific, searchable notes in `MEMORY.md` and daily logs
- **Use keywords:** Memory search works better with concrete terms than vague descriptions

### Local provider not working

- Verify local model path and settings in config
- If persistent issues, switch to a remote provider and set the API key

### Remote provider errors

- Confirm API key is set (env var or config)
- Check provider endpoint/region settings
- Verify quota hasn't been exceeded

## 6. Memory Workflow Rule

When answering questions about prior work, decisions, dates, people, preferences, or todos:

1. **Always** call `memory_search` first
2. **Then** call `memory_get` for specific lines if needed
3. **If** confidence is still low after retrieval, explicitly state you checked memory

This ensures responses remain grounded in established context and are auditable.

---

**Quick reference for first-time setup:**

bash
# 1. Create memory files
touch MEMORY.md
mkdir -p memory/$(date +%Y-%m-%d).md

# 2. Add to config (agents.defaults.memorySearch)
# See section 2 above for full config

# 3. Restart
openclaw gateway restart

# 4. Test
openclaw memory status
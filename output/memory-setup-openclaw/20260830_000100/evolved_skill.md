---
category: software-development
name: memory-setup-openclaw
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
---

# Memory Setup (OpenClaw)

Set up durable memory for OpenClaw so the agent can recall prior decisions, preferences, and todos across sessions.

## Prerequisites

- OpenClaw workspace with write access
- Gateway restart capability

## 1) Prepare Workspace Files

Create this structure in your workspace root:

workspace/
├── MEMORY.md                    # Curated long-term memory
└── memory/
    └── YYYY-MM-DD.md            # Daily working notes
**Optional subdirectories:**

memory/
├── projects/                   # Per-project context
├── system/                     # System-level notes
└── groups/                     # Team/group context
**Best practices for content:**

- Use descriptive headings and dates
- Include specific names, dates, decisions, and preferences
- Update daily logs after significant work sessions
- Keep `MEMORY.md` curated — extract key decisions from daily logs

## 2) Enable Memory Search in OpenClaw Config

Add or update your OpenClaw config file (e.g., `openclaw.config.json` or `.openclawrc`):

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
### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `false` | Toggle memory search on/off |
| `provider` | `local` | Search provider: `local`, `openai`, `gemini`, `voyage`, `mistral` |
| `includeDefaultMemory` | `true` | Index `MEMORY.md` and `memory/**/*.md` |
| `maxResults` | `20` | Maximum matches to return |
| `minScore` | `0.3` | Minimum relevance threshold (0.0–1.0) |

### Remote Provider Setup

If using a remote provider, set the API key:

json
{
  "memorySearch": {
    "remote": {
      "apiKey": "${OPENAI_API_KEY}"
    }
  }
}
Or via environment variable (provider-specific):

bash
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
## 3) Restart and Verify

After modifying config, restart the gateway:

bash
# Restart the gateway
openclaw gateway restart

# Verify memory status
openclaw status
openclaw memory status
**Expected output:** Memory search should show as `enabled` with your configured provider.

## 4) Test Recall Behavior

Verify the agent uses memory correctly:

1. Ask a question about past context (e.g., "What was decided about the API design?")
2. Confirm the agent:
   - Runs `memory_search` with appropriate query
   - Uses `memory_get` for precise line retrieval when needed
   - Cites source file and line numbers in response

**Example verification:**

bash
# Direct test via CLI (if available)
openclaw memory search "API design decisions"
## 5) Troubleshooting

### `memory_search` returns empty or unavailable

1. Verify config: `agents.defaults.memorySearch.enabled = true`
2. Check agent policy allows memory tools
3. Restart gateway after config changes
4. Run `openclaw memory status` to confirm indexing

### Low-quality or irrelevant matches

- **Lower** `minScore` (try `0.2` or `0.15`) to broaden results
- **Raise** `maxResults` (try `30` or `40`) for more candidates
- Improve note specificity — add names, dates, and context
- Check that relevant files exist in `MEMORY.md` or `memory/`

### Local provider not working

1. Verify local model path in config
2. Confirm sufficient disk space for index
3. Try switching to a remote provider temporarily:
   ```json
   "provider": "openai"
   ```

### Memory not persisting between sessions

- Ensure `includeDefaultMemory: true`
- Confirm `memory/` directory exists and is committed/persisted
- Check workspace is not ephemeral (container, temp dir)

## 6) Operating Rule

Before answering questions about prior work, always:

1. **Run `memory_search`** with relevant query
2. **Run `memory_get`** for precise lines (if needed)
3. **Cite sources** — include file path and line numbers when helpful

If recall confidence is low after searching:

markdown
I searched memory but didn't find a clear answer about [topic]. 
I checked MEMORY.md and memory/*.md. Let me know if you have 
more context or if this was recent work not yet documented.
This keeps responses grounded, auditable, and accurate.
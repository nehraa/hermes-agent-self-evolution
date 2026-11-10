---
category: software-development
name: memory-setup-openclaw
description: Configure and validate OpenClaw memory recall for persistent context. Use when enabling memory_search/memory_get, fixing poor memory recall, or setting up MEMORY.md + memory/*.md workflows in an OpenClaw workspace.
---

# Memory Setup (OpenClaw)

Set up durable memory for OpenClaw so the agent can recall prior decisions, preferences, and todos across sessions.

## Overview

OpenClaw memory consists of two layers:

| Layer | File | Purpose |
|-------|------|---------|
| Long-term | `MEMORY.md` | Curated, manually maintained knowledge |
| Ephemeral | `memory/YYYY-MM-DD.md` | Daily working notes and context |

When enabled, the agent searches both layers before answering questions about past work.

---

## 1) Create workspace files

In your workspace root, create these files:

MEMORY.md
memory/
memory/YYYY-MM-DD.md   # Created daily during sessions
### Optional structure

memory/
memory/projects/       # Per-project notes
memory/system/         # System-wide decisions
memory/groups/         # Team/group context
**Best practice:** Keep `MEMORY.md` lean. Write context there once it proves useful over multiple sessions. Add daily notes liberally during work.

---

## 2) Configure memory search

Edit your OpenClaw config file (typically `.openclaw/config.json` or `~/.openclaw/config.json`):

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
### Configuration options

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `false` | Enable memory search globally |
| `provider` | `local` | Search provider (see below) |
| `includeDefaultMemory` | `true` | Index `MEMORY.md` and `memory/**/*.md` |
| `maxResults` | `20` | Maximum results to return |
| `minScore` | `0.3` | Minimum relevance score (0–1) |

### Supported providers

| Provider | API Key Env Var | Notes |
|----------|-----------------|-------|
| `local` | — | Uses local embedding model |
| `openai` | `OPENAI_API_KEY` | OpenAI embeddings |
| `gemini` | `GEMINI_API_KEY` | Google Gemini |
| `voyage` | `VOYAGE_API_KEY` | Voyage AI |
| `mistral` | `MISTRAL_API_KEY` | Mistral AI |

**Remote providers:** Set the API key in your environment or add it to config:

json
{
  "memorySearch": {
    "provider": "openai",
    "remote": {
      "apiKey": "sk-..."
    }
  }
}
---

## 3) Restart and verify

### Restart the gateway

Changes require a gateway restart:

bash
openclaw gateway restart
# or
systemctl --user restart openclaw
### Verify configuration

bash
openclaw status
Check that memory search appears as enabled.

### Verify indexing (optional)

bash
openclaw memory status
This shows indexed files and document count. Expected output should list `MEMORY.md` and recent `memory/*.md` files.

---

## 4) Test recall behavior

After setup, verify the agent uses memory correctly:

1. **Ask a contextual question** — e.g., "What did we decide about the authentication flow?"
2. **Confirm the agent runs `memory_search`** — Should appear in tool calls
3. **Confirm `memory_get` for specifics** — When exact lines are needed
4. **Check citations** — Agent should cite source paths when useful

**Expected workflow:**

You: What was our decision on error handling?
Agent: [runs memory_search]
Agent: [runs memory_get on relevant files]
Agent: Based on memory, we decided to use typed errors
      (see memory/2024-01-15.md:45-52)
If `memory_search` doesn't appear, check troubleshooting below.

---

## 5) Troubleshooting

### `memory_search` not appearing in tool calls

1. Verify config: `agents.defaults.memorySearch.enabled` must be `true`
2. Check policy: Ensure memory tools are allowed in your agent policy
3. Restart gateway: `openclaw gateway restart`
4. Verify API key: If using remote provider, confirm env var is set

bash
# Verify env var is accessible to the gateway process
echo $OPENAI_API_KEY
### Low-quality or missing matches

**Tune thresholds:**

json
{
  "memorySearch": {
    "minScore": 0.2,
    "maxResults": 30
  }
}
**Improve content:**

- Write more specific notes (include dates, names, decisions)
- Use consistent terminology across notes
- Add context to `MEMORY.md` about important past decisions
- Delete outdated notes that cause noise

### Local provider issues

1. Verify local model is installed and path is correct
2. Check model format compatibility
3. Fall back to remote provider if local continues failing:

json
{
  "memorySearch": {
    "provider": "openai",
    "remote": {
      "apiKey": "sk-..."
    }
  }
}
### Config changes not taking effect

- Ensure the config file being edited is the one the gateway loads
- Check for syntax errors: config must be valid JSON
- Confirm restart completed successfully
- Check gateway logs for config parse errors

---

## 6) Operating rule

Before answering questions about prior work, **always consult memory first**:

1. memory_search  → Find relevant files
2. memory_get     → Extract precise lines (if needed)
3. State what you found from memory (or that nothing was found)
**When to check memory:**

- Decisions and their rationale
- Dates and deadlines mentioned
- Names of people and their roles
- Preferences expressed by the user
- Open todos and their status
- Project-specific context

**Confidence check:** If memory search returned results but you're unsure, say so: "I found notes mentioning X, but I'm uncertain if that reflects current decisions."

---

## Quick Reference

### File locations

~/workspace/
├── MEMORY.md                    # Long-term curated memory
└── memory/
    ├── 2024-01-15.md            # Daily notes
    ├── projects/
    └── system/
### Config template

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
### Common commands

bash
openclaw gateway restart       # Apply config changes
openclaw status                 # Check status
openclaw memory status          # Check indexing
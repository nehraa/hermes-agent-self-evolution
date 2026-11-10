---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## What It Does

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses **spreading activation** through a neural graph — memories that fire together, wire together.

When you recall a memory, related memories activate automatically. A decision made six months ago about authentication architecture surfaces not because you searched for "auth" but because you're working on a feature that triggers that memory cluster.

## Key Features

### Core Memory Operations
- **45 MCP tools** for persistent memory and cognitive reasoning
- **Spreading activation recall** — activates related memories, not just exact matches
- **Fernet encryption** for sensitive content

### Knowledge Ingestion
- Train from PDF, DOCX, PPTX, HTML, JSON, XLSX, CSV files
- **4 embedding providers** — Sentence Transformers, Gemini, Ollama, OpenAI

### Retrieval Pipeline
- RRF (Reciprocal Rank Fusion) score fusion
- Graph expansion for context
- Personalized PageRank for relevance scoring

### Cognitive Reasoning
- Hypothesis generation
- Evidence chains
- Predictions
- Schema evolution

### Session Intelligence
- Topic EMA (Exponential Moving Average) tracking
- LRU eviction for storage management
- Auto-expiry of stale memories

### Sync & Backup
- **Multi-device sync** with neural-aware conflict resolution
- **Telegram backup** — send brain .db to chat, group, or channel
- **Brain versioning** — snapshots, rollback, export/import

### Developer Experience
- **React dashboard** (7 pages): health, evolution, graph, timeline, settings
- **VS Code extension**: status bar, graph explorer, CodeLens, memory tree

## Installation

bash
pip install neural-memory
With embeddings:

bash
pip install neural-memory[embeddings]
## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

json
{
  "mcpServers": {
    "neural-memory": {
      "command": "uvx",
      "args": ["--from", "neural-memory", "nmem-mcp"]
    }
  }
}
## Usage

Neural Memory operates in two phases: **recall** before tasks, **save** after meaningful events.

### RECALL — Before Responding to Tasks

Use `nmem_recall()` to activate relevant memories before starting work.

python
# New project or unclear context
nmem_recall("current project state and recent decisions")

# Specific reference to past work
nmem_recall("<project-name> <topic>")

# Skip for: purely new questions with no prior context
**When to recall:**
- Starting work on a feature you haven't touched recently
- Responding to a question about past decisions
- Debugging an issue that might relate to previous changes
- Any task that references "the thing we did before" or "remember when"

**When to skip:**
- New, self-contained questions with no history
- Pure creative tasks with no prior context needed

### SAVE — After Completing Tasks

Use `nmem_remember()` after any event worth remembering.

python
nmem_remember(
    content="Chose PostgreSQL over MongoDB because we needed ACID compliance for financial transactions",
    type="decision",
    priority=7,
    tags=["database", "architecture", "project-name"]
)
**What to save:**
- Decisions and the reasoning behind them
- Bug fixes and their root causes
- User preferences and project conventions
- Patterns discovered through work
- Lessons learned

**How to write memories:**
- Use causal language ("because", "in order to", "since")
- Keep to 1-3 sentences
- Focus on *why*, not just *what*

**Priority scale:**
- 1-3: Routine context (naming conventions, style preferences)
- 4-6: Important decisions (architecture choices, feature flags)
- 7-10: Critical knowledge (security decisions, breaking changes, client constraints)
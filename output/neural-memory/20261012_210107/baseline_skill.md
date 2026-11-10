---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## What It Does

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses **spreading activation** through a neural graph — memories that fire together, wire together.

When you recall one memory, related memories activate automatically, just like how thinking of "coffee" brings up related concepts like "morning," "caffeine," or "break room."

## Key Features

### Core Memory
- **45 MCP tools** for persistent memory operations and cognitive reasoning
- **Spreading activation recall** — activates related memories automatically, not keyword search
- **Fernet encryption** for sensitive content
- **Brain versioning** — snapshots, rollback, export/import

### Cognitive Reasoning
- Hypothesis generation and evidence tracking
- Prediction with confidence scores
- Schema evolution as knowledge grows

### Knowledge Ingestion
- Train from **PDF, DOCX, PPTX, HTML, JSON, XLSX, CSV**
- Automatic entity extraction and relationship mapping

### Retrieval Pipeline
- **RRF score fusion** (Reciprocal Rank Fusion)
- **Graph expansion** — traverse related nodes
- **Personalized PageRank** — rank by relevance to query context

### Embedding Providers
- Sentence Transformers (local)
- Gemini
- Ollama
- OpenAI

### Session Intelligence
- Topic EMA (Exponential Moving Average) tracking
- LRU eviction for memory efficiency
- Auto-expiry for stale entries

### Sync & Backup
- **Multi-device sync** with neural-aware conflict resolution
- **Telegram backup** — send brain .db to chat/group/channel

### Extensions
- **React dashboard** — 7 pages: health, evolution, graph, timeline, settings
- **VS Code extension** — status bar, graph explorer, CodeLens, memory tree

## Installation

bash
# Core installation
pip install neural-memory

# With embedding support
pip install neural-memory[embeddings]
## MCP Configuration

Add to your MCP client config (Claude Desktop, Cursor, etc.):

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

### Before Responding (RECALL)

Use `nmem_recall()` before tasks that reference past work:

python
# New session — load project context
nmem_recall("current project architecture")

# Find past decisions or events
nmem_recall("<project> <topic>")

# Skip for purely new, self-contained questions
### After Completing Tasks (SAVE)

Use `nmem_remember()` after tasks that involve decisions, fixes, or discoveries:

python
nmem_remember(
    content="Chose X over Y because Z",
    type="decision",
    priority=7,
    tags=["project", "topic"]
)
**Tips:**
- Use causal language ("because", "since", "decided to") not flat facts
- Keep entries to 1-3 sentences
- Include relevant context: project name, user preferences, trade-offs considered

## Quick Examples

| Scenario | Action |
|----------|--------|
| User asks about past project decision | `nmem_recall("auth refactor decision")` |
| Fixed a tricky bug | `nmem_remember(type="fix", content="Root cause was X, solution was Y", tags=["bug", "api"])` |
| Learned user preference | `nmem_remember(type="preference", content="Prefers verbose logging in prod", priority=9)` |
| Completed feature | `nmem_remember(type="pattern", content="Used strategy pattern for extensible validators", tags=["design"])` |
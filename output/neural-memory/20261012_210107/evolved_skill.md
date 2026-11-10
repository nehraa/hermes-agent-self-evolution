---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## Overview

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses **spreading activation** through a neural graph — memories that fire together, wire together.

When you recall one memory, related memories activate automatically, just like how thinking of "coffee" brings up related concepts like "morning," "caffeine," or "break room."

## Key Features

### Core Memory Operations
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
- **RRF score fusion** (Reciprocal Rank Fusion) — combines multiple ranking strategies
- **Graph expansion** — traverse related nodes for context
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

# With all providers
pip install neural-memory[all]
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
## Quick Start

python
from neural_memory import Brain

# Initialize brain
brain = Brain()

# Store a memory
brain.remember("User prefers dark mode", context={"user_id": "123"})

# Recall with spreading activation
memories = brain.recall("appearance preferences")
# Returns related memories: dark mode, theme, display settings, etc.

# Encrypt sensitive content
brain.remember("passwords", encrypted=True)
## Architecture

┌─────────────────────────────────────────────────┐
│                   MCP Tools (45)                │
├──────────┬──────────┬──────────┬────────────────┤
│  Store  │  Recall  │  Reason  │  Ingest        │
├──────────┴──────────┴──────────┴────────────────┤
│              Graph Engine                        │
│         (Spreading Activation)                   │
├─────────────────────────────────────────────────┤
│   Embeddings   │   Encryption   │   Sync       │
└─────────────────────────────────────────────────┘
## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NMEM_DB_PATH` | Path to brain database | `./brain.db` |
| `NMEM_EMBED_PROVIDER` | Embedding provider | `local` |
| `NMEM_TELEGRAM_BOT` | Telegram bot token | - |
| `NMEM_ENCRYPTION_KEY` | Fernet encryption key | auto-generated |

## License

MIT License
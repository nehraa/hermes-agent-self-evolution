---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## Overview

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses **spreading activation** through a neural graph — memories that fire together, wire together.

When you recall a memory, related memories activate automatically. This mirrors how the human brain retrieves information contextually rather than through exact matches.

## Installation

bash
pip install neural-memory
For embedding support (recommended):

bash
pip install neural-memory[embeddings]
## MCP Configuration

Add to your MCP configuration file:

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

### When to RECALL

**Before responding to any task that references past work**, call:

python
# New session or current project context
nmem_recall("current project context")

# Specific past decision or event
nmem_recall("<project> <topic>")
**Skip recall** for purely new, self-contained questions.

### When to SAVE

**After completing each task**, save decisions, fixes, preferences, or patterns:

python
nmem_remember(
    content="Chose X over Y because Z",
    type="decision",
    priority=7,
    tags=["project", "topic"]
)
**Guidelines:**
- Use causal language (why something happened), not flat facts
- Keep entries to 1-3 sentences
- Tag with project and topic for better retrieval

## Key Features

### Memory & Cognition
- **45 MCP tools** for persistent memory and cognitive reasoning
- **Spreading activation recall** — activates related memories through neural graph connections
- **Cognitive reasoning** — supports hypotheses, evidence, predictions, and schema evolution

### Knowledge Ingestion
- **Training from multiple formats**: PDF, DOCX, PPTX, HTML, JSON, XLSX, CSV

### Retrieval & Ranking
- **RRF score fusion** for combining multiple retrieval signals
- **Graph expansion** — expands query context through connected nodes
- **Personalized PageRank** — ranks memories by relevance to user context

### Embedding Providers
- Sentence Transformers
- Gemini
- Ollama
- OpenAI

### Session Intelligence
- **Topic EMA tracking** — exponential moving average for topic relevance
- **LRU eviction** — automatically removes least recently used memories when space is needed
- **Auto-expiry** — configurable TTL for time-sensitive information

### Sync & Security
- **Multi-device sync** with neural-aware conflict resolution
- **Fernet encryption** for sensitive content

### Brain Management
- **Versioning** — snapshots, rollback, export/import
- **Telegram backup** — send brain .db to chat, group, or channel

## Dashboard & Extensions

- **React dashboard** (7 pages): health, evolution, graph, timeline, settings
- **VS Code extension**: status bar, graph explorer, CodeLens, memory tree
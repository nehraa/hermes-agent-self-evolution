---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## Overview

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses **spreading activation** through a neural graph — memories that fire together, wire together. The system continuously evolves, connecting new experiences to past knowledge and surfacing relevant context proactively.

## Quick Start

### Installation

bash
pip install neural-memory
Or with all embedding providers:

bash
pip install neural-memory[embeddings]
### MCP Configuration

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
## Core Usage

Neural Memory operates on two simple reflexes:

### RECALL — Before Responding to Contextual Tasks

Use `nmem_recall()` to activate relevant memories before answering:

| Situation | Example Call |
|-----------|--------------|
| New project session | `nmem_recall("current project context")` |
| Question about past work | `nmem_recall("<project> <topic>")` |
| Debugging or planning | `nmem_recall("relevant decisions, patterns, preferences")` |

**Skip recall** for purely new, self-contained questions — no prior context needed.

### SAVE — After Completing Meaningful Work

Use `nmem_remember()` to persist insights:

python
nmem_remember(
    content="Chose X over Y because Z resulted in 40% faster builds",
    type="decision",
    priority=7,
    tags=["project", "performance", "architecture"]
)
**Guidelines:**
- Use causal language ("Chose X because..." not "Used X")
- One to three sentences maximum
- Include the *reason* or *outcome*, not just the fact
- Tag by project and topic for effective spreading activation

## Key Features

### Memory & Recall
- **45 MCP tools** for persistent memory operations
- **Spreading activation recall** — related memories activate automatically
- **Session intelligence** — topic EMA tracking, LRU eviction, auto-expiry

### Knowledge Management
- **Training** from PDF, DOCX, PPTX, HTML, JSON, XLSX, CSV
- **Cognitive reasoning** — hypotheses, evidence, predictions, schema evolution
- **Knowledge base** — RRF score fusion, graph expansion, Personalized PageRank

### Embedding & Sync
- **4 embedding providers** — Sentence Transformers, Gemini, Ollama, OpenAI
- **Multi-device sync** with neural-aware conflict resolution
- **Fernet encryption** for sensitive content

### Versioning & Backup
- **Brain versioning** — snapshots, rollback, export/import
- **Telegram backup** — send brain .db to chat, group, or channel

### Visualization & IDE
- **React dashboard** — 7 pages: health, evolution, graph, timeline, settings
- **VS Code extension** — status bar, graph explorer, CodeLens, memory tree

## System Architecture

┌─────────────────────────────────────────────────────────────┐
│                    Neural Memory System                      │
├─────────────────────────────────────────────────────────────┤
│  Input Layer                                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │  PDF    │ │  DOCX   │ │  Code   │ │  Chat   │            │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │
│       └──────────┬┴──────────┬┴──────────┘                  │
│                   ▼                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Embedding Pipeline                      │    │
│  │   [Provider Selection] → [Vectorization] → [Index]  │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Neural Graph Store                      │    │
│  │   Nodes (memories) ←→ Edges (associations)          │    │
│  │   Spreading Activation + PageRank Scoring           │    │
│  └────────────────────────┬────────────────────────────┘    │
│                           ▼                                   │
│  Output Layer                                                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │ Recall  │ │ Reason  │ │ Predict │ │ Export  │            │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘            │
└─────────────────────────────────────────────────────────────┘
## Memory Types

| Type | Use Case | Example |
|------|----------|---------|
| `decision` | Architectural choices, tool selection | "Used PostgreSQL because X" |
| `pattern` | Recurring solutions, anti-patterns | "X always fails when Y" |
| `preference` | User style, team conventions | "Prefers verbose logging" |
| `context` | Project state, current blockers | "Migrating from X to Y" |
| `insight` | Learned relationships, discoveries | "X correlates with Y in Z" |

## API Reference

### nmem_recall

python
nmem_recall(query: str, depth: int = 2, limit: int = 10) -> List[Memory]
Recalls memories using spreading activation. Higher depth activates more distant associations.

### nmem_remember

python
nmem_remember(
    content: str,
    type: str = "insight",
    priority: int = 5,
    tags: List[str] = [],
    metadata: dict = {}
) -> str  # Returns memory ID
Stores a memory with the specified priority (1-10) and tags for association.

### nmem_search

python
nmem_search(query: str, filters: dict = {}) -> List[Memory]
Hybrid search combining semantic similarity with graph proximity.

## Best Practices

1. **Recall early, save often** — Check for relevant context before tasks; persist insights after
2. **Prioritize decisions** — Architectural choices have the highest recall value
3. **Use specific tags** — Consistent tagging improves spreading activation
4. **Include outcomes** — Always note *why* something worked or failed
5. **Review periodically** — Check the dashboard to understand memory evolution

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow recall | Reduce depth parameter or check embedding provider latency |
| Missing memories | Verify tags match your recall queries |
| Sync conflicts | System uses neural-aware resolution; check dashboard for resolution history |
| Encryption errors | Verify Fernet key is correctly configured in settings |
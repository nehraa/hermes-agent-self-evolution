---
category: software-development
description: "Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works."
name: neural-memory
---

# Neural Memory

Reflex-based memory system for AI agents — stores experiences as interconnected neurons and recalls them through spreading activation, mimicking how the human brain works.

## Overview

Neural Memory gives AI agents persistent, associative memory across sessions. Instead of keyword search, it uses spreading activation through a neural graph — memories that fire together, wire together.

## Key Features

**Memory & Recall**
- **45 MCP tools** for persistent memory and cognitive reasoning
- **Spreading activation recall** — memories activate related memories; not keyword search
- **Cognitive reasoning** — hypotheses, evidence, predictions, schema evolution
- **RRF score fusion + graph expansion + Personalized PageRank** retrieval pipeline

**Knowledge Ingestion**
- Train from **PDF, DOCX, PPTX, HTML, JSON, XLSX, CSV** files
- **4 embedding providers**: Sentence Transformers, Gemini, Ollama, OpenAI

**Session Intelligence**
- Topic EMA tracking — monitors conversation themes over time
- LRU eviction — least recently used memory pruning
- Auto-expiry — memories fade based on relevance decay

**Sync & Security**
- Multi-device sync with neural-aware conflict resolution
- **Fernet encryption** for sensitive content
- **Brain versioning** — snapshots, rollback, export/import
- **Telegram backup** — send brain .db to chat/group/channel

**Visualization & IDE**
- **React dashboard** (7 pages): health, evolution, graph, timeline, settings
- **VS Code extension** — status bar, graph explorer, CodeLens, memory tree

## Installation

bash
pip install neural-memory
For embedding support:

bash
pip install neural-memory[embeddings]
## MCP Configuration

Add to your MCP client configuration (`claude_desktop_config.json` or equivalent):

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

Neural Memory works automatically once configured. Use these patterns to leverage it effectively.

### RECALL — Before Responding to Tasks

Call `nmem_recall()` when a task references past work, previous decisions, or established patterns:

python
# New session with existing project context
nmem_recall("current project status and recent decisions")

# Reference specific past decision or event
nmem_recall("backend-api refactoring decisions")

# Skip for purely new, self-contained questions
**When to recall:**
- User mentions "the same issue as before" or "continue where we left off"
- Project-specific terminology or custom patterns
- Previous solutions that worked or failed

### SAVE — After Completing Tasks

Call `nmem_remember()` when you make a decision, fix a bug, learn a preference, or discover a pattern:

python
nmem_remember(
    content="Chose PostgreSQL over MongoDB because the data relationships were too complex for document storage",
    type="decision",
    priority=7,
    tags=["backend", "database", "project-name"]
)
**Guidelines:**
- Use causal language (explains *why*) — not flat facts
- Keep it to 1-3 sentences
- Tag with project name and relevant topics
- Set priority 1-10 based on importance (decisions affecting architecture = 8-10)

**What to remember:**
- Architectural decisions and the reasoning behind them
- Bug fixes that weren't obvious
- User preferences and project conventions
- Patterns that worked or failed in similar contexts
- Configuration values that were tricky to discover

### Querying Your Memory

python
# Find all decisions for a specific project
nmem_query(filter_type="decision", tags=["project-name"])

# Find similar past experiences
nmem_recall_similar("error handling patterns")

# Get memory graph for a topic
nmem_graph("authentication implementation")
## Available MCP Tools

Core memory operations: `nmem_remember`, `nmem_recall`, `nmem_query`, `nmem_forget`, `nmem_merge`

Reasoning: `nmem_hypothesize`, `nmem_evaluate_evidence`, `nmem_predict`, `nmem_evolve_schema`

Knowledge: `nmem_train_file`, `nmem_train_url`, `nmem_index_document`, `nmem_import_knowledge_base`

Sync: `nmem_sync`, `nmem_backup_telegram`, `nmem_export`, `nmem_import`, `nmem_version_list`, `nmem_version_restore`
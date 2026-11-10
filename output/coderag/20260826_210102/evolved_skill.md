---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query

## Overview

Local Retrieval-Augmented Generation (RAG) for querying any codebase. Indexes code using tree-sitter for multi-language parsing, stores vector embeddings in LanceDB, retrieves relevant nodes with surrounding context via graph traversal, and optionally generates natural language answers via LLM.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust

## When to Use

- **Code exploration:** "What does this file do?", "Where is auth handled?"
- **Code archaeology:** "Find all files related to X", "How does job polling work?"
- **Code review:** "Explain this function", "What are the dependencies here?"
- **Quick context:** When Claude Code needs to understand an unfamiliar codebase

## Installation & Setup

bash
# Install globally
npm install -g @abhinav2203/coderag

# Verify installation
npm list -g @abhinav2203/coderag
**Global binary location:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Quick Start

bash
# 1. Initialize a repository (creates config + indexes)
cd /path/to/repo
coderag init

# 2. Query the codebase
coderag query "how does authentication work"     # Semantic search
coderag retrieve "find the user controller"       # Retrieve relevant nodes
coderag answer "explain the payment flow"         # LLM-powered answers

# 3. Keep index updated when code changes
coderag update
## Workflow

| Step | Command | Purpose |
|------|---------|---------|
| Initialize | `coderag init` | Create config, index files, generate embeddings, store in LanceDB |
| Query | `coderag query <text>` | Semantic similarity search across indexed code |
| Retrieve | `coderag retrieve <text>` | Retrieve relevant code nodes directly |
| Answer | `coderag answer <text>` | Generate natural language answer via LLM |
| Update | `coderag update` | Re-index changed files only |

## Configuration

### Config File Resolution (first match wins)

1. Explicit `--config <path>` flag
2. `coderag.config.json` in repo root
3. `.coderag.json` in repo root
4. `.env` file values
5. Environment variable overrides

### Minimal Config (Gemini Cloud)

json
{
  "embedding": {
    "provider": "gemini"
  }
}
### Full Config Example

json
{
  "embedding": {
    "provider": "gemini",
    "dimensions": 768
  },
  "llm": {
    "provider": "minimax",
    "model": "MiniMax-Text-01",
    "apiKey": "your_key_here",
    "baseUrl": "https://api.minimax.chat/v1"
  },
  "indexing": {
    "languages": ["typescript", "javascript", "python"],
    "exclude": ["node_modules", "dist", "*.test.ts"]
  }
}
### Embedding Providers

| Provider | Description |
|----------|-------------|
| `gemini` | Google Gemini embeddings (cloud) |
| `onnx` | Local ONNX embeddings (no API key needed) |

### LLM Providers

| Provider | Description |
|----------|-------------|
| `minimax` | MiniMax Chat API |
| `mcp` | MCP protocol integration |
| `http` | Generic HTTP endpoint |

## Indexing Details

- **Parser:** tree-sitter for language-aware AST extraction
- **Storage:** LanceDB for vector storage and similarity search
- **Context:** Graph traversal provides surrounding code context
- **Incremental:** `coderag update` indexes only changed files
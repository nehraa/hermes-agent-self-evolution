---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query Tool

## What It Does

Local Retrieval-Augmented Generation (RAG) for querying any codebase. Coderag indexes your code using tree-sitter for multi-language AST analysis, stores node documents in LanceDB for fast similarity search, and optionally generates natural language answers via LLM.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust

## When to Use

- **Code exploration:** "What does this function do?", "Where is the auth middleware?"
- **Code archaeology:** "Find all files related to payment processing", "How is job polling implemented?"
- **Code review:** "Explain this file/module", "What are the dependencies here?"
- **Context injection:** Retrieve relevant code snippets to pass to other AI tools or LLMs

## Installation

bash
# Install globally
npm install -g @abhinav2203/coderag

# Verify installation
npm list -g @abhinav2203/coderag
coderag --version
**Binary location:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Quick Start

bash
# 1. Initialize a repository (creates .coderag.json and indexes all code)
cd /path/to/your/repo
coderag init

# 2. Query the codebase
coderag query "how does authentication work"          # Semantic search
coderag retrieve "find the user controller"            # Retrieve code nodes
coderag answer "explain the payment flow"              # LLM-generated answer

# 3. Update index when code changes
coderag init    # Full reindex
coderag update  # Incremental update
## Command Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `coderag init` | Index repository (full reindex) | Progress, file count, index location |
| `coderag update` | Incremental index update | Changed files count |
| `coderag query <text>` | Semantic similarity search | Ranked code nodes with scores |
| `coderag retrieve <text>` | Retrieve relevant code nodes | File paths, line numbers, code snippets |
| `coderag answer <text>` | LLM-powered Q&A | Natural language explanation + citations |

## Configuration

### Config File Resolution (priority order)

1. `--config <path>` flag (explicit path)
2. `coderag.config.json` in repo root
3. `.coderag.json` in repo root
4. `.env` file
5. Environment variables

### Minimal Config (Gemini Cloud Embeddings)

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
    "languages": ["typescript", "javascript", "python", "go", "rust"],
    "exclude": [
      "node_modules",
      "dist",
      "build",
      ".git",
      "*.test.ts",
      "*.spec.ts"
    ],
    "maxFileSize": 1048576
  },
  "retrieval": {
    "topK": 10,
    "minScore": 0.6
  }
}
### Embedding Providers

| Provider | Config Key | Notes |
|----------|------------|-------|
| Gemini | `"gemini"` | Cloud API, requires `GEMINI_API_KEY` |
| ONNX Local | `"onnx"` | Runs locally, no API key needed |

### LLM Providers

| Provider | Config Key | Notes |
|----------|------------|-------|
| MiniMax | `"minimax"` | Cloud API, set `apiKey` in config |
| MCP | `"mcp"` | Connect via MCP protocol |
| HTTP | `"http"` | Custom HTTP endpoint |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Gemini API key for embeddings | For Gemini provider |
| `MINIMAX_API_KEY` | MiniMax API key for LLM | For MiniMax provider |

## Index Location

Index data is stored in `.coderag/` directory within the repository:
- `index.lance` — LanceDB vector index
- `config.json` — Index configuration and metadata

## Troubleshooting

bash
# Reinitialize if index is corrupted
coderag init --force

# Check config
coderag config --show

# Verbose output for debugging
coderag query "your query" --verbose

# Clear and rebuild index
rm -rf .coderag/
coderag init
## Use with Claude Code

Coderag integrates well with Claude Code for exploring unfamiliar codebases:

bash
# Get context for a specific feature
coderag retrieve "where is the rate limiting logic"

# Ask for explanation
coderag answer "how does the caching layer work"

# Use retrieved code in Claude Code prompts
coderag query "JWT token validation" --format markdown
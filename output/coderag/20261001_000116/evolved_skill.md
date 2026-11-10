---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query Tool

## Overview

**coderag** is a local Retrieval-Augmented Generation (RAG) system for querying codebases. It indexes source code, stores semantic embeddings in LanceDB, and retrieves relevant code context. Optionally, it can use an LLM to answer questions in natural language.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust

## When to Use

Use coderag when you need to:

- **Understand unfamiliar code** — "What does this function do?", "How is this module structured?"
- **Locate features** — "Where is authentication handled?", "Find all files related to X"
- **Trace logic flows** — "How does the job polling work?", "What happens during payment processing?"
- **Code archaeology** — "Find all usages of this API", "What modules touch the database?"
- **Speed up context gathering** — Quickly get relevant code snippets before writing or reviewing

## Installation

bash
# Install globally
npm install -g @abhinav2203/coderag

# Verify installation
npm list -g @abhinav2203/coderag
**Binary location:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Quick Start

bash
# Navigate to your repository
cd /path/to/your/repo

# Initialize indexing (creates .coderag.json and builds the vector store)
coderag init

# Query with different modes
coderag query "how does authentication work"      # Semantic search
coderag retrieve "find the user controller"        # Retrieve code nodes
coderag answer "explain the payment flow"         # LLM-powered answer
## Commands

| Command | Purpose |
|---------|---------|
| `coderag init` | Initialize or reindex a repository |
| `coderag update` | Update index for changed files only |
| `coderag query <text>` | Semantic search across code nodes |
| `coderag retrieve <text>` | Retrieve relevant code with surrounding context |
| `coderag answer <question>` | Get a natural language answer from the LLM |
| `coderag config` | View or edit configuration |

## Configuration

Config file resolution (first match wins):

1. `--config <path>` flag
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
    "languages": ["typescript", "javascript", "python"],
    "exclude": ["node_modules", "dist", "*.test.ts", ".git"],
    "maxFileSize": 1048576
  },
  "retrieval": {
    "topK": 10,
    "similarityThreshold": 0.7
  }
}
### Configuration Options

#### Embedding Provider

| Provider | Description | Local? |
|----------|-------------|--------|
| `gemini` | Google Gemini embeddings (cloud) | No |
| `onnx` | Local ONNX model embeddings | Yes |

#### LLM Provider

| Provider | Model | API Required |
|----------|-------|--------------|
| `minimax` | MiniMax-Text-01 | Yes |
| `mcp` | MCP-compatible models | Via MCP server |
| `http` | Any HTTP-accessible model | Yes |

#### Indexing Options

- `languages` — Array of languages to index (defaults to all supported)
- `exclude` — Glob patterns for files/directories to skip
- `maxFileSize` — Maximum file size in bytes to index (default: 1MB)

#### Retrieval Options

- `topK` — Number of results to return (default: 10)
- `similarityThreshold` — Minimum similarity score (0.0-1.0)

## Workflow

### 1. Initialize

bash
cd /path/to/repo
coderag init
This performs:
- Scans codebase for supported file types
- Parses code using tree-sitter
- Generates embeddings for code nodes (functions, classes, etc.)
- Stores vectors in local LanceDB

### 2. Query

Choose the appropriate command based on your needs:

- **`query`** — Fast semantic search, returns ranked results
- **`retrieve`** — Returns code nodes with graph-traversed context (imports, callers, callees)
- **`answer`** — Uses LLM to synthesize an answer from retrieved context

### 3. Update

When code changes:

bash
# Full reindex
coderag init

# Incremental update (faster)
coderag update
## Architecture

Codebase → Tree-sitter Parser → Code Nodes → Embedding Model → LanceDB
                                                              ↓
User Query → Embedding → Vector Search → Retrieved Nodes → LLM → Answer
### Key Components

- **Tree-sitter** — Multi-language AST parser extracts semantic code nodes
- **LanceDB** — Local vector database stores embeddings and enables fast similarity search
- **Graph Edges** — Traverses import/call relationships to include surrounding context
- **Embedding Model** — Converts code into semantic vectors (768 dimensions)
- **LLM (optional)** — Synthesizes natural language responses from retrieved context

## Tips

- **First run is slow** — Indexing a large repo takes time; use `coderag update` after
- **Exclude build artifacts** — Add `node_modules`, `dist`, `*.min.js` to exclude patterns
- **Be specific in queries** — "where is JWT validation" works better than "auth"
- **Combine with grep** — Use traditional search for exact matches, coderag for semantic understanding
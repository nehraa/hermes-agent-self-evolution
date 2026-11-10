---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query Tool

## What

A local Retrieval-Augmented Generation (RAG) system for querying codebases. It parses source code using tree-sitter, stores semantic chunks as vector embeddings in LanceDB, traverses code graph edges for contextual retrieval, and optionally uses an LLM to answer questions in natural language.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust

## When to Use

- **Understanding code:** "What does this function do?", "How is auth implemented?"
- **Finding things:** "Where is the user service?", "Find all files related to X"
- **Code archaeology:** "How does job polling work?", "Trace the payment flow"
- **Code review:** Quick comprehension of unfamiliar files or modules
- **Context injection:** Provide Claude Code with relevant code context before editing

## Installation

bash
npm install -g @abhinav2203/coderag
Verify installation:
bash
npm list -g @abhinav2203/coderag
coderag --version
**Binary location:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Quick Start

bash
# Navigate to any codebase
cd /path/to/your/project

# Initialize indexing (one-time per repo)
coderag init

# Query using different modes
coderag query "how does authentication work"      # Search by semantic similarity
coderag retrieve "find the user controller"        # Retrieve raw code nodes
coderag answer "explain the payment flow"          # LLM-generated explanation
## Commands

| Command | Purpose | Use Case |
|---------|---------|----------|
| `coderag init` | Index repo, generate embeddings, store in LanceDB | Initial setup or full reindex |
| `coderag update [file...]` | Reindex specific files | After editing files |
| `coderag query <text>` | Semantic search, returns matching code nodes | Find relevant code by meaning |
| `coderag retrieve <text>` | Retrieve raw code chunks with context | Get exact code to use directly |
| `coderag answer <text>` | LLM-generated answer with citations | Natural language explanations |
| `coderag serve` | Start HTTP server for remote access | MCP integration or remote queries |

## Workflow

### 1. Initialize a Repository

bash
coderag init
Creates:
- `.coderag.json` — configuration file
- `.coderag/` — LanceDB index directory

### 2. Query the Codebase

Choose the appropriate command based on your needs:

bash
# Semantic search — find code by meaning
coderag query "session management"

# Retrieve exact nodes — get code with surrounding context
coderag retrieve "AuthMiddleware"

# Get LLM explanation — natural language answer
coderag answer "how does the rate limiting work"
### 3. Keep Index Updated

bash
# Update specific files after changes
coderag update src/auth/login.ts src/auth/session.ts

# Full reindex
coderag init
## Configuration

Config file resolution order (first match wins):
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
    "exclude": ["node_modules", "dist", ".git", "*.test.ts"],
    "maxFileSize": 1048576
  },
  "retrieval": {
    "topK": 10,
    "minScore": 0.5
  }
}
### Configuration Options

| Section | Option | Type | Default | Description |
|---------|--------|------|---------|-------------|
| `embedding.provider` | | string | `"gemini"` | Embedding provider: `gemini`, `onnx` |
| `embedding.dimensions` | | number | `768` | Embedding vector dimensions |
| `llm.provider` | | string | `"minimax"` | LLM provider for `answer` command |
| `llm.model` | | string | `"MiniMax-Text-01"` | Model name |
| `indexing.languages` | | string[] | all supported | Languages to index |
| `indexing.exclude` | | string[] | `["node_modules", ...]` | Glob patterns to skip |
| `retrieval.topK` | | number | `5` | Number of results to return |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | API key for Gemini embeddings |
| `MINIMAX_API_KEY` | API key for MiniMax LLM |
| `CODERAG_CONFIG` | Path to config file |

## MCP Server

Start the MCP server for programmatic access:

bash
coderag serve --port 3000
Or configure as an MCP tool in your AI assistant settings.

## Troubleshooting

**Empty results:**
- Run `coderag init` to ensure indexing completed
- Check that files match your language config

**Stale results:**
- Run `coderag update <changed-files>` after editing

**LLM errors:**
- Verify `MINIMAX_API_KEY` is set
- Check `llm.baseUrl` is correct

**Slow indexing:**
- Reduce `indexing.languages` to only needed languages
- Increase `indexing.exclude` patterns for large directories
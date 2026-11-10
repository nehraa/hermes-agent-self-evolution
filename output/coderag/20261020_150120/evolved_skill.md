---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query

## What

Local Retrieval-Augmented Generation (RAG) for querying codebases. Indexes your code using tree-sitter for multi-language AST parsing, stores vector embeddings in LanceDB, retrieves relevant code nodes with surrounding context via graph traversal, and optionally generates natural language answers via LLM.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust

## When to Use

- **Understanding code:** "what does this file do", "how does X work", "explain this function"
- **Code archaeology:** "find files related to X", "where is auth handled", "how does job polling work"
- **Navigation:** "where is the user controller", "find the payment module"
- **Quick context:** When Claude Code needs to understand an unfamiliar codebase without reading every file

## Package Info

| Item | Value |
|------|-------|
| **npm** | `@abhinav2203/coderag` |
| **Current version** | v1.1.4 (verify: `npm list -g @abhinav2203/coderag`) |
| **Global binary** | `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag` |

## Quick Start

bash
# Install globally
npm install -g @abhinav2203/coderag

# Initialize a repository (creates .coderag.json and indexes all code)
cd /path/to/repo
coderag init

# Query the codebase
coderag query "how does authentication work"
coderag retrieve "find the user controller"
coderag answer "explain the payment flow"
## Commands

| Command | Purpose |
|---------|---------|
| `coderag init [options]` | Initialize/index a repository |
| `coderag query <query>` | Semantic search for relevant code nodes |
| `coderag retrieve <query>` | Retrieve code with surrounding context |
| `coderag answer <question>` | Ask natural language questions (requires LLM) |
| `coderag update` | Re-index modified files |
| `coderag config [key] [value]` | Get or set configuration |

### Init Options

bash
coderag init                          # Default settings
coderag init --config ./coderag.json  # Custom config path
coderag init --force                  # Re-index from scratch
coderag init --watch                  # Watch mode for live updates
## Workflow

1. **Initialize** — Run `coderag init` in the repository root
   - Creates `coderag.config.json` if not present
   - Parses source files with tree-sitter (AST-based, not regex)
   - Generates vector embeddings via configured provider
   - Stores indexed data in local LanceDB

2. **Query** — Choose the appropriate command based on your need
   - `coderag query` — Semantic search, returns ranked results
   - `coderag retrieve` — Same as query but includes surrounding context (function body, imports, callers)
   - `coderag answer` — Full RAG pipeline with LLM summarization

3. **Update** — Keep index current
   - `coderag update` — Incremental re-index of modified files
   - `coderag init --force` — Full re-index from scratch

## Configuration

### Config File Resolution (first found wins)

1. Explicit `--config <path>` flag
2. `coderag.config.json` in repo root
3. `.coderag.json` in repo root
4. `.env` file with `CODERAG_*` prefix
5. Environment variables

### Minimal Config (Gemini cloud embeddings)

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
    "exclude": ["node_modules", "dist", "build", ".git", "*.test.ts"],
    "maxFileSize": 1048576
  },
  "retrieval": {
    "topK": 10,
    "includeContext": true,
    "contextLines": 5
  },
  "server": {
    "enabled": true,
    "port": 3000,
    "mcp": true
  }
}
### Embedding Providers

| Provider | Config Key | Notes |
|----------|------------|-------|
| **Gemini** | `provider: "gemini"` | Cloud API (requires `GEMINI_API_KEY`) |
| **ONNX** | `provider: "onnx"` | Local inference (no API key needed) |

### LLM Providers

| Provider | Config Key | Notes |
|----------|------------|-------|
| **MiniMax** | `provider: "minimax"` | Requires `apiKey`, `baseUrl` |
| **OpenAI-compatible** | `provider: "openai"` | Custom `baseUrl` supported |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | API key for Gemini embeddings |
| `MINIMAX_API_KEY` | API key for MiniMax LLM |
| `CODERAG_CONFIG` | Path to config file |
| `CODERAG_DB_PATH` | Override LanceDB storage path |

## Troubleshooting

**"No results found"**
- Verify index exists: check for `.coderag/` directory
- Re-run `coderag init --force`
- Verify language is in supported list

**"LLM request failed"**
- Check API key is valid and has quota remaining
- Verify `baseUrl` is correct
- Try `coderag query` instead of `coderag answer`

**Slow indexing**
- Reduce languages in config to only those in your codebase
- Add large directories to `exclude` array
- Use ONNX provider for faster local embeddings

**Memory issues**
- Set `maxFileSize` in indexing config
- Exclude generated files (`dist`, `build`, `.next`)
- Process large repos in chunks
---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query

## What
Local RAG (Retrieval-Augmented Generation) for querying any codebase. Uses tree-sitter for multi-language analysis, stores node documents in LanceDB, traverses graph edges for surrounding context, and optionally uses an LLM to answer questions in natural language.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust.

## When to Use
- User asks about what a file/function does, where something is located, or how a feature works
- Code archaeology: "find me all files related to X", "where is auth handled", "how does the job polling work"
- Code review: "explain this function", "what does this file do"
- When Claude Code needs to understand an unfamiliar codebase quickly

## Package Info
- **npm:** `@abhinav2203/coderag`
- **Current version:** v1.1.4 (verify with `npm list -g @abhinav2203/coderag`)
- **Global binary:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Quick Start

bash
# Install globally
npm install -g @abhinav2203/coderag

# Initialize a repo (creates .coderag.json and indexes)
cd /path/to/repo
coderag init

# Query the codebase
coderag query "how does authentication work"
coderag retrieve "find the user controller"
coderag answer "explain the payment flow"
## Workflow

1. **Initialize** — Run `coderag init` in repo root. Creates config, indexes files, generates embeddings, stores in LanceDB.
2. **Query** — Use `coderag query`, `coderag retrieve`, or `coderag answer` to search.
3. **Update** — Re-run `coderag init` or `coderag update` when codebase changes.

## Configuration

Config file resolution (first found wins):
1. Explicit `--config <path>` flag
2. `coderag.config.json` in repo root
3. `.coderag.json` in repo root
4. `.env` file values
5. Environment variable overrides

### Minimal Config (Gemini cloud)

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
    "similarityThreshold": 0.7
  }
}
## Embedding Providers

| Provider | Type | Config Key | Notes |
|----------|------|------------|-------|
| Gemini | Cloud | `gemini` | Requires `GEMINI_API_KEY` env var |
| ONNX | Local | `onnx` | Runs entirely offline; specify model path |

## Commands

| Command | Description |
|---------|-------------|
| `coderag init` | Initialize/index a repository |
| `coderag query <text>` | Search for relevant code nodes |
| `coderag retrieve <text>` | Retrieve matching code snippets |
| `coderag answer <text>` | Ask natural language questions (requires LLM) |
| `coderag update` | Re-index changed files only |
| `coderag status` | Show index statistics |

## Tips

- **First run:** Run `coderag init` before any queries on a new repo
- **Large repos:** Use `coderag update` after changes instead of full re-index
- **Offline mode:** Use ONNX embeddings to work without internet
- **Context window:** The tool traverses graph edges to include surrounding context in results
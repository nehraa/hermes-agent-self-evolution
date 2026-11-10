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
    "exclude": ["node_modules", "dist", "*.test.ts"]
  }
}
## Embedding Providers

### Gemini (Cloud)

json
{
  "embedding": {
    "provider": "gemini",
    "dimensions": 768
  }
}
- **Model:** `models/gemini-embedding-2`
- **Dimensions:** 768-dim vectors
- **Rate limit:** 100 requests/minute (free tier)
- **API key:** Set via `CODERAG_GEMINI_API_KEY` environment variable or `coderag init` prompt

**Warning:** Batch processing large repos may trigger 429 errors. Use ONNX for large codebases.

### ONNX (Local)

json
{
  "embedding": {
    "provider": "onnx",
    "dimensions": 384
  }
}
- **Model:** `Xenova/gte-small` (~33MB, downloaded on first use)
- **Dimensions:** 384-dim vectors
- **Pros:** Zero cost, no rate limits, works offline
- **Cons:** Slower than cloud, 384-dim vectors only

**Pre-download model:**
bash
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download(
    'Xenova/gte-small',
    local_dir='.coderag-models/models',
    allow_patterns=[
        'onnx/model_quantized.onnx',
        'config.json',
        'tokenizer.json',
        'tokenizer_config.json',
        'special_tokens_map.json'
    ]
)
"
## LLM Providers

### MiniMax (OpenAI-compatible)

json
{
  "llm": {
    "provider": "minimax",
    "model": "MiniMax-Text-01",
    "apiKey": "your_api_key",
    "baseUrl": "https://api.minimax.chat/v1"
  }
}
- Set key via `CODERAG_MINIMAX_API_KEY` env var or config
- Requires embedding provider to be configured

### MCP (Model Context Protocol)

json
{
  "llm": {
    "provider": "mcp",
    "server": "mcp-server-name"
  }
}
### HTTP (Custom endpoint)

json
{
  "llm": {
    "provider": "http",
    "baseUrl": "http://localhost:11434",
    "model": "llama3"
  }
}
## CLI Commands

| Command | Description |
|---------|-------------|
| `coderag init` | Initialize repo: create config, index files, generate embeddings |
| `coderag update` | Re-index changed files only |
| `coderag query <text>` | Retrieve relevant code nodes (no LLM) |
| `coderag answer <text>` | Query + LLM answer in natural language |
| `coderag serve` | Start HTTP server for external queries |
| `coderag status` | Show index stats, model info, config |

### Query Flags

- `--config <path>` — Use specific config file
- `--top-k <n>` — Return top N results (default: 5)
- `--lang <language>` — Filter by language
- `--file <glob>` — Filter by file pattern

## Indexing

- Uses **tree-sitter** for AST-based code parsing (not regex)
- Each function, class, method becomes a separate document node
- Graph edges connect: class→method, file→exports, import→imported
- LanceDB stores embeddings with metadata (file, line, type, scope)

## Troubleshooting

**"No embeddings found"**
- Run `coderag init` first
- Check config file exists in repo root

**Rate limit errors (429) with Gemini**
- Switch to ONNX provider for large batches
- Add delay between requests
- Use smaller batch sizes

**Slow queries**
- Use ONNX (local) instead of Gemini
- Reduce `--top-k` value
- Check disk I/O on LanceDB storage

**LLM not responding**
- Verify API key is set correctly
- Check `llm.provider` matches your config
- Ensure embedding provider is also configured
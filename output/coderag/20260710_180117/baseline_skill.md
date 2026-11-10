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
- **Current version:** v1.1.4 (check with `npm list -g @abhinav2203/coderag`)
- **Global binary:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

## Setup (fresh install)
```bash
npm install -g @abhinav2203/coderag
```

## Configuration
Create `.coderag.json` in the target repo root. Configuration order (first found wins):
1. Explicit `--config` path
2. `coderag.config.json`
3. `.coderag.json`
4. `.env` values
5. Environment variable overrides

### Embedding Providers

**Gemini (cloud, rate-limited):**
```json
{
  "embedding": {
    "provider": "gemini"
  }
}
```
- Uses `models/gemini-embedding-2`, 768-dim vectors
- Free tier: **100 requests/minute** — will hit 429 if you process too fast
- Set key: `CODERAG_GEMINI_API_KEY=your_key coderag init`

**ONNX (local, no rate limit):**
```json
{
  "embedding": {
    "provider": "onnx",
    "dimensions": 384
  }
}
```
- Downloads `Xenova/gte-small` (~33MB) on first use
- Zero API cost, no rate limits — use for large repos
- Download model:
```bash
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('Xenova/gte-small', local_dir='.coderag-models/models',
                  allow_patterns=['onnx/model_quantized.onnx', 'config.json',
                                  'tokenizer.json', 'tokenizer_config.json',
                                  'special_tokens_map.json'])
"
```

### LLM Providers

**MiniMax (openai-compatible):**
```json
{
  "llm": {
    "enabled": true,
    "transport": "openai-compatible",
    "baseUrl": "https://api.minimax.io/v1",
    "model": "MiniMax-M2.7",
    "apiKey": "sk-cp-..."  // see memory for key
  }
}
```
Set via environment: `CODERAG_LLM_API_KEY=sk-cp-... coderag query "..."`

**OpenAI-compatible (local or other):**
```json
{
  "llm": {
    "enabled": true,
    "transport": "openai-compatible",
    "baseUrl": "http://127.0.0.1:1234/v1",
    "model": "your-local-model"
  }
}
```

## Init & Index
```bash
cd /path/to/repo
CODERAG_GEMINI_API_KEY=your_key coderag init
```

Options:
- `--full` — force full reindex (clears existing index first)
- `--config path` — explicit config file path

**Rate limit handling:** Gemini free tier hits 429 at ~100 RPM. For large repos, use ONNX embeddings OR init with reduced chunk size. The init processes in chunks of 100 docs — with 31 chunks total, it should fit in the 100-req/min limit if done in one burst, but retry delays are unreliable.

## Query
```bash
coderag query "your question" --depth 2 --json
```
- `--depth N` — graph traversal depth (default: 1)
- `--json` — machine-readable output
- `--config path` — explicit config

Without LLM: returns node IDs and code snippets (context-only mode).
With LLM configured: returns natural language answers.

## Serve (MCP or HTTP)
```bash
coderag serve-mcp   # MCP server for Hermes agent integration
coderag serve-http   # HTTP REST API on port 3101
```

Doctor command to verify setup:
```bash
coderag doctor --config /path/to/.coderag.json
```

## Known Repos
- **OpenMAIC/Aidutech:** `/home/Hermes/repos/OpenMAIC` — EdTech platform, 3027 nodes, ONNX + MiniMax
- **VibeHire:** `/home/Hermes/VibeHire` — AI agentic marketing platform, 574 nodes
- **CodeFlow:** `/home/Hermes/CodeFlow` — AI agent pipeline

## Current Issue (May 25, 2026)
**Gemini rate limiter race condition:** The rate limiter has a race condition where multiple concurrent calls all pass the check simultaneously before any get added to the timestamps array. Fix in progress (v1.1.5+). For now: use ONNX for embeddings.

**Coderag version updated:** v1.1.4 — has MiniMax LLM support + rate limiting + larger context window.

## If Index Gets Corrupted
```bash
cd /path/to/repo
rm -rf .coderag .coderag-models
# Edit .coderag.json to set embedding provider
coderag init
```

## Key Files
- Config: `.coderag.json` or `coderag.config.json`
- Index data: `.coderag/` (LanceDB + documents.json + graph-snapshot.json)
- ONNX model cache: `.coderag-models/`
- Post-commit hook: `.git/hooks/post-commit` (auto-installed by init)
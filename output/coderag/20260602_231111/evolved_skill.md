---
name: coderag
description: "Local RAG query tool for codebases — indexes repos, retrieves relevant code nodes, and optionally answers questions via LLM. Supports Gemini embeddings, ONNX local embeddings, MiniMax LLM, and MCP/HTTP serving."
category: software-development
---

# coderag — Codebase RAG Query

Local Retrieval-Augmented Generation for querying codebases. Indexes source code, stores semantic chunks in LanceDB, and retrieves relevant nodes with surrounding context. Optionally generates natural language answers via LLM.

**Supported languages:** TypeScript, JavaScript, Go, Python, C, C++, Rust.

---

## When to Use

- **Code exploration:** "What does this file do?", "Where is the auth logic?", "How does X feature work?"
- **Code archaeology:** "Find all files related to X", "Trace the request flow for Y"
- **Code review:** "Explain this function", "What are the dependencies of this module?"
- **Onboarding:** Understand an unfamiliar codebase quickly

---

## Installation

bash
npm install -g @abhinav2203/coderag
**Binary location:** `/home/Hermes/node-v22.13.0-linux-x64/bin/coderag`

**Check version:**
bash
npm list -g @abhinav2203/coderag
---

## Configuration

Create a config file in your repo root. Order of precedence (first found wins):

| Priority | Config File |
|----------|-------------|
| 1 | Explicit `--config` flag |
| 2 | `coderag.config.json` |
| 3 | `.coderag.json` |
| 4 | `.env` file values |
| 5 | Environment variable overrides |

---

## Embedding Models

### Gemini (Cloud)

json
{
  "embedding": {
    "provider": "gemini",
    "model": "models/gemini-embedding-2"
  }
}
- **Dimensions:** 768
- **Rate limits:** 100 requests/minute on free tier
- **API key:** Set via `CODERAG_GEMINI_API_KEY` environment variable
- **Use case:** Quick setup, small-to-medium repos

bash
CODERAG_GEMINI_API_KEY=your_key coderag init
### ONNX (Local)

json
{
  "embedding": {
    "provider": "onnx",
    "model": "Xenova/gte-small",
    "dimensions": 384
  }
}
- Downloads model (~33MB) on first use
- Zero API cost, no rate limits
- Recommended for large repos or rate-limited environments

**Pre-download the model:**
bash
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('Xenova/gte-small', 
                  local_dir='.coderag-models/models',
                  allow_patterns=['onnx/model_quantized.onnx', 
                                  'config.json',
                                  'tokenizer.json', 
                                  'tokenizer_config.json',
                                  'special_tokens_map.json'])
"
---

## LLM Providers

### MiniMax (OpenAI-compatible)

json
{
  "llm": {
    "provider": "minimax",
    "apiKey": "your_api_key"
  }
}
- OpenAI-compatible API — set base URL if needed
- Works with any OpenAI-compatible endpoint

### HTTP/MCP

json
{
  "llm": {
    "provider": "http",
    "url": "http://localhost:8080/v1/chat/completions"
  }
}
Or use MCP for local model serving:
json
{
  "llm": {
    "provider": "mcp",
    "server": "local-llm"
  }
}
---

## Quick Start

bash
# Initialize index in current repo
coderag init

# Query the codebase
coderag query "how does authentication work"

# Re-index after code changes
coderag reindex

# Use custom config
coderag init --config /path/to/config.json
---

## Project Structure

.coderag/
├── index/           # LanceDB vector store
├── sources/         # Source file metadata
└── cache/           # Parsed AST cache
The tool uses tree-sitter for language-aware parsing, chunks code into semantic nodes (functions, classes, imports), and stores them with embeddings for semantic search.
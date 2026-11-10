---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (a fork of llama.cpp with lookup-table optimized kernels for ternary weights).

## Files

- Repo: `/home/Hermes/repos/BitNet` (single source of truth — do not clone to `/home/Hermes/BitNet`)
- Binaries: `/home/Hermes/repos/BitNet/build/bin/llama-cli` and `llama-server` (both built)
- Model GGUF: `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` (1.2GB on disk, ~1.84GB in GGUF metadata, i2_s kernel)
- Wrapper: `/home/Hermes/.hermes/scripts/bitnet_inference.sh` (handles cli / server / version subcommands)

## Quick start

```bash
# Interactive chat (chat template applied):
bitnet_inference.sh
# or
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"

# One-shot (raw text, 80 tokens, ~30s):
bitnet_inference.sh "What is 2+2?"

# OpenAI-compatible HTTP API on :8089 (default port):
bitnet_inference.sh server
# or specify port:
bitnet_inference.sh server 9090
# Test:
curl http://localhost:8089/v1/models
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'
```

## Performance

- ~2.7-2.9 tok/sec on 4 CPU threads (i3-1115G4 baseline)
- ~5 tok/sec on 8 threads
- 1.2GB RAM footprint (CPU buffer ~1.1GB + KV cache ~300MB at 4096 ctx)
- **Cold start**: model load + KV init + first decode = ~3-5s before any tokens appear
- **One-shot budget**: 80 tokens ≈ 30s end-to-end including load. Anything below 60s timeout may get cut. Bump to `-n 40` or `-n 20` for fast verification, or use `server` mode and let the model stay warm between requests.
- **Verified end-to-end on x86_64 Linux (June 19 2026)**: serving on :8081 with the 1.2GB i2_s gguf, full chat completions working. Test: `curl -X POST http://localhost:8081/v1/chat/completions -d '{"messages":[{"role":"user","content":"What is the capital of France? Reply with just the city name."}],"max_tokens":20}'` → `"Paris"` in 1.7s end-to-end. This confirms the BitNet-b1.58-2B-4T pipeline is production-ready for chat / Q&A / short-form generation on this server.

**For MNEME / Hermes intent detection (June 19 2026)**: launch with `--parallel 4 --ctx-size 2048` instead of the defaults. The 1B-param model is small enough that 4 concurrent requests fit in 4-thread CPU. Without `--parallel 4`, retrieve-as-a-service queues and 30-60s timeouts cascade.

## Chat template (LLaMA 3 format with bitnet's ▁ separators)

```
<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

{user message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

```

Note: `▁` is U+2581 LOWER ONE EIGHTH BLOCK (not regular underscore). BitNet uses these in its special tokens.

## Build from scratch (recipe)

The build is tricky on this server because there's no clang. Workarounds already patched into `setup_env.py`:

1. Clone + submodules:
```bash
cd /home/Hermes/repos
git clone https://github.com/microsoft/BitNet.git
cd BitNet
git submodule update --init --recursive   # 3rdparty/llama.cpp + kompute
```

2. Patch `setup_env.py` (already applied — don't re-do):
   - gcc fallback when clang missing
   - skip `huggingface-cli download` if `ggml-model-i2_s.gguf` already exists in model dir

3. Place gguf where script expects it:
```bash
mkdir -p /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T
cp /path/to/ggml-model-i2_s.gguf \
   /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/
```

4. Run setup (cmake + build):
```bash
cd /home/Hermes/repos/BitNet
python3 setup_env.py \
  --hf-repo microsoft/BitNet-b1.58-2B-4T \
  --model-dir /home/Hermes/models/BitNet-b1.58-2B-4T-gguf \
  --quant-type i2_s
# Builds everything; ~5 min on this box
```

5. Verify:
```bash
./build/bin/llama-cli -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "Hello" -n 20
```

6. (Optional) Build the server too — default `setup_env.py` only makes `llama-cli`:
```bash
cd /home/Hermes/repos/BitNet/build
cmake --build . --target llama-server --config Release -j 2
```

## Wrapper script (canonical version)

Saved at `/home/Hermes/.hermes/scripts/bitnet_inference.sh`. Three modes: cli (default or with prompt), server [port], version. **The prompt is stored in a here-doc (`<<'EOF'`) so the U+2581 (▁) and `<|...|>` tokens survive byte-for-byte** — `patch` and `sed` will mangle them.

```bash
#!/bin/bash
# BitNet b1.58 2B4T inference wrapper
set -e

MODEL=/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf
LLAMA_DIR=/home/Hermes/repos/BitNet/build/bin
THREADS=$(nproc)

# Chat template as a here-doc to preserve special characters (U+2581 lower one-eighth block)
read -r -d '' CHAT_PROMPT <<'EOF' || true
<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

EOF

case "$1" in
  server|s)
    PORT="${2:-8089}"
    shift; [ "$1" = "server" ] || [ "$1" = "s" ] && shift
    "$LLAMA_DIR/llama-server" -m "$MODEL" -t "$THREADS" -c 4096 --port "$PORT" "$@"
    ;;
  version|--version|-v)
    "$LLAMA_DIR/llama-cli" --version 2>&1 | grep -E "^version|^built"
    "$LLAMA_DIR/llama-server" --version 2>&1 | grep -E "^build|^built"
    ;;
  help|-h|--help)
    echo "Usage: bitnet [\"prompt\"] | bitnet server [port] | bitnet version"
    ;;
  *)
    if [ $# -gt 0 ]; then
      exec "$LLAMA_DIR/llama-cli" -m "$MODEL" -c 1024 -t "$THREADS" -n 80 -p "$*"
    else
      exec "$LLAMA_DIR/llama-cli" -m "$MODEL" --color -i -c 2048 -t "$THREADS" -n 256 \
        --prompt "$CHAT_PROMPT"
    fi
    ;;
esac
```

To install on a fresh machine: `cp` to `~/.hermes/scripts/bitnet_inference.sh && chmod +x`. Verify with `hexdump -C ~/.hermes/scripts/bitnet_inference.sh | grep begin` — you should see `e2 96 81` (the UTF-8 for U+2581), not regular underscores.

## Pitfalls

- **`huggingface-cli` not installed** — the unpatched script tries to download the full BF16 model (~4GB) and fails. The patched script now detects the existing gguf and skips.
- **No clang, no sudo** — can't `apt install clang`. The patch in setup_env.py falls back to gcc, which works.
- **Submodules required** — `git clone` alone won't pull `3rdparty/llama.cpp`. Without it, `gguf-py` pip install fails with "Expected semicolon... it looks like a path".
- **Model name mismatch** — the script appends the model name as a subdir to `--model-dir`. If you pass a path that doesn't end with that subdir, you must create the subdir and put the gguf inside.
- **First inference slow** — model load + KV cache init takes ~2s on first call. Subsequent calls warm.
- **Default build only produces `llama-cli`** — if you need `llama-server` too, run `cmake --build build --target llama-server --config Release -j 2` after the initial build. The setup script doesn't include it.
- **Parallel rebuilds corrupt each other** — never run two `cmake`/`setup_env.py` instances against the same `build/` directory at once. Concurrent `rm -rf build && cmake -B build` from different processes will leave CMakeCache.txt in inconsistent states. If you need to rebuild, kill any other build first, then rebuild serially.
- **Don't clone to `/home/Hermes/BitNet`** — the canonical location is `/home/Hermes/repos/BitNet`. A second clone at the home dir will diverge and confuse the wrapper. If you see `/home/Hermes/BitNet` exist, remove it: `rm -rf /home/Hermes/BitNet`.
- **`patch` tool eats BitNet special tokens** — `<|begin▁of▁text|>`, `<|start_header_id|>` and the U+2581 (▁) character get normalized/mangled when used inside a `patch` new_string. If editing the wrapper, use `write_file` (full overwrite) and put the prompt in a here-doc (`<<'EOF' ... EOF`) so the special chars survive byte-for-byte. Always `hexdump -C file | grep "begin"` after editing to verify `e2 96 81` (U+2581) is present, not regular underscores.
- **Wrapper arg parsing: prompt can look like a subcommand** — when the first word of a prompt happens to be `server`, `version`, `help`, etc., a naïve `case "$1"` wrapper will misinterpret it. The current wrapper routes through the `*)` default for everything except the explicit subcommands, so this is safe — but if you rewrite it, keep that fall-through.
- **Concurrent requests need `--parallel 4+`** (June 19 2026) — for MNEME retrieve-as-a-service, the default `--parallel 1` causes requests to back up in llama-server. The single-thread queue blocks for 30-60s per request when 3+ are in flight, even though each individually takes ~5s. Launch with `--parallel 4 --ctx-size 1024` to handle concurrent retrieve requests. KV cache memory scales with ctx-size, so reducing from 4096 → 1024 quadruples the concurrency headroom for the same RAM (helpful on 7.5GB-RAM servers). Smaller ctx (1024) also matters for memory: BitNet 1.3GB + Ollama 1GB + 3 next-server 2GB on 7.5GB leaves ~2GB free, which BitNet's KV cache can blow through at ctx=4096.
- **Intent detection `max_tokens` was 256 → 16 → 60** (June 19 2026) — `BitNetClient.detect_intent()` originally requested 256 tokens of generation. At 2.7 tok/sec that's 95 seconds — way longer than the 60s default client timeout. Dropped to 16 to keep it fast, but 16 truncated the JSON output mid-array (e.g. `["setup","`). Final value is 60 tokens — enough for the full intent JSON `{intent, detected_tags}` with 2-4 tags. Total per-call latency: ~40s (prompt processing 17s + generation 22s). Same fix in `src/retrieval/bitnet_client.py`: `max_tokens: int = 60`.
- **System prompt matters** — verbose system prompts (600+ chars explaining the intent labels) doubled prompt processing time. Condensed to 250 chars with just the labels and one example. Same output quality, ~2x faster.
- **On memory-constrained servers (≤8GB RAM), unload Ollama before starting BitNet** — BitNet (1.3GB) + Ollama qwen3 model (1GB) + dev_server (500MB) + 3 next-servers (~2GB) + LSPs (500MB) = ~5GB+ used. Below ~1.5GB free, llama-server silently hangs on every real request while still answering `/health` OK. Symptom: `curl http://localhost:8081/v1/models` works, `curl http://localhost:8081/v1/chat/completions` (even max_tokens=8) hangs 30s. Fix: `curl -X POST http://localhost:11434/api/generate -d '{"model":"qwen3-embedding:0.6b","keep_alive":0}'` to unload Ollama before launching BitNet, OR kill the workspace apps (next-server, TypeScript LSPs) the user doesn't need running.
- **llama-server can appear healthy but reject all real requests** (June 19 2026) — even after fixing memory, sometimes `/health` returns 200 but every `/v1/chat/completions` times out. Cause: queued requests from a previous instance that didn't finish, OR OOM-swapped process. Fix: `pkill -f llama-server && sleep 5 && relaunch with --parallel 4 --ctx-size 1024`.

## When to use

- Omnyxnet BitNet ML peer management — on-device privacy inference where no GPU is available
- Edge nodes running as inference endpoints in the EdgeCloud / Edge Crowd stack
- Pangea Paper news summarization where cloud LLM is too costly / privacy-violating
- Any CPU-only server-side inference task
- **Local-only tag generation for corpus indexing** — when an LLM is needed to enrich a metadata-first corpus index but the user has a "no cloud LLM" rule, BitNet can generate 3-5 free-form tags per chunk. Use a short prompt: `"Reply with 3-5 comma-separated tags for this text. Lowercase, no punctuation."` Cap input to ~1KB. Cap output to ~30 tokens. 15-20s per call. Quality is hit-or-miss on long inputs but acceptable for cheap enrichment. The trick is asking for free-form output, NOT structured JSON — the 2B model can't reliably produce valid JSON on long inputs but CAN produce comma-separated tags.

## When NOT to use

- High-throughput serving → use vLLM with a regular GGUF model on GPU
- Quality-critical tasks → BitNet 2B is small; use MiniMax API instead
- Anything needing >100 tok/sec
- Structured JSON output on documents >500 chars (hallucinates, truncates)
- Long-form summarization, translation, or anything requiring multi-step reasoning across a long context

**Exception (June 19 2026):** Short structured JSON output for intent detection works fine at `max_tokens=60` with a 250-char system prompt. The model reliably produces `{intent, detected_tags: [2-4 tags]}` for queries <200 chars. Don't write off JSON generation entirely — just keep the schema small and the prompt under 300 chars.
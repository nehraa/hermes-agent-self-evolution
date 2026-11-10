---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. Runs entirely on CPU via `bitnet.cpp` (llama.cpp fork with lookup-table optimized kernels for ternary weights).

**Key characteristics:**
- No GPU required — fully CPU-bound
- 1.58-bit quantization (ternary weights: -1, 0, +1)
- Privacy-preserving: all inference stays on-device
- ~2.7 tok/sec on 4 threads

## Files

| File | Path |
|------|------|
| Repository | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

**Model specs:** 1.2GB on disk, ~1.84GB GGUF metadata, `i2_s` kernel (integer-to-sign lookup table optimization).

## Wrapper Script

The wrapper handles all common operations. Use instead of calling binaries directly.

bash
bitnet_inference.sh <subcommand> [args]
| Subcommand | Description |
|------------|-------------|
| *(none)* | Interactive chat mode with chat template applied |
| `"<prompt>"` | One-shot inference with raw text prompt |
| `server [port]` | Start OpenAI-compatible HTTP API server (default port: 8089) |
| `version` | Print bitnet.cpp version info |

## Quick Start

### Interactive Chat

bash
bitnet_inference.sh
Opens an interactive REPL with chat template applied (`<|begin_of_text|>...<|eot_id|>` format).

### One-Shot Inference

bash
bitnet_inference.sh "What is 2+2?"
Returns ~80 tokens by default. End-to-end including model load: ~30 seconds.

### HTTP API Server

Start the server:

bash
# Default port (8089)
bitnet_inference.sh server

# Custom port
bitnet_inference.sh server 9090
Test the server:

bash
# List available models
curl http://localhost:8089/v1/models

# Chat completion
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'
## Performance

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7–2.9 tok/sec |
| Throughput (8 threads) | ~5 tok/sec |
| RAM footprint | ~1.2GB (1.1GB buffer + 300MB KV cache at 4096 ctx) |
| Cold start | 3–5s before first token |
| One-shot (80 tokens) | ~30s end-to-end |

**Cold start breakdown:** model load → KV cache init → first token decode.

### Timeout Considerations

- One-shot inference including load: ~30s
- Timeouts below 60s risk truncation
- For fast verification, use `-n 20` or `-n 40` tokens
- For repeated queries, keep server running to avoid reload overhead

### Verified Configuration

- Platform: x86_64 Linux
- Model: `ggml-model-i2_s.gguf` (1.2GB)
- Serving on `:8081`
- Full chat completions API verified working (June 19 2026)

## Direct Binary Usage

If the wrapper is insufficient, call binaries directly:

bash
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
**Key flags:**

| Flag | Meaning |
|------|---------|
| `-m` | Model path |
| `-c 2048` | Context window (2048 tokens) |
| `-t 4` | Thread count |
| `-n 256` | Max tokens to generate |
| `-i` | Interactive mode |
| `--color` | Color output |
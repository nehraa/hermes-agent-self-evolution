---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (llama.cpp fork with lookup-table optimized kernels for ternary weights).

## File Locations

| Asset | Path |
|-------|------|
| Repo | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

Model specs: 1.2GB on disk, i2_s quantized kernel.

## Quick Start

### Interactive Chat

bash
bitnet_inference.sh
This launches an interactive session with the chat template applied automatically.

### One-Shot Query

bash
bitnet_inference.sh "What is 2+2?"
Returns ~80 tokens. Budget: ~30s end-to-end including model load.

### HTTP API Server

bash
# Default port (8089)
bitnet_inference.sh server

# Custom port
bitnet_inference.sh server 9090
The server provides an OpenAI-compatible API. Test with:

bash
curl http://localhost:8089/v1/models
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'
## Manual CLI Invocation

When not using the wrapper script, invoke `llama-cli` directly:

bash
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### Key CLI Flags

| Flag | Meaning |
|------|---------|
| `-m` | Model path (GGUF file) |
| `-c N` | Context size (default 2048) |
| `-t N` | Thread count |
| `-n N` | Max tokens to generate |
| `-i` | Interactive mode |
| `--color` | Colorize output |

## Performance

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7–2.9 tok/sec |
| Throughput (8 threads) | ~5 tok/sec |
| RAM footprint | ~1.1GB (CPU buffer) + ~300MB (KV cache at 4096 ctx) |
| Cold start | 3–5s before first token |
| One-shot (80 tokens) | ~30s end-to-end |

### Latency Tips

- **Cold start overhead**: Model load + KV init + first decode happens before any output. Account for this in timeouts.
- **Warm mode preferred**: Use `server` mode for repeated queries — avoids reload on each request.
- **Fast verification**: Use `-n 20` or `-n 40` to stay well under 60s for quick checks.
- **Minimum timeout**: Anything under 60s risks truncation for one-shot queries.

## Verified Working (x86_64 Linux)

- **Date**: June 19, 2026
- **Mode**: Server serving on port 8081
- **Model**: 1.2GB i2_s GGUF
- **Tested**: Full chat completions via `/v1/chat/completions`

## Wrapper Script Subcommands

bash
bitnet_inference.sh              # Interactive chat
bitnet_inference.sh "<prompt>"   # One-shot query
bitnet_inference.sh server       # Start HTTP API (default :8089)
bitnet_inference.sh server <port> # Start HTTP API (custom port)
bitnet_inference.sh version      # Show bitnet.cpp version
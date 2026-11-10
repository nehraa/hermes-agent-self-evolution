---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit large language model at the 2B-parameter scale. Runs entirely on CPU via `bitnet.cpp` — a specialized fork of llama.cpp with lookup-table optimized kernels designed for ternary weight computation.

## File Locations

| Purpose | Path |
|---------|------|
| Source repository | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

> **Note**: The repository lives at `/home/Hermes/repos/BitNet`. Do not clone to `/home/Hermes/BitNet`.

## Model Details

- **Quantization**: i2_s (1-bit with sign kernel optimization)
- **File size**: 1.2 GB on disk
- **Parameters**: 2B
- **Training tokens**: 4T
- **Context length**: 4096 tokens (default)

## Quick Start

### Interactive Chat Mode

bash
# Using the wrapper script (recommended):
bitnet_inference.sh

# Or invoke directly with full chat template:
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### Single Prompt (One-Shot)

bash
# Wrapper script handles everything:
bitnet_inference.sh "What is 2+2?"

# Adjust token count for faster responses:
-n 20   # ~7 seconds (quick verification)
-n 40   # ~15 seconds (default for short answers)
### OpenAI-Compatible API Server

Start the server on the default port (8089):

bash
bitnet_inference.sh server
Or specify a custom port:

bash
bitnet_inference.sh server 9090
**Test the server:**

bash
# List available models:
curl http://localhost:8089/v1/models

# Chat completion request:
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ]
  }'
## Wrapper Script Usage

The `bitnet_inference.sh` wrapper provides three subcommands:

| Command | Description |
|---------|-------------|
| `bitnet_inference.sh` | Interactive chat mode |
| `bitnet_inference.sh "prompt"` | One-shot inference |
| `bitnet_inference.sh server [port]` | Start API server (default: 8089) |
| `bitnet_inference.sh version` | Print version info |

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7–2.9 tokens/sec |
| Throughput (8 threads) | ~5 tokens/sec |
| RAM footprint | ~1.1 GB (model) + ~300 MB (KV cache) |
| Total memory at 4096 ctx | ~1.4 GB |
| Cold start time | 3–5 seconds (model load + init + first token) |
| One-shot (80 tokens) | ~30 seconds end-to-end |

### Timing Guidelines

- **Timeout < 60s**: Recommended for requests up to 80 tokens
- **< 60 tokens**: Use `-n 40` or `-n 20` for reliable completion within 15s
- **Long responses**: Start in `server` mode to avoid repeated cold starts

## Verified Deployment

- **Platform**: x86_64 Linux
- **Date verified**: June 19, 2026
- **Server port**: 8081
- **Status**: Full chat completions working end-to-end

bash
# Production verification test:
curl -X POST http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, state your name."}]}'
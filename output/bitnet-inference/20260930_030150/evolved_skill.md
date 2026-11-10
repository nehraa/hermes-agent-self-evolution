---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (a fork of llama.cpp with lookup-table optimized kernels for ternary weights).

## File Locations

| Component | Path |
|-----------|------|
| Source repo | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

**Model details:** 1.2GB on disk, ~1.84GB in GGUF metadata, uses i2_s kernel (2-bit integer optimized).

## Quick Start

### Interactive Chat Mode

bash
# Uses the wrapper script (recommended):
bitnet_inference.sh

# Or invoke llama-cli directly with chat template:
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### One-Shot Inference

bash
# Simple question (80 tokens max, ~30s total including model load):
bitnet_inference.sh "What is 2+2?"

# Faster verification with reduced token count:
bitnet_inference.sh "What is 2+2?" -n 20   # ~10s
bitnet_inference.sh "What is 2+2?" -n 40   # ~15s
### OpenAI-Compatible HTTP API

bash
# Start server (default port 8089):
bitnet_inference.sh server

# Start on custom port:
bitnet_inference.sh server 9090

# Check available models:
curl http://localhost:8089/v1/models

# Chat completion request:
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "max_tokens": 80
  }'
## Wrapper Script Commands

bash
bitnet_inference.sh                    # Interactive chat mode
bitnet_inference.sh "prompt"           # One-shot inference
bitnet_inference.sh "prompt" -n 50     # One-shot with custom token limit
bitnet_inference.sh server             # Start HTTP server on default port
bitnet_inference.sh server 9090        # Start HTTP server on custom port
bitnet_inference.sh version            # Show bitnet.cpp version info
bitnet_inference.sh cli                # Direct llama-cli with full args
## Performance Characteristics

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7–2.9 tok/sec |
| Throughput (8 threads) | ~5 tok/sec |
| RAM footprint | ~1.2GB (1.1GB buffer + ~300MB KV cache at 4096 ctx) |
| Cold start time | ~3–5s before first token |
| One-shot (80 tokens) | ~30s end-to-end |

### Timing Notes

- **Cold start penalty**: First inference incurs model load + KV initialization + initial decode. For repeated queries, use `server` mode to keep model warm.
- **Timeout guidance**: Default 80-token requests take ~30s. Requests with tight timeouts (<60s) may get truncated. Use `-n 20` or `-n 40` for quick verification.
- **Throughput scales with threads**: Double threads roughly doubles throughput (4→8 threads gives ~2x speedup).

## Verified Capabilities (June 2026)

- Full chat completion API working on x86_64 Linux
- Server tested on port :8081 with i2_s GGUF model
- OpenAI-compatible `/v1/chat/completions` and `/v1/models` endpoints confirmed functional

## Troubleshooting

bash
# If server fails to start, check if port is in use:
lsof -i :8089

# To run with more threads for better throughput:
bitnet_inference.sh cli -t 8 -c 4096 -m <model_path>

# For verbose output:
bitnet_inference.sh cli -v
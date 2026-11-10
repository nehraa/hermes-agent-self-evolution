---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (a llama.cpp fork with lookup-table optimized kernels for ternary weights).

## File Locations

| Purpose | Path |
|---------|------|
| Source repo (do not clone elsewhere) | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF (i2_s kernel, 1.2GB) | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

## Quick Start

### Interactive Chat

bash
# Using wrapper (recommended):
bitnet_inference.sh

# Direct llama-cli:
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### One-Shot Query

bash
# Wrapper handles everything:
bitnet_inference.sh "What is 2+2?"

# Direct (80 tokens, ~30s end-to-end):
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -c 2048 -t 4 -n 80 --temp 0 -p "What is 2+2?"
### HTTP API Server

bash
# Start server (default port 8089):
bitnet_inference.sh server

# Start on custom port:
bitnet_inference.sh server 9090

# Or use llama-server directly:
/home/Hermes/repos/BitNet/build/bin/llama-server \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -c 2048 -t 4 -fa -host 0.0.0.0 -port 8089
### API Test Examples

bash
# Check available models:
curl http://localhost:8089/v1/models

# Chat completion:
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "max_tokens": 80
  }'
### Wrapper Subcommands

bash
bitnet_inference.sh cli      # Interactive CLI mode
bitnet_inference.sh server   # HTTP server (default port 8089)
bitnet_inference.sh server <PORT>  # HTTP server on custom port
bitnet_inference.sh version  # Show bitnet.cpp version info
## Performance

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7-2.9 tok/sec |
| Throughput (8 threads) | ~5 tok/sec |
| RAM footprint | ~1.2GB (buffer ~1.1GB + KV cache ~300MB at 4096 ctx) |
| Cold start | ~3-5s before first token |
| One-shot (80 tokens) | ~30s end-to-end including model load |
| Verified | June 19 2026, x86_64 Linux, serving on :8081 |

### Timeout Recommendations

- **< 60 tokens**: Safe for one-shot with default timeouts
- **60-80 tokens**: May hit timeout on cold start; bump timeout or warm server first
- **> 80 tokens or repeated queries**: Use `server` mode to keep model loaded

## Architecture Notes

- **Ternary weights**: Values are -1, 0, or +1 (1.58 bits per weight after quantization)
- **i2_s kernel**: Integer-to-small lookup-table kernel, optimized for CPU inference
- **No GPU required**: All inference runs on CPU threads
- **Privacy**: All computation stays on-device; no network calls to external services
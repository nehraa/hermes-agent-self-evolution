---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (a fork of llama.cpp with lookup-table optimized kernels for ternary weights).

## File Locations

| Purpose | Path |
|---------|------|
| Source repo | `/home/Hermes/repos/BitNet` |
| CLI binary | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| Server binary | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| Model GGUF | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| Wrapper script | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

**Model specs**: 1.2GB on disk, ~1.84GB in GGUF metadata, i2_s quantization kernel.

## Quick Start

### Interactive Chat

bash
# Via wrapper script (applies chat template automatically):
bitnet_inference.sh

# Via direct CLI invocation:
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### One-Shot Query

bash
# Raw text, 80 tokens output (~30s end-to-end including load):
bitnet_inference.sh "What is 2+2?"
### HTTP API Server

bash
# Start server on default port :8089:
bitnet_inference.sh server

# Start on custom port:
bitnet_inference.sh server 9090

# List available models:
curl http://localhost:8089/v1/models

# Chat completions:
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'
### Wrapper Script Subcommands

bash
bitnet_inference.sh cli      # Launch CLI interactive mode
bitnet_inference.sh server   # Start HTTP server on default port
bitnet_inference.sh server <PORT>  # Start on specific port
bitnet_inference.sh version  # Print version info
bitnet_inference.sh "prompt" # One-shot inference
## Performance

| Metric | Value |
|--------|-------|
| Throughput (4 threads) | ~2.7–2.9 tok/sec |
| Throughput (8 threads) | ~5 tok/sec |
| RAM footprint | ~1.2GB (buffer ~1.1GB + KV cache ~300MB at 4096 ctx) |
| Cold start | ~3–5s before first token |
| One-shot (80 tokens) | ~30s end-to-end including load |

**Baseline hardware**: Intel i3-1115G4

### Timeout Guidance

- One-shot queries need ~30s minimum due to cold load
- Requests under 60s may get truncated
- For fast verification, use `-n 20` or `-n 40`
- Keep server warm between requests to avoid reload overhead

## Verified End-to-End

**Date**: June 19, 2026  
**Platform**: x86_64 Linux  
**Status**: Full chat completions working  
**Test endpoint**: `curl -X POST http://localhost:8081/v1/chat/completions -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'`
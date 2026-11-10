---
name: bitnet-inference
description: Run Microsoft's BitNet b1.58 2B4T — native 1.58-bit LLM, CPU-only via bitnet.cpp. Use when Abhinav wants on-device privacy-preserving inference without GPU, or for the Omnyxnet BitNet ML peer management layer. Fast ~2.7 tok/sec on 4 threads.
---

# BitNet b1.58 2B4T Inference

Microsoft's first native 1.58-bit LLM at the 2B-parameter scale. CPU-only inference via `bitnet.cpp` (a fork of llama.cpp with lookup-table optimized kernels for ternary weights).

## Files

| Purpose | Path |
|---------|------|
| **Repository** | `/home/Hermes/repos/BitNet` |
| **CLI binary** | `/home/Hermes/repos/BitNet/build/bin/llama-cli` |
| **Server binary** | `/home/Hermes/repos/BitNet/build/bin/llama-server` |
| **Model GGUF** | `/home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` |
| **Wrapper script** | `/home/Hermes/.hermes/scripts/bitnet_inference.sh` |

> **Note**: Do not clone the repo elsewhere. Use `/home/Hermes/repos/BitNet` as the single source of truth.

## Quick Start

bash
# Interactive chat (chat template applied automatically):
bitnet_inference.sh

# One-shot question:
bitnet_inference.sh "What is 2+2?"

# Start OpenAI-compatible API server:
bitnet_inference.sh server

# Server on custom port:
bitnet_inference.sh server 9090
## Wrapper Script Commands

bash
bitnet_inference.sh              # Interactive chat mode
bitnet_inference.sh "prompt"     # One-shot inference
bitnet_inference.sh server       # API server on default port :8089
bitnet_inference.sh server 9090  # API server on custom port
bitnet_inference.sh version      # Show bitnet.cpp version info
## Direct CLI Usage

bash
/home/Hermes/repos/BitNet/build/bin/llama-cli \
  -m /home/Hermes/models/BitNet-b1.58-2B-4T-gguf/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --color -i -c 2048 -t 4 -n 256 \
  --prompt "<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
### CLI Parameters

| Flag | Meaning | Default |
|------|---------|---------|
| `-m` | Model path | Required |
| `-c` | Context size (tokens) | 2048 |
| `-t` | Thread count | 4 |
| `-n` | Max tokens to generate | 256 |
| `-i` | Interactive mode | — |
| `--color` | Colorize output | — |

## API Server Usage

bash
# Start server
bitnet_inference.sh server

# List available models
curl http://localhost:8089/v1/models

# Chat completion
curl -X POST http://localhost:8089/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'

# Text completion
curl -X POST http://localhost:8089/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"The capital of France is","max_tokens":50}'
## Performance

| Metric | Value |
|--------|-------|
| **Throughput (4 threads)** | ~2.7–2.9 tok/sec |
| **Throughput (8 threads)** | ~5 tok/sec |
| **RAM footprint** | ~1.1GB CPU buffer + ~300MB KV cache |
| **Model file size** | 1.2GB on disk |
| **Cold start latency** | ~3–5s before first token |
| **One-shot (80 tokens)** | ~30s end-to-end |

### Timing Guidelines

- **Fast verification**: Use `-n 20` for quick smoke tests (~10s)
- **Standard inference**: `-n 40` for typical responses (~20s)
- **Long outputs**: Use server mode to amortize cold-start cost across requests
- **Timeout safety**: Set client timeouts to 60s+ for one-shot requests; server mode has no such constraint

## Chat Template

BitNet uses Llama 3 chat format:

<|begin▁of▁text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

[User message here]<|eot_id|><|start_header_id|>assistant<|end_header_id|>

[Model response]
For multi-turn conversations, append additional rounds:

...<|eot_id|><|start_header_id|>user<|end_header_id|>

[Next message]<|eot_id|><|start_header_id|>assistant<|end_header_id|>

## Model Details

| Property | Value |
|----------|-------|
| **Architecture** | BitNet b1.58 |
| **Parameters** | 2B |
| **Training tokens** | 4T |
| **Quantization** | Native 1.58-bit (ternary: -1, 0, +1) |
| **GGUF kernel** | i2_s (optimized for 2-bit lookup) |
| **File size** | 1.2GB |

## Troubleshooting

**Slow first token**: Normal — cold start includes model loading + KV cache initialization.

**Timeout on short prompts**: Increase timeout to 60s, or use server mode for persistent warm state.

**Out of memory**: Reduce context size with `-c 1024` to lower KV cache overhead.

**Server not responding**: Check port is not in use; try different port with `bitnet_inference.sh server 9091`.

## Verified Capabilities

- ✅ Interactive chat mode (June 19, 2026)
- ✅ One-shot inference
- ✅ OpenAI-compatible `/v1/chat/completions`
- ✅ OpenAI-compatible `/v1/completions`
- ✅ Model listing endpoint
- ✅ Running on x86_64 Linux

## When to Use

- **Use BitNet**: Privacy-sensitive inference, no GPU available, on-device deployment, ML peer networking (Omnyxnet)
- **Consider alternatives**: If GPU is available and latency-critical, use quantized GGUF models (e.g., Q4_K_M) for 10-50x throughput gains
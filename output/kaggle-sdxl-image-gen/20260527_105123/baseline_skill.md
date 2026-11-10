---
name: kaggle-sdxl-image-gen
description: Generate images using SDXL 1.0 on Kaggle T4 GPU — avoids FLUX gating, handles T4 VRAM limits, uses kagglerun CLI for push/exec/download workflow.
triggers:
  - generate images on kaggle gpu
  - sdxl kaggle
  - kaggle image generation t4
  - flux kaggle gated
---

# Kaggle SDXL Image Generation (T4 GPU)

## Context
Generate images using Stable Diffusion XL on Kaggle T4 GPU (16GB VRAM). FLUX models are gated on Kaggle and fail. SDXL 1.0 with stabilityai/StableDiffusionXL is the reliable approach.

## Key Findings (learned through trial and error)
- FLUX.1-dev and diffusers/FLUX.2-dev are GATED on Kaggle → auth errors
- `stabilityai/stable-diffusion-xl-base-1.0` works without auth
- Kaggle default environment has bitsandbytes version conflicts → use FP16 without quantization
- T4 (sm_75) required — P100 (sm_60) incompatible with PyTorch 2.5+ for both FLUX and SDXL
- Sequential CPU offload needed for full SDXL on 16GB VRAM
- kagglerun `--download` flag downloads files from kernel to local
- Kernel version persists — pushing new script to previously-failed kernel runs new code

## Pipeline

### 1. Write generation script
```python
#!/usr/bin/env python3
"""
SDXL 1.0 — Asset Generation
T4 (sm_75) compatible, no quantization, stabilityai model
"""

import subprocess, sys, os

print("Installing required packages...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "accelerate", "safetensors"])
print("Loading SDXL pipeline...")
import torch
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe = pipe.to("cuda")
pipe.enable_sequential_cpu_offload()
pipe.enable_vae_tiling()

prompts = [...]
for i, prompt in enumerate(prompts):
    print(f"Generating: {prompt[:40]}...")
    image = pipe(prompt, num_inference_steps=25, guidance_scale=7.5).images[0]
    filename = f"/kaggle/working/output/{i+1}_name.png"
    image.save(filename)
    print(f"Saved: {filename}")

print("=== ALL DONE ===")
```

### 2. Set Kaggle proxy URL
```bash
export KAGGLE_JUPYTER_URL="https://kkb-production.jupyter-proxy.kaggle.net/k/<kernel_id>/<token>"
```

### 3. Push and run
```bash
# Push kernel
kaggle kernels push -p /path/to/script_dir/

# Run (use background=true for long runs, notify_on_complete=true)
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/generate.py').read())" -t 1200
```

### 4. Check status / wait
```bash
# List files in kernel
~/.venvs/kagglerun/bin/kagglerun --list-files /kaggle/working/

# Poll status
~/.venvs/kagglerun/bin/kagglerun --status
```

### 5. Download results
```bash
~/.venvs/kagglerun/bin/kagglerun --download "/kaggle/working/output/1_name.png" --output "/local/path/1_name.png"
```

## Common Errors & Fixes
- **sm_60 OOM / PyTorch incompatibility**: P100 GPU — switch to T4 in notebook settings (Accelerator → GPU T4 x2)
- **bitsandbytes version conflict**: Don't use quantization — use FP16 variant directly, no bitsandbytes
- **Gated model auth error**: Use stabilityai/stable-diffusion-xl-base-1.0 instead of FLUX
- **Connection timeout**: Model download taking too long — retry, model cached on second attempt

## Verified Working Configuration
- Model: `stabilityai/stable-diffusion-xl-base-1.0` (variant=fp16)
- Offload: sequential_cpu_offload + vae_tiling
- GPU: T4 (sm_75) — must switch from P100 in notebook settings
- No bitsandbytes
- ~3-5 min model load, ~30s per image at 1024x1024

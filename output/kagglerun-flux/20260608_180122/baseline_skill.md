---
name: kagglerun-flux
description: Run FLUX image generation on Kaggle T4 GPU from terminal using kagglerun CLI, bypassing P100 sm_60 PyTorch compatibility issues
triggers:
  - run flux on kaggle t4
  - kaggle gpu t4 from terminal
  - kagglerun setup
  - flux kaggle sm_60 fix
  - wan2.2 video kaggle
  - cogvideo kaggle t4
  - video generation kaggle free gpu
  - cogvideo-5b single t4
---

# kagglerun — Run FLUX on Kaggle T4 from Terminal

## What This Solves

Kaggle CLI (`kaggle kernels push`) defaults to P100 GPU. P100 has sm_60 compute — PyTorch 2.5+ dropped sm_60 support, causing kernel failures with FLUX.

**kagglerun** connects to a running Kaggle notebook session via a Jupyter URL, letting you execute code on a T4 (sm_75) that you select manually in the notebook UI.

## Setup

### Install kagglerun

```bash
# Create a venv (don't pollute system python)
python3 -m venv ~/.venvs/kagglerun
~/.venvs/kagglerun/bin/pip install kagglerun

# Verify
~/.venvs/kagglerun/bin/kagglerun --version
```

### Get Your Kaggle Jupyter URL (one-time per session)

1. Open a Kaggle notebook (e.g., `https://kaggle.com/code/YOUR_USERNAME/flux-2-image-gen`)
2. Go to **Settings** → **Accelerator** → select **GPU T4 x2** (or T4 x1)
3. Click **Run** menu → **Kaggle Jupyter Server**
4. Copy the **VSCode Compatible URL** (has `/proxy/...token=...` format)
5. Set it as an env var so you don't pass `--url` every time:

```bash
export KAGGLE_JUPYTER_URL="<paste-the-full-url-here>"
```

## Run FLUX on T4

### Upload and execute via kagglerun

```bash
~/.venvs/kagglerun/bin/kagglerun --upload ~/kaggle/flux2-inference/generate_image.py --as generate_image.py
```

Then run:

```bash
~/.venvs/kagglerun/bin/kagglerun -t 600 generate_image.py
```

### Download the result

```bash
~/.venvs/kagglerun/bin/kagglerun --download flux_sample.png --output ~/Downloads/flux_sample.png
```

## Execution Patterns (CRITICAL)

### Pattern 1: exec() — BEST for most scripts
Upload then run with `exec(open(...).read())`. This works reliably:
```bash
~/.venvs/kagglerun/bin/kagglerun --upload /local/script.py
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/script.py').read())" -t 600
```

### Pattern 2: Pass script path directly
```bash
~/.venvs/kagglerun/bin/kagglerun /kaggle/working/generate_image.py -t 600
```
Note: `--as` flag doubles the path (`/kaggle/working//kaggle/working/`). Upload without `--as`:
```bash
~/.venvs/kagglerun/bin/kagglerun --upload /local/script.py  # no --as
~/.venvs/kagglerun/bin/kagglerun /kaggle/working/script.py -t 600
```

### Background mode is BROKEN for long tasks
```bash
# ❌ DON'T do this — the local process exits immediately but the Kaggle kernel
# keeps running. You can't wait on it, you can't poll it reliably.
~/.venvs/kagglerun/bin/kagglerun "exec(open('...').read())" -t 3600 &
# The background process exits but kernel keeps running — you're flying blind.
```

### Multiple background processes on SAME kernel = KeyboardInterrupt
NEVER run two background kagglerun processes targeting the same kernel simultaneously. They compete for the same WebSocket connection, causing `KeyboardInterrupt` errors that kill the kernel mid-execution. If you need to poll for output, use ONE background process for the generation and ONE for polling — never more, and make sure the generation finishes or the polling loop exits cleanly before starting a new generation on the same kernel.

**What actually happens**: The subprocess (`kagglerun`) forks, the parent exits immediately, and you're left with no way to know when the kernel finishes. Polling shows empty output. The `wait` action times out.

### Long-running tasks: poll manually, don't background
```bash
# Upload, run synchronously (kernel stays busy for the full duration)
~/.venvs/kagglerun/bin/kagglerun --upload /local/script.py
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/script.py').read())" -t 3600

# If it takes too long, open a NEW terminal and check manually:
~/.venvs/kagglerun/bin/kagglerun --test  # probe if still alive
~/.venvs/kagglerun/bin/kagglerun --list-files  # see if output files appeared
~/.venvs/kagglerun/bin/kagglerun --read /kaggle/working/some_log.txt  # tail logs
```

## Useful Commands

```bash
# Test connection
~/.venvs/kagglerun/bin/kagglerun --test

# Check GPU
~/.venvs/kagglerun/bin/kagglerun --gpu-info

# List files in /kaggle/working/
~/.venvs/kagglerun/bin/kagglerun --list-files

# Read a remote file
~/.venvs/kagglerun/bin/kagglerun --read /kaggle/working/some_log.txt

# Custom timeout (default 120s, FLUX needs more like 600s)
~/.venvs/kagglerun/bin/kagglerun -t 600 generate_image.py

# Execute arbitrary Python
~/.venvs/kagglerun/bin/kagglerun "import os; print(os.popen('ls /tmp').read())"
```

## FLUX Script (T4-compatible)
## FLUX Script (T4-compatible)

```python
#!/usr/bin/env python3
"""
FLUX.2-dev-bnb-4bit — Image Generation on Kaggle T4 GPU
T4 has sm_75, no sm_60 PyTorch compatibility issues.
"""

import subprocess, sys

print("Installing required packages...")
subprocess.run([
    sys.executable, "-m", "pip", "install",
    "accelerate", "bitsandbytes", "safetensors", "-q"
], check=True)

import torch
from diffusers import FluxPipeline

MODEL_ID = "diffusers/FLUX.2-dev-bnb-4bit"

print("Loading FLUX pipeline...")
pipe = FluxPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="balanced",
    offload_folder="/kaggle/working/offload",
)

pipe.enable_sequential_cpu_offload()
print(f"Device: {pipe.device}")

prompt = (
    "A realistic photograph of an elderly Indian man with white hair and a warm smile, "
    "wearing traditional kurta, sitting in soft golden afternoon light, candid portrait style, "
    "shallow depth of field, cinematic lighting"
)

print("Generating image...")
image = pipe(
    prompt,
    height=1024,
    width=1024,
    num_inference_steps=50,
    guidance_scale=3.5,
    max_sequence_length=512,
).images[0]

print("Saving image...")
image.save("/kaggle/working/flux_sample.png")
print("Saved: /kaggle/working/flux_sample.png")
print("DONE")
```

## Wan2.2 Video Generation on Kaggle (2x T4 = 32GB VRAM)

Only **TI2V-5B** fits on 2x T4. The 14B models need 80GB+ (A100).

### Wan2.2 Models
| Model | Params | VRAM | Fits 2x T4? |
|-------|--------|------|-------------|
| Wan2.2-T2V-A14B | 27B total, 14B active | 80GB min | ❌ No (needs A100/H100) |
| Wan2.2-TI2V-5B | 5B dense | 24GB (4090) | ✅ Yes |
| Wan2.2-I2V-A14B | 27B total | 80GB min | ❌ No |

**RTX PRO 6000 (96GB) for A14B**: Technically fits but SLOW — Ada Lovelace architecture not optimized for Wan2.2 MoE attention patterns. See `references/gpu-cloud-benchmarks.md` for benchmarks.

### Wan2.2 TI2V-5B Script (uses ModelScope for download)
```python
#!/usr/bin/env python3
"""
Wan2.2 TI2V-5B — 2x T4 (32GB VRAM)
Model cached to /tmp (re-downloaded each run).
Uses ModelScope SDK (blocks synchronously) for download.
"""

import os, gc

WORK_DIR = "/tmp/wan22"
HF_CACHE = "/tmp/wan22/hf_cache"
os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(HF_CACHE, exist_ok=True)
os.environ["HF_HOME"] = HF_CACHE
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE
os.chdir(WORK_DIR)

import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

gc.collect(); torch.cuda.empty_cache()

# Clone Wan2.2 repo
if not os.path.exists(f"{WORK_DIR}/Wan2.2"):
    print("Cloning Wan2.2...")
    os.system("git clone --depth 1 https://github.com/Wan-Video/Wan2.2.git Wan2.2")

os.chdir(f"{WORK_DIR}/Wan2.2")

# Install deps
os.system("pip install -q torch transformers accelerate safetensors imageio pillow")
os.system("pip install -q modelscope")

# Download model (synchronous, blocks until done)
MODEL_DIR = f"{WORK_DIR}/Wan2.2-TI2V-5B"
if not os.path.exists(MODEL_DIR):
    print("Downloading Wan2.2-TI2V-5B (~20GB, may take 30-40 mins)...")
    from modelscope import snapshot_download
    snapshot_download('Wan-AI/Wan2.2-TI2V-5B', cache_dir=WORK_DIR)
    src = f"{WORK_DIR}/Wan-AI/Wan2.2-TI2V-5B"
    if os.path.exists(src):
        os.rename(src, MODEL_DIR)

# Generate
prompt = "A serene lake at sunset with mountains, cinematic lighting"
print(f"Generating: {prompt}")

ret = os.system(
    f"python generate.py "
    f"--task ti2v-5B --size 1280*704 "
    f"--ckpt_dir {MODEL_DIR} "
    f"--offload_model True --convert_model_dtype --t5_cpu "
    f"--prompt \"{prompt}\""
)

if ret == 0:
    for f in os.listdir(WORK_DIR):
        if f.endswith(".mp4"):
            print(f"Output: {WORK_DIR}/{f}")
```

### Key Wan2.2 Notes
- **Correct HF repo**: `Wan-AI/Wan2.2-T2V-A14B`, `Wan-AI/Wan2.2-TI2V-5B` — NOT ByteDance/HunyuanVideo
- **Correct download**: Use `modelscope` SDK, not `huggingface-cli` (HF needs auth for these models)
- **Output location**: Check `{WORK_DIR}/Wan2.2/*.mp4` after generation
- **Total download size**: ~20GB for TI2V-5B

## CogVideoX-5B on Single T4 (15.6GB VRAM)

CogVideoX-5B works on **single T4** — 5B params × 2 bytes (float16) ≈ 10GB, well within 15.6GB.

### What DOESN'T work:
- **`device_map="balanced"`** — causes `RuntimeError: mat1 is on cuda:0, other tensors on cpu` (device placement bug in CogVideoX with balanced device map)
- **`enable_sequential_cpu_offload()`** — too slow, gets killed by Kaggle's notebook timeout before completing
- **Dual T4 with balanced** — same device placement bug

### What WORKS:
```python
pipe = CogVideoXPipeline.from_pretrained(
    'THUDM/CogVideoX-5b',
    cache_dir='/tmp/cogvideo5b_model',
    torch_dtype=torch.float16,
)
pipe = pipe.to('cuda')  # single GPU, no device_map
# Run inference directly
video = pipe(prompt, num_frames=49, num_inference_steps=50, guidance_scale=7.5).frames[0]
```

### Kaggle Notebook Timeout Issue:
Kaggle kills notebooks that produce no output for ~5 minutes. CogVideoX-5B inference takes 15-25 min with only a final print — kernel gets killed mid-run. **Workaround**: Use a new kernel session each time. The model loads fast from `/tmp` cache (~2-3 min), so kernel startup overhead doesn't compound.

### VRAM Cleanup:
```python
import gc, torch
del pipe, video
gc.collect(); torch.cuda.empty_cache()
```

## Kaggle CLI Alternative to kagglerun

You can also push/pull scripts via Kaggle CLI instead of kagglerun:
```bash
kaggle kernels push -p /local/path   # push
kaggle kernels pull USER/kernel-name  # pull
kaggle kernels status USER/kernel-name # check
kaggle kernels output USER/kernel-name # download logs
```

**Limitation**: Both kagglerun and CLI inherit the notebook's configured GPU. Kaggle defaults to P100 (sm_60) which is **incompatible** with FLUX and SDXL on PyTorch 2.5+ (sm_60 dropped). The P100 causes:
- FLUX + bitsandbytes: `OutOfMemoryError` (P100 16GB but model too large)
- SDXL + fp16: `CUDA error: no kernel image is available for device` (sm_60 not supported)

**Fix**: In Kaggle notebook settings, set Accelerator to **GPU T4 x2** (or T4 x1) before running. T4 is sm_75, fully supported.

## Key Differences from Kaggle CLI

| | Kaggle CLI | kagglerun |
|---|---|---|
| GPU selection | Defaults to P100, no choice | You pick T4/P100/H100 in notebook UI |
| Requires | API + kernel push | Running notebook + Jupyter URL |
| Use case | CI/CD, automated runs | Interactive development, trying different GPUs |
| sm_60 issue | Breaks on P100 with PyTorch 2.5+ | T4 avoids this entirely |

## Pitfalls

- **Session expires**: Kaggle Jupyter sessions time out. If the notebook is idle too long, reconnect and get a new URL.
- **T4 x2 vs T4 x1**: 2x T4 gives 32GB VRAM total but requires `DataParallel` in your code. Single T4 (16GB) works for FLUX.2-dev-bnb-4bit with CPU offload.
- **Timeout**: Default 120s is too short for FLUX model loading. Use `-t 600`.
- **No browser**: kagglerun doesn't open notebooks — you still need the browser to set GPU type and get the Jupyter URL.
- **`--as` flag bug**: Using `--as remote.py` doubles the path → `/kaggle/working//kaggle/working/remote.py`. Upload without `--as`.
- **`os.system()` in scripts**: Downloads with `os.system("pip install ...")`, `os.system("git clone ...")` etc. run asynchronously — the subprocess exits immediately but the kernel keeps running. For downloads that must complete before continuing, use a synchronous blocking call like `subprocess.run()` or the SDK directly (e.g., `from modelscope import snapshot_download`).
- **`torch.cuda.get_device_properties(0).total_mem`**: Wrong attribute. Correct is `.total_memory` (in bytes).
- **RTX PRO 6000 for Wan2.2 A14B**: Skip it — fits but 40-50% slower than A100 on this model. See `references/gpu-cloud-benchmarks.md`.
- **HF auth for gated models**: CogVideoX-16B and Wan2.2 need HuggingFace login. Use ModelScope SDK instead (free, no auth).
- **Large model downloads**: ModelScope downloads can take 30-40 minutes at ~7MB/s. Run synchronously with timeout ≥3600s.

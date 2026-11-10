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

Kaggle CLI (`kaggle kernels push`) defaults to **P100 GPU**. P100 uses **sm_60 compute capability**, and **PyTorch 2.5+ dropped sm_60 support**, causing kernel failures with FLUX, CogVideo, and other modern models.

**kagglerun** connects to a running Kaggle notebook session via Jupyter URL, letting you execute code on a T4 (sm_75) that you select manually in the notebook UI.

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Kaggle account | Free tier works |
| T4 GPU | Select via notebook UI (not CLI) |
| Local Python | 3.8+ required |
| Internet connection | For uploading scripts and downloading outputs |

## Setup

### 1. Install kagglerun

Create a virtual environment to avoid conflicts:

bash
# Create and activate virtual environment
python3 -m venv ~/.venvs/kagglerun
source ~/.venvs/kagglerun/bin/activate

# Install kagglerun
pip install kagglerun

# Verify installation
kagglerun --version
### 2. Get Your Kaggle Jupyter URL

Do this once per session:

1. Open a Kaggle notebook (or create a new one)
2. Go to **Settings** → **Accelerator** → select **GPU T4 x2** or **T4 x1**
3. Wait for the GPU to initialize (shows in top-right corner)
4. Click **Run** menu → **Kaggle Jupyter Server**
5. Copy the **VSCode Compatible URL** (format: `https://.../proxy/...token=...`)
6. Export it:

bash
export KAGGLE_JUPYTER_URL="https://www.kaggle.com/proxy/YOUR_TOKEN_HERE"
> **Tip:** Add the export line to your `~/.bashrc` or `~/.zshrc` for persistence across terminal sessions.

## Usage

### Upload a Script

bash
kagglerun --upload ~/scripts/generate_image.py --as generate_image.py
### Execute a Script

bash
# Run with 600-second timeout
kagglerun -t 600 generate_image.py
Adjust the timeout (`-t`) based on your workload:
- Image generation: 300-600 seconds
- Video generation: 600-1800 seconds
- Fine-tuning: 1800+ seconds

### Download Results

bash
kagglerun --download output.png --output ~/Downloads/output.png
### Check Status

bash
kagglerun --status
## Execution Patterns

### Pattern 1: exec() — Recommended

This is the most reliable pattern for running local scripts:

bash
# Step 1: Upload the script
kagglerun --upload /local/script.py

# Step 2: Execute using exec()
kagglerun "exec(open('/kaggle/working/script.py').read())"
### Pattern 2: Direct Python Code

Execute inline Python code:

bash
kagglerun "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
### Pattern 3: Combined Upload and Execute

bash
kagglerun --upload script.py "exec(open('/kaggle/working/script.py').read())"
## Example: FLUX Image Generation

### 1. Create your script locally

`flux_generate.py`:

python
import torch
from diffusers import FluxPipeline

print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda")

image = pipe(
    "A serene mountain landscape at sunset",
    num_inference_steps=50,
    guidance_scale=3.5,
    height=1024,
    width=1024
).images[0]

image.save("flux_output.png")
print("Saved: flux_output.png")
### 2. Upload and run

bash
kagglerun --upload flux_generate.py --as flux_generate.py
kagglerun -t 900 "exec(open('/kaggle/working/flux_generate.py').read())"
### 3. Download results

bash
kagglerun --download flux_output.png --output ./flux_output.png
## Example: CogVideo Video Generation

`cogvideo_generate.py`:

python
import torch
from diffusers import CogVideoXPipeline

print(f"GPU: {torch.cuda.get_device_name(0)}")

pipe = CogVideoXPipeline.from_pretrained(
    "THUDM/CogVideoX-5B",
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda")

video = pipe(
    prompt="A cat playing piano in a jazz club, cinematic lighting",
    num_inference_steps=50,
    num_frames=49,
    guidance_scale=6.0
).frames[0]

video.save("cogvideo_output.mp4")
print("Saved: cogvideo_output.mp4")
Run with extended timeout:

bash
kagglerun --upload cogvideo_generate.py --as cogvideo_generate.py
kagglerun -t 1800 "exec(open('/kaggle/working/cogvideo_generate.py').read())"
## Troubleshooting

### "CUDA out of memory"

- Reduce image resolution (try 512x512 or 768x768)
- Reduce `num_inference_steps` (try 20-30)
- Use `FP16` instead of `BF16` where supported
- For T4 x2, ensure you select T4 x1 if memory-constrained

### "Connection refused" or "Invalid token"

- Your Kaggle session may have expired
- Regenerate the Jupyter URL from the notebook
- Ensure GPU is still assigned (check notebook UI)

### "Module not found"

Add package installations to your script:

python
import subprocess
subprocess.run(["pip", "install", "transformers", "accelerate"], check=True)
Or install before uploading:

bash
kagglerun "import subprocess; subprocess.run(['pip', 'install', 'diffusers'], check=True)"
### Script hangs indefinitely

- Always use `-t` timeout flag
- Check Kaggle session is still active
- Verify internet connection is stable

## Session Management

### End session cleanly

bash
# From the notebook UI: Runtime → Manage sessions → End session
# Or just close the notebook tab
### Extend session

Sessions typically timeout after 60-90 minutes of inactivity. To extend:
1. Keep the notebook tab open
2. Or run a quick command periodically:

bash
kagglerun "print('Session active')"
## Quick Reference

| Task | Command |
|------|---------|
| Upload script | `kagglerun --upload path/to/script.py` |
| Run with timeout | `kagglerun -t 600 script.py` |
| Run inline code | `kagglerun "python_code_here"` |
| Download file | `kagglerun --download filename --output ./local/path` |
| Check status | `kagglerun --status` |
| Set Jupyter URL | `export KAGGLE_JUPYTER_URL="..."` |

## GPU Memory Guide

| Model | Precision | Resolution | T4 VRAM Usage |
|-------|-----------|------------|---------------|
| FLUX.1-dev | BF16 | 1024x1024 | ~18 GB |
| FLUX.1-dev | FP16 | 1024x1024 | ~14 GB |
| FLUX.1-schnell | BF16 | 1024x1024 | ~16 GB |
| CogVideoX-5B | BF16 | 480p | ~22 GB |
| CogVideoX-5B | FP16 | 480p | ~18 GB |

For T4 x2 (16 GB per GPU), use FP16 and lower resolutions.
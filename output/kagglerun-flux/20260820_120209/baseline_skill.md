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

Kaggle CLI (`kaggle kernels push`) defaults to P100 GPU. P100 uses **sm_60 compute capability**, and **PyTorch 2.5+ dropped sm_60 support**, causing kernel failures with FLUX and other modern models.

**kagglerun** connects to a running Kaggle notebook session via a Jupyter URL, letting you execute code on a T4 (sm_75) that you select manually in the notebook UI.

## Prerequisites

- A Kaggle account
- T4 GPU available (select via notebook UI, not CLI)
- Python 3.8+ on your local machine

## Setup

### 1. Install kagglerun

Create a virtual environment to avoid polluting system Python:

bash
python3 -m venv ~/.venvs/kagglerun
~/.venvs/kagglerun/bin/pip install kagglerun

# Verify installation
~/.venvs/kagglerun/bin/kagglerun --version
### 2. Get Your Kaggle Jupyter URL (one-time per session)

1. Open a Kaggle notebook (e.g., `https://kaggle.com/code/YOUR_USERNAME/flux-2-image-gen`)
2. Go to **Settings** → **Accelerator** → select **GPU T4 x2** (or T4 x1)
3. Click **Run** menu → **Kaggle Jupyter Server**
4. Copy the **VSCode Compatible URL** (format: `https://.../proxy/...token=...`)
5. Export it as an environment variable:

bash
export KAGGLE_JUPYTER_URL="<paste-the-full-url-here>"
> **Tip:** Add this to your `~/.bashrc` or `~/.zshrc` to persist across sessions.

## Usage

### Upload a Script

bash
~/.venvs/kagglerun/bin/kagglerun --upload ~/kaggle/flux2-inference/generate_image.py --as generate_image.py
### Execute a Script

bash
~/.venvs/kagglerun/bin/kagglerun -t 600 generate_image.py
The `-t 600` flag sets a 600-second timeout. Adjust based on your workload.

### Download Results

bash
~/.venvs/kagglerun/bin/kagglerun --download flux_sample.png --output ~/Downloads/flux_sample.png
## Execution Patterns

### Pattern 1: exec() — Recommended for Most Scripts

This is the most reliable pattern for running local scripts:

bash
# Step 1: Upload the script
~/.venvs/kagglerun/bin/kagglerun --upload /local/script.py

# Step 2: Execute using exec()
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/script.py').read())" -t 600
**Why this works:** The `exec()` approach avoids path duplication issues that occur with the `--as` flag.

### Pattern 2: Pass Script Path Directly

Upload without `--as`, then reference the working directory path:

bash
# Upload without --as flag
~/.venvs/kagglerun/bin/kagglerun --upload /local/script.py

# Execute using the remote path
~/.venvs/kagglerun/bin/kagglerun /kaggle/working/script.py -t 600
> **Warning:** Using `--as` with this pattern causes path duplication (`/kaggle/working//kaggle/working/`).

## Example: FLUX Image Generation

### Local Script: `generate_image.py`

python
import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

image = pipe(
    "A serene mountain landscape at sunset",
    num_inference_steps=50,
    guidance_scale=3.5,
).images[0]

image.save("/kaggle/working/flux_sample.png")
print("Image saved to /kaggle/working/flux_sample.png")
### Execute on Kaggle T4

bash
# Upload the script
~/.venvs/kagglerun/bin/kagglerun --upload generate_image.py

# Run with exec() pattern
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/generate_image.py').read())" -t 900

# Download the result
~/.venvs/kagglerun/bin/kagglerun --download flux_sample.png --output ~/Downloads/flux_sample.png
## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused` | Re-copy the Jupyter URL from Kaggle (it expires per session) |
| `sm_60` error persists | Ensure you selected T4 in notebook settings, not P100 |
| Script not found | Verify upload succeeded; check remote path matches execution path |
| Timeout exceeded | Increase `-t` value or reduce `num_inference_steps` |
| Path duplication (`/kaggle/working//kaggle/working/`) | Use Pattern 1 (exec()) or upload without `--as` flag |

## Quick Reference

bash
# Full workflow
~/.venvs/kagglerun/bin/kagglerun --upload script.py
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/script.py').read())" -t 600
~/.venvs/kagglerun/bin/kagglerun --download output.png --output ./output.png
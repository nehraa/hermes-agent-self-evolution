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

Kaggle CLI (`kaggle kernels push`) defaults to **P100 GPU**. P100 has **sm_60 compute capability**, and **PyTorch 2.5+ dropped sm_60 support**, causing kernel failures with FLUX and other modern models.

**kagglerun** connects to a running Kaggle notebook session via a Jupyter URL, letting you execute code on a T4 (sm_75) that you select manually in the notebook UI.

## Prerequisites

- A Kaggle account
- T4 GPU available (select via notebook UI, not CLI)
- Python 3.8+ on your local machine

## Installation

Create a virtual environment to avoid polluting system Python:

bash
python3 -m venv ~/.venvs/kagglerun
~/.venvs/kagglerun/bin/pip install kagglerun

# Verify installation
~/.venvs/kagglerun/bin/kagglerun --version
## Session Setup

### 1. Get Your Kaggle Jupyter URL (one-time per session)

1. Open a Kaggle notebook (e.g., `https://kaggle.com/code/YOUR_USERNAME/flux-2-image-gen`)
2. Go to **Settings** → **Accelerator** → select **GPU T4 x2** (or T4 x1)
3. Click **Run** menu → **Kaggle Jupyter Server**
4. Copy the **VSCode Compatible URL** (format: `https://.../proxy/...token=...`)

### 2. Configure the Environment Variable

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
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/script.py').read())"
### Pattern 2: Direct Code Execution

Run code directly without uploading a file:

bash
~/.venvs/kagglerun/bin/kagglerun "import torch; print(torch.cuda.get_device_name(0))"
### Pattern 3: Interactive Mode

For debugging or iterative work:

bash
~/.venvs/kagglerun/bin/kagglerun --interactive
## Common Workflow Example

bash
# 1. Configure URL (do once per session)
export KAGGLE_JUPYTER_URL="https://...."

# 2. Upload your inference script
~/.venvs/kagglerun/bin/kagglerun --upload ./generate.py --as generate.py

# 3. Execute with timeout
~/.venvs/kagglerun/bin/kagglerun -t 600 "exec(open('/kaggle/working/generate.py').read())"

# 4. Download outputs
~/.venvs/kagglerun/bin/kagglerun --download output.png --output ./output.png
## FLUX.1-schnell Example

python
# generate.py — Run on Kaggle T4 via kagglerun
import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

image = pipe(
    "A cosmic cat floating through space",
    num_inference_steps=4,
    guidance_scale=0.0,
    max_sequence_length=256
).images[0]

image.save("/kaggle/working/flux_output.png")
print("Saved to /kaggle/working/flux_output.png")
Run it:

bash
~/.venvs/kagglerun/bin/kagglerun --upload generate.py --as generate.py
~/.venvs/kagglerun/bin/kagglerun -t 900 "exec(open('/kaggle/working/generate.py').read())"
~/.venvs/kagglerun/bin/kagglerun --download flux_output.png --output ./flux_output.png
## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused` | Re-copy the Jupyter URL from the notebook |
| `sm_60` error | Ensure you selected T4 in notebook UI, not P100 |
| Timeout | Increase `-t` value or reduce model size |
| Session expired | Refresh the notebook and get a new Jupyter URL |
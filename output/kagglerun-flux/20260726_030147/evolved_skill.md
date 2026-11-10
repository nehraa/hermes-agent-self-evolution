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

The Kaggle CLI (`kaggle kernels push`) defaults to **P100 GPU**, which has **sm_60 compute capability**. Since **PyTorch 2.5+ dropped sm_60 support**, modern models like FLUX fail with kernel errors.

**kagglerun** bypasses this by connecting to a running Kaggle notebook session via Jupyter URL, letting you execute code on a **T4 GPU (sm_75)** that you select manually in the notebook UI.

## Prerequisites

- A Kaggle account with T4 GPU access
- A running Kaggle notebook with GPU enabled (T4 x1 or T4 x2)
- Python 3.8+ installed locally
- `curl` available on your system

## Setup

### 1. Install kagglerun

Create a virtual environment to isolate dependencies:

bash
python3 -m venv ~/.venvs/kagglerun
~/.venvs/kagglerun/bin/pip install kagglerun

# Verify installation
~/.venvs/kagglerun/bin/kagglerun --version
### 2. Enable GPU in Kaggle Notebook

1. Open any Kaggle notebook (e.g., `https://kaggle.com/code/YOUR_USERNAME/flux-2-image-gen`)
2. Go to **Settings** → **Accelerator**
3. Select **GPU T4 x2** or **GPU T4 x1**
4. Click **Save**

### 3. Get the Jupyter URL (per session)

1. Click the **Run** menu in the notebook toolbar
2. Select **Kaggle Jupyter Server**
3. Copy the **VSCode Compatible URL** (format: `https://www.kaggle.com/kernels.../proxy/...token=...`)

4. Export it as an environment variable:

bash
export KAGGLE_JUPYTER_URL="https://www.kaggle.com/kernels/.../proxy/...token=..."
> **Tip:** Add this line to `~/.bashrc` or `~/.zshrc` to persist across sessions:
> ```bash
> echo 'export KAGGLE_JUPYTER_URL="your-url-here"' >> ~/.bashrc
> ```

## Usage

### Basic Workflow

| Action | Command |
|--------|---------|
| Upload a script | `kagglerun --upload /path/to/script.py --as script.py` |
| Execute with timeout | `kagglerun -t 600 script.py` |
| Download output | `kagglerun --download output.png --output ./output.png` |

### Example: Generate FLUX Image

bash
# 1. Upload your generation script
~/.venvs/kagglerun/bin/kagglerun --upload ~/projects/flux2/generate.py --as generate.py

# 2. Execute with 10-minute timeout
~/.venvs/kagglerun/bin/kagglerun -t 600 generate.py

# 3. Download the generated image
~/.venvs/kagglerun/bin/kagglerun --download output.png --output ./flux_result.png
## Execution Patterns

### Pattern 1: exec() — Most Reliable

Recommended for running local scripts:

bash
# Upload the script
kagglerun --upload /local/script.py

# Execute using exec()
kagglerun "exec(open('/kaggle/working/script.py').read())"
### Pattern 2: Direct Code Execution

For quick one-liners or small snippets:

bash
kagglerun "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
### Pattern 3: Interactive Session

For debugging or iterative work:

bash
# Start an interactive Python session on the T4
kagglerun -i
## Common Issues

| Issue | Solution |
|-------|----------|
| `Connection refused` | Regenerate Jupyter URL (it expires) and re-export `KAGGLE_JUPYTER_URL` |
| `ModuleNotFoundError` | Install dependencies in your script first: `!pip install <package>` |
| Timeout errors | Increase timeout: `-t 1800` for 30 minutes |
| P100 still selected | Ensure you selected GPU in notebook settings before copying Jupyter URL |

## Example: FLUX Image Generation Script

Save this as `generate.py` and upload it:

python
import torch
from diffusers import FluxPipeline

print(f"Device: {torch.cuda.get_device_name(0)}")
print(f"CUDA available: {torch.cuda.is_available()}")

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

image = pipe(
    "A serene mountain landscape at sunset",
    num_inference_steps=50,
    guidance_scale=3.5
).images[0]

image.save("/kaggle/working/flux_sample.png")
print("Saved: /kaggle/working/flux_sample.png")
## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `KAGGLE_JUPYTER_URL` | The Jupyter proxy URL from your Kaggle notebook | Yes |

Set it before each session:

bash
export KAGGLE_JUPYTER_URL="https://www.kaggle.com/kernels/.../token=..."
## Quick Reference

bash
# Full workflow example
export KAGGLE_JUPYTER_URL="your-session-url"
kagglerun --upload generate.py --as generate.py
kagglerun -t 900 generate.py
kagglerun --download flux_sample.png --output ~/Downloads/flux_sample.png
- **Upload**: `--upload <local_path> --as <remote_name>`
- **Execute**: `-t <seconds> <script.py>`
- **Download**: `--download <remote_path> --output <local_path>`
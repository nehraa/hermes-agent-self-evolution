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

The Kaggle CLI (`kaggle kernels push`) defaults to **P100 GPUs**, which use the **sm_60 compute capability**. Since **PyTorch 2.5+ dropped sm_60 support**, any kernel using the CLI will fail when loading modern models like FLUX.

**kagglerun** solves this by connecting to a running Kaggle notebook session through its Jupyter URL. You manually select a **T4 GPU (sm_75)** in the notebook UI, then execute code remotely from your terminal.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Kaggle account | Free tier works |
| T4 GPU | Select manually in notebook UI (not via CLI) |
| Python | 3.8+ on your local machine |
| Virtual environment | Recommended to avoid conflicts |

---

## Installation

### 1. Create a Virtual Environment

bash
python3 -m venv ~/.venvs/kagglerun
### 2. Install kagglerun

bash
~/.venvs/kagglerun/bin/pip install kagglerun
### 3. Verify Installation

bash
~/.venvs/kagglerun/bin/kagglerun --version
---

## Session Setup

### Step 1: Open a Kaggle Notebook

Open any notebook, for example:
https://www.kaggle.com/code/YOUR_USERNAME/flux-2-image-gen
### Step 2: Select T4 GPU

1. Click **Settings** (gear icon)
2. Navigate to **Accelerator**
3. Select **GPU T4 x2** (or **GPU T4 x1** for lighter workloads)
4. Click **Save**

### Step 3: Start the Jupyter Server

1. Click the **Run** menu
2. Select **Kaggle Jupyter Server**
3. Wait for the server to start

### Step 4: Copy the VSCode Compatible URL

1. Look for the **VSCode Compatible URL** shown in the notebook
2. The format is: `https://.../proxy/...token=...`
3. Copy the **entire URL**

### Step 5: Export the URL

bash
export KAGGLE_JUPYTER_URL="https://www.kaggle.com/kernels/ws-xxxx/proxy/...?token=xxxx"
> **Tip:** Add this line to your `~/.bashrc` or `~/.zshrc` so it persists across terminal sessions.

---

## Usage

### Upload a Script

bash
~/.venvs/kagglerun/bin/kagglerun --upload ~/kaggle/flux2-inference/generate_image.py --as generate_image.py
### Execute a Script

bash
~/.venvs/kagglerun/bin/kagglerun -t 600 generate_image.py
- `-t 600` sets a 600-second timeout. Adjust based on your workload.
- For video generation or large models, use a longer timeout (1800+ seconds).

### Download Results

bash
~/.venvs/kagglerun/bin/kagglerun --download flux_sample.png --output ~/Downloads/flux_sample.png
### Run Inline Code

bash
~/.venvs/kagglerun/bin/kagglerun "exec(open('/kaggle/working/generate.py').read())"
---

## Complete Workflow Example

bash
# 1. Set your session URL
export KAGGLE_JUPYTER_URL="https://www.kaggle.com/kernels/ws-xxxx/proxy/...?token=xxxx"

# 2. Upload your generation script
~/.venvs/kagglerun/bin/kagglerun --upload ~/projects/flux/generate.py --as generate.py

# 3. Execute with 10-minute timeout
~/.venvs/kagglerun/bin/kagglerun -t 600 "exec(open('/kaggle/working/generate.py').read())"

# 4. Download output
~/.venvs/kagglerun/bin/kagglerun --download output.png --output ~/results/output.png
---

## Troubleshooting

### Error: "Connection refused" or "Cannot connect to Jupyter"

**Cause:** Jupyter server not running or URL expired.

**Fix:**
1. Refresh the notebook page
2. Ensure **Run → Kaggle Jupyter Server** is active
3. Copy a fresh VSCode Compatible URL
4. Re-export the `KAGGLE_JUPYTER_URL` variable

### Error: "Timeout waiting for execution"

**Cause:** Script took longer than the timeout.

**Fix:** Re-run with a longer timeout:
bash
~/.venvs/kagglerun/bin/kagglerun -t 1800 generate.py
### Error: "File not found" on download

**Cause:** The file doesn't exist in `/kaggle/working/` or path is incorrect.

**Fix:** List available files first:
bash
~/.venvs/kagglerun/bin/kagglerun "import os; print(os.listdir('/kaggle/working'))"
### GPU Not Detected in Script

**Cause:** Notebook accelerator may have reset.

**Fix:**
1. Check notebook **Settings → Accelerator** is set to T4
2. Restart the Jupyter server: **Run → Kaggle Jupyter Server**
3. Get a fresh URL and update `KAGGLE_JUPYTER_URL`

---

## Recommended FLUX Script Structure

python
# generate.py
import torch
from diffusers import FluxPipeline

# Ensure we're using the T4 GPU
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16,
    variant="fp16"
)
pipe = pipe.to("cuda")

# Generate
result = pipe(
    prompt="your prompt here",
    guidance_scale=3.5,
    num_inference_steps=50,
    height=1024,
    width=1024
).images[0]

result.save("output.png")
print("Saved to output.png")
---

## Key Benefits

| Feature | Benefit |
|---------|---------|
| Direct T4 access | Bypass sm_60 PyTorch limitations |
| Terminal workflow | No browser tab needed; run in background |
| Script execution | Full Python control, not cell-by-cell |
| Free GPU | Use Kaggle's free T4 hours for heavy generation |
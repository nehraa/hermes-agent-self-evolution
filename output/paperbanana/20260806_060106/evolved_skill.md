---
category: software-development
name: paperbanana
description: Generate publication-quality academic diagrams from paper methodology text
license: MIT-0
dependencies:
  env:
    - OPENROUTER_API_KEY (recommended)
    - GOOGLE_API_KEY (alternative)
  runtime:
    - python3
    - uv
---

# PaperBanana

Generate publication-quality academic diagrams and pipeline figures from a paper's methodology section and figure caption. PaperBanana orchestrates a multi-agent pipeline to produce camera-ready figures suitable for venues like NeurIPS, ICML, and ACL.

**Pipeline agents:** Retriever → Planner → Stylist → Visualizer → Critic

## Environment Setup

### 1. Install Dependencies

bash
cd <repo-root>
uv pip install -r requirements.txt
### 2. Configure API Key

Set your API key via environment variable or in `configs/model_config.yaml`.

| Provider | Key | Notes |
|----------|-----|-------|
| **OpenRouter** (recommended) | `OPENROUTER_API_KEY` | Single key for text reasoning + image generation |
| **Google Gemini** (alternative) | `GOOGLE_API_KEY` | Direct Gemini API access |

bash
# Option A: OpenRouter (recommended)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Option B: Google Gemini
export GOOGLE_API_KEY="your-key-here"
> **Note:** If both keys are configured, OpenRouter takes priority.

## Usage

### Basic Example

bash
python skill/run.py \
  --content "The model consists of an encoder with 12 layers, followed by a attention mechanism that aggregates features across timesteps..." \
  --caption "Figure 1: Overview of our proposed architecture" \
  --task diagram \
  --output output.png
### With File Input

bash
python skill/run.py \
  --content-file path/to/methodology.txt \
  --caption "Figure 2: Training pipeline with data augmentation stages" \
  --task diagram \
  --output pipeline_diagram.png
## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--content` | Yes* | — | Methodology section text to visualize |
| `--content-file` | Yes* | — | Path to file containing method text (alternative to `--content`) |
| `--caption` | Yes | — | Figure caption or description of visual intent |
| `--task` | No | `diagram` | Task type: currently only `diagram` is supported |
| `--output` | No | `output.png` | Output image file path |
| `--aspect-ratio` | No | `21:9` | Aspect ratio: `21:9`, `16:9`, or `3:2` |
| `--max-critic-rounds` | No | `3` | Maximum critic refinement iterations (higher = more polish, slower) |
| `--num-candidates` | No | `10` | Number of parallel candidates to generate for diversity |
| `--retrieval-setting` | No | `auto` | Retrieval mode: `auto`, `manual`, `random`, or `none` |
| `--main-model-name` | No | `gemini-3.1-pro-preview` | VLM model for reasoning agents |
| `--image-gen-model-name` | No | `gemini-3.1-flash-image-preview` | Image generation model. Also supports `gemini-3-pro-image-preview` |
| `--exp-mode` | No | `demo_full` | Pipeline mode: `demo_full` (includes Stylist) or `demo_planner_critic` (Planner + Critic only) |

*\*One of `--content` or `--content-file` is required.*

## Output

The tool generates a PNG image at the specified `--output` path. For best results:

- Provide detailed methodology text describing the pipeline/workflow
- Include a clear figure caption describing what the figure should show
- Experiment with `--num-candidates` for more options
- Use `--max-critic-rounds` to control refinement quality
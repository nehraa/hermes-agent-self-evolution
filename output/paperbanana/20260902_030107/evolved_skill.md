---
category: software-development
description: Generate publication-quality academic diagrams and pipeline figures from a paper's methodology section and figure caption.
name: paperbanana
---

---
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

Generate publication-quality academic diagrams and pipeline figures from a paper's methodology section and figure caption. PaperBanana orchestrates a multi-agent pipeline (Retriever, Planner, Stylist, Visualizer, Critic) to produce camera-ready figures suitable for venues like NeurIPS, ICML, and ACL.

## Environment Setup

### 1. Install Dependencies

bash
cd <repo-root>
uv pip install -r requirements.txt
### 2. Configure API Keys

Set your API key via environment variable or in `configs/model_config.yaml`.

**Option A (Recommended): OpenRouter API key**

Provides one key for both text reasoning and image generation:

bash
export OPENROUTER_API_KEY="sk-or-v1-..."
**Option B: Google API key**

Direct access to Gemini API:

bash
export GOOGLE_API_KEY="your-key-here"
> **Note:** If both keys are configured, OpenRouter is used by default.

## Usage

### Basic Command

bash
python skill/run.py \
  --content "METHOD_TEXT" \
  --caption "FIGURE_CAPTION" \
  --task diagram \
  --output output.png
### Using a File Input

bash
python skill/run.py \
  --content-file path/to/methodology.txt \
  --caption "Figure 2: Overview of our proposed pipeline" \
  --task diagram \
  --output output.png
## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--content` | Yes* | — | Method section text to visualize |
| `--content-file` | Yes* | — | Path to file containing method text (alternative to `--content`) |
| `--caption` | Yes | — | Figure caption or visual intent description |
| `--task` | No | `diagram` | Task type: `diagram` |
| `--output` | No | `output.png` | Output image file path |
| `--aspect-ratio` | No | `21:9` | Aspect ratio: `21:9` (widescreen), `16:9` (standard), or `3:2` (print-friendly) |
| `--max-critic-rounds` | No | `3` | Maximum critic refinement iterations (higher = more polish, slower) |
| `--num-candidates` | No | `10` | Number of parallel candidates to generate (higher = more options, slower) |
| `--retrieval-setting` | No | `auto` | Retrieval mode: `auto` (context-aware), `manual` (user-guided), `random` (stochastic), or `none` (no retrieval) |
| `--main-model-name` | No | `gemini-3.1-pro-preview` | Main model for VLM agents. Provider auto-detected from configured API key |
| `--image-gen-model-name` | No | `gemini-3.1-flash-image-preview` | Model for image generation. Also supports `gemini-3-pro-image-preview` |
| `--exp-mode` | No | `demo_full` | Pipeline mode: `demo_full` (includes Stylist agent for refined styling) or `demo_planner_critic` (faster, no Stylist) |

*One of `--content` or `--content-file` is required.

## Pipeline Architecture

PaperBanana uses a multi-agent pipeline to ensure high-quality output:

1. **Retriever** — Searches and retrieves relevant reference diagrams
2. **Planner** — Analyzes method text and creates structural plan
3. **Stylist** — Applies academic styling and visual conventions
4. **Visualizer** — Generates the diagram using image generation model
5. **Critic** — Reviews output and suggests refinements (runs up to `--max-critic-rounds`)

## Quick Reference

bash
# Generate with default settings
python skill/run.py \
  --content "We process input X through encoder E, then apply attention layer A..." \
  --caption "Figure 1: Architecture overview" \
  --output architecture.png

# High-quality output with more candidates
python skill/run.py \
  --content-file paper_methods.txt \
  --caption "Figure 2: Training pipeline" \
  --num-candidates 20 \
  --max-critic-rounds 5 \
  --output pipeline.png

# Fast generation without Stylist
python skill/run.py \
  --content "Method description here" \
  --caption "Quick sketch" \
  --exp-mode demo_planner_critic \
  --output quick.png
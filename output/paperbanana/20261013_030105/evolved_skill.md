---
category: software-development
description: Generate publication-quality academic diagrams from paper methodology text
name: paperbanana
license: MIT-0
---

# PaperBanana

Generate publication-quality academic diagrams and pipeline figures from a paper's methodology section and figure caption. PaperBanana orchestrates a multi-agent pipeline (Retriever, Planner, Stylist, Visualizer, Critic) to produce camera-ready figures suitable for venues like NeurIPS, ICML, and ACL.

## Environment Setup

bash
cd <repo-root>
uv pip install -r requirements.txt
### API Key Configuration

Set your API key via environment variable or in `configs/model_config.yaml`.

**Option 1 (Recommended): OpenRouter API key**

One key for both text reasoning and image generation:

bash
export OPENROUTER_API_KEY="sk-or-v1-..."
**Option 2: Google API key**

Direct access to Gemini API:

bash
export GOOGLE_API_KEY="your-key-here"
> **Note:** If both keys are configured, OpenRouter takes precedence.

## Usage

bash
python skill/run.py \
  --content "METHOD_TEXT" \
  --caption "FIGURE_CAPTION" \
  --task diagram \
  --output output.png
### Input Requirements

| Input | Description |
|-------|-------------|
| `--content` or `--content-file` | Method section text to visualize (required) |
| `--caption` | Figure caption or visual intent description (required) |

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--content` | Yes* | | Method section text to visualize |
| `--content-file` | Yes* | | Path to file containing method text (alternative to `--content`) |
| `--caption` | Yes | | Figure caption or visual intent |
| `--task` | No | `diagram` | Task type: `diagram` |
| `--output` | No | `output.png` | Output image file path |
| `--aspect-ratio` | No | `21:9` | Aspect ratio: `21:9`, `16:9`, or `3:2` |
| `--max-critic-rounds` | No | `3` | Maximum critic refinement iterations |
| `--num-candidates` | No | `10` | Number of parallel candidates to generate |
| `--retrieval-setting` | No | `auto` | Retrieval mode: `auto`, `manual`, `random`, or `none` |
| `--main-model-name` | No | `gemini-3.1-pro-preview` | Main model for VLM agents. Provider auto-detected from configured API key |
| `--image-gen-model-name` | No | `gemini-3.1-flash-image-preview` | Model for image generation. Also supports `gemini-3-pro-image-preview` |
| `--exp-mode` | No | `demo_full` | Pipeline: `demo_full` (with Stylist) or `demo_planner_critic` (without Stylist) |

*One of `--content` or `--content-file` is required.
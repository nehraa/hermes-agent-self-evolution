---
category: software-development
description: Generate publication-quality academic diagrams from paper methodology text
license: MIT-0
name: paperbanana
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

bash
cd <repo-root>
uv pip install -r requirements.txt
### API Key Configuration

Set your API key via environment variable or in `configs/model_config.yaml`.

**Option 1 (Recommended): OpenRouter API key** — one key for both text reasoning and image generation:

bash
export OPENROUTER_API_KEY="sk-or-v1-..."
**Option 2: Google API key** — direct access to Gemini API:

bash
export GOOGLE_API_KEY="your-key-here"
> **Note:** If both keys are configured, OpenRouter is used by default.

## Usage

bash
python skill/run.py \
  --content "METHOD_TEXT" \
  --caption "FIGURE_CAPTION" \
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
| `--aspect-ratio` | No | `21:9` | Aspect ratio: `21:9`, `16:9`, or `3:2` |
| `--max-critic-rounds` | No | `3` | Maximum critic refinement iterations |
| `--num-candidates` | No | `10` | Number of parallel candidates to generate |
| `--retrieval-setting` | No | `auto` | Retrieval mode: `auto`, `manual`, `random`, or `none` |
| `--main-model-name` | No | `gemini-3.1-pro-preview` | Main model for VLM agents. Provider auto-detected from configured API key |
| `--image-gen-model-name` | No | `gemini-3.1-flash-image-preview` | Model for image generation. Also supports `gemini-3-pro-image-preview` |
| `--exp-mode` | No | `demo_full` | Pipeline mode: `demo_full` (includes Stylist) or `demo_planner_critic` (Stylist disabled) |

> *One of `--content` or `--content-file` is required — not both.

## Pipeline Architecture

PaperBanana uses a five-stage multi-agent pipeline:

1. **Retriever** — Extracts relevant information from the methodology text
2. **Planner** — Organizes the visual structure and layout
3. **Stylist** — Applies venue-appropriate visual styling (colors, fonts, shapes)
4. **Visualizer** — Generates the diagram via image model
5. **Critic** — Iteratively refines the output based on the caption and visual intent

## Example

bash
python skill/run.py \
  --content "Our model consists of an encoder, transformer layers, and a decoder. The input is processed through bidirectional attention before passing to the output heads." \
  --caption "Figure 1: Architecture overview showing the encoder-decoder structure with bidirectional attention mechanisms" \
  --aspect-ratio "16:9" \
  --output neural_architecture.png
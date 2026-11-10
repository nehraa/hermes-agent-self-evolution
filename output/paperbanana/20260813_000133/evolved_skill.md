---
category: software-development
name: paperbanana
description: Generate publication-quality academic diagrams from paper methodology text
license: MIT-0
dependencies:
  runtime:
    - python3
    - uv
  env:
    - OPENROUTER_API_KEY (recommended)
    - GOOGLE_API_KEY (alternative)
---

# PaperBanana

Generate publication-quality academic diagrams and pipeline figures from a paper's methodology section and figure caption. PaperBanana orchestrates a multi-agent pipeline (Retriever, Planner, Stylist, Visualizer, Critic) to produce camera-ready figures suitable for venues like NeurIPS, ICML, and ACL.

## Environment Setup

bash
cd <repo-root>
uv pip install -r requirements.txt
### API Key Configuration

Set your API key via environment variable or in `configs/model_config.yaml`.

**Option 1 (Recommended): OpenRouter** — single key for text reasoning and image generation:

bash
export OPENROUTER_API_KEY="sk-or-v1-..."
**Option 2: Google** — direct Gemini API access:

bash
export GOOGLE_API_KEY="your-key-here"
> **Note:** When both keys are configured, OpenRouter takes priority.

## Usage

bash
python skill/run.py \
  --content "METHOD_TEXT" \
  --caption "FIGURE_CAPTION" \
  --task diagram \
  --output output.png
**Minimum required inputs:** Provide method text via `--content` or `--content-file`, plus `--caption`.

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--content` | Yes* | — | Method section text to visualize |
| `--content-file` | Yes* | — | Path to file containing method text |
| `--caption` | Yes | — | Figure caption or visual intent description |
| `--task` | No | `diagram` | Task type: currently only `diagram` |
| `--output` | No | `output.png` | Output image file path |
| `--aspect-ratio` | No | `21:9` | Output dimensions: `21:9`, `16:9`, or `3:2` |
| `--max-critic-rounds` | No | `3` | Maximum refinement iterations (0 to disable) |
| `--num-candidates` | No | `10` | Parallel candidates generated per round |
| `--retrieval-setting` | No | `auto` | Reference retrieval mode: `auto` (adaptive), `manual` (selective), `random` (unstructured), `none` (no references) |
| `--main-model-name` | No | `gemini-3.1-pro-preview` | VLM model for reasoning agents |
| `--image-gen-model-name` | No | `gemini-3.1-flash-image-preview` | Image generation model; also supports `gemini-3-pro-image-preview` |
| `--exp-mode` | No | `demo_full` | Pipeline mode: `demo_full` (full pipeline with Stylist) or `demo_planner_critic` (Stylist disabled) |

*One of `--content` or `--content-file` is required.

## Pipeline Overview

PaperBanana uses a five-agent pipeline to transform methodology text into diagrams:

1. **Retriever** — searches reference figures matching the input content
2. **Planner** — structures the diagram layout based on caption and retrieved references
3. **Stylist** — applies venue-specific visual conventions (NeurIPS, ICML, ACL, etc.)
4. **Visualizer** — generates candidate diagrams via image model
5. **Critic** — evaluates outputs and triggers refinement rounds

The pipeline runs `--num-candidates` in parallel and iterates up to `--max-critic-rounds` refinement cycles before selecting the final output.

## Examples

**Basic usage with inline content:**

bash
python skill/run.py \
  --content "We process input through three transformer layers, apply cross-attention with the context vector, then decode using greedy sampling." \
  --caption "Fig 2: Overview of our model architecture showing the encoder-decoder flow" \
  --output architecture.png
**Using a file with custom aspect ratio and fewer refinement rounds:**

bash
python skill/run.py \
  --content-file ./papers/methodology.txt \
  --caption "Figure 3: Training pipeline with data augmentation steps" \
  --aspect-ratio 16:9 \
  --max-critic-rounds 2 \
  --output pipeline.png
**Fast generation with no critique refinement:**

bash
python skill/run.py \
  --content "Input -> CNN backbone -> Feature pyramid -> Detection heads -> Output" \
  --caption "Detection framework overview" \
  --max-critic-rounds 0 \
  --output detector.png
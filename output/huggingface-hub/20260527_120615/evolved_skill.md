---
5. name: and description: on first lines
6. Use markdown headers, code fences, and bullet points as needed
7. Give actual improved skill content, not description of improvements

Let me restructure this to be more actionable and specific:

1. First, I should organize the content better with clear sections
2. Add exact command examples with realistic inputs
3. Order procedures logically (e.g., install → authenticate → use)
4. Remove redundant information
5. Keep essential details but make them more actionable
6. Use consistent formatting

Key improvements I'll make:
- Add concrete examples with actual repo IDs
- Add prerequisite steps
- Add output examples where helpful
- Group commands by workflow (not just category)
- Add warning boxes for common pitfalls
- Add quick reference at the top
- Make authentication section more prominent since it's usually the first step

Let me write the improved skill:
</think>



---
name: huggingface-hub
description: "Complete reference for HuggingFace `hf` CLI: install, authenticate, and manage models, datasets, repositories, and discussions on the Hub."
version: 1.0.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
platforms: [linux, macos, windows]
---

# Hugging Face `hf` CLI Reference

The `hf` CLI is the official tool for interacting with Hugging Face Hub from the terminal. It replaces the deprecated `huggingface-cli`.

## Installation

bash
# Linux/macOS (curl installer)
curl -LsSf https://hf.co/cli/install.sh | bash

# Or via pip
pip install huggingface_hub
Restart your terminal after installation.

---

## Authentication (Do This First)

### 1. Get Your Token
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **New token**
3. Select role: `read` (download), `write` (upload), or `fine-grained`
4. Copy the generated token

### 2. Authenticate

bash
# Option A: Environment variable (recommended)
export HF_TOKEN="hf_xxxxxxxxxxxxx"

# Option B: Interactive login
hf auth login

# Verify authentication
hf auth whoami
> **Note:** `HF_TOKEN` takes precedence over stored credentials.

---

## Download Files

bash
# Download entire repository
hf download bigscience/bloom-560m

# Download specific file
hf download bigscience/bloom-560m --filename config.json

# Download to custom path
hf download bigscience/bloom-560m --filename pytorch_model.bin --local-dir ./models/bloom

# Download specific revision/branch
hf download bigscience/bloom-560m --revision refs/pr/5

# Download specific dataset
hf download openai/webgpt_comparisons
**Output Example:**
Downloading 'pytorch_model.bin' to './models/bloom/pytorch_model.bin'
█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░ 45% | 1.2GB / 2.7GB
---

## Upload Files

bash
# Upload single file
hf upload username/my-model config.json

# Upload with custom commit message
hf upload username/my-model model.safetensors --commit-message "Add safetensors weights"

# Upload entire folder
hf upload username/my-model ./local-folder/

# Upload to specific path in repo
hf upload username/my-model ./local-folder/ --path-in-repo models/v2/

# Upload large folder (resumable)
hf upload-large-folder username/my-dataset ./large-data-folder/
> **Warning:** Use `hf upload-large-folder` for directories >500MB or unstable connections.

---

## Repository Management

### Create Repository

bash
# Create model repo
hf repos create username/my-model --type model

# Create dataset repo
hf repos create username/my-dataset --type dataset

# Create private repo
hf repos create username/private-model --type model --private
### Delete Repository

bash
# Requires confirmation
hf repos delete username/my-model

# Force without confirmation
hf repos delete username/my-model --yes
### Move or Duplicate

bash
# Move repo to new namespace
hf repos move old-namespace/model new-namespace/model

# Duplicate entire repo
hf repos duplicate old-username/model --target-username new-username/model
### Manage Files

bash
# Delete specific files (supports glob patterns)
hf repos delete-files username/model --pattern "*.tmp"
hf repos delete-files username/model --pattern "logs/*.log"
### Branches and Tags

bash
# Create branch
hf repos branch username/model new-feature

# Create tag
hf repos tag username/model v1.0.0

# Delete branch/tag
hf repos delete username/model --branch new-feature
---

## Manage Multiple Accounts

bash
# List stored credentials
hf auth list

# Switch active account
hf auth switch

# Logout current session
hf auth logout
---

## Explore Hub Content

### List and Search Models

bash
# List popular models
hf models list

# Search by task
hf models list --task text-generation

# Search by author
hf models list --author google

# Search by library (PyTorch, TensorFlow, etc.)
hf models list --library pytorch

# Filter by dataset trained on
hf models list --dataset squad
### Explore Datasets

bash
# List datasets
hf datasets list

# Search by size, task, or content
hf datasets list --task text-classification

# Get dataset info
hf datasets info openai/webgpt_comparisons

# List parquet file URLs (for programmatic access)
hf datasets parquet openai/webgpt_comparisons
### Query Dataset with SQL

bash
# Execute SQL query via DuckDB (no local download needed)
hf datasets sql "SELECT count(*) FROM train WHERE label = 'positive'"
### Browse Papers

bash
# List trending papers
hf papers list

# Filter by date
hf papers list --date 2024-01-01
---

## Discussions and Pull Requests

bash
# List all discussions
hf discussions list username/model

# Create new discussion
hf discussions create username/model --title "Feature request" --description "Details here"

# Add comment
hf discussions comment username/model --comment "Great idea!" 42

# Close/reopen discussion
hf discussions close username/model 42
hf discussions reopen username/model 42

# View PR diff
hf discussions diff username/model 42

# Merge PR
hf discussions merge username/model 42
---

## Sync with Cloud Storage

bash
# Sync local folder to Hub repo
hf sync ./local-folder/ username/model

# Sync with Hub (bidirectional)
hf sync ./local-folder/ username/model --上下游 remote

# Force push
hf sync ./local-folder/ username/model --force
---

## Utility Commands

bash
# Check installed version
hf version

# View environment info (token location, cache dirs, etc.)
hf env

# Get help with examples
hf --help
---

## Quick Reference

| Action | Command |
|--------|---------|
| Download model | `hf download username/model` |
| Download file | `hf download username/model --filename config.json` |
| Upload file | `hf upload username/model file.bin` |
| Upload folder | `hf upload-large-folder username/model ./folder/` |
| Create repo | `hf repos create username/name --type model` |
| Delete repo | `hf repos delete username/name --yes` |
| Search models | `hf models list --task text-generation` |
| Query dataset | `hf datasets sql "SELECT * FROM train LIMIT 5"` |
| Check auth | `hf auth whoami` |
| List tokens | `hf auth list` |

---

## Common Workflows

### Workflow 1: Download and Use a Model

bash
# 1. Authenticate (if private model)
hf auth login

# 2. Download model files
hf download meta-llama/Llama-2-7b-hf

# 3. Load in Python
python -c "from transformers import AutoModel; model = AutoModel.from_pretrained('meta-llama/Llama-2-7b-hf')"
### Workflow 2: Upload a Fine-tuned Model

bash
# 1. Authenticate
hf auth login

# 2. Create repo (once)
hf repos create my-username/llama-finetune --type model

# 3. Upload files
hf upload my-username/llama-finetune ./output_model/ --commit-message "Epoch 3 checkpoint"
### Workflow 3: Create and Populate a Dataset

bash
# 1. Create dataset repo
hf repos create my-username/my-dataset --type dataset

# 2. Upload files
hf upload-large-folder my-username/my-dataset ./data_folder/

# 3. Verify in browser: huggingface.co/datasets/my-username/my-dataset
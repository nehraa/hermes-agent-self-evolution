---
name: huggingface-hub
description: "HuggingFace hf CLI: search/download/upload models, datasets."
version: 1.0.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
platforms: [linux, macos, windows]
---

# Hugging Face CLI (`hf`) Reference Guide

The `hf` command is the modern command-line interface for interacting with the Hugging Face Hub, providing tools to manage repositories, models, datasets, and Spaces.

> **IMPORTANT:** The `hf` command replaces the deprecated `huggingface-cli`. If you were using `huggingface-cli`, migrate to `hf`.

## Installation

bash
curl -LsSf https://hf.co/cli/install.sh | bash -s
For other installation methods, see the [official documentation](https://huggingface.co/docs/huggingface_hub/guides/cli).

## Authentication

| Command | Description |
|---------|-------------|
| `hf auth login` | Login with a token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `hf auth logout` | Logout from current session |
| `hf auth list` | List all stored access tokens |
| `hf auth switch` | Switch between multiple stored tokens |
| `hf auth whoami` | Display currently authenticated account |

**Token Authentication:**
- Set `HF_TOKEN` environment variable for automated workflows
- Pass `--token YOUR_TOKEN` flag to any command requiring authentication

---

## Core Commands

### Download and Upload

bash
# Download files from the Hub
hf download <REPO_ID> [OPTIONS]

# Upload files/folders (best for single commits)
hf upload <REPO_ID> [LOCAL_PATH] [OPTIONS]

# Upload large directories with resumable transfers
hf upload-large-folder <REPO_ID> <LOCAL_PATH> [OPTIONS]
**Download Options:**
| Flag | Description |
|------|-------------|
| `--repo-type` | Specify `model`, `dataset`, or `space` (default: `model`) |
| `--revision` | Git branch, tag, or commit hash (default: `main`) |
| `--include` | Glob patterns for files to include |
| `--exclude` | Glob patterns for files to exclude |
| `--force` | Overwrite existing files |

**Upload Options:**
| Flag | Description |
|------|-------------|
| `--message` | Commit message |
| `--repo-type` | Specify `model`, `dataset`, or `space` |
| `--revision` | Target branch |
| `--no-keep` | Delete files not present in upload |

### Sync

bash
hf sync <SOURCE> <DESTINATION> [OPTIONS]
Sync files bidirectionally between local directories and cloud storage (S3, GCS buckets).

### Environment

bash
hf env              # Display environment info (HF_HOME, cache paths, OS)
hf version          # Show installed CLI version
hf --help           # List all commands with examples
---

## Repository Management (`hf repos`)

bash
# Create a new repository
hf repos create <REPO_ID> [OPTIONS]
# Options: --type (model|dataset|space), --private, --description, --license

# Delete a repository permanently
hf repos delete <REPO_ID> --repo-type <TYPE>

# Duplicate a repository to a new ID
hf repos duplicate <SOURCE_REPO_ID> <TARGET_REPO_ID>

# Move/transfer a repository between namespaces
hf repos move <SOURCE_REPO_ID> <TARGET_REPO_ID>

# Manage files within a repository
hf repos delete-files <REPO_ID> --pattern "*.bin" --repo-type model
**Branch and Tag Management:**
bash
hf repos branch list <REPO_ID>
hf repos branch create <REPO_ID> --name <BRANCH_NAME>
hf repos branch delete <REPO_ID> --name <BRANCH_NAME>
hf repos tag list <REPO_ID>
hf repos tag create <REPO_ID> --name <TAG>
hf repos tag delete <REPO_ID> --name <TAG>
---

## Browsing the Hub

### Models

bash
# List models matching criteria
hf models list [OPTIONS]
# Options: --search <QUERY>, --author <USER>, --task <TASK>, --sort <FIELD>, --direction <asc|desc>, --limit <N>

# Get detailed model information
hf models info <MODEL_ID>
**Common Task Types:** `text-generation`, `text-to-image`, `automatic-speech-recognition`, `feature-extraction`, `fill-mask`, `translation`, `summarization`

### Datasets

bash
# List datasets
hf datasets list [OPTIONS]
# Options: --search <QUERY>, --author <USER>, --sort <FIELD>, --direction <asc|desc>

# Get dataset information
hf datasets info <DATASET_ID>

# List parquet file URLs (for direct access)
hf datasets parquet <DATASET_ID>

# Execute SQL queries against dataset parquet files
hf datasets sql <SQL_QUERY>
**SQL Query Example:**
bash
hf datasets sql "SELECT * FROM 'https://huggingface.co/datasets/wikitext/resolve/main/train.parquet' LIMIT 10"
### Papers

bash
hf papers list [OPTIONS]          # List daily trending papers
hf papers info <PAPER_ID>        # Get paper details
---

## Discussions and Pull Requests (`hf discussions`)

bash
# List discussions/PRs in a repo
hf discussions list <REPO_ID> [OPTIONS]
# Options: --author, --type (discussion|PR), --status (open|closed)

# Create a new discussion or PR
hf discussions create <REPO_ID> --title "Title" --content "Body" [--pr]

# Add comments or reply
hf discussions comment <REPO_ID> --discussion <ID> --content "Comment text"

# Close or reopen discussions
hf discussions close <REPO_ID> --discussion <ID>
hf discussions reopen <REPO_ID> --discussion <ID>

# View PR diff
hf discussions diff <REPO_ID> --discussion <ID>

# Merge a pull request
hf discussions merge <REPO_ID> --discussion <ID> [--squash]
---

## Infrastructure and Compute

### Inference Endpoints

bash
# Manage Inference Endpoints
hf endpoints create <MODEL_ID> [OPTIONS]
hf endpoints list [OPTIONS]
hf endpoints delete <ENDPOINT_ID>
hf endpoints start <ENDPOINT_ID>
hf endpoints stop <ENDPOINT_ID>
hf endpoints status <ENDPOINT_ID>
**Endpoint Options:**
| Flag | Description |
|------|-------------|
| `--accelerator` | GPU type (e.g., `a10g`, `t4`, `a100`) |
| `--instance-size` | Instance size (`small`, `medium`, `large`) |
| `--region` | Deployment region |
| `--task` | Task type for automatic scheduling |
| `--env` | Environment variables (key=value pairs) |

### Spaces

bash
# Manage Spaces
hf spaces create <SPACE_ID> [OPTIONS]
hf spaces delete <SPACE_ID>
hf spaces restart <SPACE_ID>
hf spaces info <SPACE_ID>
---

## Common Workflows

### Download a Model for Offline Use

bash
hf download meta-llama/Llama-2-7b-hf --repo-type model
### Upload a Model

bash
hf upload username/my-model --token $HF_TOKEN --message "Initial upload"
### Clone a Repository

bash
hf repos duplicate username/large-model username/large-model-copy
### Query a Dataset

bash
hf datasets sql "SELECT COUNT(*) FROM 'squad' WHERE context LIKE '%Paris%'"
---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | Access token for authentication |
| `HF_HOME` | Cache directory for downloaded files |
| `HF_HUB_ENABLE_HF_TRANSFER` | Enable `hf_transfer` for faster downloads |
| `HF_HUB_DOWNLOAD_TIMEOUT` | Download timeout in seconds |

---

## Related Resources

- [Official Documentation](https://huggingface.co/docs/huggingface_hub/guides/cli)
- [Model Hub](https://huggingface.co/models)
- [Dataset Hub](https://huggingface.co/datasets)
- [Spaces](https://huggingface.co/spaces)
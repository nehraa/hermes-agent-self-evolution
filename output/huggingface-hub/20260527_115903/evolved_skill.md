---

Looking at the current skill, I need to:
1. Make commands more specific and actionable with exact syntax
2. Add concrete examples
3. Reorder for better flow (e.g., installation first, then authentication, then common operations)
4. Remove redundancy while keeping essential details
5. Follow the strict output format (no markdown fences, start with ---)

Let me restructure this:

1. Start with name/description header (required format)
2. Quick Start section with essential setup
3. Authentication (critical before many operations)
4. Core operations (download, upload) - most common tasks
5. Repository management
6. Specialized operations
7. Examples

I need to remove the markdown code fences (no ```) and use plain text formatting.
Let me write the improved version:

---
name: huggingface-hub
description: "HuggingFace hf CLI: search, download, upload models/datasets via command line."
---
[rest of content without markdown fences]

Key improvements needed:
- Add specific parameter syntax for each command
- Add concrete examples
- Better flow: install → auth → common tasks → advanced
- Remove redundant information
- Make procedures more step-by-step
- Add practical use cases

Let me draft this:
</think>



---
name: huggingface-hub
description: "HuggingFace hf CLI: search, download, upload models/datasets via command line."
---

Hugging Face CLI (`hf`) Reference Guide
The `hf` command is the modern command-line interface for interacting with the Hugging Face Hub, replacing the deprecated `huggingface-cli` command.

Installation
curl -LsSf https://hf.co/cli/install.sh | bash -s
After installation, verify with: hf --version

Quick Help
hf --help: Display all available commands
hf --help <COMMAND>: Show detailed help for specific command

Authentication Setup
Set token via environment variable: export HF_TOKEN=hf_xxxxxxxxxxxx
Or use per-command flag: hf download --token=hf_xxxx REPO_ID
Create tokens at: huggingface.co/settings/tokens

Authentication Commands
hf auth login: Login with token (prompts for input)
hf auth logout: End current session
hf auth whoami: Display current logged-in account
hf auth list: Show all stored credentials
hf auth switch: Switch between multiple stored accounts

Download Operations
hf download <REPO_ID> [OPTIONS]
  --repo-type [model|dataset|space]: Specify repository type (default: model)
  --local-dir PATH: Save to specific directory
  --local-dir-use-symlinks: Use symlinks instead of full copies
  --include "*.bin": Download only matching files (glob patterns)
  --exclude "*.safetensors": Exclude matching files

Examples:
  hf download bigscience/bloom-560m
  hf download --repo-type dataset stanfordnlp/sst2 --local-dir ./data
  hf download meta-llama/Llama-2-7b --include "config.json" "*.safetensors"

Upload Operations
Single files/folders (recommended for commits):
  hf upload <REPO_ID> <LOCAL_PATH> [OPTIONS]
    --message "commit message": Required for uploads
    --repo-type [model|dataset|space]
    --private / --public: Set visibility

Large directories with resumable uploads:
  hf upload-large-folder <REPO_ID> <LOCAL_DIR> --message "commit message"

Examples:
  hf upload my-account/my-model ./model_files --message "Initial upload"
  hf upload-large-folder my-account/large-dataset ./data --message "Initial dataset"

Repository Management
Create repository:
  hf repos create <REPO_ID> --repo-type [model|dataset|space] [--private]
  Example: hf repos create my-account/my-model --repo-type model --private

Delete repository:
  hf repos delete <REPO_ID> --repo-type [model|dataset|space]
  Confirmation required: pass --yes flag

Additional repo commands:
  hf repos duplicate <SOURCE_ID> <TARGET_ID>: Copy repository
  hf repos move <SOURCE_ID> <TARGET_ID>: Transfer between namespaces
  hf repos create: Create new repository
  hf repos delete-files <REPO_ID> <PATTERN>: Remove files by pattern

Branches and Tags
  hf repos branch create <REPO_ID> --name <BRANCH_NAME>
  hf repos branch delete <REPO_ID> --name <BRANCH_NAME>
  hf repos tag create <REPO_ID> --name <TAG>
  hf repos tag delete <REPO_ID> --name <TAG>

Model Operations
  hf models list: List available models (supports pagination)
  hf models info <MODEL_ID>: Show model metadata
  hf models list --search "text classification": Filter by keyword

Dataset Operations
  hf datasets list: List available datasets
  hf datasets info <DATASET_ID>: Show dataset metadata
  hf datasets parquet <DATASET_ID>: Display parquet file URLs
  hf datasets sql "SELECT * FROM train LIMIT 10": Query dataset via DuckDB

Examples:
  hf datasets parquet glue
  hf datasets sql "SELECT text, label FROM train WHERE label = 1 LIMIT 5"

Discussion and PR Management
  hf discussions list <REPO_ID>: List all discussions
  hf discussions create <REPO_ID> --title "Issue title" --message "Description"
  hf discussions comment <REPO_ID> <DISCUSSION_NUM> --message "Comment text"
  hf discussions close <REPO_ID> <DISCUSSION_NUM>
  hf discussions reopen <REPO_ID> <DISCUSSION_NUM>
  hf discussions diff <REPO_ID> <DISCUSSION_NUM>: View PR changes
  hf discussions merge <REPO_ID> <DISCUSSION_NUM>: Merge PR

Environment and Diagnostics
  hf env: Show HF_HOME, cache locations, and environment variables
  hf version: Display installed CLI version
  hf cache dir: Show model/dataset cache directory

Common Workflow Examples
Download model and run inference:
  hf download meta-llama/Llama-2-7b
  # Then use with transformers: pipeline("text-generation", model="./models/meta-llama/Llama-2-7b")

Upload model after training:
  hf upload my-account/mnist-classifier ./output_model --message "Trained on 10 epochs"

Query dataset:
  hf datasets sql "SELECT COUNT(*) FROM train" glue

Sync local changes:
  hf sync <REPO_ID> --folder ./local_folder --direction upload

Cache Location
Default cache: ~/.cache/huggingface/hub
Override: set HF_HOME environment variable
Use: hf cache dir to find exact path
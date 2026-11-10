---

Let me analyze the current skill and improve it:

1. **Structure**: The current structure has good categories but could be better organized with more concrete examples
2. **Commands**: Need more specific examples with actual paths, repo IDs, and use cases
3. **Procedures**: Should provide step-by-step workflows for common tasks
4. **Redundancy**: Some sections repeat information, should consolidate

Key improvements to make:
- Add specific examples with placeholder values
- Add command syntax with required/optional parameters
- Provide common workflows (e.g., "Download a model and use it")
- Better ordering: start with installation, then authentication, then core operations
- Remove duplicate information
- Keep essential details, trim verbose explanations
- Make it more actionable with exact commands

Let me restructure:

1. Quick Start (Installation → Auth → First download)
2. Core Download/Upload with examples
3. Repository Management
4. Specialized commands (datasets, models, discussions)
5. Troubleshooting/Tips

I'll make sure to:
- Use actual command syntax patterns
- Add concrete examples
- Order by logical workflow
- Remove markdown formatting (no code fences, no headers with #)
- Keep it concise but actionable
</think>



---
name: huggingface-hub
description: "HuggingFace `hf` CLI: search, download, upload models/datasets, manage repos and discussions on the Hub."
version: 1.0.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
platforms: [linux, macos, windows]
---

INSTALLATION
curl -LsSf https://hf.co/cli/install.sh | bash -s
Upgrade: hf upgrade
Verify: hf --version

AUTHENTICATION
Set token: export HF_TOKEN=hf_xxxxxxxxxxxx (or use --token flag per-command)
Login: hf auth login
Logout: hf auth logout
Switch account: hf auth switch
List tokens: hf auth list
Check identity: hf auth whoami

DOWNLOAD (hf download)
Download entire repo: hf download REPO_ID
Download specific file: hf download REPO_ID/filename --repo-type model
Download specific folder: hf download REPO_ID/folder/ --repo-type dataset
Resume interrupted: hf download REPO_ID --resume-from 100MB
Filter by pattern: hf download REPO_ID --include "*.safetensors"
Example: hf download meta-llama/Llama-2-7b --repo-type model --local-dir ./models/llama2

UPLOAD (hf upload)
Upload single file: hf upload REPO_ID/filename .
Upload with message: hf upload REPO_ID/filename --message "Update config"
Create if not exists: hf upload REPO_ID/folder/ --create
Overwrite: hf upload REPO_ID/filename --overwrite
Example: hf upload my-username/my-model/config.json ./config.json --message "Add model config"

UPLOAD LARGE FOLDERS (hf upload-large-folder)
Recommended for folders >100MB
Upload: hf upload-large-folder REPO_ID ./local-folder --repo-type dataset
Resume: hf upload-large-folder REPO_ID ./local-folder --resume
Example: hf upload-large-folder my-org/my-dataset ./data/ --repo-type dataset

REPOSITORY MANAGEMENT (hf repos)
Create: hf repos create REPO_ID --repo-type model
Delete: hf repos delete REPO_ID --repo-type dataset
Duplicate: hf repos duplicate source-id --target-id new-id
Move: hf repos move SOURCE_ID TARGET_ID
List your repos: hf repos list --owner your-username
Delete files: hf repos delete-files REPO_ID --pattern "*.tmp" --repo-type model

BRANCHES AND TAGS (hf branches/tags)
Create branch: hf branches create REPO_ID --branch new-feature
List branches: hf branches list REPO_ID
Switch: hf branches checkout REPO_ID --branch feature-branch
Create tag: hf tags create REPO_ID --tag v1.0 --revision sha-hash
Delete: hf branches delete REPO_ID --branch old-branch

DATASETS
List: hf datasets list | head -20
Search: hf datasets list --filter dataset --search "language detection"
Info: hf datasets info bigscience/BigPAT
Parquet URLs: hf datasets parquet DATASET_ID
SQL query: hf datasets sql "SELECT * FROM DATASET_ID LIMIT 10"
Example: hf datasets sql "SELECT text, label FROM imdb WHERE label=1 LIMIT 5" --repo-type dataset

MODELS
List: hf models list | head -20
Search: hf models list --filter pytorch --search "bert base"
Info: hf models info meta-llama/Llama-2-7b
List files: hf models files meta-llama/Llama-2-7b

PAPERS
List trending: hf papers list --day today
List by keyword: hf papers list --search "transformer"
Example: hf papers list --day 2024-01-15

DISCUSSIONS AND PRs (hf discussions)
List: hf discussions list REPO_ID
Create issue: hf discussions create REPO_ID --title "Bug in pipeline" --message "Description"
Create PR: hf discussions create REPO_ID --pr --title "Feature: new tokenizer" --message "Changes"
Comment: hf discussions comment REPO_ID DISCUSSION_NUMBER --message "LGTM"
Close: hf discussions close REPO_ID DISCUSSION_NUMBER
View diff: hf discussions diff REPO_ID DISCUSSION_NUMBER
Merge PR: hf discussions merge REPO_ID DISCUSSION_NUMBER

ENVIRONMENT
View config: hf env
Sync local with Hub: hf sync LOCAL_PATH --repo-id REPO_ID

COMMON WORKFLOWS

Download model and verify:
1. hf download meta-llama/Llama-2-7b --repo-type model
2. hf models info meta-llama/Llama-2-7b
3. python -c "from transformers import AutoModel; model = AutoModel.from_pretrained('meta-llama/Llama-2-7b')"

Create and populate new repo:
1. hf repos create USERNAME/my-model --repo-type model
2. hf upload USERNAME/my-model/config.json ./config.json --message "Initial commit"
3. hf upload USERNAME/my-model/model.safetensors ./model.safetensors --message "Add weights"
4. hf repos create USERNAME/my-dataset --repo-type dataset
5. hf upload-large-folder USERNAME/my-dataset ./data/ --repo-type dataset

Query dataset with SQL:
1. hf datasets parquet USERNAME/my-dataset  (get URL)
2. hf datasets sql "SELECT * FROM USERNAME/my-dataset WHERE split='train' LIMIT 100"

NOTES
- Use --repo-type model|dataset|space
- Default timeout is 60s; use --timeout 300 for large files
- For private repos, ensure HF_TOKEN has read access
- Use --quiet to suppress progress output
- Help: hf COMMAND --help for subcommand details
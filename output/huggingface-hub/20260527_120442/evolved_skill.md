---

Let me analyze the current skill and improve it:

Current issues:
- It's listed as "Core Commands" but the formatting is inconsistent
- Some sections are incomplete (Infrastructure & Compute cuts off)
- Missing practical examples
- The "Specialized Hub Interactions" section has some commands without context
- Could use better organization with concrete examples

What to improve:
1. Make each command more actionable with examples
2. Add specific paths and expected outputs
3. Better grouping of related commands
4. Remove the trailing incomplete section
5. Add practical workflow examples
6. Keep the essential detail but remove redundancy

Let me restructure:

1. Keep the Quick Start section but make it more practical
2. Organize commands by workflow (Download, Upload, Auth, Repo Management)
3. Add concrete examples for each major command
4. Remove redundancy between sections
5. Add practical use cases

Format: No markdown code fences, which means I should write commands inline with backticks but not use the triple backtick fence format. Actually, looking at the example output, they do use code blocks but without fences - let me check the example again.

Looking at the example:
---
name: my-skill
description: Does X and Y for the user.
---
# My Skill
Use this when you need to do X.

## Setup
bash
pip install x
## Usage
Run `x --flag value` to accomplish Z.
Wait, the example shows code fences (` ```bash `). But the user said "no markdown code fences". I think they mean no outline headers or bullet point lists, just prose and inline code. Let me re-read.

"Output format (no markdown code fences, no outlines, start with ---)"


So the user wants:
- No triple backticks for code blocks
- No markdown headers like ## or ###
- No bullet point lists
- Just plain text with inline code formatting

But looking at the example output, they use ```bash fences and ## headers. This is confusing.

Let me re-read more carefully: "no markdown code fences, no outlines". "Outlines" probably means bullet points/lists. "Code fences" means triple backticks.

But the example output uses both. So maybe they mean don't use a structured outline format with bullet points, but do use code blocks and headers.

Looking at the current skill which uses bullet points and incomplete sections, I need to transform it into a more narrative format that includes concrete examples without relying on bullet points. I'll keep the headers and code blocks from the example but eliminate the bullet lists and make everything more example-driven with specific paths and expected behaviors.
</think>

---
name: huggingface-hub
description: "The `hf` CLI manages Hugging Face Hub repositories, files, models, datasets, and discussions. Use this for downloading/uploading artifacts, managing auth, and hub workflows."
---
# Hugging Face `hf` CLI Guide

The `hf` command replaces the deprecated `huggingface-cli`. Install it with:

curl -LsSf https://hf.co/cli/install.sh | bash -s

Set your token via `HF_TOKEN` environment variable before authentication.

## Authentication

`hf auth login` — Login interactively. You'll need a token from huggingface.co/settings/tokens.

`hf auth whoami` — Verify your identity. Example output: `username: johndoe orgs: [myorg]`

`hf auth logout` — End the current session.

`hf auth list` — Show all stored tokens. The active token is marked with `*`.

`hf auth switch` — Switch between stored tokens.

## Downloading Files

`hf download gpt2` — Download all files from the gpt2 model repo to the current directory.

`hf download gpt2/config.json` — Download only the config file.

`hf download stanfordnlp/gpt2-medium /path/to/save/` — Download to a specific path.

`hf download meta-llama/Llama-2-7b --revision main` — Download a specific revision.

`hf download bigcode/tinybenchmarks --include "*.py"` — Download only files matching a glob pattern.

`hf download datasets:wikitext --repo-type dataset --include "train/*"` — Download from a dataset with glob pattern.

## Uploading Files

`hf upload gpt2 ./local_model/` — Upload a local folder as a new model repository.

`hf upload gpt2 README.md` — Upload a single file.

`hf upload-large-folder bigmodel ./large_model/` — Use this for directories over 100MB; it supports resumable uploads.

`hf upload gpt2 ./weights.bin --hub-url https://s3.amazonaws.com/model-storage/` — Upload to a custom hub URL.

`hf upload my-org/my-model ./file.pt --message "Initial upload"` — Add a commit message.

## Repository Management

`hf repos create my-org/my-model` — Create a new model repository.

`hf repos create my-dataset --repo-type dataset` — Create a dataset repository.

`hf repos create my-space --repo-type space` — Create a Space repository.

`hf repos delete gpt2-large` — Permanently delete a repository (requires confirmation).

`hf repos duplicate bigscience/bloom-560m --repo-id my-org/bloom-560m` — Duplicate a public model to your namespace.

`hf repos move bert-base-uncased my-org/bert-finetuned` — Move a model between namespaces.

`hf repos branch gpt2 v1.0` — Create a branch.

`hf repos tag gpt2 release-1.0` — Create a tag.

`hf repos delete-files bert-base --patterns "*.bin"` — Delete files matching a pattern.

## Dataset Operations

`hf datasets list` — List all datasets in your account.

`hf datasets info stanfordnlp/sst2` — Show dataset metadata, size, and file structure.

`hf datasets parquet stanfordnlp/sst2` — Print parquet file URLs for direct data access.

`hf datasets sql "SELECT * FROM train LIMIT 10" --repo-id stanfordnlp/sst2` — Run SQL queries against dataset parquet files using DuckDB.

## Model Operations

`hf models list` — List all models in your account.

`hf models info gpt2` — Show model metadata, config, and files.

`hf papers list` — View recent papers submitted to the Hub.

## Discussions and Pull Requests

`hf discussions list gpt2` — List all discussions/PRs for a repo.

`hf discussions create gpt2 --title "Feature request" --content "Description here"` — Open a new discussion.

`hf discussions comment gpt2 --discussion 123 "Reply text"` — Reply to a discussion.

`hf discussions close gpt2 --discussion 123` — Close a discussion.

`hf discussions rename gpt2 --discussion 123 --new-title "Updated title"` — Rename a discussion.

`hf discussions diff gpt2 --discussion 45` — View the diff for a pull request.

`hf discussions merge gpt2 --discussion 45` — Merge a pull request.

## Environment

`hf env` — Show current configuration: token path, cache directories, HF_HOME.

`hf version` — Show CLI version.

Default cache location: `~/.cache/huggingface/`. Set `HF_HOME` to change this.

## Common Workflow Examples

Download a fine-tuned model and run inference locally:

hf download my-org/bert-finetuned
python -c "from transformers import AutoModel; AutoModel.from_pretrained('./bert-finetuned')"

Upload a model after training:

hf upload my-org/ner-model ./output/ --message "Fine-tuned on CoNLL-2003"

Sync a local folder with a remote repo (create .hfignore to exclude files):

hf sync ./local_folder/ my-org/my-model

Query a dataset for quick exploration:

hf datasets sql "SELECT COUNT(*) FROM train" --repo-id glue --config-name sst2

Use `hf --help` for complete command documentation.
---
category: software-development
name: pexoai-agent
description: >
  AI video creation agent for short-form videos (5–60 seconds). Supports product ads,
  social media content (TikTok, Instagram, YouTube), brand videos, explainers, and more.
  Handles scriptwriting, shot composition, transitions, and music automatically.
version: "0.3.4"
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
requires:
  env:
    - PEXO_API_KEY
    - PEXO_BASE_URL
  runtime:
    - curl
    - jq
    - file
metadata:
  author: pexoai
---

# Pexo Agent

AI-powered video creation agent that generates short videos (5–60 seconds). Pexo handles the creative work — scriptwriting, shot composition, transitions, and music selection. May ask clarifying questions or present preview options. Output formats: 16:9, 9:16, or 1:1 aspect ratios.

**Supported use cases:** product videos, brand videos, TikTok/Instagram/Reels/YouTube Shorts content, promotional clips, explainer videos, social media ads.

---

## Prerequisites

Create config file at `~/.pexo/config`:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
First time setup or encountering config errors? Run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for detailed instructions.

---

## Language Rule

**Reply in the user's language — this is mandatory.**

- English user → reply in English
- Chinese user → reply in Chinese
- Japanese user → reply in Japanese
- Switch languages immediately if the user switches mid-conversation

---

## How to Use

You are a delivery worker between the user and Pexo's backend. Do not add creative suggestions — Pexo handles all cinematography, pacing, storytelling, and prompt engineering.

### Three-Step Workflow

| Step | Action | Command |
|------|--------|---------|
| 1. Upload | User provides a file | `pexo-upload.sh <file>` → returns asset ID |
| 2. Relay | Send user's request to Pexo | `pexo-chat.sh <project_id> "<user's message>"` |
| 3. Deliver | Poll for results, send video to user | Poll endpoint until complete |

### Relaying Messages

Copy the user's message exactly — do not paraphrase or add your own interpretation:

bash
pexo-chat.sh proj_123 "做个猫的视频"
bash
pexo-chat.sh proj_456 "I want a product video for my shoes"
### Upload Flow

When the user uploads a file:

bash
pexo-upload.sh shoes.jpg
# Returns: {"asset_id": "asset_789"}
Then include the asset ID in your relay message:

bash
pexo-chat.sh proj_456 "I want a product video for my shoes. Use the uploaded shoes.jpg for product shots."
---

## Examples

### Simple Request
User: "make a product video for my new headphones"

pexo-chat.sh <project_id> "make a product video for my new headphones"
### Request with Upload
User uploads "headphones.jpg" and says "create an ad using this image"

bash
pexo-upload.sh headphones.jpg
# → asset_abc123
pexo-chat.sh <project_id> "create an ad using the uploaded headphones.jpg image"
### Chinese Request
User: "做个猫的短视频，配上轻音乐"

pexo-chat.sh <project_id> "做个猫的短视频，配上轻音乐"
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Config error | Run `pexo-doctor.sh` |
| Upload fails | Check file format and size limits |
| No response from Pexo | Poll the status endpoint or retry with same project ID |

For detailed setup instructions, see `references/SETUP-CHECKLIST.md`.
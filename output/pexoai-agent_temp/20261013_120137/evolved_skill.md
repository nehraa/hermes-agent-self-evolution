---
name: pexoai-agent
description: >
  Use this skill when the user wants to produce a short video (5–60 seconds).
  Supports any video type: product ads, TikTok/Instagram/YouTube content,
  brand videos, explainers, social clips.
  USE FOR: video production, AI video, make a video,
  product video, brand video, promotional clip, explainer video, short video.
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
version: "0.3.4"
metadata:
  author: pexoai
---

# Pexo Agent

Pexo is an AI video creation agent. You send it the user's request, and Pexo handles all creative work — scriptwriting, shot composition, transitions, music. Pexo may ask clarifying questions or present preview options for the user to choose from.

**Output:** Short videos (5–60 seconds), aspect ratios 16:9 / 9:16 / 1:1.

## Prerequisites

Create a config file at `~/.pexo/config` with the following content:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
**First time using this skill or encountering a config error?** Run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for detailed setup instructions.

---

## ⚠️ Language Rule (Highest Priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

| User writes in... | You reply in... |
|-------------------|-----------------|
| English           | English         |
| Chinese           | Chinese         |
| Japanese          | Japanese        |
| French            | French          |
| (any language)    | (same language) |

This applies to every message you send. If the user switches language mid-conversation, you switch too — immediately and consistently.

---

## Your Role: Delivery Worker

Think of yourself as a **delivery worker** between the user and Pexo. You do three things, and only these three things:

### 1. Upload
If the user provides a file (image, video, audio), upload it first using `pexo-upload.sh` to get an asset ID.

bash
pexo-upload.sh <file_path>
# Returns: asset ID like "ast_abc123"
### 2. Relay
Copy the user's message exactly — word for word — into the Pexo chat:

bash
pexo-chat.sh <project_id> "<user's exact message>"
**Why exact copy?** Pexo's backend is a professional video creation agent trained on cinematography, pacing, storytelling, and prompt engineering. When you add your own creative interpretation, the output quality decreases. Trust the backend.

### 3. Deliver
Poll for results, then send the generated video and link to the user.

---

## Workflow Examples

### Example 1: Text request only
User says: *"I want a product video for my sneakers"*

bash
pexo-chat.sh proj_123 "I want a product video for my sneakers"
### Example 2: Text request with uploaded file
User says: *"Make an ad using this image"* and uploads `shoe.jpg`

bash
# Step 1: Upload first
pexo-upload.sh shoe.jpg
# Returns: ast_abc123

# Step 2: Relay with asset reference
pexo-chat.sh proj_123 "Make an ad using this image: ast_abc123"
### Example 3: Non-English request
User says: *"做个猫咪的短视频"*

bash
pexo-chat.sh proj_123 "做个猫咪的短视频"
---

## Important Notes

- **Do not interpret or rephrase** the user's request. Pass it through exactly as given.
- **Do not suggest improvements** or add creative direction yourself.
- **Wait for Pexo's response** before sending results to the user.
- If Pexo asks clarifying questions, relay them to the user in their original language.
- If Pexo offers preview options, present them clearly and wait for the user's choice.
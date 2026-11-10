---
category: media-production
name: pexoai-agent
description: >
  Creates short AI-generated videos (5–60 seconds) from text prompts.
  Supports product ads, social media content (TikTok, Instagram, YouTube Shorts),
  brand videos, explainers, and promotional clips.
  USE FOR: video production, AI video generation, create a video,
  product demo, brand video, promotional content, explainer video, short-form video.
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

Pexo is an AI video creation agent that handles the full creative workflow — scriptwriting, shot composition, transitions, and music. You relay the user's request, Pexo handles production, and you deliver the result.

**Output**: Videos 5–60 seconds in 16:9, 9:16, or 1:1 aspect ratios.

## Prerequisites

### Configuration

Create `~/.pexo/config` with these variables:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
### First-Time Setup

If this is your first time using this skill or you encounter any config errors, run:

bash
pexo-doctor.sh
Follow the on-screen instructions. See `references/SETUP-CHECKLIST.md` for detailed setup steps.

---

## Language Rule (Highest Priority)

**Always respond in the user's language — this is non-negotiable.**

| User writes in | You reply in |
|----------------|--------------|
| English | English |
| Chinese | Chinese |
| Japanese | Japanese |
| Spanish | Spanish |

If the user switches language mid-conversation, switch your response language immediately.

---

## Your Role: User Relay

You are a relay between the user and Pexo's backend. You do three things:

1. **Upload** — User provides files → `pexo-upload.sh` → get asset ID
2. **Relay** — Forward user's request exactly to `pexo-chat.sh`
3. **Deliver** — Poll for results → send video file and link to user

### Important

Pexo's backend is a professional video production agent. It understands cinematography, pacing, storytelling, and prompt optimization far better than you. **Do not add your own creative suggestions.** Forward the user's request exactly as given.

---

## Workflow

### Step 1: Upload Assets (If User Provides Files)

If the user uploads files (images, reference videos, audio), upload them first:

bash
pexo-upload.sh /path/to/file.jpg
This returns an `asset_id`. Include this in your relay message.

### Step 2: Relay the User's Request

Copy the user's message exactly and send it to Pexo:

bash
pexo-chat.sh <project_id> "<user's exact message>"
**Rule: Copy the user's words verbatim.** Do not rephrase, improve, or add context.

#### Example 1 — Chinese request:
User said: "做个猫的视频"

bash
pexo-chat.sh proj_abc123 "做个猫的视频"
#### Example 2 — English request with uploaded file:
User said: "I want a product video for my shoes" and uploaded `shoes.jpg`

bash
# First upload the file
pexo-upload.sh shoes.jpg
# Returns: asset_id "ast_xyz789"

# Then relay with the asset
pexo-chat.sh proj_abc123 "I want a product video for my shoes" --asset ast_xyz789
#### Example 3 — Japanese request:
User said: "スニーカー商品のプロモーションビデオを作成してください"

bash
pexo-chat.sh proj_abc123 "スニーカー商品のプロモーションビデオを作成してください"
### Step 3: Present Options (If Pexo Offers Choices)

If Pexo responds with preview options, present them clearly to the user and ask them to choose.

### Step 4: Deliver Results

When video generation completes, provide:
- The video file
- The shareable link
- Any relevant metadata (duration, aspect ratio)

---

## Common Scenarios

| User wants... | Action |
|---------------|--------|
| A product ad | Relay the product description + upload product images if provided |
| TikTok/Instagram content | Relay the content idea + upload any reference media |
| Brand video | Relay brand guidelines/description + upload brand assets if provided |
| Explainer video | Relay the topic + any script or outline the user provides |
| Video from existing script | Upload the script file, then relay with the project context |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Config error | Run `pexo-doctor.sh` |
| Upload fails | Check file path and format compatibility |
| No response from Pexo | Wait and retry; check `pexo-doctor.sh` for API connectivity |
| Wrong language in response | Verify user's input language and adjust accordingly |

---

## Reference Scripts

| Script | Purpose |
|--------|---------|
| `pexo-doctor.sh` | Diagnose setup and connectivity issues |
| `pexo-upload.sh` | Upload user files to get asset IDs |
| `pexo-chat.sh` | Send requests to Pexo backend |

See `references/` directory for additional documentation.
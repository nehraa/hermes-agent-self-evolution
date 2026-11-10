---
category: software-development
description: 'AI video creation agent for producing short videos (5–60 seconds). Supports product ads, social media content, brand videos, explainers, and promotional clips. Available for TikTok, Instagram, YouTube, and other platforms.'
name: pexoai-agent
---

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

Pexo is an AI video creation agent. You send it the user's request, and Pexo handles all creative work — scriptwriting, shot composition, transitions, and music. Pexo may ask clarifying questions or present preview options for the user to choose from.

**Output:** Short videos (5–60 seconds) in 16:9, 9:16, or 1:1 aspect ratios.

## Prerequisites

### Configuration

Create a config file at `~/.pexo/config`:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
### First-Time Setup or Troubleshooting

If this is your first time using the skill or if you encounter a config error, run:

bash
pexo-doctor.sh
Follow the instructions in its output. See `references/SETUP-CHECKLIST.md` for detailed setup steps.

---

## ⚠️ Language Rule (Highest Priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

| User writes in... | You reply in... |
|-------------------|-----------------|
| English | English |
| Chinese (中文) | Chinese (中文) |
| Japanese (日本語) | Japanese (日本語) |
| Spanish | Spanish |
| French | French |
| *Any other language* | *That same language* |

If the user switches language mid-conversation, switch immediately to match.

---

## Your Role: Delivery Worker

You act as a delivery worker between the user and Pexo. You do **not** make creative decisions — Pexo's backend is a professional video creation agent that understands cinematography, pacing, storytelling, and prompt engineering. When you add your own creative ideas, the video quality goes down.

### Workflow

User Request → [You] → Pexo Backend → [You] → User
**Step 1: Upload** (if user provides a file)
- Run `pexo-upload.sh` with the file
- Receive and store the asset ID

**Step 2: Relay**
- Copy the user's message **exactly as written**
- Pass it to `pexo-chat.sh` along with the project ID

**Step 3: Deliver**
- Poll for results using `pexo-poll.sh`
- Send the completed video and shareable link to the user

### How to Relay Messages

When calling `pexo-chat.sh`, copy the user's message **exactly** — do not interpret, simplify, or improve it.

bash
pexo-chat.sh <project_id> "{user's message, copied exactly}"
### Examples

**Example 1 — Chinese request:**
User said: "做个猫的视频"
You run:  pexo-chat.sh proj_123 "做个猫的视频"
**Example 2 — English request with uploaded file:**
User said: "I want a product video for my shoes"
User uploaded: shoes.jpg
You run:  pexo-upload.sh shoes.jpg
         pexo-chat.sh proj_123 "I want a product video for my shoes"
**Example 3 — Chinese request with uploaded file:**
User said: "帮我做这个产品的宣传视频"
User uploaded: product.png
You run:  pexo-upload.sh product.png
         pexo-chat.sh proj_123 "帮我做这个产品的宣传视频"
**Example 4 — Japanese request:**
User said: "料理のデモ動画を作って"
You run:  pexo-chat.sh proj_456 "料理のデモ動画を作って"
---

## Important Rules

1. **Never add creative suggestions** — let Pexo handle all creative decisions
2. **Copy-paste exactly** — do not paraphrase or modify the user's words
3. **Match the language** — reply in the same language the user wrote in
4. **Include uploaded files** — if a file is provided, upload it first before relaying
5. **Deliver results promptly** — once the video is ready, send it to the user immediately
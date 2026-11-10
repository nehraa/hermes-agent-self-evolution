---
category: software-development
name: pexoai-agent
description: >
  Use this skill when the user wants to produce a short video (5–60 seconds).
  Supports any video type: product ads, TikTok/Instagram/YouTube content,
  brand videos, explainers, social clips.
  USE FOR: video production, AI video, make a video, product video, brand video,
  promotional clip, explainer video, short video.
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
version: "0.4.0"
metadata:
  author: pexoai
---

# Pexo Agent

Pexo is an AI video creation agent. You send it the user's request, and Pexo handles all creative work — scriptwriting, shot composition, transitions, music. Pexo may ask clarifying questions or present preview options for the user to choose from.

**Output:** short videos (5–60 seconds, aspect ratios 16:9 / 9:16 / 1:1.

## Prerequisites

Create a config file at `~/.pexo/config`:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
First time using this skill or encountering a config error? Run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for detailed setup instructions.

---

## Language Rule (Highest Priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

| User writes in... | You reply in... |
|--------------------|-----------------|
| English | English |
| Chinese (中文) | Chinese |
| Japanese (日本語) | Japanese |
| Spanish | Spanish |

If the user switches language mid-conversation, switch immediately.

---

## Your Role: Delivery Worker

You are a delivery worker between the user and Pexo. You do three things only:

1. **Upload** — User provides a file → run `pexo-upload.sh` → receive asset ID
2. **Relay** — Copy the user's exact message into `pexo-chat.sh`
3. **Deliver** — Poll for results → send video file and shareable link to user

### ⚠️ Do Not Be Creative

Pexo's backend is a professional video creation agent. It understands cinematography, pacing, storytelling, and prompt engineering far better than you. When you add your own creative ideas or interpretations, video quality goes down.

**Rule: Copy the user's words EXACTLY. Do not rephrase, interpret, or improve them.**

---

## Usage

### Start a New Project

bash
pexo-chat.sh "<project_id>" "<user's exact request>"
### Upload an Asset (image, audio, video)

bash
pexo-upload.sh "<file_path>"
Returns an asset ID. Include this in your message to Pexo.

### Examples

**English request:**
User: "I want a product video for my shoes"
You run: pexo-chat.sh proj_123 "I want a product video for my shoes"
**Chinese request:**
User: "做个猫的视频"
You run: pexo-chat.sh proj_123 "做个猫的视频"
**Request with uploaded file:**
User: "Use this image for the background" (and uploads image.jpg)
You run: 
  pexo-upload.sh image.jpg
  # Returns: asset_abc123
  pexo-chat.sh proj_123 "Use this image for the background" --asset asset_abc123
---

## Workflow

User Request → [Copy Exactly] → pexo-chat.sh → Pexo Backend
                                                 ↓
                                         [Polling for Results]
                                                 ↓
User ← [Video File + Shareable Link] ← Delivery
---

## Error Handling

| Error | Action |
|-------|--------|
| Config not found | Run `pexo-doctor.sh` |
| API key invalid | Run `pexo-doctor.sh` |
| Upload failed | Check file format/size, retry |
| Polling timeout | Check project status manually |

---

## File References

- `references/SETUP-CHECKLIST.md` — Detailed setup guide
- `references/EXAMPLES.md` — More usage examples
- `scripts/pexo-doctor.sh` — Diagnostic tool
- `scripts/pexo-chat.sh` — Send requests to Pexo
- `scripts/pexo-upload.sh` — Upload assets
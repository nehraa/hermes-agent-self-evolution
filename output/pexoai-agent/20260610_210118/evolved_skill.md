---
category: software-development
description: >
  Use this skill when the user wants to produce a short video (5–60 seconds).
  Supports any video type: product ads, TikTok/Instagram/YouTube content,
  brand videos, explainers, social clips.
  USE FOR: video production, AI video, make a video,
  product video, brand video, promotional clip, explainer video, short video.
name: pexoai-agent
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

Pexo is an AI video creation agent that handles all creative work — scriptwriting, shot composition, transitions, and music. You relay the user's request to Pexo, and it produces short videos (5–60 seconds) in aspect ratios 16:9, 9:16, or 1:1.

Pexo may ask clarifying questions or present preview options. Your role is to facilitate communication between the user and Pexo.

## Prerequisites

Create the config file `~/.pexo/config` with your credentials:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
First time using this skill or encountering a config error? Run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for details.

---

## Language Rule (Highest Priority)

**Reply in the SAME language the user uses. This is non-negotiable.**

| User writes in | You reply in |
|----------------|--------------|
| English | English |
| Chinese | Chinese |
| Japanese | Japanese |

If the user switches language mid-conversation, switch immediately.

---

## Your Role: Delivery Worker

You are a conduit between the user and Pexo. Do not add your own creative ideas — Pexo's backend is a professional video creation agent that understands cinematography, pacing, storytelling, and prompt engineering. Your interference degrades output quality.

**Your three tasks:**

1. **Upload**: User provides a file → run `pexo-upload.sh` → receive asset ID
2. **Relay**: Forward the user's exact message to `pexo-chat.sh`
3. **Deliver**: Poll for results → send video and link to user

---

## Relaying Messages

Copy the user's message **exactly** and pass it to `pexo-chat.sh`:

bash
pexo-chat.sh <project_id> "<user's exact message>"
### Examples

**User speaks English:**
User: "I want a product video for my shoes"
bash
pexo-chat.sh proj_123 "I want a product video for my shoes"
**User speaks Chinese:**
User: "做个猫的视频"
bash
pexo-chat.sh proj_123 "做个猫的视频"
**User uploads a file:**
1. Run `pexo-upload.sh <file>` to get an asset ID
2. Include the asset ID when relaying:
bash
pexo-chat.sh proj_123 "Use this product image to create a promotional video: asset_abc123"
---

## Workflow Summary

User Request → You (relay exactly) → Pexo Backend → Video Output → You (deliver to user)
Do not interpret, expand, or improve the user's request. Your job is accurate transmission, not creative direction.
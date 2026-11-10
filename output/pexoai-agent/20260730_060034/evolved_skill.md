---
category: software-development
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

---

## ⚠️ LANGUAGE RULE (highest priority)

**Reply in the SAME language the user uses — this is non-negotiable.**

- English message → English reply
- Chinese message → Chinese reply
- Japanese message → Japanese reply

Switch immediately if the user changes language mid-conversation.

---

## Prerequisites

Config file `~/.pexo/config`:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
**First time using this skill or encountering a config error?** Run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for details.

---

## Your Role: Delivery Worker

You are a relay between the user and Pexo. Do not add creative ideas — Pexo's backend is a professional video creation agent that understands cinematography, pacing, storytelling, and prompt engineering.

### Workflow

| Step | Action | Command |
|------|--------|---------|
| 1. Upload | User provides a file | `pexo-upload.sh` → returns asset ID |
| 2. Relay | Pass user's exact message | `pexo-chat.sh <project_id> "<user's message>"` |
| 3. Deliver | Poll for results | Send video and link to user |

---

## Relaying Messages

Copy the user's message exactly into the command. Do not paraphrase, interpret, or embellish.

### Examples

**User speaks Chinese:**
User: 做个猫的视频
→ pexo-chat.sh proj_123 "做个猫的视频"
**User speaks English with a file:**
User: I want a product video for my shoes (uploads shoes.jpg)
→ pexo-upload.sh shoes.jpg  # returns asset ID
→ pexo-chat.sh proj_123 "I want a product video for my shoes" --asset <asset_id>
**User speaks Japanese:**
User: ブランドの 소개 영상을 만들어주세요
→ pexo-chat.sh proj_456 "ブランドの紹介 영상을 만들어주세요"
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Config not found | Run `pexo-doctor.sh` |
| Upload fails | Check file exists and is valid format |
| No response from Pexo | Poll again — processing may take time |
| User asks for help | Direct them to `references/SETUP-CHECKLIST.md` |
---
category: software-development
description: 'AI-powered short video creation agent for product ads, social media content, brand videos, and explainers (5–60 seconds).'
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

# Pexo AI Video Agent

An AI-powered video creation agent that produces short videos (5–60 seconds) for any purpose: product advertisements, TikTok/Instagram/YouTube content, brand videos, explainers, and social clips.

**Supported aspect ratios:** 16:9, 9:16, 1:1

Pexo handles the full creative pipeline — scriptwriting, shot composition, transitions, and music selection. It may ask clarifying questions or present preview options for the user to choose from.

---

## Prerequisites

### Configuration

Create the config file at `~/.pexo/config`:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
### First-Time Setup or Troubleshooting

If this is your first time using the skill or if you encounter any configuration errors, run:

bash
pexo-doctor.sh
Follow the instructions in its output. For detailed setup guidance, see `references/SETUP-CHECKLIST.md`.

---

## ⚠️ Critical Rule: Language Matching

**You MUST reply in the same language the user uses. This is non-negotiable.**

| User's language | Your response language |
|-----------------|------------------------|
| English         | English                |
| Chinese (中文)   | Chinese (中文)          |
| Japanese (日本語) | Japanese (日本語)        |
| Any other language | Match the user's language |

If the user switches languages mid-conversation, switch immediately to match.

---

## Workflow: Delivery Worker

You act as a delivery worker between the user and the Pexo backend. Your role has three phases:

### 1. Upload (if user provides files)

When the user uploads a file:

bash
pexo-upload.sh <file_path>
This returns an **asset ID** that Pexo uses to reference the uploaded content.

### 2. Relay (mandatory)

Pass the user's request to Pexo using the exact wording they provided:

bash
pexo-chat.sh <project_id> "<user's exact message>"
**Important:** Copy the user's message verbatim. Do not rephrase, enhance, or add your own creative suggestions. The Pexo backend is optimized for prompt engineering — adding your own ideas degrades video quality.

### 3. Deliver (mandatory)

Poll the backend for results, then send the finished video and download link to the user.

---

## Usage Examples

### Example 1: Text request (Chinese)

User: `做个猫的视频`

Your command:
bash
pexo-chat.sh proj_123 "做个猫的视频"
### Example 2: Text request (English)

User: `I want a product video for my running shoes`

Your command:
bash
pexo-chat.sh proj_456 "I want a product video for my running shoes"
### Example 3: Request with file upload

User: `Create a promotional video using this logo` (and uploads `logo.png`)

Your workflow:
bash
# Step 1: Upload the file
pexo-upload.sh logo.png
# Returns: asset_id "asset_789"

# Step 2: Relay the message (optionally include asset references)
pexo-chat.sh proj_456 "Create a promotional video using this logo"
---

## Best Practices

| Do | Don't |
|----|-------|
| Copy user messages exactly | Paraphrase or improve their wording |
| Upload files before relaying | Send creative suggestions of your own |
| Match the user's language | Switch languages independently |
| Poll and deliver results | Assume the first response is final |

Pexo's backend understands cinematography, pacing, storytelling, and prompt engineering. Trust the system — your job is accurate transmission, not creative input.
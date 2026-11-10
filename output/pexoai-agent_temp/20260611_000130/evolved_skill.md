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

---

## ⚠️ Language Rule (Highest Priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

| User writes in... | You reply in... |
|-------------------|-----------------|
| English | English |
| Chinese | Chinese |
| Japanese | Japanese |
| Any other language | That same language |

If the user switches language mid-conversation, switch immediately.

---

## Prerequisites

### 1. Configuration File

Create `~/.pexo/config` with the following:

bash
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
### 2. First-Time Setup or Troubleshooting

If this is your first time using this skill or you encounter any config errors:

bash
pexo-doctor.sh
Follow the output recommendations. See `references/SETUP-CHECKLIST.md` for detailed setup instructions.

---

## Your Role: Delivery Worker

You are a delivery worker between the user and Pexo. Your job is to relay messages accurately — nothing more.

### Core Workflow

User → You → pexo-chat.sh → Pexo Backend → Video Output → User
### Step-by-Step Instructions

#### Step 1: Upload Assets (If Provided)

If the user uploads files (images, videos, audio), upload them first:

bash
pexo-upload.sh <file_path>
This returns an **asset ID** — note it for use in your message to Pexo.

#### Step 2: Relay the User's Request

Copy the user's message **exactly** and send it to Pexo:

bash
pexo-chat.sh <project_id> "<user's message, copied verbatim>"
**Important:** Do not add your own creative ideas, rephrasing, or interpretations. Pexo's backend is a professional video creation agent that understands cinematography, pacing, storytelling, and prompt engineering. Adding your own ideas degrades video quality.

#### Step 3: Poll for Results

Once Pexo starts processing, poll for results:

bash
pexo-poll.sh <project_id>
#### Step 4: Deliver the Output

When the video is ready, send the user:
- The video file
- A shareable link to the video

---

## Examples

### Example 1: Simple Text Request

**User says:** "做个猫的视频"

bash
pexo-chat.sh proj_123 "做个猫的视频"
---

### Example 2: Product Video with Asset

**User says:** "I want a product video for my shoes" and uploads `shoes.jpg`

bash
# Step 1: Upload the image
pexo-upload.sh shoes.jpg
# Returns: asset_abc123

# Step 2: Relay with asset reference
pexo-chat.sh proj_123 "I want a product video for my shoes. Use the uploaded image (asset_abc123)."
---

### Example 3: Brand Video Request

**User says:** "帮我制作一个品牌宣传片，时长30秒，适合抖音平台"

bash
pexo-chat.sh proj_456 "帮我制作一个品牌宣传片，时长30秒，适合抖音平台"
---

## Available Commands

| Command | Purpose |
|---------|---------|
| `pexo-doctor.sh` | Diagnose config issues and guide setup |
| `pexo-upload.sh <file>` | Upload asset files to Pexo |
| `pexo-chat.sh <project_id> "<message>"` | Send request to Pexo |
| `pexo-poll.sh <project_id>` | Poll for video generation status |

---

## Tips

- **Copy-paste only.** Never paraphrase or add creative commentary.
- **If the user uploads files**, always upload them first and include the asset ID in your relay message.
- **If Pexo asks questions**, relay those questions to the user in their language, wait for their response, then relay back.
- **If something breaks**, run `pexo-doctor.sh` first.
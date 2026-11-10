---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Structured Data for LLMs

Extract frames, audio, and transcripts from any video file into formats that LLMs can process. Works with bug reports, security footage, lectures, product demos, and more.

**Supported formats:** MP4, MOV, WebM, MKV, GIF, APNG, WebP

---

## Installation

bash
npm i -g peepshow
**Optional dependencies:**

| Tool | Purpose | Install |
|------|---------|---------|
| `ffmpeg` | Hardware-accelerated video decoding | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| `whisper.cpp` | Local transcription (no API key required) | `brew install whisper.cpp` (macOS) / `scoop install whisper.cpp` (Windows) |

---

## Basic Usage

bash
# Extract frames only (prints file paths)
peepshow ./video.mp4

# Structured output with audio + transcript
peepshow ./video.mp4 --emit json
peepshow ./video.mp4 --emit markdown

# Token-compressed output (~70% fewer tokens)
peepshow ./video.mp4 --emit caveman
---

## Output Formats

### `--emit json`
Returns structured JSON with frame metadata, timestamps, audio path, and transcript segments.

### `--emit markdown`
Human-readable markdown with a timeline of frames and transcribed text.

### `--emit caveman`
Minimal output for token-constrained models. Compresses visual data to essential descriptions with timestamps.

---

## Frame Extraction Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max N` | 40 | Maximum frames to extract |
| `--strategy scene` | uniform | Use scene-detection instead of uniform sampling |
| `--threshold N` | 0.3 | Scene-change sensitivity (0.0–1.0, lower = more sensitive) |
| `--fps N` | — | Force fixed-rate sampling (overrides `--strategy`) |
| `--width N` | 1280 | Max output width in pixels |
| `--format jpg\|png` | jpg | Frame image format |
| `--output <dir>` | ./peepshow-out | Output directory |

**Examples:**

bash
# Extract up to 12 frames at scene changes
peepshow ./video.mp4 --strategy scene --max 12

# High-sensitivity scene detection
peepshow ./video.mp4 --strategy scene --threshold 0.18

# Fixed 1 frame per second
peepshow ./video.mp4 --fps 1

# Higher quality PNG frames
peepshow ./video.mp4 --format png --width 1920
---

## Audio & Transcription

### Local Transcription (Free, No API Key)

bash
peepshow ./video.mp4 --transcribe whisper-cpp
Requires `whisper.cpp` installed. Runs entirely offline.

### Cloud Transcription Options

bash
peepshow ./video.mp4 --transcribe openai      # Uses OPENAI_API_KEY
peepshow ./video.mp4 --transcribe groq        # Uses GROQ_API_KEY (free tier available)
peepshow ./video.mp4 --transcribe deepgram    # Uses DEEPGRAM_API_KEY
peepshow ./video.mp4 --transcribe assemblyai  # Uses ASSEMBLYAI_API_KEY
### Skip Audio/Transcript

bash
# Extract frames only, skip audio entirely
peepshow ./video.mp4 --no-audio --no-transcribe
---

## Frame Descriptions (Vision LLM Captioning)

Add AI-generated descriptions to each frame for vision-capable LLMs.

bash
peepshow ./video.mp4 --describe anthropic   # Uses ANTHROPIC_API_KEY
peepshow ./video.mp4 --describe openai      # Uses OPENAI_API_KEY
peepshow ./video.mp4 --describe google      # Uses GOOGLE_AI_API_KEY
peepshow ./video.mp4 --describe azure       # Uses AZURE_OPENAI_API_KEY
**Combined example:**

bash
peepshow ./video.mp4 \
  --emit markdown \
  --describe anthropic \
  --transcribe whisper-cpp \
  --strategy scene \
  --max 20
---

## Data Sinks (71 Integrations)

Export processed video data to external systems:

bash
# SQLite database
peepshow ./video.mp4 --sink sqlite --db ./peepshow.db

# Cloud storage
peepshow ./video.mp4 --sink s3 --bucket my-videos --prefix frames/

# Notion database
peepshow ./video.mp4 --sink notion --database-id <id> --token <secret>

# Slack notification
peepshow ./video.mp4 --sink slack --webhook <url>

# GitHub Issue
peepshow ./video.mp4 --sink github --repo owner/repo --token <ghp_xxx>

# All sinks: use --sink all or specify multiple
peepshow ./video.mp4 --sink sqlite,slack,notion
Available sinks include: SQLite, S3, GCS, Azure Blob, Notion, Slack, Discord, GitHub Issues, Linear, Jira, Trello, Asana, Airtable, PostgreSQL, MySQL, MongoDB, Elasticsearch, Pinecone, Weaviate, Qdrant, and more.

---

## Common Use Cases

bash
# Bug reproduction analysis
peepshow ./screen-recording.mp4 --emit markdown --describe openai --max 30

# CCTV footage review
peepshow ./cam-footage.mkv --strategy scene --threshold 0.2 --transcribe whisper-cpp

# Lecture notes extraction
peepshow ./lecture.mp4 --emit markdown --transcribe groq --max 50

# Demo walkthrough for code review
peepshow ./demo.mp4 --emit caveman --describe anthropic --sink github
---

## Environment Variables

Set these once; they're reused across runs:

bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GROQ_API_KEY=gsk_...
export DEEPGRAM_API_KEY=...
export ASSEMBLYAI_API_KEY=...
export GOOGLE_AI_API_KEY=...
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_ENDPOINT=https://...
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ffmpeg not found` | Install via `brew install ffmpeg` or `sudo apt install ffmpeg` |
| `whisper-cpp not found` | Install via `brew install whisper.cpp` |
| Slow extraction | Use `--width 640` for smaller frames, or install `ffmpeg` for hardware acceleration |
| Out of memory | Reduce `--max` frames or `--width` size |
| Transcription fails | Verify API key environment variable is set correctly |
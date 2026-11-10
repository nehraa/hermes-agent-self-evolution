---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Structured Data → Any LLM

Extract frames, audio, and transcripts from any video file so any LLM can analyze visual content, speech, and timeline simultaneously.

**Supported formats:** MP4, MOV, WebM, MKV, GIF, APNG, WebP

## Installation

bash
npm i -g peepshow
**Optional dependencies:**

bash
# Local transcription (no API key required)
brew install whisper.cpp        # macOS
# or: scoop install whisper.cpp # Windows

# Hardware-accelerated video decoding
brew install ffmpeg             # macOS
sudo apt install ffmpeg         # Linux
---

## Basic Usage

bash
# Frame paths only (fastest)
peepshow ./video.mp4

# Full structured output (frames + audio + transcript)
peepshow ./video.mp4 --emit json

# Human-readable markdown report
peepshow ./video.mp4 --emit markdown

# Token-compressed output (~70% fewer tokens)
peepshow ./video.mp4 --emit caveman
---

## Frame Extraction Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **uniform** (default) | Evenly spaced frames across entire video | `peepshow ./video.mp4 --max 30` |
| **scene** | Key moments only (scene changes, motion) | `peepshow ./video.mp4 --strategy scene --max 15` |
| **fps** | Fixed rate sampling | `peepshow ./video.mp4 --fps 2` |

bash
# Control frame count
peepshow ./video.mp4 --max 20

# Scene detection sensitivity (0-1, lower = more sensitive)
peepshow ./video.mp4 --strategy scene --threshold 0.18

# Force specific frame rate
peepshow ./video.mp4 --fps 1
---

## Frame Output Options

bash
# Resize frames (maintains aspect ratio)
peepshow ./video.mp4 --width 1280    # max width in pixels
peepshow ./video.mp4 --width 1920    # HD quality

# Change format
peepshow ./video.mp4 --format png    # lossless
peepshow ./video.mp4 --format jpg    # smaller files (default)

# Custom output directory
peepshow ./video.mp4 --output /tmp/analysis
---

## Transcription

### Local (No API Key)

bash
peepshow ./video.mp4 --transcribe whisper-cpp
Requires `whisper.cpp` installed locally.

### Cloud Services (Requires API Key)

bash
peepshow ./video.mp4 --transcribe openai      # OPENAI_API_KEY
peepshow ./video.mp4 --transcribe groq        # GROQ_API_KEY
peepshow ./video.mp4 --transcribe deepgram    # DEEPGRAM_API_KEY
peepshow ./video.mp4 --transcribe assemblyai  # ASSEMBLYAI_API_KEY
### Skip Audio/Transcription

bash
peepshow ./video.mp4 --no-audio --no-transcribe
---

## Frame Descriptions (Vision LLM)

Add AI-generated captions to each frame for vision-capable LLMs.

bash
peepshow ./video.mp4 --describe anthropic   # ANTHROPIC_API_KEY
peepshow ./video.mp4 --describe openai      # OPENAI_API_KEY
---

## Data Sinks (71 Integrations)

Export analysis results to your preferred destination.

bash
# Database
peepshow ./video.mp4 --sink sqlite
peepshow ./video.mp4 --sink postgres

# Cloud Storage
peepshow ./video.mp4 --sink s3
peepshow ./video.mp4 --sink gcs
peepshow ./video.mp4 --sink azure

# Collaboration Tools
peepshow ./video.mp4 --sink notion
peepshow ./video.mp4 --sink slack
peepshow ./video.mp4 --sink github-issues

# CI/CD & DevOps
peepshow ./video.mp4 --sink github-actions
peepshow ./video.mp4 --sink pagerduty
peepshow ./video.mp4 --sink datadog

# Communication
peepshow ./video.mp4 --sink email
peepshow ./video.mp4 --sink discord
peepshow ./video.mp4 --sink teams
Full list: `peepshow --sinks`

---

## Complete Examples

bash
# Bug report analysis: scenes + transcription + JSON output
peepshow ./bug-repro.mp4 --strategy scene --max 15 --transcribe whisper-cpp --emit json --output ./bug-analysis

# Lecture notes: uniform frames + markdown + Notion export
peepshow ./lecture.mp4 --max 40 --transcribe openai --emit markdown --sink notion

# CCTV review: high frame rate + no audio + SQLite storage
peepshow ./cctv.mp4 --fps 5 --no-audio --sink sqlite
---

## Output Structure

./output/
├── frames/
│   ├── frame-001.jpg
│   ├── frame-002.jpg
│   └── ...
├── audio.mp3
├── transcript.json
├── timeline.json      # frame + transcript alignment
└── analysis.json      # vision descriptions (if --describe)
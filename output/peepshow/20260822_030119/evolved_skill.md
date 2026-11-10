---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video Analysis Pipeline

Transform any video into structured data (frames, audio, transcript) that LLMs can process. Ideal for analyzing bug reproductions, security footage, lecture recordings, product demos, and training data extraction.

## Supported Formats

**Video:** MP4, MOV, WebM, MKV, GIF, APNG, WebP
**Transcription engines:** whisper.cpp (local), OpenAI Whisper, Groq, Deepgram, AssemblyAI

---

## Installation

bash
npm install -g peepshow
### Optional Dependencies

**Local transcription (no API key required):**

bash
# macOS
brew install whisper.cpp

# Linux
sudo apt install whisper.cpp   # Debian/Ubuntu
sudo dnf install whisper.cpp   # Fedora

# Windows
scoop install whisper.cpp
# or download from: https://github.com/ggerganov/whisper.cpp/releases
**Hardware-accelerated video decoding (recommended for large files):**

bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg        # Debian/Ubuntu
sudo dnf install ffmpeg        # Fedora

# Windows (via package managers)
scoop install ffmpeg
winget install ffmpeg
---

## Quick Start

bash
# Extract frames only (fastest, default 40 frames)
peepshow ./video.mp4

# Full analysis with transcript and timestamps
peepshow ./video.mp4 --transcribe whisper-cpp --emit json

# Human-readable report
peepshow ./video.mp4 --transcribe whisper-cpp --emit markdown
---

## Output Formats

| Format | Best For | Size |
|--------|----------|------|
| `paths` (default) | Debugging, custom pipelines | Smallest |
| `json` | Structured data, API integration | Medium |
| `markdown` | Human review, documentation | Large |
| `caveman` | Token-constrained LLM contexts (~70% reduction) | Smallest |

bash
peepshow ./video.mp4 --emit json
peepshow ./video.mp4 --emit markdown
peepshow ./video.mp4 --emit caveman
---

## Frame Selection Strategies

| Strategy | When to Use |
|----------|-------------|
| `uniform` (default) | General-purpose, even coverage |
| `scene` | Detects cuts/fades, better for edited content |
| `fps` | Fixed interval sampling |

bash
# Scene detection (good for movies, screen recordings)
peepshow ./video.mp4 --strategy scene --max 20

# Fixed rate (1 frame per second)
peepshow ./video.mp4 --strategy fps --fps 1

# Tune scene sensitivity (lower = more sensitive)
peepshow ./video.mp4 --strategy scene --threshold 0.18
---

## Frame Extraction Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max N` | 40 | Maximum frames to extract |
| `--width N` | 1280 | Max output width (aspect preserved) |
| `--format jpg\|png` | jpg | Image format |
| `--output <dir>` | ./peepshow-* | Output directory |
| `--quality N` | 80 | JPEG quality (1-100) |

bash
# High-quality PNG frames for detailed analysis
peepshow ./video.mp4 --format png --max 60 --output ./frames

# Thumbnail-sized frames for overview
peepshow ./video.mp4 --width 640 --max 100
---

## Transcription

### Local (Recommended — No API Key)

bash
# whisper.cpp must be installed
peepshow ./video.mp4 --transcribe whisper-cpp
### Cloud Services (Requires API Key)

Set the environment variable before running:

bash
export OPENAI_API_KEY="sk-..."
export GROQ_API_KEY="gsk_..."
export DEEPGRAM_API_KEY="..."
export ASSEMBLYAI_API_KEY="..."
bash
# OpenAI Whisper (uses OPENAI_API_KEY)
peepshow ./video.mp4 --transcribe openai

# Groq (fast, free tier available, uses GROQ_API_KEY)
peepshow ./video.mp4 --transcribe groq

# Deepgram (uses DEEPGRAM_API_KEY)
peepshow ./video.mp4 --transcribe deepgram

# AssemblyAI (uses ASSEMBLYAI_API_KEY)
peepshow ./video.mp4 --transcribe assemblyai
### Skip Audio/Transcription

bash
# Extract frames only (fastest option)
peepshow ./video.mp4 --no-audio --no-transcribe

# Extract frames + audio, skip transcription
peepshow ./video.mp4 --no-transcribe
---

## Frame Description (Vision Models)

Add AI-generated captions to each frame using vision-capable models:

bash
# Anthropic Claude (requires ANTHROPIC_API_KEY)
peepshow ./video.mp4 --describe anthropic

# OpenAI GPT-4 Vision (requires OPENAI_API_KEY)
peepshow ./video.mp4 --describe openai

# Combine with transcription for full analysis
peepshow ./video.mp4 --describe anthropic --transcribe whisper-cpp --emit json
---

## Data Sinks (71 Integrations)

Export extracted data to external systems:

bash
# SQLite database
peepshow ./video.mp4 --sink sqlite --db ./analysis.db

# AWS S3
peepshow ./video.mp4 --sink s3 --bucket my-bucket --prefix frames/

# Project management
peepshow ./video.mp4 --sink github --repo owner/repo --issue
peepshow ./video.mp4 --sink notion --database-id <id>

# Notifications
peepshow ./video.mp4 --sink slack --channel #video-analysis
peepshow ./video.mp4 --sink email --to analyst@company.com

# Full list of sinks:
# airtable, asana, axiodb, bastion, bedrock, bigquery, bloc, chrome, confluence,
# cortex, couchdb, crowdstrike, database, demisto, dingtalk, elasticsearch,
# embedding, eventbridge, fanout, firebase, firestore, gcs, ghost, github,
# gitlab, google-sheets, graphite, hubspot, jira, kinesis, kodi, lambdalib,
# linear, lore, luma, meetup, mermaid, mongodb, notion, openfaas, otel,
# pagerduty, pinecone, postgres, print, prometheus, pubsub, pushover, qdrant,
# redash, redis, registry, s3, sanitize, sftp, slack, snowflake, sql,
# sqlite, statsd, stream, supernotes, sync, telegram, timescale, trello,
# twisted, typesense, weaviate, webhook, wordpress, xata, youtube
---

## Common Workflows

### Bug Report Analysis

bash
# Capture screen recording, extract key frames + audio
peepshow ./bug-repro.mp4 --strategy scene --max 30 --transcribe whisper-cpp --emit markdown --output ./bug-frames
### CCTV/Security Footage Review

bash
# 24-hour footage → 50 representative frames
peepshow ./camera1.mp4 --strategy scene --max 50 --fps 0.1 --output ./review
### Lecture/Meeting Notes

bash
# Generate searchable transcript + slide frames
peepshow ./lecture.mp4 --transcribe groq --max 25 --emit markdown --sink notion
### Training Data Extraction

bash
# High-quality frames for ML datasets
peepshow ./raw-footage.mp4 --format png --width 1920 --max 500 --describe openai --emit json
---

## Environment Variables

| Variable | Used By | Required For |
|----------|---------|--------------|
| `OPENAI_API_KEY` | `--transcribe openai`, `--describe openai` | Cloud transcription, OpenAI vision |
| `ANTHROPIC_API_KEY` | `--describe anthropic` | Anthropic vision captions |
| `GROQ_API_KEY` | `--transcribe groq` | Groq transcription |
| `DEEPGRAM_API_KEY` | `--transcribe deepgram` | Deepgram transcription |
| `ASSEMBLYAI_API_KEY` | `--transcribe assemblyai` | AssemblyAI transcription |
| `AWS_*` | `--sink s3`, `--sink kinesis`, etc. | AWS integrations |
| `NOTION_TOKEN` | `--sink notion` | Notion integration |

---

## Troubleshooting

**"whisper.cpp not found":** Install it separately or use cloud transcription. See [Optional Dependencies](#optional-dependencies).

**Slow extraction on large files:** Install ffmpeg for hardware acceleration.

**Low scene detection accuracy:** Adjust `--threshold` (try 0.15 for subtle changes, 0.5 for obvious cuts).

**Token limit exceeded:** Use `--emit caveman` for compressed output.

**API rate limits:** Use `--transcribe whisper-cpp` for local transcription with no rate limits.

---

## See Also

- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) — Local transcription engine
- [ffmpeg](https://ffmpeg.org/) — Video processing backend
- Video frame extraction patterns in `~/.peepshow/examples/`
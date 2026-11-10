---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Structured Data for LLMs

Convert any video into a timeline of frames + audio + transcript, enabling any LLM to "watch and listen" for analysis.

**Supported formats:** MP4, MOV, WebM, MKV, GIF, APNG, WebP

## Installation

bash
npm i -g peepshow
**Recommended dependencies:**

bash
# Local transcription (no API key required)
brew install whisper.cpp    # macOS
# or: scoop install whisper.cpp   # Windows
# or: build from source           # Linux

# Hardware-accelerated video decoding
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Linux
scoop install ffmpeg         # Windows
---

## Basic Usage

bash
# Extract frames only (default output)
peepshow ./video.mp4

# Structured JSON (frames + audio + transcript)
peepshow ./video.mp4 --emit json

# Human-readable Markdown
peepshow ./video.mp4 --emit markdown

# Token-compressed output (~70% fewer tokens)
peepshow ./video.mp4 --emit caveman
---

## Output Formats

### `--emit json`

Returns structured data suitable for programmatic processing:

json
{
  "metadata": { "duration": 120.5, "fps": 30, "resolution": "1920x1080" },
  "frames": [
    { "timestamp": 0.0, "path": "/tmp/frame_0000.jpg", "description": "..." },
    { "timestamp": 2.5, "path": "/tmp/frame_0001.jpg", "description": "..." }
  ],
  "audio": { "path": "/tmp/audio.wav", "duration": 120.5 },
  "transcript": { "text": "...", "segments": [...] }
}
### `--emit markdown`

Human-readable format with timestamps and descriptions:

markdown
# Video Analysis

**Duration:** 2:00 | **Frames:** 40 | **Resolution:** 1920x1080

## Frame 0:00
![](./frames/frame_0000.jpg)
> Loading screen with progress bar at 0%

## Frame 0:02
![](./frames/frame_0001.jpg)
> Application window opens showing dashboard
### `--emit caveman`

Ultra-minimal token-efficient format for constrained contexts:

00:00 [frame_0000.jpg] loading screen
00:02 [frame_0001.jpg] dashboard visible
00:05 [frame_0002.jpg] user clicks settings
---

## Frame Selection Strategies

| Strategy | Use Case | Example |
|----------|----------|---------|
| `uniform` (default) | General purpose, evenly spaced frames | `--strategy uniform --max 40` |
| `scene` | Detect meaningful changes, skip static content | `--strategy scene --max 20` |
| `fps` | Fixed-rate sampling | `--fps 2` (2 frames per second) |

bash
# Scene detection with custom sensitivity
peepshow ./video.mp4 --strategy scene --threshold 0.2

# Force specific frame rate
peepshow ./video.mp4 --fps 1 --max 30
---

## Key Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--max N` | 40 | Maximum frames to extract |
| `--strategy scene\|uniform\|fps` | uniform | Frame selection algorithm |
| `--threshold N` | 0.3 | Scene detection sensitivity (0.0–1.0) |
| `--fps N` | — | Fixed frames-per-second sampling |
| `--width N` | 1280 | Max output width (preserves aspect ratio) |
| `--format jpg\|png\|webp` | jpg | Output image format |
| `--output <dir>` | `./peepshow_output/` | Output directory |
| `--start N` | 0 | Start time in seconds |
| `--end N` | video duration | End time in seconds |

---

## Audio Extraction

bash
# Extract audio track only
peepshow ./video.mp4 --audio-only

# Skip audio entirely
peepshow ./video.mp4 --no-audio
---

## Transcription

Transcription uses local Whisper by default when available.

bash
# Local transcription (whisper.cpp — no API key)
peepshow ./video.mp4 --transcribe whisper-cpp

# Skip transcription
peepshow ./video.mp4 --no-transcribe

# Cloud transcription options
peepshow ./video.mp4 --transcribe openai       # OPENAI_API_KEY
peepshow ./video.mp4 --transcribe groq         # GROQ_API_KEY
peepshow ./video.mp4 --transcribe deepgram     # DEEPGRAM_API_KEY
peepshow ./video.mp4 --transcribe assemblyai   # ASSEMBLYAI_API_KEY
---

## Frame Description (Vision LLM)

Add AI-generated captions to each frame:

bash
# Anthropic Claude
peepshow ./video.mp4 --describe anthropic    # ANTHROPIC_API_KEY

# OpenAI GPT-4 Vision
peepshow ./video.mp4 --describe openai       # OPENAI_API_KEY

# Google Gemini
peepshow ./video.mp4 --describe google       # GOOGLE_API_KEY
---

## Output Sinks

Export results directly to 71 integrations:

bash
# Database
peepshow ./video.mp4 --sink sqlite --db ./results.db
peepshow ./video.mp4 --sink postgres --url "postgresql://..."

# Cloud storage
peepshow ./video.mp4 --sink s3 --bucket my-bucket --region us-east-1

# Note-taking & docs
peepshow ./video.mp4 --sink notion --page-id <id>
peepshow ./video.mp4 --sink confluence --url https://... --space KEY

# Communication
peepshow ./video.mp4 --sink slack --channel #alerts --webhook <url>
peepshow ./video.mp4 --sink discord --webhook <url>

# Issue tracking
peepshow ./video.mp4 --sink github --repo owner/repo --token <key>
peepshow ./video.mp4 --sink jira --url https://... --project KEY

# Search & vector DB
peepshow ./video.mp4 --sink elasticsearch --url https://...
peepshow ./video.mp4 --sink pinecone --index video-analysis
peepshow ./video.mp4 --sink weaviate --url https://...

# File-based
peepshow ./video.mp4 --sink filesystem --path ./output
peepshow ./video.mp4 --sink json --path ./results.json
Run `peepshow --sinks` for the full list of 71 supported integrations.

---

## Complete Examples

bash
# Bug reproduction report
peepshow ./screenrecord.mp4 --emit markdown --transcribe whisper-cpp --describe anthropic --output ./bug_report

# CCTV footage analysis
peepshow ./security_cam.mkv --strategy scene --threshold 0.15 --transcribe none --describe openai --sink sqlite --db ./footage.db

# Lecture notes extraction
peepshow ./lecture.mp4 --max 25 --emit markdown --transcribe openai --sink notion --page-id <id>
---

## Environment Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `OPENAI_API_KEY` | `--transcribe openai`, `--describe openai` | OpenAI Whisper & GPT-4 Vision |
| `ANTHROPIC_API_KEY` | `--describe anthropic` | Claude for frame descriptions |
| `GROQ_API_KEY` | `--transcribe groq` | Groq cloud transcription |
| `DEEPGRAM_API_KEY` | `--transcribe deepgram` | Deepgram transcription |
| `ASSEMBLYAI_API_KEY` | `--transcribe assemblyai` | AssemblyAI transcription |
| `GOOGLE_API_KEY` | `--describe google` | Gemini for frame descriptions |

---

## Troubleshooting

**"whisper.cpp not found"** — Install via `brew install whisper.cpp` or ensure it's in your PATH

**"ffmpeg not found"** — Install via your package manager or set `FFMPEG_PATH` env var

**Slow processing** — Install ffmpeg for hardware acceleration; use `--strategy scene` to skip duplicate frames

**High token usage** — Use `--emit caveman` for ~70% token reduction or `--max 20` to limit frames
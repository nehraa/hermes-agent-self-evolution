---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Frames → LLM

Convert any video into a timeline of still frames with audio and transcript, enabling any LLM to analyze visual and audio content.

**Supported formats:** MP4, MOV, WebM, MKV, GIF, APNG, WebP

---

## Installation

bash
npm i -g peepshow
**Optional dependencies:**

| Tool | Purpose | Install Command |
|------|---------|-----------------|
| whisper.cpp | Local transcription (no API key) | `brew install whisper.cpp` (macOS) or `scoop install whisper.cpp` (Windows) |
| ffmpeg | Hardware-accelerated decoding | `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux) |

---

## Quick Start

bash
# Basic: extract frames only, output file paths
peepshow ./video.mp4

# Structured output with audio and transcript
peepshow ./video.mp4 --emit json

# Human-readable report
peepshow ./video.mp4 --emit markdown

# Token-compressed format (~70% fewer tokens)
peepshow ./video.mp4 --emit caveman
---

## Output Formats

| Format | Use Case |
|--------|----------|
| `json` | Machine parsing, API integration, structured analysis |
| `markdown` | Human review, documentation, sharing |
| `caveman` | Token-limited contexts, budget-conscious inference |

---

## Frame Extraction Options

### Sampling Strategies

| Strategy | Description |
|----------|-------------|
| `uniform` (default) | Evenly spaced frames across video duration |
| `scene` | Detect scene changes, extract keyframes only |
| `smart` | Combine uniform + scene detection for optimal coverage |

bash
# Scene-change detection (good for action-heavy content)
peepshow ./video.mp4 --strategy scene --max 12

# Fixed framerate sampling
peepshow ./video.mp4 --fps 2   # 2 frames per second
### Frame Controls

| Flag | Default | Description |
|------|---------|-------------|
| `--max N` | 40 | Maximum frames to extract |
| `--fps N` | auto | Force fixed frames-per-second |
| `--threshold N` | 0.3 | Scene sensitivity (0.0–1.0, lower = more sensitive) |
| `--width N` | 1280 | Max output width in pixels |
| `--format jpg\|png` | jpg | Image format (png for transparency) |
| `--output <dir>` | ./peepshow | Output directory path |

bash
# High-quality extraction with more frames
peepshow ./video.mp4 --max 60 --width 1920 --format png

# Custom output location
peepshow ./video.mp4 --output /tmp/analysis
---

## Audio Extraction

bash
# Extract audio track separately
peepshow ./video.mp4 --extract-audio

# Skip audio processing entirely
peepshow ./video.mp4 --no-audio
---

## Transcription

### Local (No API Key)

bash
peepshow ./video.mp4 --transcribe whisper-cpp
Requires `whisper.cpp` installed. Runs entirely offline.

### Cloud Services (Requires API Key)

| Provider | Flag | Environment Variable |
|----------|------|---------------------|
| OpenAI Whisper | `--transcribe openai` | `OPENAI_API_KEY` |
| Groq | `--transcribe groq` | `GROQ_API_KEY` |
| Deepgram | `--transcribe deepgram` | `DEEPGRAM_API_KEY` |
| AssemblyAI | `--transcribe assemblyai` | `ASSEMBLYAI_API_KEY` |

bash
# Using OpenAI
peepshow ./video.mp4 --transcribe openai

# Skip transcription
peepshow ./video.mp4 --no-transcribe
---

## Frame Description (Vision LLM Captioning)

Add natural language descriptions to each frame using a vision-capable LLM.

| Provider | Flag | Environment Variable |
|----------|------|---------------------|
| Anthropic (Claude) | `--describe anthropic` | `ANTHROPIC_API_KEY` |
| OpenAI (GPT-4o) | `--describe openai` | `OPENAI_API_KEY` |
| Google (Gemini) | `--describe google` | `GOOGLE_API_KEY` |

bash
# Describe frames with Claude
peepshow ./video.mp4 --describe anthropic --emit json

# Combine with transcription
peepshow ./video.mp4 --describe anthropic --transcribe whisper-cpp
---

## Data Sink Integration

Export structured data to 71 destinations including:

**Databases:** SQLite, PostgreSQL, MySQL, MongoDB, Redis

**Storage:** S3, GCS, Azure Blob, local filesystem

**Productivity:** Notion, Slack, GitHub Issues, Linear, Jira

**Analytics:** Datadog, New Relic, PagerDuty

bash
# Export to SQLite database
peepshow ./video.mp4 --sink sqlite --db ./analysis.db

# Send summary to Slack
peepshow ./video.mp4 --sink slack --slack-channel #video-alerts

# Create GitHub Issue with findings
peepshow ./video.mp4 --sink github --repo owner/repo
---

## Common Workflows

### Bug Reproduction Analysis

bash
peepshow ./bug-repro.mp4 --emit json --describe anthropic --transcribe whisper-cpp
### CCTV/Footage Review

bash
peepshow ./surveillance.mp4 --strategy scene --max 20 --output ./review
### Lecture/Demo Processing

bash
peepshow ./lecture.mp4 --emit markdown --transcribe deepgram --describe anthropic
### Quick Frame Dump

bash
peepshow ./video.mp4 --max 10 --output ./frames --format png
---

## Output Structure

./peepshow/
├── frames/
│   ├── frame_0001.jpg
│   ├── frame_0002.jpg
│   └── ...
├── audio.wav
├── transcript.txt
├── transcript.json
└── report.json    # Full analysis with descriptions
---

## Environment Variables

Set these once; `peepshow` uses them automatically:

bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GROQ_API_KEY=gsk_...
export DEEPGRAM_API_KEY=...
export ASSEMBLYAI_API_KEY=...
export GOOGLE_API_KEY=...
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No frames extracted | Check video codec compatibility; install ffmpeg |
| Transcription fails | Verify API key, check network, try `--transcribe whisper-cpp` |
| Slow processing | Use `--strategy scene` or reduce `--max` frames |
| Memory errors | Lower `--max` or `--width` values |
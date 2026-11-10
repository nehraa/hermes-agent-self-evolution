---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Structured Analysis Output

Convert any video into a timeline of still frames, audio track, and transcript — enabling LLMs to "watch and listen" to video content.

**Supported formats:** MP4, MOV, WebM, MKV, GIF, APNG, WebP

---

## Installation

bash
npm i -g peepshow
**Optional dependencies:**

| Tool | Purpose | Install Command |
|------|---------|-----------------|
| `whisper.cpp` | Local transcription (no API key, no cloud) | `brew install whisper.cpp` (macOS) or `scoop install whisper.cpp` (Windows) |
| `ffmpeg` | Hardware-accelerated video decoding | `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux) |

---

## Basic Usage

bash
# Extract frames only (outputs paths)
peepshow ./video.mp4

# Structured JSON (frames + audio + transcript)
peepshow ./video.mp4 --emit json

# Human-readable Markdown
peepshow ./video.mp4 --emit markdown

# Token-compressed output (~70% fewer tokens, for smaller-context LLMs)
peepshow ./video.mp4 --emit caveman
---

## Frame Extraction Flags

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `--max N` | Maximum frames to extract | 40 | `--max 20` |
| `--strategy scene` | Use scene-change detection instead of uniform sampling | off | `--strategy scene --max 12` |
| `--threshold N` | Scene sensitivity (0 = most sensitive, 1 = least) | 0.3 | `--threshold 0.18` |
| `--fps N` | Force fixed frame-rate sampling | auto | `--fps 1` |
| `--width N` | Max output width (maintains aspect ratio) | 1280 | `--width 1920` |
| `--format jpg\|png` | Output image format | jpg | `--format png` |
| `--output <dir>` | Output directory | ./peepshow-out | `--output /tmp/frames` |

### Sampling Strategies

**Uniform sampling** (default): Evenly spaced frames across the video duration.
bash
peepshow ./video.mp4 --max 30
**Scene detection**: Detects cuts, fades, and transitions; captures fewer but more meaningful frames.
bash
peepshow ./video.mp4 --strategy scene --max 12 --threshold 0.2
**Fixed FPS**: Extracts one frame every N seconds.
bash
peepshow ./video.mp4 --fps 0.5   # one frame every 2 seconds
---

## Audio + Transcription

bash
# Local transcription (no API key required)
peepshow ./video.mp4 --transcribe whisper-cpp

# Cloud transcription options (requires API key)
peepshow ./video.mp4 --transcribe openai       # needs OPENAI_API_KEY
peepshow ./video.mp4 --transcribe groq         # needs GROQ_API_KEY
peepshow ./video.mp4 --transcribe deepgram     # needs DEEPGRAM_API_KEY
peepshow ./video.mp4 --transcribe assemblyai   # needs ASSEMBLYAI_API_KEY

# Skip audio and transcription entirely
peepshow ./video.mp4 --no-audio --no-transcribe
---

## Frame Description (Vision LLM Captioning)

Automatically generate natural-language descriptions of each frame using a vision-capable LLM.

bash
# Anthropic Claude
peepshow ./video.mp4 --describe anthropic    # needs ANTHROPIC_API_KEY

# OpenAI GPT-4 Vision
peepshow ./video.mp4 --describe openai       # needs OPENAI_API_KEY

# Combine with transcription
peepshow ./video.mp4 --describe openai --transcribe whisper-cpp --emit markdown
---

## Output Formats

### JSON Output
json
{
  "video": "./video.mp4",
  "duration": 120.5,
  "frames": [
    {
      "timestamp": 0.0,
      "path": "./peepshow-out/frame_0000.jpg",
      "description": "..."
    },
    {
      "timestamp": 5.2,
      "path": "./peepshow-out/frame_0001.jpg",
      "description": "..."
    }
  ],
  "transcript": "...",
  "audio": "./peepshow-out/audio.wav"
}
### Markdown Output
markdown
# Video Analysis: ./video.mp4 (2m 0s)

## 00:00 — Frame 1
![](./peepshow-out/frame_0000.jpg)
*Scene shows a user clicking the login button*

## 00:05 — Frame 2
![](./peepshow-out/frame_0001.jpg)
*Error dialog appears with 'Connection Timeout'*

## Transcript
00:00 Hello, welcome to the demo...
00:05 As you can see here, when I click...
---

## Common Use Cases

| Scenario | Recommended Command |
|----------|---------------------|
| Bug reproduction video | `peepshow bug.mp4 --emit markdown --transcribe whisper-cpp` |
| CCTV / security footage | `peepshow cam.mp4 --strategy scene --max 20 --no-transcribe` |
| Lecture recording | `peepshow lecture.mp4 --describe openai --transcribe openai` |
| Quick frame count | `peepshow video.mp4 --max 5 --no-audio` |

---

## Environment Variables

Set these in your shell profile or `.env` file:

bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...
DEEPGRAM_API_KEY=...
ASSEMBLYAI_API_KEY=...
---

## Output Directory

All outputs are written to `./peepshow-out/` by default. Use `--output` to change:

bash
peepshow ./video.mp4 --output ./analysis/run-001
**Contents:**
- `frame_XXXX.jpg` (or `.png`) — extracted frames
- `audio.wav` — extracted audio track
- `transcript.txt` — full transcription
- `output.json` or `output.md` — structured results
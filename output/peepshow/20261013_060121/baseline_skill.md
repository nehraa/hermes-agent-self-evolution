---
name: peepshow
description: Extract frames + audio + transcript from any video so any LLM can watch and listen. Turn bug repro videos, CCTV footage, lectures, demos into structured frames for analysis. Supports 71 sink integrations (SQLite, S3, Notion, Slack, GitHub Issues, etc.).
trigger: "peepshow <video>"
category: video
tools: [terminal, file]
---

# Peepshow — Video → Frames → LLM

Turn any video (MP4, MOV, WebM, MKV, GIF, APNG, WebP) into a timeline of still frames + audio track + transcript, so any LLM can watch and listen.

## Installation

```bash
npm i -g peepshow
```

**Optional dependencies:**
```bash
# For local transcription (no cloud, no API key)
brew install whisper.cpp   # macOS
# or: scoop install whisper.cpp  # Windows

# For faster hardware-accelerated decoding
brew install ffmpeg   # macOS
sudo apt install ffmpeg   # Linux
```

---

## Core Usage

```bash
# Default: extract frames, output paths only
peepshow ./video.mp4

# Structured JSON (includes audio + transcript)
peepshow ./video.mp4 --emit json

# Markdown (human-readable)
peepshow ./video.mp4 --emit markdown

# Token-compressed (~70% fewer tokens, pairs with caveman LLM)
peepshow ./video.mp4 --emit caveman
```

---

## Key Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--max N` | Max frames to keep (default 40) | `--max 20` |
| `--strategy scene` | Scene-change detection | `--strategy scene --max 12` |
| `--threshold N` | Scene sensitivity 0-1 (default 0.3) | `--threshold 0.18` |
| `--fps N` | Force fixed fps sampling | `--fps 1` |
| `--width N` | Max output width (default 1280) | `--width 1920` |
| `--format jpg\|png` | Frame format (default jpg) | `--format png` |
| `--output <dir>` | Output directory | `--output /tmp/frames` |

---

## Audio + Transcription

```bash
# Local transcription (whisper.cpp — no API key needed)
peepshow ./video.mp4 --transcribe whisper-cpp

# Cloud transcription options
peepshow ./video.mp4 --transcribe openai      # needs OPENAI_API_KEY
peepshow ./video.mp4 --transcribe groq        # needs GROQ_API_KEY
peepshow ./video.mp4 --transcribe deepgram    # needs DEEPGRAM_API_KEY
peepshow ./video.mp4 --transcribe assemblyai  # needs ASSEMBLYAI_API_KEY

# Skip audio entirely
peepshow ./video.mp4 --no-audio --no-transcribe
```

---

## Frame Description (Vision LLM)

```bash
# Auto-caption each frame with vision LLM
peepshow ./video.mp4 --describe anthropic   # needs ANTHROPIC_API_KEY
peepshow ./video.mp4 --describe openai     # needs OPENAI_API_KEY
```

---

## Sink Integrations (71 supported stores)

```bash
# SQLite — tag and search footage
peepshow ./cctv.mp4 --strategy scene --max 60 \
  --sink sqlite:./incidents.db --tag camera=front-door

# Obsidian — lecture to notes
peepshow ./lecture.mp4 --strategy scene \
  --emit markdown --sink obsidian:~/vault/Lectures

# GitHub Issues — CVE/exploit analysis
peepshow ./cve.mp4 --strategy scene --max 20 \
  --emit xml --sink github-issues:owner/repo --tag severity=high

# S3-compatible storage
peepshow ./video.mp4 --sink s3:my-bucket/path

# Slack notification
peepshow ./video.mp4 --sink slack

# Webhook (generic)
peepshow ./video.mp4 --sink webhook:https://example.com/describe

# Multiple sinks at once
peepshow ./video.mp4 --sink sqlite:./db.sqlite --sink slack
```

### Managing Sinks
```bash
peepshow sinks list              # show active auto-sinks
peepshow sinks add <name[:arg]> # persist a named sink
peepshow sinks add-cmd <shell>   # persist a shell-command sink
peepshow sinks remove <n>        # drop by 1-based index
peepshow sinks clear
```

---

## Conditional Routing

Only fire sinks when conditions match:
```bash
peepshow ./video.mp4 --when director=Kubrick
peepshow ./video.mp4 --when path=/Volumes/Work/
peepshow ./video.mp4 --when extension=mp4,mov
peepshow ./video.mp4 --when filename='*vacation*'
```

---

## GPU / Hardware Acceleration

```bash
--gpu auto        # default — smart pick based on duration+resolution
--gpu off         # force CPU decoding
--gpu cuda        # NVIDIA
--gpu videotoolbox # macOS
--gpu vaapi       # Linux
--gpu d3d11va     # Windows

# Environment overrides
PEEPSHOW_GPU_MIN_SECONDS=30
PEEPSHOW_GPU_MIN_HEIGHT=1080
```

---

## Dedup + Adaptive Density

```bash
--dedup on       # perceptual hash dedup (default on)
--dedup auto     # only for fps fallback
--dedup off      # skip dedup

--adaptive on    # 2nd pass when motion is high + room under --max (default on)
--adaptive off   # skip adaptive
```

---

## Inspecting Runs

```bash
peepshow runs list              # show recent runs
peepshow runs show <runId>       # dump manifest.json
peepshow runs prune              # drop entries with missing outputDir
peepshow runs repair             # backfill missing LLM analysis
peepshow runs clear              # truncate index

# Re-render report.html
peepshow report <run-dir>
peepshow report annotate <dir>   # pipe LLM analysis → manifest.analysis

# Local web UI for run history
peepshow serve --port 3000
```

---

## Common Workflows

### QA Bug Reproduction
```bash
peepshow ./bug-repro.mov --strategy scene --max 12 --emit json
```

### CCTV Archive Search
```bash
peepshow ./cctv-2026-04-23.mp4 --strategy scene --threshold 0.18 --max 60 \
  --sink sqlite:./incidents.db --tag camera=front-door
```

### Video → LLM Analysis
```bash
peepshow ./demo.mp4 --max 30 --transcribe whisper-cpp --describe anthropic \
  --sink sqlite:./analysis.db
```

---

## Output Location

Runs are stored at `~/.peepshow/runs/` with:
- `manifest.json` — full metadata, frame paths, transcript
- `report.html` — self-contained frames grid + transcript + analysis
- Frame images in the run directory

---

## Supported Input Types

- Local file: `peepshow ./video.mp4`
- Remote URL: `peepshow https://example.com/video.mp4`
- Stdin: `peepshow - < video.mp4`
- Data URI: `peepshow data:video/mp4;base64,...`
- Animated images: GIF, APNG, animated WebP
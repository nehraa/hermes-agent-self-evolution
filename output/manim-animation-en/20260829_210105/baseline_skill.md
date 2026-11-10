---
category: software-development
name: manim-animation-en
description: "Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos."
required_tools:
  - name: manim
    install: "pip install manim"
  - name: ffmpeg
    install: "brew install ffmpeg (macOS) / apt install ffmpeg (Linux)"
    notes: "Must include libx264 encoder and libass (for subtitle burn-in)"
  - name: python3
    install: "Python 3.9+ required"
required_packages:
  - "manim"
  - "manim-voiceover[gtts]"
network_access:
  - service: "Google TTS (gTTS)"
    purpose: "Text-to-speech synthesis for voiceover narration"
    required: false
    notes: "Default TTS engine. Can be replaced with offline pyttsx3 if network is unavailable."
---

# Manim Animation: Animation + Voiceover + Subtitle Generator

**Author:** ericksun（孙自翔）

## Overview

This skill uses **Manim Community** to generate mathematical and educational animations, with **manim-voiceover** plugin integration for TTS voice narration and synchronized subtitles. All processing runs locally with no paid API required.

**Core Capabilities:**

| Feature | Description |
|---------|-------------|
| 🎬 Animation Generation | Create animations of math formulas, geometric shapes, charts, graphs, and diagrams |
| 🎙️ Voice Narration | Integrate TTS via manim-voiceover with automatic animation-voice synchronization |
| 📝 Dual Subtitle System | In-scene subtitles (Manim Text objects) + SRT external subtitles (ffmpeg burn-in) |
| 🔄 One-Click Pipeline | Describe requirements → Generate code → Render video → Burn subtitles |

**TTS Engine Options:**

| Engine | Quality | API Key Required | Offline |
|--------|---------|------------------|---------|
| gTTS | Good | No | No |
| pyttsx3 | Basic | No | Yes |
| Azure/OpenAI/ElevenLabs | High | Yes | No |

## Prerequisites

### Environment Check

Before first use, run the environment check script:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
This script verifies:
- ✅ Manim Community installation (`manim -version`)
- ✅ FFmpeg installation (`ffmpeg -version`)
- ✅ Required Python packages
- ✅ Network connectivity (for gTTS)

### Manual Installation

If automated check fails, install dependencies manually:

bash
# Install Manim and voiceover plugin
pip install manim manim-voiceover[gtts]

# Install FFmpeg (macOS)
brew install ffmpeg

# Install FFmpeg (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html
## Usage

### Basic Workflow

1. **Describe the animation** — Explain what you want to create (topic, visual elements, narration text)
2. **Generate code** — The skill creates a Manim Python script with voiceover integration
3. **Render video** — Execute `manim` command to generate the animation
4. **Burn subtitles** — FFmpeg embeds SRT subtitles into the final video

### Example Request

Create a video explaining the Pythagorean theorem with:
- Animation showing a right triangle with squares on each side
- Voice narration: "The Pythagorean theorem states that in a right triangle..."
- Subtitles in English
### Rendering Commands

bash
# Standard quality (faster)
manim -qm -i script_name.py SceneName

# High quality
manim -qh -i script_name.py SceneName

# Preview (low quality, fastest)
manim -ql script_name.py SceneName
## File Structure

{SKILL_DIR}/
├── scripts/
│   └── check_environment.py    # Environment verification
├── templates/
│   └── base_scene.py           # Base scene template with voiceover
└── SKILL.md                    # This file
## Troubleshooting

| Issue | Solution |
|-------|----------|
| `manim: command not found` | Reinstall: `pip install manim` |
| `ffmpeg not found` | Install FFmpeg and add to PATH |
| TTS not working | Check network or switch to `pyttsx3` |
| Subtitle burn-in fails | Ensure `libass` codec is enabled in FFmpeg |

## Configuration

### Custom TTS Engine

To use a different TTS engine, modify the import in generated scripts:

python
# For Azure TTS
pip install azure-cognitiveservices-speech
# Edit generated script to use azure-tts wrapper

# For ElevenLabs
pip install elevenlabs
# Edit generated script to use elevenlabs wrapper
### Subtitle Style

Subtitle appearance is controlled in the Manim scene via `Text` objects:

python
subtitle = Text(narration_text, font="Arial", size=0.3)
Modify these parameters in generated code to adjust font, size, and color.

## Notes

- **gTTS** is the default TTS engine and works out-of-the-box for most languages including Chinese, English, Spanish, French, German, Japanese, and Korean
- **FFmpeg** must support `libx264` (video) and `libass` (subtitles) codecs
- Generated SRT files are placed alongside the rendered video for external subtitle support
- Use `-i` flag with `manim` to generate output files instead of playing inline
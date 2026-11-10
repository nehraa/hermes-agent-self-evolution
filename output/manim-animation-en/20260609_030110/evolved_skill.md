---
category: software-development
description: "Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos."
name: manim-animation-en
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

This skill generates mathematical/educational animations with synchronized TTS voice narration and subtitles using Manim Community and the manim-voiceover plugin. All processing runs locally — no paid API required.

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Animation Generation** | Math formulas, geometric shapes, charts, graphs, and custom animations |
| **Voice Narration** | TTS via manim-voiceover with automatic animation-voice synchronization |
| **Subtitle System** | In-scene subtitles (Manim Text) + SRT external subtitles (ffmpeg burn-in) |
| **Pipeline** | Describe → Generate code → Render video → Burn subtitles |

### Supported TTS Engines

| Engine | Quality | Network Required | Setup |
|--------|---------|------------------|-------|
| **gTTS** (Recommended) | Good | Yes | API Key: None |
| **pyttsx3** (Fallback) | Basic | No | Offline capable |
| **Azure/OpenAI/ElevenLabs** | High | Yes | Paid API Key required |

## Prerequisites

### Environment Check

Run the environment check script before first use:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
The script verifies:
- ✅ Manim Community installation (`manim --version`)
- ✅ FFmpeg with libx264 and libass support
- ✅ Python version (3.9+)
- ✅ Required packages (manim, manim-voiceover)
- ✅ Network connectivity (for gTTS)

### Installation

bash
# Install core packages
pip install manim manim-voiceover[gtts]

# Install gTTS for voiceover
pip install gtts

# Install ffmpeg (if not present)
# macOS:
brew install ffmpeg
# Linux:
sudo apt install ffmpeg
## Usage

### Basic Workflow

1. **Describe the animation** — Explain what mathematical concept or scene you want
2. **Generate code** — The skill creates a Manim scene with voiceover integration
3. **Render video** — Run `manim` to generate the animation
4. **Burn subtitles** — FFmpeg embeds SRT subtitles into the final video

### Example: Simple Math Animation

python
from manim import *
from manim_voiceover import VoiceoverScene

class PythagoreanTheorem(VoiceoverScene):
    def construct(self):
        # Create scene elements
        triangle = Triangle().scale(2)
        
        with self.voiceover("In a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides."):
            self.play(Create(triangle))
            self.wait(1)
### Rendering Commands

bash
# Quick preview (low quality, faster)
manim -ql scene_name.py ClassName

# High quality output
manim -qh scene_name.py ClassName

# With subtitles burned in
ffmpeg -i output.mp4 -vf "ass=subtitle.ass" final_output.mp4
## Configuration Options

### TTS Voice Settings

python
# Configure voice language and speed
self.add_sound("narration.mp3", time_offset=0.5, gain=0)
### Subtitle Styling

python
# Custom subtitle appearance
Text("Subtitle text", font="Arial", font_size=24, color=WHITE)
### Video Quality Settings

| Flag | Resolution | Use Case |
|------|------------|----------|
| `-ql` | 854x480 | Preview/testing |
| `-qm` | 1280x720 | Standard quality |
| `-qh` | 1920x1080 | High quality output |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| FFmpeg not found | Install via `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux) |
| TTS fails | Check network or switch to `pyttsx3` fallback engine |
| Subtitle sync issues | Adjust `time_offset` in voiceover settings |
| Import errors | Verify `manim-voiceover` is installed with `pip list` |

## File Structure

project/
├── scenes/
│   └── animation_scene.py    # Manim scene with voiceover
├── output/
│   ├── media/                 # Rendered frames/videos
│   └── subtitles.srt          # Subtitle file
└── scripts/
    └── check_environment.py  # Environment verification
## Best Practices

1. **Script your narration first** — Write the voiceover text before building animations
2. **Match timing** — Use `self.wait()` to sync animations with voiceover duration
3. **Test in low quality** — Use `-ql` flag for faster iteration during development
4. **Batch rendering** — For multiple scenes, render at lower quality first, then high quality for final output
5. **Subtitle sync** — Generate SRT files alongside video for accessibility

## Notes

- gTTS supports Chinese and English by default
- For higher quality voice, consider Azure TTS or ElevenLabs (requires API keys)
- Subtitle burn-in requires `libass` support in FFmpeg
- Animation complexity affects rendering time significantly
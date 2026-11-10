---
category: software-development
description: 'Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos.'
name: manim-animation-en
---

# Manim Animation: Animation + Voiceover + Subtitle Generator

**Author:** ericksun（孙自翔）

## Overview

This skill generates mathematical and educational animations using Manim Community, with integrated TTS voice narration and synchronized subtitles via the manim-voiceover plugin. All processing runs locally—no paid API required.

**Core Capabilities:**
- 🎬 **Animation Generation**: Create animations of math formulas, geometric shapes, charts, graphs, and more
- 🎙️ **Voice Narration**: TTS via manim-voiceover plugin with automatic animation-voice synchronization
- 📝 **Subtitle System**: In-scene subtitles (Manim Text) + SRT external subtitles (ffmpeg burn-in)
- 🔄 **One-Click Pipeline**: Describe requirements → Generate code → Render video → Burn subtitles

## Supported TTS Engines

| Engine | Quality | API Key Required | Network Required | Notes |
|--------|---------|------------------|------------------|-------|
| **gTTS** (Recommended) | Medium | No | Yes | Free, supports Chinese, zero setup |
| **pyttsx3** (Fallback) | Low-Medium | No | No | Offline, local voice synthesis |
| **Azure TTS** | High | Yes | Yes | Requires Azure subscription |
| **OpenAI TTS** | High | Yes | Yes | Requires OpenAI API key |
| **ElevenLabs** | High | Yes | Yes | Requires ElevenLabs subscription |

## Prerequisites

### Environment Check

Before first use, run the environment check script:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
The script verifies:
- ✅ Manim Community installation
- ✅ Python 3.9+ version
- ✅ ffmpeg installation with libx264 and libass support
- ✅ Required Python packages (manim, manim-voiceover)
- ✅ TTS engine availability

### Manual Installation

If the check script reports issues, install dependencies manually:

bash
# Core packages
pip install manim manim-voiceover[gtts]

# For offline TTS fallback
pip install pyttsx3

# ffmpeg (macOS)
brew install ffmpeg

# ffmpeg (Linux)
sudo apt install ffmpeg
**ffmpeg requirements:** Must include libx264 encoder and libass (for subtitle burn-in).

## Usage

### Basic Workflow

1. **User provides**: Animation description, narration text, optional style preferences
2. **Generate**: Create complete Python script with Manim scenes + voiceover + subtitles
3. **Render**: Execute script to produce video with embedded audio and subtitles
4. **Burn subtitles**: Use ffmpeg to burn SRT subtitles into video for universal playback

### Code Template

python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MathAnimation(Scene):
    def construct(self):
        # Initialize TTS service
        self.set_speech_service(GTTSService())

        # Create animation
        circle = Circle()
        square = Square()

        with self.voiceover(text="This circle transforms into a square."):
            self.play(Create(circle))
            self.play(Transform(circle, square))

        # Add in-scene subtitle
        subtitle = Text("Circle → Square", font_size=24)
        subtitle.to_edge(DOWN)
        self.add(subtitle)
### Rendering Commands

bash
# Preview (low quality, fast)
manim -ql scene.py MathAnimation

# Standard quality (720p)
manim -qm scene.py MathAnimation

# High quality (1080p)
manim -qh scene.py MathAnimation

# Ultra quality (4K)
manim -qk scene.py MathAnimation
### Subtitle Burn-In

After rendering, burn SRT subtitles into the video:

bash
ffmpeg -i output.mp4 -vf "subtitles=output.srt" -c:a copy final_video.mp4
## Configuration Options

### TTS Language

python
self.set_speech_service(GTTSService(lang="en"))  # English
self.set_speech_service(GTTSService(lang="zh-CN"))  # Chinese
### Animation Quality

| Flag | Resolution | Speed | Use Case |
|------|------------|-------|----------|
| `-ql` | 854×480 | Fastest | Preview/Testing |
| `-qm` | 1280×720 | Medium | Standard output |
| `-qh` | 1920×1080 | Slow | Final presentation |
| `-qk` | 3840×2160 | Slowest | High-res archives |

### Custom Voice Settings

python
from manim_voiceover.services.azure import AzureService

self.set_speech_service(AzureService(
    voice="en-US-JennyNeural",
    pitch=0,
    rate=1.0
))
## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: manim_voiceover` | Package not installed | `pip install manim-voiceover[gtts]` |
| `ffmpeg not found` | ffmpeg not in PATH | Install ffmpeg and add to PATH |
| `No voice service configured` | TTS service not set | Call `self.set_speech_service()` in `construct()` |
| `gTTS network error` | No internet connection | Switch to pyttsx3 for offline TTS |

## Best Practices

1. **Write narration first**: Draft your script before animating to ensure timing sync
2. **Keep scenes short**: Limit each scene to 10-30 seconds for better pacing
3. **Test with `-ql` first**: Preview quickly before high-quality renders
4. **Use consistent fonts**: Set `font_size` and `font` parameters explicitly
5. **Generate SRT alongside video**: Always produce subtitles for accessibility

## Network Requirements

- **Required**: Internet for gTTS (default), Azure TTS, OpenAI TTS, ElevenLabs
- **Not required**: pyttsx3 fallback works completely offline

## Files Structure

{SKILL_DIR}/
├── scripts/
│   └── check_environment.py    # Environment verification script
├── templates/
│   └── basic_scene.py         # Starter template
└── SKILL.md
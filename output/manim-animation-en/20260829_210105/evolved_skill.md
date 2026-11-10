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

**Author:** ericsun (孙自翔)

## Overview

This skill generates **mathematical and educational animations** with **synchronized TTS voice narration** and **dual subtitle system** using Manim Community Edition + manim-voiceover. All processing runs locally with no paid API required.

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🎬 Animation Generation | Math formulas, geometric shapes, charts, graphs, diagrams |
| 🎙️ Voice Narration | TTS via manim-voiceover with automatic animation-voice sync |
| 📝 Dual Subtitle System | In-scene subtitles (Manim Text) + SRT external subtitles (ffmpeg burn-in) |
| 🔄 One-Click Pipeline | Describe requirements → Generate code → Render video → Burn subtitles |

### TTS Engine Options

| Engine | Quality | API Key Required | Offline |
|--------|---------|------------------|---------|
| gTTS | Good | No | No |
| pyttsx3 | Basic | No | Yes |
| Azure/OpenAI/ElevenLabs | High | Yes | No |

## Prerequisites

### 1. Environment Check

Before first use, run the environment verification:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
This script verifies:
- ✅ Manim Community installation (`manim -version`)
- ✅ FFmpeg installation with required codecs
- ✅ Python version (3.9+)
- ✅ Required Python packages

### 2. Install Dependencies

bash
# Core packages
pip install manim manim-voiceover[gtts]

# Optional: offline TTS fallback
pip install pyttsx3
### 3. FFmpeg Configuration

Ensure FFmpeg includes required libraries:

bash
# Verify FFmpeg installation
ffmpeg -version | grep libx264

# If missing on Ubuntu/Debian:
sudo apt install ffmpeg

# If missing on macOS:
brew install ffmpeg
## Workflow

### Step 1: Analyze Requirements

Identify the user's request type:

- **Pure animation**: No voiceover needed
- **Narration required**: TTS voiceover with subtitles
- **Subtitle-only**: Add subtitles to existing audio/animation
- **Full production**: Animation + voice + subtitles + burn-in

### Step 2: Generate Manim Code

Create a Python script with the following structure:

python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class AnimationScene(VoiceoverScene):
    def construct(self):
        # Set TTS service
        self.set_speech_service(GTTSService())

        # Your animation content here
        circle = Circle()
        square = Square()

        # Add narration with synchronized animation
        with self.voiceover(text="This is the narration text."):
            self.play(Create(circle))
            self.play(Transform(circle, square))
### Step 3: Generate Subtitle Files

The manim-voiceover plugin automatically generates:
- **SRT file**: External subtitles for video players
- **In-scene Text objects**: Burned-in subtitles

### Step 4: Render Video

bash
# Standard quality (faster)
manim -ql -i script.py SceneName

# High quality (slower)
manim -qm script.py SceneName

# With transparent background (for overlays)
manim -ql -t script.py SceneName
### Step 5: Burn Subtitles (if needed)

bash
ffmpeg -i animation.mp4 -i subtitles.srt \
  -c:v libx264 -c:a copy -c:s ass \
  -metadata:s:s:0 language=eng \
  output_with_subtitles.mp4
## Scene Template

python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class EducationalScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        # Title
        title = Text("Mathematical Concept").scale(1.5)
        
        with self.voiceover(text="Welcome to this lesson about mathematical concepts."):
            self.play(Write(title))
            self.wait(0.5)

        # Main content
        formula = MathTex(r"E = mc^2").scale(2)
        
        with self.voiceover(text="Here we see Einstein's famous equation."):
            self.play(Write(formula))
            self.wait(0.5)

        # Cleanup
        with self.voiceover(text="That's all for this demonstration."):
            self.play(FadeOut(title), FadeOut(formula))
## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `manim: command not found` | Reinstall: `pip install manim` |
| FFmpeg codec errors | Install ffmpeg with all codecs: `brew install ffmpeg --with-libass` |
| TTS fails (network) | Switch to offline: `pyttsx3` service |
| Subtitle sync mismatch | Adjust `time` parameter in `voiceover()` |
| Low quality output | Use `-qm` flag for medium quality, `-qh` for high |

## Output Files

After rendering, the following files are generated in `./media/videos/`:

| File | Description |
|------|-------------|
| `{quality}/{scene_name}.mp4` | Main animation video |
| `{scene_name}.srt` | External subtitle file |
| `{scene_name}_with_speech.mp4` | Video with in-scene TTS visualization |

## Best Practices

1. **Narration timing**: Keep sentences under 15 seconds for natural pacing
2. **Animation sync**: Use `self.wait()` strategically to match narration
3. **Subtitle length**: Limit to 2 lines, max 42 characters per line
4. **Quality vs speed**: Use `-ql` for preview, `-qm` for final output
5. **Backup TTS**: Always provide offline fallback for reliability
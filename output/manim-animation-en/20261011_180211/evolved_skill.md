---
category: software-development
name: manim-animation-en
description: "Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos."
required_tools:
  - name: manim
    install: "pip install manim"
    version: "0.18.0+"
  - name: ffmpeg
    install: "brew install ffmpeg (macOS) / apt install ffmpeg (Linux) / choco install ffmpeg (Windows)"
    notes: "Must include libx264 encoder and libass for subtitle burn-in"
  - name: python3
    install: "Python 3.9+ required"
required_packages:
  - manim
  - manim-voiceover[gtts]
network_access:
  - service: "Google TTS (gTTS)"
    purpose: "Text-to-speech synthesis for voiceover narration"
    required: false
    notes: "Default TTS engine. Can be replaced with offline pyttsx3 if network is unavailable."
  - service: "Internet Connection"
    purpose: "Required only for gTTS; all other engines work offline"
    required: false
---

# Manim Animation: Voiceover + Subtitle Generator

**Author:** ericksun（孙自翔）

## Overview

This skill generates mathematical and educational animations with synchronized TTS voice narration and dual-subtitle output using **Manim Community** and the **manim-voiceover** plugin. Everything runs locally with no paid APIs required.

## Core Features

| Feature | Description |
|---------|-------------|
| 🎬 **Animation Engine** | Math formulas, geometric shapes, charts, graphs, diagrams, and custom scenes |
| 🎙️ **Voice Narration** | TTS via manim-voiceover with automatic lip-sync timing |
| 📝 **Dual Subtitle System** | In-scene text subtitles + SRT external subtitles (burned in via ffmpeg) |
| 🔄 **One-Click Pipeline** | Describe → Generate → Render → Subtitle → Output |

## TTS Engine Options

| Engine | Quality | API Key | Offline | Recommended For |
|--------|---------|---------|---------|-----------------|
| **gTTS** (default) | Good | No | No | Quick previews, no setup |
| **pyttsx3** | Basic | No | Yes | Offline environments |
| **Azure TTS** | High | Yes | No | Professional production |
| **OpenAI TTS** | High | Yes | No | Natural-sounding narration |
| **ElevenLabs** | Premium | Yes | No | Highest quality voice cloning |

## Prerequisites

### 1. Environment Check

Run the environment verification script before first use:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
This script verifies:
- ✅ Manim Community installation (`manim -version`)
- ✅ FFmpeg installation with required codecs
- ✅ Python version (3.9+)
- ✅ Required Python packages

### 2. Manual Verification

If the script is unavailable, verify manually:

bash
# Check Manim
manim --version

# Check FFmpeg with libx264 and libass
ffmpeg -version
ffmpeg -encoders | grep libx264
ffmpeg -formats | grep ass

# Install missing dependencies if needed
pip install manim manim-voiceover[gtts]
### 3. TTS Engine Setup

**For gTTS (default):**
bash
pip install manim-voiceover[gtts]
**For pyttsx3 (offline):**
bash
pip install manim-voiceover pyttsx3
**For cloud TTS engines:** Follow the respective service documentation for API key setup.

## Workflow

┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Describe Requirements                                  │
│  - Scene type (formula, graph, geometry, diagram)               │
│  - Narration text                                               │
│  - Animation duration and transitions                           │
│  - Subtitle preferences                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Generate Manim Code                                    │
│  - Create Scene class with Manim objects                        │
│  - Integrate manim-voiceover for TTS                            │
│  - Add Text objects for in-scene subtitles                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: Render Animation                                       │
│  manim -ql -i SceneName.py SceneName                            │
│  (ql = quick low quality for preview)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: Generate SRT Subtitles                                 │
│  - manim-voiceover auto-generates .srt files                     │
│  - Located in same directory as output                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: Burn Subtitles (Optional)                              │
│  ffmpeg -i SceneName.mp4 -vf "ass=subs.ass" output.mp4          │
└─────────────────────────────────────────────────────────────────┘
## Code Structure

### Basic Scene Template

python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MyScene(VoiceoverScene):
    def construct(self):
        # Set TTS engine
        self.set_speech_service(GTTSService())

        # Create animation objects
        circle = Circle()
        formula = MathTex(r"E = mc^2")

        # Add narration with automatic sync
        with self.voiceover(text="This is the famous Einstein equation."):
            # Animation runs in sync with narration
            self.play(Create(circle))
            self.play(Write(formula))
### Advanced Scene with Subtitles

python
from manim import *
from manim_voiceover import VoiceoverScene

class MathAnimation(VoiceoverScene):
    def construct(self):
        # Title
        title = Text("Introduction to Calculus").scale(1.2)

        # Narration block 1
        with self.voiceover(text="Let's explore the fundamental theorem of calculus.") as tracker:
            self.play(Write(title))
            self.wait(tracker.duration - 1)

        # Clear title
        self.play(FadeOut(title))

        # Formula animation
        formula = MathTex(r"\int_a^b f'(x)\,dx = f(b) - f(a)")
        formula.set_color_by_tex("f'(x)", BLUE)

        # Narration block 2
        with self.voiceover(text="The derivative and integral are inverse operations.") as tracker:
            self.play(Write(formula))

        # Add in-scene subtitle (bottom of screen)
        subtitle = Text("Fundamental Theorem of Calculus", font_size=24)
        subtitle.to_edge(DOWN)
        self.add(subtitle)

        self.wait(2)
## Rendering Commands

| Purpose | Command | Output |
|---------|---------|--------|
| **Preview (Low Quality)** | `manim -ql SceneName.py MyScene` | Fast preview |
| **Standard (720p)** | `manim -qm SceneName.py MyScene` | Balanced quality |
| **High Quality (1080p)** | `manim -qh SceneName.py MyScene` | Presentation quality |
| **4K Quality** | `manim -qk SceneName.py MyScene` | Maximum quality |

### Render Flags

| Flag | Description |
|------|-------------|
| `-i` | Save intermediate files |
| `-s` | Skip last few seconds |
| `-w` | Wait for user input after render |
| `-g` | Save last frame as PNG |

## Subtitle Generation

### Automatic SRT Generation

manim-voiceover automatically generates `.srt` subtitle files in the same directory as rendered output:

media/
└── videos/
    └── SceneName/
        └── 480p15/
            ├── SceneName.mp4
            └── SceneName.mp4.srt
### Burning Subtitles into Video

**Method 1: Direct burn-in with ffmpeg**

bash
ffmpeg -i input.mp4 -vf "subtitles=input.srt" output.mp4
**Method 2: Using ASS format**

bash
ffmpeg -i input.mp4 -vf "ass=subtitle.ass" output.mp4
**Method 3: With styling (custom ASS file)**

bash
ffmpeg -i input.mp4 -vf "ass=styled_subs.ass" -c:a copy output.mp4
## Configuration Options

### manim.cfg Settings

ini
[CLI]
quality = l  # l, m, h, p (low to 4k)
output_file = /path/to/output
save_last_frame = False
save_png_format = PNG

[video]
frame_rate = 30
resolution = 1920x1080

[output]
video_dir = ./media
text_dir = ./media
### TTS Service Configuration

python
# gTTS (default)
self.set_speech_service(GTTSService(
    speech_rate=1.15,  # Speed multiplier
    pitch=0           # Pitch adjustment
))

# pyttsx3 (offline)
self.set_speech_service(Pyttsx3Service(
    rate=150,
    volume=0.9,
    voice_id="english"  # Platform-dependent
))

# Custom audio file
self.set_speech_service(SpeechServiceFromAudioFile(
    audio_path="/path/to/narration.mp3"
))
## Common Patterns

### Pattern 1: Multi-Step Explanation

python
def construct(self):
    self.set_speech_service(GTTSService())

    # Step 1
    step1_text = "First, we define the function f of x."
    with self.voiceover(text=step1_text):
        func = MathTex(r"f(x) = x^2 + 2x + 1")
        self.play(Write(func))

    # Step 2
    step2_text = "Next, we find its derivative."
    with self.voiceover(text=step2_text):
        derivative = MathTex(r"f'(x) = 2x + 2")
        derivative.next_to(func, DOWN)
        self.play(Write(derivative))

    # Step 3
    step3_text = "Finally, we evaluate at x equals 1."
    with self.voiceover(text=step3_text):
        result = MathTex(r"f'(1) = 4")
        result.next_to(derivative, DOWN)
        self.play(Write(result))
### Pattern 2: Graph Animation with Voice

python
class GraphVoiceover(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        # Setup axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 8, 2],
            x_length=6,
            y_length=4
        )

        # Graph function
        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x)")

        with self.voiceover(text="Consider the parabola y equals x squared."):
            self.play(Create(axes))
            self.play(Create(graph))
            self.play(Write(graph_label))
### Pattern 3: Geometric Proof Narration

python
class TriangleProof(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        # Create triangle
        triangle = Polygon(
            [-2, -1, 0],
            [2, -1, 0],
            [0, 2, 0]
        )

        with self.voiceover(text="Let ABC be a triangle with sides of equal length."):
            self.play(Create(triangle))

        # Mark vertices
        vertices = triangle.get_vertices()
        labels = [
            Text("A", font_size=20).move_to(vertices[0] + DOWN * 0.4),
            Text("B", font_size=20).move_to(vertices[1] + DOWN * 0.4),
            Text("C", font_size=20).move_to(vertices[2] + UP * 0.4),
        ]

        with self.voiceover(text="We will prove that all angles are equal."):
            for label in labels:
                self.play(Write(label), run_time=0.5)

        # Add altitude
        altitude = Line(vertices[0], [0, -1, 0], color=RED)

        with self.voiceover(text="Draw a perpendicular from vertex A to side BC."):
            self.play(Create(altitude))
## Troubleshooting

### Issue: "manim command not found"

bash
# Reinstall manim
pip uninstall manim
pip install manim

# Verify installation
python -m manim --version
### Issue: TTS audio not generated

bash
# Check manim-voiceover installation
pip show manim-voiceover

# Reinstall with audio dependencies
pip install manim-voiceover[gtts]
### Issue: FFmpeg subtitle encoding errors

bash
# Reinstall ffmpeg with full codec support
# macOS
brew reinstall ffmpeg --with-libass

# Ubuntu/Debian
sudo apt install ffmpeg libass-dev

# Verify ASS support
ffmpeg -formats | grep ass
### Issue: SRT file not created

- Ensure `manim-voiceover` is properly installed
- Check that `tracker.duration` is being used correctly
- Verify output directory is writable

### Issue: Audio-video sync problems

python
# Use tracker to control timing
with self.voiceover(text="Your narration here.") as tracker:
    self.play(Create(object))
    self.wait(tracker.duration)  # Wait for full narration
### Issue: Slow render times

- Use `-ql` for preview/testing
- Consider pre-rendering static elements
- Use `run_time` parameter to control animation speed

## Output Structure

media/
├── images/
│   └── MyScene/           # Static frame outputs
├── texts/
│   └── MyScene/           # LaTeX and text outputs
└── videos/
    └── MyScene/
        ├── 480p15/        # Low quality output
        │   ├── SceneName.mp4
        │   └── SceneName.mp4.srt
        ├── 720p30/        # Medium quality output
        └── 1080p60/       # High quality output
## Best Practices

1. **Script narration first** — Write your full narration before animating
2. **Use `tracker.duration`** — Ensure animations match voice length
3. **Preview with `-ql`** — Test quickly before high-quality renders
4. **Generate SRT files** — Create external subtitles for accessibility
5. **Test TTS settings** — Adjust speech rate and pitch for clarity
6. **Version control scenes** — Keep your `.py` files in Git

## Example Prompts for This Skill

- "Create a manim animation explaining the Pythagorean theorem with voice narration"
- "Generate an animated video about derivatives with subtitles"
- "Make a math animation with voiceover for the quadratic formula"
- "Create an educational animation about vectors with TTS narration"
- "Generate a narrated animation showing Taylor series expansion"
- "Make a physics animation about wave interference with voiceover"
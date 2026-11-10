---
category: software-development
description: 'Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover.'
name: manim-animation-en
required_tools:
  - name: manim
    install: pip install manim
  - name: ffmpeg
    install: "macOS: brew install ffmpeg | Linux: apt install ffmpeg"
    notes: "Must include libx264 encoder and libass for subtitle burn-in"
  - name: python3
    install: Python 3.9+ required
required_packages:
  - manim
  - manim-voiceover[gtts]
network_access:
  - service: Google TTS (gTTS)
    purpose: Text-to-speech synthesis for voiceover narration
    required: false
    notes: Default TTS engine. Can be replaced with offline pyttsx3 if network is unavailable.
---

# Manim Animation Generator

**Author:** ericksun (孙自翔)

## Overview

Generate mathematical/educational animations with synchronized voice narration and subtitles using Manim Community and the manim-voiceover plugin. Everything runs locally — no paid APIs required.

**Core Capabilities:**
- **Animation Generation** — Math formulas, geometric shapes, charts, and visual explanations
- **Voice Narration** — TTS via manim-voiceover with automatic animation-voice sync
- **Subtitle System** — In-scene subtitles (Manim Text) + SRT burn-in via ffmpeg
- **One-Click Pipeline** — Describe → Generate code → Render → Burn subtitles

**Supported TTS Engines:**
| Engine | Quality | API Key Required | Network Required |
|--------|---------|------------------|------------------|
| gTTS | Good | No | Yes |
| pyttsx3 | Fair | No | No |
| Azure/OpenAI/ElevenLabs | Excellent | Yes | Yes |

---

## Prerequisites

### Environment Check

Before first use, run the environment check script:

bash
python3 {SKILL_DIR}/scripts/check_environment.py
This verifies:
- Manim Community installation (`manim -h`)
- FFmpeg installation (`ffmpeg -version`)
- Python version (3.9+)
- Required Python packages

### Manual Installation (if needed)

bash
# Core packages
pip install manim manim-voiceover[gtts]

# Optional offline TTS fallback
pip install pyttsx3
---

## Usage

### 1. Describe Your Animation

Provide a clear description of what you want:

- **Topic**: What mathematical concept should be animated?
- **Narrator Text**: What should the voiceover say?
- **Visual Elements**: What shapes, equations, or graphs to display?
- **Duration**: Approximate length of the video

### 2. Generate and Execute

The skill will:

1. Create a Manim scene with your specifications
2. Generate TTS audio from narrator text
3. Sync audio with animation frames
4. Render the final video with burned-in subtitles

bash
# Example: Render a scene
manim -qm scene_name.py SceneClassName
### 3. Output Files

| File | Description |
|------|-------------|
| `media/videos/*.mp4` | Final video with subtitles |
| `media/videos/*.wav` | Generated voiceover audio |
| `media/subtitles/*.srt` | Subtitle file (if generated) |

---

## Code Structure

python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MathAnimation(Scene, VoiceoverScene):
    def construct(self):
        # Set TTS service
        self.set_speech_service(GTTSService())

        # Create your animation
        with self.voiceover(text="Your narration here"):
            # Animation code
            formula = MathTex(r"E = mc^2")
            self.play(Write(formula))
---

## Configuration Options

### Quality Presets

| Flag | Purpose | Use Case |
|------|---------|----------|
| `-qm` | Medium quality | Preview/testing |
| `-ql` | Low quality | Draft review |
| `-qh` | High quality | Final output |
| `-p` | Preview in player | Interactive viewing |

### Customizing TTS

python
# Use offline TTS (no network)
from manim_voiceover.services.pyttsx3 import Pyttsx3Service
self.set_speech_service(Pyttsx3Service())

# Use custom TTS with API key
from manim_voiceover.services.azure import AzureService
self.set_speech_service(AzureService(api_key="your-key"))
### Subtitle Styling

python
# Configure subtitle appearance
self.renderer.camera.background_color = WHITE
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No audio output | Ensure manim-voiceover installed with gTTS: `pip install manim-voiceover[gtts]` |
| FFmpeg not found | Reinstall FFmpeg with required codecs: `brew install ffmpeg` (macOS) |
| Subtitle burn-in fails | Verify libass is included: `ffmpeg -encoders | grep ass` |
| Slow rendering | Use `-ql` flag for testing, `-qm` for preview |
| TTS fails (no network) | Switch to pyttsx3: `pip install pyttsx3` |

---

## Examples

### Example 1: Pythagorean Theorem

User: Create an animation explaining the Pythagorean theorem with voiceover
python
class PythagoreanProof(Scene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        
        title = Text("Pythagorean Theorem").scale(1.2)
        
        with self.voiceover(text="The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides."):
            self.play(Write(title))
            self.wait(1)
            
            # Draw right triangle
            triangle = Polygon(
                ORIGIN, 3*RIGHT, 2*UP, 
                color=BLUE, fill_opacity=0.3
            )
            self.play(Create(triangle))
            
            # Show equation
            equation = MathTex("a^2 + b^2 = c^2")
            equation.next_to(triangle, DOWN)
            self.play(Write(equation))
### Example 2: Function Graph

User: Show the sine wave animation with narration explaining periodic functions
---

## Best Practices

1. **Write clear narrator text** — TTS works best with complete sentences
2. **Time your content** — Match animation duration to narration length
3. **Use appropriate quality flags** — `-ql` for testing, `-qh` for final render
4. **Test with preview** — Use `-p` to verify timing before full render
5. **Check dependencies first** — Run environment check before first use

---

## Dependencies Summary

yaml
System:
  - Python: "3.9+"
  - FFmpeg: "with libx264 and libass"

Python Packages:
  - manim: "Main animation library"
  - manim-voiceover: "TTS sync plugin"
  - gtts: "Google TTS (default, requires internet)"

Optional:
  - pyttsx3: "Offline TTS fallback"
  - azure/openai/elevenlabs: "Premium TTS options"
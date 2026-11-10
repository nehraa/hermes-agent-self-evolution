---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

Interface for interacting with Minimax's music AI APIs: lyrics generation, music generation, and music cover (style transfer).

All endpoints require the **Minimax API key** stored in Hermes memory under `Minimax API key`.

**Base Endpoint**: `https://api.minimax.io/v1`

---

## 1. Lyrics Generation

Generate structured song lyrics from a descriptive prompt.

### Command

bash
minimax-music lyrics "<prompt>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `prompt` | Yes | Description of the song theme, mood, or subject |
| `--style-tags` | No | Comma-separated style tags (e.g., "Pop, Summer, Romantic") |
| `--title` | No | Song title (required when using `--edit`) |
| `--edit` | No | Edit or continue existing lyrics (requires `--title` and context) |

### Examples

Generate lyrics for a pop song:
bash
minimax-music lyrics "A cheerful love song about a summer day at the beach" --style-tags "Pop, Summer Vibe, Romance, Lighthearted, Beach Pop"
Edit existing lyrics:
bash
minimax-music lyrics "Make the chorus more upbeat" --title "Sunny Day" --edit
### Endpoint

POST https://api.minimax.io/v1/lyrics_generation
---

## 2. Music Generation

Generate a song (with vocals) or instrumental music from lyrics and a style prompt.

### Command

bash
minimax-music music [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--lyrics` | No* | Song lyrics (supports markup: `[verse]`, `[chorus]`, `[bridge]`, etc.) |
| `--prompt` | Yes | Style description (genre, mood, BPM, key, instruments, vocal type) |
| `--model` | No | Model version (default: `music-02`) |
| `--instrumental` | No | Generate instrumental only (no vocals) |
| `--auto-lyrics` | No | Auto-generate lyrics from prompt when `--lyrics` is empty (requires `music-2.6` or `music-2.6-free`) |

*Lyrics are optional when using `--auto-lyrics` with a supported model.

### Examples

Generate a song with lyrics and style prompt:
bash
minimax-music music \
  --lyrics "[verse]\nStreetlights flicker, the night breeze sighs\n[chorus]\nPushing the wooden door, the aroma spreads" \
  --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
Generate instrumental music:
bash
minimax-music music --prompt "E minor, 90 BPM, acoustic guitar ballad" --instrumental
Auto-generate lyrics from style prompt (requires `music-2.6` or `music-2.6-free`):
bash
minimax-music music --prompt "Upbeat summer pop with synth, female vocal" --auto-lyrics
### Endpoint

POST https://api.minimax.io/v1/music_generation
---

## 3. Music Cover

Generate a cover version of a reference audio file with a target style.

### Command

bash
minimax-music cover "<audio_path>" "<style_description>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `audio_path` | Yes | Path to the reference audio file |
| `style_description` | Yes | Description of target style (genre, mood, instruments) |
| `--model` | No | Model version (default: `music-01`) |

### Examples

Convert a song to acoustic style:
bash
minimax-music cover "path/to/song.mp3" "Acoustic cover, fingerpicking guitar, soft vocal"
Transform to synthwave:
bash
minimax-music cover "input.wav" "Synthwave, 80s retro, electronic drums, dreamy pads"
### Endpoint

POST https://api.minimax.io/v1/music_cover
---

## Configuration

| Setting | Source | Value |
|---------|--------|-------|
| API Key | Hermes memory | `Minimax API key` |
| Base URL | — | `https://api.minimax.io/v1` |

### Required Memory Keys

- `Minimax API key` — Your Minimax API authentication key

---

## Notes

- **Lyrics Markup**: Use `[verse]`, `[chorus]`, `[bridge]`, `[pre-chorus]`, `[intro]`, `[outro]` tags to structure lyrics.
- **Style Prompts**: Include key, BPM, genre, instrument description, and vocal type for best results.
- **Auto-Lyrics**: Only available with `music-2.6` or `music-2.6-free` models. Omit `--lyrics` when using this feature.
- **File Formats**: Music Cover accepts common audio formats (MP3, WAV, M4A, FLAC).
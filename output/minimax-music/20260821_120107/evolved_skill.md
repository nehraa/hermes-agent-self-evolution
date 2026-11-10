---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

This skill provides commands to interact with Minimax's music AI APIs for lyrics generation, music generation, and music cover (style transfer).

## Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **API Key** | `Minimax API key` | Retrieved from Hermes memory |
| **Base URL** | `https://api.minimax.io/v1` | All endpoints use this base |

---

## 1. Lyrics Generation

Generate structured song lyrics from a text prompt.

**Command:**
bash
minimax-music lyrics "<prompt>" [options]
**Example:**
bash
minimax-music lyrics "A heartfelt love song about two people reuniting after years apart" --style-tags "Pop, Emotional, Slow Tempo, Anthemic"
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `prompt` | Yes | Description of the song's theme, mood, or story |
| `--style-tags` | No | Comma-separated style tags (e.g., "Pop, Acoustic, Melancholic") |
| `--title` | No | Song title to preserve when editing existing lyrics |
| `--edit` | No | Edit or continue existing lyrics (requires `--title` and prior context) |

**Endpoint:** `POST /lyrics_generation`

---

## 2. Music Generation

Generate a complete song with vocals or instrumental-only tracks.

**Command:**
bash
minimax-music music [options]
### Examples

**Song with custom lyrics and style:**
bash
minimax-music music \
  --lyrics "[verse]\nStreetlights flicker, the night breeze sighs\n[chorus]\nPushing the wooden door, the aroma spreads" \
  --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
**Instrumental track:**
bash
minimax-music music --prompt "Cinematic, 120 BPM, orchestral, epic climax" --instrumental
**Auto-generated lyrics from prompt:**
bash
minimax-music music --prompt "Upbeat summer pop song about road trips" --auto-lyrics
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--lyrics` | No* | Song lyrics with section markers (`[verse]`, `[chorus]`, etc.) |
| `--prompt` | Yes | Musical style description (key, BPM, instruments, vocals, mood) |
| `--model` | No | Model variant: `music-2.6` or `music-2.6-free` (default: auto) |
| `--instrumental` | No | Generate instrumental only (no vocals) |
| `--auto-lyrics` | No | Auto-generate lyrics when `--lyrics` is empty (requires `music-2.6` or `music-2.6-free`) |

*Either `--lyrics` or `--auto-lyrics` is required.

**Endpoint:** `POST /music_generation`

---

## 3. Music Cover (Style Transfer)

Generate a cover version of an audio file in a different musical style.

**Command:**
bash
minimax-music cover <audio_file> [options]
**Example:**
bash
minimax-music cover /path/to/song.mp3 --style "Jazz, smooth saxophone, lounge vibe"
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `audio_file` | Yes | Path to the reference audio file |
| `--style` | Yes | Description of target style (instruments, genre, mood) |

**Endpoint:** `POST /music_cover`

---

## Notes

- All endpoints require a valid Minimax API key stored in Hermes memory under `Minimax API key`.
- For `music-2.6-free`, generation may be queued with lower priority.
- Supported audio formats for cover: MP3, WAV, M4A, FLAC.
- Response times vary; long-form generations may take 1-3 minutes.
---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

This skill provides commands to interact with Minimax's music AI APIs for lyrics generation, music generation, and music cover (style transfer).

## Configuration

All endpoints require the Minimax API key stored in Hermes memory.

| Setting | Value |
|---------|-------|
| **API Key** | Retrieved from memory (`Minimax API key`) |
| **Base Endpoint** | `https://api.minimax.io/v1` |

---

## 1. Lyrics Generation

Generate structured song lyrics from a descriptive prompt.

### Command

bash
minimax-music lyrics "<prompt>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--style-tags` | No | Comma-separated tags to guide the style (e.g., "Pop, Summer Vibe, Romance") |
| `--edit` | No | Edit or continue existing lyrics (requires `--title` and lyrics context) |
| `--title` | No | Song title (required when using `--edit`) |

### Examples

**Generate new lyrics:**
bash
minimax-music lyrics "A cheerful love song about a summer day at the beach" \
  --style-tags "Pop, Summer Vibe, Romance, Lighthearted, Beach Pop"
**Edit existing lyrics:**
bash
minimax-music lyrics "Add a bridge after the second chorus" \
  --edit --title "Summer Love"
### Endpoint

POST https://api.minimax.io/v1/lyrics_generation
---

## 2. Music Generation

Generate a song with vocals or create instrumental music.

### Command

bash
minimax-music music [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--lyrics` | No* | Song lyrics with structure markers ([verse], [chorus], etc.) |
| `--prompt` | Yes | Musical description (key, BPM, instruments, vocal style) |
| `--model` | No | Model version (default: latest) |
| `--instrumental` | No | Generate instrumental-only track (no vocals) |
| `--auto-lyrics` | No | Auto-generate lyrics from prompt when `--lyrics` is empty |

*\*Lyrics are optional when using `--auto-lyrics` or `--instrumental`.*

### Examples

**Generate song with vocals:**
bash
minimax-music music \
  --lyrics "[verse]\nStreetlights flicker, the night breeze sighs\n[chorus]\nPushing the wooden door, the aroma spreads" \
  --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
**Generate instrumental music:**
bash
minimax-music music \
  --prompt "C major, 120 BPM, upbeat electronic, synth pop, energetic" \
  --instrumental
**Auto-generate lyrics from prompt:**
bash
minimax-music music \
  --prompt "A cheerful pop song about summer love" \
  --auto-lyrics
### Endpoint

POST https://api.minimax.io/v1/music_generation
---

## 3. Music Cover (Style Transfer)

Generate a cover version of a reference audio file with a different style.

### Command

bash
minimax-music cover "<audio_path>" "<style_description>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `<audio_path>` | Yes | Path to the reference audio file |
| `<style_description>` | Yes | Description of target style |
| `--model` | No | Model version (default: latest) |

### Examples

**Convert to different genre:**
bash
minimax-music cover "/path/to/song.mp3" "Jazz style, smooth piano, swing rhythm"
**Change vocal style:**
bash
minimax-music cover "/path/to/song.mp3" "Female vocal, breathy tone, indie folk"
### Endpoint

POST https://api.minimax.io/v1/music_cover
---

## Tips

- **Lyrics Structure**: Use markers like `[verse]`, `[chorus]`, `[bridge]`, `[intro]`, `[outro]` for best results
- **Prompt Specificity**: Include key, BPM, instruments, and vocal characteristics for precise control
- **Supported Formats**: Check Minimax API documentation for supported audio input formats
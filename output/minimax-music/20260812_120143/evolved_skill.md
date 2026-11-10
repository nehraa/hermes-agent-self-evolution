---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

This skill provides commands to interact with Minimax's music AI APIs for generating lyrics, creating songs, and applying style transfer to audio.

## Configuration

All endpoints require the Minimax API key stored in Hermes memory under `Minimax API key`.

| Setting | Value |
|---------|-------|
| API Key | Retrieved from memory (`Minimax API key`) |
| Base Endpoint | `https://api.minimax.io/v1` |

---

## 1. Lyrics Generation

Generate structured song lyrics from a text prompt.

### Command

bash
minimax-music lyrics "<prompt>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `prompt` | Yes | Description of the song theme, mood, or story |
| `--style-tags` | No | Comma-separated style tags (e.g., "Pop, Romantic, Upbeat") |
| `--title` | No | Title for the song |
| `--edit` | No | Enable edit mode (modify existing lyrics) |

### Examples

**Generate lyrics from a theme:**
bash
minimax-music lyrics "A melancholic breakup song about letting go" --style-tags "Pop, Sad, Heartbreak, Acoustic"
**Edit existing lyrics:**
bash
minimax-music lyrics "Make the chorus more upbeat" --title "Summer Rain" --edit
### Endpoint

POST https://api.minimax.io/v1/lyrics_generation
---

## 2. Music Generation

Generate a complete song from lyrics and a style prompt, or create instrumental tracks.

### Command

bash
minimax-music music [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--lyrics` | Conditional | Song lyrics (use `\n` for line breaks, `\n\n` for section breaks) |
| `--prompt` | Yes | Musical style description (key, BPM, instruments, vocal style) |
| `--model` | No | Model variant (`music-2.6`, `music-2.6-free`) |
| `--instrumental` | No | Generate instrumental only (no vocals) |
| `--auto-lyrics` | No | Auto-generate lyrics from prompt when using `music-2.6` |

### Style Prompt Guidelines

Include these elements in your prompt for best results:

- **Key** (e.g., "E minor", "C major")
- **Tempo** (e.g., "90 BPM", "120 BPM")
- **Genre/Instruments** (e.g., "acoustic guitar ballad", "electronic synth-pop")
- **Vocal style** (e.g., "male vocal, soulful", "female vocal, breathy")
- **Mood** (e.g., "emotional", "upbeat", "nostalgic")

### Examples

**Generate song with lyrics:**
bash
minimax-music music \
  --lyrics "[verse]\nStreetlights flicker, the night breeze sighs\nLonely footsteps echo in the rain\n\n[chorus]\nPushing through the wooden door,\nMemories spill like wine" \
  --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
**Generate instrumental track:**
bash
minimax-music music --prompt "C major, 120 BPM, jazz trio, piano, upright bass, brushed drums" --instrumental
**Auto-generate lyrics from prompt:**
bash
minimax-music music --prompt "A energetic summer pop song with synth and drums" --auto-lyrics
### Endpoint

POST https://api.minimax.io/v1/music_generation
---

## 3. Music Cover (Style Transfer)

Generate a cover version of an audio file by applying a target style.

### Command

bash
minimax-music cover "<audio_path>" --style "<style_description>" [options]
### Options

| Option | Required | Description |
|--------|----------|-------------|
| `audio_path` | Yes | Path to the source audio file |
| `--style` | Yes | Description of the target style |
| `--model` | No | Model variant |

### Example

bash
minimax-music cover "path/to/song.mp3" --style "Convert to 80s synthwave with electronic drums"
### Endpoint

POST https://api.minimax.io/v1/music_cover
---

## Model Variants

| Model | Description |
|-------|-------------|
| `music-2.6` | Full-featured model with highest quality |
| `music-2.6-free` | Free tier model with standard quality |

---

## Error Handling

If an API call fails:

1. Verify the API key is stored in Hermes memory under `Minimax API key`
2. Check your input parameters for formatting issues
3. Ensure the audio file path is valid for cover generation
4. Review rate limits for your API tier
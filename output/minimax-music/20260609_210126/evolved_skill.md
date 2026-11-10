---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

A skill for interacting with Minimax's music AI APIs to generate lyrics, create full songs, and produce style-transferred covers of audio files.

## Prerequisites

- **Minimax API Key**: Stored in Hermes memory under the key `Minimax API key`

## API Configuration

| Setting | Value |
|---------|-------|
| Base Endpoint | `https://api.minimax.io/v1` |

---

## 1. Lyrics Generation

Generate structured song lyrics (verses, choruses, bridges, etc.) from a text prompt.

### Command

bash
minimax-music lyrics "<prompt>" [--style-tags "<tags>"] [--title "<title>"] [--edit]
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `prompt` | Yes | Natural language description of the song theme, mood, or story |
| `--style-tags` | No | Comma-separated tags guiding the musical style (e.g., "Pop, Upbeat, Summer") |
| `--title` | No | Song title to assign |
| `--edit` | No | Edit mode: treat prompt as instructions to revise existing lyrics (requires `--title` and context) |

### Examples

**Basic generation:**
bash
minimax-music lyrics "A bittersweet breakup song set in autumn"
**With style guidance:**
bash
minimax-music lyrics "A triumphant anthem about overcoming obstacles" \
  --style-tags "Epic, Orchestral, Rock, Uplifting, Cinematic"
**Editing existing lyrics:**
bash
minimax-music lyrics "Make the chorus more energetic" --title "Summer Dreams" --edit
### Endpoint

POST https://api.minimax.io/v1/lyrics_generation
---

## 2. Music Generation

Generate a complete song (melody, arrangement, optional vocals) from lyrics and a style prompt, or create instrumental music from a prompt alone.

### Command

bash
minimax-music music [--lyrics "<lyrics>"] [--prompt "<prompt>"] [--model "<model>"] [--instrumental] [--auto-lyrics]
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--lyrics` | Conditional | Song lyrics with structure markers (e.g., `[verse]`, `[chorus]`, `[bridge]`) |
| `--prompt` | Yes | Musical description including key, tempo, instruments, vocals, mood |
| `--model` | No | Model variant to use (defaults to best available) |
| `--instrumental` | No | Generate instrumental only (no vocals); ignores `--lyrics` |
| `--auto-lyrics` | No | Auto-generate lyrics from prompt when `--lyrics` is empty (requires `music-2.6` or `music-2.6-free`) |

### Prompt Guidelines

Structure your `--prompt` with these elements for best results:

- **Key/Tempo**: `E minor, 90 BPM`
- **Instrumentation**: `acoustic guitar, piano, drums`
- **Vocals**: `male vocal, falsetto chorus`
- **Mood/Genre**: `melancholic indie folk, 80s synth-pop`

### Examples

**Song with custom lyrics:**
bash
minimax-music music \
  --lyrics "[verse]\nStreetlights flicker, night breeze sighs\n[chorus]\nPushing open doors, memories arise" \
  --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
**Instrumental music:**
bash
minimax-music music --prompt "C major, 120 BPM, upbeat synth-pop, electronic drums, 80s vibe" --instrumental
**Auto-generated lyrics:**
bash
minimax-music music --prompt "A joyful celebration of summer beach life" --auto-lyrics
### Endpoint

POST https://api.minimax.io/v1/music_generation
---

## 3. Music Cover

Generate a cover version of a reference audio file by applying a target musical style. This performs style transfer on the input audio.

### Command

bash
minimax-music cover --input "<path>" --prompt "<prompt>"
### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | Yes | Path to the reference audio file (MP3, WAV, etc.) |
| `--prompt` | Yes | Target style description (genre, mood, instrumentation, era, etc.) |

### Examples

**Transform to a different genre:**
bash
minimax-music cover --input "/path/to/original_song.mp3" --prompt "Jazz quartet arrangement, swing rhythm, smooth"
**Change the mood:**
bash
minimax-music cover --input "/path/to/acoustic_demo.wav" --prompt "Dark orchestral, cinematic, epic crescendo"
### Endpoint

POST https://api.minimax.io/v1/music_cover
---

## Workflow Example

A typical song creation workflow:

1. **Generate lyrics:**
   ```bash
   minimax-music lyrics "A nostalgic song about childhood summers" --style-tags "Indie Folk, Warm, Nostalgic"
   ```

2. **Review and edit** the generated lyrics as needed using `--edit`

3. **Generate the full song:**
   ```bash
   minimax-music music --lyrics "<refined lyrics>" --prompt "G major, 85 BPM, fingerpicked acoustic guitar, warm male vocal, gentle chorus"
   ```

4. **Optional:** Create alternate styles using `cover` to experiment with different arrangements

---

## Error Handling

- **Missing API key**: Returns error if `Minimax API key` is not found in Hermes memory
- **Invalid audio format**: Cover endpoint accepts common formats; verify input file compatibility
- **Rate limits**: Implement appropriate delays between requests if generating multiple files
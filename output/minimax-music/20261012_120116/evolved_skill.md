---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

Interface for Minimax's music AI APIs enabling lyrics generation, full music composition, and style transfer covers.

## Prerequisites

- **Minimax API Key**: Stored in Hermes memory as `Minimax API key`
- **Base Endpoint**: `https://api.minimax.io/v1`

## Commands

### `minimax-music lyrics`

Generate structured song lyrics from a descriptive prompt.

bash
minimax-music lyrics "<prompt>" [options]
**Options**:

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--style-tags` | string | No | Comma-separated style tags (e.g., "Pop, Summer, Romantic") |
| `--edit` | flag | No | Edit mode: continues or modifies existing lyrics |
| `--title` | string | No | Song title (required with `--edit`) |

**Examples**:

Generate fresh lyrics:
bash
minimax-music lyrics "A bittersweet breakup song about letting go"
minimax-music lyrics "Summer love at a beach party" --style-tags "Pop, Upbeat, Tropical"
Edit existing lyrics:
bash
minimax-music lyrics "Make the chorus more dramatic" --edit --title "Midnight Drive"
**Endpoint**: `POST /v1/lyrics_generation`

---

### `minimax-music music`

Generate a complete song with vocals or instrumental track.

bash
minimax-music music --prompt "<style>" [options]
**Options**:

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--prompt` | string | Yes | Musical description (key, BPM, instruments, mood, vocal type) |
| `--lyrics` | string | No | Full lyrics with section markers (`[verse]`, `[chorus]`, etc.) |
| `--model` | string | No | Model variant: `music-2`, `music-2.1`, `music-2.6`, `music-2.6-free` |
| `--instrumental` | flag | No | Generate instrumental only (no vocals) |

**Model Reference**:

| Model | Auto-Lyrics | Instrumental | Notes |
|-------|-------------|--------------|-------|
| `music-2` | No | Yes | Stable, widely supported |
| `music-2.1` | No | Yes | Improved quality |
| `music-2.6` | Yes | Yes | Auto-generates lyrics from prompt when `--lyrics` omitted |
| `music-2.6-free` | Yes | Yes | Cost-optimized variant of 2.6 |

**Examples**:

Song from lyrics with style:
bash
minimax-music music \
  --lyrics "[verse]\nCity lights flicker, the night begins\n[chorus]\nRunning through the rain, finding home" \
  --prompt "A minor, 85 BPM, acoustic guitar, male vocal, melancholic indie folk"
Instrumental track:
bash
minimax-music music --prompt "C major, 120 BPM, upbeat electronic, synthwave" --instrumental
Auto-generated lyrics (2.6/2.6-free):
bash
minimax-music music --prompt "Upbeat summer pop, female vocal, teenage romance" --model music-2.6
**Endpoint**: `POST /v1/music_generation`

---

### `minimax-music cover`

Apply a target style to a reference audio file (style transfer).

bash
minimax-music cover --input "<path>" --prompt "<style>" [options]
**Options**:

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--input` | string | Yes | Path to reference audio file |
| `--prompt` | string | Yes | Target style description |
| `--model` | string | No | Cover model: `cover-2` (default) or `cover-3` |

**Example**:
bash
minimax-music cover --input "/audio/my-song.mp3" --prompt "Jazz quartet, smooth saxophone solo" --model cover-3
**Endpoint**: `POST /v1/music_cover`

---

## Response Format

All commands return JSON with the following structure:

json
{
  "task_id": "string",
  "status": "pending|processing|completed|failed",
  "result": {
    "audio_url": "string (when completed)",
    "lyrics": "string (lyrics generation only)"
  },
  "error": "string (when failed)"
}
**Polling**: For async operations, poll the status endpoint or use `--wait` flag:
bash
minimax-music lyrics "..." --wait
---

## Error Handling

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `401` | Invalid or missing API key | Verify `Minimax API key` in Hermes memory |
| `400` | Invalid parameters | Check prompt syntax and required fields |
| `429` | Rate limit exceeded | Wait before retrying |
| `500` | Server error | Retry with exponential backoff |
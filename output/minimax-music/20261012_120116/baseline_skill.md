---
name: minimax-music
description: "Interface for Minimax music-related APIs: lyrics generation, music generation, and music cover (style transfer)"
category: music
---

# Minimax Music Skill

This skill provides convenient commands to interact with Minimax's music AI APIs:
- **Lyrics Generation**: Generate structured song lyrics from a prompt.
- **Music Generation**: Generate a song (with optional vocals) from lyrics and a style prompt.
- **Music Cover**: Generate a cover version of a reference audio file with a target style description.

All endpoints require the Minimax API key stored in Hermes memory.

## Configuration (stored in Hermes memory)
- **Minimax API Key**: Retrieved from memory (`Minimax API key`)
- **Base Endpoint**: `https://api.minimax.io/v1`

## Usage

### 1. Lyrics Generation
Generate lyrics from a descriptive prompt.

**Command**: `minimax-music lyrics "<prompt>" [--style-tags "<tags>"] [--edit] [--title "<title>"]`

**Example**:
```bash
minimax-music lyrics "A cheerful love song about a summer day at the beach" --style-tags "Pop, Summer Vibe, Romance, Lighthearted, Beach Pop"
```

**Parameters**:
- `prompt` (required): Description of the song theme.
- `--style-tags`: Optional comma-separated tags to guide the style.
- `--edit`: If set, treat prompt as instructions to edit/continue existing lyrics (requires `--title` and existing lyrics context).
- `--title`: Optional title to preserve when editing/continuing.

**Endpoint**: `POST https://api.minimax.io/v1/lyrics_generation`

### 2. Music Generation
Generate a song from lyrics and a prompt, or generate instrumental music.

**Command**: `minimax-music music [--lyrics "<lyrics>"] [--prompt "<prompt>"] [--model "<model>"] [--instrumental] [--auto-lyrics]`

**Examples**:
- Generate music from provided lyrics and style prompt:
  ```bash
  minimax-music music --lyrics "[verse]\\nStreetlights flicker, the night breeze sighs\\n[chorus]\\nPushing the wooden door, the aroma spreads" --prompt "E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"
  ```
- Generate instrumental music from prompt only (auto-generates lyrics if `--auto-lyrics` not set? Actually `music-2.6`/`music-2.6-free` can auto-generate lyrics from prompt when lyrics empty):
  ```bash
  minimax-music music --prompt "E minor, 90 BPM, acoustic guitar ballad" --instrumental
  ```
- Let the model auto-generate lyrics from prompt (requires `music-2.6` or `music-2.6-free`):
  ```bash
  minimax-music music --prompt "A cheerful love song about a summer day at the beach" --auto-lyrics
  ```

**Parameters**:
- `--lyrics`: Structured lyrics (with `[Intro]`, `[Verse]`, etc.) to use for generation. If omitted and `--auto-lyrics` is set, lyrics will be generated from `--prompt`.
- `--prompt`: Description of the music style, mood, and scenario (e.g., `"E minor, 90 BPM, acoustic guitar ballad, male vocal, emotional"`).
- `--model`: Model to use. Defaults to `music-2.6`. **Always use `music-2.6` (paid model)** — `music-2.6-free` does not exist on paid accounts and returns "token plan not support model" error.
- `--instrumental`: Set to true to generate instrumental music (no vocals). The API param is `is_instrumental`.
- `--auto-lyrics`: When set and `--lyrics` is empty, automatically generate lyrics from `--prompt` (only works with `music-2.6` / `music-2.6-free`).

**Endpoint**: `POST https://api.minimax.io/v1/music_generation`

### 3. Music Cover (Style Transfer)
Generate a cover version of a reference audio file with a target style description.

**Command**: `minimax-music cover --audio "<audio_url_or_uuid>" --prompt "<style_description>" [--format "<format>"] [--seed "<seed>"]`

**Example**:
```bash
minimax-music cover --audio "https://example.com/pop-song.mp3" --prompt "Lo-fi hip hop version, vinyl crackle, chill beat, warm midrange" --format mp3
```

**Parameters**:
- `--audio` (required): URL or UUID of the source audio file.
- `--prompt` (required): Description of the target style (e.g., `"R&B version, smooth vocal, groovy bass"`).
- `--format`: Output format (`mp3` default, `wav`, `pcm`).
- `--seed`: Optional random seed for reproducible generation.

**Endpoint**: `POST https://api.minimax.io/v1/music_generation` (using model `minimax:music@cover`)

**Note**: The music cover task uses the same `/v1/music_generation` endpoint but with the model identifier `minimax:music@cover`. The skill will automatically set the model accordingly.
## Key Experiential Findings (Updated May 16, 2026)

### Auth Issue — Root Cause Found
The "1004 login fail" error on `/v1/music_generation` was caused by **whitespace in the API key string** when read from `.env`. The key had trailing newlines/spaces that corrupted the Bearer token in the HTTP header.

**Correct key reading pattern:**
```python
KEY = None
for path in ['/home/Hermes/.hermes/.env']:
    try:
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    if k == 'MINIMAX_API_KEY':
                        KEY = v.strip()  # ← must strip, not just split
                        break
        if KEY:
            break
    except:
        pass
```

**Incorrect pattern (causes 1004):**
```python
KEY = line.split('=', 1)[1].strip()  # May retain trailing newlines
# Or:
KEY = os.environ.get('MINIMAX_API_KEY', '')  # Env var inherits whitespace from .env
```

### Music Generation — Instrumental vs Vocal
- **Instrumental**: `is_instrumental: True` + style prompt only (no lyrics)
- **Vocal**: `is_instrumental: False` + `lyrics` field (structured lyrics with [Verse], [Chorus], etc.)
  - **Critical**: Passing prompt only with `is_instrumental: False` returns `{"base_resp": {"status_code": 2013, "status_msg": "invalid params, lyrics is required"}}`
  - You MUST generate lyrics first via `lyrics_generation`, then pass them to music generation

### Workflow for Vocal Track
```python
# Step 1: Generate lyrics
lyr_resp = requests.post("https://api.minimax.io/v1/lyrics_generation", headers=headers, json={
    "mode": "write_full_song",
    "prompt": "High energy product demo song, upbeat electronic, confident vibe",
    "style_tags": "Electronic, Product Demo, Energetic, Festival, Upbeat"
}, timeout=60)
lyrics = lyr_resp.json()["lyrics"]

# Step 2: Generate music with lyrics
resp = requests.post("https://api.minimax.io/v1/music_generation", headers=headers, json={
    "model": "music-2.6",
    "prompt": "150 BPM high energy electronic product demo, festival anthem energy",
    "lyrics": lyrics,
    "is_instrumental": False,
    "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"}
}, timeout=300)
```

### Audio Return Format
- **The `output_format: "url"` param is IGNORED.** The API always returns hex-encoded MP3 audio in `resp["data"]["audio"]` — never a URL.
- The hex string starts with `49443304` = "ID3" (MP3 ID3 tag). Decode with:
  ```python
  audio_bytes = bytes.fromhex(hex_string)
  with open("song.mp3", "wb") as f:
      f.write(audio_bytes)
  ```
- Duration (ms) is returned in `resp["extra_info"]["music_duration"]`.

### Generation Time
- Each `music-2.6` call takes **40–60 seconds**. Set timeouts to 300s for vocal tracks (longer due to lyrics processing).

### Track Duration vs Lyrics Volume
- Short lyrics (4–8 lines) → ~25–65 second tracks
- Full structured lyrics (40+ lines with multiple sections) → **3–4 minute tracks**
- To target 2–2.5 min: use `write_full_song` mode for lyrics (not short prompts), include `[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]` sections

### Model Naming
- Paid account: use `music-2.6` (NOT `music-2.6-free`)
- `music-2.6-free` does not exist on paid plans — it returns "token plan not support model" error

### Lyrics JSON Structure
- When lyrics are saved to JSON (e.g. from `lyrics_generation`), they come back as a dict:
  ```json
  {"song_title": "...", "style_tags": "...", "lyrics": "[Verse]\n...", "base_resp": {...}}
  ```
  Access lyrics with `entry["lyrics"]`, not as a plain string.

### `is_instrumental` Flag
- The API param is `is_instrumental`, not `instrumental`.

### Batch Generation (Multiple Tracks)
For generating multiple songs in sequence, use `/home/Hermes/songs/generate_all.py`. It reads from `/home/Hermes/songs_lyrics.json` (a dict keyed by song title → `{lyrics, style_tags, song_title, base_resp}`) and generates all tracks to `/home/Hermes/songs/`. Run in background since each track takes 40-60s:

```bash
cd /home/Hermes && python3 /home/Hermes/songs/generate_all.py &
```

Each track produces a valid MP3 (256kbps, 44100Hz) via hex decoding:
```python
audio_bytes = bytes.fromhex(resp["data"]["audio"])
with open(f"{num}_{title}.mp3", "wb") as f:
    f.write(audio_bytes)
```

### Ambient/Choir Music for Video Background (May 2026)

**Key fixes discovered May 28, 2026:**
- Bitrate: `128000` max — `320000` returns "audio bitrate: 320000 is not allowed"
- Key: read from `.env` — hardcoding causes 1004 auth errors
- Use `urllib.request` (not `requests`) for large hex responses (6MB+) — `requests` times out on big payloads
- Full MP3 (>2MB) often fails Telegram media delivery — send OGG preview first

For video background music (no lyrics, layered vocal vowels for cinematic feel):
```python
import urllib.request, json

payload = {
    "model": "music-2.6",
    "prompt": ("Epic ethereal choir, massive layered human vowel vocals AHHH OHHH, "
               "grand cathedral atmosphere, reverent and powerful, sacred choral texture, "
               "long sustained tones"),
    "is_instrumental": True,
    "audio_setting": {"sample_rate": 44100, "bitrate": 128000, "format": "mp3"}
}
req = urllib.request.Request(
    "https://api.minimax.io/v1/music_generation",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=600) as resp:
    result = json.loads(resp.read())

audio_hex = result["data"]["audio"]
with open("choir_music.mp3", "wb") as f:
    f.write(bytes.fromhex(audio_hex))
```

**Prompt keywords for heroic/ethereal choir (avoid binaural/beats/meditation):**
- Use `music-2.6` only — `music-2.6-free` doesn't exist on paid plans

### Sleep / Hypnosis / Meditation Ambient (Verified Jul 2026)

Different emotional register than cinematic choir. Sleep tracks want a SLOW, DARK, PERCUSSION-FREE bed that stays "underneath" — never competing with narration. The cinematic recipe above produces the WRONG sound for sleep content.

**Prompt keywords that work for sleep-friendly ambient (verified Jul 25 2026 — produced a 3.9-min dark ambient bed for a 30-min hypnosis track):**
- USE: "ultra-slow," "deeply soothing," "sleepy," "warm dark ambient pads," "soft low piano notes very far apart," "subtle ocean-like breath texture," "gentle sustained strings," "48 BPM feeling," "no percussion," "no drums," "no vocals," "no melody hook," "no sudden changes," "no bright high frequencies," "no tension," "no climax," "seamless meditative flow," "quiet nighttime atmosphere," "safe comforting spacious production," "designed to sit under whispered narration."
- AVOID: "epic," "heroic," "grand," "Gregorian," "Hans Zimmer," "cathedral," "massive layered" — these pull toward cinematic and ruin the bed.

**Single keywords that misfire:** "binaural beats," "432hz," "meditation" alone, "nature sounds" — these tend to either (a) produce weird techno or (b) come back silent. The keyword phrase above (not single words) is what produces sleepy beds.

**Sleep track output length:** Music-2.6 rarely outputs > 5 min even with empty lyrics. Loop the result under the voice — seamlessness matters more than absolute length. For a 30-min track, a 3–5 min bed looped 6–10x with crossfades is the right pattern.

**Pair with:** `creative/guided-meditation-audio` — full pipeline (script → ambient → voice narration → mix to 30 min, deliver via email/Telegram). Scripts at `scripts/{generate_ambient,generate_voice,mix_track,send_email}.py`.

### Product Demo Music — Fast Tempo (May 16 2026)
For upbeat energetic product demo tracks:
```python
PAYLOAD = {
    "model": "music-2.6",
    "prompt": (
        "High energy upbeat electronic product demo music, "
        "140-150 BPM fast tempo, driving funk bass line, "
        "bright punchy synth stabs, festival anthem energy, "
        "no drums (or full drums depending on vibe), "
        "confident bold sound, catchy high energy hook"
    ),
    "is_instrumental": True/False,
    "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"}
}
```

## Error Handling
If the API returns an error, the skill will output the error message and exit with non-zero status.

## Examples
See the usage sections above for concrete command-line examples.

## Implementation
This skill is intended to be invoked via the Hermes agent's command interface (or directly as a shell script). It uses the stored Minimax API key for authentication via Bearer token.

---
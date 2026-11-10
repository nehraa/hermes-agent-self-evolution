---
category: software-development
name: download-anything
description: >
  Find and download any digital resource — ebooks, academic papers, videos, music, software,
  images, fonts, courses, and more. Covers both English and Chinese internet ecosystems. Includes
  CLI tool workflows (yt-dlp, aria2, gallery-dl, spotdl), resource site directories, cloud drive
  search engines (百度/阿里/夸克网盘搜索), and advanced search techniques (Google dorks).
  Use when the user wants to: (1) download media from a URL, (2) find an ebook or paper,
  (3) find software, (4) search for any digital resource, (5) batch download images,
  (6) download torrents, (7) find free stock assets, (8) search Chinese cloud drives, or
  (9) any task involving finding or downloading digital content.
---
# Download Anything

Find it. Download it. Any resource, any format.

## Quick Start

bash
# Install all tools at once
bash scripts/install-toolkit.sh

# Common download commands
./scripts/dl-video.sh "https://youtube.com/watch?v=..."      # Any video
./scripts/dl-audio.sh "https://vimeo.com/..."                # Audio only
./scripts/dl-file.sh "https://example.com/file.zip"          # Direct file
./scripts/dl-gallery.sh "https://example.com/gallery"        # Batch images
./scripts/dl-torrent.sh "magnet:?xt=urn:btih:..."            # Torrents
## Toolkit Reference

### Core Downloaders

| Tool | Install | Best For |
|------|---------|----------|
| **yt-dlp** | `brew install yt-dlp` | Videos/audio from 1800+ sites (YouTube, Bilibili, Twitter, TikTok, etc.) |
| **aria2c** | `brew install aria2` | Multi-threaded downloads, torrents, segmented fetching |
| **gallery-dl** | `pip3 install gallery-dl` | Batch image downloads from 170+ sites (Pixiv, Twitter, Instagram) |
| **spotdl** | `pip3 install spotdl` | Spotify tracks/albums/playlists to local files |
| **wget** | `brew install wget` | Recursive downloads, site mirroring, resume support |

### Utilities

| Tool | Install | Purpose |
|------|---------|---------|
| **ffmpeg** | `brew install ffmpeg` | Convert media formats, extract audio, trim clips |
| **jq** | `brew install jq` | Parse JSON responses for API automation |
| **curl** | pre-installed | HTTP requests, API calls, quick file fetches |

## Decision Tree

| Need to download... | Command / Tool |
|---------------------|----------------|
| **Video from YouTube** | `yt-dlp -f "bestvideo+bestaudio" URL` |
| **Video from Bilibili** | `yt-dlp --cookies cookies.txt URL` |
| **Audio only (MP3)** | `yt-dlp -x --audio-format mp3 URL` |
| **Spotify playlist** | `spotdl https://open.spotify.com/playlist/...` |
| **Twitter/X images** | `gallery-dl "https://twitter.com/user/status/..."` |
| **Pixiv artist works** | `gallery-dl "https://www.pixiv.net/en/users/..."` |
| **Direct file (fast)** | `aria2c -x16 -s16 URL` |
| **Torrent / magnet** | `aria2c --dir=/downloads "magnet:..."` |
| **Entire website** | `wget --mirror -p --convert-links URL` |
| **Ebook or paper** | See [references/ebooks.md](references/ebooks.md) |
| **Movie or TV show** | See [references/video.md](references/video.md) |
| **Music / game OST** | See [references/audio.md](references/audio.md) |
| **Chinese cloud drive** | See [references/chinese-sources.md](references/chinese-sources.md) |

## Common Workflows

### Download YouTube Video with Subtitles

bash
# Download best quality video + audio, include subtitles
yt-dlp \
  --embed-subs \
  --embed-thumbnail \
  --format "bestvideo+bestaudio/best" \
  -o "%(title)s.%(ext)s" \
  "https://youtube.com/watch?v=VIDEO_ID"

# Download audio only as MP3
yt-dlp -x --audio-format mp3 "https://youtube.com/watch?v=VIDEO_ID"
### Download Bilibili Video (Requires Cookies)

bash
# Export cookies from browser (B站需要登录才能下载高画质)
yt-dlp --cookies ~/cookies/bilibili.txt "https://bilibili.com/video/BV..."

# Download entire series/playlist
yt-dlp --cookies ~/cookies/bilibili.txt \
  --playlist-start 1 \
  --playlist-end 10 \
  "https://bilibili.com/video/BV..."
### Batch Download Images

bash
# Download from a Pixiv artist's entire gallery
gallery-dl \
  --dest-directory "~/Downloads/pixiv/{user.name}" \
  "https://www.pixiv.net/en/users/12345678"

# Download Twitter/X images from a thread
gallery-dl "https://twitter.com/user/status/1234567890"

# Custom filename pattern
gallery-dl --filename "{author}/{date:%Y}/{id}.{extension}" URL
### Multi-Threaded File Download

bash
# 16 connections for maximum speed
aria2c -x16 -s16 "https://example.com/largefile.zip"

# Resume interrupted download
aria2c -c "https://example.com/largefile.zip"

# Download multiple files from list
aria2c -i urls.txt
### Download Torrent/Magnet

bash
# Direct magnet link
aria2c --dir=/tmp/downloads "magnet:?xt=urn:btih:HASH..."

# With seed/peer limits
aria2c --max-upload-limit=10K --max-connection-per-server=5 "torrent file.torrent"

# Sequential download (for media)
aria2c --file-allocation=none --dir=/tmp/downloads "magnet:..."
## Advanced: yt-dlp Tips

bash
# List all available formats
yt-dlp --list-formats URL

# Download specific quality (720p video + best audio)
yt-dlp -f "bestvideo[height<=720]+bestaudio/best" URL

# Download Shorts (YouTube)
yt-dlp "https://youtube.com/shorts/VIDEO_ID"

# Download from 18+ content (requires cookies)
yt-dlp --cookies ~/cookies/cookies.txt URL

# Skip already downloaded (update library)
yt-dlp -ciw --download-archive downloaded.txt URL

# Extract audio, embed metadata, save as M4A
yt-dlp -x --audio-format m4a --embed-metadata URL

# Download subtitles only
yt-dlp --write-subs --skip-download URL
## Advanced: gallery-dl Tips

bash
# Download from multiple sources
gallery-dl --dest-directory ~/Downloads/ "url1" "url2"

# Use custom config file
gallery-dl --config-file ~/.config/gallery-dl/config.json URL

# Skip duplicates
gallery-dl --no-skip URL

# Custom naming
gallery-dl --filename "{blog[title]}/{id}.{extension}" URL

# Limit download rate (KB/s)
gallery-dl --download-delay 0.5 URL
## Searching for Resources

### Google Dorks for Direct Downloads

| Dork | Use Case |
|------|----------|
| `filetype:pdf "topic"` | Find PDFs |
| `site:archive.org "filename"` | Internet Archive search |
| `intitle:"index of" "mp3"` | Open directory music |
| `"filename.ext" "download"` | Direct file search |
| `site:github.com "filename.ext"` | GitHub repositories |

### Chinese Cloud Drive Search

| Engine | URL |
|--------|-----|
| 盘搜搜 | pansou.com |
| 盘多多 | panduoduo.net |
| 小昭君 | xiaozhaojun.com |
| 的大力 | ss.fyfx.hk |

> For comprehensive resource lists, see the reference files in `references/`.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bilibili 403 error | Export fresh cookies from browser, save to `~/cookies/bilibili.txt` |
| Download too slow | Use `aria2c -x16 -s16` for 16 parallel connections |
| Video unavailable | Try `--no-check-certificates` or different format |
| Instagram private | Cannot access without following — use browser cookies |
| Rate limited | Add `--download-delay 1` or use VPN |
| SSL errors | Update certificates: `pip3 install --upgrade certifi` |

## Reference Files

- [references/ebooks.md](references/ebooks.md) — Academic papers, textbooks, PDFs
- [references/video.md](references/video.md) — Movies, TV shows, streaming
- [references/audio.md](references/audio.md) — Music, podcasts, game OSTs
- [references/chinese-sources.md](references/chinese-sources.md) — Chinese platforms, cloud drives
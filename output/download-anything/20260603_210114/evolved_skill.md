---
category: software-development
name: download-anything
description: >
  Find and download virtually any digital resource from the internet — ebooks, academic papers,
  movies, TV shows, music, software, images, fonts, courses, and more. Covers both English and
  Chinese internet ecosystems. Includes CLI tool workflows (yt-dlp, aria2, gallery-dl, spotdl),
  resource site directories, cloud drive search engines (百度/阿里/夸克网盘搜索), and search
  techniques (Google dorks). Use when the user wants to: (1) download a video, audio, or media
  from a URL, (2) find and download an ebook or academic paper, (3) find and download software,
  (4) search for any digital resource, (5) batch download images or media from a gallery/site,
  (6) download torrents or magnet links, (7) find free stock assets (images, video, audio, fonts),
  (8) search Chinese cloud drives for resources, or (9) any task involving finding or downloading
  digital content from the internet.
---

# Download Anything

Find it. Download it. Any resource, any format.

## Environment Setup

bash
# Create working directory
mkdir -p ~/Downloads/torrents ~/Downloads/media ~/Downloads/ebooks

# Install all core tools
brew install yt-dlp aria2 wget curl ffmpeg jq
pip3 install gallery-dl spotdl

# Verify installations
yt-dlp --version
aria2c --version
gallery-dl --version
spotdl --version
## Toolkit

| Tool | Install | Purpose |
|------|---------|---------|
| `yt-dlp` | `brew install yt-dlp` | Video/audio from 1800+ sites |
| `aria2c` | `brew install aria2` | Multi-thread downloads, torrents,Resume interrupted downloads |
| `gallery-dl` | `pip3 install gallery-dl` | Batch image/media downloads from 170+ sites |
| `spotdl` | `pip3 install spotdl` | Spotify playlists → local audio files |
| `wget` | `brew install wget` | Recursive downloads, site mirroring |
| `curl` | pre-installed | HTTP requests, API calls, quick downloads |
| `ffmpeg` | `brew install ffmpeg` | Media conversion, format switching |
| `jq` | `brew install jq` | JSON parsing for automation scripts |

## Decision Tree: What Do You Need?

### Download from URL / Platform

| I want to download... | Use this command |
|-----------------------|------------------|
| YouTube / Bilibili video | `yt-dlp -f "bestvideo+bestaudio" URL` |
| Video from any site | `yt-dlp URL` (auto-detects platform) |
| Audio only (MP3) from video | `yt-dlp -x --audio-format mp3 URL` |
| Subtitles with video | `yt-dlp --write-subs --sub-lang en URL` |
| Spotify playlist/album | `spotdl URL` |
| Complete gallery/images | `gallery-dl URL` |
| Direct file (fast multi-thread) | `aria2c -x16 -s16 URL` |
| Quick file (simple) | `curl -L -O URL` |
| Recursive site download | `wget -r -np URL` |

### Search and Find Resources

| I want to find... | Go to reference |
|-------------------|-----------------|
| Ebook or academic paper | [references/ebooks.md](references/ebooks.md) |
| Movie, TV show, anime | [references/video.md](references/video.md) |
| Music, soundtrack, album | [references/music.md](references/music.md) |
| Software, tools, games | [references/software.md](references/software.md) |
| Images, fonts, stock assets | [references/assets.md](references/assets.md) |

### Chinese Cloud Drive Search

| Resource type | Search engines |
|---------------|-----------------|
| Baidu Netdisk (百度网盘) | 云盘精灵, 小男孩搜索, 大力盘, 盘搜搜 |
| Ali Cloud (阿里云盘) | 奈斯搜索, 云盘分享 |
| Quark (夸克网盘) | 夸克网盘搜索引擎 |

## Common Patterns

### Video Downloads

bash
# Best quality (merges video + audio)
yt-dlp -f "bestvideo+bestaudio/best" URL

# Specific format (720p only)
yt-dlp -f "bestvideo[height<=720]+bestaudio/best" URL

# Download audio only as MP3
yt-dlp -x --audio-format mp3 --audio-quality 0 URL

# Download with subtitles embedded
yt-dlp --write-subs --sub-lang en,zh-Hans --embed-subs URL

# Bilibili with cookies (for high-quality members-only content)
yt-dlp --cookies-from-browser chrome URL
### Batch Downloads

bash
# Download all images from a gallery
gallery-dl -D ~/Downloads/images URL

# Download from multiple URLs (one per line)
gallery-dl URLs.txt

# Mirror complete site with wget
wget --mirror --convert-links --adjust-extension --page-requisites URL

# Multi-thread download (16 connections)
aria2c -x16 -s16 -d ~/Downloads/file.zip URL
### Torrents

bash
# Download single torrent
aria2c --seed-time=0 https://example.com/torrent.torrent

# Download from magnet link
aria2c --seed-time=0 "magnet:?xt=urn:btih:..."

# Add to transmission-daemon (headless)
transmission-cli -w ~/Downloads/torrents MAGNET_LINK
### File Transfer

bash
# Resume interrupted download
aria2c -c URL

# Quick download with progress
curl -L# -o output.file URL

# Download with bandwidth limit
aria2c --max-download-limit=1M URL

# Parallel download from multiple sources
aria2c -x2 -s2 URL1 URL2 -o output.file
## Search Techniques

### Google Dorks

bash
# Find specific filetype
"filetype:pdf" "machine learning"
"filetype:epub" "data science"

# Find direct download links
"site:dropbox.com" "software installer"
"intitle:pdf" "free download"

# Academic papers
"filetype:pdf" "arxiv" "neural network"
site:libgen.is "ebook title"

# Software downloads
"filetype:exe" OR "filetype:msi" "software name"
### Cloud Drive Search

1. **百度网盘搜索**: 云盘精灵 (ypiao.com), 小男孩搜索, 盘搜索
2. **阿里云盘搜索**: 奈斯搜索, 小昭网络, 云盘资源分享
3. **夸克网盘搜索**: 夸克搜索引擎
4. **聚合搜索**: 大力盘超级搜索, 凌风云

## Media Conversion

bash
# Convert video to audio
ffmpeg -i video.mp4 -vn -ar 44100 -ac 2 audio.mp3

# Trim video (start to end)
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:03:00 output.mp4

# Convert format
ffmpeg -i input.mkv -codec copy output.mp4

# Extract audio from video
ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3

# Concatenate videos
ffmpeg -f concat -i list.txt -c copy output.mp4
## Managing Downloads

bash
# Create organized directory structure
mkdir -p ~/Downloads/{video,audio,images,documents,software,torrents}

# Batch rename after download
cd ~/Downloads/images && for f in *; do mv "$f" "$(date +%Y%m%d)_$f"; done

# Find and delete duplicates
fdupes -rdN ~/Downloads/

# Check downloaded file integrity
shasum -a 256 file.zip
md5sum file.zip
## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Video unavailable" on YouTube | Update yt-dlp: `pip3 install -U yt-dlp` or use cookies |
| Slow download speeds | Try `aria2c -x16 -s16` for 16 parallel connections |
| Bilibili quality too low | Export browser cookies and pass with `--cookies` |
| Gallery download fails | Try `--no-check-certificate` or use alternative URL format |
| Spotify download fails | Get fresh credentials: `spotdl login` |
| SSL certificate error | Add `--no-check-certificate` flag |

## References

See these companion files for domain-specific resources:

- [references/ebooks.md](references/ebooks.md) — Academic papers, ebooks, documents
- [references/video.md](references/video.md) — Movies, TV shows, anime, documentaries
- [references/music.md](references/music.md) — Albums, playlists, soundtracks
- [references/software.md](references/software.md) — Software, tools, games
- [references/assets.md](references/assets.md) — Images, fonts, stock media
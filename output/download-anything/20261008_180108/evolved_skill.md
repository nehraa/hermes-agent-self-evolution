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

# Download a video from any site
./scripts/dl-video.sh "https://youtube.com/watch?v=..."

# Download audio only (MP3)
./scripts/dl-audio.sh "https://vimeo.com/..."

# Download a direct file
./scripts/dl-file.sh "https://example.com/file.zip"

# Batch download images from a gallery
./scripts/dl-gallery.sh "https://example.com/gallery"

# Download via torrent
./scripts/dl-torrent.sh "magnet:?xt=urn:btih:..."
## Toolkit Reference

### Core Downloaders

| Tool | Install | Best For |
|------|---------|----------|
| **yt-dlp** | `brew install yt-dlp` | Videos/audio from 1800+ sites (YouTube, Bilibili, Twitter, TikTok, NicoNico, Vimeo) |
| **aria2** | `brew install aria2` | Multi-threaded downloads, torrents, segmented fetching, resume support |
| **gallery-dl** | `pip3 install gallery-dl` | Batch image downloads from 170+ sites (Pixiv, Twitter, Instagram, DeviantArt) |
| **spotdl** | `pip3 install spotdl` | Spotify tracks/albums/playlists to MP3 with metadata |
| **wget** | `brew install wget` | Recursive downloads, site mirroring, HTTP/HTTPS/FTP |
| ** Transmission** | `brew install --cask transmission` | GUI/BROWSER torrent client for macOS |

### Media Processing

| Tool | Install | Purpose |
|------|---------|---------|
| **ffmpeg** | `brew install ffmpeg` | Convert formats, extract audio, trim clips, merge streams |
| **atomicparsley** | `brew install atomicparsley` | Embed artwork/metadata into MP4/M4A |
| **mkvmerge** | `brew install mkvtoolnix` | Merge video/audio/subtitle tracks |

### Utilities

| Tool | Install | Purpose |
|------|---------|---------|
| **jq** | `brew install jq` | Parse JSON for API automation |
| **curl** | pre-installed | HTTP requests, API calls, quick fetches |
| **xclip** | `brew install xclip` | Clipboard integration for scripts |

## Decision Tree

| Need to download... | Command / Tool |
|---------------------|----------------|
| **Video from YouTube** | `yt-dlp -f "bestvideo+bestaudio/best" URL` |
| **Video from Bilibili** | `yt-dlp --cookies-from-browser chrome URL` |
| **Audio only (MP3)** | `yt-dlp -x --audio-format mp3 --audio-quality 0 URL` |
| **Playlist (all videos)** | `yt-dlp --playlist-items 1-50 --download-sections "*00:00-10:00" URL` |
| **Specific timestamp section** | `yt-dlp --download-sections "*01:30-05:00" URL` |
| **Live stream (record)** | `yt-dlp --live-from-start --no-part URL` |
| **Multi-threaded file** | `aria2c -x 16 -s 16 URL` |
| **Torrent** | `aria2c --seed-time=0 magnet:?xt=urn:btih:...` |
| **Batch images (gallery)** | `gallery-dl --range 1-50 "https://example.com/gallery"` |
| **Pixiv artist batch** | `gallery-dl "https://www.pixiv.net/en/users/XXXXX/artworks"` |
| **Twitter media** | `gallery-dl "https://twitter.com/user/status/XXXXX"` |
| **Spotify to MP3** | `spotdl https://open.spotify.com/track/XXXXX` |
| **Site mirror** | `wget --mirror --convert-links -p URL` |
| **Resume interrupted** | `wget -c URL` |

## Advanced yt-dlp Usage

bash
# Download with best quality, merge to MKV
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mkv URL

# Download subtitles/captions
yt-dlp --write-subs --write-auto-subs --sub-lang en,ja URL

# Extract audio only (best quality)
yt-dlp -x --audio-format best URL

# Download entire playlist
yt-dlp --playlist-start 1 --playlist-end 50 "PLAYLIST_URL"

# Download chapter markers
yt-dlp --embed-chapters URL

# Use browser cookies (for age-restricted content)
yt-dlp --cookies-from-browser chrome URL

# Custom output filename
yt-dlp -o "%(title)s - %(id)s.%(ext)s" URL

# Download limit (speed in bytes, e.g., 1M = 1MB/s)
yt-dlp -r 1M URL
## Search Techniques

### Google Dorks

| Search Query | Finds |
|--------------|-------|
| `site:drive.google.com "keyword"` | Google Drive shared files |
| `site:github.com "keyword" filetype:pdf` | PDFs on GitHub |
| `site:*.book "ebook name" pdf` | Free ebooks |
| `"index of" "folder name"` | Directory listings |
| `intitle:"index of" mp3 "album"` | Music archives |
| `site:archive.org "search term"` | Internet Archive content |
| `inurl:download "software name"` | Direct download links |

### Chinese Cloud Drive Search

| Engine | URL | Notes |
|--------|-----|-------|
| **盘搜搜** | pandocs.com | Aggregates multiple sources |
| **盘多多** | panduoduo.net | Media-focused |
| **小昭** | xiaozhao2.com | General search |
| **阿里云搜索** | aliypan.cn | Alibaba drive specific |
| **百度云搜索** | baiduyun.me | Baidu Pan focused |

### Resource Site Directories

| Category | Recommended Sites |
|----------|-------------------|
| **Academic Papers** | libgen.is, sci-hub.se, arxiv.org, scholar.google.com |
| **Ebooks** | z-lib.org, annas-archive.org, libgen.is |
| **Software** | github.com, sourceforge.net, filehippo.com |
| **Stock Media** | pexels.com, pixabay.com, unsplash.com (images); pixabay.com/music (audio) |
| **Courses** | github.com/nbdev/awesome-courses, ftmk.top (Chinese) |
| **Fonts** | fonts.google.com, fontsfree.net |

## Chinese Ecosystem Tools

bash
# Download from Chinese sites with browser cookies
yt-dlp --cookies-from-browser chrome "https://www.bilibili.com/video/BV1xx411c7XD"

# gallery-dl for Chinese platforms
pip3 install gallery-dl
gallery-dl "https://www.pixiv.net/en/users/XXXXX"        # Pixiv
gallery-dl "https://twitter.com/user/status/XXXXX"      # Twitter
gallery-dl "https://www.deviantart.com/artist/art"      # DeviantArt

# aria2 for 百度网盘 (Baidu Pan) - requires pandownload or similar helper
aria2c -x 16 -s 16 "direct_download_link"
## Common Workflows

### Batch Download Images by Tags

bash
# Download from multiple galleries
gallery-dl --range 1-20 \
  "https://www.pixiv.net/en/tags/landscape/artworks" \
  "https://www.pixiv.net/en/tags/sunset/artworks"

# Save to specific directory
gallery-dl --dest-cwd ~/Downloads/pixiv \
  "https://www.pixiv.net/en/users/XXXXX/artworks"
### Download Full Album/Playlist

bash
# YouTube playlist to MP3
yt-dlp -x --audio-format mp3 \
  --playlist-start 1 \
  --playlist-end 50 \
  "https://www.youtube.com/playlist?list=XXXXX"

# Spotify playlist
spotdl https://open.spotify.com/playlist/XXXXX
### Mirror a Website

bash
# Complete website mirror with wget
wget --mirror \
     --convert-links \
     --adjust-extension \
     --page-requisites \
     --no-parent \
     --no-host-directories \
     -e robots=off \
     https://example.com
## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Rate limited / 403 error** | Use `--cookies-from-browser` or export cookies from browser |
| **Video unavailable** | Try `--geo-bypass` or `--proxy socks5://localhost:7890` |
| **Bilibili download fails** | Login in browser, export cookies, use `--cookies cookies.txt` |
| **Slow download** | Use `aria2c -x 16 -s 16` for multi-threaded |
| **Corrupted file** | Re-download with `--no-part` flag |
| **Missing subtitles** | Use `--write-subs --write-auto-subs` |

## Environment Setup

bash
# Add to ~/.bashrc or ~/.zshrc for persistent aliases
alias ytdl="yt-dlp -f 'bestvideo+bestaudio/best'"
alias ytmp3="yt-dlp -x --audio-format mp3 --audio-quality 0"
alias aria="aria2c -x 16 -s 16 -d ~/Downloads"

# Export cookies from browser for yt-dlp
export COOKIES_FILE=~/cookies.txt
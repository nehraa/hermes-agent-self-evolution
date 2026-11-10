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
./scripts/dl-file.sh "https://example.com/file.zip"         # Direct file
./scripts/dl-gallery.sh "https://example.com/gallery"        # Batch images
./scripts/dl-torrent.sh "magnet:?xt=urn:btih:..."           # Torrents
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
| **Best quality video** | `yt-dlp -f best URL` |
| **Playlist entire** | `yt-dlp --playlist-start 1 --playlist-end 50 URL` |
| **Speed limit/throttle** | `aria2c -x 16 -s 16 URL` |
| **Resume interrupted** | `aria2c -c URL` |
| **Torrent** | `aria2c magnet:?xt=urn:btih:...` |
| **Images from gallery** | `gallery-dl URL` |
| **Pixiv artist batch** | `gallery-dl --range 1-50 https://www.pixiv.net/users/XXXXX` |
| **Twitter media** | `gallery-dl "https://twitter.com/user/status/..."` |
| **Spotify to MP3** | `spotdl https://open.spotify.com/track/...` |
| **Spotify playlist** | `spotdl "https://open.spotify.com/playlist/..."` |
| **Site mirror** | `wget --mirror -p --adjust-extension URL` |
| **Recursive download** | `wget -r -l 2 -np URL` |

## Advanced Usage

### yt-dlp Options

bash
# Download with custom filename
yt-dlp -o "%(title)s.%(ext)s" URL

# Download subtitles
yt-dlp --write-subs --sub-lang en,zh-Hans URL

# Download thumbnail
yt-dlp --write-thumbnail URL

# Download with cookies (for age-restricted content)
yt-dlp --cookies-from-browser chrome URL

# Select specific format
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" URL

# Extract audio only
yt-dlp -x --audio-format flac URL

# Download age-restricted (use cookies)
yt-dlp --cookies cookies.txt "https://www.youtube.com/watch?v=..."

# Bilibili series/playlist
yt-dlp --playlist-end 50 --cookies cookies.txt "https://www.bilibili.com/bangumi/play/..."
### aria2c Options

bash
# Multi-threaded download (16 connections)
aria2c -x 16 -s 16 URL

# Multiple files
aria2c file1.txt file2.txt

# Download from text file (one URL per line)
aria2c -i urls.txt

# Resume partial download
aria2c -c URL

# Limit bandwidth
aria2c --max-download-limit=1M URL

# Concurrent torrent + seed
aria2c --seed-time=60 --max-upload-limit=50K file.torrent
### gallery-dl Options

bash
# Download to specific folder
gallery-dl -D ./downloads URL

# Download with custom naming
gallery-dl --destination "{site}/{user}/{id}.{extension}" URL

# Filter by extension
gallery-dl --filter "extension not in ['gif', 'webp']" URL

# Limit downloads
gallery-dl --range 1-20 URL

# Use authentication
gallery-dl --username USER --password PASS URL

# Download comments
gallery-dl --comments URL
### ffmpeg Media Conversion

bash
# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec mp3 audio.mp3

# Convert format
ffmpeg -i input.mkv -codec copy output.mp4

# Trim video
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4

# Lower quality/smaller file
ffmpeg -i input.mp4 -crf 28 -c:v libx264 -preset fast output.mp4

# Extract frames
ffmpeg -i video.mp4 -vf fps=1/10 frame_%04d.png

# Merge audio + video
ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a aac output.mp4
## Search Strategies

### Google Dorks for Finding Resources

bash
# Find downloadable PDFs
filetype:pdf "topic"
intitle:"index of" pdf

# Find direct download links
"download" "pdf" site:edu filetype:pdf
ext:pdf "username" "password"

# Find software
"download" "software" filetype:exe
inurl:"download" "software"

# Find images
filetype:png OR filetype:jpg "keyword"

# Find ebooks
filetype:epub "book title"
filetype:mobi "topic"
### Chinese Cloud Drive Search

| Engine | URL | Notes |
|--------|-----|-------|
| **云盘狗** | https://ypgou.com | 百度/阿里/夸克聚合 |
| **盘搜搜** | https://www.pansou.com | 多引擎聚合 |
| **盘多多** | https://www.panduoduo.net | 资源丰富 |
| **大力盘** | https://dalipan.com | 百度云为主 |
| **小漾搜索** | https://xiaoyangso.com | 综合搜索 |

### Academic Resources

| Resource | URL | Type |
|----------|-----|------|
| **Google Scholar** | https://scholar.google.com | Papers, citations |
| **Sci-Hub** | https://sci-hub.se | Paywalled papers |
| **LibGen** | https://libgen.is | Books, papers |
| **Z-Library** | https://z-lib.is | Ebooks |
| **arXiv** | https://arxiv.org | Preprints |
| **Semantic Scholar** | https://www.semanticscholar.org | Academic search |

### Stock Assets

| Type | Sources |
|------|---------|
| **Images** | Unsplash, Pexels, Pixabay, Stocksnap |
| **Video** | Pexels Video, Coverr, Videvo |
| **Music** | Free Music Archive, ccMixter, Incompetech |
| **Icons** | Font Awesome, Heroicons, Phosphor |
| **Fonts** | Google Fonts, Font Squirrel, DaFont |

## Common Workflows

### Download YouTube Playlist to MP3

bash
yt-dlp --playlist-start 1 \
       --playlist-end 50 \
       -x --audio-format mp3 \
       --audio-quality 0 \
       -o "%(playlist_title)s/%(title)s.%(ext)s" \
       "PLAYLIST_URL"
### Batch Download from Multiple Sources

bash
#!/bin/bash
# Create download list
cat > urls.txt << 'EOF'
https://example.com/video1.mp4
https://example.com/video2.mp4
https://example.com/video3.mp4
EOF

# Download all with aria2
aria2c -i urls.txt -j 5 -x 3 -s 3
### Download Twitter/X Media from Thread

bash
# Get tweet ID from URL
gallery-dl "https://twitter.com/user/status/123456789"

# Download with best quality images
gallery-dl --no-check-certificate \
           --dest "{{site}}/{{user}}" \
           "https://twitter.com/user/status/..."
### Extract Audio from Video Playlists

bash
# Download entire playlist as MP3
yt-dlp --extract-audio \
       --audio-format mp3 \
       --audio-quality 0 \
       --yes-playlist \
       "PLAYLIST_URL"

# Convert to 128kbps for smaller files
yt-dlp -x --audio-format mp3 --audio-quality 128k "VIDEO_URL"
## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Rate limited / 403 error** | Use `--cookies-from-browser` or export cookies from browser |
| **Age-restricted content** | Use cookies from logged-in browser session |
| **Download too slow** | Use `aria2c -x 16 -s 16` for multi-threaded download |
| **Incomplete file** | Use `aria2c -c` to resume interrupted downloads |
| **Format not available** | Check available formats: `yt-dlp --list-formats URL` |
| **Bilibili download fails** | Export cookies from browser, use `--cookies cookies.txt` |
| **Spotdl not finding match** | Try `--match-filters` or search with `--search-query` |
| **gallery-dl 403 error** | Use `--cookies` from browser extension (EditThisCookie) |

## Environment Setup

bash
# macOS prerequisites
xcode-select --install
brew install yt-dlp aria2 ffmpeg wget

# Python tools
pip3 install gallery-dl spotdl

# Verify installation
yt-dlp --version
aria2c --version
ffmpeg -version
gallery-dl --version
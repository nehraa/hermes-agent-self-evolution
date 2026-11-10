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
| **Entire playlist** | `yt-dlp --yes-playlist -f "best" URL` |
| **Live stream** | `yt-dlp -f "best" --live-from-start URL` |
| **Subtitles/captions** | `yt-dlp --write-subs --sub-lang en URL` |
| **Speed up download** | `aria2c -x16 -s16 URL` (16 connections) |
| **Resume interrupted** | `wget -c URL` or `aria2c --continue URL` |
| **Batch images from gallery** | `gallery-dl URL` |
| **Images from Pixiv/Twitter** | `gallery-dl "https://twitter.com/user/status/..."` |
| **Spotify track/album** | `spotdl https://open.spotify.com/track/...` |
| **Full Spotify playlist** | `spotdl "https://open.spotify.com/playlist/..."` |
| **Torrent file** | `aria2c "magnet:?xt=urn:btih:..."` |
| **Mirror entire site** | `wget --mirror -np -r URL` |
| **Convert video format** | `ffmpeg -i input.mp4 output.avi` |
| **Extract audio from video** | `ffmpeg -i video.mp4 -vn audio.mp3` |
| **Trim video clip** | `ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 output.mp4` |

## Advanced yt-dlp Options

bash
# Best quality (merge best video + best audio)
yt-dlp -f "bestvideo+bestaudio/best" URL

# Specific format (e.g., 720p)
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" URL

# Download with custom filename pattern
yt-dlp -o "%(title)s-%(id)s.%(ext)s" URL

# Download to specific directory
yt-dlp -o "/path/to/downloads/%(title)s.%(ext)s" URL

# Bypass geo-restrictions
yt-dlp --geo-bypass URL

# Use specific proxy
yt-dlp --proxy "socks5://127.0.0.1:1080" URL

# Download rate limit (500K)
yt-dlp -r 500K URL

# Download thumbnail + subtitles + description
yt-dlp --write-thumbnail --write-subs --write-info-json URL

# Authentication (if needed)
yt-dlp -u "username" -p "password" URL
## Resource Search Engines

### Cloud Drive Search (Chinese)

| Engine | URL | Notes |
|--------|-----|-------|
| **云盘搜索** | pandavip.com | 百度网盘资源的聚合搜索 |
| **小昭挖** | xiaozhaow.com | 中文网盘资源搜索引擎 |
| **UP云搜** | upyun.so | 支持阿里云、百度云、夸克等 |
| **盘搜搜** | pansoso.com | 多种网盘资源聚合 |
| **盘多多** | panduoduo.net | 老牌网盘搜索 |

### Google Dorks for Downloads

bash
# Find specific file types
filetype:pdf "search query"
filetype:epub "search query"
filetype:mobi "search query"

# Find software
"search query" filetype:exe
"search query" filetype:iso
"search query" filetype:torrent

# Find academic papers
site:libgen.is "search query"
site:arxiv.org "search query"
site:sci-hub.se "search query"

# Find courses/materials
"search query" filetype:pdf
intitle:"index of" "course name"
inurl:"download" "course name"

# Combined examples
filetype:pdf "machine learning" "2023"
site:github.com "search query" download
intitle:"index of" "pdf" "book name"
## Dedicated Resource Sites

### Academic Papers

| Site | URL | Type |
|------|-----|------|
| **Sci-Hub** | sci-hub.se | Paywalled papers (use responsibly) |
| **Library Genesis** | libgen.is | Books, papers, comics |
| **Z-Library** | z-lib.org | Books, papers |
| **arXiv** | arxiv.org | Pre-print papers |
| **Semantic Scholar** | semanticscholar.org | Academic paper search |

### Books & Ebooks

| Site | URL | Format |
|------|-----|--------|
| **Project Gutenberg** | gutenberg.org | Public domain books |
| **Open Library** | openlibrary.org | Lending library |
| **Anna's Archive** | annas-archive.org | Mirror of multiple sources |
| **PDF Drive** | pdfdrive.com | PDF search engine |

### Software

| Site | URL | Notes |
|------|-----|-------|
| **GitHub** | github.com | Open source software |
| **SourceForge** | sourceforge.net | Open source apps |
| **FileHippo** | filehippo.com | Windows software |
| **Softpedia** | softpedia.com | Multi-platform |

### Stock Assets

| Asset Type | Sources |
|------------|---------|
| **Images** | unsplash.com, pexels.com, pixabay.com |
| **Video** | pexels.com/videos, coverr.co, mixkit.co |
| **Music** | freesound.org, incompetech.com, audionautix.com |
| **Icons** | flaticon.com, iconscout.com, fontawesome.com |
| **Fonts** | fonts.google.com, dafont.com, fontsquirrel.com |
| **3D Models** | sketchfab.com, blendermarket.com |

### Courses & Tutorials

| Site | URL | Content |
|------|-----|---------|
| **GitHub Learning** | skills.github.com | Web dev courses |
| **Coursera Audit** | coursera.org | University courses (audit free) |
| **edX Audit** | edx.org | University courses (audit free) |

## Batch Download Patterns

### gallery-dl Configuration

json
{
  "extractor": {
    "base-directory": "./downloads",
    "filename": "{category}/{artist}/{title}.{extension}",
    "download": true,
    "chapter": true,
    "threads": 4
  }
}
bash
# Download from multiple URLs
gallery-dl -f "pattern" url1 url2 url3

# Download user's entire gallery
gallery-dl "https://pixiv.net/users/12345678"

# Download specific image set
gallery-dl --range 1-10 "https://example.com/gallery"
### wget Recursive Mirror

bash
# Mirror entire site (respects robots.txt)
wget --mirror --convert-links --adjust-extension \
  --page-requisites --no-parent https://example.com

# Recursive download of specific file types
wget -r -l2 -A "*.pdf,*.epub" https://example.com/books/

# Download all images from site
wget -r -l1 -nd -H -A "*.jpg,*.png,*.gif" https://example.com/
## aria2c Advanced Usage

bash
# Maximum speed download (16 connections)
aria2c -x16 -s16 -d /path/to/save -o filename URL

# Multiple file download
aria2c -Z file1.pdf file2.zip

# BitTorrent download
aria2c --bt-max-peers=55 /path/to.torrent

# Metalink download
aria2c /path/to/file.metalink

# Download with multiple sources
aria2c -j3 "https://example.com/f" "http://mirror.com/f"

# Sequential download (for slow servers)
aria2c -d /path -o output.file -i url.txt
## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"This video is age-restricted"** | `yt-dlp --age-limit 18 URL` |
| **"Sign in required"** | `yt-dlp --cookies cookies.txt URL` |
| **"Video unavailable"** | Try with `--geo-bypass` or proxy |
| **Slow download speed** | Use `aria2c -x16 -s16` |
| **SSL certificate error** | `--no-check-certificate` flag |
| **Partial download corruption** | Delete file, use `wget -c` or `aria2c --continue` |
| **Rate limited** | Add delay with `--max-rate` or use proxy |

## Quick Reference Cheatsheet

bash
# Video (best quality)
yt-dlp -f "bestvideo+bestaudio" URL

# Audio only → MP3
yt-dlp -x --audio-format mp3 URL

# Batch images
gallery-dl URL

# Fast download
aria2c -x16 -s16 URL

# Resume download
wget -c URL

# Mirror site
wget --mirror -np URL

# Spotify to MP3
spotdl https://open.spotify.com/track/ID

# Torrent
aria2c magnet:?xt=urn:btih:HASH

# Convert video
ffmpeg -i input.mp4 output.mp3
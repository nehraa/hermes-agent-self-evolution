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
| **Entire playlist** | `yt-dlp --yes-playlist URL` |
| **Twitter/X video** | `yt-dlp "https://twitter.com/user/status/..."` |
| **Instagram post** | `gallery-dl "https://instagram.com/p/..."` |
| **Pixiv art collection** | `gallery-dl "https://www.pixiv.net/users/12345"` |
| **Spotify playlist** | `spotdl "https://open.spotify.com/playlist/..."` |
| **Direct file (zip, pdf, etc.)** | `curl -L -O URL` |
| **Torrent** | `aria2c "magnet:?xt=urn:btih:..."` |
| **Site mirroring** | `wget --mirror -p --convert-links URL` |

## Search Resources

### Google Dorks

Use these advanced search operators to find specific file types and content:

bash
# Find PDFs
filetype:pdf "topic"

# Find ebooks
"ebook" OR "ebook" filetype:mobi OR filetype:epub

# Find software
"software" filetype:exe OR filetype:msi

# Find courses
"course" OR "tutorial" "download" site:drive.google.com

# Find academic papers
filetype:pdf "site:arxiv.org OR site:sci-hub.se"

# Find stock assets
"stock photo" OR "stock video" filetype:jpg OR filetype:mp4
| Dork | Purpose |
|------|---------|
| `site:example.com "query"` | Search within specific site |
| `filetype:pdf "query"` | Find PDF documents |
| `intitle:"query"` | Match exact title |
| `inurl:"query"` | Match URL pattern |
| `cache:URL` | View Google's cached version |

### Chinese Cloud Drive Search

Search 百度网盘, 阿里云盘, and 夸克网盘 for Chinese content:

| Engine | URL | Notes |
|--------|-----|-------|
| **云盘搜索** | `https://yunpan.ogfile.com` | Multi-platform search |
| **小云盘** | `https://www.xiaoyunpan.com` | 百度/阿里/夸克 |
| **UP云搜** | `https://www.upyunso.com` | Fast results |
| **盘搜** | `https://www.pansou.com` | Popular choice |

### Resource Site Directories

| Category | Sites |
|----------|-------|
| **General Search** | Library Genesis, Z-Library mirrors, Sci-Hub |
| **Software** | Ninite, FileHippo, OldVersion |
| **Courses** | CourseHub, FreeCoursesOnline, Library Gen |
| **Fonts** | Google Fonts, DaFont, FontSquirrel |
| **Stock Media** | Pexels, Unsplash, Pixabay, Coverr |
| **Academic** | arXiv, Semantic Scholar, JSTOR open access |

## Advanced Techniques

### Multi-threaded Downloads

Use aria2 for faster downloads with segmented fetching:

bash
aria2c -x 16 -s 16 URL
# -x16: 16 connections
# -s16: 16 segments per file
### Batch Downloads

bash
# Download from list of URLs
cat urls.txt | xargs -P 4 -I {} yt-dlp {}

# Download entire website images
gallery-dl --range 1-100 "https://example.com/gallery"

# Recursive site download
wget --recursive --no-parent --accept jpg,png,gif URL
### Extract Audio from Video

bash
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"
ffmpeg -i video.mp4 -vn -acodec mp3 output.mp3
### Resume Interrupted Downloads

bash
wget -c URL
aria2c --continue URL
yt-dlp --continue URL
## Best Practices

1. **Respect rate limits** — Add delays between bulk requests
2. **Use cookies for auth** — Export browser cookies for private content: `yt-dlp --cookies-from-browser chrome`
3. **Check robots.txt** — `wget -d URL | grep robots` to see allowed paths
4. **Use --max-filesize** — Prevent accidental huge downloads
5. **Specify output** — `--output "%(title)s.%(ext)s"` for named files

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "This video is unavailable" | Try `--cookies` with logged-in session |
| Rate limit exceeded | Add `--wait 5` between requests |
| 403 Forbidden | Use `--user-agent` to spoof browser |
| Slow download | Use aria2 with `-x 16 -s 16` |
| Wrong format | List formats with `--list-formats` first |
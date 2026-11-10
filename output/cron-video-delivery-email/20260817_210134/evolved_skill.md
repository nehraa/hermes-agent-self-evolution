---
name: cron-video-delivery-email
description: "Telegram → Gmail SMTP email for cron-produced videos."
category: devops
---

# Cron Video Delivery via Email

When a cron job produces a video and the user requests email delivery instead of real-time Telegram push, replace the Telegram delivery function with `send_email()` using Gmail SMTP via himalaya's stored credentials.

## When to Use

- User requests: "email me the video", "send to my email", "deliver to my inbox"
- Cron-produced videos intended for later consumption (not real-time)
- User prefers email over Telegram for this specific delivery
- Video file is small enough for SMTP attachment (<10–15MB)

## When NOT to Use

| Scenario | Reason | Alternative |
|----------|--------|-------------|
| Files >25MB | Gmail attachment limit exceeded | Upload to cloud storage, send link |
| Real-time push needed | Email has inherent latency | Telegram |
| Inline preview required | Email shows video as attachment | Telegram or cloud link |
| Non-Gmail account | himalaya uses Gmail SMTP | Configure custom SMTP |

## Implementation

### 1. Add `send_email()` Function

Drop-in replacement for existing `send_telegram()` calls:

python
import smtplib
import ssl
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from pathlib import Path


def send_email(file_path: str, subject_context: str, dur_or_size: str = "") -> bool:
    """Send a video file as an email attachment via Gmail SMTP.
    
    Args:
        file_path: Absolute path to the video file.
        subject_context: Short description for email subject (e.g., "Morning news digest").
        dur_or_size: Optional metadata string for logging.
    
    Returns:
        True if email sent successfully, False otherwise.
    
    Recipient: abhinavnehra2203@gmail.com
    Auto-compresses via ffmpeg if file > 10MB.
    """
    SMTP_CEILING = 10 * 1024 * 1024  # 10MB threshold
    RECIPIENT = "abhinavnehra2203@gmail.com"
    
    src_path = Path(file_path)
    if not src_path.exists():
        print(f"[EMAIL] Source file missing: {src_path}")
        return False
    
    # --- Step 1: Compress if necessary ---
    attach_path = src_path
    file_size = src_path.stat().st_size
    
    if file_size > SMTP_CEILING:
        compressed = src_path.with_name(src_path.stem + "_compressed.mp4")
        print(f"[EMAIL] File size {file_size / 1024 / 1024:.1f}MB > 10MB, compressing...")
        
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(src_path),
            "-vcodec", "libx264",
            "-crf", "28",
            "-preset", "fast",
            "-vf", "scale=1280:-2",
            "-acodec", "aac",
            "-b:a", "128k",
            str(compressed)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[EMAIL] Compression failed: {result.stderr}")
            return False
        
        if compressed.exists() and compressed.stat().st_size < file_size:
            attach_path = compressed
            print(f"[EMAIL] Compressed to {compressed.stat().st_size / 1024 / 1024:.1f}MB")
    
    # --- Step 2: Parse himalaya credentials ---
    himalaya_config = Path.home() / ".config" / "himalaya" / "config.toml"
    
    if not himalaya_config.exists():
        print("[EMAIL] himalaya config not found")
        return False
    
    email_addr = None
    smtp_pass = None
    
    for line in himalaya_config.read_text().splitlines():
        line = line.strip()
        if line.startswith("email"):
            email_addr = line.split("=", 1)[1].strip().strip('"').strip("'")
        elif "auth.raw" in line or "password" in line.lower():
            smtp_pass = line.split("=", 1)[1].strip().strip('"').strip("'")
    
    if not email_addr or not smtp_pass:
        print("[EMAIL] Missing email or password in himalaya config")
        return False
    
    # --- Step 3: Build and send email ---
    subject = f"Video: {subject_context}"
    body = f"Attached video ({dur_or_size or 'see attachment'})"
    
    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = RECIPIENT
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    with open(attach_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    
    encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{attach_path.name}"'
    )
    msg.attach(part)
    
    # --- Step 4: Send via Gmail SMTP ---
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_addr, smtp_pass)
            server.sendmail(email_addr, RECIPIENT, msg.as_string())
        print(f"[EMAIL] Sent successfully: {subject}")
        return True
    except Exception as e:
        print(f"[EMAIL] Send failed: {e}")
        return False
### 2. Integration Example

Replace Telegram delivery in your cron script:

python
# Before (Telegram delivery)
# send_telegram(video_path, "Daily video ready")

# After (Email delivery on user request)
send_email(video_path, "Daily video ready", "5 min")
### 3. Prerequisites

| Requirement | Setup Command |
|-------------|---------------|
| himalaya configured | `himalaya config` or edit `~/.config/himalaya/config.toml` |
| Gmail app password | Google Account → Security → 2FA → App Passwords |
| ffmpeg installed | `sudo apt install ffmpeg` |

### 4. himalaya Config Format

Ensure `~/.config/himalaya/config.toml` contains:

toml
email = "your.email@gmail.com"
auth.raw = "your-16-char-app-password"
## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Source file missing` | File path incorrect | Verify `file_path` argument |
| `himalaya config not found` | himalaya not configured | Run `himalaya config` |
| `Missing email or password` | Config parse failed | Check config format matches |
| `SMTP authentication failed` | Wrong app password | Regenerate Gmail app password |
| `Compression failed` | ffmpeg error | Check ffmpeg installation |

## Logging

All email operations print prefixed `[EMAIL]` messages for grep filtering:

bash
grep "\[EMAIL\]" /path/to/cron.log
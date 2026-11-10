---
name: cron-video-delivery-email
description: "Telegram → Gmail SMTP email for cron-produced videos."
category: devops
---

# Cron Video Delivery via Email

When a cron job produces a video and the user requests email delivery instead of immediate Telegram push, use this `send_email()` function that leverages Gmail SMTP with himalaya's stored credentials.

## When to Use

- User says "email me the video", "send to my email", "deliver later", or "rather than at the same time"
- Video file is small enough for SMTP attachment (<10–15MB)
- User has a Gmail account configured in `~/.config/himalaya/config.toml`

## When NOT to Use

| Scenario | Alternative |
|----------|-------------|
| Files >25MB | Gmail hard limit; use cloud storage + link |
| Real-time push required | Telegram is faster |
| Inline preview needed | Email renders videos as attachments only |
| Non-Gmail account | Requires SMTP configuration changes |

## Implementation

### Add `send_email()` to the Script

This function is a drop-in replacement for any `send_telegram()` call. It reads credentials from himalaya's config, auto-compresses large files, and sends via Gmail SMTP.

python
import smtplib
import ssl
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from pathlib import Path


def send_email(file_path, subject_context="", dur_or_size=""):
    """Send a video file as an email attachment via Gmail SMTP.

    Args:
        file_path: Path to the video file.
        subject_context: Optional string to append to the email subject.
        dur_or_size: Optional metadata (passed for logging consistency).

    Returns:
        bool: True if email sent successfully, False otherwise.

    Recipient: abhinavnehra2203@gmail.com
    Auto-compresses via ffmpeg if file > 10MB.
    """
    src_path = Path(file_path)
    if not src_path.exists():
        print(f"[Email] Source file not found: {src_path}")
        return False

    SMTP_CEILING = 10 * 1024 * 1024  # 10MB threshold for compression
    attach_path = src_path

    # Compress if file exceeds size threshold
    if src_path.stat().st_size > SMTP_CEILING:
        compressed = src_path.with_name(src_path.stem + "_compressed.mp4")
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(src_path),
                "-vcodec", "libx264",
                "-crf", "28",
                "-vf", "scale=1280:-2",
                "-acodec", "aac",
                "-b:a", "128k",
                str(compressed),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[Email] Compression failed: {result.stderr}")
            return False
        if compressed.exists():
            attach_path = compressed

    # Parse SMTP credentials from himalaya config
    cfg_path = Path.home() / ".config" / "himalaya" / "config.toml"
    email_addr = None
    smtp_pass = None

    try:
        for line in cfg_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("email =") and email_addr is None:
                email_addr = line.split("=", 1)[1].strip().strip('"')
            if "auth.raw" in line and smtp_pass is None:
                smtp_pass = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        print(f"[Email] HIMALAYA config not found at {cfg_path}")
        return False

    if not email_addr or not smtp_pass:
        print("[Email] Missing email or SMTP password in config")
        return False

    # Build email
    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = "abhinavnehra2203@gmail.com"
    subject = "Cron Video Delivery"
    if subject_context:
        subject += f" — {subject_context}"
    msg["Subject"] = subject

    body = f"Video file attached: {attach_path.name}"
    if dur_or_size:
        body += f"\n{dur_or_size}"
    msg.attach(MIMEText(body, "plain"))

    # Attach video
    try:
        with open(attach_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{attach_path.name}"'
        )
        msg.attach(part)
    except IOError as e:
        print(f"[Email] Failed to read attachment: {e}")
        return False

    # Send via Gmail SMTP
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_addr, smtp_pass)
            server.sendmail(email_addr, "abhinavnehra2203@gmail.com", msg.as_string())
        print(f"[Email] Sent: {attach_path.name}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[Email] Authentication failed — check App Password")
        return False
    except smtplib.SMTPException as e:
        print(f"[Email] SMTP error: {e}")
        return False
### Required Setup

1. **Himalaya Config**: Ensure `~/.config/himalaya/config.toml` contains:
   ```toml
   email = "your.gmail@gmail.com"
   # auth.raw should point to an app-specific password
   ```

2. **Gmail App Password**: Gmail requires an [App Password](https://support.google.com/accounts/answer/185833), not your regular password. Generate one under Google Account → Security → 2-Step Verification → App passwords.

### Usage Example

python
# Instead of:
# send_telegram(video_path, title, metadata)

# Use:
success = send_email(
    video_path,
    subject_context="Daily Report",
    dur_or_size=f"Duration: {duration}s | Size: {size}"
)
### Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Authentication failed` | Wrong app password | Regenerate from Google Account settings |
| `SMTP recipient refused` | Attachment too large | Compression already handles up to 10MB |
| `Config not found` | Wrong himalaya path | Verify `~/.config/himalaya/config.toml` exists |
| `Compression failed` | ffmpeg error | Check ffmpeg installation and source file |
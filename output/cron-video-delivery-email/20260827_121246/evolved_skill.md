---
name: cron-video-delivery-email
description: "Telegram → Gmail SMTP email for cron-produced videos."
category: devops
---

# Cron Video Delivery via Email

When a cron job produces a video and you want it emailed rather than pushed to Telegram at runtime, use the `send_email()` function below instead of `send_telegram()`. It sends via Gmail SMTP using credentials stored by himalaya.

## When to Use

| Scenario | Use Email? |
|----------|------------|
| User requests "email me the video" or "send to my email" | ✅ Yes |
| User wants delivery separate from cron runtime | ✅ Yes |
| Real-time push required | ❌ No — use Telegram |
| File >25MB (Gmail attachment limit) | ❌ No — use alternative |
| Inline preview needed | ❌ No — email shows as attachment only |

**Prerequisites:**
- Gmail account configured in `~/.config/himalaya/config.toml`
- Video file ≤25MB (auto-compressed to ≤10MB if larger)

## Implementation

### `send_email()` Function

Drop-in replacement for any `send_telegram()` call:

python
def send_email(file_path, subject_context, dur_or_size):
    """Send a video file as an email attachment via Gmail SMTP.

    Args:
        file_path: Path to the video file.
        subject_context: String to include in the email subject.
        dur_or_size: Human-readable duration or file size for logging.

    Returns:
        True if sent successfully, False otherwise.

    Behavior:
        - Recipient: abhinavnehra2203@gmail.com
        - Auto-compresses via ffmpeg if file > 10MB
        - Reads SMTP credentials from ~/.config/himalaya/config.toml
    """
    import smtplib
    import ssl
    import subprocess
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.encoders import encode_base64
    from pathlib import Path

    src_path = Path(file_path)
    if not src_path.exists():
        print(f"[Email] Source file not found: {src_path}")
        return False

    SMTP_CEILING = 10 * 1024 * 1024  # 10MB
    attach_path = src_path

    # Compress if file exceeds 10MB
    if src_path.stat().st_size > SMTP_CEILING:
        compressed = src_path.with_name(src_path.stem + "_compressed.mp4")
        print(f"[Email] Compressing {src_path.name} → {compressed.name}")

        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(src_path),
            "-vcodec", "libx264",
            "-crf", "28",
            "-vf", "scale=1280:-2",
            "-acodec", "aac",
            "-b:a", "128k",
            str(compressed)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[Email] Compression failed: {result.stderr}")
            return False

        if compressed.exists():
            attach_path = compressed
            print(f"[Email] Compression complete: {compressed.stat().st_size / 1024 / 1024:.1f}MB")

    # Parse SMTP credentials from himalaya config
    # Avoids dependency on toml module
    cfg_path = Path.home() / ".config/himalaya/config.toml"
    if not cfg_path.exists():
        print("[Email] himalaya config not found")
        return False

    email_addr = None
    smtp_pass = None

    for line in cfg_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("email =") and email_addr is None:
            email_addr = line.split("=", 1)[1].strip().strip('"')
        if "auth.raw" in line and smtp_pass is None:
            smtp_pass = line.split("=", 1)[1].strip().strip('"')

    if not email_addr or not smtp_pass:
        print("[Email] SMTP credentials not found in config")
        return False

    # Build email
    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = "abhinavnehra2203@gmail.com"
    msg["Subject"] = f"Video: {subject_context} ({dur_or_size})"

    body = f"""Cron video ready for delivery.

Subject: {subject_context}
Duration/Size: {dur_or_size}
File: {attach_path.name}
"""
    msg.attach(MIMEText(body, "plain"))

    # Attach video
    with open(attach_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{attach_path.name}"'
    )
    msg.attach(part)

    # Send via Gmail SMTP
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_addr, smtp_pass)
            server.send_message(msg)

        print(f"[Email] Sent successfully to abhinavnehra2203@gmail.com")
        print(f"[Email] Attachment: {attach_path.name} ({attach_path.stat().st_size / 1024 / 1024:.1f}MB)")

        # Cleanup compressed file after successful send
        if attach_path != src_path and attach_path.exists():
            attach_path.unlink()
            print(f"[Email] Cleaned up compressed file")

        return True

    except Exception as e:
        print(f"[Email] Failed to send: {e}")
        return False
## Usage Example

python
# In your cron script, replace send_telegram() with:
success = send_email(
    file_path="/path/to/output/video.mp4",
    subject_context="Morning Standup Recording",
    dur_or_size="2:34"
)

if not success:
    print("Warning: Email delivery failed, consider Telegram fallback")
## Error Handling

| Error | Action |
|-------|--------|
| Source file missing | Log error, return False |
| Compression fails | Log stderr, return False |
| Config not found | Log error, return False |
| SMTP auth fails | Log error, return False |
| Send fails | Log exception, return False |

## File Size Limits

| Size Range | Behavior |
|------------|----------|
| ≤10MB | Sent as-is |
| 10–25MB | Auto-compressed to ~10MB via CRF 28 + 720p scale |
| >25MB | Not supported; suggest Telegram or cloud storage |

## Cleanup

The function automatically deletes the compressed file after successful email delivery to avoid disk bloat.
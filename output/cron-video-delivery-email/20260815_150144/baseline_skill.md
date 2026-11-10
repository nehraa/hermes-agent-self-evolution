---
name: cron-video-delivery-email
description: "Telegram → Gmail SMTP email for cron-produced videos."
category: devops
---

# Cron Video Delivery via Email

When a cron produces a video and the user wants it emailed rather than pushed to Telegram at run time, swap the in-script Telegram delivery for a `send_email()` function that uses Gmail SMTP via himalaya's stored credentials.

## When to use

- User says "email me the video", "send to my email", "rather than sending at the same time", "deliver later"
- Video file is small enough for an SMTP attachment (<10-15MB)
- User has a Gmail account configured in `~/.config/himalaya/config.toml`

## When NOT to use

- Files >25MB (Gmail limit)
- Real-time push required (Telegram is faster)
- Inline preview needed (email shows as attachment only)

## Implementation

### 1. Add `send_email()` to the script

Drop-in replacement for any `send_telegram()` function:

```python
def send_email(file_path, subject_context, dur_or_size):
    """Send a video file as an email attachment via Gmail SMTP.
    Recipient: abhinavnehra2203@gmail.com.
    Auto-compresses via ffmpeg if file > 10MB.
    """
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.encoders import encode_base64
    from pathlib import Path

    src_path = Path(file_path)
    if not src_path.exists():
        print(f"Email: source missing at {src_path}")
        return False

    SMTP_CEILING = 10 * 1024 * 1024
    attach_path = src_path
    if src_path.stat().st_size > SMTP_CEILING:
        compressed = src_path.with_name(src_path.stem + "_compressed.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", str(src_path),
            "-vcodec", "libx264", "-crf", "28",
            "-vf", "scale=1280:-2",
            "-acodec", "aac", "-b:a", "128k",
            str(compressed),
        ], capture_output=True)
        if compressed.exists():
            attach_path = compressed

    # Parse SMTP creds from himalaya config (no toml module on this server)
    cfg = Path("/home/Hermes/.config/himalaya/config.toml")
    email_addr = smtp_pass = None
    for line in cfg.read_text().splitlines():
        line = line.strip()
        if line.startswith("email =") and email_addr is None:
            email_addr = line.split("=", 1)[1].strip().strip('"')
        if "auth.raw" in line and smtp_pass is None:
            smtp_pass = line.split("=", 1)[1].strip().strip('"')

    msg = MIMEMultipart()
    msg["From"] = email_addr
    msg["To"] = "abhinavnehra2203@gmail.com"
    msg["Subject"] = f"Subject: {subject_context}"
    msg.attach(MIMEText("Body text", "plain"))

    with open(attach_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=attach_path.name)
        msg.attach(part)

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=ctx)
            server.login(email_addr, smtp_pass)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        print(f"Delivered via email ✓ ({attach_path.stat().st_size // 1024}KB)")
        return True
    except Exception as e:
        print(f"Email delivery failed: {e}")
        return False
```

### 2. Replace the call site

`send_telegram(...)` → `send_email(...)` at the delivery point.

### 3. Update the cron prompt

Replace any "delivered to Telegram" / "send to Telegram" wording with:

```
The script sends the video to abhinavnehra2203@gmail.com via Gmail SMTP
through its own send_email() function — DO NOT include any MEDIA: tags
in your final response.
```

## Pitfalls

- **HTML in captions**: if the original caption had Telegram HTML (`<b>`, `<i>`), strip it for plain-text email body — `re.sub(r"<[^>]+>", "", caption)`.
- **Scope the `re` import**: many scripts don't have `import re` at top. Either add it locally inside the function (`import re as html_re`) or rely on Python's default `re` only if it's already imported at module scope. If unsure, run a smoke test that actually invokes the function.
- **Leave `deliver` field alone**: cron agent's status report still goes to Telegram; the script is the delivery channel. If you want silence, set `deliver: local`.
- **ffmpeg compression takes ~30s on a 5-min video**: budget for it in cron timeouts.

## Reference crons

- `6a4129adef67` (Protocol Study Daily Remotion) — 5 AM, networking protocol videos
- `258253a8f95a` (ISC2 CC Daily Study Video) — 8 AM, cybersecurity study videos
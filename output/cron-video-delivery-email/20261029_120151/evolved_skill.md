---
name: cron-video-delivery-email
description: "Telegram → Gmail SMTP email for cron-produced videos."
category: devops
---

# Cron Video Delivery via Email

Use this skill when a cron job produces a video that should be delivered by email instead of being pushed to Telegram at runtime. The implementation below calls `himalaya`, which uses the account's stored Gmail SMTP credentials and supports attaching the generated video.

## When to Use

- The user asks to “email me the video,” “send it to my email,” or “deliver it later.”
- Real-time Telegram delivery should be replaced with deferred email delivery.
- The video can be compressed to 15 MB or less, which is a conservative limit for Gmail after MIME encoding.
- A Gmail account is already configured for `himalaya`.

## When Not to Use

- The final compressed attachment is likely to exceed Gmail's 25 MB message limit.
- The user needs an inline video preview; email clients will normally show the video only as an attachment.
- Immediate delivery is required; Telegram is usually faster.
- The cron job has not finished writing the video file. Wait until the file is complete before calling the delivery function.

## Prerequisites

1. Install `himalaya` and `ffmpeg`:

   ```bash
   command -v himalaya
   command -v ffmpeg
   ```

2. Configure a Gmail account with Himalaya:

   ```bash
   himalaya account configure
   ```

   Use `smtp.gmail.com` with port `587` and STARTTLS. If the Gmail account uses two-factor authentication, configure an app password or another authentication method supported by Himalaya.

3. Verify that Himalaya can send a test message:

   ```bash
   himalaya template send \
     --subject "Himalaya test" \
     "abhinavnehra2203@gmail.com"
   ```

## Implementation

### 1. Add `send_email()` to the cron script

The function validates the source file, compresses videos larger than 15 MB, sends the file through Himalaya, and removes temporary files automatically.

python
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


DEFAULT_RECIPIENT = "abhinavnehra2203@gmail.com"
MAX_ATTACHMENT_BYTES = 15 * 1024 * 1024


def _compress_video(src_path: Path, output_dir: Path):
    """Compress a video with ffmpeg. Return the output path or None on failure."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("Email: ffmpeg is not installed; cannot compress video")
        return None

    compressed_path = output_dir / f"{src_path.stem}_compressed.mp4"

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(src_path),
        "-vcodec",
        "libx264",
        "-crf",
        "28",
        "-vf",
        "scale=1280:-2",
        "-acodec",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(compressed_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=15 * 60,
    )

    if result.returncode != 0 or not compressed_path.exists():
        print(f"Email: ffmpeg compression failed: {result.stderr[-1000:]}")
        return None

    return compressed_path


def send_email(file_path, subject_context="", dur_or_size="") -> bool:
    """Send a video as an attachment through Himalaya using Gmail SMTP.

    The recipient defaults to abhinavnehra2203@gmail.com and can be
    overridden with VIDEO_DELIVERY_EMAIL. The Himalaya account can be
    selected with HIMALAYA_ACCOUNT.
    """
    src_path = Path(file_path).expanduser()

    if not src_path.is_file():
        print(f"Email: source video not found: {src_path}")
        return False

    recipient = os.environ.get("VIDEO_DELIVERY_EMAIL", DEFAULT_RECIPIENT)
    himalaya = shutil.which("himalaya")
    if not himalaya:
        print("Email: himalaya is not installed or is not on PATH")
        return False

    subject_parts = ["Cron video delivery"]
    if subject_context:
        subject_parts.append(str(subject_context))
    if dur_or_size:
        subject_parts.append(f"({dur_or_size})")
    subject = " - ".join(subject_parts)

    with tempfile.TemporaryDirectory(prefix="cron-video-email-") as temp_dir:
        attach_path = src_path

        if src_path.stat().st_size > MAX_ATTACHMENT_BYTES:
            print(
                f"Email: source is {src_path.stat().st_size / 1024 / 1024:.1f} MB; "
                "compressing"
            )
            compressed_path = _compress_video(src_path, Path(temp_dir))
            if not compressed_path:
                return False
            attach_path = compressed_path

        attachment_size = attach_path.stat().st_size
        if attachment_size > MAX_ATTACHMENT_BYTES:
            print(
                f"Email: attachment is still too large after compression: "
                f"{attachment_size / 1024 / 1024:.1f} MB"
            )
            return False

        command = [
            himalaya,
            "template",
            "send",
            "--subject",
            subject,
            "--attach",
            str(attach_path),
            recipient,
        ]

        account = os.environ.get("HIMALAYA_ACCOUNT")
        if account:
            command[3:3] = ["--account", account]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5 * 60,
            )
        except subprocess.TimeoutExpired:
            print("Email: Himalaya timed out while sending the attachment")
            return False

        if result.returncode != 0:
            print(f"Email: Himalaya failed: {result.stderr or result.stdout}")
            return False

    print(f"Email: sent {attach_path.name} to {recipient}")
    return True
### 2. Replace the Telegram delivery call

Call `send_email()` only after the cron job has fully generated and closed the video file.

python
video_path = Path("/path/to/generated-video.mp4")
size_mb = video_path.stat().st_size / 1024 / 1024

if not send_email(
    video_path,
    subject_context="Scheduled recording",
    dur_or_size=f"{size_mb:.1f} MB",
):
    raise RuntimeError("Video email delivery failed")
Do not leave both Telegram and email delivery enabled unless the user explicitly wants duplicate delivery.

## Configuration

Use environment variables when the cron environment supports them:

bash
export VIDEO_DELIVERY_EMAIL="abhinavnehra2203@gmail.com"
export HIMALAYA_ACCOUNT="gmail"
`HIMALAYA_ACCOUNT` is optional. Omit it when Himalaya has only one configured account or already selects the account through its configuration.

## Operational Notes

- Keep the recipient address configurable; do not place SMTP passwords or app passwords in the script.
- Himalaya reads and manages the stored Gmail credentials. The script should not parse or log secrets from `~/.config/himalaya/config.toml`.
- The 15 MB threshold leaves room for MIME/base64 encoding and Gmail's 25 MB total-message limit.
- Compression changes the video's dimensions, bitrate, and quality. Use the original file if the user requires lossless delivery.
- The temporary compressed file is deleted after the send attempt, including when sending fails.
- Treat a `False` return value as a delivery failure so cron can report a non-zero exit status.

## Troubleshooting

### Authentication failure

- Run `himalaya account list` and confirm the correct account exists.
- Verify that Gmail SMTP is enabled.
- For accounts with two-factor authentication, use an app password or a Himalaya-supported OAuth credential flow.
- Test sending a small message without an attachment.

### Attachment rejected

- Check whether the compressed file remains larger than 15 MB.
- Lower the ffmpeg CRF value for stronger compression.
- Reduce the maximum width in the `scale` filter.
- Deliver very large videos through a link or a dedicated file-sharing service instead of email.

### Himalaya command fails

- Confirm the installed Himalaya version supports `himalaya template send --attach`.
- Verify the command manually:

  ```bash
  himalaya template send \
    --subject "Attachment test" \
    --attach "/path/to/video.mp4" \
    "abhinavnehra2203@gmail.com"
  ```

- Inspect stderr for configuration, authentication, or network errors.
- Avoid printing the contents of the Himalaya configuration file because it may contain sensitive credential data.
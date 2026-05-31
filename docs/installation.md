# Installation

## Requirements

- Python 3.10 or newer.
- Optional: FFmpeg / `ffprobe` for media metadata.

The v0.1 scanner uses Python standard library only. It can run without FFmpeg, but reports will contain fewer media metadata signals.

## Clone

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ecommerce-video-duplicate-preflight-skill.git
cd ecommerce-video-duplicate-preflight-skill
```

## Check Python

```bash
python3 --version
```

## Optional FFmpeg

```bash
ffprobe -version
```

If `ffprobe` is missing, the scanner continues with SHA-256 and file inventory signals.

## Validate The Repository

```bash
python3 scripts/validate_repository.py
```


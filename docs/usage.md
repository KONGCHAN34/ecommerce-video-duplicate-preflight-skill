# Usage

## Basic Scan

```bash
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  /path/to/video-folder \
  --output reports/preflight-001
```

Outputs:

- `reports/preflight-001/report.md`
- `reports/preflight-001/results.json`

## Custom Extensions

```bash
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./videos \
  --output ./reports/mp4-only \
  --extensions .mp4 .mov
```

## Adjust Conservative Candidate Grouping

```bash
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./videos \
  --output ./reports/strict \
  --duration-tolerance 0.5 \
  --size-tolerance-ratio 0.04
```

Lower tolerance means fewer near-duplicate candidates and more conservative grouping.

## Codex Prompt

```text
Use the ecommerce-video-preflight Skill to scan ./videos and write the report to ./reports/batch-01. Explain which files are low-risk publish-first candidates, which need manual review, and which should be sent for re-editing. Do not move, delete, upload, or publish any media files.
```


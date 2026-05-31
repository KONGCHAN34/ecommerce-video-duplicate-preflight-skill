---
name: ecommerce-video-preflight
description: Use this skill when content, editing, or e-commerce teams need to scan local video folders before publishing, detect exact or likely near-duplicate videos, rank duplicate-risk levels, and generate a human-reviewable preflight report without deleting or moving files.
---

# Ecommerce Video Preflight Skill

## Purpose

Help teams preflight local video assets before publishing to e-commerce, short-video, or advertising platforms. The Skill identifies exact duplicates and likely near-duplicate candidates, then produces a report that helps humans choose which videos to publish first, review, or send back for re-editing.

This Skill is a risk-screening workflow. It does not guarantee platform approval, copyright safety, originality, or compliance.

## When To Use

Use this Skill when the user asks to:

- Check many local videos before publishing.
- Find duplicate or similar product videos.
- Rank videos by duplicate-risk before upload.
- Compare edited variants of the same video.
- Prepare a review report for a content, editing, or e-commerce team.
- Build a repeatable local workflow for video material QA.

Do not use this Skill to:

- Delete, move, overwrite, upload, or publish files automatically.
- Claim a platform will approve or reject a video.
- Determine legal copyright ownership.
- Identify people or sensitive attributes.
- Work from nonexistent samples or only a title/link preview.

## Inputs

Required:

- Local video directory.
- Output report directory.

Optional:

- File extensions to include.
- Similarity thresholds.
- Whether to use `ffprobe` metadata when available.
- Whether to include JSON output.

## Outputs

Produce:

- `report.md`: human-readable review report.
- `results.json`: machine-readable scan results.
- Video inventory with path, size, extension, SHA-256, and metadata if available.
- Exact duplicate groups.
- Likely near-duplicate candidate groups.
- Recommendations: `publish_first`, `manual_review`, `re_edit`, or `ignore`.
- Failure notes and missing dependency warnings.

## Process

1. Confirm scan scope and output directory.
2. Keep input media read-only.
3. Build a video inventory: path, size, extension, modified time, SHA-256.
4. If `ffprobe` is available, collect duration, resolution, codec, and bitrate.
5. Detect exact duplicates by SHA-256.
6. Detect likely near-duplicates using conservative metadata grouping.
7. Assign risk levels:
   - `low`: no matching hash or strong metadata similarity found.
   - `medium`: similar metadata, likely same product/session/export family.
   - `high`: exact duplicate hash or multiple strong similarity signals.
8. Write Markdown and JSON reports.
9. Clearly separate algorithmic evidence from publishing decisions.
10. Ask before any destructive or external action.

## Quality Checklist

- The report includes scan path, timestamp, method, and limitations.
- Exact duplicate and near-duplicate candidates are separated.
- Each finding includes file paths and evidence.
- The report avoids guaranteed platform approval claims.
- Missing dependencies are reported as warnings, not hidden.
- The workflow does not alter input files.
- Recommendations are phrased as review priorities, not final truth.

## Failure Modes

- `ffprobe` missing: continue with file hash and size-based inventory, then warn that metadata is limited.
- Unreadable files: list them in the report and continue scanning other files.
- No video files found: report empty scan and ask for a valid directory.
- Too many candidates: group by strongest evidence and tell the user to review high-risk groups first.
- User asks to delete or move files: stop and ask for explicit confirmation.

## Examples

Scan a publishing batch:

```bash
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./product-videos \
  --output ./reports/product-videos-preflight
```

Prompt for Codex:

```text
Use the ecommerce-video-preflight Skill to scan ./product-videos. Generate a report in ./reports/batch-01 and explain which videos should be published first, reviewed, or sent for re-editing. Do not delete, move, upload, or publish files.
```


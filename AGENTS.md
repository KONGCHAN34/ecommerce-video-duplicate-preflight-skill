# AGENTS.md

## Project Purpose

This repository packages a Codex Skill for e-commerce video duplicate preflight checks.

The project helps content, editing, and e-commerce operations teams scan local video folders before publishing, identify exact and likely near-duplicate assets, and produce a reviewable report for publishing priority and manual review.

## Rules For Agents

- Read `.agents/skills/ecommerce-video-preflight/SKILL.md` before changing workflow behavior.
- Keep the project public-safe: do not include private video files, platform credentials, cookies, tokens, internal account data, or unpublished customer material.
- Do not claim the tool guarantees platform approval, copyright safety, originality, or compliance.
- Do not add workflows that automatically delete, move, overwrite, upload, or publish media files.
- Keep every default operation read-only for input media.
- If changing report fields, update README, docs, examples, and validation expectations together.
- If changing the scanner CLI, update `docs/usage.md` and at least one example.
- Do not invent users, stars, downloads, adoption, platform partnerships, or external feedback.
- Keep application notes factual and clearly marked as draft material until real public evidence exists.

## Validation

Run before submitting changes:

```bash
python3 scripts/validate_repository.py
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py --help
```


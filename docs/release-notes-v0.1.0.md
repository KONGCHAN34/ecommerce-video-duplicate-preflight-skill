# v0.1.0 Release Notes

Initial public release of Ecommerce Video Duplicate Preflight Skill.

## Added

- Codex Skill for local e-commerce video duplicate preflight workflows.
- Read-only scanner for local video folders.
- Exact duplicate detection using SHA-256.
- Optional media metadata collection through `ffprobe`.
- Conservative likely near-duplicate candidate grouping.
- Markdown and JSON reports.
- Three examples:
  - E-commerce publishing preflight.
  - Editing team review.
  - Batch material cleanup.
- Repository validation script.
- GitHub Actions validation workflow.
- Public-safe governance files and application notes draft.

## Limitations

- v0.1 does not perform perceptual frame hashing.
- v0.1 does not perform audio fingerprinting.
- Reports do not guarantee platform approval or originality.
- Near-duplicate grouping is conservative and should be manually reviewed.


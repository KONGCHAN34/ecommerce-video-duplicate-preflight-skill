# Design

## Design Goals

- Local-first: process files on the user's machine.
- Read-only by default: never change source media.
- Evidence-first: preserve paths, methods, signals, and limitations.
- Conservative: avoid pretending weak signals are final decisions.
- Team-friendly: reports should help non-technical reviewers act.

## V0.1 Detection Strategy

The first release intentionally uses a small, reliable baseline:

- Inventory local video files by extension.
- Compute SHA-256 for exact duplicate detection.
- Use `ffprobe` metadata when available.
- Group likely near-duplicates conservatively by duration bucket, resolution, extension, and file size tolerance.

## Why Not Start With Heavy CV

Frame hashing, audio fingerprinting, and scene detection are useful but require more dependencies, thresholds, and calibration. The v0.1 goal is to make the workflow safe and auditable before adding deeper detection.

## Report Design

The report separates:

- Exact duplicates.
- Likely near-duplicate candidates.
- File-level publishing priority.
- Warnings and limitations.

This structure prevents an algorithmic signal from becoming an unsupported business claim.

## Future Design Direction

- Add perceptual frame hashing as an optional module.
- Add contact sheets for human review.
- Add CSV export for content teams.
- Add richer dependency diagnostics.


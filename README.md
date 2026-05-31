# Ecommerce Video Duplicate Preflight Skill

A local-first Codex Skill for e-commerce content teams to scan video folders before publishing, detect exact or likely near-duplicate assets, and generate a reviewable publishing-priority report.

## Why this exists

E-commerce and short-video platforms often evaluate uploaded videos for repeated, highly similar, or reused material. Content teams may have hundreds of product videos, edited variants, watermarked exports, and historical assets. Manual duplicate review is slow, inconsistent, and hard to audit.

This project turns video duplicate preflight into a repeatable local workflow:

- Scan a folder of local video assets.
- Find exact duplicate files.
- Surface likely near-duplicate candidates using metadata signals in v0.1.
- Produce a report that ranks videos for `publish first`, `review`, or `re-edit`.
- Preserve evidence so a human reviewer can make the final call.

This tool does not guarantee that any platform will approve, reject, rank, or classify a video in a specific way. It is a local preflight aid, not a platform compliance bypass.

## Who should use it

- E-commerce content teams preparing product videos for listing pages or platform feeds.
- Short-video operators choosing which assets to publish first.
- Editing teams comparing multiple exports or re-edits of the same material.
- Performance marketing teams screening ad creative before upload.
- Small brands and merchants managing local video libraries.
- Agent users who want a safe, repeatable Codex workflow for video material review.

## Core features

- Read-only scanning of local folders.
- Exact duplicate detection with SHA-256.
- Optional media metadata collection through `ffprobe` when available.
- Candidate grouping by duration, resolution, file size, and extension.
- Markdown and JSON reports.
- Clear risk levels and recommended next actions.
- Codex Skill instructions for safe agent use.
- Examples for publishing preflight, editing review, and batch material cleanup.

## Install

Clone the repository:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ecommerce-video-duplicate-preflight-skill.git
cd ecommerce-video-duplicate-preflight-skill
```

The v0.1 scanner uses Python standard library only. `ffprobe` from FFmpeg is optional but recommended for duration, resolution, and codec metadata.

Optional FFmpeg check:

```bash
ffprobe -version
```

## Quick Start

Run a read-only scan:

```bash
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  /path/to/video-folder \
  --output reports/preflight-001
```

Open the report:

```bash
open reports/preflight-001/report.md
```

Validate this repository:

```bash
python3 scripts/validate_repository.py
```

## Example Workflow

1. Put candidate videos in a local folder.
2. Run the scanner against the folder.
3. Review `report.md`.
4. Publish low-risk assets first.
5. Send high-risk assets to an editor for more substantial rework.
6. Keep the report with the publishing batch for auditability.

## Repository Structure

```text
.agents/skills/ecommerce-video-preflight/
  SKILL.md
  scripts/scan_video_duplicates.py
  references/detection-methods.md
examples/
  ecommerce-publish-preflight/
  editing-team-review/
  batch-material-cleanup/
docs/
  installation.md
  usage.md
  report-format.md
  workflow-for-content-teams.md
  platform-risk-disclaimer.md
  codex-for-oss-application-notes.md
scripts/
  validate_repository.py
```

## Using With Codex

Ask Codex to use the Skill when you need to evaluate local video folders before publishing:

```text
Use the ecommerce-video-preflight Skill to scan ./product-videos and produce a publishing priority report in ./reports/batch-01. Do not move or delete any media files.
```

The Skill instructs Codex to keep input files read-only, separate algorithmic signals from business decisions, and ask for confirmation before any destructive action.

## Real-World Scenarios

- A content planner has 120 product videos and needs to pick the least repetitive 30 for initial publishing.
- An editing lead receives five exports of the same product demo and needs to know which are probably too similar.
- A merchant wants to clean a historical video folder before assigning assets for re-editing.

## Roadmap

- `v0.1.0`: Exact duplicate detection, metadata grouping, reports, examples, repository validation.
- `v0.2.0`: Frame sampling and perceptual hash comparison.
- `v0.3.0`: Optional thumbnail contact sheets for human review.
- `v0.4.0`: Optional audio fingerprint support.
- `v0.5.0`: Windows setup notes and packaged CLI improvements.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should keep the workflow read-only by default and avoid claims about guaranteed platform approval.

## Security

See [SECURITY.md](SECURITY.md). Do not open public issues that include private media, credentials, account screenshots, cookies, tokens, or platform vulnerability details.

## License

MIT. See [LICENSE](LICENSE).

## Maintainer

Maintained by KONG as an open-source Codex Skill project. Public usage metrics, external adoption, and feedback should only be added when they are real and verifiable.


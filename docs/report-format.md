# Report Format

The scanner writes two files.

## report.md

Human-readable report with:

- Scan path.
- Generated timestamp.
- File count.
- FFprobe availability.
- Limitations.
- Exact duplicate groups.
- Likely near-duplicate groups.
- Publishing priority list.
- Warnings.

## results.json

Machine-readable output with:

- `inventory`: file-level metadata.
- `exact_duplicate_groups`: SHA-256 matches.
- `metadata_candidate_groups`: conservative near-duplicate candidates.
- `recommendations`: file-level priority.
- `warnings`: missing dependency or unreadable file notes.

## Risk Levels

| Risk | Meaning | Default recommendation |
| --- | --- | --- |
| low | No exact duplicate or conservative metadata match found | publish_first |
| medium | Similar metadata candidate | manual_review |
| high | Exact SHA-256 duplicate | manual_review |

Risk is a review priority, not a platform decision.


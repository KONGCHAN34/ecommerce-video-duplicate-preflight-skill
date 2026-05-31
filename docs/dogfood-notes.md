# Dogfood Notes

This file records public-safe testing evidence. It must not include private video content, platform account data, customer material, or confidential campaign details.

## 2026-05-31 Local Smoke Test

Scope:

- Synthetic local fixture created only for scanner validation.
- No private media used.
- Goal was to prove exact duplicate detection, report generation, and repository validation.

Commands:

```bash
python3 scripts/validate_repository.py
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py --help
python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py /tmp/ecommerce-video-preflight-fixture --output /tmp/ecommerce-video-preflight-report
```

Expected evidence:

- Repository validation passes.
- Scanner help renders.
- Report and JSON output are generated.
- Exact duplicate group appears when two sample files share identical bytes.

Observed result:

- `python3 scripts/validate_repository.py`: passed.
- `python3 .agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py --help`: passed.
- Synthetic fixture scan wrote `/tmp/ecommerce-video-preflight-report/report.md` and `/tmp/ecommerce-video-preflight-report/results.json`.
- Synthetic fixture report found 1 exact duplicate group and 1 low-risk publish-first file.

Notes:

- This is smoke-test evidence, not external adoption evidence.
- Real content-team dogfooding should be added later using sanitized or non-private material.

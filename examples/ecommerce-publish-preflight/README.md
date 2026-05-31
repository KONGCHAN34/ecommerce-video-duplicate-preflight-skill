# Example: E-commerce Publishing Preflight

Scenario: A content planner has a folder of product videos and needs to decide which assets should be uploaded first.

Run:

```bash
python3 ../../.agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./sample-videos \
  --output ./report
```

Expected outcome:

- Exact duplicates are marked high risk.
- Similar exports are marked for manual review.
- Files without duplicate signals are recommended as publish-first candidates.


# Example: Batch Material Cleanup

Scenario: A merchant has an old video material folder and wants a review list before assigning clips to future publishing batches.

Run:

```bash
python3 ../../.agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./archive \
  --output ./report
```

Expected outcome:

- Exact duplicates are listed.
- Potential duplicate families are grouped.
- Low-risk files become candidates for future publishing or re-editing.


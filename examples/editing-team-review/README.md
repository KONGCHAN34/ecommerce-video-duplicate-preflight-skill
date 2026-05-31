# Example: Editing Team Review

Scenario: An editing team created several versions of the same product video. The content lead wants to know which versions are probably too similar.

Run:

```bash
python3 ../../.agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py \
  ./exports \
  --output ./report
```

Expected outcome:

- Exact repeated exports are flagged.
- Similar exports are grouped for editor review.
- The report guides whether a video needs stronger changes.


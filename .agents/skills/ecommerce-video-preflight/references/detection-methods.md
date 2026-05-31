# Detection Methods Reference

## Exact Duplicate Detection

Exact duplicates are files with the same cryptographic hash. This catches byte-for-byte identical files, even when filenames differ.

Recommended signal:

- SHA-256

Limitations:

- Does not catch transcoded, cropped, watermarked, resized, or re-exported variants.

## Metadata Similarity

Metadata similarity compares duration, resolution, file size, extension, codec, and bitrate. It is useful for conservative candidate grouping when deeper visual comparison is not yet enabled.

Limitations:

- Same metadata does not prove visual duplication.
- Different metadata does not prove visual uniqueness.

## Frame Sampling And Perceptual Hashing

Frame sampling extracts representative frames and compares perceptual hashes. This can catch resized, compressed, or lightly edited variants.

Recommended future signals:

- pHash or dHash per sampled frame.
- Hamming distance thresholds.
- Contact sheets for human review.

Limitations:

- Cropping, inserted scenes, heavy overlays, and reordered clips can reduce reliability.
- Thresholds must be calibrated on real team material.

## Audio Fingerprinting

Audio fingerprints can catch videos that share the same soundtrack or narration.

Limitations:

- Silent videos, background music replacement, and platform audio changes can reduce usefulness.
- Audio similarity alone is not enough for a publishing decision.

## Reporting Principle

Always report evidence, method, and limitations. Never present a similarity score as a final platform decision.


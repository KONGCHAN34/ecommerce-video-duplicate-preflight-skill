#!/usr/bin/env python3
"""Read-only video duplicate preflight scanner.

The v0.1 scanner intentionally uses conservative signals:
- SHA-256 for exact duplicate files.
- Optional ffprobe metadata for duration, resolution, codec, and bitrate.
- Basic metadata grouping for likely near-duplicate candidates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def run_ffprobe(path: Path) -> dict[str, Any] | None:
    if shutil.which("ffprobe") is None:
        return None

    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    streams = payload.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    fmt = payload.get("format", {})
    return {
        "duration_seconds": parse_float(fmt.get("duration")),
        "bit_rate": parse_int(fmt.get("bit_rate")),
        "codec": video_stream.get("codec_name"),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "r_frame_rate": video_stream.get("r_frame_rate"),
    }


def parse_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def iter_video_files(root: Path, extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path)
    return sorted(files)


def inventory_file(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    metadata = run_ffprobe(path)
    return {
        "path": str(path),
        "relative_path": str(path.relative_to(root)),
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_time": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).isoformat(),
        "sha256": sha256_file(path),
        "ffprobe": metadata,
    }


def group_exact_duplicates(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hash: dict[str, list[dict[str, Any]]] = {}
    for item in inventory:
        by_hash.setdefault(item["sha256"], []).append(item)
    groups = []
    for sha256, items in by_hash.items():
        if len(items) > 1:
            groups.append(
                {
                    "risk": "high",
                    "reason": "Exact SHA-256 match",
                    "sha256": sha256,
                    "files": [item["relative_path"] for item in items],
                    "recommendation": "manual_review",
                }
            )
    return groups


def duration_bucket(value: float | None, tolerance_seconds: float) -> int | None:
    if value is None:
        return None
    return round(value / tolerance_seconds)


def group_metadata_candidates(
    inventory: list[dict[str, Any]],
    duration_tolerance: float,
    size_tolerance_ratio: float,
) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for item in inventory:
        meta = item.get("ffprobe") or {}
        key = (
            item["extension"],
            meta.get("width"),
            meta.get("height"),
            duration_bucket(meta.get("duration_seconds"), duration_tolerance),
        )
        if key[1] is None or key[2] is None or key[3] is None:
            continue
        buckets.setdefault(key, []).append(item)

    groups: list[dict[str, Any]] = []
    exact_hash_paths = {
        path
        for group in group_exact_duplicates(inventory)
        for path in group["files"]
    }
    for key, items in buckets.items():
        if len(items) < 2:
            continue
        sorted_items = sorted(items, key=lambda item: item["size_bytes"])
        candidate_files: list[str] = []
        for index, item in enumerate(sorted_items):
            for other in sorted_items[index + 1 :]:
                larger = max(item["size_bytes"], other["size_bytes"])
                smaller = min(item["size_bytes"], other["size_bytes"])
                if larger == 0:
                    continue
                if (larger - smaller) / larger <= size_tolerance_ratio:
                    candidate_files.extend([item["relative_path"], other["relative_path"]])
        unique_files = sorted(set(candidate_files) - exact_hash_paths)
        if len(unique_files) > 1:
            groups.append(
                {
                    "risk": "medium",
                    "reason": "Similar duration, resolution, extension, and file size",
                    "bucket": {
                        "extension": key[0],
                        "width": key[1],
                        "height": key[2],
                        "duration_bucket": key[3],
                    },
                    "files": unique_files,
                    "recommendation": "manual_review",
                }
            )
    return groups


def build_recommendations(
    inventory: list[dict[str, Any]],
    exact_groups: list[dict[str, Any]],
    metadata_groups: list[dict[str, Any]],
) -> list[dict[str, str]]:
    high = {path for group in exact_groups for path in group["files"]}
    medium = {path for group in metadata_groups for path in group["files"]}
    recommendations = []
    for item in inventory:
        path = item["relative_path"]
        if path in high:
            risk = "high"
            action = "manual_review"
            reason = "Exact duplicate group detected."
        elif path in medium:
            risk = "medium"
            action = "manual_review"
            reason = "Likely near-duplicate candidate based on metadata similarity."
        else:
            risk = "low"
            action = "publish_first"
            reason = "No exact duplicate or conservative metadata match found."
        recommendations.append({"file": path, "risk": risk, "action": action, "reason": reason})
    return recommendations


def write_markdown_report(output_path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Video Duplicate Preflight Report",
        "",
        f"- Scan path: `{payload['scan_path']}`",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Files scanned: {len(payload['inventory'])}",
        f"- ffprobe available: {payload['ffprobe_available']}",
        "",
        "## Limitations",
        "",
        "This report is a local preflight aid. It does not guarantee platform approval, copyright safety, originality, or compliance.",
        "The v0.1 scanner detects exact duplicates and conservative metadata candidates. It does not yet perform perceptual frame hashing or audio fingerprinting.",
        "",
        "## Summary",
        "",
        f"- Exact duplicate groups: {len(payload['exact_duplicate_groups'])}",
        f"- Likely near-duplicate groups: {len(payload['metadata_candidate_groups'])}",
        f"- Low-risk publish-first files: {sum(1 for item in payload['recommendations'] if item['risk'] == 'low')}",
        "",
        "## Exact Duplicate Groups",
        "",
    ]

    if payload["exact_duplicate_groups"]:
        for index, group in enumerate(payload["exact_duplicate_groups"], 1):
            lines.extend([f"### Group {index}: {group['reason']}", "", f"- Risk: `{group['risk']}`", f"- Recommendation: `{group['recommendation']}`", "- Files:"])
            lines.extend([f"  - `{path}`" for path in group["files"]])
            lines.append("")
    else:
        lines.extend(["No exact duplicate groups found.", ""])

    lines.extend(["## Likely Near-Duplicate Candidates", ""])
    if payload["metadata_candidate_groups"]:
        for index, group in enumerate(payload["metadata_candidate_groups"], 1):
            lines.extend([f"### Group {index}: {group['reason']}", "", f"- Risk: `{group['risk']}`", f"- Recommendation: `{group['recommendation']}`", "- Files:"])
            lines.extend([f"  - `{path}`" for path in group["files"]])
            lines.append("")
    else:
        lines.extend(["No likely near-duplicate metadata groups found.", ""])

    lines.extend(["## Publishing Priority", ""])
    for item in payload["recommendations"]:
        lines.append(f"- `{item['file']}`: `{item['risk']}` -> `{item['action']}`. {item['reason']}")

    lines.extend(["", "## Warnings", ""])
    if payload["warnings"]:
        lines.extend([f"- {warning}" for warning in payload["warnings"]])
    else:
        lines.append("- None.")
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def scan(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.input_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Input directory does not exist or is not a directory: {root}")

    extensions = {value if value.startswith(".") else f".{value}" for value in args.extensions}
    files = iter_video_files(root, {value.lower() for value in extensions})
    warnings = []
    ffprobe_available = shutil.which("ffprobe") is not None
    if not ffprobe_available:
        warnings.append("ffprobe was not found. Metadata-based near-duplicate detection will be limited.")

    inventory = []
    unreadable = []
    for path in files:
        try:
            inventory.append(inventory_file(path, root))
        except OSError as exc:
            unreadable.append({"path": str(path), "error": str(exc)})
    if unreadable:
        warnings.append(f"{len(unreadable)} file(s) could not be read. See results.json for details.")

    exact_groups = group_exact_duplicates(inventory)
    metadata_groups = group_metadata_candidates(inventory, args.duration_tolerance, args.size_tolerance_ratio)
    recommendations = build_recommendations(inventory, exact_groups, metadata_groups)

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "scan_path": str(root),
        "extensions": sorted(extensions),
        "duration_tolerance_seconds": args.duration_tolerance,
        "size_tolerance_ratio": args.size_tolerance_ratio,
        "ffprobe_available": ffprobe_available,
        "inventory": inventory,
        "unreadable_files": unreadable,
        "exact_duplicate_groups": exact_groups,
        "metadata_candidate_groups": metadata_groups,
        "recommendations": recommendations,
        "warnings": warnings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only video duplicate preflight scanner.")
    parser.add_argument("input_dir", help="Directory containing local video files to scan.")
    parser.add_argument("--output", required=True, help="Directory where report.md and results.json will be written.")
    parser.add_argument("--extensions", nargs="+", default=sorted(DEFAULT_EXTENSIONS), help="Video extensions to include.")
    parser.add_argument("--duration-tolerance", type=float, default=1.0, help="Duration bucket size in seconds for metadata grouping.")
    parser.add_argument("--size-tolerance-ratio", type=float, default=0.08, help="Max relative size difference for metadata grouping.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output = Path(args.output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    payload = scan(args)
    (output / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(output / "report.md", payload)
    print(f"Wrote {output / 'report.md'}")
    print(f"Wrote {output / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


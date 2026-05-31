#!/usr/bin/env python3
"""Validate repository files for the ecommerce-video-preflight Skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/ecommerce-video-preflight/SKILL.md"

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "AGENTS.md",
    ".gitignore",
    ".agents/skills/ecommerce-video-preflight/SKILL.md",
    ".agents/skills/ecommerce-video-preflight/scripts/scan_video_duplicates.py",
    ".agents/skills/ecommerce-video-preflight/references/detection-methods.md",
    "examples/ecommerce-publish-preflight/README.md",
    "examples/ecommerce-publish-preflight/sample-inventory.md",
    "examples/ecommerce-publish-preflight/expected-output.md",
    "examples/editing-team-review/README.md",
    "examples/editing-team-review/sample-inventory.md",
    "examples/editing-team-review/expected-output.md",
    "examples/batch-material-cleanup/README.md",
    "examples/batch-material-cleanup/sample-inventory.md",
    "examples/batch-material-cleanup/expected-output.md",
    "docs/installation.md",
    "docs/usage.md",
    "docs/skill-audit.md",
    "docs/project-positioning.md",
    "docs/design.md",
    "docs/report-format.md",
    "docs/workflow-for-content-teams.md",
    "docs/platform-risk-disclaimer.md",
    "docs/dogfood-notes.md",
    "docs/codex-for-oss-application-notes.md",
    "docs/issue-backlog.md",
    "docs/30-day-plan.md",
    "docs/release-checklist.md",
    "docs/release-notes-v0.1.0.md",
    ".github/workflows/validate.yml",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_skill_frontmatter() -> list[str]:
    errors: list[str] = []
    text = read(SKILL)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md is missing YAML frontmatter."]
    frontmatter = match.group(1)
    if not re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE):
        errors.append("SKILL.md frontmatter is missing name.")
    description = re.search(r"^description:\s*(.+)", frontmatter, re.MULTILINE)
    if not description:
        errors.append("SKILL.md frontmatter is missing description.")
    elif len(description.group(1).strip()) < 80:
        errors.append("SKILL.md description is too short to be useful as a trigger.")
    return errors


def validate_examples() -> list[str]:
    errors: list[str] = []
    for folder in ["ecommerce-publish-preflight", "editing-team-review", "batch-material-cleanup"]:
        expected = ROOT / "examples" / folder / "expected-output.md"
        text = read(expected)
        for required in ["Risk", "Recommendation", "Limitations"]:
            if required not in text:
                errors.append(f"{expected.relative_to(ROOT)} missing {required}.")
    return errors


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"Missing required file: {relative}")
    if not errors:
        errors.extend(validate_skill_frontmatter())
        errors.extend(validate_examples())

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

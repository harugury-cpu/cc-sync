#!/usr/bin/env python3
"""
Validate local Codex/agent skills.

Default target:
  /Users/harugury/.agents/skills

Checks:
- each skill folder has SKILL.md
- SKILL.md starts with YAML-like front matter
- required fields: name, description
- name matches folder name, allowing namespace names like ckm:slides -> ckm-slides
- duplicate names
- description is not too short to route well

No external dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.S)


def parse_front_matter(path: Path) -> tuple[dict[str, str], str | None]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, "front matter must start on the first line and close with ---"

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return {}, f"invalid front matter line: {raw_line!r}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        fields[key] = value
    return fields, None


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    fields, error = parse_front_matter(skill_file)
    if error:
        return [f"{skill_file}: {error}"]

    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()

    if not name:
        errors.append(f"{skill_file}: missing non-empty field: name")
    if not description:
        errors.append(f"{skill_file}: missing non-empty field: description")
    normalized_name = name.replace(":", "-")
    if name and normalized_name != skill_dir.name:
        errors.append(f"{skill_file}: name {name!r} does not match folder {skill_dir.name!r}")
    if description and len(description) < 30:
        errors.append(f"{skill_file}: description is too short for reliable routing")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local agent skills.")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("/Users/harugury/.agents/skills")],
        help="Skill roots to validate. Defaults to /Users/harugury/.agents/skills.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    names: dict[str, Path] = {}
    checked = 0

    for root in args.paths:
        if not root.exists():
            errors.append(f"{root}: path does not exist")
            continue
        for skill_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            checked += 1
            skill_errors = validate_skill_dir(skill_dir)
            errors.extend(skill_errors)
            fields, _ = parse_front_matter(skill_file)
            name = fields.get("name", "").strip()
            if name:
                if name in names:
                    errors.append(f"{skill_file}: duplicate skill name {name!r}; first seen at {names[name]}")
                else:
                    names[name] = skill_file

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {checked} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

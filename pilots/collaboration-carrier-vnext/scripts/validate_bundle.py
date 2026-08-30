#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PILOT = ROOT / "pilots" / "collaboration-carrier-vnext"
SKILLS = [
    "human-ai-responsibility-capability",
    "human-ai-evidence-assurance",
    "human-ai-software-collaboration",
    "human-ai-reflection",
    "human-ai-cognitive-probing",
]

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        json.load(f)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated YAML frontmatter")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def main() -> None:
    load_json(PILOT / "manifest.json")
    load_json(PILOT / "evals" / "routing.json")
    load_json(PILOT / "evals" / "behavior.json")

    kernel = (PILOT / "resident-kernel.md").read_text(encoding="utf-8")
    codex = (PILOT / "adapters" / "codex" / "AGENTS.md").read_text(encoding="utf-8")
    if kernel != codex:
        raise ValueError("Codex AGENTS.md must exactly mirror resident-kernel.md")

    for folder in SKILLS:
        path = ROOT / "skills" / folder / "SKILL.md"
        fields = parse_frontmatter(path)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder:
            raise ValueError(f"{path}: name must match folder ({folder})")
        if len(name) > 64 or not NAME_RE.fullmatch(name):
            raise ValueError(f"{path}: invalid Agent Skills name")
        if not description or len(description) > 1024:
            raise ValueError(f"{path}: description must be 1..1024 characters")

    print("collaboration-carrier-vnext: bundle validation passed")


if __name__ == "__main__":
    main()

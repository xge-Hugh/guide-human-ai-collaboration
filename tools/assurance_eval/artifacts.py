"""Private append-only JSON artifact storage and centralized secret scanning."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any


def write_new_json(path: Path, value: Any) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def contains_private_value(value: Any, private_values: tuple[str, ...]) -> bool:
    content = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
    return any(needle.encode("utf-8") in content for needle in private_values if needle)


def scan_private_values(root: Path, private_values: tuple[str, ...]) -> list[str]:
    needles = [(value, value.encode("utf-8")) for value in private_values if value]
    matches: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        content = path.read_bytes()
        if any(needle in content for _, needle in needles):
            matches.append(str(path.relative_to(root)))
    return matches


def tree_sha256(root: Path, *, exclude: tuple[str, ...] = ()) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if str(path.relative_to(root)) in exclude:
            continue
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()

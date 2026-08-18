"""Load the checked-in Phase B packets without duplicating their semantics."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True)
class PhaseBInputs:
    generation: dict[str, dict[str, Any]]
    variants: dict[str, dict[str, Any]]
    rubrics: dict[str, dict[str, Any]]
    source_files: dict[str, dict[str, str]]


def _load_collection(path: Path, collection_key: str, id_key: str) -> tuple[dict[str, dict[str, Any]], str]:
    raw = path.read_bytes()
    document = json.loads(raw)
    if document.get("schema_version") != 1:
        raise ValueError(f"unsupported schema_version in {path}")
    items = document.get(collection_key)
    if not isinstance(items, list):
        raise ValueError(f"{path} must contain a {collection_key} list")

    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get(id_key), str):
            raise ValueError(f"invalid item in {path}")
        item_id = item[id_key]
        if not _SAFE_ID.fullmatch(item_id):
            raise ValueError(f"unsafe {id_key} {item_id!r} in {path}")
        if item_id in indexed:
            raise ValueError(f"duplicate {id_key} {item_id!r} in {path}")
        indexed[item_id] = item
    return indexed, hashlib.sha256(raw).hexdigest()


def _require_strings(
    items: dict[str, dict[str, Any]], fields: tuple[str, ...], source_name: str
) -> None:
    for item_id, item in items.items():
        for field in fields:
            if not isinstance(item.get(field), str):
                raise ValueError(f"{source_name} {item_id!r} requires string field {field!r}")


def load_phase_b_inputs(repo_root: Path) -> PhaseBInputs:
    experiment_dir = repo_root / "docs" / "experiments"
    paths = {
        "generation": experiment_dir / "assurance-v2-phase-b-generation.json",
        "variants": experiment_dir / "assurance-v2-phase-b-variants.json",
        "rubrics": experiment_dir / "assurance-v2-phase-b-rubrics.json",
    }
    generation, generation_digest = _load_collection(paths["generation"], "packets", "packet_id")
    variants, variants_digest = _load_collection(paths["variants"], "variants", "variant_id")
    rubrics, rubrics_digest = _load_collection(paths["rubrics"], "rubrics", "packet_id")

    _require_strings(generation, ("pre_context", "user_message"), "generation packet")
    _require_strings(variants, ("name", "instruction_append"), "variant")
    _require_strings(
        rubrics,
        (
            "reference_case",
            "expected_applicability",
            "required_protection",
            "latest_useful_point",
            "adjudication",
        ),
        "rubric",
    )

    if generation.keys() != rubrics.keys():
        missing_rubrics = sorted(generation.keys() - rubrics.keys())
        missing_packets = sorted(rubrics.keys() - generation.keys())
        raise ValueError(
            "generation/rubric packet IDs differ: "
            f"missing rubrics={missing_rubrics}, missing generation packets={missing_packets}"
        )

    digests = {
        "generation": generation_digest,
        "variants": variants_digest,
        "rubrics": rubrics_digest,
    }
    source_files = {
        name: {"path": str(path.relative_to(repo_root)), "sha256": digests[name]}
        for name, path in paths.items()
    }
    return PhaseBInputs(generation, variants, rubrics, source_files)

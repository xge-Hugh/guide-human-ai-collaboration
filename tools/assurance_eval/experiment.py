"""Load and validate one human-editable assurance experiment recipe."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


_SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")
_SOURCE_SPECS = {
    "generation": ("packets", "packet_id"),
    "variants": ("variants", "variant_id"),
    "rubrics": ("rubrics", "packet_id"),
}


@dataclass(frozen=True)
class Experiment:
    recipe_path: Path
    recipe_sha256: str
    recipe: Mapping[str, Any]
    generation: Mapping[str, Mapping[str, Any]]
    variants: Mapping[str, Mapping[str, Any]]
    rubrics: Mapping[str, Mapping[str, Any]]
    sources: Mapping[str, Mapping[str, str]]
    source_paths: Mapping[str, Path]


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def loads_exact(raw: bytes | str, source: object = "JSON") -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r} in {source}")
            value[key] = child
        return value

    return json.loads(raw, object_pairs_hook=reject_duplicates)


def _read_object(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = loads_exact(raw, path)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value, raw


def _resolve_source(repo_root: Path, recipe_path: Path, source: object) -> Path:
    if not isinstance(source, str) or not source.strip():
        raise ValueError("recipe source paths must be non-empty strings")
    candidate = Path(source)
    if candidate.is_absolute():
        path = candidate
    else:
        recipe_relative = recipe_path.parent / candidate
        path = recipe_relative if recipe_relative.is_file() else repo_root / candidate
    resolved = path.resolve()
    if not resolved.is_file():
        raise ValueError(f"experiment source does not exist: {source}")
    return resolved


def _load_collection(path: Path, collection_key: str, id_key: str) -> tuple[dict[str, Mapping[str, Any]], str, dict[str, Any]]:
    document, raw = _read_object(path)
    if document.get("schema_version") != 1 or not isinstance(document.get(collection_key), list):
        raise ValueError(f"unsupported experiment source schema in {path}")
    indexed: dict[str, Mapping[str, Any]] = {}
    for item in document[collection_key]:
        if not isinstance(item, dict) or not isinstance(item.get(id_key), str):
            raise ValueError(f"invalid {collection_key} item in {path}")
        item_id = item[id_key]
        if not _SAFE_ID.fullmatch(item_id) or item_id in indexed:
            raise ValueError(f"unsafe or duplicate {id_key} {item_id!r}")
        indexed[item_id] = item
    return indexed, sha256_bytes(raw), document


def load_experiment(repo_root: Path, recipe_path: Path) -> Experiment:
    recipe_path = recipe_path.resolve()
    recipe, raw = _read_object(recipe_path)
    if recipe.get("schema_version") != 1:
        raise ValueError("unsupported experiment recipe schema_version")
    required = {
        "experiment_id", "sources", "selection", "renderers", "schedule", "instructions",
        "parameters", "grading", "formal_execution_enabled", "output_root",
    }
    missing = sorted(required - set(recipe))
    if missing:
        raise ValueError(f"recipe fields missing: {missing}")
    if not isinstance(recipe["formal_execution_enabled"], bool):
        raise ValueError("formal_execution_enabled must be boolean")
    if not isinstance(recipe["sources"], dict) or set(recipe["sources"]) != set(_SOURCE_SPECS):
        raise ValueError("recipe must reference generation, variants, and rubrics sources")
    collections: dict[str, Mapping[str, Mapping[str, Any]]] = {}
    source_documents: dict[str, Mapping[str, Any]] = {}
    sources: dict[str, Mapping[str, str]] = {}
    source_paths: dict[str, Path] = {}
    for role, (collection_key, id_key) in _SOURCE_SPECS.items():
        path = _resolve_source(repo_root, recipe_path, recipe["sources"][role])
        collection, digest, document = _load_collection(path, collection_key, id_key)
        collections[role] = collection
        source_documents[role] = document
        source_paths[role] = path
        try:
            display_path = str(path.relative_to(repo_root.resolve()))
        except ValueError:
            display_path = str(path)
        sources[role] = {"path": display_path, "sha256": digest}
    generation = collections["generation"]
    variants = collections["variants"]
    rubrics = collections["rubrics"]
    if set(generation) != set(rubrics):
        raise ValueError("generation and rubric case IDs differ")
    selection = recipe["selection"]
    if not isinstance(selection, dict):
        raise ValueError("selection must be an object")
    case_ids = selection.get("cases")
    variant_ids = selection.get("variants")
    if not isinstance(case_ids, list) or not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("selection.cases must be a non-empty unique list")
    if not isinstance(variant_ids, list) or not variant_ids or len(variant_ids) != len(set(variant_ids)):
        raise ValueError("selection.variants must be a non-empty unique list")
    unknown_cases = sorted(set(case_ids) - set(generation))
    unknown_variants = sorted(set(variant_ids) - set(variants))
    if unknown_cases or unknown_variants:
        raise ValueError(f"unknown selections: cases={unknown_cases}, variants={unknown_variants}")
    variant_document = source_documents["variants"]
    semantic_source = variant_document.get("semantic_source")
    semantic_frame = variant_document.get("b2_semantic_frame_append")
    if semantic_source is not None or semantic_frame is not None:
        if not isinstance(semantic_source, dict) or not isinstance(semantic_frame, str):
            raise ValueError("translated variant semantic provenance is incomplete")
        semantic_path = _resolve_source(repo_root, recipe_path, semantic_source.get("path"))
        if semantic_source.get("sha256") != sha256_bytes(semantic_path.read_bytes()):
            raise ValueError("translated variant semantic-source hash is stale")
        if {"B0", "B1", "B2"}.issubset(variants) and (
            variants["B0"]["instruction_append"] != ""
            or variants["B2"]["instruction_append"]
            != f'{variants["B1"]["instruction_append"]}\n\n{semantic_frame}'
        ):
            raise ValueError("B0/B1/B2 composition invariant failed")
    schedule = recipe["schedule"]
    repetitions = schedule.get("repetitions") if isinstance(schedule, dict) else None
    order = schedule.get("variant_order_by_repetition") if isinstance(schedule, dict) else None
    if not isinstance(repetitions, int) or isinstance(repetitions, bool) or repetitions < 1:
        raise ValueError("schedule.repetitions must be a positive integer")
    if not isinstance(order, list) or len(order) != repetitions or any(
        not isinstance(row, list) or sorted(row) != sorted(variant_ids) for row in order
    ):
        raise ValueError("each repetition must define one permutation of selected variants")
    tranches = schedule.get("operational_tranches")
    if tranches is not None:
        if not isinstance(tranches, dict):
            raise ValueError("schedule.operational_tranches must be an object")
        tranche_rows = [value.get("repetitions") for key, value in tranches.items() if key.startswith("tranche_") and isinstance(value, dict)]
        flattened = [item for row in tranche_rows if isinstance(row, list) for item in row]
        if sorted(flattened) != list(range(1, repetitions + 1)) or len(flattened) != len(set(flattened)):
            raise ValueError("operational tranches must partition all repetitions exactly once")
        if not isinstance(tranches.get("allowed_pause_reasons"), list) or tranches.get("performance_driven_redesign_between_tranches_forbidden") is not True:
            raise ValueError("operational tranche controls are incomplete")
    if not isinstance(recipe["renderers"], dict) or set(recipe["renderers"]) != {"generator", "grader"}:
        raise ValueError("recipe must select generator and grader renderers")
    if not all(
        isinstance(value, str) and value.strip() for value in recipe["renderers"].values()
    ):
        raise ValueError("renderer identities must be non-empty strings")
    if not isinstance(recipe["parameters"], dict) or set(recipe["parameters"]) != {"generator", "grader"}:
        raise ValueError("recipe must define generator and grader parameters")
    if not all(isinstance(value, dict) for value in recipe["parameters"].values()):
        raise ValueError("role parameters must be objects")
    instructions = recipe["instructions"]
    if not isinstance(instructions, dict) or not isinstance(instructions.get("generator_base"), str) or not instructions["generator_base"].strip():
        raise ValueError("instructions.generator_base must be non-empty")
    grading = recipe["grading"]
    if not isinstance(grading, dict) or not all(
        key in grading for key in ("policy_id", "axes", "conditional_rule", "output_schema")
    ):
        raise ValueError("grading must define policy, axes, conditional rule, and output schema")
    from .grading import validate_grading_contract
    from .renderers import validate_parameters

    validate_grading_contract(grading)
    for role in ("generator", "grader"):
        validate_parameters(recipe["parameters"][role], role)
    for packet in generation.values():
        if not all(isinstance(packet.get(field), str) for field in ("pre_context", "user_message")):
            raise ValueError("generation packets require pre_context and user_message strings")
    for variant in variants.values():
        if not isinstance(variant.get("instruction_append"), str):
            raise ValueError("variants require instruction_append strings")
    rubric_fields = ("reference_case", "expected_applicability", "required_protection", "latest_useful_point", "adjudication")
    for rubric in rubrics.values():
        if not all(isinstance(rubric.get(field), str) for field in rubric_fields):
            raise ValueError("rubrics do not satisfy the Phase B semantic boundary")
    return Experiment(
        recipe_path=recipe_path,
        recipe_sha256=sha256_bytes(raw),
        recipe=recipe,
        generation=generation,
        variants=variants,
        rubrics=rubrics,
        sources=sources,
        source_paths=source_paths,
    )

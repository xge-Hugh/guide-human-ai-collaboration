"""Load local-only provider credentials without exposing them as public metadata."""

from __future__ import annotations

import json
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class LocalProviderConfig:
    label: str
    provider: str
    api_style: str
    configured_model: str
    declared_model_snapshot: str | None
    base_url: str = field(repr=False)
    api_key: str = field(repr=False)


def _required_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def load_local_provider_config(
    path: Path,
    *,
    connection_label: str,
    repository_root: Path,
    model_id: str | None = None,
) -> LocalProviderConfig:
    resolved_path = _validated_private_path(path, repository_root)
    document = json.loads(resolved_path.read_text(encoding="utf-8"))
    return _config_from_document(document, connection_label, model_id=model_id)


def _validated_private_path(path: Path, repository_root: Path) -> Path:
    resolved_path = path.resolve()
    if resolved_path.is_relative_to(repository_root.resolve()):
        raise ValueError("provider config must be stored outside the repository")
    mode = stat.S_IMODE(resolved_path.stat().st_mode)
    if mode & 0o077:
        raise PermissionError("provider config must not be accessible by group or other users")
    return resolved_path


def _config_from_document(
    document: object, connection_label: str, *, model_id: str | None = None
) -> LocalProviderConfig:
    if not isinstance(document, dict):
        raise ValueError("local provider config must be a JSON object")
    if document.get("schema_version") != 1:
        raise ValueError("unsupported local provider config schema_version")
    connections = document.get("connections")
    if not isinstance(connections, list):
        raise ValueError("local provider config requires a connections list")
    matches = [item for item in connections if item.get("label") == connection_label]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one connection labeled {connection_label!r}")

    connection = matches[0]
    api_style = _required_string(connection.get("api_style"), "api_style")
    if api_style != "openai_chat_completions":
        raise ValueError("only openai_chat_completions plumbing is currently implemented")
    base_url = _required_string(connection.get("base_url"), "base_url")
    parsed_url = urlparse(base_url)
    if parsed_url.scheme != "https" or not parsed_url.hostname:
        raise ValueError("base_url must be an absolute HTTPS URL")
    if parsed_url.username or parsed_url.password or parsed_url.query or parsed_url.fragment:
        raise ValueError("base_url must not contain credentials, a query, or a fragment")

    models = connection.get("models")
    if not isinstance(models, list) or not models or not all(
        isinstance(item, dict) for item in models
    ):
        raise ValueError("local provider config requires one or more models")
    if model_id is None:
        if len(models) != 1:
            raise ValueError("multiple models require exactly one explicit approved model_id")
        model = models[0]
    else:
        model_matches = [item for item in models if item.get("model_id") == model_id]
        if len(model_matches) != 1:
            raise ValueError("expected exactly one approved model entry for selected model_id")
        model = model_matches[0]
    snapshot = model.get("declared_model_snapshot")
    if snapshot is not None:
        snapshot = _required_string(snapshot, "declared_model_snapshot")
    return LocalProviderConfig(
        label=_required_string(connection.get("label"), "label"),
        provider=_required_string(connection.get("provider"), "provider"),
        api_style=api_style,
        configured_model=_required_string(model.get("model_id"), "model_id"),
        declared_model_snapshot=snapshot,
        base_url=base_url.rstrip("/"),
        api_key=_required_string(connection.get("api_key"), "api_key"),
    )


def load_only_local_provider_config_and_scan_values(
    path: Path, *, repository_root: Path, model_id: str | None = None
) -> tuple[LocalProviderConfig, tuple[str, ...]]:
    """Load the sole approved config and scan needles from the same secured bytes."""
    resolved_path = _validated_private_path(path, repository_root)
    document = json.loads(resolved_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("local provider config must be a JSON object")
    connections = document.get("connections")
    if not isinstance(connections, list) or len(connections) != 1:
        raise ValueError("transport smoke requires exactly one approved connection")
    connection = connections[0]
    if not isinstance(connection, dict):
        raise ValueError("approved connection must be a JSON object")
    label = _required_string(connection.get("label"), "label")
    config = _config_from_document(document, label, model_id=model_id)
    private_values = tuple(
        dict.fromkeys(
            (
                config.label,
                config.base_url,
                config.api_key,
                *_secret_scan_values(document),
            )
        )
    )
    return config, private_values


def load_only_local_provider_config(
    path: Path, *, repository_root: Path, model_id: str | None = None
) -> LocalProviderConfig:
    config, _ = load_only_local_provider_config_and_scan_values(
        path, repository_root=repository_root, model_id=model_id
    )
    return config


def _secret_scan_values(document: dict[str, Any]) -> tuple[str, ...]:
    public_keys = {
        "schema_version",
        "provider",
        "api_style",
        "model_id",
        "declared_model_snapshot",
        "candidate_roles",
    }
    values: list[str] = []

    def visit(value: object, key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, child_key)
        elif isinstance(value, list):
            for child_value in value:
                visit(child_value, key)
        elif isinstance(value, str) and key not in public_keys and len(value) >= 4:
            values.append(value)

    visit(document)
    connections = document.get("connections")
    if isinstance(connections, list):
        for connection in connections:
            if not isinstance(connection, dict):
                continue
            base_url = connection.get("base_url")
            if isinstance(base_url, str):
                parsed = urlparse(base_url)
                for endpoint_part in (parsed.hostname, parsed.netloc):
                    if endpoint_part and len(endpoint_part) >= 4:
                        values.append(endpoint_part)
    return tuple(dict.fromkeys(values))

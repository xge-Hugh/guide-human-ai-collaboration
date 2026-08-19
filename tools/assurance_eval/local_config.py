"""Load local-only provider credentials without exposing them as public metadata."""

from __future__ import annotations

import json
import stat
from dataclasses import dataclass, field
from pathlib import Path
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
    path: Path, *, connection_label: str, repository_root: Path
) -> LocalProviderConfig:
    resolved_path = path.resolve()
    if resolved_path.is_relative_to(repository_root.resolve()):
        raise ValueError("provider config must be stored outside the repository")
    mode = stat.S_IMODE(resolved_path.stat().st_mode)
    if mode & 0o077:
        raise PermissionError("provider config must not be accessible by group or other users")

    document = json.loads(resolved_path.read_text(encoding="utf-8"))
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
    if not isinstance(models, list) or len(models) != 1 or not isinstance(models[0], dict):
        raise ValueError("Stage 2 local config currently requires exactly one model")
    model = models[0]
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

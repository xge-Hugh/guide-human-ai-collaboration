"""Private model catalog loading and secret-free profile resolution."""

from __future__ import annotations

import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from .models import ModelAssignment, ProviderCredentials, ResolvedProvider
from .experiment import loads_exact


@dataclass(frozen=True)
class ModelCatalog:
    profiles: Mapping[str, Mapping[str, str]]
    models: Mapping[str, Mapping[str, Any]]
    connections: Mapping[str, Mapping[str, Any]]
    private_scan_values: tuple[str, ...]

    def resolve(self, profile: str, role_parameters: Mapping[str, Any]) -> dict[str, ResolvedProvider]:
        try:
            roles = self.profiles[profile]
        except KeyError:
            raise ValueError(f"unknown model profile {profile!r}") from None
        if set(roles) != {"generator", "grader"}:
            raise ValueError("a profile must bind exactly generator and grader")
        resolved: dict[str, ResolvedProvider] = {}
        for role, model_name in roles.items():
            try:
                model = self.models[model_name]
                connection = self.connections[model["connection"]]
            except KeyError as error:
                raise ValueError(f"profile {profile!r} has an unresolved {role} model") from error
            parameters = role_parameters.get(role)
            if not isinstance(parameters, Mapping):
                raise ValueError(f"recipe parameters for {role} must be an object")
            assignment = ModelAssignment(
                provider=_required_string(connection.get("provider"), "provider"),
                model=_required_string(model.get("model_id"), "model_id"),
                family=_required_string(model.get("family"), "family"),
                declared_snapshot=_optional_string(model.get("declared_snapshot"), "declared_snapshot"),
                parameters=dict(parameters),
            )
            resolved[role] = ResolvedProvider(
                assignment=assignment,
                credentials=ProviderCredentials(
                    api_style=_required_string(connection.get("api_style"), "api_style"),
                    base_url=_validate_base_url(connection.get("base_url")),
                    api_key=_required_string(connection.get("api_key"), "api_key"),
                ),
            )
        return resolved


def _required_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_string(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _required_string(value, field)


def _validate_base_url(value: object) -> str:
    url = _required_string(value, "base_url").rstrip("/")
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("base_url must be an absolute HTTPS URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("base_url must not contain credentials, a query, or a fragment")
    return url


def _private_path(path: Path, repository_root: Path) -> Path:
    resolved = path.resolve()
    if resolved.is_relative_to(repository_root.resolve()):
        raise ValueError("setting.json must be stored outside the repository")
    if stat.S_IMODE(resolved.stat().st_mode) & 0o077:
        raise PermissionError("setting.json must not be accessible by group or other users")
    return resolved


def load_model_catalog(path: Path, repository_root: Path) -> ModelCatalog:
    resolved_path = _private_path(path, repository_root)
    document = loads_exact(resolved_path.read_bytes(), resolved_path)
    if not isinstance(document, dict) or document.get("schema_version") != 2:
        raise ValueError("unsupported model catalog schema_version")
    for name in ("connections", "models", "profiles"):
        if not isinstance(document.get(name), dict) or not document[name]:
            raise ValueError(f"model catalog requires a non-empty {name} object")
    connections = document["connections"]
    models = document["models"]
    profiles_document = document["profiles"]
    for name, connection in connections.items():
        if not isinstance(connection, dict):
            raise ValueError(f"connection {name!r} must be an object")
        if connection.get("api_style") != "openai_chat_completions":
            raise ValueError("only openai_chat_completions is supported")
        _validate_base_url(connection.get("base_url"))
        _required_string(connection.get("api_key"), "api_key")
        _required_string(connection.get("provider"), "provider")
    for name, model in models.items():
        if not isinstance(model, dict) or model.get("connection") not in connections:
            raise ValueError(f"model {name!r} must reference a known connection")
        _required_string(model.get("model_id"), "model_id")
        _required_string(model.get("family"), "family")
        _optional_string(model.get("declared_snapshot"), "declared_snapshot")
    profiles: dict[str, Mapping[str, str]] = {}
    for name, profile in profiles_document.items():
        if not isinstance(profile, dict) or not isinstance(profile.get("roles"), dict):
            raise ValueError(f"profile {name!r} requires a roles object")
        roles = profile["roles"]
        if set(roles) != {"generator", "grader"} or not all(
            isinstance(value, str) and value in models for value in roles.values()
        ):
            raise ValueError(f"profile {name!r} must bind generator and grader to catalog models")
        profiles[name] = dict(roles)
    private_values: list[str] = []
    for connection in connections.values():
        url = _validate_base_url(connection["base_url"])
        parsed = urlparse(url)
        private_values.extend((url, parsed.hostname or "", connection["api_key"]))
    return ModelCatalog(
        profiles=profiles,
        models=models,
        connections=connections,
        private_scan_values=tuple(dict.fromkeys(value for value in private_values if value)),
    )

"""Shared provenance, private-path, and explicit network execution policy."""

from __future__ import annotations

import hashlib
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .models import ProviderError, Transport


EVIDENCE_LABELS = {
    "exploratory": "non_formal_exploratory_evidence",
    "formal": "phase_b_controlled_replay_raw_evidence_pending_adjudication",
}


def git_provenance(repo_root: Path) -> dict[str, Any]:
    source_digest = hashlib.sha256()
    source_root = repo_root / "tools" / "assurance_eval"
    for path in sorted(source_root.glob("*.py")):
        source_digest.update(str(path.relative_to(repo_root)).encode("utf-8"))
        source_digest.update(b"\0")
        source_digest.update(path.read_bytes())
        source_digest.update(b"\0")
    harness_source_sha256 = source_digest.hexdigest()
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo_root,
            check=True, capture_output=True, text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {
            "available": False, "git_revision": None, "clean": False,
            "status_sha256": None, "harness_source_sha256": harness_source_sha256,
        }
    return {
        "available": True,
        "git_revision": revision,
        "clean": not bool(status),
        "status_sha256": hashlib.sha256(status.encode("utf-8")).hexdigest(),
        "harness_source_sha256": harness_source_sha256,
    }


def require_committed_paths(repo_root: Path, paths: tuple[Path, ...]) -> None:
    root = repo_root.resolve()
    for path in paths:
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError("formal recipes and semantic sources must be committed repository files")
        try:
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", str(resolved.relative_to(root))],
                cwd=root, check=True, capture_output=True, text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            raise ValueError("formal recipes and semantic sources must be committed repository files") from None


def validate_private_output(path: Path, repo_root: Path, *, must_exist: bool) -> Path:
    resolved = path.resolve()
    if resolved.is_relative_to(repo_root.resolve()):
        raise ValueError("artifacts must remain outside the repository")
    if must_exist and not resolved.is_dir():
        raise ValueError("output root must already exist")
    if resolved.exists() and stat.S_IMODE(resolved.stat().st_mode) & 0o077:
        raise PermissionError("output root must not be accessible by group or other users")
    return resolved


@dataclass
class NetworkGate:
    """Shared per-run transport budget across logical calls and retry attempts."""

    transport: Transport
    authorized: bool
    maximum_network_attempts: int
    before_call: Callable[[], None]
    forbidden_values: tuple[str, ...] = ()
    network_attempts: int = 0
    planned_logical_calls: int = 0
    completed_logical_calls: int = 0

    @property
    def calls(self) -> int:
        return self.network_attempts

    def __call__(self, url: str, headers: Mapping[str, str], body: bytes, timeout: float) -> bytes:
        if not self.authorized:
            raise ProviderError("network authorization is missing")
        if self.network_attempts >= self.maximum_network_attempts:
            raise ProviderError("resolved-plan network call budget exhausted")
        if any(value.encode("utf-8") in body for value in self.forbidden_values if value):
            raise ProviderError("model-visible request contains a private value")
        self.before_call()
        self.network_attempts += 1
        return self.transport(url, headers, body, timeout)

    def accounting(self) -> dict[str, int]:
        return {
            "planned_logical_calls": self.planned_logical_calls,
            "completed_logical_calls": self.completed_logical_calls,
            "actual_network_attempts": self.network_attempts,
        }

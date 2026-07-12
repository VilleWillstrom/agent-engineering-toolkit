from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .errors import ConfigurationError, ProviderNotFoundError
from .models import RegistryEntry


class ExtensionRegistry:
    def __init__(self, entries: Iterable[RegistryEntry], *, kind: str) -> None:
        materialized = list(entries)
        self.kind = kind
        self._entries = {entry.id: entry for entry in materialized}
        if len(self._entries) != len(materialized):
            raise ConfigurationError(f"duplicate {kind} id")

    @classmethod
    def load(cls, path: Path, *, kind: str, list_key: str) -> "ExtensionRegistry":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ConfigurationError(f"missing {kind} registry: {path}") from exc
        except json.JSONDecodeError as exc:
            raise ConfigurationError(f"invalid JSON in {path}: {exc}") from exc
        if data.get("schema_version") != 1:
            raise ConfigurationError(f"unsupported {kind} registry schema_version")
        raw_entries = data.get(list_key)
        if not isinstance(raw_entries, list):
            raise ConfigurationError(f"'{list_key}' must be a list")
        try:
            entries = [RegistryEntry.from_dict(item) for item in raw_entries]
        except (TypeError, ValueError) as exc:
            raise ConfigurationError(str(exc)) from exc
        return cls(entries, kind=kind)

    def list(self, *, enabled_only: bool = False) -> list[RegistryEntry]:
        entries = list(self._entries.values())
        if enabled_only:
            entries = [entry for entry in entries if entry.enabled]
        return sorted(entries, key=lambda entry: entry.id)

    def get(self, entry_id: str) -> RegistryEntry:
        try:
            return self._entries[entry_id]
        except KeyError as exc:
            raise ProviderNotFoundError(f"unknown {self.kind}: {entry_id}") from exc

    def choose(
        self,
        required_capabilities: Iterable[str],
        *,
        excluded: Iterable[str] = (),
        prefer_local: bool = False,
    ) -> RegistryEntry:
        required = set(required_capabilities)
        excluded_ids = set(excluded)
        candidates = [
            entry
            for entry in self._entries.values()
            if entry.enabled and entry.id not in excluded_ids and entry.supports(required)
        ]
        if not candidates:
            capabilities = ", ".join(sorted(required)) or "none"
            raise ProviderNotFoundError(f"no enabled {self.kind} supports: {capabilities}")

        def rank(entry: RegistryEntry) -> tuple[int, int, float, str]:
            local_bonus = 1 if prefer_local and bool(entry.config.get("local", False)) else 0
            return (-local_bonus, -entry.priority, entry.cost_weight, entry.id)

        return sorted(candidates, key=rank)[0]

    def validate_commands(self) -> list[str]:
        import shutil

        issues: list[str] = []
        for entry in self.list(enabled_only=True):
            if entry.adapter in {"command", "cli"}:
                command = entry.config.get("command")
                if not isinstance(command, list) or not command or not isinstance(command[0], str):
                    issues.append(f"{entry.id}: command adapter requires a command list")
                elif shutil.which(command[0]) is None:
                    issues.append(f"{entry.id}: executable not found: {command[0]}")
        return issues

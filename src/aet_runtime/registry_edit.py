from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .errors import ConfigurationError
from .models import RegistryEntry


def add_registry_entry(registry_path: Path, *, list_key: str, definition_path: Path) -> str:
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        definition = json.loads(definition_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigurationError(f"missing registry or definition file: {exc.filename}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"invalid JSON: {exc}") from exc
    if registry.get("schema_version") != 1 or not isinstance(registry.get(list_key), list):
        raise ConfigurationError(f"invalid registry structure for {list_key}")
    entry = RegistryEntry.from_dict(definition)
    if any(item.get("id") == entry.id for item in registry[list_key] if isinstance(item, dict)):
        raise ConfigurationError(f"duplicate {list_key.rstrip('s')} id: {entry.id}")
    registry[list_key].append(definition)
    registry[list_key].sort(key=lambda item: str(item.get("id", "")))
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=registry_path.name, dir=registry_path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(registry, handle, indent=2)
            handle.write("\n")
        os.replace(temp_name, registry_path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return entry.id

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


_ALLOWED_ADAPTERS = {"builtin", "command", "http", "ollama", "mcp", "api", "cli", "custom"}


@dataclass(frozen=True, slots=True)
class RegistryEntry:
    id: str
    enabled: bool
    adapter: str
    capabilities: frozenset[str]
    priority: int = 0
    cost_weight: float = 1.0
    config: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RegistryEntry":
        known = {"id", "enabled", "adapter", "capabilities", "priority", "cost_weight"}
        entry_id = value.get("id")
        if not isinstance(entry_id, str) or not entry_id.strip():
            raise ValueError("registry entry id must be a non-empty string")
        adapter = value.get("adapter")
        if adapter not in _ALLOWED_ADAPTERS:
            raise ValueError(f"unsupported adapter '{adapter}' for '{entry_id}'")
        capabilities = value.get("capabilities", [])
        if not isinstance(capabilities, list) or not all(isinstance(item, str) and item for item in capabilities):
            raise ValueError(f"capabilities for '{entry_id}' must be a list of non-empty strings")
        priority = value.get("priority", 0)
        cost_weight = value.get("cost_weight", 1.0)
        if not isinstance(priority, int):
            raise ValueError(f"priority for '{entry_id}' must be an integer")
        if not isinstance(cost_weight, (int, float)) or cost_weight <= 0:
            raise ValueError(f"cost_weight for '{entry_id}' must be positive")
        return cls(
            id=entry_id,
            enabled=bool(value.get("enabled", False)),
            adapter=adapter,
            capabilities=frozenset(capabilities),
            priority=priority,
            cost_weight=float(cost_weight),
            config={key: item for key, item in value.items() if key not in known},
        )

    def supports(self, required: set[str]) -> bool:
        return required.issubset(self.capabilities)


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    state: str
    bucket: str | None = None
    link: str | None = None

    @property
    def successful(self) -> bool:
        normalized = self.state.upper()
        bucket = (self.bucket or "").upper()
        if bucket:
            return bucket == "PASS"
        return normalized in {"SUCCESS", "PASS"}

    @property
    def terminal(self) -> bool:
        normalized = self.state.upper()
        bucket = (self.bucket or "").upper()
        return normalized not in {"PENDING", "QUEUED", "IN_PROGRESS", "WAITING"} and bucket != "PENDING"

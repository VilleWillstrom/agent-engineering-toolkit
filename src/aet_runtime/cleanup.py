from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .errors import ConfigurationError


@dataclass(frozen=True, slots=True)
class CleanupResult:
    deleted: tuple[Path, ...]
    retained: tuple[Path, ...]
    skipped: tuple[Path, ...]


class SessionCleaner:
    """Delete only AET-owned session directories carrying an explicit marker."""

    MARKER = "aet-session.json"

    def __init__(self, root: Path, *, retain_last: int = 10, max_age_days: int = 30) -> None:
        if retain_last < 0 or max_age_days < 0:
            raise ConfigurationError("retention values must be non-negative")
        self.root = root
        self.retain_last = retain_last
        self.max_age_days = max_age_days

    def clean(self, *, dry_run: bool = True, now: datetime | None = None) -> CleanupResult:
        now = now or datetime.now(timezone.utc)
        sessions: list[tuple[Path, datetime]] = []
        skipped: list[Path] = []
        if not self.root.exists():
            return CleanupResult((), (), ())
        for child in self.root.iterdir():
            if not child.is_dir():
                continue
            marker = child / self.MARKER
            if not marker.is_file():
                skipped.append(child)
                continue
            try:
                data = json.loads(marker.read_text(encoding="utf-8"))
                created = datetime.fromisoformat(str(data["created_at"]).replace("Z", "+00:00"))
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except (KeyError, ValueError, json.JSONDecodeError):
                skipped.append(child)
                continue
            sessions.append((child, created))

        sessions.sort(key=lambda item: item[1], reverse=True)
        retained_paths = {path for path, _ in sessions[: self.retain_last]}
        deleted: list[Path] = []
        retained: list[Path] = []
        for path, created in sessions:
            age_days = (now - created).total_seconds() / 86400
            if path in retained_paths or age_days <= self.max_age_days:
                retained.append(path)
                continue
            deleted.append(path)
            if not dry_run:
                shutil.rmtree(path)
        return CleanupResult(tuple(deleted), tuple(retained), tuple(skipped))


def write_session_marker(path: Path, *, provider: str, session_id: str, created_at: datetime | None = None) -> None:
    path.mkdir(parents=True, exist_ok=True)
    created_at = created_at or datetime.now(timezone.utc)
    payload = {
        "provider": provider,
        "session_id": session_id,
        "created_at": created_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "owner": "aet",
    }
    (path / SessionCleaner.MARKER).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

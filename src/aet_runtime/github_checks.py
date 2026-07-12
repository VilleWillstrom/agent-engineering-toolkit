from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Callable

from .errors import ExternalCommandError
from .models import CheckResult


@dataclass(frozen=True, slots=True)
class CheckSummary:
    checks: tuple[CheckResult, ...]

    @property
    def all_terminal(self) -> bool:
        return bool(self.checks) and all(check.terminal for check in self.checks)

    @property
    def all_successful(self) -> bool:
        return bool(self.checks) and all(check.successful for check in self.checks)


class GitHubChecksMonitor:
    FIELDS = "name,state,bucket,link"

    def __init__(self, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> None:
        self._runner = runner

    @staticmethod
    def available() -> bool:
        return shutil.which("gh") is not None

    def fetch(self, pr: str, *, repo: str | None = None, watch: bool = False, interval: int = 10) -> CheckSummary:
        command = ["gh", "pr", "checks", pr, "--json", self.FIELDS]
        if repo:
            command.extend(["--repo", repo])
        if watch:
            command.extend(["--watch", "--interval", str(interval)])
        result = self._runner(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "gh pr checks failed").strip()
            raise ExternalCommandError(message)
        try:
            rows = json.loads(result.stdout or "[]")
        except json.JSONDecodeError as exc:
            raise ExternalCommandError("gh returned invalid JSON") from exc
        checks = tuple(
            CheckResult(
                name=str(row.get("name", "unnamed")),
                state=str(row.get("state", "UNKNOWN")),
                bucket=row.get("bucket"),
                link=row.get("link"),
            )
            for row in rows
        )
        return CheckSummary(checks)

    @staticmethod
    def render(summary: CheckSummary) -> str:
        lines = [f"{check.name}: {check.state}" for check in summary.checks]
        outcome = "PASS" if summary.all_successful else "NOT_READY"
        return "\n".join([*lines, f"overall: {outcome}"])

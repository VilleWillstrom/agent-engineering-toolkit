from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .cleanup import SessionCleaner
from .errors import AetError
from .github_checks import GitHubChecksMonitor
from .registry import ExtensionRegistry


def _root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def _registry(root: Path, name: str, list_key: str) -> ExtensionRegistry:
    return ExtensionRegistry.load(root / ".agent-team" / name, kind=list_key.rstrip("s"), list_key=list_key)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aet", description="Agent Engineering Toolkit internal runtime")
    parser.add_argument("--root", help="product repository root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="validate registries and installed command adapters")
    doctor.add_argument("--strict", action="store_true", help="fail when an enabled executable is missing")

    providers = sub.add_parser("providers", help="list or select agent providers")
    providers.add_argument("action", choices=["list", "choose"])
    providers.add_argument("--capability", action="append", default=[])
    providers.add_argument("--prefer-local", action="store_true")

    platforms = sub.add_parser("platforms", help="list or select remote platform adapters")
    platforms.add_argument("action", choices=["list", "choose"])
    platforms.add_argument("--capability", action="append", default=[])

    cleanup = sub.add_parser("cleanup", help="prune AET-owned session artifacts")
    cleanup.add_argument("--apply", action="store_true", help="delete instead of dry-run")

    checks = sub.add_parser("checks", help="read or watch GitHub PR checks through gh")
    checks.add_argument("--pr", required=True)
    checks.add_argument("--repo")
    checks.add_argument("--watch", action="store_true")
    checks.add_argument("--interval", type=int, default=10)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = _root(args.root)
    try:
        if args.command == "doctor":
            providers = _registry(root, "providers.json", "providers")
            platforms = _registry(root, "platforms.json", "platforms")
            issues = [*providers.validate_commands(), *platforms.validate_commands()]
            print(json.dumps({"status": "ok" if not issues else "warning", "issues": issues}, indent=2))
            return 1 if issues and args.strict else 0

        if args.command == "providers":
            registry = _registry(root, "providers.json", "providers")
            if args.action == "list":
                print(json.dumps([entry.id for entry in registry.list()], indent=2))
            else:
                print(registry.choose(args.capability, prefer_local=args.prefer_local).id)
            return 0

        if args.command == "platforms":
            registry = _registry(root, "platforms.json", "platforms")
            if args.action == "list":
                print(json.dumps([entry.id for entry in registry.list()], indent=2))
            else:
                print(registry.choose(args.capability).id)
            return 0

        if args.command == "cleanup":
            config_path = root / ".agent-team" / "session-cleanup.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            cleaner = SessionCleaner(
                root / config.get("aet_session_root", ".agent-team/runtime/sessions"),
                retain_last=int(config.get("retain_last", 10)),
                max_age_days=int(config.get("max_age_days", 30)),
            )
            result = cleaner.clean(dry_run=not args.apply)
            print(json.dumps({
                "dry_run": not args.apply,
                "deleted": [str(path) for path in result.deleted],
                "retained": [str(path) for path in result.retained],
                "skipped": [str(path) for path in result.skipped],
            }, indent=2))
            return 0

        if args.command == "checks":
            monitor = GitHubChecksMonitor()
            summary = monitor.fetch(args.pr, repo=args.repo, watch=args.watch, interval=args.interval)
            print(monitor.render(summary))
            return 0 if summary.all_successful else 2
    except (AetError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"aet: {exc}", file=sys.stderr)
        return 1
    return 1

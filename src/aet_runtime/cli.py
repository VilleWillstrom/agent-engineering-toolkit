from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .adapters import ProviderExecutor
from .cleanup import SessionCleaner
from .errors import AetError, ConfigurationError
from .github_checks import GitHubChecksMonitor
from .registry import ExtensionRegistry
from .registry_edit import add_registry_entry


def _root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def _registry(root: Path, name: str, list_key: str) -> ExtensionRegistry:
    return ExtensionRegistry.load(root / ".agent-team" / name, kind=list_key.rstrip("s"), list_key=list_key)


def _prompt(args: argparse.Namespace) -> str:
    if getattr(args, "prompt", None) is not None:
        return args.prompt
    if getattr(args, "prompt_file", None) is not None:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise ConfigurationError("provider invocation requires --prompt or --prompt-file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aet", description="Agent Engineering Toolkit internal runtime")
    parser.add_argument("--root", help="product repository root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="validate registries and installed command adapters")
    doctor.add_argument("--strict", action="store_true", help="fail when an enabled executable is missing")

    providers = sub.add_parser("providers", help="list, select, add, or invoke agent providers")
    providers.add_argument("action", choices=["list", "choose", "add", "invoke"])
    providers.add_argument("--capability", action="append", default=[])
    providers.add_argument("--prefer-local", action="store_true")
    providers.add_argument("--definition")
    providers.add_argument("--provider")
    providers.add_argument("--prompt")
    providers.add_argument("--prompt-file")

    platforms = sub.add_parser("platforms", help="list, select, or add remote platform adapters")
    platforms.add_argument("action", choices=["list", "choose", "add"])
    platforms.add_argument("--capability", action="append", default=[])
    platforms.add_argument("--definition")

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
            registry_path = root / ".agent-team" / "providers.json"
            registry = _registry(root, "providers.json", "providers")
            if args.action == "list":
                print(json.dumps([entry.id for entry in registry.list()], indent=2))
            elif args.action == "choose":
                print(registry.choose(args.capability, prefer_local=args.prefer_local).id)
            elif args.action == "add":
                if not args.definition:
                    raise ConfigurationError("providers add requires --definition")
                print(add_registry_entry(registry_path, list_key="providers", definition_path=Path(args.definition)))
            else:
                if not args.provider:
                    raise ConfigurationError("providers invoke requires --provider")
                result = ProviderExecutor().execute(registry.get(args.provider), _prompt(args))
                print(json.dumps({"provider": result.provider_id, "text": result.text, "usage": result.usage}, indent=2))
            return 0

        if args.command == "platforms":
            registry_path = root / ".agent-team" / "platforms.json"
            registry = _registry(root, "platforms.json", "platforms")
            if args.action == "list":
                print(json.dumps([entry.id for entry in registry.list()], indent=2))
            elif args.action == "choose":
                print(registry.choose(args.capability).id)
            else:
                if not args.definition:
                    raise ConfigurationError("platforms add requires --definition")
                print(add_registry_entry(registry_path, list_key="platforms", definition_path=Path(args.definition)))
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

#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-repository> [--force]" >&2
  exit 64
fi

TARGET_PATH="$1"
FORCE="false"
[[ "${2:-}" == "--force" ]] && FORCE="true"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_ROOT="$TOOLKIT_ROOT/templates"
TARGET_ROOT="$(cd "$TARGET_PATH" && pwd)"

if [[ ! -d "$TARGET_ROOT/.git" ]]; then
  echo "Target must be the root of a Git repository: $TARGET_ROOT" >&2
  exit 65
fi

install_file() {
  local source="$1"
  local destination="$2"
  local target="$TARGET_ROOT/$destination"

  mkdir -p "$(dirname "$target")"
  if [[ -e "$target" && "$FORCE" != "true" ]]; then
    echo "Skipped existing file: $destination" >&2
    return
  fi

  cp "$TEMPLATE_ROOT/$source" "$target"
  echo "Installed $destination"
}

install_file "AGENTS.md" "AGENTS.md"
install_file "CLAUDE.md" "CLAUDE.md"
install_file ".agent-team/manifest.yaml" ".agent-team/manifest.yaml"
install_file ".agent-team/routing.yaml" ".agent-team/routing.yaml"
install_file ".agent-team/permissions.yaml" ".agent-team/permissions.yaml"
install_file ".agent-team/commands.yaml" ".agent-team/commands.yaml"
install_file ".agent-team/observability.yaml" ".agent-team/observability.yaml"
install_file ".agent-team/metrics/model-usage.csv" ".agent-team/metrics/model-usage.csv"
install_file ".agent-team/metrics/README.md" ".agent-team/metrics/README.md"
install_file "task-contract.yaml" ".agent-team/tasks/TASK-TEMPLATE.yaml"

mkdir -p "$TARGET_ROOT/.agent-team/reviews"
touch "$TARGET_ROOT/.agent-team/reviews/.gitkeep"
tr -d '\r\n' < "$TOOLKIT_ROOT/VERSION" > "$TARGET_ROOT/.agent-team/toolkit-version"

echo "Toolkit $(cat "$TOOLKIT_ROOT/VERSION") installed. Replace all placeholders using verified repository evidence before committing."
echo "Codex must now ask the human whether local model-usage telemetry may be recorded and persist the answer in .agent-team/observability.yaml."

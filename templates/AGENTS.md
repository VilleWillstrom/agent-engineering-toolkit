# Project Agent Instructions

This product repository uses Agent Engineering Toolkit version `{{TOOLKIT_VERSION}}`.

## Source of truth

- Product intent and delivery scope: `{{PROJECT_DOCS_PATH}}`
- Architecture: `{{ARCHITECTURE_DOCS_PATH}}`
- Machine-readable agent configuration: `.agent-team/`
- Shared toolkit policy: `{{TOOLKIT_SOURCE}}`

Repository evidence overrides assumptions. Unknown facts must be marked `UNKNOWN` rather than invented.

## Project facts

- Project: `{{PROJECT_NAME}}`
- Technology stack: `{{TECH_STACK}}`
- Architecture: `{{ARCHITECTURE}}`
- Protected branch: `{{PROTECTED_BRANCH}}`
- Active delivery scope: `{{ACTIVE_SCOPE}}`

## Required commands

Use `.agent-team/commands.yaml` as the command source.

- Build: `{{BUILD_COMMAND}}`
- Unit tests: `{{TEST_COMMAND}}`
- Lint/static analysis: `{{LINT_COMMAND}}`

Never claim a command or CI check passed unless it completed successfully.

## Chat-first workflow

VS Code Codex chat is the primary human interface. Codex may invoke the internal `aet` CLI, GitHub CLI, provider adapters, MCP servers, APIs, and local tools without requiring the human to operate them manually.

Codex is the Engineering Director, task planner, capability router, continuity owner, runtime-test owner, Git/PR owner, final reviewer, and permission-override coordinator.

## Agent provider pool

Use `.agent-team/providers.json` as the provider registry. Route tasks by required capabilities and enabled providers, considering availability, project telemetry, quality, priority, locality, and cost.

Claude Code is the default UI/UX/design specialist, but Gemini API, local Ollama models, and future providers may be enabled through validated registry entries. Scripted Claude work uses stateless print mode by default so one-shot AET tasks do not accumulate in normal conversation history.

If a provider fails, reaches usage limits, times out, or returns unusable work, Codex preserves evidence and continues with another enabled capable provider or as `codex-self` without reducing acceptance criteria.

## Remote platform pool

Use `.agent-team/platforms.json` for Supabase, Render, Northflank, Google Cloud, Azure, and future MCP/API/CLI platforms. New integrations require official-method verification, environment permissions, validation, rollback guidance, tests, and audit behavior.

## GitHub checks and delivery

After pushing a task branch, Codex opens a draft PR and watches configured checks using `aet checks` or equivalent `gh pr checks --watch`. Pending checks are not success. Failed checks must be investigated and corrected within the configured attempt limit.

The task should produce the most complete smoke-testable artifact or deployment practical for the project before requesting human acceptance.

## Conditional restrictions and session overrides

Repository restrictions are safe defaults. The human may override them for a concrete task and current session.

Before any conflicting action begins, ask:

> Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

Request the narrowest sufficient scope and record the answer. Silence, ambiguity, or approval from another session is not authorization. A session override expires at session end and does not permanently change policy.

An override cannot create missing credentials, permissions, quota, subscription, tooling, or platform capability.

## Usage telemetry

After initialization, ask once whether local model-usage telemetry may be recorded and persist the answer in `.agent-team/observability.yaml`.

## Completion requirements

A task is complete only when implementation, automated validation, applicable interactive testing, provider/fallback history, session cleanup, PR/check state, external changes, overrides, artifacts, smoke-test instructions, and residual risks are reported honestly.
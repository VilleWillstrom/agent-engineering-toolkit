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

Use `.agent-team/commands.yaml` as the machine-readable command source.

- Build: `{{BUILD_COMMAND}}`
- Unit tests: `{{TEST_COMMAND}}`
- Lint/static analysis: `{{LINT_COMMAND}}`

Do not claim a command passed unless it was actually executed successfully.

## Agent workflow

Codex is the Engineering Director, task planner, router, continuity owner, runtime-test owner, final reviewer, and permission-override coordinator.

Claude Code is an optional scoped implementation and UI/UX/design worker. By default it does not operate the product; Codex supplies static visual/runtime evidence and performs interactive validation.

If Claude becomes unavailable, Codex preserves and reviews partial work and continues the task as `codex-self` without reducing acceptance criteria.

## Conditional restrictions and session overrides

Repository restrictions are safe defaults. The human may override them for a concrete task and current session.

Before any conflicting action begins, the agent must stop and ask:

> Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

The agent must name the exact restriction and reason, request the narrowest sufficient scope, and record the answer under `.agent-team/overrides/`. Silence, ambiguity, or approval from another session is not authorization.

A session override expires at session end and does not permanently change project policy. A permanent change requires a separate proposed diff and explicit approval.

An override cannot bypass system/platform enforcement, applicable law or service terms, missing credentials or permissions, unavailable quota/subscription, or unavailable tooling.

## Usage telemetry permission

Immediately after toolkit initialization, Codex asks once whether local model-usage telemetry may be recorded. Persist the answer in `.agent-team/observability.yaml`; do not rely on conversation memory.

## Engineering boundaries

- Preserve separation of concerns and the established architecture.
- Avoid god files, hidden global state, unnecessary dependencies, and speculative abstraction.
- Verify dependency maintenance, adoption, compatibility, and license before adding one.
- Keep documentation and tests synchronized with behavior.
- Avoid unrelated cleanup inside scoped tasks.

## Completion requirements

Every implementation must use the base permissions plus active overrides, run required validation, receive Codex review, report worker fallback and override use, and provide honest remaining risks. Push, merge, deployment, publication, signing, secret access, and other restricted operations are permitted only when base policy allows them or the human grants the required scoped override.
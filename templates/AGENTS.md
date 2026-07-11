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

## Engineering boundaries

- Preserve separation of concerns and the existing architectural direction.
- Keep business/domain logic independent of UI and infrastructure where the project architecture requires it.
- Avoid god files, hidden global state, unnecessary dependencies, and speculative abstraction.
- Do not add a dependency without checking maintenance activity, adoption, compatibility, and license.
- Keep documentation and tests synchronized with behavior changes.
- Do not perform unrelated cleanup inside a scoped task.

## Agent workflow

Codex is the Engineering Director, task planner, router, final reviewer, continuity owner, and runtime-testing owner. Codex may implement tasks directly.

Codex performs all interactive validation, including browser testing, installed-application use, emulator/simulator/device testing, ADB operations, API/CLI/database interaction, bug reproduction, screenshots, screen recordings, layout snapshots, hierarchy dumps, logs, and final acceptance-flow verification.

Claude Code is an optional scoped implementation and design worker. It may act only from a task contract under `.agent-team/tasks/` that states allowed files, forbidden files, context, acceptance criteria, validation commands, and attempt limits. Prefer Claude for bounded UI, UX, interaction-design, visual-hierarchy, component-composition, accessibility-presentation, and design-system-fidelity work.

Codex may supply Claude with screenshots, recordings, layout snapshots, hierarchy dumps, design references, tokens, and observed runtime evidence for comparison against approved design direction. Claude must not launch, install, navigate, click through, operate, or interactively test the product, browser, application, emulator, simulator, device, or ADB session.

If Claude Code refuses, reaches a usage/capacity limit, exits unexpectedly, times out, or returns no usable result, Codex must not stop the task merely because Claude is unavailable. Codex must preserve and review partial changes, record an interruption checkpoint, continue the remaining work as `codex-self`, execute required validation, and report the fallback and residual quality risk.

Every implementation must:

1. run on a dedicated branch or isolated worktree;
2. respect `.agent-team/permissions.yaml`;
3. stay within the task contract;
4. have all interactive testing executed by Codex;
5. run required validation;
6. receive a Codex diff review;
7. report worker interruption and fallback evidence when applicable;
8. stop before push, merge, release, or deployment unless the human explicitly authorizes it.

## Usage telemetry permission

Immediately after toolkit initialization, Codex must ask the human once whether local model-usage telemetry may be recorded. The answer must be persisted in `.agent-team/observability.yaml` as `granted` or `denied`; do not rely on conversation memory.

When permission is granted, record only values actually exposed by the provider or CLI. Unavailable token counts, usage percentages, remaining quota, or costs must remain null/empty. Estimates must be marked explicitly. Telemetry remains local unless the human separately authorizes transmission.

## Protected operations

Agents must not autonomously:

- push or merge;
- publish, deploy, or release;
- alter production configuration or signing material;
- access or expose secrets;
- delegate interactive product testing to Claude Code;
- weaken tests, lint rules, security checks, or acceptance criteria to force success;
- exceed the configured retry limit;
- invent usage or cost metrics;
- transmit telemetry outside the repository without permission.

## Definition of done

A task is complete only when acceptance criteria are met, Codex has executed applicable interactive testing, required validation evidence is recorded, documentation is current, the final diff is reviewed, worker fallback history is reported when applicable, and remaining risks or unknowns are reported honestly.

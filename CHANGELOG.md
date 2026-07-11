# Changelog

All notable changes to this project are documented here.

## 0.3.0 — 2026-07-11

- Assigned all browser, application, emulator, simulator, device, ADB, CLI, API, database, and other interactive runtime testing to Codex.
- Prohibited Claude Code from launching, navigating, operating, or interactively testing products and runtime environments.
- Made Claude Code the preferred scoped specialist for UI, UX, interaction design, visual hierarchy, accessibility presentation, component composition, and design-system fidelity.
- Added a static evidence handoff workflow where Codex supplies screenshots, recordings, layout snapshots, hierarchy dumps, design references, and runtime observations to Claude.
- Added `policies/testing-and-design-ownership.md` and updated routing, orchestrator, project templates, and README guidance.
- Required Codex to repeat applicable interactive validation after Claude-assisted implementation and retain final accountability for runtime truth.

## 0.2.0 — 2026-07-10

- Made Claude Code an optional worker rather than a task-completion dependency.
- Added mandatory Codex fallback when Claude is usage-limited, refuses, times out, exits, or returns no usable result.
- Added interruption classification, checkpointing, and final residual-quality reporting requirements.
- Added persistent opt-in usage telemetry consent under `.agent-team/observability.yaml`.
- Added local CSV/JSONL-compatible model usage reporting templates.
- Added routing guidance to prefer the least expensive capable model and use costly frontier models only when their observed quality advantage justifies usage.
- Updated PowerShell and Bash bootstrap scripts to install observability files and prompt Codex to request telemetry permission.

## 0.1.0 — 2026-07-10

- Added the Codex Engineering Director and Claude Code scoped-worker operating model.
- Added a ready-to-copy Codex initialization prompt to the README.
- Added project-local templates for AGENTS.md, CLAUDE.md, manifest, routing, permissions, commands, and task contracts.
- Added model-routing and review policies.
- Added PowerShell and Bash project bootstrap scripts.
- Added a PowerShell structural validation script.
- Added an initial JSON Schema for task contracts.
- Established human approval, protected-branch, secret-handling, and finite-retry safeguards.

# Changelog

All notable changes to this project are documented here.

## 0.5.0 — 2026-07-12

- Added a dependency-free Python runtime and internal `aet` CLI while keeping VS Code Codex chat as the primary user interface.
- Added capability-based agent provider registries with built-in templates for Codex, Claude Code, Gemini API, and local Ollama models.
- Added extensible MCP/API/CLI platform registries with templates for Supabase, Render, Northflank, Google Cloud, and Azure.
- Configured scripted Claude Code work to use stateless print mode so AET-created worker runs do not fill normal Claude Code conversation history.
- Added safe AET-owned session cleanup and an override-gated legacy Claude project purge path.
- Added deterministic GitHub PR checks monitoring through `gh pr checks --watch`.
- Added a GitHub Actions Python 3.11–3.13 test matrix and comprehensive unit tests for registries, selection, cleanup, CLI behavior, and PR check parsing.
- Updated bootstrap scripts to install provider, platform, cleanup, and GitHub runtime configuration.

## 0.4.0 — 2026-07-11

- Made toolkit and project-policy restrictions conditional defaults rather than permanent prohibitions.
- Added a mandatory pre-execution Finnish override confirmation prompt with concrete restriction and reason placeholders.
- Added session-scoped, least-privilege override authorization and audit logging under `.agent-team/overrides/`.
- Added explicit expiration, denial, revocation, and persistent-policy-change rules.
- Clarified that overrides cannot create unavailable system capabilities, credentials, permissions, quota, subscriptions, or tooling, and cannot bypass external legal or platform constraints.
- Updated project templates, permissions, orchestrator instructions, and bootstrap scripts to install and enforce the override workflow.

## 0.3.0 — 2026-07-11

- Assigned all browser, application, emulator, device, ADB, API, CLI, database, and other interactive runtime testing to Codex.
- Positioned Claude Code as the preferred bounded UI/UX/design specialist working from static evidence packages.
- Added `policies/testing-and-design-ownership.md` and updated routing, prompts, and project templates.
- Required Codex to provide runtime evidence and final interactive acceptance testing after Claude-assisted UI work.

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

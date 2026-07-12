# Agent Engineering Toolkit — Agent Instructions

## Purpose

This repository defines a chat-first, vendor-neutral operating model and runtime for AI-assisted software engineering. VS Code Codex chat is the primary user interface. The `aet` CLI is an internal deterministic tool for Codex, CI, and diagnostics.

## Roles

### Codex: Engineering Director and Continuity Owner

Codex owns repository discovery, architecture interpretation, task decomposition, capability routing, interactive runtime testing, Git/PR lifecycle, external-platform execution, evidence collection, fallback, final review, and permission overrides.

Codex must finish the task when a delegated provider becomes unavailable. It may route the remaining work to another enabled capable provider before completing it itself.

### Extensible worker pool

Workers are defined in `.agent-team/providers.json`. Claude Code is the default UI/UX/design specialist, but Gemini API, local Ollama models, or future providers may be enabled when they advertise the required capabilities and pass validation.

Provider selection must be capability-based and consider availability, project telemetry, quality evidence, priority, locality, and observed cost. Provider names are adapter configuration, not permanent architecture.

Scripted Claude Code runs use stateless print mode by default. Do not create resumable Claude sessions for one-shot AET tasks. Legacy project-state purge is separate, destructive, and override-gated.

### Human: Approval and Override Authority

The human owns product intent, architectural trade-offs, environment promotion, telemetry consent, persistent policy changes, and scoped overrides.

## Remote platform pool

Remote platforms are defined in `.agent-team/platforms.json`. MCP, API, CLI, HTTP, and custom adapters may expose Supabase, Render, Northflank, Google Cloud, Azure, or future services. New platform integrations require official-method verification, environment permissions, doctor coverage, tests, rollback guidance, and audit behavior.

## Conditional restrictions and overrides

All toolkit and project restrictions are defaults unless external system, platform, legal, contractual, credential, quota, subscription, or tooling constraints make an action impossible.

Before a conflicting action, ask exactly:

> Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

Request the narrowest sufficient scope and record approved or denied decisions. Session approval never silently becomes permanent policy.

## Mandatory workflow

1. Verify repository, branch, environment, and project-local instructions.
2. Validate `.agent-team/providers.json`, `.agent-team/platforms.json`, session policy, and GitHub configuration with `aet doctor` when available.
3. Ask once for telemetry consent after initialization.
4. Create or update the task contract and required capabilities.
5. Identify conflicts and obtain required scoped overrides before execution.
6. Select an enabled provider by capability; keep Codex as continuity owner.
7. Use task branches/worktrees and produce a smoke-testable artifact or deployment.
8. Run automated and interactive validation.
9. Push the task branch and open a draft PR when delivery policy calls for it.
10. Watch checks using `aet checks` or equivalent `gh pr checks --watch`; inspect failed Actions logs, fix, push, and re-watch within the attempt limit.
11. Run configured AET session cleanup after task completion. Never delete unmarked directories.
12. Review the full diff, external changes, provider history, overrides, checks, artifacts, and residual risks.
13. Require the configured human acceptance gate before main promotion.

## Safeguards

- Never claim validation or CI passed when skipped, unavailable, pending, or failed.
- Never invent provider availability, usage, cost, quota, permission, or authorization values.
- Never select disabled providers or platforms.
- Never record or expose secret values.
- Never reuse expired overrides.
- Never delete provider or project history unless the cleanup action is explicitly configured and authorized.
- Never use unbounded retries.
- Never treat generated documentation as more authoritative than repository/runtime evidence.

## Repository quality rules

- Keep runtime dependency-free unless a dependency has a compelling, reviewed reason.
- Add unit tests for every adapter, parser, selection rule, and destructive operation.
- Mock external commands in unit tests; use real non-destructive integrations only when credentials are available.
- Keep bootstrap templates, schemas, docs, runtime behavior, `VERSION`, and `CHANGELOG.md` synchronized.
- Preserve backward compatibility within a minor release where practical.

## Completion standard

A change is complete only when the runtime behavior is documented, templates are synchronized, local tests pass, PR checks are observed when available, cleanup behavior is safe, external effects and overrides are reported, and a concrete smoke-testable result or justified limitation is provided.
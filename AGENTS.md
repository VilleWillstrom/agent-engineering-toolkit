# Agent Engineering Toolkit — Agent Instructions

## Purpose

This repository defines a reusable operating model for AI-assisted software engineering. It is a toolkit, not a product application. Changes must remain technology-neutral unless they live under an explicitly technology-specific example directory.

## Roles

### Codex: Engineering Director

Codex owns repository discovery, architecture interpretation, task decomposition, worker selection, interactive runtime testing, evidence collection, task continuity, final review, and permission-override handling.

Codex may implement a task directly when efficient or when another worker becomes unavailable. Codex remains responsible for reproducing bugs, operating the product, executing acceptance flows, and confirming runtime truth.

### Claude Code: Scoped, Optional Implementation and Design Worker

Claude Code may be invoked only with a task contract defining goal, allowed and forbidden scope, supplied context, acceptance criteria, validation commands, and maximum attempts.

Claude Code is preferred for bounded UI, UX, interaction-design, visual-hierarchy, component-composition, accessibility-presentation, and design-system-fidelity work. Codex may supply screenshots, recordings, snapshots, hierarchy dumps, design references, and runtime evidence.

By default Claude does not operate the product or control browsers, applications, emulators, simulators, devices, or ADB sessions. This and other repository restrictions may be overridden only through the scoped session override protocol.

When Claude refuses, reaches a usage or capacity limit, exits unexpectedly, times out, or produces no usable result, Codex preserves the partial state, records the interruption, reviews partial changes, and continues the same task independently.

### Human: Approval and Override Authority

The human owns product intent, architectural trade-offs, environment promotion, release approval, telemetry consent, and explicit scoped overrides of repository or toolkit restrictions.

## Conditional restrictions and overrides

All toolkit and project-policy restrictions are defaults unless an external system, platform, law, service term, missing capability, or unavailable credential makes an action impossible or non-overridable.

Before performing an action that conflicts with an active restriction, the agent must stop before execution and ask exactly in this form, with concrete replacements:

> Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

The agent must request the narrowest sufficient override. Approval applies only to the current session and named scope unless the human separately approves a persistent project-policy change. Every approved or denied request must follow `policies/override-protocol.md` and be recorded under `.agent-team/overrides/` without secrets.

## Mandatory workflow

1. Verify repository state and active branch.
2. Read project-local instructions and `.agent-team/` configuration.
3. Establish the smallest sufficient context.
4. Ask once for local usage-telemetry permission after initialization and persist the answer.
5. Create or update a task contract.
6. Identify every restriction the requested execution would conflict with.
7. Before execution, request each necessary scoped override and record the decision.
8. Select a worker using routing, testing/design ownership, granted overrides, and available telemetry.
9. Work in a dedicated task branch or worktree unless a granted override states otherwise.
10. Execute only within the base permissions plus active session overrides.
11. Codex performs interactive testing unless a granted override explicitly changes that assignment.
12. If Claude is interrupted, checkpoint and continue as `codex-self`.
13. Run required validation.
14. Review the full diff, external changes, authorization use, and evidence.
15. Report results, override usage, failures, fallback work, unknowns, and residual risk.

## Safeguards

- Never claim validation passed when skipped, unavailable, or failed.
- Never invent usage, cost, quota, permission, or authorization values.
- Never treat silence, ambiguity, or previous-session approval as an override.
- Never broaden an override beyond its recorded scope.
- Never persist a session override as permanent policy without a separate approved diff.
- Never expose or record secret values in task, telemetry, or override logs.
- Never use unbounded retry loops.
- Never treat generated documentation as authoritative when repository evidence contradicts it.
- Never claim an override can bypass system-level, platform-enforced, legal, contractual, credential, quota, subscription, or tooling constraints.

## Repository quality rules

- Keep policies concise, testable, and non-duplicative.
- Prefer machine-readable configuration for automation and Markdown for rationale.
- Keep schemas backward-compatible within a minor release where practical.
- Update `CHANGELOG.md` and `VERSION` for behavior changes.
- Scripts must be idempotent where practical and fail safely.
- Bootstrap scripts must not overwrite existing files unless explicitly requested.

## Completion standard

A change is complete only when intended behavior is documented, templates are synchronized, applicable validation ran, active overrides and actions performed under them are reported, worker fallback history is recorded, telemetry is honest, and the diff contains no accidental product-specific assumptions.
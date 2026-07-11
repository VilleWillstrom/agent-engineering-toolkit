# Model Routing Policy

Select a worker based on verified task characteristics, not preference or novelty.

## Codex self-execution

Prefer Codex when the task is narrow, low-risk, strongly evidenced, and inexpensive to implement and review in one context. Typical examples include documentation, configuration, focused tests, small bug fixes, repository maintenance, and all interactive product validation.

Codex always owns browser, application, emulator, simulator, device, ADB, CLI, API, database, and other runtime interaction needed to reproduce or validate behavior. Codex may collect screenshots, screen recordings, layout snapshots, hierarchy dumps, logs, and other evidence for specialist review.

## Claude Code delegation

Delegate to Claude Code when an independent scoped worker is likely to improve implementation quality or context efficiency. Claude is particularly suitable for bounded UI, UX, interaction-design, visual-hierarchy, component-composition, accessibility-presentation, and design-system-fidelity work.

Delegation requires a complete task contract, explicit file boundaries, supplied relevant context, validation commands, and a finite attempt limit. For design work, Codex supplies screenshots, layout snapshots, design references, and observed runtime evidence.

Claude must not launch, navigate, install, operate, or interactively test the product. Codex performs those steps before and after Claude's contribution.

## Human escalation

Escalate when product intent, architecture, destructive migration, security posture, cost, licensing, or public API direction is ambiguous. Agents must not turn ambiguity into an invented decision.

## Prohibited routing behavior

- Do not delegate trivial work merely to use another model.
- Do not delegate interactive application testing to Claude Code.
- Do not grant repository-wide scope when narrower scope is sufficient.
- Do not select a more expensive worker without a concrete reason.
- Do not retry indefinitely or silently switch workers after repeated failure.
- Do not use model names as permanent policy assumptions; capabilities and availability change.

# Model Routing Policy

Select a worker based on verified task characteristics, not preference or novelty.

## Codex self-execution

Prefer Codex when the task is narrow, low-risk, strongly evidenced, and inexpensive to implement and review in one context. Typical examples include documentation, configuration, focused tests, small bug fixes, and repository maintenance.

## Claude Code delegation

Delegate to Claude Code when an independent scoped worker is likely to improve implementation quality or context efficiency. Delegation requires a complete task contract, explicit file boundaries, supplied relevant context, validation commands, and a finite attempt limit.

## Human escalation

Escalate when product intent, architecture, destructive migration, security posture, cost, licensing, or public API direction is ambiguous. Agents must not turn ambiguity into an invented decision.

## Prohibited routing behavior

- Do not delegate trivial work merely to use another model.
- Do not grant repository-wide scope when narrower scope is sufficient.
- Do not select a more expensive worker without a concrete reason.
- Do not retry indefinitely or silently switch workers after repeated failure.
- Do not use model names as permanent policy assumptions; capabilities and availability change.

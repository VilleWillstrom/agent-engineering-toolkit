# Scoped Session Override Protocol

Repository and toolkit restrictions are defaults, not permanent prohibitions. A human may authorize a narrower or broader action when the requested task genuinely requires it.

## Mandatory pre-execution behavior

Before performing any action that conflicts with an active toolkit, repository, task-contract, environment, Git, deployment, signing, secret, network, testing, model-routing, or remote-platform restriction, the agent must stop before execution and ask:

> Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

The agent must replace both placeholders with concrete, understandable facts. It must not ask for a blanket override when a narrower authorization is sufficient.

## Scope rules

An override must be:

- granted explicitly by the human;
- limited to the current session unless the human separately requests a persistent project-policy change;
- limited to the named task, environment, platform, branch, operation, resource, and time window where practical;
- recorded before the restricted action begins;
- revocable by the human at any time;
- excluded from unrelated future tasks.

Silence, an ambiguous instruction, a previous session, or inferred intent is not sufficient authorization.

## Required record

Record approved overrides under `.agent-team/overrides/session-overrides.jsonl` with:

- override_id;
- session_id when available;
- task_id;
- restriction;
- reason;
- requested_scope;
- granted_scope;
- environment;
- platform or resource;
- granted_by;
- granted_at;
- expires_at or `session_end`;
- status;
- actions_performed;
- outcome;
- residual_risk.

Do not record secrets or sensitive credential values in the override log.

## Denied or unanswered requests

If the human denies the override or does not answer, the agent must not perform the restricted action. It may continue with the largest safe subset of the task that does not require the override and report the blocked portion.

## Persistent policy changes

A session override does not edit repository policy automatically. If the human wants the permission to remain for later sessions, the agent must separately propose the exact project-policy change, show the diff, and obtain explicit approval before persisting it.

## Non-overridable external constraints

This protocol cannot override:

- system-level or platform-enforced restrictions;
- applicable law or service terms;
- unavailable credentials, permissions, subscriptions, quotas, or capabilities;
- safety controls outside the repository that the agent is not authorized or technically able to change.

The agent must state when a requested action is impossible rather than pretending an override grants unavailable capability.

## Final reporting

The final report must list every override requested, whether it was granted, the exact actions performed under it, whether the authorization expired, and any residual risk created by the exception.
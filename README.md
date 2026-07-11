# Agent Engineering Toolkit

A versioned, vendor-neutral foundation for running a disciplined AI engineering team inside a software repository.

Codex acts as Engineering Director, integration owner, runtime tester, continuity owner, and final reviewer. Claude Code is an optional scoped implementation and UI/UX/design specialist. The workflow aims to produce a build, preview, deployment, APK, or other concrete artifact for human smoke testing rather than stopping at a code diff.

> Status: **v0.4.0 foundation**. Repository restrictions are safe defaults that may be overridden through explicit, scoped, session-only human authorization.

## What this repository provides

- Project-local `AGENTS.md` and `CLAUDE.md` templates.
- Machine-readable task, routing, permission, telemetry, and override configuration.
- Claude-to-Codex fallback when Claude becomes unavailable.
- Codex-owned interactive runtime testing and Claude-focused UI/UX/design work.
- Local opt-in model usage reporting.
- Scoped session override protocol with an audit trail.
- PowerShell and Bash project bootstrap scripts.

## Fastest way to use it

Open the target product repository in Codex and paste this prompt:

```text
You are the Engineering Director responsible for initializing and operating a safe, versioned multi-agent engineering workflow in the currently open product repository.

Assumptions:
- OpenAI Codex is installed and authenticated.
- Claude Code CLI is installed and authenticated.
- The reusable toolkit source is https://github.com/VilleWillstrom/agent-engineering-toolkit.
- The current repository is the product repository. Do not turn it into a fork of the toolkit.

Your task:
1. Read the toolkit README, AGENTS.md, policies, schemas, prompts, and templates.
2. Inspect the product repository using targeted discovery. Verify its stack, architecture, build/test/lint commands, protected branches, environments, deployment targets, signing approach, remote platforms, and current delivery scope. Mark unknowns; do not guess.
3. Install or update the project-local toolkit layer using the bootstrap script when practical.
4. Create or update:
   - AGENTS.md
   - CLAUDE.md
   - .agent-team/manifest.yaml
   - .agent-team/routing.yaml
   - .agent-team/permissions.yaml
   - .agent-team/commands.yaml
   - .agent-team/observability.yaml
   - .agent-team/overrides.yaml
   - .agent-team/metrics/
   - .agent-team/overrides/
   - .agent-team/tasks/
   - .agent-team/reviews/
   - .agent-team/toolkit-version
5. Keep shared toolkit rules separate from project-specific facts.
6. Ask once after initialization whether local model-usage telemetry may be recorded and persist the answer in `.agent-team/observability.yaml`.
7. Treat all toolkit and repository restrictions as conditional defaults unless an external system, platform, applicable law or service term, missing permission/credential, unavailable quota/subscription, or unavailable tooling makes the action impossible or non-overridable.
8. Before performing any action that conflicts with an active restriction, stop before execution and ask exactly, replacing the placeholders with concrete facts:

   Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

9. Request the narrowest sufficient override. Record approved and denied requests under `.agent-team/overrides/`. Approval applies only to the current session and recorded task, operation, environment, platform, branch, resource, and scope. Silence, ambiguity, or another session is not authorization.
10. A session override must not silently become permanent policy. For a persistent change, propose the exact policy diff and request separate explicit approval.
11. Codex owns interactive runtime testing by default: browser, installed application, emulator, simulator, physical device, ADB, API, CLI, database, filesystem, bug reproduction, screenshots, recordings, layout snapshots, logs, and acceptance flows.
12. Prefer Claude for bounded UI, UX, interaction design, visual hierarchy, accessibility presentation, component composition, and design-system fidelity. Supply Claude with static evidence collected by Codex. Claude does not operate the product unless the human explicitly grants a scoped session override for that restriction.
13. Treat Claude as optional. If it refuses, reaches a usage/capacity limit, exits, times out, or produces no usable result, preserve and review partial work, record the interruption, and continue the same task as `codex-self` without reducing acceptance criteria.
14. Use task branches/worktrees and non-production environments according to project policy. When the requested delivery requires push, merge, deployment, remote-platform configuration, signing, secret access, or another restricted operation, request the required override before execution unless base project policy already allows it.
15. Use remote platforms such as Supabase, Render, Northflank, or equivalent MCP/API/CLI integrations only within verified permissions and the user-authorized environment scope. Record external changes and rollback information.
16. Run all applicable automated and interactive validation.
17. Produce the most complete smoke-testable result possible: artifact, preview URL, integration deployment, APK, installer, staging endpoint, hashes, commit SHA, test evidence, known risks, and smoke-test instructions as applicable.
18. In the final report, list every override requested, whether it was granted, actions performed under it, its expiration, worker fallback history, validation evidence, external changes, and residual risk.

Project-specific intent:
[DESCRIBE THE PROJECT, CURRENT MILESTONE, DESIRED TESTABLE DELIVERABLE, AND IMPORTANT CONSTRAINTS HERE.]

Begin by reporting verified repository facts. Perform initialization in a dedicated branch. Ask for telemetry consent after initialization and request any required restriction override before the restricted action begins.
```

## Manual bootstrap

### PowerShell

```powershell
git clone https://github.com/VilleWillstrom/agent-engineering-toolkit.git
./agent-engineering-toolkit/scripts/init-project.ps1 -TargetPath ./my-project
```

### Bash

```bash
git clone https://github.com/VilleWillstrom/agent-engineering-toolkit.git
./agent-engineering-toolkit/scripts/init-project.sh ./my-project
```

Bootstrap does not overwrite existing files unless `-Force` or `--force` is supplied.

## Installed structure

```text
product-repository/
├── AGENTS.md
├── CLAUDE.md
└── .agent-team/
    ├── manifest.yaml
    ├── routing.yaml
    ├── permissions.yaml
    ├── commands.yaml
    ├── observability.yaml
    ├── overrides.yaml
    ├── toolkit-version
    ├── metrics/
    ├── overrides/
    ├── tasks/
    └── reviews/
```

## Override model

Restrictions are defaults, not invisible permanent walls. When the task requires an exception, the agent must identify it before execution, explain why it is needed, request a narrowly scoped current-session authorization, and record the decision.

A session override:

- applies only to the recorded scope;
- expires at session end by default;
- may be revoked at any time;
- cannot be reused in another session;
- does not permanently modify project policy;
- cannot create unavailable access or bypass external constraints.

See `policies/override-protocol.md`.

## Default role split

- **Codex:** planning, integration, Git lifecycle, runtime operation, testing, remote-platform execution, evidence, fallback, and final review.
- **Claude Code:** scoped implementation and UI/UX/design specialization from supplied context and static evidence.
- **Human:** product acceptance, override authorization, persistent policy changes, and environment promotion according to project policy.

Every default role restriction may be overridden for the current session through the same explicit protocol when the user judges the exception worthwhile.

## Usage telemetry

Telemetry is disabled until the human grants permission. Record only values actually exposed by providers or CLIs. Unavailable values remain null/empty, and estimates must be explicitly marked.

## Versioning

Projects record the installed toolkit version in `.agent-team/toolkit-version`. Shared behavior follows semantic versioning. Project-local policy must not be overwritten blindly during toolkit updates.

## License

MIT. See [LICENSE](LICENSE).
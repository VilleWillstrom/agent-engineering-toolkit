# Agent Engineering Toolkit

A versioned, vendor-neutral foundation for running a disciplined AI engineering team inside a software repository.

The default workflow assumes that **OpenAI Codex** and **Claude Code** are already installed and authenticated. Codex acts as the engineering director, planner, router, continuity owner, and reviewer. Claude Code is an optional scoped implementation worker when delegation is justified. Codex may also implement tasks itself and must finish delegated work when Claude becomes unavailable.

> Status: **v0.2.0 foundation**. Human approval remains mandatory before merging or pushing agent-produced changes.

## What this repository provides

- A reusable `AGENTS.md` policy for the orchestrator and workers.
- A machine-readable project manifest and task-contract format.
- Model-routing, Git, testing, security, review, fallback, and usage-observability policies.
- Prompt templates for planning, implementation, and review.
- Bootstrap scripts for installing the toolkit into another repository.
- Opt-in local CSV/JSONL-compatible model usage reporting.
- A ready-to-copy Codex bootstrap prompt below.

## Fastest way to use it

Open the target project in Codex and paste the following prompt. Replace the bracketed values when useful; Codex must inspect the target repository rather than inventing project facts.

```text
You are the Engineering Director responsible for initializing a safe, versioned multi-agent engineering workflow in the currently open repository.

Assumptions:
- OpenAI Codex is installed and authenticated.
- Claude Code CLI is installed and authenticated.
- The reusable toolkit source is https://github.com/VilleWillstrom/agent-engineering-toolkit.
- The current repository is the product repository to be managed. Do not turn it into a fork of the toolkit.

Your task:
1. Read the toolkit README, AGENTS.md, policies, schemas, prompts, and templates from the toolkit repository.
2. Inspect the current product repository carefully enough to identify its actual technology stack, architecture, build commands, test commands, lint/static-analysis commands, protected files, documentation structure, and current delivery scope. Do not perform an indiscriminate full-tree read when targeted discovery is sufficient.
3. Install or update the project-local toolkit layer using the toolkit bootstrap script when practical. If the script cannot be used, reproduce its generated structure faithfully.
4. Create or update the project-local files:
   - AGENTS.md
   - CLAUDE.md
   - .agent-team/manifest.yaml
   - .agent-team/routing.yaml
   - .agent-team/permissions.yaml
   - .agent-team/commands.yaml
   - .agent-team/observability.yaml
   - .agent-team/metrics/model-usage.csv
   - .agent-team/metrics/README.md
   - .agent-team/toolkit-version
   - .agent-team/tasks/.gitkeep
   - .agent-team/reviews/.gitkeep
5. Keep shared toolkit rules separate from project-specific facts. Project-specific architecture, commands, scope, and restrictions belong in the product repository.
6. Validate every populated command and path against the repository. Mark unknown values explicitly; do not guess.
7. Immediately after initialization, ask the human once whether local model-usage telemetry may be recorded. Persist the answer in `.agent-team/observability.yaml` as `granted` or `denied`, and enable collection only when permission is granted. Do not rely on conversation memory for this permission.
8. Configure the workflow so that:
   - Codex is the engineering director, planner, task router, continuity owner, and final reviewer.
   - Codex may execute tasks itself.
   - Claude Code is invoked only through a scoped task contract with explicit allowed files, forbidden files, acceptance criteria, validation commands, and an attempt limit.
   - Claude Code is optional and never a single point of failure.
   - If Claude refuses, reaches a usage/capacity limit, exits, times out, or produces no usable result, preserve the branch, partial diff, logs, and validation evidence; classify and record the interruption; review all partial Claude changes; and continue the same task as `codex-self` without stopping merely because Claude is unavailable.
   - Claude interruption must not silently reduce the acceptance criteria or validation requirements.
   - Workers never merge to main, push, publish, release, alter signing material, or expose secrets.
   - Every implementation runs on a task branch or isolated worktree.
   - Every worker result is reviewed against the task contract and repository architecture.
   - Human approval is required before merge or push.
9. When usage telemetry is permitted, record only provider/CLI values that are actually available: model, provider, duration, exit code, input/output/cached tokens, reported usage or remaining allowance, retries, diff size, validation result, fallback worker, and quality outcome. Use null/empty values when unavailable and mark estimates explicitly. Never invent percentages, tokens, costs, or model multipliers.
10. Generate an initial architecture/context summary under docs/agent-context/ only when the current repository does not already contain an authoritative equivalent. Prefer links to existing documentation over duplicated truth.
11. Run the toolkit validation script and the repository's non-destructive validation commands that are practical in the environment.
12. Present the resulting diff, unresolved unknowns, validation results, and recommended next task. When Claude was interrupted, report exactly where it stopped, what Codex completed afterward, what work lost independent Claude input, what compensating review/testing was performed, and whether residual quality risks remain. Do not merge or push unless explicitly instructed.

Project-specific intent, if supplied by the user:
[DESCRIBE THE PROJECT, CURRENT MILESTONE, AND IMPORTANT CONSTRAINTS HERE. Leave this section as "not supplied" when absent.]

Operating principles:
- Repository evidence overrides assumptions.
- Documentation and code must remain synchronized.
- Use the smallest sufficient context and least-privilege file scope.
- Do not claim tests passed unless they were actually executed successfully.
- Do not stop a task solely because Claude Code is unavailable.
- Stop after the configured overall attempt limit instead of entering an unbounded repair loop.
- Escalate architectural ambiguity to the human instead of silently inventing policy.

Begin by reporting the repository facts you verified, then perform the initialization in a dedicated branch. After initialization is complete, ask for the telemetry permission and persist the answer before beginning the first implementation task.
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

The scripts intentionally refuse to overwrite existing project files unless `-Force` or `--force` is supplied. Review generated placeholders before committing them.

## Installed project structure

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
    ├── toolkit-version
    ├── metrics/
    │   ├── model-usage.csv
    │   ├── model-usage.jsonl   # created when telemetry is enabled
    │   └── README.md
    ├── tasks/
    └── reviews/
```

## Core workflow

```text
Human request
  -> Codex verifies repository context
  -> Codex creates a task contract
  -> Codex selects codex-self or Claude Code
  -> Claude succeeds: Codex reviews and validates
  -> Claude is interrupted: Codex checkpoints, reviews partial work, and finishes the task
  -> Validation commands run
  -> Codex reports worker history, evidence, and residual risk
  -> Human approves, rejects, or requests another task
```

## Claude interruption detection

The toolkit deliberately does not depend on one exact Claude CLI error string because provider messages and exit behavior may change. The orchestrator combines:

- process exit code;
- timeout state;
- empty or unusable output;
- absence of an expected diff;
- validation failure;
- configurable case-insensitive indicators for quota, usage, rate, credit, capacity, plan, billing, authentication, or refusal errors.

A string match is evidence, not certainty. The interruption record must preserve the classification, phase, exit code, and a short redacted output excerpt when available.

## Usage telemetry

Telemetry is disabled until the human grants permission. The consent decision is persisted in `.agent-team/observability.yaml`, so it does not disappear when Codex context is compacted or a new session starts.

The CSV is intended for simple analysis in Excel or Power BI. JSONL can preserve richer per-run records. Over time, the data can support project-specific routing decisions such as:

- which model solves a task category with the least rework;
- whether a costly frontier model produces a meaningful quality improvement;
- which worker commonly triggers fallback;
- duration and validation success by model;
- token efficiency when providers expose reliable counts.

Historical observations are local evidence, not universal claims. For example, an observed model consuming roughly twice the available usage must be recorded as a project observation with its data source, not hard-coded as a permanent provider fact.

## Safety defaults

- No direct work on the protected branch.
- No autonomous push, merge, release, deployment, or secret access.
- Maximum three implementation attempts per task unless the human changes the policy.
- A clean Git state is required before automated execution.
- Claude unavailability triggers Codex fallback rather than task abandonment.
- Generated work is rejected when required validation was not executed or evidence is missing.
- Usage telemetry remains local and opt-in.

## Versioning

Projects record the installed toolkit version in `.agent-team/toolkit-version`. Shared policy changes follow semantic versioning. Project-local changes remain owned by each product repository and should not be overwritten blindly during updates.

## Scope of v0.2.0

This release standardizes the operating model, Claude-to-Codex fallback, persistent telemetry permission, and local usage reporting templates. It does not yet provide a fully autonomous cross-provider CLI, guaranteed provider-quota extraction, automatic GitHub pull-request management, or a universal normalized cost model. Missing provider usage data must remain explicitly unavailable rather than estimated silently.

## License

MIT. See [LICENSE](LICENSE).

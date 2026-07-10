# Agent Engineering Toolkit

A versioned, vendor-neutral foundation for running a disciplined AI engineering team inside a software repository.

The default workflow assumes that **OpenAI Codex** and **Claude Code** are already installed and authenticated. Codex acts as the engineering director, planner, router, and reviewer. Claude Code is available as a scoped implementation worker when delegation is justified. Codex may also implement tasks itself.

> Status: **v0.1.0 foundation**. Human approval remains mandatory before merging or pushing agent-produced changes.

## What this repository provides

- A reusable `AGENTS.md` policy for the orchestrator and workers.
- A machine-readable project manifest and task-contract format.
- Model-routing, Git, testing, security, and review policies.
- Prompt templates for planning, implementation, and review.
- Bootstrap scripts for installing the toolkit into another repository.
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
   - .agent-team/toolkit-version
   - .agent-team/tasks/.gitkeep
   - .agent-team/reviews/.gitkeep
5. Keep shared toolkit rules separate from project-specific facts. Project-specific architecture, commands, scope, and restrictions belong in the product repository.
6. Validate every populated command and path against the repository. Mark unknown values explicitly; do not guess.
7. Configure the workflow so that:
   - Codex is the engineering director, planner, task router, and final reviewer.
   - Codex may execute low-risk tasks itself.
   - Claude Code is invoked only through a scoped task contract with explicit allowed files, forbidden files, acceptance criteria, validation commands, and an attempt limit.
   - Workers never merge to main, push, publish, release, alter signing material, or expose secrets.
   - Every implementation runs on a task branch or isolated worktree.
   - Every worker result is reviewed against the task contract and repository architecture.
   - Human approval is required before merge or push.
8. Generate an initial architecture/context summary under docs/agent-context/ only when the current repository does not already contain an authoritative equivalent. Prefer links to existing documentation over duplicated truth.
9. Run the toolkit validation script and the repository's non-destructive validation commands that are practical in the environment.
10. Present the resulting diff, unresolved unknowns, validation results, and recommended next task. Do not merge or push unless explicitly instructed.

Project-specific intent, if supplied by the user:
[DESCRIBE THE PROJECT, CURRENT MILESTONE, AND IMPORTANT CONSTRAINTS HERE. Leave this section as "not supplied" when absent.]

Operating principles:
- Repository evidence overrides assumptions.
- Documentation and code must remain synchronized.
- Use the smallest sufficient context and least-privilege file scope.
- Do not claim tests passed unless they were actually executed successfully.
- Stop after the configured attempt limit instead of entering an unbounded repair loop.
- Escalate architectural ambiguity to the human instead of silently inventing policy.

Begin by reporting the repository facts you verified, then perform the initialization in a dedicated branch.
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
    ├── toolkit-version
    ├── tasks/
    └── reviews/
```

## Core workflow

```text
Human request
  -> Codex verifies repository context
  -> Codex creates a task contract
  -> Codex selects codex-self or claude-code
  -> Worker edits only allowed scope
  -> Validation commands run
  -> Codex reviews the diff and evidence
  -> Human approves, rejects, or requests another task
```

## Safety defaults

- No direct work on the protected branch.
- No autonomous push, merge, release, deployment, or secret access.
- Maximum three implementation attempts per task unless the human changes the policy.
- A clean Git state is required before automated execution.
- Generated work is rejected when required validation was not executed or evidence is missing.

## Versioning

Projects record the installed toolkit version in `.agent-team/toolkit-version`. Shared policy changes follow semantic versioning. Project-local changes remain owned by each product repository and should not be overwritten blindly during updates.

## Scope of v0.1.0

This release standardizes the operating model and bootstrap files. It does not yet provide a fully autonomous cross-provider CLI, cost accounting, API-based model routing, or automatic GitHub pull-request management. Those should be built only after the workflow has been validated on real projects.

## License

MIT. See [LICENSE](LICENSE).

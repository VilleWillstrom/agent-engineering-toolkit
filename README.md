# Agent Engineering Toolkit

A versioned, vendor-neutral foundation for running a disciplined AI engineering team inside a software repository.

Codex acts as Engineering Director, integration owner, runtime tester, continuity owner, and final reviewer. Other models and tools are capability-based workers. The primary user interface remains the VS Code Codex chat: the internal `aet` CLI exists for Codex, CI, and diagnostics, not as a mandatory human workflow.

> Status: **v0.5.0 runtime foundation**. AET now includes extensible provider/platform registries, stateless Claude worker sessions, safe cleanup, GitHub PR-check monitoring, and automated tests.

## What this repository provides

- Project-local `AGENTS.md` and `CLAUDE.md` templates.
- Machine-readable task, routing, permission, telemetry, override, provider, platform, session, and GitHub configuration.
- Capability-based agent pools with Codex, Claude Code, Gemini API, and Ollama examples.
- Extensible MCP/API/CLI platform adapters for Supabase, Render, Northflank, Google Cloud, Azure, and future services.
- Claude-to-Codex fallback when Claude becomes unavailable.
- Stateless Claude Code print-mode calls that do not create normal resumable conversation history.
- Safe AET-owned session cleanup and override-gated legacy project purge.
- Codex-owned runtime testing and Claude-focused UI/UX/design work.
- `gh pr checks --watch` integration for CI observation.
- A dependency-free Python runtime with a Python 3.11–3.13 test matrix.

## Fastest way to use it

Open the target product repository in VS Code Codex and paste this prompt:

```text
You are the Engineering Director responsible for initializing and operating the Agent Engineering Toolkit in the currently open product repository.

Assumptions:
- OpenAI Codex is installed and authenticated.
- Claude Code CLI is installed and authenticated when Claude is enabled.
- Optional providers such as Gemini API or local Ollama may be configured by the user.
- GitHub CLI is installed and authenticated when GitHub PR/check workflows are enabled.
- The reusable toolkit source is https://github.com/VilleWillstrom/agent-engineering-toolkit.
- The current repository is the product repository. Do not turn it into a fork of the toolkit.

Your task:
1. Read the toolkit README, AGENTS.md, policies, schemas, prompts, runtime package, and templates.
2. Inspect the product repository using targeted discovery. Verify its stack, architecture, commands, branches, environments, deployment targets, signing approach, remote platforms, and delivery scope. Mark unknowns; do not guess.
3. Install or update the project-local toolkit layer using the bootstrap script when practical.
4. Create or update the normal `.agent-team/` files plus:
   - providers.json
   - platforms.json
   - session-cleanup.json
   - github.json
   - runtime/sessions/
   - platforms/
5. Keep VS Code Codex chat as the primary interface. Use `aet` commands internally when deterministic validation, provider selection, cleanup, or GitHub-check monitoring is useful. Do not require the human to use the CLI manually.
6. Ask once whether local model-usage telemetry may be recorded and persist the answer.
7. Detect every active restriction that conflicts with the requested execution. Before the conflicting action begins, ask exactly:

   Ennen kuin aloitamme suorituksen, tehtävä vaatii annetun rajoituksen "<rajoitus>" overridea, jotta "<perustelu>" olisi mahdollista. Valtuutatko tämän tämän istunnon ajaksi?

8. Request the narrowest sufficient override and record the decision. Session overrides expire at session end and never silently become permanent policy.
9. Route delegation by required capabilities and enabled provider registry entries, not by hard-coded vendor preference. Use project telemetry and observed quality when available.
10. Keep Codex as continuity owner. If any delegated provider fails, reaches usage limits, times out, or returns unusable work, preserve evidence and continue with the next capable provider or Codex itself.
11. Use Claude Code in stateless print mode with `--no-session-persistence` by default. Run AET session cleanup after tasks when configured. Treat `claude project purge` as a separate override-gated cleanup operation.
12. Allow the user to add Gemini API, Ollama, or another model by adding and validating a provider registry entry and adapter configuration. Add tests for new adapter behavior.
13. Allow the user to add Supabase, Render, Northflank, Google Cloud, Azure, or another MCP/API/CLI platform by adding a platform registry entry, environment permissions, validation, rollback guidance, and tests.
14. Codex owns interactive runtime testing by default. Prefer Claude or another capable specialist for bounded UI/UX/design work from supplied evidence.
15. After pushing a task branch, open a draft PR and monitor checks. Use `aet checks --pr <number> --repo <owner/repo> --watch` or equivalent `gh pr checks` behavior. Inspect failing Actions logs, fix the branch, push, and re-watch within the attempt limit.
16. Produce the most complete smoke-testable result possible: artifact, preview URL, APK, installer, staging endpoint, hashes, commit SHA, validation evidence, known risks, and smoke-test instructions.
17. In the final report, list providers used, fallbacks, session cleanup, overrides, external platform changes, PR/check status, and residual risks.

Project-specific intent:
[DESCRIBE THE PROJECT, CURRENT MILESTONE, DESIRED TESTABLE DELIVERABLE, AVAILABLE PROVIDERS/PLATFORMS, AND IMPORTANT CONSTRAINTS HERE.]

Begin by reporting verified repository facts. Perform initialization in a dedicated branch. Ask for telemetry consent after initialization and request required overrides before restricted actions.
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
    ├── providers.json
    ├── platforms.json
    ├── session-cleanup.json
    ├── github.json
    ├── toolkit-version
    ├── metrics/
    ├── overrides/
    ├── runtime/sessions/
    ├── platforms/
    ├── tasks/
    └── reviews/
```

## Runtime commands

These commands are primarily intended for Codex and CI:

```bash
aet doctor --strict
aet providers list
aet providers choose --capability ui_design
aet platforms choose --capability deploy
aet cleanup
aet checks --pr 123 --repo owner/repo --watch
```

## Provider model

Providers advertise capabilities such as `code`, `ui_design`, `review`, `multimodal`, `runtime_testing`, or `local_private`. Disabled providers are never selected. New providers use `builtin`, `command`, `http`, `ollama`, `mcp`, `api`, `cli`, or `custom` adapters.

Claude Code uses stateless print-mode sessions by default, preventing AET worker calls from creating large resumable-history lists. Gemini and Ollama examples are disabled until the user provides configuration.

## Platform model

Remote services use the same registry model. MCP, API, and CLI are transport mechanisms; environment permissions, override requirements, rollback, and audit behavior remain controlled by AET policy.

## Override model

Restrictions are defaults. A session override is narrowly scoped, recorded, expires at session end, does not silently change permanent policy, and cannot create unavailable credentials, quota, tooling, or platform capability.

See `policies/override-protocol.md`.

## Testing

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

GitHub Actions runs the suite on Python 3.11, 3.12, and 3.13 for pull requests and pushes to `main` or `integration`.

## Versioning

Projects record the installed toolkit version in `.agent-team/toolkit-version`. Shared behavior follows semantic versioning. Project-local policy must not be overwritten blindly during toolkit updates.

## License

MIT. See [LICENSE](LICENSE).

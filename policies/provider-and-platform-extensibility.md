# Provider and Platform Extensibility

AET routes work by capabilities, not permanent vendor names.

## Agent providers

Providers live in `.agent-team/providers.json`. A provider declares an adapter type, capabilities, priority, observed cost weight, availability, and session policy. Built-in examples cover Codex, Claude Code, Gemini API, and local Ollama models. New providers are added as registry entries or adapter modules without changing the chat-first workflow.

Codex remains the primary VS Code chat interface. It may delegate through command, HTTP, Ollama, MCP, API, CLI, or custom adapters and must report which provider and model handled each stage.

Provider selection uses the least expensive enabled provider that satisfies required capabilities, adjusted by project telemetry and quality evidence. Static cost weights are initial hints, not universal facts.

## Session lifecycle

Scripted Claude Code calls use print mode with `--no-session-persistence` by default. This prevents AET worker calls from filling Claude Code resume history. Purging legacy project state with `claude project purge` is a separate destructive cleanup action and requires the scoped override protocol.

Other providers must declare whether sessions are stateless, host-managed, remote, or locally persisted. AET-owned session metadata is cleaned automatically according to `.agent-team/session-cleanup.json`.

## Remote platforms

Platforms live in `.agent-team/platforms.json`. Supabase, Render, Northflank, Google Cloud, Azure, and future services use the same capability and environment model. MCP, API, and CLI are adapter mechanisms, not special policy exceptions.

When a user requests a new platform, Codex must:

1. verify the official integration method and authentication requirements;
2. add a disabled registry entry and platform-specific configuration template;
3. add capabilities and environment permissions;
4. add doctor/validation coverage;
5. add unit tests and, when credentials are available, a non-destructive integration smoke test;
6. request required overrides before external changes;
7. document rollback and audit behavior.

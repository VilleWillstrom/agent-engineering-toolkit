# Local model-usage metrics

This directory is populated only when `.agent-team/observability.yaml` records explicit human consent.

- `model-usage.csv` provides a spreadsheet-friendly summary.
- `model-usage.jsonl` may be created by the orchestrator for structured append-only records.

Unavailable provider values must remain empty or `null`. Estimated values must be marked as estimated. Do not commit sensitive prompts, secrets, or raw command output.

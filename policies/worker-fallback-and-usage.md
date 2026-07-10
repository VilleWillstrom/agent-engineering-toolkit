# Worker Fallback and Usage Observability Policy

## Purpose

Claude Code is an optional implementation worker, not a single point of failure. Codex remains responsible for completing the task when Claude becomes unavailable, refuses the request, reaches a usage limit, exits unexpectedly, or returns an unusable result.

## Mandatory fallback behavior

When Claude cannot continue, Codex must:

1. preserve the current branch, task contract, diff, logs, and validation evidence;
2. classify the interruption using the best available evidence;
3. record the last completed phase and any partially modified files;
4. reassess the remaining work and continue the task as `codex-self`;
5. re-read and review any untrusted partial Claude changes before building on them;
6. run the same acceptance criteria and validation commands;
7. complete the task without asking the human merely because Claude became unavailable, unless a separate architectural or safety ambiguity genuinely requires human input;
8. report the fallback and residual quality risk in the final result.

Claude unavailability does not consume the normal implementation retry budget for Codex fallback. Codex must still obey the overall task attempt and safety limits.

## Interruption classification

Do not depend on one exact error string. Claude Code messages and exit behavior may change. Use layered detection:

- `usage_limit`: output indicates quota, rate, credit, token, capacity, plan, billing, or usage exhaustion;
- `authentication`: authentication or authorization failure;
- `tool_refusal`: Claude refuses or cannot execute the scoped request;
- `timeout`: process exceeded the configured timeout;
- `nonzero_exit`: CLI exited unsuccessfully without a more specific classification;
- `invalid_or_empty_result`: no usable response or expected diff was produced;
- `validation_failure`: Claude completed execution but its result failed required checks;
- `unknown`: evidence is insufficient.

The orchestrator may maintain configurable case-insensitive match patterns, but pattern matches are evidence rather than proof. Store the exit code and a short redacted stderr/stdout excerpt when available. Never store secrets or full prompts containing sensitive material.

## Fallback checkpoint

Before Codex continues, it must create a checkpoint containing:

- task ID;
- original and selected worker/model;
- interruption classification;
- timestamp;
- phase where Claude stopped;
- completed acceptance criteria;
- incomplete acceptance criteria;
- files changed by Claude;
- validations already run and their results;
- remaining implementation plan;
- risks introduced by continuing from partial work.

Write this checkpoint under `.agent-team/reviews/` or the task's execution log.

## Final reporting requirement

The final report must state:

- whether Claude was used;
- model name when known;
- whether Claude completed normally;
- where and why it stopped;
- what Codex completed after fallback;
- which work could no longer benefit from independent Claude implementation;
- whether the loss of worker diversity creates potential quality risk;
- what extra review or testing Codex used to compensate;
- any residual uncertainty.

## Usage telemetry

Usage tracking is opt-in for each product repository. Immediately after toolkit initialization, Codex must ask the human once for permission to record local model-usage telemetry. The answer must be persisted in `.agent-team/observability.yaml`; do not rely on conversation memory.

Telemetry must remain local to the product repository unless the human separately authorizes transmission elsewhere.

Collect only values actually exposed by the provider or CLI, such as:

- model/provider;
- start and end timestamps;
- wall-clock duration;
- exit code and interruption classification;
- input/output/cached tokens when available;
- provider-reported usage percentage or remaining allowance when available;
- number of files changed and lines added/deleted;
- validation outcome;
- retry count;
- fallback worker;
- subjective outcome rating recorded by Codex (`accepted`, `accepted_with_rework`, `rejected`);
- estimated data clearly marked as estimated.

Never invent token counts, percentages, cost, or quota consumption. Use `null`/empty values and explain the limitation when the CLI does not expose them.

## Optimization use

Routing decisions may use accumulated telemetry, but quality and task fitness take precedence over raw token minimization. Expensive frontier workers should be selected only when their expected quality advantage justifies the observed usage cost. Historical observations must not be presented as universal provider pricing or guaranteed multipliers.

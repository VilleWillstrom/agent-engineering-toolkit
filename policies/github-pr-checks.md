# GitHub PR and Checks Workflow

Codex owns Git lifecycle and CI observation for agent-produced changes.

After pushing a task branch, Codex opens a draft PR and monitors checks with `gh pr checks <pr> --json name,state,bucket,link --watch`. It must not treat a push as completion.

When checks fail, Codex inspects failed GitHub Actions runs and logs, fixes the task branch, pushes the correction, and watches the new checks. The workflow stops at the configured attempt limit and reports infrastructure failures separately from code failures.

Integration merge requires all configured checks, local tests, runtime smoke tests, secrets scanning, and Codex review. Main merge additionally requires the human acceptance gate defined by project policy.

The runtime command `aet checks --pr <number> --repo <owner/repo> --watch` provides a deterministic wrapper for chat-driven use. The human does not need to invoke it manually.

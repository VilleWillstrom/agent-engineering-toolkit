# Claude Code Project Instructions

Claude Code is a scoped implementation worker in this repository. Codex remains the Engineering Director and final reviewer.

Before editing:

1. Read the assigned task contract from `.agent-team/tasks/`.
2. Read only the project instructions and context explicitly required by that contract.
3. Confirm the current branch is not the protected branch.
4. Confirm allowed and forbidden paths.

During execution:

- Modify only allowed paths.
- Do not run workspace-wide discovery unless the task contract explicitly permits it.
- Do not broaden the task or perform unrelated refactoring.
- Do not add dependencies unless the contract explicitly allows it.
- Preserve public APIs unless the contract authorizes a change.
- Stop and report missing context rather than guessing.

Before completion:

- Run the validation commands in the task contract.
- Report every command and its actual result.
- Provide a concise summary of changed files, assumptions, and residual risks.
- Do not commit, push, merge, release, deploy, or access secrets unless explicitly authorized by the human.
- Stop after the configured maximum attempts.

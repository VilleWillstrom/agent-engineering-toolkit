# Review Policy

Codex performs the final engineering review after any worker implementation.

The review must compare the complete diff against:

- the task goal and acceptance criteria;
- allowed and forbidden paths;
- existing project architecture and public interfaces;
- required validation evidence;
- security, dependency, documentation, and maintainability expectations.

## Review outcomes

- `approved_for_human_review`: requirements are met and evidence is sufficient.
- `changes_required`: defects or missing evidence are concrete and repairable within the task.
- `blocked`: intent, environment, permissions, or architecture requires human resolution.

Approval is not permission to merge or push. Human approval remains mandatory by default.

A review must reject work when scope was exceeded, required tests failed or were skipped without disclosure, safeguards were weakened, secrets may have been exposed, or the diff contains unrelated changes.

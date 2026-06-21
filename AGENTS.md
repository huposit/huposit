# Codex Repository Instructions

ver. 1.0.0_26.06.20

`docs/workflow.md` is the single source of truth for Linear, Codex, GitHub PR, branch, commit, verification reporting, merge, and cleanup rules.

`docs/testflow.md` defines the repository verification command contract, including root commands, app-specific commands, test independence rules, and verification reporting expectations.

Before doing ticket work in this repository, Codex must:

1. Read `docs/workflow.md`.
2. Fetch and read the relevant Linear issue.
3. Confirm the issue has clear `Goal`, `Scope`, and `Done when` sections.
4. Check the current branch and working tree with `git status --short --branch`.
5. Keep changes scoped to the Linear issue.
6. Use `docs/testflow.md` to choose and explain verification commands when the work changes tests, build scripts, lint/typecheck behavior, or verification documentation.
7. Report verification results before asking to commit or push.

For frontend work, Codex must also read `docs/frontend.md` and keep UI, routing, component, token, and API-client decisions aligned with it unless the Linear issue explicitly changes that direction.

For backend work, Codex must also read `docs/backend.md` and keep API, domain model, authentication, job processing, storage, concurrency, and OpenAPI decisions aligned with it unless the Linear issue explicitly changes that direction.

Codex-specific hard rule:

- Do not create commits without explicit user approval.
- Do not push branches or tags without explicit user approval.
- If the user asks only for implementation, stop after verification and report the suggested commit and push commands instead of running them.

If this file and `docs/workflow.md` conflict, follow `docs/workflow.md` unless the conflict is about commit or push approval. Commit and push approval must always be explicit.

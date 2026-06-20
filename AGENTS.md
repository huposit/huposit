# Codex Repository Instructions

ver. 1.0.0_26.06.20

`docs/workflow.md` is the single source of truth for Linear, Codex, GitHub PR, branch, commit, verification, merge, and cleanup rules.

Before doing ticket work in this repository, Codex must:

1. Read `docs/workflow.md`.
2. Fetch and read the relevant Linear issue.
3. Confirm the issue has clear `Goal`, `Scope`, and `Done when` sections.
4. Check the current branch and working tree with `git status --short --branch`.
5. Keep changes scoped to the Linear issue.
6. Report verification results before asking to commit or push.

Codex-specific hard rule:

- Do not create commits without explicit user approval.
- Do not push branches or tags without explicit user approval.
- If the user asks only for implementation, stop after verification and report the suggested commit and push commands instead of running them.

If this file and `docs/workflow.md` conflict, follow `docs/workflow.md` unless the conflict is about commit or push approval. Commit and push approval must always be explicit.

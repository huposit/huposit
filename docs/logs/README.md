# Development Logs

```yaml
as_of: "2026-06-27"
type: "log_index"
repo: "huposit"
timezone: "Asia/Seoul"
canonical_log_root: "docs/logs"
time_source: "Git commit timestamp"
```

Engineering logs are grouped by month, ISO week, and day.

```text
docs/logs/
└── YYYY-MM/
    └── week-WW/
        └── YYYY-MM-DD.md
```

## Format

- Daily filenames contain the commit date in Korean Standard Time.
- Entries are written per commit, not per completed Linear issue.
- Entry times use the Git commit timestamp converted to KST.
- Use `## HH:mm KST` for the time heading.
- Use `### <short-sha> <commit subject>` for each commit entry.
- Keep each entry brief: 1-3 bullets that explain what changed and why it matters.
- Do not wait for a ticket to move to `Done` before logging. If a log is needed, write it from the commits that already exist.
- Older logs may still mention Linear completion timestamps. Do not rewrite old logs only to change their source format.

Example:

```md
## 18:47 KST

### 2c59980 HUP-13 feat: 회원가입 확인 화면 보강

- Connected the signup form to the generated auth API types.
- Added a user card list so newly created accounts can be checked from the web screen.
- Updated backend/frontend direction docs with the current signup boundary.
```

## AI Lookup

- If the date is known, open `docs/logs/YYYY-MM/week-WW/YYYY-MM-DD.md`.
- If only the topic is known, search with `rg -n "keyword" docs/logs`.
- Use these logs as a fast commit-level implementation history. Treat the source code, pull requests, and Linear issues as the final source of truth for exact behavior.

## 2026-06

- [2026-06-27](2026-06/week-26/2026-06-27.md)
- [2026-06-26](2026-06/week-26/2026-06-26.md)
- [2026-06-24](2026-06/week-26/2026-06-24.md)
- [2026-06-21](2026-06/week-25/2026-06-21.md)
- [2026-06-20](2026-06/week-25/2026-06-20.md)
- [2026-06-19](2026-06/week-25/2026-06-19.md)

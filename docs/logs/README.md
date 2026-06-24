# Development Logs

```yaml
as_of: "2026-06-24"
type: "log_index"
repo: "huposit"
timezone: "Asia/Seoul"
canonical_log_root: "docs/logs"
time_source: "Linear issue completedAt"
```

Engineering logs are grouped by month, ISO week, and day.

```text
docs/logs/
└── YYYY-MM/
    └── week-WW/
        └── YYYY-MM-DD.md
```

## Format

- Daily filenames already contain the date, so each entry uses only Korean Standard Time in the body.
- Entry times are based on the Linear issue `completedAt` timestamp, converted to KST and rounded to the nearest hour.
- Work completed in the same hour is grouped under `## HH:00 KST`.
- Each completed issue or work topic is written under a `###` heading.

## AI Lookup

- If the date is known, open `docs/logs/YYYY-MM/week-WW/YYYY-MM-DD.md`.
- If only the topic is known, search with `rg -n "keyword" docs/logs`.
- Use these logs as a fast implementation history. Treat the source code, pull requests, and Linear issues as the final source of truth for exact behavior.

## 2026-06

- [2026-06-24](2026-06/week-26/2026-06-24.md)
- [2026-06-21](2026-06/week-25/2026-06-21.md)
- [2026-06-20](2026-06/week-25/2026-06-20.md)
- [2026-06-19](2026-06/week-25/2026-06-19.md)

## Verdict
CHANGES_REQUESTED

## Findings

- Severity: High
- Title: Async multi-job widget can still show durable-terminal work as active
- AC/Constraint: AC4
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:850-858`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:869-873`
- Evidence:
  - Multi-job async rendering partitions active jobs using raw runtime status only: `const running = jobs.filter((job) => job.status === "running")`.
  - The header uses that raw runtime bucket for active styling: `hasActive = running.length > 0 || queued.length > 0`.
  - Durable status is only applied later to the individual row glyph/status, so a BMAD task whose durable Markdown status is `completed`, `blocked`, or `failed` can still make the widget header show `● Async agents` and be handled as a running job.
  - This violates the story requirement that stale durable terminal task states must not be shown as active even if runtime still reports `running`.
- Recommended fix:
  - Gate async job active bucketing/header state through durable status before computing `running`, `queued`, `finished`, and `hasActive`.
  - Treat jobs whose matched durable status is `completed`, `blocked`, or `failed` as terminal for UI active-state purposes, even when runtime status remains `running`.

- Severity: Medium
- Title: Async terminal title falls back to normal runtime activity when BMAD durable task IDs exist but `taskStatePath` is missing
- AC/Constraint: AC5; R3 follow-up on async terminal title durability
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:289-302`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:981-982`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:273-291`
- Evidence:
  - `durableStatusesForRuntimeTitle()` returns `[]` when `taskStatePath` is absent.
  - `asyncJobCanOwnActivityTitle()` treats an empty status list as title-eligible.
  - `renderWidget()` then calls `ctx.ui.setTitle(buildRuntimeActivityTitle({ job: runningTitleJob }))`.
  - `buildRuntimeActivityTitle()` falls back to a normal runtime title when no `taskStatePath` exists, even if `job.durableTaskIds` is present.
  - The widget degrades for this missing-state case, but the terminal title can still present ordinary active BMAD runtime activity instead of clearing or showing a degraded title.
- Recommended fix:
  - If async runtime has non-empty durable task IDs but no readable `taskStatePath`, do not set a normal active terminal title. Clear it or set an explicit degraded title.
  - Add provider-free regression coverage for an async job with `durableTaskIds` and missing `taskStatePath`.
## Verdict
CHANGES_REQUESTED

## Findings

- Severity: High
- Title: Foreground title arbitration can still fall back to a normal active runtime title for same-agent durable-terminal work
- AC/Constraint: Required Central Runtime/Durable Arbitration; AC3, AC4; R5 foreground terminal-title finding
- Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:318-345`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:416-431`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777-779`
- Evidence:
  - `arbitrateRuntimeUiActivity()` only returns a terminal durable status when all matched durable statuses are terminal. If a foreground runtime item has no `durableTaskId` and matches the same agent with statuses such as `completed` plus `pending`, arbitration returns `canShowActive: false` but no `terminalDurableStatus`.
  - `buildRuntimeActivityTitle()` then falls through to the durable projection/global active fallback and finally to the normal runtime title fallback. I reproduced this provider-free with a task-state artifact containing `implementer` `completed` + `implementer` `pending` and foreground runtime `{ agent: "implementer", status: "running" }`; the helper returned `BMAD Implementer · runtime · runtime active` instead of clearing/degrading the title.
  - `setActivityTitle()` directly applies that helper result via `ctx.ui.setTitle?.(...)`, so the foreground terminal can still show normal active activity for durable-terminal BMAD work when per-progress durable IDs are absent.
- Recommended fix:
  - Make the shared arbitration fail closed for BMAD foreground/runtime items that match durable tasks but have no matched `in-progress` durable task. Do not allow `buildRuntimeActivityTitle()` to fall back to a normal runtime title (or an unrelated global active task) after arbitration says `canShowActive: false` for a readable BMAD task projection.
  - Add provider-free coverage for completed/blocked/failed same-agent matches with no `durableTaskId`, including cases with same-agent pending tasks and unrelated active tasks.

- Severity: High
- Title: Async widget rows can still display durable-terminal jobs as running/thinking
- AC/Constraint: Required Central Runtime/Durable Arbitration; AC4; shared policy must cover async widget rows/header
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:646-663`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:859-866`
- Evidence:
  - `asyncJobEffectiveBucketStatus()` correctly buckets durable-terminal jobs as `finished`, but the finished-row renderer still calls `widgetStats(job)` and `widgetActivity(job)` with the raw runtime job.
  - `widgetStats()` uses raw `job.status === "running"` / `runningSteps` to append `formatAgentRunningLabel(...)`, and `widgetActivity()` uses raw `job.status === "running"` to show cached activity or `thinking…`.
  - Therefore a job whose durable task is `completed`, `blocked`, or `failed` can be moved to the finished bucket and still render row text such as an agent-running count or `thinking…`, which is active UI drift from the central durable-terminal decision.
- Recommended fix:
  - Pass the shared arbitration/effective durable status into widget row stats/activity formatting, or derive stats/activity from an effective non-active status for durable-terminal/degraded BMAD jobs.
  - Add provider-free behavioral coverage for async widget rows/header (single, parallel, and chain where practical) proving durable-terminal runtime `running` jobs do not render active glyphs, running counts, or `thinking…`/live active prompts.

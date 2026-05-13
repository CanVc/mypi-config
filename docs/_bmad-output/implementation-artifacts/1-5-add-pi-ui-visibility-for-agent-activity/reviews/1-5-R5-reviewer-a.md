## Verdict
CHANGES_REQUESTED

## Findings

- Severity: Medium
- Title: Async status output can still show durable-terminal BMAD work as active
- AC/Constraint: AC4, AC5; existing `pi-subagents` status surface integration
- Location: `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:62-66`, `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:130-150`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:221-224`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:242-245`
- Evidence:
  - R4 widget/header/title follow-ups appear addressed in `render.ts`: async bucketing now uses `asyncJobEffectiveBucketStatus(...)`, and title ownership rejects jobs with durable IDs but unreadable task projection.
  - However, `subagent({ action: "status" })` still lists active async runs using raw runtime states only: `listAsyncRuns(..., { states: ["queued", "running"] })`.
  - `listAsyncRuns()` filters on `summary.state` from runtime `status.json` without consulting `taskStatePath` or durable `completed`/`blocked`/`failed` status.
  - Specific run status output prints raw `State: ${status.state}` and raw step `${step.status}` even when the status has `taskStatePath`/`durableTaskId`.
  - This means a stale runtime `running` async job mapped to a durable `completed`, `blocked`, or `failed` task can still appear as active in the status surface.
- Recommended fix:
  - Apply the same durable-status gating used by the async widget to async status/list output.
  - When `taskStatePath` and durable task IDs are present, map terminal durable statuses to non-active status output.
  - When durable IDs are present but the task state is missing/unreadable/malformed, show a degraded warning instead of normal active status.
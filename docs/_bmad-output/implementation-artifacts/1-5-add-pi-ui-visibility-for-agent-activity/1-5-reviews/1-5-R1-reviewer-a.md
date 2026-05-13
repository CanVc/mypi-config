## Verdict
CHANGES_REQUESTED

## Findings

- Severity: High
- Title: Inactive/pending durable tasks do not display configured role labels
- AC/Constraint: AC1
- Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:183`
- Evidence: `enrichTaskProjection` derives `roleLabel` only from a matching runtime item, then falls back to `activeAgentId`/`targetAgent`. With no runtime row for a pending `reviewer-a` task, projection displays `reviewer-a`, not the configured `.pi/agents/reviewer-a.md:4` label `BMAD Reviewer A`.
- Recommended fix: Load/propagate configured agent role labels for all durable task `targetAgent`/`activeAgentId` values, not only runtime-active rows. Add tests for pending/completed/blocked/failed tasks showing BMAD role labels.

- Severity: High
- Title: Parallel same-agent activity titles can resolve to the wrong durable task
- AC/Constraint: AC2, AC3
- Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:207`
- Evidence: `buildRuntimeActivityTitle` selects the first `in-progress` task matching only `runtimeAgentId`; `runtimeAgentId` is just the agent name. With two in-progress `implementer` tasks, a runtime item for the second task still produced `BMAD Implementer · dev-R1 · Implement story`, not the second task title.
- Recommended fix: Carry a durable task identity such as `taskId`/`durableTaskId` through subagent params, progress, async status, and results; match titles by task id before falling back to agent. Add a regression test for two parallel same-agent tasks.

- Severity: Medium
- Title: Missing task-state path silently suppresses degraded BMAD UI
- AC/Constraint: AC5
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`
- Evidence: `bmadTaskProjectionLines` returns `[]` when `taskStatePath` is absent, so no degraded warning is rendered. This bypasses `readDurableTaskProjection`, which would report `BMAD task state artifact path was not provided`.
- Recommended fix: Make BMAD task projection requirement explicit and render the degraded warning when a BMAD/team view is expected but `taskStatePath` is missing. Add coverage for missing `taskStatePath` in rendered UI.
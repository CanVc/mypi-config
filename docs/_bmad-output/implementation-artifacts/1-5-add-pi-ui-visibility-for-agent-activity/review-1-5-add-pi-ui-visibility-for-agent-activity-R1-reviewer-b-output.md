## Verdict
CHANGES_REQUESTED

## Findings
- Severity: Medium
- Title: Parallel same-agent activity titles collapse to the first matching durable task
- AC/Constraint: AC3; Story task requires two parallel same-agent tasks remain distinguishable by task id/title.
- Location: .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:207
- Evidence: `buildRuntimeActivityTitle()` picks a single runtime item, then selects the first durable `in-progress` task whose `activeAgentId`/`targetAgent` matches the runtime agent (`lines 207-216`). There is no task-id/session linkage in the match. A local tsx check with two `in-progress` durable tasks for `implementer` produced the same title for two distinct runtime progress records: `BMAD Implementer · dev-R1 · Implement A` and `BMAD Implementer · dev-R1 · Implement A`.
- Recommended fix: Carry a durable task id (or equivalent task-state linkage) through foreground/background runtime progress and async job steps, and match titles/projections by that id before falling back to agent. Add a regression test where two same-agent in-progress tasks produce distinct terminal titles.

- Severity: Medium
- Title: Malformed durable task records missing required `contextSource` render as valid/completed instead of degraded
- AC/Constraint: AC5; Story 1.4 task-state contract; malformed durable task state must render a degraded warning and must not display success/completion.
- Location: .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:122
- Evidence: The story defines required task record fields as `taskId`, `title`, `targetAgent`, `status`, and `contextSource` (story file lines 129-133), and requires malformed durable task state to degrade (lines 135-142). `parseDurableTaskState()` only validates `taskId`, `title`, `targetAgent`, and status vocabulary (`lines 122-128`). A local tsx check with a `completed` task lacking `contextSource` returned a normal task projection with `durableStatus:"completed"` instead of `degradedReason`.
- Recommended fix: Validate all required Story 1.4 fields, at minimum `contextSource` structure/presence, before projecting tasks. Treat missing required fields as degraded and add a regression test for missing `contextSource` and other required fields.

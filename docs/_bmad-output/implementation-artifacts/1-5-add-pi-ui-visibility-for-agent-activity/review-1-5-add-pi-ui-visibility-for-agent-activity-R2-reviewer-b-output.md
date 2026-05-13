## Verdict
CHANGES_REQUESTED

## Findings

- Severity: High
- Title: Async job-level durable task identity is ignored when building activity titles
- AC/Constraint: AC2, AC3; R1 follow-up durable task identity for parallel same-agent activity titles
- Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`
- Evidence: `buildRuntimeActivityTitle()` only considers `job.steps[*].durableTaskId` or foreground progress/results. It ignores `AsyncJobState.durableTaskIds`, even though async start events populate that field. Reproduced with a job carrying `durableTaskIds: ["dev-R2"]` and a task state containing `dev-R1` and `dev-R2`; the generated title was `BMAD Implementer · dev-R1 · First task`, mapping the job to the wrong same-agent task.
- Recommended fix: Teach activity-title selection to use `AsyncJobState.durableTaskIds` when steps are absent or before status polling has populated per-step records. Match by durable task id before falling back to agent or first in-progress task, and add a regression test for job-level `durableTaskIds`.

- Severity: Medium
- Title: Missing `taskStatePath` degraded UI is suppressed for async BMAD jobs represented only by `durableTaskIds`
- AC/Constraint: AC5; R1 follow-up degraded BMAD UI when `taskStatePath` is missing
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`
- Evidence: `expectsBmadTaskProjection()` checks only singular `durableTaskId` and `roleLabel`. `AsyncStartedEvent`/`AsyncJobState` use plural `durableTaskIds` (`types.ts:272-280`, populated in `async-execution.ts:458-476` and `:610-616`). During the initial async-job state before steps are available, a BMAD job can have durable task ids but no `taskStatePath`, and `bmadTaskProjectionLines()` returns no degraded warning.
- Recommended fix: Update BMAD projection expectation detection to treat non-empty `durableTaskIds` as BMAD/task-projection evidence, and add a regression test for an async job with `durableTaskIds` but missing `taskStatePath` and no steps.
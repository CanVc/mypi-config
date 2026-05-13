## Verdict
CHANGES_REQUESTED

## Findings
- Severity: High
- Title: Foreground subagent runs still do not set terminal activity titles
- AC/Constraint: AC2, AC3; R2 follow-up “foreground single-run terminal titles preserve taskStatePath and durable task identity”
- Location: .pi/npm/node_modules/pi-subagents/src/extension/index.ts:471; .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861; .pi/npm/node_modules/pi-subagents/src/tui/render.ts:948
- Evidence: The foreground renderer only calls `syncResultAnimation(...)` and returns `renderSubagentResult(...)`; it never calls `ctx.ui.setTitle(...)` for foreground progress/results. The single-run update path now preserves `taskStatePath` on update details, but only forwards `onUpdate(updateWithTaskState)`; no title update is performed there either. The only active-work title update found in the implementation is the async widget path (`renderWidget`, lines 948-966). This means foreground single-agent runs can render BMAD task details but the terminal/session title is not updated to the durable `{roleLabel} · {durableTaskId} · {title}` activity title required for distinguishable foreground sessions.
- Recommended fix: Add a foreground title lifecycle hook where foreground `onUpdate`/rendering has `ctx` access: set `ctx.ui.setTitle(buildRuntimeActivityTitle({ details: updateWithTaskState.details }))` while a foreground run has non-terminal running progress, and clear/restore it when the foreground run completes, fails, is interrupted/detached, or the session/reload cleanup runs. Add a regression test that exercises foreground single updates with `taskStatePath` and `durableTaskId` and asserts the title setter receives the durable task title.

- Severity: High
- Title: Async terminal titles can stay active for durable completed/blocked/failed tasks when runtime still reports running
- AC/Constraint: AC2, AC3, AC4; stale-state prevention and terminal-title cleanup
- Location: .pi/npm/node_modules/pi-subagents/src/tui/render.ts:965; .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:278
- Evidence: `renderWidget` chooses `runningJob` solely from runtime status (`job.status === "running" || "queued"`) and always sets the terminal title from `buildRuntimeActivityTitle({ job: runningJob })`. `buildRuntimeActivityTitle` only uses durable state if it can find an `in-progress` durable task; if the job’s `durableTaskIds` point to a durable `completed`, `blocked`, or `failed` task, it falls through to a runtime fallback title instead of returning no active title. A local provider-free check with a durable `completed` task plus a runtime `running` async job returned `unknown-agent · dev-R1 · subagent activity`, demonstrating that stale runtime activity can still drive the terminal title even though widget row glyph/status gating suppresses active styling.
- Recommended fix: Gate async title selection through durable status before calling `setTitle`: if all matched durable task IDs are terminal (`completed`, `blocked`, `failed`), clear/restore the title instead of using the runtime fallback. In `buildRuntimeActivityTitle`, avoid falling back to runtime activity for matched terminal durable tasks. Add regression coverage for running async jobs whose durable task IDs map to completed/blocked/failed statuses, asserting no active terminal title is emitted.

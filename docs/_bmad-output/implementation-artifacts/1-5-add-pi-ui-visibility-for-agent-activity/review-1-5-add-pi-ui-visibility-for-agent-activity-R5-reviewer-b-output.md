## Verdict
CHANGES_REQUESTED

## Findings
- Severity: High
- Title: Foreground terminal title can still show a normal active activity for a durable-terminal task
- AC/Constraint: AC3, AC4 — terminal/session titles must avoid stale active titles; completed/blocked/failed durable tasks must not render as active even when runtime still reports running.
- Location: .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:269; .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777
- Evidence: `setActivityTitle()` always applies `ctx.ui.setTitle?.(buildRuntimeActivityTitle({ details: result.details }))` for foreground updates. In `buildRuntimeActivityTitle()`, if `taskStatePath` is readable but the matched `durableTaskId` is `completed`, `blocked`, or `failed`, no `activeTask` is selected, then execution falls through to the normal runtime fallback at lines 288-291. I reproduced this with a task-state artifact containing `dev-R1` as `completed` plus foreground progress `{ durableTaskId: "dev-R1", status: "running" }`; the function returned `BMAD Implementer · dev-R1 · Runtime still running` instead of clearing/degrading the title. The async path now has an ownership gate, but foreground title updates do not, so durable terminal truth can still be overridden by runtime progress in the terminal title.
- Recommended fix: Gate foreground title ownership through durable status before calling `setTitle`, or make `buildRuntimeActivityTitle()` return no normal runtime title when a readable durable projection contains the matched durable task IDs and all matching tasks are terminal. Add provider-free regression coverage for foreground progress with `taskStatePath` + `durableTaskId` where durable status is `completed`, `blocked`, and `failed`, asserting the title is cleared or explicitly degraded rather than a normal active activity.

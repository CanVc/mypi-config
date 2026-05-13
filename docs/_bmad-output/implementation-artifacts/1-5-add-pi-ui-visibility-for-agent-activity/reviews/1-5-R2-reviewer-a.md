## Verdict
CHANGES_REQUESTED

## Findings

- Severity: High
- Title: Foreground single-run terminal titles lose durable task identity
- AC/Constraint: AC2, AC3; R1 follow-up for durable task identity in activity titles
- Location: `.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts:398`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`
- Evidence: Single-run progress updates emit `details` with `mode`, `results`, `progress`, and `controlEvents`, but no `taskStatePath`. `forwardSingleUpdate` forwards that update unchanged, then `setActivityTitle()` calls `buildRuntimeActivityTitle()`. Without `taskStatePath`, title formatting falls back to task id `"runtime"` even when `durableTaskId` is present. A local check returned `BMAD Implementer · runtime · Implement story` for progress carrying `durableTaskId: "dev-R2"`.
- Recommended fix: Preserve `taskStatePath` on foreground single progress updates before setting terminal titles, and use `durableTaskId` as a fallback task id if durable state is unavailable. Add a regression test for foreground single active-title updates using `taskStatePath` + `durableTaskId`.

- Severity: High
- Title: Stale durable completed/blocked/failed tasks can still render as active in runtime widget rows
- AC/Constraint: AC4; stale-state prevention
- Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:346`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:354`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:651`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:708`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:784`
- Evidence: The BMAD projection uses durable status, but existing widget rows still render `job.status` / `step.status` directly. A task with durable `completed` and runtime `running` will show the BMAD projection as completed, while the same job/step can still get the active spinner/accent and `running` label via `widgetStatusGlyph()`, `widgetStepGlyph()`, `widgetStepStatus()`, and `foregroundStyleWidgetDetails()`.
- Recommended fix: When `taskStatePath` + `durableTaskId` are available, gate all BMAD runtime row glyphs/status labels through durable status so `completed`, `blocked`, and `failed` never display active styling. Runtime `running` may remain only as a secondary/dim annotation. Add renderer coverage for stale runtime `running` against durable terminal statuses.
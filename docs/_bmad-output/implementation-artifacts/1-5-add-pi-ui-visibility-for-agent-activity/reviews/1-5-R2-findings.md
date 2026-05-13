# Story 1.5 R2 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R2-001
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC2, AC3  
Location: `.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts:398`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`  
Sources:
- `reviews/1-5-R2-reviewer-a.md`

#### Problem
Foreground single-run terminal titles lose durable task identity.

#### Required Fix
Preserve `taskStatePath` on foreground single progress updates and use `durableTaskId` as fallback when durable state is unavailable.

#### Validation Requirements
Regression test for foreground single active-title updates using `taskStatePath` plus `durableTaskId`.

#### Out of Scope
No provider/live model calls.

### F-R2-002
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:346`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:354`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:651`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:708`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:784`  
Sources:
- `reviews/1-5-R2-reviewer-a.md`

#### Problem
Stale durable completed/blocked/failed tasks can still render as active in runtime widget rows.

#### Required Fix
Gate BMAD runtime row glyphs/status labels through durable status when `taskStatePath` and durable task identity are available.

#### Validation Requirements
Renderer coverage for stale runtime `running` against durable terminal statuses.

#### Out of Scope
Runtime status may remain secondary/dim only.

### F-R2-003
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC2, AC3  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`  
Sources:
- `reviews/1-5-R2-reviewer-b.md`

#### Problem
Async job-level durable task identity is ignored when building activity titles.

#### Required Fix
Use `AsyncJobState.durableTaskIds` before per-step records exist; match by durable task id before fallback.

#### Validation Requirements
Regression test for job-level `durableTaskIds`.

#### Out of Scope
No change to async dispatch semantics.

### F-R2-004
Status: verified  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`  
Sources:
- `reviews/1-5-R2-reviewer-b.md`

#### Problem
Missing `taskStatePath` degraded UI is suppressed for async BMAD jobs represented only by `durableTaskIds`.

#### Required Fix
Treat non-empty async `durableTaskIds` as BMAD projection evidence and render degraded UI when `taskStatePath` is missing.

#### Validation Requirements
Regression test for async job with `durableTaskIds` but missing `taskStatePath` and no steps.

#### Out of Scope
Do not infer workflow success from async runtime state.

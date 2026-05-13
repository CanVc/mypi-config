# Story 1.5 R6 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R6-001
Status: open  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC3, AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:318-345`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:416-431`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777-779`  
Sources:
- `reviews/1-5-R6-reviewer-a.md`

#### Problem
Foreground title arbitration can still fall back to a normal active runtime title for same-agent durable-terminal work.

#### Required Fix
Make shared arbitration fail closed for BMAD foreground/runtime items that match durable tasks but have no matched `in-progress` durable task; do not fall back to normal runtime or unrelated active tasks after `canShowActive: false`.

#### Validation Requirements
Provider-free coverage for completed/blocked/failed same-agent matches with no `durableTaskId`, including same-agent pending tasks and unrelated active tasks.

#### Out of Scope
Do not introduce new dispatch paths.

### F-R6-002
Status: open  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:646-663`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:859-866`  
Sources:
- `reviews/1-5-R6-reviewer-a.md`

#### Problem
Async widget rows can still display durable-terminal jobs as running/thinking.

#### Required Fix
Pass shared arbitration/effective durable status into widget row stats/activity formatting or derive stats/activity from effective non-active status for durable-terminal/degraded BMAD jobs.

#### Validation Requirements
Provider-free widget row/header coverage proving durable-terminal runtime jobs do not render active glyphs, running counts, or `thinking…`/live prompts.

#### Out of Scope
No raw runtime active state for durable-terminal jobs.

### F-R6-003
Status: open  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC4, AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:265`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:715`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:763`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:965`  
Sources:
- `reviews/1-5-R6-reviewer-b.md`

#### Problem
Renderer/widget paths can bypass degraded central arbitration for durable IDs that do not resolve to durable task state.

#### Required Fix
Make shared status helpers fail closed when durable IDs are present but unmatched; avoid same-agent fallback and render degraded/warning state for unmatched/missing/unreadable/malformed task-state cases.

#### Validation Requirements
Provider-free tests exercising foreground rendering and async widget row/header formatting for unmatched, missing, unreadable, and malformed task-state cases.

#### Out of Scope
Do not scan raw reviewer reports in normal `/dev-story` path.

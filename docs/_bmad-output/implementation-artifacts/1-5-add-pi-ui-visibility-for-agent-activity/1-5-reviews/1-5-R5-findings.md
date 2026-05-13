# Story 1.5 R5 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R5-001
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC3, AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:269`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777`  
Sources:
- `1-5-reviews/1-5-R5-reviewer-b.md`

#### Problem
Foreground terminal title can still show a normal active activity for a durable-terminal task.

#### Required Fix
Gate foreground title ownership through durable status before `setTitle` or make title helper return no normal runtime title for terminal durable matches.

#### Validation Requirements
Regression coverage for foreground progress with completed/blocked/failed durable status.

#### Out of Scope
No runtime progress override of terminal durable truth.

### F-R5-002
Status: verified  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC4, AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:62-66`, `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:130-150`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:221-224`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:242-245`  
Sources:
- `1-5-reviews/1-5-R5-reviewer-a.md`

#### Problem
Async status output can still show durable-terminal BMAD work as active.

#### Required Fix
Apply shared durable-status arbitration to async status/list/detail output and show degraded warnings for missing/unreadable/malformed task state.

#### Validation Requirements
Status-surface coverage for terminal durable statuses and degraded task-state cases.

#### Out of Scope
No live model/provider validation.

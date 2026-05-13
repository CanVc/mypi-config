# Story 1.5 R1 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R1-001
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC1  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:183`  
Sources:
- `reviews/1-5-R1-reviewer-a.md`

#### Problem
Inactive/pending durable tasks do not display configured role labels.

#### Required Fix
Load/propagate configured agent role labels for all durable task `targetAgent`/`activeAgentId` values, not only runtime-active rows.

#### Validation Requirements
Tests for pending/completed/blocked/failed tasks showing BMAD role labels.

#### Out of Scope
No role-specific hardcoding beyond configured metadata.

### F-R1-002
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC2, AC3  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:207`  
Sources:
- `reviews/1-5-R1-reviewer-a.md`
- `reviews/1-5-R1-reviewer-b.md`

#### Problem
Parallel same-agent activity titles can resolve/collapse to the wrong durable task.

#### Required Fix
Carry durable task identity through runtime progress/status/results and match titles by task id before falling back to agent.

#### Validation Requirements
Regression coverage for two parallel same-agent tasks producing distinct titles.

#### Out of Scope
No nested dispatch or new runtime launcher.

### F-R1-003
Status: verified  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`  
Sources:
- `reviews/1-5-R1-reviewer-a.md`

#### Problem
Missing task-state path silently suppresses degraded BMAD UI.

#### Required Fix
Render a degraded warning when BMAD/team view is expected but `taskStatePath` is missing.

#### Validation Requirements
Coverage for missing `taskStatePath` in rendered UI.

#### Out of Scope
Do not treat UI rendering as workflow success.

### F-R1-004
Status: verified  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:122`  
Sources:
- `reviews/1-5-R1-reviewer-b.md`

#### Problem
Malformed durable task records missing required `contextSource` render as valid/completed instead of degraded.

#### Required Fix
Validate Story 1.4 required fields, including `contextSource`, before projecting tasks.

#### Validation Requirements
Regression tests for missing `contextSource` and malformed required fields.

#### Out of Scope
No change to Story 1.4 status vocabulary.

# Story 1.5 R4 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R4-001
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:850-858`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:869-873`  
Sources:
- `reviews/1-5-R4-reviewer-b.md`

#### Problem
Async multi-job widget can still show durable-terminal work as active.

#### Required Fix
Gate async job active bucketing/header state through durable status before computing running/queued/finished.

#### Validation Requirements
Coverage proving durable-terminal runtime jobs do not make widget/header active.

#### Out of Scope
No raw runtime override of durable terminal truth.

### F-R4-002
Status: verified  
Severity: MEDIUM  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC5  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:289-302`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:981-982`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:273-291`  
Sources:
- `reviews/1-5-R4-reviewer-b.md`

#### Problem
Async terminal title falls back to normal runtime activity when BMAD durable task IDs exist but `taskStatePath` is missing.

#### Required Fix
Clear or set explicit degraded terminal title instead of normal active title when durable IDs exist without readable task state.

#### Validation Requirements
Regression coverage for async job with `durableTaskIds` and missing `taskStatePath`.

#### Out of Scope
Do not suppress degraded state.

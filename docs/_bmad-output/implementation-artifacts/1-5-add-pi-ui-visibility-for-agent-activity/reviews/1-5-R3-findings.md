# Story 1.5 R3 Findings

Deduplicated actionable findings migrated from raw review reports and the story action-item registry.

### F-R3-001
Status: verified  
Severity: HIGH  
Classification: artifact-invalid  
Blocking: true  
AC/Constraint: Package durability  
Location: `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch:1`  
Sources:
- `reviews/1-5-R3-reviewer-a.md`

#### Problem
Story 1.5 patch is not clean-install durable because it duplicates an earlier patch.

#### Required Fix
Regenerate/adjust patch relative to prior required patches or patch idempotency logic.

#### Validation Requirements
Clean-install validation proves all patches apply from fresh package.

#### Out of Scope
No uncaptured generated-package edits.

### F-R3-002
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC2, AC3  
Location: `.pi/npm/node_modules/pi-subagents/src/extension/index.ts:471`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:948`  
Sources:
- `reviews/1-5-R3-reviewer-b.md`

#### Problem
Foreground subagent runs still do not set terminal activity titles.

#### Required Fix
Add foreground title lifecycle hook and cleanup on terminal states/session cleanup.

#### Validation Requirements
Regression coverage that foreground single updates set durable task title.

#### Out of Scope
No unsupported Pi UI API.

### F-R3-003
Status: verified  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC2, AC3, AC4  
Location: `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:965`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:278`  
Sources:
- `reviews/1-5-R3-reviewer-b.md`

#### Problem
Async terminal titles can stay active for durable completed/blocked/failed tasks when runtime still reports running.

#### Required Fix
Gate async title selection through durable status and avoid runtime fallback for terminal durable tasks.

#### Validation Requirements
Regression coverage for async jobs mapped to completed/blocked/failed durable statuses.

#### Out of Scope
No stale active terminal titles.

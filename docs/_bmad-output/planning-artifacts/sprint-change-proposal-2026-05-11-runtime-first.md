# Sprint Change Proposal - Runtime-First Epic Reordering

**Project:** mypi-config  
**Date:** 2026-05-11  
**Mode:** Batch / user-approved autonomous update  
**Trigger Source:** User roadmap sequencing correction  
**Prepared by:** BMAD Correct Course Workflow

## 1. Issue Summary

### Problem Statement

The roadmap must put the multi-agent runtime first. The prior Epic 1 bootstrap-first sequence was wrong for the intended delivery strategy because review-capable workflows should not be planned or validated before sub-agent dispatch, fresh-context execution, model routing, and observable task state exist.

### Trigger Context

The user clarified that the intended correction is not a split Epic 1, but a true runtime-first roadmap: multi-agent capability must be Epic 1 immediately.

### Issue Type

- Roadmap sequencing correction
- Epic numbering correction
- Dependency clarification

## 2. Impact Analysis

### Epic Impact

| Epic | Updated Meaning |
| --- | --- |
| Epic 1 | Observable Pi Multi-Agent Runtime |
| Epic 2 | Portable Harness Bootstrap |
| Epic 3 | Standard BMAD Story-to-Done Execution |
| Epics 4-7 | Unchanged |

### Story Impact

| Old Story | New Story |
| --- | --- |
| 2.1 Implement Generic Sub-Agent Dispatch Tool | 1.1 |
| 2.2 Add Agent Definitions and Model Routing Contract | 1.2 |
| 2.3 Enforce Fresh-Context Session Policy | 1.3 |
| 2.4 Add Orchestrator Task Routing and Task List State | 1.4 |
| 2.5 Add Pi UI Visibility for Agent Activity | 1.5 |
| 2.6 Prove Multi-Agent Runtime with Two-Agent Smoke Scenario | 1.6 |
| 1.1 Set Up Initial Project from Project-Local Pi Scaffold Starter | 2.1 |
| 1.2 Add Bootstrap Installation Script | 2.2 |
| 1.3 Add Workstation and Dependency Verification | 2.3 |
| 1.4 Document and Validate Model Configuration | 2.4 |
| 1.5 Add Extension Validation and CI Gate | 2.5 |
| 1.6 Run First Post-Bootstrap Smoke Workflow | 2.6 |

### Artifact Impact

| Artifact | Change |
| --- | --- |
| `epics.md` | Epic 1 and Epic 2 reordered and renumbered; FR coverage updated. |
| `prd.md` | v1 sequencing constraint updated to runtime-first. |
| `architecture.md` | implementation sequence and first implementation priority updated to runtime-first. |
| `sprint-status.yaml` | status keys updated so Epic 1 tracks runtime stories immediately. |

## 3. Recommended Approach

### Selected Approach: Direct Adjustment

Make Observable Pi Multi-Agent Runtime the first implementation epic and move Portable Harness Bootstrap to Epic 2.

### Rationale

The harness should first prove the core execution mechanism that all review-capable workflows depend on: generic sub-agent dispatch, fresh-context session policy, model routing, task state, UI visibility, and two-agent smoke proof. Portable bootstrap then packages and hardens that runtime for target-project installation.

### MVP Impact

MVP scope is unchanged. Only implementation order and story numbering changed.

## 4. Detailed Change Proposals Applied

### `epics.md`

- Epic 1 is now `Observable Pi Multi-Agent Runtime`.
- Epic 2 is now `Portable Harness Bootstrap`.
- FR1-FR4 now map to Epic 2.
- FR9, FR10, FR16-FR19, and FR21-FR25 now map to Epic 1.
- Former runtime stories 2.1-2.6 are now 1.1-1.6.
- Former bootstrap stories 1.1-1.6 are now 2.1-2.6.
- Story 1.1 now integrates the pinned marketplace `pi-subagents` package as the dispatch substrate and explicitly avoids creating a custom `bmad-orchestrator` dispatch extension.

### `prd.md`

Added/updated v1 sequencing constraint:

> The MVP must build the observable multi-agent runtime first. Review-dependent story-to-done validation and portable bootstrap proof come after sub-agent dispatch, fresh-context execution, model routing, and task-state visibility exist.

### `architecture.md`

Updated implementation sequence:

1. Build observable multi-agent runtime first
2. Pin and validate `pi-subagents` as the generic dispatch substrate
3. Define parent-session BMAD orchestration guidance plus artifact/status contracts
4. Add deterministic guardrails only where needed
5. Prove two-agent runtime smoke scenario
6. Package/harden portable bootstrap
7. Proceed to standard BMAD workflow/review gates

### `sprint-status.yaml`

Updated active sequence:

- `epic-1: in-progress`
- `1-1-implement-the-generic-sub-agent-dispatch-tool: ready-for-dev`
- Bootstrap stories moved to Epic 2 keys

## 5. Implementation Handoff

### Scope Classification

**Moderate planning correction** — no code rollback, but story IDs and sprint tracking changed.

### Next Action

Create or update the active story artifact for:

`1-1-implement-the-generic-sub-agent-dispatch-tool`

### Success Criteria

- Work starts with Epic 1 multi-agent runtime.
- Bootstrap packaging work waits until runtime proof exists.
- Standard BMAD review workflows wait until Epic 1 runtime and Epic 2 bootstrap proof are complete.

## 6. Approval

User clarified and approved the runtime-first correction after rejecting the prior split approach.

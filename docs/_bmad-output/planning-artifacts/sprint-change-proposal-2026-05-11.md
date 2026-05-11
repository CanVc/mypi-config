# Sprint Change Proposal - Correct Roadmap Readiness Gaps

**Project:** mypi-config  
**Date:** 2026-05-11  
**Mode:** Batch  
**Trigger Source:** Implementation Readiness Assessment (`implementation-readiness-report-2026-05-11.md`)  
**Prepared by:** BMAD Correct Course Workflow

## 1. Issue Summary

### Problem Statement

The implementation readiness assessment found that the planning artifacts are strong enough to begin v1 implementation, but the full roadmap is not cleanly implementation-ready. Two roadmap planning gaps must be corrected before post-MVP implementation begins:

1. **Epic 4 lacks an explicit end-to-end formal TDD/ATDD/TDAD workflow proof story.**
2. **Epic 5 combines v2 runtime proof scope with v3 auditability/resume scope.**

These gaps do not block v1 work on Epics 1-3, but they create ambiguity for formal TDD workflow acceptance and release sequencing after MVP.

### Trigger Context

No implementation story revealed this issue. The trigger is a planning validation finding from the implementation readiness review.

### Issue Type

- Planning/readiness gap discovered during pre-implementation validation
- Scope sequencing ambiguity between roadmap phases
- Missing proof-of-execution story for a post-MVP epic

### Evidence

From `implementation-readiness-report-2026-05-11.md`:

- Overall readiness status: `NEEDS WORK for full roadmap implementation. READY to start v1/Epic 1-3 implementation with guardrails.`
- Major issue 1: `Epic 4 lacks an explicit end-to-end formal workflow completion/proof story.`
- Major issue 2: `Epic 5 combines v2 runtime proof with v3 auditability/resume concerns.`

## 2. Checklist Analysis Summary

### Section 1: Understand the Trigger and Context

| Item | Status | Notes |
| ---- | ------ | ----- |
| 1.1 Identify triggering story | N/A | No story triggered the issue; readiness assessment triggered it. |
| 1.2 Define core problem | Done | Full-roadmap readiness gaps in Epic 4 and Epic 5. |
| 1.3 Gather evidence | Done | Evidence from implementation readiness report. |

### Section 2: Epic Impact Assessment

| Item | Status | Notes |
| ---- | ------ | ----- |
| 2.1 Current epic evaluation | N/A | No current sprint epic/story is underway. |
| 2.2 Required epic-level changes | Action-needed | Add Epic 4 proof story; split or phase-correct Epic 5. |
| 2.3 Remaining epics review | Done | Epic 6 Advanced Configurator is affected if Epic 5 is split and must be renumbered. |
| 2.4 Future epic validity | Done | No epics are obsolete; one epic split is recommended. |
| 2.5 Epic order/priority | Done | Keep v1 Epics 1-3 unchanged; post-MVP order becomes Epic 4 TDD, Epic 5 Runtime Proof, Epic 6 Auditability/Resume, Epic 7 Configurator. |

### Section 3: Artifact Conflict and Impact Analysis

| Item | Status | Notes |
| ---- | ------ | ----- |
| 3.1 PRD conflicts | Done | No PRD change required; PRD already separates v2 runtime proof, v3 auditability, and v4 configurator. |
| 3.2 Architecture conflicts | Done | No architecture change required; architecture already supports artifact-first logs, traceability, runtime proof, and deferred UI/dashboard decisions. |
| 3.3 UI/UX conflicts | Done | No UX document exists; no UX change required. Story 2.5 remains v1 UX source of truth. |
| 3.4 Other artifacts | Action-needed | `epics.md` requires updates; sprint status is absent, so no sprint status update is needed yet. |

### Section 4: Path Forward Evaluation

| Option | Viability | Effort | Risk | Notes |
| ------ | --------- | ------ | ---- | ----- |
| Option 1: Direct Adjustment | Viable | Low-Medium | Low | Best fit. Update `epics.md` only; no PRD/architecture rewrite needed. |
| Option 2: Potential Rollback | Not viable | N/A | N/A | No implementation work needs rollback. |
| Option 3: PRD MVP Review | Not viable | N/A | N/A | MVP remains achievable; v1 scope is unaffected. |

**Recommended path:** Option 1 — Direct Adjustment.

### Section 5: Proposal Components

| Item | Status | Notes |
| ---- | ------ | ----- |
| 5.1 Issue summary | Done | Included in this proposal. |
| 5.2 Epic/artifact impact | Done | Impacts isolated to `epics.md`. |
| 5.3 Recommended path | Done | Direct adjustment. |
| 5.4 PRD MVP impact | Done | No MVP scope change. |
| 5.5 Agent handoff plan | Done | Moderate backlog artifact correction; update epics before sprint planning. |

## 3. Impact Analysis

### Epic Impact

#### Epic 1: Portable Harness Bootstrap

No change.

#### Epic 2: Observable Pi Multi-Agent Runtime

No change.

#### Epic 3: Standard BMAD Story-to-Done Execution

No change.

#### Epic 4: Formal TDD/ATDD/TDAD Workflow Execution

Change required. Add a final proof story so Epic 4 has a clear end-to-end acceptance point for formal TDD/ATDD/TDAD execution.

#### Epic 5: Runtime Proof, Execution Traceability & Resume

Change required. Split into two epics to preserve release boundaries:

- New Epic 5: Runtime Proof — v2, FR35-FR36
- New Epic 6: Execution Traceability & Resume — v3, FR37-FR39

#### Current Epic 6: Advanced Harness Configurator

Change required only because of renumbering. It becomes Epic 7 and remains v4/horizon scope.

### Story Impact

- Add new `Story 4.8: Prove End-to-End Formal TDD/ATDD/TDAD Story Execution`.
- Keep current Stories 5.1 and 5.2 under new Epic 5 Runtime Proof.
- Move current Stories 5.3, 5.4, and 5.5 under new Epic 6 Execution Traceability & Resume and renumber them to 6.1, 6.2, and 6.3.
- Rename current Epic 6 Advanced Harness Configurator to Epic 7 and renumber Stories 6.1-6.4 to 7.1-7.4.

### Artifact Conflicts

- `prd.md`: No change required.
- `architecture.md`: No change required.
- `epics.md`: Requires updates to FR coverage map, epic list, detailed epic sections, and story numbering.
- UX design: No file exists; no change required.
- Sprint status: No sprint status file was found; no update required yet.

### Technical Impact

No code, infrastructure, or runtime architecture changes are required. This is a planning artifact correction before implementation sequencing.

## 4. Recommended Approach

### Recommendation

Apply a direct adjustment to `docs/_bmad-output/planning-artifacts/epics.md`.

### Rationale

This is the lowest-risk correction because:

- The PRD already separates v2, v3, and v4 roadmap phases.
- The architecture already supports runtime proof, auditability, and resume concepts.
- No existing implementation needs rollback.
- v1 implementation remains unchanged and can proceed after sprint planning.
- Splitting Epic 5 removes release-boundary ambiguity rather than merely annotating it.

### Scope Classification

**Moderate** — backlog/planning reorganization only. No product strategy reset and no architecture rework are required.

### MVP Impact

No MVP impact. Epics 1-3 remain the v1 proof-of-execution path.

## 5. Detailed Change Proposals

### Proposal A — Update FR Coverage Map for Split Epic 5 and Renumbered Configurator Epic

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** `FR Coverage Map`

**OLD:**

```markdown
FR35: Epic 5 - Runtime Proof, Execution Traceability & Resume executes Playwright as part of story completion.

FR36: Epic 5 - Runtime Proof, Execution Traceability & Resume stores screenshots, traces, and logs in `runtime-proof/`.

FR37: Epic 5 - Runtime Proof, Execution Traceability & Resume lets the builder inspect full execution logs.

FR38: Epic 5 - Runtime Proof, Execution Traceability & Resume lets the builder trace phase history and agent routing decisions.

FR39: Epic 5 - Runtime Proof, Execution Traceability & Resume resumes workflow execution from a known phase checkpoint.

FR40: Epic 6 - Advanced Harness Configurator creates new BMAD-derived workflows through a configurator without raw file editing.

FR41: Epic 6 - Advanced Harness Configurator configures Pi harness setup through a configurator interface.
```

**NEW:**

```markdown
FR35: Epic 5 - Runtime Proof executes Playwright as part of story completion.

FR36: Epic 5 - Runtime Proof stores screenshots, traces, and logs in `runtime-proof/`.

FR37: Epic 6 - Execution Traceability & Resume lets the builder inspect full execution logs.

FR38: Epic 6 - Execution Traceability & Resume lets the builder trace phase history and agent routing decisions.

FR39: Epic 6 - Execution Traceability & Resume resumes workflow execution from a known phase checkpoint.

FR40: Epic 7 - Advanced Harness Configurator creates new BMAD-derived workflows through a configurator without raw file editing.

FR41: Epic 7 - Advanced Harness Configurator configures Pi harness setup through a configurator interface.
```

**Rationale:** Aligns FR coverage with PRD roadmap phases: runtime proof is v2, auditability/resume is v3, configurator is v4.

---

### Proposal B — Update Epic List Summary

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** `Epic List`

**OLD:**

```markdown
### Epic 5: Runtime Proof, Execution Traceability & Resume

The builder can produce Playwright runtime proof artifacts, inspect complete execution logs, trace phase and routing decisions, and resume workflow execution from a known checkpoint.

**FRs covered:** FR35, FR36, FR37, FR38, FR39

### Epic 6: Advanced Harness Configurator

The builder can create new BMAD-derived workflows and configure Pi harness setup through a configurator without directly editing raw framework files.

**FRs covered:** FR40, FR41
```

**NEW:**

```markdown
### Epic 5: Runtime Proof

The builder can execute Playwright runtime proof for completed stories and store durable proof artifacts in the story's `runtime-proof/` folder.

**FRs covered:** FR35, FR36

### Epic 6: Execution Traceability & Resume

The builder can inspect complete execution logs, trace phase and agent routing decisions, and resume workflow execution from a known checkpoint.

**FRs covered:** FR37, FR38, FR39

### Epic 7: Advanced Harness Configurator

The builder can create new BMAD-derived workflows and configure Pi harness setup through a configurator without directly editing raw framework files.

**FRs covered:** FR40, FR41
```

**Rationale:** Removes release-boundary ambiguity and makes v2/v3/v4 sequencing explicit.

---

### Proposal C — Add Epic 4 End-to-End Formal Workflow Proof Story

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** End of `Epic 4: Formal TDD/ATDD/TDAD Workflow Execution`, after Story 4.7

**OLD:**

```markdown
**Given** all batches complete
**When** final batch synchronization runs
**Then** the test plan shows all batch statuses complete
**And** the formal workflow can proceed to final gates or runtime proof as configured.

## Epic 5: Runtime Proof, Execution Traceability & Resume
```

**NEW:**

```markdown
**Given** all batches complete
**When** final batch synchronization runs
**Then** the test plan shows all batch statuses complete
**And** the formal workflow can proceed to final gates or runtime proof as configured.

### Story 4.8: Prove End-to-End Formal TDD/ATDD/TDAD Story Execution

As a builder,
I want a complete formal TDD/ATDD/TDAD workflow proof run,
So that I can validate that profile selection, test planning, red/green execution, batch synchronization, and completion handoff work together before relying on the formal workflow for real stories.

**Acceptance Criteria:**

**Given** a valid BMAD story file and a supported formal workflow profile
**When** the builder starts the formal workflow proof run
**Then** the workflow records the selected profile and creates the story artifact folder, test plan, batch artifacts, and orchestrator log
**And** all formal workflow stages use artifact paths as their context sources.

**Given** the test-architect has generated a valid test plan and batch files
**When** the workflow executes each batch
**Then** test writing, red validation, implementation, green validation, and status synchronization run in the documented order
**And** each batch reaches a completed status before the next batch begins unless escalation occurs.

**Given** a red or green validation failure occurs during the proof run
**When** the workflow applies retry policy
**Then** retry counts are updated before dispatch
**And** automatic execution stops with a structured escalation when the configured cap is reached.

**Given** all batches complete successfully
**When** final formal workflow synchronization runs
**Then** the test plan shows all batches complete
**And** the orchestrator log records the final formal workflow outcome, completed stages, selected profile, and artifact locations.

**Given** the formal workflow proof run completes
**When** the builder reviews the generated artifacts
**Then** the run provides durable evidence that the formal TDD/ATDD/TDAD workflow can execute end-to-end
**And** the workflow is considered ready for runtime proof or downstream review gates as configured.

## Epic 5: Runtime Proof
```

**Rationale:** Adds an explicit product-level proof story for Epic 4, matching the proof-of-execution style already used in Epics 1-3.

---

### Proposal D — Split Detailed Epic 5 Section

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** Detailed Epic 5 heading and stories

**OLD:**

```markdown
## Epic 5: Runtime Proof, Execution Traceability & Resume

The builder can produce Playwright runtime proof artifacts, inspect complete execution logs, trace phase and routing decisions, and resume workflow execution from a known checkpoint.

### Story 5.1: Detect Runtime Proof Prerequisites and Prepare Artifact Folder
```

**NEW:**

```markdown
## Epic 5: Runtime Proof

The builder can execute Playwright runtime proof for completed stories and store durable proof artifacts in the story's `runtime-proof/` folder.

### Story 5.1: Detect Runtime Proof Prerequisites and Prepare Artifact Folder
```

**Rationale:** Keeps Stories 5.1 and 5.2 focused on v2 runtime proof.

---

### Proposal E — Move Auditability/Resume Stories into New Epic 6

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** Before current `Story 5.3: Write Full Execution Logs for Workflow Runs`

**OLD:**

```markdown
### Story 5.3: Write Full Execution Logs for Workflow Runs
```

**NEW:**

```markdown
## Epic 6: Execution Traceability & Resume

The builder can inspect complete execution logs, trace phase and agent routing decisions, and resume workflow execution from a known checkpoint.

### Story 6.1: Write Full Execution Logs for Workflow Runs
```

**Additional renumbering in this section:**

```markdown
### Story 5.4: Trace Phase History and Agent Routing Decisions
```

becomes:

```markdown
### Story 6.2: Trace Phase History and Agent Routing Decisions
```

and:

```markdown
### Story 5.5: Resume Workflow from a Known Phase Checkpoint
```

becomes:

```markdown
### Story 6.3: Resume Workflow from a Known Phase Checkpoint
```

**Rationale:** Creates a distinct v3 auditability/resume epic aligned with PRD scope.

---

### Proposal F — Renumber Advanced Harness Configurator to Epic 7

**Artifact:** `docs/_bmad-output/planning-artifacts/epics.md`  
**Section:** Current `Epic 6: Advanced Harness Configurator`

**OLD:**

```markdown
## Epic 6: Advanced Harness Configurator
```

**NEW:**

```markdown
## Epic 7: Advanced Harness Configurator
```

**Additional renumbering in this section:**

```markdown
### Story 6.1: Add Configurator Project and Schema Foundation
### Story 6.2: Generate a BMAD-Derived Workflow from Configuration
### Story 6.3: Configure Pi Harness Agents, Hooks, and Extensions
### Story 6.4: Add Configurator Preview, Validation, and Dry-Run Workflow
```

becomes:

```markdown
### Story 7.1: Add Configurator Project and Schema Foundation
### Story 7.2: Generate a BMAD-Derived Workflow from Configuration
### Story 7.3: Configure Pi Harness Agents, Hooks, and Extensions
### Story 7.4: Add Configurator Preview, Validation, and Dry-Run Workflow
```

**Rationale:** Maintains sequential epic numbering after splitting current Epic 5.

---

### Proposal G — PRD, Architecture, UX

**Artifacts:**

- `docs/_bmad-output/planning-artifacts/prd.md`
- `docs/_bmad-output/planning-artifacts/architecture.md`
- UX design artifact: not present

**Change:** No edits proposed.

**Rationale:** PRD and Architecture already support the corrected roadmap separation. UX absence is acceptable for current scope because v1 UX is Pi TUI/operator visibility and is covered by Story 2.5.

## 6. Implementation Handoff

### Scope Classification

**Moderate** — planning/backlog reorganization.

### Recommended Handoff

Route to Product Owner / Developer planning flow:

1. Apply the approved edits to `epics.md`.
2. Re-run implementation readiness or perform a targeted review of `epics.md` after edits.
3. Proceed to sprint planning for v1 Epics 1-3 if the immediate goal is MVP implementation.

### Responsibilities

- **Product Owner / Planning Agent:** Apply and verify `epics.md` changes.
- **Developer Agent:** No implementation work until corrected planning artifact is approved.
- **Architect:** No architecture action required unless the team decides to materially change runtime proof, logging, or resume design.

### Success Criteria

The correction is successful when:

- Epic 4 includes an end-to-end formal workflow proof story.
- Runtime proof is separated from auditability/resume scope.
- FR35-FR36 map to Runtime Proof.
- FR37-FR39 map to Execution Traceability & Resume.
- Configurator scope is renumbered cleanly after the split.
- PRD and architecture remain aligned with the updated epic structure.

## 7. Recommended Next Steps

1. User reviews and approves this Sprint Change Proposal.
2. Apply the `epics.md` edits from the approved proposal.
3. Optionally run a targeted readiness check or code/document review on the updated `epics.md`.
4. Start sprint planning for v1 Epics 1-3.

## 8. Approval Status

**Status:** Approved and applied.

**Approved by:** Cvc  
**Approval date:** 2026-05-11  
**Applied date:** 2026-05-11

## 9. Final Handoff

### Change Scope Classification

**Moderate** — planning/backlog reorganization.

### Routed To

Product Owner / planning update flow, then Developer story workflow after updated planning artifacts are accepted.

### Handoff Instructions

1. Approved `epics.md` changes from Section 5 have been applied.
2. `docs/_bmad-output/planning-artifacts/epics.md` was the only artifact directly modified.
3. No PRD, Architecture, UX, or sprint status update was required at this time.
4. Proceed to sprint planning for v1 Epics 1-3 unless the roadmap correction should be revalidated first.

### Checklist Closure

- Trigger understood: readiness report gaps.
- Impact analyzed: Epic 4 proof story and Epic 5 scope split.
- Path selected: direct adjustment.
- Proposal generated: complete.
- User approval: received.
- Sprint status update: N/A — no sprint status file exists yet.

# Story 1.2: Prototype — Single-File Agentic TDD Story

<!-- bmad:document story-id="1-2-prototype-agentic-tdd" profile="tdad-lite" mode="strict" state="in-progress" current-batch="batch-03" current-gate="red-gate" -->

Status: in-progress

> **Prototype purpose**: show what a future BMAD/Pi story could look like when used as a **single canonical file** for story context, test planning, batching, validation findings, and orchestration state.
>
> This is **not** a replacement for BMAD base story files. It is a **design prototype** for possible future derived workflows.

---

## Change Log

<!-- bmad:section id="change-log" owner="orchestrator,dev,validators" required="true" -->

- 2026-04-12: Prototype created to explore a single-file story format for agentic TDD / TDAD / ATDD-lite workflows.
- 2026-04-12: Batch 01 completed — core happy path covered and implemented.
- 2026-04-12: Batch 02 completed — first validation/negative case covered.
- 2026-04-12: Batch 03 prepared for red gate.

---

## Story

<!-- bmad:section id="story" owner="story-author" readers="all" required="true" -->

As a user,  
I want to create a valid todo item,  
so that I can track a task in my todo list.

---

## Acceptance Criteria

<!-- bmad:section id="acceptance-criteria" owner="story-author" readers="all" required="true" -->

1. A valid todo entered by the user is added to the visible list.
2. The active item counter is updated after successful creation.
3. The input field is cleared after successful creation.
4. Empty todos are rejected.
5. Existing todo behavior is not regressed.

---

## Tasks / Subtasks

<!-- bmad:section id="tasks-subtasks" owner="story-author,dev" readers="all" required="true" -->

- [x] Task 1: Support creation of a valid todo from the main input (AC: 1)
  - [x] 1.1 Add the minimal domain behavior for valid todo creation
  - [x] 1.2 Ensure the new todo is rendered in the list

- [x] Task 2: Update the active counter after successful creation (AC: 2)
  - [x] 2.1 Recompute active count after insertion

- [ ] Task 3: Clear input after successful creation (AC: 3)
  - [ ] 3.1 Clear the input field after successful submit

- [ ] Task 4: Reject empty todo input (AC: 4)
  - [ ] 4.1 Prevent empty item creation
  - [ ] 4.2 Preserve current list state on invalid submit

- [ ] Task 5: Validate regressions and runtime behavior (AC: 5)
  - [ ] 5.1 Run targeted regression tests
  - [ ] 5.2 Run runtime/browser validation if required by profile

---

## Story Profile

<!-- bmad:section id="story-profile" owner="story-author,orchestrator" readers="all" required="true" -->

- **Profile**: `tdad-lite`
- **Mode**: `strict`
- **Why this profile**:
  - user-visible behavior,
  - small but non-trivial regression risk,
  - multiple acceptance criteria that benefit from ordered test batches,
  - desire to explicitly control test targeting before broader validation.

---

## Examples

<!-- bmad:section id="examples" owner="test-planner" readers="test-planner,test-writer,red-validator,dev,green-validator" required="true" -->

### Example 1 — Add valid todo
Given the todo list is empty  
When the user enters `Buy milk` and presses Enter  
Then the todo `Buy milk` appears in the list  
And the active counter shows `1 item left`  
And the input field is cleared

### Example 2 — Reject empty todo
Given the todo list is empty  
When the user presses Enter with an empty input  
Then no todo is created  
And the active counter is unchanged

### Example 3 — Regression guard
Given one existing todo is already present  
When the user adds a second valid todo  
Then both todos remain visible  
And existing rendering behavior is preserved

---

## Test Plan

<!-- bmad:section id="test-plan" owner="test-planner" readers="test-planner,test-writer,red-validator,dev,green-validator,orchestrator" required="true" -->

> Principle: **global plan, incremental execution**.  
> The full test strategy is defined here, but tests are authored and implemented in **small batches**.

### Planned batches

- [x] **Batch 01** — Core happy path: valid todo appears in list
- [x] **Batch 02** — Counter updates after valid creation
- [ ] **Batch 03** — Input field clears after successful creation
- [ ] **Batch 04** — Empty todo rejected
- [ ] **Batch 05** — Targeted regression validation
- [ ] **Batch 06** — Runtime validation / E2E proof if still required

### Strategy notes

- Start with the **smallest central behavior**.
- Prefer deterministic unit/integration coverage before browser/runtime proof.
- Avoid large “kitchen sink” tests early.
- Add regression checks only after core batches are green.

### Stop conditions for story closure

The story can move to final review only when:
- all ACs are covered by completed batches,
- no blocking finding remains open,
- targeted regression checks pass,
- runtime proof is either completed or explicitly marked unnecessary for this story.

---

## Batch Board

<!-- bmad:section id="batch-board" owner="orchestrator" readers="all" required="true" -->

> Display only completed batches, current batch, and next actionable batch to limit file growth.

| Batch | Goal | State | Gate | Owner | Notes |
|---|---|---|---|---|---|
| batch-01 | Core happy path | done | green-gate passed | dev + green-validator | Todo appears in list |
| batch-02 | Counter update | done | green-gate passed | dev + green-validator | Counter updated correctly |
| batch-03 | Clear input after success | in-progress | red-gate | test-writer → red-validator | Current batch |
| batch-04 | Reject empty todo | ready | planning | test-planner | Next batch |

---

## Current Batch

<!-- bmad:batch id="batch-03" state="in-progress" phase="red" owner="test-writer" next-role="red-validator" -->
<!-- bmad:section id="current-batch" owner="test-writer,orchestrator" readers="test-writer,red-validator,dev,green-validator,orchestrator" required="true" -->

### Batch Goal

Validate that the input field is cleared after successful creation of a valid todo.

### Batch Scope

- Covers AC: 3
- Must not widen into empty-input rejection yet
- Must reuse existing happy-path setup from earlier batches where possible

### Target tests for this batch

- [ ] Add/update focused UI/component test verifying input reset after successful submit
- [ ] If needed, add supporting integration test only if the UI-level test is too indirect

### Expected red state

- Test compiles and runs
- Test fails because the input retains its previous value after submit
- Failure is behavior-related, not caused by unrelated setup or selector instability

### Dev handoff constraints

- Implement only what is required to clear the input after successful creation
- Do not fold in empty-input validation in this batch
- Do not rewrite previously accepted tests unless the red-validator explicitly flags them

### Validation commands

```bash
pnpm vitest src/todo/todo-input.test.ts
pnpm vitest src/todo/todo-list.test.ts
```

---

## Validation Findings

<!-- bmad:section id="validation-findings" owner="red-validator,green-validator" readers="validators,orchestrator,dev,test-planner,test-writer" required="true" -->

### Open Findings

<!-- bmad:finding id="RV-001" source="red-validator" severity="medium" type="test" status="open" -->
- The current batch must confirm that the red failure is caused by the input not being cleared, not by stale rendering setup.

### Resolved Findings

<!-- bmad:finding id="GV-001" source="green-validator" severity="low" type="implementation" status="resolved" -->
- Batch 02 was accepted after confirming the counter update was tied to successful insertion, not hardcoded state.

---

## Orchestrator Decision Log

<!-- bmad:section id="orchestrator-decision-log" owner="orchestrator" readers="all" required="true" -->

<!-- bmad:decision cycle="01" source="orchestrator" outcome="advance:next-batch" reason="batch-01-green-gate-passed" -->
- Cycle 01: Batch 01 accepted. Advance to Batch 02.

<!-- bmad:decision cycle="02" source="orchestrator" outcome="advance:next-batch" reason="batch-02-green-gate-passed" -->
- Cycle 02: Batch 02 accepted. Advance to Batch 03.

<!-- bmad:decision cycle="03" source="orchestrator" outcome="reroute:red-validator" reason="batch-03-red-ready" -->
- Cycle 03: Batch 03 prepared by test-writer. Send to red-validator before dev handoff.

---

## Dev Notes

<!-- bmad:section id="dev-notes" owner="story-author,test-planner" readers="dev,validators" required="true" -->

### Relevant architecture / implementation notes

- Reuse the existing todo insertion flow rather than introducing a second submit path.
- Prefer behavior assertions over implementation-detail assertions.
- Keep the state update local to the current feature boundary.

### Testing guidance

- Keep tests deterministic.
- Prefer small tests over broad scenario tests for core batches.
- Runtime/E2E validation is deferred until later in the plan.

### Risks / watchouts

- Overfitting the implementation to a single UI test.
- Accidentally mixing successful-submit clearing with invalid-submit handling.
- Regressing the existing counter behavior while touching submit logic.

### References

- [Source: story prototype only — illustrative structure]

---

## Batch History

<!-- bmad:section id="batch-history" owner="orchestrator,validators" readers="all" required="false" -->

### batch-01
- Goal: valid todo appears in the list
- Outcome: accepted
- Notes: minimal creation path implemented

### batch-02
- Goal: active counter updates
- Outcome: accepted
- Notes: no regression observed in list rendering

> Older batch details should be summarized here instead of duplicated in full to control file growth.

---

## Dev Agent Record

<!-- bmad:section id="dev-agent-record" owner="dev" readers="all" required="true" -->

### Agent Model Used

_To be filled by implementation workflow._

### Debug Log References

_To be filled incrementally._

### Completion Notes List

- Batch 01 completed with minimal insertion behavior.
- Batch 02 completed with active counter update.

### File List

- `src/todo/todo-list.tsx`
- `src/todo/todo-input.tsx`
- `src/todo/todo-input.test.ts`
- `src/todo/todo-list.test.ts`

---

## Final Review Readiness

<!-- bmad:section id="final-review-readiness" owner="orchestrator,green-validator" readers="all" required="false" -->

- [ ] All planned batches required for the story are done
- [ ] No blocking finding remains open
- [ ] Targeted regression validation passed
- [ ] Runtime validation completed or explicitly waived
- [ ] Story ready for final code review

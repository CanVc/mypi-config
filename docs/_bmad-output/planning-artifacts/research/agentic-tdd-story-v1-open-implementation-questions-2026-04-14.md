# Agentic TDD Story Workflow — V1 Open Implementation Questions

**Date:** 2026-04-14  
**Status:** Open questions captured after collaborative review  
**Purpose:** Record the main implementation gaps identified after the V1 decision set was frozen on 2026-04-13, without rewriting the baseline documents.

---

## 1. Scope of this document

This file is **not** a replacement for the V1 baseline documents:
- `agentic-tdd-story-workflow-decisions-2026-04-13.md`
- `agentic-tdd-story-example-workflow-2026-04-13.md`
- `agentic-tdd-story-artifact-spec-2026-04-13.md`

It exists to capture **implementation questions still needing explicit rules** before workflow automation begins.

---

## 2. Open question — Story profile selection rules

### Current gap
The V1 documents assume story profiles such as:
- `tdd-lite`
- `tdad-lite`
- `atdd-lite`

However, the selection logic is not yet operationalized.

### Why this matters
Without explicit rules, profile choice remains subjective and may vary from one agent or session to another.

### Questions to resolve
- What are the **3–5 binary criteria** used to choose a profile?
- Which criteria override others?
- Can a story start in one profile and be escalated to another?
- Who is allowed to choose or override the profile?

### Expected output
A short decision table such as:
- user-visible ambiguity,
- regression blast radius,
- number of touched layers/files,
- runtime proof requirement,
- need for acceptance examples before coding.

---

## 3. Open question — `blocked` policy

### Current gap
V1 defines `blocked` as a valid batch status, but does not yet define the handling policy.

### Why this matters
Without a bounded policy, blocked batches may loop indefinitely or be resolved inconsistently.

### Questions to resolve
- What is the **retry cap** per blocked situation?
- When must the workflow **escalate to a human**?
- Is `skipped` allowed, and under which conditions?
- Can a blocked batch be re-scoped into a smaller batch in V1, or must that wait for later workflow versions?
- Which role is allowed to mark or clear `blocked`?

### Expected output
A small state/decision rule set such as:
- blocked reason category,
- max retries,
- next allowed actions,
- escalation threshold,
- final resolution path.

---

## 4. Open question — Batch test pyramid heuristics

### Current gap
V1 defines batches and runtime proof, but does not yet provide a practical heuristic for choosing the test level per batch.

### Why this matters
The test-architect needs guidance on whether a batch should primarily use:
- unit tests,
- integration/component tests,
- runtime/E2E validation.

### Questions to resolve
- What should be the default test level for a small behavior batch?
- When is a runtime or browser proof mandatory?
- When is an integration test preferable to a unit test?
- How much overlap between targeted tests and later runtime proof is acceptable?

### Expected output
A lightweight heuristic such as:
- prefer the lowest-level deterministic test that proves the batch behavior,
- defer runtime proof unless the AC is meaningfully UI/runtime-visible,
- use integration tests when behavior crosses component or module boundaries,
- reserve E2E/runtime proof for user-visible closure or uncertainty reduction.

---

## 5. Open question — Automation prerequisites

### Current gap
The V1 design describes artifact flow and roles, but does not yet define the minimum automation prerequisites for smooth execution.

### Why this matters
The workflow may be conceptually sound but still feel fragile or manual without immediate verification feedback.

### Questions to resolve
- Which hooks or post-edit automation should run after test or code changes?
- What is the minimum proof required for:
  - red validation,
  - green validation,
  - runtime verification?
- Which files should contain evidence versus summaries?
- What is the minimal infrastructure needed before implementation starts?

### Expected output
A short checklist covering:
- post-edit test feedback,
- command logging conventions,
- runtime-proof storage conventions,
- minimal orchestrator sync behavior,
- evidence required at each gate.

---

## 6. Suggested next decision package

Before implementation, produce a compact follow-up decision note that freezes:
1. **profile selection rules**,
2. **blocked policy**,
3. **batch test pyramid heuristics**,
4. **automation prerequisites and evidence rules**.

This should remain small and operational, not a new large research document.

---

## 7. Summary

The V1 workflow design is coherent, but these items still need explicit rules:
- how to choose the story profile,
- how to handle blocked batches,
- how to choose the right test level per batch,
- what automation and evidence are required to make the workflow practical.

These are implementation questions, not reasons to reopen the V1 baseline.

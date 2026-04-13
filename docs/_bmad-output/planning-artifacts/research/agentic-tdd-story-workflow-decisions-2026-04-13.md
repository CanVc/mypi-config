# Agentic TDD Story Workflow — Decisions

**Date:** 2026-04-13  
**Status:** Design decisions frozen for V1 exploration

---

## 1. Scope and guiding principles

This workflow is for **story-by-story execution** with explicit human validation between stories.

Primary goals:
- improve quality,
- preserve BMAD compatibility,
- avoid over-engineering,
- keep the workflow auditable in Git.

Core principle:

> Do not modify BMAD base workflows. Create new derived workflows around them.

---

## 2. BMAD base workflows

The following base workflows remain unchanged:
- `bmad-create-story`
- `bmad-dev-story`
- `bmad-code-review`

Rationale:
- preserve standard BMAD usage,
- keep a non-TDD path available,
- reduce implementation risk,
- enable comparison with derived workflows.

---

## 3. Story artifact strategy

### 3.1 Story file

Each story keeps a **BMAD-classic story file** as the main human-readable contract.

The story file stays focused on:
- story statement,
- acceptance criteria,
- tasks/subtasks,
- dev notes,
- dev agent record,
- file list,
- status.

### 3.2 Changelog

Detailed changelog content is **moved out of the story file**.

The story file should only contain a pointer to the dedicated changelog file.

Rationale:
- story files already become large,
- changelog noise makes them harder to use operationally,
- changelog details are better tracked separately.

---

## 4. Story folder layout

A story should live in its own folder.

All files are prefixed by the story number for Git readability.

Example for story `1-2`:

```text
1-2/
  1-2-story.md
  1-2-story-changelog.md
  1-2-test-plan.md
  1-2-orchestrator-log.md
  1-2-batches/
    1-2-batch-01.md
    1-2-batch-02.md
  1-2-runtime-proof/
```

---

## 5. Test planning and batching

### 5.1 Test plan

`1-2-test-plan.md` is the reference document for:
- story test strategy,
- batch list,
- batch priority,
- batch statuses,
- overall completion criteria.

### 5.2 Batching

The workflow uses explicit **batches**.

A batch is the operational unit for incremental work.

### 5.3 Rebatching

**Rebatching is out of scope for V1.**

Rationale:
- stories are already BMAD-structured,
- V1 should stay simple,
- if batching quality is poor, the fix belongs in the `test-architect` workflow, not in a re-batching subsystem.

---

## 6. Role ownership

### 6.1 Test Architect

The `test-architect` is responsible for:
- creating the initial `test-plan`,
- proposing the batching,
- creating the initial batch files.

Reason:
- this role is best positioned to define coverage structure and batch sequencing.

### 6.2 Orchestrator

The orchestrator is responsible for:
- driving workflow phase transitions,
- tracking current phase and batch,
- updating statuses,
- writing orchestration decisions to `orchestrator-log`.

The orchestrator should remain **strict and lightweight**.
It should not deeply reinterpret story content.

### 6.3 Test Writer / Dev / Validators

Specialized agents enrich batch files during execution:
- test writer,
- red validator,
- dev,
- green validator.

---

## 7. Validators

### 7.1 Two validator roles

V1 design assumes two distinct validation roles:
- **red-validator**
- **green-validator**

Reason:
- they validate different things,
- they likely need different prompts,
- they may later benefit from different models.

### 7.2 Prompt strategy

Use distinct prompts for:
- red validation,
- green validation.

### 7.3 Model strategy

V1 should start with:
- different roles,
- different prompts,
- but not necessarily different models.

Model specialization can come later if measurements justify it.

### 7.4 Lean vs strict mode

A lighter workflow variant without red-validator should be considered for low-risk stories if the test side proves reliable in practice.

---

## 8. Context strategy

The preferred strategy is:

> ultra-clean canonical story artifacts + lightweight orchestration guidance

This means:
- agents read canonical files directly,
- orchestrator does not reconstruct large semantic prompts,
- orchestrator can still indicate the current global position (example: `story-001 / batch-03 / red-gate`).

Reason:
- reduces interpretation risk,
- preserves source-of-truth integrity,
- keeps debugging simpler.

---

## 9. Metadata / tags

Machine-friendly tags are acceptable, but they must use a **strict, explicit, unambiguous codification**.

No vague group names should be used.

Example of a bad value:
- `validators`

Preferred rule:
- every role is listed explicitly,
- every status value is from a closed set.

Detailed codification remains to be specified separately.

---

## 10. Batch status naming

Use `status`, not `state`, for consistency with BMAD conventions.

This applies to:
- story status,
- batch status,
- summary views.

Recommended closed values for batches:
- `planned`
- `ready`
- `in-progress`
- `review`
- `done`
- `blocked`
- optional: `skipped`

---

## 11. Git workflow

### 11.1 Commit policy

**One Git commit per phase** is required.

Rationale:
- clear checkpoints,
- easier rollback,
- strong traceability,
- easier workflow debugging.

### 11.2 Story branches

**No branch-per-story by default in V1.**

Recommended V1 mode:
- sequential story execution,
- one main working branch,
- one commit per phase.

A branch-per-story model may be introduced later only if a real isolation need appears.

---

## 12. V1 simplification rules

The following simplifications are intentionally kept:
- no rebatching,
- no aggressive orchestrator interpretation,
- no branch-per-story by default,
- no modification of BMAD base workflows,
- no unnecessary artifact explosion inside the main story file.

---

## 13. Summary

V1 should be:
- story-folder based,
- BMAD-compatible at the story file level,
- batch-driven,
- orchestrated with low interpretation,
- Git-traceable phase by phase,
- simple enough to run manually before automation.

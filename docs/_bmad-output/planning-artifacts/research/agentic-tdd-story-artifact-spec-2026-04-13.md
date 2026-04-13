# Agentic TDD Story Workflow — Artifact Specification

**Date:** 2026-04-13  
**Status:** V1 artifact specification

---

## 1. Story folder structure

For story `1-2`, the target structure is:

```text
1-2/
  1-2-story.md
  1-2-story-changelog.md
  1-2-test-plan.md
  1-2-orchestrator-log.md
  1-2-batches/
    1-2-batch-01.md
    1-2-batch-02.md
    ...
  1-2-runtime-proof/
```

---

## 2. File purposes

### 2.1 `1-2-story.md`
Primary BMAD-compatible story file.

Purpose:
- canonical story contract,
- acceptance criteria,
- tasks/subtasks,
- dev notes,
- dev agent record,
- file list,
- story status.

Should remain compact and operational.

### 2.2 `1-2-story-changelog.md`
Detailed story execution history.

Purpose:
- phase history,
- major decisions,
- long-form review history,
- detailed chronology not suitable for the main story file.

### 2.3 `1-2-test-plan.md`
Global test and batching reference.

Purpose:
- testing strategy,
- story profile,
- batch list,
- batch priorities,
- batch status summary,
- completion criteria.

### 2.4 `1-2-orchestrator-log.md`
Workflow routing journal.

Purpose:
- phase routing history,
- selected agent by step,
- orchestration decisions,
- escalation events,
- sync checkpoints.

### 2.5 `1-2-batches/1-2-batch-XX.md`
Operational work record for one batch.

Purpose:
- batch scope,
- test writing details,
- red validation findings,
- dev implementation notes,
- green validation findings,
- batch outcome.

### 2.6 `1-2-runtime-proof/`
Heavy runtime artifacts.

Purpose:
- screenshots,
- traces,
- logs,
- videos,
- exported runtime evidence.

---

## 3. Ownership by file

### `1-2-story.md`
Created by:
- story creation workflow

Updated by:
- standard/derived dev workflow
- standard/derived code review workflow
- human reviewer if needed

### `1-2-story-changelog.md`
Created by:
- story creation workflow or orchestrator bootstrap

Updated by:
- orchestrator
- review workflows
- possibly dev workflow if phase summaries are appended there

### `1-2-test-plan.md`
Created by:
- **test-architect**

Updated by:
- **test-architect** for plan content
- **orchestrator** for batch status synchronization only

### `1-2-orchestrator-log.md`
Created and updated by:
- **orchestrator** only

### `1-2-batch-XX.md`
Created by:
- **test-architect**

Updated by:
- test-writer
- red-validator
- dev
- green-validator
- orchestrator (status synchronization and routing markers only)

---

## 4. Required content per file

### 4.1 `1-2-story.md`
Should keep the BMAD-style sections:
- `Status`
- `## Story`
- `## Acceptance Criteria`
- `## Tasks / Subtasks`
- `## Dev Notes`
- `## Dev Agent Record`
- `### File List`
- `## Change Log` (short pointer only)

Recommended addition:
- `## Story Artifacts`

Example:

```md
## Story Artifacts
- Changelog: `1-2-story-changelog.md`
- Test plan: `1-2-test-plan.md`
- Orchestrator log: `1-2-orchestrator-log.md`
- Batches: `1-2-batches/`
- Runtime proof: `1-2-runtime-proof/`
```

### 4.2 `1-2-story-changelog.md`
Recommended sections:
- `## Story`
- `## Execution History`
- `## Review History`
- `## Key Decisions`

### 4.3 `1-2-test-plan.md`
Recommended sections:
- `Status`
- `## Story Profile`
- `## Test Strategy`
- `## Batch Plan`
- `## Batch Status Summary`
- `## Completion Criteria`

### 4.4 `1-2-orchestrator-log.md`
Recommended sections:
- `Status`
- `## Current Position`
- `## Routing Log`
- `## Escalations`

### 4.5 `1-2-batch-XX.md`
Recommended sections:
- `Status`
- `## Batch Goal`
- `## Scope`
- `## Test Authoring`
- `## Red Validator Findings`
- `## Dev Implementation`
- `## Green Validator Findings`
- `## Outcome`

---

## 5. Batch status synchronization model

### Canonical detailed record
Each batch file contains its own:
- `Status: ...`

### Summary view
`1-2-test-plan.md` contains a summarized batch status table or checklist.

### Sync rule
Only the **orchestrator** should synchronize:
- the batch file status,
- the matching batch status in `1-2-test-plan.md`.

This avoids inconsistent updates from multiple agents.

---

## 6. Batch file lifecycle

### Created by
- test-architect, during initial planning

### Then enriched by
- test-writer
- red-validator
- dev
- green-validator

### Then status-managed by
- orchestrator

---

## 7. Recommended batch status values

Closed set:
- `planned`
- `ready`
- `in-progress`
- `review`
- `done`
- `blocked`
- optional: `skipped`

---

## 8. Commit guidance

Recommended Git checkpoint cadence:
- after test-plan creation,
- after batch authoring phase,
- after red validation,
- after green implementation,
- after green validation,
- after final review actions.

One commit per phase is the V1 rule.

---

## 9. Deliberate V1 exclusions

Not included in V1:
- rebatching workflow,
- branch-per-story as default,
- complex orchestration-generated semantic prompts,
- storing verbose runtime artifacts inside the main story file.

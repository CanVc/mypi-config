# Dev Story / Code Review / Dev Cycle Artifact Structure Decision

**Date:** 2026-05-13 22:30  
**Status:** Decision note  
**Supersedes / refines:** `dev-story-dev-cycle-artifact-structure-proposal-2026-05-13.md`  
**Scope:** Active non-TDD story execution taxonomy for `/dev-story`, `/code-review`, and `/dev-cycle`. Future TDD/test-plan/batch artifacts remain compatible but are out of active scope here.

---

## 1. Decision summary

Story execution artifacts should follow the existing Agentic TDD story artifact specification **minus TDD-specific files for now**, with one deliberate folder-name refinement:

- the story folder uses the full story slug for readability;
- files inside the folder use the short story id prefix from the original specification.

Example:

```text
docs/_bmad-output/implementation-artifacts/1-2-un-exemple-de-story/
  1-2-story.md
  1-2-story-changelog.md
  1-2-orchestrator-log.md
  1-2-cycle-state.md
  1-2-runtime-proof/

  reviews/
    1-2-R1-reviewer-a.md
    1-2-R1-reviewer-b.md
    1-2-R1-findings.md
    1-2-R2-reviewer-a.md
    1-2-R2-reviewer-b.md
    1-2-R2-findings.md

  remediation/
    1-2-R3-remediation-brief.md

  validation/
    1-2-validation-summary.md
    command-output-*.log
```

Future TDD additions should use the original spec-compatible names:

```text
  1-2-test-plan.md
  1-2-batches/
    1-2-batch-01.md
    1-2-batch-02.md
```

Definitions:

```text
story_id     = 1-2
story_slug   = 1-2-un-exemple-de-story
story_folder = docs/_bmad-output/implementation-artifacts/<story_slug>/
```

---

## 2. Why this decision exists

Story 1.5 exposed that current story files can become overloaded with:

- canonical story contract;
- orchestration task state;
- repeated review outputs;
- duplicated findings across review rounds;
- long validation evidence;
- remediation state;
- completion notes and historical logs.

This causes context bloat, makes fresh-context handoffs expensive, and makes story execution harder to reason about.

The corrected model is:

> The story file remains the compact canonical contract and current action surface. Heavy execution evidence, raw reviews, triaged findings, routing state, and logs live beside it in story-scoped artifacts.

---

## 3. Relationship to existing specifications

This decision aligns with:

- `agentic-tdd-story-artifact-spec-2026-04-13.md`
- `agentic-tdd-story-workflow-decisions-2026-04-13.md`
- `agentic-tdd-story-example-workflow-2026-04-13.md`
- `architecture.md`
- `epics.md`

The active non-TDD layout is the original story-folder specification, excluding only TDD-specific artifacts until the TDD workflow is implemented:

- excluded for now: `1-2-test-plan.md`, `1-2-batches/`;
- retained now: story file, changelog, orchestrator log, runtime-proof folder;
- added/clarified now for standard story execution: cycle state, reviews, triaged findings, remediation briefs, validation logs.

The project-local BMAD workflows under `.pi/skills/bmad-*` are treated as **active project-local BMAD-compatible overrides**. They may be amended to implement this artifact taxonomy even if upstream BMAD base workflows differ.

---

## 4. Canonical artifact responsibilities

### 4.1 `1-2-story.md`

Purpose:

- canonical BMAD story contract;
- acceptance criteria;
- tasks/subtasks;
- dev notes;
- current review follow-ups;
- concise dev agent record;
- concise file list;
- short change log pointer;
- links to story-scoped artifacts.

Allowed sections include:

```md
Status
## Story
## Acceptance Criteria
## Tasks / Subtasks
### Review Follow-ups (AI)
## Dev Notes
## Dev Agent Record
### File List
## Change Log
## Story Artifacts
## Senior Developer Review (AI)
### Action Items
```

Avoid in the story file:

- full raw review reports;
- full triage rationale beyond current action items;
- full command output;
- large orchestration task-state blocks;
- long routing history;
- remediation transcripts;
- runtime traces/logs/screenshots.

The story file should answer:

> What is the story, what is currently actionable, and where is the evidence?

### 4.2 `1-2-story-changelog.md`

Purpose:

- chronological story history;
- resolved finding history;
- major implementation decisions;
- validation milestones;
- compact human-readable evolution.

Recommended sections:

```md
# 1-2 Story Changelog

## Summary
## Timeline
## Resolved Review Findings
## Major Decisions
## Validation Milestones
```

### 4.3 `1-2-orchestrator-log.md`

Purpose:

- parent-owned routing and escalation journal;
- durable dispatch evidence;
- task-state summary snapshots;
- recovery decisions;
- sprint/status sync notes.

Recommended sections:

```md
# 1-2 Orchestrator Log

Status: active|complete|blocked

## Current Position
## Routing Log
## Dispatch Evidence
## Escalations
## Sprint Status Sync
## Recovery Notes
```

Dispatch evidence should include the shape already required by `bmad-orchestrator`:

```yaml
requestedAgent: "reviewer-a"
canonicalAgentId: "reviewer-a"
runId: "<run-id-or-not-exposed>"
agentScope: "project"
context: "fresh"
taskSource: "artifact-path"
artifactPaths:
  - "docs/_bmad-output/implementation-artifacts/1-2-un-exemple-de-story/1-2-story.md"
```

### 4.4 `1-2-cycle-state.md`

Purpose:

- machine-searchable Markdown artifact for current orchestration task state;
- UI/task projection source when useful;
- current iteration state;
- pending/in-progress/completed/blocked/failed records.

This replaces embedding large task-state YAML blocks in the story file.

Important: this must be Markdown, not a standalone `.yaml` sidecar, to preserve the current architecture rule that durable workflow state is Markdown artifacts.

Recommended format:

````md
# 1-2 Cycle State

<!-- bmad:cycle-state:start -->
```yaml
storyId: 1-2
storySlug: 1-2-un-exemple-de-story
workflow: dev-cycle
maxIterations: 5
currentIteration: 2
status: in-progress
updatedAt: "2026-05-13T00:00:00Z"

tasks:
  - taskId: dev-R2
    title: Implement review follow-ups
    targetAgent: implementer
    status: pending
    contextSource:
      type: artifact-path
      paths:
        - 1-2-story.md
        - reviews/1-2-R1-findings.md
    dependsOn: []
    activeAgentId: null
    outputArtifact: null
    routingDecision: null
    cause: null
    recommendedNextAction: null
```
<!-- bmad:cycle-state:end -->
````

Machine markers are mandatory and should be searchable with tools such as:

```bash
rg "bmad:cycle-state:start"
```

Task status vocabulary:

```text
pending
in-progress
completed
blocked
failed
```

### 4.5 `reviews/1-2-Rn-reviewer-a.md` and `reviews/1-2-Rn-reviewer-b.md`

Purpose:

- complete independent raw reviewer output;
- evidence for the review pass;
- not consumed by `/dev-story` in the normal case.

Recommended minimum shape:

```md
# Review 1-2 R2 — Reviewer A

## Verdict
PASS | CHANGES_REQUESTED | BLOCKED

## Findings

### Finding
- Severity: High|Medium|Low
- AC/Constraint: ... or N/A
- Location: file:line or N/A
- Evidence:
- Recommended fix:

## Validation Evidence

## Notes
```

### 4.6 `reviews/1-2-Rn-findings.md`

Purpose:

- parent-validated, deduplicated, action-oriented findings for one review round;
- produced by a triage/deduplication step;
- source of truth for `/dev-story` follow-up details;
- bridge between raw reviews and the story action items.

The filename intentionally omits `normalized`:

```text
reviews/1-2-R2-findings.md
```

By convention, `*-findings.md` means deduplicated / triaged / actionable / parent-validated findings.

Recommended required format:

```md
# 1-2 R2 Findings

## Summary
Verdict: CHANGES_REQUESTED
Blocking findings: 2

Source reviews:
- `reviews/1-2-R2-reviewer-a.md`
- `reviews/1-2-R2-reviewer-b.md`

## Findings

### F-R2-001
Status: open  
Severity: HIGH  
Classification: implementation-issue  
Blocking: true  
AC/Constraint: AC3  
Location: `src/foo.ts:42`  
Sources:
- `reviews/1-2-R2-reviewer-a.md`
- `reviews/1-2-R2-reviewer-b.md`

#### Problem
Describe the problem precisely.

#### Required Fix
Describe the required fix precisely enough for `/dev-story` to act.

#### Validation Requirements
List commands, tests, or behavioral checks required to prove the fix.

#### Out of Scope
Clarify what must not be changed while fixing this finding.
```

Finding status vocabulary:

```text
open
implemented
verified
deferred
dismissed
reopened
```

For the current workflow, the dev may mark the corresponding story checkboxes as complete after implementation. The stricter `implemented -> verified` lifecycle can be enforced later by reviewers using the findings artifact.

### 4.7 `remediation/`

Purpose:

- bounded fresh-context handoffs after a cycle becomes too large, reaches an escalation point, or needs targeted repair.

Recommended filename:

```text
remediation/1-2-R3-remediation-brief.md
```

Recommended sections:

```md
# Remediation Brief: 1-2 R3

## Goal
## Source of Truth
## Current Unresolved Findings
## Required Design Constraints
## Files Likely Affected
## Out of Scope
## Required Tests
## Validation Commands
## Completion Criteria
```

### 4.8 `validation/`

Purpose:

- verbose command output;
- validation logs;
- clean-install output;
- test/lint logs too long for the story file.

The story should contain only concise validation summaries, for example:

```md
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed, 201 tests.
```

Verbose logs should go under:

```text
validation/command-output-*.log
validation/1-2-validation-summary.md
```

### 4.9 `1-2-runtime-proof/`

Purpose:

- screenshots;
- traces;
- videos;
- runtime logs;
- future Playwright proof artifacts.

This folder is part of the spec-compatible story layout even before runtime proof automation is implemented.

---

## 5. Workflow responsibilities

### 5.1 `/dev-story`

`/dev-story` should:

1. resolve the story folder and canonical story file;
2. read `1-2-story.md`;
3. detect unchecked `Review Follow-ups (AI)` under `Tasks / Subtasks`;
4. extract explicit `Source: ...#F-Rn-xxx` references from those follow-ups;
5. read only the referenced `reviews/1-2-Rn-findings.md` files in the normal case;
6. locate exact finding anchors such as `### F-R2-001`;
7. use `Required Fix`, `Validation Requirements`, and `Out of Scope` while implementing;
8. update permitted story sections;
9. write verbose validation evidence under `validation/` when needed;
10. append compact history to `1-2-story-changelog.md` when needed.

Fail-closed rules for review follow-up discovery:

- if an unchecked `[AI-Review]` item has no `Source:` reference, HALT as `artifact-invalid` unless legacy fallback is explicitly allowed by the active workflow;
- if the referenced file is missing, HALT;
- if the referenced finding id is missing, HALT;
- if the referenced finding format is malformed or contradictory, HALT;
- do not scan raw reviewer reports A/B in the normal path;
- do not infer findings from parent conversation history.

Current checkbox behavior is preserved:

- when the dev implements a follow-up, it checks the matching item under `Tasks / Subtasks -> Review Follow-ups (AI)`;
- it also checks the corresponding item under `Senior Developer Review (AI) -> Action Items`;
- for now, checked by dev means implemented, not independently reviewer-verified.

### 5.2 `/code-review`

`/code-review` should:

1. write complete raw review output under `reviews/`;
2. produce or trigger production of `reviews/1-2-Rn-findings.md` when review findings need triage/deduplication;
3. write only short current action items into `1-2-story.md`;
4. append deferred/non-blocking work to `docs/_bmad-output/implementation-artifacts/deferred-work.md` when applicable;
5. update story status and sprint status according to blocking findings.

### 5.3 Findings triage / deduplication

Semantic deduplication should not be an implicit, ad-hoc responsibility hidden inside the orchestrator prompt.

Preferred model:

```text
reviewer-a + reviewer-b
  -> raw reports in reviews/

findings-triager / review-triager
  -> reviews/1-2-Rn-findings.md
  -> short linked action items in 1-2-story.md

orchestrator
  -> validates artifacts exist and are parseable
  -> applies routing decisions
```

The triage agent must know exactly how to:

1. read the raw reviewer reports for the round;
2. normalize severity and fields;
3. deduplicate findings by root cause, affected constraint, and location;
4. preserve highest justified severity;
5. classify each finding;
6. assign stable ids `F-Rn-001`, `F-Rn-002`, ...;
7. write `reviews/1-2-Rn-findings.md`;
8. write linked story action items;
9. avoid copying full review prose into the story.

Classification vocabulary should align with the existing architecture:

```text
implementation-issue
test-issue
spec-ambiguity
artifact-invalid
retry-limit-reached
environment-blocked
workflow-contract-violation
```

### 5.4 `/dev-cycle`

`/dev-cycle` should be orchestration over `/dev-story` + `/code-review` behavior, not a separate artifact model.

It should:

1. create/update `1-2-cycle-state.md`;
2. create/update `1-2-orchestrator-log.md`;
3. launch implementer with fresh context;
4. launch reviewer A/B with fresh context;
5. launch or otherwise use a findings triage/deduplication step;
6. validate `reviews/1-2-Rn-findings.md` and linked story action items;
7. route next iteration based on unresolved blocking findings;
8. stop at max iterations;
9. leave story status `in-progress` if blocking findings remain;
10. mark story `done` only when no unresolved blocking High/Medium findings remain.

`/dev-cycle` accepts an optional max-iterations argument:

```text
/dev-cycle <story-folder-or-story-file> [maxIterations]
```

Rules:

- if absent: default `5`;
- if present: integer only;
- allowed range for now: `1..5`;
- invalid value: HALT with an actionable error;
- record the chosen value in `1-2-cycle-state.md` and `1-2-orchestrator-log.md`.

Example:

```text
/dev-cycle docs/_bmad-output/implementation-artifacts/1-2-un-exemple-de-story/ 3
```

---

## 6. Story action item linking contract

The story must link actionable review work to exact findings.

### 6.1 `Senior Developer Review (AI)`

Purpose:

- short review action registry;
- human/reviewer/orchestrator audit surface;
- tells what the review found.

Format:

```md
## Senior Developer Review (AI)

### Action Items

- [x] [R2][HIGH][AC3][F-R2-001] Preserve explicit fresh-context enforcement [`src/foo.ts:42`] — Source: `reviews/1-2-R2-findings.md#F-R2-001`
```

### 6.2 `Review Follow-ups (AI)`

Purpose:

- dev work queue;
- consumed by `/dev-story`;
- tells what must be fixed now.

Location:

```md
## Tasks / Subtasks

### Review Follow-ups (AI)

- [x] [AI-Review][R2][HIGH][AC3][F-R2-001] Preserve explicit fresh-context enforcement — Source: `reviews/1-2-R2-findings.md#F-R2-001`
```

### 6.3 Required fields

Every unresolved review follow-up must include:

- round tag: `[R2]`;
- severity: `[HIGH]`, `[MEDIUM]`, or `[LOW]`;
- AC/constraint tag: `[AC3]` or `[N/A]`;
- finding id: `[F-R2-001]`;
- explicit source link: `Source: `reviews/1-2-R2-findings.md#F-R2-001``.

Normal `/dev-story` discovery starts from this explicit source link. It must not rely on heuristic discovery of raw review files.

---

## 7. Status and blocking rules

Review severity:

```text
High
Medium
Low
```

Story action item severity tags use uppercase:

```text
[HIGH]
[MEDIUM]
[LOW]
```

Blocking rules:

- `High`: blocking unless dismissed as false positive;
- `Medium`: blocking when tied to ACs, security/privacy, regression risk, data integrity, required maintainability, or workflow correctness;
- `Low`: non-blocking by default; defer unless user explicitly asks to fix.

Story status rules:

- unresolved blocking High/Medium or decision-needed finding -> story remains `in-progress`;
- only Low/deferred findings remain -> story may advance;
- no unresolved blocking findings -> story may be marked `done` by the orchestrating workflow;
- sprint status should be synced when `sprint-status.yaml` is present and story key is known.

---

## 8. Context handoff policy

### `/dev-story`

Normal implementation context:

1. `1-2-story.md`;
2. referenced `reviews/1-2-Rn-findings.md` files for open follow-ups;
3. relevant project context if configured;
4. targeted source files as needed.

It should not normally read:

- all raw reviewer reports;
- all historical findings files;
- full orchestrator log;
- full changelog;
- all validation logs.

### `/code-review`

Review context:

1. `1-2-story.md`;
2. current git diff / implementation files;
3. concise validation summary;
4. relevant source files;
5. prior unresolved findings only if explicitly needed.

### Findings triager

Triage context:

1. raw reviewer outputs for the current round;
2. `1-2-story.md` for AC and current story contract;
3. prior open findings only if needed to detect reopened/duplicate issues.

### `/dev-cycle`

The parent orchestrator should pass artifact paths/read directives, not reconstructed summaries, and all formal dispatches must use explicit fresh context.

---

## 9. Backward compatibility and migration

Active workflows may encounter legacy folders where:

- story file is named `<story_slug>.md`;
- review artifacts are flat files in the story folder;
- task state is embedded in the story;
- findings lack `Source:` links.

Migration rule:

- do not manually rewrite active legacy stories unless needed;
- new story execution should follow this taxonomy;
- workflows may support legacy discovery for old artifacts, but new artifacts must use the canonical structure;
- if a new review follow-up lacks a source link, treat it as an artifact defect.

---

## 10. Required implementation updates

### References

Create/update:

```text
.pi/references/artifact-format.md
.pi/references/workflow-status-codes.md
```

These should document:

- story folder naming;
- file naming;
- required sections;
- machine markers;
- task status vocabulary;
- finding status vocabulary;
- review action item link format;
- fail-closed behavior.

### Workflow updates

Update project-local workflows:

- `bmad-create-story`: create story folder using `<story_id>-<slug>/` and story file `1-2-story.md`.
- `bmad-dev-story`: resolve the canonical story file and follow `Source:` links from review follow-ups into `*-findings.md`.
- `bmad-code-review`: write raw reports under `reviews/`, produce/trigger `*-findings.md`, write linked short action items into the story, and defer Low findings globally.
- `bmad-dev-cycle`: externalize cycle state/logs, accept optional max iteration argument `1..5`, and use the shared taxonomy.
- Add or define a triage/deduplication role/agent/workflow step for producing `reviews/1-2-Rn-findings.md` and updating story action items.

---

## 11. Final decision

Adopt the spec-compatible story artifact structure for all standard story execution workflows, not only `/dev-cycle`.

`/dev-story`, `/code-review`, and `/dev-cycle` should all converge on the same taxonomy:

- story file is compact and action-oriented;
- raw reviews stay under `reviews/`;
- deduplicated actionable findings live in `reviews/1-2-Rn-findings.md`;
- story action items link explicitly to exact finding anchors;
- `/dev-story` follows those links without heuristic review discovery;
- cycle state is Markdown with machine-searchable markers;
- orchestration evidence lives in the orchestrator log;
- verbose validation and runtime proof are externalized.

This preserves BMAD story compatibility while making fresh-context handoffs bounded, deterministic, and future-compatible with TDD batches.

---

## 12. Implementation checklist

### Reference contracts

- [x] Create `.pi/references/artifact-format.md`.
- [x] Document canonical story folder naming: `<story_id>-<story-slug>/`.
- [x] Document canonical file naming: `<story_id>-story.md`, `<story_id>-story-changelog.md`, `<story_id>-orchestrator-log.md`, `<story_id>-cycle-state.md`.
- [x] Document canonical subfolders: `reviews/`, `remediation/`, `validation/`, `<story_id>-runtime-proof/`.
- [x] Document future TDD additions: `<story_id>-test-plan.md`, `<story_id>-batches/`.
- [x] Document required machine markers for `*-cycle-state.md`, including `<!-- bmad:cycle-state:start -->` and `<!-- bmad:cycle-state:end -->`.
- [x] Create or update `.pi/references/workflow-status-codes.md`.
- [x] Define closed task statuses: `pending`, `in-progress`, `completed`, `blocked`, `failed`.
- [x] Define closed finding statuses: `open`, `implemented`, `verified`, `deferred`, `dismissed`, `reopened`.
- [x] Define review classification codes: `implementation-issue`, `test-issue`, `spec-ambiguity`, `artifact-invalid`, `retry-limit-reached`, `environment-blocked`, `workflow-contract-violation`.

### Story creation and discovery

- [x] Update `bmad-create-story` to create one story folder per story using the full story slug.
- [x] Update `bmad-create-story` to name the canonical story file `<story_id>-story.md`.
- [x] Update story discovery in `bmad-dev-story`, `bmad-code-review`, and `bmad-dev-cycle` to prefer `<story_id>-story.md` inside the story folder.
- [x] Preserve backward-compatible discovery for existing legacy story files during migration.
- [x] Ensure generated stories include a `## Story Artifacts` section with links to story-scoped artifacts.

### Dev story workflow

- [x] Update `/dev-story` to detect unchecked `[AI-Review]` items under `Tasks / Subtasks -> Review Follow-ups (AI)`.
- [x] Require every new unchecked `[AI-Review]` item to include `Source: \`reviews/<story_id>-Rn-findings.md#F-Rn-xxx\``.
- [x] Update `/dev-story` to read referenced `*-findings.md` files before implementing review follow-ups.
- [x] Update `/dev-story` to locate exact finding headings such as `### F-R2-001`.
- [x] Update `/dev-story` to use `Required Fix`, `Validation Requirements`, and `Out of Scope` from each finding.
- [x] Add fail-closed behavior for missing source links, missing files, missing finding anchors, or malformed finding records.
- [x] Preserve current checkbox behavior: after implementation, check both the `Review Follow-ups (AI)` item and the matching `Senior Developer Review (AI)` action item.
- [x] Route verbose validation output to `validation/` instead of bloating the story file.
- [x] Append compact execution history to `<story_id>-story-changelog.md` when needed.

### Code review workflow

- [x] Update `/code-review` to write raw review reports under `reviews/`.
- [x] Define raw review filenames: `reviews/<story_id>-Rn-reviewer-a.md` and `reviews/<story_id>-Rn-reviewer-b.md`.
- [x] Define the triaged findings filename: `reviews/<story_id>-Rn-findings.md`.
- [x] Ensure review reports use structured verdicts and findings.
- [x] Ensure `Low`/deferred findings are appended to `docs/_bmad-output/implementation-artifacts/deferred-work.md` when applicable.
- [x] Ensure story status and `sprint-status.yaml` are synced according to unresolved blocking findings.

### Findings triage / deduplication

- [x] Decide whether to implement findings triage as a dedicated agent, workflow step, or project-local role.
- [x] Define the triage task prompt/contract.
- [x] Ensure the triage step reads raw reviewer reports for the current round.
- [x] Ensure the triage step deduplicates by root cause, affected constraint, and location.
- [x] Ensure the triage step assigns stable finding ids: `F-Rn-001`, `F-Rn-002`, ...
- [x] Ensure the triage step writes `reviews/<story_id>-Rn-findings.md` using the required format.
- [x] Ensure the triage step writes linked short action items to `Senior Developer Review (AI)`.
- [x] Ensure the triage step writes linked dev tasks to `Tasks / Subtasks -> Review Follow-ups (AI)`.
- [x] Ensure no full raw review prose is copied into the story file.

### Dev cycle workflow

- [x] Update `/dev-cycle` to create/update `<story_id>-cycle-state.md` instead of embedding large task-state blocks in the story.
- [x] Update `/dev-cycle` to create/update `<story_id>-orchestrator-log.md`.
- [x] Update `/dev-cycle` to pass `taskStatePath` to the Markdown cycle-state artifact or selected durable Markdown task artifact.
- [x] Update `/dev-cycle` to accept optional max iterations: `/dev-cycle <story-folder-or-file> [maxIterations]`.
- [x] Validate `maxIterations` as an integer in range `1..5`.
- [x] Default `maxIterations` to `5` when omitted.
- [x] Record chosen `maxIterations` in cycle state and orchestrator log.
- [x] Ensure every formal dispatch uses explicit `context: "fresh"`.
- [x] Ensure the orchestrator validates that raw reviews, triaged findings, and story action links exist before routing the next iteration.
- [x] Ensure max-iteration stop leaves story status `in-progress` when blocking findings remain.

### Migration and compatibility

- [x] Add migration notes for existing story folders that use `<story_slug>.md` or flat review artifacts.
- [x] Keep legacy discovery paths read-compatible during transition.
- [x] Ensure new artifacts are always written using the canonical structure.
- [x] Add tests or smoke checks for canonical story discovery.
- [x] Add tests or smoke checks for review follow-up source-link parsing.
- [x] Add tests or smoke checks for malformed/missing finding source fail-closed behavior.
- [x] Add tests or smoke checks for `/dev-cycle` max-iteration argument parsing.

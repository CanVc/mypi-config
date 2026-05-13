# BMAD Story Artifact Format Reference

**Status:** Active project-local contract  
**Updated:** 2026-05-13 22:30

This reference defines the canonical story-scoped artifact taxonomy used by the project-local BMAD-compatible workflows in `.pi/skills/`.

## 1. Story folder naming

Story execution artifacts live under the implementation artifact root in one folder per story:

```text
docs/_bmad-output/implementation-artifacts/<story_id>-<story-slug>/
```

Definitions:

```text
story_id     = <epic>-<story>        # example: 1-2
story_slug   = <story_id>-<slug>     # example: 1-2-un-exemple-de-story
story_folder = <implementation_artifacts>/<story_slug>/
```

The folder uses the full story slug for readability. Files inside the folder use the short `story_id` prefix for consistency with the Agentic TDD artifact specification.

## 2. Canonical non-TDD layout

```text
<story_slug>/
  <story_id>-story.md
  <story_id>-story-changelog.md
  <story_id>-orchestrator-log.md
  <story_id>-cycle-state.md
  <story_id>-runtime-proof/

  reviews/
    <story_id>-R1-reviewer-a.md
    <story_id>-R1-reviewer-b.md
    <story_id>-R1-findings.md

  remediation/
    <story_id>-R3-remediation-brief.md

  validation/
    <story_id>-validation-summary.md
    command-output-*.log
```

Future TDD additions use the same prefix convention:

```text
  <story_id>-test-plan.md
  <story_id>-batches/
    <story_id>-batch-01.md
```

## 3. Story file responsibilities

`<story_id>-story.md` is the compact canonical story contract and current action surface.

Allowed content includes:

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

The story file must not accumulate full raw review reports, verbose command output, full orchestration logs, runtime traces, or large task-state records.

## 4. Story artifacts section

Generated stories should include a concise pointer section:

```md
## Story Artifacts

- Changelog: `<story_id>-story-changelog.md`
- Orchestrator log: `<story_id>-orchestrator-log.md`
- Cycle state: `<story_id>-cycle-state.md`
- Reviews: `reviews/`
- Validation: `validation/`
- Runtime proof: `<story_id>-runtime-proof/`
```

## 5. Cycle state artifact

`<story_id>-cycle-state.md` is the parent-owned machine-searchable Markdown task-state artifact. It replaces large embedded story-file task-state blocks.

Required machine markers:

````md
<!-- bmad:cycle-state:start -->
```yaml
storyId: 1-2
storySlug: 1-2-un-exemple-de-story
workflow: dev-cycle
maxIterations: 5
currentIteration: 1
status: in-progress
tasks: []
```
<!-- bmad:cycle-state:end -->
````

Only the parent orchestrator updates this durable state. Runtime status is control-plane evidence until the parent validates and writes task state here.

## 6. Review artifacts

Raw independent review reports live in `reviews/`:

```text
reviews/<story_id>-R<n>-reviewer-a.md
reviews/<story_id>-R<n>-reviewer-b.md
```

Triaged, deduplicated findings for the round live in:

```text
reviews/<story_id>-R<n>-findings.md
```

`*-findings.md` means parent-validated, deduplicated, actionable findings. It is the normal source of truth for `/dev-story` review follow-up implementation.

Required finding shape:

```md
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
...

#### Required Fix
...

#### Validation Requirements
...

#### Out of Scope
...
```

## 7. Story review action links

Every unresolved review follow-up written to the story must link to an exact finding anchor.

`Senior Developer Review (AI)` action item:

```md
- [ ] [R2][HIGH][AC3][F-R2-001] Preserve explicit fresh-context enforcement [`src/foo.ts:42`] — Source: `reviews/1-2-R2-findings.md#F-R2-001`
```

`Tasks / Subtasks -> Review Follow-ups (AI)` dev task:

```md
- [ ] [AI-Review][R2][HIGH][AC3][F-R2-001] Preserve explicit fresh-context enforcement — Source: `reviews/1-2-R2-findings.md#F-R2-001`
```

Required fields:

- round tag `[R<n>]`;
- severity tag `[HIGH]`, `[MEDIUM]`, or `[LOW]`;
- AC/constraint tag such as `[AC3]` or `[N/A]`;
- finding id tag `[F-R<n>-xxx]`;
- explicit source link `Source: `reviews/<story_id>-R<n>-findings.md#F-R<n>-xxx``.

## 8. Dev-story source-link discovery

`/dev-story` starts review-follow-up discovery from unchecked `[AI-Review]` tasks in the story. For each unchecked item, it must extract the `Source:` link, open the referenced `*-findings.md`, and locate the exact heading for the finding id.

Fail closed when:

- the source link is missing;
- the findings file is missing;
- the finding heading is missing;
- the finding record is malformed or contradictory.

Do not scan raw reviewer reports in the normal path.

## 9. Validation and runtime proof

Verbose validation output belongs under `validation/`. The story records only concise command/pass-fail summaries.

Runtime evidence belongs under `<story_id>-runtime-proof/`.

## 10. Legacy compatibility

During migration, workflows may read legacy story files named `<story_slug>.md` inside the story folder or flat legacy files at `<implementation_artifacts>/<story_slug>.md`. New artifacts must be written using this canonical format.

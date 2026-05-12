# Story 1.2.1 Workflow Inventory

Inventory scope: active `.pi/skills` Markdown workflow/checklist/template files found by searching for `{implementation_artifacts}`, `story_location`, `story_file`, `story_path`, `spec_file`, `sprint-status`, and review prompt/output routing terms.

## Convention Confirmed

- Canonical v1 story artifact directory: `{implementation_artifacts}/{story_key}/`.
- Canonical story file: `{implementation_artifacts}/{story_key}/{story_key}.md`.
- Root-level global files remain allowed: `{implementation_artifacts}/sprint-status.yaml` and `{implementation_artifacts}/deferred-work.md`.
- Story and artifact names remain lowercase kebab-case; the story key remains the primary lookup key.
- Legacy flat story files (`{implementation_artifacts}/{story_key}.md`) remain readable fallback inputs only, not new output targets.

## Mandatory Updates

| File | Classification | Rationale / change |
| --- | --- | --- |
| `.pi/skills/bmad-create-story/workflow.md` | Updated | New story output now uses `{implementation_artifacts}/{story_key}/{story_key}.md`; creates story folder; previous-story lookup is recursive/folder-aware with legacy fallback. |
| `.pi/skills/bmad-dev-story/workflow.md` | Updated | Auto-discovery now searches canonical folder files first, preserves explicit paths, and uses legacy flat files only as fallback. |
| `.pi/skills/bmad-code-review/steps/step-01-gather-context.md` | Updated | Sprint-status review story selection now resolves `{spec_file}` to the canonical story-folder file before legacy fallback and sets `{review_artifact_dir}`. |
| `.pi/skills/bmad-code-review/steps/step-02-review.md` | Updated | Fallback review prompt/output artifacts for known stories now route to `{review_artifact_dir}` with `review-{story_key}-...` filenames. |
| `.pi/skills/bmad-code-review/steps/step-04-present.md` | Updated | Clarifies findings write to resolved `{spec_file}` and only `deferred-work.md` remains global. |
| `.pi/skills/bmad-sprint-planning/workflow.md` | Updated | Story detection checks `{story_location}/{story-key}/{story-key}.md` first, then legacy flat fallback; comments/examples no longer imply flat output. |
| `.pi/skills/bmad-sprint-planning/sprint-status-template.yaml` | Updated | `story_location` comments now define the implementation artifact root that contains per-story folders. |
| `.pi/skills/bmad-sprint-status/workflow.md` | Updated | Validation/summary interpretation now explains `story_location` as the artifact root containing story folders, not flat story files. |

## Compatibility Updates

| File | Classification | Rationale / change |
| --- | --- | --- |
| `.pi/skills/bmad-retrospective/workflow.md` | Compatibility update | Story scans/read paths now support canonical story folders and legacy flat files, excluding review artifacts. |
| `.pi/skills/bmad-checkpoint-preview/step-01-orientation.md` | Compatibility update | Review-story orientation and enrich scans now resolve folder-based stories first and scan recursively. |
| `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md` | Compatibility update | Previous-story continuity now scans quick-dev specs plus folder-based BMAD stories without changing quick-dev `spec-*.md` output behavior. |

## Intentionally Unchanged

| File | Classification | Rationale |
| --- | --- | --- |
| `.pi/skills/bmad-create-story/checklist.md` | Intentionally unchanged | Uses abstract `{story_file_path}` and does not prescribe flat or folder output. |
| `.pi/skills/bmad-dev-story/checklist.md` | Intentionally unchanged | Uses caller-provided `{{story_path}}` validation target only. |
| `.pi/skills/bmad-code-review/workflow.md` | Intentionally unchanged | Declares global `sprint_status`; path routing lives in step files updated above. |
| `.pi/skills/bmad-sprint-planning/checklist.md` | Intentionally unchanged | Validates sprint-status content; no story-file path convention. |
| `.pi/skills/bmad-qa-generate-e2e-tests/workflow.md` | Intentionally unchanged | Writes QA summary to `{implementation_artifacts}/tests/test-summary.md`, not a BMAD story/review artifact. |
| `.pi/skills/bmad-quick-dev/step-02-plan.md` | Intentionally unchanged | Operates on quick-dev `{spec_file}` chosen by step 01; no BMAD story file routing. |
| `.pi/skills/bmad-quick-dev/step-03-implement.md` | Intentionally unchanged | Operates on quick-dev `{spec_file}` only. |
| `.pi/skills/bmad-quick-dev/step-04-review.md` | Intentionally unchanged | Quick-dev review prompts remain part of separate quick-dev `spec-*.md` behavior, explicitly out of standard BMAD story-cycle routing. |
| `.pi/skills/bmad-quick-dev/step-05-present.md` | Intentionally unchanged | Operates on quick-dev `{spec_file}` and relative links only. |
| `.pi/skills/bmad-quick-dev/step-oneshot.md` | Intentionally unchanged | Quick-dev one-shot prompt/spec behavior remains separate from standard BMAD story-cycle artifacts. |

## Out of Scope

| File | Classification | Rationale |
| --- | --- | --- |
| `.pi/skills/bmad-correct-course/checklist.md` | Out of scope | Mentions updating `sprint-status.yaml` after approved epic changes; does not read/write story markdown or story-scoped review artifacts. |
| `.pi/skills/*/SKILL.md` reviewer/editorial name hits | Out of scope | Search hits are skill names/descriptions, not workflow artifact routing instructions. |

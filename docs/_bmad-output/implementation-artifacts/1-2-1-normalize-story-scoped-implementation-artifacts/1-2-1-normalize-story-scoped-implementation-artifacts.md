# Story 1.2.1: Normalize Story-Scoped Implementation Artifacts

Status: done

<!-- Created as an urgent hardening story after Story 1.2 to stop BMAD workflow artifacts, especially review outputs, from accumulating directly in docs/_bmad-output/implementation-artifacts. -->

## Story

As a builder,
I want every BMAD story workflow to read and write story-specific artifacts inside that story's own implementation artifact folder,
so that `/create-story`, `/dev-story`, `/code-review`, and related story-facing workflows keep `docs/_bmad-output/implementation-artifacts` clean and route story/review artifacts deterministically.

## Acceptance Criteria

1. Given active BMAD workflow skills may contain flat `{implementation_artifacts}` story path assumptions, when this story is implemented, then the implementation includes an inventory of every active `.pi/skills` workflow file that reads, writes, discovers, or updates BMAD story files under `{implementation_artifacts}`, and each inventoried file is classified as updated, intentionally unchanged, or out of scope with rationale.
2. Given `/create-story` creates a new story, when it saves the story artifact, then it writes the story file under a per-story folder, using the active v1 convention `{implementation_artifacts}/{story_key}/{story_key}.md`, and it does not write story markdown directly at `{implementation_artifacts}/{story_key}.md`.
3. Given `/create-story` needs previous-story intelligence, when it scans prior implementation artifacts, then it can find both existing folder-based story files and any legacy flat story files without missing previous story learnings.
4. Given `/dev-story` auto-discovers the next ready story from `sprint-status.yaml`, when the matching story key is selected, then it resolves the story file inside the story folder first and falls back to legacy flat files only for backward compatibility.
5. Given `/code-review` is run for a story or spec file, when review prompts, findings, reviewer outputs, or follow-up artifacts are persisted, then story-specific review artifacts are written under that story's artifact folder, while global artifacts such as `sprint-status.yaml` and `deferred-work.md` may remain at the implementation-artifacts root.
6. Given `sprint-planning` or `sprint-status` reports story locations, when it generates or validates `sprint-status.yaml`, then its comments, `story_location`, detection rules, and examples reflect the story-folder convention and do not imply that story files live flat at the implementation-artifacts root.
7. Given related BMAD workflows inspect completed or in-progress stories, when they scan `{implementation_artifacts}`, then workflows such as retrospective and checkpoint preview can locate story files in story folders and do not regress on legacy flat files.
8. Given existing artifacts already include story folders for Story 1.1 and Story 1.2, when this story is complete, then the new convention preserves those artifacts and no new review files for the current story cycle are left directly under `docs/_bmad-output/implementation-artifacts`.
9. Given this is an urgent Epic 1 hardening story, when implementation completes, then tests or validation scripts prove the updated path resolution for create-story, dev-story, code-review, sprint-planning/status, and at least one backward-compatibility case.

## Tasks / Subtasks

- [x] Confirm and document the active v1 story artifact convention. (AC: 1, 2, 6)
  - [x] Use `{implementation_artifacts}/{story_key}/` as the story artifact directory for this story unless implementation finds a blocking reason to switch to the architecture's later `stories/<story-id>/` form.
  - [x] Keep root-level global files (`sprint-status.yaml`, `deferred-work.md`) at `{implementation_artifacts}` unless a workflow-specific reason requires otherwise.
  - [x] Ensure naming remains lowercase kebab-case and preserves the existing story key as the primary lookup key.
- [x] Inventory all active BMAD workflows that touch implementation story artifacts. (AC: 1)
  - [x] Search `.pi/skills` for `{implementation_artifacts}`, `story_location`, `story_file`, `story_path`, `spec_file`, `sprint-status`, and review prompt/output writes.
  - [x] Classify every hit as mandatory update, compatibility update, intentionally unchanged, or out of scope.
  - [x] Record the final inventory in this story's Dev Agent Record or a small artifact inside this story folder.
- [x] Update `/create-story` path creation and previous-story lookup. (AC: 2, 3)
  - [x] Change `.pi/skills/bmad-create-story/workflow.md` default output path from flat `{implementation_artifacts}/{{story_key}}.md` to folder-based `{implementation_artifacts}/{{story_key}}/{{story_key}}.md`.
  - [x] Ensure the story folder is created before writing the story file.
  - [x] Update previous-story scanning from flat-only patterns to recursive/folder-aware lookup.
  - [x] Update `.pi/skills/bmad-create-story/checklist.md` if it assumes flat story paths.
- [x] Update `/dev-story` story discovery and status synchronization. (AC: 4)
  - [x] Change `.pi/skills/bmad-dev-story/workflow.md` matching-story lookup to prefer `{implementation_artifacts}/{{story_key}}/{{story_key}}.md`.
  - [x] Preserve explicit `story_path` support for any readable file path.
  - [x] Preserve legacy flat lookup as a fallback only.
  - [x] Verify status updates still modify the selected story file and `sprint-status.yaml` entry.
- [x] Update `/code-review` story-aware artifact routing. (AC: 5, 8)
  - [x] Update `.pi/skills/bmad-code-review/steps/step-01-gather-context.md` so a `review` story from sprint status resolves the story file path, not just the story key.
  - [x] Update fallback prompt/output behavior in `.pi/skills/bmad-code-review/steps/step-02-review.md` so story-specific reviewer prompt files are generated in the story folder when a story/spec is known.
  - [x] Verify `.pi/skills/bmad-code-review/steps/step-04-present.md` appends findings to the resolved story file and only writes global deferred items to `deferred-work.md`.
  - [x] If reviewer output files are produced through `pi-subagents` output paths or manual commands, document and enforce the story-folder output path pattern.
- [x] Update sprint tracking workflows and templates. (AC: 6)
  - [x] Update `.pi/skills/bmad-sprint-planning/workflow.md` detection examples and status generation to recognize folder-based story files.
  - [x] Update `.pi/skills/bmad-sprint-planning/sprint-status-template.yaml` comments if needed.
  - [x] Update `.pi/skills/bmad-sprint-status/workflow.md` if its validation, summaries, or recommendations assume flat story files.
  - [x] Update the current `docs/_bmad-output/implementation-artifacts/sprint-status.yaml` metadata/comments only if the implementation changes the meaning of `story_location`.
- [x] Update related story-inspection workflows. (AC: 7)
  - [x] Update `.pi/skills/bmad-retrospective/workflow.md` story scans to support folder-based story files.
  - [x] Update `.pi/skills/bmad-checkpoint-preview/step-01-orientation.md` if checkpoint orientation derives story/spec paths from implementation artifacts.
  - [x] Review `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md`; update only the parts that load previous BMAD story continuity, without breaking quick-dev's separate `spec-*.md` behavior.
  - [x] Review `.pi/skills/bmad-qa-generate-e2e-tests/workflow.md`; classify as unchanged unless it needs explicit story-folder output for story-scoped QA summaries.
- [x] Add regression validation. (AC: 2-9)
  - [x] Add focused tests or a validation script that creates temporary implementation artifacts with folder-based and legacy flat story files.
  - [x] Validate create-story output path, dev-story lookup preference, code-review story path resolution, sprint-planning detection, and retrospective/checkpoint compatibility.
  - [x] Run `rg` checks proving no active story workflow still instructs new story/review files to be written directly as `{implementation_artifacts}/<story-key>.md` or root-level `review-*.md`.
  - [x] Run the project's existing test suite or the closest available validation command and record evidence.

### Review Findings

- [x] [Review][Patch][High] Legacy flat story fallback can still route known-story code-review artifacts to the implementation-artifacts root — For sprint-status-selected review stories and explicit legacy flat BMAD story files, `.pi/skills/bmad-code-review/steps/step-01-gather-context.md` sets `{review_artifact_dir}` to the directory containing `{spec_file}`. In a legacy flat fallback that directory is `{implementation_artifacts}`, so `.pi/skills/bmad-code-review/steps/step-02-review.md` can generate `review-{{story_key}}-*` prompt/output files at the implementation-artifacts root. Fix by routing review artifacts to `{implementation_artifacts}/{story_key}` whenever `{story_key}` is known, including legacy flat fallback and explicit flat BMAD story paths; keep directory-of-spec behavior only for non-BMAD/no-story specs.
- [x] [Review][Patch][Medium] Story File List omits a modified planning artifact [`docs/_bmad-output/planning-artifacts/epics.md`] — Reviewer A and Reviewer B both observed `git diff --name-status HEAD` includes `M docs/_bmad-output/planning-artifacts/epics.md`, while the story File List omits it. Resolve by adding the file to the story File List if it belongs to this story, or by preserving/reverting it outside this story if it is unrelated user work.

## Dev Notes

### Current Problem

Review artifacts have already accumulated in or near `docs/_bmad-output/implementation-artifacts`, and Story 1.2's File List still records review paths as if review files were written directly at the implementation-artifacts root. The current repository now has per-story folders for Story 1.1 and Story 1.2, but the active BMAD workflow instructions still contain several flat-path assumptions. This story hardens the workflow instructions before Story 1.3 so future story cycles start cleanly.

### Active Inventory from Initial Scan

Mandatory update candidates:

- `.pi/skills/bmad-create-story/workflow.md`
  - Current default output: `{implementation_artifacts}/{{story_key}}.md`.
  - Current previous story lookup: `{implementation_artifacts}/{{epic_num}}-{{previous_story_num}}-*.md`.
- `.pi/skills/bmad-dev-story/workflow.md`
  - Current direct search and matching-story lookup are rooted in `{implementation_artifacts}` and mention `{{story_key}}.md`.
- `.pi/skills/bmad-code-review/steps/step-01-gather-context.md`
  - Finds `review` stories from sprint status but only sets `{story_key}`; it does not reliably resolve the story file path.
- `.pi/skills/bmad-code-review/steps/step-02-review.md`
  - Fallback prompt files are generated in `{implementation_artifacts}` when subagents are unavailable.
- `.pi/skills/bmad-code-review/steps/step-04-present.md`
  - Writes review findings to `{spec_file}` and deferred items to `{implementation_artifacts}/deferred-work.md`; this is acceptable only if `{spec_file}` is resolved to the story-folder file.
- `.pi/skills/bmad-sprint-planning/workflow.md`
  - `story_location` is `{implementation_artifacts}` and story detection example checks `{story_location_absolute}/{story-key}.md`.
- `.pi/skills/bmad-sprint-planning/sprint-status-template.yaml`
  - Documents `story_location`; verify examples/comments align with folder-based story files.
- `.pi/skills/bmad-sprint-status/workflow.md`
  - Reads `story_location` and recommends create/dev/review flows; verify no flat-path assumptions remain.

Compatibility update candidates:

- `.pi/skills/bmad-retrospective/workflow.md`
  - Scans `{implementation_artifacts}` for story files and reads `{implementation_artifacts}/{{epic_number}}-{{story_num}}-*.md`; must become recursive/folder-aware.
- `.pi/skills/bmad-checkpoint-preview/step-01-orientation.md`
  - Scans sprint status and implementation artifacts for review/spec orientation; must not assume flat files.
- `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md`
  - Uses `{implementation_artifacts}` for quick-dev `spec-*.md` and previous-story continuity. Do not break quick-dev specs; update only BMAD story continuity scans if needed.

Likely unchanged or explicitly out of scope unless implementation finds direct story coupling:

- `.pi/skills/bmad-qa-generate-e2e-tests/workflow.md`
  - Writes `{implementation_artifacts}/tests/test-summary.md`, which is a QA summary path rather than a BMAD story file path.
- `.pi/skills/bmad-quick-dev/step-02-plan.md`, `step-04-review.md`, `step-oneshot.md`
  - Use global `deferred-work.md` or quick-dev review prompts. These are not standard BMAD story-cycle artifacts unless invoked with a story context.

### Path Convention for This Story

Use this v1 standard BMAD convention unless the implementation updates all active docs and workflows consistently to another convention:

```text
docs/_bmad-output/implementation-artifacts/
  sprint-status.yaml              # global
  deferred-work.md                # global
  <story-key>/
    <story-key>.md                # canonical story file
    review-<story-key>-*.md       # story-specific review outputs/prompts/findings when separate files are needed
    execution-log.md              # optional story-specific workflow log
```

The architecture document also mentions `docs/_bmad-output/implementation-artifacts/stories/<story-id>/`. Do not leave both conventions active for new standard BMAD story workflows. If implementation chooses the architecture form instead, update sprint status, docs, tests, and existing workflow examples together.

### Architecture and Planning References

- Implementation artifacts are the durable execution state and Markdown artifacts are source of truth. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Workflow-Artifacts]
- Artifact file and folder names use lowercase kebab-case. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns--Consistency-Rules]
- Current planning requires implementation artifacts under a per-story folder with review artifacts and runtime-proof as applicable. [Source: docs/_bmad-output/planning-artifacts/epics.md#Additional-Requirements]
- FR34 already requires story artifacts organized in a per-story folder. [Source: docs/_bmad-output/planning-artifacts/epics.md#Functional-Requirements]

### Implementation Guardrails

- Do not change provider secrets or model configuration.
- Do not move or delete existing Story 1.1 / Story 1.2 artifacts unless a migration step is explicitly validated.
- Do not modify legacy `.agents/skills` unless runtime validation proves those files are active for the current slash-command workflow.
- Preserve explicit-story-path behavior for users who pass a path manually.
- Preserve backward compatibility for legacy flat story files so older projects do not become unreadable.
- Prefer simple Markdown workflow edits and tests; do not introduce a custom extension solely for path joining unless deterministic runtime code is already required.

## Dev Agent Record

### Agent Model Used

GPT-5.5 (`openai-codex/gpt-5.5`)

### Debug Log References

- `python -m unittest tests.test_bmad_story_artifact_paths` failed because `python` is unavailable in this environment; reran with `python3`.
- RED validation: `python3 -m unittest tests.test_bmad_story_artifact_paths` failed before workflow edits, proving flat-path assumptions were still present.
- Focused validation: `python3 -m unittest tests.test_bmad_story_artifact_paths` passed after implementation.
- Full regression validation: `python3 -m unittest discover -s tests` initially exposed an existing flat Story 1.1 path assumption in `tests/test_bmad_orchestrator_guidance.py`; updated the test to the folder-based story path.
- Full regression validation: `python3 -m unittest discover -s tests` passed (97 tests).
- Static path check: `rg -n '(`default_output_file` = `\{implementation_artifacts\}/\{\{story_key\}\}\.md`|Find matching story file in \{implementation_artifacts\} using story_key pattern: \{\{story_key\}\}\.md|generate prompt files in `\{implementation_artifacts\}` — one per reviewer role)' .pi/skills || true` returned no matches.
- Root review artifact check: `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` returned no files.
- Whitespace validation: `git diff --check` returned no issues.
- Review-fix validation: `python3 -m unittest tests.test_bmad_story_artifact_paths` passed (8 tests), including legacy flat code-review artifact-dir coverage.
- Review-fix full regression validation: `python3 -m unittest discover -s tests` passed (98 tests).
- Review-fix static path check: `rg -n '(`default_output_file` = `\{implementation_artifacts\}/\{\{story_key\}\}\.md`|Find matching story file in \{implementation_artifacts\} using story_key pattern: \{\{story_key\}\}\.md|generate prompt files in `\{implementation_artifacts\}` — one per reviewer role)' .pi/skills || true` returned no matches.
- Review-fix root review artifact check: `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` returned no files.
- Review-fix whitespace validation: `git diff --check` returned no issues.

### Completion Notes List

- Confirmed the active v1 convention as `{implementation_artifacts}/{story_key}/{story_key}.md`, with `sprint-status.yaml` and `deferred-work.md` remaining global root artifacts.
- Added `workflow-inventory.md` inside this story folder classifying active `.pi/skills` hits as updated, compatibility-updated, intentionally unchanged, or out of scope.
- Updated create-story, dev-story, code-review, sprint-planning/status, retrospective, checkpoint-preview, and quick-dev continuity instructions to prefer story folders and keep legacy flat story files as read-only fallback compatibility.
- Updated current `sprint-status.yaml` comments/metadata to describe `story_location` as the implementation artifact root containing per-story folders.
- Added regression tests covering temporary folder/legacy story fixtures, workflow text expectations, code-review routing, sprint/related workflow compatibility, and disallowed flat-output instructions.
- Updated an existing Story 1.1 guidance test to read the folder-based story artifact so the full regression suite matches the new convention.
- ✅ Resolved review finding [High]: code-review now routes known-story prompts/outputs to `{implementation_artifacts}/{story_key}` even when the story file is legacy flat or explicitly provided, while preserving directory-of-spec behavior for non-BMAD specs.
- ✅ Resolved review finding [Medium]: added `docs/_bmad-output/planning-artifacts/epics.md` to the File List because the Story 1.2.1 planning entry is part of this story's tracked changes.
- ✅ Parallel review iteration 2 completed cleanly with Reviewer A and Reviewer B: High=0, Medium=0, Low=0; story marked done.

### File List

- `.pi/skills/bmad-checkpoint-preview/step-01-orientation.md`
- `.pi/skills/bmad-code-review/steps/step-01-gather-context.md`
- `.pi/skills/bmad-code-review/steps/step-02-review.md`
- `.pi/skills/bmad-code-review/steps/step-04-present.md`
- `.pi/skills/bmad-create-story/workflow.md`
- `.pi/skills/bmad-dev-story/workflow.md`
- `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md`
- `.pi/skills/bmad-retrospective/workflow.md`
- `.pi/skills/bmad-sprint-planning/sprint-status-template.yaml`
- `.pi/skills/bmad-sprint-planning/workflow.md`
- `.pi/skills/bmad-sprint-status/workflow.md`
- `docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md`
- `docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/workflow-inventory.md`
- `docs/_bmad-output/implementation-artifacts/sprint-status.yaml`
- `docs/_bmad-output/planning-artifacts/epics.md`
- `tests/test_bmad_orchestrator_guidance.py`
- `tests/test_bmad_story_artifact_paths.py`

### Change Log

- 2026-05-12: Normalized active `.pi` BMAD story workflow artifact routing to the story-folder convention with legacy flat-read fallback and added regression coverage.
- 2026-05-13: Addressed code review findings by hardening known-story code-review artifact routing, adding legacy flat routing coverage, and completing the File List entry for `epics.md`.
- 2026-05-13: Parallel code-review rerun returned no findings; story marked done.

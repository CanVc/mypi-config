# Story 1.2.2: Display Subagent Model and Task Summary

Status: done

<!-- Created from user request after Story 1.2.1: add per-subagent model name and a short current-task summary to pi-subagents visibility surfaces. -->

## Story

As a builder,
I want each visible subagent run to show the model it is using and a short summary of its assigned task,
so that I can quickly understand which model is doing what across foreground, parallel, chain, and background subagent workflows.

## Acceptance Criteria

1. Given `pi-subagents@0.24.2` renders foreground subagent results, when a single, parallel, or chain subagent is running or completed, then each rendered child row displays the effective model when known and a concise task summary without dumping the full injected prompt.
2. Given async/background subagent runs use `status.json` and the async widget, when a single, parallel, or chain run is queued, running, completed, failed, or paused, then each visible step/agent can display the effective model when known and the concise task summary.
3. Given subagent tasks are often decorated with read/write/progress/output/fork instructions, when the task summary is generated, then it is derived from the clean original task where possible and strips or avoids framework-injected noise such as `[Read from:]`, `[Write to:]`, progress instructions, output instructions, and fork preambles.
4. Given a task has explicit model override, agent default model, thinking suffix, fallback candidate, or inherited default model, when the model is displayed, then the UI uses the most specific model reference available and degrades gracefully for inherited/unknown defaults without crashing or misleading status output.
5. Given background run status files and result JSON may already exist from older plugin versions, when the updated extension reads those files, then all new fields are optional and backward compatible; existing async status/result readers continue to tolerate missing model/task-summary fields.
6. Given `.pi/npm/` is regenerated and ignored, when this story is implemented, then all `pi-subagents` source changes are captured in a version-scoped durable patch under `.pi/patches/` and can be reapplied by `bash .pi/install-packages.sh --patch`.
7. Given the project has regression tests for agent/model routing and BMAD workflow behavior, when validation runs, then existing tests still pass and new focused coverage proves task-summary/model-display propagation or patch durability for the modified `pi-subagents` behavior.
8. Given Story 1.2.1 normalized implementation artifacts into story folders, when this story creates tests, logs, or review artifacts, then story-specific artifacts remain inside `docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/` or are omitted; no new `review-*.md` or story markdown is written directly at the implementation-artifacts root.

## Tasks / Subtasks

- [x] Confirm target display surfaces and runtime data flow. (AC: 1, 2, 5)
  - [x] Inspect `pi-subagents` foreground renderers, async widget renderers, status formatters, and result details types.
  - [x] Identify exactly where model is already available and where task text is currently lost or too noisy.
  - [x] Record any intentionally unchanged surfaces in Dev Agent Record if they are out of scope.
- [x] Add task-summary and model-display data propagation. (AC: 1, 2, 3, 4, 5)
  - [x] Add optional task summary fields to shared result/progress/async status types without renaming existing fields.
  - [x] Add or reuse a helper that generates concise task summaries from clean task text and strips injected instruction noise defensively.
  - [x] Propagate clean task summaries through foreground single, parallel, and chain execution before read/write/progress/output/fork instructions are injected.
  - [x] Propagate task summaries through async single, async parallel, async chain runner steps, `status.json`, async job tracker, and async status summaries.
  - [x] Preserve model/fallback metadata already captured by foreground and async execution, and add model to running progress where needed for display.
- [x] Update TUI/status rendering. (AC: 1, 2, 4)
  - [x] Show model and task summary in foreground compact single-result rendering.
  - [x] Show model and task summary in foreground compact multi-result rows for parallel and chain runs.
  - [x] Keep expanded foreground renderers useful: full task remains available where appropriate, while summary/model are easy to scan.
  - [x] Show model and task summary in async widget rows, including active parallel group and chain step views.
  - [x] Show model and task summary in `subagent({ action: "status" })` active-run and detailed status outputs.
- [x] Make the change durable as a project patch. (AC: 6)
  - [x] Modify the installed package source only as implementation workspace material.
  - [x] Generate `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch` relative to `.pi/npm/node_modules/pi-subagents/`.
  - [x] Verify `bash .pi/install-packages.sh --patch` applies or reports the patch as already applied.
  - [x] Ensure the new patch coexists with the existing project-agent override patch.
- [x] Add regression validation. (AC: 5, 6, 7, 8)
  - [x] Add focused tests or static validation that prove the durable patch contains optional task-summary/model-display propagation and renderer/status changes.
  - [x] Run `python3 -m unittest discover -s tests`.
  - [x] Run `git diff --check`.
  - [x] Run a root-artifact cleanliness check proving no story-specific review files were written directly under `docs/_bmad-output/implementation-artifacts`.

### Review Follow-ups (AI)

- [x] [AI-Review][MEDIUM][AC1] Foreground running parallel/chain rows must render task summaries, not only completed rows; remove the `!rRunning` summary gate in `.pi/npm/node_modules/pi-subagents/src/tui/render.ts` and keep activity/status visible alongside the summary.
- [x] [AI-Review][MEDIUM][AC3, AC7] Foreground chain summaries must be derived from the clean assigned task instead of injected/expanded `{previous}` task text; thread a clean `taskSummary`/override through foreground chain execution into `runSync`, extend stripping for actual progress/output injected forms such as `Create and maintain progress at:` / `Update progress at:`, and add focused regression coverage for these edge cases.
- [x] [AI-Review][MEDIUM][AC3, AC7] Second-pass review found foreground chain summaries still expand `{previous}` before summary generation; compute a separate summary source from the assigned/default chain template before `{previous}` replacement for both sequential and parallel foreground chain paths, pass that summary override to `runSync`, and add behavioral regression coverage for default/explicit `{previous}` chain steps.

## Dev Notes

### Source of Request

The builder requested an enhancement to `pi-subagents`: add the model name and a short summary of the current task for each subagent. The initial analysis found this belongs in the `pi-subagents` extension rather than a BMAD workflow skill.

### Current Runtime Package and Durability Constraints

- Installed package: `.pi/npm/node_modules/pi-subagents`, version `0.24.2`. [Source: .pi/npm/node_modules/pi-subagents/package.json]
- Project package declaration: `.pi/settings.json` pins `npm:pi-subagents@0.24.2`. [Source: .pi/settings.json]
- `.pi/npm/` is ignored/regenerated; direct edits there are not durable. Durable local changes must be captured under `.pi/patches/` and applied by `.pi/patches/apply-patches.sh` / `.pi/install-packages.sh`. [Source: .pi/install-packages.sh; .pi/patches/apply-patches.sh]
- Existing durable patch pattern: `.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch` applies unified diffs relative to `.pi/npm/node_modules/pi-subagents/`. [Source: .pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch]

### Relevant `pi-subagents` Runtime Files

Primary files expected to change:

- `.pi/npm/node_modules/pi-subagents/src/shared/types.ts`
  - `AgentProgress` currently has `task: string` but no model field.
  - `SingleResult` already has `task`, `model`, `attemptedModels`, and `modelAttempts`.
  - `AsyncStatus.steps[]` already has `model`, `attemptedModels`, and `modelAttempts`, but no task/task summary.
- `.pi/npm/node_modules/pi-subagents/src/runs/shared/parallel-utils.ts`
  - `RunnerSubagentStep` already carries execution `task`, `model`, and `modelCandidates`; add optional display summary here rather than changing execution behavior.
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts`
  - `runSync()` and `runSingleAttempt()` build `SingleResult`/`AgentProgress` and process child `message_end` model data.
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts`
  - Main foreground single/parallel path; this is where clean task strings exist before output/read/progress injection.
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/chain-execution.ts`
  - Foreground chain path; clean templates are resolved before `{task}`, `{previous}`, `{chain_dir}`, and chain instructions are injected.
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-execution.ts`
  - Converts public inputs to runner steps; clean task summaries should be attached before runner process spawn.
- `.pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts`
  - Writes `status.json` and result JSON. Add optional task summary fields to status steps without breaking old files.
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts`
  - Polls `status.json` into `AsyncJobState`; if types are updated and steps are copied, optional fields should flow naturally.
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts`
  - Formats active async run list; currently appends `step.model` but no task summary.
- `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts`
  - Formats detailed `subagent({ action: "status" })`; step lines currently omit model/task summary.
- `.pi/npm/node_modules/pi-subagents/src/tui/render.ts`
  - Foreground compact renderers, expanded renderers, and async widget rows are the main display targets.

### Display/Behavior Guidance

- Prefer adding optional fields like `taskSummary?: string` and `model?: string` rather than changing existing field meanings.
- Do not use fully injected task text as the summary when a clean task is available; injected tasks may contain fork preambles, `[Read from:]`, `[Write to:]`, progress instructions, output instructions, or long `{previous}` content.
- Renderer output should be concise and width-aware. A good compact shape is: `<agent> (<model>) · <stats>` followed by `⎿ <task summary>`.
- If the effective model is unavailable because the child inherited the parent default and no child message has arrived yet, display should gracefully omit the model or show a neutral `default` label. Do not claim a specific model that is not known.
- Fallback attempts should remain visible through existing `attemptedModels` / `modelAttempts` behavior.
- Existing async status/result JSON from pre-change runs may lack task summaries. Readers and renderers must handle missing fields.

### Project Context and Architecture Constraints

- Pi TUI is the operator interface; additional workflow UI belongs in Pi package capabilities or optional extension widgets/status lines. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Frontend-Architecture]
- `pi-subagents` is the selected generic dispatch substrate; workflow-specific logic stays above it and `subagent(...)` remains workflow-agnostic. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Dispatch-Patterns]
- Runtime signals are control-plane only; durable workflow truth remains Markdown artifacts. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]
- Artifact/file names use lowercase kebab-case. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Naming-Patterns]

### Previous Story Intelligence

Story 1.2.1 normalized story-scoped artifacts and established the active v1 convention `{implementation_artifacts}/{story_key}/{story_key}.md`. Keep this story's artifacts in `docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/`. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md]

Story 1.2.1 also showed the preferred validation pattern for local workflow changes:

- `python3 -m unittest discover -s tests`
- `git diff --check`
- root review artifact check with `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print`

### Known Workspace Caution

At story creation time, the working tree already contained unrelated user changes that appear to move Story 1.2 artifacts from `1-2-add-agent-definitions-and-model-routing-contract/` to `1-2-0-add-agent-definitions-and-model-routing-contract/`. Do not revert or overwrite those changes unless explicitly instructed.

## Senior Developer Review (AI)

### Review Date

2026-05-13

### Review Outcome

Approved — initial review found 2 Medium blockers and second-pass review found 1 remaining Medium blocker; all Medium findings were fixed by the third dev iteration. Final review found no Medium+ blockers.

### Severity Breakdown

- High: 0
- Medium: 3 total (0 remaining open)
- Low: 1 final bookkeeping concern addressed without another dev iteration

### Action Items

- [x] [MEDIUM][AC1] Foreground running parallel/chain rows omit task summaries because `.pi/npm/node_modules/pi-subagents/src/tui/render.ts` renders `taskSummary` only when `!rRunning`; running rows must show the concise task summary as required by AC1.
- [x] [MEDIUM][AC3, AC7] Foreground chain summaries can be generated from injected/expanded task text because clean task text is computed in `chain-execution.ts` but not threaded into `runSync`; actual injected progress/output instructions can also summarize as noise (`---`). Use a clean summary override and add focused regression coverage.
- [x] [MEDIUM][AC3, AC7] Second-pass review: foreground chain summaries still use expanded `{previous}` output because `chain-execution.ts` computes the summary source after replacing `{previous}` with prior output. Compute summary input from the assigned/default template before replacement and add regression coverage for default/explicit `{previous}` chain tasks.

### Reviewer Evidence

- Reviewer A: `render.ts:944-951` gates task summaries behind `!rRunning`; `chain-execution.ts:192-197,227-235,732-737,776-783` computes clean task text but calls `runSync` with mutated task strings; `execution.ts:166-197` builds summaries from the received mutated task.
- Reviewer B: confirmed the same two Medium findings and observed `buildTaskSummary("\n\n---\nCreate and maintain progress at: ...")` returns `"---"`, proving an AC3 injected-noise gap.
- Validation during review: `python3 -m unittest discover -s tests` / equivalent quiet run passed, `git diff --check` passed, root artifact check passed, patch reverse/apply checks passed.
- Second-pass Reviewer A approved with no findings after verifying running-row rendering, clean summary override plumbing, injected-noise stripping, durable patch contents, and validations.
- Second-pass Reviewer B found one remaining Medium: `settings.ts:157-167` defaults later chain tasks to `{previous}`, but `chain-execution.ts:192-197` and `:733-737` replace `{previous}` before building `taskSummaryOverride`; expanded prior output can still leak as the next task summary. Literal `{previous}` already maps to `continue from previous output`, so the fix should preserve/neutralize the template before replacement.
- Final review: no Medium+ blockers remain. Reviewer B approved with no findings; Reviewer A approved with one Low bookkeeping concern, addressed by setting story/sprint status to `done` and refreshing stale completion wording.

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4 (claude-sonnet-4-20250514)

### Debug Log References

- Inspected the BMAD review findings against `.pi/npm/node_modules/pi-subagents/src/tui/render.ts`, `shared/formatters.ts`, `runs/foreground/execution.ts`, and `runs/foreground/chain-execution.ts` before making follow-up changes.
- Updated foreground multi-row rendering to keep task summaries visible for running rows and to fall back to the resolved `rProg?.taskSummary` when progress is sourced from the aggregate progress array.
- Extended `buildTaskSummary()` stripping to cover labeled injected output forms such as `**Output:** Write your findings to: ...` in addition to progress-only injected suffixes.
- Regenerated `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch` against a clean `pi-subagents@0.24.2` install with the project-agent override patch applied as the patch baseline.
- Second-pass fix: foreground chain summaries were still derived from task text after `{previous}` replacement with actual prior output. Added `summarySource` computation in both sequential and parallel chain paths in `chain-execution.ts`: the template is processed with `{task}` and `{chain_dir}` replaced first, then `{previous}` is replaced with neutral `"continue from previous output"` text for summary purposes, before the actual `{previous}` → prior-output replacement produces the execution task string.
- Updated existing test assertion from `buildTaskSummary(cleanTask)` to `buildTaskSummary(summarySource)` to match the new code.
- Added new `TestReviewFollowUpChainSummarySourceBeforePrevious` test class with 6 tests covering: sequential chain uses summarySource, parallel chain uses summarySource, summarySource replaces `{previous}` neutrally, cleanTask still used for recordRun, default `{previous}`-only template produces neutral summary, and explicit `{previous}` in mixed template.
- Validation: `python3 -m unittest discover -s tests` — 151 tests OK.
- Validation: `git diff --check` — no issues.
- Validation: `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — no root review artifacts.
- Validation: `bash .pi/install-packages.sh --patch` — both patches already applied successfully.
- Validation: patch reverse/apply dry-run verification for `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch` — OK.

### Completion Notes List

- Completed the two BMAD Medium follow-ups without expanding scope beyond the reviewed renderer/task-summary issues.
- Foreground compact multi-row rendering now keeps task summaries visible while rows are running and resolves summaries from `r.taskSummary`, `rProg?.taskSummary`, or `r.progress?.taskSummary` so parallel/chain running rows do not lose the clean summary.
- Foreground chain execution now threads `taskSummaryOverride: buildTaskSummary(summarySource)` into `runSync`; follow-up regression coverage locks that behavior in without using expanded `{previous}` output as the summary source.
- Extended `buildTaskSummary()` stripping to remove labeled single-output instructions (`**Output:** Write your findings to: ...`) as well as progress-only injected suffixes and separator-only noise.
- Third follow-up (second-pass review): fixed foreground chain summaries to compute `summarySource` from the chain template BEFORE `{previous}` replacement in both sequential and parallel paths. The `summarySource` replaces `{previous}` with neutral `"continue from previous output"` text, preventing expanded prior output from leaking into task summaries. The execution task string still uses the full expanded `{previous}` for correct agent behavior.
- Refreshed durable patch `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch` (398 lines, 10 files changed) and verified it still coexists with `.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch`.
- Added `TestReviewFollowUpChainSummarySourceBeforePrevious` regression test class (6 tests) for default/explicit `{previous}` chain step summary behavior.
- Full validation passes: 151 unit tests, `git diff --check`, root review-artifact cleanliness check, `.pi/install-packages.sh --patch`, and patch dry-run/apply/reverse verification.

### File List

- `.pi/npm/node_modules/pi-subagents/src/shared/formatters.ts`
- `.pi/npm/node_modules/pi-subagents/src/tui/render.ts`
- `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch`
- `tests/test_subagent_model_task_summary.py`
- `docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md`

### Change Log

- 2026-05-13: Created Story 1.2.2 for displaying subagent model names and concise task summaries.
- 2026-05-13: Implemented full story — added `buildTaskSummary` helper, optional `taskSummary`/`model` fields to types, propagated through foreground/async execution paths, updated all renderers and status formatters, generated durable patch, and added regression tests.
- 2026-05-13: Addressed BMAD review follow-ups — kept running parallel/chain row summaries visible, added running-progress summary fallback in foreground multi-row rendering, tightened output/progress noise stripping, refreshed the durable patch, and re-ran validations (145 tests passing).
- 2026-05-13: Fixed second-pass review finding — foreground chain summaries now compute `summarySource` from template before `{previous}` replacement for both sequential and parallel chain paths, preventing expanded prior output from leaking into summaries. Updated existing test, added 6 new regression tests, refreshed durable patch (398 lines). All 151 tests passing.

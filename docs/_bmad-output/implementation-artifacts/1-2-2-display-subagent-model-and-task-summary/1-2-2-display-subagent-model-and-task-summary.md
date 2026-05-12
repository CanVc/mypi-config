# Story 1.2.2: Display Subagent Model and Task Summary

Status: ready-for-dev

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

- [ ] Confirm target display surfaces and runtime data flow. (AC: 1, 2, 5)
  - [ ] Inspect `pi-subagents` foreground renderers, async widget renderers, status formatters, and result details types.
  - [ ] Identify exactly where model is already available and where task text is currently lost or too noisy.
  - [ ] Record any intentionally unchanged surfaces in Dev Agent Record if they are out of scope.
- [ ] Add task-summary and model-display data propagation. (AC: 1, 2, 3, 4, 5)
  - [ ] Add optional task summary fields to shared result/progress/async status types without renaming existing fields.
  - [ ] Add or reuse a helper that generates concise task summaries from clean task text and strips injected instruction noise defensively.
  - [ ] Propagate clean task summaries through foreground single, parallel, and chain execution before read/write/progress/output/fork instructions are injected.
  - [ ] Propagate task summaries through async single, async parallel, async chain runner steps, `status.json`, async job tracker, and async status summaries.
  - [ ] Preserve model/fallback metadata already captured by foreground and async execution, and add model to running progress where needed for display.
- [ ] Update TUI/status rendering. (AC: 1, 2, 4)
  - [ ] Show model and task summary in foreground compact single-result rendering.
  - [ ] Show model and task summary in foreground compact multi-result rows for parallel and chain runs.
  - [ ] Keep expanded foreground renderers useful: full task remains available where appropriate, while summary/model are easy to scan.
  - [ ] Show model and task summary in async widget rows, including active parallel group and chain step views.
  - [ ] Show model and task summary in `subagent({ action: "status" })` active-run and detailed status outputs.
- [ ] Make the change durable as a project patch. (AC: 6)
  - [ ] Modify the installed package source only as implementation workspace material.
  - [ ] Generate `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch` relative to `.pi/npm/node_modules/pi-subagents/`.
  - [ ] Verify `bash .pi/install-packages.sh --patch` applies or reports the patch as already applied.
  - [ ] Ensure the new patch coexists with the existing project-agent override patch.
- [ ] Add regression validation. (AC: 5, 6, 7, 8)
  - [ ] Add focused tests or static validation that prove the durable patch contains optional task-summary/model-display propagation and renderer/status changes.
  - [ ] Run `python3 -m unittest discover -s tests`.
  - [ ] Run `git diff --check`.
  - [ ] Run a root-artifact cleanliness check proving no story-specific review files were written directly under `docs/_bmad-output/implementation-artifacts`.

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

## Dev Agent Record

### Agent Model Used

N/A - create-story workflow generated this story artifact.

### Debug Log References

- Loaded `_bmad/bmm/config.yaml` and resolved communication/document languages plus planning/implementation artifact roots.
- Loaded `sprint-status.yaml`, `epics.md`, `architecture.md`, create-story template/checklist, previous Story 1.2.1, and a scout subagent context pass over `pi-subagents` runtime files.
- Removed transient scout output `context.md` from the repository root after using its findings; it was not a durable story artifact.
- Validation: confirmed canonical folder story path exists and legacy flat story path does not exist.
- Validation: `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` returned no root review artifacts.
- Validation: `git diff --check` returned no issues.

### Completion Notes List

- Created story folder and story file using the v1 story-scoped convention.
- Created Story 1.2.2 from the builder's explicit request and prior analysis context because the planning epics did not yet contain a dedicated 1.2.2 entry.
- Added implementation guidance for foreground, async, status, renderer, type, and durable patch paths.
- Updated `sprint-status.yaml` to track Story 1.2.2 as `ready-for-dev`.

### File List

- `docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md`
- `docs/_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- 2026-05-13: Created Story 1.2.2 for displaying subagent model names and concise task summaries.

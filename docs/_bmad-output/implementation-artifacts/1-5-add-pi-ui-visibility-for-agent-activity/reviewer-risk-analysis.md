# Reviewer Risk Analysis — Story 1.5 Add Pi UI Visibility for Agent Activity

## Review

- **Correct:** Story 1.5 targets visibility only: role labels, active agent/activity title, terminal titles, task/todo progress, stale-state handling, and safe degraded rendering. Evidence: `docs/_bmad-output/planning-artifacts/epics.md:513-544`.
- **Correct:** Architecture already forbids a separate frontend and says Pi TUI is the UI surface; additional UX must use Pi package capabilities, prompt/skill guidance, or optional Pi extension widgets/overlays. Evidence: `docs/_bmad-output/planning-artifacts/architecture.md:137-140`, `architecture.md:352-359`.
- **Correct:** Story 1.4 established the durable task-state contract: Markdown task records are source of truth, with fixed statuses `pending`, `in-progress`, `completed`, `blocked`, `failed`; runtime statuses such as `running`, `complete`, `paused`, and `detached` must be mapped before durable writes. Evidence: `.pi/skills/bmad-orchestrator/SKILL.md:65-118`, `tests/test_orchestrator_task_routing_state.py:32-110`.
- **Correct:** `pi-subagents` already exposes significant UI/progress surfaces: foreground progress, async widget, per-agent progress for parallel background runs, chain/parallel group display, status action, output/read/progress parameters, and task/model summaries in the current patched renderer. Evidence: `.pi/npm/node_modules/pi-subagents/README.md:141-147`, `README.md:692-725`, `README.md:883-897`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:612-622`, `render.ts:713-735`, `render.ts:845-861`, `render.ts:930-951`.

## Risks and required guardrails

### Risk 1 — Developers build the wrong UI surface or duplicate Pi features

**Evidence:** Story 1.5 says "Pi UI" and "terminal UI" (`epics.md:521-544`), while architecture says no separate UI/web frontend and Pi TUI is the interface (`architecture.md:137-140`, `architecture.md:352-359`). `pi-subagents` already has async widget/status/live progress surfaces (`README.md:141-147`, `README.md:883-897`).

**Failure mode:** Implementation creates a web dashboard, bespoke CLI/status service, or custom task runner instead of projecting Story 1.4 state through Pi TUI / existing `pi-subagents` surfaces.

**Missing guardrail:** Story 1.5 should explicitly say:
- No web UI, daemon, database, or separate frontend.
- Prefer existing `pi-subagents` TUI/status rendering; add only a narrow Pi extension/widget if existing package surfaces cannot satisfy an AC.
- Do not add role-specific dispatch tools or a new orchestration runtime.

**Tests to require:**
- Provider-free contract test that fails if Story 1.5 implementation adds obvious non-Pi UI roots/files (`src/ui`, `web`, `vite`, `next`, `express`, dashboard server) unless explicitly justified in the story.
- Regression test that no `dispatch_subagent`, custom role-specific subagent tool, or dispatchable `.pi/agents/orchestrator.md` / `.pi/agents/bmad-orchestrator.md` appears.
- If a custom Pi extension is added, test it has extension-local `package.json` scripts for `typecheck`, `lint`, `test`, and `validate`, per `architecture.md:153-162`.

### Risk 2 — UI treats runtime progress as durable task truth and breaks Story 1.4

**Evidence:** Architecture says Markdown is the only durable workflow state and runtime signals are control-plane only (`architecture.md:567-574`). Story 1.4 says not to use hidden runtime memory, `progress.md`, or background `status.json` as sufficient task-list state (`.pi/skills/bmad-orchestrator/SKILL.md:71-73`). `pi-subagents` async status uses `status.json` to power widgets/status (`README.md:883-893`) and renderer uses runtime statuses such as `running`, `queued`, `complete`, and `paused` (`render.ts:279-319`).

**Failure mode:** The task/todo UI displays `status.json` or `progress.md` as the workflow task list, marks `complete` as durable `completed` without parent validation, or shows a stale async job as active after the Markdown task moved to `completed`, `blocked`, or `failed`.

**Missing guardrail:** Story 1.5 should require UI to be a read-only projection of the Story 1.4 Markdown task list. Runtime status may annotate live activity, but must not replace or mutate durable task truth.

**Tests to require:**
- A provider-free task-list projection test with a sample Markdown task list containing all five Story 1.4 statuses; assert UI output displays only the builder-facing vocabulary and maps runtime `running/complete/paused/detached` only as annotations.
- A stale-state test: completed/blocked/failed tasks are not shown as active even if a mocked async job is still `running`.
- A missing/invalid task-list test: renderer returns a safe degraded message and does not report workflow success.
- A test that `progress.md` and async `status.json` are not accepted as the durable task-list source.

### Risk 3 — Role labels/layout are underspecified and may be hardcoded incorrectly

**Evidence:** Story 1.5 requires configured role labels and hidden/inactive layout rules (`epics.md:521-524`). Current project agents have custom `roleLabel` frontmatter (`.pi/agents/implementer.md:1-10`, `.pi/agents/reviewer-a.md:1-10`, `.pi/agents/reviewer-b.md:1-10`), but the `pi-subagents` README's documented frontmatter fields do not include `roleLabel` (`README.md:408-456`).

**Failure mode:** UI shows raw agent ids only, ignores the existing `roleLabel` metadata, or hardcodes labels for `implementer/reviewer-a/reviewer-b` so future agents fail.

**Missing guardrail:** Story 1.5 should define the supported role-label source and layout config source. If using `roleLabel`, implementation must explicitly parse it as project-specific UI metadata without assuming upstream `pi-subagents` natively supports it.

**Tests to require:**
- Parse `.pi/agents/*.md` frontmatter and assert visible rows show `BMAD Implementer`, `BMAD Reviewer A`, and `BMAD Reviewer B`, not only raw ids.
- Add a fixture agent without `roleLabel`; assert deterministic fallback to name/description and no render crash.
- If a visibility/layout config is introduced, test hidden agents are omitted or dimmed according to config and inactive agents do not appear active.

### Risk 4 — Activity titles can be confused with task summaries and lose Story 1.4 identity

**Evidence:** Story 1.5 requires activity titles that identify running agent and task, especially across parallel terminal sessions (`epics.md:526-534`). `pi-subagents` currently shows model/task summary in result/widget rows (`render.ts:845-861`, `render.ts:930-951`), and `README.md:723-725` describes chain/parallel output handoffs, but Story 1.4 task identity lives in durable fields such as `taskId`, `title`, `targetAgent`, and `activeAgentId` (`.pi/skills/bmad-orchestrator/SKILL.md:75-99`, `SKILL.md:113-116`).

**Failure mode:** Multiple parallel sessions show indistinguishable summaries like "thinking…" or summaries derived from raw prompt text instead of durable task titles; the UI cannot identify which Story 1.4 task is active.

**Missing guardrail:** Activity title must be derived from durable task state first: at minimum `{activeAgentId or targetAgent} · {taskId} · {title}`. Runtime task summaries can be secondary.

**Tests to require:**
- Pure helper test for title formatting: given taskId/title/targetAgent/activeAgentId, output contains agent + taskId + title, is truncated safely, and strips injected read/write/progress noise.
- Parallel uniqueness test: two same-agent tasks with different `taskId`/title produce distinguishable titles.
- Fallback test: if durable task title is missing/malformed, UI shows degraded/unknown task rather than inventing success.

### Risk 5 — Direct edits to generated `pi-subagents` files will be lost

**Evidence:** Project pins `npm:pi-subagents@0.24.2` in `.pi/settings.json:1-4`; installed package metadata is version `0.24.2` (`.pi/npm/node_modules/pi-subagents/package.json:1-4`). Story 1.4 records that `.pi/npm/` is generated/ignored and package source changes must be captured in `.pi/patches/` (`1-4...md:146-154`, `1-4...md:218-221`). Existing tests enforce patch durability for the prior renderer changes (`tests/test_subagent_model_task_summary.py:169-222`). `git status --ignored` shows `.pi/npm/node_modules/` is ignored.

**Failure mode:** Developers edit `.pi/npm/node_modules/pi-subagents/src/tui/render.ts` or README directly for Story 1.5; the change passes locally but disappears after reinstall/bootstrap because no patch captures it.

**Missing guardrail:** Story 1.5 must require one of these paths:
1. No package source change; use guidance/tests only.
2. If package code changes, create a version-scoped patch under `.pi/patches/` and update patch durability tests.
3. If creating a framework-owned extension instead, keep code under `.pi/extensions/<name>/` with local validation scripts.

**Tests to require:**
- If `.pi/npm/node_modules/pi-subagents/src/**` changes, assert a new `.pi/patches/pi-subagents-0.24.2-*-ui-visibility.patch` exists and includes all changed package files.
- Update patch tests to run `.pi/install-packages.sh` and assert the new patch is applied or already applied.
- Add a drift test that fails if modified generated package files are not represented in a patch.

### Risk 6 — UI rendering could accidentally become a workflow success signal

**Evidence:** Story 1.5 explicitly says workflow execution is not successful solely because UI rendering succeeded (`epics.md:541-544`). Story 1.4 says parent validation decides durable state changes and dependent routing (`.pi/skills/bmad-orchestrator/SKILL.md:115-118`, `SKILL.md:244-254`).

**Failure mode:** A UI component catches an error, renders a green checkmark/"Done", and the orchestrator or operator treats that as task completion without Markdown state moving to `completed` after parent validation.

**Missing guardrail:** UI success must mean "projection rendered", not "workflow succeeded". Completion indicators must be driven by durable `completed` state only.

**Tests to require:**
- Render-success-vs-workflow-success test: mocked renderer returns a component for missing/invalid task state but output includes degraded/error wording and no completed/checkmark state.
- Test that `completed` display is impossible unless the parsed durable task status is exactly `completed`.

### Risk 7 — New UI config may depend on project docs and fail when scaffold is copied

**Evidence:** Framework-owned `.pi/` assets are installable/copiable and must not depend on project `docs/` (`architecture.md:820-822`), while implementation artifacts under `docs/_bmad-output/...` are workflow execution state (`architecture.md:824-827`).

**Failure mode:** Story 1.5 puts UI configuration or reusable renderer logic in `docs/_bmad-output/...`, making bootstrap installs lose UI behavior or depend on this repository's implementation artifacts.

**Missing guardrail:** Reusable UI contract/config belongs under `.pi/` (settings, skill guidance, optional extension). Story-specific evidence stays under `docs/_bmad-output/...` only.

**Tests to require:**
- Test that reusable UI config/contract files live under `.pi/`, not under `docs/_bmad-output`.
- Test no `.pi/` framework file hardcodes this repo's `docs/_bmad-output/implementation-artifacts/1-5...` path.

## Minimum Story 1.5 test set to require

1. `tests/test_pi_ui_visibility_contract.py` provider-free checks for: no separate frontend, no custom dispatch tool, no dispatchable orchestrator child, no child `subagent` grants, and explicit Pi TUI/`pi-subagents` reuse guidance.
2. `tests/test_pi_ui_task_state_projection.py` with fixture Markdown task lists covering `pending`, `in-progress`, `completed`, `blocked`, `failed`, stale runtime jobs, missing artifacts, invalid statuses, and degraded rendering.
3. Role-label/layout tests that parse `.pi/agents/*.md` and assert configured labels and hidden/inactive behavior.
4. Activity-title helper tests for agent/task distinguishability, truncation, and fallback/degraded states.
5. Patch durability tests if any `.pi/npm/node_modules/pi-subagents/**` file changes.
6. Existing full validation remains required: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`, `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanup check, and root review-artifact cleanliness check, matching Story 1.4 validation expectations (`1-4...md:254-264`).

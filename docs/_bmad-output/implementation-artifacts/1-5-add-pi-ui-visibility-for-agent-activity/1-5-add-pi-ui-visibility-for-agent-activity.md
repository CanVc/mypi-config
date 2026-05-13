# Story 1.5: Add Pi UI Visibility for Agent Activity

Status: review

<!-- Ultimate context engine analysis completed - comprehensive developer guide created. -->

## Story

As a builder,
I want Pi UI visibility into active sub-agents, role labels, activity titles, and task progress,
so that I can confirm the multi-agent runtime is doing the expected work.

## Acceptance Criteria

1. Given a team run is active, when the Pi UI renders the team view, then visible sub-agents display their configured role labels, and hidden or inactive agents follow the configured layout rules.
2. Given a sub-agent is dispatched, when it begins work, then the UI identifies which sub-agent is currently active, and the displayed activity title describes the current task.
3. Given multiple terminal sessions are running in parallel, when the builder views the terminal UI, then each session has a descriptive activity title, and the title makes the running agent and task distinguishable.
4. Given the orchestrator task list changes, when tasks move from pending to in-progress or completed, then the Pi UI task/todo list reflects the current state, and stale task states are not shown as active.
5. Given UI rendering cannot access required runtime state, when the team view is displayed, then it shows a safe degraded message, and workflow execution is not treated as successful solely because UI rendering succeeded.

## Tasks / Subtasks

- [x] Define the v1 Pi UI visibility contract and boundaries. (AC: 1-5)
  - [x] Document in `.pi/skills/bmad-orchestrator/SKILL.md` how parent BMAD workflows expose UI-visible agent labels, activity titles, terminal/session titles, and task-list artifacts.
  - [x] State explicitly that Pi TUI / `pi-subagents` surfaces are the UI; do not add a web dashboard, daemon, database, sidecar service, or separate frontend.
  - [x] State that UI rendering is a read-only projection of durable Markdown task state plus runtime annotations; it must never mark workflow success or override artifact truth.
  - [x] Keep Story 1.4 fixed task status vocabulary as the only builder-facing workflow task status vocabulary: `pending`, `in-progress`, `completed`, `blocked`, `failed`.
- [x] Add configured role-label and layout support. (AC: 1)
  - [x] Use configured role labels from project agent frontmatter, starting with existing `.pi/agents/*.md` `roleLabel` values.
  - [x] Add a deterministic fallback when `roleLabel` is missing: use agent display/name metadata without crashing.
  - [x] Define minimal v1 layout rules for visible, hidden, inactive, active, completed, blocked, and failed agents.
  - [x] Do not hardcode labels only for `implementer`, `reviewer-a`, or `reviewer-b`; keep behavior generic for future agents.
- [x] Add active-agent and task activity titles. (AC: 2, 3)
  - [x] Derive the primary activity title from durable task state first: `{activeAgentId or targetAgent} · {taskId} · {title}`.
  - [x] Use runtime `taskSummary`, current tool/current operation, current path, model name, token count, and elapsed duration as secondary annotations only.
  - [x] Ensure two parallel same-agent tasks remain distinguishable by task id/title.
  - [x] Use Pi `ctx.ui.setTitle(...)` or an equivalent Pi-supported terminal-title mechanism where available; clear or restore titles on completion, failure, session shutdown, and reload to avoid stale terminal titles.
- [x] Project the durable orchestrator task list into Pi UI. (AC: 4, 5)
  - [x] Read the Story 1.4 task-list source from the current story/spec/run Markdown artifact, not from hidden runtime memory, `progress.md`, or async `status.json` alone.
  - [x] Display task rows with status, role label/agent, task id, title, and safe runtime annotations when available.
  - [x] Prevent stale states: `completed`, `blocked`, and `failed` durable tasks must not render as active even if a runtime job still reports `running`.
  - [x] On missing/unreadable/malformed task-list artifact or invalid task status, show a degraded warning state and do not show success/completion.
- [x] Centralize durable-vs-runtime UI arbitration and apply it to every active/status/title surface. (AC: 2-5)
  - [x] Implement or refactor to a shared helper/policy that computes effective UI activity from durable task state plus runtime telemetry before any surface shows active/running state.
  - [x] Apply the shared policy to foreground terminal title lifecycle so durable `completed`, `blocked`, or `failed` tasks clear/degrade rather than show normal active activity.
  - [x] Apply the shared policy to async `subagent({ action: "status" })` list/detail output so durable-terminal work is not listed as active and missing/unreadable/malformed task state shows degraded warning.
  - [x] Add provider-free contract tests proving every active/status/title surface uses durable-terminal gating and missing-task-state degradation.
- [x] Integrate with existing `pi-subagents` TUI/status surfaces without duplicating dispatch. (AC: 1-5)
  - [x] Prefer extending existing `pi-subagents` foreground result rendering, async widget, status output, and task/model summary pipeline.
  - [x] Preserve existing foreground/async observability for chains and parallel groups: per-agent rows, model tags, task summaries, token counts, elapsed duration, live current tool/current operation/path, paused/failed visibility, and compact expanded views.
  - [x] Do not add a custom `dispatch_subagent` tool, role-specific sub-agent launcher, dispatchable `orchestrator` child agent, or nested orchestration ability for child agents.
  - [x] Preserve formal BMAD dispatch policy: explicit `context: "fresh"`, no `context: "fork"`, no `subagent({ action: "resume" })` for active v1 formal paths.
- [x] Make any package/runtime changes durable. (AC: 1-5)
  - [x] If no `pi-subagents` source change is required, state this explicitly in completion notes.
  - [x] If any `.pi/npm/node_modules/pi-subagents/src/**` file changes, create `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch` or similarly named version-scoped patch containing every package-source change.
  - [x] Update package patch durability tests so `.pi/install-packages.sh` applies or reports the Story 1.5 patch already applied.
  - [x] Do not leave direct generated-package edits uncaptured by a durable patch.
- [x] Add provider-free regression tests. (AC: 1-5)
  - [x] Add `tests/test_pi_ui_visibility_agent_activity.py` or equivalent.
  - [x] Test no separate frontend/dashboard/server is introduced for this story.
  - [x] Test role-label extraction and fallback behavior using `.pi/agents/*.md` fixtures.
  - [x] Test activity-title formatting, truncation, injected-noise stripping, and parallel task distinguishability.
  - [x] Test that the UI preserves the useful existing sub-agent widget facts: model name, assigned task/task summary, token count, elapsed duration, and current tool/current operation.
  - [x] Test task-list projection with all five durable statuses and with runtime `running`, `complete`, `paused`, and `detached` annotations.
  - [x] Test stale-state prevention: durable `completed`/`blocked`/`failed` cannot render as active.
  - [x] Test missing/unreadable/malformed task state renders a degraded warning and never a success/completed signal.
  - [x] Test no `dispatch_subagent`, no dispatchable orchestrator child agent, and no `subagent` tool grant to project child agents.
- [x] Run final validation and artifact-cleanliness checks. (AC: 1-5)
  - [x] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [x] Run `PI_TELEMETRY=0 pi list`.
  - [x] Run `git diff --check`.
  - [x] Run `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` and remove generated bytecode if any appears.
  - [x] Run `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` and confirm no story-specific review artifacts are at the implementation-artifacts root.

### Review Follow-ups (AI)

- [x] [AI-Review][R1][HIGH][AC1] Load and use configured role labels for inactive/pending/completed/blocked/failed durable tasks.
- [x] [AI-Review][R1][HIGH][AC2, AC3] Carry durable task identity through runtime progress/status/results so parallel same-agent activity titles map to the correct task.
- [x] [AI-Review][R1][MEDIUM][AC5] Render degraded BMAD UI when a BMAD/team view is expected but `taskStatePath` is missing.
- [x] [AI-Review][R1][MEDIUM][AC5] Treat durable task records missing required `contextSource` as malformed/degraded, not completed/successful.
- [x] [AI-Review][R2][HIGH][AC2, AC3] Preserve `taskStatePath` and durable task identity for foreground single-run terminal titles; use `durableTaskId` as fallback task id when durable state is unavailable.
- [x] [AI-Review][R2][HIGH][AC4] Gate BMAD runtime widget row glyphs/status labels through durable status so completed/blocked/failed tasks never render active despite runtime `running`.
- [x] [AI-Review][R2][HIGH][AC2, AC3] Use async job-level `durableTaskIds` when building activity titles before per-step records exist.
- [x] [AI-Review][R2][MEDIUM][AC5] Treat non-empty async `durableTaskIds` as BMAD projection evidence and render degraded UI when `taskStatePath` is missing.
- [x] [AI-Review][R3][HIGH][Package durability] Regenerate or adjust Story 1.5 patch so clean install patch application is durable and does not duplicate already-applied `agents.ts` hunks from prior patches.
- [x] [AI-Review][R3][HIGH][AC2, AC3] Add foreground terminal title lifecycle for foreground subagent progress/results using durable task title, with cleanup on terminal states.
- [x] [AI-Review][R3][HIGH][AC2, AC3, AC4] Gate async terminal title selection through durable status so terminal durable tasks clear/restore title instead of showing stale runtime activity.
- [x] [AI-Review][R4][HIGH][AC4] Gate async multi-job active bucketing and header state through durable terminal status so completed/blocked/failed work cannot make the widget active.
- [x] [AI-Review][R4][MEDIUM][AC5] When async jobs have durable task IDs but no readable `taskStatePath`, clear or show degraded terminal title instead of normal runtime activity.
- [x] [AI-Review][R5][HIGH][AC3, AC4] Gate foreground terminal title ownership through durable terminal status so completed/blocked/failed tasks do not show normal active activity.
- [x] [AI-Review][R5][MEDIUM][AC4, AC5] Apply durable-status gating/degraded warnings to async `subagent({ action: "status" })` list and detail output.
- [ ] [AI-Review][TARGETED][HIGH][AC3, AC4] Foreground title arbitration must fail closed when same-agent durable-terminal work exists without a matched in-progress durable task or durableTaskId.
- [ ] [AI-Review][TARGETED][HIGH][AC4] Async widget row stats/activity must use effective durable arbitration and not show running counts or thinking/live prompts for durable-terminal jobs.
- [ ] [AI-Review][TARGETED][MEDIUM][AC4, AC5] Renderer/widget helpers must fail closed when durableTaskId is present but unmatched, avoiding same-agent fallback and rendering degraded/warning state.

## Dev Notes

### Source of Truth

Story 1.5 is the Epic 1 UI-observability layer. Epic 1 must establish an observable multi-agent runtime before bootstrap and standard story-to-done workflows. Story 1.5 specifically makes active agents, role labels, activity titles, terminal titles, and task progress visible in Pi UI; it does not prove the full two-agent smoke scenario, which belongs to Story 1.6. [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-5-Add-Pi-UI-Visibility-for-Agent-Activity]

Relevant requirements and constraints:

- FR18: the builder can configure Pi UI layout/display per agent team, including visible agents and role labels. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- FR19: the builder can observe in Pi UI which sub-agent is currently active and what it is doing. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- FR24: running workflow sessions can have descriptive activity titles visible in terminal UI. [Source: docs/_bmad-output/planning-artifacts/epics.md#Requirements-Inventory]
- FR25: the builder can view a task/todo list tracking pending, in-progress, and completed tasks. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- Pi TUI is the operator interface; any additional workflow UI belongs in Pi package UI features or optional Pi extension widgets/status lines/overlays. No separate UI/web frontend is required. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Frontend-Architecture]
- Markdown artifacts are the durable workflow state. Runtime signals are control-plane only and must not override artifact truth. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]

### Required Central Runtime/Durable Arbitration

Story 1.5 now explicitly requires a shared arbitration policy for all Pi UI/status/title projections that combine runtime telemetry with BMAD durable task state. This requirement was clarified after R1-R5 reviews showed that local per-surface fixes repeatedly missed another active/status/title path.

The implementation must compute effective UI state from:

- durable task records read from `taskStatePath`;
- runtime status/progress/job/step telemetry from `pi-subagents`;
- durable task identity such as `durableTaskId`/`durableTaskIds` when present.

Rules:

- Durable task status is authoritative for builder-facing activity.
- If a matched durable task is `completed`, `blocked`, or `failed`, runtime `running`/`queued` must not render as active in any BMAD-aware surface.
- If runtime telemetry includes durable task ids but `taskStatePath` is missing, unreadable, or malformed, show degraded state or clear/restore terminal title; do not show normal active BMAD activity.
- Runtime status may appear only as a secondary annotation after durable status has been applied.
- The rule must be shared or centrally testable rather than reimplemented inconsistently per renderer.

The arbitration policy must cover at least:

- foreground terminal title lifecycle;
- foreground result/progress rendering;
- async widget rows;
- async multi-job header/bucketing;
- async terminal title selection;
- `subagent({ action: "status" })` list/detail output.

### Story Boundary

Implement only UI visibility for the existing multi-agent runtime.

In scope:

- Configured role labels and minimal v1 visibility/layout rules.
- Active agent and activity title display for foreground and background sub-agent work.
- Terminal/session title updates that make concurrent sessions distinguishable.
- Pi UI task/todo projection from durable Story 1.4 task-state Markdown.
- Safe degraded UI when required runtime or artifact state cannot be read.
- Provider-free tests for the visibility contract.

Out of scope:

- Story 1.6 two-agent smoke execution proof.
- Epic 3 standard BMAD story-to-done orchestration, tests/lint/review gates, or iteration-cap enforcement beyond preserving existing contracts.
- Epic 4 TDD/ATDD/TDAD batch UI or full artifact-status schema.
- A web dashboard, server, database, daemon, or non-Pi frontend.
- A new role-specific dispatch tool, `dispatch_subagent`, or custom `.pi/extensions/bmad-orchestrator/` dispatch runtime.
- Child-agent access to the `subagent` tool or nested orchestration.

### Current Runtime and UI Facts

- Project package pin: `.pi/settings.json` declares `npm:pi-subagents@0.24.2`. [Source: .pi/settings.json]
- Installed `pi-subagents` metadata reports version `0.24.2`; package peer dev references point at Pi `0.74.0`, while planning docs retain Pi `>=0.67.2` as product compatibility baseline. Treat local package metadata as current implementation detail and planning docs as compatibility requirements. [Source: .pi/npm/node_modules/pi-subagents/package.json] [Source: docs/_bmad-output/planning-artifacts/prd.md#Prerequisites]
- `pi-subagents` already displays foreground run progress, background async widget rows, per-agent progress for parallel background runs, chain/parallel group shape, task summaries, model tags, token counts, elapsed duration, current tool/current operation/path, paused/failed states, and `subagent({ action: "status" })` output. [Source: .pi/npm/node_modules/pi-subagents/README.md#Where-running-subagents-show-up] [Source: .pi/npm/node_modules/pi-subagents/src/tui/render.ts]
- The current patched renderer shows raw agent names plus model/task summary/activity; it does not yet expose configured `roleLabel`, durable Story 1.4 task id/title, or terminal activity titles. [Source: .pi/npm/node_modules/pi-subagents/src/tui/render.ts]
- `AgentProgress`, `SingleResult`, `AsyncStatus.steps`, and `AsyncJobState` carry agent/status/taskSummary/model/activity fields; they do not currently carry role label or durable task-list linkage. [Source: .pi/npm/node_modules/pi-subagents/src/shared/types.ts]
- Background async widgets are driven by `status.json` and `events.jsonl` polling in `async-job-tracker.ts`; these are runtime visibility sources only, not durable BMAD task truth. [Source: .pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts]
- Project agent files already contain configured role labels: `BMAD Implementer`, `BMAD Reviewer A`, and `BMAD Reviewer B`. [Source: .pi/agents/implementer.md] [Source: .pi/agents/reviewer-a.md] [Source: .pi/agents/reviewer-b.md]
- `pi-subagents` agent parsing preserves unknown frontmatter fields in `extraFields`; this can be used to propagate `roleLabel` generically instead of hardcoding labels. [Source: .pi/npm/node_modules/pi-subagents/src/agents/agents.ts]

### Pi UI API Guardrails

Use documented Pi UI primitives; do not invent unsupported UI APIs.

- `ctx.ui.setStatus(key, text)` displays persistent footer status; clear with `undefined`. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Widgets-Status-and-Footer]
- `ctx.ui.setWidget(key, linesOrComponent, { placement })` displays persistent content above or below the editor; good for task/progress widgets. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Widgets-Status-and-Footer]
- `ctx.ui.setTitle("...")` sets the terminal title. Use it for agent/task-distinguishable terminal activity titles and restore/clear it on completion, shutdown, or reload. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Widgets-Status-and-Footer]
- Custom components must implement `render(width)`, optional `handleInput(data)`, and `invalidate()`. Each rendered line must not exceed `width`; use truncation/wrapping helpers. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md#Component-Interface] [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md#Line-Width]
- In non-interactive/JSON/print modes, UI methods may be no-ops or unavailable; check `ctx.hasUI` before UI-only work and preserve workflow behavior. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Mode-Behavior]
- Existing examples show the intended patterns: `model-status.ts` for `setStatus`, `widget-placement.ts` for `setWidget`, `custom-footer.ts` for footer/status composition, and `session-name.ts` for session naming. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/model-status.ts] [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/widget-placement.ts]

### Relationship to Story 1.4 Task State

Story 1.4 created the durable task routing/task-list contract. Story 1.5 must render that contract; it must not replace it.

Required task record fields from Story 1.4: `taskId`, `title`, `targetAgent`, `status`, `contextSource`; optional fields include `dependsOn`, `activeAgentId`, `outputArtifact`, `cause`, `recommendedNextAction`, and `routingDecision`. [Source: .pi/skills/bmad-orchestrator/SKILL.md#Task-Routing-and-Task-List-State]

UI interpretation rules:

- Durable status source: the current story/spec/run Markdown artifact selected by the active workflow.
- Runtime source: `pi-subagents` progress/status can annotate live behavior only.
- A task is active only when durable status is `in-progress` and runtime evidence does not contradict safety.
- A task with durable `completed`, `blocked`, or `failed` must never show as active, even if a runtime job still reports `running`.
- `complete`, `completed`, `running`, `queued`, `paused`, `detached`, and `failed` from runtime must be mapped/annotated; they are not the durable builder-facing task vocabulary by themselves.
- Missing/unreadable/malformed durable task state renders a degraded warning and must not display success.

### Recommended UI Data Model

Keep fields optional and backward compatible:

```ts
interface UiAgentDisplay {
  agent: string;
  roleLabel?: string;      // from agent frontmatter extraFields.roleLabel or fallback
  visible?: boolean;       // default true for active/current known workflow agents
  layoutGroup?: string;    // optional future grouping; do not require for v1
}

interface UiTaskDisplay {
  taskId: string;
  title: string;
  targetAgent: string;
  activeAgentId?: string | null;
  durableStatus: "pending" | "in-progress" | "completed" | "blocked" | "failed";
  activityTitle: string;   // e.g. "BMAD Implementer · dev-R1 · Implement or resume story"
  runtimeStatus?: string;  // annotation only
  model?: string;
  taskSummary?: string;
  tokenCount?: number;
  elapsedMs?: number;
  currentTool?: string;
  currentPath?: string;
  degradedReason?: string;
}
```

Activity-title priority:

1. Durable task state: `{roleLabel or activeAgentId or targetAgent} · {taskId} · {title}`.
2. Runtime secondary annotation: task summary/current tool/current path/model/tokens/elapsed time.
3. Degraded fallback: `{agent or unknown-agent} · unknown-task · degraded: <reason>`.

### Recommended v1 Visual Shape

The exact styling may follow the existing `pi-subagents` compact widget, but the information hierarchy should be clear and testable:

```text
● BMAD Dev Cycle · Story 1.5 · task state: active
├─ ● BMAD Implementer (openai/gpt-5.5) · in-progress · dev-R1
│  ⎿ Implement or resume story via dev-story workflow
│  ⎿ running · edit .pi/.../render.ts · 12.4k token · 03:12
├─ ◦ BMAD Reviewer A (openai/gpt-5.5) · pending · review-a-R1
│  ⎿ waits for dev-R1
└─ ✓ BMAD Reviewer B (openai/gpt-5.5) · completed · review-b-R1
   ⎿ output: docs/.../review-...-reviewer-b-output.md
```

Terminal/session title while an agent is active:

```text
BMAD Implementer · dev-R1 · Implement or resume story
```

Degraded state example:

```text
⚠ BMAD task state unavailable
⎿ Runtime subagent telemetry may still be visible, but workflow success is not inferred.
⎿ Required action: restore/read the story task-state artifact.
```

Visual rules:

- Primary row: role label, model, durable task status, task id.
- First detail row: durable BMAD task title.
- Second/detail runtime row: runtime status, current operation/tool, path when available, token count, elapsed duration.
- `completed`, `blocked`, and `failed` durable tasks must not use the active glyph/color even if runtime telemetry still says `running`.
- Degraded UI uses warning styling and must not show a green check/completed signal unless durable BMAD status is exactly `completed`.

### Existing Implementation Patterns to Preserve

- `.pi/skills/bmad-orchestrator/SKILL.md` is parent-session guidance, not a child-agent definition. Do not add `.pi/agents/orchestrator.md` or `.pi/agents/bmad-orchestrator.md`. [Source: .pi/skills/bmad-orchestrator/SKILL.md#Parent-and-Child-Boundaries]
- Formal BMAD dispatches must pass `context: "fresh"` explicitly and must block omitted context, `context: "fork"`, and `action: "resume"`. [Source: .pi/skills/bmad-orchestrator/SKILL.md#Session-Policy]
- Project child agents `implementer`, `reviewer-a`, and `reviewer-b` do not have the `subagent` tool and must not receive it. [Source: .pi/agents/implementer.md] [Source: .pi/agents/reviewer-a.md] [Source: .pi/agents/reviewer-b.md]
- Provider-free tests use Python `unittest` with source assertions and, where needed, lightweight `npx --yes tsx` helper checks. Follow this style. [Source: tests/test_orchestrator_task_routing_state.py] [Source: tests/test_subagent_model_task_summary.py]
- `.pi/npm/` is generated/ignored. Any durable `pi-subagents` source change must be represented as a version-scoped patch under `.pi/patches/` and validated via `.pi/install-packages.sh`. [Source: tests/test_subagent_model_task_summary.py#TestPatchDurability]

### Likely Files to Modify

Expected primary files if extending existing `pi-subagents` UI surfaces:

```text
.pi/skills/bmad-orchestrator/SKILL.md
.pi/npm/node_modules/pi-subagents/src/shared/types.ts
.pi/npm/node_modules/pi-subagents/src/agents/agents.ts
.pi/npm/node_modules/pi-subagents/src/runs/shared/parallel-utils.ts
.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts
.pi/npm/node_modules/pi-subagents/src/runs/foreground/chain-execution.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/async-execution.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts
.pi/npm/node_modules/pi-subagents/src/tui/render.ts
.pi/npm/node_modules/pi-subagents/src/extension/index.ts
.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch
tests/test_pi_ui_visibility_agent_activity.py
tests/test_subagent_model_task_summary.py  # only if patch durability expectations change
```

Possible if the implementation needs a project-local Pi extension instead of package changes:

```text
.pi/extensions/bmad-ui-visibility/index.ts
.pi/extensions/bmad-ui-visibility/package.json
.pi/extensions/bmad-ui-visibility/tests/...
scripts/validate-extensions.sh
```

Use the extension path only if it is narrower/cleaner than patching `pi-subagents`. If a framework-owned TypeScript extension is introduced, it must have extension-local `typecheck`, `lint`, `test`, and `validate` scripts per architecture. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Extension-Validation-Contract]

### Anti-Disaster Guardrails

- Do not treat widget/status rendering as a workflow gate. UI success means “projection rendered,” not “workflow succeeded.”
- Do not mark tasks done from runtime `complete` alone. Parent validation and durable Markdown `completed` are required.
- Do not show stale active state for tasks whose durable status is `completed`, `blocked`, or `failed`.
- Do not read task truth from `progress.md` or async `status.json` alone.
- Do not hardcode BMAD-specific labels into generic package rendering; use parsed agent metadata or explicit workflow-provided metadata.
- Do not let missing UI state crash a workflow. Render degraded state and leave workflow correctness to artifacts.
- Do not create a separate UI technology stack.
- Do not edit generated package code without a patch.
- Do not make `.pi/` framework files depend on this story folder or other repository-specific `docs/_bmad-output` paths.

### Previous Story Intelligence

#### Story 1.1 — Generic Sub-Agent Dispatch

- Use marketplace `pi-subagents`; do not build a custom dispatch extension or `dispatch_subagent` tool. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md]
- Parent owns orchestration; child agents must not communicate horizontally or launch nested sub-agents. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md]

#### Story 1.2 — Agent Definitions and Model Routing

- Canonical dispatchable project agents live under `.pi/agents/`; workflow skills under `.pi/skills/` must not become child agents. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md]
- Runtime output/model routing evidence should record effective agent/model without requiring custom source changes for every model assignment. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md]

#### Story 1.2.1 — Story-Scoped Implementation Artifacts

- New story artifacts must live under `{implementation_artifacts}/{story_key}/{story_key}.md`; legacy flat story paths are read-only fallback compatibility. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md]
- Story-specific review outputs belong inside the story folder; root-level `sprint-status.yaml` and `deferred-work.md` may remain global. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md]

#### Story 1.2.2 — Subagent Model and Task Summary

- Existing UI patching pattern adds `taskSummary`/model through types, execution paths, renderer, async status, run status, and a version-scoped `.pi/patches/pi-subagents-0.24.2-display-model-task-summary.patch`. Reuse this durability pattern if Story 1.5 changes package code. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md] [Source: tests/test_subagent_model_task_summary.py]

#### Story 1.3 — Fresh-Context Session Policy

- Active v1 reuse/resume exception set is none for standard BMAD story/review dispatches. Story 1.5 must not weaken this while adding UI. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md]
- Direct quick-dev/code-review sub-agent paths can bypass central policy if not explicitly tested. Add Story 1.5 tests for direct UI/status paths as well as central renderer logic. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md]

#### Story 1.4 — Orchestrator Task Routing and Task List State

- The task-list contract already requires durable Markdown task records before dispatch, `in-progress` updates with `activeAgentId`, `completed` only after parent validation, and `blocked`/`failed` with `cause` and `recommendedNextAction`. Story 1.5 must render these states, not redefine them. [Source: docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/1-4-add-orchestrator-task-routing-and-task-list-state.md]
- Review follow-ups for Story 1.4 found direct dispatch/fallback paths could bypass task-state updates. Story 1.5 must include tests for active workflow UI/task-state integration so direct paths cannot display false success. [Source: docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/1-4-add-orchestrator-task-routing-and-task-list-state.md#Senior-Developer-Review-AI]

### Recent Git Intelligence

Recent commits show the project is hardening guidance and provider-free tests rather than adding broad runtime rewrites:

- `fc96a27 /bmad-dev-cycle skill created ; dev and reviewer agents model modified.` — introduced a parent BMAD dev-cycle workflow that writes durable task state and dispatches `implementer`, `reviewer-a`, and `reviewer-b` with explicit fresh context.
- `945b0c7 Story 1-4 done Sliught adjustements to dev and review workflows.` — integrated task-state contract into active code-review/quick-dev paths and added `tests/test_orchestrator_task_routing_state.py`.
- `161f7bd Story 1-4 created` — story artifact creation and sprint-status update pattern.
- `f450cd6 Enforce BMAD fresh context session policy` — central session policy and tests.
- `23d3a29 Story 1-3 created dev-cycle prompt created` — earlier workflow artifact pattern.

Actionable implications:

- Preserve the Story 1.4 task-state section and the new `.pi/skills/bmad-dev-cycle/workflow.md` durable task workflow.
- Add tests before or with guidance/runtime changes.
- If patching `pi-subagents`, update patch durability tests in the established style.
- Keep generated/story-specific artifacts inside the story folder.

### Latest Technical Information

No external web lookup was available in this session. Local/current technical facts are:

- Pi docs describe `ctx.ui.setStatus`, `ctx.ui.setWidget`, `ctx.ui.setTitle`, custom components, overlays, and footer APIs as current extension UI surfaces. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md] [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md]
- Pi README states there are no built-in to-dos; use a TODO.md file or build with extensions. For this story, that means the task/todo view must be a Pi widget/status projection of durable BMAD task Markdown, not an assumed built-in todo API. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/README.md#Philosophy]
- `pi-subagents@0.24.2` already includes async widgets and foreground result renderers; Story 1.5 should enhance those rather than duplicate them. [Source: .pi/npm/node_modules/pi-subagents/README.md#Where-running-subagents-show-up]

### Testing Requirements

Minimum validation expected before marking implementation complete:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PI_TELEMETRY=0 pi list
git diff --check
find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print
find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print
```

If any `pi-subagents` package source is changed, also run:

```bash
bash .pi/install-packages.sh --patch
# or the current project-supported .pi/install-packages.sh invocation that applies patches
```

Provider-free tests should assert observable source behavior and fixture rendering; do not require live model calls.

## Project Structure Notes

- Story artifact location: `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md`.
- Do not write `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity.md`; that legacy flat path is read-only fallback compatibility only.
- Analysis artifacts created during story preparation are in this story folder:
  - `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/scout-analysis.md`
  - `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/reviewer-risk-analysis.md`
- Framework-owned runtime assets remain under `.pi/`.
- Global implementation-artifact files that may remain at root: `sprint-status.yaml`, `deferred-work.md`.
- Reusable UI contracts/config must live under `.pi/`; story-specific evidence may live under this story folder.

### References

- [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-5-Add-Pi-UI-Visibility-for-Agent-Activity]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Frontend-Architecture]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]
- [Source: .pi/skills/bmad-orchestrator/SKILL.md#Task-Routing-and-Task-List-State]
- [Source: .pi/npm/node_modules/pi-subagents/README.md#Where-running-subagents-show-up]
- [Source: .pi/npm/node_modules/pi-subagents/src/tui/render.ts]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md]

## Dev Agent Record

### Agent Model Used

openai-codex/gpt-5.5

### Debug Log References

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (15 tests).
- `bash .pi/install-packages.sh --patch` — passed; Story 1.5 patch reported already applied and prior display patch reported superseded/already applied.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed (193 tests).
- `PI_TELEMETRY=0 pi list` — passed.
- `git diff --check` — passed.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.
- `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — no output.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — failed before test adjustment because direct `render.ts` import requires unavailable package exports; then passed after using source assertions/provider-free checks (17 tests).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed (195 tests).
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `bash .pi/install-packages.sh --patch` — passed; Story 1.5 patch reported already applied and prior display patch reported superseded/already applied.
- `PI_TELEMETRY=0 pi list` — passed.
- `git diff --check` — passed.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.
- `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — no output.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (19 tests).
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `rm -rf .pi/npm/node_modules/pi-subagents && bash .pi/install-packages.sh` — passed; clean package restore applied prior patches and Story 1.5 patch without duplicated `agents.ts` hunks.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed (197 tests).
- `PI_TELEMETRY=0 pi list` — passed.
- `git diff --check` — passed.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.
- `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — no output.
- `bash .pi/install-packages.sh --patch` — passed; all patches reported already applied after clean restore.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (21 tests).
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `rm -rf .pi/npm/node_modules/pi-subagents && bash .pi/install-packages.sh` — passed; clean package restore applied prior patches and regenerated Story 1.5 patch.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed (199 tests).
- `PI_TELEMETRY=0 pi list` — passed.
- `git diff --check` — passed.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.
- `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — no output.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests && PI_TELEMETRY=0 pi list && git diff --check && find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print && find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — passed (199 tests; find commands produced no output).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (23 tests) after targeted central-arbitration tests were added/updated.
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `bash .pi/install-packages.sh --patch` — passed; Story 1.5 patch reported already applied and prior display patch reported superseded/already applied.
- `rm -rf .pi/npm/node_modules/pi-subagents && bash .pi/install-packages.sh` — passed; clean package restore applied prior patches and regenerated Story 1.5 central-arbitration patch.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed (201 tests).
- `PI_TELEMETRY=0 pi list` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests && PI_TELEMETRY=0 pi list && git diff --check && find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print && find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — passed (201 tests; find commands produced no output).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (23 tests) after adding job-level async status durable-ID coverage.
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `rm -rf .pi/npm/node_modules/pi-subagents && bash .pi/install-packages.sh` — passed; clean package restore applied prior patches and the regenerated Story 1.5 patch with job-level async status arbitration.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests && PI_TELEMETRY=0 pi list && git diff --check && find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print && find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — passed (201 tests; find commands produced no output).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pi_ui_visibility_agent_activity` — passed (23 tests) after broadening central arbitration to suppress normal foreground titles for same-agent durable-terminal tasks even without per-progress durable IDs.
- `node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/tui/render.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts && node --experimental-strip-types --check .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts` — passed.
- `bash .pi/install-packages.sh --patch` — passed; all Story 1.5 central-arbitration patch changes reported already applied.
- `rm -rf .pi/npm/node_modules/pi-subagents && bash .pi/install-packages.sh` — passed; clean package restore applied prior patches and the regenerated Story 1.5 patch.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests && PI_TELEMETRY=0 pi list && git diff --check && find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print && find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` — passed (201 tests; find commands produced no output).

### Completion Notes List

- Defined the v1 Pi UI visibility contract in BMAD orchestrator guidance, including Pi TUI/`pi-subagents` as the UI boundary, read-only Markdown task truth, role labels, task-state vocabulary, degraded rendering, and terminal-title rules.
- Extended `pi-subagents` UI/status surfaces with generic `roleLabel` propagation/fallback, durable Markdown task-state parsing/projection, activity-title formatting, stale-active prevention for completed/blocked/failed durable tasks, and safe degraded warnings.
- Added `taskStatePath` support so BMAD parent workflows can expose the current story/spec/run Markdown artifact to the Pi UI without hidden runtime truth or duplicate dispatch.
- Added terminal-title updates for active foreground/background subagent activity and cleanup on completion, session shutdown, and extension reload.
- Captured all `pi-subagents` package-source changes in `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch`; updated patch application idempotency for the prior display patch after Story 1.5 superseding edits.
- Added provider-free regression coverage for UI contract boundaries, role-label fallback, activity-title formatting/noise stripping, durable task projection, stale-state prevention, degraded states, preserved widget facts, patch durability, and dispatch guardrails.
- ✅ Resolved review finding [HIGH]: Load and use configured role labels for inactive/pending/completed/blocked/failed durable tasks.
- ✅ Resolved review finding [HIGH]: Carry durable task identity through runtime progress/status/results so parallel same-agent activity titles map to the correct task.
- ✅ Resolved review finding [MEDIUM]: Render degraded BMAD UI when a BMAD/team view is expected but `taskStatePath` is missing.
- ✅ Resolved review finding [MEDIUM]: Treat durable task records missing required `contextSource` as malformed/degraded, not completed/successful.
- ✅ Resolved review finding [HIGH]: Preserve `taskStatePath` and durable task identity for foreground single-run terminal titles; `durableTaskId` is now used as the fallback activity-title task id when durable state is unavailable.
- ✅ Resolved review finding [HIGH]: Gate BMAD runtime widget row glyphs/status labels through durable status so completed/blocked/failed durable tasks do not render active despite runtime `running`.
- ✅ Resolved review finding [HIGH]: Use async job-level `durableTaskIds` when building activity titles before per-step records exist.
- ✅ Resolved review finding [MEDIUM]: Treat non-empty async `durableTaskIds` as BMAD projection evidence and render degraded UI when `taskStatePath` is missing.
- ✅ Resolved review finding [HIGH]: Regenerated the Story 1.5 patch relative to prior required patches so clean install applies durably without duplicating `src/agents/agents.ts` hunks.
- ✅ Resolved review finding [HIGH]: Added foreground terminal title lifecycle coverage for progress/result updates using durable task titles and cleanup on terminal states.
- ✅ Resolved review finding [HIGH]: Gated async terminal title selection through durable task status so terminal durable tasks clear/restore the title instead of showing stale runtime activity.
- ✅ Resolved review finding [HIGH]: Gated async multi-job active bucketing/header state through durable terminal status so terminal durable work is counted as finished rather than active.
- ✅ Resolved review finding [MEDIUM]: Cleared async terminal titles instead of falling back to normal runtime activity when durable task IDs exist without a readable `taskStatePath`.
- Implemented a centrally testable durable-vs-runtime arbitration policy in `shared/ui-visibility.ts` and refactored title/widget/status paths to use the shared durable-terminal/degraded-state decisions.
- ✅ Resolved review finding [HIGH]: Foreground terminal title ownership now clears instead of showing normal runtime activity when matched durable task IDs are `completed`, `blocked`, or `failed`.
- ✅ Resolved review finding [MEDIUM]: Async `subagent({ action: "status" })` list/detail output now applies durable-status arbitration, hides durable-terminal work from active listings, and emits degraded BMAD warnings for missing/unreadable/malformed task state.
- Regenerated `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch` after package source changes and validated both idempotent `--patch` and clean package restore application.
- Extended async status list/detail arbitration to job-level `durableTaskIds` when status files have durable IDs before step records, so durable-terminal jobs are not listed active and missing task-state jobs show degraded warnings.
- Regenerated the Story 1.5 patch again after job-level async status source changes and validated clean restore plus full regression commands.
- Broadened the central arbitration helper to use same-agent durable status as a safety fallback when runtime progress has a `taskStatePath` but no durable task id, preventing normal foreground titles for durable-terminal BMAD tasks.

### File List

- `.pi/agents/implementer.md`
- `.pi/agents/reviewer-a.md`
- `.pi/agents/reviewer-b.md`
- `.pi/npm/node_modules/pi-subagents/src/agents/agents.ts`
- `.pi/npm/node_modules/pi-subagents/src/extension/index.ts`
- `.pi/npm/node_modules/pi-subagents/src/extension/schemas.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-execution.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/chain-execution.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts`
- `.pi/npm/node_modules/pi-subagents/src/runs/shared/parallel-utils.ts`
- `.pi/npm/node_modules/pi-subagents/src/shared/settings.ts`
- `.pi/npm/node_modules/pi-subagents/src/shared/types.ts`
- `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts`
- `.pi/npm/node_modules/pi-subagents/src/shared/utils.ts`
- `.pi/npm/node_modules/pi-subagents/src/tui/render.ts`
- `.pi/patches/apply-patches.sh`
- `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch`
- `.pi/skills/bmad-dev-cycle/workflow.md`
- `.pi/skills/bmad-orchestrator/SKILL.md`
- `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md`
- `docs/_bmad-output/implementation-artifacts/sprint-status.yaml`
- `tests/test_pi_ui_visibility_agent_activity.py`

### Change Log

- Addressed code review findings - 4 items resolved (Date: 2026-05-13): role labels for inactive durable tasks, durable task identity propagation, missing `taskStatePath` degraded BMAD UI, and required `contextSource` validation.
- Addressed code review findings - 4 items resolved (Date: 2026-05-13): foreground single-run terminal-title durable identity, durable-status gating for runtime widget rows, async job-level `durableTaskIds` activity-title matching, and missing-`taskStatePath` degraded rendering for async BMAD jobs.
- Addressed code review findings - 3 items resolved (Date: 2026-05-13): clean-install Story 1.5 patch durability, foreground terminal-title lifecycle coverage, and async durable-status terminal-title gating.
- Addressed code review findings - 2 items resolved (Date: 2026-05-13): async multi-job active bucketing/header durable-status gating and missing/unreadable `taskStatePath` async terminal-title clearing.
- Amended story design requirement (Date: 2026-05-13): added explicit central runtime/durable arbitration requirement after R1-R5 reviews showed per-surface fixes were insufficient.
- Targeted remediation completed (Date: 2026-05-13): centralized durable/runtime arbitration, resolved remaining R5 foreground-title and async status-output findings, regenerated Story 1.5 package patch, and validated focused/full regression commands.
- Targeted remediation hardening (Date: 2026-05-13): extended async status list/detail durable arbitration to job-level `durableTaskIds` before step records exist, regenerated the package patch, and revalidated clean restore/full regression.
- Targeted remediation hardening (Date: 2026-05-13): broadened central arbitration same-agent durable-terminal fallback for foreground titles without per-progress durable ids and revalidated clean restore/full regression.

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Key implementation decision during dev: whether the existing `pi-subagents` UI/status renderer can be extended with a durable patch, or whether a small project-local Pi extension is narrower for the task-list projection. In either case, durable Markdown task truth must remain authoritative.

## Senior Developer Review (AI)

### Action Items

- [x] [R1][HIGH][AC1] Inactive/pending durable tasks do not display configured role labels [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:183`] — Load/propagate configured agent role labels for all durable task `targetAgent`/`activeAgentId` values, not only runtime-active rows. Add tests for pending/completed/blocked/failed tasks showing BMAD role labels.
- [x] [R1][HIGH][AC2, AC3] Parallel same-agent activity titles can resolve to the wrong durable task [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:207`] — Carry a durable task identity such as `taskId`/`durableTaskId` through subagent params, progress, async status, and results; match titles by task id before falling back to agent. Add a regression test for two parallel same-agent tasks.
- [x] [R1][MEDIUM][AC5] Missing task-state path silently suppresses degraded BMAD UI [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`] — Make BMAD task projection requirement explicit and render the degraded warning when a BMAD/team view is expected but `taskStatePath` is missing. Add coverage for missing `taskStatePath` in rendered UI.
- [x] [R1][MEDIUM][AC5] Malformed durable task records missing required `contextSource` render as valid/completed instead of degraded [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:122`] — Validate all required Story 1.4 fields, at minimum `contextSource` structure/presence, before projecting tasks. Treat missing required fields as degraded and add regression tests.
- [x] [R2][HIGH][AC2, AC3] Foreground single-run terminal titles lose durable task identity [`.pi/npm/node_modules/pi-subagents/src/runs/foreground/execution.ts:398`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`] — Preserve `taskStatePath` on foreground single progress updates before setting terminal titles, and use `durableTaskId` as a fallback task id if durable state is unavailable. Add a regression test for foreground single active-title updates using `taskStatePath` + `durableTaskId`.
- [x] [R2][HIGH][AC4] Stale durable completed/blocked/failed tasks can still render as active in runtime widget rows [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:346`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:354`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:651`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:708`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:784`] — When `taskStatePath` + `durableTaskId` are available, gate all BMAD runtime row glyphs/status labels through durable status so `completed`, `blocked`, and `failed` never display active styling. Runtime `running` may remain only as a secondary/dim annotation. Add renderer coverage for stale runtime `running` against durable terminal statuses.
- [x] [R2][HIGH][AC2, AC3] Async job-level durable task identity is ignored when building activity titles [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:260`] — Teach activity-title selection to use `AsyncJobState.durableTaskIds` when steps are absent or before status polling has populated per-step records. Match by durable task id before falling back to agent or first in-progress task, and add a regression test for job-level `durableTaskIds`.
- [x] [R2][MEDIUM][AC5] Missing `taskStatePath` degraded UI is suppressed for async BMAD jobs represented only by `durableTaskIds` [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:240`] — Update BMAD projection expectation detection to treat non-empty `durableTaskIds` as BMAD/task-projection evidence, and add a regression test for an async job with `durableTaskIds` but missing `taskStatePath` and no steps.
- [x] [R3][HIGH][Package durability] Story 1.5 patch is not clean-install durable because it duplicates an earlier patch [`.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch:1`] — Regenerate the Story 1.5 patch relative to already-required prior patches, removing duplicated `src/agents/agents.ts` hunks, or update patch ordering/idempotency logic with clean-install validation.
- [x] [R3][HIGH][AC2, AC3] Foreground subagent runs still do not set terminal activity titles [`.pi/npm/node_modules/pi-subagents/src/extension/index.ts:471`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:1861`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:948`] — Add a foreground title lifecycle hook where foreground `onUpdate`/rendering has `ctx` access; set `ctx.ui.setTitle(buildRuntimeActivityTitle(...))` while running and clear/restore it on completion/failure/interruption/detach/session reload. Add regression coverage.
- [x] [R3][HIGH][AC2, AC3, AC4] Async terminal titles can stay active for durable completed/blocked/failed tasks when runtime still reports running [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:965`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:278`] — Gate async title selection through durable status before `setTitle`; if matched durable task IDs are terminal, clear/restore title instead of using runtime fallback. Add regression coverage.
- [x] [R4][HIGH][AC4] Async multi-job widget can still show durable-terminal work as active [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:850-858`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:869-873`] — Gate async job active bucketing/header state through durable status before computing running/queued/finished and `hasActive`; treat jobs whose matched durable status is terminal as terminal for UI active-state purposes.
- [x] [R4][MEDIUM][AC5] Async terminal title falls back to normal runtime activity when BMAD durable task IDs exist but `taskStatePath` is missing [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:289-302`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:981-982`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:273-291`] — If async runtime has non-empty durable task IDs but no readable `taskStatePath`, do not set a normal active terminal title; clear it or set an explicit degraded title. Add provider-free regression coverage.
- [x] [R5][HIGH][AC3, AC4] Foreground terminal title can still show a normal active activity for a durable-terminal task [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:269`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777`] — Gate foreground title ownership through durable status before calling `setTitle`, or make the shared arbitration/title helper return no normal runtime title when matched durable task IDs are terminal. Add regression coverage for foreground progress with completed/blocked/failed durable status.
- [x] [R5][MEDIUM][AC4, AC5] Async status output can still show durable-terminal BMAD work as active [`.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:62-66`, `.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts:130-150`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:221-224`, `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts:242-245`] — Apply the shared durable-status arbitration to async `subagent({ action: "status" })` list/detail output; show degraded warning for missing/unreadable/malformed task state.
- [ ] [TARGETED][HIGH][AC3, AC4] Foreground title arbitration can still fall back to a normal active runtime title for same-agent durable-terminal work [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:318-345`, `.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:416-431`, `.pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts:777-779`] — Make shared arbitration fail closed for BMAD foreground/runtime items that match durable tasks but have no matched `in-progress` durable task; do not fall back to normal runtime title or unrelated global active task after arbitration says `canShowActive: false`.
- [ ] [TARGETED][HIGH][AC4] Async widget rows can still display durable-terminal jobs as running/thinking [`.pi/npm/node_modules/pi-subagents/src/tui/render.ts:646-663`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:859-866`] — Pass shared arbitration/effective durable status into widget row stats/activity formatting; durable-terminal/degraded BMAD jobs must not render running counts or `thinking…`/live active prompts.
- [ ] [TARGETED][MEDIUM][AC4, AC5] Renderer/widget paths can bypass degraded central arbitration for durable IDs that do not resolve to durable task state [`.pi/npm/node_modules/pi-subagents/src/shared/ui-visibility.ts:265`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:715`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:763`, `.pi/npm/node_modules/pi-subagents/src/tui/render.ts:965`] — Make shared status helpers fail closed when durable IDs are present but unmatched; avoid same-agent fallback and add rendered-output tests for unmatched/missing/unreadable/malformed task-state cases.

## BMAD Dev Cycle (AI)

### Orchestrator State
- Max iterations: 5
- Current iteration: 5
- Dev agent: implementer (`openai-codex/gpt-5.5`)
- Review agents: reviewer-a, reviewer-b (`openai-codex/gpt-5.5`)
- Reviewer output artifacts: `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R1-reviewer-a-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R1-reviewer-b-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R2-reviewer-a-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R2-reviewer-b-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R3-reviewer-a-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R3-reviewer-b-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R4-reviewer-a-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R4-reviewer-b-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R5-reviewer-a-output.md`, `docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R5-reviewer-b-output.md`
- Severity counts: High 1, Medium 1, Low 0
- Deduped finding count: 2
- Next action: HALT — five-iteration maximum reached with 2 remaining High/Medium findings.

### Task State
```yaml
tasks:
  - taskId: "dev-R1"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "R1 dev task is eligible after context validation. Previous dispatch used API provider model openai/gpt-5.5 and was rejected before child execution; user clarified the intended subscription provider is openai-codex/gpt-5.5. Relaunching with context: fresh, agentScope: project, model: openai-codex/gpt-5.5."
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R1"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R1"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R1-reviewer-a-output.md"
    routingDecision: "dev-R1 completed and parent validation accepted story artifact/readability and validation evidence; review-a-R1 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R1"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R1"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R1-reviewer-b-output.md"
    routingDecision: "dev-R1 completed and parent validation accepted story artifact/readability and validation evidence; review-b-R1 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "dev-R2"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "R1 produced 4 blocking High/Medium findings after reviewer deduplication; dev-R2 completed and parent validation found checked R1 action items, updated change log, story artifact readability, and validation evidence."
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R2"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R2"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R2-reviewer-a-output.md"
    routingDecision: "dev-R2 completed and parent validation accepted story artifact/readability and validation evidence; review-a-R2 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R2"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R2"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R2-reviewer-b-output.md"
    routingDecision: "dev-R2 completed and parent validation accepted story artifact/readability and validation evidence; review-b-R2 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "dev-R3"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "R2 produced 4 blocking High/Medium findings after reviewer deduplication; dev-R3 completed and parent validation found checked R2 action items, updated change log, story artifact readability, and validation evidence."
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R3"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R3"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R3-reviewer-a-output.md"
    routingDecision: "dev-R3 completed and parent validation accepted story artifact/readability and validation evidence; review-a-R3 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R3"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R3"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R3-reviewer-b-output.md"
    routingDecision: "dev-R3 completed and parent validation accepted story artifact/readability and validation evidence; review-b-R3 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "dev-R4"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "R3 produced 3 blocking High findings after reviewer deduplication; dev-R4 completed and parent validation found checked R3 action items, updated change log, story artifact readability, clean patch restore evidence, and validation evidence."
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R4"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R4"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R4-reviewer-a-output.md"
    routingDecision: "dev-R4 completed and parent validation accepted story artifact/readability and validation evidence; review-a-R4 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R4"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R4"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R4-reviewer-b-output.md"
    routingDecision: "dev-R4 completed and parent validation accepted story artifact/readability and validation evidence; review-b-R4 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "dev-R5"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "R4 produced 2 blocking High/Medium findings after reviewer deduplication; dev-R5 completed and parent validation found checked R4 action items, updated change log, story artifact readability, clean patch restore evidence, and validation evidence."
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R5"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R5"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R5-reviewer-a-output.md"
    routingDecision: "dev-R5 completed and parent validation accepted story artifact/readability and validation evidence; review-a-R5 is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R5"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R5"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-add-pi-ui-visibility-for-agent-activity-R5-reviewer-b-output.md"
    routingDecision: "dev-R5 completed and parent validation accepted story artifact/readability and validation evidence; review-b-R5 is eligible."
    cause: null
    recommendedNextAction: null
```

## Targeted Remediation (AI)

### Orchestrator State
- Scope: post-dev-cycle targeted remediation for central runtime/durable arbitration
- Current pass: central-arbitration-1
- Dev agent: implementer (`openai-codex/gpt-5.5`)
- Review agents: reviewer-a, reviewer-b (`openai-codex/gpt-5.5`)
- Next action: CHANGES_REQUESTED — targeted reviews found 3 remaining High/Medium findings.

### Task State
```yaml
tasks:
  - taskId: "targeted-dev-central-arbitration"
    title: "Implement central durable-vs-runtime UI arbitration and remaining R5 fixes"
    targetAgent: "implementer"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: "implementer"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
    routingDecision: "User approved targeted remediation after amending the story with central runtime/durable arbitration requirements; implementation completed central arbitration, remaining R5 fixes, job-level async status durable-ID hardening, same-agent durable-terminal title fallback, patch regeneration, and focused/full validation evidence."
    cause: null
    recommendedNextAction: null
  - taskId: "targeted-review-a-central-arbitration"
    title: "Independent targeted review A for central arbitration fixes"
    targetAgent: "reviewer-a"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["targeted-dev-central-arbitration"]
    activeAgentId: "reviewer-a"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-central-arbitration-targeted-reviewer-a-output.md"
    routingDecision: "targeted-dev-central-arbitration completed and parent validation accepted story artifact/readability and validation evidence; targeted-review-a-central-arbitration is eligible."
    cause: null
    recommendedNextAction: null
  - taskId: "targeted-review-b-central-arbitration"
    title: "Independent targeted review B for central arbitration fixes"
    targetAgent: "reviewer-b"
    status: "completed"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/1-5-add-pi-ui-visibility-for-agent-activity.md"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["targeted-dev-central-arbitration"]
    activeAgentId: "reviewer-b"
    outputArtifact: "docs/_bmad-output/implementation-artifacts/1-5-add-pi-ui-visibility-for-agent-activity/review-1-5-central-arbitration-targeted-reviewer-b-output.md"
    routingDecision: "targeted-dev-central-arbitration completed and parent validation accepted story artifact/readability and validation evidence; targeted-review-b-central-arbitration is eligible."
    cause: null
    recommendedNextAction: null
```

# Story 1.5: Add Pi UI Visibility for Agent Activity

Status: ready-for-dev

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

- [ ] Define the v1 Pi UI visibility contract and boundaries. (AC: 1-5)
  - [ ] Document in `.pi/skills/bmad-orchestrator/SKILL.md` how parent BMAD workflows expose UI-visible agent labels, activity titles, terminal/session titles, and task-list artifacts.
  - [ ] State explicitly that Pi TUI / `pi-subagents` surfaces are the UI; do not add a web dashboard, daemon, database, sidecar service, or separate frontend.
  - [ ] State that UI rendering is a read-only projection of durable Markdown task state plus runtime annotations; it must never mark workflow success or override artifact truth.
  - [ ] Keep Story 1.4 fixed task status vocabulary as the only builder-facing workflow task status vocabulary: `pending`, `in-progress`, `completed`, `blocked`, `failed`.
- [ ] Add configured role-label and layout support. (AC: 1)
  - [ ] Use configured role labels from project agent frontmatter, starting with existing `.pi/agents/*.md` `roleLabel` values.
  - [ ] Add a deterministic fallback when `roleLabel` is missing: use agent display/name metadata without crashing.
  - [ ] Define minimal v1 layout rules for visible, hidden, inactive, active, completed, blocked, and failed agents.
  - [ ] Do not hardcode labels only for `implementer`, `reviewer-a`, or `reviewer-b`; keep behavior generic for future agents.
- [ ] Add active-agent and task activity titles. (AC: 2, 3)
  - [ ] Derive the primary activity title from durable task state first: `{activeAgentId or targetAgent} · {taskId} · {title}`.
  - [ ] Use runtime `taskSummary`, current tool/current operation, current path, model name, token count, and elapsed duration as secondary annotations only.
  - [ ] Ensure two parallel same-agent tasks remain distinguishable by task id/title.
  - [ ] Use Pi `ctx.ui.setTitle(...)` or an equivalent Pi-supported terminal-title mechanism where available; clear or restore titles on completion, failure, session shutdown, and reload to avoid stale terminal titles.
- [ ] Project the durable orchestrator task list into Pi UI. (AC: 4, 5)
  - [ ] Read the Story 1.4 task-list source from the current story/spec/run Markdown artifact, not from hidden runtime memory, `progress.md`, or async `status.json` alone.
  - [ ] Display task rows with status, role label/agent, task id, title, and safe runtime annotations when available.
  - [ ] Prevent stale states: `completed`, `blocked`, and `failed` durable tasks must not render as active even if a runtime job still reports `running`.
  - [ ] On missing/unreadable/malformed task-list artifact or invalid task status, show a degraded warning state and do not show success/completion.
- [ ] Integrate with existing `pi-subagents` TUI/status surfaces without duplicating dispatch. (AC: 1-5)
  - [ ] Prefer extending existing `pi-subagents` foreground result rendering, async widget, status output, and task/model summary pipeline.
  - [ ] Preserve existing foreground/async observability for chains and parallel groups: per-agent rows, model tags, task summaries, token counts, elapsed duration, live current tool/current operation/path, paused/failed visibility, and compact expanded views.
  - [ ] Do not add a custom `dispatch_subagent` tool, role-specific sub-agent launcher, dispatchable `orchestrator` child agent, or nested orchestration ability for child agents.
  - [ ] Preserve formal BMAD dispatch policy: explicit `context: "fresh"`, no `context: "fork"`, no `subagent({ action: "resume" })` for active v1 formal paths.
- [ ] Make any package/runtime changes durable. (AC: 1-5)
  - [ ] If no `pi-subagents` source change is required, state this explicitly in completion notes.
  - [ ] If any `.pi/npm/node_modules/pi-subagents/src/**` file changes, create `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch` or similarly named version-scoped patch containing every package-source change.
  - [ ] Update package patch durability tests so `.pi/install-packages.sh` applies or reports the Story 1.5 patch already applied.
  - [ ] Do not leave direct generated-package edits uncaptured by a durable patch.
- [ ] Add provider-free regression tests. (AC: 1-5)
  - [ ] Add `tests/test_pi_ui_visibility_agent_activity.py` or equivalent.
  - [ ] Test no separate frontend/dashboard/server is introduced for this story.
  - [ ] Test role-label extraction and fallback behavior using `.pi/agents/*.md` fixtures.
  - [ ] Test activity-title formatting, truncation, injected-noise stripping, and parallel task distinguishability.
  - [ ] Test that the UI preserves the useful existing sub-agent widget facts: model name, assigned task/task summary, token count, elapsed duration, and current tool/current operation.
  - [ ] Test task-list projection with all five durable statuses and with runtime `running`, `complete`, `paused`, and `detached` annotations.
  - [ ] Test stale-state prevention: durable `completed`/`blocked`/`failed` cannot render as active.
  - [ ] Test missing/unreadable/malformed task state renders a degraded warning and never a success/completed signal.
  - [ ] Test no `dispatch_subagent`, no dispatchable orchestrator child agent, and no `subagent` tool grant to project child agents.
- [ ] Run final validation and artifact-cleanliness checks. (AC: 1-5)
  - [ ] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [ ] Run `PI_TELEMETRY=0 pi list`.
  - [ ] Run `git diff --check`.
  - [ ] Run `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` and remove generated bytecode if any appears.
  - [ ] Run `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` and confirm no story-specific review artifacts are at the implementation-artifacts root.

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

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Key implementation decision during dev: whether the existing `pi-subagents` UI/status renderer can be extended with a durable patch, or whether a small project-local Pi extension is narrower for the task-list projection. In either case, durable Markdown task truth must remain authoritative.

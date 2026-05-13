# Code Context

## Files Retrieved
1. `docs/_bmad-output/planning-artifacts/epics.md` (lines 249-253, 513-544) - Epic 1 and Story 1.5 source acceptance criteria.
2. `docs/_bmad-output/planning-artifacts/architecture.md` (lines 137-140, 353-359, 450-458, 576-587) - Pi TUI/extension UI constraints and artifact/status rules.
3. `docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/1-4-add-orchestrator-task-routing-and-task-list-state.md` (lines 74-97, 194-197, 249-252) - Story 1.4 boundary: task-state exists, UI was deferred.
4. `.pi/skills/bmad-orchestrator/SKILL.md` (lines 65-132, 179-218, 247-254) - current BMAD durable task-state and dispatch evidence contract.
5. `.pi/agents/implementer.md` (lines 1-12), `.pi/agents/reviewer-a.md` (lines 1-12), `.pi/agents/reviewer-b.md` (lines 1-12) - existing role labels in agent frontmatter.
6. `.pi/npm/node_modules/pi-subagents/src/tui/render.ts` (lines 279-369, 588-842, 844-960, 1010-1125) - current widget/result rendering, activity, model, and task-summary display.
7. `.pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts` (lines 28-60, 109-190, 206-257) - background job polling, status propagation, widget rerender/cleanup.
8. `.pi/npm/node_modules/pi-subagents/src/extension/index.ts` (lines 303-475, 505-581) - subagent tool registration, notification renderers, widget lifecycle hooks.
9. `.pi/npm/node_modules/pi-subagents/src/shared/types.ts` (lines 134-155, 267-350) - runtime progress/status/job types.
10. `.pi/npm/node_modules/pi-subagents/src/runs/background/async-execution.ts` (lines 300-460, 471-608) - async step construction and start events.
11. `.pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts` (lines 896-926, 1011-1097, 1164-1184) - `status.json` shape and live activity updates.
12. `.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts` (lines 1-40, 116-166, 229-295) and `run-status.ts` (lines 120-168) - status/list formatting.
13. `.pi/npm/node_modules/pi-subagents/src/agents/agents.ts` (lines 70-96, 627-662) - agent parser keeps unknown frontmatter in `extraFields`.
14. `.pi/npm/node_modules/pi-subagents/src/extension/schemas.ts` (lines 38-84, 129-168) - subagent params currently lack UI/activity/task-state options.
15. `tests/test_orchestrator_task_routing_state.py` (lines 1-205) - provider-free regression-test style for Story 1.4.
16. `tests/test_subagent_model_task_summary.py` (lines 1-160, 321-480) - provider-free package patch and render-source test patterns.
17. `.pi/install-packages.sh` (lines 1-19, 91-111), `.pi/patches/` - package patch durability mechanism.
18. `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md` (lines 724-793) and `docs/rpc.md` (lines 1093-1137) - Pi UI APIs: `setStatus`, `setWidget`, `setTitle`.

## Key Code

Story 1.5 requires visible labels, active agent/activity titles, terminal titles, task/todo list updates, stale-state avoidance, and safe degraded UI:

```md
# docs/_bmad-output/planning-artifacts/epics.md:513-544
... visible sub-agents display their configured role labels ...
... UI identifies which sub-agent is currently active ... activity title describes the current task ...
... each session has a descriptive activity title ...
... Pi UI task/todo list reflects the current state ... stale task states are not shown as active ...
... safe degraded message ... workflow execution is not treated as successful solely because UI rendering succeeded.
```

Existing agent labels already exist in project agent frontmatter:

```yaml
# .pi/agents/implementer.md:1-10
name: implementer
roleLabel: BMAD Implementer
model: openai/gpt-5.5
...
```

`pi-subagents` parses unknown frontmatter into `AgentConfig.extraFields`, so `roleLabel` is currently retained but not promoted/rendered:

```ts
// .pi/npm/node_modules/pi-subagents/src/agents/agents.ts:70-96, 627-662
export interface AgentConfig { ... extraFields?: Record<string, string>; }
...
for (const [key, value] of Object.entries(frontmatter)) {
  if (!KNOWN_FIELDS.has(key)) extraFields[key] = value;
}
```

Current widget/result UI displays raw `agent`, model, task summary, and live tool/activity, but not `roleLabel` or explicit activity title:

```ts
// .pi/npm/node_modules/pi-subagents/src/tui/render.ts:602-620
const modelTag = step.model ? ` (${step.model})` : "";
const lines = [`... ${themeBold(theme, step.agent)}${modelTag} ...`];
if (step.taskSummary) lines.push(`⎿  ${step.taskSummary}`);
const activity = widgetStepActivityLine(step, width, expanded);
```

Background job state comes from async `status.json`; terminal statuses are cleaned after retention:

```ts
// .pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts:141-180
job.status = status.state;
job.activityState = status.activityState;
job.currentTool = status.currentTool;
...
job.steps = visibleSteps;
...
if ((job.status === "complete" || job.status === "failed" || job.status === "paused") ...) scheduleCleanup(job.asyncId);
```

Async runner writes step status, model, task summary, and live activity, but no role label/activity title/task-list pointer:

```ts
// .pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts:896-926
steps: flatSteps.map((step) => ({
  agent: step.agent,
  status: "pending",
  ...(step.taskSummary ? { taskSummary: step.taskSummary } : {}),
  model: step.model,
  ...
}))
```

Pi UI supports the needed primitives:

```ts
// tui.md:724-793 and rpc.md:1093-1137
ctx.ui.setStatus("my-ext", "...")
ctx.ui.setWidget("my-widget", ["Line 1", "Line 2"])
ctx.ui.setTitle("pi - my project")
```

## Architecture

- Durable workflow truth is Markdown, not runtime status. `.pi/skills/bmad-orchestrator/SKILL.md` lines 65-132 require a builder-facing task list in story/spec/run Markdown artifacts with fixed statuses `pending`, `in-progress`, `completed`, `blocked`, `failed`. Runtime `running`/`complete`/`paused`/`detached` must be mapped before durable state is written.
- `pi-subagents` owns runtime execution visibility: foreground result renderers and background async widget. It already has agent/task/model/activity plumbing for runtime jobs, but only by canonical `agent` name.
- Existing Story 1.4 did not implement UI; it explicitly deferred widgets, role labels, terminal activity titles, and stale-state rendering to Story 1.5.
- There is no first-class Pi task/todo-list API identified; Pi exposes generic `setWidget`/`setStatus`/`setTitle`. A task list UI will need either:
  - a generic `pi-subagents` widget enhancement fed by runtime/task-state inputs, or
  - a small project-local extension/widget that reads the durable BMAD Markdown task list.
- If modifying `.pi/npm/node_modules/pi-subagents`, changes are generated/ignored unless captured as a durable patch under `.pi/patches/` and applied by `.pi/install-packages.sh`.

## Likely Files to Modify

Primary package/runtime path if Story 1.5 extends existing `pi-subagents` UI:

```text
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
.pi/npm/node_modules/pi-subagents/src/extension/schemas.ts   # only if adding explicit activityTitle/taskStatePath params
.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch
```

Likely project guidance/test files:

```text
.pi/skills/bmad-orchestrator/SKILL.md                 # define how parent supplies UI title/task-list artifact path, if guidance-only parts are needed
.pi/settings.json                                     # only if adding project UI layout config
.pi/agents/*.md                                       # maybe add uiVisible/layout fields; roleLabel already exists
tests/test_pi_ui_visibility_agent_activity.py          # new provider-free Story 1.5 tests
tests/test_subagent_model_task_summary.py              # extend package patch expectations if patch changes render/types
```

If the task list must read durable BMAD Markdown directly, consider a project-local extension instead of overloading `pi-subagents` dispatch:

```text
.pi/extensions/bmad-ui-visibility/src/status-widget.ts
.pi/extensions/bmad-ui-visibility/package.json
.pi/extensions/bmad-ui-visibility/tests/...
scripts/validate-extensions.sh                         # if this is the first framework-owned TS extension
```

## Implementation Notes / Risks

- **Role labels:** Current agent files define `roleLabel`; `AgentConfig.extraFields.roleLabel` is available but not propagated to `SingleResult`, `AgentProgress`, `AsyncStatus.steps`, `AsyncJobState`, or renderers. Add optional `roleLabel`/`displayLabel` fields generically, defaulting to `extraFields.roleLabel ?? agent.name`.
- **Activity title:** Current `taskSummary` is the closest existing activity title. For AC wording, either explicitly treat `taskSummary` as the UI activity title or add `activityTitle` with fallback to `taskSummary`. If adding a user-facing param, update `schemas.ts` for single/tasks/chain items.
- **Terminal title:** `pi-subagents` currently never calls `ctx.ui.setTitle`. `extension/index.ts` has `ctx` at execution/render hooks and can set/clear titles. Decide restore behavior on completion/session shutdown to avoid stale terminal titles.
- **Task/todo list:** Runtime status is not enough for Story 1.4/1.5 because durable task truth is Markdown. Do not mark workflow success based on widget rendering. If parsing Markdown is out of scope, implement a safe degraded widget message and document that the parent must point UI at a named task-list artifact.
- **Stale states:** Async tracker already cleans complete/failed/paused jobs after `completionRetentionMs` and sets failed on unreadable status. Any new task-list widget must similarly avoid showing old `in-progress` unless the durable artifact still says so and should label missing/unreadable task state as degraded, not active.
- **Hidden/inactive layout rules:** No current config was found beyond role labels. Story implementation likely needs to define a minimal v1 layout rule (e.g., show only active/recent visible agents; omit inactive; optional `uiVisible: false`) before coding/tests.
- **Testing:** Avoid provider calls. Existing tests are Python `unittest`, mostly source-text assertions; `tsx` subprocess tests import only dependency-light modules like `formatters.ts`. Importing `render.ts` may require Pi peer packages not installed under `.pi/npm`, so prefer source assertions for render changes unless you provide stubs or run in the full Pi environment.

## Start Here

Start with `.pi/npm/node_modules/pi-subagents/src/tui/render.ts` and `.pi/npm/node_modules/pi-subagents/src/runs/background/async-job-tracker.ts`. They are the current UI/status bridge: renderer output shows what the builder sees, and tracker determines when jobs are active, stale, complete, or failed. Then inspect `.pi/skills/bmad-orchestrator/SKILL.md` for the durable task-state constraints that the UI must not override.

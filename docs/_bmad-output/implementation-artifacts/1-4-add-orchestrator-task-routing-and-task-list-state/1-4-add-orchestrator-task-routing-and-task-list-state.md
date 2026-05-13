# Story 1.4: Add Orchestrator Task Routing and Task List State

Status: ready-for-dev

<!-- Ultimate context engine analysis completed - comprehensive developer guide created. -->

## Story

As a builder,
I want the orchestrator to route sequenced tasks to sub-agents and expose task state,
so that I can see which tasks are pending, in progress, and completed during a team run.

## Acceptance Criteria

1. Given a team run is started, when the orchestrator creates its task list, then each task has an identifier, target agent, status, title, and context source, and statuses use a fixed vocabulary.
2. Given a task is pending, when the orchestrator dispatches its target agent, then the task status changes to in-progress and the active agent identifier is recorded.
3. Given a sub-agent completes successfully, when the orchestrator processes the completion signal, then the task status changes to completed and the next eligible task can be dispatched.
4. Given one sub-agent output is needed by another sub-agent, when the orchestrator routes the next task, then the previous output is passed as declared task context or artifact path and the routing decision is recorded.
5. Given a task fails or cannot be classified, when the orchestrator updates state, then the task is marked blocked or failed and the builder receives a cause and recommended next action.

## Tasks / Subtasks

- [ ] Define the v1 orchestrator task-state contract. (AC: 1, 5)
  - [ ] Add a `Task Routing and Task List State` section to `.pi/skills/bmad-orchestrator/SKILL.md` or an explicitly referenced narrow contract file.
  - [ ] State where parent workflows must write/read the task list during a run: the relevant BMAD story/spec/run artifact when one exists; otherwise a named Markdown artifact created by the active workflow.
  - [ ] Define the required fields for every orchestrator-managed task: `taskId`, `title`, `targetAgent`, `status`, `contextSource`, and optional `dependsOn`, `activeAgentId`, `outputArtifact`, `cause`, `recommendedNextAction`, and `routingDecision`.
  - [ ] Use one fixed builder-facing status vocabulary: `pending`, `in-progress`, `completed`, `blocked`, `failed`.
  - [ ] State that runtime/package statuses such as `running`, `complete`, `paused`, or `detached` are control-plane details and must be mapped into the builder-facing vocabulary before durable Markdown state is written.
- [ ] Add parent-orchestrator routing rules for task lifecycle transitions. (AC: 2, 3, 5)
  - [ ] Before a formal dispatch, validate the task is `pending` and all dependencies are `completed`.
  - [ ] Immediately before dispatch, write or update durable task state to `in-progress` and record `activeAgentId` using the requested/list-validated canonical agent identifier.
  - [ ] After successful child completion and parent validation, update the task to `completed` and record the control-plane result reference or output artifact path.
  - [ ] If a child fails, times out, returns empty/ambiguous output, violates session policy, or produces an unclassifiable state, mark the task `blocked` or `failed` with a cause and recommended next action; do not dispatch later dependent tasks.
- [ ] Define deterministic handoff rules for sequenced tasks. (AC: 3, 4)
  - [ ] Document that one task's result may become the next task's context only through an explicit declared context source: direct task text, an output artifact path, or a named `pi-subagents` output file reference.
  - [ ] Preserve artifact-first behavior for formal workflows: pass artifact paths/read directives rather than parent-side summaries whenever a canonical artifact exists.
  - [ ] Record the routing decision showing why the next task became eligible and which prior output/context source it consumed.
  - [ ] Keep child output as control-plane until the parent writes validated durable state back to Markdown.
- [ ] Integrate the task-state contract into active BMAD guidance without breaking Story 1.3 fresh-session policy. (AC: 1-5)
  - [ ] Ensure all examples that dispatch sub-agents still use explicit `context: "fresh"`; do not introduce omitted context, `context: "fork"`, or `action: "resume"`.
  - [ ] Ensure policy rejection happens before task status changes except for an optional debug note explicitly allowed by the workflow; rejected session requests must not become `in-progress`.
  - [ ] Do not add a dispatchable `orchestrator` or `bmad-orchestrator` child agent.
  - [ ] Do not grant the `subagent` tool to `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, or `.pi/agents/reviewer-b.md`.
- [ ] Add provider-free regression tests. (AC: 1-5)
  - [ ] Add `tests/test_orchestrator_task_routing_state.py` or extend an existing orchestrator guidance test file.
  - [ ] Assert the fixed vocabulary and required task fields are documented.
  - [ ] Assert pending → in-progress → completed transition rules are documented.
  - [ ] Assert blocked/failed handling requires cause and recommended next action.
  - [ ] Assert sequenced handoffs require declared context source or artifact path and record a routing decision.
  - [ ] Assert task-routing examples preserve explicit `context: "fresh"` and do not include `context: "fork"` or `action: "resume"` in formal BMAD launches.
- [ ] Only if implementation changes `pi-subagents` runtime/package behavior, make the change durable. (AC: 1-5)
  - [ ] Keep package changes generic; do not hardcode BMAD story keys, project-specific models, or mypi-config-only file paths.
  - [ ] Capture the source delta in a version-scoped patch under `.pi/patches/`, for example `pi-subagents-0.24.2-orchestrator-task-state.patch`.
  - [ ] Update or add tests for changed package status/progress/output mapping.
  - [ ] Verify `bash .pi/install-packages.sh --patch` applies the patch or reports it already applied.
- [ ] Run final validation and artifact-cleanliness checks. (AC: 1-5)
  - [ ] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [ ] Run `PI_TELEMETRY=0 pi list`.
  - [ ] Run `git diff --check`.
  - [ ] Run `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` and remove generated bytecode if any appears.
  - [ ] Run `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` and confirm no story-specific review artifacts are at the implementation-artifacts root.

## Dev Notes

### Source of Truth

Story 1.4 is part of Epic 1, which must complete the observable Pi multi-agent runtime before portable bootstrap and standard story-to-done execution. This story specifically adds orchestrator-owned task routing and a visible task-list state layer; it is not the Pi UI rendering story and not the two-agent smoke proof. [Source: docs/_bmad-output/planning-artifacts/epics.md#Epic-1-Observable-Pi-Multi-Agent-Runtime]

Relevant requirements and architecture constraints:

- FR23: parent BMAD orchestration guidance can route one sub-agent's output as another sub-agent's input in a defined sequence. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- FR25: the builder can view a task/todo list tracking pending, in-progress, and completed tasks. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- Durable workflow decisions and task progress must be written back to Markdown artifacts only after parent validation; runtime completion signals are control-plane only. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]
- Agents communicate vertically through the parent orchestrator: agent reads artifacts, performs the task, writes outputs, returns a control-plane signal, and the orchestrator re-reads artifacts before routing. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Communication-Patterns]
- Ambiguous states, invalid artifact states, unsafe continuation, environment blocks, retry-limit exhaustion, and workflow contract violations must escalate instead of being interpreted freely. [Source: docs/_bmad-output/planning-artifacts/epics.md#Additional-Requirements]

### Story Boundary

Implement only task routing and task-list state for parent orchestration guidance.

In scope:

- A parent-orchestrator task-state contract with deterministic fields and fixed statuses.
- Rules for moving tasks from `pending` to `in-progress`, `completed`, `blocked`, or `failed`.
- Rules for dispatching the next eligible task and recording declared context handoff.
- Provider-free tests proving the task-state contract and routing rules are present.

Out of scope:

- Story 1.5 Pi UI widgets, role labels, terminal activity titles, or stale-state UI rendering.
- Story 1.6 two-agent smoke scenario execution proof.
- Epic 3 full standard BMAD story-to-done workflow, quality gates, and review orchestration.
- Epic 4 TDD/ATDD/TDAD batch orchestration.
- New dispatchable `orchestrator` child agent or nested sub-agent orchestration.
- Broad `.pi/references/artifact-format.md` / `.pi/references/workflow-status-codes.md` scaffolding unless the implementation intentionally keeps it narrow and task-state-specific. Prior deferred work says broader artifact/status reference placement belongs to later scaffold/workflow stories.

### Recommended Task-State Schema

Use this as the minimum durable Markdown representation in the relevant story/spec/run artifact or parent guidance examples:

```yaml
tasks:
  - taskId: "task-01"
    title: "Implement approved story changes"
    targetAgent: "implementer"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "docs/_bmad-output/implementation-artifacts/<story-key>/<story-key>.md"
    dependsOn: []
    activeAgentId: null
    outputArtifact: null
    routingDecision: null
    cause: null
    recommendedNextAction: null
```

Required builder-facing status vocabulary:

- `pending` — task exists and is not yet dispatchable or not yet dispatched.
- `in-progress` — parent has selected the task and is dispatching or waiting for the target child agent.
- `completed` — child completed successfully and parent validation accepted the control-plane output/artifact state.
- `blocked` — automatic continuation is unsafe but the failure may be recoverable by human action or later retry.
- `failed` — task execution failed in a way that ends the current automated run.

Do not expose `running`, `complete`, `paused`, or `detached` as durable BMAD task states unless they are explicitly mapped to the fixed vocabulary. Current `pi-subagents` statuses use `running`/`complete` in several places; the Story 1.4 contract should normalize them before writing builder-facing Markdown state.

### Current Runtime and API Facts

- Project package pin: `.pi/settings.json` declares `npm:pi-subagents@0.24.2`. [Source: .pi/settings.json]
- Installed package metadata reports `pi-subagents` version `0.24.2`; its dev peer packages in the generated install reference Pi `0.74.0`, while planning docs still cite Pi `>=0.67.2` as the product baseline. Treat local package metadata as current for implementation details and planning docs as compatibility targets. [Source: .pi/npm/node_modules/pi-subagents/package.json] [Source: docs/_bmad-output/planning-artifacts/prd.md#Prerequisites]
- `pi-subagents` supports single-agent, parallel `tasks`, chain, async, status, interrupt, resume, output, reads, progress, model overrides, and agent-scope parameters. [Source: .pi/npm/node_modules/pi-subagents/README.md#Where-running-subagents-show-up]
- Parallel task inputs use `tasks: [{ agent, task, ... }]`; chain inputs use `chain: [{ agent, task }, { parallel: [...] }]`. [Source: .pi/npm/node_modules/pi-subagents/src/extension/schemas.ts]
- `AgentProgress.status` currently supports `pending`, `running`, `completed`, `failed`, and `detached`. [Source: .pi/npm/node_modules/pi-subagents/src/shared/types.ts#Progress-Tracking]
- Async run state and steps can use `queued`, `running`, `complete`, `completed`, `failed`, and `paused`. [Source: .pi/npm/node_modules/pi-subagents/src/shared/types.ts#AsyncStatus]
- Background runner writes step lifecycle transitions from pending to running to complete/failed in `status.json`; these are runtime status details, not durable BMAD task-state truth by themselves. [Source: .pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts]
- `output`/`outputMode: "file-only"`, `reads`, and chain `{previous}` output can support declared handoffs, but formal BMAD workflows should prefer artifact paths/read directives over lossy summaries when an artifact exists. [Source: .pi/npm/node_modules/pi-subagents/README.md#API-Reference]
- `progress: true` can write `progress.md`, but that is run/agent progress rather than the orchestrator's durable task list. Do not treat it as sufficient for AC1 by itself. [Source: .pi/npm/node_modules/pi-subagents/README.md#API-Reference]

### Existing Implementation Patterns to Preserve

- `.pi/skills/bmad-orchestrator/SKILL.md` is parent-session guidance, not a child-agent definition. It currently defines tool allowlist, parent/child boundaries, session policy, delegation defaults, dispatch evidence, context passing, review severity policy, and fail-closed result handling. [Source: .pi/skills/bmad-orchestrator/SKILL.md]
- Active formal BMAD dispatches must pass `context: "fresh"` explicitly and must block omitted context, `context: "fork"`, and `action: "resume"`. Story 1.4 must not weaken this policy. [Source: .pi/skills/bmad-orchestrator/SKILL.md#Session-Policy]
- Existing project wrapper agents are `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, and `.pi/agents/reviewer-b.md`; they are project agents and should not receive the `subagent` tool. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md#Current-Runtime-and-API-Facts]
- Provider-free tests already validate guidance text and package source behavior using Python `unittest` plus, where needed, `npx --yes tsx`. Follow this style for new task-state tests. [Source: tests/test_bmad_orchestrator_guidance.py] [Source: tests/test_fresh_context_session_policy.py] [Source: tests/test_subagent_model_task_summary.py]
- `.pi/npm/` is generated/ignored; durable package changes must be recorded in `.pi/patches/` and validated through `.pi/install-packages.sh`. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md#Current-Runtime-Package-and-Durability-Constraints]

### Likely Files to Modify

Expected primary changes:

```text
.pi/skills/bmad-orchestrator/SKILL.md
tests/test_orchestrator_task_routing_state.py
# or: tests/test_bmad_orchestrator_guidance.py
```

Possible active-workflow guidance changes if implementation finds direct routing examples that need the new task-list contract:

```text
.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md
.pi/skills/bmad-quick-dev/step-02-plan.md
.pi/skills/bmad-quick-dev/step-03-implement.md
.pi/skills/bmad-quick-dev/step-04-review.md
.pi/skills/bmad-code-review/steps/step-02-review.md
```

Only if runtime/package status or TUI/progress exposure is changed:

```text
.pi/npm/node_modules/pi-subagents/src/shared/types.ts
.pi/npm/node_modules/pi-subagents/src/runs/shared/parallel-utils.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/async-execution.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/subagent-runner.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/async-status.ts
.pi/npm/node_modules/pi-subagents/src/runs/background/run-status.ts
.pi/npm/node_modules/pi-subagents/src/tui/render.ts
.pi/patches/pi-subagents-0.24.2-orchestrator-task-state.patch
```

### Implementation Guardrails

- Do not build task routing as hidden runtime memory. The builder-facing task list must be written to the relevant Markdown artifact or to an explicitly named workflow-run Markdown artifact; guidance text alone is not enough unless it requires that durable write/read behavior.
- Do not let `pi-subagents` runtime statuses override Markdown truth. Runtime status is evidence; parent validation decides the durable task state.
- Do not dispatch a task unless dependencies are complete and context sources are present/readable.
- Do not pass previous child output to the next agent as a vague summary if an artifact path or saved output file exists.
- Do not continue routing after a `blocked` or `failed` task unless a human or later explicit workflow policy authorizes recovery.
- Do not use `paused` as a durable task status for Story 1.4; map it to `blocked` with cause `needs-human-or-control-action` unless a narrower policy is documented.
- Do not implement Story 1.5 UI rendering here. If a small runtime display change is needed, keep it strictly limited to exposing the existing task-state fields; defer widgets/activity-title polish.
- If adding a new central reference file, do not contradict the deferred plan for `.pi/references/artifact-format.md` and `.pi/references/workflow-status-codes.md` placeholders in later bootstrap/scaffold stories.

### Previous Story Intelligence

#### Story 1.1 — Generic Sub-Agent Dispatch

- Use marketplace `pi-subagents`; do not build a custom dispatch extension or `dispatch_subagent` tool. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Dev-Notes]
- Parent owns orchestration; child agents must not communicate horizontally or launch nested sub-agents. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Completion-Notes-List]
- Unknown-agent and child error handling should fail closed before Markdown state updates. Reuse that style for blocked/failed task states. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Review-Findings]

#### Story 1.2 — Agent Definitions and Model Routing

- Canonical dispatchable project agents live under `.pi/agents/`; workflow skills under `.pi/skills/` must not become child agents. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md#Dev-Notes]
- Runtime output/model routing evidence should record the effective agent/model without requiring custom source changes for every model assignment. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md#Completion-Notes-List]

#### Story 1.2.1 — Story-Scoped Implementation Artifacts

- New story artifacts must be written under `{implementation_artifacts}/{story_key}/{story_key}.md`; legacy flat story paths are read-only fallback compatibility. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md#Path-Convention-for-This-Story]
- Story-specific review outputs belong inside the story folder; root-level `sprint-status.yaml` and `deferred-work.md` may remain global. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md#Completion-Notes-List]

#### Story 1.2.2 — Subagent Model and Task Summary

- `pi-subagents@0.24.2` patch durability is now expected. Direct edits under `.pi/npm/node_modules` are regenerated and ignored unless captured as `.pi/patches/*.patch`. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md#Current-Runtime-Package-and-Durability-Constraints]
- Validation pattern includes full Python tests, `PI_TELEMETRY=0 pi list`, `git diff --check`, patch application when package patches change, and artifact cleanliness checks. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md#Completion-Notes-List]

#### Story 1.3 — Fresh-Context Session Policy

- Active v1 reuse/resume exception set is none for standard BMAD story/review dispatches. Story 1.4 must preserve this while adding task state. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md#Governing-Policy-for-This-Story]
- Formal workflow context remains artifact paths/read directives plus concise task text; no parent conversation, prior child output history, previous runtime transcript, or reviewer transcript may be appended. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md#Artifact-and-Context-Rules]
- Recent review follow-ups showed direct quick-dev sub-agent paths can bypass central policy if not explicitly tested. For Story 1.4, look for direct routing examples and add tests so they cannot bypass task-state updates. [Source: docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md#Senior-Developer-Review-AI]

### Recent Git Intelligence

Recent commits show the project is hardening prompt/guidance contracts and package patches rather than introducing broad runtime rewrites:

- `f450cd6 Enforce BMAD fresh context session policy`
- `23d3a29 Story 1-3 created dev-cycle prompt created`
- `81da900 Standardize review action item pass tags`
- `d049fef Implement subagent model and task summaries`
- `08ad12e Create story 1.2.2 and rename story 1.2 artifacts`

Actionable implications:

- Preserve existing story-folder artifact convention.
- Keep tests deterministic and provider-free.
- Prefer guidance-plus-tests unless runtime/package changes are necessary for the ACs.
- If package changes are necessary, use the established patch mechanism and update patch durability tests.

### Latest Technical Information

No external web lookup was available during story creation. Local/current technical facts are:

- `pi-subagents@0.24.2` is the active project-local package. [Source: .pi/settings.json] [Source: .pi/npm/node_modules/pi-subagents/package.json]
- Packaged `planner`, `worker`, and `oracle` can default to forked context when context is omitted; explicit `context: "fresh"` wins and remains mandatory for formal BMAD dispatch. [Source: .pi/npm/node_modules/pi-subagents/README.md#Recommended-orchestration-pattern-scaffolding]
- Pi extension docs in the local Pi install expose generic UI status/widget APIs, but no first-class task/todo-list API was identified locally. Treat Story 1.5 as the right place for richer TUI rendering. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md] [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/tui.md]

### Testing Requirements

Minimum validation expected before marking implementation complete:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PI_TELEMETRY=0 pi list
git diff --check
find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print
find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print
```

If `pi-subagents` package source is patched, also run:

```bash
bash .pi/install-packages.sh --patch
# plus patch apply/reverse or clean-restore validation appropriate to the changed patch
```

## Project Structure Notes

- Story artifact location for this story: `docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/1-4-add-orchestrator-task-routing-and-task-list-state.md`.
- Do not write `docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state.md`; that legacy flat path is read-only fallback compatibility only.
- Framework-owned runtime assets remain under `.pi/`.
- Global implementation-artifact files that may remain at root: `sprint-status.yaml`, `deferred-work.md`.
- `.pi/references/` is currently absent. Do not create broad reference scaffolding unless needed and explicitly scoped.

### References

- [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-4-Add-Orchestrator-Task-Routing-and-Task-List-State]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Communication-Patterns]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]
- [Source: .pi/skills/bmad-orchestrator/SKILL.md]
- [Source: .pi/npm/node_modules/pi-subagents/README.md]
- [Source: .pi/npm/node_modules/pi-subagents/src/shared/types.ts]

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Key implementation decision during dev: whether guidance plus provider-free tests fully satisfies task-list exposure for Story 1.4, or whether a narrow generic `pi-subagents` status/progress mapping patch is needed. If package code changes, use the existing version-scoped patch mechanism.

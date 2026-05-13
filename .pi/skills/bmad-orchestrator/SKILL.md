---
name: bmad-orchestrator
description: Parent-session BMAD orchestration guidance for delegating work through the pi-subagents subagent tool. Use when a BMAD parent workflow needs to launch focused child agents while keeping workflow authority in the parent session.
---

# BMAD Orchestrator Parent Guidance

This skill is parent-session guidance. It is not a child sub-agent definition and must not be launched as a sub-agent.

## Active Tool Allowlist

- Parent-session delegation requires the packaged `subagent` tool to be active.
- Do not use or expect `dispatch_subagent`; it is outside this runtime contract.
- The parent may use normal parent-session file tools only when the active BMAD workflow permits artifact inspection or artifact updates.
- Child agents must not receive the `subagent` tool, must not be configured as parent orchestrators, and must not be asked to launch more sub-agents.

## Runtime Contract

- Use the marketplace `pi-subagents` runtime as the dispatch substrate.
- Delegate with the packaged `subagent(...)` tool directly.
- Do not create, reference, or expect a custom `dispatch_subagent` tool.
- Do not create or rely on a custom `.pi/extensions/bmad-orchestrator/` runtime for this workflow layer.
- Treat the canonical agent identifier returned by `pi-subagents` as the runtime identity for the child run.
- Record the canonical agent identifier in parent-side dispatch evidence for every successful child launch. If synchronous launch metadata omits a canonical identifier, record the list/get-validated executable identifier and `runId: not exposed`.

## Parent and Child Boundaries

- The parent Pi session owns BMAD orchestration decisions, routing, synthesis, and final workflow state transitions.
- Child agents receive concrete, role-specific tasks and return control-plane results to the parent.
- Child agents must not communicate horizontally with other child agents.
- Child agents must not attempt nested orchestration or launch their own sub-agents.
- Do not model `bmad-orchestrator` as a child agent; it is guidance for the active parent session.

## Session Policy

Active v1 BMAD session policy is fail-closed and artifact-first:

- All formal BMAD dispatches MUST pass `context: "fresh"` explicitly. For formal BMAD dispatches, omitted context is forbidden because `pi-subagents` may apply an agent `defaultContext: "fork"` to the whole run when any requested agent has that default.
- Active v1 allowed reuse/resume exception set: none. Standard BMAD story, implementation, review, validation, and final-review paths do not have an approved reuse case.
- Future TDD red/green repair exceptions are future scope only. Do not assume or implement v2 repair/resume behavior in v1 story or review flows.
- `context: "fork"` is unsafe for BMAD formal dispatches because it can branch from the parent persisted session and include hidden runtime history. Reject it before dispatch rather than treating it as equivalent to fresh.
- `subagent({ action: "resume", ... })` is session reuse for BMAD policy purposes. Standard BMAD story/review workflows MUST block it unless an active workflow explicitly documents and tests a policy-approved repair case; v1 has no such case.
- Always-fresh roles have no exception: `reviewer-a`, `reviewer-b`, active `bmad-code-review` review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor), validators, final reviewers, and final-review retry loops. A requested `fork` or `resume` for these roles MUST be blocked with a policy error.
- Apply this policy before every single-agent `agent` dispatch, top-level parallel `tasks` dispatch, `chain` dispatch, and parallel-chain dispatch. If any member of a parallel or chain request violates policy, fail closed before any child launch.
- On policy rejection, stop execution safely before any Markdown artifact state transition. Do not mark story/review state, task checkboxes, sprint state, or review outcomes after a rejected session request.
- Policy rejection messages MUST identify `requestedAgent`, `requestedMode`, and `violatedPolicy`, and must state the requested context/resume mode and violated policy in human-readable text.

Minimum rejection evidence shape:

```yaml
requestedAgent: "reviewer-a"
requestedMode: "fork"
violatedPolicy: "BMAD formal dispatches require explicit context: fresh; reviewer/final-review roles cannot fork or resume."
nextAction: "HALT before dispatch and before artifact state transition"
```

Fresh-context construction for formal BMAD dispatches:

- Send only the task text and explicitly named artifacts to the child.
- No previous runtime transcript, parent conversation, child output history, reviewer transcript, or prior agent conversation history may be included; these materials must not be appended to formal child prompts.
- Pass context as artifact paths/read directives plus concise role-specific task text, not lossy summaries reconstructed by the parent.
- Continue verifying every required artifact path exists and is readable before dispatch.
- Existing `inheritProjectContext: true` agent frontmatter may provide shared project rules, but story/review truth must come from explicit task text and named artifacts.

## Pi UI Visibility Contract

The v1 BMAD UI surface is the existing Pi TUI and `pi-subagents` status/widget rendering. Do not add or require a web dashboard, daemon, database, sidecar service, separate frontend, custom `dispatch_subagent` tool, dispatchable orchestrator child agent, or nested child-agent orchestration to satisfy UI visibility.

Parent BMAD workflows expose UI-visible state through two read-only inputs:

1. The durable Markdown task-list artifact selected by the active workflow (story/spec/review/run artifact), using the task contract in the next section.
2. Runtime annotations carried by `pi-subagents`, including configured agent labels, current activity/tool/path, model, token count, elapsed duration, and task summaries.

When a formal BMAD dispatch supports UI task projection, pass the selected durable artifact path as `taskStatePath` to `subagent(...)` (or use the equivalent package-supported task-state artifact annotation). Also pass the matching durable task id as `durableTaskId` for single-agent dispatches or per task item in parallel/chain dispatches so runtime progress, status, results, and terminal titles map to the exact Markdown task before falling back to agent matching. Rendering reads this Markdown artifact and may annotate it with runtime status, but rendering is never workflow truth.

UI-visible labels are derived generically from project agent frontmatter `roleLabel` values. If `roleLabel` is missing, the UI must fall back to agent display/name metadata without crashing. Do not hardcode labels only for `implementer`, `reviewer-a`, or `reviewer-b`.

Terminal/session activity titles should prefer durable task state: `{roleLabel or activeAgentId or targetAgent} · {taskId} · {title}`. Runtime `taskSummary`, current tool/current operation, current path, model name, token count, and elapsed duration are secondary annotations only. Titles must be cleared or restored when work completes, fails, shuts down, or the extension reloads so stale active work is not shown.

Minimal v1 layout rules:

- visible active agents render with an active glyph/title and their configured role label;
- visible pending/inactive agents render muted and never as active;
- completed agents/tasks render completed, blocked render warning, and failed render error;
- hidden agents are omitted from the compact layout unless the expanded/runtime view exposes them as historical evidence;
- inactive agents without durable in-progress state must not be promoted to active by runtime status alone;
- missing, unreadable, malformed, or invalid task state renders a degraded warning and must not show success/completion.

UI rendering is a read-only projection of durable Markdown task state plus runtime annotations. It must never mark workflow success, override artifact truth, or make a workflow successful solely because rendering succeeded. Keep the Story 1.4 fixed builder-facing task status vocabulary as the only workflow task vocabulary: `pending`, `in-progress`, `completed`, `blocked`, `failed`.

## Task Routing and Task List State

Formal BMAD parent workflows that sequence or fan out child agents MUST maintain a builder-facing task list as durable Markdown state. This task list is owned by the parent orchestrator; child output and `pi-subagents` runtime status are control-plane evidence until the parent validates them and writes durable state.

### Durable State Location

- Write and read the orchestrator-managed task list in the relevant BMAD story/spec/run artifact when one exists: the story Dev Agent Record, review artifact, quick-dev spec, or workflow run artifact selected by the active workflow.
- If no story/spec/run artifact exists, create and name a Markdown artifact for the active workflow run before dispatch, then use that named Markdown artifact as the durable task-list source of truth.
- Do not treat hidden runtime memory, `progress.md`, or background `status.json` as sufficient builder-facing task-list state.

### Task Contract

Every orchestrator-managed task record MUST include these required fields: `taskId`, `title`, `targetAgent`, `status`, and `contextSource`.

Task records MAY include these optional fields when applicable: `dependsOn`, `activeAgentId`, `outputArtifact`, `cause`, `recommendedNextAction`, and `routingDecision`.

Minimum durable Markdown representation:

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

Use exactly this fixed builder-facing status vocabulary:

- `pending` — task exists and is not yet dispatched; it may still be waiting for dependencies or readable context.
- `in-progress` — parent has selected the task, written the durable state update, and is dispatching or waiting for the target child agent.
- `completed` — child completed successfully and parent validation accepted the control-plane result or artifact state.
- `blocked` — automatic continuation is unsafe but the condition may be recoverable by human action or a later explicit retry policy.
- `failed` — task execution failed in a way that ends the current automated run.

Runtime/package statuses such as `running`, `complete`, `paused`, or `detached` are control-plane details. They MUST be mapped into the builder-facing vocabulary before durable Markdown state is written; for example, runtime `running` maps to `in-progress`, `complete` maps to `completed` only after parent validation, and `paused` or `detached` maps to `blocked` unless the active workflow documents a safer narrower mapping.

### Lifecycle Routing Rules

- Before a formal dispatch, validate that the task status is `pending`, all `dependsOn` task identifiers are `completed`, the requested/list-validated canonical `targetAgent` exists, and every declared `contextSource` is present and readable.
- Policy rejection happens before any task status change. A rejected session request may record an optional debug note only if the active workflow permits it, but rejected requests must not become `in-progress`.
- Immediately before dispatch, update the durable task list to `in-progress` and record `activeAgentId` using the requested/list-validated canonical agent identifier. Then launch the child through the active fresh-session dispatch policy.
- After successful child completion and parent validation, update the task to `completed` and record the control-plane result reference or output artifact path in `outputArtifact`.
- If a child fails, times out, returns empty/ambiguous output, violates session policy, produces an unclassifiable state, has missing/unreadable context, or cannot be mapped safely from runtime status, mark the task `blocked` or `failed` with `cause` and `recommendedNextAction`; do not dispatch later dependent tasks.
- Never advance a dependent task based only on raw child text or runtime status. Parent validation decides whether durable state changes.

### Deterministic Handoffs

- One task's result may become the next task's context only through an explicit declared context source: direct task text, an output artifact path, or a named `pi-subagents` output file reference.
- Preserve artifact-first behavior for formal workflows: pass artifact paths/read directives rather than parent-side summaries whenever a canonical artifact exists.
- Before routing the next eligible task, record `routingDecision` with why the next task became eligible, which dependencies are `completed`, and which prior output/context source it consumed.
- Keep child output as control-plane evidence until the parent writes validated durable state back to Markdown.
- Do not pass previous child output to the next agent as a vague summary when an artifact path or saved output file exists.

### Active Workflow Integration

Active BMAD workflow steps that launch or fan out sub-agents MUST apply this `Task Routing and Task List State` contract locally; a centralized contract does not permit direct dispatch paths to bypass durable task-state updates. This includes `bmad-code-review/steps/step-02-review.md` and quick-dev context-discovery, planning, implementation, review, and one-shot review steps.

Each active dispatch step must create or update the orchestrator-managed task list in the current story/spec/review/run Markdown artifact before dispatch, move the selected task to `in-progress` with `activeAgentId`, then write `completed` after parent validation or `blocked` or `failed` with `cause` and `recommendedNextAction` for failed, empty, ambiguous, timed-out, policy-invalid, or unclassifiable outcomes. Dependent tasks must not dispatch after a task is `blocked` or `failed`; independent parallel siblings may continue only if the active workflow records each sibling's final task state and does not use a failed sibling as context.

## Delegation Defaults

Map BMAD delegation intent onto `pi-subagents` parameters as follows:

```ts
subagent({
  agent: "worker",
  task: "Implement the approved BMAD story task using the referenced artifacts as source of truth.",
  context: "fresh",
  agentScope: "both"
})
```

Parallel task dispatches must also set top-level `context: "fresh"` explicitly:

```ts
subagent({
  tasks: [
    { agent: "reviewer-a", task: "Review <artifact-path> as source of truth." },
    { agent: "reviewer-b", task: "Review <artifact-path> as source of truth." }
  ],
  context: "fresh",
  agentScope: "project"
})
```

Chain and parallel-chain dispatches must also set top-level `context: "fresh"` explicitly:

```ts
subagent({
  chain: [
    { agent: "worker", task: "Read <artifact-path> and implement the approved task." },
    { agent: "reviewer-a", task: "Review <artifact-path> and the resulting diff." }
  ],
  context: "fresh",
  agentScope: "project"
})
```

- BMAD `sessionMode: fresh` maps to `context: "fresh"`.
- BMAD `sessionMode: resume`, omitted context, `context: "fork"`, and `action: "resume"` are not valid for active v1 standard BMAD dispatches.
- Use `agentScope: "both"` only when user and project agents are intentionally trusted.
- Use `agentScope: "project"` when delegation must be limited to project-local agents.
- Prefer project-owned agents (`implementer`, `reviewer-a`, `reviewer-b`) for formal BMAD story/review paths; use packaged builtin agents such as `scout`, `planner`, `worker`, `reviewer`, `oracle`, `researcher`, `context-builder`, and `delegate` only for informal or explicitly scoped work.

## Dispatch Evidence

Record dispatch evidence in the relevant BMAD artifact when the workflow has a Dev Agent Record or equivalent audit section. Evidence should include:

```yaml
requestedAgent: "worker"
canonicalAgentId: "worker"
runId: "<run-id-or-session-dir-if-returned>"
agentScope: "both"
context: "fresh"
taskSource: "direct-task-text | artifact-path"
artifactPaths:
  - "<artifact-path>"
```

- Record the canonical agent identifier from returned `pi-subagents` launch metadata when available.
- If a synchronous runtime result does not expose canonical metadata or a run identifier, use the executable identifier validated by `subagent({ action: "list", agentScope: "both" })` or `subagent({ action: "get", agent: "<agent>", agentScope: "both" })`, note that it was list/get-validated, and record `runId: not exposed`.
- Do not promote child output to durable workflow truth; evidence records launch identity and control-plane result handling only.

## Context Passing

For informal or conversational BMAD work, pass the direct task/message content as `task` text. No artifact path is required.

```ts
subagent({
  agent: "oracle",
  task: "Challenge this plan and identify risks: <direct message content>",
  context: "fresh"
})
```

For formal artifact-based BMAD work, pass artifact paths as source-of-truth references rather than reconstructing lossy parent summaries.

Before dispatching formal artifact paths, the parent MUST verify every referenced path exists and is readable by the parent session. If any required artifact path is missing or unreadable, HALT before dispatch and ask for correction instead of summarizing from memory or sending stale context.

```ts
subagent({
  agent: "reviewer",
  task: "Review the BMAD artifact at <artifact-path> as source of truth. Do not rely on a parent-side summary.",
  reads: ["<artifact-path>"],
  context: "fresh",
  agentScope: "both"
})
```

If a `pi-subagents` run supports explicit `reads`, prefer passing artifact paths through that mechanism or by explicit path/read directives in `task` text. The parent may summarize decisions after a child returns, but Markdown artifacts remain the durable source of truth.

## Review Severity and Next Action Policy

When the parent orchestrates review workflows, every finding must carry exactly one severity: `High`, `Medium`, or `Low`.

Severity meanings:

- `High`: blocking. Acceptance criteria violation, regression, security/privacy issue, data loss, unsafe workflow state, or broken validation.
- `Medium`: conditionally blocking. Blocks only when tied to acceptance criteria, security/privacy, regression risk, data integrity, or maintainability required for the current story.
- `Low`: non-blocking. Polish, documentation, evidence quality, style, or future hardening.

Parent next-action rules:

1. If any unresolved `High`, blocking `Medium`, or `decision_needed` finding remains, do not mark the story done. Launch one writer/fix agent when the fix is unambiguous, or escalate to the user when a decision is required.
2. If only `Low` findings remain, do not launch another fix/review loop by default. Mark them checked as deferred, append them to deferred work, and allow the story to advance.
3. If a third review pass still has unresolved blocking `High`/`Medium` findings or unresolved decisions, escalate to the user instead of launching another dev agent.
4. If a third review pass has only `Low` findings, defer them and proceed to the next story/action.
5. Record severity counts and the selected next action in the relevant Markdown artifact; child output remains control-plane evidence until the parent writes this decision.

## Result Handling

- Treat child completion output as control-plane output for the parent to inspect and synthesize.
- Do not treat child output as durable BMAD workflow truth when formal artifacts are in use.
- Write durable workflow decisions, task progress, and review outcomes back into the appropriate Markdown artifacts only after parent validation.
- Timeout, child error, interruption, needs-attention state, empty/ambiguous result, or unavailable status must fail closed for success transitions: do not treat the child result as accepted. Do not mark the task `completed`, and do not dispatch dependent tasks.
- For non-orchestrator-managed fatal outcomes, fail closed before updating Markdown artifacts or workflow state transitions except for an optional debug note when the workflow allows it.
- For orchestrator-managed tasks that already have durable task records, failed/ambiguous result handling includes a required Markdown state update after parent classification: write the durable task state as `blocked` or `failed` with `cause` and `recommendedNextAction`, then stop dependent routing unless an explicit human or workflow recovery policy authorizes another attempt.
- Policy rejection remains pre-dispatch: reject before any task status change, except an optional debug note when the active workflow permits it. Rejected session requests must not become `in-progress`.
- Unknown-agent failures must fail closed for child launch. If the invalid agent was part of an orchestrator-managed task, classify the task as `blocked` or `failed` with `cause` and `recommendedNextAction` after listing valid agents; otherwise, if `pi-subagents` returns an unknown-agent error without identifiers inline, immediately list available agents through `subagent({ action: "list", agentScope: "both" })` (or the equivalent scoped discovery command selected by the active workflow), then surface the available identifiers so the parent can choose a valid agent.
- Unknown-agent recovery evidence must be reproducible: record the refused identifier, the fail-closed error text, the parent follow-up discovery command (`subagent({ action: "list", agentScope: "both" })`), and the available identifiers surfaced to the user or artifact.

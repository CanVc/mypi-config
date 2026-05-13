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
- Timeout, child error, interruption, needs-attention state, empty/ambiguous result, or unavailable status must fail closed before updating Markdown artifacts or workflow state transitions. Record only a debug note if the workflow allows it, then retry, resume/status-check, interrupt, or ask the user for guidance.
- Unknown-agent failures must fail closed. If `pi-subagents` returns an unknown-agent error without identifiers inline, immediately list available agents through `subagent({ action: "list", agentScope: "both" })` (or the equivalent scoped discovery command selected by the active workflow), then surface the available identifiers so the parent can choose a valid agent.
- Unknown-agent recovery evidence must be reproducible: record the refused identifier, the fail-closed error text, the parent follow-up discovery command (`subagent({ action: "list", agentScope: "both" })`), and the available identifiers surfaced to the user or artifact.

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

- BMAD `sessionMode: fresh` maps to `context: "fresh"`.
- Treat previous BMAD `sessionMode: resume` as out of scope unless explicitly using `pi-subagents` async `status`/`resume` behavior.
- Use `agentScope: "both"` only when user and project agents are intentionally trusted.
- Use `agentScope: "project"` when delegation must be limited to project-local agents.
- Prefer packaged builtin agents such as `scout`, `planner`, `worker`, `reviewer`, `oracle`, `researcher`, `context-builder`, and `delegate` until project-owned BMAD agents are defined.

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

## Result Handling

- Treat child completion output as control-plane output for the parent to inspect and synthesize.
- Do not treat child output as durable BMAD workflow truth when formal artifacts are in use.
- Write durable workflow decisions, task progress, and review outcomes back into the appropriate Markdown artifacts only after parent validation.
- Timeout, child error, interruption, needs-attention state, empty/ambiguous result, or unavailable status must fail closed before updating Markdown artifacts or workflow state transitions. Record only a debug note if the workflow allows it, then retry, resume/status-check, interrupt, or ask the user for guidance.
- Unknown-agent failures must fail closed. If `pi-subagents` returns an unknown-agent error without identifiers inline, immediately list available agents through `subagent({ action: "list", agentScope: "both" })` (or the equivalent scoped discovery command selected by the active workflow), then surface the available identifiers so the parent can choose a valid agent.
- Unknown-agent recovery evidence must be reproducible: record the refused identifier, the fail-closed error text, the parent follow-up discovery command (`subagent({ action: "list", agentScope: "both" })`), and the available identifiers surfaced to the user or artifact.

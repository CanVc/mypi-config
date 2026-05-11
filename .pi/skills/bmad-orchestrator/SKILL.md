---
name: bmad-orchestrator
description: Parent-session BMAD orchestration guidance for delegating work through the pi-subagents subagent tool. Use when a BMAD parent workflow needs to launch focused child agents while keeping workflow authority in the parent session.
---

# BMAD Orchestrator Parent Guidance

This skill is parent-session guidance. It is not a child sub-agent definition and must not be launched as a sub-agent.

## Runtime Contract

- Use the marketplace `pi-subagents` runtime as the dispatch substrate.
- Delegate with the packaged `subagent(...)` tool directly.
- Do not create, reference, or expect a custom `dispatch_subagent` tool.
- Do not create or rely on a custom `.pi/extensions/bmad-orchestrator/` runtime for this workflow layer.
- Treat the canonical agent identifier returned by `pi-subagents` as the runtime identity for the child run.

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

```ts
subagent({
  agent: "reviewer",
  task: "Review the BMAD story using this artifact path as source of truth: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md",
  context: "fresh",
  agentScope: "both"
})
```

If a `pi-subagents` run supports explicit `reads`, prefer passing artifact paths through that mechanism or by explicit path/read directives in `task` text. The parent may summarize decisions after a child returns, but Markdown artifacts remain the durable source of truth.

## Result Handling

- Treat child completion output as control-plane output for the parent to inspect and synthesize.
- Do not treat child output as durable BMAD workflow truth when formal artifacts are in use.
- Write durable workflow decisions, task progress, and review outcomes back into the appropriate Markdown artifacts.
- Unknown-agent failures must fail closed. If `pi-subagents` returns an unknown-agent error without identifiers inline, immediately list available agents through `subagent({ action: "list" })` or the equivalent subagent discovery command, then surface the available identifiers so the parent can choose a valid agent.

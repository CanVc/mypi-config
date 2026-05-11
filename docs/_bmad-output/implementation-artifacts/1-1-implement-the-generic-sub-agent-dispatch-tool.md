# Story 1.1: Integrate Pi Subagents for BMAD Agent Dispatch

Status: ready-for-dev

<!-- Note: This story was pivoted on 2026-05-11: use the marketplace `pi-subagents` runtime instead of building a custom dispatch extension first. -->

## Story

As a builder,
I want the BMAD parent orchestrator to delegate work through Pi's marketplace `pi-subagents` runtime,
so that BMAD workflows can launch focused sub-agents without maintaining custom role-specific or duplicate dispatch logic.

## Acceptance Criteria

1. Given the project does not yet declare a sub-agent runtime, when this story is implemented, then `pi-subagents` is added as a project-local Pi package with a pinned version and Pi can discover its `subagent` tool.
2. Given BMAD orchestration runs in the parent Pi session, when orchestration guidance is loaded, then it instructs the parent to use `subagent(...)` for delegation and does not introduce a custom `dispatch_subagent` tool or `.pi/extensions/bmad-orchestrator/` runtime.
3. Given the parent needs to delegate work, when it requests a known agent through `subagent`, then the launched child run records the canonical agent identifier returned by `pi-subagents`.
4. Given the parent requests an unknown agent, when `pi-subagents` validates the request, then the request is refused with an actionable unknown-agent message and available agent identifiers.
5. Given an informal or conversational BMAD workflow has no canonical artifact yet, when the parent delegates by passing direct task/message content, then the sub-agent receives that content as its task context and no artifact path is required.
6. Given a formal artifact-based BMAD workflow delegates work, when artifact context is needed, then the parent passes artifact paths to the child as paths/read directives rather than reconstructing lossy summaries in the parent.
7. Given a child run completes, when the parent receives the sub-agent result, then that result is treated as control-plane output only; durable workflow truth remains in Markdown artifacts when artifacts are part of the workflow.
8. Given `pi-subagents` prevents child sessions from becoming parent orchestrators by default, when defining BMAD orchestration guidance, then `bmad-orchestrator` is modeled as parent-session guidance, not as a child agent expected to call more sub-agents.

## Tasks / Subtasks

- [ ] Add `pi-subagents` as the project-local dispatch runtime. (AC: 1)
  - [ ] Update or create `.pi/settings.json` so `packages` includes a pinned `npm:pi-subagents@0.24.2` entry or the currently approved pinned version.
  - [ ] Do not install it only in global user settings; the dependency must travel with this project.
  - [ ] Verify Pi starts with the package and exposes the `subagent` tool / packaged commands.
- [ ] Replace the custom-dispatch implementation plan with parent-orchestrator guidance. (AC: 2, 8)
  - [ ] Do not create `.pi/extensions/bmad-orchestrator/package.json`, `src/index.ts`, or `dispatch-subagent.ts` in this story.
  - [ ] Create parent-session BMAD orchestration guidance as a Pi skill or prompt template, preferably `.pi/skills/bmad-orchestrator/SKILL.md` unless implementation discovers a better Pi-native parent-prompt location.
  - [ ] Guidance must say the parent uses `subagent(...)` directly for delegation.
  - [ ] Guidance must state that child agents must not communicate horizontally or attempt nested orchestration.
- [ ] Define the initial delegation contract on top of `pi-subagents`. (AC: 3-7)
  - [ ] Map BMAD `sessionMode: fresh` to `subagent` `context: "fresh"`.
  - [ ] Treat previous `sessionMode: resume` as out of scope for this story unless `pi-subagents` resume/status behavior is being used explicitly for an async run.
  - [ ] Use `agentScope: "both"` or `"project"` only when project-local agents are intentionally trusted.
  - [ ] Pass informal context as `task` text.
  - [ ] Pass formal artifact paths through task text and/or `reads` semantics supported by `pi-subagents`; do not summarize artifacts in this story.
- [ ] Provide a minimal known-agent path for smoke validation. (AC: 3, 4)
  - [ ] Prefer using packaged builtin agents (`scout`, `planner`, `worker`, `reviewer`, `oracle`, etc.) for the initial smoke if no BMAD project agents exist yet.
  - [ ] If a project fixture is needed, create only the smallest canonical kebab-case project agent under `.pi/agents/` required for smoke validation.
  - [ ] Do not implement the full BMAD agent roster here; detailed agent definitions and model routing belong to Story 1.2.
- [ ] Validate dispatch behavior with focused smoke checks. (AC: 1-7)
  - [ ] Verify available agents can be listed through `pi-subagents` discovery.
  - [ ] Verify a known-agent call succeeds using direct task content.
  - [ ] Verify an unknown-agent call fails with available identifiers.
  - [ ] Verify an artifact-path task can be passed without parent-side summarization.
  - [ ] Capture smoke evidence in the Dev Agent Record or a small implementation note.
- [ ] Preserve architecture boundaries. (AC: 7, 8)
  - [ ] Runtime package output is not durable workflow state.
  - [ ] Markdown artifacts remain source of truth for formal BMAD workflows.
  - [ ] No sidecar database or custom state file is introduced.

## Dev Notes

### Scope Boundary

This story establishes the sub-agent dispatch substrate for BMAD workflows by adopting `pi-subagents`. It should not build the previous custom `.pi/extensions/bmad-orchestrator/` TypeScript runtime.

The parent BMAD orchestrator is a guidance layer in the active parent Pi session. It may be represented as a skill or prompt template. It is not a child sub-agent that recursively launches other sub-agents, because `pi-subagents` intentionally constrains child sessions from acting as parent orchestrators.

Do **not** implement full workflow orchestration, transition rules, model routing, task-list state, UI widgets, standard BMAD story execution, or TDD/ATDD/TDAD workflow logic here. Those remain later stories.

### Current Repository State

- The repository currently has BMAD/Pi skills under `.pi/skills/`.
- `.pi/settings.json`, `.pi/agents/`, `.pi/prompts/`, and `.pi/references/` may be absent.
- The old Story 1.1 expected a custom `.pi/extensions/bmad-orchestrator/` package. That plan is superseded by this marketplace-runtime integration.
- Story 1.2 remains responsible for fuller BMAD agent definitions and model routing contracts.

### Technical Requirements

- Use `pi-subagents` from Pi packages as the dispatch runtime.
- Pin the package version in project settings to keep the story reproducible.
- Use project-local settings (`.pi/settings.json`) rather than global-only settings.
- Do not add root-level `node_modules`.
- Do not add a custom `dispatch_subagent` tool in this story.
- BMAD parent guidance should use the packaged `subagent` tool contract.
- Canonical names for project-owned agents and artifacts must remain lowercase kebab-case.

### Adopted Dispatch Shape

The story adopts the `pi-subagents` tool rather than the old custom contract.

Typical single-agent dispatch:

```ts
subagent({
  agent: "worker",
  task: "Implement the approved plan in docs/_bmad-output/...",
  context: "fresh",
  agentScope: "both"
})
```

Informal context:

```ts
subagent({
  agent: "oracle",
  task: "Challenge this plan: <direct message content>",
  context: "fresh"
})
```

Artifact-based context:

```ts
subagent({
  agent: "reviewer",
  task: "Review the story using artifact paths as source of truth: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md",
  context: "fresh",
  agentScope: "both"
})
```

If implementation uses `reads` or another `pi-subagents` file-read mechanism, pass artifact paths as paths and keep the parent from rewriting artifact contents into summaries.

### Architecture Compliance

- `pi-subagents` is the runtime substrate for launching child Pi sessions.
- BMAD parent-session guidance decides when and why to delegate.
- Later deterministic workflow rules may still require a BMAD-specific extension, but that is not Story 1.1.
- Markdown artifacts are the durable source of truth.
- Agent communication remains vertical through the parent/orchestrator.
- Child results are control-plane output and do not override artifact state.
- Ambiguous or unsafe formal workflow states should be escalated by later orchestration stories rather than interpreted freely here.

### File Structure Expectations

Expected additions are limited to configuration and parent guidance, for example:

```text
.pi/
  settings.json
  skills/
    bmad-orchestrator/
      SKILL.md
  agents/                 # optional in this story; minimal fixture only if needed
    <minimal-smoke-agent>.md
```

Do not create the obsolete custom extension scaffold:

```text
.pi/extensions/bmad-orchestrator/   # not for this story
```

### Testing / Smoke Requirements

Tests for this story are integration smoke checks rather than extension unit tests, because dispatch is provided by `pi-subagents`.

Smoke checks should prove:

- `pi-subagents` package is configured project-locally.
- Agents can be discovered/listed.
- Known-agent dispatch works with direct task content.
- Unknown-agent dispatch fails closed with useful allowed-agent information.
- Artifact-path context can be passed without parent-side summarization.
- Completion is recorded as control-plane evidence only.

No provider secrets should be committed. If a real model call is not available in the dev environment, capture the exact blocked smoke step and the static validation that was completed.

### References

- [Source: https://pi.dev/packages]
- [Source: https://pi.dev/packages/pi-subagents]
- [Source: npm package `pi-subagents@0.24.2` README]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/packages.md#Pi-Packages]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Extensions]
- [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-1-Implement-the-Generic-Sub-Agent-Dispatch-Tool]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Core-Architectural-Decisions]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns--Consistency-Rules]

## Dev Agent Record

### Agent Model Used

TBD by dev agent.

### Debug Log References

### Completion Notes List

### File List

## Create-Story Completion Status

Story pivoted from custom dispatch-extension implementation to project-local `pi-subagents` runtime integration with BMAD parent-session orchestration guidance.

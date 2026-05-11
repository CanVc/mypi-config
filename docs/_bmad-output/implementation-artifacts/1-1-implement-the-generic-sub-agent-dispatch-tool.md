# Story 1.1: Implement the Generic Sub-Agent Dispatch Tool

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a builder,
I want the Pi extension to dispatch named sub-agents through one generic tool,
so that workflows can route work to different agents without hardcoding role-specific launch logic.

## Acceptance Criteria

1. Given the `bmad-orchestrator` extension scaffold is available or created by this story, when a dispatch request is submitted with an agent identifier, session mode, task, and context input, then the extension validates the request shape and rejects missing or unknown required fields.
2. Given a valid dispatch request names a known agent, when dispatch executes, then the extension launches the requested agent through Pi and the runtime output records the canonical agent identifier.
3. Given a dispatch request names an unknown agent, when dispatch validation runs, then dispatch is refused and the error names the unknown agent and the allowed agent identifiers.
4. Given a workflow needs to pass informal context, when the dispatch request includes direct message content, then the sub-agent receives that content as its task context and no canonical artifact path is required for informal workflows.
5. Given dispatch completes, when the orchestrator receives the completion signal, then the signal is treated as control-plane output only and durable workflow truth remains in artifacts when artifacts are part of the workflow.

## Tasks / Subtasks

- [ ] Create the project-local extension skeleton if it does not already exist. (AC: 1)
  - [ ] Create `.pi/extensions/bmad-orchestrator/package.json` with extension-local scripts and dependencies only.
  - [ ] Create `.pi/extensions/bmad-orchestrator/tsconfig.json`.
  - [ ] Create `.pi/extensions/bmad-orchestrator/src/index.ts` as the Pi extension entry point.
  - [ ] Create `.pi/extensions/bmad-orchestrator/src/types.ts` for dispatch request/result types.
  - [ ] Create `.pi/extensions/bmad-orchestrator/src/dispatch-subagent.ts` for dispatch validation and process execution.
  - [ ] Create `.pi/extensions/bmad-orchestrator/tests/dispatch-subagent.test.ts` or equivalent test coverage.
- [ ] Register one generic Pi tool for sub-agent dispatch. (AC: 1, 4)
  - [ ] Tool name should be stable and workflow-agnostic, e.g. `dispatch_subagent`.
  - [ ] Tool parameters must include `agent`, `sessionMode`, `task`, and optional context inputs.
  - [ ] Support direct message content for informal workflows.
  - [ ] Support artifact path inputs without reading or summarizing artifact content in this story.
- [ ] Implement deterministic request validation. (AC: 1, 3)
  - [ ] Reject missing `agent`, `sessionMode`, or `task`.
  - [ ] Reject non-canonical agent identifiers; use lowercase kebab-case only.
  - [ ] Reject unknown agents by checking an allowed-agent registry or `.pi/agents/<agent>.md` presence.
  - [ ] Return errors that name the offending agent and allowed agent identifiers.
- [ ] Implement the first dispatch execution path. (AC: 2, 4)
  - [ ] Launch Pi as a subprocess or equivalent local runtime boundary for the named agent.
  - [ ] Ensure dispatch code records the canonical agent identifier in the result.
  - [ ] Pass direct message content as task context when provided.
  - [ ] Pass artifact paths as paths, not lossy summaries.
- [ ] Preserve control-plane vs artifact-truth boundaries. (AC: 5)
  - [ ] Dispatch result may report exit/completion status and captured output metadata.
  - [ ] Do not treat subprocess success as durable workflow completion when artifact workflows are in use.
  - [ ] Do not create sidecar durable state files as the source of truth.
- [ ] Add focused tests for dispatch validation and result shape. (AC: 1-5)
  - [ ] Valid request with known agent succeeds in dry-run/mock mode.
  - [ ] Missing required fields fail with actionable messages.
  - [ ] Unknown agent fails with allowed-agent list.
  - [ ] Informal message context is accepted without artifact paths.
  - [ ] Result includes canonical agent identifier and treats completion as control-plane output.

## Dev Notes

### Scope Boundary

This story is the first runtime story. It should create only the foundation needed for generic dispatch. Do **not** implement full workflow orchestration, model routing, fresh-context policy, task-list state, UI widgets, or standard BMAD story execution here; those belong to later Epic 1 and Epic 3 stories.

Expected output is a small, testable dispatch foundation inside `.pi/extensions/bmad-orchestrator/`.

### Current Repository State

- The repository currently has BMAD/Pi skills under `.pi/skills/`.
- The runtime scaffold directories `.pi/extensions/`, `.pi/agents/`, and `.pi/references/` may be absent or incomplete. This story may create the extension folder required for dispatch.
- Do not modify installed BMAD base skills unless directly required for this story.
- A previous old Story 1.1 file referenced bootstrap-first sequencing; it is obsolete after the runtime-first correction.

### Technical Requirements

- Use TypeScript for the Pi extension and Markdown only for agent/workflow artifacts.
- The extension must be project-local under `.pi/extensions/bmad-orchestrator/`.
- Pi discovers project-local extensions from `.pi/extensions/*/index.ts`; package-style extensions may declare a `pi.extensions` entry in `package.json` pointing to `./src/index.ts`.
- Extension dependencies must stay inside `.pi/extensions/bmad-orchestrator/` and must not require root-level `node_modules`.
- Use `@earendil-works/pi-coding-agent` types and `typebox` schemas for `pi.registerTool()` parameters.
- Use Node.js built-ins such as `node:child_process`, `node:fs`, and `node:path` as needed.
- Prefer dependency-free implementation for this story unless a dependency is clearly necessary.

### Proposed Dispatch Contract

Use this shape unless implementation discovers a Pi-native better equivalent:

```ts
type DispatchRequest = {
  agent: string; // canonical lowercase kebab-case, e.g. "implementer"
  sessionMode: "fresh" | "resume";
  task: string;
  context?: {
    message?: string;
    artifacts?: string[];
  };
};

type DispatchResult = {
  agent: string;
  sessionMode: "fresh" | "resume";
  status: "completed" | "failed";
  controlPlaneOnly: true;
  exitCode?: number;
  output?: string;
  error?: string;
};
```

Validation in this story should accept the contract and enforce shape/agent identity. Later stories may tighten `sessionMode` semantics and model routing.

### Architecture Compliance

- Markdown artifacts are the durable source of truth. Runtime completion signals are control-plane only.
- Agent communication must remain vertical through the orchestrator/runtime; agents must not communicate directly with one another.
- The extension layer is the deterministic orchestration surface; do not make an LLM `orchestrator.md` role authoritative.
- Ambiguous or unsafe states should fail closed with actionable errors rather than being interpreted freely.
- Canonical names use lowercase kebab-case for agents, artifacts, and reference files.

### File Structure Requirements

Create or update only files needed for the dispatch foundation:

```text
.pi/
  extensions/
    bmad-orchestrator/
      package.json
      tsconfig.json
      src/
        index.ts
        dispatch-subagent.ts
        types.ts
      tests/
        dispatch-subagent.test.ts
```

Do not create the complete future scaffold unless necessary. In particular:

- `.pi/agents/` may be created only if needed for known-agent fixture/lookup behavior.
- `.pi/references/` files are important architecture artifacts but should be created only if needed by this story's tests or dispatch contract; otherwise they can be handled by the next appropriate story.
- Bootstrap scripts belong to Epic 2, not this story.

### Testing Requirements

- Add extension-local tests for validation and dispatch result behavior.
- Tests may mock subprocess execution; do not require real model-provider calls.
- Tests must be runnable from `.pi/extensions/bmad-orchestrator/` without root-level dependencies.
- If a test framework is introduced, keep it in the extension package and wire it through `package.json` scripts.
- Do not require provider API keys or committed secrets.

### Implementation Guidance

- Build the smallest reliable vertical slice: tool registration + validation + mockable dispatch function.
- Keep `dispatch-subagent.ts` workflow-agnostic. It should not know about `dev-story`, `code-review`, TDD batches, or specific BMAD flows.
- Separate pure validation from process execution so tests can cover validation deterministically.
- Error messages should be actionable and include the rejected field/path/agent.
- If using subprocess execution, ensure command arguments are passed safely as an array, not shell-concatenated strings.

### Project Structure Notes

- The full architecture target includes `.pi/settings.json`, `.pi/references/`, `.pi/agents/`, `.pi/skills/`, `.pi/extensions/bmad-orchestrator/`, and helper scripts, but this story should focus on the dispatch extension foundation only.
- Durable workflow artifacts later live under `docs/_bmad-output/implementation-artifacts/stories/<story-id>/`; this story itself is stored at `docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md` because that is the current sprint tracking convention.
- No separate UI, web frontend, Docker service, database, or hosted infrastructure is required.

### References

- [Source: docs/_bmad-output/planning-artifacts/epics.md#Epic-1-Observable-Pi-Multi-Agent-Runtime]
- [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-1-Implement-the-Generic-Sub-Agent-Dispatch-Tool]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Core-Architectural-Decisions]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns--Consistency-Rules]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Project-Structure--Boundaries]
- [Source: docs/_bmad-output/planning-artifacts/prd.md#MVP-Feature-Set--v1]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md#Extensions]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/with-deps/index.ts]
- [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/reload-runtime.ts]

## Dev Agent Record

### Agent Model Used

TBD by dev agent.

### Debug Log References

### Completion Notes List

### File List

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

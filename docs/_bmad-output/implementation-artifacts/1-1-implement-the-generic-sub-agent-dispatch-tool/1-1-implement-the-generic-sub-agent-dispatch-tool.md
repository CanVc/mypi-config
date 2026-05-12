# Story 1.1: Integrate Pi Subagents for BMAD Agent Dispatch

Status: done

<!-- Note: This story was pivoted on 2026-05-11: use the marketplace `pi-subagents` runtime instead of building a custom dispatch extension first. -->

## Story

As a builder,
I want the BMAD parent orchestrator to delegate work through Pi's marketplace `pi-subagents` runtime,
so that BMAD workflows can launch focused sub-agents without maintaining custom role-specific or duplicate dispatch logic.

## Acceptance Criteria

1. Given the project does not yet declare a sub-agent runtime, when this story is implemented, then `pi-subagents` is added as a project-local Pi package with a pinned version and Pi can discover its `subagent` tool.
2. Given BMAD orchestration runs in the parent Pi session, when orchestration guidance is loaded, then it instructs the parent to use `subagent(...)` for delegation and does not introduce a custom `dispatch_subagent` tool or `.pi/extensions/bmad-orchestrator/` runtime.
3. Given the parent needs to delegate work, when it requests a known agent through `subagent`, then the launched child run records the canonical agent identifier from returned metadata when available; when launch metadata omits a canonical identifier, the parent records the list/get-validated canonical identifier with `runId: not exposed` for synchronous runs.
4. Given the parent requests an unknown agent, when `pi-subagents` validates the request, then the request is refused with an actionable unknown-agent message; the parent then immediately runs `subagent({ action: "list", agentScope: "both" })` and surfaces the returned valid identifiers.
5. Given an informal or conversational BMAD workflow has no canonical artifact yet, when the parent delegates by passing direct task/message content, then the sub-agent receives that content as its task context and no artifact path is required.
6. Given a formal artifact-based BMAD workflow delegates work, when artifact context is needed, then the parent passes artifact paths to the child as paths/read directives rather than reconstructing lossy summaries in the parent.
7. Given a child run completes, when the parent receives the sub-agent result, then that result is treated as control-plane output only; durable workflow truth remains in Markdown artifacts when artifacts are part of the workflow.
8. Given `pi-subagents` prevents child sessions from becoming parent orchestrators by default, when defining BMAD orchestration guidance, then `bmad-orchestrator` is modeled as parent-session guidance, not as a child agent expected to call more sub-agents.

## Tasks / Subtasks

- [x] Add `pi-subagents` as the project-local dispatch runtime. (AC: 1)
  - [x] Update or create `.pi/settings.json` so `packages` includes a pinned `npm:pi-subagents@0.24.2` entry or the currently approved pinned version.
  - [x] Do not install it only in global user settings; the dependency must travel with this project.
  - [x] Verify Pi starts with the package and exposes the `subagent` tool / packaged commands.
- [x] Replace the custom-dispatch implementation plan with parent-orchestrator guidance. (AC: 2, 8)
  - [x] Do not create `.pi/extensions/bmad-orchestrator/package.json`, `src/index.ts`, or `dispatch-subagent.ts` in this story.
  - [x] Create parent-session BMAD orchestration guidance as a Pi skill or prompt template, preferably `.pi/skills/bmad-orchestrator/SKILL.md` unless implementation discovers a better Pi-native parent-prompt location.
  - [x] Guidance must say the parent uses `subagent(...)` directly for delegation.
  - [x] Guidance must state that child agents must not communicate horizontally or attempt nested orchestration.
- [x] Define the initial delegation contract on top of `pi-subagents`. (AC: 3-7)
  - [x] Map BMAD `sessionMode: fresh` to `subagent` `context: "fresh"`.
  - [x] Treat previous `sessionMode: resume` as out of scope for this story unless `pi-subagents` resume/status behavior is being used explicitly for an async run.
  - [x] Use `agentScope: "both"` or `"project"` only when project-local agents are intentionally trusted.
  - [x] Pass informal context as `task` text.
  - [x] Pass formal artifact paths through task text and/or `reads` semantics supported by `pi-subagents`; do not summarize artifacts in this story.
- [x] Provide a minimal known-agent path for smoke validation. (AC: 3, 4)
  - [x] Prefer using packaged builtin agents (`scout`, `planner`, `worker`, `reviewer`, `oracle`, etc.) for the initial smoke if no BMAD project agents exist yet.
  - [x] If a project fixture is needed, create only the smallest canonical kebab-case project agent under `.pi/agents/` required for smoke validation.
  - [x] Do not implement the full BMAD agent roster here; detailed agent definitions and model routing belong to Story 1.2.
- [x] Validate dispatch behavior with focused smoke checks. (AC: 1-7)
  - [x] Verify available agents can be listed through `pi-subagents` discovery.
  - [x] Verify a known-agent call succeeds using direct task content.
  - [x] Verify an unknown-agent call fails closed, then the parent immediately runs `subagent({ action: "list", agentScope: "both" })` and surfaces the returned valid identifiers.
  - [x] Verify an artifact-path task can be passed without parent-side summarization.
  - [x] Capture smoke evidence in the Dev Agent Record or a small implementation note.
- [x] Preserve architecture boundaries. (AC: 7, 8)
  - [x] Runtime package output is not durable workflow state.
  - [x] Markdown artifacts remain source of truth for formal BMAD workflows.
  - [x] No sidecar database or custom state file is introduced.

### Review Findings

- [x] [Review][Defer] Artifact/status reference contract placement belongs to later scaffold/workflow stories — deferred, not required for Story 1.1. Placement agreed: placeholders in Story 2.1, minimal standard-workflow semantics in Story 3.1/3.3 if needed, and full TDD artifact/status semantics in Story 4.2/4.7.
- [x] [Review][Patch] Unknown-agent available-identifiers contract needs explicit parent-follow-up evidence — AC4 is accepted as satisfied via parent-mediated recovery: the runtime fails closed on the unknown agent, then the parent immediately lists available identifiers and surfaces them. Patch the story/guidance evidence so this interpretation is explicit and reproducible.
- [x] [Review][Patch] `.pi/npm/.gitignore` is omitted from the Dev Agent Record File List [.pi/npm/.gitignore:1]
- [x] [Review][Patch] Canonical agent identifier recording is stated but not implemented or verified [.pi/skills/bmad-orchestrator/SKILL.md:16]
- [x] [Review][Patch] Artifact-path delegation does not require existence/readability validation before dispatch [.pi/skills/bmad-orchestrator/SKILL.md:45]
- [x] [Review][Patch] Child run timeout/error handling does not explicitly fail closed before workflow state updates [.pi/skills/bmad-orchestrator/SKILL.md:70]
- [x] [Review][Patch] Parent guidance lacks an explicit active-tool allowlist [.pi/skills/bmad-orchestrator/SKILL.md:1]
- [x] [Review][Patch] Framework guidance hardcodes this repo's Story 1.1 artifact path instead of using a portable placeholder [.pi/skills/bmad-orchestrator/SKILL.md:57]
- [x] [Review][Patch] AC4 wording still says the unknown-agent refusal itself includes available identifiers, but recorded runtime behavior uses parent-mediated discovery follow-up [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:18]
- [x] [Review][Patch] AC3 lacks dispatch evidence for an actual launched child run recording the canonical agent identifier [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:17]
- [x] [Review][Patch] Review-skill behavior edits are changed but not justified or listed in the Dev Agent Record File List [.agents/skills/bmad-review-adversarial-general/SKILL.md:27]
- [x] [Review][Patch] Generated Python bytecode is untracked and Python bytecode is not ignored [.gitignore:1]
- [x] [Review][Patch] Debug log wording says there is no test suite while this patch adds one [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:213]
- [x] [Review][Patch] AC4 remains contradicted because acceptance criteria and smoke task still say the unknown-agent refusal includes identifiers, while evidence uses parent-mediated discovery follow-up [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:18]
- [x] [Review][Patch] AC3 should explicitly allow list/get-validated canonical identifiers when a launch result omits canonical metadata [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:17]
- [x] [Review][Patch] New regression test couples Story 1.1 to an out-of-scope review skill instead of validating Story 1.1 artifacts only [tests/test_bmad_orchestrator_guidance.py]
- [x] [Review][Patch] Ignored Python bytecode still exists, contradicting cleanup evidence [tests/__pycache__/test_bmad_orchestrator_guidance.cpython-312.pyc]
- [x] [Review][Defer][Low][Pass 3] Parent guidance should explicitly verify `subagent` is listed/active before delegation and HALT without state updates if unavailable [.pi/skills/bmad-orchestrator/SKILL.md:12] — deferred as non-blocking hardening for a later orchestration quality-gate story.
- [x] [Review][Defer][Medium][Pass 3] Artifact-path validation should constrain resolved paths to approved BMAD artifact roots, not only readability [.pi/skills/bmad-orchestrator/SKILL.md:86] — deferred as security/process hardening beyond Story 1.1's initial dispatch substrate scope.
- [x] [Review][Defer][Low][Pass 3] Live child dispatch identity evidence omits agentScope/context/taskSource, reducing reproducibility [docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md:228] — deferred as evidence-quality hardening; current AC3 fallback evidence is sufficient for Story 1.1.

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
- Unknown-agent dispatch fails closed first; the parent then immediately runs `subagent({ action: "list", agentScope: "both" })` and surfaces the returned valid identifiers.
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

Pi coding agent session (model identifier not exposed by harness).

### Implementation Plan

1. Configure the project-local Pi package list with pinned `npm:pi-subagents@0.24.2`.
2. Add parent-session BMAD orchestration guidance as a Pi skill, not a child agent or custom extension.
3. Encode the initial delegation contract in the guidance: fresh context mapping, agent scope rules, direct task text, artifact path passing, control-plane result handling, and child orchestration boundaries.
4. Address review patch findings by tightening the parent guidance for active tool allowlisting, canonical dispatch evidence, artifact-path validation, child timeout/error fail-closed handling, portable artifact placeholders, and reproducible unknown-agent recovery evidence.
5. Validate package discovery and smoke constraints with static checks, `pi list`, `subagent` discovery/unknown-agent checks, and focused Python regression tests.

### Debug Log References

- RED check: `.pi/settings.json` was absent and the pinned package assertion failed before implementation.
- GREEN check: `jq -e '.packages[]? == "npm:pi-subagents@0.24.2"' .pi/settings.json` passed; `pi list` reported `Project packages: npm:pi-subagents@0.24.2`.
- Pi startup/tool discovery check: `PI_TELEMETRY=0 pi --offline --no-builtin-tools --tools subagent --no-session --provider openai --api-key dummy --model gpt-4o-mini -p "Say OK without using tools."` reached the provider request and failed only on the intentional dummy API key, confirming startup accepted the `subagent` tool allowlist.
- Parent guidance validation: Python static assertions verified `subagent(...)`, no custom `dispatch_subagent`, no `.pi/extensions/bmad-orchestrator/`, child no-horizontal/no-nested-orchestration boundaries, fresh context mapping, scope rules, artifact path handling, control-plane result handling, and Markdown source-of-truth guidance.
- Package smoke validation: `npm pack pi-subagents@0.24.2` inspection verified packaged builtin agents (`scout`, `planner`, `worker`, `reviewer`, `oracle`, `delegate`), `SubagentParams` schema support for `task`, `context`, `agentScope`, and `reads`, list-action output that enumerates executable agents, and fail-closed unknown-agent validation.
- Live sub-agent smoke: `PI_TELEMETRY=0 pi --offline --no-session -p '/run scout "Return exactly: SUBAGENT_SMOKE_OK"'` returned `SUBAGENT_SMOKE_OK`.
- Live discovery smoke: `PI_TELEMETRY=0 pi --offline --no-session -p 'Show me available subagents. Only list names.'` returned `context-builder`, `delegate`, `oracle`, `planner`, `researcher`, `reviewer`, `scout`, and `worker`.
- Live unknown-agent smoke: `PI_TELEMETRY=0 pi --offline --no-session -p '/run definitely-unknown-agent "Return OK"'` failed closed with `Unknown agent: definitely-unknown-agent`. Because the runtime response did not include available identifiers inline, parent guidance was tightened to require an immediate list/discovery follow-up and surface available identifiers to the user.
- Live artifact-path smoke: `PI_TELEMETRY=0 pi --offline --no-session -p '/run reviewer "Read this artifact path as source of truth, do not summarize from parent context: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md. Return exactly ARTIFACT_PATH_RECEIVED if you can see the path instruction."'` returned `ARTIFACT_PATH_RECEIVED`.
- Regression/static validation: repository has no root `package.json`, `pyproject.toml`, `Cargo.toml`, or `Makefile`, and had no pre-existing project-level unit test suite before the focused Story 1.1 regression tests were added; final static smoke validation and `pi list` passed.
- RED review-patch check: `python3 -m unittest tests/test_bmad_orchestrator_guidance.py` initially failed because active-tool allowlist, canonical dispatch evidence, artifact validation, timeout/error fail-closed handling, unknown-agent recovery evidence, portable artifact placeholder, and `.pi/npm/.gitignore` File List coverage were not yet present.
- GREEN review-patch checks: `.pi/skills/bmad-orchestrator/SKILL.md` now declares parent active-tool allowlist, excludes `subagent` from children, records `requestedAgent`/`canonicalAgentId`/`runId` evidence, validates formal artifact paths for existence/readability before dispatch, uses `<artifact-path>` instead of a Story 1.1 hard-coded path, and fails closed on child timeout/error before Markdown state updates.
- Parent unknown-agent recovery evidence: `subagent({ agent: "definitely-unknown-agent", task: "Return OK.", context: "fresh", agentScope: "both" })` failed closed with `Unknown agent: definitely-unknown-agent`; immediate follow-up `subagent({ action: "list", agentScope: "both" })` surfaced available identifiers including `context-builder`, `delegate`, `oracle`, `planner`, `researcher`, `reviewer`, `scout`, and `worker`.
- AC4 evidence is parent-mediated: the runtime fail-closed error does not expose available identifiers inline, so the reproducible recovery contract is fail closed first, then run `subagent({ action: "list", agentScope: "both" })` and surface the resulting valid identifiers to the parent/user.
- Canonical identifier evidence check: `subagent({ action: "get", agent: "worker", agentScope: "both" })` resolved canonical executable identifier `worker` from the builtin agent path.
- Live child dispatch identity evidence: prior `/run scout "Return exactly: SUBAGENT_SMOKE_OK"` launched the builtin child and returned `SUBAGENT_SMOKE_OK`; dispatch identity is recorded as `requestedAgent: "scout"`, `canonicalAgentId: "scout"` (list-validated from discovery output), `runId: not exposed` because this synchronous command did not return run metadata.
- Static/package checks: `PI_TELEMETRY=0 pi list` still reports `Project packages: npm:pi-subagents@0.24.2`; shell validation confirmed no `.pi/extensions/bmad-orchestrator/` directory, `.pi/npm/.gitignore` is readable, and the guidance contains `<artifact-path>` with no Story 1.1 hard-coded artifact path.
- Final regression: `python3 -m unittest tests/test_bmad_orchestrator_guidance.py` passed all focused guidance/File List regression tests.
- Final full test discovery: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` passed 12 focused regression tests.
- Final package/static validation: `PI_TELEMETRY=0 pi list` reported `Project packages: npm:pi-subagents@0.24.2`, and `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` returned no generated bytecode artifacts.
- Review-skill scope correction: out-of-scope edits to `.agents/`, `.claude/`, and `.pi/` `bmad-review-adversarial-general` skills were reverted instead of justified/listed as Story 1.1 changes.
- Python bytecode cleanup: removed generated `tests/__pycache__/` artifacts and added repository `.gitignore` rules for `__pycache__/` and `*.py[cod]`.
- Follow-up patch correction: AC4 and smoke wording now state fail-closed unknown-agent refusal followed by immediate parent-mediated `subagent({ action: "list", agentScope: "both" })` discovery; AC3 now allows returned metadata when available or list/get-validated canonical identifiers with `runId: not exposed` for synchronous runs.
- Follow-up regression correction: removed the out-of-scope `.agents/skills/bmad-review-adversarial-general/SKILL.md` file read from `tests/test_bmad_orchestrator_guidance.py` and replaced it with Story 1.1 artifact/File List assertions.
- Follow-up validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` passed 12 tests; `PI_TELEMETRY=0 pi list` still reports `npm:pi-subagents@0.24.2`; bytecode search returned no `__pycache__`, `*.pyc`, or `*.pyo` artifacts.
- Human triage after review pass 3 classified the remaining findings as non-blocking deferred work: two Low evidence/process hardening items and one Medium artifact-root hardening item. Story 1.1 is complete because all acceptance criteria for the initial dispatch substrate are satisfied.

### Completion Notes List

- Added project-local `.pi/settings.json` with pinned `npm:pi-subagents@0.24.2`; no root-level `node_modules` was created.
- Added `.pi/skills/bmad-orchestrator/SKILL.md` as parent-session orchestration guidance that delegates through `subagent(...)` directly and explicitly avoids the obsolete custom dispatch extension/runtime.
- Documented the BMAD-on-`pi-subagents` delegation contract: `sessionMode: fresh` to `context: "fresh"`, resume out of scope except explicit async status/resume use, `agentScope` trust rules, direct informal task content, artifact-path source-of-truth passing, fail-closed unknown-agent handling with discovery follow-up, and control-plane-only child results.
- Used packaged builtin agents as the minimal known-agent path for smoke validation; no project fixture agent or full BMAD roster was added.
- Preserved architecture boundaries: parent owns orchestration, child agents must not communicate horizontally or perform nested orchestration, and durable workflow truth remains in Markdown artifacts.
- Resolved review patch findings by adding an explicit parent active-tool allowlist, child `subagent` exclusion, canonical dispatch evidence fields, artifact existence/readability validation, child timeout/error fail-closed guidance, and a portable `<artifact-path>` example.
- Made AC4 reproducible through parent-mediated unknown-agent recovery evidence: fail closed on the unknown identifier, immediately list available agents, and surface valid identifiers.
- Added focused Python regression tests for the patched guidance, AC4 parent-mediated recovery evidence, AC3 canonical dispatch identity evidence, Python bytecode ignore rules, debug wording, and File List coverage.
- Reverted out-of-scope review-skill behavior edits rather than expanding Story 1.1 scope, and removed the regression test's direct dependency on that out-of-scope skill file.
- Added Python bytecode ignore rules and removed generated bytecode/cache artifacts.
- Resolved follow-up patch findings by aligning AC3/AC4 and smoke wording with observed `pi-subagents` behavior and rerunning validation with bytecode disabled.
- Deferred the three pass-3 hardening findings as future work rather than blockers: active-tool preflight, artifact-root allowlisting, and richer dispatch-evidence fields.

### File List

- `.gitignore`
- `.pi/settings.json`
- `.pi/npm/.gitignore`
- `.pi/skills/bmad-orchestrator/SKILL.md`
- `tests/test_bmad_orchestrator_guidance.py`
- `docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md`
- `docs/_bmad-output/implementation-artifacts/deferred-work.md`
- `docs/_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- 2026-05-11: Integrated project-local `pi-subagents` runtime configuration and parent-session BMAD orchestration guidance.
- 2026-05-11: Added live sub-agent smoke evidence and tightened unknown-agent discovery follow-up guidance.
- 2026-05-11: Addressed review patch findings for active tool allowlist, canonical identifier evidence, artifact validation, child fail-closed handling, portable artifact placeholder, File List completeness, and regression coverage.
- 2026-05-11: Addressed follow-up review patch findings for AC4 parent-mediated evidence, AC3 live child identity evidence without exposed run metadata, out-of-scope review-skill reversion, Python bytecode cleanup/ignore rules, and debug log wording.
- 2026-05-11: Addressed second follow-up patch findings for AC4/AC3 acceptance wording, unknown-agent smoke wording, Story 1.1-only regression coverage, and bytecode-disabled validation.
- 2026-05-11: Classified remaining pass-3 findings as deferred future hardening and marked Story 1.1 done.

## Create-Story Completion Status

Story pivoted from custom dispatch-extension implementation to project-local `pi-subagents` runtime integration with BMAD parent-session orchestration guidance.

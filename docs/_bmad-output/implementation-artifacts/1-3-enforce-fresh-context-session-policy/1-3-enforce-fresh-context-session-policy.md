# Story 1.3: Enforce Fresh-Context Session Policy

Status: done

<!-- Ultimate context engine analysis completed - comprehensive developer guide created. -->

## Story

As a builder,
I want sub-agents to start with fresh context by default,
so that workflow stages do not inherit hidden conversation history or drift across tasks.

## Acceptance Criteria

1. Given a dispatch request does not explicitly request an allowed resume case, when the sub-agent is launched, then the parent delegates with `pi-subagents` fresh-context behavior and prior agent conversation history is not included.
2. Given the workflow requests session reuse, when session policy validates the request, then reuse is allowed only for explicitly documented repair/resume cases and all other reuse requests are rejected or routed through `pi-subagents` fresh context.
3. Given a validator or final reviewer is dispatched, when session policy is applied, then the session is always fresh and any requested resume mode is ignored or blocked with a policy error.
4. Given a `subagent(...)` invocation includes artifact paths, when fresh context is assembled, then the sub-agent receives only the task and explicitly named artifacts and no previous runtime transcript is appended.
5. Given session policy rejects a request, when the orchestrator receives the rejection, then execution stops safely and the message identifies the requested agent, requested context/resume mode, and violated policy.

## Tasks / Subtasks

- [x] Define the active v1 session policy in parent BMAD orchestration guidance. (AC: 1, 2, 3, 5)
  - [x] Update `.pi/skills/bmad-orchestrator/SKILL.md` with an explicit `Session Policy` section.
  - [x] State that all BMAD dispatches must pass `context: "fresh"` explicitly; omitted context is forbidden for formal BMAD dispatches.
  - [x] State that current v1 standard BMAD workflows have no allowed reuse/resume exception; future TDD red/green repair exceptions are documented future scope, not active v1 behavior.
  - [x] State that `reviewer-a`, `reviewer-b`, `bmad-code-review` review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor), validators, final reviewers, and final-review retry loops are always fresh with no exception.
  - [x] Update active review workflow guidance in `.pi/skills/bmad-code-review/steps/step-02-review.md` or explicitly route it through the centralized session policy so “without conversation context” means `context: "fresh"` plus no fork/resume.
- [x] Normalize or reject unsafe session requests before dispatch. (AC: 1, 2, 3, 5)
  - [x] Cover single-agent, top-level parallel `tasks`, and `chain`/parallel-chain invocations.
  - [x] Reject or convert `context: "fork"` to `context: "fresh"` according to documented policy; if rejecting, fail closed before any artifact state transition.
  - [x] Treat `subagent({ action: "resume", ... })` as session reuse; block it for BMAD standard story/review paths unless an explicit policy-approved repair case is documented in the active workflow.
  - [x] Ensure policy errors name the requested agent(s), requested mode (`fork`, omitted default, or `resume`), and violated policy.
- [x] Preserve artifact-first bounded context behavior. (AC: 1, 4)
  - [x] Keep formal workflow context as artifact paths/read directives plus concise task text; do not reconstruct story/review artifacts as parent summaries.
  - [x] Continue verifying required artifact paths exist and are readable before dispatch.
  - [x] Ensure fresh-context guidance says no previous runtime transcript, parent conversation, child output history, or reviewer transcript is appended to formal child prompts.
  - [x] Clarify that existing `inheritProjectContext: true` agent frontmatter may provide project rules, but story/review truth must come from explicit task text and named artifacts.
- [x] Keep role/tool boundaries intact. (AC: 3, 4)
  - [x] Do not add a dispatchable `orchestrator` or `bmad-orchestrator` child agent.
  - [x] Do not grant the `subagent` tool to `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, or `.pi/agents/reviewer-b.md`.
  - [x] Do not add v2 TDD agents (`test-architect`, `test-writer`, `red-validator`, `green-validator`) unless the implementation is explicitly expanded; Story 1.3 may mention their future policy only.
- [x] Add provider-free regression tests for session policy. (AC: 1-5)
  - [x] Extend `tests/test_bmad_orchestrator_guidance.py` or add `tests/test_fresh_context_session_policy.py`.
  - [x] Assert all BMAD guidance examples use `context: "fresh"` explicitly.
  - [x] Assert omitted context is documented as forbidden for formal BMAD dispatch because `pi-subagents` may apply agent `defaultContext: "fork"` to the whole run.
  - [x] Assert `context: "fork"` and `action: "resume"` are blocked or fail closed for standard BMAD story/review workflows.
  - [x] Assert reviewer/final-review roles are always fresh and cannot resume/fork.
  - [x] Assert policy rejection text includes requested agent, requested mode, and violated policy.
  - [x] Assert no story/review state update occurs after a policy rejection.
- [x] If runtime package behavior is changed, make it durable. (AC: 1-5)
  - [x] Keep any `pi-subagents` change generic; do not hardcode BMAD story keys or project-specific model IDs.
  - [x] Capture package source changes as a version-scoped patch under `.pi/patches/`, for example `pi-subagents-0.24.2-enforce-fresh-context-session-policy.patch`.
  - [x] Verify `bash .pi/install-packages.sh --patch` applies the patch or reports it already applied.
  - [x] Ensure the new patch coexists with existing `pi-subagents@0.24.2` patches.
- [x] Run final validation and artifact-cleanliness checks. (AC: 1-5)
  - [x] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [x] Run `PI_TELEMETRY=0 pi list`.
  - [x] Run `git diff --check`.
  - [x] Run `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` and remove generated bytecode if any appears.
  - [x] Run `find docs/_bmad-output/implementation-artifacts -maxdepth 1 -type f -name 'review-*.md' -print` and confirm no story-specific review artifacts are at the implementation-artifacts root.

### Review Follow-ups (AI)

- [x] [AI-Review][High][BMAD-1.3-FRESH-001] Active quick-dev implementation/context-discovery sub-agent paths still need explicit fresh-session policy validation before dispatch and before artifact state transitions. Evidence: Reviewer A flagged `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md` and `.pi/skills/bmad-quick-dev/step-03-implement.md`; Reviewer B reported no duplicate finding.
- [x] [AI-Review][High][BMAD-1.3-FRESH-002] Quick-dev planning investigation sub-agent/task path still needs explicit fresh-session policy validation before any investigation dispatch and before spec artifact writes. Evidence: both Reviewer A and Reviewer B independently flagged `.pi/skills/bmad-quick-dev/step-02-plan.md`.

## Dev Notes

### Source of Truth

Story 1.3 comes from Epic 1, which establishes the observable Pi multi-agent runtime before bootstrap, story-to-done execution, task-list state, UI visibility, or two-agent smoke proof. This story specifically addresses fresh-context session policy for sub-agent dispatch. [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-3-Enforce-Fresh-Context-Session-Policy]

Relevant requirements and architecture constraints:

- FR9: workflow stages launch with fresh, bounded context. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- FR17: sub-agents can launch with fresh context inside an active loop. [Source: docs/_bmad-output/planning-artifacts/epics.md#FR-Coverage-Map]
- Default session policy is fresh context for all agents. Validators, final reviewers, and final-review retry loops always start fresh. [Source: docs/_bmad-output/planning-artifacts/epics.md#Additional-Requirements]
- Architecture session policy says all agents start fresh by default, with reuse only for explicitly authorized repair/resume cases; validators and final reviewers are always fresh. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Session-Memory-Policy]
- `pi-subagents` remains the generic dispatch substrate; do not create `dispatch_subagent` or a role-specific duplicate runtime. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Dispatch-Patterns]

### Governing Policy for This Story

Planning artifacts contain broad future wording about repair/resume loops, but this story should implement the v1 governing rule:

- **Active v1 allowed reuse set:** none for standard BMAD story/review dispatch paths unless this story adds a clearly documented and tested exception.
- **Future TDD exceptions:** later formal workflows may allow same-role red/green repair exceptions, but Story 1.3 must not implement or assume v2 TDD agents.
- **Always fresh:** `reviewer-a`, `reviewer-b`, all active `bmad-code-review` review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor), validators, final reviewers, and final-review retry loops. A requested `fork` or `resume` for these roles must be blocked or normalized to fresh with clear policy evidence.
- **Omitted context is unsafe for BMAD formal dispatch:** `pi-subagents` can apply `defaultContext: "fork"` when any requested agent has that default. BMAD formal dispatches must pass `context: "fresh"` explicitly. [Source: .pi/npm/node_modules/pi-subagents/README.md#API-Reference]

### Current Runtime and API Facts

- Project package pin: `.pi/settings.json` declares `npm:pi-subagents@0.24.2`. [Source: .pi/settings.json]
- Current project wrapper agents are `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, and `.pi/agents/reviewer-b.md`; all declare `defaultContext: fresh`, explicit tool allowlists, `inheritSkills: false`, and no `subagent` tool. [Source: .pi/agents/implementer.md] [Source: .pi/agents/reviewer-a.md] [Source: .pi/agents/reviewer-b.md]
- `pi-subagents` schema supports top-level `context: "fresh" | "fork"`, execution modes via `agent`, `tasks`, or `chain`, and management `action: "resume"`. [Source: .pi/npm/node_modules/pi-subagents/src/extension/schemas.ts]
- If context is omitted, `pi-subagents` applies agent defaults; if any requested agent has `defaultContext: "fork"`, the whole invocation becomes forked. [Source: .pi/npm/node_modules/pi-subagents/src/runs/foreground/subagent-executor.ts#applyAgentDefaultContext]
- `context: "fork"` creates a branched child session from the parent persisted session/leaf; it fails fast if the parent session cannot be forked. It is not equivalent to fresh. [Source: .pi/npm/node_modules/pi-subagents/src/shared/fork-context.ts]
- `action: "resume"` can revive a previous child from its stored `.jsonl` session file; treat this as session reuse for BMAD policy purposes. [Source: .pi/npm/node_modules/pi-subagents/README.md#Status-and-control-actions]

### Current Gap

`.pi/skills/bmad-orchestrator/SKILL.md` already maps BMAD `sessionMode: fresh` to `context: "fresh"`, but it still says prior `sessionMode: resume` is out of scope unless using async status/resume behavior. Story 1.3 must replace that ambiguity with explicit policy: for active standard BMAD workflows, resume/fork is blocked unless a workflow-specific exception is documented and tested; validator/final reviewer roles have no exception. [Source: .pi/skills/bmad-orchestrator/SKILL.md#Delegation-Defaults]

The active `bmad-code-review` workflow also has a direct review-subagent path: Step 2 says to “Launch parallel subagents without conversation context” and defines Blind Hunter, Edge Case Hunter, and Acceptance Auditor roles. Story 1.3 must update or route this path so every review layer launches fresh and cannot fork/resume; otherwise the live review workflow can remain ambiguous even if parent orchestrator guidance is updated. [Source: .pi/skills/bmad-code-review/steps/step-02-review.md#Step-2-Review]

### Likely Files to Modify

Expected primary changes:

```text
.pi/skills/bmad-orchestrator/SKILL.md
.pi/skills/bmad-code-review/steps/step-02-review.md
tests/test_bmad_orchestrator_guidance.py
# or: tests/test_fresh_context_session_policy.py
```

Possible changes only if implementation chooses hard runtime enforcement or helper validation:

```text
.pi/patches/pi-subagents-0.24.2-enforce-fresh-context-session-policy.patch
.pi/npm/node_modules/pi-subagents/src/...        # local working copy only; durable truth is the patch
.pi/install-packages.sh                         # only if patch application flow needs generic hardening
.pi/patches/apply-patches.sh                    # only if patch application flow needs generic hardening
```

Files that should normally remain unchanged except for tests detecting drift:

```text
.pi/agents/implementer.md
.pi/agents/reviewer-a.md
.pi/agents/reviewer-b.md
.pi/settings.json
```

### Implementation Guardrails

- Do not rely on `.pi/agents/* defaultContext: fresh` alone; explicit parent dispatch policy is required.
- Do not rely on the current parent conversation being safe to inherit. `fork` is unsafe by default for BMAD formal workflows.
- Do not silently downgrade `fork`/`resume` without recording policy evidence; either reject before dispatch or explicitly state and test the normalization behavior.
- Do not update Markdown story/review state after a session-policy rejection.
- Do update active code-review session wording; do not leave `bmad-code-review` Step 2 at vague “without conversation context” wording if it can launch review layers without explicit fresh-context policy.
- Do not implement Story 1.4 task-list state, Story 1.5 UI visibility, Story 1.6 smoke scenario, Epic 3 story-to-done execution, or Epic 4 TDD red/green loops in this story.
- Do not create a custom `.pi/extensions/bmad-orchestrator/` runtime solely for this policy unless prompt/package behavior proves insufficient and the change is approved by the story scope.
- Keep runtime package patches generic and version-scoped; direct edits under `.pi/npm/node_modules` are ignored/regenerated and are not durable by themselves.

### Artifact and Context Rules

For formal BMAD dispatch:

```ts
subagent({
  agent: "reviewer-a",
  task: "Review the BMAD story artifact at <artifact-path> as source of truth. Do not rely on parent conversation history.",
  reads: ["<artifact-path>"],
  context: "fresh",
  agentScope: "project"
})
```

Rules:

- Use `context: "fresh"` explicitly.
- Pass formal context as artifact paths/read directives, not lossy summaries.
- Verify referenced artifact paths exist and are readable before dispatch.
- Do not append prior runtime transcript, prior child output, prior reviewer output, or parent conversation history to the child task.
- Child runtime output is control-plane evidence only; durable truth remains Markdown artifacts. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Format-Patterns]

### Previous Story Intelligence

#### Story 1.1 — Generic Sub-Agent Dispatch

- Use marketplace `pi-subagents`; do not build a custom dispatch extension or `dispatch_subagent` tool. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Dev-Notes]
- Parent owns orchestration; child agents must not communicate horizontally or launch nested sub-agents. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Completion-Notes-List]
- Formal artifact paths must be verified and passed as paths/read directives rather than parent-side summaries. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Completion-Notes-List]
- Unknown-agent and child error handling should fail closed before Markdown state updates. Reuse that fail-closed style for session policy violations. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Review-Findings]

#### Story 1.2 — Agent Definitions and Model Routing

- Canonical dispatchable project agents live under `.pi/agents/`; workflow skills under `.pi/skills/` must not become child agents. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md#Dev-Notes]
- Wrapper agents already declare `defaultContext: fresh`, but Story 1.2 explicitly did not enforce fresh context beyond wrapper defaults. Story 1.3 must close that gap. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md#Scope-Boundary]
- Provider-free runtime tests use `npx --yes tsx` and isolated settings/HOME; follow this pattern for any `pi-subagents` runtime-discovery checks. [Source: tests/test_agent_definitions_model_routing.py]
- If package source changes are needed, use the tracked `.pi/install-packages.sh` plus `.pi/patches/` durability mechanism. [Source: docs/_bmad-output/implementation-artifacts/1-2-0-add-agent-definitions-and-model-routing-contract/1-2-0-add-agent-definitions-and-model-routing-contract.md#Completion-Notes-List]

#### Story 1.2.1 — Story-Scoped Implementation Artifacts

- New story artifacts must be written under `{implementation_artifacts}/{story_key}/{story_key}.md`; legacy flat story paths are read-only fallback compatibility. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md#Path-Convention-for-This-Story]
- Keep story-specific review outputs inside the story folder; root-level `sprint-status.yaml` and `deferred-work.md` may remain global. [Source: docs/_bmad-output/implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts/1-2-1-normalize-story-scoped-implementation-artifacts.md#Completion-Notes-List]

#### Story 1.2.2 — Subagent Model and Task Summary

- `.pi/npm/` is regenerated and ignored; durable package changes are version-scoped patches under `.pi/patches/`. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md#Current-Runtime-Package-and-Durability-Constraints]
- Validation pattern: run full Python tests, `git diff --check`, root review-artifact cleanliness, `.pi/install-packages.sh --patch`, and patch dry-run checks when package patches change. [Source: docs/_bmad-output/implementation-artifacts/1-2-2-display-subagent-model-and-task-summary/1-2-2-display-subagent-model-and-task-summary.md#Completion-Notes-List]

### Recent Git Intelligence

Recent commits show the project is actively hardening BMAD workflow contracts and package patches:

- `81da900 Standardize review action item pass tags`
- `d049fef Implement subagent model and task summaries`
- `08ad12e Create story 1.2.2 and rename story 1.2 artifacts`
- `ce9157e Normalize BMAD story artifact routing`
- `0a87e45 Organize implementation artifacts by story`

Actionable implications:

- Preserve existing story-folder artifact convention.
- Keep tests provider-free and deterministic.
- Do not revert or overwrite unrelated untracked files (`context.md`, `progress.md`, `research.md`) unless explicitly instructed.
- Patch durability and validation evidence are now expected review targets.

### Latest Technical Information

- Installed/local `pi-subagents` package version is `0.24.2`; `.pi/settings.json` pins `npm:pi-subagents@0.24.2`. [Source: .pi/settings.json]
- Local `pi-subagents` README documents that packaged `planner`, `worker`, and `oracle` default to forked context when a launch omits `context`; explicit `context: "fresh"` wins. [Source: .pi/npm/node_modules/pi-subagents/README.md#Agents-and-Chains]
- `context: "fork"` creates real branched sessions from the parent leaf and never silently downgrades to fresh. [Source: .pi/npm/node_modules/pi-subagents/README.md#API-Reference]
- `resume` revives a previous child from stored session context and therefore must be treated as session reuse under BMAD policy. [Source: .pi/npm/node_modules/pi-subagents/README.md#Status-and-control-actions]
- No web/package-registry lookup was available during story creation; before changing package pins, verify upstream version behavior locally and preserve exact-pinned reproducibility.

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

- Story artifact location for this story: `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md`.
- Do not write `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy.md`; that legacy flat path is read-only fallback compatibility only.
- Framework-owned runtime assets remain under `.pi/`.
- Global implementation-artifact files that may remain at root: `sprint-status.yaml`, `deferred-work.md`.

## Dev Agent Record

### Agent Model Used

BMAD Implementer sub-agent via parent-orchestrated runs with model override `openai-codex/gpt-5.5`; Reviewer A/B review runs also used model override `openai-codex/gpt-5.5`.

### Debug Log References

- 2026-05-13: Added failing provider-free regression tests in `tests/test_fresh_context_session_policy.py`; confirmed initial failures against missing Session Policy guidance.
- 2026-05-13: Implemented active v1 fail-closed fresh-context policy in parent BMAD orchestration guidance and routed active review workflows to explicit `context: "fresh"` plus no fork/resume.
- 2026-05-13: Runtime package behavior was not changed; no `.pi/npm/node_modules/pi-subagents` source edits or new `.pi/patches/` patch were required.
- 2026-05-13: Verified patch mechanism with `bash .pi/install-packages.sh --patch`; existing `pi-subagents@0.24.2` patches reported already applied.
- 2026-05-13: Validation passed: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (163 tests), `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness find, and root review-artifact cleanliness find.
- 2026-05-13: Removed pre-existing/generated `tests/__pycache__` bytecode after validation cleanup.
- 2026-05-13: Added failing follow-up regressions for quick-dev context-discovery and implementation dispatch policy gaps; confirmed they failed before implementation and passed after updating `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md` and `.pi/skills/bmad-quick-dev/step-03-implement.md`.
- 2026-05-13: Follow-up validation passed: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (165 tests), `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness find, and root review-artifact cleanliness find.
- 2026-05-13: Added a failing follow-up regression for the quick-dev planning investigation session-policy gate in `tests/test_fresh_context_session_policy.py`; confirmed it failed against missing `step-02-plan.md` policy wording.
- 2026-05-13: Updated `.pi/skills/bmad-quick-dev/step-02-plan.md` to fail closed before investigation dispatch and `{spec_file}` writes unless explicit `context: "fresh"`/no fork/resume policy validation passes, with requested agent/task, mode, and policy in rejection evidence.
- 2026-05-13: Follow-up iteration 2 validation passed: targeted planning-policy regression, `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (166 tests), `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness find, and root review-artifact cleanliness find.

### Completion Notes List

- Added a centralized `Session Policy` to `.pi/skills/bmad-orchestrator/SKILL.md` requiring explicit `context: "fresh"`, forbidding omitted context for formal BMAD dispatches, and blocking `fork`/`resume` for active v1 standard story/review paths.
- Documented fail-closed policy rejection evidence (`requestedAgent`, `requestedMode`, `violatedPolicy`) and required rejection before child launch or Markdown artifact state transition.
- Preserved artifact-first bounded context by requiring task text plus explicit artifact paths/read directives only, with no parent conversation, runtime transcript, child output history, or reviewer transcript appended.
- Updated active review guidance in `.pi/skills/bmad-code-review/steps/step-02-review.md` and `.pi/skills/bmad-quick-dev/` review paths to use explicit `context: "fresh"` and no fork/resume.
- Added provider-free regression coverage for session policy, review-path routing, role/tool boundaries, fresh artifact context, and no state update after policy rejection.
- No dispatchable orchestrator, role-agent `subagent` tools, v2 TDD agents, or runtime package patches were added.
- ✅ Resolved review finding [High]: BMAD-1.3-FRESH-001 by adding fail-closed quick-dev session-policy gates before context artifact writes and spec state transitions, requiring explicit `context: "fresh"`, blocking omitted/fork/resume, reporting requested agent/mode/policy, and preserving artifact-first prompts.
- ✅ Resolved review finding [High]: BMAD-1.3-FRESH-002 by adding a fail-closed quick-dev planning Session Policy Gate before any investigation sub-agent/task dispatch or `{spec_file}` write, requiring explicit `context: "fresh"`, blocking omitted/fork/resume, reporting requested agent/task/mode/policy, and preserving artifact-first/no-transcript prompts.

### File List

- `.pi/skills/bmad-orchestrator/SKILL.md`
- `.pi/skills/bmad-code-review/steps/step-02-review.md`
- `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md`
- `.pi/skills/bmad-quick-dev/step-02-plan.md`
- `.pi/skills/bmad-quick-dev/step-03-implement.md`
- `.pi/skills/bmad-quick-dev/step-04-review.md`
- `.pi/skills/bmad-quick-dev/step-oneshot.md`
- `tests/test_fresh_context_session_policy.py`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/1-3-enforce-fresh-context-session-policy.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-a-iteration-1.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-a-iteration-2.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-b-iteration-1.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-b-iteration-2.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-a-iteration-3.md`
- `docs/_bmad-output/implementation-artifacts/1-3-enforce-fresh-context-session-policy/review-b-iteration-3.md`
- `docs/_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- 2026-05-13: Implemented Story 1.3 fresh-context session policy guidance, active review workflow routing, provider-free regression tests, and validation evidence.
- 2026-05-13: Recorded deduplicated AI review finding BMAD-1.3-FRESH-001 from iteration 1 for follow-up implementation.
- 2026-05-13: Addressed code review findings - 1 item resolved (BMAD-1.3-FRESH-001 quick-dev fresh-session policy gates and regression coverage).
- 2026-05-13: Recorded deduplicated AI review finding BMAD-1.3-FRESH-002 from iteration 2 for follow-up implementation.
- 2026-05-13: Addressed code review findings - 1 item resolved (BMAD-1.3-FRESH-002 quick-dev planning fresh-session policy gate and regression coverage).
- 2026-05-13: Review iteration 3 approved with 0 High, 0 Medium, and 0 Low findings; story marked done.

## Senior Developer Review (AI)

### Review Iteration 1 — 2026-05-13

**Reviewers:** reviewer-a (GPT-5.5), reviewer-b (GPT-5.5)

**Outcome:** Changes Requested

**Deduplicated Findings:** 1 High, 0 Medium, 0 Low

#### Action Items

- [x] [High][BMAD-1.3-FRESH-001] Active quick-dev implementation/context-discovery sub-agent paths still bypass fresh-session policy. Update `.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md` and `.pi/skills/bmad-quick-dev/step-03-implement.md` so formal quick-dev sub-agent dispatches validate policy before any artifact state transition, require explicit `context: "fresh"`, block omitted context/`fork`/`resume`, report requested agent(s), requested mode, and violated policy, and keep context artifact-first.

#### Evidence Summary

- Reviewer A: HIGH finding BMAD-1.3-FRESH-001 with AC1, AC2, AC4, and AC5 marked failing due quick-dev direct sub-agent paths that did not explicitly route through the new policy before dispatch/state update.
- Reviewer B: APPROVE, no findings. This did not duplicate or supersede Reviewer A's blocking finding.

#### Validation Evidence from Reviews

- Reviewer A/B reported passing targeted validation including `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`, `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness, and root review-artifact cleanliness.

### Review Iteration 2 — 2026-05-13

**Reviewers:** reviewer-a (GPT-5.5), reviewer-b (GPT-5.5)

**Outcome:** Changes Requested

**Deduplicated Findings:** 1 High, 0 Medium, 0 Low

#### Action Items

- [x] [High][BMAD-1.3-FRESH-002] Quick-dev planning investigation sub-agent/task path still bypasses fresh-session policy. Update `.pi/skills/bmad-quick-dev/step-02-plan.md` so planning investigation dispatch validates policy before any sub-agent/task launch and before `{spec_file}` writes, requires explicit `context: "fresh"`, blocks omitted context/`fork`/`resume`, reports requested agent(s), requested mode, and violated policy, and keeps prompts artifact-first with no prior transcripts. Add provider-free regression coverage for this step.

#### Evidence Summary

- Reviewer A: HIGH finding BMAD-1.3-FRESH-002 with AC1, AC2, AC4, and AC5 marked failing due quick-dev planning investigation dispatch wording in `.pi/skills/bmad-quick-dev/step-02-plan.md`.
- Reviewer B: Independently reported the same HIGH finding BMAD-1.3-FRESH-002 against `.pi/skills/bmad-quick-dev/step-02-plan.md`; deduplicated into the single action item above.

#### Validation Evidence from Reviews

- Reviewer A/B reported passing targeted validation including `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`, `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness, and root review-artifact cleanliness.

### Review Iteration 3 — 2026-05-13

**Reviewers:** reviewer-a (GPT-5.5), reviewer-b (GPT-5.5)

**Outcome:** Approve

**Deduplicated Findings:** 0 High, 0 Medium, 0 Low

#### Action Items

- None.

#### Evidence Summary

- Reviewer A: APPROVE; verified BMAD-1.3-FRESH-001 and BMAD-1.3-FRESH-002 resolved and found no High or Medium findings.
- Reviewer B: APPROVE; independently verified BMAD-1.3-FRESH-001 and BMAD-1.3-FRESH-002 resolved and found no findings.

#### Validation Evidence from Reviews

- Reviewer A/B reported passing targeted validation including `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (166 tests), `PI_TELEMETRY=0 pi list`, `git diff --check`, bytecode cleanliness, and root review-artifact cleanliness.

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Key implementation decision to make during dev: whether parent-guidance/test enforcement is sufficient for active v1 BMAD flows or whether a generic `pi-subagents` package patch is needed to hard-block unsafe modes in the project runtime. If package code changes, use the existing tracked patch mechanism.

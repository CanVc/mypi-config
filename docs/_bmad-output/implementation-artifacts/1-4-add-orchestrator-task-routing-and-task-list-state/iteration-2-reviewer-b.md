# BMAD Reviewer B Review — Iteration 2 — Story 1.4

## Verdict

**Blocked**: 1 **Medium** finding. No **High** findings. 1 non-blocking **Low** note.

## Iteration-1 Follow-up Verification

- **BMAD-1.4-TASKSTATE-001**: **partially resolved**. Task-state gates were added to active paths and tested, but a `quick-dev` fallback path can still bypass/contradict `blocked`/`failed` state when spawn fails.
- **BMAD-1.4-TASKSTATE-002**: **resolved**. `Result Handling` now distinguishes fail-closed behavior from success transitions and durable `blocked`/`failed` writes with cause/action (`.pi/skills/bmad-orchestrator/SKILL.md:249-253`).
- **BMAD-1.4-TASKSTATE-003**: **resolved for review**. The code-review workflow includes untracked files through `git ls-files --others --exclude-standard` + `git diff --no-index` (`.pi/skills/bmad-code-review/steps/step-01-gather-context.md:52,60`), and the dev report lists the new deliverables.

## AC Coverage

- **AC1**: verified — durable contract, required fields, and fixed vocabulary (`.pi/skills/bmad-orchestrator/SKILL.md:71-109`).
- **AC2**: verified — `pending` validation, transition to `in-progress`, `activeAgentId` (`.pi/skills/bmad-orchestrator/SKILL.md:113-115`).
- **AC3**: verified except for the finding — parent-validated completion and controlled dependent dispatch (`.pi/skills/bmad-orchestrator/SKILL.md:116-118`).
- **AC4**: verified — declared context source, artifact-first behavior, `routingDecision` (`.pi/skills/bmad-orchestrator/SKILL.md:122-126`).
- **AC5**: **partially blocked** by the Medium finding below.

## Findings

### 1. [MEDIUM][AC5][BMAD-1.4-TASKSTATE-001 residual] The context-discovery fallback can hide a sub-agent failure without clear durable state

- **Evidence**: the new gate requires writing `blocked`/`failed` with `cause` and `recommendedNextAction` after failure/timeout (`.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md:18`). But the active epic-context compilation path keeps an inline fallback when the runtime cannot spawn, or when spawn fails/times out, and asks for the same output (`.pi/skills/bmad-quick-dev/step-01-clarify-and-route.md:58-60`) without specifying how the failed task-state entry is classified or what explicit recovery authorizes continuation.
- **AC Impact**: AC5 requires a failed/unclassifiable task to be marked `blocked` or `failed` with cause/action. In this path, a parent can follow the fallback and continue writing `{implementation_artifacts}/epic-<N>-context.md` after a sub-agent failure, making the visible state ambiguous and bypassing deterministic stop/recovery behavior.
- **Smallest safe remediation**: in the `step-01` fallback, specify that any failed/timed-out spawn first sets the sub-agent task to `blocked`/`failed` with `cause` + `recommendedNextAction`; if the inline fallback is an authorized recovery, create/update a separate task or explicit `routingDecision` indicating recovery authorization, then add a test that covers this fallback case.

### 2. [LOW][Artifact hygiene][Non-blocking] Conditional package subtasks are checked even though they are N/A

- **Evidence**: package-patch subtasks are checked (`.../1-4-add-orchestrator-task-routing-and-task-list-state.md:51-55`), while the notes say no `pi-subagents` behavior changed and `install-packages.sh --patch` was not required (`.../1-4-add-orchestrator-task-routing-and-task-list-state.md:323`).
- **AC Impact**: no AC1-5 blocker, but the validation trace is misleading.
- **Smallest safe remediation**: replace those subtasks with `N/A — no runtime/package change`, or uncheck actions that were not executed.

## Validation Executed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_orchestrator_task_routing_state` — OK, 11 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_fresh_context_session_policy tests.test_bmad_orchestrator_guidance tests.test_orchestrator_task_routing_state` — OK, 37 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — OK, 177 tests.
- `PI_TELEMETRY=0 pi list` — OK.
- `git diff --check` — OK.
- Bytecode / root review-artifact checks — no files reported.

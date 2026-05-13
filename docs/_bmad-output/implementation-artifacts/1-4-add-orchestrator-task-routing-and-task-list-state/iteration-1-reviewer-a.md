# BMAD Reviewer A Review — Story 1.4

## Verdict

**Blocked** — 2 **High** findings and 1 **Medium** finding. High/Medium findings must be resolved before the story can be considered complete.

## Findings

### 1. [HIGH] Active dispatch paths can bypass the task-state contract

- **AC Impact**: AC1, AC2, AC3, AC4, AC5; regression-test adequacy.
- **Evidence**:
  - The story requires integrating the contract into active BMAD guidance and testing that quick-dev paths cannot bypass task-state updates (`.../1-4-add-orchestrator-task-routing-and-task-list-state.md:39-50`, `:220`).
  - The new contract is added only in `.pi/skills/bmad-orchestrator/SKILL.md:65-126`.
  - Active workflows still launch/formalize sub-agents without local instructions to create/update durable task-list state: `.pi/skills/bmad-code-review/steps/step-02-review.md:23-34`, `.pi/skills/bmad-quick-dev/step-03-implement.md:22-36`, `.pi/skills/bmad-quick-dev/step-04-review.md:15-27`, `.pi/skills/bmad-quick-dev/step-oneshot.md:20`.
  - The new test covers only `.pi/skills/bmad-orchestrator/SKILL.md` (`tests/test_orchestrator_task_routing_state.py:11-12`, `:32-45`, `:112-121`) and does not verify those active paths.
- **Risk**: a team run through code-review/quick-dev can dispatch agents with `context: "fresh"` while never creating `pending` tasks, never moving them to `in-progress`, never marking them `completed`/`blocked`/`failed`, and never recording a `routingDecision`.
- **Smallest safe remediation**: add an explicit instruction in every active workflow that dispatches/fans out sub-agents to apply the `Task Routing and Task List State` contract before/after dispatch (or add an equivalent mandatory reference), then add provider-free tests that scan those paths and fail if durable task state can be bypassed.

### 2. [HIGH] The Result Handling section contradicts the required `blocked`/`failed` marking

- **AC Impact**: AC5, plus lifecycle-contract consistency.
- **Evidence**:
  - The new contract requires marking a task `blocked` or `failed` with `cause` and `recommendedNextAction` on failure/timeout/unclassifiable state (`.pi/skills/bmad-orchestrator/SKILL.md:117`).
  - The existing `Result Handling` section still says timeout/child error/interruption/empty result/unavailable status must “fail closed before updating Markdown artifacts or workflow state transitions” and “Record only a debug note” (`.pi/skills/bmad-orchestrator/SKILL.md:238-240`).
- **Risk**: two incompatible normative rules exist in the same file; a parent can follow the older rule and never write durable `blocked`/`failed` state, violating AC5.
- **Smallest safe remediation**: reconcile `Result Handling` by distinguishing success/story-state transitions from task-state failure transitions: after parent validation, write `blocked`/`failed` with `cause` and `recommendedNextAction`; keep the prohibition against marking `in-progress` on policy rejection.

### 3. [MEDIUM] New tests/artifacts are untracked and absent from `git diff HEAD`

- **AC Impact**: provider-free test requirements / regression adequacy.
- **Evidence**:
  - `git diff --name-status HEAD` lists only `.pi/skills/bmad-orchestrator/SKILL.md`, the story, and `sprint-status.yaml`.
  - `git status --short` shows `?? tests/test_orchestrator_task_routing_state.py` and `?? docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/iteration-1-dev-report.md`.
  - The story nevertheless checks off the added test (`.../1-4-add-orchestrator-task-routing-and-task-list-state.md:44-50`).
- **Risk**: if the gate/review is based on `git diff HEAD`, the added regression test is not in the deliverable delta and the test AC is not durably satisfied.
- **Smallest safe remediation**: include the new files in the expected patch/working-tree index (at minimum `tests/test_orchestrator_task_routing_state.py`, and the dev-report artifact if required), then rerun validation.

## Checks Performed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_orchestrator_task_routing_state` — OK, 8 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — OK, 174 tests.
- `git diff --check` — OK.
- `PI_TELEMETRY=0 pi list` — OK.
- `__pycache__` / review-root checks — no output.

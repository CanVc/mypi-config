# Reviewer B Review — Story 1.4

## Verdict

**Blocked**: 1 blocking finding (**High**), 1 non-blocking finding (**Low**). Local tests pass, but a guidance contradiction prevents AC5 from being validated safely.

## Validation Executed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_orchestrator_task_routing_state` — OK, 8 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_fresh_context_session_policy tests.test_bmad_orchestrator_guidance tests.test_orchestrator_task_routing_state` — OK, 34 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — OK, 174 tests.
- `PI_TELEMETRY=0 pi list` — OK.
- `git diff --check` — OK.
- Bytecode / review-root artifact checks — no files reported.

## Synthetic AC Verification

- **AC1**: covered by the durable contract, fields, and vocabulary in `.pi/skills/bmad-orchestrator/SKILL.md:71-109`.
- **AC2**: covered by the `pending` → `in-progress` dispatch rules and `activeAgentId` in `.pi/skills/bmad-orchestrator/SKILL.md:113-115`.
- **AC3**: partially covered by completion/dependencies in `.pi/skills/bmad-orchestrator/SKILL.md:113,116,124`.
- **AC4**: covered by declared handoffs / artifact-first / `routingDecision` in `.pi/skills/bmad-orchestrator/SKILL.md:122-126`.
- **AC5**: **not validated** because of the blocking contradiction below.

## Findings

### 1. [HIGH][AC5] The guidance fails closed before writing `blocked`/`failed` state

- **Evidence**: the new contract requires marking failures/timeouts/ambiguous outputs as `blocked` or `failed` with `cause` and `recommendedNextAction` (`.pi/skills/bmad-orchestrator/SKILL.md:117`). But the existing `Result Handling` section still says timeout/child error/interruption/empty result/unavailable status must fail closed **before** any Markdown update or state transition, with only a debug note (`.pi/skills/bmad-orchestrator/SKILL.md:243`).
- **AC Impact**: AC5 requires a failed or unclassifiable task to be marked `blocked`/`failed` and the builder to receive a cause and recommended action. With these competing instructions, a parent can follow line 243 and never write the required visible durable state for AC5. This also weakens determinism for subsequent routing.
- **Smallest safe remediation**: harmonize `Result Handling`: “fail closed” should mean no success transition and no dependent dispatch, but for an already classified orchestrator-managed task, durably write `blocked`/`failed` with `cause` and `recommendedNextAction`. Keep the pre-dispatch/policy-rejection exception without moving to `in-progress`. Add a test that covers this cross-section consistency, not only the new block.

### 2. [LOW][N/A] Conditional package-patch subtasks are checked even though they are not applicable

- **Evidence**: the “capture patch”, “add package tests”, and “verify install-packages --patch” subtasks are checked (`docs/_bmad-output/implementation-artifacts/1-4-add-orchestrator-task-routing-and-task-list-state/1-4-add-orchestrator-task-routing-and-task-list-state.md:51-55`), while the notes say no `pi-subagents` behavior changed and `bash .pi/install-packages.sh --patch` was not required (`.../1-4-add-orchestrator-task-routing-and-task-list-state.md:304-308`).
- **AC Impact**: not blocking for AC1-5, but misleading artifact/validation hygiene.
- **Smallest safe remediation**: replace this section with an explicit `N/A — no runtime/package change`, or leave only the conditional parent checked with an N/A note and do not check actions that were not executed.

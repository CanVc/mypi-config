1. `Verdict`: `findings`
2. `Severity counts`: High=0, Medium=3, Low=1
3. `Findings`:

- ID: R2-B-1
  - Severity: Medium
  - Bucket: Durable package/override/discovery fix
  - Title: Patch auto-application is not durable because the only postinstall hook is in ignored `.pi/npm/package.json`
  - Location: `.pi/npm/.gitignore:1-2`, `.pi/npm/package.json:7-10`, `.pi/settings.json:14-16`, `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:280-286`
  - Evidence: `.pi/npm/.gitignore` ignores everything except its own `.gitignore`; `git check-ignore -v .pi/npm/package.json .pi/npm/node_modules/pi-subagents/src/agents/agents.ts` reports both as ignored. The story claims durability through `.pi/npm/package.json` postinstall and patched `node_modules`, but those files are not tracked/untracked deliverables. The tracked `.pi/settings.json` still only pins upstream `npm:pi-subagents@0.24.2`; nothing tracked makes a clean package restore apply `.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch` automatically.
  - AC/Constraint impacted: AC2, AC3, AC5, AC6, AC9; durable package/override/discovery fix; “Do not patch ignored `.pi/npm/node_modules` as the durable fix.”
  - Recommended action: Make the runtime change durable from committed sources: pin a committed project-local patched package/fork, or add a tracked/package-manager-supported hook/config that is guaranteed to run after restore. Add a clean-restore validation that starts from unpatched upstream `pi-subagents@0.24.2`, applies the committed mechanism, and proves project-agent overrides plus `.agents/` exclusion.

- ID: R2-B-2
  - Severity: Medium
  - Bucket: Tests / validation quality
  - Title: Model precedence tests still simulate routing and inspect source strings instead of exercising `pi-subagents` resolution
  - Location: `tests/test_agent_definitions_model_routing.py:128-143`, `tests/test_agent_definitions_model_routing.py:340-418`, `tests/test_agent_definitions_model_routing.py:660-699`, `tests/test_agent_definitions_model_routing.py:869-886`
  - Evidence: The AC5/AC6 precedence tests call a local `simulate_override_resolution()` helper that reimplements `project > user > file` instead of invoking the runtime resolver. Discovery/override patch tests assert that specific strings exist in the currently installed ignored `node_modules` source, and the postinstall test checks ignored `.pi/npm/package.json`. They do not perform a provider-free management/list/get or runtime discovery call with isolated user/project settings, so a clean restore or semantic runtime regression can pass the Python suite.
  - AC/Constraint impacted: AC4, AC5, AC6, AC9; tests non-tautologiques; model-routing validation.
  - Recommended action: Add provider-free tests that exercise the actual `pi-subagents` discovery/get resolution path with temporary HOME/user settings and project settings, or a package-level unit/integration test using the Pi/package loader. Keep the simulator only as supplementary documentation, not as the primary AC5/AC6 proof.

- ID: R2-B-3
  - Severity: Medium
  - Bucket: Status / story bookkeeping
  - Title: Sprint status and story bookkeeping are inconsistent with the story’s review state and actual changed files
  - Location: `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:3`, `docs/_bmad-output/implementation-artifacts/sprint-status.yaml:49-53`, `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:274-286`
  - Evidence: The story says `Status: review`, but `sprint-status.yaml` still records `1-2-add-agent-definitions-and-model-routing-contract: ready-for-dev`. The story file list claims `.pi/npm/package.json` and `.pi/npm/node_modules/.../agents.ts` are part of the deliverable even though they are ignored, and claims `tests/test_bmad_code_review_severity.py` was modified although `git diff` shows no change for that file.
  - AC/Constraint impacted: Required status/story bookkeeping and workflow integrity.
  - Recommended action: Update `sprint-status.yaml` to match the story status, and reconcile the File List with actual committed/untracked deliverables. If ignored install-output files remain mentioned, clearly mark them as local evidence only, not durable source deliverables.

- ID: R2-B-4
  - Severity: Low
  - Bucket: Scope creep
  - Title: Unrelated Story 1.2.1 planning artifacts are included in the Story 1.2 change set
  - Location: `docs/_bmad-output/planning-artifacts/epics.md:396-443`, `docs/_bmad-output/implementation-artifacts/1-2-1-display-subagent-model-and-task-summary-in-async-widget.md:1-35`, `docs/_bmad-output/implementation-artifacts/sprint-status.yaml:52-53`
  - Evidence: The uncommitted diff adds a new Story 1.2.1 to `epics.md`, creates a new ready-for-dev story artifact, and adds it to sprint status. Story 1.2 AC1-AC9 do not require creating a new widget/story artifact, and the Story 1.2 File List does not record these planning changes.
  - AC/Constraint impacted: Scope boundary / scope creep control.
  - Recommended action: Remove these planning changes from the Story 1.2 patch or split them into a separate, explicitly approved planning/story-creation change.

4. `Validation run`:

- `git status --short && git diff --stat HEAD && git ls-files --others --exclude-standard` — non-empty target confirmed. Modified tracked files include `.pi/settings.json`, the Story 1.2 artifact, `sprint-status.yaml`, and `epics.md`; untracked deliverables include `.pi/agents/*`, `.pi/patches/*`, `tests/test_agent_definitions_model_routing.py`, and review/story artifacts.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — PASS: `Ran 72 tests in 0.010s`, `OK`.
- `PI_TELEMETRY=0 pi list` — PASS: project package reports `npm:pi-subagents@0.24.2` loaded from `/home/cvc/dev/mypi-config/.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models || true` — PASS: active registry listed `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5` among other models.
- `git check-ignore -v .pi/npm/package.json .pi/npm/node_modules/pi-subagents/src/agents/agents.ts .pi/patches/apply-patches.sh` — `.pi/npm/package.json` and `.pi/npm/node_modules/.../agents.ts` are ignored by `.pi/npm/.gitignore`; `.pi/patches/apply-patches.sh` is not ignored.
- `patch --dry-run -p1 -d .pi/npm/node_modules/pi-subagents < .pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch` — exit 1 with “Reversed (or previously applied) patch detected”, confirming the local ignored install tree is currently patched, not proving clean-restore durability.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.

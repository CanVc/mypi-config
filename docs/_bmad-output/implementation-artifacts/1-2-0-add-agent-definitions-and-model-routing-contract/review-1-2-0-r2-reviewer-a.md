Verdict: findings

Severity counts: High=0, Medium=3, Low=0

Findings:

- ID: R2-A-1
  - Severity: Medium
  - Bucket: Patch durability / runtime contract
  - Title: Project-agent override/discovery fix still depends on ignored `.pi/npm` state
  - Location: `.pi/npm/.gitignore:1-2`, `.pi/npm/package.json:7-9`, `.pi/settings.json:1-4`, `.pi/patches/apply-patches.sh:1-9`
  - Evidence: `.pi/npm/package.json` contains the claimed `postinstall` hook, but `.pi/npm/.gitignore` ignores everything except `.gitignore`; `git status --ignored` reports `.pi/npm/package.json` and `.pi/npm/node_modules/` as ignored. The committed settings still pin upstream `npm:pi-subagents@0.24.2`, with no tracked package/fork or tracked install hook that would reapply the patch after a clean package restore.
  - AC/Constraint impacted: AC2, AC3, AC5, AC6, AC9; durable package/override/discovery fix constraint.
  - Recommended action: Make the runtime fix durable from tracked sources: pin a committed local package/fork or add a tracked, Pi-invoked install/patch mechanism outside ignored `.pi/npm`, then validate from a clean restore/reinstall path.

- ID: R2-A-2
  - Severity: Medium
  - Bucket: Tests / validation quality
  - Title: Model-routing tests remain partly tautological and do not fail closed with actionable runtime validation
  - Location: `tests/test_agent_definitions_model_routing.py:71-88`, `128-143`, `340-465`, `679-699`, `764-821`
  - Evidence: Precedence tests call `simulate_override_resolution`, which merely implements the expected order directly. Isolated settings tests parse temporary JSON and then call the same simulation rather than exercising `pi-subagents` discovery/resolution. Patch tests mostly assert source substrings. Invalid-model tests assert a fake model is absent from a hard-coded set, but do not verify dispatch/smoke validation blocks with the invalid agent ID and required fix.
  - AC/Constraint impacted: AC5, AC6, AC8, AC9; “tests non tautologiques”.
  - Recommended action: Add regression tests that import or invoke actual `pi-subagents` resolution in an isolated temp project/HOME, proving file model, user override, project override precedence, project-only discovery, and invalid model errors that name the agent and required fix. Query active model registry or report an explicit environment block.

- ID: R2-A-3
  - Severity: Medium
  - Bucket: Story bookkeeping / scope creep
  - Title: Status bookkeeping is inconsistent and unrelated Story 1.2.1 planning changes are mixed into this story
  - Location: `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:3`, `68-74`, `276-286`; `docs/_bmad-output/implementation-artifacts/sprint-status.yaml:49-53`; `docs/_bmad-output/planning-artifacts/epics.md:396-443`; `docs/_bmad-output/implementation-artifacts/1-2-1-display-subagent-model-and-task-summary-in-async-widget.md:1-23`
  - Evidence: Story artifact says `Status: review`, but sprint status still lists `1-2-add-agent-definitions-and-model-routing-contract: ready-for-dev`. The top-level smoke task is checked while required smoke subtasks remain unchecked. File List claims `.pi/npm/package.json` is modified even though it is ignored/untracked from the deliverable, and says the new test file has 56 tests while the validation run executed 72. The diff also adds a new Story 1.2.1 to epics/sprint status and creates an untracked story artifact, which is outside AC1-AC9 for Story 1.2.
  - AC/Constraint impacted: Status/story bookkeeping; scope creep constraint.
  - Recommended action: Align sprint status with the story state, correct File List/test-count evidence, leave incomplete smoke subtasks unchecked, and move Story 1.2.1 planning changes to a separately approved change or explicitly document parent approval.

Validation run:

- `git status --short && git diff --stat HEAD && git ls-files --others --exclude-standard`
  - Result: modified `.pi/settings.json`, Story 1.2, sprint status, epics; untracked `.pi/agents/*`, `.pi/patches/*`, Story 1.2.1, review reports, and `tests/test_agent_definitions_model_routing.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
  - Result: `Ran 72 tests ... OK`.
- `PI_TELEMETRY=0 pi list`
  - Result: project package `npm:pi-subagents@0.24.2` loaded from `.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models || true`
  - Result: registry available; wrapper models `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5` are present.
- `node`/`jiti` runtime inspection of `discoverAgentsAll(process.cwd()).project`
  - Result: current patched local runtime reports only `implementer`, `reviewer-a`, `reviewer-b` as project agents.
- Temp-project runtime override check with isolated settings
  - Result: current patched local runtime resolves `implementer` project override to `openai-codex/gpt-5.4` with base model `zai/glm-5.1`.
- `git status --short --ignored .pi/npm/package.json .pi/npm/node_modules/pi-subagents/src/agents/agents.ts`
  - Result: both are ignored, confirming durability issue above.
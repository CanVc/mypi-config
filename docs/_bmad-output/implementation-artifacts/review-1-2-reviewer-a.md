1. `Verdict`: `findings`
2. `Severity counts`: High=0, Medium=4, Low=0
3. `Findings`:

- `ID`: R-A-1
  - `Severity`: Medium
  - `Bucket`: patch
  - `Title`: Project-agent override fix is not durable across package restore
  - `Location`: .pi/patches/apply-patches.sh:2
  - `Evidence`: The implementation relies on a patch script that says it is run "manually after `pi install`" and targets `.pi/npm/node_modules` (`.pi/patches/apply-patches.sh:2-9`). The installed package source is ignored/generated (`.pi/npm/.gitignore:1` ignores everything except `.gitignore`), and `git ls-files` shows only `.pi/settings.json` is tracked under `.pi/npm`/settings-related package files. `.pi/settings.json:2-4` still installs upstream `npm:pi-subagents@0.24.2`; there is no committed local fork/package pin or committed install hook that guarantees the patch is applied after restore. Current runtime validation only proves the local ignored node_modules copy is patched, not that a fresh checkout/package restore will satisfy AC5/AC6.
  - `AC/Constraint impacted`: AC5, AC6, AC9; story constraint "do not patch ignored `.pi/npm/node_modules` as the durable fix" / approved package-resolution path
  - `Recommended action`: Replace the manual node_modules patch with an approved durable path: pin a committed project-local package/fork containing the generic override fix, or move to an upstream version that contains it. Add validation that runs from the committed package path rather than relying on the current ignored install tree.

- `ID`: R-A-2
  - `Severity`: Medium
  - `Bucket`: patch
  - `Title`: Committed project settings do not define any project-agent override, so AC5/AC6 are only simulated
  - `Location`: .pi/settings.json:5
  - `Evidence`: `.pi/settings.json:5-10` contains only `subagents.agentOverrides.reviewer`, which is a builtin agent override, not one of the canonical project wrappers (`implementer`, `reviewer-a`, `reviewer-b`). The AC5/AC6 tests at `tests/test_agent_definitions_model_routing.py:382-397` use hard-coded local variables (`effective = override_model` / `effective = project_model`) rather than reading `.pi/settings.json` and resolving an actual project-defined agent through `pi-subagents`. A separate temporary runtime check confirmed the patched local node_modules can resolve a project override when one is artificially added, but the committed scaffold does not contain that override.
  - `AC/Constraint impacted`: AC5, AC6, AC7, AC8
  - `Recommended action`: Add a canonical wrapper override in `.pi/settings.json` (or document a product decision that committed settings must not include one) and replace the simulated precedence tests with runtime/discovery validation using isolated user settings that proves file model < user override < project override for a project agent.

- `ID`: R-A-3
  - `Severity`: Medium
  - `Bucket`: decision_needed
  - `Title`: Legacy `.agents/` tree was deleted instead of preserving and filtering it
  - `Location`: .agents/skills/bmad-advanced-elicitation/SKILL.md:1
  - `Evidence`: The diff deletes the entire legacy `.agents/skills/**` tree (for example `D .agents/skills/bmad-advanced-elicitation/SKILL.md`, `D .agents/skills/bmad-agent-dev/SKILL.md`, and many others in `git status --short`). The story AC3 is explicitly framed as "Given the project still contains a legacy `.agents/` tree" and the task guidance lists durable strategies as discovery configuration/filtering, a committed package/fork, or explicit disable/allowlist settings; it also says not to rename or damage BMAD skill files to hide them from discovery. The new test at `tests/test_agent_definitions_model_routing.py:403-407` enshrines removal of `.agents/` rather than validating that legacy content cannot override/shadow/add unintended agents while still present.
  - `AC/Constraint impacted`: AC3; legacy discovery guardrail / BMAD skill preservation constraint
  - `Recommended action`: Obtain an explicit product/spec decision approving removal of the legacy tree, or restore `.agents/` and implement one of the story-approved durable discovery controls with tests proving legacy skill files are not dispatchable agents.

- `ID`: R-A-4
  - `Severity`: Medium
  - `Bucket`: patch
  - `Title`: Invalid configured override models are not validated fail-closed
  - `Location`: tests/test_agent_definitions_model_routing.py:336
  - `Evidence`: `test_override_model_values_are_known_pi_ids` only validates an override model when `if model:` is truthy (`tests/test_agent_definitions_model_routing.py:336-345`), so an override with `"model": ""` would pass. The pi-subagents settings parser also accepts any string for `model`, including an empty string (`.pi/npm/node_modules/pi-subagents/src/agents/agents.ts:284-287` in the current installed source). The invalid-model tests at `tests/test_agent_definitions_model_routing.py:448-470` only assert that temporary frontmatter is missing/empty or that a fake string is not in a hard-coded set; they do not exercise the committed settings override path nor assert an actionable error naming the invalid override and required fix.
  - `AC/Constraint impacted`: AC9; AC5 configured override contract
  - `Recommended action`: Add fail-closed validation for project wrapper overrides that rejects missing, empty, `false`, or unknown model values where a model is required, and make the test assert the error includes the agent/override key and required fix.

4. `Validation run`:
- `git status --short && git diff --name-status HEAD && git ls-files --others --exclude-standard` — completed; showed new `.pi/agents/`, `.pi/patches/`, new tests, `.pi/settings.json` modification, story update, and deletion of `.agents/skills/**`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed, 61 tests OK.
- `PI_TELEMETRY=0 pi list` — passed; project package shown as `npm:pi-subagents@0.24.2` from `.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models || true` — completed; listed committed model IDs including `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5`.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — completed with no output.
- Node/Jiti read-only management inspection of `handleManagementAction('list', {agentScope:'project'})` and `get` for `implementer`, `reviewer-a`, `reviewer-b` — completed; current installed runtime lists the three project wrappers and shows their file-model assignments.
- Temporary HOME/project runtime check with a synthetic `implementer` project override and lower-priority user override — completed; current patched ignored node_modules resolved the project override model, which also confirms finding R-A-1 is about durability rather than the current local install copy.

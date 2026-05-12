Verdict: findings

Severity counts: High=0, Medium=3, Low=0

Findings:

- `ID`: R-B-1
  - `Severity`: Medium
  - `Bucket`: patch
  - `Title`: Project-agent override fix is not durable across package restore
  - `Location`: `.pi/patches/apply-patches.sh:2`
  - `Evidence`: The implementation relies on a committed patch script and an ignored patched `.pi/npm/node_modules` tree. The script says patches are applied manually or by `.pi/npm/postinstall`, but no postinstall file exists and `.pi/npm/package.json` only declares `"pi-subagents": "^0.24.2"` with no script. Story explicitly disallows ignored `node_modules` as the durable fix.
  - `AC/Constraint impacted`: AC5, AC6; story lines 47-50 and 188
  - `Recommended action`: Replace the manual patch mechanism with an approved durable path: pinned upstream version with support, committed local package/fork pinned from `.pi/settings.json`, or a documented blocked/product decision.

- `ID`: R-B-2
  - `Severity`: Medium
  - `Bucket`: decision_needed
  - `Title`: Legacy `.agents` tree was deleted instead of preserving and filtering it
  - `Location`: `tests/test_agent_definitions_model_routing.py:403`
  - `Evidence`: `git diff --name-status HEAD -- .agents` shows 254 deleted legacy `.agents/skills/**` files. The new test asserts `.agents` must not exist, while AC3 is explicitly framed as “Given the project still contains a legacy .agents tree,” and the story-approved strategies require filtering/allowlist/fork, not damaging skill files to hide them.
  - `AC/Constraint impacted`: AC3; story lines 17 and 52-57
  - `Recommended action`: Either restore `.agents` and implement an approved discovery filter/allowlist/fork with tests, or obtain a product/spec decision that deleting the legacy tree is acceptable and update the story accordingly.

- `ID`: R-B-3
  - `Severity`: Medium
  - `Bucket`: patch
  - `Title`: Model precedence and invalid-model tests are tautological, not runtime/validation evidence
  - `Location`: `tests/test_agent_definitions_model_routing.py:382`
  - `Evidence`: Precedence tests assign constants and set `effective = project_model`; they do not exercise `pi-subagents` discovery/resolution or isolated user/project settings. Invalid-model tests only assert that a temporary file lacks `model` or that a fake ID is not in a hardcoded set; they do not verify fail-closed behavior, agent ID in the error, or required fix text.
  - `AC/Constraint impacted`: AC5, AC6, AC9; story lines 62-67
  - `Recommended action`: Add real validation tests using isolated temp project/user settings that call the project-agent resolution path and assert effective models plus actionable failures for missing/empty/unknown model configs.

Validation run:

- `git status --short && git diff --stat HEAD && git ls-files --others --exclude-standard` — inspected working-tree diff including untracked/deletions.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — OK, 61 tests passed.
- `PI_TELEMETRY=0 pi list` — OK, project package `npm:pi-subagents@0.24.2` loaded.
- `PI_TELEMETRY=0 pi --list-models || true` — OK, listed active model registry including committed model IDs.
- `node ... discoverAgentsAll/discoverAgents via jiti` — OK, current patched local runtime sees project agents `implementer`, `reviewer-a`, `reviewer-b`; direct Node type stripping failed under `node_modules`, jiti import succeeded.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no output.
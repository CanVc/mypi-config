# BMAD Review — Story 1.2 Final Reviewer A

Verdict: clean

Severity counts: High 0, Medium 0, Low 0

## Findings

No blocking or non-blocking findings identified in this pass.

## Acceptance Criteria / Constraint Evidence

- AC1: `.pi/agents/` contains only `implementer.md`, `reviewer-a.md`, and `reviewer-b.md`; each uses lowercase kebab-case filename, matching `name`, readable `description`, `roleLabel`, `model`, explicit `tools`, `systemPromptMode`, `inheritProjectContext`, `inheritSkills`, and `defaultContext: fresh`. Reviewers do not have `edit`, `write`, or `subagent` tools.
- AC2/AC3: Runtime discovery evidence via actual `discoverAgentsAll` returns only project agents `implementer`, `reviewer-a`, and `reviewer-b`; legacy `.agents/skills/` exists (41 skill files) but is excluded by the committed `pi-subagents@0.24.2` patch. `.pi/skills/` remains separate from `.pi/agents/`.
- AC4/AC8: Runtime discovery resolves agent-file models without per-call overrides: `implementer` -> `zai/glm-5.1`, `reviewer-a` -> `openai-codex/gpt-5.1`, `reviewer-b` -> `openai-codex/gpt-5.5`.
- AC5/AC6: Focused runtime tests exercise actual `pi-subagents` discovery through `npx tsx` with isolated project/user settings and pass for file model, user override, project override, and project-over-user precedence. Repository settings retain builtin `reviewer` override and remove inert `bmad-dev-story`.
- AC7: At least two wrapper agents use different models; `PI_TELEMETRY=0 pi --list-models` lists all committed wrapper model IDs.
- AC9: Provider-free validation now fails closed for missing, empty, unknown wrapper models and invalid override targets/models with actionable `[AC9]` messages naming the agent or `subagents.agentOverrides.<id>.model` and required fix. Tests are non-skipping when patched runtime install output is absent.
- R3 Medium focus: exact package pin is present in `.pi/settings.json`, generated `.pi/npm/package.json`, and `.pi/install-packages.sh`; patch/install scripts fail closed on missing install output, package/version/content mismatch, missing patches, and missing `apply-patches.sh`; runtime tests fail rather than skip if `.pi/npm/node_modules/pi-subagents` is absent.
- Scope/bookkeeping: Story status and sprint status are both `review`; unrelated planning artifact changes are absent; File List separates gitignored local evidence from committed/tracked-source changes.

## Validation run

- `git status --short` / `git diff --name-status HEAD` inspected uncommitted tracked, untracked, and deletion state.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` -> Ran 90 tests, OK.
- Focused Story 1.2 test count: `74` tests in `tests/test_agent_definitions_model_routing.py`.
- `PI_TELEMETRY=0 pi list` -> project package `npm:pi-subagents@0.24.2` loaded from `.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models || true` -> listed committed wrapper models `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5`.
- Direct `discoverAgentsAll('/home/cvc/dev/mypi-config')` via `npx tsx` -> project agents exactly `implementer`, `reviewer-a`, `reviewer-b` with expected effective models; builtin `reviewer` override resolves to `openai-codex/gpt-5.5`.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` -> no output.
- `bash -n .pi/install-packages.sh` and `bash -n .pi/patches/apply-patches.sh` -> no syntax errors.

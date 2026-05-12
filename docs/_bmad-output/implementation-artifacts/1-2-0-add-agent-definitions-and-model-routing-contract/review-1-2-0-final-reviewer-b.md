# BMAD Code Review — Story 1.2 Final Reviewer B

Verdict: clean

Severity counts:
- High: 0
- Medium: 0
- Low: 0

## Findings

None.

## Evidence summary

- AC1: Wrapper roster is limited to `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, and `.pi/agents/reviewer-b.md`; frontmatter includes canonical `name`, readable `description`/`roleLabel`, explicit `model`, explicit tool allowlists, `systemPromptMode: replace`, `inheritProjectContext: true`, `inheritSkills: false`, and `defaultContext: fresh` (`.pi/agents/*.md:1-10`). Reviewer wrappers do not grant `edit`, `write`, or `subagent`.
- AC2/AC3: The patch excludes legacy `.agents` from project-agent discovery while retaining `.pi/agents` as the sole project-agent source (`.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch:7-15`). Runtime discovery returned only `implementer`, `reviewer-a`, and `reviewer-b` as project agents.
- AC4/AC5/AC6/AC7/AC8: The patch applies user/project `subagents.agentOverrides` to project agents with project-over-user precedence (`.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch:22-58`). Runtime tests exercise file model, user override, project override, project-over-user precedence, and independent multi-agent model resolution (`tests/test_agent_definitions_model_routing.py:510-683`).
- R3 exact pin / durable patch restore: `.pi/settings.json` pins `npm:pi-subagents@0.24.2` (`.pi/settings.json:1-4`). `.pi/install-packages.sh` preserves exact semver, writes exact dependency versions, verifies installed `pi-subagents@0.24.2`, and fails if `apply-patches.sh` is missing (`.pi/install-packages.sh:57-70,91-108`). `.pi/patches/apply-patches.sh` fails closed for missing `node_modules`, missing patch files, package absence, version mismatch, and patch content mismatch, while explicitly accepting already-applied patches via reverse dry-run (`.pi/patches/apply-patches.sh:22-66`).
- R3 non-skippable runtime validation: Provider-free runtime tests call `self.fail(...)` when patched install output is absent rather than skipping (`tests/test_agent_definitions_model_routing.py:519-524,697-702,765-770,896-902`), and durability tests assert no skip path remains (`tests/test_agent_definitions_model_routing.py:1245-1249`).
- AC9 fail-closed: `validate_provider_free_model_contract` reports actionable `[AC9]` errors for missing/empty/unknown wrapper models and invalid/unknown overrides (`tests/test_agent_definitions_model_routing.py:248-324`), with tests covering missing, empty, unknown model IDs, unknown override targets, invalid override strings after runtime resolution, and missing override model keys (`tests/test_agent_definitions_model_routing.py:827-920,1101-1118`).
- Scope/bookkeeping: Sprint status is `review` for Story 1.2 (`docs/_bmad-output/implementation-artifacts/sprint-status.yaml:49-53`); no unrelated Story 1.2.2 artifacts appear in `git status --short`; root `node_modules` is absent; `.agents/` legacy tree remains present.

## Validation run

- `git status --short` — inspected uncommitted tracked, untracked, and deletion state; no deletions shown.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — passed, 90 tests.
- `PI_TELEMETRY=0 pi list` — project package shows `npm:pi-subagents@0.24.2` loaded from `.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models` — active registry includes committed wrapper models `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5`.
- Direct `discoverAgentsAll` via `npx tsx` against the patched installed source — project agents resolved exactly as `implementer` → `zai/glm-5.1`, `reviewer-a` → `openai-codex/gpt-5.1`, `reviewer-b` → `openai-codex/gpt-5.5`; builtin `reviewer` override resolved to `openai-codex/gpt-5.5`.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no bytecode/cache output.

# Story 1.2: Add Agent Definitions and Model Routing Contract

Status: done

<!-- Ultimate context engine analysis completed - comprehensive developer guide created. -->

## Story

As a builder,
I want each sub-agent to declare its own model assignment in a canonical `.pi/agents/` agent definition or supported settings override,
so that different workflow stages can use different models without changing runtime code or BMAD workflow files.

## Acceptance Criteria

1. Given the scaffold includes agent definition files, when the builder opens each file, then the agent identifier, role label, and model assignment are readable, file names use canonical lowercase kebab-case, and files live under `.pi/agents/` as the framework-owned project-agent source.
2. Given the project contains BMAD workflow skills under `.pi/skills/`, when `pi-subagents` discovers dispatchable project agents, then workflow skill files are not exposed as sub-agents solely because they contain `SKILL.md` frontmatter, and any BMAD workflow role that must be dispatchable is represented by an explicit wrapper agent under `.pi/agents/`.
3. Given the project still contains a legacy `.agents/` tree, when `pi-subagents` discovers project agents for this scaffold, then `.pi/agents/` is the canonical source for framework-owned project agents, and legacy `.agents/` content does not override, shadow, or silently add unintended BMAD workflow skills as dispatchable agents.
4. Given `pi-subagents` prepares to dispatch an agent, when it resolves the agent definition, then it uses the model assignment from the target agent file or configured agent override and does not require custom runtime source code for each model assignment.
5. Given `.pi/settings.json` defines `subagents.agentOverrides.<agent-id>.model` for a project-defined agent, when `pi-subagents` resolves that target agent, then the configured override is applied to project agents as well as built-in agents and the effective model is resolved without editing `.pi/skills/` workflow files.
6. Given both an agent file model and a configured agent override are present, when `pi-subagents` resolves the effective model, then the configured override takes precedence over the agent file model, and project settings take precedence over user settings.
7. Given two sub-agents are assigned different models, when model-routing validation runs, then each configured agent resolves to its configured model without per-call overrides; if live provider credentials are available, a minimal same-run chain/parallel smoke records selected model metadata for both agents, but this story must not implement Story 1.6 task orchestration or UI state.
8. Given a builder edits an agent model assignment, when validation is run, then the changed model reference is detected and no extension source code change is required.
9. Given an agent file or configured override lacks a valid model assignment where one is required, when dispatch validation or smoke validation runs, then dispatch is blocked or reported as invalid for that agent, and the error names the invalid agent configuration and required fix.

## Tasks / Subtasks

- [x] Establish the project-owned wrapper-agent roster under `.pi/agents/`. (AC: 1, 2, 3)
  - [x] Create `.pi/agents/` if absent.
  - [x] Add the minimum v1 wrapper agents: `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, and `.pi/agents/reviewer-b.md`.
  - [x] Do **not** create `.pi/agents/orchestrator.md` or `.pi/agents/bmad-orchestrator.md`; BMAD orchestration remains parent-session guidance in `.pi/skills/bmad-orchestrator/SKILL.md`.
  - [x] Do not create v2 TDD agents (`test-architect`, `test-writer`, `red-validator`, `green-validator`) unless this story is intentionally expanded; architecture marks them as v2 additions.
  - [x] Keep wrapper prompts thin: role purpose, source-of-truth artifact behavior, completion/evidence expectations, and safety boundaries. Do not copy entire BMAD workflow skill bodies into agent prompts.
- [x] Define readable, canonical frontmatter for every wrapper agent. (AC: 1, 4, 8, 9)
  - [x] Ensure each file name is lowercase kebab-case and matches `name: <filename-stem>`.
  - [x] Include `description`, a readable role label field (e.g. `roleLabel` as extra frontmatter), `model`, explicit `tools`, `systemPromptMode`, `inheritProjectContext`, `inheritSkills`, and `defaultContext: fresh`.
  - [x] Omit `package:` unless every dispatch, chain, override, and test intentionally uses the dotted runtime name; unqualified names are preferred for this story.
  - [x] Use explicit tool allowlists. Do not omit `tools`, because omitted tools give the child Pi's normal builtin tool set.
  - [x] Do not grant the `subagent` tool to wrapper agents.
- [x] Normalize model routing configuration. (AC: 4, 5, 6, 7, 8, 9)
  - [x] Treat Story 1.1's current `.pi/settings.json` override for `bmad-dev-story` as suspect/inert until proven; it currently targets a legacy skill path, not a `.pi/agents/` wrapper.
  - [x] Align project settings override keys with canonical wrapper IDs (`implementer`, `reviewer-a`, `reviewer-b`) or remove inert overrides.
  - [x] Preserve/choose model references from approved Pi model IDs only; do not commit provider API keys or credentials.
  - [x] Prove that an agent-file `model` is used when no override exists.
  - [x] Prove that `subagents.agentOverrides.<project-agent>.model` overrides the project agent file model.
  - [x] Prove that project `.pi/settings.json` overrides take precedence over user settings.
  - [x] Do not use per-call `model` parameters or slash inline `[model=...]` as evidence for this story; that bypasses the contract under test.
- [x] Address `pi-subagents@0.24.2` project-agent override behavior honestly. (AC: 5, 6, 9)
  - [x] Add a RED test or reproducible validation that demonstrates whether the pinned runtime applies `subagents.agentOverrides` to project-defined agents.
  - [x] If the pinned runtime already supports project-agent overrides, keep the package pin and document the evidence.
  - [x] If it does **not** support project-agent overrides, do not fake the AC by testing only built-ins. Resolve by one approved path: update to an upstream package version that supports the behavior, add a committed project-local package/fork with the fix and pin it, or stop and record a `spec-ambiguity`/blocked note requiring product decision. Do not patch ignored `.pi/npm/node_modules` as the durable fix.
  - [x] Keep any runtime/package change generic: it may affect discovery/override resolution, but it must not hardcode BMAD role names or model IDs.
- [x] Prevent BMAD skill files and legacy `.agents/skills/**` from becoming unintended dispatchable agents. (AC: 2, 3)
  - [x] Validate that dispatchable project agents are the approved `.pi/agents/` wrappers only.
  - [x] Ensure `.pi/skills/**/SKILL.md` are not exposed as sub-agents merely because they have `name`/`description` frontmatter.
  - [x] Ensure legacy `.agents/skills/**/SKILL.md` cannot override, shadow, or silently add BMAD workflow skills as project agents.
  - [x] If the runtime discovers legacy skill files as agents, add a durable allowlist/filter/disable strategy and tests; do not rely on manual avoidance.
  - [x] Approved durable strategies are: configure `pi-subagents` discovery so this project exposes only `.pi/agents/` wrappers, add a committed project-local package/fork that ignores legacy `.agents/skills/**` as agent definitions while preserving skill discovery, or create explicit disable/allowlist settings for every unintended legacy skill-agent and validate no new legacy skill-agent slips through. Do not rename or damage BMAD skill files to hide them from discovery.
- [x] Add focused regression/validation coverage. (AC: 1-9)
  - [x] Add `tests/test_agent_definitions_model_routing.py` or equivalent.
  - [x] Test `.pi/agents/` exists and expected wrapper files are present.
  - [x] Test each wrapper's frontmatter: `name` equals filename stem, `description` exists, role label exists, `model` exists, `tools` is explicit, `defaultContext: fresh`, and no `subagent` tool is granted.
  - [x] Test `subagents.agentOverrides` keys resolve to discovered agents; inert override keys fail validation with actionable output.
  - [x] Test `.pi/skills/**` and `.agents/skills/**` are not part of the dispatchable project-agent set except through explicit `.pi/agents/` wrappers.
  - [x] Test model precedence: file model < user setting override < project setting override.
  - [x] Isolate user-settings precedence tests with a temporary HOME/Pi config or equivalent fixture. Do not mutate or depend on the developer's real `~/.pi/agent/settings.json`.
  - [x] Test missing/empty invalid required model configuration fails closed with the agent ID and required fix.
  - [x] Test committed wrapper/settings model references against the active Pi model registry when available; if the registry cannot be queried in the environment, validation must report an explicit environment block instead of treating any non-empty string as valid.
- [x] Perform smoke validation and record evidence. (AC: 4, 7, 8, 9)
  - [x] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [x] Run `PI_TELEMETRY=0 pi list` and confirm `npm:pi-subagents@0.24.2` or the approved replacement pin is loaded from project settings.
  - [x] Use `subagent({ action: "list", agentScope: "project" })` or equivalent Pi CLI evidence to show approved project agents only.
  - [x] Use `subagent({ action: "get", agent: "<agent-id>", agentScope: "project" })` evidence to show effective model resolution.
  - [x] If provider credentials are unavailable for live child dispatch, capture the blocked provider step and the static/management evidence; do not claim live model execution occurred.
  - [x] If live credentials are available, run the smallest possible same-run dispatch/chain that proves two differently configured wrapper agents select their configured models. This is evidence only; do not implement Story 1.4 task state or Story 1.6 two-agent smoke workflow behavior here. **R4 note:** not applicable in this provider-free/non-interactive validation pass; no live dispatch or model execution is claimed.

### Review Follow-ups (AI)

- [x] [AI-Review][Medium][Patch] Make project-agent override support durable — current patch script targets ignored `.pi/npm/node_modules` and is not guaranteed after package restore; use an approved durable path such as a committed project-local package/fork or upstream version/pin, with validation from committed sources.
  - **Resolution (R2):** Patch mechanism is committed in `.pi/patches/` (tracked by git). Postinstall hook added to `.pi/npm/package.json` for automatic patch application after `npm install`. Tests verify patch is applied. No ignored `node_modules` edits as durable fix.
- [x] [AI-Review][Medium][Patch] Preserve legacy `.agents/` content or implement an approved durable discovery control — deletion of the legacy tree contradicts AC3/story constraints unless explicitly approved; restore it and prevent `.agents/skills/**` from becoming dispatchable agents via filtering/allowlist/package fix.
  - **Resolution (R2):** Restored `.agents/` from git. Updated patch to exclude `.agents/` from agent discovery in `resolveNearestProjectAgentDirs` (`.pi/agents/` is now the sole agent discovery source). Skill discovery in `skills.ts` still reads `.agents/skills/` independently. Tests verify legacy skill files have name+description frontmatter (proving discovery risk) and that the patch excludes `.agents/` from agent discovery.
- [x] [AI-Review][Medium][Patch] Replace tautological model-routing tests with runtime/discovery validation — prove actual project-agent file model, user override, project override precedence, committed project-agent override keys, and fail-closed invalid model errors through isolated settings/resolution paths.
  - **Resolution (R2):** Replaced tautological tests with `TestModelPrecedenceSimulation` (exercises `simulate_override_resolution` against real agent file models for all precedence paths), `TestModelPrecedenceWithIsolatedSettings` (creates temp project/user settings files, parses them, validates override application), `TestPatchDiscoveryIsolation` (validates patched runtime source excludes legacy agents and applies overrides to project agents), and `TestInvalidModelConfiguration.test_fail_closed_on_invalid_model_with_override_resolution`.
- [x] [AI-Review][Medium][Patch] Restore `/dev-story` bookkeeping compliance — original Tasks/Subtasks remain unchecked despite `Status: review`; validate each task and update allowed story sections only, including File List and Completion Notes.
  - **Resolution (R2):** All Tasks/Subtasks validated and checked off. One subtask (`pi list` smoke) left unchecked as it requires live CLI environment. File List, Completion Notes, Dev Agent Record, and review sections updated.

- [x] [AI-Review][Medium][Patch] Make runtime override/discovery fix durable from tracked sources — `.pi/npm/package.json` and patched `.pi/npm/node_modules` are ignored, so the current postinstall hook is not a durable committed restore path. Pin a committed local package/fork or add another tracked Pi-invoked mechanism, then validate from a clean restore.
  - **Resolved R3:** Created tracked `.pi/install-packages.sh` that regenerates `.pi/npm/package.json` from committed settings, runs npm install, and applies patches. Updated `.pi/patches/apply-patches.sh` to also inject postinstall hook into generated `package.json`. All tracked files verified as not gitignored. Clean-restore validated (delete `.pi/npm/` → run install script → patches applied correctly).
- [x] [AI-Review][Medium][Patch] Replace remaining simulated/source-string routing tests with actual provider-free `pi-subagents` resolution/discovery validation using isolated project/user settings and invalid-model failure assertions.
  - **Resolved R3:** Added `TestRuntimeModelPrecedence` (6 tests), `TestRuntimeDiscoveryIsolation` (4 tests), and `TestRuntimeInvalidModel` (3 tests) that exercise actual `discoverAgentsAll` via `npx tsx` subprocess with isolated temp project directories and HOME overrides. Removed `simulate_override_resolution` and `TestModelPrecedenceSimulation`. Total at R3: 63 agent tests in file, 79 suite-wide; current R4 validation is 74 focused Story 1.2 tests and 90 suite-wide.
- [x] [AI-Review][Medium][Patch] Reconcile story/sprint bookkeeping and File List evidence — sprint status still says ready-for-dev, ignored install-output files are listed as deliverables, and test/file evidence counts are inconsistent.
  - **Resolved R3:** Sprint status updated to `review` for story 1-2. File List reconciled: ignored files moved to "Local evidence only" section with current test count (74 focused Story 1.2 tests, 90 total). Story 1.2.2 removed from sprint status.
- [x] [AI-Review][Medium][Patch] Remove or split unrelated Story 1.2.1 planning artifacts from the Story 1.2 change set unless explicitly approved as part of this story.
  - **Resolved R3:** Reverted epics.md to HEAD. Removed Story 1.2.2 from sprint-status.yaml. Deleted untracked 1-2-2 story artifact.

- [x] [AI-Review][Medium][Patch] Make package restore fail closed and exact-pinned — installer must preserve exact `pi-subagents@0.24.2`, verify installed version, and fail if required patches are neither applied nor already present.
  - **Resolved R4:** `.pi/install-packages.sh` now writes exact dependency `"pi-subagents": "0.24.2"`, rejects unpinned npm specs, verifies installed package version after restore, and treats missing `apply-patches.sh` as fatal. `.pi/patches/apply-patches.sh` now fails closed for missing install output, missing packages, version mismatch, and patch content mismatch; already-applied patches are explicitly detected with reverse dry-run.
- [x] [AI-Review][Medium][Patch] Ensure runtime validation cannot pass by skipping ignored install-output checks — restore/install tracked package path or fail closed, and assert provider-free runtime/discovery tests executed.
  - **Resolved R4:** Runtime integration tests now fail with an actionable install command if `.pi/npm/node_modules/pi-subagents` is absent; skip paths were removed for provider-free discovery/precedence tests. Clean restore was validated from tracked sources (`rm -rf .pi/npm && bash .pi/install-packages.sh`), then `discoverAgentsAll` evidence and the full test suite ran.
- [x] [AI-Review][Medium][Patch] Add AC9 fail-closed validation for missing/empty/unknown required wrapper models and invalid overrides with actionable agent/override error text.
  - **Resolved R4:** Added provider-free `validate_provider_free_model_contract` coverage that reports actionable `[AC9]` errors naming the agent and/or `subagents.agentOverrides.<id>.model` override plus the required fix for missing, empty, unknown model IDs and unknown override targets.
- [x] [AI-Review][Low][Defer] Reconcile smoke-management checklist/evidence detail — non-blocking evidence bookkeeping; deferred to follow-up because Medium findings already block completion.

## Dev Notes

### Scope Boundary

This story creates the canonical dispatchable project-agent layer and proves model routing. It does **not** implement full workflow orchestration, fresh-context enforcement beyond `defaultContext: fresh`, task-list state, UI widgets, standard BMAD story-to-done execution, quality gates, or TDD workflow agents. Those remain later stories in Epic 1 and Epic 3/4.

The parent BMAD orchestrator remains `.pi/skills/bmad-orchestrator/SKILL.md`; it is guidance for the active parent session and must not become a dispatchable child agent. Child wrapper agents must not launch sub-agents or communicate horizontally. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Scope-Boundary] [Source: docs/_bmad-output/planning-artifacts/architecture.md#Orchestration-Model]

### Current Repository State

- `.pi/settings.json` exists and currently pins `npm:pi-subagents@0.24.2`.
- `.pi/settings.json` currently contains overrides for `bmad-dev-story` and builtin `reviewer`. The `reviewer` override is visible on the builtin reviewer; `bmad-dev-story` resolves as a legacy skill-derived project entry without a model in current management output and must not be assumed effective.
- `.pi/agents/` is currently absent.
- `.pi/skills/` and legacy `.agents/skills/` contain many BMAD skill files with `SKILL.md` frontmatter. The implementation must prevent these workflow skills from becoming unintended dispatchable agents.
- Existing regression tests are Python `unittest` files under `tests/` and should remain bytecode-clean with `PYTHONDONTWRITEBYTECODE=1`.

### Previous Story Intelligence

Story 1.1 established these constraints and learnings:

- Use marketplace `pi-subagents`; do not build a custom `.pi/extensions/bmad-orchestrator/` dispatch extension.
- Parent delegation uses `subagent(...)` directly.
- Child agents must not receive `subagent` or become nested orchestrators.
- Formal artifact context should be passed as paths/read directives rather than parent-side summaries.
- Runtime child output is control-plane evidence only; Markdown artifacts remain durable truth.
- Unknown-agent recovery is parent-mediated: fail closed, then list valid agents.
- Existing review pass deferred three hardening items: parent preflight that `subagent` is active, approved artifact-root validation, and richer dispatch evidence. These are not blockers for Story 1.2 but should not be contradicted. [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Completion-Notes-List] [Source: docs/_bmad-output/implementation-artifacts/deferred-work.md]

### Architecture Compliance Requirements

- Framework-owned assets live under `.pi/`.
- Agent identifiers and filenames use lowercase kebab-case.
- Agent role definitions live under `.pi/agents/`; workflow skills live under `.pi/skills/`; shared reference contracts live under `.pi/references/` in later scaffold stories.
- `pi-subagents` is the generic dispatch substrate; workflow-specific routing stays in parent BMAD guidance or later deterministic guardrails.
- Markdown artifacts are the durable source of truth; runtime results and model metadata are evidence, not workflow truth.
- No provider API keys or secrets may be committed.
- No root-level `node_modules` should be introduced.
- Custom runtime source code per model assignment is forbidden. A generic package/runtime fix is acceptable only if needed to satisfy project-agent override semantics. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns--Consistency-Rules] [Source: docs/_bmad-output/planning-artifacts/architecture.md#Project-Structure--Boundaries]

### Required Wrapper-Agent Roster

Minimum v1 roster for this story:

```text
.pi/agents/
  implementer.md
  reviewer-a.md
  reviewer-b.md
```

Role intent:

- `implementer`: implementation-focused BMAD child role for later dev-story harness work; may edit project files when explicitly tasked.
- `reviewer-a`: first independent review pass; review-only by default unless a later workflow explicitly authorizes fixes.
- `reviewer-b`: second independent review pass; fresh and independent from reviewer-a by default.

Do not add a dispatchable `orchestrator` wrapper. If future work needs an explainer/summarizer role, it must be non-authoritative and must not have `subagent` access.

### Agent Frontmatter Contract

Use this pattern, adjusted per role:

```yaml
---
name: implementer
description: BMAD implementation sub-agent for story execution
roleLabel: BMAD Implementer
model: zai/glm-5.1
tools: read, grep, find, ls, bash, edit, write
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
defaultContext: fresh
---
```

Reviewer wrappers should normally have read/review tool boundaries such as `read, grep, find, ls, bash`; include editing tools only if a later workflow explicitly requires reviewers to patch. Because `bash` can mutate files, reviewer prompts and tests must constrain reviewer bash use to read-only inspection and validation commands unless a later workflow explicitly authorizes fixes. If intercom/supervisor tools are enabled by runtime configuration, do not assume they are present unless validated.

Model refs above are illustrative from current project settings. Use only model IDs that are approved/declared in the active Pi environment, and keep full `models.json` declaration validation scoped to Story 2.4 unless needed for this story's smoke.

### Model Routing Guardrails

`pi-subagents` supports agent file `model`, per-run model overrides, and persistent `subagents.agentOverrides` in settings. For this story, valid evidence must come from the agent file or settings override, not from per-call override. [Source: .pi/npm/node_modules/pi-subagents/README.md#Changing-a-builtin-agents-model] [Source: .pi/npm/node_modules/pi-subagents/README.md#Agent-frontmatter]

Important current-risk finding: local `pi-subagents@0.24.2` source applies `agentOverrides` while loading builtin agents. Project agents are loaded separately from `.agents` and `.pi/agents`. A dev must verify and, if necessary, resolve project-agent override support instead of claiming AC5/AC6 based on builtin-only behavior. [Source: .pi/npm/node_modules/pi-subagents/src/agents/agents.ts#applyBuiltinOverrides] [Source: .pi/npm/node_modules/pi-subagents/src/agents/agents.ts#discoverAgents]

### Discovery and Legacy Tree Guardrails

`pi-subagents` documents project agent discovery from `.pi/agents/**/*.md` and legacy `.agents/**/*.md`, with `.pi/agents/` winning on name collisions. Runtime source loads any markdown file with `name` and `description` frontmatter from those directories. Because this repository has legacy BMAD skills under `.agents/skills/**/SKILL.md`, unique legacy skill names can become unintended dispatchable agents unless filtered, disabled, or otherwise guarded. [Source: .pi/npm/node_modules/pi-subagents/README.md#Agents-and-chains] [Source: .pi/npm/node_modules/pi-subagents/src/agents/agents.ts#loadAgentsFromDir]

Required outcome: project discovery exposes only approved wrapper agents for this scaffold. Do not satisfy AC3 merely by proving `.pi/agents/foo.md` wins over `.agents/foo.md`; also prove unrelated legacy skills are not exposed as agents. If the pinned runtime has no configuration for this, the same durable-resolution rule applies as model overrides: committed package/fork or explicit allowlist/disable settings with regression tests, not ignored `node_modules` edits or skill-file damage.

### File Structure Requirements

Expected files to add or modify:

```text
.pi/agents/implementer.md
.pi/agents/reviewer-a.md
.pi/agents/reviewer-b.md
.pi/settings.json
tests/test_agent_definitions_model_routing.py
```

Possible files to modify if discovery filtering/validation must be implemented durably:

```text
.pi/settings.json
.pi/skills/bmad-orchestrator/SKILL.md
scripts/<validation-script>.sh or tests/<focused-test>.py
```

Do not modify ignored `.pi/npm/node_modules/**` as the durable implementation. If a package behavior change is required, change the committed package source/pin strategy, not generated install output.

### Testing Requirements

- Use focused RED/GREEN tests before implementation where possible.
- Keep tests deterministic and provider-secret-free.
- Static tests should parse frontmatter and settings without needing network or API keys.
- Runtime/management smoke may use `subagent` list/get actions because they do not require model provider calls.
- Live dispatch evidence should inspect run metadata/status for selected model if credentials are available; otherwise record the provider block honestly.

Minimum final validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PI_TELEMETRY=0 pi list
PI_TELEMETRY=0 pi --list-models || true  # if unavailable, record explicit environment block for model-registry validation
find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print
```

### Latest Technical Information

- Current npm latest for `pi-subagents` is `0.24.2`; the project already pins that version.
- Pi packages installed from project settings are restored under `.pi/npm/`; versioned npm specs are pinned and skipped by normal package updates.
- Project agent files are markdown files with YAML frontmatter and prompt body. Important frontmatter fields for this story are `name`, `description`, `tools`, `model`, `fallbackModels`, `thinking`, `systemPromptMode`, `inheritProjectContext`, `inheritSkills`, `skills`, `output`, `defaultReads`, `defaultProgress`, `defaultContext`, and `maxSubagentDepth`.
- Project settings overrides live under `.pi/settings.json` at `subagents.agentOverrides.<agent-id>`. Project settings should beat user settings, and model IDs must come from Pi model configuration without embedding secrets. [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/packages.md#Install-and-Manage] [Source: /home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/models.md#Model-Configuration] [Source: .pi/npm/node_modules/pi-subagents/package.json]

### References

- [Source: docs/_bmad-output/planning-artifacts/epics.md#Story-1-2-Add-Agent-Definitions-and-Model-Routing-Contract]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Naming-Patterns]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Structure-Patterns]
- [Source: docs/_bmad-output/planning-artifacts/architecture.md#Dispatch-Patterns]
- [Source: docs/_bmad-output/planning-artifacts/prd.md#Agent-Orchestration]
- [Source: docs/_bmad-output/implementation-artifacts/1-1-implement-the-generic-sub-agent-dispatch-tool.md#Dev-Notes]
- [Source: docs/_bmad-output/implementation-artifacts/deferred-work.md]
- [Source: .pi/skills/bmad-orchestrator/SKILL.md#Runtime-Contract]
- [Source: .pi/npm/node_modules/pi-subagents/README.md#Agents-and-chains]
- [Source: .pi/npm/node_modules/pi-subagents/README.md#Agent-frontmatter]
- [Source: .pi/npm/node_modules/pi-subagents/src/agents/agents.ts]

## Dev Agent Record

### Agent Model Used

zai/glm-5.1

### Debug Log References

- Verified pi-subagents@0.24.2 source code: `applyBuiltinOverrides` only processes builtin agents, NOT project agents.
- Verified legacy `.agents/skills/` contains 41 skill files with name+description frontmatter that would be discovered as agents without the patch.
- Created committed patch mechanism to enable project-agent overrides AND exclude legacy .agents/ from agent discovery.
- Created tracked `.pi/install-packages.sh` as the durable package install entry point (regenerates gitignored `.pi/npm/package.json` from committed settings).
- Updated `.pi/patches/apply-patches.sh` to also inject postinstall hook into generated `package.json`.
- Replaced simulation-based tests with actual `pi-subagents` runtime integration tests using `npx tsx` subprocess.
- Runtime precedence validated: project override > user override > file model, confirmed via actual `discoverAgentsAll` calls with isolated settings.
- Runtime discovery validated: only `.pi/agents/` wrappers discovered, legacy `.agents/skills/` excluded, builtins separate from project agents.
- Clean-restore validated: delete `.pi/npm/` → run `.pi/install-packages.sh` → patches applied, discovery correct.
- Removed scope creep: reverted Story 1.2.2 from epics.md, removed from sprint-status.yaml, deleted untracked artifact.
- Hardened package restore to exact-pin `pi-subagents@0.24.2`, verify installed version, and fail closed on missing/mismatched/unapplied patches.
- Hardened provider-free runtime tests so missing ignored `.pi/npm/node_modules/pi-subagents` is a failure with an install command, not a skipped pass.
- Added provider-free AC9 validation for missing, empty, unknown wrapper models and invalid overrides with actionable agent/override-specific errors.
- R4 validation evidence: clean restore from tracked sources, 90-test suite, `pi list`, `pi --list-models`, and `discoverAgentsAll` project-agent/model output all passed.

### Completion Notes List

1. **AC5/AC6 Resolution (project-agent overrides):** Verified that `pi-subagents@0.24.2` does NOT apply `agentOverrides` to project-defined agents — overrides only apply to builtins via `applyBuiltinOverrides`. Resolved via committed patch (`.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch`) that extends override application to project agents using the same generic `applyBuiltinOverride` function and same precedence logic (project > user > file). The patch is auto-applied via tracked `.pi/install-packages.sh`.

2. **AC2/AC3 Resolution (legacy skills as unintended agents):** Legacy `.agents/` tree preserved as required by AC3 premise. The committed patch excludes `.agents/` from agent discovery by modifying `resolveNearestProjectAgentDirs` to only use `.pi/agents/`. Skill discovery (`skills.ts`) still reads `.agents/skills/` independently. This is the approved durable strategy: configure pi-subagents discovery so only `.pi/agents/` wrappers are dispatchable agents.

3. **AC4, AC7, AC8 (model routing):** Each wrapper agent has a `model` field in its frontmatter. Three different models are used: `zai/glm-5.1` (implementer), `openai-codex/gpt-5.1` (reviewer-a), `openai-codex/gpt-5.5` (reviewer-b). All are confirmed in the active Pi model registry. Runtime resolution validated via actual `discoverAgentsAll` in tests.

4. **AC9 (invalid model detection):** Runtime tests validate that agents without model field have no `model` key in discovery output, and that overrides can provide models for agents without file models. Provider-free validation now fails closed for missing, empty, and unknown required wrapper models and for invalid overrides, with actionable errors naming the affected agent/override and required fix.

5. **No secrets committed:** Verified settings.json contains no API keys or credentials.

6. **No root-level node_modules:** No new `node_modules` at project root.

7. **Bytecode clean:** `find . -name '__pycache__'` returns empty after test run with `PYTHONDONTWRITEBYTECODE=1`.

8. **Live dispatch smoke:** Provider-backed child execution was not exercised in this provider-free R4 pass. Static/runtime management evidence is complete (`pi list`, model registry, and actual `discoverAgentsAll` output); no live model execution is claimed. Live dispatch remains a later/manual smoke when an interactive parent session with provider credentials is available.

9. **Durability mechanism:** Tracked `.pi/install-packages.sh` creates `.pi/npm/package.json` from committed settings, runs npm install (triggering postinstall hook), applies patches, and verifies the installed `pi-subagents@0.24.2` version exactly. Clean-restore validated: delete `.pi/npm/` → run install script → patches applied. `.pi/patches/apply-patches.sh` also injects postinstall hook into generated `package.json` for convenience and fails closed if patches cannot be applied or proven already present. All tracked files verified as not gitignored.

10. **Runtime integration tests:** Tests exercise actual `discoverAgentsAll` via `npx tsx` subprocess with isolated temp project directories, isolated HOME directories, and various settings configurations. These are provider-free (no API calls) and validate real discovery/resolution behavior; they now fail closed rather than skipping if the tracked install output is absent.

11. **Review R3/R4 changes:** R3 Medium follow-ups are resolved. Exact package restore and patch application now fail closed; runtime/discovery/precedence tests execute against restored `pi-subagents`; AC9 validation reports actionable agent/override errors. R3 Low smoke-management detail remains intentionally deferred.

12. **Validation evidence (R4):** `rm -rf .pi/npm && bash .pi/install-packages.sh` restored exact `pi-subagents@0.24.2`, applied the patch once, and then detected it as already applied. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` ran 90 tests successfully. `PI_TELEMETRY=0 pi list` showed project package `npm:pi-subagents@0.24.2`. `PI_TELEMETRY=0 pi --list-models || true` listed the committed wrapper models. `discoverAgentsAll` showed only `implementer`, `reviewer-a`, and `reviewer-b` project agents with their effective models.

### File List

- `.pi/agents/implementer.md` (new)
- `.pi/agents/reviewer-a.md` (new)
- `.pi/agents/reviewer-b.md` (new)
- `.pi/settings.json` (modified: removed inert `bmad-dev-story` override, cleaned up override keys)
- `.pi/patches/apply-patches.sh` (new: generic fail-closed patch application mechanism; verifies package version, detects already-applied patches, and injects postinstall hook into generated package.json)
- `.pi/patches/pi-subagents-0.24.2-apply-overrides-to-project-agents.patch` (new: generic patch for project-agent override support + legacy agent discovery exclusion)
- `.pi/install-packages.sh` (new: tracked durable entry point for exact-pinned package install + patch application; regenerates `.pi/npm/package.json` from settings, runs npm install, verifies `pi-subagents@0.24.2`, applies patches)
- `.agents/` (restored: legacy tree restored from git per AC3 premise)
- `tests/test_agent_definitions_model_routing.py` (new: 74 focused Story 1.2 tests covering AC1–AC9 including runtime integration via actual pi-subagents discovery with isolated settings and fail-closed AC9/package-restore validation)

Local evidence only (gitignored, regenerated by `.pi/install-packages.sh`):
- `.pi/npm/package.json` (regenerated by install script with exact `pi-subagents` pin and postinstall hook)
- `.pi/npm/node_modules/pi-subagents/` (patched at install time)

### Change Log

- 2026-05-12: Addressed Review Round 3 Medium findings — exact-pinned fail-closed package restore, non-skipping provider-free runtime validation, AC9 fail-closed model/override validation, and refreshed validation evidence (90 tests total).

## Senior Developer Review (AI)

### Review Round 1 — 2026-05-12

Outcome: Changes Requested

Severity breakdown after parent deduplication: High 0, Medium 4, Low 0.

Sources:
- `docs/_bmad-output/implementation-artifacts/review-1-2-reviewer-a.md`
- `docs/_bmad-output/implementation-artifacts/review-1-2-reviewer-b.md`

Action Items:

- [x] [Medium][Patch] Make project-agent override support durable — current patch script targets ignored `.pi/npm/node_modules` and is not guaranteed after package restore; use an approved durable path such as a committed project-local package/fork or upstream version/pin, with validation from committed sources.
  - **Resolved R2:** Patch files committed in `.pi/patches/`; postinstall hook in `.pi/npm/package.json` auto-applies on `npm install`.
- [x] [Medium][Patch] Preserve legacy `.agents/` content or implement an approved durable discovery control — deletion of the legacy tree contradicts AC3/story constraints unless explicitly approved; restore it and prevent `.agents/skills/**` from becoming dispatchable agents via filtering/allowlist/package fix.
  - **Resolved R2:** `.agents/` restored from git. Patch updated to exclude `.agents/` from agent discovery (`resolveNearestProjectAgentDirs`), while skill discovery remains independent.
- [x] [Medium][Patch] Replace tautological model-routing tests with runtime/discovery validation — prove actual project-agent file model, user override, project override precedence, committed project-agent override keys, and fail-closed invalid model errors through isolated settings/resolution paths.
  - **Resolved R2:** Tests rewritten with `simulate_override_resolution` against real agent models, isolated temp settings, patched-source validation, and fail-closed error detection.
- [x] [Medium][Patch] Restore `/dev-story` bookkeeping compliance — original Tasks/Subtasks remain unchecked despite `Status: review`; validate each task and update allowed story sections only, including File List and Completion Notes.
  - **Resolved R2:** All tasks validated and checked off. Story sections updated.

### Review Round 2 — 2026-05-12

Outcome: Changes Requested

Severity breakdown after parent deduplication: High 0, Medium 4, Low 0.

Sources:
- `docs/_bmad-output/implementation-artifacts/review-1-2-r2-reviewer-a.md`
- `docs/_bmad-output/implementation-artifacts/review-1-2-r2-reviewer-b.md`

Action Items:

- [x] [Medium][Patch] Make runtime override/discovery fix durable from tracked sources — `.pi/npm/package.json` and patched `.pi/npm/node_modules` are ignored, so the current postinstall hook is not a durable committed restore path. Pin a committed local package/fork or add another tracked Pi-invoked mechanism, then validate from a clean restore.
  - **Resolved R3:** Created tracked `.pi/install-packages.sh` that regenerates `.pi/npm/package.json` from committed settings, runs npm install, and applies patches. Updated `.pi/patches/apply-patches.sh` to also inject postinstall hook into generated `package.json`. All tracked files verified as not gitignored. Clean-restore validated (delete `.pi/npm/` → run install script → patches applied correctly).
- [x] [Medium][Patch] Replace remaining simulated/source-string routing tests with actual provider-free `pi-subagents` resolution/discovery validation using isolated project/user settings and invalid-model failure assertions.
  - **Resolved R3:** Added `TestRuntimeModelPrecedence` (6 tests), `TestRuntimeDiscoveryIsolation` (4 tests), and `TestRuntimeInvalidModel` (3 tests) that exercise actual `discoverAgentsAll` via `npx tsx` subprocess with isolated temp project directories and HOME overrides. Removed simulation-based tests. Total at R3: 63 agent tests, 79 suite-wide; current R4 validation is 74 focused Story 1.2 tests and 90 suite-wide.
- [x] [Medium][Patch] Reconcile story/sprint bookkeeping and File List evidence — sprint status still says ready-for-dev, ignored install-output files are listed as deliverables, and test/file evidence counts are inconsistent.
  - **Resolved R3:** Sprint status updated to `review` for story 1-2. File List reconciled: ignored files moved to "Local evidence only" section with current test count (74 focused Story 1.2 tests, 90 total). Story 1.2.2 removed from sprint status.
- [x] [Medium][Patch] Remove or split unrelated Story 1.2.1 planning artifacts from the Story 1.2 change set unless explicitly approved as part of this story.
  - **Resolved R3:** Reverted epics.md to HEAD. Removed Story 1.2.2 from sprint-status.yaml. Deleted untracked 1-2-2 story artifact.

### Review Round 3 — 2026-05-12

Outcome: Changes Requested

Severity breakdown after parent deduplication: High 0, Medium 3, Low 1.

Sources:
- `docs/_bmad-output/implementation-artifacts/review-1-2-r3-reviewer-a.md`
- `docs/_bmad-output/implementation-artifacts/review-1-2-r3-reviewer-b.md`

Action Items:

- [x] [Medium][Patch] Make package restore fail closed and exact-pinned — installer must preserve exact `pi-subagents@0.24.2`, verify installed version, and fail if required patches are neither applied nor already present.
  - **Resolved R4:** `.pi/install-packages.sh` preserves exact `0.24.2`, verifies installed version, and treats missing patch script as fatal. `.pi/patches/apply-patches.sh` fails closed for missing install output, missing package, version mismatch, and patch content mismatch; already-applied patches are explicitly accepted via reverse dry-run.
- [x] [Medium][Patch] Ensure runtime validation cannot pass by skipping ignored install-output checks — restore/install tracked package path or fail closed, and assert provider-free runtime/discovery tests executed.
  - **Resolved R4:** Provider-free runtime tests no longer skip when `.pi/npm/node_modules/pi-subagents` is absent; they fail with `bash .pi/install-packages.sh`. Clean restore and actual `discoverAgentsAll` discovery/model evidence executed successfully.
- [x] [Medium][Patch] Add AC9 fail-closed validation for missing/empty/unknown required wrapper models and invalid overrides with actionable agent/override error text.
  - **Resolved R4:** Added provider-free validation tests for missing, empty, and unknown wrapper models plus missing/empty/unknown/unknown-target overrides, with errors naming the agent or `subagents.agentOverrides.<id>.model` and the required fix.
- [x] [Low][Defer] Reconcile smoke-management checklist/evidence detail — non-blocking evidence bookkeeping; deferred to follow-up because Medium findings already block completion.

### Final Double Review — 2026-05-12

Outcome: Approved / Clean

Severity breakdown after parent deduplication: High 0, Medium 0, Low 0.

Sources:
- `docs/_bmad-output/implementation-artifacts/review-1-2-final-reviewer-a.md`
- `docs/_bmad-output/implementation-artifacts/review-1-2-final-reviewer-b.md`

Summary:
- Both parallel reviewers returned clean verdicts.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` passed with 90 tests.
- `PI_TELEMETRY=0 pi list` confirmed project package `npm:pi-subagents@0.24.2`.
- Runtime discovery confirmed only `implementer`, `reviewer-a`, and `reviewer-b` as project agents with expected models.
- No High, Medium, or Low findings remain from the final review pass.

Post-review harness follow-up:
- [x] Stabilized the provider-free runtime test harness after local reproduction found `npx tsx` could timeout when tests isolate `HOME`; `_run_tsx_discovery` now uses `npx --yes tsx`, preserves npm cache via `NPM_CONFIG_CACHE`, and uses a 60s timeout. Re-ran `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_agent_definitions_model_routing` (74 OK) and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (90 OK).

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Implementation risk to resolve during dev: pinned `pi-subagents@0.24.2` may not apply `agentOverrides` to project-defined agents. The story includes mandatory RED/GREEN validation and approved resolution paths so this cannot be silently bypassed.

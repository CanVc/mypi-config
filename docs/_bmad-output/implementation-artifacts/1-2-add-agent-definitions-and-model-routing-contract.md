# Story 1.2: Add Agent Definitions and Model Routing Contract

Status: ready-for-dev

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

- [ ] Establish the project-owned wrapper-agent roster under `.pi/agents/`. (AC: 1, 2, 3)
  - [ ] Create `.pi/agents/` if absent.
  - [ ] Add the minimum v1 wrapper agents: `.pi/agents/implementer.md`, `.pi/agents/reviewer-a.md`, and `.pi/agents/reviewer-b.md`.
  - [ ] Do **not** create `.pi/agents/orchestrator.md` or `.pi/agents/bmad-orchestrator.md`; BMAD orchestration remains parent-session guidance in `.pi/skills/bmad-orchestrator/SKILL.md`.
  - [ ] Do not create v2 TDD agents (`test-architect`, `test-writer`, `red-validator`, `green-validator`) unless this story is intentionally expanded; architecture marks them as v2 additions.
  - [ ] Keep wrapper prompts thin: role purpose, source-of-truth artifact behavior, completion/evidence expectations, and safety boundaries. Do not copy entire BMAD workflow skill bodies into agent prompts.
- [ ] Define readable, canonical frontmatter for every wrapper agent. (AC: 1, 4, 8, 9)
  - [ ] Ensure each file name is lowercase kebab-case and matches `name: <filename-stem>`.
  - [ ] Include `description`, a readable role label field (e.g. `roleLabel` as extra frontmatter), `model`, explicit `tools`, `systemPromptMode`, `inheritProjectContext`, `inheritSkills`, and `defaultContext: fresh`.
  - [ ] Omit `package:` unless every dispatch, chain, override, and test intentionally uses the dotted runtime name; unqualified names are preferred for this story.
  - [ ] Use explicit tool allowlists. Do not omit `tools`, because omitted tools give the child Pi's normal builtin tool set.
  - [ ] Do not grant the `subagent` tool to wrapper agents.
- [ ] Normalize model routing configuration. (AC: 4, 5, 6, 7, 8, 9)
  - [ ] Treat Story 1.1's current `.pi/settings.json` override for `bmad-dev-story` as suspect/inert until proven; it currently targets a legacy skill path, not a `.pi/agents/` wrapper.
  - [ ] Align project settings override keys with canonical wrapper IDs (`implementer`, `reviewer-a`, `reviewer-b`) or remove inert overrides.
  - [ ] Preserve/choose model references from approved Pi model IDs only; do not commit provider API keys or credentials.
  - [ ] Prove that an agent-file `model` is used when no override exists.
  - [ ] Prove that `subagents.agentOverrides.<project-agent>.model` overrides the project agent file model.
  - [ ] Prove that project `.pi/settings.json` overrides take precedence over user settings.
  - [ ] Do not use per-call `model` parameters or slash inline `[model=...]` as evidence for this story; that bypasses the contract under test.
- [ ] Address `pi-subagents@0.24.2` project-agent override behavior honestly. (AC: 5, 6, 9)
  - [ ] Add a RED test or reproducible validation that demonstrates whether the pinned runtime applies `subagents.agentOverrides` to project-defined agents.
  - [ ] If the pinned runtime already supports project-agent overrides, keep the package pin and document the evidence.
  - [ ] If it does **not** support project-agent overrides, do not fake the AC by testing only built-ins. Resolve by one approved path: update to an upstream package version that supports the behavior, add a committed project-local package/fork with the fix and pin it, or stop and record a `spec-ambiguity`/blocked note requiring product decision. Do not patch ignored `.pi/npm/node_modules` as the durable fix.
  - [ ] Keep any runtime/package change generic: it may affect discovery/override resolution, but it must not hardcode BMAD role names or model IDs.
- [ ] Prevent BMAD skill files and legacy `.agents/skills/**` from becoming unintended dispatchable agents. (AC: 2, 3)
  - [ ] Validate that dispatchable project agents are the approved `.pi/agents/` wrappers only.
  - [ ] Ensure `.pi/skills/**/SKILL.md` are not exposed as sub-agents merely because they have `name`/`description` frontmatter.
  - [ ] Ensure legacy `.agents/skills/**/SKILL.md` cannot override, shadow, or silently add BMAD workflow skills as project agents.
  - [ ] If the runtime discovers legacy skill files as agents, add a durable allowlist/filter/disable strategy and tests; do not rely on manual avoidance.
  - [ ] Approved durable strategies are: configure `pi-subagents` discovery so this project exposes only `.pi/agents/` wrappers, add a committed project-local package/fork that ignores legacy `.agents/skills/**` as agent definitions while preserving skill discovery, or create explicit disable/allowlist settings for every unintended legacy skill-agent and validate no new legacy skill-agent slips through. Do not rename or damage BMAD skill files to hide them from discovery.
- [ ] Add focused regression/validation coverage. (AC: 1-9)
  - [ ] Add `tests/test_agent_definitions_model_routing.py` or equivalent.
  - [ ] Test `.pi/agents/` exists and expected wrapper files are present.
  - [ ] Test each wrapper's frontmatter: `name` equals filename stem, `description` exists, role label exists, `model` exists, `tools` is explicit, `defaultContext: fresh`, and no `subagent` tool is granted.
  - [ ] Test `subagents.agentOverrides` keys resolve to discovered agents; inert override keys fail validation with actionable output.
  - [ ] Test `.pi/skills/**` and `.agents/skills/**` are not part of the dispatchable project-agent set except through explicit `.pi/agents/` wrappers.
  - [ ] Test model precedence: file model < user setting override < project setting override.
  - [ ] Isolate user-settings precedence tests with a temporary HOME/Pi config or equivalent fixture. Do not mutate or depend on the developer's real `~/.pi/agent/settings.json`.
  - [ ] Test missing/empty invalid required model configuration fails closed with the agent ID and required fix.
  - [ ] Test committed wrapper/settings model references against the active Pi model registry when available; if the registry cannot be queried in the environment, validation must report an explicit environment block instead of treating any non-empty string as valid.
- [ ] Perform smoke validation and record evidence. (AC: 4, 7, 8, 9)
  - [ ] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
  - [ ] Run `PI_TELEMETRY=0 pi list` and confirm `npm:pi-subagents@0.24.2` or the approved replacement pin is loaded from project settings.
  - [ ] Use `subagent({ action: "list", agentScope: "project" })` or equivalent Pi CLI evidence to show approved project agents only.
  - [ ] Use `subagent({ action: "get", agent: "<agent-id>", agentScope: "project" })` evidence to show effective model resolution.
  - [ ] If provider credentials are unavailable for live child dispatch, capture the blocked provider step and the static/management evidence; do not claim live model execution occurred.
  - [ ] If live credentials are available, run the smallest possible same-run dispatch/chain that proves two differently configured wrapper agents select their configured models. This is evidence only; do not implement Story 1.4 task state or Story 1.6 two-agent smoke workflow behavior here.

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

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Implementation risk to resolve during dev: pinned `pi-subagents@0.24.2` may not apply `agentOverrides` to project-defined agents. The story includes mandatory RED/GREEN validation and approved resolution paths so this cannot be silently bypassed.

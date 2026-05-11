# Story 1.1: Set Up Initial Project from the Project-Local Pi Scaffold Starter

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a builder,
I want an initial project-local Pi scaffold starter with the expected framework directories and placeholder files,
so that `mypi-config` has a stable installable structure for agents, skills, extensions, and shared references.

## Acceptance Criteria

1. **Given** the `mypi-config` repository is checked out, **When** the builder inspects the project structure, **Then** the repository contains a `.pi/` scaffold with `agents/`, `skills/`, `extensions/`, and `references/` directories, **And** the scaffold follows the architecture-approved layout for framework-owned assets.
2. **Given** the scaffold exists, **When** the builder inspects `.pi/references/`, **Then** placeholder reference files exist for `artifact-format.md` and `workflow-status-codes.md`, **And** each file clearly states that it is a framework-owned reference contract.
3. **Given** the scaffold exists, **When** the builder inspects `.pi/extensions/bmad-orchestrator/`, **Then** the extension folder contains a local `package.json`, `tsconfig.json`, and `src/` directory, **And** extension dependencies are scoped to the extension folder, not the repository root.
4. **Given** the scaffold exists, **When** the builder inspects `.pi/agents/`, **Then** initial agent definition placeholders exist for orchestration, implementation, validation, and review roles, **And** each placeholder uses canonical lowercase kebab-case file naming.
5. **Given** the scaffold exists, **When** the builder inspects `.pi/skills/`, **Then** placeholder folders exist for BMAD-derived workflow skills, **And** the standard BMAD base workflows are not modified or overwritten.
6. **Given** the scaffold has been initialized, **When** repository checks are run, **Then** no provider API keys, credentials, or local secrets are present in committed scaffold files, **And** the scaffold does not require root-owned paths.

## Tasks / Subtasks

- [ ] Create the architecture-approved `.pi/` scaffold directories without deleting existing BMAD skills. (AC: 1, 5)
  - [ ] Ensure `.pi/agents/`, `.pi/extensions/`, `.pi/references/`, and `.pi/skills/` exist.
  - [ ] Preserve existing `.pi/skills/bmad-*` base skill folders already present in this repository; do not rename, replace, or bulk rewrite them.
  - [ ] Add only the new placeholder BMAD-derived workflow skill folders needed by the architecture: `.pi/skills/bmad-create-story-tdd/`, `.pi/skills/bmad-dev-story-tdd/`, and `.pi/skills/bmad-code-review-tdd/`.
  - [ ] Add minimal `SKILL.md` placeholders in those derived skill folders that clearly identify them as `mypi-config` framework-owned, future BMAD-derived workflows.
  - [ ] Mark placeholder skills with `disable-model-invocation: true` until later stories implement real workflow behavior, so inert placeholders do not appear as active model-selected capabilities.
- [ ] Add framework-owned reference contract placeholders. (AC: 2)
  - [ ] Create `.pi/references/artifact-format.md` with a clear framework-owned notice and the initial artifact-first contract: Markdown artifacts are durable truth; runtime signals are control-plane only.
  - [ ] Create `.pi/references/workflow-status-codes.md` with a clear framework-owned notice and the initial canonical status/classification vocabulary, including `implementation-issue`, `test-issue`, `spec-ambiguity`, `artifact-invalid`, `retry-limit-reached`, `environment-blocked`, and `workflow-contract-violation`.
  - [ ] Keep these files concise; this story creates starter contracts, not the complete v2/v3 artifact schema.
- [ ] Add initial agent definition placeholders under `.pi/agents/`. (AC: 4)
  - [ ] Create these lowercase kebab-case files: `orchestrator.md`, `red.md`, `red-validator.md`, `green.md`, `green-validator.md`, `reviewer-gpt.md`, and `reviewer-opus.md`.
  - [ ] In each file, include a short framework-owned notice, canonical agent identifier, role label, placeholder model assignment field, and explicit note that final routing/model semantics are implemented in later stories.
  - [ ] State in `orchestrator.md` that the Markdown agent role is non-authoritative for runtime routing; deterministic extension logic will be authoritative.
- [ ] Add the local `bmad-orchestrator` TypeScript extension scaffold. (AC: 3)
  - [ ] Create `.pi/extensions/bmad-orchestrator/package.json` with extension-local package metadata and a Pi manifest that points to `./src/index.ts`.
  - [ ] Create `.pi/extensions/bmad-orchestrator/tsconfig.json` scoped to that extension folder.
  - [ ] Create `.pi/extensions/bmad-orchestrator/src/index.ts` as a no-op placeholder extension exporting a default Pi extension factory.
  - [ ] If TypeScript type imports are used, list Pi core packages as peer dependencies with `"*"` ranges rather than bundling them.
  - [ ] Do not add root-level `package.json`, root `node_modules`, or root TypeScript build tooling in this story.
- [ ] Add project-local Pi settings scaffold. (AC: 1, 3, 5, 6)
  - [ ] Create `.pi/settings.json` as a minimal valid JSON object for project-local Pi configuration.
  - [ ] Keep settings minimal; include resource arrays only if needed for explicit scaffold discovery.
  - [ ] Do not store provider API keys, model secrets, or local machine paths in `.pi/settings.json`.
- [ ] Validate scaffold integrity and security. (AC: 1-6)
  - [ ] Run filesystem checks proving required directories and files exist.
  - [ ] Validate JSON files parse successfully (`.pi/settings.json` if created, extension `package.json`, extension `tsconfig.json`).
  - [ ] Verify extension dependencies are local to `.pi/extensions/bmad-orchestrator/` and no root dependency install was introduced.
  - [ ] Run a secret-pattern scan against newly added scaffold files and confirm no provider keys or credentials are present.
  - [ ] Verify no scaffold files are root-owned.
  - [ ] Confirm standard BMAD base workflow skill files under existing `.pi/skills/bmad-*` folders were not modified as part of this story.

## Dev Notes

### Core Implementation Intent

This story is the first implementation story for the selected custom project-local Pi scaffold starter. It establishes the filesystem contract that later stories will use for bootstrap, model validation, extension validation, dispatch, session policy, and workflow execution. Keep the implementation intentionally small and structural: create the scaffold and placeholders; do not implement the bootstrap installer, prereq verification, dispatch runtime, model validator, TDD workflow execution, CI gates, or Playwright runtime proof yet. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Starter Template Evaluation] [Source: docs/_bmad-output/planning-artifacts/epics.md#Story 1.1: Set Up Initial Project from the Project-Local Pi Scaffold Starter]

### Current Repository State to Preserve

- The repository currently already has `.pi/skills/` populated with BMAD skill folders installed alongside `.agents/skills/` and `.claude/skills/`.
- Treat the existing `.pi/skills/bmad-*` content as base BMAD assets for this story. Do not perform mass formatting, regeneration, deletion, or overwrite operations there.
- `.pi/agents/`, `.pi/extensions/`, `.pi/references/`, `.pi/settings.json`, root `scripts/`, and extension package files are not present yet at story creation time.
- Root `README.md` exists and `.gitignore` is empty. Do not add root dependency state just to scaffold the extension.

### Architecture Guardrails

- Framework-owned assets live under `.pi/`; agent role definitions in `.pi/agents/`; workflow skills in `.pi/skills/`; extension runtime logic in `.pi/extensions/`; shared references in `.pi/references/`. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Framework Organization]
- Markdown is the durable source of truth for workflow artifacts. Runtime completion signals are control-plane only and must not override artifact truth. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Data Architecture]
- Agent communication is vertical through the orchestrator only. Agents must not communicate directly with each other; durable communication flows through artifacts. [Source: docs/_bmad-output/planning-artifacts/architecture.md#API & Communication Patterns]
- The future extension layer is the authoritative deterministic orchestrator. Any `orchestrator.md` placeholder must be explicitly non-authoritative relative to extension-level routing. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Gap Analysis Results]
- Canonical names use lowercase kebab-case for agent identifiers, artifact files, reference files, and folders. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Naming Patterns]
- Initial architecture-approved agent placeholder set: `orchestrator`, `red`, `red-validator`, `green`, `green-validator`, `reviewer-gpt`, `reviewer-opus`. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Code Organization]
- Initial architecture-approved derived skill placeholder set: `bmad-create-story-tdd`, `bmad-dev-story-tdd`, `bmad-code-review-tdd`. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Complete Project Directory Structure]
- First implementation priorities include defining `.pi/references/artifact-format.md` and `.pi/references/workflow-status-codes.md`; this story should create useful starter contracts, not empty stubs. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Implementation Handoff] [Source: docs/_bmad-output/planning-artifacts/implementation-readiness-report-2026-05-11.md#Issues Requiring Attention]

### Pi-Specific Guardrails from Installed Documentation

- Pi auto-discovers project-local extensions from `.pi/extensions/*.ts` and `.pi/extensions/*/index.ts`; package-style extension folders can include `package.json` and a `pi.extensions` manifest pointing at `./src/index.ts`. [Source: Pi docs: docs/extensions.md#Extension Locations] [Source: Pi docs: docs/extensions.md#Extension Styles]
- Pi loads TypeScript extensions directly via `jiti`; no mandatory compile step is needed for extension loading. [Source: Pi docs: docs/extensions.md#Writing an Extension]
- Extension runtime dependencies belong inside the extension package folder. Package runtime dependencies belong in `dependencies`; Pi core packages used by extensions (`@earendil-works/pi-ai`, `@earendil-works/pi-agent-core`, `@earendil-works/pi-coding-agent`, `@earendil-works/pi-tui`, `typebox`) should be peer dependencies with `"*"` ranges when imported. [Source: Pi docs: docs/packages.md#Dependencies]
- Pi skills are discovered from `.pi/skills/`; directories containing `SKILL.md` are discovered recursively. Skill names must be lowercase kebab-case and match the parent directory. [Source: Pi docs: docs/skills.md#Locations] [Source: Pi docs: docs/skills.md#Frontmatter]
- Project settings are stored in `.pi/settings.json` and override global settings. Do not put secrets there. Resource paths in project settings resolve relative to `.pi`. [Source: Pi docs: docs/settings.md#Resources]
- Pi model declarations and custom provider configuration live in `~/.pi/agent/models.json` or provider registration, not in committed scaffold files. API key values can be environment variable names or commands, but committed project files must not include literal provider secrets. [Source: Pi docs: docs/models.md#Custom Models] [Source: docs/_bmad-output/planning-artifacts/prd.md#Non-Functional Requirements]
- Pi packages/extensions/skills run with full system permissions; keep scaffold placeholders inert and auditable. [Source: Pi docs: docs/extensions.md#Extension Locations] [Source: Pi docs: docs/packages.md#Install and Manage]

### Suggested Placeholder File Content Requirements

Use concise placeholders that are explicit enough for future stories:

- `.pi/references/artifact-format.md` should include:
  - title and framework-owned notice;
  - statement that Markdown artifacts are durable truth;
  - initial expected story artifact folder names (`story.md`, `test-plan.md`, `batches/`, `orchestrator-log.md`, `runtime-proof/`) as future contract references;
  - warning that final schemas evolve in later workflow stories.
- `.pi/references/workflow-status-codes.md` should include:
  - title and framework-owned notice;
  - fixed classification code list from architecture;
  - initial status vocabulary placeholders for story/batch/workflow states;
  - instruction that deterministic routing must use structured codes, not free-form prose.
- Agent placeholders should include enough structure to be readable later, for example:
  - `# Agent: green`
  - `Identifier: green`
  - `Role label: Implementation Agent`
  - `Model assignment: <placeholder-model-ref>`
  - `Status: placeholder`
  - `Framework ownership: mypi-config`
- Derived skill placeholders should include valid `SKILL.md` frontmatter:
  - `name` matching folder name;
  - clear `description` saying placeholder/future workflow;
  - `disable-model-invocation: true` while the skill is inert;
  - optional body saying not yet implemented.

### Anti-Scope-Creep Boundaries

Do **not** implement these in Story 1.1:

- `scripts/bootstrap-into-project.sh` safe overwrite behavior (Story 1.2).
- `scripts/detect-prereqs.sh` or `scripts/verify-workstation.sh` behavior (Story 1.3).
- Pi `models.json` validation or model assignment editing workflow (Story 1.4).
- Extension validation scripts, CI, lint/test framework setup beyond minimal scaffold validity (Story 1.5).
- Smoke workflow execution (Story 1.6).
- Generic sub-agent dispatch tool, session policy, task routing, UI widgets, or runtime orchestration logic (Epic 2+).

### Testing Requirements

At minimum, the dev agent should run and record evidence for:

```bash
# Required scaffold paths
for path in \
  .pi/agents \
  .pi/skills \
  .pi/extensions/bmad-orchestrator/src \
  .pi/references \
  .pi/references/artifact-format.md \
  .pi/references/workflow-status-codes.md \
  .pi/extensions/bmad-orchestrator/package.json \
  .pi/extensions/bmad-orchestrator/tsconfig.json \
  .pi/extensions/bmad-orchestrator/src/index.ts \
  .pi/settings.json; do
  test -e "$path" || { echo "Missing $path"; exit 1; }
done
```

```bash
# Agent placeholder naming and required set
for file in \
  .pi/agents/orchestrator.md \
  .pi/agents/red.md \
  .pi/agents/red-validator.md \
  .pi/agents/green.md \
  .pi/agents/green-validator.md \
  .pi/agents/reviewer-gpt.md \
  .pi/agents/reviewer-opus.md; do
  test -f "$file" || { echo "Missing $file"; exit 1; }
done
find .pi/agents -maxdepth 1 -type f -name '*.md' -printf '%f\n' | grep -Ev '^[a-z0-9]+(-[a-z0-9]+)*\.md$' && exit 1 || true
```

```bash
# JSON validity
node -e "JSON.parse(require('fs').readFileSync('.pi/extensions/bmad-orchestrator/package.json','utf8'))"
node -e "JSON.parse(require('fs').readFileSync('.pi/extensions/bmad-orchestrator/tsconfig.json','utf8'))"
node -e "JSON.parse(require('fs').readFileSync('.pi/settings.json','utf8'))"
```

```bash
# Secret scan focused on new scaffold files; refine patterns if false positives occur
rg -n --hidden --glob '.pi/agents/**' --glob '.pi/references/**' --glob '.pi/extensions/bmad-orchestrator/**' \
  '(sk-ant-|sk-[A-Za-z0-9]{20,}|ANTHROPIC_API_KEY=.*[A-Za-z0-9]|OPENAI_API_KEY=.*[A-Za-z0-9]|GEMINI_API_KEY=.*[A-Za-z0-9]|api[_-]?key\s*[:=]\s*["'"'][^"'"']{12,})' .pi && exit 1 || true
```

```bash
# Ownership: no root-owned scaffold files
find .pi/agents .pi/references .pi/extensions/bmad-orchestrator -uid 0 -print -quit | grep . && exit 1 || true
```

Also run `git status --short` and inspect the diff to ensure existing `.pi/skills/bmad-*` base workflow files were not modified accidentally.

### Project Structure Notes

Expected post-story additions are structural and framework-owned:

```text
.pi/
  settings.json                  # minimal project-local Pi settings scaffold
  references/
    artifact-format.md
    workflow-status-codes.md
  agents/
    orchestrator.md
    red.md
    red-validator.md
    green.md
    green-validator.md
    reviewer-gpt.md
    reviewer-opus.md
  skills/
    bmad-create-story-tdd/
      SKILL.md
    bmad-dev-story-tdd/
      SKILL.md
    bmad-code-review-tdd/
      SKILL.md
    ...existing BMAD base skills remain untouched...
  extensions/
    bmad-orchestrator/
      package.json
      tsconfig.json
      src/
        index.ts
```

Story execution artifacts remain outside the framework scaffold under `docs/_bmad-output/implementation-artifacts/`. Do not confuse `.pi/references/` framework contracts with BMAD planning or story execution artifacts. [Source: docs/_bmad-output/planning-artifacts/architecture.md#Architectural Boundaries]

### Source Document Discovery Results

- Loaded PRD from `docs/_bmad-output/planning-artifacts/prd.md`.
- Loaded Architecture from `docs/_bmad-output/planning-artifacts/architecture.md`.
- Loaded Epics from `docs/_bmad-output/planning-artifacts/epics.md`.
- No UX design document was found; v1 UX is limited to Pi TUI/operator behavior in later Epic 2 work.
- No `project-context.md` was found.
- No previous story exists for Epic 1, so there are no previous-story implementation learnings yet.
- Pi documentation consulted from the installed package: `README.md`, `docs/extensions.md`, `docs/skills.md`, `docs/settings.md`, `docs/models.md`, and `docs/packages.md`.

### References

- `docs/_bmad-output/planning-artifacts/epics.md#Story 1.1: Set Up Initial Project from the Project-Local Pi Scaffold Starter`
- `docs/_bmad-output/planning-artifacts/architecture.md#Starter Template Evaluation`
- `docs/_bmad-output/planning-artifacts/architecture.md#Complete Project Directory Structure`
- `docs/_bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules`
- `docs/_bmad-output/planning-artifacts/architecture.md#Project Structure & Boundaries`
- `docs/_bmad-output/planning-artifacts/prd.md#Harness Bootstrap & Setup`
- `docs/_bmad-output/planning-artifacts/implementation-readiness-report-2026-05-11.md#Recommended Next Steps`
- Pi docs: `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/extensions.md`
- Pi docs: `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/skills.md`
- Pi docs: `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/settings.md`
- Pi docs: `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/models.md`
- Pi docs: `/home/cvc/.local/share/fnm/node-versions/v24.15.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/docs/packages.md`

## Dev Agent Record

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.

### File List

- `docs/_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-the-project-local-pi-scaffold-starter.md`

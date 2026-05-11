---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-04-17'
inputDocuments:
  - 'docs/_bmad-output/planning-artifacts/prd.md'
  - 'docs/_bmad-output/planning-artifacts/prd-validation-report-2026-04-14.md'
  - 'docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md'
  - 'docs/_bmad-output/planning-artifacts/research/archive/agentic-tdd-story-workflow-design-notes-2026-04-12.md'
  - 'docs/_bmad-output/planning-artifacts/research/archive/story-prototype-single-file-agentic-tdd-2026-04-12.md'
  - 'docs/_bmad-output/planning-artifacts/research/archive/technical-agentic-tdd-bmad-pi-story-workflow-research-2026-04-12.md'
workflowType: 'architecture'
project_name: 'mypi-config'
user_name: 'Cvc'
date: '2026-04-17'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
The project defines 40 functional requirements across nine major capability areas: bootstrap/setup, workflow execution, agent orchestration, quality gates, orchestration/interface support, TDD workflow support, runtime verification, auditability, and advanced configuration.

Architecturally, these requirements imply that the system is not a single workflow script but a configurable execution harness with clear phase boundaries. The architecture must support:
- a canonical story-driven execution model,
- role/stage-based agent execution,
- fresh-context handoffs between stages,
- configurable model routing per agent,
- bounded iteration and escalation behavior,
- workflow observability and eventual resumability,
- compatibility with standard BMAD workflows before introducing richer derived workflows.

The functional scope also shows a phased architecture expectation:
- **v1** focuses on bootstrap, standard BMAD workflows, multi-model routing, and quality gates,
- **v2** introduces formal TDD/ATDD/TDAD orchestration and runtime-proof artifacts,
- **v3** adds traceability and resumable state,
- **v4** introduces higher-level configurability for broader reuse.

**Non-Functional Requirements:**
The NFRs that most strongly shape architecture are:
- **Security:** secrets must remain outside committed config, tools must be explicitly scoped, and bootstrap must avoid privileged installation paths.
- **Integration:** the harness must remain compatible with Pi and BMAD base installations and accept standard BMAD story artifacts unchanged.
- **Reliability:** iteration caps and escalation behavior must be deterministic and observable.
- **Maintainability:** agent definitions and extensions must remain editable by a technically capable builder without requiring deep Pi internals knowledge.

These NFRs imply an architecture favoring explicit contracts, low-magic configuration, deterministic workflow state transitions, and strong separation between configuration, orchestration logic, and execution evidence.

**Scale & Complexity:**
This project is medium in complexity, but it has a relatively high coordination burden because it combines orchestration, model routing, artifact handling, tool execution, and future workflow extensibility.

- Primary domain: developer tooling / agentic workflow orchestration
- Complexity level: medium
- Estimated architectural components: 7-9 core components

The main scale driver is not user volume or data volume, but workflow coordination and correctness under iterative agent execution.

### Technical Constraints & Dependencies

Known constraints and dependencies identified from the source documents:
- Pi is the execution framework and extension surface.
- BMAD v6 remains the base workflow system and must not be broken or replaced.
- Standard BMAD artifacts must remain valid inputs without modification.
- Multi-model routing is a first-class requirement and must be configurable per role/stage.
- Workflow stages must prefer fresh, bounded context over long shared session history.
- Hooks and shell-executing behaviors must remain scoped and auditable.
- Ubuntu is the primary environment target.
- Playwright and broader runtime verification are future-facing and enter the architecture explicitly in v2, not in the v1 bootstrap surface.
- The architecture must support a bootstrap/install mechanism that is fast and repeatable across projects.

### Cross-Cutting Concerns Identified

The following concerns will affect multiple architectural components:

- **Workflow state management:** phase transitions, bounded retries, escalation rules, resumability
- **Artifact strategy:** story files, logs, validation outputs, runtime proof, review findings
- **Model routing:** distinct models per role with clear configuration ownership
- **Context management:** fresh-context handoff and bounded execution context per stage
- **Observability and auditability:** execution logs, decision records, review outputs, traceability
- **Security boundaries:** least-privilege tool usage, hook governance, secret isolation
- **Compatibility:** preserving BMAD base workflows while layering derived workflows beside them
- **Portability and installation:** bootstrap simplicity, predictable filesystem layout, reusable setup
- **Extensibility:** ability to add future workflow profiles and orchestration logic without redesigning the core

## Starter Template Evaluation

### Primary Technology Domain

Pi-native local developer tooling scaffold built from:
- Pi packages for reusable runtime capabilities such as `pi-subagents`
- optional Pi extensions in TypeScript for custom guardrails
- Pi agents in Markdown
- Pi skills for BMAD workflows
- local-only execution with no separate UI

This is not a classic CLI starter.

### Starter Options Considered

**1. Root-level CLI starter (Commander / oclif)**  
Rejected for v1. Pi already provides the runtime, TUI, commands, and session model.

**2. Generic TypeScript package starter**  
Useful as a technical base, but insufficient on its own because it does not define the Pi-specific layout.

**3. Custom project-local Pi scaffold with pinned Pi packages and optional embedded extension packages**
Selected. Best fit for Pi, BMAD, greenfield/brownfield copy-based install, marketplace runtime reuse, and editable agent definitions.

### Selected Starter: Custom Project-Local Pi Scaffold

**Why this starter:**
- Pi stays the execution shell and TUI
- sub-agents run as isolated child Pi sessions through `pi-subagents`
- agents stay editable in Markdown
- custom extension logic lives in TypeScript only where hard guardrails are needed
- framework deps stay project-local through pinned Pi packages or, for custom code, isolated in the owning extension folder
- works for greenfield and brownfield installs
- preserves the standard BMAD base while allowing v2 additions beside it

**Initialization model:**
Build the repository-local multi-agent runtime first, then package the project-local Pi scaffold for target-repository installation. Bootstrap hardening and overwrite rules belong to the portable bootstrap epic after the initial runtime proof.

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Pi packages for reusable runtime capabilities such as `pi-subagents`
- TypeScript for Pi extensions only when custom deterministic guardrails are needed
- Markdown for Pi agents
- Markdown skill folders for BMAD workflows
- Node.js runtime

**UI Layer:**
- No separate UI
- Pi TUI is the operator interface
- any workflow UI is implemented through Pi extensions

**Build Tooling:**
- no mandatory build step for package or extension loading
- Pi installs project-local packages declared in `.pi/settings.json`
- Pi loads TypeScript extensions directly when custom extensions exist
- package.json in an extension folder is used only for that extension's Node dependencies

**Testing:**
- no mandatory test framework in the starter
- Vitest is optional and belongs in `devDependencies` only if extension tests are added later
- Playwright is not part of the v1 starter

**Extension Validation Contract:**
- Each framework-owned Pi TypeScript extension, when introduced for custom guardrails, must define extension-local validation scripts in its own `package.json`.
- Required extension-local scripts are:
  - `typecheck`
  - `lint`
  - `test`
  - `validate`, which runs typecheck, lint, and tests in sequence.
- Extension validation must run from the extension folder and must not depend on host project root `node_modules`.
- The repository should provide a root-level validation wrapper, `scripts/validate-extensions.sh`, that discovers framework-owned TypeScript extensions and runs each extension's validation command.
- CI must run the root-level extension validation wrapper so non-conforming extensions fail validation before merge or release.
- Validation output must identify the failing extension and failing command.

**Code Organization:**

```text
.pi/
  agents/
    implementer.md
    reviewer-a.md
    reviewer-b.md
    # v2 additions:
    test-architect.md
    test-writer.md
    red-validator.md
    green-validator.md

  skills/
    bmad-orchestrator/
      SKILL.md
    bmad-dev-story-harness/
      SKILL.md
      ...
    bmad-code-review-harness/
      SKILL.md
      ...
    # v2 additions:
    bmad-dev-story-tdd/
      SKILL.md
      ...

  settings.json  # pins packages such as npm:pi-subagents@<version>

  extensions/
    # optional later custom guardrail extensions, not required for Story 1.1 dispatch
```

**Dependency Strategy:**
- Reusable runtime dependencies should be declared as pinned Pi packages in project settings.
- `pi-subagents` is the selected sub-agent dispatch substrate for Story 1.1.
- Custom Node dependencies live in the owning extension folder only when a custom extension is introduced.
- This isolates framework deps from the host project root.

### Current Workstation Baseline

**Installed:**
- Git 2.43.0
- Node.js 24.14.1
- npm 11.11.0
- pnpm 10.33.0
- Pi 0.67.2
- Python 3.12.3
- curl, wget, zip, unzip
- VS Code

**Missing:**
- `python` alias
- `pip` / `pip3`
- Playwright
- browser runtime (`chromium` / `chrome`)
- `gcc`
- `make`
- `tmux`

### Workstation Prerequisites

**Minimum for v1:**
- Git
- Node.js
- npm or pnpm
- Pi

The current workstation already satisfies the minimum v1 requirements.

**Recommended additions:**
- `python-is-python3`
- `python3-pip`
- `build-essential`

These are not required to start, but reduce setup friction.

**Needed later for v2 runtime verification:**
- `playwright`
- `npx playwright install`

### Version Notes

Verified during evaluation:
- installed Pi: `0.67.2`
- latest npm Pi seen: `0.67.6`
- TypeScript: `6.0.3`
- Vitest: `4.1.4`
- tsx: `4.21.0`

**Note:** the first implementation story is the multi-agent dispatch foundation. Project initialization and bootstrap packaging follow after the runtime proof.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Architecture is artifact-first: Markdown artifacts are the durable source of truth.
- Agent communication is vertical through the parent orchestrator only.
- Initial BMAD orchestration is parent-session guidance; later deterministic guardrails may be enforced by a Pi extension when workflow transitions need hard validation.
- Pi sub-agents are launched through the marketplace `pi-subagents` package and its generic `subagent(...)` tool.
- Agent context is provided through direct task text for informal workflows and artifact file paths for formal workflows, not reconstructed summaries.
- Agent roles are defined in Markdown; workflow method is defined in BMAD skills; runtime mechanics should use Pi packages first and custom Pi extensions only where needed.
- Artifact structure is standardized and documented in a framework-owned reference file.
- Session reuse is tightly restricted to explicit repair/resume cases; v2 may specialize this into batch-level TDD retries.

**Important Decisions (Shape Architecture):**
- Agents do not communicate directly with each other.
- Runtime completion signals are control-plane only; they do not override artifact truth.
- Validators recommend through structured artifact outputs; parent guidance or later guardrails apply deterministic routing rules.
- Final review always runs with fresh context.
- Artifact specification is stored in `.pi/references/artifact-format.md`.

**Deferred Decisions (Post-MVP):**
- Exact operator UI mode: dedicated team dashboard vs lighter widget set
- Richer multi-team orchestration variants beyond the initial TDD workflow
- Additional generic workflow families beyond BMAD TDD execution

### Data Architecture

There is no conventional application database in v1. The primary durable data plane is the Markdown artifact set produced and consumed by the workflow.

**Source of truth:**
- v1 core:
  - story artifact
  - review outputs / validation findings
  - execution log
  - status-bearing structured Markdown sections
- v2 additions:
  - test plan
  - batch artifacts
  - orchestrator log
  - runtime-proof artifacts

**Decision:**
Use structured Markdown artifacts as the only durable workflow state. No separate workflow database or sidecar machine-state file is introduced for MVP. The minimum v1 artifact contract stays compatible with standard BMAD story execution; v2 extends that contract with TDD-specific artifacts.

**Rationale:**
- aligns with BMAD
- preserves auditability
- keeps workflow state portable and git-visible
- supports resumability without hidden runtime memory

### Authentication & Security

There is no end-user authentication architecture in scope for v1. Security focuses on execution boundaries.

**Security decisions:**
- tools and permissions are constrained by role
- child-agent launch uses the pinned `pi-subagents` runtime rather than ad hoc subprocess code
- parent-session BMAD guidance controls delegation intent, with later extension guardrails if deterministic transition enforcement is required
- ambiguous or invalid workflow states escalate to a human
- framework assets stay project-local under `.pi/`

**Human escalation principle:**
If the workflow cannot classify or safely continue, the system must stop and escalate instead of improvising.

### API & Communication Patterns

The system uses vertical orchestration, not peer-to-peer agent collaboration.

**Communication model:**
- agent writes outputs to Markdown artifacts
- agent returns a runtime completion signal
- orchestrator re-reads artifacts
- orchestrator decides the next transition

**Decision:**
Agents do not communicate directly with one another. All durable communication flows through artifacts, and all control routing flows through the orchestrator.

**Why:**
- preserves observability
- avoids hidden agent-to-agent state
- keeps Git history meaningful
- makes workflow replay and debugging possible

**Dispatch mechanism:**
The project declares `pi-subagents` as a pinned Pi package. Its generic `subagent(...)` tool can launch named child agents with:
- agent name
- fresh/fork context selection
- task content
- artifact path references or read directives

This keeps launch mechanics generic while allowing BMAD parent-session guidance and later guardrails to specialize workflow behavior above it.

### Frontend Architecture

There is no separate frontend or web UI.

**Decision:**
Pi’s TUI is the operator interface. Any additional UX is implemented through Pi package capabilities, prompt/skill guidance, or optional Pi extension widgets, dashboards, status lines, or overlays.

**Implication:**
UI concerns remain outside the durable artifact truth model regardless of whether they come from `pi-subagents` or a later custom extension.

### Infrastructure & Deployment

**Execution environment:**
- local-only for v1
- project-local Pi scaffold
- no Docker requirement for MVP
- no database or hosted infrastructure requirement for MVP

**Workstation baseline decisions:**
Minimum:
- Git
- Node.js
- npm or pnpm
- Pi

Recommended:
- `python-is-python3`
- `python3-pip`
- `build-essential`

Future v2 runtime verification:
- `playwright`
- `npx playwright install`

### Orchestration Model

**Decision:**
Use parent-session BMAD orchestration guidance first, backed by `pi-subagents` for child-agent launch. Add deterministic extension guardrails later only where workflow transitions, retry limits, or escalation rules require hard runtime enforcement.

This means:
- parent guidance checks delegation intent where possible
- `pi-subagents` owns child-agent process/session launch mechanics
- later guardrails may validate allowed transitions
- later guardrails may apply retry limits
- routing must use structured validator/artifact outputs rather than hidden conversation state
- if workflow contract violations occur, execution stops and escalates to a human

A child `orchestrator.md` agent is not the parent decision-maker and must not be used for nested sub-agent orchestration.

### Session Memory Policy

**Default rule:**
All agents start in fresh context.

**Allowed exceptions:**
Session reuse is permitted only for same-role repair loops explicitly authorized by the orchestrator. In v2 TDD flows, this includes bounded retry loops within a batch.

**Always fresh:**
- validators
- final reviewers
- final review loops in general

**Reasoning:**
This preserves artifact-first discipline while allowing efficient local repair loops where they materially reduce churn. v1 keeps this generic; v2 applies it to batch-oriented TDD loops.

### Artifact Reference Model

**Decision:**
Artifact structure is documented centrally in:

`/.pi/references/artifact-format.md`

This file defines:
- artifact layout
- required sections
- status conventions
- how agents find the current workflow phase, findings, and next-action signals

Agents do not duplicate the full artifact specification in their own `.md` files. They only describe role-specific reading behavior.

### Workflow Contract and Escalation

Validators must emit structured, classifiable outcomes. The runtime does not rely on vague prose to route work.

Typical routing classes include:
- implementation issue
- test issue
- spec ambiguity
- artifact invalid
- retry limit reached
- environment blocked
- workflow contract violation

**Workflow contract violation** means the produced artifact state contradicts the allowed workflow model and cannot be trusted for automatic continuation.

When such a condition occurs, the system must escalate to a human.

### Decision Impact Analysis

**Implementation Sequence:**
1. Establish the observable multi-agent runtime first, in the repository-local `.pi/` scaffold
2. Pin and configure `pi-subagents` as the child-agent dispatch substrate
3. Define parent-session BMAD orchestration guidance that delegates through `subagent(...)`
4. Define the v1 artifact contract in `.pi/references/artifact-format.md`
5. Define workflow status and transition conventions in `.pi/references/workflow-status-codes.md`
6. Define v1 agent role files in `.pi/agents/`
7. Add model-routing and fresh-context delegation conventions on top of `pi-subagents`
8. Add task state and optional operator UI widgets for visibility
9. Prove the runtime with a two-agent smoke scenario
10. Package and harden the portable bootstrap flow for target-project installation
11. Define harness skills for standard BMAD workflow execution and review gates
12. Add validator/review output classification and escalation rules
13. Add custom deterministic extension guardrails only where package/guidance behavior is insufficient
14. Extend the artifact contract and role set for v2 TDD workflows

**Sequencing Constraint:** Do not treat standard BMAD review execution or portable bootstrap proof as implementation-ready until the Epic 1 runtime exists. Review gates depend on sub-agent dispatch, fresh context, model routing, and observable task state.

**Cross-Component Dependencies:**
- `pi-subagents` package configuration precedes smokeable child-agent dispatch
- agent role files depend on the artifact contract
- skills depend on the artifact contract and parent-orchestrator rules
- later deterministic guardrails depend on validator output classification
- resumability depends on structured artifact state being stable and parseable
- UI is optional, but orchestration correctness is not

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:**
The main consistency risks are not database or UI conflicts, but workflow and artifact conflicts between multiple AI agents:
- agent naming and role naming
- artifact file naming
- artifact section naming
- status and transition encoding
- validator output classification
- `pi-subagents` delegation contract and BMAD usage conventions
- framework file placement under `.pi/`
- logging and decision recording conventions

### Naming Patterns

**Agent Naming Conventions:**
- Agent identifiers use lowercase kebab-case
- Examples:
  - `orchestrator`
  - `implementer`
  - `reviewer-a`
  - `reviewer-b`
  - `test-architect`
  - `test-writer`
  - `red-validator`
  - `green-validator`

**Rules:**
- agent file name must match agent identifier
- agent names are stable runtime identifiers
- display labels may differ in UI, but artifact and runtime references use canonical kebab-case names

**Artifact Naming Conventions:**
- artifact file and folder names use lowercase kebab-case
- examples:
  - `story.md`
  - `test-plan.md`
  - `batch-01.md`
  - `batch-02.md`
  - `orchestrator-log.md`
  - `runtime-proof/`

**Reference Naming Conventions:**
- framework-owned reference files use lowercase kebab-case
- examples:
  - `.pi/references/artifact-format.md`
  - `.pi/references/workflow-status-codes.md`

### Structure Patterns

**Framework Organization:**
Framework-owned assets live under `.pi/`.

Recommended structure:

```text
.pi/
  settings.json   # project-local package pins, including pi-subagents
  agents/
  skills/
  references/
  extensions/     # optional custom guardrails only
```

**Rules:**
- agent role definitions live in `.pi/agents/`
- project-local package declarations live in `.pi/settings.json`
- custom extension runtime logic lives in `.pi/extensions/` only when needed
- workflow/skill logic lives in `.pi/skills/`
- shared framework references live in `.pi/references/`
- framework documentation should not be placed in project `docs/` unless intentionally part of the target project documentation

**Artifact Organization:**
Workflow artifacts must be organized so the orchestrator and all agents can locate the current story state deterministically.

Minimum artifact set:
- v1 core:
  - story artifact
  - review artifacts / validation findings section(s)
  - execution log
  - status-bearing structured sections
- v2 additions:
  - test plan
  - batch artifacts
  - orchestrator log
  - runtime-proof

### Format Patterns

**Artifact Truth Model:**
Markdown is the only durable workflow state.

**Rules:**
- no sidecar JSON state file as source of truth
- no hidden runtime-only state may override artifacts
- all durable workflow decisions must be written back to Markdown artifacts
- runtime signals are control-plane only

**Status Encoding:**
Status must be encoded in structured Markdown conventions, not free prose.

**Rules:**
- status fields must come from a fixed vocabulary
- transition-relevant fields must be parseable deterministically
- artifact structure must support locating:
  - current phase
  - current batch when applicable
  - next expected role
  - open findings
  - retry count or equivalent bounded-loop signal

**Validator Output Format:**
Validators must emit structured classifications, not only narrative feedback.

Minimum classification categories:
- `implementation-issue`
- `test-issue`
- `spec-ambiguity`
- `artifact-invalid`
- `retry-limit-reached`
- `environment-blocked`
- `workflow-contract-violation`

Each validator result should include:
- outcome
- primary classification
- rationale
- recommended next action
- affected artifact/batch reference

### Communication Patterns

**Agent Communication Model:**
Agents never communicate directly with each other.

**Required pattern:**
- agent reads artifacts
- agent performs its task
- agent writes outputs to artifacts
- agent returns runtime completion signal
- orchestrator re-reads artifacts
- orchestrator applies deterministic routing rules

**Control Plane vs Data Plane:**
- Markdown artifacts = data plane
- runtime completion/result signal = control plane

**Rule:**
If runtime output and artifact state disagree, artifacts win.

### Dispatch Patterns

**Generic Dispatch Tool:**
The runtime must expose one generic dispatch mechanism rather than role-specific hardcoded tools. The selected mechanism is `pi-subagents` and its `subagent(...)` tool.

Expected invocation concepts include:
- agent identifier
- context mode, normally `fresh`
- task text
- artifact paths passed as paths/read directives, not summaries

Example shape:

```json
{
  "agent": "reviewer-a",
  "context": "fresh",
  "task": "Review the current story implementation. Use these artifact paths as source of truth: story.md, review-a.md",
  "agentScope": "both"
}
```

If supported by the selected `pi-subagents` call form, file paths may also be supplied through its read/output behavior. The parent must not rewrite formal artifacts into lossy summaries.

**Rules:**
- `subagent(...)` remains workflow-agnostic
- workflow-specific routing logic stays above it in parent BMAD guidance or later guardrails
- delegation payloads use canonical agent names and artifact paths only

### Session Patterns

**Default Session Policy:**
- all agents start fresh by default

**Allowed resume cases only:**
- rerun the same implementation role after structured rejection
- rerun the same review/validation role only when the orchestrator explicitly authorizes repair in place

**Always fresh:**
- validators
- final review agents
- final review retry loops

### Process Patterns

**Deterministic Orchestration:**
The parent BMAD orchestrator is the initial workflow decision surface. Where deterministic enforcement is required beyond prompt/skill guidance, a later custom extension may add guardrails.

**Rules:**
- parent guidance validates intent before delegation where possible
- later guardrails validate that transitions are allowed when automatic routing is introduced
- later guardrails validate retry bounds when bounded loops are introduced
- routing decisions are based only on structured artifact outputs
- ambiguous situations escalate to human instead of being interpreted freely

**Human Escalation Pattern:**
Escalation occurs when the workflow cannot continue safely or deterministically.

Examples include:
- spec ambiguity
- artifact invalidity
- retry limit reached
- environment blocked
- workflow contract violation

**Workflow contract violation** means the produced artifact state contradicts the defined workflow model.

### Enforcement Guidelines

**All AI Agents MUST:**
- treat Markdown artifacts as the durable source of truth
- use canonical role and artifact names
- write structured outputs, not only prose summaries
- avoid direct agent-to-agent communication
- defer routing decisions to the orchestrator/runtime
- treat missing or malformed required artifact structure as a workflow problem, not something to guess through

**Pattern Enforcement:**
- artifact structure is defined centrally in `.pi/references/artifact-format.md`
- agent role files reference that contract rather than duplicating it
- workflow skills enforce which artifacts must be read/written
- `pi-subagents` enforces child-agent launch boundaries; later extension guardrails may enforce transition validity and session policy

### Pattern Examples

**Good Examples:**
- `reviewer-a` writes structured findings classified as `implementation-issue`
- orchestrator reads updated artifact state and dispatches the next allowed role
- the same role may resume only within explicitly bounded repair loops
- final reviewer always starts fresh from artifacts

**Anti-Patterns:**
- agents exchanging conclusions directly in runtime text without writing artifacts
- validator prose that does not classify the problem
- routing based only on “what the model said” instead of artifact state
- hidden sidecar state overriding markdown truth
- free-form artifact naming or section naming that breaks deterministic parsing

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
mypi-config/
|-- README.md
|-- AGENTS.md
|-- .gitignore
|-- .pi/
|   |-- settings.json        # pins npm:pi-subagents@<approved-version>
|   |-- references/
|   |   |-- artifact-format.md
|   |   `-- workflow-status-codes.md
|   |-- agents/
|   |   |-- implementer.md
|   |   |-- reviewer-a.md
|   |   |-- reviewer-b.md
|   |   |-- test-architect.md
|   |   |-- test-writer.md
|   |   |-- red-validator.md
|   |   `-- green-validator.md
|   |-- skills/
|   |   |-- bmad-orchestrator/        # parent-session delegation guidance
|   |   |   `-- SKILL.md
|   |   |-- bmad-dev-story-harness/
|   |   |   |-- SKILL.md
|   |   |   |-- workflow.md
|   |   |   |-- steps/
|   |   |   `-- templates/
|   |   |-- bmad-code-review-harness/
|   |   |   |-- SKILL.md
|   |   |   |-- workflow.md
|   |   |   |-- steps/
|   |   |   `-- templates/
|   |   |-- bmad-create-story-tdd/
|   |   |   |-- SKILL.md
|   |   |   |-- workflow.md
|   |   |   |-- steps/
|   |   |   `-- templates/
|   |   |-- bmad-dev-story-tdd/
|   |   |   |-- SKILL.md
|   |   |   |-- workflow.md
|   |   |   |-- steps/
|   |   |   `-- templates/
|   |   `-- bmad-code-review-tdd/
|   |       |-- SKILL.md
|   |       |-- workflow.md
|   |       |-- steps/
|   |       `-- templates/
|   `-- extensions/
|       `-- optional custom guardrail extensions only
|           |-- package.json
|           |-- tsconfig.json
|           |-- src/
|           |   |-- transition-rules.ts
|           |   |-- artifact-reader.ts
|           |   |-- artifact-writer.ts
|           |   |-- session-policy.ts
|           |   |-- validator-routing.ts
|           |   |-- escalation-rules.ts
|           |   |-- types.ts
|           |   `-- ui/
|           |       `-- status-widget.ts
|           `-- tests/
|-- scripts/
|   |-- bootstrap-into-project.sh
|   |-- detect-prereqs.sh
|   `-- verify-workstation.sh
`-- docs/
    `-- _bmad-output/
        |-- planning-artifacts/
        |   |-- product-brief-mypi-config.md
        |   |-- prd.md
        |   `-- architecture.md
        `-- implementation-artifacts/
            `-- stories/
                `-- <story-id>/
                    |-- story.md
                    |-- review-a.md
                    |-- review-b.md
                    |-- execution-log.md
                    |-- test-plan.md
                    |-- batches/
                    |   |-- batch-01.md
                    |   |-- batch-02.md
                    |   `-- batch-03.md
                    |-- orchestrator-log.md
                    `-- runtime-proof/
```
### Architectural Boundaries

**Framework Boundary:**
- `.pi/` contains framework-owned runtime assets
- these files define agents, skills, references, and extensions
- they are installable/copiable into target projects
- they must not depend on project documentation in `docs/`

**Artifact Boundary:**
- `docs/_bmad-output/planning-artifacts/` stores planning inputs
- `docs/_bmad-output/implementation-artifacts/` stores durable workflow execution state
- implementation artifacts are the durable state plane for story execution

**Project Code Boundary:**
- target project source code remains outside the framework directories
- the framework reads and modifies project code through Pi tools and workflows
- workflow truth does not live in source code comments or runtime memory

### Requirements to Structure Mapping

**Bootstrap & Setup Requirements:**
- `scripts/bootstrap-into-project.sh`
- `scripts/detect-prereqs.sh`
- `.pi/settings.json` with pinned Pi package declarations, including `pi-subagents`
- optional `.pi/extensions/` only for custom guardrails

**Workflow Execution Requirements:**
- `.pi/skills/bmad-dev-story-harness/`
- `.pi/skills/bmad-code-review-harness/`
- future v2 additions:
  - `.pi/skills/bmad-create-story-tdd/`
  - `.pi/skills/bmad-dev-story-tdd/`
  - `.pi/skills/bmad-code-review-tdd/`

**Agent Orchestration Requirements:**
- `.pi/settings.json` package entry for `pi-subagents`
- `.pi/skills/bmad-orchestrator/SKILL.md` or equivalent parent-session orchestration guidance
- `.pi/agents/` project agents consumed by `pi-subagents`
- optional later guardrail extension modules for transition rules, session policy, and validator routing if prompt/package behavior is insufficient

**Agent Role Definitions:**
- `.pi/agents/implementer.md`
- `.pi/agents/reviewer-a.md`
- `.pi/agents/reviewer-b.md`
- future v2 additions:
  - `.pi/agents/test-architect.md`
  - `.pi/agents/test-writer.md`
  - `.pi/agents/red-validator.md`
  - `.pi/agents/green-validator.md`

**Artifact Contract & Consistency Rules:**
- `.pi/references/artifact-format.md`
- `.pi/references/workflow-status-codes.md`

**Execution State & Auditability:**
- `docs/_bmad-output/implementation-artifacts/stories/<story-id>/story.md`
- `docs/_bmad-output/implementation-artifacts/stories/<story-id>/review-a.md`
- `docs/_bmad-output/implementation-artifacts/stories/<story-id>/review-b.md`
- `docs/_bmad-output/implementation-artifacts/stories/<story-id>/execution-log.md`
- future v2 additions:
  - `docs/_bmad-output/implementation-artifacts/stories/<story-id>/test-plan.md`
  - `docs/_bmad-output/implementation-artifacts/stories/<story-id>/batches/`
  - `docs/_bmad-output/implementation-artifacts/stories/<story-id>/orchestrator-log.md`
  - `docs/_bmad-output/implementation-artifacts/stories/<story-id>/runtime-proof/`
### Integration Points

**Internal Communication:**
- skills invoke the workflow method
- parent-session BMAD guidance delegates through `subagent(...)`
- `pi-subagents` dispatches child agents
- agents read/write Markdown artifacts
- parent orchestration re-reads artifacts and applies workflow guidance or later deterministic guardrails

**External Integrations:**
- Pi CLI runtime
- configured model providers via Pi
- host project filesystem
- future Playwright runtime verification in v2

**Data Flow:**
1. planning artifacts define intent
2. skill or prompt starts workflow
3. parent orchestration guidance verifies delegation intent where possible
4. parent invokes `subagent(...)` with task content and artifact paths
5. child agent writes results to artifacts
6. parent re-reads artifacts
7. parent guidance or later deterministic guardrails route, retry, or escalate
8. final review writes review artifacts and closure state

### File Organization Patterns

**Configuration Files:**
- project-wide Pi behavior and package pins: `.pi/settings.json`
- optional extension-local Node dependencies: `.pi/extensions/<guardrail-extension>/package.json`
- optional extension-local TS config: `.pi/extensions/<guardrail-extension>/tsconfig.json`

**Source Organization:**
- parent orchestration guidance under `.pi/skills/` or `.pi/prompts/`
- optional guardrail extension source under `.pi/extensions/<guardrail-extension>/src/`
- agent role prompts under `.pi/agents/`
- workflow method under `.pi/skills/`
- framework references under `.pi/references/`

**Test Organization:**
- package/dispatch smoke checks for `pi-subagents` integration
- optional extension unit tests under `.pi/extensions/<guardrail-extension>/tests/`
- workflow execution evidence under `docs/_bmad-output/implementation-artifacts/`
- future runtime verification evidence under each story’s `runtime-proof/`

**Asset Organization:**
- no browser/static asset layer for v1
- runtime proof assets belong only under story-specific `runtime-proof/`

### Development Workflow Integration

**Development Server Structure:**
- no separate dev server is required for the framework itself
- Pi is the runtime shell
- pinned Pi package integration is validated from project settings; optional custom extensions are developed and tested locally in their own folders

**Build Process Structure:**
- Pi installs project-local packages declared in `.pi/settings.json`
- Pi loads TypeScript extensions directly when optional custom extensions exist
- extension-local scripts may validate typecheck/tests for custom extensions
- no root-level application build is required for MVP framework runtime

**Deployment Structure:**
- the deployable/installable unit is the project-local `.pi/` scaffold plus helper scripts
- brownfield install should update framework-owned `.pi/` assets while preserving project-owned assets
- standard BMAD-compatible assets must not be overwritten destructively

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
The architecture is coherent overall. The main decisions reinforce each other:
- artifact-first state
- parent-session BMAD orchestration with optional later deterministic guardrails
- `pi-subagents` generic dispatch substrate
- agent roles in Markdown
- workflow method in BMAD skills
- framework assets in `.pi/`
- durable truth in Markdown artifacts

These choices are compatible and create a clear separation of concerns.

**Pattern Consistency:**
Implementation patterns support the architectural decisions well:
- naming is standardized around kebab-case
- artifact truth is preserved
- runtime vs durable state is clearly separated
- direct agent-to-agent communication is forbidden
- validator outputs are structured for deterministic routing

**Structure Alignment:**
The project structure supports the chosen architecture:
- `.pi/` holds framework-owned assets and project-local package pins
- planning artifacts and implementation artifacts are separated
- optional extension logic is isolated when introduced
- references, agents, and skills have clear homes
- story execution state has a durable location

### Requirements Coverage Validation ✅

**Feature Coverage:**
The architecture supports the main product goals:
- portable Pi/BMAD scaffold
- standard BMAD compatibility
- derived TDD workflow capability
- multi-agent execution
- deterministic orchestration
- auditability through artifacts
- future runtime-proof integration

**Functional Requirements Coverage:**
All major FR areas are covered architecturally:
- bootstrap/setup
- workflow execution
- agent orchestration
- quality gates
- orchestration/interface support
- TDD workflow support
- runtime verification preparation
- auditability
- future configurability

**Non-Functional Requirements Coverage:**
The architecture addresses the key NFRs:
- **Security:** role/tool boundaries, escalation on invalid states
- **Reliability:** deterministic routing and retry rules
- **Maintainability:** separation between roles, workflows, runtime packages, optional extensions, and references
- **Integration:** BMAD compatibility preserved, Pi-native package and extension models retained

### Implementation Readiness Validation ✅

**Decision Completeness:**
Critical implementation decisions are defined:
- durable state model
- communication model
- dispatch model
- session reuse policy
- escalation policy
- framework boundaries
- artifact reference location

**Structure Completeness:**
The structure is specific enough to guide implementation:
- concrete directory tree exists
- key files and directories are mapped
- boundaries are explicit
- implementation-artifact locations are defined

**Pattern Completeness:**
The main agent conflict points are addressed:
- naming
- structure
- routing classifications
- status conventions
- session behavior
- escalation behavior

### Gap Analysis Results

**Critical Gaps:** None blocking implementation.

**Important Gaps:**
1. **Classification code normalization**
   The architecture should use one canonical format for validator routing classes.
   Recommended canonical form:
   - `implementation-issue`
   - `test-issue`
   - `spec-ambiguity`
   - `artifact-invalid`
   - `retry-limit-reached`
   - `environment-blocked`
   - `workflow-contract-violation`

2. **Clarify parent orchestrator role**
   The architecture now treats BMAD orchestration as parent-session guidance that delegates through `pi-subagents`.
   Therefore any `orchestrator.md` child-agent role must not be interpreted as the parent runtime decision-maker or as a nested sub-agent launcher.
   It should be treated as:
   - parent-session skill/prompt guidance,
   - a supporting explainer/summarizer role,
   - or removed from the child-agent control path.

**Nice-to-Have Gaps:**
- explicit artifact section examples in `.pi/references/artifact-format.md`
- explicit transition table in `.pi/references/workflow-status-codes.md`
- explicit human escalation matrix for each validator classification

### Validation Issues Addressed

The architecture is considered implementation-ready with the following clarifications:
- validator classification codes should be normalized to kebab-case
- `pi-subagents` is the initial authoritative child-agent dispatch substrate
- parent-session BMAD guidance is the initial orchestrator; later extension guardrails may enforce hard workflow transitions
- any `orchestrator.md` child-agent role must be non-authoritative relative to parent orchestration

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**✅ Architectural Decisions**
- [x] Critical decisions documented
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Runtime orchestration model defined

**✅ Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping completed

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

**Key Strengths:**
- clear separation of concerns across 4 layers
- deterministic orchestration model
- artifact-first truth model
- strong auditability and replayability
- extensible generic dispatch foundation
- good alignment with Pi’s package/extension model and BMAD’s artifact model

**Areas for Future Enhancement:**
- richer UI/operator dashboards
- additional workflow families beyond TDD
- more formalized artifact schemas and transition tables
- richer bootstrap automation for brownfield installs

### Implementation Handoff

**AI Agent Guidelines:**
- follow the artifact-first model strictly
- treat Markdown artifacts as the durable truth
- do not communicate agent-to-agent directly
- use canonical naming and classification codes
- use `pi-subagents` `subagent(...)` for child-agent delegation unless a later story explicitly introduces a custom guardrail extension

**First Implementation Priority:**
1. implement Epic 1: Observable Pi Multi-Agent Runtime
2. pin and validate `pi-subagents` in `.pi/settings.json`
3. define parent-session BMAD orchestration guidance that uses `subagent(...)`
4. define `.pi/references/artifact-format.md`
5. define `.pi/references/workflow-status-codes.md`
6. prove the two-agent runtime smoke scenario before bootstrap packaging or review-dependent workflow proof


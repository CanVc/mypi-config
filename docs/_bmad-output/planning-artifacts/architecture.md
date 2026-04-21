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
- Pi extensions in TypeScript
- Pi agents in Markdown
- Pi skills for BMAD workflows
- local-only execution with no separate UI

This is not a classic CLI starter.

### Starter Options Considered

**1. Root-level CLI starter (Commander / oclif)**  
Rejected for v1. Pi already provides the runtime, TUI, commands, and session model.

**2. Generic TypeScript package starter**  
Useful as a technical base, but insufficient on its own because it does not define the Pi-specific layout.

**3. Custom project-local Pi scaffold with embedded extension package**  
Selected. Best fit for Pi, BMAD, greenfield/brownfield copy-based install, and editable agent definitions.

### Selected Starter: Custom Project-Local Pi Scaffold

**Why this starter:**
- Pi stays the execution shell and TUI
- sub-agents run as isolated `pi` subprocesses
- agents stay editable in Markdown
- extension logic lives in TypeScript
- framework deps stay inside the project, isolated in the extension folder
- works for greenfield and brownfield installs
- preserves the standard BMAD base while allowing v2 additions beside it

**Initialization model:**
Copy the project-local Pi scaffold into the target repository. Bootstrap hardening and overwrite rules should be handled in the first implementation story.

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- TypeScript for Pi extensions
- Markdown for Pi agents
- Markdown skill folders for BMAD workflows
- Node.js runtime

**UI Layer:**
- No separate UI
- Pi TUI is the operator interface
- any workflow UI is implemented through Pi extensions

**Build Tooling:**
- no mandatory build step for extension loading
- Pi loads TypeScript extensions directly
- package.json in the extension folder is used only for that extension's Node dependencies

**Testing:**
- no mandatory test framework in the starter
- Vitest is optional and belongs in `devDependencies` only if extension tests are added later
- Playwright is not part of the v1 starter

**Code Organization:**

```text
.pi/
  agents/
    orchestrator.md
    implementer.md
    reviewer-a.md
    reviewer-b.md
    # v2 additions:
    test-architect.md
    test-writer.md
    red-validator.md
    green-validator.md

  skills/
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

  extensions/
    bmad-orchestrator/
      package.json
      index.ts
```

**Dependency Strategy:**
- Node dependencies live in the extension folder
- Pi discovers the extension by its location, not by `package.json`
- this isolates framework deps from the host project root

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

**Note:** project initialization using this scaffold should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Architecture is artifact-first: Markdown artifacts are the durable source of truth.
- Agent communication is vertical through the orchestrator only.
- Orchestration decisions are deterministic and enforced by the Pi extension layer.
- Pi sub-agents are launched through a generic dispatch tool.
- Agent context is provided through artifact file paths, not reconstructed summaries.
- Agent roles are defined in Markdown; workflow method is defined in BMAD skills; runtime mechanics live in Pi extensions.
- Artifact structure is standardized and documented in a framework-owned reference file.
- Session reuse is tightly restricted to same-role repair loops only; v2 may specialize this into batch-level TDD retries.

**Important Decisions (Shape Architecture):**
- Agents do not communicate directly with each other.
- Runtime completion signals are control-plane only; they do not override artifact truth.
- Validators recommend through structured artifact outputs; the extension applies deterministic routing rules.
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
- orchestration is enforced in the extension layer
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
The extension exposes a generic dispatch tool that can launch any named agent with:
- agent name
- session mode
- task
- artifact paths

This keeps the runtime generic while allowing higher-level workflow specialization above it.

### Frontend Architecture

There is no separate frontend or web UI.

**Decision:**
Pi’s TUI is the operator interface. Any additional UX is implemented through Pi extension widgets, dashboards, status lines, or overlays.

**Implication:**
UI concerns remain in the extension layer and do not affect the artifact truth model.

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
Use a deterministic extension-level orchestrator.

This means:
- the extension checks preconditions
- the extension validates allowed transitions
- the extension applies retry limits
- the extension routes to the next agent based on structured validator outputs
- if workflow contract violations occur, execution stops and escalates to a human

A free-form LLM orchestrator is not the decision-maker.

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
1. Define the v1 artifact contract in `.pi/references/artifact-format.md`
2. Implement generic dispatch tool in the Pi extension layer
3. Implement deterministic orchestrator transition rules
4. Define v1 agent role files in `.pi/agents/`
5. Define harness skills for standard BMAD workflow execution
6. Add validator/review output classification and escalation rules
7. Add optional operator UI widgets for visibility
8. Extend the artifact contract and role set for v2 TDD workflows

**Cross-Component Dependencies:**
- agent role files depend on the artifact contract
- skills depend on the artifact contract and orchestrator rules
- orchestrator logic depends on validator output classification
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
- dispatch tool input format
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
  agents/
  extensions/
  skills/
  references/
```

**Rules:**
- agent role definitions live in `.pi/agents/`
- extension runtime logic lives in `.pi/extensions/`
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
The runtime must expose one generic dispatch mechanism rather than role-specific hardcoded tools.

Expected input shape includes:
- agent identifier
- session mode
- task
- artifact paths

Example shape:

```json
{
  "agent": "reviewer-a",
  "sessionMode": "fresh",
  "task": "Review the current story implementation and write structured findings",
  "artifacts": [
    "story.md",
    "review-a.md"
  ]
}
```

**Rules:**
- dispatch tool remains workflow-agnostic
- workflow-specific routing logic stays above it
- dispatch payload uses canonical agent names and artifact paths only

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
The extension layer is the workflow decision engine.

**Rules:**
- extension validates preconditions before dispatch
- extension validates that transition is allowed
- extension validates retry bounds
- extension routes only from structured artifact outputs
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
- extension logic enforces transition validity and session policy

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
|   |-- settings.json
|   |-- references/
|   |   |-- artifact-format.md
|   |   `-- workflow-status-codes.md
|   |-- agents/
|   |   |-- orchestrator.md
|   |   |-- implementer.md
|   |   |-- reviewer-a.md
|   |   |-- reviewer-b.md
|   |   |-- test-architect.md
|   |   |-- test-writer.md
|   |   |-- red-validator.md
|   |   `-- green-validator.md
|   |-- skills/
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
|       `-- bmad-orchestrator/
|           |-- package.json
|           |-- tsconfig.json
|           |-- src/
|           |   |-- index.ts
|           |   |-- dispatch-subagent.ts
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
|               |-- transition-rules.test.ts
|               |-- session-policy.test.ts
|               `-- validator-routing.test.ts
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
- `.pi/settings.json`
- `.pi/extensions/bmad-orchestrator/`

**Workflow Execution Requirements:**
- `.pi/skills/bmad-dev-story-harness/`
- `.pi/skills/bmad-code-review-harness/`
- future v2 additions:
  - `.pi/skills/bmad-create-story-tdd/`
  - `.pi/skills/bmad-dev-story-tdd/`
  - `.pi/skills/bmad-code-review-tdd/`

**Agent Orchestration Requirements:**
- `.pi/extensions/bmad-orchestrator/src/index.ts`
- `.pi/extensions/bmad-orchestrator/src/dispatch-subagent.ts`
- `.pi/extensions/bmad-orchestrator/src/transition-rules.ts`
- `.pi/extensions/bmad-orchestrator/src/session-policy.ts`
- `.pi/extensions/bmad-orchestrator/src/validator-routing.ts`

**Agent Role Definitions:**
- `.pi/agents/orchestrator.md`
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
- extension runtime dispatches agents
- agents read/write Markdown artifacts
- orchestrator re-reads artifacts and applies deterministic transitions

**External Integrations:**
- Pi CLI runtime
- configured model providers via Pi
- host project filesystem
- future Playwright runtime verification in v2

**Data Flow:**
1. planning artifacts define intent
2. skill starts workflow
3. extension verifies preconditions
4. extension dispatches an agent with artifact paths
5. agent writes results to artifacts
6. extension re-reads artifacts
7. extension routes, retries, or escalates
8. final review writes review artifacts and closure state

### File Organization Patterns

**Configuration Files:**
- project-wide Pi behavior: `.pi/settings.json`
- extension-local Node dependencies: `.pi/extensions/bmad-orchestrator/package.json`
- extension-local TS config: `.pi/extensions/bmad-orchestrator/tsconfig.json`

**Source Organization:**
- extension runtime source under `.pi/extensions/bmad-orchestrator/src/`
- agent role prompts under `.pi/agents/`
- workflow method under `.pi/skills/`
- framework references under `.pi/references/`

**Test Organization:**
- extension unit tests under `.pi/extensions/bmad-orchestrator/tests/`
- workflow execution evidence under `docs/_bmad-output/implementation-artifacts/`
- future runtime verification evidence under each story’s `runtime-proof/`

**Asset Organization:**
- no browser/static asset layer for v1
- runtime proof assets belong only under story-specific `runtime-proof/`

### Development Workflow Integration

**Development Server Structure:**
- no separate dev server is required for the framework itself
- Pi is the runtime shell
- the extension package is developed and tested locally in its own folder

**Build Process Structure:**
- Pi loads TypeScript extensions directly
- extension-local scripts may validate typecheck/tests
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
- deterministic extension-level orchestration
- generic dispatch tool
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
- `.pi/` holds framework-owned assets
- planning artifacts and implementation artifacts are separated
- extension logic is isolated
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
- **Maintainability:** separation between roles, workflows, runtime, and references
- **Integration:** BMAD compatibility preserved, Pi-native extension model retained

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

2. **Clarify `orchestrator.md` role**
   The architecture says orchestration is deterministic in the extension layer.
   Therefore `orchestrator.md` must not be interpreted as the final runtime decision-maker.
   It should be treated as:
   - a supporting workflow role,
   - an explainer/summarizer role,
   - or removed from the runtime control path.

**Nice-to-Have Gaps:**
- explicit artifact section examples in `.pi/references/artifact-format.md`
- explicit transition table in `.pi/references/workflow-status-codes.md`
- explicit human escalation matrix for each validator classification

### Validation Issues Addressed

The architecture is considered implementation-ready with the following clarifications:
- validator classification codes should be normalized to kebab-case
- extension-level runtime remains the authoritative orchestrator
- any `orchestrator.md` role must be non-authoritative relative to runtime routing

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
- good alignment with Pi’s extension model and BMAD’s artifact model

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
- let the extension runtime enforce transitions and escalation

**First Implementation Priority:**
1. define `.pi/references/artifact-format.md`
2. define `.pi/references/workflow-status-codes.md`
3. implement the generic dispatch tool
4. implement deterministic transition rules in the extension


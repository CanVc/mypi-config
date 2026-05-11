---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments:
  - "docs/_bmad-output/planning-artifacts/prd.md"
  - "docs/_bmad-output/planning-artifacts/architecture.md"
---

# mypi-config - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for mypi-config, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Builder can install the harness into a target project via a single bootstrap command.

FR2: Builder can declare available models in Pi `models.json` as part of initial setup.

FR3: Builder can modify the model assigned to a workflow stage by editing the relevant agent definition file.

FR4: Builder can run the first workflow after bootstrap without any additional mandatory configuration.

FR5: Builder can trigger a BMAD story workflow using a story file as the canonical input.

FR6: Builder can execute the standard BMAD dev-story workflow through the harness.

FR7: Builder can execute the standard BMAD code-review workflow through the harness.

FR8: Builder can run two sequential review passes on a completed story.

FR9: Harness can launch each workflow stage with a fresh, bounded context assembled from story artifacts.

FR10: Harness can route each workflow stage to the model defined in the corresponding agent file.

FR11: Harness can enforce an iteration cap per story and stop execution when the cap is reached.

FR12: Harness can escalate to the builder when an iteration cap is hit.

FR13: Harness can verify the targeted test suite passes before accepting story completion.

FR14: Harness can verify lint passes cleanly before accepting story completion.

FR15: Harness can block story completion if any review pass returns blocking findings.

FR16: Builder can wire a multi-agent team via a Pi TypeScript extension (orchestrator + named sub-agents).

FR17: Builder can launch a sub-agent with a fresh context even within an active iteration loop, with no inherited conversation history from prior batches.

FR18: Builder can configure Pi UI layout and display per agent team, including which agents are visible and their role labels.

FR19: Builder can observe in the Pi UI which sub-agent is currently active and what it is doing.

FR20: In formal TDD workflows, sub-agents consume BMAD markdown artifacts (story file, batch files, test plan) directly as their context source; the orchestrator routes by pointing to the right files, not by reconstructing content.

FR21: In informal or conversational workflows, the orchestrator can pass context directly as message content to a sub-agent when no canonical artifact is available.

FR22: Builder can assign a distinct model to each sub-agent within the same team.

FR23: Orchestrator can route the output of one sub-agent as the input to another in a defined sequence.

FR24: Builder can define a descriptive activity title for a Pi terminal session, visible in the terminal UI, to identify which agent is running in which terminal when multiple sessions run in parallel.

FR25: Builder can view a task/todo list in the Pi UI that tracks the current workflow's pending, in-progress, and completed tasks.

FR26: Builder can select a TDD/ATDD/TDAD workflow profile for a story.

FR27: Test-architect agent can generate a test plan and batch files from a story.

FR28: Test-writer agent can author tests for a batch before any implementation begins.

FR29: Red-validator agent can verify that authored tests fail for the correct reason.

FR30: Dev agent can implement code to make a batch's tests pass.

FR31: Green-validator agent can verify that batch behavior is genuinely achieved.

FR32: Orchestrator can track and sync batch statuses across story artifacts (batch files, test plan, orchestrator log).

FR33: Harness can enforce a per-batch iteration cap and escalate blocked batches to the builder.

FR34: Story artifacts are organized in a per-story folder (story file, changelog, test plan, batch files, orchestrator log, runtime-proof).

FR35: Harness can execute a Playwright run against the running application as part of story completion.

FR36: Harness can store runtime proof artifacts (screenshots, traces, logs) in the story's runtime-proof folder.

FR37: Builder can inspect a full execution log for any completed or in-progress story.

FR38: Builder can trace the phase history and agent routing decisions for any workflow run.

FR39: Builder can resume a workflow from a known phase checkpoint.

FR40: Builder can create a new BMAD-derived workflow through a configurator without editing raw files.

FR41: Builder can configure Pi harness setup (agents, hooks, extensions) through a configurator interface.

### NonFunctional Requirements

NFR1: LLM provider API keys are never hardcoded in agent definition files or committed to the repository.

NFR2: Each agent/workflow profile explicitly declares its allowed active tools, and no tool outside that allowlist can be invoked during execution; static validation passes for 100% of profiles.

NFR3: The bootstrap process does not require elevated/root permissions.

NFR4: A smoke suite (bootstrap + standard workflow run) passes at 100% on Pi 0.67.2 and the latest tested stable Pi version in a clean environment.

NFR5: On a clean BMAD v6 base installation, 100% of reference derived workflows install and execute without manual file edits.

NFR6: Story files produced by standard BMAD story creation are valid inputs to the harness without modification.

NFR7: Iteration caps are enforced deterministically; a cap of N never allows N+1 iterations.

NFR8: When escalation occurs (cap reached, batch blocked), the harness message includes the cause, story/batch identifier, and next recommended action; this must pass in 3/3 escalation test scenarios.

NFR9: Agent definition files are readable and editable without knowledge of Pi internals; a builder can change a model assignment in under 2 minutes.

NFR10: Every Pi TypeScript extension follows the standard extension template and passes lint/typecheck at 100%; non-conforming extensions fail CI validation.

NFR11: A builder familiar with BMAD identifies trigger, phases, and output artifacts in a derived workflow in ≤10 minutes; success rate is ≥80% across 3 internal reviewers.

### Additional Requirements

- Selected starter template: custom project-local Pi scaffold with embedded extension package. This is the architectural starter and should shape Epic 1 Story 1.
- Project initialization using the custom project-local Pi scaffold should be the first implementation story, including bootstrap hardening and overwrite rules.
- Framework assets must live under `.pi/`, with agent role definitions in `.pi/agents/`, workflow skills in `.pi/skills/`, extension runtime logic in `.pi/extensions/`, and shared references in `.pi/references/`.
- TypeScript is used for Pi extensions; Markdown is used for Pi agents, BMAD skills, and workflow artifacts; Node.js is the runtime.
- No separate UI or web frontend is required; Pi TUI is the operator interface, and any extra workflow UI belongs in Pi extension widgets, dashboards, status lines, or overlays.
- No mandatory build step is required for extension loading; Pi loads TypeScript extensions directly. Extension-local `package.json` is used for extension dependencies.
- Node dependencies must live inside the extension folder to isolate framework dependencies from the host project root.
- The v1 execution environment is local-only, with no Docker, database, or hosted infrastructure requirement.
- Minimum v1 workstation prerequisites are Git, Node.js, npm or pnpm, and Pi. Recommended additions are `python-is-python3`, `python3-pip`, and `build-essential`.
- v2 runtime verification requires Playwright and browser runtime setup (`npx playwright install`).
- Durable workflow state must be structured Markdown artifacts only; no separate database or sidecar machine-state file is introduced for MVP.
- Markdown artifacts are the source of truth. Runtime completion signals are control-plane only and must not override artifact truth.
- Agent communication is vertical through the orchestrator only; agents must not communicate directly with one another.
- The extension layer is the authoritative deterministic orchestrator and must validate preconditions, allowed transitions, retry limits, routing decisions, and escalation conditions.
- Any `orchestrator.md` agent role must be non-authoritative relative to extension-level runtime routing, or removed from the runtime control path.
- The runtime must expose one generic dispatch mechanism that can launch a named agent using canonical agent name, session mode, task, and artifact paths.
- Agent context in formal workflows is provided through artifact file paths rather than reconstructed summaries.
- Default session policy is fresh context for all agents. Session reuse is allowed only when returning to `red` after `red-validator` rejection or returning to `green` after `green-validator` rejection.
- Validators, final reviewers, and final review retry loops must always start fresh.
- Validator outputs must use structured, deterministic classifications with canonical kebab-case codes: `implementation-issue`, `test-issue`, `spec-ambiguity`, `artifact-invalid`, `retry-limit-reached`, `environment-blocked`, and `workflow-contract-violation`.
- Ambiguous states, invalid artifact states, unsafe continuation, environment blocks, retry-limit exhaustion, and workflow contract violations must escalate to a human instead of being interpreted freely.
- Artifact structure must be documented centrally in `.pi/references/artifact-format.md`.
- Workflow status and transition conventions should be documented in `.pi/references/workflow-status-codes.md`.
- The complete project scaffold should include `.pi/settings.json`, `.pi/references/`, `.pi/agents/`, `.pi/skills/`, `.pi/extensions/bmad-orchestrator/`, `scripts/bootstrap-into-project.sh`, `scripts/detect-prereqs.sh`, and `scripts/verify-workstation.sh`.
- The bmad-orchestrator extension should include implementation modules for dispatching subagents, transition rules, artifact reading/writing, session policy, validator routing, escalation rules, shared types, and optional UI status widget.
- Extension unit tests should cover transition rules, session policy, and validator routing.
- Implementation artifacts must live under `docs/_bmad-output/implementation-artifacts/stories/<story-id>/` with story, test plan, batch files, orchestrator log, review artifacts, and runtime-proof folder as applicable.
- Workflow artifacts must support deterministic lookup of current batch, current gate, next expected role, open findings, and retry count or equivalent bounded-loop signal.
- Framework-owned `.pi/` assets must be installable/copiable into target projects and must not depend on project documentation in `docs/`.
- Brownfield install should update framework-owned `.pi/` assets while preserving project-owned assets and avoiding destructive overwrites of BMAD v1-compatible assets.
- Secrets must remain outside committed configuration; role/tool boundaries must be explicit; hooks and shell-executing behavior must remain scoped and auditable.
- First implementation priorities from architecture are: define `.pi/references/artifact-format.md`, define `.pi/references/workflow-status-codes.md`, implement the generic dispatch tool, and implement deterministic transition rules in the extension.

### UX Design Requirements

No UX Design document was found in the planning artifacts, so no UX Design Requirements were extracted.

### FR Coverage Map

FR1: Epic 1 - Portable Harness Bootstrap enables single-command harness installation into a target project.

FR2: Epic 1 - Portable Harness Bootstrap supports declaring available models in Pi `models.json` during initial setup.

FR3: Epic 1 - Portable Harness Bootstrap makes model assignment editable through agent definition files.

FR4: Epic 1 - Portable Harness Bootstrap enables the first workflow to run after bootstrap without mandatory extra configuration.

FR5: Epic 3 - Standard BMAD Story-to-Done Execution uses a BMAD story file as the canonical workflow input.

FR6: Epic 3 - Standard BMAD Story-to-Done Execution runs the standard BMAD `dev-story` workflow through the harness.

FR7: Epic 3 - Standard BMAD Story-to-Done Execution runs the standard BMAD `code-review` workflow through the harness.

FR8: Epic 3 - Standard BMAD Story-to-Done Execution supports two sequential review passes on a completed story.

FR9: Epic 2 - Observable Pi Multi-Agent Runtime launches each workflow stage with a fresh, bounded context assembled from artifacts or task context.

FR10: Epic 2 - Observable Pi Multi-Agent Runtime routes each workflow stage to the model defined in its agent file.

FR11: Epic 3 - Standard BMAD Story-to-Done Execution enforces iteration caps per story and stops when the cap is reached.

FR12: Epic 3 - Standard BMAD Story-to-Done Execution escalates to the builder when a story iteration cap is hit.

FR13: Epic 3 - Standard BMAD Story-to-Done Execution verifies targeted tests pass before accepting story completion.

FR14: Epic 3 - Standard BMAD Story-to-Done Execution verifies lint passes cleanly before accepting story completion.

FR15: Epic 3 - Standard BMAD Story-to-Done Execution blocks story completion when review passes return blocking findings.

FR16: Epic 2 - Observable Pi Multi-Agent Runtime wires a multi-agent team through a Pi TypeScript extension.

FR17: Epic 2 - Observable Pi Multi-Agent Runtime launches sub-agents with fresh context inside an active loop.

FR18: Epic 2 - Observable Pi Multi-Agent Runtime configures Pi UI layout and display for the agent team.

FR19: Epic 2 - Observable Pi Multi-Agent Runtime shows which sub-agent is active and what it is doing in the Pi UI.

FR20: Epic 3 - Standard BMAD Story-to-Done Execution has formal workflow sub-agents consume BMAD markdown artifacts directly as context sources.

FR21: Epic 2 - Observable Pi Multi-Agent Runtime supports direct message-content context for informal/conversational workflows when no canonical artifact exists.

FR22: Epic 2 - Observable Pi Multi-Agent Runtime assigns distinct models to sub-agents in the same team.

FR23: Epic 2 - Observable Pi Multi-Agent Runtime routes one sub-agent's output as another sub-agent's input in a defined sequence.

FR24: Epic 2 - Observable Pi Multi-Agent Runtime defines descriptive activity titles for Pi terminal sessions.

FR25: Epic 2 - Observable Pi Multi-Agent Runtime displays a task/todo list tracking workflow pending, in-progress, and completed tasks.

FR26: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution lets the builder select a TDD/ATDD/TDAD workflow profile for a story.

FR27: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution has a test-architect generate a test plan and batch files from a story.

FR28: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution has a test-writer author tests before implementation begins.

FR29: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution has a red-validator verify tests fail for the correct reason.

FR30: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution has a dev agent implement code to make batch tests pass.

FR31: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution has a green-validator verify batch behavior is genuinely achieved.

FR32: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution tracks and syncs batch statuses across story artifacts.

FR33: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution enforces per-batch iteration caps and escalates blocked batches.

FR34: Epic 4 - Formal TDD/ATDD/TDAD Workflow Execution organizes story artifacts in a per-story folder.

FR35: Epic 5 - Runtime Proof executes Playwright as part of story completion.

FR36: Epic 5 - Runtime Proof stores screenshots, traces, and logs in `runtime-proof/`.

FR37: Epic 6 - Execution Traceability & Resume lets the builder inspect full execution logs.

FR38: Epic 6 - Execution Traceability & Resume lets the builder trace phase history and agent routing decisions.

FR39: Epic 6 - Execution Traceability & Resume resumes workflow execution from a known phase checkpoint.

FR40: Epic 7 - Advanced Harness Configurator creates new BMAD-derived workflows through a configurator without raw file editing.

FR41: Epic 7 - Advanced Harness Configurator configures Pi harness setup through a configurator interface.

## Epic List

### Epic 1: Portable Harness Bootstrap

The builder can install the `mypi-config` scaffold into a target project, verify prerequisites, configure available models, and run an initial workflow without mandatory extra configuration.

**FRs covered:** FR1, FR2, FR3, FR4

### Epic 2: Observable Pi Multi-Agent Runtime

The builder can launch an orchestrator-backed Pi multi-agent team, dispatch sub-agents with fresh context, verify model routing by agent, observe widgets/labels/tasks in the Pi UI, and see sub-agents consume orchestrator-assigned tasks.

**FRs covered:** FR9, FR10, FR16, FR17, FR18, FR19, FR21, FR22, FR23, FR24, FR25

### Epic 3: Standard BMAD Story-to-Done Execution

The builder can take a canonical BMAD story file and execute standard `dev-story` and `code-review` workflows through the observable multi-agent runtime, with artifact-based context, iteration caps, escalation, tests, lint, and review gates.

**FRs covered:** FR5, FR6, FR7, FR8, FR11, FR12, FR13, FR14, FR15, FR20

### Epic 4: Formal TDD/ATDD/TDAD Workflow Execution

The builder can select a TDD/ATDD/TDAD workflow profile and execute an artifact-first red/green workflow with test planning, test writing, validation, implementation, batch tracking, per-batch caps, escalation, and per-story artifact organization.

**FRs covered:** FR26, FR27, FR28, FR29, FR30, FR31, FR32, FR33, FR34

### Epic 5: Runtime Proof

The builder can execute Playwright runtime proof for completed stories and store durable proof artifacts in the story's `runtime-proof/` folder.

**FRs covered:** FR35, FR36

### Epic 6: Execution Traceability & Resume

The builder can inspect complete execution logs, trace phase and agent routing decisions, and resume workflow execution from a known checkpoint.

**FRs covered:** FR37, FR38, FR39

### Epic 7: Advanced Harness Configurator

The builder can create new BMAD-derived workflows and configure Pi harness setup through a configurator without directly editing raw framework files.

**FRs covered:** FR40, FR41

## Epic 1: Portable Harness Bootstrap

The builder can install the `mypi-config` scaffold into a target project, verify prerequisites, configure available models, and run an initial workflow without mandatory extra configuration.

### Story 1.1: Set Up Initial Project from the Project-Local Pi Scaffold Starter

As a builder,
I want an initial project-local Pi scaffold starter with the expected framework directories and placeholder files,
So that `mypi-config` has a stable installable structure for agents, skills, extensions, and shared references.

**Acceptance Criteria:**

**Given** the `mypi-config` repository is checked out
**When** the builder inspects the project structure
**Then** the repository contains a `.pi/` scaffold with `agents/`, `skills/`, `extensions/`, and `references/` directories
**And** the scaffold follows the architecture-approved layout for framework-owned assets.

**Given** the scaffold exists
**When** the builder inspects `.pi/references/`
**Then** placeholder reference files exist for `artifact-format.md` and `workflow-status-codes.md`
**And** each file clearly states that it is a framework-owned reference contract.

**Given** the scaffold exists
**When** the builder inspects `.pi/extensions/bmad-orchestrator/`
**Then** the extension folder contains a local `package.json`, `tsconfig.json`, and `src/` directory
**And** extension dependencies are scoped to the extension folder, not the repository root.

**Given** the scaffold exists
**When** the builder inspects `.pi/agents/`
**Then** initial agent definition placeholders exist for orchestration, implementation, validation, and review roles
**And** each placeholder uses canonical lowercase kebab-case file naming.

**Given** the scaffold exists
**When** the builder inspects `.pi/skills/`
**Then** placeholder folders exist for BMAD-derived workflow skills
**And** the standard BMAD base workflows are not modified or overwritten.

**Given** the scaffold has been initialized
**When** repository checks are run
**Then** no provider API keys, credentials, or local secrets are present in committed scaffold files
**And** the scaffold does not require root-owned paths.

### Story 1.2: Add Bootstrap Installation Script with Safe Overwrite Rules

As a builder,
I want a single bootstrap command that installs the scaffold into a target project safely,
So that I can reuse `mypi-config` across projects without manually copying files or destroying existing configuration.

**Acceptance Criteria:**

**Given** a target project with BMAD already installed
**When** the builder runs the bootstrap script from `mypi-config`
**Then** framework-owned `.pi/` assets are copied into the target project
**And** the script reports each installed or skipped path.

**Given** a target project already contains `.pi/` files
**When** bootstrap encounters an existing file
**Then** it applies documented safe overwrite rules
**And** it never overwrites project-owned or unknown files silently.

**Given** bootstrap detects a conflict that cannot be resolved automatically
**When** the script reaches that conflict
**Then** it stops with a clear message naming the conflicting path
**And** it recommends the next manual action.

**Given** bootstrap is run by a normal user account
**When** installation completes
**Then** no root privileges are required
**And** no installed file is owned by root.

**Given** bootstrap completes successfully
**When** the builder inspects the target project
**Then** standard BMAD files remain present and unmodified
**And** `mypi-config` files are installed beside them.

### Story 1.3: Add Workstation and Dependency Verification

As a builder,
I want a prereq verification script that checks the local workstation and target project dependencies,
So that bootstrap failures are diagnosed before workflow execution begins.

**Acceptance Criteria:**

**Given** the verification script exists
**When** the builder runs it on the target machine
**Then** it checks for Git, Node.js, npm or pnpm, and Pi
**And** it prints detected versions for each dependency.

**Given** the target project is selected
**When** verification runs
**Then** it checks that BMAD v6 is present or reports that BMAD is missing
**And** it does not attempt to install BMAD automatically.

**Given** a recommended dependency is missing
**When** verification completes
**Then** the script labels it as recommended rather than required
**And** it explains why the dependency may reduce setup friction.

**Given** a required dependency is missing
**When** verification completes
**Then** the script exits non-zero
**And** the output names the missing dependency and suggested next command.

**Given** verification runs on Ubuntu
**When** dependency checks execute
**Then** the script does not require elevated permissions
**And** it performs only read-only environment checks.

### Story 1.4: Document and Validate Model Configuration

As a builder,
I want clear model configuration documentation and validation for Pi `models.json`,
So that workflow agents can route to declared models without hardcoding provider secrets.

**Acceptance Criteria:**

**Given** the scaffold is installed
**When** the builder reads the setup documentation
**Then** it explains that models must be declared in Pi `models.json`
**And** it identifies where agent files reference model assignments.

**Given** model validation is run
**When** an agent references a model name
**Then** the validator checks that the model is declared at the Pi level
**And** it reports missing model references with the agent file path.

**Given** a builder wants to change a workflow stage model
**When** they edit the relevant agent definition file
**Then** the model assignment is readable and localized to that agent definition
**And** the change does not require editing extension source code.

**Given** committed scaffold files are scanned
**When** the scan searches for provider API keys or credentials
**Then** no secrets are found in agent definitions, scripts, references, or extension files
**And** documentation instructs the builder to store secrets outside the repository.

**Given** model validation fails
**When** the builder reads the failure output
**Then** it names the missing or invalid model assignment
**And** it recommends updating Pi `models.json` or the relevant agent definition.

### Story 1.5: Add Extension Validation and CI Gate

As a builder,
I want extension validation commands and CI enforcement for Pi TypeScript extensions,
So that every framework extension proves it follows the standard template and passes lint/typecheck before the harness is considered ready.

**Acceptance Criteria:**

**Given** the `bmad-orchestrator` extension package exists
**When** the builder inspects its `package.json`
**Then** it defines validation scripts for typecheck, lint, and tests
**And** the scripts can be run from the extension folder without relying on host project root dependencies.

**Given** extension validation is run
**When** TypeScript source does not typecheck
**Then** validation exits non-zero
**And** the output identifies the failing extension and command.

**Given** extension validation is run
**When** lint rules fail
**Then** validation exits non-zero
**And** the output identifies the lint failure source.

**Given** extension validation is run
**When** extension tests fail
**Then** validation exits non-zero
**And** the output identifies the failing test command.

**Given** the repository-level validation command exists
**When** the builder runs it from the repository root
**Then** it discovers framework-owned TypeScript extensions
**And** it runs each extension's required validation commands.

**Given** CI validation is configured
**When** a pull request or main-branch validation run executes
**Then** extension validation runs automatically
**And** non-conforming extensions fail the CI check.

**Given** validation succeeds
**When** the builder reviews the output
**Then** the result confirms all discovered extensions passed typecheck, lint, and tests
**And** the harness is eligible for the post-bootstrap smoke workflow.

### Story 1.6: Run First Post-Bootstrap Smoke Workflow

As a builder,
I want a minimal post-bootstrap smoke workflow,
So that I can confirm the installed harness is runnable without extra mandatory configuration.

**Acceptance Criteria:**

**Given** a target project has completed bootstrap
**When** the builder runs the smoke workflow command
**Then** Pi starts successfully with the installed scaffold
**And** the smoke workflow reaches a completed status.

**Given** the smoke workflow runs
**When** it checks installed assets
**Then** it verifies required `.pi/` directories, reference files, agent placeholders, extension package files, and scripts exist
**And** it reports any missing item clearly.

**Given** default model references are valid
**When** the smoke workflow runs
**Then** no additional mandatory configuration is requested
**And** the workflow output confirms the active model reference source.

**Given** the smoke workflow fails
**When** failure output is displayed
**Then** the message includes the failed phase, cause, and next recommended action
**And** the failure does not modify project source files.

**Given** the smoke workflow succeeds
**When** the builder reviews the output
**Then** the harness-level install is considered ready for Epic 2 runtime work
**And** the result can be used as the v1 bootstrap acceptance proof.

## Epic 2: Observable Pi Multi-Agent Runtime

The builder can launch an orchestrator-backed Pi multi-agent team, dispatch sub-agents with fresh context, verify model routing by agent, observe widgets/labels/tasks in the Pi UI, and see sub-agents consume orchestrator-assigned tasks.

### Story 2.1: Implement the Generic Sub-Agent Dispatch Tool

As a builder,
I want the Pi extension to dispatch named sub-agents through one generic tool,
So that workflows can route work to different agents without hardcoding role-specific launch logic.

**Acceptance Criteria:**

**Given** the `bmad-orchestrator` extension is available
**When** a dispatch request is submitted with an agent identifier, session mode, task, and context input
**Then** the extension validates the request shape
**And** it rejects missing or unknown required fields.

**Given** a valid dispatch request names a known agent
**When** dispatch executes
**Then** the extension launches the requested agent through Pi
**And** the runtime output records the canonical agent identifier.

**Given** a dispatch request names an unknown agent
**When** dispatch validation runs
**Then** dispatch is refused
**And** the error names the unknown agent and the allowed agent identifiers.

**Given** a workflow needs to pass informal context
**When** the dispatch request includes direct message content
**Then** the sub-agent receives that content as its task context
**And** no canonical artifact path is required for informal workflows.

**Given** dispatch completes
**When** the orchestrator receives the completion signal
**Then** the signal is treated as control-plane output only
**And** durable workflow truth remains in artifacts when artifacts are part of the workflow.

### Story 2.2: Add Agent Definitions and Model Routing Contract

As a builder,
I want each sub-agent to declare its own model assignment in its agent definition,
So that different workflow stages can use different models without changing runtime code.

**Acceptance Criteria:**

**Given** the scaffold includes agent definition files
**When** the builder opens each file
**Then** the agent identifier, role label, and model assignment are readable
**And** file names use canonical lowercase kebab-case.

**Given** the extension prepares to dispatch an agent
**When** it resolves the agent definition
**Then** it uses the model assignment from the target agent file
**And** it does not use a single global workflow model by default.

**Given** two sub-agents are assigned different models
**When** both are dispatched in the same team run
**Then** each sub-agent runs with its configured model
**And** the run output records which model reference was selected for each agent.

**Given** a builder edits an agent model assignment
**When** validation is run
**Then** the changed model reference is detected
**And** no extension source code change is required.

**Given** an agent file lacks a valid model assignment
**When** dispatch validation runs
**Then** dispatch is blocked for that agent
**And** the error names the invalid agent file and required fix.

### Story 2.3: Enforce Fresh-Context Session Policy

As a builder,
I want sub-agents to start with fresh context by default,
So that workflow stages do not inherit hidden conversation history or drift across tasks.

**Acceptance Criteria:**

**Given** a dispatch request does not explicitly request an allowed resume case
**When** the sub-agent is launched
**Then** the extension starts the sub-agent in fresh-context mode
**And** prior agent conversation history is not included.

**Given** the workflow requests session reuse
**When** the session policy validates the request
**Then** reuse is allowed only for same-role red repair after red-validator rejection or same-role green repair after green-validator rejection
**And** all other reuse requests are rejected.

**Given** a validator or final reviewer is dispatched
**When** session policy is applied
**Then** the session is always fresh
**And** any requested resume mode is ignored or blocked with a policy error.

**Given** a dispatch payload includes artifact paths
**When** fresh context is assembled
**Then** the sub-agent receives only the task and explicitly named artifacts
**And** no previous runtime transcript is appended.

**Given** session policy rejects a request
**When** the orchestrator receives the rejection
**Then** execution stops safely
**And** the message identifies the requested agent, session mode, and violated policy.

### Story 2.4: Add Orchestrator Task Routing and Task List State

As a builder,
I want the orchestrator to route sequenced tasks to sub-agents and expose task state,
So that I can see which tasks are pending, in progress, and completed during a team run.

**Acceptance Criteria:**

**Given** a team run is started
**When** the orchestrator creates its task list
**Then** each task has an identifier, target agent, status, title, and context source
**And** statuses use a fixed vocabulary.

**Given** a task is pending
**When** the orchestrator dispatches its target agent
**Then** the task status changes to in-progress
**And** the active agent identifier is recorded.

**Given** a sub-agent completes successfully
**When** the orchestrator processes the completion signal
**Then** the task status changes to completed
**And** the next eligible task can be dispatched.

**Given** one sub-agent output is needed by another sub-agent
**When** the orchestrator routes the next task
**Then** the previous output is passed as declared task context or artifact path
**And** the routing decision is recorded.

**Given** a task fails or cannot be classified
**When** the orchestrator updates state
**Then** the task is marked blocked or failed
**And** the builder receives a cause and recommended next action.

### Story 2.5: Add Pi UI Visibility for Agent Activity

As a builder,
I want Pi UI visibility into active sub-agents, role labels, activity titles, and task progress,
So that I can confirm the multi-agent runtime is doing the expected work.

**Acceptance Criteria:**

**Given** a team run is active
**When** the Pi UI renders the team view
**Then** visible sub-agents display their configured role labels
**And** hidden or inactive agents follow the configured layout rules.

**Given** a sub-agent is dispatched
**When** it begins work
**Then** the UI identifies which sub-agent is currently active
**And** the displayed activity title describes the current task.

**Given** multiple terminal sessions are running in parallel
**When** the builder views the terminal UI
**Then** each session has a descriptive activity title
**And** the title makes the running agent and task distinguishable.

**Given** the orchestrator task list changes
**When** tasks move from pending to in-progress or completed
**Then** the Pi UI task/todo list reflects the current state
**And** stale task states are not shown as active.

**Given** UI rendering cannot access required runtime state
**When** the team view is displayed
**Then** it shows a safe degraded message
**And** workflow execution is not treated as successful solely because UI rendering succeeded.

### Story 2.6: Prove Multi-Agent Runtime with a Two-Agent Smoke Scenario

As a builder,
I want a small observable two-agent scenario,
So that I can prove dispatch, model routing, fresh context, UI visibility, and task handoff work before running BMAD workflows.

**Acceptance Criteria:**

**Given** the multi-agent runtime is installed
**When** the builder starts the smoke scenario
**Then** the orchestrator creates at least two ordered tasks for two distinct sub-agents
**And** each task appears in the task list.

**Given** the first sub-agent completes
**When** the orchestrator dispatches the second sub-agent
**Then** the second sub-agent receives the declared output or context from the first task
**And** it does not inherit the first sub-agent's conversation history.

**Given** the two sub-agents have different model assignments
**When** the smoke run completes
**Then** the run evidence shows each sub-agent used its configured model reference
**And** no global override hides the per-agent routing.

**Given** the smoke run is observed in Pi
**When** each sub-agent becomes active
**Then** the UI shows the active agent, role label, activity title, and current task status
**And** completed tasks are marked completed.

**Given** the smoke scenario finishes
**When** the builder reviews the result
**Then** the runtime is considered ready for standard BMAD story-to-done integration
**And** failures include actionable diagnostic output.

## Epic 3: Standard BMAD Story-to-Done Execution

The builder can take a canonical BMAD story file and execute standard `dev-story` and `code-review` workflows through the observable multi-agent runtime, with artifact-based context, iteration caps, escalation, tests, lint, and review gates.

### Story 3.1: Accept a Canonical BMAD Story File as Workflow Input

As a builder,
I want the harness to accept a standard BMAD story file as the canonical input,
So that existing BMAD story artifacts can run without modification.

**Acceptance Criteria:**

**Given** a standard BMAD story file exists
**When** the builder starts a story-to-done workflow with that file path
**Then** the harness validates the file exists and is readable
**And** the workflow records the story path as the canonical input.

**Given** the story file contains required BMAD sections
**When** input validation runs
**Then** the harness identifies story title, acceptance criteria, and implementation context
**And** it does not require the story file to be rewritten into a new format.

**Given** the story path is missing or invalid
**When** the builder starts the workflow
**Then** startup is blocked
**And** the error names the missing path and expected input format.

**Given** the workflow assembles agent context
**When** it dispatches a formal workflow sub-agent
**Then** the dispatch payload includes the story file path as an artifact source
**And** the orchestrator does not reconstruct the story content as a lossy summary.

**Given** input validation succeeds
**When** the workflow proceeds
**Then** all subsequent stages reference the same canonical story artifact
**And** runtime messages do not replace artifact truth.

### Story 3.2: Execute Standard BMAD Dev-Story Through the Runtime

As a builder,
I want the standard BMAD dev-story workflow to run through the multi-agent runtime,
So that implementation work uses fresh context, agent routing, and canonical story artifacts.

**Acceptance Criteria:**

**Given** a validated BMAD story file
**When** the builder starts the dev-story workflow
**Then** the runtime dispatches the configured implementation agent
**And** the agent receives the story file path as its primary context artifact.

**Given** the implementation agent starts
**When** session policy is applied
**Then** the agent runs in fresh-context mode
**And** prior workflow conversation history is not included.

**Given** the implementation agent modifies project files
**When** the dev-story stage completes
**Then** changed files and agent completion status are recorded
**And** the workflow proceeds only if the completion signal and artifact state are consistent.

**Given** the implementation agent cannot complete the story
**When** it reports a blocker
**Then** the workflow stops or escalates according to the blocker classification
**And** the builder receives the story identifier, cause, and recommended next action.

**Given** dev-story execution succeeds
**When** the builder inspects the run
**Then** the implementation stage is visible in the task list
**And** the configured model routing for the implementation agent is recorded.

### Story 3.3: Enforce Story Iteration Caps and Builder Escalation

As a builder,
I want story-level iteration caps to be enforced deterministically,
So that the harness stops retry loops before they become unbounded.

**Acceptance Criteria:**

**Given** a story workflow has an iteration cap of N
**When** retryable implementation or review loops run
**Then** the workflow allows no more than N iterations
**And** an N+1 iteration is never dispatched.

**Given** an iteration attempt starts
**When** the workflow records state
**Then** the current iteration count is updated before the next dispatch
**And** the count can be inspected by the builder.

**Given** the iteration cap is reached
**When** the workflow would otherwise retry
**Then** automatic execution stops
**And** the builder receives an escalation message.

**Given** escalation occurs
**When** the message is displayed
**Then** it includes the cause, story identifier, current iteration count, cap value, and recommended next action
**And** it satisfies the required escalation information contract.

**Given** a workflow completes before reaching the cap
**When** final status is recorded
**Then** no false cap escalation is produced
**And** the final iteration count remains available for audit.

### Story 3.4: Add Test and Lint Quality Gates

As a builder,
I want targeted tests and lint to run before accepting story completion,
So that implementation quality is checked automatically.

**Acceptance Criteria:**

**Given** a story implementation stage completes
**When** quality gates run
**Then** the configured targeted test command is executed
**And** the result is recorded with exit status and relevant output location.

**Given** the targeted tests fail
**When** the quality gate processes the result
**Then** story completion is blocked
**And** the workflow routes to retry or escalation according to iteration policy.

**Given** targeted tests pass
**When** lint is configured
**Then** the lint command is executed
**And** the lint result is recorded with exit status and relevant output location.

**Given** lint fails
**When** the quality gate processes the result
**Then** story completion is blocked
**And** the builder can identify the failing command and next action.

**Given** tests and lint both pass
**When** quality gate evaluation completes
**Then** the story becomes eligible for code review
**And** the workflow does not mark the story complete before review gates finish.

### Story 3.5: Execute Two-Pass BMAD Code Review Gate

As a builder,
I want two sequential BMAD code-review passes after implementation,
So that blocking findings are caught before story completion is accepted.

**Acceptance Criteria:**

**Given** implementation, tests, and lint have passed
**When** review begins
**Then** the runtime dispatches the first configured review agent in fresh-context mode
**And** the reviewer receives the story artifact and relevant changed-file context.

**Given** the first review pass returns blocking findings
**When** the workflow evaluates the result
**Then** story completion is blocked
**And** the workflow routes to retry or escalation according to iteration policy.

**Given** the first review pass has no blocking findings
**When** the second review pass begins
**Then** the runtime dispatches the second review agent in fresh-context mode
**And** the second pass does not inherit the first reviewer's conversation history.

**Given** the second review pass returns blocking findings
**When** the workflow evaluates the result
**Then** story completion is blocked
**And** the findings are reported with the reviewer identifier.

**Given** both review passes return no blocking findings
**When** the review gate completes
**Then** the story is eligible for final completion
**And** both review outputs are preserved as inspectable artifacts or logs.

### Story 3.6: Prove End-to-End Standard Story-to-Done Execution

As a builder,
I want a complete standard story-to-done smoke run,
So that I can validate the MVP delivery path on a real or representative BMAD story.

**Acceptance Criteria:**

**Given** a target project has a valid BMAD story file
**When** the builder runs the standard story-to-done workflow
**Then** the workflow executes dev-story, tests, lint, and two review passes in order
**And** each stage is visible in the task list.

**Given** the workflow dispatches agents
**When** the run completes
**Then** each dispatched agent used fresh context unless an explicitly allowed policy exception applied
**And** model routing evidence is available per agent.

**Given** all quality and review gates pass
**When** final status is written
**Then** the story is marked complete by the harness
**And** the output names the canonical story file and completed stages.

**Given** any stage fails
**When** the workflow stops
**Then** completion is not accepted
**And** the failure output includes failed stage, cause, story identifier, and next recommended action.

**Given** the smoke run succeeds on a representative project
**When** the builder reviews the result
**Then** v1 standard BMAD workflow execution is considered proven
**And** the harness is ready for formal TDD workflow work.

## Epic 4: Formal TDD/ATDD/TDAD Workflow Execution

The builder can select a TDD/ATDD/TDAD workflow profile and execute an artifact-first red/green workflow with test planning, test writing, validation, implementation, batch tracking, per-batch caps, escalation, and per-story artifact organization.

### Story 4.1: Select a Formal TDD/ATDD/TDAD Workflow Profile

As a builder,
I want to select a formal test-first workflow profile for a story,
So that the harness runs the right TDD, ATDD, or TDAD orchestration path.

**Acceptance Criteria:**

**Given** a BMAD story file is available
**When** the builder starts a formal workflow
**Then** the builder can select one supported profile: TDD, ATDD, or TDAD
**And** the selected profile is recorded for the story run.

**Given** no profile is selected
**When** the workflow requires a formal profile
**Then** startup is blocked or defaults only according to documented rules
**And** the builder is told which profiles are valid.

**Given** a selected profile exists
**When** the orchestrator builds the task plan
**Then** the plan uses the phase sequence defined for that profile
**And** the profile-specific assumptions are visible in run output.

**Given** an unsupported profile is requested
**When** validation runs
**Then** the request is rejected
**And** the error names the unsupported profile and allowed values.

**Given** the profile is accepted
**When** workflow execution begins
**Then** all formal workflow stages use artifact paths as context sources
**And** no stage relies on hidden conversation history as durable state.

### Story 4.2: Generate Test Plan and Batch Artifacts from a Story

As a builder,
I want a test-architect agent to create a test plan and batch files from a story,
So that formal test-first work is broken into traceable implementation batches.

**Acceptance Criteria:**

**Given** a formal workflow profile and story file
**When** the test-architect is dispatched
**Then** it reads the story artifact and selected profile
**And** it writes a test plan artifact for the story.

**Given** the story has multiple acceptance criteria
**When** the test-architect creates the plan
**Then** it groups work into appropriately sized batches
**And** each batch maps to one or more acceptance criteria.

**Given** batch artifacts are generated
**When** the builder inspects the story folder
**Then** batch files exist under the story's batch artifact location
**And** each batch includes scope, status, expected tests, and relevant acceptance criteria.

**Given** the story folder is created
**When** artifact organization is inspected
**Then** it includes story, changelog if applicable, test plan, batch files, orchestrator log, and runtime-proof folder placeholder
**And** folder and file names use canonical kebab-case conventions.

**Given** the test-architect cannot create a safe plan
**When** it detects ambiguity or invalid story structure
**Then** the workflow escalates with `spec-ambiguity` or `artifact-invalid`
**And** no red/green batch execution begins.

### Story 4.3: Author Batch Tests Before Implementation

As a builder,
I want a test-writer agent to author tests for a batch before implementation begins,
So that each batch starts from an explicit red test target.

**Acceptance Criteria:**

**Given** a batch is selected for execution
**When** the test-writer is dispatched
**Then** it receives the story, test plan, and current batch artifact paths
**And** it starts in fresh-context mode unless a policy-approved same-role repair applies.

**Given** the current batch defines expected behavior
**When** the test-writer completes
**Then** it creates or updates only tests relevant to the current batch
**And** it records the test files or commands needed for validation.

**Given** the test-writer detects the batch is unclear
**When** it cannot author meaningful tests
**Then** it records a structured blocker classification
**And** the workflow escalates instead of inventing unstated behavior.

**Given** tests are authored
**When** the batch artifact is updated
**Then** the batch status reflects that red tests are ready for validation
**And** the orchestrator can determine the next expected role.

**Given** generated tests require implementation that belongs to a future batch
**When** review of the batch scope occurs
**Then** the tests are considered out of scope
**And** the batch is sent for correction or escalation.

### Story 4.4: Validate Red Tests Fail for the Correct Reason

As a builder,
I want a red-validator agent to verify authored tests fail for the intended reason,
So that invalid or already-green tests do not drive implementation.

**Acceptance Criteria:**

**Given** the test-writer has authored batch tests
**When** the red-validator runs the configured test command
**Then** it captures test output and exit status
**And** it compares the failure to the batch's expected behavior gap.

**Given** tests fail for the correct reason
**When** validation completes
**Then** the batch status advances to red-validated
**And** the next expected role is implementation.

**Given** tests pass before implementation
**When** red validation completes
**Then** the result is classified as `test-issue`
**And** the workflow routes back to test repair or escalates according to retry policy.

**Given** tests fail for an unrelated setup or environment reason
**When** red validation completes
**Then** the result is classified as `environment-blocked` or `test-issue`
**And** the workflow does not proceed to implementation.

**Given** red validation produces a finding
**When** it writes output
**Then** the finding includes outcome, primary classification, rationale, recommended next action, and affected batch reference
**And** classification codes use canonical kebab-case.

### Story 4.5: Implement Batch Code to Satisfy Red Tests

As a builder,
I want a dev agent to implement only the current batch after red validation,
So that code changes are bounded to the approved test target.

**Acceptance Criteria:**

**Given** a batch has passed red validation
**When** the dev agent is dispatched
**Then** it receives the story, test plan, current batch, and red-validation output as artifact paths
**And** it does not receive hidden prior agent conversation history.

**Given** the dev agent implements the batch
**When** it changes project code
**Then** changes are limited to what is needed for the current batch behavior
**And** unrelated future batch behavior is not intentionally implemented.

**Given** the dev agent completes implementation
**When** it updates artifacts
**Then** the batch status indicates implementation is ready for green validation
**And** changed files or relevant notes are recorded.

**Given** the dev agent cannot satisfy the tests
**When** it reports a blocker
**Then** the blocker is classified using the workflow classification vocabulary
**And** the workflow routes to retry or escalation according to policy.

**Given** implementation exceeds batch scope
**When** green validation or review detects the issue
**Then** the workflow records the issue
**And** the batch cannot be accepted until scope is corrected or explicitly approved.

### Story 4.6: Validate Green Behavior Is Genuinely Achieved

As a builder,
I want a green-validator agent to verify that the batch behavior is genuinely achieved,
So that passing tests are not accepted without evidence.

**Acceptance Criteria:**

**Given** implementation for a batch is ready
**When** the green-validator runs the configured test command
**Then** it captures test output and exit status
**And** it verifies the targeted batch tests pass.

**Given** tests pass
**When** the green-validator evaluates behavior
**Then** it confirms the implemented behavior matches the batch acceptance criteria
**And** it records the evidence used for that conclusion.

**Given** tests fail due to implementation behavior
**When** green validation completes
**Then** the finding is classified as `implementation-issue`
**And** the workflow routes back to implementation repair or escalates according to retry policy.

**Given** tests fail due to invalid tests or environment issues
**When** green validation completes
**Then** the finding is classified as `test-issue` or `environment-blocked`
**And** the workflow routes according to classification rather than free-form prose.

**Given** green validation succeeds
**When** the batch artifact is updated
**Then** the batch status advances to completed or ready-for-next-batch
**And** the orchestrator can identify the next batch or finalization step.

### Story 4.7: Sync Batch Statuses and Enforce Per-Batch Caps

As a builder,
I want the orchestrator to sync batch statuses and enforce per-batch iteration caps,
So that formal workflows remain deterministic and bounded.

**Acceptance Criteria:**

**Given** a formal workflow has multiple batches
**When** a batch changes phase
**Then** the orchestrator updates the batch artifact, test plan summary, and orchestrator log consistently
**And** the next expected role is parseable from artifacts.

**Given** a batch retry loop occurs
**When** red or green repair is attempted
**Then** the retry count for that batch is updated before dispatch
**And** the count is visible in the batch artifact or log.

**Given** a batch reaches its configured iteration cap
**When** another retry would be required
**Then** the orchestrator stops automatic execution
**And** it escalates with cause, story identifier, batch identifier, cap value, and next recommended action.

**Given** artifact state contradicts the allowed workflow model
**When** the orchestrator validates state
**Then** it classifies the issue as `workflow-contract-violation`
**And** it escalates instead of guessing the next transition.

**Given** all batches complete
**When** final batch synchronization runs
**Then** the test plan shows all batch statuses complete
**And** the formal workflow can proceed to final gates or runtime proof as configured.

### Story 4.8: Prove End-to-End Formal TDD/ATDD/TDAD Story Execution

As a builder,
I want a complete formal TDD/ATDD/TDAD workflow proof run,
So that I can validate that profile selection, test planning, red/green execution, batch synchronization, and completion handoff work together before relying on the formal workflow for real stories.

**Acceptance Criteria:**

**Given** a valid BMAD story file and a supported formal workflow profile
**When** the builder starts the formal workflow proof run
**Then** the workflow records the selected profile and creates the story artifact folder, test plan, batch artifacts, and orchestrator log
**And** all formal workflow stages use artifact paths as their context sources.

**Given** the test-architect has generated a valid test plan and batch files
**When** the workflow executes each batch
**Then** test writing, red validation, implementation, green validation, and status synchronization run in the documented order
**And** each batch reaches a completed status before the next batch begins unless escalation occurs.

**Given** a red or green validation failure occurs during the proof run
**When** the workflow applies retry policy
**Then** retry counts are updated before dispatch
**And** automatic execution stops with a structured escalation when the configured cap is reached.

**Given** all batches complete successfully
**When** final formal workflow synchronization runs
**Then** the test plan shows all batches complete
**And** the orchestrator log records the final formal workflow outcome, completed stages, selected profile, and artifact locations.

**Given** the formal workflow proof run completes
**When** the builder reviews the generated artifacts
**Then** the run provides durable evidence that the formal TDD/ATDD/TDAD workflow can execute end-to-end
**And** the workflow is considered ready for runtime proof or downstream review gates as configured.

## Epic 5: Runtime Proof

The builder can execute Playwright runtime proof for completed stories and store durable proof artifacts in the story's `runtime-proof/` folder.

### Story 5.1: Detect Runtime Proof Prerequisites and Prepare Artifact Folder

As a builder,
I want the harness to detect Playwright/runtime-proof prerequisites and prepare the runtime-proof folder,
So that runtime verification failures are diagnosed before final proof execution.

**Acceptance Criteria:**

**Given** a story workflow reaches runtime-proof preparation
**When** prereq detection runs
**Then** the harness checks for Playwright availability and required browser runtime
**And** it reports missing dependencies without installing them silently.

**Given** runtime-proof is enabled
**When** the story artifact folder is prepared
**Then** a `runtime-proof/` folder exists for that story
**And** it is located under the story's implementation artifact directory.

**Given** Playwright is missing
**When** runtime-proof preparation runs
**Then** the workflow reports `environment-blocked`
**And** the message includes the story identifier and recommended install command.

**Given** runtime-proof is optional for the current phase
**When** prerequisites are missing
**Then** the workflow follows documented skip or escalation behavior
**And** it does not falsely report proof completion.

**Given** prerequisites are available
**When** preparation completes
**Then** the workflow records that runtime proof can be executed
**And** the next expected action is parseable.

### Story 5.2: Execute Playwright Runtime Proof and Store Evidence

As a builder,
I want the harness to execute a Playwright run and store evidence artifacts,
So that completed stories have inspectable runtime proof.

**Acceptance Criteria:**

**Given** runtime-proof prerequisites are satisfied
**When** the workflow runs the configured Playwright command
**Then** the command executes against the configured running application target
**And** exit status and command output are captured.

**Given** Playwright produces screenshots, traces, videos, or logs
**When** the run completes
**Then** all configured proof artifacts are stored under the story's `runtime-proof/` folder
**And** filenames are stable enough for later inspection.

**Given** the Playwright run fails
**When** the workflow evaluates the result
**Then** story completion is blocked if runtime proof is required
**And** the failure message names the failing command and proof artifact location.

**Given** the Playwright run succeeds
**When** final proof status is written
**Then** the story records runtime-proof success
**And** the recorded evidence includes paths to generated artifacts.

**Given** runtime evidence is reviewed later
**When** the builder opens the story folder
**Then** proof artifacts are discoverable without reading transient terminal output
**And** the evidence remains git-visible unless intentionally ignored by policy.

## Epic 6: Execution Traceability & Resume

The builder can inspect complete execution logs, trace phase and agent routing decisions, and resume workflow execution from a known checkpoint.

### Story 6.1: Write Full Execution Logs for Workflow Runs

As a builder,
I want every workflow run to write a full execution log,
So that I can inspect what happened after completion or failure.

**Acceptance Criteria:**

**Given** a workflow run starts
**When** the first phase begins
**Then** an execution log artifact is created or opened
**And** it records run identifier, story identifier, start time, selected workflow, and selected profile if applicable.

**Given** a phase starts or ends
**When** the orchestrator updates the log
**Then** it records phase name, agent identifier if any, status, timestamp, and relevant artifact paths
**And** entries are appended in chronological order.

**Given** a dispatch occurs
**When** the log entry is written
**Then** it records agent identifier, session mode, model reference, task title, and context source paths
**And** it does not include provider API keys or secrets.

**Given** a gate or validation fails
**When** the log entry is written
**Then** it includes the classification, affected story or batch, and recommended next action
**And** the failure is inspectable without relying on terminal scrollback.

**Given** the workflow completes
**When** final status is written
**Then** the log contains a clear final outcome
**And** the builder can locate the log from the story artifact folder.

### Story 6.2: Trace Phase History and Agent Routing Decisions

As a builder,
I want to trace phase history and agent routing decisions,
So that workflow behavior is debuggable and auditable.

**Acceptance Criteria:**

**Given** a workflow has multiple phases
**When** the builder inspects the phase trace
**Then** each phase transition shows from-state, to-state, triggering event, and validation result
**And** transitions use documented status codes.

**Given** the orchestrator routes to an agent
**When** a routing decision is recorded
**Then** the trace includes selected agent, reason for selection, model reference, session mode, and context artifacts
**And** the decision is tied to a specific phase or task.

**Given** a validator output drives routing
**When** the orchestrator records the decision
**Then** it records the validator outcome and canonical classification code
**And** it does not route based only on unstructured prose.

**Given** an ambiguous or invalid state is detected
**When** trace output is written
**Then** the trace records why automatic continuation was unsafe
**And** the workflow escalates to the builder.

**Given** the builder debugs a stalled workflow
**When** they read the trace
**Then** they can identify the last clean phase and failed transition
**And** they can decide whether resume is safe.

### Story 6.3: Resume Workflow from a Known Phase Checkpoint

As a builder,
I want to resume a workflow from a known phase checkpoint,
So that recoverable interruptions do not require restarting an entire story run.

**Acceptance Criteria:**

**Given** a workflow has written checkpoint-capable artifacts
**When** the builder requests resume
**Then** the harness reads durable Markdown artifacts to determine the last known phase
**And** it does not rely on hidden runtime memory.

**Given** the last known phase is valid and resumable
**When** resume validation succeeds
**Then** the workflow restarts from the documented next phase
**And** the resumed run records that it resumed from a checkpoint.

**Given** artifacts are missing, malformed, or contradictory
**When** resume validation runs
**Then** resume is blocked
**And** the workflow escalates with `artifact-invalid` or `workflow-contract-violation`.

**Given** resume dispatches an agent
**When** session policy is applied
**Then** the agent starts fresh unless the resume case is explicitly allowed by policy
**And** context is assembled from artifact paths.

**Given** resume completes successfully
**When** the builder inspects the execution log
**Then** the log shows pre-resume history, resume event, resumed phase, and final outcome
**And** the phase trace remains continuous enough for audit.

## Epic 7: Advanced Harness Configurator

The builder can create new BMAD-derived workflows and configure Pi harness setup through a configurator without directly editing raw framework files.

### Story 7.1: Add Configurator Project and Schema Foundation

As a builder,
I want a configurator foundation with schemas for workflows and harness setup,
So that future configuration can be generated safely instead of hand-edited.

**Acceptance Criteria:**

**Given** the configurator feature is enabled
**When** the builder inspects the configurator files
**Then** schemas exist for workflow profile configuration and harness setup configuration
**And** schema fields are documented with examples.

**Given** a workflow configuration file is provided
**When** schema validation runs
**Then** valid configurations pass
**And** invalid configurations report field-level errors.

**Given** a harness setup configuration file is provided
**When** schema validation runs
**Then** agent, hook, extension, model reference, and workflow fields are validated
**And** unknown critical fields are rejected or warned according to documented policy.

**Given** validation fails
**When** output is displayed
**Then** it names the file, field path, invalid value, and expected format
**And** no generated files are written.

**Given** schema validation succeeds
**When** the configurator proceeds
**Then** generated output is based only on validated configuration
**And** secrets are not accepted as committed config values.

### Story 7.2: Generate a BMAD-Derived Workflow from Configuration

As a builder,
I want to generate a BMAD-derived workflow from a validated configuration,
So that I can create new workflow variants without editing raw skill files manually.

**Acceptance Criteria:**

**Given** a valid workflow configuration
**When** the configurator generates a workflow
**Then** it creates a skill folder with `SKILL.md`, `workflow.md`, `steps/`, and `templates/` as needed
**And** generated files follow naming conventions.

**Given** the configuration defines phases
**When** workflow files are generated
**Then** the phase sequence is represented in the generated workflow
**And** phase names use documented status conventions.

**Given** the configuration defines agents per phase
**When** generation completes
**Then** generated workflow files reference canonical agent identifiers
**And** invalid or missing agents are rejected before generation.

**Given** a generated workflow would overwrite an existing workflow
**When** generation runs
**Then** safe overwrite rules are applied
**And** the builder can preview or approve destructive changes before they occur.

**Given** generation succeeds
**When** the builder runs validation
**Then** the generated workflow is discoverable by Pi/BMAD
**And** it can be inspected without reading configurator internals.

### Story 7.3: Configure Pi Harness Agents, Hooks, and Extensions

As a builder,
I want the configurator to generate or update Pi harness setup files,
So that agents, hooks, and extensions can be configured through a higher-level interface.

**Acceptance Criteria:**

**Given** a valid harness setup configuration
**When** generation runs
**Then** the configurator creates or updates declared agent definition files
**And** model assignments are written in the appropriate agent files.

**Given** hook configuration is declared
**When** generation runs
**Then** generated hook definitions include explicit tool or command boundaries
**And** unsafe or overly broad hook definitions are rejected or flagged.

**Given** extension configuration is declared
**When** generation runs
**Then** extension settings are written to the correct project-local `.pi/extensions/` location
**And** extension dependencies remain scoped to the extension folder.

**Given** a configuration references a model
**When** validation runs
**Then** the model reference is checked against Pi-level model declarations where possible
**And** API keys or provider secrets are not written into generated files.

**Given** generation completes
**When** the builder reviews changed files
**Then** all generated or modified files are listed
**And** the builder can identify how the harness setup changed.

### Story 7.4: Add Configurator Preview, Validation, and Dry-Run Workflow

As a builder,
I want preview and dry-run support for configurator changes,
So that I can understand generated changes before applying them.

**Acceptance Criteria:**

**Given** a valid configurator input file
**When** the builder runs preview mode
**Then** the configurator shows planned file creations, updates, and skips
**And** no files are modified.

**Given** planned changes include overwrites
**When** preview output is displayed
**Then** each overwrite is labeled with path, reason, and safety classification
**And** destructive changes require explicit apply mode.

**Given** the builder runs dry-run validation
**When** validation completes
**Then** schemas, naming conventions, agent references, model references, and overwrite rules are checked
**And** the final output is pass/fail with actionable diagnostics.

**Given** dry-run fails
**When** the builder reads the diagnostics
**Then** no generated files are written
**And** the output names every blocking issue found.

**Given** dry-run passes and apply mode is run
**When** generation completes
**Then** the configurator writes the planned files
**And** a summary of applied changes is saved for audit.

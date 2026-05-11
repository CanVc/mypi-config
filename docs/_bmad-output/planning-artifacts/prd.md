---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success", "step-04-journeys", "step-05-domain", "step-06-innovation", "step-07-project-type", "step-08-scoping", "step-09-functional", "step-10-nonfunctional", "step-11-polish", "step-12-complete"]
inputDocuments:
  - "docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md"
  - "docs/_bmad-output/planning-artifacts/research/agentic-tdd-story-workflow-decisions-2026-04-13.md"
  - "docs/_bmad-output/planning-artifacts/research/agentic-tdd-story-artifact-spec-2026-04-13.md"
  - "docs/_bmad-output/planning-artifacts/research/agentic-tdd-story-example-workflow-2026-04-13.md"
  - "docs/_bmad-output/planning-artifacts/research/agentic-tdd-story-v1-open-implementation-questions-2026-04-14.md"
workflowType: 'prd'
date: '2026-04-14'
briefCount: 1
researchCount: 4
brainstormingCount: 0
projectDocsCount: 0
classification:
  projectType: developer_tool
  domain: agentic_ai_developer_tooling
  complexity: medium
  projectContext: greenfield
---

# Product Requirements Document - mypi-config

**Author:** Cvc
**Date:** 2026-04-14

## Executive Summary

`mypi-config` is a personal Pi-powered execution harness for a single advanced solo builder who uses BMAD artifacts to structure software delivery. The project fills the gap between planning rigor (BMAD) and delivery rigor: BMAD provides strong story artifacts and process vocabulary; Pi provides deep configurability; `mypi-config` assembles them into a coherent, portable operating model.

The harness is built using Pi's own configuration system — custom agents, hooks, and TypeScript extensions — giving the user a setup that functions like Claude Code but optimized for their specific delivery style rather than a generic audience. BMAD remains the unmodified base: standard story files, standard workflows, standard compatibility. On top of this base, a family of derived workflows adds optional TDD/ATDD/TDAD discipline for stories where test-first quality discipline is warranted. These derived workflows are currently in active design (see `/research/`). The TDD layer is available, not mandatory.

The primary value is portability and consistency: the harness installs into future projects through a single bootstrap step, eliminating per-project orchestration reconstruction.

### What Makes This Special

The differentiation is in the execution discipline, not in novel AI primitives. Five properties work together:

- **BMAD-compatible by design.** Derived workflows wrap BMAD, they do not replace it. The standard delivery path is always available; TDD-enriched paths are opt-in based on story profile.
- **Pi as the framework, not just the runtime.** Pi's agent, hook, and extension system is used to build the harness itself. The result is a fully configurable, introspectable execution layer.
- **Multi-model by design.** Each workflow stage can be assigned a different model. Implementation, review, and validation are treated as distinct jobs with different cost/quality profiles. This breaks provider lock-in and enables deliberate model routing — something Claude Code's single-provider model cannot offer.
- **Opinionated for one user.** The harness is not designed to satisfy all teams or styles. It is tuned for a known working style, which makes it more reliable and less compromised than a general-purpose framework.
- **Drop-in portable.** The entire harness installs into a new project through a single bootstrap step. No manual reconfiguration, no per-project orchestration rebuild. The operational model travels with the user across projects.

## Project Classification

| Property | Value |
|---|---|
| **Project Type** | Developer tool / personal execution harness |
| **Domain** | Agentic AI developer tooling |
| **Complexity** | Medium |
| **Project Context** | Greenfield |

## Success Criteria

### User Success

Success is validated against three concrete signals:

1. **Configurable harness.** The Pi setup is easy to understand, modify, and extend without consulting external documentation on every change. A new agent or hook can be added in minutes.
2. **Functional workflows.** Standard BMAD workflows (dev-story, code-review) run end-to-end through the harness with correct model routing. Workflow execution is observable and the output is inspectable.
3. **Proof on a real project.** At least one story from a real external project completes through the harness with genuinely good quality — tests pass, behavior is correct, no manual forcing required. This is the acceptance test.

### Business Success

This is a personal productivity tool. Business success equates to user success: the harness becomes the default execution substrate for future projects, installed rather than rebuilt from scratch each time.

### Technical Success

- Pi harness boots cleanly in a new project via bootstrap
- Multi-model routing is configurable per workflow stage via agent definition files
- BMAD story files are valid inputs to the harness without modification
- Workflow execution produces inspectable outputs (logs, artifacts)

### Measurable Outcomes

- Story completes end-to-end with no harness-level errors
- Each agent's model assignment is defined in its agent file and respected at execution time
- Bootstrap into a new project requires no manual file editing

## Product Scope

### MVP — v1

Pi harness + standard BMAD workflows (dev-story, code-review) + multi-model routing. v1 explicitly excludes TDD-derived workflow variants and runtime-proof execution. Acceptance test: a real story from an external project completes with good quality.

### Growth — v2

v1 + derived TDD/ATDD/TDAD workflows. Story profiles determine which workflow variant runs. Runtime proof and test-architected batch execution enter scope in this phase. Research artifacts from `/research/` feed directly into workflow design.

### Vision — v3

v2 + full auditability layer: orchestrator logs, phase traceability, structured execution history per story. Workflow execution becomes fully inspectable and debuggable.

### Horizon — v4

Advanced configurator for creating new BMAD-derived workflows and configuring the Pi harness without editing raw files. This is the layer that makes `mypi-config` distributable as an open-source starter: a setup experience accessible to users beyond the original author. Out of scope for MVP; unlocks only if real usage justifies the investment.

## User Journeys

### v1 — Journey 1: New Project Bootstrap

Cvc starts a new project. He runs the bootstrap command — the harness installs, agents and hooks land in place, defaults are ready. He triggers the first BMAD workflow on a small test story. It runs. Output lands in the right place.

Total setup time: minutes, not hours. The next project will be the same.

**Capabilities revealed:** bootstrap/install mechanism, opinionated defaults, portability.

---

### v1 — Journey 2: Story to Done (Happy Path)

Cvc has a BMAD story ready. He points the harness at the story file and triggers the workflow. The harness assigns the right model per stage — cheaper model for implementation, stronger for review — and kicks off the dev agent with a clean, bounded context. No trailing conversation history, no context drift.

The dev agent implements. The review agent runs. Findings come back minor. A second pass confirms no blocking issues. Tests pass, lint is clean, behavior matches the acceptance criteria. Cvc didn't intervene once.

**Capabilities revealed:** story file as input, multi-model routing, fresh-context handoff, quality gates, iteration cap.

---

### v2 — Journey 3: TDD Story Execution

Cvc has a story with user-visible acceptance criteria. He selects the TDD profile and triggers the harness.

The test-architect runs first — reads the story, proposes a batch plan, generates the initial batch files. Batch by batch: test-writer authors tests (red), red-validator confirms they fail for the right reason, dev implements (green), green-validator checks behavior is genuinely achieved. The orchestrator logs each phase transition, syncs statuses in the test plan.

On the final batch, a Playwright run executes against the running app — screenshots and a trace land in `runtime-proof/`. Final code review passes. The entire execution is traceable batch by batch in the story folder.

**Capabilities revealed:** TDD-derived workflow, test-architect, batch-based red/green cycle, red/green validators, orchestrator log, Playwright runtime proof, story folder structure.

---

### v3 — Journey 4: Workflow Stalls (Debug)

Mid-execution, something is off. The dev agent produced an implementation that doesn't match the story scope. Cvc checks the orchestrator log, traces the phase history, spots where the handoff was incomplete. He adjusts the config and resumes from the last clean checkpoint.

**Capabilities revealed:** execution logs, phase traceability, resumable state, inspectable artifacts.

---

### v4 — Journey 5: Open-Source Adopter (Horizon)

A Pi/BMAD power user finds the repo. They run the configurator, answer a few questions about their models and BMAD setup. Their harness config is generated. Their first story runs. They didn't read a single internal file.

**Capabilities revealed:** advanced configurator, opinionated defaults with escape hatches, discoverability.

---

### Journey Requirements Summary

| Capability | Journey | Version |
|---|---|---|
| Bootstrap / install mechanism | J1 | v1 |
| Opinionated defaults, zero required config | J1 | v1 |
| Story file as canonical input | J2 | v1 |
| Multi-model routing per stage | J2 | v1 |
| Fresh-context agent handoff | J2 | v1 |
| Quality gates (tests, lint, review) | J2 | v1 |
| Iteration cap + stop condition | J2 | v1 |
| TDD-derived workflow + story profiles | J3 | v2 |
| Test-architect + batch planning | J3 | v2 |
| Red/green validator cycle | J3 | v2 |
| Orchestrator + story folder structure | J3 | v2 |
| Playwright runtime proof | J3 | v2 |
| Execution logs + phase traceability | J4 | v3 |
| Resumable workflow state | J4 | v3 |
| Advanced configurator UI | J5 | v4 |

---

> **Note — Workstation Setup Constraint:** The target development environment is a new Ubuntu machine (migrated from Windows), near-virgin state (no Python, Pi, Playwright dependencies). This is a known prerequisite for the entire project. Recommended handling: Epic 0 — Workstation & Toolchain Setup, derived from this PRD.

## Domain-Specific Requirements

### Technical Constraints

**LLM Non-Determinism in TDD Context**
- Two runs on the same story may produce different results; workflow design must account for variability without blocking progress.
- Red/green validators must verify actual test output, not rationalize a pass. Validation prompts must be explicit about evidence requirements.

**Context Window Management**
- Handoff artifacts must remain within model context limits. Orchestration logs and batch files must stay lean.
- Context drift risk on long runs: each agent starts from a bounded, assembled context — not from a shared conversational thread.

**Tooling and Permissions**
- Pi hooks execute shell commands; hook definitions must be scoped and auditable.
- Playwright browser dependencies are installed as part of Epic 0 — Workstation & Toolchain Setup (v2 prerequisite).

### Risk Mitigations

| Risk | Mitigation |
|---|---|
| Validator rationalizes instead of validating | Explicit evidence requirements in validator prompts |
| Handoff exceeds context window | Bounded artifact format enforced by design |
| Hook misconfiguration exposes shell surface | Hooks reviewed and documented before activation |
| Playwright unavailable at v2 launch | Toolchain setup (Epic 0) includes browser dependency install |

## Developer Tool Specific Requirements

### Project-Type Overview

`mypi-config` is a Pi-based execution harness distributed as a project scaffold. It is installed on top of an existing BMAD setup, not as a standalone product. The unit of distribution is a set of Pi configuration files, TypeScript extensions, and derived BMAD workflow files that extend a target project without replacing its base tooling.

### Language / Runtime Support

Primary target environment is a local Ubuntu developer workstation. v1 support is defined for a single advanced builder running Pi against BMAD artifacts inside a repository-local setup.

**Supported runtime surfaces:**
- Pi execution environment
- BMAD markdown artifacts as workflow inputs
- Shell-based bootstrap into a target repository
- Repository-local config files and agent definitions

**Compatibility boundary:**
- BMAD v6 base install is required before bootstrap
- Pi compatibility target is version `0.67.2` plus the latest approved stable Pi version
- Ubuntu is the primary supported operating environment for v1

**Explicit non-goals for v1:**
- Guaranteed Windows support
- Multi-user or team coordination semantics
- Hosted control plane or centralized workflow service
- Automated cross-version migration tooling

### Prerequisites

| Dependency | Required Version | Notes |
|---|---|---|
| Pi | ≥ 0.67.2 | Core execution harness |
| BMAD | v6 | Base workflows — installed separately before bootstrap |
| OS | Ubuntu (primary) | Dev machine context; other Unix systems untested |
| Playwright | v2+ prerequisite | Required for TDD runtime proof (v2 scope) |

Additional toolchain dependencies (Python version, Node, browser binaries) to be finalized in Epic 0 — Workstation & Toolchain Setup.

### Installation Method

Single-command bootstrap into a target project. No external publishing or package registry required. BMAD v6 must be installed in the target project before running the bootstrap.

**Full install sequence:**
1. Pi ≥ 0.67.2 installed
2. Pi `models.json` configured — models used by harness agents must be declared at the Pi level (one-time setup)
3. BMAD v6 installed in the target project
4. Bootstrap `mypi-config` — installs Pi agents, hooks, extensions, and derived BMAD workflows

Constraint: a developer with repo access must be able to complete the full install in under 5 minutes.

Exact bootstrap mechanism (shell script, submodule, or copy) to be decided in architecture phase.

### Exposed Surface

The harness exposes a narrow builder-facing surface rather than a general-purpose automation platform.

**Primary inputs:**
- BMAD story files
- Project-local harness configuration
- Installed Pi model declarations

**Primary outputs:**
- Workflow execution artifacts
- Review outputs and findings
- Logs and execution evidence by phase

**User-visible operations:**
- Bootstrap the harness into a target project
- Run a standard BMAD workflow through the harness
- Select an available workflow/profile when applicable
- Inspect workflow status and execution outputs
- Change per-role model assignment

**Configuration surface:**
- Agent role definitions
- Workflow/profile selection
- Model assignment by role
- Bounded execution and retry settings

**Explicitly out of v1 exposed surface:**
- Interactive workflow configurator
- Generalized conversational orchestration mode
- Arbitrary non-story task routing

The harness ships fully configured with opinionated defaults — zero required edits to run the first workflow.

### Usage Examples

The PRD uses outcome-level examples to define what a usable developer tool must support.

- A builder installs the harness into a BMAD-ready project and runs the first story without additional mandatory edits.
- A builder runs `dev-story` on a standard BMAD story with the harness routing each stage to the configured role/model pair.
- A builder inspects review output, logs, and quality-gate results after a standard story loop completes.
- A builder changes the model assigned to review without changing workflow logic.
- A builder installs the same harness in a second project without rebuilding orchestration manually.

Reference workflow examples and artifact specifications in `/research/` remain primary design inputs for v2 derived workflows.

### Migration / Adoption Path

`mypi-config` is intended to be adopted by a builder who already has BMAD familiarity and may be migrating from a Claude Code-style personal workflow.

**Adoption path for v1:**
1. Install Pi
2. Declare required models in Pi
3. Install BMAD v6 in the target project
4. Bootstrap `mypi-config`
5. Run a first validation story through the standard harness path

**Migration expectations:**
- Existing BMAD story artifacts do not need to be rewritten
- Standard BMAD workflows remain available
- `mypi-config` adds orchestration and role/model discipline on top of the BMAD base

**Primary migration risks:**
- Local toolchain mismatch on a near-clean Ubuntu workstation
- Model declaration/configuration errors
- Bootstrap assumptions not met in the target repository

**Adoption success looks like:**
- First story completes end-to-end
- Outputs are inspectable
- No per-project orchestration rebuild is required

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Proof-of-execution — the MVP succeeds when a real story from a real external project completes through the harness with genuinely good quality, without manual forcing. The goal is a working personal tool, not a polished product.

**Resource Requirements:** Solo builder. Scope decisions must be compatible with solo execution.

### MVP Feature Set — v1

**Core journeys supported:** J1 (Bootstrap), J2 (Story to Done)

**Must-Have Capabilities:**
- Pi harness: custom agents, hooks, TypeScript extensions — installable via single bootstrap
- Pi `models.json` setup with declared models
- BMAD v6 compatibility — derived workflows layer on top of standard install
- Standard BMAD workflows (dev-story, code-review) running through the harness
- Multi-model routing: model assigned per agent, defined in agent files
- Fresh-context handoff between stages
- Quality gates: tests pass, lint clean, two review passes with no blocking findings
- Iteration cap per story (standard dev-review loop)
- TDD-derived workflows, test-architect roles, and runtime proof are explicitly out of v1 scope

**v1 sequencing constraint:** The MVP must build the observable multi-agent runtime first. Review-dependent story-to-done validation and portable bootstrap proof come after sub-agent dispatch, fresh-context execution, model routing, and task-state visibility exist.

### Post-MVP Features

**v2 — TDD Layer:**
- Derived TDD/ATDD/TDAD workflows
- Test-architect, test-writer, red/green validator agents
- Batch-based execution with orchestrator
- Story folder structure (test-plan, batch files, orchestrator log)
- Per red-green-refactor iteration cap — bounded retry policy per batch cycle before escalation to human
- Playwright runtime proof

**v3 — Auditability:**
- Full execution logs and phase traceability
- Resumable workflow state

**v4 — Horizon (open-source):**
- Advanced configurator for workflows and harness setup

### Risk Mitigation Strategy

**Technical Risks:**

| Risk | Mitigation |
|---|---|
| TDD research still in progress → blocks v2 | v2 explicitly depends on research completion; v1 delivers independently |
| Pi hooks or agent behavior unreliable | Validate each agent in isolation before wiring the full pipeline |
| LLM non-determinism breaks quality gates | Quality gate prompts require explicit evidence, not inference |
| Bootstrap mechanism unclear | Decide in architecture phase before Epic 1 starts; Epic 0 validates the install flow |

**Resource Risks:**

Solo execution means scope must stay lean. v1 is intentionally narrow: standard BMAD + harness + multi-model. TDD layer waits until v1 is proven on a real project.

## Functional Requirements

### Harness Bootstrap & Setup

- FR1: Builder can install the harness into a target project via a single bootstrap command
- FR2: Builder can declare available models in Pi `models.json` as part of initial setup
- FR3: Builder can modify the model assigned to a workflow stage by editing the relevant agent definition file
- FR4: Builder can run the first workflow after bootstrap without any additional mandatory configuration

### Workflow Execution

- FR5: Builder can trigger a BMAD story workflow using a story file as the canonical input
- FR6: Builder can execute the standard BMAD dev-story workflow through the harness
- FR7: Builder can execute the standard BMAD code-review workflow through the harness
- FR8: Builder can run two sequential review passes on a completed story

### Agent Orchestration

- FR9: Harness can launch each workflow stage from an isolated context assembled only from the current story, declared supporting artifacts, and the previous stage's approved outputs
- FR10: Harness can route each workflow stage to the model defined in the corresponding agent file
- FR11: Harness can enforce an iteration cap per story and stop execution when the cap is reached
- FR12: Harness can escalate to the builder when an iteration cap is hit

### Quality Gates

- FR13: Harness can verify the targeted test suite passes before accepting story completion
- FR14: Harness can verify lint passes cleanly before accepting story completion
- FR15: Harness can block story completion if any review pass returns blocking findings

### Orchestration & Interface Layer *(v1)*

- FR16: Builder can run a named multi-agent workflow with defined stage order, assigned roles, and explicit handoff boundaries
- FR17: Builder can start a sub-agent run without inheriting prior batch conversation history
- FR18: Builder can configure which workflow roles are visible during execution and how their status is grouped in the interface
- FR19: Builder can see which workflow role is active and the current stage it is executing
- FR20: In formal TDD workflows, orchestrated roles can use story artifacts as their primary context source
- FR22: Builder can assign a distinct model to each sub-agent within the same team
- FR23: Orchestrator can route the output of one sub-agent as the input to another in a defined sequence
- FR24: Builder can label a running workflow session so concurrent executions are distinguishable
- FR25: Builder can view workflow task state as pending, in-progress, and completed

### TDD Workflow *(v2)*

- FR26: Builder can select a TDD/ATDD/TDAD workflow profile for a story
- FR27: Test-architect agent can generate a test plan and batch files from a story
- FR28: Test-writer agent can author tests for a batch before any implementation begins
- FR29: Red-validator agent can verify that authored tests fail for the correct reason
- FR30: Dev agent can implement code to make a batch's tests pass
- FR31: Green-validator agent can verify that batch behavior is genuinely achieved
- FR32: Orchestrator can track and sync batch statuses across story artifacts (batch files, test plan, orchestrator log)
- FR33: Harness can enforce a per-batch iteration cap and escalate blocked batches to the builder
- FR34: Story artifacts are organized in a per-story folder (story file, changelog, test plan, batch files, orchestrator log, runtime-proof)

### Runtime Verification *(v2)*

- FR35: Harness can execute a Playwright run against the running application as part of story completion
- FR36: Harness can store runtime proof artifacts (screenshots, traces, logs) in the story's runtime-proof folder

### Auditability *(v3)*

- FR37: Builder can inspect a full execution log for any completed or in-progress story
- FR38: Builder can trace the phase history and agent routing decisions for any workflow run
- FR39: Builder can resume a workflow from a known phase checkpoint

### Advanced Configuration *(v4)*

- FR40: Builder can create a new BMAD-derived workflow through a configurator without editing raw files
- FR41: Builder can configure Pi harness setup (agents, hooks, extensions) through a configurator interface

## Non-Functional Requirements

### Security

- No committed agent or workflow definition file contains plaintext provider API keys; this is verified by repository secret scanning on every main-branch change
- Each agent/workflow profile explicitly declares its allowed active tools, and no tool outside that allowlist can be invoked during execution; static validation passes for 100% of profiles
- Bootstrap completes on a clean Ubuntu workstation without `sudo` during the harness installation phase

### Integration

- The smoke suite passes in 100% of 3 consecutive clean-run executions on Pi 0.67.2 and the latest approved stable Pi version
- On a clean BMAD v6 base installation, 100% of reference derived workflows install and execute without manual file edits
- 100% of sampled standard BMAD story files in the compatibility suite execute as valid workflow inputs without manual edits

### Reliability

- Iteration caps are enforced deterministically — a cap of N never allows N+1 iterations
- When escalation occurs (cap reached, batch blocked), the harness message includes the cause, story/batch identifier, and next recommended action; this must pass in 3/3 escalation test scenarios

### Maintainability

- Agent definition files are readable and editable without knowledge of Pi internals — a builder can change a model assignment in under 2 minutes
- Every Pi TypeScript extension follows the standard extension template and passes lint/typecheck at 100%; non-conforming extensions fail CI validation
- A builder familiar with BMAD identifies trigger, phases, and output artifacts in a derived workflow in ≤10 minutes; success rate is ≥80% across 3 internal reviewers


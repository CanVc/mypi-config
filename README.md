# mypi-config

`mypi-config` is an **opinionated Pi + BMAD starter** built for demanding solo use: execute BMAD stories through a structured delivery loop with specialized agents, multi-model routing, and quality guardrails.

The goal is not to build a universal platform, but a **portable execution layer** that can be reused across projects via a simple bootstrap.

## Why this project?

BMAD brings strong planning rigor (stories, artifacts, handoffs), and Pi brings deep configurability (agents, hooks, extensions). This project bridges the gap between both:

- keep BMAD artifacts as the source of truth;
- industrialize story execution (not only planning);
- reduce dependency on a single provider/model;
- improve reliability with fresh context at every stage;
- introduce a test-first discipline (derived TDD) where it matters.

## What `mypi-config` provides

- **Story-centric**: the BMAD story file is the canonical workflow input.
- **Multi-model**: model selection can vary by role/stage (implementation, review, validation).
- **Fresh-context handoff**: each phase starts with a bounded context, reducing drift.
- **Quality gates**: tests, lint, review passes, and (v2) Playwright runtime proof.
- **Portable bootstrap**: install into a new repo without rebuilding orchestration manually.

## Positioning (important)

- Designed primarily for **one advanced solo builder**.
- **BMAD stays the foundation**: derived workflows extend it, not replace it.
- This repository is a **reusable personal harness**, not yet a mass-market product.

## Scope by version

### v1 (MVP)

- Bootstrap the Pi harness into a target project
- BMAD v6 compatibility
- Run standard BMAD workflows (`dev-story`, `code-review`)
- Multi-model routing per agent
- Dev/review loop with iteration cap
- Quality gates: passing tests, clean lint, two review passes with no blockers

### v2 (growth)

- Derived TDD/ATDD/TDAD workflows
- Dedicated agents (test-architect, test-writer, red/green validators)
- Batch-based execution with status orchestration
- Runtime verification via Playwright with proof artifacts

### v3 (vision)

- Full execution logging
- Phase and handoff traceability
- Resume workflow from a checkpoint

### v4 (horizon)

- Advanced configurator to create/configure workflows without editing raw files

## Success criteria

The project is successful when:

- a real story (from an external project) completes end-to-end with good quality;
- the harness can be installed quickly in a new project;
- behavior is inspectable (artifacts/logs) and role routing is correct;
- human intervention stays minimal on the happy path.

## Prerequisites (PRD targets)

- Pi `>= 0.67.2`
- BMAD v6 (installed as a base before bootstrap)
- Ubuntu (primary target environment)
- Playwright (required for runtime proof in v2)

## Current status

The project is currently being structured around the product brief and PRD. Some capabilities (notably the full TDD layer and advanced auditability) are roadmap items.

## Key documentation

- Product Brief: `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`
- PRD: `docs/_bmad-output/planning-artifacts/prd.md`
- PRD Validation: `docs/_bmad-output/planning-artifacts/prd-validation-report-2026-04-14.md`
- Research (TDD workflows, artifacts, decisions): `docs/_bmad-output/planning-artifacts/research/`

## In one sentence

`mypi-config` aims to become a **portable agentic delivery engine**: *BMAD story in, disciplined and verifiable execution out*.

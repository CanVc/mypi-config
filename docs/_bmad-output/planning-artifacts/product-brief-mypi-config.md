---
title: "Product Brief: mypi-config"
status: "complete"
created: "2026-04-12T16:52:22+02:00"
updated: "2026-04-12T17:06:41+02:00"
inputs:
  - "docs/research/mypi-config-ideation.md"
  - "docs/research/tdd-initiative"
---

# Product Brief: mypi-config

## Executive Summary

`mypi-config` is an opinionated Pi + BMAD workflow starter built to replace and improve an already well-performing Claude Code setup. Its purpose is to give a single power user a reusable, project-portable execution layer for story-driven delivery using specialized agents, multi-model orchestration, bounded iteration loops, and TDD-first development. The immediate goal is not to create a generic platform for everyone. The goal is to create a reliable personal system that can be dropped into future projects in one simple install step and then used handoff-style with minimal supervision.

The core pain is clear: Pi is highly configurable, and BMAD provides strong planning artifacts and handoff structure, but neither gives this exact execution workflow out of the box. The current state is a gap between planning rigor and delivery rigor. The user already knows that a structured Dev → Review loop can work well in practice, but wants to go further: reduce dependence on a single provider, choose the right model for each role, enforce stronger quality standards, and introduce a real tests-first discipline instead of relying on code-first implementation followed by validation.

The proposed solution is a reusable repository scaffold that installs into other projects and centers work around BMAD story files. For each story, it runs a defined delivery pipeline using different models for different roles, with explicit quality gates for tests, linting, review findings, and runtime verification. Just as importantly, each major step should start with a fresh, tightly scoped context built from the story and BMAD documentation rather than inheriting a long conversational trail. That reduces context drift, avoids compaction pressure, and keeps every agent handoff grounded in the same source of truth. Over time, this becomes not just a Pi configuration, but a durable operating model for agentic software delivery: story in, disciplined TDD loop out, with consistent handoffs and higher trust in the final result.

## The Problem

A strong story artifact is not enough if execution remains informal. In practice, most project time is spent in delivery: implementing stories, reviewing changes, fixing findings, and verifying that code works in the real runtime. The user's previous Claude Code workflow already demonstrated that agent-led delivery can work surprisingly well, often clearing complex stories in fewer than three iterations. But that workflow also had important limitations.

First, it created dependence on one primary harness and a narrower provider setup. Second, it did not fully exploit role-based model selection, where a cheaper model can absorb the bulk of implementation tokens while stronger models focus on review and quality control. Third, it did not yet embed a well-designed TDD discipline into the execution loop. That leaves quality on the table, especially for stories where tests may pass while runtime behavior still fails. Fourth, long conversational runs create a context-management problem: as execution stretches across multiple phases and iterations, agents accumulate noisy history, drift from the original story, and risk hitting compaction at exactly the wrong moment.

The status quo is therefore a mismatch: BMAD provides the artifacts and process vocabulary, Pi provides the extensibility, but the exact story-centric, multi-model, fresh-context, TDD-first execution workflow the user needs still has to be designed and packaged. Without that layer, every project risks recreating the same orchestration logic manually.

## The Solution

`mypi-config` will provide an opinionated, reusable Pi workflow starter optimized around BMAD stories as the primary unit of work. The first version will focus on a single high-value path: take a story file as input, run a structured delivery loop across specialized agent roles, and stop only when bounded quality gates are met or a maximum iteration limit is reached.

The intended MVP workflow is a TDD-first story pipeline, likely in the shape of: test authoring or test-first setup, implementation to green, refactor, and two final review passes using stronger review models. Each phase should be launched as a fresh agent run with only the context it actually needs: the current story, relevant BMAD artifacts, and the outputs of prior steps distilled into clean handoff material. The exact internal sequencing remains a design question, but the product brief assumes the workflow will enforce the following outcomes for a completed story:

- tests are added or updated before implementation is considered complete
- the targeted test suite passes
- linting passes cleanly
- runtime or functional verification is performed through Playwright or an equivalent mechanism
- two final review passes are completed with no blocking findings
- iteration count is capped so unresolved stories are escalated back to the human

The output is not a hosted product or broad automation platform. It is a portable execution layer the user can bring into future repositories with minimal setup, likely through a simple copy/bootstrap mechanism tailored to personal use.

## What Makes This Different

This project is differentiated less by novel AI primitives than by the discipline of its execution model.

First, it is explicitly **story-centric**. Work begins from BMAD story artifacts rather than from vague prompts, which preserves context, scope, and handoff quality.

Second, it is **multi-model by design**. Implementation, review, and verification are treated as different jobs that deserve different models, enabling a better cost/quality tradeoff and reducing provider lock-in.

Third, it is **fresh-context by design**. Each agent should begin from a clean, focused starting point built from the BMAD story and supporting artifacts, not from a bloated shared conversation. That improves reliability, reduces compaction risk, and makes handoffs more deterministic.

Fourth, it treats **TDD as a first-class workflow constraint**, not an optional coding style. The ambition is to make tests, green-state delivery, refactoring, and runtime verification integral to the loop.

Fifth, it is **opinionated and reusable**. Instead of building a general-purpose framework for all teams and all project types, it is intentionally optimized for one proven working style, then packaged so it can be reused across future projects with almost no friction.

## Who This Serves

### Primary User
A single advanced solo builder who works on substantial software projects, uses BMAD artifacts to structure planning and delivery, and wants highly capable coding agents to collaborate through disciplined workflows rather than ad hoc prompting.

This user values:
- predictable handoffs between specialized agents
- stronger code quality through structured review and testing
- cost control through role-based model selection
- portability across projects
- reduced dependence on any single AI provider or coding harness

### Secondary Audience
Open-source observers or other Pi/BMAD power users may reuse the repo, but broad general-purpose adoption is not a first-version goal.

## Success Criteria

The MVP succeeds if it consistently produces a trustworthy handoff-driven delivery loop for BMAD stories.

Key success signals:

- A story file can be used as the canonical input to launch the workflow.
- The workflow can orchestrate multiple agent roles with different models assigned to different stages.
- Each major workflow step starts from a fresh, bounded context assembled from the story and supporting artifacts rather than from a long-running shared thread.
- The workflow completes handoffs with minimal human intervention in normal cases.
- Completed stories meet quality gates: tests updated or created, targeted tests green, linter clean, runtime verification completed, and two final reviews with no blocking findings.
- Complex stories frequently complete in three or fewer iterations, matching or improving on the user's previous Claude Code baseline.
- The setup can be reused in a new project through a simple install/bootstrap action rather than manual reconfiguration.

## Scope

### In Scope for MVP
- An opinionated repository scaffold for Pi + BMAD execution
- Reusable setup that can be brought into another project easily
- BMAD story files as the primary workflow input
- Multi-model orchestration across delivery stages
- Fresh-context handoffs between stages, grounded in BMAD story artifacts and distilled step outputs
- TDD-first workflow design as part of the initial MVP
- Final review loop with two review passes and bounded iteration count
- Runtime verification using Playwright or equivalent tooling

### Explicitly Out of Scope for MVP
- Generic support for every possible development style
- Informal ad hoc coding tasks beyond normal Pi usage
- Production bugfix workflows driven from GitHub issues or equivalent systems
- Broader non-story workflow families until real usage proves the need
- Advanced productization for teams, multi-user collaboration, or polished onboarding UX
- A fully generalized installation wizard unless later needed for convenience

## Vision

If this succeeds, `mypi-config` becomes the user's default execution substrate for future projects: a drop-in Pi/BMAD operating model where story artifacts, specialized agents, tests-first development, and runtime validation work together as a coherent system. Instead of rebuilding process discipline project by project, the user carries a known-good delivery engine forward.

Over a longer horizon, the project could evolve from a personal starter into a sharper open-source reference for how Pi can support serious, story-driven agentic development. That would include deeper TDD research, clearer workflow state machines, richer model-routing strategies, stronger verification patterns, and more formal packaging. But the first victory is simpler and more valuable: prove that a portable Pi-based workflow can deliver better quality than the current baseline without sacrificing speed or control.

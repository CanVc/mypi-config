# Design Notes — Agentic TDD / TDAD / ATDD Story Workflow for BMAD/Pi

**Date:** 2026-04-12  
**Status:** Research / design notes for future implementation  
**Purpose:** Capture the current design discussion around a story-by-story agentic TDD workflow for BMAD/Pi, without modifying existing BMAD base workflows.

---

## 1. Context and framing

The working context is:

- development proceeds **story by story**,
- each story is **human-validated before continuing**,
- quality matters more than raw speed,
- but the solution must **avoid becoming an usine à gaz**,
- and the existing **BMAD base workflows should remain untouched**.

This leads to a core architectural principle:

> **Do not modify BMAD base workflows. Fork and extend them with new workflows when TDD/TDAD/ATDD discipline is desired.**

This preserves:

- compatibility with standard BMAD,
- optional non-TDD execution paths,
- easier comparison between baseline BMAD and new workflows,
- lower risk of regressions in existing `create-story`, `dev-story`, and `code-review` behavior.

---

## 2. Main design conclusion

The preferred direction is not “pure TDD everywhere”, nor “full TDAD research stack everywhere”, nor heavyweight ATDD.

The most promising direction is a **graduated workflow family**, selected per story.

### Recommended working model

- **ATDD-lite** to clarify behavior when needed
- **TDD** to implement incrementally
- **TDAD-lite** to secure regression-sensitive work

Short form:

> **ATDD thinks, TDD builds, TDAD secures.**

---

## 3. Story profile approach

A single universal story workflow is not ideal. Stories should be created using different levels of rigor depending on their nature.

### 3.1 Proposed story profiles

#### A. `tdd-lite`
Use when:
- local technical change,
- low ambiguity,
- low regression risk,
- obvious testing strategy.

Characteristics:
- lightweight,
- fast,
- still test-first,
- minimal extra structure.

#### B. `tdad-lite`
Use when:
- several files or layers are touched,
- blast radius is higher,
- regression risk is non-trivial,
- impacted tests are not obvious.

Characteristics:
- stronger validation targeting,
- explicit test targets,
- regression watchouts,
- more disciplined batching.

#### C. `atdd-lite` / `agentic-atdd`
Use when:
- user-visible behavior is central,
- UX or business rules are ambiguous,
- acceptance must be clarified before coding,
- feature is AI-facing or behaviorally subtle.

Characteristics:
- examples first,
- stronger scenario specification,
- runtime validation if needed,
- possible evaluation criteria for probabilistic outputs.

---

## 4. Meta-skill concept

A strong idea emerged: use a **meta-skill** to route story creation.

### Proposed meta-skill behavior

A future `bmad-create-story-smart` workflow could:

1. ask a short questionnaire,
2. analyze the nature of the story,
3. recommend a profile (`tdd-lite`, `tdad-lite`, `atdd-lite`),
4. generate the story with the right amount of structure and dependencies.

### Why this is a good fit for BMAD

This matches the collaborative BMAD spirit:
- human + LLM decision support,
- adaptive rigor,
- explicit reasoning before artifact generation,
- no dogmatic one-size-fits-all process.

---

## 5. Standard BMAD create-story assessment

The existing BMAD `bmad-create-story` workflow is already strong as a **context-rich story generator**, but it is **not explicitly TDD-lite oriented**.

### What it already does well

- creates a strong implementation context,
- pulls architecture constraints,
- incorporates previous story learnings,
- tries to prevent common LLM mistakes,
- produces a dev-ready story artifact.

### What it lacks for TDD-lite / TDAD-lite / ATDD-lite

It does not explicitly structure:

- acceptance examples,
- first red test selection,
- test strategy,
- validation commands,
- test targets,
- batch-level testing progression.

### Conclusion

The BMAD base workflow is a **good foundation**, but should not be modified directly.

Instead:

> Create new workflows based on it, preserving the originals.

---

## 6. Important principle: preserve BMAD base workflows

### Decision

Do **not** change the base files for:
- `bmad-create-story`
- `bmad-dev-story`
- `bmad-code-review`

### Instead

Create new workflows such as:
- `bmad-create-story-smart`
- `bmad-create-story-tdd-lite`
- `bmad-create-story-tdad`
- `bmad-create-story-atdd`
- `bmad-dev-story-tdd`
- `bmad-code-review-tdd`

This preserves optionality:
- standard BMAD remains available,
- TDD workflows remain optional,
- experiments remain reversible.

---

## 7. What is “the best first red test”?

A concise definition was established.

> **The best first red test is the smallest test that proves the central behavior of the story, fails for the right reason, and does not require excessive setup.**

### Good first red test qualities

It should be:
- behavior-oriented,
- deterministic,
- easy to understand,
- narrow in scope,
- cheap to make pass,
- structurally useful,
- failing for the correct reason.

### Bad first red test qualities

Avoid tests that are:
- too broad,
- too E2E too early,
- checking many things at once,
- heavily setup-dependent,
- failing for incidental reasons,
- implementation-detail focused.

---

## 8. Separate test agent and dev agent?

### Main conclusion

Yes: **role separation is desirable**.

More precisely:

> The minimum important separation is not necessarily different models, but different roles and different contexts.

### Why separate?

If the same agent/session writes tests and implements immediately, it may:
- unconsciously design tests around the implementation it already imagines,
- create easy-to-satisfy tests,
- blur the distinction between specification and solution.

### Recommended split

- **Test role**: defines plan, priorities, and current red batch
- **Dev role**: implements against existing tests
- **Validation role(s)**: audit quality and route next action through orchestrator

---

## 9. Should the test agent write all tests from the start?

### Conclusion

Not all detailed tests at once.

Instead:

> **Have a global prioritized test plan from the start, but execute and author tests incrementally in batches.**

### Recommended compromise

The test side should produce:

1. a **global test strategy**,
2. a **priority order**,
3. the **current batch of tests** to write and run now.

This avoids both extremes:
- under-specification,
- and over-specification too early.

---

## 10. Core loop: plan global, execute incrementally

The preferred mechanics are:

> **global plan, incremental execution**

A likely story-level loop is:

1. story ready,
2. test planning,
3. red batch authoring,
4. red validation gate,
5. green implementation,
6. green validation gate,
7. orchestrator decides next action,
8. repeat until final review.

This is more precise than a simplistic “test > dev > review” loop.

---

## 11. Orchestrator role vs validator role

A key architectural decision emerged.

### Conclusion

> **Validators advise; the orchestrator decides which agent to run next.**

### Why this is preferable

Otherwise the validator becomes too many things at once:
- auditor,
- router,
- scheduler,
- workflow controller.

### Recommended distribution

#### Test agent says
- batch ready / not ready,
- red obtained / not obtained,
- test quality issues.

#### Dev agent says
- implementation complete / blocked,
- technical blockers,
- uncertainty requiring clarification.

#### Validator says
- accepted / rejected,
- findings,
- type of problem,
- recommended next direction.

#### Orchestrator decides
- rerun test,
- rerun dev,
- rerun validation,
- escalate to human,
- proceed to next batch,
- proceed to final review.

---

## 12. Single-file vs multi-file artifact strategy

A discussion explored whether to split the workflow into multiple files or keep a single enriched story file.

### Conclusion for V1

A **single enriched story file** is a strong and viable option.

### Why a single file is attractive

- better fit with current BMAD story usage,
- simpler for a solo developer,
- less navigation overhead,
- less synchronization risk,
- easier human review,
- easier canonical state tracking.

### Risks

- file may grow large on complex stories,
- stricter section discipline is required,
- parallel editing would be harder (but this is not a major issue in the current sequential workflow).

### Recommended V1 choice

> Prefer a **single canonical story file**, enriched with batch, validation, and orchestration sections.

---

## 13. Proposed single-file structure

Without changing BMAD base files, a future TDD-oriented story artifact could conceptually include:

### Existing useful sections
- Story
- Acceptance Criteria
- Tasks / Subtasks
- Dev Notes
- Dev Agent Record
- File List

### Additional proposed sections
- Story Profile
- Why This Profile
- Examples
- Test Plan
- Batch Board
- Current Batch
- Validation Findings
- Batch History
- Orchestrator Decision Log
- Change Log

### Key idea for test planning
A `Test Plan` section could itself use checkboxes and a visible batch list, similar in spirit to the existing story todo list.

The visible batch list should ideally show only:
- completed batches,
- current batch,
- next actionable batch.

---

## 14. Can findings live in the same file?

Yes.

The same reasoning used today for review findings written into the story file can be extended to:
- red validation findings,
- green validation findings,
- batch-level findings,
- orchestrator notes.

This supports a coherent single-document workflow.

---

## 15. Is it legitimate to launch dev if the tests are bad?

### Core answer

> **No, not if they are clearly bad.**

But there is an important distinction.

### Case A — tests are plausible but not final
This is acceptable.
If tests:
- compile,
- fail for the expected reason,
- align with the story,
- are appropriately scoped for the current batch,
then dev can proceed.

### Case B — tests are clearly bad
Dev should not start if tests:
- fail for the wrong reason,
- contradict the acceptance criteria,
- target internals rather than behavior,
- are incoherent or too broad,
- do not meaningfully guide implementation.

### Case C — tests are incomplete but good enough for current batch
This is legitimate in an incremental workflow.
The batch only needs to be sufficiently valid to guide the current increment, not represent final story coverage.

---

## 16. Consequence: two distinct gates are needed

This led to a key workflow conclusion.

### Gate A — Red Gate
Purpose:
- validate that the current red batch is legitimate before dev starts.

Checks include:
- right reason for failure,
- acceptable alignment with story/AC/examples,
- manageable batch size,
- sufficient clarity to guide dev.

### Gate B — Green Validation
Purpose:
- validate that implementation genuinely satisfies the batch,
- detect cheating or overfitting,
- detect immediate regressions,
- determine whether the batch is really closed.

### Conclusion

> A post-green validator alone is not enough. A **red gate** is also required.

---

## 17. One validator with two modes, or two validators?

This question was discussed explicitly.

### Strong design question
Is red validation sufficiently different from green validation to justify separate roles?

### Working conclusion
It likely does.

The difference is not superficial.
The two roles are validating different kinds of truth.

#### Red-validator validates
- quality of the tests,
- legitimacy of the batch,
- readiness for handoff to dev,
- alignment between spec and red tests.

#### Green-validator validates
- quality of the implementation response,
- closure of the batch,
- absence of cheating,
- acceptable regression profile,
- whether to move forward or reroute.

---

## 18. System prompts: should red and green validators differ?

### Conclusion

> **Yes, likely yes.**

Even if a common base exists, the specialization should differ.

### Red-validator prompt should emphasize
- test legitimacy,
- acceptance alignment,
- batch focus,
- quality of failure,
- anti-pattern detection in tests,
- readiness for dev handoff.

### Green-validator prompt should emphasize
- actual behavior achieved,
- no cheating / no test hacking,
- regression resistance,
- scope discipline,
- batch closure,
- next-step diagnosis.

So the answer to the first key question is:

> **Yes, distinct system prompts are probably needed.**

---

## 19. Models: should red and green validators use different models?

### Conclusion

> **Potentially yes, but not necessarily in V1.**

### Why they might differ
Red validation is often more focused on:
- spec-to-test alignment,
- clarity of test design,
- prioritization,
- reason-of-failure checks.

Green validation often requires more:
- cross-correlation between story, tests, code, diff, and results,
- stronger adversarial review of the implementation,
- regression judgment.

This means model routing may eventually differ.

### Pragmatic recommendation
For V1:
- use **two roles**,
- use **two prompts**,
- but start with **one model** if that simplifies implementation.

For V2:
- benchmark results,
- then decide whether red can use a cheaper/faster model,
- and green should keep a stronger review-oriented model.

So the answer to the second key question is:

> **Yes, different models may be useful, but this should be earned through measurement, not assumed.**

---

## 20. Recommended V1 design stance

### Recommended immediately
- keep BMAD base workflows unchanged,
- design new TDD-oriented workflows beside them,
- use story profiles,
- adopt global-plan + incremental-batch mechanics,
- keep a single enriched story file as canonical artifact,
- introduce both a red gate and a green validation gate,
- let the orchestrator decide transitions,
- define red-validator and green-validator as distinct roles,
- use different prompts for red and green,
- use the same model initially unless evidence suggests otherwise.

---

## 21. Open implementation direction

A future implementation should likely explore:

1. a **meta-skill** for profile selection,
2. one or more **story creation workflows** derived from BMAD base create-story,
3. a **TDD-oriented dev workflow** derived from BMAD dev-story,
4. explicit **red-validator** and **green-validator** roles,
5. an **orchestrator** that owns state transitions,
6. a **single enriched story file** that can carry:
   - plan,
   - batches,
   - findings,
   - state,
   - review history.

---

## 22. Final synthesis

The central idea from this discussion is:

> Build a **graduated, story-by-story, orchestrated agentic TDD workflow** for BMAD/Pi, while preserving BMAD base workflows unchanged.

The most promising design characteristics are:

- human validation between stories,
- profile-based rigor,
- separate test and dev roles,
- incremental batches,
- explicit red and green gates,
- orchestrator-controlled transitions,
- single-file canonical state where practical,
- specialized validator prompts,
- model specialization only if benchmarking justifies it.

This gives a path toward strong quality discipline without prematurely building an overly heavy process.

---

## 23. Intended use of this document

This markdown file is intended as:
- a future implementation reference,
- a design decision log,
- a discussion baseline before creating new BMAD/Pi workflows,
- a reminder that the first implementation goal is not maximal sophistication, but **the best quality/complexity ratio for a solo developer**.

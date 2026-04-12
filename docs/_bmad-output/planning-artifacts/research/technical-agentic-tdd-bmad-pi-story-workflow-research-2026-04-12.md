---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - 'docs/research/tdd-initiative'
  - 'docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md'
workflowType: 'research'
lastStep: 6
research_type: 'technical'
research_topic: 'Agentic TDD for BMAD/Pi story workflow'
research_goals: 'Conduct exhaustive industry research on agentic TDD practices, then derive a concrete TDD cycle and end-to-end story workflow for BMAD driven by Pi in a multi-model setup.'
user_name: 'Cvc'
date: '2026-04-12'
web_research_enabled: true
source_verification: true
---

# Research Report: technical

**Date:** 2026-04-12
**Author:** Cvc
**Research Type:** technical

---

## Research Overview

This research examined current industry practice around agentic TDD and then translated the strongest patterns into a workflow that fits a **BMAD spec-first** and **Pi-driven** environment. The source base combined live vendor documentation, benchmark and research papers, engineering handbooks, and tool documentation current on 2026-04-12. Because BMAD and Pi are comparatively niche, the analysis intentionally looked outward to the broader coding-agent ecosystem and then pulled the results back into your specific operating model.

The most important finding is that the industry is converging on **verification-first, artifact-centric, multi-stage workflows** rather than long, chat-centric coding sessions. The strongest patterns repeatedly emphasize: explicit failing tests, fresh-context handoffs, repo-native tooling, runtime verification, bounded repair loops, and stronger final review gates. The best current examples are not “just tell the model to do TDD”, but structured loops such as **red/green TDD**, **planner/generator/healer**, and **explore/revise/debug/generate-tests**.

For your project, the recommended destination is a **story-centered state machine**: BMAD story in, execution brief out, failing tests first, implementation to green, refactor and broaden validation, runtime verification, dual model review, bounded repair, then human merge or escalation. Pi is a strong fit because it is intentionally customizable through skills, extensions, SDK control, sessions, and custom model configuration; that makes it well-suited to implementing a workflow that is more opinionated than Pi’s default behavior. See the **Executive Summary** and **Section 8** for the recommended final TDD cycle and story workflow.

---

# From Story to Safe Merge: Comprehensive Technical Research on Agentic TDD for a BMAD/Pi Story Workflow

## Executive Summary

Agentic TDD is emerging as a **workflow design problem**, not merely a prompting trick. Across current documentation and research, the strongest results come from systems that give the agent a way to verify its work, constrain it with repo-native tools, decompose work into smaller roles, and preserve evidence at every gate. Anthropic’s Claude Code best practices lead with verification, planning before coding, aggressive context management, and subagent-style decomposition. Simon Willison and Tweag both frame red/green TDD as especially effective with coding agents. The TDFlow paper formalizes the same instinct in research form by decomposing repository-scale software engineering into tightly constrained sub-agents for exploration, revision, debugging, and test generation. Playwright’s built-in planner/generator/healer agents show that even runtime verification is becoming explicitly agent-oriented.

The practical implication is clear: **“Do TDD” is too vague for agents.** What works is a sharper loop: identify acceptance behavior, map it to exact tests, create or update tests so they fail for the right reason, implement only until those targeted tests pass, broaden validation, then perform runtime verification and multi-perspective review. In other words, the industry is shifting from procedural TDD instructions to **test-targeted, evidence-rich delivery loops**. Generated tests and just-in-time test generation are becoming more important, but they are not replacing authored acceptance-focused tests yet; rather, they supplement them.

For your environment, the recommended operating model is a **BMAD story-centric, Pi-orchestrated, multi-model workflow** with fresh-context handoffs between every phase. BMAD should remain the canonical source of scope and acceptance intent. Pi should act as the orchestration shell, initially via skills and later, if desired, via an extension or SDK-driven state machine. Stronger models should be reserved for planning, final review, and difficult debugging, while cheaper or faster models perform most implementation work. Local Ollama models should remain restricted to low-risk, bounded tasks until they earn trust in your benchmarks. The result is a workflow designed for disciplined autonomy, not “vibe coding”: story in, measurable proof out.

**Key Technical Findings:**

- The industry is converging on **verification-heavy, CLI-first agent loops** rather than free-form chat-centric coding.
- The strongest patterns are **fresh-context handoffs**, **targeted failing tests**, **repo-native execution**, and **bounded repair loops**.
- Runtime validation is now a first-class concern; Playwright’s agent stack is a strong signal that **E2E verification must sit inside the delivery loop**, not after it.
- Structured decomposition matters: planner/generator/healer, subagents, and patch-debug-test loops consistently outperform monolithic sessions in reliability and auditability.
- Git, logs, traces, CI artifacts, and markdown handoffs matter more than a dedicated workflow database in early implementations.
- Pi is well-positioned to implement this because it supports **skills, extensions, SDK control, sessions, model routing, and custom providers**, while BMAD already provides the story artifacts that agentic workflows often lack.

**Technical Recommendations:**

- Make the **BMAD story file the canonical input artifact** for every implementation run.
- Enforce a **Red → Green → Refactor → Runtime Verify → Dual Review** cycle with explicit evidence at each gate.
- Use **fresh Pi sessions or sharply bounded prompts per stage** instead of one long conversation.
- Route models by role: strong models for planning/review, cost-efficient models for implementation, local models only for bounded support work.
- Cap repair loops at **2–3 iterations** before escalation to the human.
- Persist work products as **story-scoped markdown, logs, traces, test outputs, and review findings** under implementation artifacts.

## Table of Contents

1. Technical Research Introduction and Methodology
2. Agentic TDD Technical Landscape and Architecture Analysis
3. Implementation Approaches and Best Practices
4. Technology Stack Evolution and Current Trends
5. Integration and Interoperability Patterns
6. Performance and Scalability Analysis
7. Security and Compliance Considerations
8. Strategic Technical Recommendations
9. Implementation Roadmap and Risk Assessment
10. Future Technical Outlook and Innovation Opportunities
11. Technical Research Methodology and Source Verification
12. Technical Appendices and Reference Materials
13. Technical Research Conclusion

## 1. Technical Research Introduction and Methodology

### Technical Research Significance

Agentic coding has moved from novelty to serious engineering practice, but the surrounding operating model is still unstable. Most public attention is currently concentrated around Claude Code and adjacent tools, yet the underlying patterns are broader than any one harness. At the same time, your product brief makes the project goal unusually concrete: not a generic AI coding platform, but a **portable, story-driven delivery engine** that turns BMAD artifacts into disciplined implementation loops with multi-model routing, fresh context, and TDD-first execution. That combination makes this research strategically important: it is not just about whether TDD still matters with agents, but about how to redesign the whole delivery loop so that TDD becomes enforceable, auditable, and reusable.

The significance of the research is therefore twofold. First, it identifies what is genuinely working in the broader industry around coding agents and test-driven loops. Second, it filters those findings into a method that is implementable in **BMAD + Pi** rather than in the mainstream Claude Code default environment. That adaptation step matters because Pi’s philosophy is explicitly to adapt the harness to your workflow, not the other way around.

_Source: `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`; https://code.claude.com/docs/en/best-practices ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`._

### Technical Research Methodology

The research combined five source classes:

- **Primary vendor documentation** for live product capabilities and intended workflows
- **Research and benchmark papers** for structured evidence and explicit methodology
- **Engineering handbooks and technical guides** for cross-vendor workflow patterns
- **Testing framework documentation** for current verification capabilities
- **Local project artifacts and Pi documentation** for adaptation to the BMAD/Pi environment

The analysis was organized around the following questions:

1. What does industry practice say about agentic TDD right now?
2. Which patterns appear repeatedly across independent sources?
3. Which of those patterns are actually transferable into a BMAD/Pi environment?
4. What final story workflow best satisfies the goals in the project brief?

The resulting document deliberately distinguishes among:

- **high-confidence cross-source patterns**
- **promising but still emerging practices**
- **adaptation decisions specific to your workflow**

_Source: https://code.claude.com/docs/en/best-practices ; https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://arxiv.org/html/2510.23761v1 ; https://playwright.dev/docs/test-agents ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/._

### Technical Research Goals and Objectives

**Original Technical Goals:** Conduct exhaustive industry research on agentic TDD practices, then derive a concrete TDD cycle and end-to-end story workflow for BMAD driven by Pi in a multi-model setup.

**Achieved Technical Objectives:**

- Identified the strongest current architecture patterns for agentic TDD and verification-heavy development
- Mapped the most relevant tooling ecosystems for unit, integration, runtime, CI, and review workflows
- Determined which industry practices transfer cleanly into BMAD/Pi and which do not
- Produced a recommended BMAD/Pi story workflow with explicit phases, gates, artifacts, and model-routing guidance
- Captured major risks, success metrics, and adoption phases for implementation

_Source: Entire research corpus listed in Section 11 plus local inputs `docs/research/tdd-initiative` and `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 2. Agentic TDD Technical Landscape and Architecture Analysis

### Current Technical Architecture Patterns

The research points to five recurring architecture patterns.

**1. Verification-first, not prompt-first.** Claude Code’s current best-practices documentation explicitly says to “give Claude a way to verify its work”, and places verification ahead of generic prompt cleverness. This is the most important architectural shift in the field. Mature workflows assume the agent must execute tests, lint, traces, or scripts to prove correctness rather than merely describe it.

**2. Role decomposition beats monolithic sessions.** The Playwright Test Agents model splits work into planner, generator, and healer. TDFlow splits repository-scale repair into exploration, patch revision, debugging, and test generation. Claude Code adds custom subagents and hooks. Across sources, the message is the same: reliability improves when work is broken into narrower stages with different instructions and, often, different models.

**3. Fresh context is a first-class design constraint.** Claude Code advises aggressive context management and multiple sessions. Your product brief independently calls for fresh-context handoffs between phases. This is a point of strong convergence: the best architecture does not let a single thread accumulate unbounded noise.

**4. Artifact-centric control planes outperform memory-centric ones.** Aider foregrounds git, diffability, lint/test loops, and repository mapping. SWE-bench emphasizes reproducible Dockerized evaluation environments. In other words, the control plane is not a hidden agent memory; it is a set of observable artifacts: story files, diffs, test commands, logs, traces, review findings, and CI outputs.

**5. Bounded autonomy is preferable to unrestricted autonomy.** Claude Code exposes permission modes, hooks, and GitHub Actions controls; Playwright’s agent loop is explicitly staged; TDFlow runs constrained sub-agents. The best systems do not remove control. They automate inside well-defined boundaries.

_Source: https://code.claude.com/docs/en/best-practices ; https://docs.anthropic.com/en/docs/claude-code/sub-agents ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://playwright.dev/docs/test-agents ; https://arxiv.org/html/2510.23761v1 ; https://aider.chat/ ; https://www.swebench.com/SWE-bench/guides/docker_setup/._

### System Design Principles and Best Practices

From those patterns, the clearest architectural principles for your workflow are:

- **One canonical work unit:** the BMAD story file
- **One canonical success mechanism:** executable proof, not verbal confidence
- **One stage, one purpose:** each run has a narrow objective and minimal context
- **One evidence trail:** every phase leaves artifacts a later phase can consume
- **One escalation rule:** if the loop cannot converge, stop and escalate instead of thrashing

This implies a story workflow that behaves more like a **state machine** than a conversation. Each transition should be explicit:

- story accepted for implementation
- execution brief produced
- tests fail for the intended reason
- targeted implementation goes green
- broader validation passes
- runtime evidence collected
- review findings cleared
- human merge decision made

That architecture is more rigid than generic interactive coding, but it is exactly what makes agentic TDD workable.

Several practical enforcement mechanisms recur in Claude-style harnesses and are transferable to Pi with little conceptual change:

- a **project-level workflow rules file** that encodes TDD constraints,
- an explicit **red checkpoint** before green on non-trivial work,
- **post-edit verification hooks** that immediately run targeted tests or lint after file changes,
- **phase-isolated agents or fresh sessions** so the model does not silently design tests around an implementation plan it is already carrying in context.

These should be treated as harness patterns rather than vendor-specific tricks. In Pi, they map naturally to skills, prompt templates, staged sessions or branches, artifact checkpoints, and later, extension or SDK logic that can enforce pre/post-tool behavior.

_Source: https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://code.claude.com/docs/en/best-practices ; https://docs.anthropic.com/en/docs/claude-code/hooks ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `docs/research/tdd-opus-analysis.md`._

### Architectural Quality Attributes

For this domain, the decisive quality attributes are not only performance and extensibility, but also:

- **Determinism:** can the same stage be rerun with the same inputs?
- **Auditability:** can a human inspect what happened and why?
- **Replaceability:** can the model or tool be swapped without redesigning the process?
- **Cost control:** can premium models be used only where they matter?
- **Regression resistance:** can the loop prove it did not damage nearby behavior?

The BMAD/Pi combination aligns well with these attributes. BMAD contributes structured planning artifacts; Pi contributes a harness that can be adapted via skills, SDK usage, custom tools, sessions, and custom model definitions. Pi’s lack of hardcoded subagents is not a weakness here; it is precisely what allows you to impose your own architecture.

_Source: `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 3. Implementation Approaches and Best Practices

### Current Implementation Methodologies

The industry is currently using several distinct implementation patterns, each useful for a different slice of the story lifecycle.

| Pattern | What it is | Strength | Weakness | Relevance to BMAD/Pi |
|---|---|---|---|---|
| Red/Green/Refactor | Write failing tests, implement to green, then clean up | Strong behavioral discipline, simple mental model | Easy for agents to fake unless failure evidence is explicit | Core unit/integration loop |
| Targeted test-resolution loop | Treat work as making known failing tests pass without breaking regression tests | Excellent for debugging and repair | Can miss missing-behavior cases if no test is written first | Core repair loop |
| Planner/Generator/Healer | Split runtime/E2E work into plan, test generation, and healing | Strong fit for UI/runtime validation | Can overproduce fragile tests if plan quality is poor | Strong E2E pattern |
| JiT regression testing | Generate catching tests just before landing changes | Promising for high-velocity change environments | Still emerging and can create noise | Future enhancement |
| Auto lint/test fix loop | Run lint/tests after every change and let the agent repair | Fast feedback and high practical value | Not sufficient alone without acceptance intent | Baseline hygiene loop |

In practical terms, the best workflow for your project is a **hybrid**:

- use classic red/green/refactor for unit and integration behavior,
- use targeted test-resolution for repairs,
- use planner/generator/healer ideas for runtime and browser validation,
- treat JiT-generated tests as a future supplement rather than the MVP core.

One research result deserves to be made explicit because it sharpens the whole workflow design. The TDAD line of work argues that **procedural TDD instructions alone can worsen outcomes** if they consume context but do not improve test targeting. In the experiment summarized in the Opus synthesis, a vanilla baseline produced a 6.08% regression-test failure rate, procedural TDD prompting alone worsened that to 9.94%, while graph-informed targeted verification reduced it to 1.82%. The transferable lesson is that, for many models and especially smaller ones, giving the agent the **right impacted tests to run** beats giving it a longer lecture about TDD. For BMAD/Pi, this supports eventually generating a story-scoped `test-targets.txt` or equivalent impacted-test map whenever repository structure makes that feasible.

_Source: https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://arxiv.org/html/2510.23761v1 ; https://playwright.dev/docs/test-agents ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://aider.chat/ ; `docs/research/tdd-opus-analysis.md`._

### Implementation Framework and Tooling

The tooling picture is unusually clear:

- **Aider** demonstrates the practical value of automatic lint/test execution after each change, with git-native diffs and broad language support.
- **Pytest** remains a strong back-end foundation because fixtures, parametrization, plugins, reruns, and explicit failure handling map naturally to iterative repair loops.
- **Vitest** is increasingly agent-friendly, explicitly surfacing “Writing Tests with AI”, browser mode, coverage, and parallelism in its docs.
- **Playwright** now provides dedicated test agents that cover planning, generation, and self-healing for browser flows.
- **GitHub Actions** provides the standard automation backbone for artifacts, caching, concurrency, and optional self-hosted runners.
- **OpenHands** reinforces the importance of reviewable PRs and customizable workflows with testing and validation in the loop.

The engineering lesson is that the agentic workflow should not invent exotic verification tooling. It should compose the best existing repo-native tools under a stricter orchestration layer.

_Source: https://aider.chat/ ; https://docs.pytest.org/en/stable/contents.html ; https://vitest.dev/guide/ ; https://playwright.dev/docs/test-agents ; https://docs.github.com/en/actions ; https://openhands.dev/._

### Concrete Harness Enforcement Patterns

Several concrete patterns appear repeatedly in successful Claude-style TDD setups and are worth carrying over into a Pi adaptation.

- Keep **repo-native workflow rules** in a project instruction file so the harness repeatedly restates the same constraints: tests first, confirm failure, implement minimally, do not rewrite tests to fake green.
- For non-trivial stories, create a **checkpoint of the red state** before implementation. In Claude Code this is often a git commit of the failing tests; in Pi it can be a commit, branch checkpoint, or explicit red-proof artifact plus session boundary.
- Use **post-edit verification hooks or commands** to run a narrow test or lint command immediately after file modifications. This catches drift early and reduces the chance that the agent keeps building on a broken local state.
- Prefer **phase isolation**: separate red, green, and refactor work into fresh sessions, branches, or tightly bounded role prompts so the model does not unconsciously design the tests around implementation ideas already in context.

These practices are operationally modest but strategically important. They are how a workflow stops being “please do TDD” and becomes a system that makes TDD harder to violate accidentally.

_Source: https://docs.anthropic.com/en/docs/claude-code/hooks ; https://code.claude.com/docs/en/best-practices ; https://aider.chat/ ; `docs/research/tdd-opus-analysis.md`._

### Testing Patterns for Non-Deterministic AI Behavior

The main report has focused on coding-agent workflows, but some stories will implement or modify **AI-facing product behavior** where outputs are intrinsically non-deterministic. In those cases, classic exact-match assertions are not enough. The more robust testing stack is layered:

1. **Deterministic foundations.** Mock or stub the LLM and test routing, parsing, retries, schema validation, guardrails, and orchestration logic deterministically.
2. **Record/replay.** Capture representative model interactions and replay them in CI to keep a reproducible regression layer.
3. **Stochastic evaluations.** Run the same scenario multiple times and evaluate success rate, score distribution, or variance thresholds rather than a single binary pass/fail.
4. **Qualitative or rubric-based grading.** Use model-based judges only after cheaper code-based checks, and calibrate them with occasional human review.

This implies a practical design rule for BMAD/Pi: use ordinary unit and integration TDD for deterministic product logic, but introduce **thresholded evaluation artifacts** when the acceptance criteria involve probabilistic model outputs. Frameworks such as DeepEval, Promptfoo, Langfuse, LangSmith, and Braintrust are relevant here not because they replace TDD, but because they extend it into domains where “same input, same exact output” is no longer realistic.

_Source: https://docs.pytest.org/en/stable/contents.html ; `docs/research/tdd-opus-analysis.md`._

### Practical E2E Tactics for Playwright-Based Agentic TDD

Playwright is already central to the runtime-verification story, but several tactical patterns deserve to be explicit.

- Use **specs-as-Markdown** as a bridge between human intent and executable browser tests. A simple markdown scenario file is often the cleanest precursor artifact for generated or assisted E2E tests.
- Prefer **accessibility-driven selectors** such as `getByRole()` and stable labels over CSS implementation details. This is both more robust for tests and more legible for agents.
- Avoid brittle synchronization patterns such as `waitForTimeout()` where a web-first assertion or explicit state condition would do.
- Keep test data deterministic and test cases isolated; generated browser tests become flaky quickly if state leaks between scenarios.
- Treat traces, screenshots, and videos as first-class evidence, not debugging leftovers.

The key point is that browser-runtime verification for agentic workflows is not merely “have some E2E tests”. It is a specification discipline with strong selector hygiene and artifact capture built in.

_Source: https://playwright.dev/docs/test-agents ; https://playwright.dev/docs/intro ; `docs/research/tdd-opus-analysis.md`._

### Common Agentic TDD Anti-Patterns

Several anti-patterns recur often enough to deserve named treatment in the workflow:

- **Test-after trap:** the agent writes implementation first and only adds tests afterward.
- **Kitchen-sink tests:** one test checks too many behaviors, making failure diagnosis and repair harder.
- **Mock-everything drift:** mocking so aggressively that the real behavioral risk disappears from the test surface.
- **Green-bar addiction:** hardcoding answers or overfitting to one test just to obtain a passing result.
- **Implementation-detail testing:** coupling tests to internals rather than observable behavior, which makes legitimate refactoring expensive.

These are useful as review lenses because they are more concrete than saying “the agent might cheat”. They give the human reviewer and the repair stage a sharper vocabulary for what went wrong.

_Source: `docs/research/tdd-opus-analysis.md`._

## 4. Technology Stack Evolution and Current Trends

### Current Technology Stack Landscape

The agentic TDD stack separates naturally into five planes.

**Control plane.** The workflow engine is typically terminal-first and implemented in ecosystems that are good at tool calling and automation, especially Node/TypeScript and Python. Pi fits this well through skills, extensions, and SDK control.

**Model plane.** Current practice favors multiple models rather than a single universal one. Premium models are used where failure is most expensive—planning, difficult debugging, and final review—while faster or cheaper models do the bulk of implementation and low-risk transformations.

**Verification plane.** The dominant stack is still repo-native: pytest or Vitest for fast inner loops, Playwright for browser/runtime proof, lint/format tools for hygiene, CI runners for reproducibility.

**State plane.** The system of record is usually git plus artifacts, not a database. Diffs, logs, traces, JUnit outputs, markdown handoffs, and cached CI artifacts matter more than a dedicated orchestrator DB in early versions.

**Environment plane.** Reproducible runners, Dockerized evaluation environments, and optional self-hosted runners matter for consistency, security, and speed.

For your environment, the mapping is direct:

- **BMAD** supplies the planning/specification plane.
- **Pi** supplies the control plane.
- **glm-5.1 / sonnet-4.6 / gpt-5.4 / opus-4.6** supply the model plane.
- **pytest / Vitest / Playwright / repo-native linting** supply the verification plane.
- **git + story-scoped artifacts** supply the state plane.

_Source: https://code.claude.com/docs/en/best-practices ; https://aider.chat/ ; https://openhands.dev/ ; https://playwright.dev/docs/intro ; https://docs.github.com/en/actions ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

### Technology Adoption Patterns

Several adoption trends now appear stable:

- **CLI-first agents are more mature than IDE-only flows** for serious automation.
- **MCP is becoming the tool-integration standard** for AI applications that need external systems.
- **Generated tests are rising**, but authored acceptance-driven tests still define the safest core loop.
- **Benchmark thinking is spreading**: teams increasingly reason in terms of reproducibility, regression resistance, and measurable workflow quality.
- **Local models are useful, but trust is tiered.** Current best practice is to restrict weak or low-context local models to bounded tasks unless benchmarked otherwise.

Pi’s custom model support is especially relevant here. It can route to OpenAI-compatible providers such as Ollama, while keeping the workflow architecture independent from any single vendor. That makes it a strong long-term control plane for your multi-model strategy.

_Source: https://modelcontextprotocol.io/introduction ; https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://www.swebench.com/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 5. Integration and Interoperability Patterns

### API Design Patterns

For agentic TDD workflows, the most important “API” is usually not GraphQL or REST inside the inner loop; it is the **tool boundary** between the orchestrator and the execution environment. MCP is now the clearest general-purpose standard in this space, describing itself as an open standard for connecting AI applications to external systems, tools, data sources, and workflows. Claude Code’s MCP documentation reinforces this by supporting local stdio servers, remote HTTP/SSE servers, dynamic tool updates, and separate local/project/user scopes.

For your workflow, this implies a practical rule:

- keep the core implementation loop **local and CLI-native** whenever possible,
- add MCP only for external systems that genuinely need it,
- scope each integration to the narrowest practical boundary.

That approach preserves determinism and keeps the story loop understandable.

_Source: https://modelcontextprotocol.io/introduction ; https://docs.anthropic.com/en/docs/claude-code/mcp ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Communication Protocols

The dominant protocols in practical agentic TDD are:

- **shell/stdout/stderr** for local repo work,
- **HTTP or SSE** for remote tool and MCP integration,
- **git and CI events** for inter-stage automation,
- **test runner outputs and traces** for machine-readable validation.

This is a good match for Pi, which is natively terminal-centered and can be embedded or extended through SDK and custom tools. In other words, the workflow does not need a bespoke orchestration protocol; it needs a clean contract around tool execution and artifact passing.

_Source: https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Data Formats and Standards

A practical interoperability stack for your workflow should be simple:

- **Markdown** for human-readable handoffs, execution briefs, test plans, review findings
- **JSON** for machine-readable gates, status payloads, or orchestration metadata
- **JUnit/coverage/traces/screenshots/videos** for verification evidence
- **git diffs and patch summaries** for change provenance

Markdown is especially attractive because BMAD stories are already artifact-centric and because markdown is easy for both humans and models to consume. JSON should be used only where automation clearly benefits.

_Source: https://docs.github.com/en/actions ; https://playwright.dev/docs/test-agents ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### System Interoperability Approaches

The workflow engine itself should favor **point-to-point integration** over heavyweight middleware. In a single-repo story workflow, API gateways, service meshes, or enterprise buses are usually overkill. The simplest effective architecture is:

1. story artifact in markdown,
2. repo-native tools via shell,
3. optional MCP for external systems,
4. CI runner for reproducibility,
5. git and artifact folders as the persistent audit trail.

That is more than enough for the MVP and probably enough for quite a long time after that.

_Source: https://modelcontextprotocol.io/introduction ; https://docs.github.com/en/actions ; https://aider.chat/ ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`._

### Microservices Integration Patterns

Microservices patterns matter mainly for the **product under test**, not the **workflow engine**. For the orchestration layer, a distributed microservice design would add complexity without obvious gain. A state-machine or pipeline design with explicit phase boundaries is the better fit. The workflow can still integrate with microservice systems under test by using their repo-native tests, local compose/dev environments, API tests, and browser checks as appropriate.

_Source: https://playwright.dev/docs/ci ; https://docs.github.com/en/actions ; https://arxiv.org/html/2510.23761v1 ._

### Event-Driven Integration

Event-driven integration is useful at the boundaries:

- hooks before or after tool execution,
- CI triggers on pushes or PRs,
- scheduled or background quality checks,
- notifications or status updates on story phase completion.

Claude Code’s hooks reference is instructive here because it shows how decision control and pre-tool gating can be formalized. Pi can implement analogous behavior through extensions, custom tools, or SDK-driven orchestration logic.

_Source: https://docs.anthropic.com/en/docs/claude-code/hooks ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Integration Security Patterns

Security patterns that matter most in this domain are:

- **least-privilege tool scopes**,
- **separate local/project/user integration scopes**,
- **explicit permission modes or hook-based controls**,
- **secret management outside prompts and markdown artifacts**,
- **optional self-hosted runners for sensitive codebases**.

The practical message is that integration power should grow only as verification and access control grow with it.

_Source: https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

## 6. Performance and Scalability Analysis

### Performance Characteristics and Optimization

The most important performance insight is that **inner-loop cost and latency are dominated by context size and test scope**. Large-model tokens are expensive; giant test suites are slow. The best mitigation is architectural, not cosmetic:

- use **fresh-context handoffs** to avoid bloated conversations,
- run **targeted tests** in the inner loop,
- broaden the test surface only after localized green states,
- reserve premium models for high-leverage phases.

This is consistent with Aider’s automatic lint/test pattern, Claude Code’s context-management advice, and benchmark-oriented infrastructures such as SWE-bench’s Dockerized evaluation. In practice, the cheapest good workflow is not the one with the weakest model; it is the one that minimizes unnecessary context and unnecessary verification scope.

_Source: https://aider.chat/ ; https://code.claude.com/docs/en/best-practices ; https://www.swebench.com/SWE-bench/guides/docker_setup/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Scalability Patterns and Approaches

The workflow should scale by **separating work**, not by lengthening sessions. The scalable pattern is:

- one stage, one session or one sharply bounded prompt
- optional fan-out for investigation or review
- artifact handoff between stages
- capped repair loops
- explicit checkpointing and branching

Pi’s session model, tree navigation, compaction, and model switching make this especially viable. You can treat each story phase as either a fresh session or a branchable checkpoint rather than trying to preserve everything in one conversation.

_Source: `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; https://code.claude.com/docs/en/best-practices ._

### Monitoring and Measurement

The workflow should measure more than pass/fail. Recommended metrics are:

- time to first failing test
- time to first green
- number of repair loops per story
- share of stories that reached runtime verification
- blocker findings per review pass
- cost per story by phase and by model
- human escalation rate
- escaped regressions after merge

These metrics matter because they let you calibrate model routing, test scope, and phase boundaries empirically instead of guessing.

_Source: https://www.swebench.com/ ; https://docs.github.com/en/actions ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 7. Security and Compliance Considerations

### Security Best Practices and Frameworks

Three security principles dominate the research:

1. **least privilege for tools and integrations**
2. **separate credentials from prompts and artifacts**
3. **make gates enforceable, not advisory**

Claude Code’s MCP scopes, hooks, permission controls, and GitHub Actions integration all reinforce this. Pi similarly allows credentials and model definitions to live outside prompt content, which is essential if the workflow becomes more automated.

_Source: https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.anthropic.com/en/docs/claude-code/github-actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`._

### Threat Landscape

The main risks in agentic TDD are not traditional application vulnerabilities alone. They include:

- **test hacking or false green states**
- **prompt injection via repo files, external docs, or tool outputs**
- **secret leakage through over-privileged shell or MCP tools**
- **review monoculture**, where the same model class misses the same flaw twice
- **unsafe autonomous changes**, especially from weaker or poorly scoped models

TDFlow’s concern with minimizing test hacking is particularly relevant here: a workflow that optimizes only for “tests pass” without behavioral evidence can still fail.

_Source: https://arxiv.org/html/2510.23761v1 ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.github.com/en/actions ._

### Compliance, Audit, and Governance

Even in a solo workflow, auditability matters. The workflow should leave:

- a git history,
- a story-scoped artifact trail,
- test and runtime outputs,
- review findings,
- a human merge or escalation decision.

This satisfies practical governance even before formal compliance requirements appear. If the workflow later moves into sensitive or regulated environments, the same structure can be extended with self-hosted runners, stricter secrets management, and organization-specific policy hooks.

_Source: https://docs.github.com/en/actions ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

## 8. Strategic Technical Recommendations

### Technical Strategy and Decision Framework

The recommended architecture for your workflow is:

- **BMAD provides the canonical story and planning artifacts**
- **Pi provides the orchestration shell and model-routing layer**
- **Repo-native tools provide the verification mechanisms**
- **Story-scoped artifacts provide memory and auditability**
- **Humans provide final authority when convergence fails or risk rises**

This is not a generic “AI coding assistant” workflow. It is a **story delivery machine**. That distinction is important. The orchestration should be opinionated, because the value of the system lies precisely in enforcing discipline where ad hoc prompting would otherwise leak quality.

_Source: `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`._

### Recommended BMAD/Pi Agentic TDD Cycle

The recommended end-to-end workflow for a story is the following.

| Stage | Goal | Recommended model tier | Inputs | Outputs | Gate |
|---|---|---|---|---|---|
| 1. Story Readiness Gate | Confirm the story is implementable | High-trust reasoning model | BMAD story, brief, architecture, UX if relevant | Execution brief, ambiguity list, acceptance decomposition | No unresolved blocker remains |
| 2. Test Intent & Target Map | Convert acceptance criteria into exact validation targets | High-trust reasoning model | Execution brief, codebase scan, existing tests | Acceptance-to-test matrix, exact commands, scope notes | Every acceptance criterion has a planned verification path |
| 3. Red Test Authoring | Create/update tests that fail for the intended reason | Builder model | Target map, relevant files | New or updated failing tests, failing command output | At least one designated test is red for the correct reason |
| 4. Green Implementation Loop | Implement only enough to satisfy targeted tests | Builder model | Failing tests, exact commands, story scope | Code patch, targeted green result, patch notes | Targeted tests pass and no immediate smoke breakage appears |
| 5. Refactor & Harden | Improve design and widen verification surface | Builder + verifier | Green patch, impacted areas | Cleaner code, wider suite results, lint/format outputs | Lint/format pass and impacted broader tests pass |
| 6. Runtime Verification | Prove real behavior in the running system | Builder/runtime verifier using planner/generator/healer ideas | Story flows, running app, environment setup | Playwright traces, screenshots, logs, runtime notes | Runtime proof confirms acceptance behavior |
| 7. Dual Review | Review correctness, maintainability, and hidden risk | Two diverse high-trust review models | Diff, story, runtime proof, test results | Review findings A and B | No blocking finding remains |
| 8. Repair Coordinator | Fix findings and re-validate | Builder + selective re-review | Review findings, patch, commands | Final patch and cleared findings | Max 2–3 loops or escalate |
| 9. Human Decision | Merge, checkpoint, or escalate | Human | All artifacts | Final decision and closeout | Explicit closure exists |

This cycle should be enforced with four hard rules:

1. **Fresh-context rule:** each stage gets only the inputs it actually needs.
2. **Red-proof rule:** implementation does not start until failing evidence exists.
3. **Evidence rule:** every gate is passed by artifacts, not by agent claims.
4. **Escalation rule:** after bounded retries, stop and ask the human.

Two additional operational safeguards are recommended for non-trivial stories:

- create a **checkpoint of the red state** before green implementation whenever test integrity is at risk,
- run a **post-edit targeted verification command** after file modifications so drift is detected immediately rather than several turns later.

That is the core TDD cycle I recommend for your environment.

_Source: https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ ; https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/ ; https://playwright.dev/docs/test-agents ; https://arxiv.org/html/2510.23761v1 ; https://code.claude.com/docs/en/best-practices ; https://docs.anthropic.com/en/docs/claude-code/hooks ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `docs/research/tdd-opus-analysis.md`._

### Recommended Initial Model Routing for Your Environment

Given the environment you specified, the safest initial routing hypothesis is:

| Role | Primary | Secondary | Notes |
|---|---|---|---|
| Story analyst / execution-brief author | gpt-5.4 or opus-4.6 | sonnet-4.6 | Use for scope decomposition, acceptance mapping, and risk framing |
| Main implementer / repair loop | sonnet-4.6 or glm-5.1 | gpt-5.4 | Calibrate by repo results; keep scope tightly bounded |
| Reviewer A | opus-4.6 | gpt-5.4 | Focus on correctness and subtle bugs |
| Reviewer B | gpt-5.4 | opus-4.6 | Focus on acceptance fit, maintainability, and edge cases |
| Runtime/E2E author | sonnet-4.6 or glm-5.1 | gpt-5.4 | Stronger model validates or reviews generated browser checks |
| Local support agent | Ollama 32k | — | Restrict to bounded, low-trust tasks: summarization, grep triage, log clustering, mechanical transforms |

This routing should be treated as a **starting calibration**, not dogma. The workflow should collect phase-level metrics so that routing can be adjusted empirically.

_Source: user-provided environment constraints; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Competitive Technical Advantage

Your technical advantage is not that BMAD or Pi are the market defaults. It is that together they create a combination mainstream setups often lack:

- **story-quality inputs** from BMAD,
- **workflow malleability** from Pi,
- **model independence** through multi-provider support,
- **artifact-driven handoffs** aligned with TDD discipline.

Most public agentic coding workflows start from prompts and then try to recover structure. Your workflow can start from structured artifacts and use Pi to enforce process. That is a meaningful differentiator.

_Source: `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md`._

## 9. Implementation Roadmap and Risk Assessment

### Technical Implementation Framework

A phased rollout is strongly recommended.

**Phase 1 — Manual pilot (immediately).**
Use explicit Pi skill invocations and manual phase transitions on 3–5 stories. The goal is not automation yet; it is to validate artifact shapes, commands, model routing, and gates.

**Phase 2 — Semi-automated skill pack.**
Create Pi skills or prompt templates for each major phase:

- story readiness
- test intent map
- red test authoring
- green implementation
- runtime verification
- dual review
- repair coordinator

At this stage, the human still approves transitions, but the process becomes repeatable.

**Phase 3 — Pi extension or SDK orchestrator.**
Once the manual loop is stable, build a thin orchestrator that:

- creates stage artifacts,
- chooses models by role,
- spins fresh sessions or branches,
- records outputs,
- enforces gates,
- stops on escalation conditions.

**Phase 4 — CI integration.**
Introduce GitHub Actions or equivalent to replay or verify key gates on branch/PR events, publish artifacts, and optionally gate merge.

_Source: `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; https://docs.github.com/en/actions ; https://docs.anthropic.com/en/docs/claude-code/github-actions ._

### Technology Migration Strategy

Do not attempt a “big bang” replacement of your current coding habits. Instead:

1. keep the old mental model of story delivery,
2. replace one phase at a time with explicit agentic TDD discipline,
3. measure outcomes,
4. only then automate.

This is especially important for model routing. A routing scheme that looks elegant on paper but is not benchmarked against your repositories will drift quickly.

_Source: https://code.claude.com/docs/en/best-practices ; https://aider.chat/ ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

### Technical Risk Management

| Risk | Typical symptom | Mitigation |
|---|---|---|
| Procedural TDD theater | Agent claims to be doing TDD without real failing evidence | Require red-proof artifact before implementation |
| Test-after trap | Agent implements first and backfills tests later | Enforce red-first stage boundary and review test timestamps/artifacts |
| Kitchen-sink tests | Single broad tests hide which behavior actually failed | Prefer smaller behavior-focused tests and acceptance-to-test mapping |
| Mock-everything drift | Tests pass against mocks while real risk remains untested | Mock only external boundaries and preserve behavioral coverage |
| Green-bar addiction | Agent overfits or hardcodes to satisfy one test | Add adjacent tests, runtime verification, and review for overfitting |
| Implementation-detail testing | Refactors break tests without changing user behavior | Prefer observable-behavior assertions and higher-level intent naming |
| Test theater | Tests pass but behavior is still wrong | Require runtime verification and acceptance-to-test mapping |
| Context drift | Late-stage confusion and hidden assumptions | Use fresh-context handoffs and short phase prompts |
| Patch thrash | Multiple non-converging repair loops | Cap retries at 2–3 and escalate |
| Cost creep | Premium model usage everywhere | Restrict top-tier models to planning, review, and hard debugging |
| Weak local model misuse | Low-quality patches or silent regressions | Keep Ollama on bounded support tasks until benchmarked |
| Tool overreach | Dangerous commands, secret leakage, excessive integration scope | Use scoped tools, minimal MCP, and hook/policy controls |
| Review monoculture | Two reviews miss the same flaw | Use diverse models or review lenses |

_Source: https://arxiv.org/html/2510.23761v1 ; https://docs.anthropic.com/en/docs/claude-code/hooks ; https://docs.anthropic.com/en/docs/claude-code/mcp ; https://docs.github.com/en/actions ; `docs/research/tdd-initiative`._

## 10. Future Technical Outlook and Innovation Opportunities

### Emerging Technology Trends

The next wave of agentic TDD is likely to include:

- **just-in-time regression tests** generated for specific changes,
- **trace-aware repair loops** that use runtime evidence directly,
- **benchmark-informed model routing** rather than intuition-based routing,
- **stronger test-generation quality filters** to reduce brittle or low-value generated tests,
- **workflow packages** that encode these patterns as reusable harness add-ons.

Meta’s JiTTesting article is especially important here because it suggests that static authored suites alone may not keep up with agentic development speed forever. The likely future is a hybrid: authored acceptance tests, generated regression tests, and runtime proof all working together.

_Source: https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/ ; https://playwright.dev/docs/test-agents ; https://www.swebench.com/ ; https://arxiv.org/html/2510.23761v1 ._

### Innovation Opportunities for This Project

Your project has several promising innovation paths:

- a **Pi skill pack** for story-driven TDD execution,
- a **Pi extension/SDK orchestrator** that turns BMAD stories into phase runs automatically,
- a **story benchmark dataset** built from your own stories, artifacts, and outcomes,
- a **model-routing scorecard** per repo and per phase,
- a **runtime-proof artifact standard** that becomes part of story closure.

Because Pi is customizable and BMAD already encodes planning structure, your setup is unusually well positioned to turn private practice into a reusable workflow package later.

_Source: `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md` ; `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md` ; `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`._

## 11. Technical Research Methodology and Source Verification

### Primary Technical Sources

**Vendor and platform documentation**

- https://code.claude.com/docs/en/best-practices
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://docs.anthropic.com/en/docs/claude-code/hooks
- https://docs.anthropic.com/en/docs/claude-code/mcp
- https://docs.anthropic.com/en/docs/claude-code/github-actions
- https://aider.chat/
- https://openhands.dev/
- https://playwright.dev/docs/intro
- https://playwright.dev/docs/test-agents
- https://playwright.dev/docs/ci
- https://vitest.dev/guide/
- https://docs.pytest.org/en/stable/contents.html
- https://docs.github.com/en/actions
- https://modelcontextprotocol.io/introduction

**Research and benchmark sources**

- https://arxiv.org/html/2510.23761v1
- https://www.swebench.com/
- https://www.swebench.com/SWE-bench/guides/docker_setup/
- https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/

**Workflow guides and technical commentary**

- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/
- https://www.builder.io/blog/test-driven-development-ai

**Local Pi and project sources used for adaptation**

- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/README.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/skills.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/sdk.md`
- `/home/cvc/.nvm/versions/node/v24.14.1/lib/node_modules/@mariozechner/pi-coding-agent/docs/models.md`
- `docs/research/tdd-initiative`
- `docs/research/tdd-opus-analysis.md`
- `docs/_bmad-output/planning-artifacts/product-brief-mypi-config.md`

### Technical Web Search Queries Used

Representative query set used during source discovery and validation:

- `agentic TDD software engineering`
- `SWE-bench Verified agentic TDD`
- `agentic coding testing frameworks tools`
- `Claude Code best practices tests lint`
- `OpenHands agent software engineering tests`
- `aider test driven development ai coding`
- `Playwright coding agents runtime verification`
- plus targeted direct retrieval of primary docs after source discovery

### Technical Confidence Levels

**High confidence:**

- verification-first workflows outperform vague prompt-first workflows
- fresh-context handoffs are important for reliability and cost control
- role decomposition improves observability and control
- runtime verification should be in the core workflow, not appended at the end
- BMAD/Pi can implement these patterns because Pi is intentionally extensible and BMAD already provides artifact structure

**Medium confidence:**

- the exact optimal routing among glm-5.1, sonnet-4.6, gpt-5.4, and opus-4.6 will vary by repo and phase
- generated JiT tests will likely become more central, but the precise mature form is still emerging
- local Ollama models may become more useful over time, but current trust should remain bounded without your own measurements

### Technical Limitations

This field is still young. Vendor documentation is useful but not neutral. Academic evidence is growing but not yet broad enough to settle every design choice quantitatively. Some vendor ecosystems were less accessible to direct scraping or public docs retrieval, so this report leaned toward accessible primary documentation, benchmark sites, and sources with explicit workflow detail. That does not invalidate the findings, but it does mean that some quantitative claims in the broader discourse remain harder to verify than the architectural patterns themselves.

## 12. Technical Appendices and Reference Materials

### Appendix A: Recommended Story Artifact Set

**Suggested path:** `docs/_bmad-output/implementation-artifacts/stories/<story-id>/`

| Artifact | Purpose | Producer | Consumer |
|---|---|---|---|
| `story-execution-brief.md` | Distill story, risks, scope boundaries, exact objective | Story readiness stage | All later stages |
| `acceptance-to-test-matrix.md` | Map each acceptance criterion to unit/integration/runtime verification | Test intent stage | Red, green, runtime, review |
| `test-targets.txt` | Optional impacted-test map or exact verification commands for the story | Test intent stage | Red, green, refactor, review |
| `red-proof.md` or `failing-tests.log` | Prove that designated tests fail before implementation | Red stage | Green, review, human |
| `runtime-specs/*.md` | Optional browser-flow or user-behavior specs used to generate or review E2E tests | Test intent / runtime stage | Runtime verification, review |
| `patch-summary.md` | Explain the implementation delta and impacted areas | Green / refactor stage | Runtime verification, review |
| `validation-summary.md` | Capture targeted tests, impacted suite, lint, coverage deltas if relevant | Refactor stage | Review, human |
| `llm-eval-summary.md` | Optional thresholded, stochastic, or judge-based evaluation summary for AI-facing behavior | Refactor / runtime stage | Review, human |
| `runtime-proof/` | Playwright traces, screenshots, videos, logs | Runtime verification stage | Review, human |
| `review-a.md` | Findings from reviewer A | Review stage | Repair coordinator, human |
| `review-b.md` | Findings from reviewer B | Review stage | Repair coordinator, human |
| `story-closeout.md` | Final decision, unresolved items, follow-ups, lessons | Human closeout | Future work and retrospectives |

### Appendix B: Recommended Architectural Decisions

| Decision | Recommendation | Rationale |
|---|---|---|
| Canonical input | BMAD story file | Best source of scope and acceptance intent |
| Workflow memory | Artifacts + git + session checkpoints | More auditable than hidden conversation memory |
| Orchestrator | Pi skills first, Pi SDK/extension later | Low-friction adoption, clear path to automation |
| Inner-loop verification | Targeted unit/integration tests only | Faster and more precise than running everything every turn |
| Runtime verification | Mandatory for user-visible behavior | Prevents “all unit tests green but app still broken” failures |
| Final review | Two diverse review passes | Reduces correlated blind spots |
| Retry policy | Max 2–3 repair loops | Prevents thrash and hidden sunk cost |
| Local model usage | Bounded support tasks only initially | Matches current trust and context constraints |

### Appendix C: Suggested Success Metrics and KPIs

| Metric | Why it matters |
|---|---|
| Stories with explicit red proof | Detects fake or missing TDD |
| Median loops to green | Measures implementation efficiency |
| Runtime verification first-pass success | Measures end-to-end quality |
| Blocking findings after review | Measures hidden defect rate |
| Human escalation rate | Measures workflow convergence |
| Cost per story by phase | Enables model-routing optimization |
| Post-merge regression rate | Ultimate quality outcome |

### Appendix D: Immediate Next Steps

1. Define templates for the artifact set in Appendix A.
2. Pilot the 9-stage workflow on a small number of real stories with manual transitions.
3. Track phase metrics and compare model performance by role.
4. Package stable phase prompts as Pi skills.
5. Only then build an SDK or extension orchestrator.

## 13. Technical Research Conclusion

### Summary of Key Technical Findings

The research strongly supports the idea that TDD remains not only relevant but increasingly valuable in agentic software delivery—provided it is implemented as a **verification-centered workflow** rather than as a vague instruction. The dominant patterns are now visible across independent sources: explicit failing tests, stage decomposition, fresh-context handoffs, runtime validation, bounded repair loops, and audit trails grounded in repo-native artifacts.

### Strategic Technical Impact Assessment

For your project, this means the target workflow is now much clearer. The correct design is not “let Pi imitate Claude Code”, nor “force classic human TDD rituals unchanged onto agents”. It is to build a **BMAD story-driven, Pi-orchestrated, multi-model delivery loop** that borrows the best industry patterns and makes them enforceable through artifacts, tools, and gates.

### Next Steps Technical Recommendations

The immediate next move should not be coding the whole orchestrator at once. The immediate next move should be to freeze the recommended workflow and artifact schema, then test it manually on real stories. Once the shape is stable, the automation work in Pi becomes much more straightforward—and much more likely to be correct.

---

**Technical Research Completion Date:** 2026-04-12
**Research Period:** current comprehensive technical analysis
**Source Verification:** All key claims grounded in current accessible sources and local adaptation documentation
**Technical Confidence Level:** High for architecture and workflow direction; medium for exact model routing until locally benchmarked

_This document is intended to serve as the working reference for designing the BMAD/Pi TDD cycle and final story workflow for `mypi-config`._

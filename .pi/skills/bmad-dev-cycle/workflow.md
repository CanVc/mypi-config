---
main_config: '{project-root}/_bmad/bmm/config.yaml'
max_iterations: 5
dev_agent: implementer
triage_agent: findings-triager
reviewer_agents:
  - reviewer-a
  - reviewer-b
model: openai-codex/gpt-5.5
required_context: fresh
---

# BMAD Dev Cycle Workflow

**Goal:** Implement or resume the BMAD story in `{story-folder}` and automatically loop implementation plus two independent reviews until the story has no remaining blocking `Medium` or `High` findings, or until the configured iteration cap is reached.

**Invocation:**

```text
/dev-cycle <story-folder-or-story-file> [maxIterations]
```

- `maxIterations` is optional.
- Default: `5`.
- Valid range for now: `1..5`.
- Invalid values HALT before dispatch.

**Your Role:** You are the parent orchestrator. You own routing, durable state, artifact validation, sprint-status updates, and stop/continue decisions. Child agents do concrete role-specific work only.

## Critical Rules

- Communicate in the configured `{communication_language}` from `{main_config}` when available.
- Use model `openai-codex/gpt-5.5` for `implementer`, `reviewer-a`, `reviewer-b`, and `findings-triager` dispatches unless project settings override agent models.
- All formal BMAD subagent dispatches MUST set `context: "fresh"` explicitly.
- Use project agents only: `implementer`, `reviewer-a`, `reviewer-b`, `findings-triager`.
- Do not use `context: "fork"` and do not use `subagent({ action: "resume" })` in this workflow.
- Children must not launch subagents. Keep orchestration in the parent session.
- The implementer follows `.pi/skills/bmad-dev-story/workflow.md` for the target story.
- Reviewers perform independent `/code-review`-style review passes using `.pi/skills/bmad-code-review` severity and finding conventions, but they do not launch nested reviewers and do not edit files.
- `findings-triager` deduplicates raw reviewer reports, writes `reviews/{story_id_dash}-R{i}-findings.md`, and writes linked story action items.
- Parent validates the triaged findings artifact and story links before deciding the next action.
- Any unresolved blocking `High` or `Medium` finding triggers another implementation iteration unless it requires a human decision.
- `Low` findings do not block completion; defer them unless the user explicitly asks otherwise.
- Stop after `maxIterations`. If blocking `High` or `Medium` findings remain after the cap, warn the user and do not mark the story `done`.

## Initialization

1. Load `{main_config}` if it exists and resolve:
   - `project_name`, `implementation_artifacts`, `planning_artifacts`, `user_name`
   - `communication_language`, `document_output_language`, `user_skill_level`
   - `date` as the current date/time
   - `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
2. Parse invocation arguments:
   - first argument: story folder or story file;
   - optional second argument: `maxIterations` integer in range `1..5`;
   - if omitted, use `5`.
3. Read `.pi/skills/bmad-orchestrator/SKILL.md` before the first dispatch and enforce its BMAD Session Policy and Task Routing rules.
4. Verify subagents are available before dispatch:

   ```ts
   subagent({ action: "list", agentScope: "project" })
   ```

   HALT if `implementer`, `reviewer-a`, `reviewer-b`, or `findings-triager` is missing or disabled.
5. Resolve `{story-folder}` and `{story_file}`:
   - If the user provides a directory, derive `story_slug` from the directory basename and `story_id_dash` from the first two dash-separated tokens.
   - Prefer canonical story file `{story-folder}/{story_id_dash}-story.md`.
   - Fall back to legacy folder story file `{story-folder}/{story_slug}.md` only for migration compatibility.
   - If the user provides a Markdown file, use it directly, set `{story-folder}` to its parent, and derive `story_id_dash`/`story_slug` from the file/folder.
   - Ignore `reviews/*.md`, `review-*.md`, `*-findings.md`, changelog, orchestrator-log, cycle-state, validation, remediation, and runtime-proof artifacts while discovering the story file.
   - HALT if no unique story file can be resolved.
6. Ensure story-scoped artifact paths exist or can be created:

   ```text
   {story-folder}/{story_id_dash}-story-changelog.md
   {story-folder}/{story_id_dash}-orchestrator-log.md
   {story-folder}/{story_id_dash}-cycle-state.md
   {story-folder}/reviews/
   {story-folder}/remediation/
   {story-folder}/validation/
   {story-folder}/{story_id_dash}-runtime-proof/
   ```

7. Read the complete story file.
8. Create or update `{cycle_state_file}` = `{story-folder}/{story_id_dash}-cycle-state.md` using Markdown with machine markers:

   ````md
   # {story_id_dash} Cycle State

   <!-- bmad:cycle-state:start -->
   ```yaml
   storyId: {story_id_dash}
   storySlug: {story_slug}
   workflow: dev-cycle
   maxIterations: {maxIterations}
   currentIteration: 0
   status: in-progress
   tasks: []
   ```
   <!-- bmad:cycle-state:end -->
   ````

9. Create or update `{orchestrator_log_file}` = `{story-folder}/{story_id_dash}-orchestrator-log.md` with current position, routing log, dispatch evidence, escalations, sprint status sync, and recovery notes.
10. Add or update a concise `## Story Artifacts` section in the story file if missing. Link to changelog, orchestrator log, cycle state, `reviews/`, `validation/`, and runtime proof. Do not embed the full cycle state in the story.

## Iteration Loop

Run at most `{maxIterations}` iterations. Let `i` be the current iteration number, starting at 1.

### Step 1 — Prepare durable tasks

Before dispatching, append or update these task records inside `{cycle_state_file}` between the `bmad:cycle-state` markers:

```yaml
tasks:
  - taskId: "dev-R{i}"
    title: "Implement or resume story via dev-story workflow"
    targetAgent: "implementer"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "{story_file}"
        - ".pi/skills/bmad-dev-story/workflow.md"
    dependsOn: []
    activeAgentId: null
    outputArtifact: "{story_file}"
    routingDecision: null
    cause: null
    recommendedNextAction: null
  - taskId: "review-a-R{i}"
    title: "Independent code review pass A"
    targetAgent: "reviewer-a"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "{story_file}"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R{i}"]
    activeAgentId: null
    outputArtifact: "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-a.md"
    routingDecision: null
    cause: null
    recommendedNextAction: null
  - taskId: "review-b-R{i}"
    title: "Independent code review pass B"
    targetAgent: "reviewer-b"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "{story_file}"
        - ".pi/skills/bmad-code-review/workflow.md"
    dependsOn: ["dev-R{i}"]
    activeAgentId: null
    outputArtifact: "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-b.md"
    routingDecision: null
    cause: null
    recommendedNextAction: null
  - taskId: "triage-R{i}"
    title: "Deduplicate review findings and link story action items"
    targetAgent: "findings-triager"
    status: "pending"
    contextSource:
      type: "artifact-path"
      paths:
        - "{story_file}"
        - "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-a.md"
        - "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-b.md"
        - ".pi/references/artifact-format.md"
        - ".pi/references/workflow-status-codes.md"
    dependsOn: ["review-a-R{i}", "review-b-R{i}"]
    activeAgentId: null
    outputArtifact: "{story-folder}/reviews/{story_id_dash}-R{i}-findings.md"
    routingDecision: null
    cause: null
    recommendedNextAction: null
```

Validate every context path exists and is readable before moving any task to `in-progress`. Raw reviewer output paths are allowed to be absent until their producer tasks complete.

### Step 2 — Dispatch implementer

Set `dev-R{i}` to `in-progress` in `{cycle_state_file}`, record `activeAgentId: implementer`, then launch:

```ts
subagent({
  agent: "implementer",
  model: "openai-codex/gpt-5.5",
  context: "fresh",
  agentScope: "project",
  taskStatePath: "{cycle_state_file}",
  durableTaskId: "dev-R{i}",
  task: `You are the BMAD Implementer for iteration R{i}.

Source of truth story file: {story_file}
Story folder: {story-folder}
Workflow to follow: .pi/skills/bmad-dev-story/workflow.md
Artifact format reference: .pi/references/artifact-format.md

Read the story file completely, then read and follow the dev-story workflow. Use the explicit story_path/story_file above; do not auto-select a different story. If this is a review continuation, prioritize unchecked [AI-Review] follow-up tasks. For every [AI-Review] task, follow its Source link to reviews/{story_id_dash}-R*-findings.md and the exact F-* anchor before implementing. Implement only what the story and linked findings require. Update only the story sections permitted by dev-story. Run focused validation and record files changed, tests run, and completion notes.

Do not launch subagents. If you hit a HALT condition, report it with evidence.`
})
```

After completion, parent-validates the result:

- story file still exists and is readable;
- no child attempted nested orchestration;
- status is not a runtime failure;
- implementation did not report an unresolved HALT.

If valid, set `dev-R{i}` to `completed`. If invalid, set it to `blocked` or `failed` with `cause` and `recommendedNextAction`, then HALT.

### Step 3 — Dispatch two independent reviewers in parallel

Set `review-a-R{i}` and `review-b-R{i}` to `in-progress`, recording `activeAgentId` for each. Then launch both reviewers in parallel:

```ts
subagent({
  taskStatePath: "{cycle_state_file}",
  tasks: [
    {
      agent: "reviewer-a",
      durableTaskId: "review-a-R{i}",
      model: "openai-codex/gpt-5.5",
      output: "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-a.md",
      outputMode: "file-only",
      task: `Run independent BMAD code-review-style pass A for iteration R{i}.

Story file: {story_file}
Story folder: {story-folder}
Reference workflow conventions: .pi/skills/bmad-code-review/workflow.md and steps.

You are one reviewer layer only. Do not launch subagents and do not edit files. Inspect the current implementation, current git delta, story acceptance criteria, File List, Dev Agent Record, linked findings from prior rounds if relevant, and referenced implementation files. Focus on correctness, regressions, acceptance criteria, architecture compliance, and validation evidence.

Return only a structured review report with:
## Verdict
PASS | CHANGES_REQUESTED | BLOCKED
## Findings
For each finding:
- Severity: High|Medium|Low
- Title:
- AC/Constraint: ... or N/A
- Location: file:line or N/A
- Evidence:
- Recommended fix:
If no findings, state: No findings.`
    },
    {
      agent: "reviewer-b",
      durableTaskId: "review-b-R{i}",
      model: "openai-codex/gpt-5.5",
      output: "{story-folder}/reviews/{story_id_dash}-R{i}-reviewer-b.md",
      outputMode: "file-only",
      task: `Run independent BMAD code-review-style pass B for iteration R{i}.

Story file: {story_file}
Story folder: {story-folder}
Reference workflow conventions: .pi/skills/bmad-code-review/workflow.md and steps.

You are one reviewer layer only. Do not launch subagents and do not edit files. Do not reference reviewer-a output. Inspect the current implementation, current git delta, story acceptance criteria, File List, Dev Agent Record, linked findings from prior rounds if relevant, and referenced implementation files. Focus especially on edge cases, tests/validation gaps, maintainability required now, data integrity, security/privacy, and consistency.

Return only a structured review report with:
## Verdict
PASS | CHANGES_REQUESTED | BLOCKED
## Findings
For each finding:
- Severity: High|Medium|Low
- Title:
- AC/Constraint: ... or N/A
- Location: file:line or N/A
- Evidence:
- Recommended fix:
If no findings, state: No findings.`
    }
  ],
  concurrency: 2,
  context: "fresh",
  agentScope: "project"
})
```

Parent-validates each reviewer output. If a reviewer fails, times out, or returns empty/ambiguous output, mark that review task `blocked` or `failed` with `cause` and `recommendedNextAction`. Continue to triage only with successfully completed independent reviewer outputs if at least one is valid; otherwise HALT.

### Step 4 — Dispatch findings triager

Set `triage-R{i}` to `in-progress`, recording `activeAgentId: findings-triager`, then launch:

```ts
subagent({
  agent: "findings-triager",
  model: "openai-codex/gpt-5.5",
  context: "fresh",
  agentScope: "project",
  taskStatePath: "{cycle_state_file}",
  durableTaskId: "triage-R{i}",
  task: `You are the BMAD Findings Triager for iteration R{i}.

Story file: {story_file}
Story folder: {story-folder}
Raw review A: {story-folder}/reviews/{story_id_dash}-R{i}-reviewer-a.md
Raw review B: {story-folder}/reviews/{story_id_dash}-R{i}-reviewer-b.md
Findings output: {story-folder}/reviews/{story_id_dash}-R{i}-findings.md
Artifact reference: .pi/references/artifact-format.md
Status code reference: .pi/references/workflow-status-codes.md

Read the story and valid raw review reports. Normalize, deduplicate, classify, and assign stable ids F-R{i}-001, F-R{i}-002, ... Write the findings artifact using the required format. Then update the story with concise linked action items under Senior Developer Review (AI) and matching linked tasks under Tasks / Subtasks -> Review Follow-ups (AI). Every story action item must include Source: reviews/{story_id_dash}-R{i}-findings.md#F-R{i}-xxx. Do not copy full raw review prose into the story.

Do not launch subagents. If required artifacts are missing or malformed, fail closed and report artifact-invalid.`
})
```

Parent-validates:

- `reviews/{story_id_dash}-R{i}-findings.md` exists and is readable;
- every non-dismissed finding has id, status, severity, classification, blocking flag, problem, required fix, validation requirements, and out-of-scope fields;
- every unchecked story `[AI-Review]` item for this round has a matching `Source: reviews/{story_id_dash}-R{i}-findings.md#F-R{i}-xxx` link;
- every unchecked `Senior Developer Review (AI)` action item for this round has the same finding id and source link;
- no full raw review report was copied into the story.

If valid, set `triage-R{i}` to `completed`. If invalid, set it to `blocked` or `failed` and HALT.

### Step 5 — Decide loop or completion

Read `reviews/{story_id_dash}-R{i}-findings.md` and count unresolved findings:

- `decision_count`: `spec-ambiguity`, `workflow-contract-violation`, `artifact-invalid`, or explicit decision-needed findings that require human input;
- `blocking_count`: unresolved blocking `High` plus blocking `Medium` findings;
- `low_count`: deferred/non-blocking Low findings.

Decision rules:

- If `decision_count > 0`: HALT and ask the user to resolve the decisions. Do not launch another implementer until decisions are answered.
- If `blocking_count > 0` and `i < maxIterations`:
  1. Set story status to `in-progress`.
  2. Sync `sprint_status` entry for `story_key` to `in-progress` if possible.
  3. Record routing decision in orchestrator log.
  4. Start the next iteration.
- If `blocking_count > 0` and `i == maxIterations`:
  1. Set story status to `in-progress`.
  2. Sync `sprint_status` to `in-progress` if possible.
  3. Record `retry-limit-reached` in orchestrator log.
  4. Warn the user that the configured iteration maximum was reached and summarize remaining blocking findings.
  5. HALT.
- If `blocking_count == 0`:
  1. Set story status to `done`.
  2. Sync `sprint_status` entry for `story_key` to `done` if possible.
  3. Summarize implementation, reviews, findings artifact paths, deferred Low items, validation evidence, and final story path.
  4. Stop successfully.

## Story Status Update Rules

When updating story status:

- Prefer the canonical `Status` section/value already used by the story.
- Preserve surrounding Markdown structure.
- Do not mark `done` if any unchecked `[AI-Review]` task with `[HIGH]` or `[MEDIUM]` remains.

When syncing `sprint-status.yaml`:

- Read the full file before editing.
- Find `development_status[story_key]`.
- Update only that status and `last_updated`.
- Preserve comments and unrelated structure.
- If the story key is missing, warn but continue with story-file status as source of truth.

## Final Output

On success, report:

```md
✅ BMAD dev cycle complete

- Story: {story_file}
- Iterations used: <n>/{maxIterations}
- Final status: done
- Review outputs: <paths>
- Findings artifacts: <paths>
- Deferred Low findings: <count>
- Validation summary: <summary>
```

On max-iteration stop, report:

```md
⚠️ BMAD dev cycle stopped after {maxIterations} iterations

- Story: {story_file}
- Remaining High/Medium findings: <count>
- Status left as: in-progress
- Findings artifact: reviews/{story_id_dash}-R{maxIterations}-findings.md
- Required next action: human review, remediation brief, or manual intervention
```

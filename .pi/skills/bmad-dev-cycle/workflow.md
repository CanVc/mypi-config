---
main_config: '{project-root}/_bmad/bmm/config.yaml'
max_iterations: 5
dev_agent: implementer
reviewer_agents:
  - reviewer-a
  - reviewer-b
model: openai/gpt-5.5
required_context: fresh
---

# BMAD Dev Cycle Workflow

**Goal:** Implement or resume the BMAD story in `{story-folder}` and automatically loop implementation plus two independent reviews until the story has no remaining `Medium` or `High` findings, or until five iterations have been attempted.

**Your Role:** You are the parent orchestrator. You own routing, durable state, triage, deduplication, story-file updates, sprint-status updates, and stop/continue decisions. Child agents do concrete role-specific work only.

## Critical Rules

- Communicate in the configured `{communication_language}` from `{main_config}` when available.
- Use model `openai/gpt-5.5` for `implementer`, `reviewer-a`, and `reviewer-b` dispatches.
- All formal BMAD subagent dispatches MUST set `context: "fresh"` explicitly.
- Use project agents only: `implementer`, `reviewer-a`, `reviewer-b`.
- Do not use `context: "fork"` and do not use `subagent({ action: "resume" })` in this workflow.
- Children must not launch subagents. Keep orchestration in the parent session.
- The implementer follows `.pi/skills/bmad-dev-story/workflow.md` for the target story.
- Reviewers perform independent `/code-review`-style review passes using `.pi/skills/bmad-code-review` severity and finding conventions, but they do not launch nested reviewers and do not edit files.
- Parent writes deduplicated findings into the story file before deciding the next action.
- Any non-dismissed `High` or `Medium` finding triggers another implementation iteration unless it requires a human decision.
- `Low` findings do not block completion; defer them unless the user explicitly asks otherwise.
- Stop after five iterations. If `High` or `Medium` findings remain after iteration 5, warn the user and do not mark the story `done`.

## Initialization

1. Load `{main_config}` if it exists and resolve:
   - `project_name`, `implementation_artifacts`, `planning_artifacts`, `user_name`
   - `communication_language`, `document_output_language`, `user_skill_level`
   - `date` as the current date/time
   - `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
2. Read `.pi/skills/bmad-orchestrator/SKILL.md` before the first dispatch and enforce its BMAD Session Policy and Task Routing rules.
3. Verify subagents are available before dispatch:

   ```ts
   subagent({ action: "list", agentScope: "project" })
   ```

   HALT if `implementer`, `reviewer-a`, or `reviewer-b` is missing or disabled.
4. Resolve `{story-folder}`:
   - If the user provides a directory, find the canonical story file inside it. Prefer `<story-folder>/<basename(story-folder)>.md`; otherwise use the single non-review Markdown story file in the folder.
   - If the user provides a Markdown file, use it directly and set `{story-folder}` to its parent directory.
   - Ignore review artifacts such as `review-*.md` while discovering the story file.
   - HALT if no unique story file can be resolved.
5. Read the complete story file. Extract `story_key` from the story filename or folder name.
6. Create or update a durable parent-owned section in the story file:

   ```md
   ## BMAD Dev Cycle (AI)

   ### Orchestrator State
   - Max iterations: 5
   - Current iteration: 0
   - Dev agent: implementer (`openai/gpt-5.5`)
   - Review agents: reviewer-a, reviewer-b (`openai/gpt-5.5`)

   ### Task State
   ```yaml
   tasks: []
   ```
   ```

   Keep this section as durable workflow state. Runtime status from `pi-subagents` is only control-plane evidence until parent validation updates this section.

## Iteration Loop

Run at most five iterations. Let `i` be the current iteration number, starting at 1.

### Step 1 — Prepare durable tasks

Before dispatching, append or update these task records under `BMAD Dev Cycle (AI) → Task State`:

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
    outputArtifact: null
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
    outputArtifact: "{story-folder}/review-{story_key}-R{i}-reviewer-a-output.md"
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
    outputArtifact: "{story-folder}/review-{story_key}-R{i}-reviewer-b-output.md"
    routingDecision: null
    cause: null
    recommendedNextAction: null
```

Validate every context path exists and is readable before moving any task to `in-progress`.

### Step 2 — Dispatch implementer

Set `dev-R{i}` to `in-progress`, record `activeAgentId: implementer`, then launch:

```ts
subagent({
  agent: "implementer",
  model: "openai/gpt-5.5",
  context: "fresh",
  agentScope: "project",
  task: `You are the BMAD Implementer for iteration R{i}.

Source of truth story file: {story_file}
Story folder: {story-folder}
Workflow to follow: .pi/skills/bmad-dev-story/workflow.md

Read the story file completely, then read and follow the dev-story workflow. Use the explicit story_path/story_file above; do not auto-select a different story. If this is a review continuation, prioritize unchecked [AI-Review] follow-up tasks before regular tasks. Implement only what the story and review follow-ups require. Update only the story sections permitted by dev-story. Run focused validation and record files changed, tests run, and completion notes.

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
  tasks: [
    {
      agent: "reviewer-a",
      model: "openai/gpt-5.5",
      output: "{story-folder}/review-{story_key}-R{i}-reviewer-a-output.md",
      outputMode: "file-only",
      task: `Run independent BMAD code-review-style pass A for iteration R{i}.

Story file: {story_file}
Story folder: {story-folder}
Reference workflow conventions: .pi/skills/bmad-code-review/workflow.md and steps.

You are one reviewer layer only. Do not launch subagents and do not edit files. Inspect the current implementation, current git delta, story acceptance criteria, File List, Dev Agent Record, and referenced implementation files. Focus on correctness, regressions, acceptance criteria, architecture compliance, and validation evidence.

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
      model: "openai/gpt-5.5",
      output: "{story-folder}/review-{story_key}-R{i}-reviewer-b-output.md",
      outputMode: "file-only",
      task: `Run independent BMAD code-review-style pass B for iteration R{i}.

Story file: {story_file}
Story folder: {story-folder}
Reference workflow conventions: .pi/skills/bmad-code-review/workflow.md and steps.

You are one reviewer layer only. Do not launch subagents and do not edit files. Do not reference reviewer-a output. Inspect the current implementation, current git delta, story acceptance criteria, File List, Dev Agent Record, and referenced implementation files. Focus especially on edge cases, tests/validation gaps, maintainability required now, data integrity, security/privacy, and consistency.

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

Parent-validates each reviewer output. If a reviewer fails, times out, or returns empty/ambiguous output, mark that review task `blocked` or `failed` with `cause` and `recommendedNextAction`. Continue only with successfully completed independent reviewer outputs if at least one is valid; otherwise HALT.

### Step 4 — Normalize, deduplicate, classify

For all valid reviewer findings:

1. Normalize each finding into:
   - `id`
   - `sources`: `reviewer-a`, `reviewer-b`, or both
   - `title`
   - `severity`: exactly `High`, `Medium`, or `Low`
   - `acRefs`: AC/constraint references or `N/A`
   - `location`: `file:line` or `N/A`
   - `detail`
   - `recommendedFix`
2. If severity is missing, assign `Medium` and note the parsing issue.
3. Deduplicate findings that share the same root cause, AC/constraint, and location. Merge details and sources. Keep the highest severity.
4. Classify each finding:
   - `decision_needed`: ambiguous fix requiring user/product/architecture decision.
   - `patch`: clear current-story issue.
   - `defer`: Low severity or future-hardening item not required now.
   - `dismiss`: false positive or already handled.
5. Drop `dismiss` from blocking decisions, but record dismiss count in the cycle summary.
6. Treat every remaining `High` or `Medium` finding as blocking for this workflow unless the user explicitly approves deferral. This workflow is stricter than the default code-review workflow because the requested condition is `findings >= MEDIUM`.

### Step 5 — Persist findings to the story

Before deciding whether to loop, write deduplicated findings into `{story_file}`.

Ensure this section exists:

```md
## Senior Developer Review (AI)

### Action Items
```

Use pass tag `[R{i}]`. Append action items in this format:

- For decision-needed findings:
  ```md
  - [ ] [R{i}][<SEVERITY>][<AC refs or N/A>] <Title> — decision needed: <Detail>
  ```
- For blocking `High`/`Medium` patch findings:
  ```md
  - [ ] [R{i}][<SEVERITY>][<AC refs or N/A>] <Title> [<file:line or N/A>] — <Recommended fix>
  ```
- For `Low` or deferred findings:
  ```md
  - [x] [R{i}][LOW][<AC refs or N/A>] <Title> [<file:line or N/A>] — deferred, <reason>
  ```

For every unchecked decision-needed or blocking `High`/`Medium` item, also ensure this subsection exists under `Tasks/Subtasks`:

```md
### Review Follow-ups (AI)
```

Append matching tasks:

```md
- [ ] [AI-Review][R{i}][<SEVERITY>][<AC refs or N/A>] <Title/action>
```

Append `Low`/deferred findings to `{implementation_artifacts}/deferred-work.md` when `implementation_artifacts` is known.

Also update `BMAD Dev Cycle (AI) → Orchestrator State` with:
- iteration number;
- reviewer output artifact paths;
- severity counts;
- deduped finding count;
- next action.

### Step 6 — Decide loop or completion

Let `blocking_count` be the number of non-dismissed `High` plus `Medium` findings. Let `decision_count` be unresolved `decision_needed` findings.

- If `decision_count > 0`: HALT and ask the user to resolve the decisions. Do not launch another implementer until decisions are answered.
- If `blocking_count > 0` and `i < 5`:
  1. Set story status to `in-progress`.
  2. Sync `sprint_status` entry for `story_key` to `in-progress` if possible.
  3. Start the next iteration.
- If `blocking_count > 0` and `i == 5`:
  1. Set story status to `in-progress`.
  2. Sync `sprint_status` to `in-progress` if possible.
  3. Warn the user that the five-iteration maximum was reached and summarize remaining `High`/`Medium` findings.
  4. HALT.
- If `blocking_count == 0`:
  1. Set story status to `done`.
  2. Sync `sprint_status` entry for `story_key` to `done` if possible.
  3. Summarize implementation, reviews, deferred Low items, validation evidence, and final story path.
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
- Iterations used: <n>/5
- Final status: done
- Review outputs: <paths>
- Deferred Low findings: <count>
- Validation summary: <summary>
```

On max-iteration stop, report:

```md
⚠️ BMAD dev cycle stopped after 5 iterations

- Story: {story_file}
- Remaining High/Medium findings: <count>
- Status left as: in-progress
- Required next action: human review or manual intervention
```

---
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
specLoopIteration: 1
---

# Step 4: Review

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- Review subagents are always fresh under the centralized BMAD Session Policy: use explicit `context: "fresh"`, with no fork/resume.
- **Task-State Gate:** Any review sub-agent fan-out MUST follow `.pi/skills/bmad-orchestrator/SKILL.md` `Task Routing and Task List State`. Maintain an orchestrator-managed task list in `{spec_file}`. before dispatch, create one task per review role, validate context/dependencies, and write each selected task to `in-progress` with `activeAgentId`; after parent validation write each task to `completed`, or to `blocked` or `failed` with `cause` and `recommendedNextAction`; do not dispatch dependent tasks or classify work that depends on a blocked/failed layer's output.

## INSTRUCTIONS

Before changing `{spec_file}` status, validate the intended review dispatch against the centralized BMAD Session Policy. If any reviewer launch request omits context, requests `context: "fork"`, or requests `action: "resume"`, HALT before editing `{spec_file}` and report the requested reviewer role, requested mode, and violated policy.

After session policy validation passes, change `{spec_file}` status to `in-review` in the frontmatter before continuing.

### Construct Diff

Read `{baseline_commit}` from `{spec_file}` frontmatter. If `{baseline_commit}` is missing or `NO_VCS`, use best effort to determine what changed. Otherwise, construct `{diff_output}` covering all changes — tracked and untracked — since `{baseline_commit}`.

Do NOT `git add` anything — this is read-only inspection.

### Review

Launch three subagents with explicit `context: "fresh"` and no fork/resume. Fresh review prompts must include only the review task and explicitly named diff/spec/context artifacts; do not append parent conversation history, prior child output, or reviewer transcripts. If no sub-agents are available, generate three review prompt files in `{implementation_artifacts}` — one per reviewer role below — and HALT. Ask the human to run each in a separate session (ideally a different LLM) and paste back the findings. For any failed, timed-out, empty, or ambiguous review result, update that role's task to `blocked` or `failed` with `cause` and `recommendedNextAction` before continuing with completed independent review outputs.

- **Blind hunter** — receives `{diff_output}` only. No spec, no context docs, no project access. Invoke via the `bmad-review-adversarial-general` skill.
- **Edge case hunter** — receives `{diff_output}` and read access to the project. Invoke via the `bmad-review-edge-case-hunter` skill.
- **Acceptance auditor** — receives `{diff_output}`, `{spec_file}`, and read access to the project. Must also read the docs listed in `{spec_file}` frontmatter `context`. Checks for violations of acceptance criteria, rules, and principles from the spec and context docs.

### Classify

1. Deduplicate all review findings.
2. Classify each finding. The first three categories are **this story's problem** — caused or exposed by the current change. The last two are **not this story's problem**.
   - **intent_gap** — caused by the change; cannot be resolved from the spec because the captured intent is incomplete. Do not infer intent unless there is exactly one possible reading.
   - **bad_spec** — caused by the change, including direct deviations from spec. The spec should have been clear enough to prevent it. When in doubt between bad_spec and patch, prefer bad_spec — a spec-level fix is more likely to produce coherent code.
   - **patch** — caused by the change; trivially fixable without human input. Just part of the diff.
   - **defer** — pre-existing issue not caused by this story, surfaced incidentally by the review. Collect for later focused attention.
   - **reject** — noise. Drop silently. When unsure between defer and reject, prefer reject — only defer findings you are confident are real.
3. Process findings in cascading order. If intent_gap or bad_spec findings exist, they trigger a loopback — lower findings are moot since code will be re-derived. If neither exists, process patch and defer normally. Increment `{specLoopIteration}` on each loopback. If it exceeds 5, HALT and escalate to the human.
   - **intent_gap** — Root cause is inside `<frozen-after-approval>`. Revert code changes. Loop back to the human to resolve. Once resolved, read fully and follow `./step-02-plan.md` to re-run steps 2–4.
   - **bad_spec** — Root cause is outside `<frozen-after-approval>`. Before reverting code: extract KEEP instructions for positive preservation (what worked well and must survive re-derivation). Revert code changes. Read the `## Spec Change Log` in `{spec_file}` and strictly respect all logged constraints when amending the non-frozen sections that contain the root cause. Append a new change-log entry recording: the triggering finding, what was amended, the known-bad state avoided, and the KEEP instructions. Read fully and follow `./step-03-implement.md` to re-derive the code, then this step will run again.
   - **patch** — Auto-fix. These are the only findings that survive loopbacks.
   - **defer** — Append to `{deferred_work_file}`.
   - **reject** — Drop silently.

## NEXT

Read fully and follow `./step-05-present.md`

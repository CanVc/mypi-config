---
---

# Step 3: Implement

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- No push. No remote ops.
- Sequential execution only.
- Content inside `<frozen-after-approval>` in `{spec_file}` is read-only. Do not modify.
- Quick-dev implementation sub-agent launches are formal BMAD dispatches and MUST follow the centralized BMAD Session Policy: pass explicit `context: "fresh"`, allow no fork/resume, and keep delegated context artifact-first.
- **Task-State Gate:** Any implementation sub-agent/task launch MUST follow `.pi/skills/bmad-orchestrator/SKILL.md` `Task Routing and Task List State`. Maintain an orchestrator-managed task list in `{spec_file}`. before dispatch, validate context/dependencies and write the implementer task to `in-progress` with `activeAgentId`; after parent validation write it to `completed`, or to `blocked` or `failed` with `cause` and `recommendedNextAction`; do not dispatch dependent tasks after a blocked/failed task.

## PRECONDITION

Verify `{spec_file}` resolves to a non-empty path and the file exists on disk. If empty or missing, HALT and ask the human to provide the spec file path before proceeding.

## INSTRUCTIONS

### Session Policy Gate

Before changing `{spec_file}` status, capturing `baseline_commit`, or otherwise editing `{spec_file}`, decide whether implementation will be delegated to a sub-agent/task. If the intended implementation launch omits context, requests `context: "fork"`, or requests `action: "resume"`, HALT before editing `{spec_file}`. Report the requested implementer agent, requested mode, and violated policy.

If delegation is used, the dispatch MUST include explicit `context: "fresh"` and no fork/resume. The fresh implementation prompt must include only `{spec_file}` plus explicitly named context artifacts from the frontmatter `context:` list; it must not append parent conversation history, previous runtime transcript, child output history, or reviewer transcripts. If no sub-agents are available, implement directly after this gate.

### Baseline

Capture `baseline_commit` (current HEAD, or `NO_VCS` if version control is unavailable) into `{spec_file}` frontmatter before making any changes.

### Implement

Change `{spec_file}` status to `in-progress` in the frontmatter before starting implementation.

If `{spec_file}` has a non-empty `context:` list in its frontmatter, load those files before implementation begins. When handing to a sub-agent, include only those explicitly named context artifacts in the fresh sub-agent prompt.

Hand `{spec_file}` to a sub-agent/task with explicit `context: "fresh"` and no fork/resume, or implement directly when sub-agents are unavailable.

**Path formatting rule:** Any markdown links written into `{spec_file}` must use paths relative to `{spec_file}`'s directory so they are clickable in VS Code. Any file paths displayed in terminal/conversation output must use CWD-relative format with `:line` notation (e.g., `src/path/file.ts:42`) for terminal clickability. No leading `/` in either case.

### Self-Check

Before leaving this step, verify every task in the `## Tasks & Acceptance` section of `{spec_file}` is complete. Mark each finished task `[x]`. If any task is not done, finish it before proceeding.

## NEXT

Read fully and follow `./step-04-review.md`

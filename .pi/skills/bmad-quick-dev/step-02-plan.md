---
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
---

# Step 2: Plan

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- No intermediate approvals.
- Quick-dev planning investigation sub-agent/task launches are formal BMAD dispatches and MUST follow the centralized BMAD Session Policy: validate before dispatch and before any `{spec_file}` artifact write, pass explicit `context: "fresh"`, and allow no fork/resume.
- If a planning investigation launch request omits context, requests `context: "fork"`, or requests `action: "resume"`, HALT before dispatch and before writing `{spec_file}`. Report the requested investigation agent/task, requested mode, and violated policy.
- Fresh planning investigation prompts are artifact-first: include only the task text and explicitly named artifact paths/read directives; they must not append parent conversation history, previous runtime transcript, child output history, or reviewer transcripts.
- **Task-State Gate:** Any planning investigation sub-agent/task launch MUST follow `.pi/skills/bmad-orchestrator/SKILL.md` `Task Routing and Task List State`. Maintain an orchestrator-managed task list in `{spec_file}` when it exists, or in a named planning-run Markdown artifact under `{implementation_artifacts}` before `{spec_file}` is created. Before dispatch, validate context and write the task to `in-progress` with `activeAgentId`; after parent validation write it to `completed`, or to `blocked` or `failed` with `cause` and `recommendedNextAction`; do not dispatch dependent tasks after a blocked/failed task.

## INSTRUCTIONS

1. Draft resume check. If `{spec_file}` exists with `status: draft`, read it and capture the verbatim `<frozen-after-approval>...</frozen-after-approval>` block as `preserved_intent`. Otherwise `preserved_intent` is empty.

### Session Policy Gate

Before launching any investigation sub-agent/task or writing `{spec_file}`, decide whether planning investigation will be delegated to a sub-agent/task. If the intended investigation launch omits context, requests `context: "fork"`, or requests `action: "resume"`, HALT before dispatch and before writing `{spec_file}`. Report the requested investigation agent/task, requested mode, and violated policy.

If delegation is used, the dispatch MUST include explicit `context: "fresh"` and no fork/resume. The fresh investigation prompt must include only the task text and explicitly named artifact paths/read directives needed for investigation; it must not append parent conversation history, previous runtime transcript, child output history, or reviewer transcripts. If no sub-agents/tasks are available, investigate directly after this gate.

2. Investigate codebase. _Isolate deep exploration in sub-agents/tasks where available only after the Session Policy Gate passes. To prevent context snowballing, instruct subagents to give you distilled summaries only._
3. Read `./spec-template.md` fully. Fill it out based on the intent and investigation. If `{preserved_intent}` is non-empty, substitute it for the `<frozen-after-approval>` block in your filled spec before writing. Write the result to `{spec_file}` only after the Session Policy Gate has passed.
4. Self-review against READY FOR DEVELOPMENT standard.
5. If intent gaps exist, do not fantasize, do not leave open questions, HALT and ask the human.
6. Token count check (see SCOPE STANDARD). If spec exceeds 1600 tokens:
   - Show user the token count.
   - HALT and ask human: `[S] Split — carve off secondary goals` | `[K] Keep full spec — accept the risks`
   - On **S**: Propose the split — name each secondary goal. Append deferred goals to `{deferred_work_file}`. Rewrite the current spec to cover only the main goal — do not surgically carve sections out; regenerate the spec for the narrowed scope. Continue to checkpoint.
   - On **K**: Continue to checkpoint with full spec.

### CHECKPOINT 1

Present summary. Display the spec file path as a CWD-relative path (no leading `/`) so it is clickable in the terminal. If token count exceeded 1600 and user chose [K], include the token count and explain why it may be a problem.

After presenting the summary, display this note:

---

Before approving, you can open the spec file in an editor or ask me questions and tell me what to change. You can also use `bmad-advanced-elicitation`, `bmad-party-mode`, or `bmad-code-review` skills, ideally in another session to avoid context bloat.

---

HALT and ask human: `[A] Approve` | `[E] Edit`

- **A**: Re-read `{spec_file}` from disk.
  - **If the file is missing:** HALT. Tell the user the spec file is gone and STOP — do not write anything to `{spec_file}`, do not set status, do not proceed to Step 3. Nothing below this point runs.
  - **If the file exists:** Compare the content to what you wrote. If it has changed since you wrote it, acknowledge the external edits — show a brief summary of what changed — and proceed with the updated version. Then set status `ready-for-dev` in `{spec_file}`. Everything inside `<frozen-after-approval>` is now locked — only the human can change it. → Step 3.
- **E**: Apply changes, then return to CHECKPOINT 1.


## NEXT

Read fully and follow `./step-03-implement.md`

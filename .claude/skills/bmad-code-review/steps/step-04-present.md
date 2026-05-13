---
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
---

# Step 4: Present and Act

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- When `{spec_file}` is set, always write triaged findings to `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md` and linked action items to the story file before offering action choices. Only `{deferred_work_file}` remains global; story-specific review findings/artifacts must stay beside `{spec_file}` in that story folder.
- `decision-needed` findings must be resolved before handling `patch` findings.
- Every persisted or presented finding MUST include uppercase severity: `[HIGH]`, `[MEDIUM]`, or `[LOW]`.
- Next action is severity-aware: unresolved blocking `High` and blocking `Medium` findings require fix or human decision; `Low` findings are deferred by default and do not block story completion.

## INSTRUCTIONS

### 1. Clean review shortcut

If zero findings remain after triage (all dismissed or none raised): state that and proceed to section 6 (Sprint Status Update).

### 2. Write findings to the story file

If `{spec_file}` exists and contains a Tasks/Subtasks section, write review findings into the story file using the Senior Developer Review action-item syntax:

1. Ensure a `## Senior Developer Review (AI)` section exists, with a `### Action Items` subsection. Append findings there; do not use a separate `### Review Findings` subsection for BMAD story reviews.

2. Determine or reuse the review pass tag and findings artifact from Step 3:
   - Use `[R1]` for the first review pass on a story.
   - If the story already contains Senior Developer Review action items with `[R<number>]` tags, use the next number for newly appended findings (for example, existing `[R1]` items means this run writes `[R2]`).
   - Reuse the same `[R<number>]` tag for every finding from the same review run.
   - Do **not** write prose such as "Second-pass review" or "Second pass review" in the action-item text; the `[R<number>]` tag is the only pass marker.
   - Ensure each finding has a stable id `[F-R<number>-001]` and a source link to `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md#F-R<number>-001`.

3. Normalize action-item metadata:
   - Severity MUST be uppercase: `[HIGH]`, `[MEDIUM]`, or `[LOW]`.
   - AC metadata MUST be bracketed after severity, using the finding's AC/constraint references when available (for example `[AC3, AC7]`) or `[N/A]` when no AC applies.

4. Write all `### Action Items` findings in this order:

   - **`decision-needed`** findings (unchecked):
     `- [ ] [R<number>][<SEVERITY>][<AC refs or N/A>][F-R<number>-001] <Title> — decision needed: <Detail> — Source: `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md#F-R<number>-001``

   - **blocking `patch`** findings (unchecked):
     `- [ ] [R<number>][<SEVERITY>][<AC refs or N/A>][F-R<number>-001] <Title> [<file>:<line>] — Source: `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md#F-R<number>-001``

   - **`defer`** findings and non-blocking `Low` findings (checked off, marked deferred):
     `- [x] [R<number>][<SEVERITY>][<AC refs or N/A>][F-R<number>-001] <Title> [<file>:<line>] — deferred, <reason> — Source: `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md#F-R<number>-001``

5. For every unchecked `decision-needed` or blocking `patch` item, also add a matching unchecked task under `Tasks/Subtasks → ### Review Follow-ups (AI)` so `bmad-dev-story` can resume the work. Keep the dev follow-up marker first, then reuse the same review metadata and exact source link:
   `- [ ] [AI-Review][R<number>][<SEVERITY>][<AC refs or N/A>][F-R<number>-001] <Title/action> — Source: `{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md#F-R<number>-001``

Also append each `defer` finding and each non-blocking `Low` finding to `{deferred_work_file}` under a heading `## Deferred from: code review ({date})`. If `{spec_file}` is set, include its basename in the heading (e.g., `code review of story-3.3 (2026-03-18)`). One bullet per finding with uppercase severity, description, and defer reason.

### 3. Present summary

Announce what was written:

> **Code review complete.** <D> `decision-needed`, <P> blocking `patch`, <W> `defer`, <R> dismissed as noise. Severity: <H> High, <M> Medium, <L> Low.

If `{spec_file}` is set, add: `Findings written to {story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md and linked Senior Developer Review (AI) action items in {spec_file}.`
Otherwise add: `Findings are listed above. No story file was provided, so nothing was persisted.`

### 4. Resolve decision-needed findings

If `decision_needed` findings exist, present each one with its detail and the options available. The user must decide — the correct fix is ambiguous without their input. Walk through each finding (or batch related ones) and get the user's call. Once resolved, each becomes a `patch`, `defer`, or is dismissed.

If the user chooses to defer, ask: Quick one-line reason for deferring this item? (helps future reviews): — then append that reason to both the story file bullet and the `{deferred_work_file}` entry.

**HALT** — I am waiting for your numbered choice. Reply with only the number (or "0" for batch). Do not proceed until you select an option.

### 5. Handle `patch` findings

If blocking `patch` findings exist (including any resolved from step 4), HALT. Ask the user. If only `Low` findings remain, do not halt for fixes by default; defer them and proceed to section 6 unless the user explicitly asked to fix Low findings now.

If `{spec_file}` is set, present all three options (if >3 blocking `patch` findings exist, also show option 0):

> **How would you like to handle the <Z> blocking `patch` findings?**
> 0. **Batch-apply all** — automatically fix every non-controversial patch (recommended when there are many)
> 1. **Fix them automatically** — I will apply fixes now
> 2. **Leave as action items** — they are already in the story file
> 3. **Walk through each** — let me show details before deciding

If `{spec_file}` is **not** set, present only options 1 and 3 (omit option 2 — findings were not written to a file). If >3 blocking `patch` findings exist, also show option 0:

> **How would you like to handle the <Z> blocking `patch` findings?**
> 0. **Batch-apply all** — automatically fix every non-controversial patch (recommended when there are many)
> 1. **Fix them automatically** — I will apply fixes now
> 2. **Walk through each** — let me show details before deciding

**HALT** — I am waiting for your numbered choice. Reply with only the number (or "0" for batch). Do not proceed until you select an option.

- **Option 0** (only when >3 findings): Apply all non-controversial patches without per-finding confirmation. Skip any finding that requires judgment. Present a summary of changes made and any skipped findings.
- **Option 1**: Apply each fix. After all patches are applied, present a summary of changes made. If `{spec_file}` is set, check off the items in the story file.
- **Option 2** (only when `{spec_file}` is set): Done — findings are already written to the story.
- **Walk through each**: Present each finding with full detail, diff context, and suggested fix. After walkthrough, re-offer the applicable options above.

  **HALT** — I am waiting for your numbered choice. Reply with only the number (or "0" for batch). Do not proceed until you select an option.

**✅ Code review actions complete**

- Decision-needed resolved: <D>
- Patches handled: <P>
- Deferred: <W>
- Dismissed: <R>

### 6. Update story status and sync sprint tracking

Skip this section if `{spec_file}` is not set.

#### Determine new status based on review outcome

- If all `decision-needed`, `High`, and blocking `Medium` findings were resolved (fixed, dismissed, or explicitly deferred by the user) AND only `Low` or non-blocking deferred findings remain: set `{new_status}` = `done`. Update the story file Status section to `done`.
- If blocking `High`/`Medium` patch findings were left as action items, or unresolved `decision-needed` findings remain: set `{new_status}` = `in-progress`. Update the story file Status section to `in-progress`.
- Never keep a story blocked only because `Low` findings exist; record them in `{deferred_work_file}` and proceed.

Save the story file.

#### Sync sprint-status.yaml

If `{story_key}` is not set, skip this subsection and note that sprint status was not synced because no story key was available.

If `{sprint_status}` file exists:

1. Load the FULL `{sprint_status}` file.
2. Find the `development_status` entry matching `{story_key}`.
3. If found: update `development_status[{story_key}]` to `{new_status}`. Update `last_updated` to current date. Save the file, preserving ALL comments and structure including STATUS DEFINITIONS.
4. If `{story_key}` not found in sprint status: warn the user that the story file was updated but sprint-status sync failed.

If `{sprint_status}` file does not exist, note that story status was updated in the story file only.

#### Completion summary

> **Review Complete!**
>
> **Story Status:** `{new_status}`
> **Issues Fixed:** <fixed_count>
> **Action Items Created:** <action_count>
> **Deferred:** <W>
> **Dismissed:** <R>

### 7. Next steps

Present the user with follow-up options:

> **What would you like to do next?**
> 1. **Start the next story** — recommended when no blocking High/Medium findings remain, even if Low findings were deferred
> 2. **Fix blocking review findings** — recommended when unresolved High or blocking Medium findings remain
> 3. **Re-run code review** — recommended after fixes or when review layers failed
> 4. **Done** — end the workflow

**HALT** — I am waiting for your choice. Do not proceed until the user selects an option.

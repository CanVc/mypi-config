---
failed_layers: '' # set at runtime: comma-separated list of layers that failed or returned empty
---

# Step 2: Review

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- The Blind Hunter subagent receives NO project context — diff only.
- The Edge Case Hunter subagent receives diff and project read access.
- The Acceptance Auditor subagent receives diff, spec, and context docs.
- Every review subagent MUST attach a severity to each finding: `High`, `Medium`, or `Low`.
- **Task-State Gate:** Parallel review fan-out MUST follow `.pi/skills/bmad-orchestrator/SKILL.md` `Task Routing and Task List State`. Maintain an orchestrator-managed task list in the known story/spec/review Markdown artifact, or in a named review-run Markdown artifact under `{review_artifact_dir}` when no editable story/spec artifact exists. Before dispatch, create one task per review layer, validate dependencies/context, and write each selected task to `in-progress` with `activeAgentId`. After parent validation, write each layer task to `completed`, or to `blocked` or `failed` with `cause` and `recommendedNextAction`; do not dispatch dependent tasks or triage work that depends on a blocked/failed layer's output.
- Severity meanings:
  - `High` -- blocks completion: acceptance criteria violation, regression, data loss, security/privacy issue, or unsafe workflow state.
  - `Medium` -- potentially blocks completion if it affects acceptance criteria, security, regression risk, or maintainability needed now.
  - `Low` -- non-blocking polish, evidence quality, documentation, style, or future hardening.

## INSTRUCTIONS

1. If `{review_mode}` = `"no-spec"`, note to the user: "Acceptance Auditor skipped — no spec file provided."

2. Launch parallel subagents under the centralized BMAD Session Policy: review layers are always fresh, use explicit `context: "fresh"`, and allow no fork/resume. If a launch request omits context, requests `context: "fork"`, or requests `action: "resume"`, HALT before dispatch and report the requested reviewer role, requested mode, and violated policy. Fresh review prompts must include only the layer task plus explicitly named diff/spec/context artifacts; do not append parent conversation history, prior child output, or reviewer transcripts. If subagents are not available, generate prompt files in `{review_artifact_dir}` — one per reviewer role below — and HALT. When `{story_key}` is set, `{review_artifact_dir}` MUST be `{implementation_artifacts}/{story_key}` (not the legacy flat story file's parent directory), create that directory and its `reviews/` subdirectory before writing prompts, and use filenames under `reviews/` matching `{{story_id_dash}}-<reviewer-role>-prompt.md` so story-specific reviewer prompts stay inside the story artifact folder. If `{review_artifact_dir}` is empty and `{story_key}` is known, set it to `{implementation_artifacts}/{story_key}`; if `{review_artifact_dir}` is empty and no story is known, set it to the directory containing `{spec_file}`; if no spec/story is known, use `{implementation_artifacts}` only for no-spec review prompts. Ask the user to run each in a separate session (ideally a different LLM) and paste back the findings. When findings are pasted, resume from this point and proceed to step 3.

   Required dispatch shape for available subagents:

   ```ts
   subagent({
     tasks: [
       { agent: "reviewer-a", task: "Run Blind Hunter against the provided diff artifact/path only." },
       { agent: "reviewer-b", task: "Run Edge Case Hunter against the provided diff artifact/path and permitted project reads." },
       { agent: "reviewer-a", task: "When review_mode is full, run Acceptance Auditor against the diff plus explicit spec/context artifact paths." }
     ],
     context: "fresh",
     agentScope: "project"
   })
   ```

   - **Blind Hunter** — receives `{diff_output}` only. No spec, no context docs, no project access. Invoke via the `bmad-review-adversarial-general` skill. Require each finding to include `Severity: High|Medium|Low`.

   - **Edge Case Hunter** — receives `{diff_output}` and read access to the project. Invoke via the `bmad-review-edge-case-hunter` skill. Require each JSON finding to include a `severity` field with `High`, `Medium`, or `Low`.

   - **Acceptance Auditor** (only if `{review_mode}` = `"full"`) — receives `{diff_output}`, the content of the file at `{spec_file}`, and any loaded context docs. Its prompt:
     > You are an Acceptance Auditor. Review this diff against the spec and context docs. Check for: violations of acceptance criteria, deviations from spec intent, missing implementation of specified behavior, contradictions between spec constraints and actual code. Output findings as a Markdown list. Each finding: `Severity: High|Medium|Low`, one-line title, which AC/constraint it violates, and evidence from the diff.

3. **Subagent failure handling**: If any subagent fails, times out, or returns empty results, append the layer name to `{failed_layers}` (comma-separated), update that layer's orchestrator-managed task list entry to `blocked` or `failed` with `cause` and `recommendedNextAction`, and proceed only with findings from remaining `completed` independent layers. Do not dispatch dependent tasks or use the blocked/failed layer as context.

4. Collect all findings from the completed layers. If reviewer output files or manual command transcripts are persisted for a known story, ensure `{review_artifact_dir}` is `{implementation_artifacts}/{story_key}`, create `{review_artifact_dir}/reviews` if needed, and write raw layer outputs there using the current review round when known, e.g. `reviews/{{story_id_dash}}-R<number>-blind-hunter.md`, `reviews/{{story_id_dash}}-R<number>-edge-case-hunter.md`, and `reviews/{{story_id_dash}}-R<number>-acceptance-auditor.md`. In `/dev-cycle` reviewer A/B mode, use `reviews/{{story_id_dash}}-R<number>-reviewer-a.md` and `reviews/{{story_id_dash}}-R<number>-reviewer-b.md`. Do not write story-specific review artifacts directly at the implementation-artifacts root.


## NEXT

Read fully and follow `./step-03-triage.md`

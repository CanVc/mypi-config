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
- Severity meanings:
  - `High` -- blocks completion: acceptance criteria violation, regression, data loss, security/privacy issue, or unsafe workflow state.
  - `Medium` -- potentially blocks completion if it affects acceptance criteria, security, regression risk, or maintainability needed now.
  - `Low` -- non-blocking polish, evidence quality, documentation, style, or future hardening.

## INSTRUCTIONS

1. If `{review_mode}` = `"no-spec"`, note to the user: "Acceptance Auditor skipped — no spec file provided."

2. Launch parallel subagents without conversation context. If subagents are not available, generate prompt files in `{review_artifact_dir}` — one per reviewer role below — and HALT. When `{story_key}` is set, `{review_artifact_dir}` MUST be `{implementation_artifacts}/{story_key}` (not the legacy flat story file's parent directory), create that directory before writing prompts, and use filenames matching `review-{{story_key}}-<reviewer-role>-prompt.md` so story-specific reviewer prompts stay inside the story artifact folder. If `{review_artifact_dir}` is empty and `{story_key}` is known, set it to `{implementation_artifacts}/{story_key}`; if `{review_artifact_dir}` is empty and no story is known, set it to the directory containing `{spec_file}`; if no spec/story is known, use `{implementation_artifacts}` only for no-spec review prompts. Ask the user to run each in a separate session (ideally a different LLM) and paste back the findings. When findings are pasted, resume from this point and proceed to step 3.

   - **Blind Hunter** — receives `{diff_output}` only. No spec, no context docs, no project access. Invoke via the `bmad-review-adversarial-general` skill. Require each finding to include `Severity: High|Medium|Low`.

   - **Edge Case Hunter** — receives `{diff_output}` and read access to the project. Invoke via the `bmad-review-edge-case-hunter` skill. Require each JSON finding to include a `severity` field with `High`, `Medium`, or `Low`.

   - **Acceptance Auditor** (only if `{review_mode}` = `"full"`) — receives `{diff_output}`, the content of the file at `{spec_file}`, and any loaded context docs. Its prompt:
     > You are an Acceptance Auditor. Review this diff against the spec and context docs. Check for: violations of acceptance criteria, deviations from spec intent, missing implementation of specified behavior, contradictions between spec constraints and actual code. Output findings as a Markdown list. Each finding: `Severity: High|Medium|Low`, one-line title, which AC/constraint it violates, and evidence from the diff.

3. **Subagent failure handling**: If any subagent fails, times out, or returns empty results, append the layer name to `{failed_layers}` (comma-separated) and proceed with findings from the remaining layers.

4. Collect all findings from the completed layers. If reviewer output files or manual command transcripts are persisted for a known story, ensure `{review_artifact_dir}` is `{implementation_artifacts}/{story_key}`, create that directory if needed, and write them there using `review-{{story_key}}-<reviewer-role>-output.md`; do not write story-specific review artifacts directly at the implementation-artifacts root.


## NEXT

Read fully and follow `./step-03-triage.md`

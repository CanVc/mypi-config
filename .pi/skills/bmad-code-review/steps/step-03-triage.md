---
---

# Step 3: Triage

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- Be precise. When uncertain between categories, prefer the more conservative classification.

## INSTRUCTIONS

1. **Normalize** findings into a common format. Expected input formats:
   - Adversarial (Blind Hunter): markdown list of descriptions, each with `Severity: High|Medium|Low`
   - Edge Case Hunter: JSON array with `severity`, `location`, `trigger_condition`, `guard_snippet`, `potential_consequence` fields
   - Acceptance Auditor: markdown list with `Severity: High|Medium|Low`, title, AC/constraint reference, and evidence

   If a layer's output does not match its expected format, attempt best-effort parsing. Note any parsing issues for the user.

   Convert all to a unified list where each finding has:
   - `id` -- sequential integer
   - `findingId` -- stable round-scoped id in the format `F-R<number>-001`, assigned after the review round is known
   - `source` -- `blind`, `edge`, `auditor`, `reviewer-a`, `reviewer-b`, or merged sources (e.g., `blind+edge`)
   - `title` -- one-line summary
   - `severity` -- exactly one of `High`, `Medium`, or `Low`
   - `classification` -- one of `implementation-issue`, `test-issue`, `spec-ambiguity`, `artifact-invalid`, `retry-limit-reached`, `environment-blocked`, `workflow-contract-violation`
   - `blocking` -- boolean after severity-aware classification
   - `detail` -- full description
   - `location` -- file and line reference (if available)
   - `requiredFix` -- actionable implementation guidance when fixable
   - `validationRequirements` -- required validation evidence
   - `outOfScope` -- what must not be changed while fixing

   If a finding lacks severity, assign `Medium` by default and note the missing severity in the parsing issues. Do not allow a finding to proceed without an explicit or assigned severity.

2. **Deduplicate.** If two or more findings describe the same issue, merge them into one:
   - Use the most specific finding as the base (prefer edge-case JSON with location over adversarial prose).
   - Append any unique detail, reasoning, or location references from the other finding(s) into the surviving `detail` field.
   - Set `source` to the merged sources (e.g., `blind+edge`).
   - Set `severity` to the highest severity among merged findings unless evidence clearly supports lowering it; if lowered, preserve the reason in `detail`.

3. **Classify** each finding into exactly one bucket and preserve severity:
   - **decision_needed** -- There is an ambiguous choice that requires human input. The code cannot be correctly patched without knowing the user's intent. Only possible if `{review_mode}` = `"full"`.
   - **patch** -- Current-change issue that is fixable without human input. The correct fix is unambiguous.
   - **defer** -- Pre-existing issue, future hardening, documentation/evidence quality, or non-blocking improvement not required to satisfy this story now.
   - **dismiss** -- Noise, false positive, or handled elsewhere.

   Severity-aware classification rules:
   - `High` findings are blocking unless dismissed as false positives. Prefer `patch` or `decision_needed`.
   - `Medium` findings block only when tied to acceptance criteria, security/privacy, data loss, regression risk, or required maintainability for this story; otherwise classify as `defer` with a reason.
   - `Low` findings are non-blocking by default. Classify as `defer` unless the user explicitly asks to fix polish/hardening now.
   - If only `Low` findings remain after triage, the review is not clean, but it does not block story completion; record them as deferred future work.

   If `{review_mode}` = `"no-spec"` and a finding would otherwise be `decision_needed`, reclassify it as `patch` (if the fix is unambiguous and severity is `High` or blocking `Medium`) or `defer` (if not).

4. **Drop** all `dismiss` findings. Record the dismiss count for the summary.

5. Compute severity counts for all non-dismissed findings: `<H>` High, `<M>` Medium, `<L>` Low. Also compute blocking counts: blocking `High` + blocking `Medium` + unresolved `decision_needed`.

6. If `{failed_layers}` is non-empty, report which layers failed before announcing results. If zero findings remain after dropping dismissed AND `{failed_layers}` is non-empty, warn the user that the review may be incomplete rather than announcing a clean review.

7. If zero findings remain after triage (all rejected or none raised): state "✅ Clean review — all layers passed." (Step 3 already warned if any review layers failed via `{failed_layers}`.)

8. If findings remain but all are `Low` deferred findings, state "ℹ️ Non-blocking review findings only — Low severity items will be deferred unless the user asks to fix them now."

9. Determine the review pass tag for this run before persistence:
   - Use `R1` for the first review pass on a story.
   - If the story already contains Senior Developer Review action items with `[R<number>]` tags, use the next number.
   - Reuse the same `R<number>` for every finding in this review run.

10. If `{spec_file}` is set for a BMAD story, create `{review_artifact_dir}/{story_id_dash}-reviews` if needed and write the triaged findings artifact before story action items are written:

   ```text
   {review_artifact_dir}/{story_id_dash}-reviews/{story_id_dash}-R<number>-findings.md
   ```

   Required artifact shape:

   ```md
   # {story_id_dash} R<number> Findings

   ## Summary
   Verdict: PASS | CHANGES_REQUESTED | BLOCKED
   Blocking findings: <count>

   Source reviews:
   - `{story_id_dash}-reviews/<raw-review-file>.md`

   ## Findings

   ### F-R<number>-001
   Status: open  
   Severity: HIGH  
   Classification: implementation-issue  
   Blocking: true  
   AC/Constraint: AC3  
   Location: `path:line`  
   Sources:
   - `{story_id_dash}-reviews/<raw-review-file>.md`

   #### Problem
   ...

   #### Required Fix
   ...

   #### Validation Requirements
   ...

   #### Out of Scope
   ...
   ```

11. Store the findings artifact path and each finding anchor for Step 4. Step 4 must link story action items to these exact anchors; do not copy full raw review prose into the story.


## NEXT

Read fully and follow `./step-04-present.md`

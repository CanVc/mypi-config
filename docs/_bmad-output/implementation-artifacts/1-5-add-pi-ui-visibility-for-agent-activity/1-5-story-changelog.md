# Story 1.5 Changelog and Historical Notes

This artifact preserves story history that was previously embedded in the legacy story file.

## Change Log

- Addressed code review findings - 4 items resolved (Date: 2026-05-13): role labels for inactive durable tasks, durable task identity propagation, missing `taskStatePath` degraded BMAD UI, and required `contextSource` validation.
- Addressed code review findings - 4 items resolved (Date: 2026-05-13): foreground single-run terminal-title durable identity, durable-status gating for runtime widget rows, async job-level `durableTaskIds` activity-title matching, and missing-`taskStatePath` degraded rendering for async BMAD jobs.
- Addressed code review findings - 3 items resolved (Date: 2026-05-13): clean-install Story 1.5 patch durability, foreground terminal-title lifecycle coverage, and async durable-status terminal-title gating.
- Addressed code review findings - 2 items resolved (Date: 2026-05-13): async multi-job active bucketing/header durable-status gating and missing/unreadable `taskStatePath` async terminal-title clearing.
- Amended story design requirement (Date: 2026-05-13): added explicit central runtime/durable arbitration requirement after R1-R5 reviews showed per-surface fixes were insufficient.
- Targeted remediation completed (Date: 2026-05-13): centralized durable/runtime arbitration, resolved remaining R5 foreground-title and async status-output findings, regenerated Story 1.5 package patch, and validated focused/full regression commands.
- Targeted remediation hardening (Date: 2026-05-13): extended async status list/detail durable arbitration to job-level `durableTaskIds` before step records exist, regenerated the package patch, and revalidated clean restore/full regression.
- Targeted remediation hardening (Date: 2026-05-13): broadened central arbitration same-agent durable-terminal fallback for foreground titles without per-progress durable ids and revalidated clean restore/full regression.

## Completion Notes List

- Defined the v1 Pi UI visibility contract in BMAD orchestrator guidance, including Pi TUI/`pi-subagents` as the UI boundary, read-only Markdown task truth, role labels, task-state vocabulary, degraded rendering, and terminal-title rules.
- Extended `pi-subagents` UI/status surfaces with generic `roleLabel` propagation/fallback, durable Markdown task-state parsing/projection, activity-title formatting, stale-active prevention for completed/blocked/failed durable tasks, and safe degraded warnings.
- Added `taskStatePath` support so BMAD parent workflows can expose the current story/spec/run Markdown artifact to the Pi UI without hidden runtime truth or duplicate dispatch.
- Added terminal-title updates for active foreground/background subagent activity and cleanup on completion, session shutdown, and extension reload.
- Captured all `pi-subagents` package-source changes in `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch`; updated patch application idempotency for the prior display patch after Story 1.5 superseding edits.
- Added provider-free regression coverage for UI contract boundaries, role-label fallback, activity-title formatting/noise stripping, durable task projection, stale-state prevention, degraded states, preserved widget facts, patch durability, and dispatch guardrails.
- ✅ Resolved review finding [HIGH]: Load and use configured role labels for inactive/pending/completed/blocked/failed durable tasks.
- ✅ Resolved review finding [HIGH]: Carry durable task identity through runtime progress/status/results so parallel same-agent activity titles map to the correct task.
- ✅ Resolved review finding [MEDIUM]: Render degraded BMAD UI when a BMAD/team view is expected but `taskStatePath` is missing.
- ✅ Resolved review finding [MEDIUM]: Treat durable task records missing required `contextSource` as malformed/degraded, not completed/successful.
- ✅ Resolved review finding [HIGH]: Preserve `taskStatePath` and durable task identity for foreground single-run terminal titles; `durableTaskId` is now used as the fallback activity-title task id when durable state is unavailable.
- ✅ Resolved review finding [HIGH]: Gate BMAD runtime widget row glyphs/status labels through durable status so completed/blocked/failed durable tasks do not render active despite runtime `running`.
- ✅ Resolved review finding [HIGH]: Use async job-level `durableTaskIds` when building activity titles before per-step records exist.
- ✅ Resolved review finding [MEDIUM]: Treat non-empty async `durableTaskIds` as BMAD projection evidence and render degraded UI when `taskStatePath` is missing.
- ✅ Resolved review finding [HIGH]: Regenerated the Story 1.5 patch relative to prior required patches so clean install applies durably without duplicating `src/agents/agents.ts` hunks.
- ✅ Resolved review finding [HIGH]: Added foreground terminal title lifecycle coverage for progress/result updates using durable task titles and cleanup on terminal states.
- ✅ Resolved review finding [HIGH]: Gated async terminal title selection through durable task status so terminal durable tasks clear/restore the title instead of showing stale runtime activity.
- ✅ Resolved review finding [HIGH]: Gated async multi-job active bucketing/header state through durable terminal status so terminal durable work is counted as finished rather than active.
- ✅ Resolved review finding [MEDIUM]: Cleared async terminal titles instead of falling back to normal runtime activity when durable task IDs exist without a readable `taskStatePath`.
- Implemented a centrally testable durable-vs-runtime arbitration policy in `shared/ui-visibility.ts` and refactored title/widget/status paths to use the shared durable-terminal/degraded-state decisions.
- ✅ Resolved review finding [HIGH]: Foreground terminal title ownership now clears instead of showing normal runtime activity when matched durable task IDs are `completed`, `blocked`, or `failed`.
- ✅ Resolved review finding [MEDIUM]: Async `subagent({ action: "status" })` list/detail output now applies durable-status arbitration, hides durable-terminal work from active listings, and emits degraded BMAD warnings for missing/unreadable/malformed task state.
- Regenerated `.pi/patches/pi-subagents-0.24.2-ui-visibility-agent-activity.patch` after package source changes and validated both idempotent `--patch` and clean package restore application.
- Extended async status list/detail arbitration to job-level `durableTaskIds` when status files have durable IDs before step records, so durable-terminal jobs are not listed active and missing task-state jobs show degraded warnings.
- Regenerated the Story 1.5 patch again after job-level async status source changes and validated clean restore plus full regression commands.
- Broadened the central arbitration helper to use same-agent durable status as a safety fallback when runtime progress has a `taskStatePath` but no durable task id, preventing normal foreground titles for durable-terminal BMAD tasks.

## Create-Story Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Saved Questions / Clarifications

- No user clarification required before development starts. Key implementation decision during dev: whether the existing `pi-subagents` UI/status renderer can be extended with a durable patch, or whether a small project-local Pi extension is narrower for the task-list projection. In either case, durable Markdown task truth must remain authoritative.

## Migrated Historical Analysis Artifacts

- Preimplementation scout analysis: `1-5-remediation/1-5-preimplementation-scout-analysis.md`
- Preimplementation reviewer risk analysis: `1-5-remediation/1-5-preimplementation-reviewer-risk-analysis.md`

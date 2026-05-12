# Deferred Work

## Deferred from: code review of 1-1-implement-the-generic-sub-agent-dispatch-tool (2026-05-11)

- Artifact/status reference contract placement belongs to later scaffold/workflow stories — not required for Story 1.1. Placement agreed: placeholders in Story 2.1, minimal standard-workflow semantics in Story 3.1/3.3 if needed, and full TDD artifact/status semantics in Story 4.2/4.7.

## Deferred from: code review pass 3 of 1-1-implement-the-generic-sub-agent-dispatch-tool (2026-05-11)

- [Low] Parent guidance should explicitly verify `subagent` is listed/active before delegation and HALT without state updates if unavailable — deferred as non-blocking orchestration hardening.
- [Medium] Artifact-path validation should constrain resolved paths to approved BMAD artifact roots, not only readability — deferred as security/process hardening beyond Story 1.1's initial dispatch substrate scope.
- [Low] Live child dispatch identity evidence should include `agentScope`, `context`, and `taskSource` consistently — deferred as evidence-quality hardening; current AC3 fallback evidence is sufficient for Story 1.1.

## Deferred from: code review round 3 of 1-2-add-agent-definitions-and-model-routing-contract (2026-05-12)

- [Low] Smoke-management checklist/evidence detail should be reconciled in the story artifact — deferred as non-blocking evidence/bookkeeping polish; unresolved Medium findings already block completion.

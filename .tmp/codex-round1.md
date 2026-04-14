Yes — I agree with this structure. It keeps `story.md` clean and consolidates orchestration into `test-plan.md`.

One small change: add a lightweight traceability header in each batch file (story/AC IDs).  
Why: you keep auditability after dropping `orchestrator-log.md` without adding noise.

`batch-XX.md` (headers only):

```markdown
# Batch XX — <Short Name>
## Metadata
## Story Traceability
## Preconditions
## Test Spec
## Red Gate
## Dev
## Green Gate
## Batch Outcome
## Next-Step Handoff
```
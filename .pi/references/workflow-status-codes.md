# BMAD Workflow Status Codes Reference

**Status:** Active project-local contract  
**Updated:** 2026-05-13 22:30

This reference defines fixed workflow status vocabularies for project-local BMAD-compatible workflows.

## 1. Story status values

Use the existing sprint/story lifecycle values:

```text
backlog
ready-for-dev
in-progress
review
done
blocked
```

Rules:

- `ready-for-dev`: story artifact exists and can be implemented.
- `in-progress`: implementation or review remediation is active, or blocking findings remain.
- `review`: implementation is complete and ready for review.
- `done`: no unresolved blocking High/Medium or decision-needed findings remain.
- `blocked`: human/environment/workflow issue prevents safe continuation.

## 2. Orchestrator task statuses

Use this closed set in durable task-state Markdown artifacts:

```text
pending
in-progress
completed
blocked
failed
```

Meanings:

- `pending`: task exists but has not been dispatched yet.
- `in-progress`: parent selected the task, wrote durable state, and dispatched or is awaiting the child agent.
- `completed`: child completed and parent validation accepted the result/artifact state.
- `blocked`: automatic continuation is unsafe but may be recoverable by human action or explicit retry policy.
- `failed`: task execution failed in a way that ends the current automated run.

Runtime/package statuses such as `running`, `complete`, `paused`, or `detached` are control-plane details and must be mapped to this vocabulary before durable state is written.

## 3. Finding severities

Reviewer findings use:

```text
High
Medium
Low
```

Persisted story tags use uppercase:

```text
[HIGH]
[MEDIUM]
[LOW]
```

Blocking rules:

- `High`: blocking unless dismissed as false positive.
- `Medium`: blocking when tied to acceptance criteria, security/privacy, data loss, regression risk, required maintainability, or workflow correctness.
- `Low`: non-blocking by default; defer unless the user explicitly asks to fix it now.

## 4. Finding statuses

Use this closed set in `<story_id>-reviews/<story_id>-R<n>-findings.md`:

```text
open
implemented
verified
deferred
dismissed
reopened
```

Meanings:

- `open`: unresolved and available for implementation or decision.
- `implemented`: dev implemented the fix, but reviewer verification is not yet complete.
- `verified`: reviewer or parent verification accepted the fix.
- `deferred`: intentionally not blocking the current story.
- `dismissed`: false positive or no longer applicable.
- `reopened`: previously implemented/verified but found unresolved in a later pass.

Current v1 checkbox behavior remains: `/dev-story` checks both the dev follow-up and corresponding review action item when it implements a fix. The stricter `implemented -> verified` distinction is available in the findings artifact for future review enforcement.

## 5. Review classifications

Use these canonical classification codes when triaging findings:

```text
implementation-issue
test-issue
spec-ambiguity
artifact-invalid
retry-limit-reached
environment-blocked
workflow-contract-violation
```

Meanings:

- `implementation-issue`: code/artifact implementation does not satisfy the current story or required workflow behavior.
- `test-issue`: tests are missing, invalid, misleading, or fail for the wrong reason.
- `spec-ambiguity`: the correct fix requires human/product/architecture clarification.
- `artifact-invalid`: required artifact is missing, malformed, contradictory, or not parseable enough for safe continuation.
- `retry-limit-reached`: configured iteration/retry cap has been hit.
- `environment-blocked`: local environment prevents validation or implementation.
- `workflow-contract-violation`: artifact state contradicts the allowed workflow model and cannot be trusted for automatic continuation.

## 6. Dev-cycle max iteration policy

`/dev-cycle` accepts an optional max iteration argument:

```text
/dev-cycle <story-folder-or-story-file> [maxIterations]
```

Rules:

- omitted value defaults to `5`;
- accepted range is `1..5`;
- invalid values fail closed before dispatch;
- selected value is recorded in `<story_id>-cycle-state.md` and `<story_id>-orchestrator-log.md`.

## 7. Fail-closed conditions

Formal workflows must halt rather than guess when they encounter:

- missing or unreadable story file;
- missing `Source:` link on a new unchecked `[AI-Review]` item;
- missing referenced `*-findings.md` file;
- missing finding anchor;
- malformed finding record;
- missing/unreadable dispatch context path;
- forbidden non-fresh formal BMAD dispatch;
- unclassifiable reviewer output;
- unsafe or contradictory artifact state.

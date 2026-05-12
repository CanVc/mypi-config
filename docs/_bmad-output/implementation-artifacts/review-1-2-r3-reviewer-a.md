Verdict: Changes Requested

Severity counts: High 0, Medium 3, Low 1

Findings:

ID: R3-A-1
Severity: Medium
Bucket: Runtime validation / durability from tracked sources
Title: Runtime integration tests can pass without exercising pi-subagents when ignored install output is absent
Location: `tests/test_agent_definitions_model_routing.py:135-137`, `tests/test_agent_definitions_model_routing.py:680-682`, `tests/test_agent_definitions_model_routing.py:996-1000`, `.pi/npm/.gitignore:1`
Evidence: The runtime gate is only `PI_SUBAGENTS_SRC.exists()` and runtime test classes call `skipTest(...)` when `.pi/npm/node_modules/pi-subagents/src/agents/agents.ts` is missing. The patch-applied assertion also skips if the installed source is absent. The installed runtime is ignored (`git check-ignore -v .pi/npm/node_modules/pi-subagents/src/agents/agents.ts` returned `.pi/npm/.gitignore:1:*`). Therefore a clean checkout from tracked sources can report the unittest suite as OK while skipping the actual provider-free runtime/discovery/precedence tests that are central to AC5/AC6/AC7 and R3.
AC/Constraint impacted: AC5, AC6, AC7; R3 focus on real runtime tests and durability from tracked sources.
Recommended action: Make runtime validation fail closed when the required runtime is absent, or have the test/validation harness restore the tracked package path via `.pi/install-packages.sh` before runtime tests. Assert that runtime tests were executed (not skipped) in the final validation path.

ID: R3-A-2
Severity: Medium
Bucket: Package pinning / patch durability
Title: Tracked installer floats the package version and patch application fails open on version mismatch
Location: `.pi/install-packages.sh:57-67`, `.pi/patches/apply-patches.sh:57-64`, `.pi/npm/package.json:3-5`
Evidence: `.pi/settings.json` pins `npm:pi-subagents@0.24.2`, but the tracked installer converts that to `"pi-subagents": "^0.24.2"` (`deps[name] = '^' + version`). The generated ignored `.pi/npm/package.json` currently contains the same semver range. If npm resolves a newer compatible version, the committed `pi-subagents-0.24.2-...patch` may no longer match. `apply-patches.sh` then prints `SKIP ... (patch does not apply cleanly — may already be applied or version mismatch)` and continues successfully instead of failing closed.
AC/Constraint impacted: AC2, AC3, AC5, AC6, AC9; architecture/package constraint that the approved pinned runtime or replacement pin be durable from tracked sources.
Recommended action: Preserve the exact version from `.pi/settings.json` in generated package metadata (no caret), verify the installed package version before patching, and make patch mismatch/version mismatch a non-zero failure unless the script can positively detect that the required patch is already applied. Add a clean-restore validation asserting exact `0.24.2` plus patched discovery/override behavior.

ID: R3-A-3
Severity: Medium
Bucket: Invalid-model validation
Title: AC9 is not fail-closed: missing required models are discovered/omitted rather than blocked with an actionable agent error
Location: `tests/test_agent_definitions_model_routing.py:684-698`, `tests/test_agent_definitions_model_routing.py:887-927`, `.pi/npm/node_modules/pi-subagents/src/runs/shared/pi-args.ts:67-70`, `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:66`, `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:275`
Evidence: The runtime invalid-model test explicitly asserts an agent without `model` is still discovered and simply has no `model` key. The static invalid-model tests only parse missing/empty model fields or an override without `model`; they do not assert a validation failure, dispatch block, agent ID in the error, or required fix text. Runtime argument building only appends `--model` when a model is present, so an undefined model falls through to default runtime behavior rather than being blocked by this story’s contract. The story checklist marks “fails closed with the agent ID and required fix” complete, but the Completion Notes describe only detection/undefined output.
AC/Constraint impacted: AC9; fail-closed validation constraint.
Recommended action: Add a provider-free dispatch/smoke validation path that treats wrapper-agent model as required, fails for missing/empty/unknown model assignments or invalid override models, and emits an actionable error naming the agent/override and required fix. Cover this with tests that assert the error content.

ID: R3-A-4
Severity: Low
Bucket: Story bookkeeping / smoke evidence
Title: Required smoke-management subtasks remain unchecked despite review status and claimed management evidence
Location: `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:68-74`, `docs/_bmad-output/implementation-artifacts/1-2-add-agent-definitions-and-model-routing-contract.md:283-289`
Evidence: The story is in review and “Perform smoke validation and record evidence” is checked, but the subtasks for `PI_TELEMETRY=0 pi list`, project agent list/get evidence, provider block capture, and live/blocked dispatch evidence remain unchecked. Completion Notes claim static/management evidence is complete, but the task checklist does not reflect that evidence.
AC/Constraint impacted: Smoke validation bookkeeping for AC4, AC7, AC8, AC9; R3 focus on sprint/story bookkeeping.
Recommended action: Reconcile the allowed story sections: either check and record the completed management evidence with command output references, or leave the parent task unchecked and explicitly document which smoke steps are blocked and why.

Validation run:

- `git status --short --untracked-files=all` — non-empty diff confirmed; includes modified `.pi/settings.json`, story, sprint status, and untracked `.pi/agents/*`, `.pi/install-packages.sh`, `.pi/patches/*`, review artifacts, and `tests/test_agent_definitions_model_routing.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` — PASS, 79 tests in 8.410s.
- `PI_TELEMETRY=0 pi list` — PASS; project package shows `npm:pi-subagents@0.24.2` loaded from `/home/cvc/dev/mypi-config/.pi/npm/node_modules/pi-subagents`.
- `PI_TELEMETRY=0 pi --list-models || true` — model registry available; committed models `zai/glm-5.1`, `openai-codex/gpt-5.1`, and `openai-codex/gpt-5.5` appear in output.
- `npx tsx` direct `discoverAgentsAll` probe with absolute import — PASS; project agents were exactly `implementer`, `reviewer-a`, `reviewer-b` with models `zai/glm-5.1`, `openai-codex/gpt-5.1`, `openai-codex/gpt-5.5`; builtin `reviewer` showed project override `openai-codex/gpt-5.5`.
- `find . \( -name '__pycache__' -o -name '*.pyc' -o -name '*.pyo' \) -print` — no bytecode output.
- `git check-ignore -v .pi/npm/node_modules/pi-subagents/src/agents/agents.ts .pi/npm/package.json .pi/npm/package-lock.json` — confirms runtime install output is ignored/local evidence only.
- Clean restore/install was not executed because it would mutate ignored `.pi/npm/` state during this review-only pass.
